# Generated by Django 3.1 on 2020-10-26 07:46

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BillofLading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_number', models.IntegerField(verbose_name='نمبر بار نامه')),
                ('check_number', models.IntegerField(verbose_name='نمبر بیجک')),
                ('arrival_date', models.DateField(verbose_name='تاریخ ورودی')),
                ('lading_date', models.DateField(blank=True, null=True, verbose_name='تاریخ بارکیری')),
                ('exit_date', models.DateField(verbose_name='تاریخ خروج')),
                ('origin_custom', models.CharField(max_length=50, verbose_name='کمرک مبداء')),
                ('destination_custom', models.CharField(max_length=50, verbose_name=' مقصد')),
                ('act_cmr', models.IntegerField(verbose_name='کت )سی-ام-ار(')),
                ('container_number', models.CharField(max_length=20, verbose_name='نمبر کانتینر / واکن')),
                ('empty_number', models.CharField(max_length=15, verbose_name='کانتینر خالی')),
                ('commodity', models.CharField(max_length=100, verbose_name='نوع جنس')),
                ('quantity', models.CharField(max_length=20, verbose_name='تعداد')),
                ('net_weight', models.IntegerField(verbose_name='وزن مجموعی')),
                ('container_weight', models.CharField(choices=[('1', 2000), ('2', 4000), ('3', 4500)], default=0, max_length=1, verbose_name='وزن کانتنر')),
                ('licens_number', models.IntegerField(blank=True, null=True, verbose_name='شماره جواز')),
                ('b_l_number', models.IntegerField(blank=True, null=True, verbose_name='شماره B/L')),
                ('transport', models.CharField(max_length=20, verbose_name='ترانسپورت')),
                ('asab_shasi', models.IntegerField(blank=True, null=True, verbose_name='شاسی اسب')),
                ('truck_shasi', models.IntegerField(blank=True, null=True, verbose_name='شاسی تیلر')),
            ],
        ),
        migrations.CreateModel(
            name='Commissionaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='نام کمیشنکار')),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='اسم شرکت')),
                ('tin_number', models.CharField(max_length=10, verbose_name='تین جواز')),
            ],
            options={
                'verbose_name': 'Companies',
                'verbose_name_plural': 'Companies',
            },
        ),
        migrations.CreateModel(
            name='Consignee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='نام صاحب مال')),
                ('phone_number', models.CharField(max_length=15, verbose_name='شماره تماس')),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='اسم درایور')),
                ('truck_number', models.IntegerField(verbose_name='نمبر لاری')),
            ],
            options={
                'verbose_name': 'Driver',
                'verbose_name_plural': 'Drivers',
            },
        ),
        migrations.CreateModel(
            name='Recive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('i_number', models.IntegerField(verbose_name='ای نمبر ')),
                ('taliban_expenses', models.IntegerField(verbose_name='مصارف ظالمان')),
                ('eslam_qala_expenses', models.IntegerField(verbose_name='مصارف اسلام قلعه')),
                ('bascol_expenses', models.IntegerField(verbose_name='مصارف باسکول')),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.billoflading')),
            ],
        ),
        migrations.CreateModel(
            name='FareBill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('porterage_expenses', models.IntegerField(verbose_name='مصارف حمالی')),
                ('invoice_copy', models.IntegerField(verbose_name='مصارف انوایس، کاپی و اتحادیه')),
                ('commission_fee', models.IntegerField(verbose_name='کمیشن بارچلانی')),
                ('custom_expenses', models.IntegerField(verbose_name='مصارف کمرک اسلام قلعه')),
                ('rent', models.IntegerField(verbose_name='کرایه')),
                ('farebill_date', models.DateField(verbose_name='تاریخ')),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.billoflading')),
            ],
        ),
        migrations.AddField(
            model_name='billoflading',
            name='commissionaire',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.commissionaire', verbose_name='کمیشنر'),
        ),
        migrations.AddField(
            model_name='billoflading',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company', verbose_name='TIN - اسم شرکت'),
        ),
        migrations.AddField(
            model_name='billoflading',
            name='consignee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.consignee', verbose_name='صاحب مال'),
        ),
        migrations.AddField(
            model_name='billoflading',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.driver', verbose_name='اسم درایور'),
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recieve_date', models.DateField(default=django.utils.timezone.now, verbose_name='تاریخ رسید')),
                ('amount', models.FloatField(verbose_name='مقدار')),
                ('consignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='company.consignee', verbose_name='صاحب بار')),
            ],
        ),
    ]
