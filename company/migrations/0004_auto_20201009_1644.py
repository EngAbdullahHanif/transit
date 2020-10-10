# Generated by Django 3.1 on 2020-10-09 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_billoflading_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billoflading',
            name='slug',
        ),
        migrations.AddField(
            model_name='farebill',
            name='bill',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='company.billoflading'),
            preserve_default=False,
        ),
    ]