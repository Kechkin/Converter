# Generated by Django 3.2.1 on 2021-05-25 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_test_pub_time'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Test',
            new_name='Convert',
        ),
    ]