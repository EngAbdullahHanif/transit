# Generated by Django 3.1 on 2020-11-02 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0018_auto_20201102_0846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billoflading',
            name='asab_shasi',
            field=models.IntegerField(blank=True, default=' ', null=True, verbose_name='شاسی اسب'),
        ),
        migrations.AlterField(
            model_name='billoflading',
            name='container_type',
            field=models.CharField(choices=[('CH', 'چادری'), ('KA', 'کفی'), ('20', '20ft'), ('40', '40ft'), ('45', '45ft')], max_length=2, verbose_name='نوعیت کانتینر'),
        ),
        migrations.AlterField(
            model_name='billoflading',
            name='truck_shasi',
            field=models.IntegerField(blank=True, default=' ', null=True, verbose_name='شاسی تیلر'),
        ),
    ]
