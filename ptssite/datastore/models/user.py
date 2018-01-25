from django.db import models
from django.core import validators

name_validator = [validators.RegexValidator(regex=r'\A[ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیءٔ‌ٰٓكةآأإيئؤًٌٍَُِّْ ]+\Z',
                                            message='تنها از الفبای فارسی استفاده کنید',
                                            code='invalid_name')]
id_validator = [validators.RegexValidator(regex=r'\A[0-9۰۱۲۳۴۵۶۷۸۹]{10}\Z',
                                          message='تنها از اعداد استفاده کنید',
                                          code='invalid_national_id')]
phone_validator = [validators.RegexValidator(regex=r'\A[0۰][0-9۰۱۲۳۴۵۶۷۸۹]{10}\Z',
                                             message='شماره تلفن همراه باید شبیه ۰۹۱۱۱۱۱۱۱۱۱ باشد',
                                             code='invalid_phone_number')]
account_validator = [validators.RegexValidator(regex=r'\A[0-9۰۱۲۳۴۵۶۷۸۹]{16}\Z',
                                               message='شماره کارت بانکی باید شبیه ۱۱۱۱۱۱۱۱۱۱۱۱۱۱۱۱ باشد',
                                               code='invalid_account_number')]
num_tab = str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹')

class AnonymousUser:

    def is_anonymous(self):
        return True

    def is_authenticated(self):
        return False
    
class User(models.Model):
    username = models.CharField(max_length=200,
                                 primary_key=True,
                                 verbose_name="نام کاربری",
                                 error_messages={
                                     'unique': 'نام کاربری استفاده شده قبلا در سیستم ثبت شده است'
                                 })
    password = models.CharField(max_length=200,
                                verbose_name="گذرواژه")
    first_name = models.CharField(max_length=20,
                                  verbose_name="نام",
                                  validators=name_validator)
    last_name = models.CharField(max_length=20,
                                 verbose_name="نام خانوادگی",
                                 validators=name_validator)
    phone_number = models.CharField(max_length=11,
                                    verbose_name="شماره تلفن همراه",
                                    validators=phone_validator)
    def clean(self):
        self.phone_number = self.phone_number.translate(num_tab)

    def __str__(self):
        fullname = self.first_name + " " + self.last_name
        return fullname

    def is_unprivileged(self):
        return hasattr(self, 'unprivilegeduser')

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

class UnprivilegedUser(User):
    national_id = models.CharField(max_length=10,
                                   verbose_name="کد ملی",
                                   validators=id_validator)
    banned = models.BooleanField(verbose_name="ممنوعیت استفاده از سامانه",
                                 default=False)
    account_number = models.CharField(max_length=16,
                                      verbose_name="شماره کارت",
                                      validators=account_validator)

    def clean(self):
        super().clean()
        self.national_id = self.national_id.translate(num_tab)
        self.account_number = self.account_number.translate(num_tab)

    def is_driver(self):
        return hasattr(self, 'driver')

    def is_customer(self):
        return hasattr(self, 'customer')
