from django.urls import path

from . import views

app_name = 'student_portal'

urlpatterns = [
    path('', views.StudentLoginView.as_view(), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register-course/<int:course_id>/', views.register_course, name='register_course'),
    path('drop-course/<int:course_id>/', views.drop_course, name='drop_course'),
    path('results/', views.results_view, name='results'),
    path('results/pdf/', views.download_results_pdf, name='download_results_pdf'),
    path('logout/', views.student_logout, name='logout'),
]
