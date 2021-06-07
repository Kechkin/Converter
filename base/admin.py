from django.contrib import admin
from .models import Exchange_rate


# Register your models here.

class BaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'currency', 'value', 'pub_time')


admin.site.register(Exchange_rate, BaseAdmin)
