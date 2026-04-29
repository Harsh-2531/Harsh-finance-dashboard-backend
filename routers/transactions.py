from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionOut, TransactionUpdate
from app.services.access_control import require_role, get_current_user
from typing import Optional
from datetime import date
from prometheus_client import Counter

router = APIRouter(prefix="/transactions", tags=["Transactions"])

# Custom Prometheus metrics
transaction_counter = Counter(
    "finance_transactions_total",
    "Total number of transactions created",
    ["type", "category"]
)

transaction_errors = Counter(
    "finance_transaction_errors_total",
    "Total failed transaction operations"
)

transaction_deletes = Counter(
    "finance_transaction_deletes_total",
    "Total number of transactions deleted"
)

transaction_updates = Counter(
    "finance_transaction_updates_total",
    "Total number of transactions updated"
)


@router.post("/", response_model=TransactionOut)
def create(data: TransactionCreate, db: Session = Depends(get_db),
           user=Depends(require_role("admin"))):
    try:
        tx = Transaction(**data.dict(), created_by=user.id)
        db.add(tx)
        db.commit()
        db.refresh(tx)
        transaction_counter.labels(
            type=data.type,
            category=data.category
        ).inc()
        return tx
    except Exception as e:
        transaction_errors.inc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=list[TransactionOut])
def list_transactions(
    type: Optional[str] = None,
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin", "analyst", "viewer"))
):
    try:
        q = db.query(Transaction)
        if type: q = q.filter(Transaction.type == type)
        if category: q = q.filter(Transaction.category == category)
        if start_date: q = q.filter(Transaction.date >= start_date)
        if end_date: q = q.filter(Transaction.date <= end_date)
        return q.all()
    except Exception as e:
        transaction_errors.inc()
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{tx_id}", response_model=TransactionOut)
def update(tx_id: int, data: TransactionUpdate, db: Session = Depends(get_db),
           _=Depends(require_role("admin"))):
    try:
        tx = db.query(Transaction).filter(Transaction.id == tx_id).first()
        if not tx:
            raise HTTPException(status_code=404, detail="Not found")
        for k, v in data.dict(exclude_none=True).items():
            setattr(tx, k, v)
        db.commit()
        db.refresh(tx)
        transaction_updates.inc()
        return tx
    except HTTPException:
        raise
    except Exception as e:
        transaction_errors.inc()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{tx_id}")
def delete(tx_id: int, db: Session = Depends(get_db), _=Depends(require_role("admin"))):
    try:
        tx = db.query(Transaction).filter(Transaction.id == tx_id).first()
        if not tx:
            raise HTTPException(status_code=404, detail="Not found")
        db.delete(tx)
        db.commit()
        transaction_deletes.inc()
        return {"message": "Deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        transaction_errors.inc()
        raise HTTPException(status_code=500, detail=str(e))