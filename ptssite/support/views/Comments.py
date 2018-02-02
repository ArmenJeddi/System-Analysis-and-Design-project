from django.shortcuts import render, redirect, get_object_or_404

from datastore.models.order import Order
from datastore.models.comt import Comment
from datastore.models.driver import alpha

from authentication.decorators import customer_required
import datetime

@customer_required
def commentOnFarmer(request, order_id):

    rel_order = get_object_or_404(Order, pk = order_id)

    if request.method == 'POST':
        comment = Comment(commenter = request.user.unprivilegeduser.customer, undercomment = rel_order.product.submitter, content = request.POST['comment'],
                          date = datetime.datetime.today(),
                          order_id = rel_order)
        comment.save()
        return redirect('reporting:listpurchases')
    else:
        this_user = request.user.unprivilegeduser.customer
        this_user_comments = Comment.objects.filter(commenter = this_user, undercomment = rel_order.product.submitter, order = rel_order)
        length_u_c = len(this_user_comments)
        return render(request, 'support/commentOnFarmer.html', {'order': rel_order, 'length': length_u_c})

@customer_required
def commentOnDriver(request, order_id):
    rel_order = get_object_or_404(Order, pk = order_id)
    if request.method == 'POST':
        comment = Comment(commenter=request.user.unprivilegeduser.customer, undercomment=rel_order.driver,
                          content=request.POST['comment'],
                          date=datetime.datetime.today(),
                          order_id = rel_order)
        comment.save()
        rate = int(request.POST['rate'])
        print('before: ',rel_order.driver.rate)
        rel_order.driver.rate = (1 - alpha) * rel_order.driver.rate + alpha * rate
        rel_order.driver.save()
        print('after: ', rel_order.driver.rate)

        return redirect('reporting:listpurchases')
    else:
        this_user = request.user.unprivilegeduser.customer
        this_user_comments = Comment.objects.filter(commenter = this_user, undercomment = rel_order.driver, order = rel_order)
        length_u_c = len(this_user_comments)
        print(length_u_c)
        return render(request, 'support/commentOnDriver.html', {'order': rel_order, 'length': length_u_c})

