from django.shortcuts import render, redirect, get_object_or_404

from datastore.models.order import Order
from datastore.models.comt import Comment

from authentication.decorators import customer_required

@customer_required
def commentOnFarmer(request, order_id):

    rel_order = get_object_or_404(Order, pk = order_id)

    if request.method == 'POST':
        None
    else:
        this_user = request.user.unprivilegeduser.customer
        this_user_comments = Comment.objects.filter(commenter = this_user, undercomment = rel_order.product.submitter)
        length_u_c = len(this_user_comments)
        return render(request, 'tradeproduct/commentOnFarmer.html', {'order': rel_order, 'length': length_u_c})

@customer_required
def commentOnDriver(request, order_id):
    rel_order = get_object_or_404(Order, pk = order_id)
    if request.method == 'POST':
        None
    else:
        this_user = request.user.unprivilegeduser.customer
        this_user_comments = Comment.objects.filter(commenter = this_user, undercomment = rel_order.driver)
        length_u_c = len(this_user_comments)
        return render(request, 'tradeproduct/commentOnDriver.html', {'order': rel_order, 'length': length_u_c})

