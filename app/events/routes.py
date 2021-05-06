from typing import List, Optional

from fastapi import APIRouter, HTTPException, status
from tortoise.contrib.pydantic import PydanticModel

from . import crud
from .schemas import (
    EventCreateSchema,
    EventSchema,
    SuggestedTimeIntervalSchema,
    TimetableListSchema,
    TimetableSchema,
)

api = APIRouter()


class EventNotFound(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, detail='Event not found'
        )


@api.get('/events/{event_id}', response_model=EventSchema)
async def get_event(event_id: int) -> PydanticModel:
    """Get an event by its id."""
    event = await crud.get_event(event_id)
    if not event:
        raise EventNotFound()
    return await EventSchema.from_tortoise_orm(event)


@api.post('/events', response_model=EventSchema)
async def create_event(event_data: EventCreateSchema) -> PydanticModel:
    """Create new event."""
    event = await crud.create_event(event_data)
    return await EventSchema.from_tortoise_orm(event)


@api.post('/events/{event_id}/timetables', response_model=TimetableSchema)
async def create_timetable(
    event_id: int, timetable_data: TimetableSchema
) -> PydanticModel:
    """Create a new timetable for the specified event."""
    event = await crud.get_event(event_id)
    if not event:
        raise EventNotFound()
    timetable = await crud.create_timetable(event, timetable_data)

    return await TimetableSchema.from_tortoise_orm(timetable)


@api.get('/events/{event_id}/timetables', response_model=TimetableListSchema)
async def get_timetables(event_id: int) -> TimetableListSchema:
    """Get timetables for the specified event."""
    event = await crud.get_event(event_id)
    if not event:
        raise EventNotFound()

    timetables = await crud.get_timetables(event)
    return await TimetableListSchema.from_tortoise_models(timetables)


@api.get(
    '/events/{event_id}/time-suggestions',
    response_model=List[SuggestedTimeIntervalSchema],
)
async def get_suggested_time(
    event_id: int, limit: Optional[int] = None
) -> list[SuggestedTimeIntervalSchema]:
    """Get the most suitable time intervals (by the number of active participants)."""
    event = await crud.get_event(event_id)
    if not event:
        raise EventNotFound()

    return await crud.get_suggested_time_intervals(event, limit)
