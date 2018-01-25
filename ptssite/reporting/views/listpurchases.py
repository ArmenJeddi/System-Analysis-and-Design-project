from django.shortcuts import render
from django.http import HttpResponse

def listpurchases(request):
    if request.method == 'GET':
        return render(request, 'reporting/listpurchases.html')