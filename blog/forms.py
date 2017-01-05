from django import forms
from django.contrib.auth import authenticate
from .models import Post
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class PostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ('title', 'text',)

class LoginForm(forms.Form):
	username = forms.CharField(label='username', max_length=20)
	password = forms.CharField(label='password', max_length=20, widget=forms.PasswordInput)

	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		if not user or not user.is_active:
			raise forms.ValidationError('username e/o password errati')
		return self.cleaned_data

	def login(self, request):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		return user

class RegistrationForm(forms.Form):
	username = forms.CharField(label='username', max_length=20)
	password = forms.CharField(label='password', max_length=20, widget=forms.PasswordInput)
	confirmPassword = forms.CharField(label='confirm password', max_length=20, widget=forms.PasswordInput)
	firstname = forms.CharField(label='name', max_length=20)
	lastname = forms.CharField(label='lastname', max_length=20)
	email = forms.CharField(label='email', max_length=100)

	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		confirmPassword = self.cleaned_data.get('confirmPassword')
		firstname = self.cleaned_data.get('firstname')
		surname = self.cleaned_data.get('lastname')
		email = self.cleaned_data.get('email')
		if password != confirmPassword:
			raise ValidationError("Password mismatch!!")
		return self.cleaned_data

	def clean_username(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		if User.objects.filter(username=username).exists():
			raise ValidationError("Username already exists!!")
		return username


	def clean_email(self):
		email = self.cleaned_data.get('email')
		try:
			validate_email(email)
		except:
			raise ValidationError("Wrong email address!!")
		if User.objects.filter(email=email).exists():
			raise ValidationError("Email already exists!!")
		return email


	def register(self,request):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		firstname = self.cleaned_data.get('firstname')
		lastname = self.cleaned_data.get('lastname')
		email = self.cleaned_data.get('email')

		user = User.objects.create_user(username)
		user.set_password(password)
		user.first_name = firstname
		user.last_name = lastname
		user.email = email

		return user

class UserProfileForm(forms.Form):
	username = forms.CharField(label='username', max_length=20)
	firstname = forms.CharField(label='name', max_length=20)
	lastname = forms.CharField(label='lastname', max_length=20)
	email = forms.CharField(label='email', max_length=100)
