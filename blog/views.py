from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Post
from .forms import PostForm,LoginForm,RegistrationForm

# Create your views here.
#view for index page
def index(request):
	form = LoginForm
	posts = Post.objects.all().order_by('published_date')
	return render(request, 'blog/index.html', {'form':form, 'posts':posts })
#----------------------------------------------------------------------#

def log_in(request):
	form = LoginForm(request.POST or None)
	posts = Post.objects.all().order_by('published_date')
	if request.POST and form.is_valid():
		user = form.login(request)
		if user:
			login(request, user)
			return redirect('index')
	return render(request, 'blog/index.html', {'form':form, 'posts':posts })

def log_out(request):
	if request.method == 'POST':
		logout(request)
	return redirect('index')

def registration(request):
	form = RegistrationForm(request.POST or None)
	if request.POST and form.is_valid():
		user = form.register(request)
		user.save()
		return redirect('index')
	return render(request, 'blog/registration.html', {'form': form})

def userProfile(request, pk):
	user = get_object_or_404(User, pk=pk)
	if request.user.is_anonymous():
		return redirect('index')
	if request.user != user:
		return redirect('index')
	return render(request, 'blog/user-profile.html', {'user':user})
#---------------------------- post_list -------------------------------

def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post':post})

def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
