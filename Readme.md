# Django Authentication API Project

A Django-based authentication system with cookie-based authentication, OTP verification, and Swagger documentation.

## Features

- User Registration with Email Verification (OTP)
- Cookie-based Authentication
- Swagger API Documentation
- CSRF Protection
- Secure Cookie Configuration
- Interactive HTML Test Interface

## Prerequisites

- Python 3.x
- Django 4.2.x
- Django REST Framework
- drf-yasg (for Swagger)
- django-cors-headers

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Documentation

### Swagger UI
Access the Swagger documentation at:
- http://localhost:8000/swagger/ (Swagger UI)
- http://localhost:8000/redoc/ (ReDoc UI)

### API Endpoints

#### Authentication Endpoints

1. **Register User**
   - URL: `/api/auth/register/`
   - Method: POST
   - Body:
     ```json
     {
         "email": "user@example.com",
         "password": "secure_password",
         "password2": "secure_password"
     }
     ```

2. **Verify OTP**
   - URL: `/api/auth/verify-otp/`
   - Method: POST
   - Body:
     ```json
     {
         "email": "user@example.com",
         "otp": "123456"
     }
     ```

3. **Login**
   - URL: `/api/auth/login/`
   - Method: POST
   - Body:
     ```json
     {
         "email": "user@example.com",
         "password": "secure_password"
     }
     ```

4. **Logout**
   - URL: `/api/auth/logout/`
   - Method: POST
   - Authentication: Required

5. **Get User Profile**
   - URL: `/api/auth/profile/`
   - Method: GET
   - Authentication: Required

6. **Resend OTP**
   - URL: `/api/auth/resend-otp/`
   - Method: POST
   - Body:
     ```json
     {
         "email": "user@example.com"
     }
     ```

## Authentication

The API uses cookie-based authentication. After successful login, the server will set an HTTP-only cookie that will be automatically included in subsequent requests.

## CSRF Protection

For POST, PUT, PATCH, and DELETE requests, include the CSRF token in the header: