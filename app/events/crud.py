from typing import Optional

from .models import Event, TimeInterval, Timetable
from .scheduler import Scheduler
from .schemas import (
    EventCreateSchema,
    SuggestedTimeIntervalSchema,
    TimeIntervalSchema,
    TimetableSchema,
)


async def create_event(event_data: EventCreateSchema) -> Event:
    """
    Create new event from a schema.

    :param event_data: pydantic model
    :return: event - tortoise model
    """
    return await Event.create(**event_data.dict())


async def get_event(event_id: int) -> Optional[Event]:
    """
    Get an event by its id.

    :param event_id: id of an event
    :return: event - tortoise model
    """
    return await Event.get_or_none(pk=event_id)


async def create_time_interval(
    timetable: Timetable, time_interval_data: TimeIntervalSchema
) -> TimeInterval:
    """
    Create a time interval from a schema.

    :param timetable: associated timetable, tortoise model
    :param time_interval_data: pydantic model
    :return: timetable - tortoise model
    """
    return await TimeInterval.create(timetable=timetable, **time_interval_data.dict())


async def create_timetable(event: Event, timetable_data: TimetableSchema) -> Timetable:
    """
    Create a timetable from a schema.

    :param event: associated event
    :param timetable_data: pydantic model
    :return: timetable - tortoise model
    """
    timetable = await Timetable.create(
        event=event, **timetable_data.dict(exclude={'time_intervals'})
    )
    for time_interval_data in timetable_data.time_intervals:
        await create_time_interval(timetable, time_interval_data)
    return timetable


async def get_timetables(event: Event) -> list[Timetable]:
    """
    Get all timetables for the specified event.

    :param event: event tortoise model
    :return: list of timetables (tortoise models)
    """
    return await Timetable.filter(event=event)


async def get_suggested_time_intervals(
    event: Event, limit: Optional[int]
) -> list[SuggestedTimeIntervalSchema]:
    """
    Get a list of suggested time intervals (start, end, participants).
    The list is sorted in descending order by the number of active participants.

    :param event: event for which we are looking suitable time.
    :param limit: if specified only `limit` first time intervals will be returned.
    :return: list of suggested time intervals (pydantic models)
    """
    scheduler = await Scheduler.from_event(event)
    time_intervals = scheduler.get_most_suitable_time_intervals(event.duration, limit)
    return [
        SuggestedTimeIntervalSchema(start=start, end=end, participants=participants)
        for start, end, participants in time_intervals
    ]
