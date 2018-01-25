from django.http import HttpResponse
from django.shortcuts import render
from datastore.models import User, Customer
from django import forms
from django.core.exceptions import ValidationError

template = 'finance/depositmoney.html'

class DepositForm(forms.Form):
    balance = forms.IntegerField(min_value= 1000,
                                error_messages={
                                    'required': 'لطفا مبلغی را مشخص کنید',
                                    'min_value': 'مبلغ وارده باید حداقل 1000 تومان باشد'
                                })

def depositmoney(request):
    if request.method == 'GET':
        if 'user_name' in request.session and request.session['role'] == 'customer':
            current_amount = Customer.objects.get(pk=request.session['user_name']).account_balance
            response = render(request, template, context=dict(form=DepositForm(), current_amount=current_amount))
        else:
            response = HttpResponse(status=303)
            response['Location']='/useraccountmanagement/login/'
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