from django.db import models
from djang.core import validators

max_account_number_length = 16
account_number_help = "شماره کارت به صورت <em>XXXX-XXXX-XXXX-XXXX</em>"
account_number_validators = []
english_digits_class = '[1234567890]'
arabic_digits_class = '[۱۲۳۴۵۶۷۸۹۰]'
account_number_regex = r'\A(' + english_digits_class + '{16,16}|' +\
                       arabic_digits_class + r'{16,16})\Z'

class SystemAccount(models.Model):
    account_number = models.CharField(max_length = max_account_number_length,
                                      help_text=account_number_help,
                                      primary_key=True,
                                      verbose_name="شماره کارت",
                                      validators=account_number_validators)
