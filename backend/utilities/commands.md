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