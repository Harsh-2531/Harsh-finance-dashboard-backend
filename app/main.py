from fastapi import FastAPI
from app.database import Base, engine
from app.models import user, transaction
from app.routers import auth, transactions, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance Dashboard API", version="1.0.0")

app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(dashboard.router)

@app.get("/")
def root():
    return {"message": "Finance Dashboard API is running"}