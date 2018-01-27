from django.shortcuts import render
from django.http import HttpResponse
from datastore.models import Driver, ProductSubmit, Order
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from authentication.decorators import customer_required

@customer_required
def listpurchases(request):
    if request.method == 'GET':
        
        purchase_list = Order.objects.get(buyer=request.user.username)
        page = request.GET.get('page', 1)

        paginator = Paginator(purchase_list, 10)
        try:
            purchases = paginator.page(page)
        except PageNotAnInteger:
            purchases = paginator.page(1)
        except EmptyPage:
            purchases = paginator.page(paginator.num_pages)

        return render(request, 'reporting/listpurchases.html', { 'purchases': purchases })