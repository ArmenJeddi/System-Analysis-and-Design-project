from django.http import HttpResponse
from django.shortcuts import render
from datastore.models import Driver, ProductSubmit, Order
from django import forms
from django.core.exceptions import ValidationError

template = 'finance/payorder.html'

class PayForm(forms.Form):
    address = forms.CharField(error_messages={
                                    'required': 'لطفا آدرسی را مشخص کنید',
                                })

def payorder(request):
    if request.method == 'GET':
        if 'user_name' in request.session and request.session['role'] == 'customer':
            submittedProduct = ProductSubmit.objects.get(pk=request.session['name'])
            assignedDriver = Driver.objects.get(pk=request.session['username'])
            product_final_price = submittedProduct.quantity * submittedProduct.price
            driver_name = assignedDriver.first_name + " " + assignedDriver.last_name
            response = render(request, template, context=dict(form=PayForm(), 
                                                                submittedProduct=submittedProduct,
                                                                assignedDriver=assignedDriver,
                                                                product_final_price=product_final_price,
                                                                driver_name=driver_name))
        else:
            response = render(request, template)
    elif request.method == 'POST':
        form = PayForm(request.POST)
        if form.is_valid():
            order = Order.objects.get(pk=request.session['username'])
            order.location = form.cleanes_data['address']
            order.save()
            response = HttpResponse(status=303)
            response['Location'] = '/reporting/listpurchases/'
            #set timer
            #resign from purchasing
        else:
            response = render(request, template, context=dict(form=form))
    return response