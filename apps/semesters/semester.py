from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from apps.models import Program, Semester, Subject
from .forms import  SemesterForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def semester_list(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    semesters = program.semesters.all()
    return render(request, 'semesters/semester_list.html', {'program': program, 'semesters': semesters})

def semester_create(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    if request.method == 'POST':
        form = SemesterForm(request.POST)
        if form.is_valid():
            semester = form.save(commit=False)
            semester.program = program
            semester.save()
            return redirect('semester_list', program_id=program.id)
    else:
        form = SemesterForm()
    return render(request, 'semesters/semester_form.html', {'form': form, 'program': program})

def semester_update(request, pk):
    semester = get_object_or_404(Semester, pk=pk)
    if request.method == 'POST':
        form = SemesterForm(request.POST, instance=semester)
        if form.is_valid():
            form.save()
            return redirect('semester_list', program_id=semester.program.id)
    else:
        form = SemesterForm(instance=semester)
    return render(request, 'semesters/semester_form.html', {'form': form, 'program': semester.program})

def semester_delete(request, pk):
    semester = get_object_or_404(Semester, pk=pk)
    if request.method == 'POST':
        program_id = semester.program.id
        semester.delete()
        return redirect('semester_list', program_id=program_id)
    return render(request, 'semesters/semester_confirm_delete.html', {'semester': semester})
