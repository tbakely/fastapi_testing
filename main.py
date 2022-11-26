from fastapi import FastAPI
from pydantic import BaseModel

houses = []

class NewHouse(BaseModel):
    id: int
    rooms: int
    sqft: float
    school_score: int

app = FastAPI()

@app.get('/predict')
def view_houses():
    return houses

# @app.get('/predict/{id}')
# def predict_sale(id: int):
#     input = houses[id]
#     output = input.rooms * 100 + input.sqft * 150 + input.school_score * 10000
    
#     return f'The predicted sale of this home is {output}.'

@app.get('/predict/{id}')
def predict_sale(id: int):
    input = [house for house in houses if house.id == id][0]
    output = input.rooms * 100 + input.sqft * 150 + input.school_score * 10000
    
    return f'The predicted sale of this home is {output}.'

# @app.post('/houses')
# def add_house(id: int, house: NewHouse):
#     houses[id] = house
#     return house

@app.post('/houses')
def add_house(house: NewHouse):
    houses.append(house)
    return house