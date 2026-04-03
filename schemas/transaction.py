from pydantic import BaseModel
from enum import Enum
from datetime import date
from typing import Optional

class TypeEnum(str, Enum):
    income = "income"
    expense = "expense"

class TransactionCreate(BaseModel):
    amount: float
    type: TypeEnum
    category: str
    date: date
    notes: Optional[str] = None

class TransactionOut(TransactionCreate):
    id: int
    created_by: int

    class Config:
        from_attributes = True

class TransactionUpdate(BaseModel):
    amount: Optional[float]
    type: Optional[TypeEnum]
    category: Optional[str]
    date: Optional[date]
    notes: Optional[str]