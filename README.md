# Blinkit Clone — FastAPI + PostgreSQL

A Blinkit-style full-stack clone built with **FastAPI**, **SQLAlchemy**, **PostgreSQL**, JWT authentication, branch-level inventory, product catalog, cart management, admin controls, and customer-facing product browsing.

## Features

### Backend
- FastAPI REST API
- PostgreSQL database
- SQLAlchemy ORM
- Alembic migrations
- JWT access + refresh token authentication
- Super Admin
- Branch Managers
- Customers
- Branch management
- Brand management
- Categories & Subcategories
- Products
- Product Variants
- Product Images
- Branch-wise Inventory
- Branch Catalog
- Cart / Cart Items
- Stock increase / decrease
- Activate / deactivate resources
- Swagger / OpenAPI docs

### Admin UI
The admin panel supports branch management, manager assignment, brands, categories, subcategories, products, variants, images, inventory, branch catalog preview, customers, API console and admin profile.

### Customer UI
The customer UI supports authentication, branch selection, branch-specific catalog, product search/sorting and cart operations.

> Important: customer products should be loaded from the selected branch catalog, not from the global `/products` endpoint.

---

# 1. Recommended Project Structure

```text
blinkit_clone_fast_api/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── exceptions/
│   │   └── __init__.py
│   │
│   ├── alembic/
│   ├── alembic.ini
│   ├── requirements.txt
│   ├── .env
│   └── venv/
│
├── blinkit-customer-ui/
│   ├── index.html
│   ├── app.js
│   └── ...
│
├── blinkit-admin-ui/
│   ├── index.html
│   ├── app.js
│   └── ...
│
└── README.md
```

If you run Uvicorn **inside the `backend` folder**, imports should normally look like:

```python
from app.database.database import get_db
from app.routes.admin_routes import router
```

Do not use:

```python
from backend.app.database.database import get_db
```

when running:

```bash
uvicorn app.main:app --reload
```

from inside `backend/`.

---

# 2. Requirements

Recommended:
- Python 3.11+
- PostgreSQL
- pip
- Git
- Modern browser

The project has also been run with Python 3.14. If a package compatibility issue appears, Python 3.11 or 3.12 is generally a safer development choice.

---

# 3. Clone Project

```bash
git clone YOUR_REPOSITORY_URL
cd blinkit_clone_fast_api
```

---

# 4. Backend Setup

```bash
cd backend
```

## Remove old virtual environment

```bash
deactivate
rm -rf venv
```

> Be careful with `rm -rf`. Confirm you are in the correct project directory.

## Create new venv

```bash
python3 -m venv venv
source venv/bin/activate
```

Verify:

```bash
which python
which pip
```

Expected paths should point inside:

```text
.../backend/venv/bin/python
.../backend/venv/bin/pip
```

---

# 5. Install Dependencies

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install requirements:

```bash
pip install -r requirements.txt
```

Current `requirements.txt`:

```txt
uvicorn
fastapi
sqlalchemy
psycopg[binary]
python-dotenv
alembic
pydantic
email-validator
passlib[bcrypt]
bcrypt==4.0.1
PyJWT
```

Verify:

```bash
pip list
```

Quick import test:

```bash
python -c "import fastapi, sqlalchemy, dotenv, psycopg, jwt; print('ALL IMPORTS OK')"
```

Expected:

```text
ALL IMPORTS OK
```

---

# 6. PostgreSQL Setup

On macOS with Homebrew:

```bash
brew services start postgresql
```

Check services:

```bash
brew services list
```

Open PostgreSQL:

```bash
psql postgres
```

Create database:

```sql
CREATE DATABASE blinkit_db;
```

List databases:

```sql
\l
```

Connect:

```sql
\c blinkit_db
```

Exit:

```sql
\q
```

---

# 7. Environment Variables

Create:

```text
backend/.env
```

Example:

