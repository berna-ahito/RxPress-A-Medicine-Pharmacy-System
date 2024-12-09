from django import forms
from admin_dashboard.models import Medicine

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'description', 'strength', 'category', 'price', 'quantity', 'picture']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter medicine name',
                'class': 'form-control',
                'style': 'font-family: Montserrat Alternates, sans-serif;'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Enter description',
                'class': 'form-control',
                'style': 'font-family: Montserrat Alternates, sans-serif;'
            }),
            'strength': forms.TextInput(attrs={
                'placeholder': 'Enter strength',
                'class': 'form-control',
                'style': 'font-family: Montserrat Alternates, sans-serif;'
            }),
            'category': forms.TextInput(attrs={
                'placeholder': 'Enter category',
                'class': 'form-control',
                'style': 'font-family: Montserrat Alternates, sans-serif;'
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': 'Enter price',
                'class': 'form-control',
                'style': 'font-family: Montserrat Alternates, sans-serif;'
            }),
            'quantity': forms.NumberInput(attrs={
                'placeholder': 'Enter quantity',
                'class': 'form-control',
                'style': 'font-family: Montserrat Alternates, sans-serif;'
            }),
            'medicine_picture': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'style': 'font-family: Montserrat Alternates, sans-serif;'
            }),
        }
