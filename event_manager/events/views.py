
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from events.models import Event

@login_required(login_url="/auth/login")
def create_event(request):
    user = request.user
    if user.role != "organizer":
        return render(request, "events/create_event.html", {"error": "403"})
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        location = request.POST.get("location")
        startTime = request.POST.get("startTime")
        endTime = request.POST.get("endTime")
        capacity = request.POST.get("capacity")
        event = Event.objects.create(
            title=title,
            description=description,
            location=location,
            startTime=startTime,
            endTime=endTime,
            capacity=capacity,
            organizer=user
        )
        messages.success(request, "Event created successfully!")
        return redirect("view_events")
    return render(request, "events/create_event.html")

@login_required(login_url="/auth/login")
def edit_event(request, event_id):
    user = request.user
    event = get_object_or_404(Event, id=event_id, organizer=user)
    if user.role != "organizer":
        return render(request, "events/edit_event.html", {"error": "403"})
    if request.method == "POST":
        event.title = request.POST.get("title")
        event.description = request.POST.get("description")
        event.location = request.POST.get("location")
        event.startTime = request.POST.get("startTime")
        event.endTime = request.POST.get("endTime")
        event.capacity = request.POST.get("capacity")
        event.save()
        messages.success(request, "Event updated successfully!")
        return redirect("view_events")
    return render(request, "events/edit_event.html", {"event": event})

def view_events(request):
    user = request.user
    if user.is_authenticated:
        if user.role == "organizer":
            events = Event.objects.filter(organizer=user)
        else:
            events = Event.objects.filter(
                status__in=["published", "expired"]
            )
    else:
        events = Event.objects.filter(status="published")
    return render(request, "events/view_events.html", {"events": events})

@login_required(login_url="/auth/login")
def delete_event(request, event_id):
    user = request.user
    event = get_object_or_404(Event, id=event_id, organizer=user)
    if user.role != "organizer":
        return render(request, "events/delete_event.html", {"error": "403"})
    if request.method == "POST":
        event.delete()
        messages.success(request, "Event deleted successfully!")
        return redirect("view_events")
    return render(request, "events/delete_event.html", {"event": event})