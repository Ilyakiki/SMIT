from pydantic import BaseModel, PositiveInt, RootModel, constr
from typing import List, Dict
from datetime import date


rate_regex= r"^\d+(\.\d+)?$"

# Определение Item модели
class Item(BaseModel):
    price: PositiveInt
    date: date
    cargo_type: str

# Определение RateItem модели
class RateItem(BaseModel):
    cargo_type: str
    rate: constr(pattern=rate_regex)


class RatesByDate(RootModel):
    root: Dict[date, List[RateItem]]
