from django.shortcuts import render, redirect, get_object_or_404
from ..forms.browseForm import BrowseForm
from datastore.models.product import Product
from datastore.models.prodsub import ProductSubmit
from datastore.models.driver import Driver
import random
from authentication.decorators import customer_required

def browseProduct(request):
    print('in browse')
    print(dict(request.session))
    if request.method == "POST":
        d = dict(request.POST)
        allSubmitted = ProductSubmit.objects.all()
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
@customer_required
def selectProduct(request, select_id):
    sp = ProductSubmit.objects.get(pk=select_id)
    if request.method == "POST":
        print('in select Product')
        print(dict(request.POST))
        select_quantity = int(request.POST['rangeInput'])
        request.session['selected_product']= select_id
        request.session['selected_quantity'] = select_quantity
        ### this will change --> prob : we should not delete
        new_quantity = sp.quantity - select_quantity
        sp.quantity -= select_quantity
        sp.save()
        return redirect('tradeproduct:selectDriver')

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
    for driver in drivers:
        cost_drive = compute_cost(driver, product)
        mapping.append((driver, cost_drive, driver.rate))

    if option == 1:
        mapping.sort(key=lambda tup: tup[1])
    elif option == 2:
        mapping.sort(key=lambda tup: tup[1], reverse=True)
    else:
        mapping.sort(key=lambda tup: tup[2], reverse=True)

    return mapping
@customer_required
def selectDriver(request):
    if (not 'selected_product' in request.session) or (not 'selected_quantity' in request.session):
        # notification
        return redirect('tradeproduct:browse')

    chosen_capacity = request.session['selected_quantity']
    chosenP = get_object_or_404(ProductSubmit, pk=request.session['selected_product'])
    province = chosenP.province

    drivers = Driver.objects.all()
    available_drivers = []
    for driver in drivers:
        if driver.availability:
            if driver.vehicle_capacity >= chosen_capacity:
                if province in driver.province_list_keys():
                    available_drivers.append(driver)

    if request.method == 'POST':
        print('HI')
        print(request.POST)

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

@customer_required
def driver_details(request, username):
    driver = get_object_or_404(Driver, pk=username)
    return render(request, 'tradeproduct/driver_details.html', {'driver': driver})

@customer_required
def confirmIt(request, username):
    print('in confirm it')
    print(dict(request.session))
    if (not 'selected_product' in request.session) or (not 'selected_quantity' in request.session):
        #notification
        return redirect('tradeproduct:browse')

    driver = get_object_or_404(Driver, pk=username)
    driver.availability = False
    driver.save()
    request.session['driver_id'] = username
    product = get_object_or_404(ProductSubmit, pk=request.session['selected_product'])

    if request.method == 'POST':
        if 'order_confirm' in request.POST:
            # add some stuff to session
            # and call berjis
            None
        elif 'order_cancel' in request.POST:
            driver.availability = True
            driver.save()
            product.quantity += request.session['selected_quantity']
            product.save()
            request.session.pop('selected_product', None)
            request.session.pop('selected_quantity', None)
            request.session.pop('driver_id', None)
            return redirect('tradeproduct:browse')
    else:
        driver_cost = compute_cost(driver, product)
        product_cost = request.session['selected_quantity'] * product.price
        total_cost = driver_cost + product_cost
        return render(request, 'tradeproduct/confirm_order.html', {'driver': driver, 'product': product,
                                                              'quantity': request.session['selected_quantity'], 'cost': product_cost,
                                                              'driver_cost':driver_cost, 'total_cost': total_cost})
