from django.shortcuts import render
from django.http import HttpResponse
from django.forms import ModelForm
from datastore.models import User, Driver, Customer
from datastore.models.driver import provinces
from django.forms import widgets
from django import forms
from django.core.exceptions import ValidationError
from django.db import IntegrityError

template = 'useraccountmanagement/registration.html'
max_length_msg = 'مقدار وارد شده باید حداکثر {} کاراکتر باشد'

class UserForm(ModelForm):
    field_order = ['first_name', 'last_name', 'user_name', 'password',
                   'password2', 'national_id', 'phone_number',
                   'account_number', 'license_agreement']
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'user_name', 'password',
                  'national_id', 'phone_number', 'account_number']
        widgets = {'password': widgets.PasswordInput}
        error_messages = {
            'first_name': {
                'required': 'لطفا نام خود را وارد کنید',
                'max_length': max_length_msg.format(User._meta.get_field('first_name').max_length)
            },
            'last_name': {
                'required': 'لطفا نام خانوادگی خود را وارد کنید',
                'max_length': max_length_msg.format(User._meta.get_field('last_name').max_length)
            },
            'user_name': {
                'required': 'لطفا یک نام کاربری برای خود وارد کنید',
                'max_length': max_length_msg.format(User._meta.get_field('user_name').max_length)
            },
            'password': {
                'required': 'لطفا یک گذرواژه برای خود وارد کنید',
                'max_length': max_length_msg.format(User._meta.get_field('password').max_length)
            },
            'national_id': {
                'required': 'لطفاکد ملی خود را وارد کنید',
                'max_length': max_length_msg.format(User._meta.get_field('national_id').max_length)
            },
            'phone_number': {
                'required': 'لطفا شماره تلفن همراه خود را وارد کنید',
                'max_length': max_length_msg.format(User._meta.get_field('phone_number').max_length)
            },
            'account_number': {
                'required': 'لطفا شماره کارت بانکی خود را وارد کنید',
                'max_length': max_length_msg.format(User._meta.get_field('account_number').max_length)
            }
        }
        
    password2 = forms.CharField(label='تکرار گذرواژه',
                                widget=widgets.PasswordInput,
                                max_length=User._meta.get_field(
                                    'password').max_length,
                                error_messages={
                                    'required': 'لطفا تکرار گذرواژه خود را وارد کنید',
                                    'max_length': max_length_msg.format(User._meta.get_field('password').max_length)
                                })
    

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
                                  code='password-disagreement')
        ModelForm.clean(self)

class DriverForm(UserForm):
    field_order = ['first_name', 'last_name', 'user_name', 'password',
                   'password2', 'national_id', 'phone_number',
                   'account_number', 'license_plate', 'certificate_number',
                   'regions', 'license_agreement']
    class Meta(UserForm.Meta):
        model = Driver
        fields = UserForm.Meta.fields + ['license_plate', 'certificate_number']
        error_messages = {
            **UserForm.Meta.error_messages,
            'license_plate': {
                'max_length': max_length_msg.format(Driver._meta.get_field('license_plate').max_length)
            },
            'certificate_number': {
                'max_length': max_length_msg.format(Driver._meta.get_field('certificate_number').max_length)
            }
        }
    regions = forms.MultipleChoiceField(label='از چه مناطقی درخواست جا به جایی می پذیرید؟',
                                        choices=provinces,
                                        widget=widgets.CheckboxSelectMultiple)

class CustomerForm(UserForm):
    class Meta(UserForm.Meta):
        model = Customer

def registration(request):
    if 'user_name' in request.session:
        response = HttpResponse(status=307)
        response['Location'] = ''
        raise NotImplementedError
    elif request.method == 'GET':
        response = render(request, template,
                          context={
                              'driver_form': DriverForm(),
                              'customer_form': CustomerForm()
                          })
    elif request.method == 'POST':
        if request.path.endswith('customer/'):
            form = CustomerForm(request.POST)
            if form.is_valid():
                try:
                    form.save()
                except IntegrityError:
                    response = render(render, template,
                                      context={
                                          'driver_form': DriverForm(),
                                          'customer_form': CustomerForm()
                                      })
                else:
                    response = HttpResponse(status=303)
                    response['Location'] = '/useraccountmanagement/login/'
            else:
                response = render(request, template,
                                  context={
                                      'driver_form': DriverForm(),
                                      'customer_form': form
                                  })
        elif request.path.endswith('driver/'):
            form = DriverForm(request.POST)
            if form.is_valid():
                for province in form.cleaned_data['regions']:
                    form.instance.add_province(province)
                form.instance.vehicle_model = 'کامیون'
                form.instance.vehicle_capacity = 20000
                try:
                    form.save()
                except IntegrityError:
                    response = render(render, template,
                                      context={
                                          'driver_form': DriverForm(),
                                          'customer_form': CustomerForm()
                                      })
                else:
                    response = HttpResponse(status=303)
                    response['Location'] = '/useraccountmanagement/login/'
            else:
                response = render(request, template,
                                  context={
                                      'driver_form': form,
                                      'customer_form': CustomerForm()
                                  })
        else:
            response = render(request, template,
                              context={
                                  'driver_form': DriverForm(),
                                  'customer_form': CustomerForm()
                              })
    return response
