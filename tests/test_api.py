import pytest
from fastapi import status
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient

from app.events.schemas import (
    EventCreateSchema,
    EventSchema,
    SuggestedTimeIntervalSchema,
    SuggestedTimeIntervalsSchema,
    TimetableListSchema,
    TimetableSchema,
)
from tests.factories import (
    EventDataFactory,
    EventFactory,
    TimeIntervalDataFactory,
    TimeIntervalFactory,
    TimetableDataFactory,
    TimetableFactory,
)


@pytest.mark.asyncio
async def test_create_event(client: AsyncClient):
    event_data = EventDataFactory()

    response = await client.post('/api/events', json=jsonable_encoder(event_data))
    assert response.status_code == status.HTTP_200_OK

    retrieved_event_data = EventCreateSchema.parse_raw(response.text)
    assert event_data == retrieved_event_data


@pytest.mark.asyncio
async def test_create_event_invalid_boundaries(client: AsyncClient):
    event_data = EventDataFactory()
    event_data.start, event_data.end = event_data.end, event_data.start

    response = await client.post('/api/events', json=jsonable_encoder(event_data))
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_get_event(client: AsyncClient):
    event = await EventFactory()

    response = await client.get(f'/api/events/{event.id}')
    assert response.status_code == status.HTTP_200_OK

    actual_event_data = await EventSchema.from_tortoise_orm(event)
    retrieved_event_data = EventSchema.parse_raw(response.text)
    assert actual_event_data == retrieved_event_data


@pytest.mark.asyncio
async def test_get_nonexistent_event(client: AsyncClient):
    response = await client.get('/api/events/1234')
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_create_timetable(client: AsyncClient):
    event = await EventFactory()

    time_intervals_data = TimeIntervalDataFactory.create_batch(3)
    timetable_data = TimetableDataFactory(time_intervals=time_intervals_data)

    response = await client.post(
        f'/api/events/{event.id}/timetables', json=jsonable_encoder(timetable_data)
    )
    assert response.status_code == status.HTTP_200_OK

    retrieved_event_data = TimetableSchema.parse_raw(response.text)
    assert timetable_data == retrieved_event_data


@pytest.mark.asyncio
async def test_create_timetable_invalid_boundaries(client: AsyncClient):
    event = await EventFactory()

    time_interval_data = TimeIntervalDataFactory()
    time_interval_data.start, time_interval_data.end = (
        time_interval_data.end,
        time_interval_data.start,
    )
    timetable_data = TimetableDataFactory(time_intervals=[time_interval_data])

    response = await client.post(
        f'/api/events/{event.id}/timetables', json=jsonable_encoder(timetable_data)
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_timetable_for_nonexistent_event(client: AsyncClient):
    time_intervals_data = TimeIntervalDataFactory.create_batch(3)
    timetable_data = TimetableDataFactory(time_intervals=time_intervals_data)
    response = await client.post(
        '/api/events/1234/timetables', json=jsonable_encoder(timetable_data)
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_timetables(client: AsyncClient):
    event = await EventFactory()
    timetables = await TimetableFactory.create_batch(3, event=event)

    response = await client.get(f'/api/events/{event.id}/timetables')
    assert response.status_code == status.HTTP_200_OK

    actual_event_data = await TimetableListSchema.from_tortoise_models(timetables)
    retrieved_event_data = TimetableListSchema.parse_raw(response.text)
    assert actual_event_data == retrieved_event_data


@pytest.mark.asyncio
async def test_get_timetables_for_nonexistent_event(client: AsyncClient):
    response = await client.get('/api/events/1234/timetables')
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_suggested_time(client: AsyncClient):
    event = await EventFactory()
    timetable = await TimetableFactory(event=event)
    time_interval = await TimeIntervalFactory(timetable=timetable)

    response = await client.get(f'/api/events/{event.id}/time-suggestions')
    assert response.status_code == status.HTTP_200_OK

    retrieved_suggestions = SuggestedTimeIntervalsSchema.parse_raw(response.text)
    actual_time_interval = SuggestedTimeIntervalsSchema(
        __root__=[
            SuggestedTimeIntervalSchema(
                start=time_interval.start,
                end=time_interval.end,
                participants=[timetable.participant_name],
            )
        ]
    )
    assert retrieved_suggestions == actual_time_interval


@pytest.mark.asyncio
async def test_get_suggested_time_for_nonexistent_event(client: AsyncClient):
    response = await client.get('/api/events/1234/time-suggestions')
    assert response.status_code == status.HTTP_404_NOT_FOUND
