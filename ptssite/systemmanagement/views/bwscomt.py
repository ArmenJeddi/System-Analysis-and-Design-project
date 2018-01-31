from django.views.generic.list import ListView
from authentication.mixins import PrivilegedRequired
from datastore.models import Comment

class BrowseCommentsView(PrivilegedRequired, ListView):
    template_name = 'systemmanagement/browse_comments.html'

    def get_queryset(self):
        params = self.request.GET
        comments = Comment.objects.all()
        kwargs = {}

        undercomment = params.get('undercomment')
        if undercomment:
            kwargs['undercomment__first_name__contains'] = undercomment
            kwargs['undercomment__last_name__contains'] = undercomment

        commenter = params.get('commenter')
        if commenter:
            kwargs['commenter__first_name__contains'] = commenter
            kwargs['commenter__last_name__contains'] = commenter

        