```env
DATABASE_URL=postgresql+psycopg://YOUR_DB_USER:YOUR_DB_PASSWORD@localhost:5432/blinkit_db
SECRET_KEY=0f8d7c6b5a4e392817263544536271809f8e7d6c5b4a39281726354453627180a1b2c3d4e5f60718293a4b5c6d7e8f90
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

Example without DB password:

```env
DATABASE_URL=postgresql+psycopg://Aman@localhost:5432/blinkit_db
```

Use the **exact environment variable names expected by your code**. If your `database.py` or auth config uses different names, match those names.

Never commit `.env`.

Recommended `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
.DS_Store
```

---

# 8. Alembic Migrations

Apply existing migrations:

```bash
alembic upgrade head
```

Create migration after model changes:

```bash
alembic revision --autogenerate -m "describe your change"
```

Apply:

```bash
alembic upgrade head
```

Check current revision:

```bash
alembic current
```

History:

```bash
alembic history
```

---

# 9. Start FastAPI Backend

Make sure you are inside:

```text
blinkit_clone_fast_api/backend
```

Activate venv:

```bash
source venv/bin/activate
```

Run:

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

OpenAPI JSON:

```text
http://127.0.0.1:8000/openapi.json
```

---

# 10. Import Path Rule

If you are inside `backend/` and run:

```bash
uvicorn app.main:app --reload
```

use:

```python
from app.database.database import get_db
from app.services.cart_service import CartService
from app.schemas.cart_schema import CartCreate
```

If you see:

```text
ModuleNotFoundError: No module named 'backend'
```

search:

```bash
grep -R "from backend\.app" app
grep -R "import backend\.app" app
```

Change imports such as:

```python
from backend.app.database.database import get_db
```

to:

```python
from app.database.database import get_db
```

---

# 11. Start Customer Frontend

Open a new terminal:

```bash
cd blinkit-customer-ui
python3 -m http.server 5600
```

Open:

```text
http://localhost:5600
```

If port `5600` is busy:

```bash
lsof -nP -iTCP:5600 -sTCP:LISTEN
```

Kill old process:

```bash
kill -9 $(lsof -ti :5600)
```

Then restart:

```bash
python3 -m http.server 5600
```

Or another port:

```bash
python3 -m http.server 5601
```

---

# 12. Start Admin Frontend

Example:

```bash
cd blinkit-admin-ui
python3 -m http.server 5500
```

Open:

```text
http://localhost:5500
```

Admin API base URL should point to:

```text
http://127.0.0.1:8000
```

---

# 13. CORS

Because frontend and backend run on different origins, configure CORS in FastAPI.

Example:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5600",
        "http://127.0.0.1:5600",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Important: create `app = FastAPI()` only once. Do not overwrite the app after adding middleware.

---

# 14. Authentication

Login:

```http
POST /auth/login
```

Example body:

```json
{
  "email": "user@example.com",
  "password": "your-password"
}
```

Protected API calls use:

```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Never publish real JWT tokens.

---

# 15. Catalog + Inventory Design

The project uses a **global catalog + branch-level inventory** design.

```text
Brand
  ↓
Category
  ↓
Subcategory
  ↓
Product
  ↓
Product Variant
  ↓
Branch Inventory
  ↓
Branch Catalog
```

A product can exist globally but not be purchasable in every branch.

---

# 16. Branch Inventory

Create inventory:

```http
POST /inventory
```

Example:

```json
{
  "branch_unique_id": "BRANCH_UUID",
  "product_variant_unique_id": "VARIANT_UUID",
  "stock_quantity": 50,
  "selling_price_override": null,
  "is_available": true
}
```

Exact inventory lookup:

```http
GET /inventory/branch/{branch_unique_id}/variant/{product_variant_unique_id}
```

Increase stock:

```http
PATCH /inventory/branch/{branch_unique_id}/variant/{product_variant_unique_id}/increase-stock
```

Example:

```json
{
  "quantity": 10
}
```

Decrease stock:

```http
PATCH /inventory/branch/{branch_unique_id}/variant/{product_variant_unique_id}/decrease-stock
```

Activate inventory:

```http
PATCH /inventory/branch/{branch_unique_id}/variant/{product_variant_unique_id}/activate
```

Deactivate inventory:

```http
PATCH /inventory/branch/{branch_unique_id}/variant/{product_variant_unique_id}/deactivate
```

---

# 17. Branch Catalog

Customer product listing should use:

```http
GET /branch-catalog/{branch_unique_id}
```

Do not use global `/products` for customer availability-sensitive listing.

Correct flow:

```text
Customer selects branch
        ↓
GET /branch-catalog/{branch_id}
        ↓
Only that branch's purchasable products
        ↓
Customer selects variant
        ↓
Add to cart
```

---

# 18. Cart Flow

Create cart:

```http
POST /cart
```

Body:

```json
{
  "branch_unique_id": "BRANCH_UUID"
}
```

Get cart:

```http
GET /cart
```

Add item:

```http
POST /cart/items
```

Body:

```json
{
  "product_variant_unique_id": "VARIANT_UUID",
  "quantity": 1
}
```

Clear only items:

```http
DELETE /cart/clear
```

Delete complete cart:

```http
DELETE /cart/delete
```

---

# 19. Important Cart + Branch Rule

The cart is attached to a branch.

If:

```text
Selected Branch = Branch B
Cart Branch     = Branch A
```

then adding a Branch B variant can fail with:

```text
Product not available in this branch
```

Correct flow:

```text
Selected branch
      ↓
Create/use cart for same branch
      ↓
Load branch catalog for same branch
      ↓
Add only variants from that branch
```

---

# 20. Debug: Product Not Available in This Branch

If `POST /cart/items` returns:

```text
400 Bad Request
Product not available in this branch
```

