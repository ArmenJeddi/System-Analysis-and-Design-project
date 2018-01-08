from django.http import HttpResponse
from django.shortcuts import render

def login(request):
    if 'user_name' in request.session:
        return HttpResponse()
    if request.method == 'GET':
        return render(request, 'useraccountmanagement/login.html')
