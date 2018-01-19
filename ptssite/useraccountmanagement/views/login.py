from django.http import HttpResponse
from django.shortcuts import render
from datastore.models import User
from django import forms
from .register import max_length_msg
from django.core.exceptions import ValidationError

template = 'useraccountmanagement/login.html'

class UserForm(forms.Form):
    user_name = forms.CharField(label='نام کاربری',
                                error_messages={
                                    'required': 'لطفا نام کاربری را وارد نمایید',
                                    'max_length': max_length_msg.format(User._meta.get_field('user_name').max_length)
                                })
    password = forms.CharField(label='گذرواژه',
                                error_messages={
                                    'required': 'لطفا گذرواژه را وارد نمایید',
                                    'max_length': max_length_msg.format(User._meta.get_field('password').max_length)
                                },
                               widget=forms.PasswordInput)
        
def login(request):
    if request.method == 'GET':
        if 'user_name' in request.session:
            response = HttpResponse(status=307)
            response['Location'] = ''
            raise NotImplementedError
        else:
            response = render(request, template, context=dict(form=UserForm()))
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(pk=form.cleaned_data['user_name'])
                if user.password == form.cleaned_data['password']:
                    role = getattr(user, 'driver', None)
                    if not role:
                        role = getattr(user, 'customer')
                    request.session['role'] = role
                    response = HttpResponse(status=303)
                    response['Location'] = ''
                    raise NotImplementedError
                else:
                    form.add_error(None, ValidationError('نام کاربری یا گذرواژه وارد شده اشتباه است',
                                                         code='invalid-username-password'))
                    response = render(request, template, context=dict(form=form))
            except (User.DoesNotExist, AttributeError):
                form.add_error(None, ValidationError('نام کاربری یا گذرواژه وارد شده اشتباه است',
                                                     code='invalid-username-password'))
                response = render(request, template, context=dict(form=form))
        else:
            response = render(request, template, context=dict(form=form))
    return response
