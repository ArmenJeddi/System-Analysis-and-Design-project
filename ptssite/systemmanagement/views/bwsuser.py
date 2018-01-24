from django.views.generic.list import ListView
from datastore.models import User
from django.http import HttpResponseForbidden

class BrowseUsers(ListView):
    
    model = User
    context_object_name = 'users'
    template_name = 'browseusers.html'

    def get(self, request, *args, **kwargs):
        role = request.session.get('role')
        if role == 'admin':
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
