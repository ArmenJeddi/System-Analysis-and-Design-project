from django.views.generic.list import ListView
from authentication.mixins import PrivilegedRequired
from datastore.models import ProductSubmit
from django.db.models import Q
import re
from datetime import date
from convertdate import persian

num_tab = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'),\
          str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
num_reg = re.compile(r'[0-9۰۱۲۳۴۵۶۷۸۹]+')
date_reg = re.compile(r'[0-9۰۱۲۳۴۵۶۷۸۹]{4}/[0-9۰۱۲۳۴۵۶۷۸۹]{1,2}/[0-9۰۱۲۳۴۵۶۷۸۹]{1,2}')

class BrowseProductsView(PrivilegedRequired, ListView):
    context_object_name = 'products'
    template_name = 'systemmanagement/browse_products.html'

    def get_queryset(self):
        params = self.request.GET
        products = ProductSubmit.objects.all()
        kwargs = {}

        product = params.get('product', '')
        if product:
            kwargs['product__name'] = product

        submitter = params.get('submitter', '')
        if submitter:
            kwargs['submitter__first_name__contains'] = submitter
            kwargs['submitter__last_name__contains'] = submitter

        province = params.get('province', '')
        if province:
            kwargs['province'] = province

        price_min = params.get('price_min', '')
        if price_min and re.fullmatch(num_reg, price_min):
            kwargs['price__gte'] = int(price_min.translate(num_tab[1]))

        price_max = params.get('price_max', '')
        if price_max and re.fullmatch(num_reg, price_max):
            kwargs['price__lte'] = int(price_max.translate(num_tab[1]))

        start_date = params.get('start_date', '')
        if start_date and re.fullmatch(date_reg, start_date):
            year, month, day = start_date.translate(num_tab[1]).split('/')
            kwargs['date__gte'] = date(*persian.to_gregorian(int(year),
                                                             int(month),
                                                             int(day)))

        end_date = params.get('end_date', '')
        if end_date and re.fullmatch(date_reg, end_date):
            year, month, day = start_date.translate(num_tab[1]).split('/')
            kwargs['date__lte'] = date(*persian.to_gregorian(int(year),
                                                             int(month),
                                                             int(day)))

        quantity_min = params.get('quantity_min', '')
        if quantity_min and re.fullmatch(num_reg, quantity_min):
            kwargs['quantity__gte'] = int(quantity_min)

        quantity_max = params.get('quantity_max', '')
        if quantity_max and re.fullmatch(num_reg, quantity_max):
            kwargs['quantity__lte'] = int(quantity_max)
            
        if kwargs:
            products = products.filter(**kwargs)

        for product in products:
            date = persian.from_gregorian(product.date.year,
                                          product.date.month,
                                          product.date.day)
            product.date_str = (str(date[0]) + '/' + str(date[1]) + '/'
                                + str(date[2])).translate(num_tab[0])
            product.quantity_str = str(product.quantity).translate(num_tab[0])
            product.price_str = str(product.price).translate(num_tab[0])
        
        return products
