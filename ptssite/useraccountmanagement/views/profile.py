from django.views.generic.base import TemplateView
from authentication.mixins import UnprivilegedRequired
from django.http import HttpResponseRedirect

class ProfileView(UnprivilegedRequired, TemplateView):

    def get_template_names(self):
        if self.request.user.unprivilegeduser.is_customer():
            return 'useraccountmanagement/profile_customer.html'
        elif self.request.user.unprivilegeduser.is_driver():
            return 'useraccountmanagement/profile_driver.html'

    def post(self, request, *args, **kwargs):
        if request.user.unprivilegeduser.is_driver():
            avail = True if request.POST.get('available') == 'true' else False
            request.user.unprivilegeduser.driver.availability = avail
            request.user.unprivilegeduser.driver.save()
            return HttpResponseRedirect('/useraccountmanagement/profile/')
