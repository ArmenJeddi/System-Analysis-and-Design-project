from django.shortcuts import render
from django.http import HttpResponse

def listproducts(request):
    if request.method == 'GET':
        return render(request, 'reporting/listproducts.html')