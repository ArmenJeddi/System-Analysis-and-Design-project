from django.shortcuts import render
from django.http import HttpResponse
from datastore.models import Driver, ProductSubmit, Order
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from authentication.decorators import privileged_required

@privileged_required(login_url="/systemmanagement/login/")
def listdrivers(request):
    if request.method == 'GET':
        
        driver_list = Driver.objects.all()
        page = request.GET.get('page')

        paginator = Paginator(driver_list, 2)
        try:
            drivers = paginator.get_page(page)
        except PageNotAnInteger:
            drivers = paginator.get_page(1)
        except EmptyPage:
            drivers = paginator.get_page(paginator.num_pages)

        return render(request, 'reporting/listdrivers.html', { 'drivers': drivers })