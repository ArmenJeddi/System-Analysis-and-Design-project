from django.views.generic.list import ListView
from authentication.mixins import PrivilegedRequired
from datastore.models import UnprivilegedUser
from django.db.models import Q

num_tab = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'),\
          str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')

class BrowseUsersView(PrivilegedRequired, ListView):
    context_object_name = 'users'
    template_name = 'systemmanagement/browse_users.html'

    def get_queryset(self):
        params = self.request.GET
        users = UnprivilegedUser.objects.all()

        name = params.get('name', '')
        if name:
            users = users.filter(Q(first_name__contains=name)
                                 |Q(last_name__contains=name))

        phone_number = params.get('phone_number', '').translate(num_tab[0])
        if phone_number:
            users = users.filter(phone_number__contains=phone_number)

        national_id = params.get('national_id', '').translate(num_tab[0])
        if national_id:
            users = users.filter(national_id__contains=national_id)

        license_plate = params.get('license_plate', '').translate(num_tab[0])
        certificate_number = params.get('certificate_number', '').translate(num_tab[1])
        kwargs = {}
        if license_plate:
            kwargs['driver__license_plate__contains'] = license_plate
        if certificate_number:
            kwargs['driver__certificate_number__contains'] = certificate_number
        if kwargs:
            users = users.filter(**kwargs)
        return users
