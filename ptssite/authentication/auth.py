from datastore.models import User

def login(request, user):
    try:
        request.session['username'] = user.username
    except:
        pass

def logout(request):
    try:
        request.session.flush()
    except:
        pass

def authenticate(username, password):
    try:
        user = User.objects.get(pk=username)
        if user.password == password and\
           not (user.is_unprivileged() and user.unprivilegeduser.banned):
            return user
    except(User.DoesNotExist):
        pass
        
    return None
