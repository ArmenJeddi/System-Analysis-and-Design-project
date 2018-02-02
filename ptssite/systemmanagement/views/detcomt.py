from django.views.generic.edit import DeleteView
from authentication.mixins import PrivilegedRequired
from datastore.models import Comment
from convertdate import persian

num_tab = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')

class DetailCommentView(PrivilegedRequired, DeleteView):
    template_name = 'systemmanagement/detail_comment.html'
    model = Comment
    context_object_name = 'comment'
    success_url = '/systemmanagement/browsecomments/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment = context[self.context_object_name]
        date = persian.from_gregorian(comment.date.year,
                                      comment.date.month,
                                      comment.date.day)
        comment.date_str = (str(date[0]) + '/' + str(date[1]) + '/'
                            + str(date[2])).translate(num_tab)
        return context
