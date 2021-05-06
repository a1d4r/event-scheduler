from datetime import datetime
from typing import Any, Dict, List

from pydantic import BaseModel, Field, validator
from tortoise.contrib.pydantic.base import PydanticModel

from app.events.models import TimeInterval


class TimeIntervalSchema(PydanticModel):
    """Properties of a time interval."""

    start: datetime = Field(
        description='Start of the time interval.',
        example=datetime(2000, 1, 1, 9, 0, 0),
    )
    end: datetime = Field(
        description='End of the time interval.',
        example=datetime(2000, 1, 1, 12, 0, 0),
    )

    @validator('end')
    def end_after_start(cls, v: datetime, values: Dict[str, Any]) -> datetime:
        if v <= values['start']:
            raise ValueError('end must be after start')
        return v

    class Config:
        orig_model = TimeInterval


class SuggestedTimeIntervalSchema(TimeIntervalSchema):
    """Properties of suggested time interval."""

    participants: List[str] = Field(
        description='List of names of participants for which this time interval is suitable.',
        example=['John', 'Carolina'],
    )


class SuggestedTimeIntervalsSchema(BaseModel):
    """List of suggested time intervals."""

    __root__: List[SuggestedTimeIntervalSchema]
