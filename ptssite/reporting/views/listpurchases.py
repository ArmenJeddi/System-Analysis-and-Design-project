from django.shortcuts import render
from django.http import HttpResponse
from datastore.models import Driver, ProductSubmit, Order
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from authentication.decorators import customer_required
from django import forms
from django.core.exceptions import ValidationError
import datetime

from convertdate import persian

template = 'reporting/listpurchases.html'

class ReceptionForm(forms.Form):
    order = forms.IntegerField()

@customer_required
    
def listpurchases(request):

    temp_list = Order.objects.filter(buyer=request.user.username)
    purchase_list = [[0 for x in range(3)] for y in range(len(temp_list))]
    for i in range(0, len(temp_list)):
        purchase_list[i][0] = i + 1
        purchase_list[i][1] = temp_list[i]
        tarikh = persian.from_gregorian(temp_list[i].date.year, temp_list[i].date.month, temp_list[i].date.day)
        purchase_list[i][2] = tarikh

    page = request.GET.get('page')

    paginator = Paginator(purchase_list, 2)
    try:
        purchases = paginator.get_page(page)
    except PageNotAnInteger:
        purchases = paginator.get_page(1)
    except EmptyPage:
        purchases = paginator.get_page(paginator.num_pages)

    if request.method == 'POST':
        print(dict(request.POST))
        keys = [key for key in request.POST.keys()]
        order_id = int(keys[1])

        sel_order = Order.objects.get(pk = order_id)
        sel_order.buyer_receipt = True
        sel_order.date_received = datetime.date.today()
        sel_order.save()
        sel_order.driver.reserved = False
        sel_order.driver.save()
        # request.session.pop('driver_id', None)


    return render(request, 'reporting/listpurchases.html', {'purchases': purchases})