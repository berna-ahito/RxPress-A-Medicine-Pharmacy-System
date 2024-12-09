from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user) 
                if user.is_superuser: 
                    return redirect('admin_dashboard:medicine_list')
                else:
                    return redirect('homepage:homepage')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid form data.')
    else:
        form = LoginForm()
    return render(request, 'login_register/login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            if User.objects.filter(username=data['username']).exists():
                messages.error(request, 'Username already exists. Please choose another.')
                return render(request, 'login_register/signup.html', {'form': form})

            if User.objects.filter(email=data['email']).exists():
                messages.error(request, 'Email already exists. Please choose another.')
                return render(request, 'login_register/signup.html', {'form': form})

            # Create and save the new user
            user = User(
                first_name=data['first_name'],
                last_name=data['last_name'],
                username=data['username'],
                email=data['email'],
                password=make_password(data['password']),  # Encrypt the password
                is_superuser=False  # Default to a regular user; adjust as needed
            )
            user.save()
            messages.success(request, 'User created successfully! You can now log in.')
            return redirect('login_register:login')
        else:
            messages.error(request, 'Passwords do not match.')
    else:
        form = RegisterForm()
    return render(request, 'login_register/signup.html', {'form': form})

@login_required
def logout_user(request):
    logout(request)
    return redirect('login_register:onboarding')

def onboarding(request):
    return render(request, 'login_register/onboarding.html')

def splash(request):
    return render(request, 'login_register/splash.html')

def homepage(request):
    return render(request, 'login_register/homepage.html')
