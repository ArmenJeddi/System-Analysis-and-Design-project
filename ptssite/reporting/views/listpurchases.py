from django.shortcuts import render
from django.http import HttpResponse
from datastore.models import Driver, ProductSubmit, Order
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from authentication.decorators import customer_required
from django import forms
from django.core.exceptions import ValidationError

from convertdate import persian

template = 'reporting/listpurchases.html'

class ReceptionForm(forms.Form):
    order = forms.IntegerField()

@customer_required
    
def listpurchases(request):
    if request.method == 'GET':
        
        temp_list = Order.objects.filter(buyer=request.user.username)
        purchase_list = [[0 for x in range(3)] for y in range(len(temp_list))]
        for i in range(0, len(temp_list)):
            purchase_list[i][0] = i + 1
            purchase_list[i][1] = temp_list[i]
            tarikh = persian.from_gregorian(temp_list[i].year, temp_list[i].month, temp_list[i].day)
            purchase_list[i][2] = tarikh
        page = request.GET.get('page')

        paginator = Paginator(purchase_list, 2)
        try:
            purchases = paginator.get_page(page)
        except PageNotAnInteger:
            purchases = paginator.get_page(1)
        except EmptyPage:
            purchases = paginator.get_page(paginator.num_pages)

        response = render(request, 'reporting/listpurchases.html', { 'purchases': purchases })
        
    elif request.method == 'POST':
        
        form = ReceptionForm(request.POST)
        if form.is_valid():
            order = Order.objects.get(pk = form.cleaned_data['order'])
            order.buyer_receipt = True
            order.save()
            response = HttpResponse(status=303)
            response['Location'] = '/reporting/listpurchases/'
        else:
            response = render(request, template, context=dict(form=form))
    
    return response