from django.shortcuts import render
from django.http import HttpResponse
from datastore.models import Driver, ProductSubmit, Order
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from authentication.decorators import customer_required
from convertdate import persian

@customer_required
def listproducts(request):
    if request.method == 'GET':
        
        temp_list = ProductSubmit.objects.filter(submitter=request.user.username)
        if request.GET.get('search'):
            temp_list = temp_list.filter(product__name__contains = request.GET.get('search'))
        temp_list = list(reversed(temp_list))
        product_list = [[0 for x in range(3)] for y in range(len(temp_list))]
        for i in range(0, len(temp_list)):
            product_list[i][0] = i + 1
            product_list[i][1] = temp_list[i]
            product_list[i][2] = persian.from_gregorian(temp_list[i].date.year, temp_list[i].date.month, temp_list[i].date.day)

        page = request.GET.get('page')

        paginator = Paginator(product_list, 2)
        try:
            list_with_dates = paginator.get_page(page)
        except PageNotAnInteger:
            list_with_dates = paginator.get_page(1)
        except EmptyPage:
            list_with_dates = paginator.get_page(paginator.num_pages)

        return render(request, 'reporting/listproducts.html', { 'products': product_list })