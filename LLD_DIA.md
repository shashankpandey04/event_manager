# LLD Flow Diagrams - Event Manager System

## 1. System Data Flow Architecture

```mermaid
graph LR
    Client["Client Browser<br/>(HTML/CSS/JS)"]
    Django["Django Framework<br/>(Views & Models)"]
    ORM["Django ORM<br/>(Query Builder)"]
    MySQL["MySQL Database<br/>(Tables & Indices)"]
    
    Client -->|HTTP Request| Django
    Django -->|Return Response| Client
    Django -->|Query/Save| ORM
    ORM -->|SQL Commands| MySQL
    MySQL -->|Result Set| ORM
    ORM -->|Data Objects| Django
    
    style Client fill:#e1f5ff
    style Django fill:#fff3e0
    style ORM fill:#f3e5f5
    style MySQL fill:#e8f5e9
```

## 2. User Authentication & Registration Flow

```mermaid
graph TD
    A["User Visits Site"] -->|Access /register| B["Registration Page"]
    B -->|Fill Form| C["Validate Input"]
    C -->|Invalid| D["Show Errors"]
    D -->|Re-enter| B
    C -->|Valid| E["Create User Object"]
    E -->|Hash Password| F["Store in DB"]
    F -->|Success| G["Redirect to Login"]
    G -->|Enter Credentials| H["Login Page"]
    H -->|Submit| I["Authenticate User"]
    I -->|Invalid| J["Show Error"]
    J -->|Retry| H
    I -->|Valid| K["Create Session"]
    K -->|Set Role| L["Redirect to Dashboard"]
    L -->|Display| M["User Dashboard"]
    
    style A fill:#e3f2fd
    style B fill:#e3f2fd
    style C fill:#fff3e0
    style E fill:#fff3e0
    style F fill:#e8f5e9
    style L fill:#c8e6c9
    style M fill:#c8e6c9
```

## 3. Event Creation & Management Workflow

```mermaid
graph TD
    A["Organizer Login"] -->|Role: Organizer| B["Access Dashboard"]
    B -->|Click Create Event| C["Event Form"]
    C -->|Fill Details| D["Validate Form"]
    D -->|title, description,<br/>location, dates| E{"All Required<br/>Fields?"}
    E -->|No| F["Show Validation Errors"]
    F -->|Fix| C
    E -->|Yes| G["Create Event Object"]
    G -->|Set Status=Draft| H["Save to Database"]
    H -->|Success| I["Edit Event Details"]
    I -->|Add Volunteers| J["Manage Volunteers"]
    J -->|Enable Attendance| K["Set attendanceEnabled=True"]
    K -->|Publish Event| L["Set Status=Published"]
    L -->|Event Visible| M["Event Listed for Registration"]
    M -->|Deadline Passed| N["Set Status=Expired"]
    M -->|Cancel Event| O["Set Status=Cancelled"]
    
    style A fill:#e3f2fd
    style G fill:#fff3e0
    style H fill:#e8f5e9
    style L fill:#c8e6c9
    style M fill:#c8e6c9
```

## 4. Event Registration & Approval Flow

```mermaid
graph TD
    A["Participant Views Events"] -->|Browse Events| B["Select Event"]
    B -->|Click Register| C["Check Prerequisites"]
    C -->|Verify Capacity| D{"Capacity<br/>Available?"}
    D -->|No| E["Show Error:<br/>Event Full"]
    D -->|Yes| F["Check Deadline"]
    F -->|Passed| G["Show Error:<br/>Deadline Passed"]
    F -->|Valid| H["Check Duplicate"]
    H -->|Exists| I["Show Error:<br/>Already Registered"]
    H -->|New| J["Create Registration"]
    J -->|Set Status=Pending| K["Save to Database"]
    K -->|Notify Organizer| L["Organizer Receives<br/>Notification"]
    L -->|Organizer Reviews| M["Registration List"]
    M -->|Approve| N["Update Status=Approved"]
    M -->|Reject| O["Update Status=Rejected"]
    N -->|Notify User| P["Participant Approved<br/>Can Attend Event"]
    O -->|Notify User| Q["Participant Rejected"]
    
    style A fill:#e3f2fd
    style J fill:#fff3e0
    style K fill:#e8f5e9
    style P fill:#c8e6c9
    style Q fill:#ffcdd2
```

## 5. QR Code Generation & Attendance Tracking Flow

