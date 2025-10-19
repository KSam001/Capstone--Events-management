from django.db import models
from django.conf import settings

class Event(models.Model):
    """Represents an organized event."""
    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='hosted_events'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'time']
        unique_together = ('title', 'date', 'host')

    def __str__(self):
        return f"{self.title} on {self.date}"

class RSVP(models.Model):
    """Represents an attendee's RSVP to an event."""
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='rsvps'
    )
    attendee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='attended_events'
    )
    rsvped_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensures a user can only RSVP to an event once
        unique_together = ('event', 'attendee')

    def __str__(self):
        return f"{self.attendee.email} attending {self.event.title}"
