from datastore.models.user import AnonymousUser, User

class AuthenticationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        try:
            request.user = User.objects.get(pk=request.session['username'])
        except(User.DoesNotExist, KeyError):
            request.user = AnonymousUser()

        return self.get_response(request)
