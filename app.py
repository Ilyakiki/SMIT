import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import init_database, get_async_session
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
            insert_stmt = insert(CargoRate).values(
                cargo_type=rate.cargo_type.title(),
                rate=float(rate.rate),
                date=date
            )

            insert_stmt = insert_stmt.on_conflict_do_update(
                index_elements=['date', 'cargo_type'],  # Указываем, по каким столбцам будет проверяться конфликт
                set_={'rate': float(rate.rate)}  # Обновляем поле rate при конфликте
            )

            await session.execute(insert_stmt)
    await session.commit()
    return {"message": "OK"}, status.HTTP_200_OK

@app.post("/get_price")
async def get_price(item:Item, session:AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(CargoRate).where(CargoRate.cargo_type==item.cargo_type.title(),CargoRate.date==item.date))
    rate = result.first()

    if rate:
        return item.price*rate[0].rate

    result = await session.execute(
        select(CargoRate).where(CargoRate.cargo_type == "Other", CargoRate.date == item.date))
    rate = result.first()

    if rate:
        return item.price*rate[0].rate

    raise HTTPException(status_code=404, detail="Rate not found for the given date and cargo type")


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)