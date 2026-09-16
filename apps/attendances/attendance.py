from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from apps.models import *
from datetime import datetime
from datetime import date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, F
from django.db.models.functions import TruncDate
from datetime import datetime, date, timedelta


def AttendanceView(request):
    today = date.today()
    if Attendance.objects.filter(date=today).exists():
        return redirect('attendance_report')

    if request.method == 'POST':
        for student_id, status in request.POST.items():
            if student_id.startswith('student_'):
                student_id = student_id.split('_')[1]
                student = Student.objects.get(pk=student_id)
                if not Attendance.objects.filter(student=student, date=today).exists():
                    Attendance.objects.create(student=student, date=today, status=status)
        return redirect('attendance/success')
    students = Student.objects.all()
    return render(request, 'attendances/attendance.html', {'students': students})

def AttendanceSuccess(request):
    return render(request, 'attendances/attendance_success.html')

def AttendanceReportView(request):
    today_date = datetime.now().date()
    attendance_records = Attendance.objects.filter(date=today_date).order_by('student')
    student_name = request.GET.get('student_name')

    if student_name:
        attendance_records = attendance_records.filter(student__name__icontains=student_name)

    paginator = Paginator(attendance_records, 10)
    page_number = request.GET.get('page')
    try:
        attendance_data = paginator.page(page_number)
    except PageNotAnInteger:
        attendance_data = paginator.page(1)
    except EmptyPage:
        attendance_data = paginator.page(paginator.num_pages)

    if not attendance_data:
        attendance_data = paginator.page(1)

    return render(request, 'attendances/attendance_report.html', {
        'attendance_data': attendance_data,
        'student_name': student_name
    })


def this_months_attendance_report(request):
    today = date.today()
    first_day_of_month = today.replace(day=1)

    attendance_records = Attendance.objects.filter(
        date__gte=first_day_of_month
    )

    student_name = request.GET.get('student_name')
    if student_name:
        attendance_records = attendance_records.filter(student__name__icontains=student_name)

    start_date = request.GET.get('start_date')
    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            attendance_records = attendance_records.filter(date__gte=start_date)
        except ValueError:
            start_date = None

    end_date = request.GET.get('end_date')
    if end_date:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            end_date = end_date + timedelta(days=1)
            attendance_records = attendance_records.filter(date__lt=end_date)
        except ValueError:
            end_date = None

    attendance_counts = attendance_records.values('student__name').annotate(total_attendance=Count('id')).order_by('student__name')

    paginator = Paginator(attendance_counts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'attendances/this_months_attendance_report.html', {
        'attendance_counts': page_obj,
        'student_name': student_name,
        'start_date': start_date,
        'end_date': end_date,
        'today': today,
    })
