# LLD UML Diagrams - Event Manager System

## 1. Class Diagram - Complete Data Model

```mermaid
classDiagram
    class User {
        -id: int
        -username: string
        -email: string
        -password: string
        -fullName: string
        -phoneNumber: string
        -dateOfBirth: date
        -role: enum[admin|organizer|volunteer|participant]
        -is_active: bool
        -createdAt: datetime
        -updatedAt: datetime
        +getRole() string
        +isAdmin() bool
        +isOrganizer() bool
        +isVolunteer() bool
        +isParticipant() bool
    }
    
    class Event {
        -id: int
        -title: string
        -description: string
        -organizer_id: int
        -location: string
        -startTime: datetime
        -endTime: datetime
        -registrationDeadline: datetime
        -capacity: int
        -status: enum[draft|published|cancelled|expired]
        -attendanceEnabled: bool
        -createdAt: datetime
        -updatedAt: datetime
        +getRegistrationCount() int
        +canRegister() bool
        +isFull() bool
        +getRemainingCapacity() int
        +getAttendees() QuerySet
        +publishEvent() void
        +cancelEvent() void
    }
    
    class Registration {
        -id: int
        -user_id: int
        -event_id: int
        -status: enum[pending|approved|rejected|cancelled]
        -registeredAt: datetime
        -updatedAt: datetime
        +isPending() bool
        +isApproved() bool
        +approve() bool
        +reject() bool
        +cancel() bool
    }
    
    class Attendance {
        -id: int
        -user_id: int
        -event_id: int
        -registration_id: int
        -checkInTime: datetime
        -checkOutTime: datetime
        -checkedInBy_id: int
        -createdAt: datetime
        -updatedAt: datetime
        +isCheckedOut() bool
        +getDurationMinutes() int
        +getCheckInTime() datetime
    }
    
    class QRUtils {
        +generateQRToken(user_id: int) string
        +verifyQRToken(token: string) int
    }
    
    class EventVolunteer {
        -id: int
        -event_id: int
        -user_id: int
    }
    
    User "1" -- "*" Event : organizes
    User "1" -- "*" Registration : makes
    User "1" -- "*" Attendance : has
    User "1" -- "*" EventVolunteer : volunteers
    Event "1" -- "*" Registration : receives
    Event "1" -- "*" Attendance : tracks
    Event "1" -- "*" EventVolunteer : assigns
    Registration "1" -- "0..1" Attendance : creates
```

## 2. Class Diagram - Accounts Module

```mermaid
classDiagram
    class AbstractUser {
        -id: int
        -password: string
        -username: string
        -first_name: string
        -last_name: string
        -email: string
        -is_staff: bool
        -is_active: bool
        -date_joined: datetime
    }
    
    class User {
        -fullName: string
        -phoneNumber: string
        -dateOfBirth: date
        -role: string
        -createdAt: datetime
        -updatedAt: datetime
        +get_role_display() string
        +is_admin() bool
        +is_organizer() bool
        +is_volunteer() bool
        +is_participant() bool
    }
    
    AbstractUser <|-- User : extends
```

## 3. Class Diagram - Events Module

```mermaid
classDiagram
    class User {
        -id: int
        -username: string
    }
    
    class Event {
        -id: int
        -title: string
        -description: string
        -organizer_id: int FK
        -location: string
        -startTime: datetime
        -endTime: datetime
        -registrationDeadline: datetime
        -capacity: int
        -status: string
        -attendanceEnabled: bool
        -createdAt: datetime
        -updatedAt: datetime
        +__str__() string
        +getRegistrationCount() int
        +canRegister() bool
        +isFull() bool
    }
    
    class EventVolunteer {
        -id: int
        -event_id: int FK
        -user_id: int FK
    }
    
    User "1" -- "*" Event : organizes
    Event "1" -- "*" EventVolunteer : has
    User "1" -- "*" EventVolunteer : volunteers
```

## 4. Class Diagram - Registrations Module

