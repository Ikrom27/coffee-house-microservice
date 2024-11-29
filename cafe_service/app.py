import threading
from typing import List

from fastapi import FastAPI

from cafe_service import crud
from cafe_service.models import Coffee
from cafe_service.rabbitmq import listen_queue
from cafe_service.schemas import CoffeeShopCreate, CoffeeResponse, CreateCoffeeRequest, CoffeeShopResponse


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    listener_thread = threading.Thread(target=listen_queue, daemon=True)
    listener_thread.start()


@app.post("/coffee_shops/", response_model=CoffeeShopResponse)
async def create_coffee_shop(coffee_shop: CoffeeShopCreate):
    return crud.create_coffee_shop(coffee_shop)


@app.get("/coffee_shops/", response_model=List[CoffeeShopResponse])
async def get_coffee_shops():
    return crud.get_all_coffee_shops()


@app.delete("/coffee_shops/{coffee_shop_id}")
async def delete_coffee_shop(coffee_shop_id: int):
    return crud.delete_coffee_shop(coffee_shop_id)


@app.put("/coffee_shops/{coffee_shop_id}/status", response_model=CoffeeShopResponse)
async def update_coffee_shop_status(coffee_shop_id: int, is_active: bool):
    return crud.update_coffee_shop_status(coffee_shop_id, is_active)


# @app.post("/coffee_shops/{coffee_shop_id}/coffees/{coffee_id}/add")
# async def add_coffee_to_coffee_shop(coffee_shop_id: int, coffee_id: int):
#     return crud.add_coffee_to_all_shops(coffee_shop_id, coffee_id)


@app.delete("/coffee_shops/{coffee_shop_id}/coffees/{coffee_id}/remove")
async def remove_coffee_from_coffee_shop(coffee_shop_id: int, coffee_id: int):
    return crud.remove_coffee_from_coffee_shop(coffee_shop_id, coffee_id)


@app.get("/coffees/{coffee_shop_id}")
async def get_coffee_shop_menu(coffee_shop_id: int):
    return crud.get_coffee_shop_menu(coffee_shop_id)


@app.post("/coffees/", response_model=CoffeeResponse)
async def add_coffee(coffee: CreateCoffeeRequest):
    return CoffeeResponse.from_orm(crud.create_coffee(Coffee(
        name=coffee.name,
        price=coffee.price,
        description=coffee.description
    )))
