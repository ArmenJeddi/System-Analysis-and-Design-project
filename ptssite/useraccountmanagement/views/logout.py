from django.shortcuts import render

template =''

def logout(request):
    request.session.flush()
    #return render(request, template)
    raise NotImplementedError
