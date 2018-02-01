from django.shortcuts import render
from django.http import HttpResponse
from datastore.models import Driver, ProductSubmit, Order
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from authentication.decorators import customer_required

@customer_required
def listproducts(request):
    if request.method == 'GET':
        
        temp_list = ProductSubmit.objects.filter(submitter=request.user.username)
        product_list = [[0 for x in range(2)] for y in range(len(temp_list))]
        for i in range(0, len(temp_list)):
            product_list[i][0] = i + 1
            product_list[i][1] = temp_list[i]
        page = request.GET.get('page')

        paginator = Paginator(product_list, 2)
        try:
            products = paginator.get_page(page)
        except PageNotAnInteger:
            products = paginator.get_page(1)
        except EmptyPage:
            products = paginator.get_page(paginator.num_pages)

        return render(request, 'reporting/listproducts.html', { 'products': products })