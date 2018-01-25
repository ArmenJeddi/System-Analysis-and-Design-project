from django.shortcuts import render
from django.http import HttpResponse

def listorders(request):
    if request.method == 'GET':
        return render(request, 'reporting/listorders.html')