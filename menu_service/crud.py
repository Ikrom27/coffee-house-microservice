from typing import List

from menu_service.rabbitmq import send_coffee_action
from menu_service.schemas import CreateCoffeeRequest, CoffeeResponse
from menu_service.database import engine
from menu_service.models import Coffee
from sqlalchemy.orm import Session


def create_coffee(coffee: CreateCoffeeRequest) -> CoffeeResponse:
    coffee_db = Coffee(name=coffee.name,
                       description=coffee.description,
                       price=coffee.price)
    with Session(engine) as session:
        session.add(coffee_db)
        session.commit()
        session.refresh(coffee_db)
        send_coffee_action(CoffeeResponse.from_orm(coffee_db).dict(), "add")
    return CoffeeResponse.from_orm(coffee_db)


def get_all_coffees() -> List[Coffee]:
    with Session(engine) as session:
        return session.query(Coffee).all()


def delete_coffee(coffee_id: int) -> dict:
    with Session(engine) as session:
        coffee = session.query(Coffee).filter(Coffee.id == coffee_id).first()
        if coffee:
            session.delete(coffee)
            session.commit()
            send_coffee_action(coffee, "delete")
            return {"message": "successful deleted"}
        return {"message": "item is not exist"}


def coffee_availability(coffee_id: int, is_available: bool) -> Coffee:
    with Session(engine) as session:
        coffee = session.query(Coffee).filter(Coffee.id == coffee_id).first()
        if coffee:
            coffee.is_available = is_available
            session.commit()
            session.refresh(coffee)
        send_coffee_action(coffee, "toggle_availability")
    return coffee