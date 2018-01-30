from django.views.generic.base import RedirectView
from authentication.auth import logout

class LogoutView(RedirectView):

    url = '/useraccountmanagement/login/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)
