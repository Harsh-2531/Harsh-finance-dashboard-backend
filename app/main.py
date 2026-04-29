from fastapi import FastAPI
from app.database import Base, engine
from app.models import user, transaction
from app.routers import auth, transactions, dashboard
from prometheus_fastapi_instrumentator import Instrumentator

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance Dashboard API", version="1.0.0")

app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(dashboard.router)

# Add this line — instruments all routes automatically
Instrumentator().instrument(app).expose(app)

@app.get("/")
def root():
    return {"message": "Finance Dashboard API is running"}