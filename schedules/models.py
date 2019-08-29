import pendulum
import uuid

from django.db import models


class Track(models.Model):
    title = models.CharField(max_length=120)
    code = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('id', )

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=120)
    code = models.CharField(max_length=30, unique=True)
    instructor = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('title', )

    def __str__(self):
        return self.title


class Schedule(models.Model):

    # Sessions
    DAY = 'DAY'
    EVENING = 'EVE'
    SESSION_CHOICES = (
        (DAY, 'Day'),
        (EVENING, 'Evening')
    )

    # Class Type
    REGULAR = 'REGULAR'
    MAKEUP = 'MAKEUP'
    TYPE_CHOICES = (
        (REGULAR, 'Regular'),
        (MAKEUP, 'Makeup')
    )

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    tracks = models.ManyToManyField(Track)
    session = models.CharField(max_length=3, choices=SESSION_CHOICES)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    type = models.TextField(
        max_length=10, choices=TYPE_CHOICES, default=REGULAR)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        default_related_name = 'schedules'
        ordering = ('-date', )

    def __str__(self):
        return f'{self.course.title} | {self.date}'


class ScheduleRule(models.Model):
    """
    Rule for generating a Schedule instance.
    """
    # Sessions
    DAY = 'DAY'
    EVENING = 'EVE'
    SESSION_CHOICES = (
        (DAY, 'Day'),
        (EVENING, 'Evening')
    )

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    tracks = models.ManyToManyField(Track)
    session = models.CharField(max_length=3, choices=SESSION_CHOICES)
    start_date = models.DateField(
        'rule start date',
        help_text='Date is inclusive.'
    )
    end_date = models.DateField(
        'rule end date',
        help_text='Date is inclusive.'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        default_related_name = 'rules'

    def __str__(self):
        return f'{self.course} <{self.start_date} - {self.end_date}>'

    def generate(self):
        """
        Generate a schedule from the rule
        """
        period = pendulum.period(self.start_date, self.end_date)
        for dt in period.range('days'):
            for pattern in self.patterns.all():
                if dt.day_of_week == pattern.day:
                    schedule, _ = Schedule.objects.get_or_create(
                        course=self.course,
                        session=self.session,
                        date=dt,
                        start_time=pattern.start_time,
                        end_time=pattern.end_time,
                    )
                    tracks = self.tracks.all()
                    schedule.tracks.set(tracks)


class Pattern(models.Model):
    """
    Schedule rule patterns
    """

    # Days
    SUNDAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6

    DAY_CHOICES = (
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday')
    )

    schedule = models.ForeignKey(ScheduleRule, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering= ('day', )
        default_related_name = 'patterns'
