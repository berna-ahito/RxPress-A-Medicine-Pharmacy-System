from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from django.contrib.auth.hashers import check_password 
from .models import User

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(username=username)
                if check_password(password, user.password):
                    request.session['id'] = user.id
                    request.session['username'] = user.username
                    request.session['user_type'] = user.user_type

                    if user.user_type == 'admin':
                        messages.success(request, 'Welcome, Admin!')
                        return redirect('admin_dashboard:medicine_list') 
                    else:
                        messages.success(request, 'Login successful!')
                        return redirect('homepage:homepage')  # Redirecting to homepage app here

                else:
                    messages.error(request, 'Invalid password.')
            except User.DoesNotExist:
                messages.error(request, 'User does not exist.')
        else:
            messages.error(request, 'Invalid credentials.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if User.objects.filter(username=data['username']).exists():
                messages.error(request, 'Username already exists. Please choose another.')
                return render(request, 'signup.html', {'form': form})

            if User.objects.filter(email=data['email']).exists():
                messages.error(request, 'Email already exists. Please choose another.')
                return render(request, 'signup.html', {'form': form})

            user = form.save()
            messages.success(request, 'User created successfully! You can now log in.')
            return redirect('login_register:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'signup.html', {'form': form})

def logout(request):
    request.session.clear()  
    messages.success(request, 'You have been logged out.')
    return redirect('login') 

def onboarding(request):
    return render(request, 'onboarding.html')

def splash(request):
    return render(request, 'splash.html')

def homepage(request):
    return render(request, 'homepage.html')