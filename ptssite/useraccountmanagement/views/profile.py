from django.views.generic.base import TemplateView
from authentication.mixins import UnprivilegedRequired

class ProfileView(UnprivilegedRequired, TemplateView):

    def get_template_names(self):
        if self.request.user.unprivilegeduser.is_customer():
            return 'useraccountmanagement/profile_customer.html'
        elif self.request.user.unprivilegeduser.is_driver():
            return 'useraccountmanagement/profile_driver.html'
