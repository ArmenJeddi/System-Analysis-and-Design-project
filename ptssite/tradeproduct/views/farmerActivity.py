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
            return redirect('/reporting/listproducts/')

    else:
        # if user is logged in and is a customer do following
        form = SubmitForm()

    return render(request, 'tradeproduct/submitProduct.html', {'form':form})

def removeProduct(request):

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