# Generated by Django 3.1 on 2020-10-14 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0008_auto_20201014_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recive',
            name='i_number',
            field=models.IntegerField(verbose_name='ای نمبر '),
        ),
    ]
