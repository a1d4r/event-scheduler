from datetime import datetime, timedelta, timezone

import pytest

from app.events.models import Event, TimeInterval, Timetable
from tests.factories import EventFactory, TimeIntervalFactory, TimetableFactory


@pytest.mark.asyncio
async def test_time_interval():
    timetable = await TimetableFactory()
    start = datetime.now(timezone.utc)
    end = start + timedelta(hours=1)

    time_interval = await TimeInterval.create(start=start, end=end, timetable=timetable)
    assert time_interval.start == start
    assert time_interval.end == end
    assert str(time_interval) == f'{start} - {end}'
    assert repr(time_interval) == f'<TimeInterval(id={time_interval.id})>'


@pytest.mark.asyncio
async def test_timetable():
    event = await EventFactory()
    name = 'Name'

    timetable = await Timetable.create(participant_name=name, event=event)

    assert timetable.participant_name == name
    assert str(timetable) == name
    assert repr(timetable) == f'<Timetable(id={timetable.id}, participant_name={name})>'


@pytest.mark.asyncio
async def test_event():
    name = 'Event'
    start = datetime.now(timezone.utc)
    end = start + timedelta(days=3)
    duration = timedelta(hours=1)

    event = await Event.create(name=name, start=start, end=end, duration=duration)

    assert event.start == start
    assert event.end == end
    assert event.name == name
    assert event.duration == duration
    assert str(event) == name
    assert repr(event) == f'<Event(id={event.id}, name={event.name})>'


@pytest.mark.asyncio
async def test_event_with_timetables():
    event = await EventFactory()
    timetables = await TimetableFactory.create_batch(3, event=event)

    assert await event.timetables.all() == timetables


@pytest.mark.asyncio
async def test_timetable_with_time_intervals():
    timetable = await TimetableFactory()
    time_intervals = await TimeIntervalFactory.create_batch(3, timetable=timetable)

    assert await timetable.time_intervals.all() == time_intervals
