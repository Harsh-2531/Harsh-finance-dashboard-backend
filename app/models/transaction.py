from sqlalchemy import Column, Integer, String, Float, Date, Enum, Text, ForeignKey
from app.database import Base
import enum

class TypeEnum(str, enum.Enum):
    income = "income"
    expense = "expense"

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    type = Column(Enum(TypeEnum), nullable=False)
    category = Column(String(100), nullable=False)
    date = Column(Date, nullable=False)
    notes = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"))