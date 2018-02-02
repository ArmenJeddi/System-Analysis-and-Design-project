from django.views.generic.edit import UpdateView
from authentication.mixins import PrivilegedRequired
from datastore.models import UnprivilegedUser
from external import smsgw

num_tab = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = context['user']
        if user.is_customer():
            user = user.customer
            user.account_balance_str = str(user.account_balance).translate(num_tab)
        return context
