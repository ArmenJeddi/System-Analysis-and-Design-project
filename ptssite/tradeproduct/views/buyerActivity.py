from django.shortcuts import render, redirect, get_object_or_404
from ..forms.browseForm import BrowseForm
from datastore.models.product import Product
from datastore.models.prodsub import ProductSubmit
from datastore.models.driver import Driver
import random

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
    sp = ProductSubmit.objects.get(pk=select_id)
    if request.method == "POST":
        select_quantity = int(request.POST['rangeInput'])
        print(select_quantity)

        ### this will change --> prob : we should not delete
        new_quantity = sp.quantity - select_quantity
        if new_quantity == 0:
            sp.delete()
        else:
            sp.quantity = new_quantity
            sp.save()
        id_cap = str(select_id) + '_' + str(select_quantity)
        return redirect('tradeproduct:selectDriver', chosenID_cap = id_cap)

    else:
        if sp.quantity % 2 == 0:
            half = int(sp.quantity / 2)
        else:
            half = int((sp.quantity+1) / 2)

        return render(request, 'tradeproduct/selectProduct.html', {'selectedProduct': sp, 'halfvalue': half })

def compute_cost(driver, product):
    return random.randint(50,300)

def getMap(drivers, product, option = 1):
    mapping = []
    if option < 3:
        for driver in drivers:
            cost_drive = compute_cost(driver, product)
            mapping.append((driver, cost_drive))

        if option == 1:
            mapping.sort(key=lambda tup: tup[1])
        else:
            mapping.sort(key=lambda tup: tup[1], reverse=True)

    else:
        mapping = []
        for driver in drivers:
            mapping.append((driver, driver.rate))
        mapping.sort(key=lambda tup: tup[1], reverse=True)

    return mapping

def selectDriver(request, chosenID_cap):
    chosen_prodict_id = int(chosenID_cap[:chosenID_cap.index('_')])
    chosen_capacity = int(chosenID_cap[chosenID_cap.index('_') + 1:])
    chosenP = ProductSubmit.objects.get(pk=chosen_prodict_id)
    province = chosenP.province

    drivers = Driver.objects.all()
    available_drivers = []
    for driver in drivers:
        if driver.availability:
            if driver.vehicle_capacity >= chosen_capacity:
                if province in driver.province_list_keys():
                    available_drivers.append(driver)

    if request.method == 'POST':
        option = int(request.POST['rule_select'])
        mapped_driver = getMap(available_drivers, chosenP, option=option)
        print(option)
        if option == 1:
            select_value = 'قیمت صعودی'
        elif option == 2:
            select_value = 'قیمت نزولی'
        else:
            select_value = 'امتیاز'
        print(select_value)
        return render(request, 'tradeproduct/driver_list.html', {'driverMap': mapped_driver, 'option': option, 'select_value': select_value})
    else:
        mapped_driver = getMap(available_drivers, chosenP, option = 1)
        return render(request, 'tradeproduct/driver_list.html', {'driverMap': mapped_driver, 'option':1, 'select_value' : 'قیمت صعودی'})