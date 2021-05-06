from datetime import datetime, timedelta

import pytest

from app.events.scheduler import Interval, Scheduler
from tests.factories import EventFactory, TimeIntervalFactory, TimetableFactory

sample_intervals = [
    Interval(*t)
    for t in [
        (datetime(2000, 1, 1, 9, 0, 0), (datetime(2000, 1, 1, 12, 0, 0)), 'user1'),
        (datetime(2000, 1, 1, 13, 0, 0), (datetime(2000, 1, 1, 14, 0, 0)), 'user1'),
        (datetime(2000, 1, 1, 16, 0, 0), (datetime(2000, 1, 1, 20, 0, 0)), 'user1'),
        (datetime(2000, 1, 1, 8, 0, 0), (datetime(2000, 1, 1, 11, 0, 0)), 'user2'),
        (datetime(2000, 1, 1, 12, 0, 0), (datetime(2000, 1, 1, 15, 0, 0)), 'user2'),
        (datetime(2000, 1, 1, 17, 0, 0), (datetime(2000, 1, 1, 21, 0, 0)), 'user2'),
        (datetime(2000, 1, 1, 8, 0, 0), (datetime(2000, 1, 1, 9, 0, 0)), 'user3'),
        (datetime(2000, 1, 1, 10, 0, 0), (datetime(2000, 1, 1, 12, 0, 0)), 'user3'),
        (datetime(2000, 1, 1, 13, 0, 0), (datetime(2000, 1, 1, 19, 0, 0)), 'user3'),
        (datetime(2000, 1, 1, 20, 0, 0), (datetime(2000, 1, 1, 21, 0, 0)), 'user3'),
        (datetime(2000, 1, 1, 8, 0, 0), (datetime(2000, 1, 1, 21, 0, 0)), 'user4'),
    ]
]


def test_scheduler_short_duration():
    scheduler = Scheduler(sample_intervals)
    result = scheduler.get_most_suitable_time_intervals(timedelta(hours=1), limit=3)
    assert result == [
        Interval(
            datetime(2000, 1, 1, 10, 0, 0),
            (datetime(2000, 1, 1, 11, 0, 0)),
            ['user1', 'user2', 'user3', 'user4'],
        ),
        Interval(
            datetime(2000, 1, 1, 13, 0, 0),
            (datetime(2000, 1, 1, 14, 0, 0)),
            ['user1', 'user2', 'user3', 'user4'],
        ),
        Interval(
            datetime(2000, 1, 1, 17, 0, 0),
            (datetime(2000, 1, 1, 19, 0, 0)),
            ['user1', 'user2', 'user3', 'user4'],
        ),
    ]


def test_scheduler_long_duration():
    scheduler = Scheduler(sample_intervals)
    result = scheduler.get_most_suitable_time_intervals(timedelta(hours=2), limit=1)
    assert result == [
        Interval(
            datetime(2000, 1, 1, 17, 0, 0),
            (datetime(2000, 1, 1, 19, 0, 0)),
            ['user1', 'user2', 'user3', 'user4'],
        ),
    ]


def test_scheduler_no_intervals():
    scheduler = Scheduler([])
    result = scheduler.get_most_suitable_time_intervals(timedelta(hours=2))
    assert result == []


@pytest.mark.asyncio
async def test_scheduler_from_event():
    event = await EventFactory()
    timetable = await TimetableFactory(event=event)
    time_interval = await TimeIntervalFactory(timetable=timetable)

    scheduler = await Scheduler.from_event(event)
    result = scheduler.get_most_suitable_time_intervals(timedelta(hours=2))
    assert result == [
        Interval(time_interval.start, time_interval.end, [timetable.participant_name])
    ]
