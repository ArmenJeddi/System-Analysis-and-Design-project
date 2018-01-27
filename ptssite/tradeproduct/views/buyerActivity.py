from django.shortcuts import render, redirect, get_object_or_404
from ..forms.browseForm import BrowseForm
from datastore.models.product import Product
from datastore.models.prodsub import ProductSubmit

def browseProduct(request):
    if request.method == "POST":
        d = dict(request.POST)
        print(request.POST)
        print(d)
        allSubmitted = ProductSubmit.objects.all()
        print('number : {}'.format(len(allSubmitted)))
        searchResult = []

        if 'province' in d.keys():
            for prod in allSubmitted:
                if prod.product.__str__() == d['product'][0]:
                    if prod.price < int(d['to'][0]) and prod.price > int(d['from'][0]):
                        if prod.province in d['province']:
                            searchResult.append(prod)
        else:
            for prod in allSubmitted:
                if prod.product.__str__() == d['product'][0]:
                    if prod.price < int(d['to'][0]) and prod.price > int(d['from'][0]):
                        searchResult.append(prod)

        return render(request, 'tradeproduct/searchResult.html', {'searchResult': searchResult})

    else:
        productList = []
        for prod in Product.objects.all():
            productList.append((prod.pk , prod.name))
        form = BrowseForm(productList)

        return render(request, 'tradeproduct/browse.html', {'form':form})

# must be logged in customer
def selectProduct(request, select_id):

    sp = ProductSubmit.objects.get(pk = select_id)

    return render(request, 'tradeproduct/selectProduct.html', {'selectedProduct': sp})
