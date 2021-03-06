from django.contrib import admin

from .models import Event


class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = ('title', 'registration_count', 'start_time', 'published',
                    'registration_open', 'submission_open',
                    'sessions_published')
    prepopulated_fields = {'slug': ("title",)}
    filter_horizontal = ('talkformat', )


admin.site.register(Event, EventAdmin)
