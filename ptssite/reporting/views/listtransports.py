from django.shortcuts import render
from django.http import HttpResponse
from datastore.models import order, ProductSubmit, Order
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from authentication.decorators import driver_required

@driver_required
def listtransports(request):
    if request.method == 'GET':
        
        order_list = Order.objects.filter(driver=request.user.username)
        page = request.GET.get('page')

        paginator = Paginator(order_list, 2)
        try:
            orders = paginator.get_page(page)
        except PageNotAnInteger:
            orders = paginator.get_page(1)
        except EmptyPage:
            orders = paginator.get_page(paginator.num_pages)

        return render(request, 'reporting/listtransports.html', { 'orders': orders })