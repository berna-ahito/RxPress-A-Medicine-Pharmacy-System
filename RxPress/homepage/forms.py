from django import forms

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
