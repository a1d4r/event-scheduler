from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app import settings
from app.events.routes import api


def create_app() -> FastAPI:
    """Create an instance of FastAPI application."""
    app = FastAPI(title='Event Scheduler')
    register_tortoise(app, config=settings.TORTOISE_ORM)
    app.include_router(api, prefix='/api', tags=['events'])
    return app


app = create_app()
