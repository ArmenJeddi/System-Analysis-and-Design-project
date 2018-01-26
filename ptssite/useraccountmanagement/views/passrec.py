from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView, ModelFormMixin
from datastore.models import User
from django.http import HttpResponseNotFound

class PasswordRecoveryView(ModelFormMixin, FormView):

    model = User
    fields = ['phone_number']
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

    def form_invalid(self, form):
        return form_valid(self, form)

class PasswordRecoverySuccessView(TemplateView):
    template_name = 'useraccountmanagement/password_recovery_success.html'
