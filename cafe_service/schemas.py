from pydantic import BaseModel


class CoffeeShopCreate(BaseModel):
    name: str
    location: str


class CoffeeShopResponse(BaseModel):
    id: int
    name: str
    location: str
    is_active: bool

    class Config:
        from_attributes = True


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