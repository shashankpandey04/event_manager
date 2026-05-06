# Test Suite Overview

This project now includes a pytest-based test suite under the root `tests/` folder. The suite uses a dedicated SQLite test settings module so the tests can run without connecting to the production MySQL database.

## Test Infrastructure

- `pytest.ini` configures pytest to use `event_manager.test_settings`.
- `event_manager/test_settings.py` overrides the database to SQLite and uses an in-memory email backend.
- `tests/conftest.py` contains reusable fixtures for users, events, registrations, attendance records, and QR helpers.

## Module Coverage

### `tests/test_accounts.py`
Covers the account flows:
- registration creates a new user and redirects to the dashboard
- login authenticates a valid user
- logout clears the session and redirects to login

### `tests/test_events.py`
Covers event management behavior:
- participants only see published events
- non-organizers are blocked from the create-event page
- organizers can create events
- organizers can add volunteers to an event
- organizers can delete their own events

### `tests/test_registrations.py`
Covers registration workflows:
- users can register for an event
- duplicate registrations are prevented at the view level
- participants can see their own registrations
- organizers can approve registrations
- organizers can reject registrations

### `tests/test_attendance.py`
Covers attendance and QR handling:
- QR tokens can be generated and verified
- tampered QR tokens are rejected
- participants receive QR data on the attendance home page
- unauthorized volunteers are redirected away from attendance pages
- valid QR scans create attendance rows
- check-out updates the attendance record

### `tests/test_dashboard.py`
Covers the dashboard module:
- organizers see their own events and QR data
- participants see their registrations and QR data

### `tests/test_admin_panel.py`
Covers admin-panel access control:
- participants see the unauthorized page
- organizers can access the admin dashboard

## Notes

- The suite focuses on the public behavior of each module rather than internal implementation details.
- The tests use Django’s test client, model factories built with fixtures, and QR token helpers.
- To run the suite from this workspace, activate the venv and point `PYTHONPATH` at the inner Django project directory:

```powershell
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& c:\Users\jpsha\OneDrive\Desktop\event_manager\venv\Scripts\Activate.ps1) ; $env:PYTHONPATH='c:\Users\jpsha\OneDrive\Desktop\event_manager\event_manager' ; python -m pytest -q tests
```
