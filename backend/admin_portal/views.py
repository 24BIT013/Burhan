from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from .forms import (
    AdminLoginForm,
    AdminRegisterForm,
    CourseForm,
    EnrollmentForm,
    ResultForm,
    StudentCreateForm,
    StudentUpdateForm,
)
from .models import Course, Enrollment, Result, StudentProfile


def admin_check(user):
    return user.is_authenticated and user.is_staff


class AdminLoginView(LoginView):
    template_name = 'admin_portal/login.html'
    authentication_form = AdminLoginForm

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_staff:
            form.add_error(None, 'Only admins can log in here.')
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('admin_portal:dashboard')


def admin_register(request):
    if request.method == 'POST':
        form = AdminRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            login(request, user)
            return redirect('admin_portal:dashboard')
    else:
        form = AdminRegisterForm()
    return render(request, 'admin_portal/register.html', {'form': form})


@login_required(login_url='admin_portal:login')
@user_passes_test(admin_check, login_url='admin_portal:login')
def admin_dashboard(request):
    context = {
        'student_count': StudentProfile.objects.count(),
        'course_count': Course.objects.count(),
        'enrollment_count': Enrollment.objects.count(),
        'result_count': Result.objects.count(),
    }
    return render(request, 'admin_portal/dashboard.html', context)


@login_required(login_url='admin_portal:login')
@user_passes_test(admin_check, login_url='admin_portal:login')
def admin_logout(request):
    logout(request)
    return redirect('admin_portal:login')


@login_required(login_url='admin_portal:login')
@user_passes_test(admin_check, login_url='admin_portal:login')
def student_create(request):
    if request.method == 'POST':
        form = StudentCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False
            user.save()
            StudentProfile.objects.create(
                user=user,
                matric_number=form.cleaned_data['matric_number'],
                department=form.cleaned_data['department'],
                level=form.cleaned_data['level'],
            )
            messages.success(request, 'Student registered successfully.')
            return redirect('admin_portal:student_list')
    else:
        form = StudentCreateForm()
    return render(
        request,
        'admin_portal/student_form.html',
        {
            'form': form,
            'title': 'Register Student',
            'back_url': 'admin_portal:student_list',
        },
    )


@login_required(login_url='admin_portal:login')
@user_passes_test(admin_check, login_url='admin_portal:login')
def student_edit(request, pk):
    student = get_object_or_404(StudentProfile.objects.select_related('user'), pk=pk)
    if request.method == 'POST':
        form = StudentUpdateForm(request.POST, instance=student.user, student_profile=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully.')
            return redirect('admin_portal:student_list')
    else:
        form = StudentUpdateForm(instance=student.user, student_profile=student)
    return render(
        request,
        'admin_portal/student_form.html',
        {
            'form': form,
            'title': 'Edit Student',
            'back_url': 'admin_portal:student_list',
        },
    )


@login_required(login_url='admin_portal:login')
@user_passes_test(admin_check, login_url='admin_portal:login')
def student_list(request):
    students = StudentProfile.objects.select_related('user').all().order_by('matric_number')
    return render(request, 'admin_portal/student_list.html', {'students': students})


@login_required(login_url='admin_portal:login')
@user_passes_test(admin_check, login_url='admin_portal:login')
def course_list(request):
    courses = Course.objects.all().order_by('code')
    return render(request, 'admin_portal/course_list.html', {'courses': courses})


@login_required(login_url='admin_portal:login')
@user_passes_test(admin_check, login_url='admin_portal:login')
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course added.')
            return redirect('admin_portal:course_list')
    else:
        form = CourseForm()
    return render(request, 'admin_portal/course_form.html', {'form': form, 'title': 'Add Course'})


@login_required(login_url='admin_portal:login')
@user_passes_test(admin_check, login_url='admin_portal:login')
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated.')
            return redirect('admin_portal:course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'admin_portal/course_form.html', {'form': form, 'title': 'Edit Course'})


@login_required(login_url='admin_portal:login')
@user_passes_test(admin_check, login_url='admin_portal:login')
def enrollment_list(request):
    enrollments = Enrollment.objects.select_related('student__user', 'course').all().order_by('student__matric_number')
    return render(request, 'admin_portal/enrollment_list.html', {'enrollments': enrollments})


@login_required(login_url='admin_portal:login')
@user_passes_test(admin_check, login_url='admin_portal:login')
def enrollment_approve(request, pk):
    if request.method == 'POST':
        enrollment = get_object_or_404(Enrollment, pk=pk)
        if enrollment.approved:
            messages.info(request, 'Enrollment is already approved.')
        else:
            enrollment.approved = True
            enrollment.approved_at = timezone.now()
            enrollment.save(update_fields=['approved', 'approved_at'])
            messages.success(request, 'Enrollment approved successfully.')
    return redirect('admin_portal:enrollment_list')


@login_required(login_url='admin_portal:login')
@user_passes_test(admin_check, login_url='admin_portal:login')
def enrollment_create(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Enrollment created.')
            return redirect('admin_portal:enrollment_list')
    else:
        form = EnrollmentForm()
    return render(request, 'admin_portal/enrollment_form.html', {'form': form})


@login_required(login_url='admin_portal:login')
@user_passes_test(admin_check, login_url='admin_portal:login')
def result_list(request):
    results = Result.objects.select_related('enrollment__student__user', 'enrollment__course').all()
    return render(request, 'admin_portal/result_list.html', {'results': results})


@login_required(login_url='admin_portal:login')
@user_passes_test(admin_check, login_url='admin_portal:login')
def result_create(request):
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Result saved.')
            return redirect('admin_portal:result_list')
    else:
        form = ResultForm()
    return render(request, 'admin_portal/result_form.html', {'form': form, 'title': 'Enter Result'})


@login_required(login_url='admin_portal:login')
@user_passes_test(admin_check, login_url='admin_portal:login')
def result_edit(request, pk):
    result = get_object_or_404(Result, pk=pk)
    if request.method == 'POST':
        form = ResultForm(request.POST, instance=result)
        if form.is_valid():
            form.save()
            messages.success(request, 'Result updated.')
            return redirect('admin_portal:result_list')
    else:
        form = ResultForm(instance=result)
    return render(request, 'admin_portal/result_form.html', {'form': form, 'title': 'Edit Result'})
