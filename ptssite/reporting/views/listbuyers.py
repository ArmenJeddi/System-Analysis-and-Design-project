from django.shortcuts import render
from django.http import HttpResponse
from datastore.models import Order
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from authentication.decorators import privileged_required

@privileged_required(login_url="/systemmanagement/login/")
def listbuyers(request):
    if request.method == 'GET':
        
        buyer_list = Order.objects.values_list("buyer", flat=True).distinct()
        order_list = Order.objects.filter(buyer__in=buyer_list)
        
        set_seen = {}
        lst_result = []
     
        for order in order_list:
            if order.buyer in set_seen:
                continue
            set_seen[order.buyer] = 1
            lst_result.append(order)
     
        order_list = lst_result
        
        page = request.GET.get('page')

        paginator = Paginator(order_list, 2)
        try:
            orders = paginator.get_page(page)
        except PageNotAnInteger:
            orders = paginator.get_page(1)
        except EmptyPage:
            orders = paginator.get_page(paginator.num_pages)

        return render(request, 'reporting/listbuyers.html', { 'orders': orders })