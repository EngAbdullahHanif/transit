# Generated by Django 3.1 on 2020-10-29 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0008_auto_20201029_1028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recive',
            name='bill',
        ),
        migrations.AddField(
            model_name='recive',
            name='bill',
            field=models.ManyToManyField(to='company.BillofLading'),
        ),
    ]