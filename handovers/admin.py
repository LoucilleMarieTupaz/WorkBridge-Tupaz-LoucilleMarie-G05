from django.contrib import admin
from .models import HandoverEntry


@admin.register(HandoverEntry)
class HandoverEntryAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'progress',
        'created_by',
        'assigned_to',
        'created_at',
        'updated_at',
    )

    list_filter = (
        'progress',
        'created_at',
    )

    search_fields = (
        'title',
        'task_description',
        'instructions',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )