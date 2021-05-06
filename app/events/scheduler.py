from __future__ import annotations

from datetime import timedelta
from typing import Optional

from intervaltree import Interval, IntervalTree

from .models import Event


class Scheduler:
    """Scheduler for event looking for the most suitable time."""

    def __init__(self, intervals: list[Interval]):
        self._tree = IntervalTree()
        for interval in intervals:
            self._tree.add(interval)

    def get_most_suitable_time_intervals(
        self, duration: timedelta, limit: Optional[int] = None
    ) -> list[Interval]:
        """
        Get most suitable time intervals based on the number of active participants.
        Return not more than `limit` time intervals if specified.
        """
        # get interval boundaries
        boundaries = list(self._tree.boundary_table.keys())

        # check if tree is not empty
        if len(boundaries) < 2:
            return []
        result = []

        # find all intervals with length greater than duration
        # using two-pointers technique
        left, right = 0, 1
        while left < len(boundaries):
            # move right pointer until the interval has enough duration

            while (
                right < len(boundaries)
                and boundaries[right] - boundaries[left] < duration
            ):
                right += 1
            if (
                right == len(boundaries)
                or boundaries[right] - boundaries[left] < duration
            ):
                break

            # go through all intervals and intersect data (participants)
            participants = set.intersection(
                *(
                    {interval.data for interval in self._tree[start:end]}
                    for start, end in zip(
                        boundaries[left:right], boundaries[left + 1 : right + 1]
                    )
                )
            )
            result.append(
                Interval(boundaries[left], boundaries[right], sorted(participants))
            )
            left += 1

        # sort by number of active participants
        result.sort(key=lambda t: len(t.data), reverse=True)

        if limit:
            result = result[:limit]

        return result

    @classmethod
    async def from_event(cls, event: Event) -> Scheduler:
        """Create an instance of Scheduler from tortoise event model."""
        intervals = []
        await event.fetch_related('timetables__time_intervals')
        async for timetable in event.timetables:
            async for time_interval in timetable.time_intervals:
                intervals.append(
                    Interval(
                        time_interval.start,
                        time_interval.end,
                        timetable.participant_name,
                    )
                )
        return Scheduler(intervals)
