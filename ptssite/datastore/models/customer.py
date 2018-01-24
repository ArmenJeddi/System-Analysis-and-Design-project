from django.db import models
from . import user

class Customer(user.UnprivilegedUser):
    account_balance =  models.BigIntegerField(verbose_name="موجودی",
                                              default=0)
