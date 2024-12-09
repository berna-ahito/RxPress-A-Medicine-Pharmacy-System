from django.dispatch import receiver
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from django.contrib import messages
from login_register.views import logout
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@login_required
def profile_view(request):
    return render(request, 'edit_profile.html')

@login_required
def account(request):
    if request.method == 'POST':
        # Use the user's profile, not the user directly
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('profile_management:profile_view')  
    else:
        # Pass the profile to the form for initial population
        form = UserProfileForm(instance=request.user.userprofile)
    
    return render(request, 'profile_management/account.html', {'form': form})

@login_required
def edit_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            old_password = request.user.password  # Store the current password
            new_password = request.POST.get('password', '').strip()  # Get the new password, if provided

            # Save changes to the user and profile
            form.save(user=request.user)

            # Check if the password field has input
            if new_password:
                # Check if the password has changed
                if old_password != new_password:
                    logout(request)
                    return redirect('login_register:login')
            return redirect('profile_management:account')
    else:
        form = UserProfileForm(instance=profile, user=request.user)  # Pre-fill the form

    return render(request, 'profile_management/edit_profile.html', {'form': form})

@login_required
def logout_user(request):
    logout(request)
    messages.success(request,"You have been logged out.")
    return redirect('login_register:login')

@login_required
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@login_required
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


