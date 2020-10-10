from django.db import models


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
    name = models.CharField(max_length=20)

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
    conatiner_weight = models.CharField(
        max_length=1, choices=WEIGHT_CHOICES, verbose_name='وزن کانتنر')
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


class FareBill(models.Model):
    bill = models.ForeignKey(
        BillofLading, on_delete=models.CASCADE)
    porterage_expenses = models.IntegerField()
    invoice_copy = models.IntegerField()
    commission_fee = models.IntegerField()
    custom_expenses = models.IntegerField()
    rent = models.IntegerField()


class Recive(models.Model):
    billoflading = models.ForeignKey(
        BillofLading, on_delete=models.CASCADE)
    taliban_expenses = models.IntegerField()
    eslam_qala_expenses = models.IntegerField()
    bascol_expenses = models.IntegerField()

    def __str__(self):
        return self.billoflading.bill_number
