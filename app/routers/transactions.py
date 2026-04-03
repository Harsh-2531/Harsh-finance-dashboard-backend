from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionOut, TransactionUpdate
from app.services.access_control import require_role
from typing import Optional
from datetime import date

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/", response_model=TransactionOut)
def create(data: TransactionCreate, db: Session = Depends(get_db),
           user=Depends(require_role("admin"))):
    tx = Transaction(**data.dict(), created_by=user.id)
    db.add(tx)
    db.commit()
    db.refresh(tx)
    return tx

@router.get("/", response_model=list[TransactionOut])
def list_transactions(
    type: Optional[str] = None,
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    user=Depends(require_role("admin", "analyst", "viewer"))
):
    q = db.query(Transaction)
    if type: q = q.filter(Transaction.type == type)
    if category: q = q.filter(Transaction.category == category)
    if start_date: q = q.filter(Transaction.date >= start_date)
    if end_date: q = q.filter(Transaction.date <= end_date)
    return q.all()

@router.patch("/{tx_id}", response_model=TransactionOut)
def update(tx_id: int, data: TransactionUpdate, db: Session = Depends(get_db),
           _=Depends(require_role("admin"))):
    tx = db.query(Transaction).filter(Transaction.id == tx_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Not found")
    for k, v in data.dict(exclude_none=True).items():
        setattr(tx, k, v)
    db.commit()
    db.refresh(tx)
    return tx

@router.delete("/{tx_id}")
def delete(tx_id: int, db: Session = Depends(get_db),
           _=Depends(require_role("admin"))):
    tx = db.query(Transaction).filter(Transaction.id == tx_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(tx)
    db.commit()
    return {"message": "Deleted successfully"}