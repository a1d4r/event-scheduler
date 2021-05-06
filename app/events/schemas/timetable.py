from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field
from tortoise.contrib.pydantic.base import PydanticModel

from app.events.models import Timetable
from app.events.schemas import TimeIntervalSchema


class TimetableSchema(PydanticModel):
    """Properties of a timetable."""

    participant_name: Optional[str] = Field(
        max_length=100, description='Name of the participant.', example='John'
    )
    time_intervals: List[TimeIntervalSchema] = Field(
        description='List of time intervals which are suitable for the participant.',
        example=[
            {
                'start': datetime(2000, 1, 1, 9, 0, 0),
                'end': datetime(2000, 1, 1, 12, 0, 0),
            }
        ],
    )

    class Config:
        orig_model = Timetable


class TimetableListSchema(BaseModel):
    """List of timetables."""

    __root__: List[TimetableSchema]

    @classmethod
    async def from_tortoise_models(
        cls, timetables: List[Timetable]
    ) -> 'TimetableListSchema':
        return TimetableListSchema(
            __root__=[
                await TimetableSchema.from_tortoise_orm(timetable)
                for timetable in timetables
            ]
        )
