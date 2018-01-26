from django.views.generic.edit import FormView
from django.forms import ModelForm, PasswordInput
from datastore.models import User
from authentication.auth import authenticate, login
from django.core.exceptions import ValidationError

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': PasswordInput
            }

    def clean(self):
        user = authenticate(self.cleaned_data['username'],
                            self.cleaned_data['password'])
        if user:
            self.instance = user
        else:
            raise ValidationError('نام کاربری یا گذرواژه اشتباه وارد شده است',
                                  'invalid_username_password')

    def login(self, request):
        if self.is_valid():
            login(request, self.instance)

    
class LoginView(FormView):
    template_name = 'useraccountmanagement/login.html'
    form_class = LoginForm
    success_url = '/useraccountmanagement/profile/'

    def form_valid(self, form):
        form.login(self.request)
        return super().form_valid(form)
