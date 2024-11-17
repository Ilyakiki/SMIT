import uvicorn
from fastapi import FastAPI, Depends, Query
from fastapi import APIRouter
from typing import Optional,List
from sqlalchemy import select,insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import init_database,get_async_session
from schemas import *
from models import CargoRate
app = FastAPI()


@app.on_event("startup")
async def startup():
    await init_database()

@app.get("/")
async def test():
    return {"Hello": "World"}


@app.post("/insert_rates")
async def insert_rates(rates:RatesByDate, session:AsyncSession = Depends(get_async_session)):
    rates = dict(rates)
    for date in rates['root']:
        for rate in rates['root'][date]:
            await session.execute(insert(CargoRate).values(cargo_type=rate.cargo_type, rate=float(rate.rate), date=date))
    await session.commit()
    return {"ok":"ok"}

@app.post("/get_price")
async def get_price(item:Item, session:AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(CargoRate).where(CargoRate.cargo_type==item.cargo_type,CargoRate.date==item.date))
    rate = result.fetchone()
    return item.price*rate[0].rate

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)