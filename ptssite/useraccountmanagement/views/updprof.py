from django.shortcuts import render
from datastore.models import UnprivilegedUser, Driver, Customer
from datastore.models.driver import provinces
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.views import View
from django import forms

temp_driv = 'useraccountmanagement/settings_driver.html'
temp_cust = 'useraccountmanagement/settings_customer.html'

class UserForm(forms.ModelForm):
    field_order = ['password', 'password2', 'first_name', 'last_name',
                   'national_id', 'phone_number', 'account_number']
    class Meta:
        model = UnprivilegedUser
        fields = ['first_name', 'last_name', 'password',
                  'national_id', 'phone_number', 'account_number']
        widgets = {'password': forms.PasswordInput}
        
    password2 = forms.CharField(label='تکرار گذرواژه',
                                widget=forms.PasswordInput,
                                max_length=UnprivilegedUser._meta.get_field(
                                    'password').max_length)
    
    def clean(self):
        if 'password' in self.cleaned_data and 'password2' in self.cleaned_data\
           and self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise ValidationError('گذرواژه وارد شده و تکرار آن همخوانی ندارند',
                                  code='password-disagreement')
        ModelForm.clean(self)

class DriverForm(UserForm):
    field_order = UserForm.field_order + ['license_plate', 'certificate_number',
                   'regions']
    class Meta(UserForm.Meta):
        model = Driver
        fields = UserForm.Meta.fields + ['license_plate', 'certificate_number']
    regions = forms.MultipleChoiceField(label='از چه مناطقی درخواست جا به جایی می پذیرید؟',
                                        choices=provinces,
                                        widget=forms.CheckboxSelectMultiple)

class CustomerForm(UserForm):
    class Meta(UserForm.Meta):
        model = Customer
        
class UpdateProfileView(View):
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        role = request.session.get('role')
        if role == 'driver':
            driver = Driver.objects.get(pk=request.session['user_name'])
            return render(request, temp_driv, context={
                'form': DriverForm(instance=driver)
            })
        elif role == 'customer':
            customer = Customer.objects.get(pk=request.session['user_name'])
            return render(request, temp_cust, context={
                'form': CustomerForm(instance=customer)
            })
        else:
            return HttpResponseForbidden()

    def post(self, request, *args, **kwargs):
        role = request.session.get('role')
        if role == 'driver':
            driver = Driver.objects.get(pk=request.session['user_name'])
            form = DriverForm(initial=request.POST, instance=driver)
        elif role == 'customer':
            customer = Customer.objects.get(pk=request.session['user_name'])
            form = CustomerForm(initial=request.POST, instance=customer)
        else:
            return HttpResponseForbidden()
        if form.is_valid():
            form.save()
        return render(request, temp_driv, context={
            'form': form})
            
            
