# Low-Level Design (LLD) - Event Manager System

## 1. Database Schema

### 1.1 User Table (extends Django's AbstractUser)

```sql
CREATE TABLE accounts_user (
    id INT PRIMARY KEY AUTO_INCREMENT,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME NULL,
    is_superuser BOOLEAN DEFAULT FALSE,
    username VARCHAR(150) UNIQUE NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    email VARCHAR(254) UNIQUE,
    is_staff BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    date_joined DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Custom Fields
    fullName VARCHAR(100) NOT NULL,
    phoneNumber VARCHAR(15),
    dateOfBirth DATE NULL,
    role VARCHAR(20) DEFAULT 'participant'
        CHECK (role IN ('admin', 'organizer', 'volunteer', 'participant')),
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 1.2 Event Table

```sql
CREATE TABLE events_event (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    description LONGTEXT NOT NULL,
    organizer_id INT NOT NULL,
    location VARCHAR(255) NOT NULL,
    startTime DATETIME NOT NULL,
    endTime DATETIME NOT NULL,
    registrationDeadline DATETIME NULL,
    capacity INT NULL,
    status VARCHAR(20) DEFAULT 'draft'
        CHECK (status IN ('draft', 'published', 'cancelled', 'expired')),
    attendanceEnabled BOOLEAN DEFAULT FALSE,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (organizer_id) REFERENCES accounts_user(id) ON DELETE CASCADE,
    INDEX idx_organizer (organizer_id),
    INDEX idx_status (status),
    INDEX idx_startTime (startTime)
);
```

### 1.3 Event-Volunteer Many-to-Many Table

```sql
CREATE TABLE events_event_volunteers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    event_id INT NOT NULL,
    user_id INT NOT NULL,
    
    FOREIGN KEY (event_id) REFERENCES events_event(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES accounts_user(id) ON DELETE CASCADE,
    UNIQUE KEY unique_event_volunteer (event_id, user_id),
    INDEX idx_user (user_id)
);
```

### 1.4 Registration Table

```sql
CREATE TABLE registrations_registration (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending'
        CHECK (status IN ('pending', 'approved', 'rejected', 'cancelled')),
    registeredAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES accounts_user(id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events_event(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_event_registration (user_id, event_id),
    INDEX idx_status (status),
    INDEX idx_user (user_id),
    INDEX idx_event (event_id)
);
```

### 1.5 Attendance Table

```sql
CREATE TABLE attendance_attendance (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    registration_id INT NULL,
    checkInTime DATETIME DEFAULT CURRENT_TIMESTAMP,
    checkOutTime DATETIME NULL,
    checkedInBy_id INT NULL,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES accounts_user(id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events_event(id) ON DELETE CASCADE,
    FOREIGN KEY (registration_id) REFERENCES registrations_registration(id) ON DELETE CASCADE,
    FOREIGN KEY (checkedInBy_id) REFERENCES accounts_user(id) ON DELETE SET NULL,
    UNIQUE KEY unique_attendance_per_event (user_id, event_id),
    INDEX idx_event (event_id),
    INDEX idx_checkInTime (checkInTime),
    INDEX idx_checkedInBy (checkedInBy_id)
);
```

## 2. Detailed Module Design

### 2.1 Accounts Module (accounts/)

#### 2.1.1 Models

**User Model** (`models.py`)
```python
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('organizer', 'Organizer'),
        ('volunteer', 'Volunteer'),
        ('participant', 'Participant'),
    )
    
    # Fields
    fullName: CharField(max_length=100)
    phoneNumber: CharField(max_length=15)
    dateOfBirth: DateField(null=True, blank=True)
    role: CharField(max_length=20, choices=ROLE_CHOICES)
    createdAt: DateTimeField(auto_now_add=True)
    updatedAt: DateTimeField(auto_now=True)
    
    # Methods
    get_role_display() -> str
    is_admin() -> bool
    is_organizer() -> bool
    is_volunteer() -> bool
    is_participant() -> bool
```

#### 2.1.2 Views

**URL Routes** (`urls.py`)
```
/register                 - GET, POST    (register.html)
/login                    - GET, POST    (login.html)
/logout                   - POST         (redirect to home)
/profile                  - GET          (user profile)
/profile/edit             - GET, POST    (edit profile)
```

**Key Views** (`views.py`)
```python
def register(request) -> HttpResponse
    """Handle user registration"""
    - Validate form data
    - Create new user with custom fields
    - Set default role as 'participant'
    - Redirect to login
    
def login(request) -> HttpResponse
    """Handle user login"""
    - Validate credentials
    - Create session
    - Redirect based on role
    
def logout(request) -> HttpResponse
    """Handle user logout"""
    - Clear session
    - Redirect to home
    
def user_profile(request) -> HttpResponse
    """Display user profile"""
    - Get current user
    - Display user information
    - Show role and permissions
```

#### 2.1.3 Admin Configuration

**Admin Register** (`admin.py`)
```python
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'fullName', 'role', 'createdAt']
    list_filter = ['role', 'is_active', 'createdAt']
    search_fields = ['username', 'email', 'fullName']
    fieldsets = [
        ('Authentication', {'fields': ['username', 'password', 'email']}),
        ('Personal Info', {'fields': ['first_name', 'last_name', 'fullName', 'phoneNumber', 'dateOfBirth']}),
        ('Permissions', {'fields': ['is_active', 'is_staff', 'is_superuser', 'role', 'groups']}),
        ('Timestamps', {'fields': ['date_joined', 'last_login', 'createdAt', 'updatedAt']}),
    ]
```

### 2.2 Events Module (events/)

#### 2.2.1 Models

**Event Model** (`models.py`)
```python
class Event(models.Model):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
        ("cancelled", "Cancelled"),
        ("expired", "Expired")
    )
    
    # Fields
    title: CharField(max_length=200)
    description: TextField()
    organizer: ForeignKey(User, related_name="organized_events")
    volunteers: ManyToManyField(User, related_name="volunteered_events", blank=True)
    location: CharField(max_length=255)
    startTime: DateTimeField()
    endTime: DateTimeField()
    registrationDeadline: DateTimeField(null=True, blank=True)
    capacity: PositiveIntegerField(null=True, blank=True)
    status: CharField(max_length=20, choices=STATUS_CHOICES)
    attendanceEnabled: BooleanField(default=False)
    createdAt: DateTimeField(auto_now_add=True)
    updatedAt: DateTimeField(auto_now=True)
    
    # Methods
    __str__() -> str
    get_registration_count() -> int
    can_register() -> bool
    is_full() -> bool
    get_remaining_capacity() -> int
    get_attendees() -> QuerySet
