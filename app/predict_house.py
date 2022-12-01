from fastapi import FastAPI, HTTPException, Request
from typing import Optional
import numpy as np
import pickle

#Import pydantic models and house data
from schemas import House, NewHouse
from house_data import houses

#Testing frontend packages
from fastapi.templating import Jinja2Templates
from pathlib import Path


app = FastAPI()


BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))


@app.get('/')
def root(request: Request) -> dict:
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "houses": houses},
    )


# @app.get('/', status_code=200)
# def root() -> dict:
#     return {'message': 'Predict house sales.'}


@app.get('/houses')
def view_houses():
    return {'houses': houses}


@app.post('/houses/add_house', response_model=House)
def add_house(house: NewHouse):
    new_id = len(houses) + 1
    house_entry = House(
        id = new_id,
        bedroom = house.bedroom,
        bathroom = house.bathroom,
        sqft = house.sqft,
    )
    houses.append(house_entry)
    return house_entry


@app.delete('/houses/delete_house/{id}')
def delete_house(id: int):
    selected_house = [house for house in houses if house.id == id][0]
    houses.remove(selected_house)

    return {'message': f'House_id {id} successfully deleted.'}


@app.put('/houses/update_house/{id}')
def update_house(id: int, bedroom: Optional[int] = None, bathroom: Optional[int] = None, sqft: Optional[float] = None):
    selected_house = [house for house in houses if house.id == id][0]
    if bedroom:
        selected_house.bedroom = bedroom
    if bathroom:
        selected_house.bathroom = bathroom
    if sqft:
        selected_house.sqft = sqft

    return {'message': f'House_id {id} successfully updated.'}



@app.get('/predict/{id}')
def predict_sale(id: int):
    result = [house for house in houses if house.id == id]
    if not result:
        raise HTTPException(
            status_code=404, detail=f'House with ID {id} not found.'
        )

    model = pickle.load(open('dt_regressor.pkl', 'rb'))
    input = result[0]
    predictors = np.array([input.bedroom, input.bathroom, input.sqft]).reshape(1, -1)
    output = model.predict(predictors)

    return f'The predicted sale of this home is {output[0]:.2f}.'