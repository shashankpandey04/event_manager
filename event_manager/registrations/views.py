
from django.shortcuts import render, redirect, get_object_or_404
from .models import Registration
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from events.models import Event

from django.http import HttpResponseRedirect

@login_required(login_url="/auth/login")
def my_registrations_view(request):
    user = request.user
    registrations = Registration.objects.filter(user=user)
    return render(request, "registrations/my_registrations.html", {"registrations": registrations})

@login_required(login_url="/auth/login")
def register_event_view(request, event_id):
    user = request.user
    event = get_object_or_404(Event, id=event_id)
    if Registration.objects.filter(user=user, event=event).exists():
        messages.info(request, "You are already registered for this event.")
        return redirect("registrations")
    Registration.objects.create(user=user, event=event)
    messages.success(request, "Registered for event successfully!")
    return redirect("registrations")

@login_required(login_url="/auth/login")
def unregister_event_view(request, event_id):
    user = request.user
    event = get_object_or_404(Event, id=event_id)
    reg = Registration.objects.filter(user=user, event=event).first()
    if reg:
        reg.delete()
        messages.success(request, "Unregistered from event successfully!")
    else:
        messages.info(request, "You are not registered for this event.")
    return redirect("registrations")