# start redis
brew services start redis

curl -N \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI5YmQ5ZGQxNi04NGVkLTRjN2YtYmQ1OC03NDQyZjY0NGE0NmYiLCJyb2xlIjoiY3VzdG9tZXIiLCJ0eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg3MTQ0NDYyfQ.Aapx6nc_7sRck8PyOx7sM3Gar3D03rrDxjOv9kJTkgA" \
http://127.0.0.1:8000/cart/events



curl -N \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI5YmQ5ZGQxNi04NGVkLTRjN2YtYmQ1OC03NDQyZjY0NGE0NmYiLCJyb2xlIjoiY3VzdG9tZXIiLCJ0eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg3MTQ0NDYyfQ.Aapx6nc_7sRck8PyOx7sM3Gar3D03rrDxjOv9kJTkgA" \
http://127.0.0.1:8000/cart/events


# to test redis 
curl -N \
-H "Authorization: Bearer TOKEN" \
http://127.0.0.1:8000/cart/events

# Create python Environment
python3 -m venv venv

# Activate environment
source venv/bin/activate

# Install all the requirements 
pip install -r requirements.txt

# check installed packages
pip list

# run Uvicron
uvicorn app.main:app --reload

## initilize alembic
alembic init alembic

## upgrade alembic head
alembic upgrade head



## steps to delete alembic versions and fresh start 
        1 - DROP DATABASE blinkit_db;
        2 - CREATE DATABASE blinkit_db;

        ## delete migraton files
        3 - rm -f alembic/versions/*.py
        
        ## fresh migration
        4 - alembic revision --autogenerate -m "initial schema"




## for api in json
http://localhost:8000/openapi.json






# -----------------------------------
# # Redis Local Setup — macOS
# -----------------------------------



## 1. Install Redis

```bash
brew install redis
```

## 2. Start Redis

Redis ko background service ke roop me start karne ke liye:

```bash
brew services start redis
```

Default Redis address:

```text
localhost:6379
```

## 3. Check Redis Connection

Redis properly run ho raha hai ya nahi:

```bash
redis-cli ping
```

Expected output:

```text
PONG
```

Agar `PONG` aa raha hai, Redis successfully running hai.

## 4. Check Redis Service Status

```bash
brew services list
```

Isse pata chalega Redis `started` hai ya `stopped`.

## 5. Stop Redis

```bash
brew services stop redis
```

## 6. Restart Redis

```bash
brew services restart redis
```

## Quick Commands

```bash
# Install
brew install redis

# Start
brew services start redis

# Test connection
redis-cli ping

# Check status
brew services list

# Stop
brew services stop redis

# Restart
brew services restart redis
```

## Expected Flow

```text
brew install redis
        ↓
brew services start redis
        ↓
redis-cli ping
        ↓
PONG
        ↓
Redis ready at localhost:6379
```
