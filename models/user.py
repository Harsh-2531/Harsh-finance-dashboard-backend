from sqlalchemy import Column, Integer, String, Boolean, Enum
from app.database import Base
import enum

class RoleEnum(str, enum.Enum):
    viewer = "viewer"
    analyst = "analyst"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.viewer)
    is_active = Column(Boolean, default=True)