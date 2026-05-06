# Event Manager

A comprehensive Django-based event management system with QR code attendance tracking, user authentication, and administrative capabilities.

## Features

- **Event Management**: Create, edit, and manage events with status tracking
- **User Accounts**: Secure user registration and authentication with role-based access
- **Attendance Tracking**: QR code-based attendance system for events
- **Event Registrations**: Users can register for events and track their registrations
- **Admin Panel**: Comprehensive admin dashboard for system administrators
- **User Dashboard**: Personalized dashboard for regular users
- **Volunteer Management**: Manage volunteers for events
- **Role-Based Access Control**: Different user roles with appropriate permissions

## Project Structure

```
event_manager/
├── accounts/              # User authentication and account management
├── admin_panel/           # Admin dashboard and management
├── attendance/            # QR code-based attendance tracking
├── dashboard/             # User dashboard
├── events/                # Event management system
├── registrations/         # Event registration system
├── event_manager/         # Main project configuration
└── templates/             # HTML templates for all apps
```

### Key Modules

- **accounts**: User registration, login, and profile management
- **admin_panel**: Administrative functions and system management
- **attendance**: QR code generation and attendance marking
- **events**: Event creation, editing, and volunteer management
- **registrations**: Event registration and management
- **dashboard**: User dashboard and overview

## Technologies Used

- **Framework**: Django 6.0.2
- **Database**: MySQL (via mysqlclient)
- **Environment**: Python 3.x, python-dotenv
- **QR Code**: QR code generation and scanning capabilities

## Installation

### Prerequisites

- Python 3.8 or higher
- MySQL 5.7 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd event_manager
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the template
   cp .env.template .env
   
   # Edit .env with your configuration
   ```

5. **Set up the database**
   ```bash
   # Run migrations
   python manage.py migrate
   
   # Create superuser for admin access
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

   The application will be available at `http://localhost:8000`

## Usage

### Accessing the Application

- **Main Site**: `http://localhost:8000/`
- **Admin Panel**: `http://localhost:8000/admin/`

### User Roles

- **Admin**: Full system access and management capabilities
- **Event Manager**: Can create and manage events
- **Volunteer**: Can help with event operations
- **Participant**: Can register for and attend events

## Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_NAME=event_manager
DATABASE_USER=root
DATABASE_PASSWORD=your-password
DATABASE_HOST=localhost
DATABASE_PORT=3306
```

## Development

### Running Tests

```bash
python manage.py test
```

### Database Migrations

```bash
# Create migration files
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# View migration status
python manage.py showmigrations
```

### Admin Panel

Access the Django admin interface to manage users, events, and registrations:

```
URL: http://localhost:8000/admin/
```

## Project Apps

### Accounts (`accounts/`)
- User registration and authentication
- User profile management
- Role assignment

### Events (`events/`)
- Event creation and editing
- Event status management
- Volunteer assignment

### Attendance (`attendance/`)
- QR code generation for events
- Attendance marking
- Attendance history tracking

### Registrations (`registrations/`)
- Event registration management
- Registration tracking
- User registration history

### Dashboard (`dashboard/`)
- User dashboard overview
- Quick access to events and registrations

### Admin Panel (`admin_panel/`)
- Administrative functions
- System management
- User and event administration

## Directory Structure

```
event_manager/
├── manage.py                          # Django management script
├── requirements.txt                   # Project dependencies
├── .env.template                      # Environment variables template
├── event_manager/                     # Main project folder
│   ├── settings.py                    # Django settings
│   ├── urls.py                        # Main URL configuration
│   ├── asgi.py                        # ASGI configuration
│   ├── wsgi.py                        # WSGI configuration
│   └── templates/                     # Main templates
└── [apps]/                            # Individual app directories
    ├── models.py                      # Database models
    ├── views.py                       # View functions
    ├── urls.py                        # URL routing
    ├── admin.py                       # Admin configuration
    ├── apps.py                        # App configuration
    ├── tests.py                       # Test cases
    ├── migrations/                    # Database migrations
    └── templates/                     # App-specific templates
```

## Features in Detail

### QR Code Attendance System
- Generate unique QR codes for events
- Scan QR codes for attendance marking
- Track attendance records per event
- Generate attendance reports

### Event Management
- Create and schedule events
- Assign volunteers to events
- Track event status (draft, published, completed)
- Manage event details and descriptions

### User Registration
- Event-based registration system
- Registration status tracking
- Registration history
- Participant management

## Troubleshooting

### Database Connection Issues
- Ensure MySQL is running
- Verify database credentials in `.env`
- Check database name and port

### Migration Errors
- Reset migrations: `python manage.py migrate --fake accounts zero`
- Re-run migrations: `python manage.py migrate`

### Port Already in Use
```bash
# Use different port
python manage.py runserver 8001
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

This project is part of an event management system.

## Support

For issues or questions, please contact the development team or create an issue in the repository.
