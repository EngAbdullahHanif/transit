# Generated by Django 3.1 on 2020-11-02 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0016_auto_20201102_0704'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dosebolaq',
            name='recieved_date',
            field=models.DateField(),
        ),
    ]
