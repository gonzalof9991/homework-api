## Installation

````
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
uvicorn src.app.main:api --host 0.0.0.0 --workers 4  
````
