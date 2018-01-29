from django.views.generic.base import TemplateView
from authentication.mixins import PrivilegedRequired

class ProfileView(PrivilegedRequired, TemplateView):
    template_name = 'systemmanagement/profile.html'
