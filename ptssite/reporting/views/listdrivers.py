from django.shortcuts import render
from django.http import HttpResponse

def listdrivers(request):
    if request.method == 'GET':
        return render(request, 'reporting/listdrivers.html')