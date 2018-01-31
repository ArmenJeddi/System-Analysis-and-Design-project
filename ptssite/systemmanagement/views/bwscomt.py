from django.views.generic.list import ListView
from authentication.mixins import PrivilegedRequired
from datastore.models import Comment
import re
from convertdate import persian
from datetime import date

num_tab = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'),\
          str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
num_reg = re.compile(r'[0-9۰۱۲۳۴۵۶۷۸۹]+')
date_reg = re.compile(r'[0-9۰۱۲۳۴۵۶۷۸۹]{4}/[0-9۰۱۲۳۴۵۶۷۸۹]{1,2}/[0-9۰۱۲۳۴۵۶۷۸۹]{1,2}')

class BrowseCommentsView(PrivilegedRequired, ListView):
    template_name = 'systemmanagement/browse_comments.html'
    context_object_name = 'comments'

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

        date_start = params.get('date_start')
        if date_start and re.fullmatch(date_reg, date_start):
            year, month, day = start_date.translate(num_tab[1]).split('/')
            kwargs['date__gte'] = date(*persian.to_gregorian(int(year),
                                                             int(month),
                                                             int(day)))
        date_end = params.get('date_end')
        if date_end and re.fullmatch(date_reg, date_end):
            year, month, day = start_date.translate(num_tab[1]).split('/')
            kwargs['date__lte'] = date(*persian.to_gregorian(int(year),
                                                             int(month),
                                                             int(day)))

        keyword = params.get('keyword')
        if keyword:
            kwargs['content__contains'] = keyword

        if kwargs:
            comments = comments.filter(**kwargs)

        for comment in comments:
            date = persian.from_gregorian(comment.date.year,
                                          comment.date.month,
                                          comment.date.day)
            comment.date_str = (str(date[0]) + '/' + str(date[1]) + '/'
                                + str(date[2])).translate(num_tab[0])

        return comments