```

#### 2.2.2 Views

**URL Routes** (`urls.py`)
```
/events                        - GET         (list all events)
/events/create                 - GET, POST   (create event)
/events/<id>                   - GET         (view event details)
/events/<id>/edit              - GET, POST   (edit event)
/events/<id>/delete            - POST        (delete event)
/events/<id>/manage-volunteers - GET, POST   (manage volunteers)
```

**Key Views** (`views.py`)
```python
def list_events(request) -> HttpResponse
    """Display all published events"""
    - Filter by status='published'
    - Apply pagination
    - Search/filter by title, location
    
def create_event(request) -> HttpResponse
    """Create new event (Organizer only)"""
    - Validate organizer role
    - Get form data
    - Create event with organizer
    - Set status='draft'
    - Redirect to edit event
    
def view_event(request, id) -> HttpResponse
    """Display event details"""
    - Get event by id
    - Show event information
    - Show registration count vs capacity
    - Show volunteer list
    - Show attendance tracking status
    
def edit_event(request, id) -> HttpResponse
    """Edit event (Organizer only)"""
    - Verify ownership
    - Update event fields
    - Prevent editing if status != 'draft' or 'published'
    
def delete_event(request, id) -> HttpResponse
    """Delete event (Organizer/Admin)"""
    - Verify permission
    - Set status='cancelled' or DELETE
    - Notify registered users
    
