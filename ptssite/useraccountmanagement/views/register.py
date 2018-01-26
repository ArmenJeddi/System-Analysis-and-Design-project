from datastore.models import UnprivilegedUser, Driver, Customer
from datastore.models.driver import provinces
from django.forms import widgets
from django import forms
from django.core.exceptions import ValidationError
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.http import HttpResponseBadRequest
from django.utils.datastructures import MultiValueDictKeyError

class UserForm(forms.ModelForm):
    field_order = ['first_name', 'last_name', 'username', 'password',
                   'password2', 'national_id', 'phone_number',
                   'account_number', 'license_agreement']
    class Meta:
        model = UnprivilegedUser
        fields = ['first_name', 'last_name', 'username', 'password',
                  'national_id', 'phone_number', 'account_number']
        widgets = {'password': widgets.PasswordInput}
        
    password2 = forms.CharField(label='تکرار گذرواژه',
                                widget=widgets.PasswordInput,
                                max_length=UnprivilegedUser._meta.get_field(
                                    'password').max_length)
    

    def license_agreed(value):
        if value != True:
            raise ValidationError('باید با شرایط و ضوابط موافق باشید',
                                  code='disagreement')
        
    license_agreement = forms.BooleanField(label='شرایط و ضوابط مذکور را قبول دارم',
                                           validators=[license_agreed])
    
    def clean(self):
        if 'password' in self.cleaned_data and 'password2' in self.cleaned_data\
           and self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise ValidationError('گذرواژه وارد شده و تکرار آن همخوانی ندارند',
                                  code='password_disagreement')
        super().clean()

class DriverForm(UserForm):
    field_order = ['first_name', 'last_name', 'username', 'password',
                   'password2', 'national_id', 'phone_number',
                   'account_number', 'license_plate', 'certificate_number',
                   'regions', 'license_agreement']

    class Meta(UserForm.Meta):
        model = Driver
        fields = UserForm.Meta.fields + ['license_plate', 'certificate_number']
        
    regions = forms.MultipleChoiceField(label='از چه مناطقی درخواست جا به جایی می پذیرید؟',
                                        choices=provinces,
                                        widget=widgets.CheckboxSelectMultiple)

    def register_regions(self):
        for province in self.cleaned_data['regions']:
            self.instance.add_province(province)

class DriverRegistrationView(CreateView):
    form_class = DriverForm
    success_url = '/useraccountmanagement/login/'

    def form_valid(self, form):
        for province in form.cleaned_data['regions']:
            form.instance.add_province(province)
        super().form_valid(form)
        
class CustomerForm(UserForm):
    class Meta(UserForm.Meta):
        model = Customer

class CustomerRegistrationView(CreateView):
    form_class = CustomerForm
    success_url = '/useraccountmanagement/login/'
    
class RegistrationView(TemplateView):

    template_name = 'useraccountmanagement/registration.html'

    def get_context_data(self, **kwargs):
        context = {
            'driver_form': DriverForm(),
            'customer_form': CustomerForm()
            }
        return context

    def post(self, request, *args, **kwargs):
        try:
            role = request.POST['role']
            if role == 'driver':
                return DriverRegistrationView.as_view()(reqeust, *args, **kwargs)
            elif role == 'customer':
                return CustomerRegistrationView.as_view()(request, *args, **kwargs)
            else:
                raise MultiValueDictKeyError()
        except MultiValueDictKeyError:
            return HttpResponseBadRequest()
