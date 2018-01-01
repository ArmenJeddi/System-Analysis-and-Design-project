from django.db import models

class User(models.Model):
    user_name = models.CharField(max_length=20,
                                 primary_key=True,
                                 verbose_name="نام کاربری")
    password = models.CharField(max_length=20,
                                verbose_name="رمز عبور")
    first_name = models.CharField(max_length=20,
                                  verbose_name="نام")
    last_name = models.CharField(max_length=20,
                                 verbose_name="نام خانوادگی")
    national_id = models.CharField(max_length=10,
                                   verbose_name="کد ملی",
                                   unique=True)
    phone_number = models.CharField(max_length=11,
                                    verbose_name="شماره تلفن همراه")
    banned = models.BooleanField(verbose_name="ممنوعیت استفاده از سامانه",
                                 default=False)
    account_number = models.CharField(max_length=16,
                                      verbose_name="شماره کارت")