```mermaid
classDiagram
    class User {
        -id: int
        -username: string
    }
    
    class Event {
        -id: int
        -title: string
    }
    
    class Registration {
        -id: int
        -user_id: int FK
        -event_id: int FK
        -status: string
        -registeredAt: datetime
        -updatedAt: datetime
        +__str__() string
        +isPending() bool
        +isApproved() bool
        +approve() void
        +reject() void
        +cancel() void
    }
    
    User "1" -- "*" Registration : makes
    Event "1" -- "*" Registration : has
```

## 5. Class Diagram - Attendance Module

```mermaid
classDiagram
    class User {
        -id: int
        -username: string
    }
    
    class Event {
        -id: int
        -title: string
    }
    
    class Registration {
        -id: int
    }
    
    class Attendance {
        -id: int
        -user_id: int FK
        -event_id: int FK
        -registration_id: int FK
        -checkInTime: datetime
        -checkOutTime: datetime
        -checkedInBy_id: int FK
        -createdAt: datetime
        -updatedAt: datetime
        +isCheckedOut() bool
        +getDurationMinutes() int
    }
    
    class QRTokenUtils {
        -secret_key: string
        +generateQRToken(user_id: int) string
        +verifyQRToken(token: string) Optional~int~
        -generateHMAC(user_id: int) string
        -verifyHMAC(expected: string, provided: string) bool
    }
    
    User "1" -- "*" Attendance : checks in
    Event "1" -- "*" Attendance : has
    Registration "1" -- "0..1" Attendance : links
    User "1" -- "*" Attendance : scans as
    Attendance --> QRTokenUtils : uses
```

## 6. Sequence Diagram - User Registration & Event Attendance

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant Django
    participant Database
    
    User->>Browser: Visit Website
    Browser->>Django: GET /register
    Django->>Browser: Show Registration Form
    User->>Browser: Fill Form & Submit
    Browser->>Django: POST /register
    Django->>Django: Validate Form
    Django->>Database: Create User Record
    Database->>Django: Return User ID
    Django->>Browser: Redirect to Login
    User->>Browser: Login with Credentials
    Browser->>Django: POST /login
    Django->>Database: Verify Credentials
    Database->>Django: User Found
    Django->>Browser: Set Session Cookie
    Browser->>Django: Redirect to Dashboard
    Django->>Browser: Show Dashboard
```

## 7. Sequence Diagram - Event Registration Process

```mermaid
sequenceDiagram
    participant Participant
    participant App as Event App
    participant Organizer as Organizer
    participant DB as Database
    
    Participant->>App: Browse Events
    App->>DB: Query Published Events
    DB->>App: Return Event List
    App->>Participant: Show Events
    Participant->>App: Click Register
    App->>DB: Check Capacity
    DB->>App: Return Capacity Status
    alt Event Full
        App->>Participant: Show Error: Event Full
    else Capacity Available
        Participant->>App: Confirm Registration
        App->>DB: Create Registration Record
        DB->>App: Success
        App->>Organizer: Notify New Registration
        App->>Participant: Show Pending Status
        Organizer->>App: Review Registrations
        Organizer->>App: Approve Registration
        App->>DB: Update Status to Approved
        DB->>App: Success
        App->>Participant: Send Approval Notification
        Participant->>Participant: Can Now Attend Event
    end
```

## 8. Sequence Diagram - QR Code Check-in Process

```mermaid
sequenceDiagram
    participant Participant
    participant Volunteer
        EventUser->>App
    participant QR as QR Utils
    participant DB as Database
    
    Participant->>App: Receive QR Code
    Participant->>Volunteer: Arrive at Event
    Volunteer->>App: Open QR Scanner
    Participant->>App: Show QR Code
    App->>App: Scan QR Code
    App->>QR: verify_qr_token(token)
    QR->>QR: Parse Token: user_id:signature
    QR->>QR: Regenerate HMAC Signature
    QR->>QR: Compare Signatures
    alt Valid Token
        QR->>App: Return user_id
        App->>DB: Create Attendance Record
        DB->>DB: Set checkInTime = NOW()
        DB->>DB: Set checkedInBy = Volunteer
        DB->>App: Success
        App->>Volunteer: Check-in Successful
        Volunteer->>Participant: Welcome to Event!
    else Invalid Token
        QR->>App: Return None
        App->>Volunteer: Invalid QR Code
        Volunteer->>Participant: Please Try Again
    end
