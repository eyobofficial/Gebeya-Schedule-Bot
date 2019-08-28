import uuid

from django.db import models


class Track(models.Model):
    title = models.CharField(max_length=120)
    code = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('title', )

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=120)
    code = models.CharField(max_length=30, unique=True)
    instructor = models.CharField(max_length=120)
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

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    tracks = models.ManyToManyField(Track)
    session = models.CharField(max_length=3, choices=SESSION_CHOICES)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        default_related_name = 'schedules'
        ordering = ('-date', )

    def __str__(self):
        return f'{self.course.title} | {self.date}'
