from sqlalchemy import Column, Integer, Float, String, Date, UniqueConstraint

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class CargoRate(Base):
    __tablename__ = 'CargoRate'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cargo_type = Column(String,nullable=False)
    date = Column(Date, nullable=False)
    rate = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint('date', 'cargo_type', name='uix_date_cargo_type'),
    )