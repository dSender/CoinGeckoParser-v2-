from django import forms

class FilterForm(forms.Form):
    name = forms.CharField(max_length=42, required=False)
    precent = forms.FloatField(label='Precent', required=False)
    volume = forms.IntegerField(label='Volume', required=False)
    markets = forms.CharField(required=False)
    only_checked_markets = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(FilterForm, self).__init__(*args, **kwargs)
        self.fields['markets'].widget.attrs['hidden'] = True
