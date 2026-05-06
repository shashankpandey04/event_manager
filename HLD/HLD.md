# High-Level Design (HLD) - Event Manager System

## 1. System Overview

The Event Manager is a Django-based web application that enables organizations to create, manage, and track events with comprehensive features including user registration, QR code-based attendance tracking, volunteer management, and role-based access control.

## 2. System Architecture

### 2.1 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Client Layer (Browser)                   │
│                         (HTML/CSS/JS)                       │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                   Django Application Layer                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │               URL Router (urls.py)                   │   │
│  └────────────────┬────────────────────────────────────┘   │
│                   │                                         │
│  ┌────────────────▼──────────────────────────────────┐      │
│  │          Application Modules                      │      │
│  │ ┌──────────┬──────────┬────────┬──────────┬────┐  │      │
│  │ │Accounts  │Dashboard │Events  │Attend.   │Reg.│  │      │
│  │ │          │          │        │          │    │  │      │
│  │ │- Auth    │- Views   │- CRUD  │- QR Gen  │-   │  │      │
│  │ │- User    │- Charts  │- Vol.  │- Scan    │Mgmt│  │      │
│  │ │- Roles   │- Stats   │- Status│- Track   │    │  │      │
│  │ └──────────┴──────────┴────────┴──────────┴────┘  │      │
│  └──────────────────────────────────────────────────┘       │
│                        │                                    │
│                        │ Models & Views                     │
│  ┌─────────────────────▼──────────────────────────┐        │
│  │         Admin Panel & Authentication            │        │
│  │  - Admin Dashboard                              │        │
│  │  - User Management                              │        │
│  │  - Permission Control                           │        │
│  └──────────────────────────────────────────────────┘      │
└──────────────────────────┬───────────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────────┐
│                   Data Access Layer                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Django ORM                              │   │
│  │  (Object-Relational Mapping)                         │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────┬───────────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────────┐
│                   Database Layer                             │
│              MySQL Database                                  │
│  - Users & Roles                                             │
│  - Events & Registrations                                    │
│  - Attendance Records                                        │
│  - Event Details & Metadata                                  │
└──────────────────────────────────────────────────────────────┘
```

## 3. Core Components

### 3.1 Accounts Module
**Purpose**: User authentication and profile management

**Responsibilities**:
- User registration and login
- User profile management
- Role assignment (Admin, Organizer, Volunteer, Participant)
- Authentication and session management

**Key Features**:
- Custom User model extending Django's AbstractUser
- Role-based user classification
- Personal information storage (full name, phone, DOB)
- User creation and update timestamps

### 3.2 Events Module
**Purpose**: Event creation and management

**Responsibilities**:
- Event CRUD operations (Create, Read, Update, Delete)
- Event status management (Draft, Published, Cancelled, Expired)
- Volunteer assignment to events
- Event scheduling and capacity management

**Key Features**:
- Event details (title, description, location, timing)
- Event organizer tracking
- Volunteer management (ManyToMany relationship)
- Registration deadline and capacity constraints
- Attendance enabling/disabling per event

### 3.3 Attendance Module
**Purpose**: QR code-based attendance tracking

**Responsibilities**:
- QR code generation and verification
- Check-in/Check-out tracking
- Attendance record management
- Attendance history and reporting

**Key Features**:
- HMAC-based secure QR token generation
- QR code scanning capabilities
- Unique attendance constraints per user per event
- Check-in and check-out timestamps
- Staff member tracking (who scanned the QR code)

### 3.4 Registrations Module
**Purpose**: Event registration management

**Responsibilities**:
- User event registration processing
- Registration status tracking
- Registration lifecycle management
- Capacity validation

**Key Features**:
- Registration status tracking (Pending, Approved, Rejected, Cancelled)
- Unique user-event registration constraint
- Registration timeline tracking
- Link to attendance records

### 3.5 Dashboard Module
**Purpose**: User dashboard and overview

**Responsibilities**:
- Display personalized information
- Show registered events
- Display attendance information
- Provide quick navigation

**Key Features**:
- User event summary
- Upcoming events
- Past attendance
- Quick access to features

### 3.6 Admin Panel Module
**Purpose**: Administrative system management

**Responsibilities**:
- System-wide management
- User administration
- Event oversight
- Access control

**Key Features**:
- Admin dashboard
- User and role management
- Event approval/cancellation
- System statistics

## 4. Data Model Overview

### 4.1 Entity Relationships

```
User (Custom)
├── (1:M) → Organized Events
├── (M:M) → Volunteered Events
├── (1:M) → Registrations
├── (1:M) → Attendance Records
└── (1:M) → Scanned Attendances

Event
├── (M:1) ← Organizer (User)
├── (M:M) ← Volunteers (User)
├── (1:M) → Registrations
└── (1:M) → Attendance Records

