from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponseNotAllowed

driver_template = 'useraccountmanagement/profile_driver.html'
customer_template = 'useraccountmanagement/profile_customer.html'

def profile(request):
    if request.method == 'GET':
        role = request.session.get('role')
        if role == 'driver':
            return render(request, driver_template)
        elif role == 'customer':
            return render(request, customer_template)
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseNotAllowed(['GET'])
