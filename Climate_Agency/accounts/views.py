from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
# from .documents import CustomUser
from .views import index 
from climate_data.views import index
# Register view
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

# Dashboard view
def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'accounts/dashboard.html')


def register_view(request):
    ...

def login_view(request):
    ...

def logout_view(request):
    ...

def dashboard_view(request):
    ...
accounts/views.py (example)


def create_user(request):
    user = CustomUser(username="arsalan", email="arsalan@mail.com", country="Pakistan")
    user.save()
    return HttpResponse(f"User {user.username} saved successfully!")

def list_users(request):
    users = CustomUser.objects()
    result = ", ".join([user.username for user in users])
    return HttpResponse(f"Users: {result}")
