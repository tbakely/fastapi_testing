from pydantic import BaseModel


class House(BaseModel):
    id: int
    bedroom: int
    bathroom: int
    sqft: float

class NewHouse(BaseModel):
    bedroom: int
    bathroom: int
    sqft: float