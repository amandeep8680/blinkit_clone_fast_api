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