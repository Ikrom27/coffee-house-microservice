import os

from sqlalchemy import create_engine
from menu_service.models import Base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:11111111@localhost:5432/menu_db")
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
