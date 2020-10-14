# Generated by Django 3.1 on 2020-10-14 03:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_farebill_rent'),
    ]

    operations = [
        migrations.AddField(
            model_name='farebill',
            name='farebill_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='consignee',
            name='name',
            field=models.CharField(max_length=50, verbose_name='نام صاحب مال'),
        ),
        migrations.AlterField(
            model_name='consignee',
            name='phone_number',
            field=models.CharField(max_length=15, verbose_name='شماره تماس'),
        ),
    ]