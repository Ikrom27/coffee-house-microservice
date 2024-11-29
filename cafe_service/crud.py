from typing import List

from sqlalchemy.orm import Session

from cafe_service.database import engine
from cafe_service.models import CoffeeShop, Coffee, CoffeeOfShop
from cafe_service.schemas import CoffeeShopCreate


def create_coffee_shop(coffee_shop: CoffeeShopCreate) -> CoffeeShop:
    coffee_shop_db = CoffeeShop(name=coffee_shop.name, location=coffee_shop.location)
    with Session(engine) as session:
        session.add(coffee_shop_db)
        session.commit()
        session.refresh(coffee_shop_db)
    return coffee_shop_db


def create_coffee(coffee: Coffee) -> int:
    with Session(engine) as session:
        session.add(coffee)
        session.commit()
        session.refresh(coffee)


def get_all_coffee_shops() -> List[CoffeeShop]:
    with Session(engine) as session:
        return session.query(CoffeeShop).all()


def delete_coffee_shop(coffee_shop_id: int) -> dict:
    with Session(engine) as session:
        coffee_shop = session.query(CoffeeShop).filter(CoffeeShop.id == coffee_shop_id).first()
        if coffee_shop:
            session.delete(coffee_shop)
            session.commit()
            return {"message": "successful deleted"}
        return {"message": "item is not exist"}


def update_coffee_shop_status(coffee_shop_id: int, is_active: bool) -> CoffeeShop:
    with Session(engine) as session:
        coffee_shop = session.query(CoffeeShop).filter(CoffeeShop.id == coffee_shop_id).first()
        if coffee_shop:
            coffee_shop.is_active = is_active
            session.commit()
            session.refresh(coffee_shop)
    return coffee_shop


def add_coffee_to_all_shops(coffee: Coffee):
    with Session(engine) as session:
        session.add(coffee)
        session.commit()
        session.refresh(coffee)
        print(f"Coffee ID: {coffee.id}")
        coffee_shops = session.query(CoffeeShop).all()
        for shop in coffee_shops:
            coffee_of_shop = CoffeeOfShop(coffee_id=coffee.id, coffee_shop_id=shop.id)
            session.add(coffee_of_shop)

        session.commit()



def remove_coffee_from_coffee_shop(coffee_shop_id: int, coffee_id: int) -> dict:
    with Session(engine) as session:
        coffee_shop = session.query(CoffeeShop).filter(CoffeeShop.id == coffee_shop_id).first()
        coffee = session.query(Coffee).filter(Coffee.id == coffee_id).first()
        if coffee_shop and coffee:
            relation = session.query(CoffeeOfShop).filter(
                CoffeeOfShop.coffee_shop_id == coffee_shop_id,
                CoffeeOfShop.coffee_id == coffee_id
            ).first()
            if relation:
                session.delete(relation)
                session.commit()
                return {"message": "coffee removed from coffee shop"}
            return {"message": "coffee not found in this coffee shop"}
        return {"message": "coffee or coffee shop not found"}


def delete_coffee(coffee):
    with Session(engine) as session:
        session.delete(coffee)
        session.commit()
        return {"message": "successful deleted"}


def coffee_availability(coffee: Coffee) -> Coffee:
    with Session(engine) as session:
        session.commit()
        session.refresh(coffee)


def get_coffee_shop_menu(coffee_shop_id: int):
    with Session(engine) as session:
        coffee_shop = session.query(CoffeeShop).filter(CoffeeShop.id == coffee_shop_id).first()
        if coffee_shop:
            return coffee_shop.coffees
        return []