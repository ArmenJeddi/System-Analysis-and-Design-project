from django.shortcuts import render
from django.http import HttpResponse
from datastore.models import Driver, ProductSubmit, Order
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from authentication.decorators import customer_required

@customer_required
def listpurchases(request):
    if request.method == 'GET':
        
        purchase_list = Order.objects.filter(buyer=request.user.username)
        page = request.GET.get('page')

        paginator = Paginator(purchase_list, 15)
        try:
            purchases = paginator.get_page(page)
        except PageNotAnInteger:
            purchases = paginator.get_page(1)
        except EmptyPage:
            purchases = paginator.get_page(paginator.num_pages)

        return render(request, 'reporting/listpurchases.html', { 'purchases': purchases })