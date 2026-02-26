from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from admin_portal.models import Course, Enrollment, Result

from .forms import StudentLoginForm


def _released_results_summary(results):
    total_points = 0.0
    total_units = 0
    for result in results:
        units = result.enrollment.course.units
        total_points += float(result.gpa) * units
        total_units += units
    cgpa = round(total_points / total_units, 2) if total_units else 0
    return total_points, total_units, cgpa


def student_check(user):
    return user.is_authenticated and hasattr(user, 'student_profile') and not user.is_staff


class StudentLoginView(LoginView):
    template_name = 'student_portal/login.html'
    authentication_form = StudentLoginForm

    def form_valid(self, form):
        user = form.get_user()
        if user.is_staff:
            form.add_error(None, 'Admins should use the admin portal login.')
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_portal:dashboard')


@login_required
@user_passes_test(student_check)
def dashboard(request):
    profile = request.user.student_profile
    courses = Course.objects.all().order_by('code')
    enrollments = profile.enrollments.select_related('course')
    approved_ids = {enrollment.course_id for enrollment in enrollments if enrollment.approved}
    pending_ids = {enrollment.course_id for enrollment in enrollments if not enrollment.approved}
    enrolled_ids = approved_ids | pending_ids
    context = {
        'courses': courses,
        'enrolled_ids': enrolled_ids,
        'approved_ids': approved_ids,
        'pending_ids': pending_ids,
    }
    return render(request, 'student_portal/dashboard.html', context)


@login_required
@user_passes_test(student_check)
def register_course(request, course_id):
    if request.method == 'POST':
        profile = request.user.student_profile
        course = get_object_or_404(Course, pk=course_id)
        enrollment, created = Enrollment.objects.get_or_create(student=profile, course=course)
        if created:
            messages.success(request, f'Registered for {course.code}. Waiting for admin approval.')
        elif enrollment.approved:
            messages.info(request, f'{course.code} is already approved.')
        else:
            messages.info(request, f'{course.code} is already registered and pending approval.')
    return redirect('student_portal:dashboard')


@login_required
@user_passes_test(student_check)
def drop_course(request, course_id):
    if request.method == 'POST':
        profile = request.user.student_profile
        enrollment = Enrollment.objects.filter(student=profile, course_id=course_id).first()
        if enrollment:
            if enrollment.approved:
                messages.error(request, 'You cannot drop this course because it has been approved by admin.')
            elif hasattr(enrollment, 'result'):
                messages.error(request, 'You cannot drop a course after a result has been entered.')
            else:
                enrollment.delete()
                messages.success(request, 'Course dropped successfully.')
    return redirect('student_portal:dashboard')


@login_required
@user_passes_test(student_check)
def results_view(request):
    profile = request.user.student_profile
    results = Result.objects.select_related('enrollment__course').filter(
        enrollment__student=profile,
        released=True,
    )
    total_points, total_units, cgpa = _released_results_summary(results)
    return render(
        request,
        'student_portal/results.html',
        {
            'results': results,
            'total_points': round(total_points, 2),
            'total_units': total_units,
            'cgpa': cgpa,
        },
    )


@login_required
@user_passes_test(student_check)
def download_results_pdf(request):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas

    profile = request.user.student_profile
    results = Result.objects.select_related('enrollment__course').filter(
        enrollment__student=profile,
        released=True,
    )
    total_points, total_units, cgpa = _released_results_summary(results)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{profile.matric_number}_results.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - 50

    p.setFont('Helvetica-Bold', 14)
    p.drawString(40, y, 'Student Result Report')
    y -= 25

    p.setFont('Helvetica', 11)
    p.drawString(40, y, f'Name: {request.user.get_full_name() or request.user.username}')
    y -= 20
    p.drawString(40, y, f'Matric Number: {profile.matric_number}')
    y -= 25

    p.setFont('Helvetica-Bold', 10)
    p.drawString(40, y, 'Course')
    p.drawString(180, y, 'Marks')
    p.drawString(250, y, 'Grade')
    p.drawString(320, y, 'GPA')
    p.drawString(390, y, 'Status')
    y -= 15

    p.setFont('Helvetica', 10)
    for result in results:
        if y < 80:
            p.showPage()
            y = height - 50
            p.setFont('Helvetica', 10)
        course = result.enrollment.course
        p.drawString(40, y, f'{course.code} ({course.units}u)')
        p.drawString(180, y, str(result.marks))
        p.drawString(250, y, result.grade)
        p.drawString(320, y, str(result.gpa))
        p.drawString(390, y, result.get_status_display())
        y -= 18

    if y < 90:
        p.showPage()
        y = height - 50

    p.setFont('Helvetica-Bold', 11)
    y -= 10
    p.drawString(40, y, f'Total GPA Points: {round(total_points, 2)}')
    y -= 20
    p.drawString(40, y, f'Total Units: {total_units}')
    y -= 20
    p.drawString(40, y, f'CGPA: {cgpa}')

    p.showPage()
    p.save()
    return response


@login_required
def student_logout(request):
    logout(request)
    return redirect('student_portal:login')
