from datetime import datetime, timedelta
from typing import Any, Dict

from pydantic import Field, validator
from tortoise.contrib.pydantic.base import PydanticModel

from app.events.models import Event

__all__ = ['EventBaseSchema', 'EventCreateSchema', 'EventSchema']


class EventBaseSchema(PydanticModel):
    """Shared properties of event schemas."""

    name: str = Field(
        max_length=100, description='Name for the event.', example='Meeting'
    )
    start: datetime = Field(
        description='Starting point for the event datetime frame. '
        'Time intervals before it will not be considered.',
        example=datetime(2000, 1, 1, 8, 0, 0),
    )
    end: datetime = Field(
        description='Ending point for the event datetime frame. '
        'Time intervals after it will not be considered.',
        example=datetime(2000, 1, 1, 21, 0, 0),
    )
    duration: timedelta = Field(
        description='Duration of the event.', example=timedelta(hours=2)
    )

    @validator('end')
    def end_after_start(cls, v: datetime, values: Dict[str, Any]) -> datetime:
        if v <= values['start']:
            raise ValueError('end must be after start')
        return v

    class Config:
        orig_model = Event


class EventCreateSchema(EventBaseSchema):
    """Properties to receive on an event creation."""


class EventSchema(EventBaseSchema):
    """Event properties to return to a client."""

    id: int = Field(description='ID of the event', example=1)
