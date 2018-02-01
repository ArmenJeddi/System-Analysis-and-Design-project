from django.shortcuts import render
from django.http import HttpResponse
from datastore.models import ProductSubmit
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from authentication.decorators import privileged_required

@privileged_required(login_url="/systemmanagement/login/")
def listfarmers(request):
    if request.method == 'GET':
        
        farmer_list = ProductSubmit.objects.values_list("submitter", flat=True).distinct()
        product_list = ProductSubmit.objects.filter(submitter__in=farmer_list)
        
        set_seen = {}
        lst_result = []
     
        for product in product_list:
            if product.submitter in set_seen:
                continue
            set_seen[product.submitter] = 1
            lst_result.append(product)
     
        temp_list = lst_result
        product_list = [[0 for x in range(2)] for y in range(len(temp_list))]
        for i in range(0, len(temp_list)):
            product_list[i][0] = i + 1
            product_list[i][1] = temp_list[i]
        page = request.GET.get('page')

        paginator = Paginator(product_list, 2)
        try:
            products = paginator.get_page(page)
        except PageNotAnInteger:
            products = paginator.get_page(1)
        except EmptyPage:
            products = paginator.get_page(paginator.num_pages)
        return render(request, 'reporting/listfarmers.html', { 'products': products })