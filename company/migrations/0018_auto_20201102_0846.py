# Generated by Django 3.1 on 2020-11-02 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0017_auto_20201102_0752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dosebolaq',
            name='amount',
            field=models.IntegerField(verbose_name='مقدار'),
        ),
        migrations.AlterField(
            model_name='dosebolaq',
            name='recieved_date',
            field=models.DateField(verbose_name='تاریخ رسید'),
        ),
    ]
