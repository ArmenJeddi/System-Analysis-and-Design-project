from django import forms
# from datastore.models.prodsub import ProductSubmit
from datastore.models.driver import provinces


class BrowseForm(forms.Form):

    def __init__(self, productList, *args, **kwargs):
        super(BrowseForm, self).__init__(*args, **kwargs)

        self.fields['product'] = forms.ChoiceField(
            choices = productList
        )

        self.fields['from'] = forms.IntegerField()
        self.fields['to'] = forms.IntegerField()

        self.fields['province'] = forms.MultipleChoiceField(
            required = True,
            widget=forms.CheckboxSelectMultiple,
            choices=provinces,
        )
