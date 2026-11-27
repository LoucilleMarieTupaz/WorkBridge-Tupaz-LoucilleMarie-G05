from django.db import models
from django.conf import settings


class HandoverEntry(models.Model):

    class Progress(models.TextChoices):
        NOT_STARTED = 'NOT_STARTED', 'Not Started'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'

    title = models.CharField(max_length=200)

    task_description = models.TextField()

    progress = models.CharField(
        max_length=20,
        choices=Progress.choices,
        default=Progress.NOT_STARTED
    )

    instructions = models.TextField()

    pending_work = models.TextField(blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='created_handover_entries'
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_handover_entries'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Handover Entry'
        verbose_name_plural = 'Handover Entries'