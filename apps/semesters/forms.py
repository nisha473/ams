from django import forms
from apps.models import Semester


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['program', 'semester_number']