def manage_volunteers(request, id) -> HttpResponse
    """Manage event volunteers"""
    - Add volunteers to event
    - Remove volunteers from event
    - Display current volunteers
```

#### 2.2.3 Admin Configuration

**Admin Register** (`admin.py`)
```python
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'organizer', 'status', 'startTime', 'capacity']
    list_filter = ['status', 'startTime', 'attendanceEnabled']
    search_fields = ['title', 'description', 'organizer__username']
    fieldsets = [
        ('Basic Info', {'fields': ['title', 'description']}),
        ('Scheduling', {'fields': ['startTime', 'endTime', 'registrationDeadline']}),
        ('Details', {'fields': ['organizer', 'location', 'capacity', 'status']}),
        ('Attendance', {'fields': ['attendanceEnabled', 'volunteers']}),
        ('Timestamps', {'fields': ['createdAt', 'updatedAt']}),
    ]
    filter_horizontal = ['volunteers']
```

### 2.3 Attendance Module (attendance/)

#### 2.3.1 Models

**Attendance Model** (`models.py`)
```python
class Attendance(models.Model):
    # Fields
    user: ForeignKey(User, related_name="attendances")
    event: ForeignKey(Event, related_name="attendances")
    registration: OneToOneField(Registration, related_name="attendance", null=True)
    checkInTime: DateTimeField(auto_now_add=True)
    checkOutTime: DateTimeField(null=True, blank=True)
    checkedInBy: ForeignKey(User, related_name="scanned_attendances", null=True)
    createdAt: DateTimeField(auto_now_add=True)
    updatedAt: DateTimeField(auto_now=True)
    
    # Constraints
    UNIQUE(user, event)  # Unique attendance per event
    
    # Methods
    __str__() -> str
    is_checked_out() -> bool
    duration_minutes() -> int
    get_check_in_time() -> datetime
```

#### 2.3.2 QR Utilities (`qr_utils.py`)

```python
def generate_qr_token(user_id: int) -> str:
    """
    Generate secure HMAC-based QR token
    
    Args:
        user_id: Integer user ID
    
    Returns:
        str: Format '<user_id>:<hmac_signature>'
    
    Process:
        1. Create key from SECRET_KEY
        2. Create message from user_id
        3. Generate HMAC-SHA256 signature
        4. Return formatted token
    """
    
def verify_qr_token(token: str) -> Optional[int]:
    """
    Verify QR token integrity
    
    Args:
        token: QR token string
    
    Returns:
        int: User ID if valid, None if invalid
    
    Process:
        1. Parse token '<user_id>:<signature>'
        2. Extract user_id and signature
        3. Generate expected signature
        4. Compare with provided signature (timing-safe)
        5. Return user_id or None
    
    Exceptions Handled:
        - ValueError: Invalid token format
        - AttributeError: Token parsing error
    """
