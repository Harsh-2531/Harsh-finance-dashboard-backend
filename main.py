from fastapi import FastAPI
from database import Base, engine
from routers import auth, users, transactions, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance Dashboard API", version="1.0.0")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(dashboard.router)

@app.get("/")
def root():
    return {"message": "Finance Dashboard API is running"}