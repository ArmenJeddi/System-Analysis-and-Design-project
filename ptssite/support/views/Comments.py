from django.shortcuts import render, redirect, get_object_or_404

from datastore.models.ordre import Order

def commentOnFarmer(request, order_id):

    rel_order = Order.objects.get(pk = order_id)

    if request.method == 'POST':
        None
    else:
        farmer = rel_order.product.submitter
        return render(request, 'tradeproduct/commentOnFarmer.html', {'order': rel_order})
