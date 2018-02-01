from django.shortcuts import render, redirect, get_object_or_404
from ..forms.browseForm import BrowseForm
from datastore.models.product import Product
from datastore.models.prodsub import ProductSubmit
from datastore.models.driver import Driver
from datastore.models.order import Order

import datetime
import random
from authentication.decorators import customer_required
from convertdate import persian

def browseProduct(request):
    if request.method == "POST":
        d = dict(request.POST)

        from_ = request.POST['from']
        to_ = request.POST['to']

        lower_bound = 0
        if len(from_) > 0:
            lower_bound = int(from_)

        upper_bound = -1
        if len(to_) > 0:
            upper_bound = int(to_)

        allSubmitted = ProductSubmit.objects.all()
        filtered = []

        for prod in allSubmitted:
            if prod.price >= lower_bound:
                if upper_bound > -1:
                    if prod.price <= upper_bound:
                        filtered.append(prod)
                else:
                    filtered.append(prod)

        searchResult = []

        print(d)

        if 'province' in d.keys():
            for prod in filtered:
                if prod.product.__str__() == d['product'][0] and prod.active:
                    if prod.province in d['province']:
                        searchResult.append(prod)
        else:
            for prod in filtered:
                if prod.product.__str__() == d['product'][0] and prod.active:
                    searchResult.append(prod)

        my_template = "navbar.html"
        if request.user.is_authenticated():
            my_template = "navbar_signedin.html"
        return render(request, 'tradeproduct/searchResult.html', {'searchResult': searchResult, 'mytemplate': my_template})

    else:
        productList = []
        for prod in Product.objects.all():
            productList.append((prod.pk , prod.name))
        form = BrowseForm(productList)

        browse_notify = False
        if 'browse_notif' in request.session:
            browse_notify = True
            request.session.pop('browse_notif', None)

        my_template = "navbar.html"
        if request.user.is_authenticated():
            my_template ="navbar_signedin.html"

        return render(request, 'tradeproduct/browse.html', {'form':form, 'my_template': my_template, 'browse_notify': browse_notify})

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
        sp.quantity -= select_quantity
        sp.save()
        return redirect('tradeproduct:selectDriver')

    else:
        if ('selected_product' in request.session) or ('selected_quantity' in request.session):
            request.session['print_driver_notification'] = 1
            return redirect('tradeproduct:selectDriver')
        if sp.quantity % 2 == 0:
            half = int(sp.quantity / 2)
        else:
            half = int((sp.quantity+1) / 2)

        return render(request, 'tradeproduct/selectProduct.html', {'selectedProduct': sp, 'halfvalue': half, 'activiate': sp.active })

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
        request.session['browse_notif'] = 1
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

        if 'reject_and_browse_again' in request.POST:
            chosenP.quantity += request.session['selected_quantity']
            chosenP.save()
            request.session.pop('selected_product', None)
            request.session.pop('selected_quantity', None)
            return redirect('tradeproduct:browse')

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
        return render(request, 'tradeproduct/driver_list.html', {'driverMap': mapped_driver, 'option': option,
                                                                 'select_value': select_value})
    else:
        driver_notif = False
        if 'print_driver_notification' in request.session:
            driver_notif = True
            request.session.pop('print_driver_notification', None)
        mapped_driver = getMap(available_drivers, chosenP, option = 1)
        return render(request, 'tradeproduct/driver_list.html', {'driverMap': mapped_driver, 'option':1,
                                                                 'select_value' : 'قیمت صعودی', 'driver_notif': driver_notif})


@customer_required
def driver_details(request, username):
    if (not 'selected_product' in request.session) or (not 'selected_quantity' in request.session):
        request.session['browse_notif'] = 1
        return redirect('tradeproduct:browse')
    driver = get_object_or_404(Driver, pk=username)
    return render(request, 'tradeproduct/driver_details.html', {'driver': driver})

@customer_required
def confirmIt(request, username):

    if (not 'selected_product' in request.session) or (not 'selected_quantity' in request.session):
        request.session['browse_notif'] = 1
        return redirect('tradeproduct:browse')
    print('in confirm it')
    print(dict(request.session))

    driver = get_object_or_404(Driver, pk=username)
    driver.availability = False
    driver.save()
    request.session['driver_id'] = username
    product = get_object_or_404(ProductSubmit, pk=request.session['selected_product'])

    prod_tarikh = product.date
    tarikh = persian.from_gregorian(prod_tarikh.year, prod_tarikh.month, prod_tarikh.day)
    driver_cost = compute_cost(driver, product)
    product_cost = request.session['selected_quantity'] * product.price
    total_cost = driver_cost + product_cost

    buyer = request.user.unprivilegeduser.customer
    if request.method == 'POST':
        if 'order_confirm' in request.POST:
            if total_cost > buyer.account_balance:
                request.session['diff_amount'] = total_cost - buyer.account_balance
                return redirect('finance:deposit')

            buyer.account_balance -= total_cost
            new_order = Order(buyer = buyer, product = product, driver = driver, quantity = request.session['selected_quantity'],
                              driver_cost = driver_cost, location = request.POST['buyer_address'], date = datetime.date.today() )
            new_order.save()
            request.session.pop('selected_product', None)
            request.session.pop('selected_quantity', None)
            request.session.pop('driver_id', None)
            print(dict(request.session))
            return redirect('reporting:listpurchases')

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
        return render(request, 'tradeproduct/confirm_order.html', {'driver': driver, 'product': (product, tarikh),
                                                              'quantity': request.session['selected_quantity'], 'cost': product_cost,
                                                              'driver_cost':driver_cost, 'total_cost': total_cost,
                                                                   'balance': buyer.account_balance})
