from django.contrib import admin

from .models import Track, Course, Schedule, ScheduleRule, Pattern


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'code')
    search_fields = ('title', 'code', 'description')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'code')
    search_fields = ('title', 'code', 'instructor', 'description')


class PatternInline(admin.TabularInline):
    model = Pattern

@admin.register(ScheduleRule)
class ScheduleRuleAdmin(admin.ModelAdmin):
    list_display = ('course', 'session', 'start_date', 'end_date')
    list_filter = ('session', )
    filter_horizontal = ('tracks', )
    inlines = (PatternInline, )


@admin.register(Schedule)
class Schedule(admin.ModelAdmin):
    list_display = (
        'course','session', 'date',
        'start_time', 'end_time', 'type'
    )
    list_filter = ('session', 'date', 'type')
    filter_horizontal = ('tracks', )
