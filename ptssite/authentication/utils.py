from datastore.models import User

def login(request, user):
    request.session['username'] = user.username

def logout(request):
    request.session.flush()
