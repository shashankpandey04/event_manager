from django.db import models
from django.conf import settings
from events.models import Event
from registrations.models import Registration

User = settings.AUTH_USER_MODEL


class Attendance(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="attendances"
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="attendances"
    )

    registration = models.OneToOneField(
        Registration,
        on_delete=models.CASCADE,
        related_name="attendance",
        null=True,
        blank=True
    )

    checkInTime = models.DateTimeField(auto_now_add=True)
    checkOutTime = models.DateTimeField(null=True, blank=True)

    checkedInBy = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="scanned_attendances"
    )

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "event"],
                name="unique_attendance_per_event"
            )
        ]

    def __str__(self):
        return f"{self.user} @ {self.event}"
