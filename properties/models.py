from django.db import models
from django.utils import timezone

status_choices = [
    ('CO', 'سالم'),
    ('DA', 'داغمه')
]


class Property(models.Model):
    description = models.CharField(max_length=100, verbose_name='توضیحات')
    price = models.IntegerField(verbose_name='قیت')
    quantity = models.IntegerField(verbose_name='تعداد')
    location = models.CharField(max_length=100, verbose_name='موقعیت')
    status = models.CharField(choices=status_choices,
                              max_length=2, verbose_name='حالت فعلی')
    purchase_date = models.DateField(
        default=timezone.now, verbose_name='تاریخ خرید')
