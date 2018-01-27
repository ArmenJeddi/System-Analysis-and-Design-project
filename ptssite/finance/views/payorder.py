from django.http import HttpResponse
from django.shortcuts import render
from datastore.models import Driver, ProductSubmit, Order
from django import forms
from django.core.exceptions import ValidationError
from authentication.decorators import customer_required

template = 'finance/payorder.html'

class PayForm(forms.Form):
    customer_address = forms.CharField(error_messages={
                                    'required': 'لطفا آدرسی را مشخص کنید',
                                })
@customer_required
def payorder(request):
    if request.method == 'GET':
        #to complete the form. what data is passed to payOrder?
        submittedProduct = ProductSubmit.objects.get(submitter=request.user.username)
        assignedDriver = Driver.objects.get(pk=request.user.session['username'])
        product_final_price = submittedProduct.quantity * submittedProduct.price
        driver_name = assignedDriver.first_name + " " + assignedDriver.last_name
        response = render(request, template, context=dict(form=PayForm(), 
                                                            submittedProduct=submittedProduct,
                                                            assignedDriver=assignedDriver,
                                                            product_final_price=product_final_price,
                                                            driver_name=driver_name))
    elif request.method == 'POST':
        form = PayForm(request.POST)
        if form.is_valid():
            if 'pay' in request.POST:
                order = Order.objects.get(pk=request.user.session['username'])
                order.location = form.cleanes_data['address']
                order.save()
                response = HttpResponse(status=303)
                response['Location'] = '/reporting/listpurchases/'
                #set timer
            elif 'cancel' in request.POST:
                response = HttpResponse(status=303)
                response['Location'] = '/finance/depositmoney/'
        else:
            response = render(request, template, context=dict(form=form))
    return response