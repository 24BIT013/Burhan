from django.contrib import admin

from .models import Course, Enrollment, Result, StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('matric_number', 'user', 'department', 'level')
    search_fields = ('matric_number', 'user__username', 'user__first_name', 'user__last_name')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'units')
    search_fields = ('code', 'title')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'created_at')
    search_fields = ('student__matric_number', 'course__code')


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'marks', 'grade', 'gpa', 'status', 'released', 'updated_at')
    list_filter = ('status', 'released', 'grade')
    search_fields = ('enrollment__student__matric_number', 'enrollment__course__code')