```

#### 2.3.3 Views

**URL Routes** (`urls.py`)
```
/attendance                      - GET         (attendance home)
/attendance/my-attendance        - GET         (user's attendance records)
/attendance/event/<id>           - GET         (event attendance list)
/attendance/scan-qr              - GET, POST   (scan QR code)
/attendance/check-in/<user_id>   - POST        (manual check-in)
/attendance/check-out/<id>       - POST        (check-out from event)
```

**Key Views** (`views.py`)
```python
def attendance_home(request) -> HttpResponse
    """Display attendance options"""
    - Show user role (participant/volunteer/organizer)
    - Show available actions
    
def my_attendance(request) -> HttpResponse
    """Show user's attendance history"""
    - Get all attendance records for current user
    - Display check-in/check-out times
    - Filter by date range
    - Show event details
    
def event_attendance(request, event_id) -> HttpResponse
    """Display attendees for event (Organizer/Volunteer)"""
    - Verify permission (organizer or volunteer)
    - Get all attendance records for event
    - Display attendee list with check-in times
    - Show attendance statistics
    
def scan_qr(request) -> HttpResponse
    """QR code scanning interface"""
    - Display QR code scanner
    - Parse scanned token
    - Call verify_qr_token()
    - Create/update Attendance record
    - Show confirmation
    
def check_in(request, user_id) -> JsonResponse
    """Process QR check-in"""
    - Verify token validity
    - Get user and event context
    - Create Attendance record with checkedInBy=request.user
    - Handle duplicate attendance (same user, same event)
    - Return success/error status
    
def check_out(request, attendance_id) -> HttpResponse
    """Mark check-out time"""
    - Get Attendance record
    - Verify permission (user or organizer)
    - Update checkOutTime=now()
    - Calculate duration
    - Save record
```

#### 2.3.4 Admin Configuration

```python
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'checkInTime', 'checkOutTime', 'checkedInBy']
    list_filter = ['event', 'checkInTime', 'checkedInBy']
    search_fields = ['user__username', 'event__title']
    readonly_fields = ['createdAt', 'updatedAt', 'checkInTime']
    fieldsets = [
        ('User Info', {'fields': ['user', 'event']}),
        ('Check In/Out', {'fields': ['checkInTime', 'checkOutTime', 'checkedInBy']}),
        ('Registration', {'fields': ['registration']}),
        ('Timestamps', {'fields': ['createdAt', 'updatedAt']}),
    ]
```

### 2.4 Registrations Module (registrations/)

#### 2.4.1 Models

**Registration Model** (`models.py`)
```python
class Registration(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("cancelled", "Cancelled"),
    )
    
    # Fields
    user: ForeignKey(User, related_name="registrations")
    event: ForeignKey(Event, related_name="registrations")
    status: CharField(max_length=20, choices=STATUS_CHOICES)
    registeredAt: DateTimeField(auto_now_add=True)
    updatedAt: DateTimeField(auto_now=True)
    
    # Constraints
    UNIQUE(user, event)  # One registration per user per event
    
    # Methods
    __str__() -> str
    is_pending() -> bool
    is_approved() -> bool
    approve() -> bool
    reject() -> bool
    cancel() -> bool
```

#### 2.4.2 Views

**URL Routes** (`urls.py`)
```
/registrations/my-registrations     - GET         (user's registrations)
/registrations/manage               - GET         (manage registrations - organizer)
/registrations/register/<event_id>  - POST        (register for event)
/registrations/<id>/approve         - POST        (approve registration)
/registrations/<id>/reject          - POST        (reject registration)
/registrations/<id>/cancel          - POST        (cancel registration)
```

**Key Views** (`views.py`)
```python
def register_for_event(request, event_id) -> HttpResponse
    """Register user for event"""
    - Get event and user
    - Check capacity (if limit exists)
    - Check deadline
    - Check if already registered
    - Create Registration with status='pending'
    - Notify organizer
    
def my_registrations(request) -> HttpResponse
    """Show user's registrations"""
    - Get all registrations for current user
    - Group by status
    - Show event details
    - Show attendance status
    - Allow cancel registration
    
def manage_registrations(request, event_id) -> HttpResponse
    """Manage event registrations (Organizer only)"""
    - Get all registrations for event
    - Display grouped by status
    - Allow approve/reject/cancel
    - Show registration statistics
    
def approve_registration(request, reg_id) -> HttpResponse
    """Approve pending registration"""
    - Get registration
    - Verify organizer permission
    - Update status='approved'
    - Send notification to user
    
def reject_registration(request, reg_id) -> HttpResponse
    """Reject registration"""
    - Get registration
    - Update status='rejected'
    - Send notification
    
def cancel_registration(request, reg_id) -> HttpResponse
    """Cancel registration"""
    - Get registration
    - Verify user permission
    - Update status='cancelled'
    - If attendance exists, cascade delete
```

#### 2.4.3 Admin Configuration

```python
@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'status', 'registeredAt']
    list_filter = ['status', 'registeredAt', 'event']
    search_fields = ['user__username', 'event__title']
    fieldsets = [
        ('User & Event', {'fields': ['user', 'event']}),
        ('Status', {'fields': ['status']}),
        ('Timestamps', {'fields': ['registeredAt', 'updatedAt']}),
    ]
