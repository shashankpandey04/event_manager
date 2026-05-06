from django.shortcuts import render, redirect, get_object_or_404
from .models import Registration
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from events.models import Event


@login_required(login_url="/auth/login")
def my_registrations_view(request):
    user = request.user
    # Organizers/admins see all registrations for their events
    if user.role in ('organizer', 'admin'):
        registrations = Registration.objects.filter(
            event__organizer=user
        ).select_related('user', 'event').order_by('event__title', '-registeredAt')
        context = {
            "registrations": registrations,
            "approved_count": registrations.filter(status="approved").count(),
            "pending_count": registrations.filter(status="pending").count(),
            "rejected_count": registrations.filter(status="rejected").count(),
        }
        return render(request, "registrations/manage_registrations.html", context)
    registrations = Registration.objects.filter(user=user).select_related('event')
    return render(request, "registrations/my_registrations.html", {"registrations": registrations})


@login_required(login_url="/auth/login")
def approve_registration(request, registration_id):
    reg = get_object_or_404(Registration, id=registration_id)
    if request.user.role not in ('organizer', 'admin') or reg.event.organizer != request.user:
        messages.error(request, "You do not have permission to do that.")
        return redirect("registrations")
    reg.status = "approved"
    reg.save()
    messages.success(request, f"{reg.user.fullName or reg.user.username}'s registration approved.")
    return redirect("registrations")


@login_required(login_url="/auth/login")
def reject_registration(request, registration_id):
    reg = get_object_or_404(Registration, id=registration_id)
    if request.user.role not in ('organizer', 'admin') or reg.event.organizer != request.user:
        messages.error(request, "You do not have permission to do that.")
        return redirect("registrations")
    reg.status = "rejected"
    reg.save()
    messages.success(request, f"{reg.user.fullName or reg.user.username}'s registration rejected.")
    return redirect("registrations")


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
