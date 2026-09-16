from django import forms
from apps.models import Program

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['name', 'is_annual', 'credits', 'quota', 'fee', 'level', 'is_active']
