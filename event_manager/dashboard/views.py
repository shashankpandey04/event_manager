from django.shortcuts import render
from attendance.models import Attendance
from attendance.qr_utils import generate_qr_token
from registrations.models import Registration
from events.models import Event
from django.contrib.auth.decorators import login_required


@login_required(login_url="/auth/login")
def dashboard_view(request):
    user = request.user
    events = None
    myRegistrations = Registration.objects.filter(user=user)

    if user.role in ("organizer", "admin"):
        events = Event.objects.filter(organizer=user)
    elif user.role == "volunteer":
        events = Event.objects.filter(volunteers=user)
    else:
        events = Event.objects.all()

    qr_token = generate_qr_token(user.id)
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={qr_token}"

    context = {
        "events": events,
        "attendance_count": Attendance.objects.filter(user=user).count(),
        "myRegistrations": myRegistrations,
        "qr_url": qr_url,
        "qr_token": qr_token,
    }

    return render(request, "dashboard/index.html", context)
