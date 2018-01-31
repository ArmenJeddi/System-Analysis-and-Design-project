from django.views.generic.edit import UpdateView
from authentication.mixins import PrivilegedRequired
from datastore.models import ProductSubmit
from convertdate import persian

num_tab = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')

class DetailProductView(PrivilegedRequired, UpdateView):
    template_name = 'systemmanagement/detail_product.html'
    model = ProductSubmit
    fields = ['active']
    context_object_name = 'product'
    success_url = '/systemmanagement/browseproducts/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = context['product']
        date = persian.from_gregorian(product.date.year,
                                      product.date.month,
                                      product.date.day)
        product.date_str = (str(date[0]) + '/' + str(date[1]) + '/'
                            + str(date[2])).translate(num_tab)
        product.quantity_str = str(product.quantity).translate(num_tab)
        product.price_str = str(product.price).translate(num_tab)

        return context
