import asyncio
import inspect
from datetime import timedelta, timezone

import factory

from app.events.models import Event, TimeInterval, Timetable
from app.events.schemas import EventCreateSchema, TimeIntervalSchema, TimetableSchema


# https://github.com/FactoryBoy/factory_boy/issues/679#issuecomment-673960170
class TortoiseModelFactory(factory.Factory):
    """Asynchronous factory for creating tortoise model."""

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        async def maker_coroutine():
            for key, value in kwargs.items():
                if inspect.isawaitable(value):
                    kwargs[key] = await value
            return await model_class.create(*args, **kwargs)

        return asyncio.create_task(maker_coroutine())

    @classmethod
    async def create_batch(cls, size, **kwargs):  # pylint: disable=W0236
        return [await cls.create(**kwargs) for _ in range(size)]


class EventDataFactory(factory.Factory):
    """Factory for creating pydantic event model based on schema."""

    class Meta:
        model = EventCreateSchema

    name = factory.Faker('text', max_nb_chars=30)
    start = factory.Faker('date_time', tzinfo=timezone.utc)
    end = factory.LazyAttribute(lambda obj: obj.start + obj.time_delta)
    duration = factory.Faker('time_delta', end_datetime=timedelta(hours=3))

    class Params:
        time_delta = timedelta(days=3)


class EventFactory(TortoiseModelFactory, EventDataFactory):
    """Factory for creating event tortoise model."""

    class Meta:
        model = Event


class TimetableDataFactory(factory.Factory):
    """Factory for creating timetable pydantic model based on schema."""

    class Meta:
        model = TimetableSchema

    participant_name = factory.Faker('name')


class TimetableFactory(TortoiseModelFactory, TimetableDataFactory):
    """Factory for creating timetable tortoise model."""

    class Meta:
        model = Timetable

    event = factory.SubFactory(EventFactory)


class TimeIntervalDataFactory(factory.Factory):
    """Factory for creating time interval pydantic model base on schema."""

    class Meta:
        model = TimeIntervalSchema

    start = factory.Faker('date_time', tzinfo=timezone.utc)
    end = factory.LazyAttribute(lambda obj: obj.start + obj.time_delta)

    class Params:
        time_delta = timedelta(days=3)


class TimeIntervalFactory(TortoiseModelFactory, TimeIntervalDataFactory):
    """Factory for creating time interval tortoise model."""

    class Meta:
        model = TimeInterval

    timetable = factory.SubFactory(TimetableFactory)
