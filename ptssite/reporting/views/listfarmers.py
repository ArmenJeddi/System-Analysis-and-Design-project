from django.shortcuts import render
from django.http import HttpResponse

def listfarmers(request):
    if request.method == 'GET':
        return render(request, 'reporting/listfarmers.html')