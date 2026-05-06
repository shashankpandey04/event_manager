import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()
pytestmark = pytest.mark.django_db


def test_register_view_creates_user_and_redirects_to_dashboard(client, password):
    response = client.post(
        reverse("register"),
        data={
            "fullName": "New Participant",
            "username": "new_participant",
            "email": "new@example.com",
            "phoneNumber": "8888888888",
            "dateOfBirth": "1996-01-01",
            "password": password,
            "confirmPassword": password,
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("dashboard")
    assert User.objects.filter(username="new_participant", role="participant").exists()
    assert client.session.get("_auth_user_id") is not None


def test_login_view_authenticates_valid_user(client, participant_user, password):
    response = client.post(
        reverse("login"),
        data={
            "username": participant_user.username,
            "password": password,
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("dashboard")
    assert str(participant_user.id) == client.session.get("_auth_user_id")


def test_logout_view_redirects_logged_in_user_to_login(client, participant_user):
    client.force_login(participant_user)

    response = client.get(reverse("logout"))

    assert response.status_code == 302
    assert response.url == reverse("login")
    assert client.session.get("_auth_user_id") is None
