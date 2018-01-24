from django.shortcuts import render
from django.views import View
from django import forms
from datastore.models import User

template = 'useraccountmanagement/password_recovery.html'

class PasswordRecoveryForm(forms.Form):
    username = forms.CharField(label=User._meta.get_field('username').
                                verbose_name,
                                max_length=User._meta.get_field('username').
                                max_length)

class PasswordRecoveryView(View):

    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        if 'user_name' in request.session:
            response = HttpResponse(status=303)
            response['Location'] = '/useraccountmanagement/updateprofile/'
        else:
            response = render(request, template,
                              context={
                                  'form': PasswordRecoveryForm()
                              })
        return response

    def post(self, request, *args, **kwargs):
        if'user_name' in request.session:
            response = HttpResponse(status=303)
            response['Location'] = '/useraccountmanagement/updateprofile/'
        else:
            form = PasswordRecoveryForm(request.POST)
            if form.is_valid():
                response = HttpResponse('درخواست با موفقیت انجام شد',
                                        status=303)
                respone['Location'] = '/useraccountmanagement/login/'
            else:
                response = render(request, template,
                                  context={
                                      'form': form
                                  })
        return response
