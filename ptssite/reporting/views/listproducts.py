from django.shortcuts import render
from django.http import HttpResponse
from datastore.models import Driver, ProductSubmit, Order
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from authentication.decorators import customer_required
from convertdate import persian

@customer_required
def listproducts(request):
    if request.method == 'GET':

        submittedList = ProductSubmit.objects.filter(submitter=request.user.unprivilegeduser.customer)
        list_with_dates = []
        for sp in submittedList:
            list_with_dates.append((sp, persian.from_gregorian(sp.date.year, sp.date.month, sp.date.day)))

        page = request.GET.get('page')

        paginator = Paginator(list_with_dates, 2)
        try:
            list_with_dates = paginator.get_page(page)
        except PageNotAnInteger:
            list_with_dates = paginator.get_page(1)
        except EmptyPage:
            list_with_dates = paginator.get_page(paginator.num_pages)

        return render(request, 'reporting/listproducts.html', { 'products': list_with_dates })