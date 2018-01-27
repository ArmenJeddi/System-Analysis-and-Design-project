from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.forms import Form, CharField
from datastore.models import User
from django.http import HttpResponseNotFound
import string
import random
from external import smsgw

class PasswordRecoveryForm(Form):
    username = CharField(label='نام کاربری')

password_alphabet = string.ascii_letters + string.digits

class PasswordRecoveryView(FormView):

    form_class = PasswordRecoveryForm
    success_url = '/useraccountmanagement/passwordrecoverysuccess/'
    template_name = 'useraccountmanagement/password_recovery.html'

    def post(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            return super().post(request, *args, **kwargs)
        else:
            return HttpResponseNotFound()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            del context['form']
            context['logged_in'] = True
        return context

    def form_valid(self, form):
        try:
            user = User.objects.get(username=form.cleaned_data['username'])
            new_password = ''.join(random.choices(password_alphabet, k=7))
            user.password = new_password
            user.save()
            smsgw.send_password(user.phone_number, new_password)
        except User.DoesNotExist:
            pass
        return super().form_valid(form)

class PasswordRecoverySuccessView(TemplateView):
    template_name = 'useraccountmanagement/password_recovery_success.html'
