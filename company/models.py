from django.db import models
from django.utils import timezone


WEIGHT_CHOICES = (
    ('1', 2000),
    ('2', 4000),
    ('3', 6000)
)


class Consignee(models.Model):
    name = models.CharField(max_length=50, verbose_name='نام صاحب مال')
    phone_number = models.CharField(max_length=15, verbose_name='شماره تماس')

    def __str__(self):
        return self.name


class Commissionaire(models.Model):
    name = models.CharField(max_length=20, verbose_name='نام کمیشنکار')

    def __str__(self):
        return self.name


class BillofLading(models.Model):
    consignee = models.ForeignKey(
        Consignee, on_delete=models.CASCADE, verbose_name='صاحب مال')
    commissionaire = models.ForeignKey(
        Commissionaire, on_delete=models.CASCADE, verbose_name='کمیشنر')
    bill_number = models.IntegerField(verbose_name='نمبر بار نامه')
    check_number = models.IntegerField(verbose_name='نمبر بیجک')
    arrival_date = models.DateField(
        auto_now=False, auto_now_add=False, verbose_name='تاریخ ورودی')
    lading_date = models.DateField(
        auto_now=False, auto_now_add=False, verbose_name='تاریخ بارکیری')
    exit_date = models.DateField(
        auto_now=False, auto_now_add=False, verbose_name='تاریخ خروج')
    origin_custom = models.CharField(max_length=50, verbose_name='کمرک مبداء')
    destination_custom = models.CharField(
        max_length=50, verbose_name='کمرک مقصد')
    act_cmr = models.IntegerField(verbose_name='کت )سی-ام-ار(')
    container_number = models.CharField(
        max_length=20, verbose_name='نمبر کانتینر / واکن')
    empty_number = models.CharField(max_length=15, verbose_name='کانتینر خالی')
    commodity = models.CharField(max_length=100, verbose_name='نوع جنس')
    quantity = models.CharField(max_length=20, verbose_name='تعداد')
    net_weight = models.IntegerField(verbose_name='وزن خالص')
    container_weight = models.CharField(
        max_length=1, choices=WEIGHT_CHOICES, verbose_name='وزن کانتنر', default=0)
    licens_number = models.IntegerField(verbose_name='شماره جواز')
    b_l_number = models.IntegerField(verbose_name='شماره B/L')
    driver = models.CharField(max_length=20, verbose_name='درایور')
    driver_father = models.CharField(
        max_length=20, verbose_name='نام پدر درایور')
    truck_number = models.IntegerField(verbose_name='نمبر لاری')
    transport = models.CharField(max_length=20, verbose_name='ترانسپورت')
    asab_shasi = models.IntegerField(verbose_name='شاسی اسب')
    truck_shasi = models.IntegerField(verbose_name='شاسی تیلر')
    tin_jawaz = models.IntegerField(verbose_name='تنن جواز (TIN JAWAZ)')

    @property
    def total_weight(self):
        total = 0
        if self.container_weight is not int(0):
            total = self.net_weight + int(self.container_weight)
        else:
            total = self.net_weight
        return total


class FareBill(models.Model):
    bill = models.ForeignKey(
        BillofLading, on_delete=models.CASCADE)
    porterage_expenses = models.IntegerField(verbose_name="مصارف حمالی")
    invoice_copy = models.IntegerField(
        verbose_name='مصارف انوایس، کاپی و اتحادیه')
    commission_fee = models.IntegerField(verbose_name='کمیشن بارچلانی')
    custom_expenses = models.IntegerField(verbose_name='مصارف کمرک اسلام قلعه')
    rent = models.IntegerField(verbose_name='کرایه')
    farebill_date = models.DateField(
        auto_now=False, auto_now_add=False, verbose_name='تاریخ')

    def __str__(self):
        return self.bill.bill_number

    @property
    def total_expenses(self):
        total = self.porterage_expenses + self.invoice_copy + \
            self.commission_fee + self.custom_expenses + self.rent
        return total


class Recive(models.Model):
    bill = models.ForeignKey(
        BillofLading, on_delete=models.CASCADE)
    i_number = models.IntegerField(verbose_name="ای نمبر ")
    taliban_expenses = models.IntegerField(verbose_name="مصارف ظالمان")
    eslam_qala_expenses = models.IntegerField(verbose_name="مصارف اسلام قلعه")
    bascol_expenses = models.IntegerField(verbose_name="مصارف باسکول")

    def __str__(self):
        return self.billoflading.bill_number

    @property
    def total_expenses(self):
        total = self.taliban_expenses + self.eslam_qala_expenses + \
            self.bascol_expenses
        return total


class Account(models.Model):
    consignee = models.ForeignKey(
        Consignee, on_delete=models.CASCADE, null=True, blank=True, verbose_name=('صاحب بار'))
    recieve_date = models.DateField(
        verbose_name="تاریخ رسید", default=timezone.now)
    amount = models.FloatField(verbose_name="مقدار")
