from django.http import HttpResponse
from django.shortcuts import render

def depositmoney(request):
    if request.method == 'GET':
        return render(request, 'finance/depositmoney.html')
