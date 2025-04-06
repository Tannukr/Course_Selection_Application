from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # Template URLs - Serve the same HTML for all frontend routes
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register'),
    path('student-dashboard/', TemplateView.as_view(template_name='student-dashboard.html'), name='student_dashboard'),
    path('faculty-dashboard/', TemplateView.as_view(template_name='faculty-dashboard.html'), name='faculty_dashboard'),

    # Authentication API URLs
    path('api/register/', views.RegisterView.as_view(), name='api_register'),
    path('api/login/', views.LoginView.as_view(), name='api_login'),
    path('api/logout/', views.LogoutView.as_view(), name='api_logout'),
    
    # Faculty API URLs - RESTful approach
    path('api/courses/stats/', views.CourseRegistrationStatsView.as_view(), name='course_stats'),
    path('api/courses/available/', views.AvailableCoursesView.as_view(), name='available_courses'),
    path('api/courses/registered/', views.GetRegisteredCoursesView.as_view(), name='registered_courses'),
    path('api/courses/<int:course_id>/register/', views.RegisterCourseView.as_view(), name='register_course'),
    path('api/courses/', views.GetCoursesView.as_view(), name='get_courses'),
    path('api/courses/<int:course_id>/', views.UpdateCourseView.as_view(), name='update_course'),
]
