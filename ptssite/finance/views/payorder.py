from django.http import HttpResponse
from django.shortcuts import render
from datastore.models import Driver, ProductSubmit
from django import forms
from django.core.exceptions import ValidationError

template = 'finance/payorder.html'

class PayForm(forms.Form):
    balance = forms.IntegerField(min_value= 1000,
                                error_messages={
                                    'required': 'لطفا مبلغی را مشخص کنید',
                                    'min_value': 'مبلغ وارده باید حداقل 1000 تومان باشد'
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
        form = DepositForm(request.POST)
        if form.is_valid():
            customer = Customer.objects.get(pk=request.session['user_name'])
            customer.account_balance += form.cleaned_data['balance']
            customer.save()
            response = HttpResponse(status=303)
            response['Location'] = '/finance/depositmoney/'
        else:
            response = render(request, template, context=dict(form=form))
    return response