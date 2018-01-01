from django.db import models
from . import user

class Driver(user.User):
    certificate_number = models.CharField(max_length=20,
                                   verbose_name="شماره گواهینامه")
    rate = models.PositiveSmallIntegerField(verbose_name="امتیاز")
    availability = models.BooleanField(default=False,
                                       verbose_name="آمادگی برای انتقال")
