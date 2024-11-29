from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Coffee(Base):
    __tablename__ = 'coffees'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Integer)
    is_available = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Coffee(name={self.name}, price={self.price}, available={self.is_available})>"

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "is_available": self.is_available
        }