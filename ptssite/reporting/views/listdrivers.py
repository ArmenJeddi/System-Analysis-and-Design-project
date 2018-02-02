from django.shortcuts import render
from django.http import HttpResponse
from datastore.models import Driver, ProductSubmit, Order
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from authentication.decorators import privileged_required

@privileged_required(login_url="/systemmanagement/login/")
def listdrivers(request):
    if request.method == 'GET':
        
        temp_list = Driver.objects.all()
        if request.GET.get('search'):
            temp_list = temp_list.filter(username__contains = request.GET.get('search'))
        driver_list = [[0 for x in range(2)] for y in range(len(temp_list))]
        for i in range(0, len(temp_list)):
            driver_list[i][0] = i + 1
            driver_list[i][1] = temp_list[i]
        page = request.GET.get('page')

        paginator = Paginator(driver_list, 2)
        try:
            drivers = paginator.get_page(page)
        except PageNotAnInteger:
            drivers = paginator.get_page(1)
        except EmptyPage:
            drivers = paginator.get_page(paginator.num_pages)

        return render(request, 'reporting/listdrivers.html', { 'drivers': drivers })