```

## 9. Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    USER ||--o{ EVENT : organizes
    USER ||--o{ REGISTRATION : makes
    USER ||--o{ ATTENDANCE : has
    USER ||--o{ EVENT_VOLUNTEERS : "as volunteer"
    USER ||--o{ ATTENDANCE : scans_as
    EVENT ||--o{ REGISTRATION : receives
    EVENT ||--o{ ATTENDANCE : tracks
    EVENT ||--o{ EVENT_VOLUNTEERS : assigns
    REGISTRATION ||--o| ATTENDANCE : creates
    
    USER {
        int id PK
        string username UK
        string email
        string password
        string fullName
        string phoneNumber
        date dateOfBirth
        string role
        bool is_active
        datetime date_joined
        datetime createdAt
        datetime updatedAt
    }
    
    EVENT {
        int id PK
        string title
        text description
        int organizer_id FK
        string location
        datetime startTime
        datetime endTime
        datetime registrationDeadline
        int capacity
        string status
        bool attendanceEnabled
        datetime createdAt
        datetime updatedAt
            participant EventUser
    
    REGISTRATION {
        int id PK
        int user_id FK
            EventUser->>App: Browse Events
            App->>DB: Query Published Events
            DB->>App: Return Event List
            App->>EventUser: Show Events
            EventUser->>App: Click Register
            App->>DB: Check Capacity
            DB->>App: Return Capacity Status
            alt Event Full
                App->>EventUser: Show Error: Event Full
            else Capacity Available
                EventUser->>App: Confirm Registration
                App->>DB: Create Registration Record
                DB->>App: Success
                App->>Organizer: Notify New Registration
                App->>EventUser: Show Pending Status
                Organizer->>App: Review Registrations
                Organizer->>App: Approve Registration
                App->>DB: Update Status to Approved
                DB->>App: Success
                App->>EventUser: Send Approval Notification
                EventUser->>EventUser: Can Now Attend Event
        int user_id FK
    }
```
## 10. State Diagram - Event Lifecycle
        ## 8. Sequence Diagram - QR Code Check-in Process

        ```mermaid
        sequenceDiagram
            participant EventUser
            participant Volunteer
            participant App as Event App
            participant QR as QR Utils
            participant DB as Database
    
            EventUser->>App: Receive QR Code
            EventUser->>Volunteer: Arrive at Event
            Volunteer->>App: Open QR Scanner
            EventUser->>App: Show QR Code
            App->>App: Scan QR Code
            App->>QR: verify_qr_token method
            QR->>QR: Parse Token
            QR->>QR: Regenerate HMAC Signature
            QR->>QR: Compare Signatures
            alt Valid Token
                QR->>App: Return user_id
                App->>DB: Create Attendance Record
                DB->>DB: Set checkInTime
                DB->>DB: Set checkedInBy
                DB->>App: Success
                App->>Volunteer: Check-in Successful
                Volunteer->>EventUser: Welcome to Event!
            else Invalid Token
                QR->>App: Return None
                App->>Volunteer: Invalid QR Code
                Volunteer->>EventUser: Please Try Again
    
    note right of Expired
        Event date has passed.
        No more registrations.
        Attendance finalized.
    end note
```

## 11. State Diagram - Registration Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Pending: User Registers
    
    Pending --> Approved: Organizer Approves
    Pending --> Rejected: Organizer Rejects
    Pending --> Cancelled: User Cancels
    
    Approved --> Cancelled: User Cancels
    
    Rejected --> [*]: Final
    Cancelled --> [*]: Final
    Approved --> [*]: Event Complete
    
    note right of Pending
        Registration submitted.
        Awaiting organizer review.
    end note
    
    note right of Approved
        Registration approved.
        User can attend event.
    end note
    
    note right of Rejected
        Registration rejected.
        User cannot attend.
    end note
    
    note right of Cancelled
        Registration cancelled by user.
        Cannot be recovered.
    end note
