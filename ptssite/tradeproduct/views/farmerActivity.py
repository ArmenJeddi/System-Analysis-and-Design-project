from django.shortcuts import render, redirect, get_object_or_404
from ..forms.tradeForm import SubmitForm
from datastore.models.product import Product
from datastore.models.prodsub import ProductSubmit
from django.utils import timezone

def submitProduct(request):
    if request.method == 'POST':
        form = SubmitForm(request.POST)
        if form.is_valid():
            subprod = form.save(commit=False)
            # subprod.submitter = ??
            subprod.date = timezone.now()
            # subprod.save()
            return redirect('/reporting/listproducts/')

    else:
        # if user is logged in and is a customer do following
        # if "user_name" in request.session:
        #     role = request.session['role']
        #
        form = SubmitForm()

    return render(request, 'tradeproduct/submitProduct.html', {'form':form})

def updateProducts(request):

    if request.method == 'POST':
        # reload the page
        # submittedList = ProductSubmit.objects.filter(submitter= ?)
        None
    else:
        # submittedList = ProductSubmit.objects.filter(submitter = ?)
        submittedList = ProductSubmit.objects.all()

    return render(request, 'tradeproduct/updateSubmittedProduct.html', {'submittedList': submittedList})

def submit_details(request, prodsub_id):
    subprod = get_object_or_404(ProductSubmit, pk=prodsub_id)
    return render(request, 'tradeproduct/submittedProduct_details.html', {'submittedProduct': subprod})

def delete_submittedProduct(request, delete_id):
    if request.method == "POST":
        ps = ProductSubmit.objects.get(pk=delete_id)
        ps.delete()
        # send a message that it was successfully deleted
        # submittedList = ProductSubmit.objects.filter(submitter = ?)
        submittedList = ProductSubmit.objects.all()
        return redirect('/tradeproduct/updateSubmittedProduct/')
    else:
        None
        # error

def change_details(request, change_id):
    if request.method == "POST":
        form = SubmitForm(request.POST)
        subprod = ProductSubmit.objects.get(pk=change_id)
        if form.data['quantity'] == '0':
            subprod.delete()
        else:
            subprod.quantity = form.data['quantity']
            subprod.location = form.data['location']
            subprod.price = form.data['price']
            subprod.date = timezone.now()
            subprod.save()

        submittedList = ProductSubmit.objects.all()
        return redirect('/tradeproduct/updateSubmittedProduct/', {'submittedList': submittedList})

    else:
        # if user is logged in and is a customer do following
        subprod = get_object_or_404(ProductSubmit, pk=change_id)
        form = SubmitForm(instance=subprod)
        form.fields['product'].widget.attrs['disabled'] = 'disabled'
        form.fields['province'].widget.attrs['disabled'] = 'disabled'
        return render(request, 'tradeproduct/change_details.html', {'form': form, 'subp_id': change_id})