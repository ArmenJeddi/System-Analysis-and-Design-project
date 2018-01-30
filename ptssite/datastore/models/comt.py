from django.db import models
from . import user, customer

class Comment(models.Model):
    commenter = models.ForeignKey(to=customer.Customer,
                                  on_delete=models.CASCADE,
                                  related_name="from_comment_set",
                                  verbose_name="نظر دهنده")
    undercomment = models.ForeignKey(to=user.User,
                                     on_delete=models.CASCADE,
                                     related_name="to_comment_set",
                                     verbose_name="نظر گیرنده")
    content = models.TextField(verbose_name="نظر")

    date = models.DateField(verbose_name= "تاریخ ثبت", null=False)