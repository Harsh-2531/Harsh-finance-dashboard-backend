from fastapi import FastAPI
from database import Base, engine
from routers import auth, users, transactions, dashboard
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram
import time

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance Dashboard API", version="1.0.0")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(dashboard.router)

# Prometheus auto-instruments all routes — tracks request count, latency etc.
Instrumentator().instrument(app).expose(app)

# Custom business metrics
transaction_counter = Counter(
    "finance_transactions_total",
    "Total number of transactions created",
    ["type", "category"]
)

transaction_errors = Counter(
    "finance_transaction_errors_total",
    "Total failed transaction operations"
)

@app.get("/")
def root():
    return {"message": "Finance Dashboard API is running"}