```

## 12. State Diagram - Attendance Status

```mermaid
stateDiagram-v2
    [*] --> NoCheckIn: User Registered
    
    NoCheckIn --> CheckedIn: QR Code Scanned
    CheckedIn --> CheckedOut: User Leaves Event
    CheckedOut --> [*]: Attendance Complete
    
    NoCheckIn --> [*]: Event Ended
    
    note right of NoCheckIn
        User registered but has not
        checked in to the event.
    end note
    
    note right of CheckedIn
        User has checked in.
        Check-in time recorded.
    end note
    
    note right of CheckedOut
        User has checked out.
        Duration calculated.
    end note
```

## 13. Component Diagram - System Architecture

```mermaid
graph TB
    subgraph Client["Client Layer"]
        Browser["Browser<br/>HTML/CSS/JS"]
    end
    
    subgraph Django["Django Application Layer"]
        ACC["Accounts App<br/>- Register<br/>- Login<br/>- Profile"]
        EV["Events App<br/>- Create<br/>- Edit<br/>- Manage"]
        REG["Registrations App<br/>- Register<br/>- Approve<br/>- Manage"]
        ATT["Attendance App<br/>- QR Gen<br/>- Scan<br/>- Check-in"]
        DASH["Dashboard App<br/>- Statistics<br/>- Overview"]
        ADMIN["Admin Panel<br/>- Management<br/>- Control"]
    end
    
    subgraph ORM["Data Access Layer"]
        ORM_Layer["Django ORM<br/>Query Builder"]
    end
    
    subgraph DB["Database Layer"]
        MySQL["MySQL Database"]
    end
    
    Browser -->|HTTP| ACC
    Browser -->|HTTP| EV
    Browser -->|HTTP| REG
    Browser -->|HTTP| ATT
    Browser -->|HTTP| DASH
    Browser -->|HTTP| ADMIN
    
    ACC --> ORM_Layer
    EV --> ORM_Layer
    REG --> ORM_Layer
    ATT --> ORM_Layer
    DASH --> ORM_Layer
    ADMIN --> ORM_Layer
    
    ORM_Layer --> MySQL
    
    style Client fill:#e3f2fd,color:#000000
    style Django fill:#fff3e0,color:#000000
    style ORM fill:#f3e5f5,color:#000000
    style DB fill:#e8f5e9,color:#000000
```

## 14. Use Case Diagram - Admin

```mermaid
graph TD
    Admin["Admin<br/>User"]
    
    ManageUsers["Manage Users"]
    ManageEvents["Manage Events"]
    ViewStats["View Statistics"]
    ApproveEvents["Approve Events"]
    ApproveRegistrations["Approve Registrations"]
    
    Admin -->|Perform| ManageUsers
    Admin -->|Perform| ManageEvents
    Admin -->|Perform| ViewStats
    Admin -->|Perform| ApproveEvents
    Admin -->|Perform| ApproveRegistrations
    
    style Admin fill:#e3f2fd,color:#000000
    style ManageUsers fill:#fff3e0,color:#000000
    style ManageEvents fill:#fff3e0,color:#000000
    style ViewStats fill:#fff3e0,color:#000000
    style ApproveEvents fill:#fff3e0,color:#000000
    style ApproveRegistrations fill:#fff3e0,color:#000000
```

## 15. Use Case Diagram - Organizer

```mermaid
graph TD
    Organizer["Organizer<br/>User"]
    
    CreateEvent["Create Event"]
    EditEvent["Edit Event"]
    PublishEvent["Publish Event"]
    ManageVolunteers["Manage Volunteers"]
    ViewRegistrations["View Registrations"]
    ApproveReg["Approve Registrations"]
    ViewAttendance["View Attendance"]
    
    Organizer -->|Perform| CreateEvent
    Organizer -->|Perform| EditEvent
    Organizer -->|Perform| PublishEvent
    Organizer -->|Perform| ManageVolunteers
    Organizer -->|Perform| ViewRegistrations
    Organizer -->|Perform| ApproveReg
    Organizer -->|Perform| ViewAttendance
    
    style Organizer fill:#e3f2fd,color:#000000
    style CreateEvent fill:#fff3e0,color:#000000
    style EditEvent fill:#fff3e0,color:#000000
    style PublishEvent fill:#fff3e0,color:#000000
    style ManageVolunteers fill:#fff3e0,color:#000000
    style ViewRegistrations fill:#fff3e0,color:#000000
    style ApproveReg fill:#fff3e0,color:#000000
    style ViewAttendance fill:#fff3e0,color:#000000
