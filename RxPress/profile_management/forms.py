from django import forms
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'username', 'email']  # Excluded password from this list for optional editing
    
    password = forms.CharField(widget=forms.PasswordInput, label="New Password", required=False)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password", required=False)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data
