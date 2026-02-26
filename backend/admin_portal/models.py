from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    matric_number = models.CharField(max_length=30, unique=True)
    department = models.CharField(max_length=100)
    level = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.matric_number})"


class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=120)
    units = models.PositiveSmallIntegerField(default=3)

    def __str__(self):
        return f"{self.code} - {self.title}"


class Enrollment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.matric_number} - {self.course.code}"


class Result(models.Model):
    PASS = 'PASS'
    FAIL = 'FAIL'
    STATUS_CHOICES = [(PASS, 'Pass'), (FAIL, 'Fail')]

    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='result')
    marks = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=2, blank=True)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    status = models.CharField(max_length=4, choices=STATUS_CHOICES, blank=True)
    released = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.marks < 0 or self.marks > 100:
            raise ValidationError('Marks must be between 0 and 100.')

    @staticmethod
    def calculate_grade_and_gpa(marks):
        marks = float(marks)
        if marks >= 70:
            return 'A', 4.00
        if marks >= 60:
            return 'B', 3.00
        if marks >= 50:
            return 'C', 2.00
        if marks >= 45:
            return 'D', 1.00
        return 'F', 0.00

    def save(self, *args, **kwargs):
        self.grade, self.gpa = self.calculate_grade_and_gpa(self.marks)
        if not self.status:
            self.status = self.PASS if self.grade != 'F' else self.FAIL
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.enrollment} - {self.grade}"
