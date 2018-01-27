from django import forms
from datastore.models.prodsub import ProductSubmit

class SubmitForm(forms.ModelForm):
    class Meta:
        model = ProductSubmit
        fields = ('product', 'quantity', 'price', 'province', 'location')
