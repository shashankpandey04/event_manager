import pytest
from django.urls import reverse
from registrations.models import Registration

pytestmark = pytest.mark.django_db


def test_register_event_creates_pending_registration(client, participant_user, published_event):
    client.force_login(participant_user)

    response = client.post(reverse("register_event", args=[published_event.id]))

    assert response.status_code == 302
    assert response.url == reverse("registrations")
    assert Registration.objects.filter(
        user=participant_user,
        event=published_event,
        status="pending",
    ).exists()


def test_duplicate_registration_does_not_create_second_row(client, participant_user, published_event):
    Registration.objects.create(user=participant_user, event=published_event, status="pending")
    client.force_login(participant_user)

    response = client.post(reverse("register_event", args=[published_event.id]))

    assert response.status_code == 302
    assert Registration.objects.filter(user=participant_user, event=published_event).count() == 1


def test_my_registrations_view_shows_participant_rows(client, participant_user, pending_registration):
    client.force_login(participant_user)

    response = client.get(reverse("registrations"))

    assert response.status_code == 200
    registrations = list(response.context["registrations"])
    assert pending_registration in registrations


def test_approve_registration_updates_status_for_owner(client, organizer_user, pending_registration):
    client.force_login(organizer_user)

    response = client.get(reverse("approve_registration", args=[pending_registration.id]))

    assert response.status_code == 302
    pending_registration.refresh_from_db()
    assert pending_registration.status == "approved"


def test_reject_registration_updates_status_for_owner(client, organizer_user, published_event, participant_user):
    registration = Registration.objects.create(
        user=participant_user,
        event=published_event,
        status="pending",
    )
    client.force_login(organizer_user)

    response = client.get(reverse("reject_registration", args=[registration.id]))

    assert response.status_code == 302
    registration.refresh_from_db()
    assert registration.status == "rejected"
