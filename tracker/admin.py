from django.contrib import admin

from .models import Tracker


@admin.register(Tracker)
class TrackerAdmin(admin.ModelAdmin):
    autocomplete_fields = ["requested_by", "updated_by",]
    list_display = ("ticket_id", "status", "created_on")
