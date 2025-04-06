# Course Management System

A modern web-based Course Management System built with Django that allows students to enroll in courses and faculty members to manage course offerings.

## Features

### For Students
- User registration and authentication
- Browse available courses
- Enroll in up to 2 courses
- View enrolled courses
- Drop courses when needed

### For Faculty
- User registration and authentication
- Create new courses
- Manage existing courses
- View enrolled students count
- Update course information

### General Features
- Clean and modern user interface
- Secure authentication system
- Role-based access control
- Responsive design for all devices
- Traditional form submissions (no JavaScript required)

## Technical Details

### Built With
- Django (Backend Framework)
- HTML5 & CSS3 (Frontend)
- PostgreSQL (Database)

### Security Features
- CSRF protection
- Password hashing
- Session management
- Form validation

## Pages and Functionality

### 1. Home Page
- Welcome message
- Login and Register buttons
- Feature highlights for students and faculty

### 2. Login Page
- Username and password fields
- Error message display
- Link to registration page
- Back to home navigation

### 3. Registration Page
- User information fields (username, email, password)
- Role selection (student/faculty)
- Form validation
- Error message display

### 4. Student Dashboard
- View enrolled courses
- Course enrollment functionality
- Maximum 2 courses limit
- Course dropping capability
- Display of course details

### 5. Faculty Dashboard
- Course creation form
- List of created courses
- Student enrollment count
- Course management options

## Routes

### Authentication
- `/register/` - Register a new user
- `/login/` - User login
- `/logout/` - User logout

### Main Pages
- `/` - Home page
- `/student-dashboard/` - Student dashboard for course management
- `/faculty-dashboard/` - Faculty dashboard for course management

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

## Usage Instructions

### First Time Setup
1. Navigate to http://127.0.0.1:8000/
2. Register a new account by clicking "Register"
3. Select a role (Student or Faculty)
4. Login with your new account

### Faculty Workflow
1. After logging in, you'll be directed to the faculty dashboard
2. Click "Create New Course" to add a new course
3. Fill in course details (name, code, credits)
4. View created courses on your dashboard
5. Edit or delete courses using the buttons on each course card
6. View students enrolled in each course

### Student Workflow
1. After logging in, you'll be directed to the student dashboard
2. View available courses in the "Available Courses" section
3. Register for courses (maximum 2) by clicking "Enroll"
4. View your registered courses
5. Drop courses when needed using the "Drop" button

