from django.db import models
from . import user

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

class Driver(user.User):
    certificate_number = models.CharField(max_length=20,
                                   verbose_name="شماره گواهینامه")
    rate = models.PositiveSmallIntegerField(verbose_name="امتیاز")
    availability = models.BooleanField(default=False,
                                       verbose_name="آمادگی برای انتقال")
    region_field = models.PositiveIntegerField()

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