Registration
├── (M:1) ← User
├── (M:1) ← Event
└── (1:1) → Attendance

Attendance
├── (M:1) ← User
├── (M:1) ← Event
├── (1:1) ← Registration
└── (M:1) ← CheckedInBy (User)
```

### 4.2 Key Entities

**User Model**:
- Authentication credentials
- Personal information
- Role designation
- Timestamps

**Event Model**:
- Event metadata
- Status lifecycle
- Organizer and volunteer assignments
- Timing and capacity information

**Registration Model**:
- User-Event relationship
- Status tracking
- Lifecycle management

**Attendance Model**:
- User check-in/check-out
- Event attendance linking
- Registration linking
- Staff tracking (who checked in the user)

## 5. User Roles and Permissions

### 5.1 Role Hierarchy

```
Admin
  ├── Full system access
  ├── User management
  ├── Event approval/cancellation
  └── System administration

Organizer
  ├── Create events
  ├── Manage own events
  ├── Manage volunteers
  ├── View attendance
  └── Edit registrations

Volunteer
  ├── View assigned events
  ├── Check-in attendees (scan QR codes)
  ├── View event details
  └── Basic participation

Participant
  ├── Register for events
  ├── View registered events
  ├── Mark attendance (with QR code)
  └── View personal dashboard
```

## 6. Key Workflows

### 6.1 Event Creation and Management Workflow

```
Organizer → Create Event → Event Status: Draft
    ↓
Configure Event (details, volunteers, capacity)
    ↓
Publish Event → Event Status: Published
    ↓
Accept Registrations (pending → approved)
    ↓
Event Date Arrives
    ↓
Volunteers Scan QR Codes → Mark Attendance
    ↓
Event Ends → Event Status: Expired
```

### 6.2 User Registration Workflow

```
Participant → Browse Events
    ↓
Select Event and Register
    ↓
Registration Created (Status: Pending)
    ↓
Admin/Organizer Approves
    ↓
Registration Status: Approved
    ↓
Event Attendance: Check-in with QR Code
```

### 6.3 Attendance Tracking Workflow

```
Event Organizer → Enable Attendance Tracking
    ↓
Generate QR Code (with HMAC-based token)
    ↓
Participant → Receive QR Code (email/event page)
    ↓
At Event: Volunteer Scans QR Code
    ↓
System Verifies Token (HMAC verification)
    ↓
Check-in Time Recorded
    ↓
Attendance Record Created
```

## 7. Security Considerations

### 7.1 Authentication & Authorization
- Django's built-in authentication system
- Custom User model for role-based access
- Session management
- Login/registration validation

### 7.2 Data Protection
- HMAC-based QR token signing for attendance
- Unique constraints on registrations and attendance
- Foreign key relationships with CASCADE/SET_NULL policies
- Timestamps for audit trails

### 7.3 Access Control
- Role-based permission system
- View-level access restrictions
- Admin panel access control
- User-specific data isolation

## 8. Technology Stack

| Layer | Technology |
|-------|-----------|
| Framework | Django 6.0.2 |
| Database | MySQL 5.7+ |
| ORM | Django ORM |
| Authentication | Django Authentication |
| QR Codes | QR code generation library |
| Backend | Python 3.8+ |
| Frontend | HTML/CSS/JavaScript |
| Web Server | Django Development Server / Gunicorn |

## 9. Deployment Architecture

```
┌─────────────────────────────────────────┐
│        Web Server (Gunicorn/Nginx)      │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│   Django Application Instance(s)        │
│   - Multiple worker processes           │
│   - Load balancing ready                │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│      Database Connection Pool           │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│      MySQL Database                     │
│   - User Tables                         │
│   - Event Data                          │
│   - Attendance Records                  │
│   - Registration Data                   │
└─────────────────────────────────────────┘
```

## 10. Scalability Considerations

### 10.1 Horizontal Scaling
- Multiple Django application instances
- Load balancer distribution
- Connection pooling for database
- Session store (database/cache)

### 10.2 Vertical Scaling
- Database query optimization
- Indexing on frequently queried fields
- Caching mechanisms
- Background job processing for heavy operations

### 10.3 Performance Optimization
- Database query optimization
- Template caching
- Static file CDN delivery
- Pagination for large datasets

## 11. System Constraints and Limitations

1. **Capacity Management**: Events have optional capacity limits
2. **Unique Constraints**: One registration per user per event; one attendance record per user per event
3. **Status Lifecycle**: Events follow defined status transitions
4. **Role-Based Access**: Users can only perform actions allowed by their role
5. **QR Code Security**: HMAC-based verification prevents token tampering

## 12. Future Enhancements

- Real-time notifications for registration approvals
- Email notifications for event updates
- Calendar integration
- Mobile app for QR code scanning
- Analytics and reporting dashboard
- Payment integration for paid events
- Automated reminders and follow-ups
- Event feedback and rating system
