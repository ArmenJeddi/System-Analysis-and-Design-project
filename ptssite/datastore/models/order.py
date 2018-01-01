from django.db import models
from . import customer, prodsub, driver

class Order(models.Model):
    buyer = models.ForeignKey(to=customer.Customer,
                              on_delete=models.CASCADE,
                              verbose_name="خریدار")
    product = models.ForeignKey(to=prodsub.ProductSubmit,
                                on_delete=models.CASCADE,
                                verbose_name="محصول")
    driver = models.ForeignKey(to=driver.Driver,
                               on_delete=models.CASCADE,
                               verbose_name="راننده")
    quantity = models.PositiveIntegerField(verbose_name="مقدار سفارش")
    location = models.TextField(verbose_name="آدرس خریدار")
    final = models.BooleanField(verbose_name="سفارش نهایی", default=False)
    driver_receipt = models.BooleanField(verbose_name="تحویل راننده",
                                         default=False)
    buyer_receipt = models.BooleanField(verbose_name="تحویل خریدار",
                                        default=False)
    driver_rating = models.PositiveSmallIntegerField(verbose_name=\
                                                     "امتیاز راننده")
    seller_rating = models.PositiveSmallIntegerField(verbose_name=\
                                                     "امتیاز فروشنده")
