from pydantic import BaseModel


class CreateCoffeeRequest(BaseModel):
    name: str
    description: str
    price: int


class CoffeeResponse(BaseModel):
    id: int
    name: str
    description: str
    price: int
    is_available: bool

    class Config:
        from_attributes = True