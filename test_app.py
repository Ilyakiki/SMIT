import pytest
from httpx import AsyncClient
from datetime import date
from app import app
from database import init_database, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

import asyncio
from anyio import run

@pytest.fixture(scope="session")
async def event_loop():
    """Исправление для конфликтующих циклов"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="module", autouse=True)
async def setup_database():
    """Инициализация базы данных перед выполнением тестов"""
    await init_database()


@pytest.fixture
async def client():
    """Фикстура для асинхронного клиента"""
    async with AsyncClient(app=app, base_url="http://0.0.0.0:8000") as ac:
        yield ac


@pytest.mark.asyncio
async def test_insert_rates(client):
    """Тест на добавление тарифов через /insert_rates"""
    rates_data = {
        "2024-11-19": [
            {"cargo_type": "Electronics", "rate": "1.5"},
            {"cargo_type": "Furniture", "rate": "2.0"}
        ],
        "2024-11-20": [
            {"cargo_type": "Other", "rate": "1.0"}
        ]
    }

    response = await client.post("/insert_rates", json=rates_data)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_price(client):
    """Тест на получение цены через /get_price"""
    rates_data = {
        "2024-11-19": [
            {"cargo_type": "Electronics", "rate": "1.5"},
        ]
    }
    await client.post("/insert_rates", json=rates_data)

    item_data = {
        "price": 100,
        "date": "2024-11-19",
        "cargo_type": "Electronics"
    }
    response = await client.post("/get_price", json=item_data)
    assert response.status_code == 200
    assert response.json() == 150.0


@pytest.mark.asyncio
async def test_get_price_with_fallback(client):
    """Тест на получение цены для типа 'Other' через /get_price"""
    # Вставляем тарифы перед проверкой
    rates_data = {
        "2024-11-19": [
            {"cargo_type": "Other", "rate": "1.0"},
        ]
    }
    await client.post("/insert_rates", json=rates_data)

    item_data = {
        "price": 200,
        "date": "2024-11-19",
        "cargo_type": "Unknown"
    }
    response = await client.post("/get_price", json=item_data)
    assert response.status_code == 200