```mermaid
graph TD
    A["Event Date Arrives"] -->|Organizer Enables| B["Attendance Tracking ON"]
    B -->|Generate QR Code| C["Call generate_qr_token"]
    C -->|user_id = 123| D["Create HMAC-SHA256<br/>Signature"]
    D -->|key = SECRET_KEY<br/>msg = user_id| E["Token = 123:abc123..."]
    E -->|Encode to QR| F["QR Code Generated"]
    F -->|Distribute to Users| G["QR Code Ready"]
    G -->|Event Time| H["Volunteer at Gate"]
    H -->|Participant Arrives| I["Scan QR Code"]
    I -->|Get Token| J["Parse Token String"]
    J -->|Call verify_qr_token| K["Verify HMAC Signature"]
    K -->|Compare Signatures| L{"Token<br/>Valid?"}
    L -->|No| M["Check-in Failed<br/>Show Error"]
    L -->|Yes| N["Extract user_id"]
    N -->|Get User & Event| O["Create Attendance Record"]
    O -->|Set checkInTime=NOW| P["Set checkedInBy=Volunteer"]
    P -->|Save to DB| Q["Check-in Success"]
    Q -->|Confirmation| R["Check-in Time Recorded"]
    R -->|Event Ends| S["User Checks Out"]
    S -->|Set checkOutTime=NOW| T["Calculate Duration"]
    T -->|Save| U["Attendance Complete"]
    
    style B fill:#fff3e0
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e8f5e9
    style I fill:#e3f2fd
    style K fill:#f3e5f5
    style L fill:#ffe0b2
    style Q fill:#c8e6c9
```

## 6. Database Query Flow - Event Registration

```mermaid
graph TD
    A["User Submits Registration"] -->|POST /register/event_id| B["View Function"]
    B -->|Get user = request.user| C["Database Query 1"]
    C -->|SELECT * FROM users WHERE id=...| D["User Object"]
    B -->|Get event = Event.objects.get| E["Database Query 2"]
    E -->|SELECT * FROM events WHERE id=...| F["Event Object"]
    B -->|Check existing| G["Database Query 3"]
    G -->|SELECT COUNT FROM registrations<br/>WHERE user_id=? AND event_id=?| H["Duplicate Check"]
    B -->|Verify capacity| I["Database Query 4"]
    I -->|SELECT COUNT FROM registrations<br/>WHERE event_id=?<br/>AND status=approved| J["Registration Count"]
    B -->|Compare with capacity| K{"Count <br/>Capacity?"}
    K -->|No| L["Reject - Full"]
    K -->|Yes| M["Create Registration"]
    M -->|INSERT into registrations| N["Database Write"]
    N -->|registration_id, user_id,<br/>event_id, status=pending| O["Save Complete"]
    O -->|Return to User| P["Confirmation Page"]
    
    style A fill:#e3f2fd
    style B fill:#fff3e0
    style C fill:#f3e5f5
    style D fill:#e8f5e9
    style N fill:#e8f5e9
    style P fill:#c8e6c9
```

## 7. Role-Based Access Control Flow

```mermaid
graph TD
    A["User Makes Request"] -->|GET /events/create| B["Check Authentication"]
    B -->|Is Logged In?| C{"Authenticated?"}
    C -->|No| D["Redirect to Login"]
    C -->|Yes| E["Get User Role"]
    E -->|role = request.user.role| F{"Role in<br/>Allowed Roles?"}
    F -->|Admin| G["Grant Access"]
    F -->|Organizer| G
    F -->|Volunteer| H["Check Specific Permission"]
    F -->|Participant| I["Deny Access"]
    G -->|Load Resource| J["Display View/Template"]
    H -->|Has Permission?| K{"Allowed?"}
    K -->|Yes| G
    K -->|No| I
    I -->|Redirect| L["Unauthorized Page"]
    
    style A fill:#e3f2fd
    style B fill:#fff3e0
    style C fill:#ffe0b2
    style G fill:#c8e6c9
    style I fill:#ffcdd2
    style L fill:#ffcdd2
```

## 8. Complete Event Lifecycle Flow

```mermaid
graph LR
    A["Event Created<br/>Status: Draft"] -->|Organizer Configures| B["Event Details Set"]
    B -->|Add Volunteers| C["Volunteers Assigned"]
    C -->|Publish| D["Status: Published"]
    D -->|Registrations Open| E["Users Register"]
    E -->|Organizer Approves| F["Registration Approved"]
    F -->|Check-in Enabled| G["Attendance Ready"]
    G -->|Event Date| H["Check-ins Recorded"]
    H -->|Event Time| I["Status: Expired"]
    I -->|View Reports| J["Attendance Summary"]
    
    D -->|Cancel Before| K["Status: Cancelled"]
    K -->|Notify Users| L["Event Cancelled"]
    
    style A fill:#fff3e0
    style D fill:#c8e6c9
    style E fill:#e3f2fd
    style H fill:#c8e6c9
    style I fill:#fff9c4
    style K fill:#ffcdd2
```

## 9. Attendance Check-in Process Flow

