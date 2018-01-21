from django.db import models
from . import customer

class Product(models.Model):
    name = models.CharField(max_length=20, primary_key=True,
                     verbose_name="نوع محصول")

