# Generated by Django 3.2.1 on 2021-06-07 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_rename_convert_exchangerate'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ExchangeRate',
            new_name='Exchange_rate',
        ),
    ]