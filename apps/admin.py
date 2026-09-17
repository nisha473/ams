from django.contrib import admin
from django import forms
from django.contrib.auth import get_user_model
from apps.models import Teacher

User = get_user_model()


class TeacherAdminForm(forms.ModelForm):
	username = forms.CharField(max_length=150)
	first_name = forms.CharField(max_length=150, required=False)
	last_name = forms.CharField(max_length=150, required=False)
	email = forms.EmailField(required=False)
	password = forms.CharField(widget=forms.PasswordInput, required=False)

	class Meta:
		model = Teacher
		fields = ['employee_id', 'username', 'first_name', 'last_name', 'email', 'password']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if not self.instance.pk:
			self.fields['password'].required = True
		if self.instance.pk:
			self.fields['username'].initial = self.instance.user.username
			self.fields['first_name'].initial = self.instance.user.first_name
			self.fields['last_name'].initial = self.instance.user.last_name
			self.fields['email'].initial = self.instance.user.email

	def clean_username(self):
		username = self.cleaned_data['username'].strip()
		duplicate_users = User.objects.filter(username__iexact=username)
		if self.instance.pk:
			duplicate_users = duplicate_users.exclude(pk=self.instance.user_id)
		if duplicate_users.exists():
			raise forms.ValidationError('A user with this username already exists.')
		return username

	def save(self, commit=True):
		teacher = super().save(commit=False)
		if teacher.pk:
			user = teacher.user
			user.username = self.cleaned_data['username']
			user.first_name = self.cleaned_data['first_name']
			user.last_name = self.cleaned_data['last_name']
			user.email = self.cleaned_data['email']
			if self.cleaned_data['password']:
				user.set_password(self.cleaned_data['password'])
			user.save()
		else:
			user = User.objects.create_user(
				username=self.cleaned_data['username'],
				password=self.cleaned_data['password'],
				first_name=self.cleaned_data['first_name'],
				last_name=self.cleaned_data['last_name'],
				email=self.cleaned_data['email'],
			)
			teacher.user = user
		if commit:
			teacher.save()
		return teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
	form = TeacherAdminForm
	list_display = ('employee_id', 'full_name', 'username', 'email')
	search_fields = ('employee_id', 'user__username', 'user__first_name', 'user__last_name')

	@admin.display(description='Name')
	def full_name(self, obj):
		return obj.user.get_full_name() or '-'

	@admin.display(description='Username')
	def username(self, obj):
		return obj.user.username

	@admin.display(description='Email')
	def email(self, obj):
		return obj.user.email
