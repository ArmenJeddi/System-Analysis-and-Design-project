from django.views.generic.base import RedirectView
from authentication import auth

class LogoutView(RedirectView):
    url = '/systemmanagement/login/'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return super().get(request, *args, **kwargs)
