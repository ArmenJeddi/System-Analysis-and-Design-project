from django.views.generic.edit import UpdateView
from authentication.mixins import PrivilegedRequired
from datastore.models import UnprivilegedUser
from external import smsgw

class DetailUserView(PrivilegedRequired, UpdateView):
    template_name = 'systemmanagement/detail_user.html'
    model = UnprivilegedUser
    fields = ['banned']
    pk_url_kwarg = 'username'
    context_object_name = 'user'
    success_url = '/systemmanagement/browseusers/'

    def form_valid(self, form):
        smsgw.send_account_status(self.object.phone_number,
                                  form.cleaned_data['banned'])
        return super().form_valid(form)
