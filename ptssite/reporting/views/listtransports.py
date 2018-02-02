from django.shortcuts import render
from django.http import HttpResponse
from datastore.models import order, ProductSubmit, Order
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from authentication.decorators import driver_required
from django import forms
from django.core.exceptions import ValidationError

template = 'reporting/listpurchases.html'

class ReceptionForm(forms.Form):
    order = forms.IntegerField()

@driver_required
def listtransports(request):
    if request.method == 'GET':
        
        temp_list = Order.objects.filter(driver=request.user.username)
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

        response = render(request, 'reporting/listtransports.html', { 'orders': orders })
        
    elif request.method == 'POST':
        
        form = ReceptionForm(request.POST)
        if form.is_valid():
            order = Order.objects.get(pk = form.cleaned_data['order'])
            order.driver_receipt = True
            order.save()
            response = HttpResponse(status=303)
            response['Location'] = '/reporting/listtransports/' 
        else:
            response = render(request, template, context=dict(form=form))
    
    return response