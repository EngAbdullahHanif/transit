# Generated by Django 3.1 on 2020-10-27 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_item_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='user',
            new_name='consumer',
        ),
    ]
