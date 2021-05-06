from tortoise import fields
from tortoise.models import Model


class Event(Model):
    """Event for which we are looking the most suitable time."""

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    start = fields.DatetimeField()
    end = fields.DatetimeField()
    duration = fields.TimeDeltaField()

    timetables: fields.ReverseRelation['Timetable']

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return f'<{type(self).__name__}(id={self.id}, name={self.name})>'


class Timetable(Model):
    """Participant name and all time intervals which are suitable for him/her."""

    id = fields.IntField(pk=True)
    participant_name = fields.CharField(max_length=100)

    event = fields.ForeignKeyField('models.Event', related_name='timetables')
    time_intervals: fields.ReverseRelation['TimeInterval']

    def __str__(self) -> str:
        return str(self.participant_name)

    def __repr__(self) -> str:
        return f'<{type(self).__name__}(id={self.id}, participant_name={self.participant_name})>'


class TimeInterval(Model):
    """Single time interval which is suitable for a participant."""

    id = fields.IntField(pk=True)
    start = fields.DatetimeField()
    end = fields.DatetimeField()

    timetable = fields.ForeignKeyField(
        'models.Timetable', related_name='time_intervals'
    )

    def __str__(self) -> str:
        return f'{self.start} - {self.end}'

    def __repr__(self) -> str:
        return f'<{type(self).__name__}(id={self.id})>'
