from django.http import HttpResponse
from django.shortcuts import render
from datastore.models import User
from django import forms
from django.core.exceptions import ValidationError

template = 'useraccountmanagement/login.html'

class UserForm(forms.Form):
    user_name = forms.CharField(label='نام کاربری')
    password = forms.CharField(label='گذرواژه', widget=forms.PasswordInput)
        
def login(request):
    if request.method == 'GET':
        if 'user_name' in request.session:
            response = HttpResponse(status=307)
            response['Location'] = ''
            raise NotImplementedError
        else:
            response = render(request, template,
                              context={
                                  'form': UserForm()
                              })
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(pk=form.cleaned_data['user_name'])
                if user.password == form.cleaned_data['password']:
                    request.session['user_name'] = user.user_name
                    if hasattr(user, 'driver'):
                        role = 'driver'
                    elif hasattr(user, 'customer'):
                        role = 'customer'
                    request.session['role'] = role
                    response = HttpResponse(status=303)
                    response['Location'] = '/useraccountmanagement/updateprofile'
                    #raise NotImplementedError
                else:
                    form.add_error(None, ValidationError('نام کاربری یا گذرواژه وارد شده اشتباه است',
                                                         code='invalid-username-password'))
                    response = render(request, template,
                                      context={
                                          'form': form
                                      })
            except (User.DoesNotExist):
                form.add_error(None, ValidationError('نام کاربری یا گذرواژه وارد شده اشتباه است',
                                                     code='invalid-username-password'))
                response = render(request, template,
                                  context={
                                      'form': form
                                  })
        else:
            response = render(request, template,
                              context={
                                  'form': form
                              })
    return response
