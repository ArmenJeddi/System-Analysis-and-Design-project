from datastore.models.user import AnonymousUser, User

class AuthenticationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        try:
            user = User.objects.get(pk=request.session['username'])
        except(User.DoesNotExist, KeyError):
            request.user = AnonymousUser()
        else:
            if user.is_unprivileged() and user.banned:
                request.user = AnonymousUser()
            else:
                request.user = user

        return self.get_response(request)
