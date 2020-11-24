from django.db import models
from company.models import Consignee, BillofLading


class Item(models.Model):
    consumer = models.CharField(max_length=50, verbose_name='مصرف کننده')
    bill = models.ForeignKey(BillofLading, verbose_name=(
        "نمبر بارنامه"), on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(
        max_length=100, verbose_name='توضیحات', blank=True, null=True)
    price = models.IntegerField(verbose_name='قیمت')
    purchase_date = models.DateField(
        verbose_name='تاریخ', blank=True, null=True)

    def __str__(self):
        return self.description
