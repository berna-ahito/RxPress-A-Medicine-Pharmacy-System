from django import forms
from .models import Medicine

class AddToCartForm(forms.Form):
    medicine_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'quantity-input', 'style': 'width: 60px;'})
    )

class MedicineSearchForm(forms.Form):
    search_query = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'search-bar',
            'placeholder': 'Search for medicines...',
            'onkeyup': 'filterMedicines()'
        })
    )
