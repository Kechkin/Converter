from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.

class Manager_Search_data(models.Manager):
    def get_course_value(self, time, currency):
        return self.get_queryset().filter(pub_time__lte=time, currency=currency)[:1]


class ExchangeRate(models.Model):
    currency = models.CharField(max_length=5, verbose_name="Валюта")
    value = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Значение",
                                validators=[MinValueValidator(Decimal('0.01'))])
    pub_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    objects = Manager_Search_data()

    def __str__(self):
        return self.currency

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"
        ordering = ['-pub_time']
