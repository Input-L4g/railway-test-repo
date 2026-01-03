from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String

class Base(DeclarativeBase):
    pass

class TestItem(Base):
    __tablename__ = "test_items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
