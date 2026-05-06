import pytest
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from events.models import Event

pytestmark = pytest.mark.django_db


def _event_post_data(title="Launch Summit"):
    start_time = (timezone.now() + timedelta(days=4)).isoformat()
    end_time = (timezone.now() + timedelta(days=4, hours=2)).isoformat()
    return {
        "title": title,
        "description": "Event created from test suite",
        "location": "Grand Hall",
        "startTime": start_time,
        "endTime": end_time,
        "capacity": "120",
        "status": "draft",
    }


def test_view_events_shows_only_published_events_to_participant(client, participant_user, draft_event, published_event):
    client.force_login(participant_user)

    response = client.get(reverse("view_events"))

    assert response.status_code == 200
    events = list(response.context["events"])
    assert published_event in events
    assert draft_event not in events


def test_create_event_rejects_non_organizer(client, participant_user):
    client.force_login(participant_user)

    response = client.get(reverse("create_event"))

    assert response.status_code == 200
    assert response.context["error"] == "403"


def test_create_event_persists_event_for_organizer(client, organizer_user):
    client.force_login(organizer_user)

    response = client.post(reverse("create_event"), data=_event_post_data())

    assert response.status_code == 302
    assert response.url == reverse("view_events")
    assert Event.objects.filter(title="Launch Summit", organizer=organizer_user, status="draft").exists()


def test_manage_volunteers_adds_volunteer_to_event(client, organizer_user, volunteer_user, published_event):
    client.force_login(organizer_user)

    response = client.post(
        reverse("manage_volunteers", args=[published_event.id]),
        data={"action": "add", "volunteer_id": volunteer_user.id},
    )

    assert response.status_code == 302
    published_event.refresh_from_db()
    assert volunteer_user in published_event.volunteers.all()


def test_delete_event_removes_owned_event(client, organizer_user):
    event = Event.objects.create(
        title="Delete Me",
        description="To be removed",
        organizer=organizer_user,
        location="Room 1",
        startTime=timezone.now() + timedelta(days=5),
        endTime=timezone.now() + timedelta(days=5, hours=1),
        status="draft",
        capacity=25,
    )
    client.force_login(organizer_user)

    response = client.post(reverse("delete_event", args=[event.id]))

    assert response.status_code == 302
    assert response.url == reverse("view_events")
    assert not Event.objects.filter(id=event.id).exists()