```

## 16. Use Case Diagram - Volunteer

```mermaid
graph TD
    Volunteer["Volunteer<br/>User"]
    
    ViewAssignedEvents["View Assigned Events"]
    ScanQRCode["Scan QR Codes"]
    MarkAttendance["Mark Attendance"]
    ViewEventDetails["View Event Details"]
    
    Volunteer -->|Perform| ViewAssignedEvents
    Volunteer -->|Perform| ScanQRCode
    Volunteer -->|Perform| MarkAttendance
    Volunteer -->|Perform| ViewEventDetails
    
    style Volunteer fill:#e3f2fd,color:#000000
    style ViewAssignedEvents fill:#fff3e0,color:#000000
    style ScanQRCode fill:#fff3e0,color:#000000
    style MarkAttendance fill:#fff3e0,color:#000000
    style ViewEventDetails fill:#fff3e0,color:#000000
```

## 17. Use Case Diagram - Participant

```mermaid
graph TD
    Participant["Participant<br/>User"]
    
    BrowseEvents["Browse Events"]
    RegisterEvent["Register for Event"]
    ViewDashboard["View Dashboard"]
    CheckIn["Check-in with QR"]
    ViewHistory["View Attendance History"]
    
    Participant -->|Perform| BrowseEvents
    Participant -->|Perform| RegisterEvent
    Participant -->|Perform| ViewDashboard
    Participant -->|Perform| CheckIn
    Participant -->|Perform| ViewHistory
    
    style Participant fill:#e3f2fd,color:#000000
    style BrowseEvents fill:#fff3e0,color:#000000
    style RegisterEvent fill:#fff3e0,color:#000000
    style ViewDashboard fill:#fff3e0,color:#000000
    style CheckIn fill:#fff3e0,color:#000000
    style ViewHistory fill:#fff3e0,color:#000000
```

## 18. Activity Diagram - Event Registration Workflow

```mermaid
graph TD
    Start(["Start"]) --> Browse["Browse Events"]
    Browse --> Select["Select Event"]
    Select --> RegisterClick["Click Register"]
    RegisterClick --> Check{"Prerequisites<br/>Met?"}
    
    Check -->|Capacity Full| CapError["Show Error:<br/>Event Full"]
    Check -->|Deadline Passed| DeadlineError["Show Error:<br/>Deadline Passed"]
    Check -->|Already Registered| DupError["Show Error:<br/>Already Registered"]
    Check -->|Valid| CreateReg["Create Registration<br/>Status: Pending"]
    
    CapError --> End1(["End"])
    DeadlineError --> End1
    DupError --> End1
    
    CreateReg --> Notify["Notify Organizer"]
    Notify --> OrgReview["Organizer Reviews"]
    OrgReview --> Decision{"Approved?"}
    
    Decision -->|Approve| Approve["Update Status:<br/>Approved"]
    Decision -->|Reject| Reject["Update Status:<br/>Rejected"]
    
    Approve --> NotifyUser["Notify User"]
    Reject --> NotifyUser
    NotifyUser --> End2(["End"])
    
    style Start fill:#c8e6c9,color:#000000
    style End1 fill:#ffcdd2,color:#000000
    style End2 fill:#c8e6c9,color:#000000
    style Check fill:#ffe0b2,color:#000000
    style Decision fill:#ffe0b2,color:#000000
