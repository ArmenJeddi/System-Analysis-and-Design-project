from django.shortcuts import render
from django.http import HttpResponse
from datastore.models import Driver, ProductSubmit, Order
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from authentication.decorators import privileged_required

@privileged_required(login_url="/systemmanagement/login/")
def listorders(request):
    if request.method == 'GET':
        
        temp_list = Order.objects.all()
        if request.GET.get('search'):
            temp_list = temp_list.filter(product__product__name__contains = request.GET.get('search'))
        temp_list = list(reversed(temp_list))
        order_list = [[0 for x in range(2)] for y in range(len(temp_list))]
        for i in range(0, len(temp_list)):
            order_list[i][0] = i + 1
            order_list[i][1] = temp_list[i]
        page = request.GET.get('page')

        paginator = Paginator(order_list, 2)
        try:
            orders = paginator.get_page(page)
        except PageNotAnInteger:
            orders = paginator.get_page(1)
        except EmptyPage:
            orders = paginator.get_page(paginator.num_pages)

        return render(request, 'reporting/listorders.html', { 'orders': orders })