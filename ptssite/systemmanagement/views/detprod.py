from django.views.generic.edit import UpdateView
from authentication.mixins import PrivilegedRequired
from datastore.models import ProductSubmit

class DetailUserView(PrivilegedRequired, UpdateView):
    template_name = 'systemmanagement/detail_product.html'
    model = ProductSubmit
    context_object_name = 'product'
    success_url = '/systemmanagement/browseproducts/'
