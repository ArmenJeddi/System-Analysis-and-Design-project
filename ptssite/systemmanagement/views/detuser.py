from django.views.generic.edit import UpdateView
from authentication.mixins import PrivilegedRequired
from datastore.models import UnprivilegedUser

class DetailUserView(PrivilegedRequired, UpdateView):
    template_name = 'systemmanagement/detail_user.html'
    model = UnprivilegedUser
    fields = ['banned']
    pk_url_kwarg = 'username'
    context_object_name = 'user'
    success_url = '/systemmanagement/browseusers/'
