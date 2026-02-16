## Create virtaul Env
python -m venv venv
venv\Scripts\activate

## install requirements
pip install -r requirements.txt


## Training
python src/trainer.py

## Run FAST API server
cd src

uvicorn api:app --reload




