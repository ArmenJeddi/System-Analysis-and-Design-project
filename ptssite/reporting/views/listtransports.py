from django.shortcuts import render
from django.http import HttpResponse

def listtransports(request):
    if request.method == 'GET':
        return render(request, 'reporting/listtransports.html')