from django import forms
from apps.models import Program

class ProgramForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        duplicate_programs = Program.objects.filter(name__iexact=name)
        if self.instance.pk:
            duplicate_programs = duplicate_programs.exclude(pk=self.instance.pk)
        if duplicate_programs.exists():
            raise forms.ValidationError('A program with this name already exists.')
        return name

    class Meta:
        model = Program
        fields = ['name', 'is_annual', 'credits', 'quota', 'fee', 'level', 'is_active']
