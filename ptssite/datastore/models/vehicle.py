from django.db import models
from . import driver

class Vehicle(models.Model):
    driver = models.OneToOneField(to=driver.Driver,
                                  on_delete=models.CASCADE,
                                  primary_key=True,
                                  verbose_name="راننده")
    model = models.CharField(max_length=50,
                             verbose_name="نوع وسیله نقلیه")
    number = models.CharField(max_length=20,
                              verbose_name="شماره ماشین")
    capacity = models.CharField(max_length=5,
                                verbose_name="ظرفیت")