```

### 2.5 Dashboard Module (dashboard/)

#### 2.5.1 Views

**URL Routes** (`urls.py`)
```
/dashboard      - GET   (user dashboard)
```

**Key Views** (`views.py`)
```python
def dashboard(request) -> HttpResponse
    """Main user dashboard"""
    - Get upcoming events (user registrations)
    - Get past events with attendance
    - Show event statistics
    - Display registered events
    - Show attendance summary
    - Check events by role:
      * Admin: System-wide statistics
      * Organizer: Organized events, registration stats
      * Volunteer: Assigned events
      * Participant: Registered events, attendance
```

### 2.6 Admin Panel Module (admin_panel/)

#### 2.6.1 Views

**URL Routes** (`urls.py`)
```
/admin-panel               - GET   (admin dashboard)
/admin-panel/users         - GET   (user management)
/admin-panel/events        - GET   (event management)
/admin-panel/statistics    - GET   (system statistics)
```

**Key Views** (`views.py`)
```python
def admin_dashboard(request) -> HttpResponse
    """Admin dashboard (Admin only)"""
    - Verify admin role
    - Display system statistics
    - Show total users, events, registrations
    - Show recent activities
    
def unauthorized(request) -> HttpResponse
    """Handle unauthorized access"""
    - Display error message
    - Redirect to appropriate page
