import pytest
from httpx import AsyncClient
from tortoise.contrib.test import finalizer, initializer

from app.main import app
from app.settings import settings


@pytest.fixture(autouse=True)
def db():
    initializer(['app.events.models'], db_url=settings.DATABASE_TEST_URL)
    yield
    finalizer()


@pytest.fixture()
async def client():
    async with AsyncClient(app=app, base_url='http://test') as c:
        yield c