```mermaid
sequenceDiagram
    participant P as Participant
    participant V as Volunteer
    participant S as System
    participant DB as Database
    
    P->>V: Arrives at Event
    V->>P: "Scan QR Code"
    P->>S: Scans QR (token)
    S->>S: Parse Token
    S->>S: Verify HMAC Signature
    alt Token Valid
        S->>DB: Create Attendance Record
        DB->>DB: checkInTime = NOW()
        DB->>DB: checkedInBy = Volunteer
        DB->>S: Success
        S->>V: ✓ Check-in Complete
        V->>P: "Welcome!"
    else Token Invalid
        S->>V: ✗ Invalid QR Code
        V->>P: "Try Again"
    end
```

## 10. Data Relationships & Constraints

```mermaid
graph TD
    U["User<br/>- id<br/>- role<br/>- email"]
    E["Event<br/>- id<br/>- title<br/>- organizer_id<br/>- status"]
    R["Registration<br/>- id<br/>- user_id<br/>- event_id<br/>- status"]
    A["Attendance<br/>- id<br/>- user_id<br/>- event_id<br/>- checkInTime"]
    V["Volunteers<br/>Many-to-Many<br/>event_id, user_id"]
    
    U -->|Organizes| E
    U -->|Many| R
    U -->|Many| A
    U -->|Many| V
    E -->|One-to-Many| R
    E -->|One-to-Many| A
    E -->|Many| V
    R -->|One| U
    R -->|One| E
    R -->|Has One| A
    A -->|One| U
    A -->|One| E
    A -->|One| R
    
    U -.->|Scanned By| A
    
    style U fill:#e3f2fd
    style E fill:#fff3e0
    style R fill:#f3e5f5
    style A fill:#e8f5e9
    style V fill:#fce4ec
```

## 11. Module Interaction Flow

```mermaid
graph TB
    ACC["Accounts Module<br/>- Register<br/>- Login<br/>- Profile"]
    
    DASH["Dashboard Module<br/>- Display Stats<br/>- Show Events"]
    
    EV["Events Module<br/>- Create Event<br/>- Edit Event<br/>- Manage Volunteers"]
    
    REG["Registrations Module<br/>- Register for Event<br/>- Approve/Reject<br/>- Manage"]
    
    ATT["Attendance Module<br/>- Generate QR<br/>- Verify QR<br/>- Check-in/out"]
    
    ADMIN["Admin Panel<br/>- User Mgmt<br/>- Event Approval<br/>- Statistics"]
    
    ACC -->|Authenticate| DASH
    DASH -->|View| EV
    DASH -->|View| REG
    DASH -->|View| ATT
    
    EV -->|Organizer| ADMIN
    REG -->|User/Organizer| EV
    ATT -->|Volunteer| EV
    REG -->|Create| ATT
    ADMIN -->|Manage| ACC
    ADMIN -->|Manage| EV
    
    style ACC fill:#e3f2fd
    style DASH fill:#fff3e0
    style EV fill:#fff3e0
    style REG fill:#f3e5f5
    style ATT fill:#e8f5e9
    style ADMIN fill:#fce4ec
```

## 12. Request-Response Cycle

```mermaid
graph LR
    A["HTTP Request<br/>GET/POST"] -->|URL Path| B["URL Router"]
    B -->|Match Pattern| C["View Function"]
    C -->|Authenticate| D["Middleware<br/>Auth Check"]
    D -->|Valid?| E{"Permission<br/>Check"}
    E -->|No| F["401/403 Response"]
    E -->|Yes| G["Query Database"]
    G -->|ORM| H["Get Data"]
    H -->|Process Data| I["Render Template"]
    I -->|HTML/JSON| J["HTTP Response"]
    J -->|Send to| K["Client Browser"]
    
    F -->|Error Page| K
    
    style A fill:#e3f2fd
    style B fill:#fff3e0
    style C fill:#fff3e0
    style G fill:#f3e5f5
    style H fill:#e8f5e9
    style K fill:#c8e6c9
```

## 13. Error Handling Flow

```mermaid
graph TD
    A["User Action"] -->|Execute Code| B["Try Block"]
    B -->|Process| C["Check Conditions"]
    C -->|Valid| D["Complete Action"]
    C -->|Invalid| E{"Exception<br/>Type"}
    E -->|DuplicateRegistration| F["Error: Already Registered"]
    E -->|EventCapacityExceeded| G["Error: Event Full"]
    E -->|RegistrationDeadlineExceeded| H["Error: Deadline Passed"]
    E -->|InvalidQRToken| I["Error: Invalid QR Code"]
    E -->|UnauthorizedAccess| J["Error: No Permission"]
    E -->|ValidationError| K["Error: Invalid Input"]
    F -->|Display| L["Error Message to User"]
    G -->|Display| L
    H -->|Display| L
    I -->|Display| L
    J -->|Display| L
    K -->|Display| L
    L -->|Redirect| M["User Retries or Cancels"]
    D -->|Success| N["Redirect to Success"]
    
    style A fill:#e3f2fd
    style B fill:#fff3e0
    style D fill:#c8e6c9
    style E fill:#ffe0b2
    style L fill:#ffcdd2
    style N fill:#c8e6c9
```

