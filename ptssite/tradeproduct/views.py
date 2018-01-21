from django.shortcuts import render
from .forms.tradeForm import SubmitForm

# Create your views here.

def submitProduct(request):
    if request.method == 'POST':
        None
    else:
        # user = request.session['user_name']
        # if user is logged in and is a customer do following
        form = SubmitForm()

        return render(request, 'tradeproduct/submitProduct.html', {'form':form})