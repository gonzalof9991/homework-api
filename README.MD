## Installation

````
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
pip freeze > requirements.txt
uvicorn src.app.main:api --reload --host 0.0.0.0 --workers 4  
````

## Upgrade alembic

````
alembic revision --autogenerate -m "Add column"
alembic upgrade head

````
