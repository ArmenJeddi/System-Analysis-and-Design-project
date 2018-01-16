from django.http import HttpResponse
from django.shortcuts import render

def depositmoney(request):
    if request.method == 'GET':
        return render(request, 'finance/depositmoney.html')

def payorder(request):
    if request.method == 'GET':
        return render(request, 'finance/payorder.html')
        
def listorders(request):
    if request.method == 'GET':
        return render(request, 'finance/listorders.html')
        