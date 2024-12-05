from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages
from django.contrib.auth import logout

@login_required
def profile_view(request):
    return render(request, 'edit_profile.html')

@login_required
def account(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile_management:profile_view')  
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'account.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password and password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'profile_management/edit_profile.html', {'form': form})

        if form.is_valid():
            user = form.save(commit=False)

            if password:
                user.set_password(password)
            user.save()
            if password:
                logout(request)
                messages.success(request, 'Your password has been updated. Please log in again.')
                return redirect('login_register:login')
            
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile_management:profile_view')
    
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'profile_management/edit_profile.html', {'form': form})


