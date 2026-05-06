from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Attendance
from .qr_utils import generate_qr_token, verify_qr_token
from events.models import Event
from registrations.models import Registration


def can_manage_attendance(user, event):
    """Organizer of the event, or a volunteer assigned to it."""
    if user.role in ('organizer', 'admin') and event.organizer == user:
        return True
    if user.role == 'volunteer' and event.volunteers.filter(id=user.id).exists():
        return True
    return False
@login_required(login_url="/auth/login")
def attendance_home(request):
    user = request.user
    if user.role in ('organizer', 'admin'):
        # Show all their events — attendanceEnabled is not a gate for seeing the page
        events = Event.objects.filter(organizer=user).order_by('-startTime')
    elif user.role == 'volunteer':
        events = Event.objects.filter(volunteers=user).order_by('-startTime')
    else:
        # Participants see their own attendance history
        attendances = Attendance.objects.filter(user=user).select_related('event')
        qr_token = generate_qr_token(user.id)
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={qr_token}"
        return render(request, 'attendance/my_attendance.html', {
            'attendances': attendances,
            'qr_url': qr_url,
            'qr_token': qr_token,
        })

    return render(request, 'attendance/attendance_home.html', {'events': events})


@login_required(login_url="/auth/login")
def event_attendance(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    if not can_manage_attendance(user, event):
        messages.error(request, "You do not have permission to manage attendance for this event.")
        return redirect('attendance_home')

    registrations = Registration.objects.filter(
        event=event, status='approved'
    ).select_related('user')

    checked_in_ids = set(
        Attendance.objects.filter(event=event).values_list('user_id', flat=True)
    )

    attendance_data = []
    for reg in registrations:
        attendance = Attendance.objects.filter(user=reg.user, event=event).first()
        attendance_data.append({
            'user': reg.user,
            'checked_in': reg.user.id in checked_in_ids,
            'attendance': attendance,
        })

    return render(request, 'attendance/event_attendance.html', {
        'event': event,
        'attendance_data': attendance_data,
        'total': len(attendance_data),
        'checked_in_count': len(checked_in_ids),
    })


@login_required(login_url="/auth/login")
def scan_qr(request, event_id):
    """Page with camera QR scanner for volunteers/organizers."""
    event = get_object_or_404(Event, id=event_id)
    if not can_manage_attendance(request.user, event):
        messages.error(request, "You do not have permission to scan attendance for this event.")
        return redirect('attendance_home')
    return render(request, 'attendance/scan_qr.html', {'event': event})


@login_required(login_url="/auth/login")
@require_POST
def process_scan(request, event_id):
    """AJAX endpoint — receives a QR token, marks check-in, returns JSON."""
    from django.contrib.auth import get_user_model
    User = get_user_model()

    event = get_object_or_404(Event, id=event_id)

    if not can_manage_attendance(request.user, event):
        return JsonResponse({'status': 'error', 'message': 'Permission denied.'}, status=403)

    token = request.POST.get('token', '').strip()
    user_id = verify_qr_token(token)

    if user_id is None:
        return JsonResponse({'status': 'error', 'message': 'Invalid or tampered QR code.'}, status=400)

    try:
        participant = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found.'}, status=404)

    # Check they have an approved registration
    registration = Registration.objects.filter(
        user=participant, event=event, status='approved'
    ).first()

    if not registration:
        return JsonResponse({
            'status': 'error',
            'message': f'{participant.fullName or participant.username} does not have an approved registration for this event.',
        }, status=400)

    # Already checked in?
    if Attendance.objects.filter(user=participant, event=event).exists():
        return JsonResponse({
            'status': 'already',
            'message': f'{participant.fullName or participant.username} is already checked in.',
            'name': participant.fullName or participant.username,
        })

    Attendance.objects.create(
        user=participant,
        event=event,
        registration=registration,
        checkedInBy=request.user,
    )

    return JsonResponse({
        'status': 'success',
        'message': f'{participant.fullName or participant.username} checked in successfully!',
        'name': participant.fullName or participant.username,
    })


@login_required(login_url="/auth/login")
def check_in(request, event_id, user_id):
    from django.contrib.auth import get_user_model
    User = get_user_model()

    event = get_object_or_404(Event, id=event_id)
    participant = get_object_or_404(User, id=user_id)

    if not can_manage_attendance(request.user, event):
        messages.error(request, "You do not have permission to do that.")
        return redirect('attendance_home')

    registration = Registration.objects.filter(user=participant, event=event, status='approved').first()

    if Attendance.objects.filter(user=participant, event=event).exists():
        messages.info(request, f"{participant.fullName or participant.username} is already checked in.")
    else:
        Attendance.objects.create(
            user=participant,
            event=event,
            registration=registration,
            checkedInBy=request.user,
        )
        messages.success(request, f"{participant.fullName or participant.username} checked in successfully.")

    return redirect('event_attendance', event_id=event_id)


@login_required(login_url="/auth/login")
def check_out(request, event_id, user_id):
    from django.contrib.auth import get_user_model
    User = get_user_model()

    event = get_object_or_404(Event, id=event_id)
    participant = get_object_or_404(User, id=user_id)

    if not can_manage_attendance(request.user, event):
        messages.error(request, "You do not have permission to do that.")
        return redirect('attendance_home')

    attendance = Attendance.objects.filter(user=participant, event=event).first()
    if attendance:
        if attendance.checkOutTime:
            messages.info(request, f"{participant.fullName or participant.username} is already checked out.")
        else:
            attendance.checkOutTime = timezone.now()
            attendance.save()
            messages.success(request, f"{participant.fullName or participant.username} checked out.")
    else:
        messages.warning(request, f"{participant.fullName or participant.username} was not checked in.")

    return redirect('event_attendance', event_id=event_id)
