from django.urls import path

from . import views

app_name = 'admin_portal'

urlpatterns = [
    path('login/', views.AdminLoginView.as_view(), name='login'),
    path('register/', views.admin_register, name='register'),
    path('logout/', views.admin_logout, name='logout'),
    path('dashboard/', views.admin_dashboard, name='dashboard'),
    path('students/', views.student_list, name='student_list'),
    path('students/new/', views.student_create, name='student_create'),
    path('students/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/new/', views.course_create, name='course_create'),
    path('courses/<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('enrollments/', views.enrollment_list, name='enrollment_list'),
    path('enrollments/new/', views.enrollment_create, name='enrollment_create'),
    path('enrollments/<int:pk>/approve/', views.enrollment_approve, name='enrollment_approve'),
    path('results/', views.result_list, name='result_list'),
    path('results/new/', views.result_create, name='result_create'),
    path('results/<int:pk>/edit/', views.result_edit, name='result_edit'),
]
