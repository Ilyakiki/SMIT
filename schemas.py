from pydantic import BaseModel, PositiveInt, RootModel
from typing import List, Dict
from datetime import date

# Определение Item модели
class Item(BaseModel):
    price: PositiveInt
    date: date
    cargo_type: str

# Определение RateItem модели
class RateItem(BaseModel):
    cargo_type: str
    rate: str

# Определение модели с корневым полем (RatesByDate)
class RatesByDate(RootModel):
    root: Dict[date, List[RateItem]]
