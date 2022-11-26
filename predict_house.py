from fastapi import FastAPI
from pydantic import BaseModel
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

@app.get('/predict')
def view_houses():
    return houses


@app.get('/predict/{id}')
def predict_sale(id: int):
    model = pickle.load(open('dt_regressor.pkl', 'rb'))
    input = [house for house in houses if house.id == id][0]
    predictors = np.array([input.bedroom, input.bathroom, input.sqft]).reshape(1, -1)
    output = model.predict(predictors)
    
    return f'The predicted sale of this home is {output[0]:.2f}.'


@app.post('/houses')
def add_house(house: NewHouse):
    houses.append(house)
    return house