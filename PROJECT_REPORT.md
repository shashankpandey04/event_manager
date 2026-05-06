# Event Manager Project Report

## Cover Page

**Project Title:** Event Manager

**Type:** Django-based Event Management System

**Repository:** [event_manager](README.md)

**Prepared For:** Academic / Project Submission

**Prepared By:** Shashank Pandey

**Date:** May 6, 2026

---

## Introduction

Event Manager is a Django web application for creating, managing, registering for, and tracking events. It supports role-based access for admins, organizers, volunteers, and participants. The system also includes QR-based attendance tracking, event volunteer assignment, and user dashboards. The project is built with Django, MySQL, and a custom user model to support event workflows end to end.

## Problem Statement

Many small organizations still manage events through spreadsheets, messages, or disconnected tools.
Organizers struggle to track registrations, approvals, attendance, and volunteers in one place.
Participants often do not know which events are open, approved, or full.
Manual attendance causes delays, duplicate entries, and poor auditability.
Current solutions are either too generic, too expensive, or too complex for lightweight event operations.
This project addresses those gaps with a focused event workflow built around roles and QR attendance.
The goal is to provide a single system that simplifies event setup, participation, and reporting.

## Existing System Analysis

The current manual or semi-manual approach usually depends on forms, chat apps, spreadsheets, and ad hoc coordination. That approach works for very small events but becomes unreliable once there are multiple roles, registrations, and attendance checkpoints. It lacks strong validation, consistent approvals, and traceable attendance logs. The Event Manager system improves on this by centralizing the workflow and making the state of each event, registration, and attendance record visible.

## Requirements

### Functional Requirements

1. Users must be able to register, log in, and log out.
2. The system must support role-based access for admin, organizer, volunteer, and participant users.
3. Organizers must be able to create, edit, publish, and delete events.
4. Participants must be able to register and unregister for events.
5. Organizers must be able to approve or reject event registrations.
6. Volunteers and organizers must be able to manage event attendance.
7. The system must generate and verify QR tokens for attendance check-in.
8. Users must be able to view dashboards and registration or attendance history.

### Non-Functional Requirements

1. The system must keep attendance and registration data consistent with unique constraints.
2. The system must protect restricted actions through authentication and authorization.
3. The system must respond quickly enough for normal event operations and QR scans.
4. The system must remain maintainable through clear module separation and reusable views or models.
5. The system should be testable through automated unit and integration tests.
6. The system should be reliable when handling duplicate registrations or repeated attendance scans.

### Hardest Requirement

The hardest requirement to implement is secure QR-based attendance verification with duplicate prevention. It combines token generation, token validation, role checks, registration checks, and attendance constraints in a single flow, so a small mistake can cause false check-ins or rejected valid scans.

## Design

### Rough Design Before Coding

The system was designed around a modular Django structure with separate apps for accounts, events, registrations, attendance, dashboard, and admin panel. The data model centers on a custom user model, event records, registration records, and attendance records. The attendance flow uses signed QR tokens so that a volunteer can verify a participant securely at the event. Views are organized by module so each app owns its own logic, templates, and URLs.

### High Level Diagrams

- System architecture and module flow: [HLD.md](HLD.md)
- LLD flow diagrams: [LLD_DIA.md](LLD_DIA.md)
- UML diagrams: [LLD_UML.md](LLD_UML.md)
- High-level overview and design notes: [LLD.md](LLD.md)

### Data Models

The main data entities are documented in the existing design files, especially [LLD.md](LLD.md) and [LLD_UML.md](LLD_UML.md). The core models are:

- User: custom authentication and role field
- Event: event metadata, scheduling, status, volunteers, and capacity
- Registration: user-to-event registration with approval state
- Attendance: check-in and check-out records linked to registrations

### System Architecture

The application uses Django as the web framework, MySQL as the primary database in production settings, and Django templates for server-rendered pages. The app is split into functional modules so that each business capability is isolated and easier to maintain. The overall architecture is documented in [HLD.md](HLD.md).

### DFD Diagrams

The data-flow and process diagrams are already available in [LLD_DIA.md](LLD_DIA.md). These diagrams show the system data flow, registration workflow, event management flow, QR attendance flow, and role-based access paths.

## Testing Implementation

The project includes a dedicated test suite under [tests/](tests) and a written test guide in [tests.md](tests.md). The tests are organized by module and cover accounts, events, registrations, attendance, dashboard, and admin panel behavior. The suite was validated in the project virtual environment and passes successfully.

### Test Files

- Shared fixtures and setup: [tests/conftest.py](tests/conftest.py)
- Accounts tests: [tests/test_accounts.py](tests/test_accounts.py)
- Event tests: [tests/test_events.py](tests/test_events.py)
- Registration tests: [tests/test_registrations.py](tests/test_registrations.py)
- Attendance tests: [tests/test_attendance.py](tests/test_attendance.py)
- Dashboard tests: [tests/test_dashboard.py](tests/test_dashboard.py)
- Admin panel tests: [tests/test_admin_panel.py](tests/test_admin_panel.py)

## User Manual

The usage instructions are already documented in [README.md](README.md). In short:

1. Set up the virtual environment.
2. Install the dependencies.
3. Configure the environment variables.
4. Run migrations.
5. Create a superuser if needed.
6. Start the development server.

After login, organizers manage events, participants register for events, and volunteers help check attendance using the QR workflow.

## Source Code

The main source code is organized inside the Django project directory:

- Project settings and URL routing: [event_manager/event_manager/settings.py](event_manager/event_manager/settings.py)
- Main project URLs: [event_manager/event_manager/urls.py](event_manager/event_manager/urls.py)
- Accounts model: [event_manager/accounts/models.py](event_manager/accounts/models.py)
- Events model: [event_manager/events/models.py](event_manager/events/models.py)
- Registrations model: [event_manager/registrations/models.py](event_manager/registrations/models.py)
- Attendance model and QR utilities: [event_manager/attendance/models.py](event_manager/attendance/models.py) and [event_manager/attendance/qr_utils.py](event_manager/attendance/qr_utils.py)

For the full project structure, see [README.md](README.md).

## References

- Django documentation: https://docs.djangoproject.com/
- Pytest documentation: https://docs.pytest.org/
- Project overview: [README.md](README.md)
- Design documentation: [HLD.md](HLD.md), [LLD.md](LLD.md), [LLD_DIA.md](LLD_DIA.md), [LLD_UML.md](LLD_UML.md)
- Test documentation: [tests.md](tests.md)
