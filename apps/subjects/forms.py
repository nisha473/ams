from django import forms
from apps.models import Program, Semester, Subject

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['semester', 'name', 'code', 'credits', 'type']
