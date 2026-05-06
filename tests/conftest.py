from datetime import date, timedelta

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from attendance.models import Attendance
from events.models import Event
from registrations.models import Registration

User = get_user_model()
PASSWORD = "TestPass123!"


def create_user(username, email, role, full_name, phone_number="9999999999"):
    user = User.objects.create_user(
        username=username,
        email=email,
        password=PASSWORD,
    )
    user.fullName = full_name
    user.phoneNumber = phone_number
    user.dateOfBirth = date(1995, 1, 1)
    user.role = role
    user.save()
    return user


@pytest.fixture
def password():
    return PASSWORD


@pytest.fixture
def admin_user(db):
    return create_user("admin_user", "admin@example.com", "admin", "Admin User")


@pytest.fixture
def organizer_user(db):
    return create_user("organizer_user", "organizer@example.com", "organizer", "Organizer User")


@pytest.fixture
def volunteer_user(db):
    return create_user("volunteer_user", "volunteer@example.com", "volunteer", "Volunteer User")


@pytest.fixture
def participant_user(db):
    return create_user("participant_user", "participant@example.com", "participant", "Participant User")


@pytest.fixture
def other_organizer_user(db):
    return create_user("other_organizer", "other@example.com", "organizer", "Other Organizer")


@pytest.fixture
def draft_event(db, organizer_user):
    start_time = timezone.now() + timedelta(days=2)
    end_time = start_time + timedelta(hours=2)
    return Event.objects.create(
        title="Draft Event",
        description="Draft event description",
        organizer=organizer_user,
        location="Main Hall",
        startTime=start_time,
        endTime=end_time,
        status="draft",
        capacity=50,
    )


@pytest.fixture
def published_event(db, organizer_user):
    start_time = timezone.now() + timedelta(days=2)
    end_time = start_time + timedelta(hours=2)
    return Event.objects.create(
        title="Published Event",
        description="Published event description",
        organizer=organizer_user,
        location="Auditorium",
        startTime=start_time,
        endTime=end_time,
        status="published",
        capacity=100,
    )


@pytest.fixture
def other_published_event(db, other_organizer_user):
    start_time = timezone.now() + timedelta(days=3)
    end_time = start_time + timedelta(hours=3)
    return Event.objects.create(
        title="Other Organizer Event",
        description="Other event description",
        organizer=other_organizer_user,
        location="Conference Room",
        startTime=start_time,
        endTime=end_time,
        status="published",
        capacity=80,
    )


@pytest.fixture
def managed_event(db, organizer_user, volunteer_user):
    start_time = timezone.now() + timedelta(days=1)
    end_time = start_time + timedelta(hours=2)
    event = Event.objects.create(
        title="Managed Event",
        description="Managed event description",
        organizer=organizer_user,
        location="Exhibition Center",
        startTime=start_time,
        endTime=end_time,
        status="published",
        capacity=75,
    )
    event.volunteers.add(volunteer_user)
    return event


@pytest.fixture
def pending_registration(db, participant_user, published_event):
    return Registration.objects.create(
        user=participant_user,
        event=published_event,
        status="pending",
    )


@pytest.fixture
def approved_registration(db, participant_user, published_event):
    return Registration.objects.create(
        user=participant_user,
        event=published_event,
        status="approved",
    )


@pytest.fixture
def approved_managed_registration(db, participant_user, managed_event):
    return Registration.objects.create(
        user=participant_user,
        event=managed_event,
        status="approved",
    )


@pytest.fixture
def attendance_record(db, participant_user, published_event, approved_registration, volunteer_user):
    return Attendance.objects.create(
        user=participant_user,
        event=published_event,
        registration=approved_registration,
        checkedInBy=volunteer_user,
    )