## 14. Database Write Operations Flow

```mermaid
graph TD
    A["User Submits Form"] -->|Validated Data| B["Create Model Instance"]
    B -->|user = User(...)|  C["In-Memory Object"]
    C -->|Call save()| D["Pre-save Signal"]
    D -->|Validation| E{"All Valid?"}
    E -->|No| F["Raise ValidationError"]
    F -->|Display to User| G["Show Errors"]
    E -->|Yes| H["Generate SQL"]
    H -->|INSERT/UPDATE| I["Django ORM"]
    I -->|Transaction| J["MySQL Database"]
    J -->|Lock Table| K["Write Data"]
    K -->|Commit| L["Auto-increment ID"]
    L -->|Release Lock| M["Post-save Signal"]
    M -->|Update In-Memory| N["Success Response"]
    N -->|Redirect| O["Confirmation Page"]
    
    style A fill:#e3f2fd
    style B fill:#fff3e0
    style H fill:#f3e5f5
    style J fill:#e8f5e9
    style N fill:#c8e6c9
```

## 15. QR Token Generation & Verification Algorithm Flow

```mermaid
graph TD
    A["User Participates<br/>user_id = 123"] -->|Generate Token| B["Call generate_qr_token"]
    B -->|Input: user_id=123| C["Get SECRET_KEY<br/>from Settings"]
    C -->|Convert to Bytes| D["key = SECRET_KEY.encode()"]
    D -->|Create Message| E["msg = str(123).encode()"]
    E -->|HMAC-SHA256| F["signature = hmac.new<br/>key, msg, sha256"]
    F -->|Hash Output| G["signature = abc123..."]
    G -->|Format Token| H["token = '123:abc123...'"]
    H -->|Encode to QR| I["QR Code Image"]
    I -->|Share with User| J["QR Ready for Scan"]
    
    J -->|Later: Event Time| K["Volunteer Scans"]
    K -->|Read Token| L["token = '123:abc123...'"]
    L -->|Verify Token| M["Call verify_qr_token"]
    M -->|Parse String| N["user_id_str, signature<br/>= token.split(':')"]
    N -->|Extract ID| O["user_id = 123"]
    O -->|Regenerate Signature| P["Get SECRET_KEY"]
    P -->|Recreate HMAC| Q["expected_sig =<br/>hmac.new(key, msg, sha256)"]
    Q -->|Compare| R["hmac.compare_digest<br/>expected vs provided"]
    R -->|Safe Comparison| S{"Match?"}
    S -->|Yes| T["Valid Token<br/>Return user_id"]
    S -->|No| U["Invalid Token<br/>Return None"]
    T -->|Create Attendance| V["Attendance Record Saved"]
    U -->|Reject| W["Check-in Failed"]
    
    style B fill:#fff3e0
    style C fill:#f3e5f5
    style F fill:#f3e5f5
    style I fill:#e8f5e9
    style M fill:#fff3e0
    style Q fill:#f3e5f5
    style R fill:#ffe0b2
    style T fill:#c8e6c9
    style W fill:#ffcdd2
```

## 16. Complete User Journey - End-to-End

```mermaid
graph TD
    A["1. New User<br/>Visits Site"] -->|Home Page| B["2. Browse Events"]
    B -->|Click Event| C["3. View Details"]
    C -->|Not Logged In| D["4. Redirect to Login"]
    D -->|No Account?| E["5. Register"]
    E -->|Fill Form| F["6. Account Created<br/>Role: Participant"]
    F -->|Auto Login| G["7. Dashboard"]
    G -->|Search Events| B
    B -->|Select Event| C
    C -->|Click Register| H["8. Registration Form"]
    H -->|Submit| I["9. Registration Created<br/>Status: Pending"]
    I -->|Wait| J["10. Organizer Reviews"]
    J -->|Approve| K["11. Status: Approved<br/>Notification Sent"]
    K -->|Event Date| L["12. Receive QR Code"]
    L -->|Arrive at Event| M["13. Volunteer Scans QR"]
    M -->|Valid QR| N["14. Check-in Success"]
    N -->|Participate| O["15. Event Time"]
    O -->|Event Ends| P["16. Check-out"]
    P -->|View History| Q["17. Dashboard<br/>Attendance Recorded"]
    
    style A fill:#e3f2fd
    style F fill:#c8e6c9
    style I fill:#fff3e0
    style K fill:#c8e6c9
    style N fill:#c8e6c9
    style Q fill:#e8f5e9
```
