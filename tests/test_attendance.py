import pytest
from django.urls import reverse
from attendance.models import Attendance
from attendance.qr_utils import generate_qr_token, verify_qr_token

pytestmark = pytest.mark.django_db


def test_qr_token_round_trip_and_tamper_detection(participant_user):
    token = generate_qr_token(participant_user.id)

    assert verify_qr_token(token) == participant_user.id
    assert verify_qr_token(f"{participant_user.id}:tampered") is None


def test_attendance_home_returns_qr_data_for_participant(client, participant_user):
    client.force_login(participant_user)

    response = client.get(reverse("attendance_home"))

    assert response.status_code == 200
    assert response.context["qr_token"].startswith(f"{participant_user.id}:")
    assert "qrserver.com" in response.context["qr_url"]


def test_event_attendance_denies_unassigned_volunteer(client, volunteer_user, managed_event):
    other_volunteer = volunteer_user.__class__.objects.create_user(
        username="stranger_volunteer",
        email="stranger@example.com",
        password="TestPass123!",
    )
    other_volunteer.fullName = "Stranger Volunteer"
    other_volunteer.phoneNumber = "7777777777"
    other_volunteer.role = "volunteer"
    other_volunteer.save()

    client.force_login(other_volunteer)

    response = client.get(reverse("event_attendance", args=[managed_event.id]))

    assert response.status_code == 302
    assert response.url == reverse("attendance_home")


def test_process_scan_creates_attendance_for_valid_qr(client, volunteer_user, managed_event, approved_managed_registration, participant_user):
    client.force_login(volunteer_user)
    token = generate_qr_token(participant_user.id)

    response = client.post(reverse("process_scan", args=[managed_event.id]), data={"token": token})

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "success"
    assert Attendance.objects.filter(user=participant_user, event=managed_event).exists()


def test_check_out_sets_checkout_time(client, volunteer_user, managed_event, approved_managed_registration, participant_user):
    attendance = Attendance.objects.create(
        user=participant_user,
        event=managed_event,
        registration=approved_managed_registration,
        checkedInBy=volunteer_user,
    )
    client.force_login(volunteer_user)

    response = client.get(reverse("check_out", args=[managed_event.id, participant_user.id]))

    assert response.status_code == 302
    attendance.refresh_from_db()
    assert attendance.checkOutTime is not None
