from datastore.models import UnprivilegedUser, Driver, Customer
from datastore.models import driver
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.forms import ModelForm, CharField, MultipleChoiceField,\
    CheckboxSelectMultiple, PasswordInput
from authentication.mixins import UnprivilegedRequired
from django.core.exceptions import ValidationError

class UserForm(ModelForm):
    field_order = ['password', 'password2', 'first_name', 'last_name',
                   'national_id', 'phone_number', 'account_number']
    class Meta:
        model = UnprivilegedUser
        fields = ['first_name', 'last_name', 'password',
                  'national_id', 'phone_number', 'account_number']
    
    password = CharField(label='تکرار گذرواژه',
                         required=False,
                         widget=PasswordInput,
                         max_length=UnprivilegedUser._meta.get_field(
                             'password').max_length)
    password2 = CharField(label='تکرار گذرواژه',
                          required=False,
                          widget=PasswordInput,
                          max_length=UnprivilegedUser._meta.get_field(
                              'password').max_length)
    
    def clean(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise ValidationError('گذرواژه وارد شده و تکرار آن همخوانی ندارند',
                                  code='password_disagreement')

        if password1 == '':
            self.cleaned_data['password'] = self.instance.password
            
class DriverForm(UserForm):
    field_order = UserForm.field_order + ['license_plate',
                                          'certificate_number', 'regions']
    class Meta(UserForm.Meta):
        model = Driver
        fields = UserForm.Meta.fields + ['license_plate',
                                         'certificate_number']
    regions = MultipleChoiceField(label='از چه مناطقی درخواست جا به جایی می پذیرید؟',
                                  choices=driver.provinces,
                                  widget=CheckboxSelectMultiple)

    def register_regions(self):
        old_provinces = {province[0] for province in\
                         self.instance.province_list()}
        new_provinces = {*self.cleaned_data['regions']}
        
        for province in old_provinces - new_provinces:
            self.instance.remove_province(province)

        for province in new_provinces - old_provinces:
            self.instance.add_province(province)
            
class CustomerForm(UserForm):
    class Meta(UserForm.Meta):
        model = Customer

class UpdateProfileView(UnprivilegedRequired, UpdateView):
    template_name = 'useraccountmanagement/settings.html'
    success_url = '/useraccountmanagement/updateprofilesuccess/'
    model = UnprivilegedUser
    pk_url_kwarg = 'username'

    def form_valid(self, form):
        form.register_regions()
        return super().form_valid(form)
    
    def get_initial(self):
        initial = super().get_initial()
        if self.object.is_driver():
            current_provinces = [province[0] for province in self.object.province_list()]
            initial.update(regions=current_provinces)
        return initial

    def get_form_class(self):
        if self.object.is_driver():
            return DriverForm
        elif self.object.is_customer():
            return CustomerForm

    def get_object(self, queryset=None):
        unprivilegeduser = super().get_object(queryset)
        if unprivilegeduser.is_driver():
            return unprivilegeduser.driver
        elif unprivilegeduser.is_customer():
            return unprivilegeduser.customer

class UpdateProfileSuccessView(TemplateView):
    template_name = 'useraccountmanagement/update_profile_success.html'
