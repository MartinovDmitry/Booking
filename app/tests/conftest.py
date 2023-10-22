import asyncio
import json
from datetime import datetime

import pytest
import pytest_asyncio
from sqlalchemy import insert

from app.config import settings
from app.database import engine, Base, async_session_maker

from app.bookings.models import Booking
from app.main import app as fastapi_app
from app.rooms.models import Room
from app.hotels.models import Hotel
from app.users.models import User

from fastapi.testclient import TestClient
from httpx import AsyncClient


# @pytest_asyncio.fixture(autouse=True, scope='function')
# async def prepare_database():
#     assert settings.MODE == 'TEST'
#
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#
#     def model_mock_json(model: str):
#         with open(f'app/tests/mock_{model}.json', encoding='utf-8') as file:
#             return json.load(file)
#
#     hotels = model_mock_json('hotels')
#     rooms = model_mock_json('rooms')
#     bookings = model_mock_json('bookings')
#     users = model_mock_json('users')
#
#     for booking in bookings:
#         booking['date_from'] = datetime.strptime(booking['date_from'], '%Y-%m-%d')
#         booking['date_to'] = datetime.strptime(booking['date_to'], '%Y-%m-%d')
#
#     async with async_session_maker() as session:
#         add_hotels = insert(Hotel).values(hotels)
#         add_rooms = insert(Room).values(rooms)
#         add_users = insert(User).values(users)
#         add_bookings = insert(Booking).values(bookings)
#
#         await session.execute(add_hotels)
#         await session.execute(add_rooms)
#         await session.execute(add_users)
#         await session.execute(add_bookings)
#
#         await session.commit()
#
#     @pytest_asyncio.fixture(scope='session')
#     def event_loop(request):
#         loop = asyncio.get_event_loop_policy().new_event_loop()
#         yield loop
#         loop.close()


@pytest_asyncio.fixture(scope='function')
async def async_client():
    async with AsyncClient(app=fastapi_app, base_url='http://test') as ac:
        yield ac


@pytest_asyncio.fixture(scope='function')
async def authenticated_async_client():
    async with AsyncClient(app=fastapi_app, base_url='http://test') as auth_ac:
        await auth_ac.post('/auth/login', json={
            'email': 'Pavel@example.com',
            'password': 'Pavel',
        })
        assert auth_ac.cookies['booking_access_token']
        yield auth_ac


@pytest_asyncio.fixture(scope='function')
async def session():
    async with async_session_maker() as session:
        yield session
