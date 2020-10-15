from django.db import models


class Item(models.Model):
    description = models.CharField(max_length=100, verbose_name='توضیحات')
    price = models.IntegerField(verbose_name='قیمت')
    purchase_date = models.DateField(verbose_name='تاریخ')

    def __str__(self):
        return self.description
