from django.shortcuts import render

template = 'useraccountmanagement/password_recovery.html'

def passwordrecovery(request):
    if 'user_name' in request.session:
        pass
    elif request.method == 'GET':
        response = render(request, template)
    return response
