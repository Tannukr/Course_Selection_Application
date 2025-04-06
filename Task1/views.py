from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from .serializers import UserSerializer, CourseSerializer, StudentSerializer
from rest_framework.authtoken.models import Token
from .permissions import IsFaculty, IsStudent
from django.shortcuts import get_object_or_404
from .models import Course, Student, User
from rest_framework.permissions import IsAuthenticated

# API Views
class RegisterView(APIView):
    def post(self,request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username = username,password = password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'message': 'Login successful',
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'token': token.key
            }, status=status.HTTP_200_OK)
        return Response({'message':'Invalid credentials'}, status = status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self,request):
        request.user.auth_token.delete()
        return Response({'message':'Logout successful'},status = status.HTTP_200_OK)

class GetCoursesView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsFaculty]

    def get(self, request):
        courses = Course.objects.filter(instructor=request.user)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        # Make sure we have the necessary fields
        if 'course_name' not in request.data or 'course_code' not in request.data:
            return Response({
                'error': 'Course name and course code are required'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # Convert field names if necessary
        data = request.data.copy()
        
        serializer = CourseSerializer(data=data)
        if serializer.is_valid():
            serializer.save(instructor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateCourseView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsFaculty]

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id, instructor=request.user)
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, course_id):
        course = get_object_or_404(Course, id=course_id, instructor=request.user)
        
        print(f"Updating course {course_id} (original: {course.course_name}, {course.course_code}) with data: {request.data}")
        
        # Ensure we're updating the existing course with the instance parameter
        serializer = CourseSerializer(instance=course, data=request.data, partial=True)
        
        if serializer.is_valid():
            updated_course = serializer.save()
            print(f"Course updated successfully: {updated_course.course_name}, {updated_course.course_code}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        print(f"Validation errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, course_id):
        course = get_object_or_404(Course, id=course_id, instructor=request.user)
        course.delete()
        return Response({'message': 'Course deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class AvailableCoursesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Get all courses taught by faculty members (not by the current student)
        if request.user.role == 'Student':
            courses = Course.objects.filter(instructor__role='Faculty')
        else:
            courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RegisterCourseView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def post(self, request, course_id):
        if request.user.role != 'Student':
            return Response({'error': 'User is not a student'}, status=status.HTTP_403_FORBIDDEN)
        
        student, created = Student.objects.get_or_create(user=request.user)
        
        if student.courses.count() >= 2:
            return Response({'message': 'You have already registered for 2 courses'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        course = get_object_or_404(Course, id=course_id)

        if student.courses.filter(id=course.id).exists():
            return Response({'message': 'You already registered for this course'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        student.courses.add(course)
        return Response({'message': 'Course registered successfully'}, status=status.HTTP_200_OK)
    
class GetRegisteredCoursesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            # Get or create a student profile for the current user
            student, created = Student.objects.get_or_create(user=request.user)
            courses = student.courses.all()
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CourseRegistrationStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsFaculty]

    def get(self, request):
        courses = Course.objects.filter(instructor=request.user)
        stats = []
        for course in courses:
            course_stats = {
                'course_name': course.course_name,
                'course_code': course.course_code,
                'total_students': course.students.count(),
                'registered_students': [
                    {
                        'username': student.user.username,
                        'email': student.user.email
                    } for student in course.students.all()
                ]
            }
            stats.append(course_stats)
        return Response(stats, status=status.HTTP_200_OK)
