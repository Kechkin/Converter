from django.contrib import admin
from .models import ExchangeRate


# Register your models here.

class BaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'currency', 'value', 'pub_time')


admin.site.register(ExchangeRate, BaseAdmin)
