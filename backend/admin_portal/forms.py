import re

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Course, Enrollment, Result, StudentProfile


USERNAME_PATTERN = re.compile(r'^[A-Za-z0-9]+$')
PASSWORD_PATTERN = re.compile(r'^\d{5}$')


def validate_student_username(username):
    username = username or ''
    if not USERNAME_PATTERN.fullmatch(username):
        raise forms.ValidationError('Username must contain only letters and numbers.')
    return username


class AdminRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class AdminLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150)


class StudentCreateForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    matric_number = forms.CharField(max_length=30)
    department = forms.CharField(max_length=100)
    level = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'matric_number',
            'department',
            'level',
        )

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        return validate_student_username(username)

    def clean_password1(self):
        password = self.cleaned_data.get('password1', '')
        if not PASSWORD_PATTERN.fullmatch(password):
            raise forms.ValidationError('Password must be exactly 5 digits.')
        return password

    def clean_password2(self):
        return self.cleaned_data.get('password2', '')

    def clean_matric_number(self):
        matric_number = self.cleaned_data['matric_number']
        if StudentProfile.objects.filter(matric_number=matric_number).exists():
            raise forms.ValidationError('A student with this matric number already exists.')
        return matric_number

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'The two password fields must match.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class StudentUpdateForm(forms.ModelForm):
    matric_number = forms.CharField(max_length=30)
    department = forms.CharField(max_length=100)
    level = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

    def __init__(self, *args, student_profile=None, **kwargs):
        self.student_profile = student_profile
        super().__init__(*args, **kwargs)
        if student_profile:
            self.fields['matric_number'].initial = student_profile.matric_number
            self.fields['department'].initial = student_profile.department
            self.fields['level'].initial = student_profile.level

    def clean_username(self):
        username = self.cleaned_data.get('username', '')
        return validate_student_username(username)

    def clean_matric_number(self):
        matric_number = self.cleaned_data['matric_number']
        queryset = StudentProfile.objects.filter(matric_number=matric_number)
        if self.student_profile:
            queryset = queryset.exclude(pk=self.student_profile.pk)
        if queryset.exists():
            raise forms.ValidationError('A student with this matric number already exists.')
        return matric_number

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = self.student_profile or StudentProfile(user=user)
        profile.user = user
        profile.matric_number = self.cleaned_data['matric_number']
        profile.department = self.cleaned_data['department']
        profile.level = self.cleaned_data['level']
        if commit:
            profile.save()
        return user


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('code', 'title', 'units')


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ('student', 'course')


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ('enrollment', 'marks', 'status', 'released')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['enrollment'].queryset = Enrollment.objects.select_related('student__user', 'course')
