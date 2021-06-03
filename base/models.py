from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.
class Convert(models.Model):
    currency = models.CharField(max_length=5, verbose_name="Валюта")
    value = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Значение",
                                validators=[MinValueValidator(Decimal('0.01'))])
    pub_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    def __str__(self):
        return self.currency

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"
        ordering = ['-pub_time']

