from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Coffee(Base):
    __tablename__ = 'coffees'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Integer)
    is_available = Column(Boolean, default=True)

    coffee_shops = relationship('CoffeeShop', secondary='coffee_of_shop', back_populates="coffees")

    def __repr__(self):
        return f"<Coffee(name={self.name}, price={self.price}, available={self.is_available})>"


class CoffeeOfShop(Base):
    __tablename__ = 'coffee_of_shop'

    coffee_id = Column(Integer, ForeignKey('coffees.id'), primary_key=True)
    coffee_shop_id = Column(Integer, ForeignKey('coffee_shops.id'), primary_key=True)


class CoffeeShop(Base):
    __tablename__ = 'coffee_shops'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    is_active = Column(Boolean, default=True)

    coffees = relationship('Coffee', secondary='coffee_of_shop', back_populates="coffee_shops")

    def __repr__(self):
        return f"<CoffeeShop(name={self.name}, location={self.location})>"
