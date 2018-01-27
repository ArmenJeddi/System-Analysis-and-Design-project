from django.db import models
from . import user
from django.core import validators

provinces = [('east_azerbaijan', 'آذربایجان شرقی'),
          ('west_azerbaijan', 'آذربایجان غربی'),
          ('ardabil', 'اردبیل'),
          ('isfahan', 'اصفهان'),
          ('alborz', 'البرز'),
          ('ilam', 'ایلام'),
          ('bushehr', 'بوشهر'),
          ('tehran', 'تهران'),
          ('chaharmahal_and_bakhtiari', 'چهارمحال و بختیاری'),
          ('south_khorasan', 'خراسان جنوبی'),
          ('razavi_khorasan', 'خراسان رضوی'),
          ('north_khorasan', 'خراسان شمالی'),
          ('khuzestan', 'خوزستان'),
          ('zanjan', 'زنجان'),
          ('semnan', 'سمنان'),
          ('sistan_and_baluchestan', 'سیستان و بلوچستان'),
          ('fars', 'فارس'),
          ('qazvin', 'قزوین'),
          ('qom', 'قم'),
          ('kurdistan', 'کردستان'),
          ('kerman', 'کرمان'),
          ('kermanshah', 'کرمانشاه'),
          ('kohgiluyeh_and_boyer_ahmad', 'کهگیلویه و بویراحمد'),
          ('golestan', 'گلستان'),
          ('gilan', 'گیلان'),
          ('lorestan', 'لرستان'),
          ('mazandaran', 'مازندران'),
          ('markazi', 'مرکزی'),
          ('hormozgan', 'هرمزگان'),
          ('hamadan', 'همدان'),
          ('yazd', 'یزد')]

certificate_validator = [validators.RegexValidator(regex=r'\A[a-zA-Z0-9۰۱۲۳۴۵۶۷۸۹]{17}\Z',
                                                   message='شماره گواهینامه باید شبیه IR111111111111111 باشد',
                                                   code='invalid_certificate_number')]
license_validator = [validators.RegexValidator(regex=r'\A[0-9۰۱۲۳۴۵۶۷۸۹]{2}[ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی][0-9۰۱۲۳۴۵۶۷۸۹]{5}\Z',
                                               message='شماره  پلاک باید شبیه ۱۲ب۱۲۳۱۲ باشد',
                                               code='invalid_license_number')]

num_tab = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')

class Driver(user.UnprivilegedUser):
    certificate_number = models.CharField(max_length=17,
                                          verbose_name="شماره گواهینامه",
                                          validators=certificate_validator)
    rate = models.PositiveSmallIntegerField(verbose_name="امتیاز",
                                            default=0)
    availability = models.BooleanField(default=False,
                                       verbose_name="آمادگی برای انتقال")
    vehicle_model = models.CharField(max_length=50,
                             verbose_name="نوع وسیله نقلیه")
    license_plate = models.CharField(max_length=8,
                                     verbose_name="شماره پلاک",
                                     validators=license_validator)
    vehicle_capacity = models.PositiveIntegerField(verbose_name="ظرفیت")
    region_field = models.PositiveIntegerField(default=0)

    def clean(self):
        super().clean()
        self.license_plate = self.license_plate.translate(user.num_tab)
        self.certificate_number = self.certificate_number.translate(num_tab)

    def add_province(self, province):
        index = prov_ind(province)
        if index is None:
            return
        mask = 1 << index
        self.region_field = self.region_field | mask

    def remove_province(self, province):
        index = prov_ind(province)
        if index is None:
            return
        mask = ~(1 << index)
        self.region_field = self.region_field & mask

    def has_province(self, province):
        index = prov_ind(province)
        if index is None:
            return
        mask = 1 << index
        if self.region_field & mask == 0:
            return False
        return True

    def province_list(self):
        prov_ls = []
        mask = 1
        for prov in provinces:
            if self.region_field & mask != 0:
                prov_ls.append(prov)
            mask = mask << 1
        return prov_ls

def prov_ind(province):
    for ind, prov in enumerate(provinces):
        if province == prov[0] or province == prov[1]:
            return ind
