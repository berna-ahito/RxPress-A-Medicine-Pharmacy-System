from django import forms

class MedicineForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter medicine name',
            'class': 'form-control',
            'style': 'font-family: Montserrat Alternates, sans-serif;'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter description',
            'class': 'form-control',
            'style': 'font-family: Montserrat Alternates, sans-serif;'
        })
    )
    strength = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter strength',
            'class': 'form-control',
            'style': 'font-family: Montserrat Alternates, sans-serif;'
        })
    )
    category = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter category',
            'class': 'form-control',
            'style': 'font-family: Montserrat Alternates, sans-serif;'
        })
    )
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter price',
            'class': 'form-control',
            'style': 'font-family: Montserrat Alternates, sans-serif;'
        })
    )
    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'placeholder': 'Enter quantity',
            'class': 'form-control',
            'style': 'font-family: Montserrat Alternates, sans-serif;'
        })
    )
