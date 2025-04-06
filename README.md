# Course Management System

A full-stack web application for managing university courses, student registrations, and faculty teaching assignments.

## Overview

This Course Management System is built using Django REST Framework for the backend API and vanilla JavaScript for the frontend. It provides separate dashboards for students and faculty members with role-based access control.

## Features

### For Students
- View available courses
- Register for up to 2 courses
- View registered courses
- See course details including credits, instructor, and description

### For Faculty
- Create new courses with name, code, credits and description
- View courses they've created
- Update course details
- Delete courses
- See students enrolled in their courses

### Authentication
- User registration with role selection (Student/Faculty)
- Secure login with token-based authentication
- Logout functionality

## Technology Stack

- **Backend**: Django, Django REST Framework
- **Frontend**: HTML, CSS, JavaScript
- **Authentication**: Token-based authentication
- **Database**: SQLite (default Django database)

## Project Structure

- `Assignment/` - Main project directory
  - `settings.py` - Project settings
  - `urls.py` - Main URL configuration
- `Task1/` - Main application
  - `models.py` - Database models (User, Course, Student)
  - `views.py` - API views for handling requests
  - `serializers.py` - Serializers for converting model data to JSON
  - `urls.py` - URL routes for the application
  - `permissions.py` - Custom permissions for role-based access
  - `templates/` - HTML templates
    - `index.html` - Landing page
    - `login.html` - Login page
    - `register.html` - Registration page
    - `faculty-dashboard.html` - Faculty dashboard
    - `student-dashboard.html` - Student dashboard

## API Endpoints

### Authentication
- `POST /api/register/` - Register a new user
- `POST /api/login/` - Login and get token
- `POST /api/logout/` - Logout and invalidate token

### Faculty Endpoints
- `GET /api/courses/` - Get all courses created by the faculty
- `POST /api/courses/` - Create a new course
- `GET /api/courses/<id>/` - Get details of a specific course
- `PUT /api/courses/<id>/` - Update a course
- `DELETE /api/courses/<id>/` - Delete a course
- `GET /api/courses/stats/` - Get enrollment statistics

### Student Endpoints
- `GET /api/courses/available/` - Get all available courses
- `GET /api/courses/registered/` - Get all courses registered by the student
- `POST /api/courses/<id>/register/` - Register for a course

## Setup Instructions

### Database Setup

1. Install PostgreSQL if you haven't already:
   - [PostgreSQL Downloads](https://www.postgresql.org/download/)

2. Create a PostgreSQL database:
   ```sql
   CREATE DATABASE Task1db;
   ```

3. Configure Environment Variables:
   - Copy `.env.example` to `.env` and update with your database credentials:
   ```
   cp .env.example .env
   ```
   - Edit the `.env` file with your database credentials and other settings

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/course-management-system.git
   cd course-management-system
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```
   python manage.py migrate
   ```

4. Start the development server:
   ```
   python manage.py runserver
   ```

5. Access the application at http://127.0.0.1:8000/

### API Endpoints

- Registration: `/api/register/`
- Login: `/api/login/`
- Courses (Faculty): `/api/courses/`
- Enrollments (Student): `/api/enrollments/`

## Frontend Pages

- Home: `/`
- Login: `/login/`
- Registration: `/register/`
- Student Dashboard: `/student-dashboard/`
- Faculty Dashboard: `/faculty-dashboard/`

## Usage Instructions

### First Time Setup
1. Navigate to http://127.0.0.1:8000/
2. Register a new account by clicking "Register"
3. Select a role (Student or Faculty)
4. Login with your new account

### Faculty Workflow
1. After logging in, you'll be directed to the faculty dashboard
2. Click "Create New Course" to add a new course
3. Fill in course details (name, code, credits, description)
4. View created courses on your dashboard
5. Edit or delete courses using the buttons on each course card
6. View students enrolled in each course

### Student Workflow
1. After logging in, you'll be directed to the student dashboard
2. View available courses in the "Available Courses" tab
3. Register for courses (maximum 2) by clicking "Register for Course"
4. View your registered courses in the "My Courses" tab

