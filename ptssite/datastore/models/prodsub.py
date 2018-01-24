from django.db import models
from . import product, customer

class ProductSubmit(models.Model):
    submitter = models.ForeignKey(to=customer.Customer,
                                  on_delete=models.CASCADE,
                                  verbose_name="فروشنده")
    product = models.ForeignKey(to=product.Product,
                                on_delete=models.CASCADE,
                                verbose_name="نوع محصول")
    date = models.DateTimeField(verbose_name="تاریخ ثبت")
    quantity = models.PositiveIntegerField(verbose_name="مقدار محصول")
    price = models.PositiveIntegerField(verbose_name="قیمت")
    location = models.TextField(verbose_name="آدرس فروشنده")

    def __str__(self):
        fullname = self.submitter.first_name + self.submitter.last_name
        pr = self.product.name
        return pr + " توسط " + fullname
