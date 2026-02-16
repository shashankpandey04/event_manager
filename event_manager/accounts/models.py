from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    ROLE_CHOICES = (
        ('organizer', 'Organizer'),
        ('volunteer', 'Volunteer'),
        ('participant', 'Participant'),
    )

    fullName = models.CharField(max_length=100)
    phoneNumber = models.CharField(max_length=15)
    dateOfBirth = models.DateField(null=True, blank=True)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='participant'
    )

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
