from django.shortcuts import render
from django.http import HttpResponse
from datastore.models import Driver, ProductSubmit, Order
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from authentication.decorators import customer_required
from django import forms
from django.core.exceptions import ValidationError

template = 'reporting/listpurchases.html'

class ReceptionForm(forms.Form):
    order = forms.IntegerField()

@customer_required
    
def listpurchases(request):
    if request.method == 'GET':
        
        purchase_list = Order.objects.filter(buyer=request.user.username)
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