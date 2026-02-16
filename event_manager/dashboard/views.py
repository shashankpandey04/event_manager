from django.shortcuts import render
from attendance.models import Attendance
from registrations.models import Registration
from events.models import Event
from django.contrib.auth.decorators import login_required

@login_required(login_url="/auth/login")
def dashboard_view(request):
    
    user = request.user
    events = None
    myRegistrations = Registration.objects.filter(user=user)

    if user.role == "organizer":
        events = Event.objects.filter(organizer=user)

    elif user.role == "volunteer":
        events = Event.objects.filter(volunteers=user)

    else:
        events = Event.objects.all()

    context = {
        "events": events,
        "attendance_count": Attendance.objects.filter(user=user).count(),
        "myRegistrations": myRegistrations
    }

    return render(request, "dashboard/index.html", context)
