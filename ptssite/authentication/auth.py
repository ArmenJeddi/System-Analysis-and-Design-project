from datastore.models import User

def login(request, user):
    request.session['username'] = user.username

def logout(request):
    request.session.flush()

def authenticate(username, password):
    try:
        user = User.objects.get(pk=username)
        if user.password == password and\
           not (user.is_unprivileged() and user.unprivileged.banned):
            return user
    except(User.DoesNotExist):
        pass
        
    return None
