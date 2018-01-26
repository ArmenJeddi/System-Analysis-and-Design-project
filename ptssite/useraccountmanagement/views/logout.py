from django.views.generic.base import RedirectView
from authentication.auth import logout

class LogoutView(RedirectView):

    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)
