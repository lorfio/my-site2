from django import forms
from django.contrib.auth import authenticate
from .models import Post
from django.contrib.auth.models import User

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
	firstname = forms.CharField(label='name', max_length=20)
	lastname = forms.CharField(label='lastname', max_length=20)
	email = forms.CharField(label='email', max_length=100)

	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		firstname = self.cleaned_data.get('firstname')
		surname = self.cleaned_data.get('lastname')
		email = self.cleaned_data.get('email')
		return self.cleaned_data

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
