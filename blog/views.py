from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm, PostForm, KomentarzForm, UserUpdateForm
from .models import Post, Komentarz

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('logout_message')

def index(request):
    if request.user.is_authenticated:
        posts = Post.objects.all().order_by('-data_publikacji')
        return render(request, 'index.html', {'posts': posts})
    else:
        return redirect('login')


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required
def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = KomentarzForm(request.POST)
        if form.is_valid():
            komentarz = form.save(commit=False)
            komentarz.post = post
            komentarz.autor = request.user
            komentarz.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = KomentarzForm()
    return render(request, 'post_detail.html', {'post': post, 'form': form})

def logout_message(request):
    return render(request, 'logout_message.html')

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
    return render(request, 'profile.html', {'user_form': user_form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Ważne, aby po zmianie hasła nie wylogowało użytkownika
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})
