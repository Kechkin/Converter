# Generated by Django 3.2.1 on 2021-06-07 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_delete_myuser'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Convert',
            new_name='ExchangeRate',
        ),
    ]