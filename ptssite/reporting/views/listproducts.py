from django.shortcuts import render
from django.http import HttpResponse
from datastore.models import Driver, ProductSubmit, Order
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from authentication.decorators import customer_required

@customer_required
def listproducts(request):
    if request.method == 'GET':
        
        product_list = ProductSubmit.objects.filter(submitter=request.user.username)
        page = request.GET.get('page')

        paginator = Paginator(product_list, 2)
        try:
            products = paginator.get_page(page)
        except PageNotAnInteger:
            products = paginator.get_page(1)
        except EmptyPage:
            products = paginator.get_page(paginator.num_pages)

        return render(request, 'reporting/listproducts.html', { 'products': products })