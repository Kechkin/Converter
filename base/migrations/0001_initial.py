# Generated by Django 3.2.1 on 2021-05-24 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(max_length=5)),
                ('value', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