```

## 19. Deployment Diagram

```mermaid
graph TB
    subgraph Client["Client Tier"]
        Web["Web Browser<br/>HTML/CSS/JS"]
    end
    
    subgraph App["Application Tier"]
        WebServer["Nginx<br/>Web Server"]
        AppServer1["Django Instance 1<br/>Gunicorn"]
        AppServer2["Django Instance 2<br/>Gunicorn"]
        AppServer3["Django Instance 3<br/>Gunicorn"]
    end
    
    subgraph Data["Data Tier"]
        MySQL["MySQL<br/>Master Database"]
        MySQLRep["MySQL<br/>Replica"]
    end
    
    subgraph Services["Supporting Services"]
        Cache["Redis<br/>Cache"]
        Queue["Celery<br/>Queue"]
    end
    
    Web -->|HTTP/HTTPS| WebServer
    WebServer -->|Route| AppServer1
    WebServer -->|Route| AppServer2
    WebServer -->|Route| AppServer3
    
    AppServer1 -->|Query| MySQL
    AppServer2 -->|Query| MySQL
    AppServer3 -->|Query| MySQL
    
    MySQL -->|Replicate| MySQLRep
    
    AppServer1 -->|Cache| Cache
    AppServer2 -->|Cache| Cache
    AppServer3 -->|Cache| Cache
    
    AppServer1 -->|Task| Queue
    AppServer2 -->|Task| Queue
    AppServer3 -->|Task| Queue
    
    style Client fill:#e3f2fd,color:#000000
    style App fill:#fff3e0,color:#000000
    style Data fill:#e8f5e9,color:#000000
    style Services fill:#f3e5f5,color:#000000
```

## 20. Package Diagram

```mermaid
graph TB
    subgraph Package["Event Manager Package"]
        subgraph Accounts["accounts"]
            UserModel["User Model"]
            AuthViews["Auth Views"]
            AuthForms["Auth Forms"]
        end
        
        subgraph Events["events"]
            EventModel["Event Model"]
            EventViews["Event Views"]
            EventForms["Event Forms"]
        end
        
        subgraph Registrations["registrations"]
            RegModel["Registration Model"]
            RegViews["Registration Views"]
            RegForms["Registration Forms"]
        end
        
        subgraph Attendance["attendance"]
            AttModel["Attendance Model"]
            QRUtils["QR Utils"]
            AttViews["Attendance Views"]
        end
        
        subgraph Dashboard["dashboard"]
            DashViews["Dashboard Views"]
        end
        
        subgraph AdminPanel["admin_panel"]
            AdminViews["Admin Views"]
        end
        
        Accounts -->|uses| UserModel
        Events -->|uses| EventModel
        Registrations -->|uses| RegModel
        Registrations -->|depends on| EventModel
        Attendance -->|uses| AttModel
        Attendance -->|uses| QRUtils
        Attendance -->|depends on| RegModel
        Dashboard -->|depends on| Events
        Dashboard -->|depends on| Registrations
        AdminPanel -->|manages| UserModel
        AdminPanel -->|manages| EventModel
    end
    
    style Accounts fill:#e3f2fd,color:#000000
    style Events fill:#fff3e0,color:#000000
    style Registrations fill:#f3e5f5,color:#000000
    style Attendance fill:#e8f5e9,color:#000000
    style Dashboard fill:#c8e6c9,color:#000000
    style AdminPanel fill:#fce4ec,color:#000000
```

## 21. Interaction Overview Diagram - Event Registration

```mermaid
graph TB
    subgraph Flow["Event Registration Flow"]
        A["1. User Browse Events"]
        B["2. Select Event"]
        C["3. Submit Registration"]
        D{"4. Validation Check"}
        E["5. Create Registration"]
        F["6. Notify Organizer"]
        G["7. Organizer Reviews"]
        H["8. Organizer Decision"]
        I["9. Update Status"]
        J["10. Notify User"]
    end
    
    A --> B
    B --> C
    C --> D
    D -->|Pass| E
    D -->|Fail| F
    E --> F
    F --> G
    G --> H
    H -->|Approve| I
    H -->|Reject| I
    I --> J
    
    style A fill:#e3f2fd,color:#000000
    style B fill:#e3f2fd,color:#000000
    style C fill:#fff3e0,color:#000000
    style D fill:#ffe0b2,color:#000000
    style E fill:#f3e5f5,color:#000000
    style F fill:#e8f5e9,color:#000000
    style G fill:#fff3e0,color:#000000
    style H fill:#ffe0b2,color:#000000
    style I fill:#f3e5f5,color:#000000
    style J fill:#e8f5e9,color:#000000
```
