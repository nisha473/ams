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
    
    course = forms.ChoiceField(choices=COURSE_CHOICES)
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


    class Meta:
        model = Student
        fields = ['name', 'roll_number', 'course', 'dob', 'email']

    def clean(self):
        cleaned_data = super().clean()
        roll_number = cleaned_data.get('roll_number')
        course = cleaned_data.get('course')

        # Check if a student with the same roll number exists in the same course
        if Student.objects.filter(roll_number=roll_number, course=course).exists():
            raise forms.ValidationError("A student with the same roll number already exists in this course.")

        return cleaned_data