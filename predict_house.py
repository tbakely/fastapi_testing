from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import numpy as np
import pickle

houses = []

class NewHouse(BaseModel):
    id: int
    bedroom: int
    bathroom: int
    sqft: float
    school_score: int


app = FastAPI()


@app.get('/', status_code=200)
def root() -> dict:
    return {'message': 'Predict house sales.'}


@app.get('/houses')
def view_houses():
    return houses


@app.post('/houses/add_house')
def add_house(house: NewHouse):
    houses.append(house)
    return house


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
    model = pickle.load(open('dt_regressor.pkl', 'rb'))
    input = [house for house in houses if house.id == id][0]
    predictors = np.array([input.bedroom, input.bathroom, input.sqft]).reshape(1, -1)
    output = model.predict(predictors)
    
    return f'The predicted sale of this home is {output[0]:.2f}.'


