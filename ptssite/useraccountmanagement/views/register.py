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
    use_required_attribute = False
    class Meta:
        model = UnprivilegedUser
        fields = ['first_name', 'last_name', 'username', 'password',
                  'national_id', 'phone_number', 'account_number']
        widgets = {'password': widgets.PasswordInput}
        error_messages = {
            'first_name': {
                'required': 'نام خود را وارد کنید'
            },
            'last_name': {
                'required': 'نام خانوادگی خود را وارد کنید'
            },
            'username': {
                'required': 'نام کاربری خود را وارد کنید'
            },
            'password': {
                'required': 'گذرواژه خود را وارد کنید'
            },
            'national_id': {
                'required': 'کد ملی خود را وارد کنید'
            },
            'phone_number': {
                'required': 'شماره تلفن خود را وارد کنید'
            },
            'account_number': {
                'required': 'شماره حساب خود را وارد کنید'
            }
        }
        
    password2 = forms.CharField(label='تکرار گذرواژه',
                                widget=widgets.PasswordInput,
                                max_length=UnprivilegedUser._meta.get_field(
                                    'password').max_length,
                                error_messages={
                                    'required': 'تکرار گذرواژه خود را وارد کنید'
                                })
    

    def license_agreed(value):
        if value != True:
            raise ValidationError('باید با شرایط و ضوابط موافق باشید',
                                  code='disagreement')
        
    license_agreement = forms.BooleanField(label='شرایط و ضوابط مذکور را قبول دارم',
                                           validators=[license_agreed],
                                           required=False)
    
    def clean(self):
        password1 = self.cleaned_data.get('password', '1')
        password2 = self.cleaned_data.get('password2', '2')
        if password1 != password2:
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
        error_messages = {
            **UserForm.Meta.error_messages,
            'license_plate': {
                'required': 'شماره پلاک خود را وارد کنید'
            },
            'certificate_number': {
                'required': 'شماره گواهینامه خود را وارد کنید'
            }
        }
        
    regions = forms.MultipleChoiceField(label='از چه مناطقی درخواست جا به جایی می پذیرید',
                                        choices=provinces,
                                        widget=widgets.CheckboxSelectMultiple,
                                        required=False)

    def register_regions(self):
        for province in self.cleaned_data['regions']:
            self.instance.add_province(province)

class DriverRegistrationView(CreateView):
    template_name = 'useraccountmanagement/register_driver.html'
    form_class = DriverForm
    success_url = '/useraccountmanagement/registrationsuccess/'

    def form_valid(self, form):
        form.register_regions()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseBadRequest()

    def post(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return super().post(request, *args, **kwargs)
        else:
            return HttpResponseBadRequest()
        
class CustomerForm(UserForm):
    class Meta(UserForm.Meta):
        model = Customer

class CustomerRegistrationView(CreateView):
    template_name = 'useraccountmanagement/register_customer.html'
    form_class = CustomerForm
    success_url = '/useraccountmanagement/registrationsuccess/'

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseBadRequest()

    def post(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return super().post(request, *args, **kwargs)
        else:
            return HttpResponseBadRequest()
    
class RegistrationView(TemplateView):
    template_name = 'useraccountmanagement/registration.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseBadRequest()

class RegistrationSuccessView(TemplateView):
    template_name = 'useraccountmanagement/registration_success.html'
