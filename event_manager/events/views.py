
from django.shortcuts import render
from .models import Event
from events.models import Event

def view_events(request):
    events = Event.objects.filter(status="published")
    return render(request, "events/view_events.html", {"events": events})