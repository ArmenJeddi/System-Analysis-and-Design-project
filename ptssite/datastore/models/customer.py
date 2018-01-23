from django.db import models
from . import user

class Customer(user.User):
    account_balance =  models.BigIntegerField(verbose_name="موجودی",
                                              default=0)

    def __str__(self):
        fullname = self.first_name + " " + self.last_name
        return fullname