```

## 3. URL Routing Architecture

**Main Routes** (`event_manager/urls.py`)
```python
urlpatterns = [
    path('', home, name='home'),                           # Landing page
    path('', include('accounts.urls')),                    # /register, /login, etc.
    path('', include('dashboard.urls')),                   # /dashboard
    path('', include('events.urls')),                      # /events
    path('', include('registrations.urls')),               # /registrations
    path('', include('attendance.urls')),                  # /attendance
    path('', include('admin_panel.urls')),                 # /admin-panel
]
```

## 4. Middleware and Decorators

### 4.1 Custom Decorators (proposed)

```python
def role_required(role):
    """Check if user has required role"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.role == role:
                return view_func(request, *args, **kwargs)
            return redirect('unauthorized')
        return wrapper
    return decorator

def organizer_or_admin(view_func):
    """Check if user is organizer or admin"""
    def wrapper(request, *args, **kwargs):
        if request.user.role in ['organizer', 'admin']:
            return view_func(request, *args, **kwargs)
        return redirect('unauthorized')
    return wrapper

def owner_or_admin(model_field):
    """Check if user owns the resource or is admin"""
    def decorator(view_func):
        def wrapper(request, resource_id, *args, **kwargs):
            resource = get_object_or_404(model_field, id=resource_id)
            if resource.organizer == request.user or request.user.is_superuser:
                return view_func(request, resource_id, *args, **kwargs)
            return redirect('unauthorized')
        return wrapper
    return decorator
```

## 5. API Endpoints (if REST API is implemented)

```
Authentication:
  POST   /api/auth/register
  POST   /api/auth/login
  POST   /api/auth/logout
  GET    /api/auth/profile

Events:
  GET    /api/events                    # List all
  POST   /api/events                    # Create
  GET    /api/events/<id>               # Get details
  PUT    /api/events/<id>               # Update
  DELETE /api/events/<id>               # Delete

Registrations:
  GET    /api/events/<id>/registrations     # List
  POST   /api/events/<id>/register          # Register
  PUT    /api/registrations/<id>            # Update status
  DELETE /api/registrations/<id>            # Cancel

Attendance:
  GET    /api/events/<id>/attendance        # List
  POST   /api/attendance/check-in           # Check in
  PUT    /api/attendance/<id>/check-out     # Check out
  GET    /api/attendance/my-records         # User's records
```

## 6. Error Handling and Validation

### 6.1 Common Exceptions

```python
class EventCapacityExceeded(Exception):
    """Raised when event registration exceeds capacity"""
    
class RegistrationDeadlineExceeded(Exception):
    """Raised when registering after deadline"""
    
class DuplicateRegistration(Exception):
    """Raised when user attempts to register twice"""
    
class InvalidQRToken(Exception):
    """Raised when QR token verification fails"""
    
class UnauthorizedAccess(Exception):
    """Raised when user lacks permission"""
```

### 6.2 Form Validation

```python
# Registration form
class RegistrationForm(forms.Form):
    - email: EmailField (required)
    - password: CharField (min_length=8)
    - fullName: CharField (max_length=100)
    - phoneNumber: CharField (max_length=15)

# Event creation form
class EventForm(forms.ModelForm):
    - title: CharField (max_length=200, required)
    - description: CharField (required)
    - location: CharField (required)
    - startTime: DateTimeField (future date validation)
    - endTime: DateTimeField (after startTime validation)
    - capacity: IntegerField (positive integer validation)
```

## 7. Performance Considerations

### 7.1 Database Indexing Strategy

```sql
-- Frequently queried fields
CREATE INDEX idx_user_role ON accounts_user(role);
CREATE INDEX idx_event_status ON events_event(status);
CREATE INDEX idx_event_startTime ON events_event(startTime);
CREATE INDEX idx_registration_user ON registrations_registration(user_id);
CREATE INDEX idx_registration_event ON registrations_registration(event_id);
CREATE INDEX idx_attendance_event ON attendance_attendance(event_id);
CREATE INDEX idx_attendance_user ON attendance_attendance(user_id);
```

### 7.2 Query Optimization

```python
# Use select_related for foreign keys
Event.objects.select_related('organizer')

# Use prefetch_related for reverse relations
Event.objects.prefetch_related('volunteers', 'registrations')

# Use only() to limit fields
User.objects.only('id', 'username', 'fullName', 'role')

# Pagination for large result sets
paginator = Paginator(queryset, 25)
page = paginator.get_page(request.GET.get('page'))
```

### 7.3 Caching Strategy

```python
# Cache event list
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # 5 minutes
def list_events(request):
    # View implementation
```

## 8. Security Implementation Details

### 8.1 CSRF Protection
- Django's CSRF middleware enabled
- All forms include {% csrf_token %}
- POST requests validated

### 8.2 SQL Injection Prevention
- Django ORM used (parameterized queries)
- User input never directly in SQL

### 8.3 XSS Prevention
- Template auto-escaping enabled
- sanitize_html() for user-generated content
- Content-Security-Policy headers

### 8.4 Authentication Security
- Passwords hashed using Django's PBKDF2
- Session timeouts implemented
- Login attempt rate limiting (future)

## 9. Testing Strategy

### 9.1 Unit Tests (tests.py in each app)

```python
class UserModelTests(TestCase):
    - test_user_creation
    - test_role_assignment
    - test_user_validation

class EventModelTests(TestCase):
    - test_event_creation
    - test_status_transitions
    - test_capacity_validation
    
class RegistrationViewTests(TestCase):
    - test_register_for_event
    - test_duplicate_registration_prevention
    - test_capacity_enforcement
    
class AttendanceTests(TestCase):
    - test_qr_token_generation
    - test_qr_token_verification
    - test_check_in_process
```

### 9.2 Integration Tests
- User registration to attendance workflow
- Event creation to completion workflow
- Permission and role-based access control

## 10. Deployment Checklist

- [ ] Set DEBUG = False in production
- [ ] Configure ALLOWED_HOSTS
- [ ] Set unique SECRET_KEY
- [ ] Configure database credentials
- [ ] Set up static files collection
- [ ] Configure logging
- [ ] Enable SSL/HTTPS
- [ ] Configure CORS if needed
- [ ] Set up backups
- [ ] Configure monitoring and alerts
