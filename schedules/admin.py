from django.contrib import admin

from .models import Track, Course, Schedule


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'code')
    search_fields = ('title', 'code', 'description')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'code')
    search_fields = ('title', 'code', 'instructor', 'description')


@admin.register(Schedule)
class Schedule(admin.ModelAdmin):
    list_display = ('course', 'session', 'date', 'start_time', 'end_time')
    list_filter = ('session', 'date')
    filter_horizontal = ('tracks', )