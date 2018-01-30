from django.shortcuts import render
from django.http import HttpResponse
from datastore.models import Driver, ProductSubmit, Order
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from authentication.decorators import privileged_required

@privileged_required(login_url="/systemmanagement/login/")
def listorders(request):
    if request.method == 'GET':
        
        order_list = Order.objects.all()
        page = request.GET.get('page')

        paginator = Paginator(order_list, 2)
        try:
            orders = paginator.get_page(page)
        except PageNotAnInteger:
            orders = paginator.get_page(1)
        except EmptyPage:
            orders = paginator.get_page(paginator.num_pages)

        return render(request, 'reporting/listorders.html', { 'orders': orders })