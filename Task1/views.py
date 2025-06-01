from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, Course, Student

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if hasattr(request.user, 'student_profile') or request.user.role == 'Student':
                return redirect('student-dashboard')
            return redirect('faculty-dashboard')
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not all([username, password]):
            messages.error(request, 'Please fill in all fields')
            return render(request, 'login.html', {'error_message': 'Please fill in all fields'})

        user = authenticate(username=username, password=password)
        
        if user is None:
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})

        login(request, user)
        
        # Check both student profile and role
        if hasattr(user, 'student_profile') or user.role == 'Student':
            return redirect('student-dashboard')
        return redirect('faculty-dashboard')

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if not all([username, email, password, role]):
            return render(request, 'register.html', {'error_message': 'Please fill in all fields'})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error_message': 'Username already exists'})

        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error_message': 'Email already exists'})

        try:
            # Create the user with role
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role='Student' if role.lower() == 'student' else 'Faculty'
            )

            # If student, create profile
            if role.lower() == 'student':
                Student.objects.create(user=user)

            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')

        except Exception as e:
            print(f"Error during registration: {str(e)}")
            return render(request, 'register.html', {'error_message': str(e)})


class StudentDashboardView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        # Check if user is a student
        if not hasattr(request.user, 'student_profile'):
            messages.error(request, 'Access denied. Student account required.')
            return redirect('login')
        
        enrolled_courses = request.user.student_profile.courses.all()
        available_courses = Course.objects.exclude(id__in=[course.id for course in enrolled_courses])
        
        return render(request, 'student-dashboard.html', {
            'enrolled_courses': enrolled_courses,
            'available_courses': available_courses,
            'can_enroll': enrolled_courses.count() < 2  # Add this to check if student can enroll in more courses
        })

    def post(self, request):
        # Check if user is a student
        if not hasattr(request.user, 'student_profile'):
            messages.error(request, 'Access denied. Student account required.')
            return redirect('login')

        action = request.POST.get('action')
        course_id = request.POST.get('course_id')

        try:
            course = Course.objects.get(id=course_id)
            if action == 'enroll':
                # Check if student has already enrolled in 2 courses
                enrolled_count = request.user.student_profile.courses.count()
                if enrolled_count >= 2:
                    messages.error(request, 'You cannot enroll in more than 2 courses.')
                else:
                    request.user.student_profile.courses.add(course)
                    messages.success(request, f'Successfully enrolled in {course.course_name}')
            elif action == 'drop':
                request.user.student_profile.courses.remove(course)
                messages.success(request, f'Successfully dropped {course.course_name}')
        except Course.DoesNotExist:
            messages.error(request, 'Course not found')
        except Exception as e:
            messages.error(request, str(e))

        return redirect('student-dashboard')

class FacultyDashboardView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        if hasattr(request.user, 'student_profile'):
            return redirect('student-dashboard')
        
        courses = Course.objects.filter(instructor=request.user)
        return render(request, 'faculty-dashboard.html', {'courses': courses})

    def post(self, request):
        if hasattr(request.user, 'student_profile'):
            return redirect('student-dashboard')

        action = request.POST.get('action')
        course_id = request.POST.get('course_id')
        
        if action == 'create':
            name = request.POST.get('name')
            code = request.POST.get('code')
            credits = request.POST.get('credits')

            try:
                Course.objects.create(
                    course_name=name,
                    course_code=code,
                    credits=credits,
                    instructor=request.user
                )
                messages.success(request, f'Successfully created course {name}')
            except Exception as e:
                messages.error(request, str(e))

        elif action == 'delete' and course_id:
            try:
                course = Course.objects.get(id=course_id, instructor=request.user)
                course.delete()
                messages.success(request, 'Course deleted successfully')
            except Course.DoesNotExist:
                messages.error(request, 'Course not found')

        elif action == 'update' and course_id:
            try:
                course = Course.objects.get(id=course_id, instructor=request.user)
                course.course_name = request.POST.get('name', course.course_name)
                course.course_code = request.POST.get('code', course.course_code)
                course.credits = request.POST.get('credits', course.credits)
                course.save()
                messages.success(request, 'Course updated successfully')
            except Course.DoesNotExist:
                messages.error(request, 'Course not found')
            except Exception as e:
                messages.error(request, str(e))

        return redirect('faculty-dashboard')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')
