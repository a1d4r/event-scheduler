import pytest

from app.events.crud import create_event, create_timetable, get_event, get_timetables
from app.events.schemas import EventCreateSchema, TimetableSchema
from tests.factories import (
    EventDataFactory,
    EventFactory,
    TimeIntervalDataFactory,
    TimetableDataFactory,
    TimetableFactory,
)


@pytest.mark.asyncio
async def test_create_event():
    event_data = EventDataFactory()

    event = await create_event(event_data)

    saved_event_data = await EventCreateSchema.from_tortoise_orm(event)
    assert event_data == saved_event_data


@pytest.mark.asyncio
async def test_get_event():
    saved_event = await EventFactory()

    retrieved_event = await get_event(saved_event.id)

    assert retrieved_event == saved_event


@pytest.mark.asyncio
async def test_create_timetable():
    saved_event = await EventFactory()

    time_intervals_data = TimeIntervalDataFactory.create_batch(3)
    timetable_data = TimetableDataFactory(time_intervals=time_intervals_data)

    timetable = await create_timetable(saved_event, timetable_data)
    saved_timetable_data = await TimetableSchema.from_tortoise_orm(timetable)
    assert timetable_data == saved_timetable_data


@pytest.mark.asyncio
async def test_get_timetables():
    event = await EventFactory()
    timetables = await TimetableFactory.create_batch(3, event=event)

    retrieved_timetables = await get_timetables(event)

    assert timetables == retrieved_timetables
