from sqlalchemy import Column, Integer, Float, String, Date

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class CargoRate(Base):
    __tablename__ = 'CargoRate'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cargo_type = Column(String,nullable=False)
    date = Column(Date, nullable=False)
    rate = Column(Float, nullable=False)