from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

# Custom Registration Form
class RegisterForm(UserCreationForm):
    # You can add additional fields like first_name if needed
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))

    class Meta:
        model = User
        fields = ['first_name', 'username', 'password1', 'password2']  # Removed 'email' from the fields
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('A user with this username already exists.')
        return username

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 6:  # Minimum password length can be 6 characters (less strict)
            raise forms.ValidationError('Password must be at least 6 characters long.')
        return password

    def clean_password2(self):
        password2 = self.cleaned_data.get('password2')
        password1 = self.cleaned_data.get('password1')
        if password2 != password1:
            raise forms.ValidationError('Passwords do not match.')
        return password2


# Edit Profile Form
class EditProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'New Password (optional)'}),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and len(password) < 6:
            raise forms.ValidationError('Password must be at least 6 characters long.')
        return password
