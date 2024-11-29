from fastapi import FastAPI
from menu_service.schemas import CreateCoffeeRequest, CoffeeResponse
from menu_service import crud


app = FastAPI()


@app.post("/coffees/", response_model=CoffeeResponse)
async def add_coffee(coffee: CreateCoffeeRequest):
    return crud.create_coffee(coffee)


@app.get("/coffees", response_model=list[CoffeeResponse])
async def get_coffees():
    return crud.get_all_coffees()


@app.delete("/coffees/{coffee_id}")
async def delete_coffee(coffee_id: int):
    return crud.delete_coffee(coffee_id)


@app.post("/coffees/{coffee_id}/block")
async def block_coffee(coffee_id: int):
    return crud.coffee_availability(coffee_id, False)


@app.post("/coffees/{coffee_id}/unblock")
async def block_coffee(coffee_id: int):
    return crud.coffee_availability(coffee_id, True)
