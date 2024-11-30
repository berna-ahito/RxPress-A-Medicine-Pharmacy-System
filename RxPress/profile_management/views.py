# profile_management/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserProfileForm


@login_required
def profile_view(request):
    return render(request, 'profile_management/profile.html')

@login_required
def account(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile_management:profile_view')  # Redirect to the profile page after saving
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'profile_management/account.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('homepage:homepage')  # Redirect to homepage after saving changes
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'profile_management/account.html', {'form': form})
