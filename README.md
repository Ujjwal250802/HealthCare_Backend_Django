# Django Healthcare Backend

A comprehensive healthcare management system built with Django REST Framework, featuring JWT authentication, patient management, doctor management, and patient-doctor mapping functionality.

## Features

- **Authentication System**: JWT-based authentication with user registration and login
- **Patient Management**: Full CRUD operations for patient records (authenticated users only)
- **Doctor Management**: Complete CRUD functionality for doctor profiles
- **Patient-Doctor Mapping**: System for assigning patients to doctors
- **PostgreSQL Integration**: Robust database with Django ORM
- **Security**: Environment-based configuration and proper authentication

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

## Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Database Setup
Make sure PostgreSQL is running and create a database:
```sql
CREATE DATABASE healthcare_db;
```

### 3. Environment Configuration
Copy the example environment file and update with your settings:
```bash
cp .env.example .env
```

Edit `.env` with your PostgreSQL credentials:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=healthcare_db
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
```

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 6. Start Development Server
```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

## API Endpoints

### Authentication APIs
- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/login/` - Login user and get JWT token
- `GET /api/auth/profile/` - Get current user profile
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Patient Management APIs
- `POST /api/patients/` - Add a new patient
- `GET /api/patients/` - Get all patients (user's own)
- `GET /api/patients/<id>/` - Get specific patient details
- `PUT /api/patients/<id>/` - Update patient details
- `DELETE /api/patients/<id>/` - Delete patient record

### Doctor Management APIs
- `POST /api/doctors/` - Add a new doctor
- `GET /api/doctors/` - Get all doctors
- `GET /api/doctors/<id>/` - Get specific doctor details
- `PUT /api/doctors/<id>/` - Update doctor details
- `DELETE /api/doctors/<id>/` - Delete doctor record

### Patient-Doctor Mapping APIs
- `POST /api/mappings/` - Assign doctor to patient
- `GET /api/mappings/` - Get all mappings
- `GET /api/mappings/<patient_id>/` - Get doctors for specific patient
- `PUT /api/mappings/<id>/` - Update mapping
- `DELETE /api/mappings/<id>/` - Remove doctor from patient

## Testing with Postman

### 1. Register a User
```
POST http://127.0.0.1:8000/api/auth/register/
Content-Type: application/json

{
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "testpass123",
    "password_confirm": "testpass123"
}
```

### 2. Login
```
POST http://127.0.0.1:8000/api/auth/login/
Content-Type: application/json

{
    "email": "test@example.com",
    "password": "testpass123"
}
```

### 3. Use JWT Token
Add to headers for authenticated requests:
```
Authorization: Bearer <your-access-token>
```

### 4. Create a Patient
```
POST http://127.0.0.1:8000/api/patients/
Authorization: Bearer <your-access-token>
Content-Type: application/json

{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone_number": "+1234567890",
    "date_of_birth": "1990-01-01",
    "gender": "M",
    "blood_group": "O+",
    "address_line_1": "123 Main St",
    "city": "New York",
    "state": "NY",
    "postal_code": "10001",
    "emergency_contact_name": "Jane Doe",
    "emergency_contact_phone": "+1234567891"
}
```

## Project Structure

```
healthcare_project/
├── healthcare_project/     # Main project settings
├── authentication/        # User authentication app
├── patients/              # Patient management app
├── doctors/               # Doctor management app
├── mappings/              # Patient-doctor mapping app
├── manage.py
├── requirements.txt
└── README.md
```

## Admin Panel

Access the Django admin at `http://127.0.0.1:8000/admin/` using your superuser credentials to manage data through a web interface.

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check database credentials in `.env`
- Verify database exists

### Migration Issues
```bash
python manage.py makemigrations --empty <app_name>
python manage.py migrate --fake-initial
```

### Permission Errors
- Ensure you're sending the JWT token in the Authorization header
- Check token hasn't expired (60 minutes by default)

## Security Notes

- Never commit `.env` file to version control
- Use strong SECRET_KEY in production
- Set DEBUG=False in production
- Configure proper CORS settings for production