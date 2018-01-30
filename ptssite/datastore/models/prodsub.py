from django.db import models
from . import product, customer
from .driver import provinces

class ProductSubmit(models.Model):
    submitter = models.ForeignKey(to=customer.Customer,
                                  on_delete=models.CASCADE,
                                  verbose_name="فروشنده")
    product = models.ForeignKey(to=product.Product,
                                on_delete=models.CASCADE,
                                verbose_name="نوع محصول")
    date = models.DateField(verbose_name= "تاریخ ثبت", null=False)
    quantity = models.PositiveIntegerField(verbose_name="مقدار محصول", null=False)
    price = models.PositiveIntegerField(verbose_name="قیمت", null=False)
    province = models.CharField(max_length=30, choices=provinces, verbose_name="استان", null=False, default='tehran')
    location = models.TextField(verbose_name="آدرس فروشنده", null=False)

    def __str__(self):
        fullname = self.submitter.first_name + self.submitter.last_name
        pr = self.product.name
        return pr + " توسط " + fullname
