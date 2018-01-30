from django.views.generic.edit import DeleteView
from authentication.mixins import PrivilegedRequired
from datastore.models import ProductSubmit

class DetailUserView(PrivilegedRequired, DeleteView):
    template_name = 'systemmanagement/detail_product.html'
    model = ProductSubmit
    pk_url_kwarg = 'product_id'
    context_object_name = 'product'
    success_url = '/systemmanagement/browseproducts/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = self.object.order_set.all()
        return context
        
