# Eventify — Event Manager Project

## Overview
Django 6.0.2 web app for managing events, registrations, attendance, and volunteers. Uses MySQL, Tailwind CSS (browser CDN), Lucide icons, and html5-qrcode for QR scanning.

## Stack
- **Backend:** Django 6.0.2, Python
- **Database:** MySQL (`django_db`, host `localhost:3306`, user `root`)
- **Frontend:** Tailwind CSS v4 (browser CDN), Lucide icons (unpkg CDN), html5-qrcode v2.3.8 (unpkg CDN)
- **Auth:** Custom `accounts.User` extending `AbstractUser`
- **Timezone:** Asia/Kolkata

## Running the project
```bash
cd event_manager
python manage.py runserver
```
Always run management commands from the `event_manager/` directory (where `manage.py` lives), not the workspace root.

## Environment variables
Copy `.env.template` to `.env` and fill in SMTP credentials. Required vars:
- `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_PORT`, `DEFAULT_FROM_EMAIL`

## Project structure
```
event_manager/          ← Django project root (contains manage.py)
  accounts/             ← Custom user model, auth views (register/login/logout)
  admin_panel/          ← Organizer/admin dashboard (was named 'admin', renamed to avoid Django conflict)
  attendance/           ← Attendance tracking, QR scan views
  dashboard/            ← Per-role dashboard
  events/               ← Event CRUD + volunteer management
  registrations/        ← Registration + approve/reject
  event_manager/        ← Django settings, root urls, base templates
```

## User roles
Stored in `accounts.User.role`. Four valid values:
- `admin` — full access, same permissions as organizer
- `organizer` — creates/manages events, approves registrations, manages volunteers
- `volunteer` — assigned to events by organizer, scans QR codes for attendance
- `participant` — registers for events, has a personal QR code for check-in

Role checks always use `user.role in ('organizer', 'admin')` — never just `== 'organizer'`.

## URL map
| Path | Name | Who |
|------|------|-----|
| `/` | `home` | All |
| `/auth/register/` | `register` | Public |
| `/auth/login/` | `login` | Public |
| `/auth/logout/` | `logout` | Authenticated |
| `/dashboard/` | `dashboard` | Authenticated |
| `/events/` | `view_events` | All |
| `/events/create/` | `create_event` | Organizer/Admin |
| `/events/<id>/edit/` | `edit_event` | Organizer/Admin (own events) |
| `/events/<id>/delete/` | `delete_event` | Organizer/Admin (own events) |
| `/events/<id>/volunteers/` | `manage_volunteers` | Organizer/Admin (own events) |
| `/registrations/` | `registrations` | Authenticated (role-branched) |
| `/registrations/<id>/approve/` | `approve_registration` | Organizer/Admin |
| `/registrations/<id>/reject/` | `reject_registration` | Organizer/Admin |
| `/register/<event_id>/` | `register_event` | Participant |
| `/unregister/<event_id>/` | `unregister_event` | Participant |
| `/attendance/` | `attendance_home` | Authenticated (role-branched) |
| `/attendance/<id>/` | `event_attendance` | Organizer/Volunteer |
| `/attendance/<id>/scan/` | `scan_qr` | Organizer/Volunteer |
| `/attendance/<id>/scan/process/` | `process_scan` | Organizer/Volunteer (POST/AJAX) |
| `/attendance/<id>/checkin/<uid>/` | `check_in` | Organizer/Volunteer |
| `/attendance/<id>/checkout/<uid>/` | `check_out` | Organizer/Volunteer |
| `/admin/` | `admin_dashboard` | Organizer/Admin |

## QR attendance flow
1. Every user has a unique HMAC-SHA256 signed token: `user_id:signature` (generated in `attendance/qr_utils.py`)
2. QR code is rendered via `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=<token>`
3. QR is shown on the dashboard (all roles) and on the attendance page (participants)
4. Volunteer/organizer opens `/attendance/<event_id>/scan/` → html5-qrcode scans the camera
5. Decoded token is POSTed to `/attendance/<event_id>/scan/process/` → server verifies HMAC, checks approved registration, creates `Attendance` record
6. `attendanceEnabled` must be `True` on the event for Scan QR / View List buttons to appear; organizers see all their events with a link to enable it

## Key models
- `accounts.User` — extends AbstractUser, adds `fullName`, `phoneNumber`, `dateOfBirth`, `role`
- `events.Event` — `title`, `organizer` (FK), `volunteers` (M2M), `status`, `attendanceEnabled`, `capacity`, `startTime`, `endTime`
- `registrations.Registration` — `user`, `event`, `status` (pending/approved/rejected/cancelled)
- `attendance.Attendance` — `user`, `event`, `registration` (OneToOne), `checkInTime`, `checkOutTime`, `checkedInBy`

## Templates
- Base template: `event_manager/event_manager/templates/base.html`
- App templates live in `<app>/templates/<app>/` (Django APP_DIRS convention)
- Tailwind is loaded via `<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>` in base.html — no build step needed
- Lucide icons: `<i data-lucide="icon-name">` + `lucide.createIcons()` called at end of base.html

## Conventions
- Login redirect: `login_url="/auth/login"` on all `@login_required` decorators
- Permission denied: render the same template with `{"error": "403"}` context, or `messages.error` + redirect
- Role-branched views (registrations, attendance): check `user.role` at the top and render different templates
- Always use `user.fullName or user.username` when displaying names (fullName can be blank for superusers)
- Migrations live in each app's `migrations/` folder; run `python manage.py migrate` from `event_manager/`
