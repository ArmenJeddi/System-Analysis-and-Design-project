from django.shortcuts import render
from datastore.models import User, Driver, Customer

temp_driv = 'useraccountmanagement/settings_driver.html'
temp_cust = 'useraccountmanagement/settings_customer.html'

def updateprofile(request):
    if request.method == 'GET':
        if 'role' in request.session:
            if request.session['role'] == 'driver':
                response = render(request, temp_driv)
            else:
                response = render(request, temp_cust)
        else:
            pass
    elif request.method == 'POST':
        pass
    return response
