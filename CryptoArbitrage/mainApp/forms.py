from django import forms

class FilterForm(forms.Form):
    name = forms.CharField(max_length=42, required=False)
