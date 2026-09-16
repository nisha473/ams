from django import forms
from ..models import CustomUser

class CustomUser(forms.ModelForm):
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
        model = CustomUser
        fields = ['firstname', 'lastname', 'mobile_num', 'dob', 'email']

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')

        # Check if a student with the same roll number exists in the same course
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with the same username already exists.")

        return cleaned_data