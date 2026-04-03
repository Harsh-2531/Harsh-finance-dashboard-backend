from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.core.security import verify_password, create_access_token, hash_password

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(name: str, email: str, password: str, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    user = User(name=name, email=email, hashed_password=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User created successfully", "email": user.email}

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register")
def register(name: str, email: str, password: str, role: str = "viewer", db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    user = User(name=name, email=email, 
                hashed_password=hash_password(password),
                role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User created successfully", "email": user.email, "role": user.role}