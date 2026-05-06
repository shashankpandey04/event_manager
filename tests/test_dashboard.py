import pytest
from django.urls import reverse
from attendance.models import Attendance
from registrations.models import Registration
from events.models import Event
from django.utils import timezone
from datetime import timedelta

pytestmark = pytest.mark.django_db


def test_dashboard_view_groups_events_by_organizer_and_includes_qr_data(client, organizer_user, other_organizer_user, participant_user):
    own_event = Event.objects.create(
        title="Organizer Own Event",
        description="Owned by organizer",
        organizer=organizer_user,
        location="Venue A",
        startTime=timezone.now() + timedelta(days=1),
        endTime=timezone.now() + timedelta(days=1, hours=2),
        status="published",
        capacity=30,
    )
    other_event = Event.objects.create(
        title="Another Organizer Event",
        description="Owned by someone else",
        organizer=other_organizer_user,
        location="Venue B",
        startTime=timezone.now() + timedelta(days=2),
        endTime=timezone.now() + timedelta(days=2, hours=2),
        status="published",
        capacity=40,
    )
    Registration.objects.create(user=organizer_user, event=own_event, status="approved")
    Attendance.objects.create(user=organizer_user, event=own_event, checkedInBy=organizer_user)
    client.force_login(organizer_user)

    response = client.get(reverse("dashboard"))

    assert response.status_code == 200
    events = list(response.context["events"])
    assert own_event in events
    assert other_event not in events
    assert response.context["qr_token"].startswith(f"{organizer_user.id}:")
    assert response.context["attendance_count"] == 1


def test_dashboard_view_for_participant_includes_registrations(client, participant_user, published_event):
    Registration.objects.create(user=participant_user, event=published_event, status="approved")
    client.force_login(participant_user)

    response = client.get(reverse("dashboard"))

    assert response.status_code == 200
    assert response.context["myRegistrations"].count() == 1
    assert response.context["myRegistrations"].first().event == published_event
    assert response.context["qr_token"].startswith(f"{participant_user.id}:")
