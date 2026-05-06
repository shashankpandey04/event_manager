import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_admin_dashboard_shows_unauthorized_page_for_participant(client, participant_user):
    client.force_login(participant_user)

    response = client.get(reverse("admin_dashboard"))

    assert response.status_code == 200
    assert "Access Denied" in response.content.decode()


def test_admin_dashboard_allows_organizer(client, organizer_user):
    client.force_login(organizer_user)

    response = client.get(reverse("admin_dashboard"))

    assert response.status_code == 200
    assert "Access Denied" not in response.content.decode()
