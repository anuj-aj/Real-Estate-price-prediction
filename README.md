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


### Sample Request Body for FAST API post request execution
{
  "property_type": "Unit",
  "property_subtype": "Hotel Apartment",
  "area": "JUMEIRAH VILLAGE CIRCLE",
  "actual_area": 16000,
  "rooms": 2,
  "parking": 1,
  "is_offplan": true,
  "is_freehold": true,
  "usage": "Residential",
  "nearest_metro": "Dubai Internet City",
  "nearest_mall": "Marina Mall",
  "master_project": "NORTH FORTY THREE SERVICED RESIDENCES",
  "project": "NORTH FORTY THREE SERVICED RESIDENCES"
}




