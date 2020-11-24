from django.db import models
from django.utils import timezone


WEIGHT_CHOICES = (
    ('1', 2000),
    ('2', 4000),
    ('3', 4500)
)

CONTAINER_TYPE = (
    ('CH', 'چادری'),
    ('KA', 'کفی'),
    ('20', '20ft'),
    ('40', '40ft'),
    ('45', '45ft'),
)

EMPTY_CONTAINER = (
    ('A', 'بازگشتی است'),
    ('B', 'بازگشت شد است'),
    ('B', 'محصولی است')
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


class Driver(models.Model):
    name = models.CharField(max_length=20, verbose_name="اسم درایور")
    truck_number = models.IntegerField(verbose_name='نمبر لاری')

    class Meta:
        verbose_name = ("Driver")
        verbose_name_plural = ("Drivers")

    def __str__(self):
        return self.name + " - " + str(self.truck_number)


class Company(models.Model):
    name = models.CharField(max_length=30, verbose_name="اسم شرکت")
    tin_number = models.CharField(max_length=10, verbose_name="تین جواز")

    class Meta:
        verbose_name = ("Companies")
        verbose_name_plural = ("Companies")

    def __str__(self):
        return self.name + " - " + self.tin_number


class Recieve(models.Model):
    # bill = models.ManyToManyField(BillofLading)
    i_number = models.IntegerField(verbose_name="ای نمبر ")
    taliban_expenses = models.IntegerField(verbose_name="مصارف طالبان")
    eslam_qala_expenses = models.IntegerField(verbose_name="مصارف اسلام قلعه")
    bascol_expenses = models.IntegerField(verbose_name="مصارف باسکول")

    def __str__(self):
        return str(self.i_number)

    @property
    def total_expenses(self):
        total = self.taliban_expenses + self.eslam_qala_expenses + \
            self.bascol_expenses
        return total


class BillofLading(models.Model):
    consignee = models.ForeignKey(
        Consignee, on_delete=models.CASCADE, verbose_name='صاحب مال')
    commissionaire = models.ForeignKey(
        Commissionaire, on_delete=models.CASCADE, verbose_name='کمیشنر', blank=True, null=True)
    bill_number = models.IntegerField(verbose_name='نمبر بار نامه')
    check_number = models.IntegerField(verbose_name='نمبر بیجک')
    arrival_date = models.DateField(
        auto_now=False, auto_now_add=False, verbose_name='تاریخ ورودی')
    lading_date = models.DateField(
        auto_now=False, auto_now_add=False, verbose_name='تاریخ بارکیری', blank=True, null=True)
    exit_date = models.DateField(
        auto_now=False, auto_now_add=False, verbose_name='تاریخ خروج')
    origin_custom = models.CharField(max_length=50, verbose_name='کمرک مبداء')
    destination_custom = models.CharField(
        max_length=50, verbose_name=' مقصد')
    act_cmr = models.IntegerField(verbose_name='کت )سی-ام-ار(')
    container_type = models.CharField(
        max_length=2, choices=CONTAINER_TYPE, verbose_name='نوعیت کانتینر')
    container_number = models.CharField(
        max_length=10, verbose_name='نمبر کانتینر / واکن', null=True, blank=True)
    empty_number = models.CharField(
        max_length=1, choices=EMPTY_CONTAINER, verbose_name='کانتینر خالی')
    commodity = models.CharField(max_length=100, verbose_name='نوع جنس')
    quantity = models.CharField(max_length=20, verbose_name='تعداد')
    net_weight = models.IntegerField(verbose_name='وزن خالص')
    # 1
    # container_weight = models.CharField(
    #     max_length=1, choices=WEIGHT_CHOICES, verbose_name='وزن کانتنر', default=0)
    licens_number = models.IntegerField(
        verbose_name='شماره جواز', blank=True, null=True)
    b_l_number = models.IntegerField(
        verbose_name='شماره B/L', blank=True, null=True)
    driver = models.ForeignKey(Driver, verbose_name=(
        "اسم درایور"), on_delete=models.CASCADE)
    company = models.ForeignKey(Company, verbose_name=(
        "TIN - اسم شرکت"), on_delete=models.CASCADE)
    # driver = models.CharField(
    #     max_length=20, verbose_name='درایور', default='ali')
    # driver_father = models.CharField(
    #     max_length=20, verbose_name='نام پدر درایور', blank=True, null=True)
    transport = models.CharField(max_length=20, verbose_name='ترانسپورت')
    asab_shasi = models.IntegerField(
        verbose_name='شاسی اسب', blank=True, null=True, default=' ')
    truck_shasi = models.IntegerField(
        verbose_name='شاسی تیلر', blank=True, null=True, default=' ')
    # tin_jawaz = models.IntegerField(verbose_name='تنن جواز (TIN JAWAZ)')

    # *Recieve is brought here to make reports batter
    recieve = models.ForeignKey(
        Recieve, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return str(self.bill_number)

    @property
    def total_weight(self):
        total_weight = 0
        if self.container_number == 'CH' or self.container_number == 'KA':
            total_weight = self.net_weight
        elif (self.container_number == 1):
            total_weight = self.net_weight - 2000
        elif (self.container_number == 2):
            total_weight = self.net_weight - 4000
        else:
            total_weight = self.net_weight - 4500
        return total_weight

    @property
    def container_weight(self):
        container_weight = 0
        if self.container_number == 'CH' or self.container_number == 'KA':
            container_weight = 'نه دارد'
        else:
            if self.container_type == '20':
                container_weight = '2000 کلو گرام'
            elif self.container_type == '40':
                container_weight = '400 کلو گرام'
            else:
                container_weight = '4500 کلو گرام'
        return container_weight


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
        auto_now=False, auto_now_add=False, verbose_name='تاریخ', blank=True, null=True)
    received = models.IntegerField(verbose_name='وصول')

    def __str__(self):
        return str(self.bill.bill_number)

    @property
    def total_expenses(self):
        total = self.porterage_expenses + self.invoice_copy + \
            self.commission_fee + self.custom_expenses
        return total

    @property
    def remained(self):
        remained = self.total_expenses - self.received
        return remained


class Account(models.Model):
    consignee = models.ForeignKey(
        Consignee, on_delete=models.CASCADE, null=True, blank=True, verbose_name=('صاحب بار'))

    recieve_date = models.DateField(
        verbose_name="تاریخ رسید", default=timezone.now)
    amount = models.FloatField(verbose_name="مقدار")


class DoseBolaq(models.Model):
    truck_number = models.ForeignKey(
        Driver, verbose_name=("نمبر موتر"), on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField(verbose_name='مقدار')
    reciever = models.CharField(
        max_length=20, verbose_name='گیرنده', null=True)
    recieved_date = models.DateField(
        auto_now=False, auto_now_add=False, verbose_name='تاریخ رسید')
