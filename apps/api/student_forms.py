from django import forms
from ..models import Student

class StudentForm(forms.ModelForm):
    COURSE_CHOICES = [
        ('BBA', 'BBA'),
        ('BHM', 'BHM'),
        ('BIT', 'BIT'),
        ('BCS', 'BCS'),
        ('MBA', 'MBA'),
    ]
    SHIFT_CHOICES = [
        ('Morning', 'Morning'),
        ('Evening', 'Evening'),
    ]
    
    course = forms.ChoiceField(choices=COURSE_CHOICES)
    shift = forms.ChoiceField(choices=SHIFT_CHOICES)
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


    class Meta:
        model = Student
        fields = ['name', 'roll_number', 'course', 'shift', 'dob', 'email']

    def clean(self):
        cleaned_data = super().clean()
        roll_number = (cleaned_data.get('roll_number') or '').strip()
        course = cleaned_data.get('course')

        duplicate_students = Student.objects.filter(
            roll_number__iexact=roll_number,
            course__iexact=course,
        )
        if self.instance.pk:
            duplicate_students = duplicate_students.exclude(pk=self.instance.pk)
        if duplicate_students.exists():
            raise forms.ValidationError("A student with the same roll number already exists in this course.")

        cleaned_data['roll_number'] = roll_number
        return cleaned_data