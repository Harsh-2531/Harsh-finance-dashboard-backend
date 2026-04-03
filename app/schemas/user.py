from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional

class RoleEnum(str, Enum):
    viewer = "viewer"
    analyst = "analyst"
    admin = "admin"

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: RoleEnum = RoleEnum.viewer

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: RoleEnum
    is_active: bool

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[RoleEnum] = None
    is_active: Optional[bool] = None