from django.http import HttpResponse
from django.shortcuts import render
from datastore.models import User, Customer
from django import forms
from django.core.exceptions import ValidationError
from authentication.decorators import customer_required

template = 'finance/depositmoney.html'

class DepositForm(forms.Form):
    balance = forms.IntegerField(
                                error_messages={
                                    'required': 'لطفا مبلغی را مشخص کنید',
                                })
    
@customer_required
def depositmoney(request):
    customer = request.user.unprivilegeduser.customer
    if request.method == 'GET':
        diff_amount = 0
        if 'diff_amount' in request.session:
            diff_amount = request.session.pop('diff_amount')

        current_amount = customer.account_balance
        response = render(request, template, context=dict(form=DepositForm(), current_amount=current_amount, diff_amount = diff_amount))
    elif request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            customer.account_balance += form.cleaned_data['balance']
            customer.save()
            response = HttpResponse(status=303)
            response['Location'] = '/finance/depositmoney/'
        else:
            response = render(request, template, context=dict(form=form))
    return response