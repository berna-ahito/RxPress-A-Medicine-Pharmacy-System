from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    # Include fields from the User model
    first_name = forms.CharField(max_length=255, required=True)
    last_name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=255, required=True)

    class Meta:
        model = UserProfile
        fields = ['profile_picture']  # Fields from UserProfile

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Pre-fill user-related fields if user is provided
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['username'].initial = user.username

    def save(self, user=None, commit=True):
        # Update the related user fields
        profile = super().save(commit=False)
        if user:
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.username = self.cleaned_data['username']
            if commit:
                user.save()  # Save the user object
                profile.user = user
        if commit:
            profile.save()  # Save the profile object
        return profile
