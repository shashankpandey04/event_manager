from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Event

User = get_user_model()

def is_organizer(user):
    return user.role in ('organizer', 'admin')

def view_events(request):
    user = request.user
    if user.is_authenticated and is_organizer(user):
        from django.db.models import Q
        events = Event.objects.filter(Q(organizer=user) | Q(status="published")).distinct()
    else:
        events = Event.objects.filter(status="published")

    # For volunteers, also pass their assigned events separately
    volunteer_events = []
    if user.is_authenticated and user.role == 'volunteer':
        volunteer_events = Event.objects.filter(volunteers=user, attendanceEnabled=True)

    return render(request, "events/view_events.html", {
        "events": events,
        "volunteer_events": volunteer_events,
    })

@login_required(login_url="/auth/login")
def create_event(request):
    if not is_organizer(request.user):
        return render(request, "events/create_event.html", {"error": "403"})
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        location = request.POST.get("location")
        start_time = request.POST.get("startTime")
        end_time = request.POST.get("endTime")
        capacity = request.POST.get("capacity") or None
        status = request.POST.get("status", "draft")
        Event.objects.create(
            title=title,
            description=description,
            location=location,
            startTime=start_time,
            endTime=end_time,
            capacity=capacity,
            status=status,
            organizer=request.user,
        )
        messages.success(request, "Event created successfully!")
        return redirect("view_events")
    return render(request, "events/create_event.html")

@login_required(login_url="/auth/login")
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if not is_organizer(request.user) or event.organizer != request.user:
        return render(request, "events/edit_event.html", {"error": "403", "event": event})
    if request.method == "POST":
        event.title = request.POST.get("title")
        event.description = request.POST.get("description")
        event.location = request.POST.get("location")
        event.startTime = request.POST.get("startTime")
        event.endTime = request.POST.get("endTime")
        event.capacity = request.POST.get("capacity") or None
        event.status = request.POST.get("status", event.status)
        event.attendanceEnabled = request.POST.get("attendanceEnabled") == "on"
        event.save()
        messages.success(request, "Event updated successfully!")
        return redirect("view_events")
    return render(request, "events/edit_event.html", {"event": event})

@login_required(login_url="/auth/login")
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if not is_organizer(request.user) or event.organizer != request.user:
        return render(request, "events/delete_event.html", {"error": "403", "event": event})
    if request.method == "POST":
        event.delete()
        messages.success(request, "Event deleted successfully!")
        return redirect("view_events")
    return render(request, "events/delete_event.html", {"event": event})

@login_required(login_url="/auth/login")
def manage_volunteers(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if not is_organizer(request.user) or event.organizer != request.user:
        messages.error(request, "You do not have permission to manage volunteers for this event.")
        return redirect("view_events")

    if request.method == "POST":
        action = request.POST.get("action")
        volunteer_id = request.POST.get("volunteer_id")
        volunteer = get_object_or_404(User, id=volunteer_id)
        if action == "add":
            event.volunteers.add(volunteer)
            messages.success(request, f"{volunteer.fullName or volunteer.username} added as volunteer.")
        elif action == "remove":
            event.volunteers.remove(volunteer)
            messages.success(request, f"{volunteer.fullName or volunteer.username} removed from volunteers.")
        return redirect("manage_volunteers", event_id=event_id)

    current_volunteers = event.volunteers.all()
    available_volunteers = User.objects.filter(role="volunteer").exclude(id__in=current_volunteers)

    return render(request, "events/manage_volunteers.html", {
        "event": event,
        "current_volunteers": current_volunteers,
        "available_volunteers": available_volunteers,
    })