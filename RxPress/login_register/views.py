from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from django.contrib.auth.hashers import check_password, make_password
from .models import User  

def create_default_superuser():
    try:
        # Check if a superuser already exists with the given email or username
        if not User.objects.filter(username='rxpress').exists():
            admin = User(
                username='rxpress',
                first_name='Admin',
                last_name='User',
                email='admin@rxpress.com',
                password=make_password('rxpress123'),  # Hashed password
                is_superuser=True
            )
            admin.save()
            print("Default superuser created successfully.")
        else:
            print("Superuser already exists.")
    except Exception as e:
        print(f"Error creating default superuser: {e}")

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
                    messages.success(request, 'Login successful!')
                    if user.is_superuser: 
                        return redirect('admin_dashboard:medicine_list')  # Redirect to your custom admin dashboard
                    else:
                        return redirect('homepage:homepage')
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
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'signup.html', {'form': form})

def logout(request):
    request.session.clear()
    messages.success(request, 'You have been logged out.')
    return redirect('login')  # Adjust the URL name as needed

def onboarding(request):
    return render(request, 'onboarding.html')

def splash(request):
    return render(request, 'splash.html')

def homepage(request):
    return render(request, 'homepage.html')
