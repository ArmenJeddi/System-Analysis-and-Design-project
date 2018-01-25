from django.shortcuts import render
from django.http import HttpResponse

def listbuyers(request):
    if request.method == 'GET':
        return render(request, 'reporting/listbuyers.html')