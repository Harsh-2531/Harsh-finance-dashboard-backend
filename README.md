# Finance Dashboard Backend API

A production-ready backend API for a finance dashboard system built with **Python**, **FastAPI**, and **MySQL**. Supports user role management, financial records, and dashboard analytics with JWT authentication.

---

## Live API

> Test the API directly — no setup required

**Swagger UI:** https://harsh-finance-dashboard-backend-production.up.railway.app/docs

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.13 |
| Framework | FastAPI |
| Database | MySQL 8.0 |
| ORM | SQLAlchemy |
| Auth | JWT (python-jose) |
| Password Hashing | bcrypt (passlib) |
| Deployment | Railway |

---

## Features

- JWT based authentication (register and login)
- Role based access control (viewer, analyst, admin)
- Financial records management (income and expense tracking)
- Record filtering by date, category and type
- Dashboard summary APIs (totals, trends, category breakdown)
- Input validation and error handling
- MySQL database with auto table creation

---

## Role Permissions

| Endpoint | Viewer | Analyst | Admin |
|---|---|---|---|
| GET /transactions | ✅ | ✅ | ✅ |
| POST /transactions | ❌ | ❌ | ✅ |
| PATCH /transactions | ❌ | ❌ | ✅ |
| DELETE /transactions | ❌ | ❌ | ✅ |
| GET /dashboard/summary | ✅ | ✅ | ✅ |
| GET /dashboard/recent | ✅ | ✅ | ✅ |
| GET /dashboard/by-category | ❌ | ✅ | ✅ |
| GET /dashboard/monthly-trends | ❌ | ✅ | ✅ |

---

## Project Structure

finance-dashboard-backend/
├── app/
│   ├── main.py              # App entry point
│   ├── database.py          # DB connection and session
│   ├── core/
│   │   ├── config.py        # Environment config
│   │   └── security.py      # JWT and password hashing
│   ├── models/
│   │   ├── user.py          # User table model
│   │   └── transaction.py   # Transaction table model
│   ├── routers/
│   │   ├── auth.py          # Register and login
│   │   ├── transactions.py  # CRUD for transactions
│   │   └── dashboard.py     # Summary and analytics
│   ├── schemas/
│   │   ├── user.py          # User request/response schemas
│   │   └── transaction.py   # Transaction schemas
│   └── services/
│       └── access_control.py # Role based auth middleware
├── .env                     # Environment variables
├── Procfile                 # Railway start command
└── requirements.txt         # Python dependencies

---

## Local Setup

### Prerequisites
- Python 3.10+
- MySQL 8.0

### Steps
```bash
# 1. Clone the repository
git clone https://github.com/Harsh-2531/Harsh-finance-dashboard-backend.git
cd Harsh-finance-dashboard-backend

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost:3306/finance_db
SECRET_KEY=supersecretkey123
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# 5. Create MySQL database
mysql -u root -p
CREATE DATABASE finance_db;

# 6. Run the server
uvicorn app.main:app --reload
```

Visit http://localhost:8000/docs

---

## API Endpoints

### Auth
| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | /auth/register | Register new user | Public |
| POST | /auth/login | Login and get token | Public |

### Transactions
| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | /transactions/ | Create transaction | Admin |
| GET | /transactions/ | List all transactions | All roles |
| PATCH | /transactions/{id} | Update transaction | Admin |
| DELETE | /transactions/{id} | Delete transaction | Admin |

### Dashboard
| Method | Endpoint | Description | Access |
|---|---|---|---|
| GET | /dashboard/summary | Total income, expenses, balance | All roles |
| GET | /dashboard/by-category | Totals grouped by category | Analyst, Admin |
| GET | /dashboard/recent | Last 10 transactions | All roles |
| GET | /dashboard/monthly-trends | Monthly breakdown | Analyst, Admin |

---

## Quick Test

### 1. Register
```bash
curl -X POST "https://harsh-finance-dashboard-backend-production.up.railway.app/auth/register?name=Test&email=test@test.com&password=test123&role=admin"
```

### 2. Login
```bash
curl -X POST "https://harsh-finance-dashboard-backend-production.up.railway.app/auth/login" \
  -d "username=test@test.com&password=test123"
```

### 3. Create Transaction
```bash
curl -X POST "https://harsh-finance-dashboard-backend-production.up.railway.app/transactions/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"amount": 5000, "type": "income", "category": "Salary", "date": "2026-04-03"}'
```

---

## Environment Variables

| Variable | Description |
|---|---|
| DATABASE_URL | MySQL connection string |
| SECRET_KEY | JWT signing key |
| ALGORITHM | JWT algorithm (HS256) |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token expiry time |

---

## Assumptions Made

- Admin role is assigned manually via DB after registration
- Soft delete is not implemented, records are permanently deleted
- All dates follow YYYY-MM-DD format
- Token expiry is set to 60 minutes by default

---

## Author

**Harsh Kumar Sharma**
GitHub: https://github.com/Harsh-2531
