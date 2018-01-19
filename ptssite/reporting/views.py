from django.shortcuts import render
from django.http import HttpResponse

def listbuyers(request):
    if request.method == 'GET':
        return render(request, 'reporting/listbuyers.html')

def listdrivers(request):
    if request.method == 'GET':
        return render(request, 'reporting/listdrivers.html')

def listfarmers(request):
    if request.method == 'GET':
        return render(request, 'reporting/listfarmers.html')

def listorders(request):
    if request.method == 'GET':
        return render(request, 'reporting/listorders.html')

def listproducts(request):
    if request.method == 'GET':
        return render(request, 'reporting/listproducts.html')

def listpurchases(request):
    if request.method == 'GET':
        return render(request, 'reporting/listpurchases.html')

def listtransports(request):
    if request.method == 'GET':
        return render(request, 'reporting/listtransports.html')