check:
1. cart branch UUID
2. selected branch UUID
3. product variant UUID
4. exact branch inventory
5. stock quantity
6. `is_available`
7. product/variant active state
8. branch catalog

Exact test:

```http
GET /inventory/branch/{BRANCH_UUID}/variant/{VARIANT_UUID}
```

Also test:

```http
GET /branch-catalog/{BRANCH_UUID}
```

The variant should exist in the branch catalog if it is purchasable there.

---

# 21. Cart Delete Message Constant

If cart delete throws:

```text
AttributeError: module 'app.exceptions.messages' has no attribute 'CART_DELETED'
```

add to:

```text
app/exceptions/messages.py
```

```python
CART_DELETED = "Cart deleted successfully"
```

---

# 22. Seed Test Data

If your repository contains `seed_blinkit.py`, install requests if required:

```bash
pip install requests
```

Run:

```bash
python seed_blinkit.py \
  --base-url http://127.0.0.1:8000 \
  --email admin@example.com \
  --password YOUR_PASSWORD
```

Assign inventory to an existing branch:

```bash
python seed_blinkit.py \
  --base-url http://127.0.0.1:8000 \
  --email admin@example.com \
  --password YOUR_PASSWORD \
  --branch-id YOUR_BRANCH_UUID
```

Important:
- branch must already exist
- products are global
- inventory is branch-specific
- `--branch-id` decides which branch receives inventory rows

---

# 23. Reset All Data But Keep Tables

Connect to PostgreSQL:

```bash
psql blinkit_db
```

Run:

```sql
DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN (
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
    )
    LOOP
        EXECUTE 'TRUNCATE TABLE public.'
            || quote_ident(r.tablename)
            || ' RESTART IDENTITY CASCADE';
    END LOOP;
END $$;
```

This removes rows but keeps schema/tables.

---

# 24. Full Database Schema Reset

Warning: this removes tables, constraints, indexes and data.

```sql
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
```

Then:

```bash
alembic upgrade head
```

---

# 25. Common Errors

## `ModuleNotFoundError: No module named 'backend'`

Cause: running from `backend/` while imports still use `backend.app...`.

Fix imports to `app...`.

## `ModuleNotFoundError: No module named 'sqlalchemy'`

```bash
which python
which pip
pip install -r requirements.txt
python -c "import sqlalchemy; print(sqlalchemy.__version__)"
```

## `ModuleNotFoundError: No module named 'dotenv'`

```bash
pip install python-dotenv
python -c "import dotenv; print('dotenv OK')"
```

## `OSError: [Errno 48] Address already in use`

Backend port:

```bash
lsof -nP -iTCP:8000 -sTCP:LISTEN
```

Customer port:

```bash
lsof -nP -iTCP:5600 -sTCP:LISTEN
```

Kill:

```bash
kill -9 PID
```

## 401 Not Authenticated

Login and send:

```http
Authorization: Bearer ACCESS_TOKEN
```

## 403 Forbidden

User is authenticated but does not have permission for that operation.

---

# 26. Recommended Development Startup Order

Use separate terminals.

### Terminal 1 — PostgreSQL

```bash
brew services start postgresql
```

### Terminal 2 — Backend

```bash
cd blinkit_clone_fast_api/backend
source venv/bin/activate
alembic upgrade head
uvicorn app.main:app --reload
```

### Terminal 3 — Customer UI

```bash
cd blinkit-customer-ui
python3 -m http.server 5600
```

### Terminal 4 — Admin UI

```bash
cd blinkit-admin-ui
python3 -m http.server 5500
```

Open:

```text
Backend docs: http://127.0.0.1:8000/docs
Customer UI:  http://localhost:5600
Admin UI:     http://localhost:5500
```

---

# 27. Quick Fresh Setup

```bash
git clone YOUR_REPOSITORY_URL
cd blinkit_clone_fast_api/backend

python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create `.env`, create PostgreSQL database, then:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

# 28. Useful Commands

```bash
which python
which pip
pip list
pip freeze > requirements-lock.txt
lsof -i :8000
lsof -i :5600
```

PostgreSQL:

```bash
psql postgres
```

```sql
\l
\dt
\q
```

---

# 29. Security Notes

- Never commit `.env`
- Never expose `SECRET_KEY`
- Never publish real JWT access/refresh tokens
- Never commit database passwords
- Rotate exposed tokens
- Use HTTPS in production
- Restrict CORS origins in production
- Do not use development credentials in production

---

# 30. API Documentation

```text
Swagger UI: http://127.0.0.1:8000/docs
ReDoc:      http://127.0.0.1:8000/redoc
OpenAPI:    http://127.0.0.1:8000/openapi.json
```

Swagger is the easiest place to inspect the current request/response schemas and test endpoints.

---

## Author

**Aman**

Blinkit Clone built with FastAPI, SQLAlchemy, PostgreSQL and vanilla frontend technologies.
