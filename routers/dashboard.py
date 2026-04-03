from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.transaction import Transaction, TypeEnum
from app.services.access_control import require_role

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary")
def summary(db: Session = Depends(get_db), _=Depends(require_role("admin", "analyst", "viewer"))):
    income = db.query(func.sum(Transaction.amount)).filter(Transaction.type == TypeEnum.income).scalar() or 0
    expense = db.query(func.sum(Transaction.amount)).filter(Transaction.type == TypeEnum.expense).scalar() or 0
    return {"total_income": income, "total_expenses": expense, "net_balance": income - expense}

@router.get("/by-category")
def by_category(db: Session = Depends(get_db), _=Depends(require_role("admin", "analyst"))):
    results = db.query(Transaction.category, func.sum(Transaction.amount))\
                .group_by(Transaction.category).all()
    return [{"category": r[0], "total": r[1]} for r in results]

@router.get("/recent")
def recent(db: Session = Depends(get_db), _=Depends(require_role("admin", "analyst", "viewer"))):
    return db.query(Transaction).order_by(Transaction.date.desc()).limit(10).all()

@router.get("/monthly-trends")
def monthly_trends(db: Session = Depends(get_db), _=Depends(require_role("admin", "analyst"))):
    results = db.query(
        func.month(Transaction.date).label("month"),
        func.year(Transaction.date).label("year"),
        Transaction.type,
        func.sum(Transaction.amount)
    ).group_by("year", "month", Transaction.type).order_by("year", "month").all()
    return [{"year": r[1], "month": r[0], "type": r[2], "total": r[3]} for r in results]