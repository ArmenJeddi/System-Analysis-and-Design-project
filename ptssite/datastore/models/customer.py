from django.db import models
from . import user

class Customer(user.User):
    account_balance =  models.BigIntegerField(verbose_name="موجودی")
