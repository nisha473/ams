from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from apps.models import Program, Semester, Subject
from .forms import SubjectForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def subject_list(request, semester_id):
    semester = get_object_or_404(Semester, pk=semester_id)
    subjects = semester.subjects.all()
    return render(request, 'subjects/subject_list.html', {'semester': semester, 'subjects': subjects})

def subject_create(request, semester_id):
    semester = get_object_or_404(Semester, pk=semester_id)
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.semester = semester
            subject.save()
            return redirect('subject_list', semester_id=semester.id)
    else:
        form = SubjectForm()
    return render(request, 'subjects/subject_form.html', {'form': form, 'semester': semester})

def subject_update(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('subject_list', semester_id=subject.semester.id)
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'subjects/subject_form.html', {'form': form, 'semester': subject.semester})

def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        semester_id = subject.semester.id
        subject.delete()
        return redirect('subject_list', semester_id=semester_id)
    return render(request, 'subjects/subject_confirm_delete.html', {'subject': subject})
