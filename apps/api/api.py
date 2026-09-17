from django.views.generic import TemplateView
from decouple import config
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from apps.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from .student_forms import StudentForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.http import url_has_allowed_host_and_scheme
from datetime import date
import csv
from django.core.paginator import Paginator
from django.db.models import Count, F
from django.db.models import Q
from django.db.models.functions import TruncDate
from .signup_forms import SignupForm


def dashboard_view(request):
    return render(request, 'apps/dashboard.html')

class HomeView(LoginRequiredMixin,TemplateView):
    template_name = "apps/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = datetime.now()
        return context

    def get(self, request):
        user = request.user
        active_page="home"
        context = {
            "users": user,
            }
        return render(request, self.template_name, context)


class WelcomeView(TemplateView):
    template_name = "apps/welcome.html"

    def get(self, request):
        return render(request, self.template_name)
    
class LoginView(TemplateView):
    template_name = "apps/login.html"
    default_redirect = "/"

    # @method_decorator(login_required)
    def get(self, request):
        next = request.GET.get("next","/home/")
        return render(request, self.template_name)

    def post(self, request):
        next = request.POST.get("next","")
        if next == "/logout/":
            next = "/home/"
        username = request.POST["username"]
        password = request.POST["password"]
        print(username)
        user = User.objects.filter(username=username).first()
        print(user)
        if user:
            if not user.is_active:
                messages.error(
                    request, "Login failed ! user is deactivated."
                )
                return HttpResponseRedirect(f"/login/?next={next}")

            user = authenticate(username=username, password=password)
            if user and user.is_authenticated:
                login(request, user)
                if next:
                    return HttpResponseRedirect(next)
                return redirect("home_page")

            messages.error(
                request, "Login failed ! password do not match."
            )
        else:
            messages.error(
                request, "Login failed ! username do not match."
            )
        return HttpResponseRedirect(f"/login/?next={next}")


def signup_view(request):
    next_url = request.GET.get('next', request.POST.get('next', '/home/'))
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = '/home/'

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(next_url)
    else:
        form = SignupForm()
    return render(request, 'apps/signup.html', {'form': form, 'next': next_url})


def logout_view(request):
    logout(request)
    return redirect('home_page')


@login_required(login_url='/login/')
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been changed successfully.')
            return redirect('home_page')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'apps/change_password.html', {'form': form})

def add_student_view(request):
    form = StudentForm()  # Ensure form is always initialized
    if request.method == 'POST':
        if 'form_submit' in request.POST:
            form = StudentForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('add-student-success')
        elif 'csv_submit' in request.POST:
            csv_file = request.FILES.get('csv_file')
            if csv_file:
                handle_uploaded_csv(csv_file)
                return redirect('add-student-success')
    return render(request, 'students/add_student.html', {'form': form})

def handle_uploaded_csv(csv_file):
    decoded_file = csv_file.read().decode('utf-8').splitlines()
    reader = csv.reader(decoded_file)
    for row in reader:
        name, roll_number, course, dob, email = row
        # Check if a student with the same roll number and course already exists
        if not Student.objects.filter(
            roll_number__iexact=roll_number.strip(),
            course__iexact=course.strip(),
        ).exists():
            Student.objects.create(
                name=name,
                roll_number=roll_number,
                course=course,
                dob=dob,
                email=email
            )

def add_student_success(request):
    return render(request, 'students/student_success.html')

def edit_student_view(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student-list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/edit_student.html', {'form': form, 'student': student})

def student_list_view(request):
    if request.method == 'POST':
        course = request.POST.get('course')
        shift = request.POST.get('shift')
        search = ''
    else:
        course = request.GET.get('course')
        shift = request.GET.get('shift')
        search = request.GET.get('search', '').strip()

    students = Student.objects.all()
    if course:
        students = students.filter(course__iexact=course)
    if shift:
        students = students.filter(shift__iexact=shift)
    if search:
        students = students.filter(
            Q(name__icontains=search) | Q(roll_number__icontains=search)
        )
    students = students.order_by('name')
    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'students/students.html', {
        'page_obj': page_obj,
        'course': course,
        'shift': shift,
        'search': search,
        'courses': Student.objects.values_list('course', flat=True).distinct().order_by('course'),
        'shifts': ['Morning', 'Evening'],
    })
    
def csv_preview(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        try:
            # Read the CSV file
            csv_data = csv_file.read().decode('utf-8')
            csv_reader = csv.reader(csv_data.splitlines())

            # Prepare HTML for CSV preview
            preview_html = '<table class="table table-bordered table-sm"><thead><tr>'

            # Add headers
            headers = next(csv_reader)
            for header in headers:
                preview_html += '<th>' + header + '</th>'
            preview_html += '</tr></thead><tbody>'

            # Add rows
            for row in csv_reader:
                preview_html += '<tr>'
                for cell in row:
                    preview_html += '<td>' + cell + '</td>'
                preview_html += '</tr>'

            preview_html += '</tbody></table>'
            
            # Render the preview in a new tab
            return HttpResponse(preview_html)
        
        except Exception as e:
            # Handle errors gracefully
            error_message = f"Error processing CSV file: {str(e)}"
            return HttpResponse(error_message, status=400)

    # Handle GET requests or invalid requests
    return HttpResponse("Invalid request method or missing CSV file", status=400)