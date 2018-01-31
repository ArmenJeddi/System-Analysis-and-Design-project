from django.views.generic.edit import FormView
from django.forms import Form, CharField, PasswordInput
from authentication.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest

class LoginForm(Form):
    username = CharField(label='نام کاربری')
    password = CharField(label='گذرواژه',
                         widget=PasswordInput)

    def clean(self):
        try:
            user = authenticate(self.cleaned_data['username'],
                                self.cleaned_data['password'])
            if user is None or not user.is_unprivileged():
                raise ValidationError('نام کاربری یا گذرواژه اشتباه است',
                                      code='invalid_username_password')
            else:
                self.user = user
        except KeyError:
            pass

class LoginView(FormView):
    template_name = 'useraccountmanagement/login.html'
    form_class = LoginForm
    success_url = '/useraccountmanagement/profile/'

    def form_valid(self, form):
        login(self.request, form.user)
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
