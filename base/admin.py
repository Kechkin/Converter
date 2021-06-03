from django.contrib import admin
from .models import Convert


# Register your models here.

class BaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'currency', 'value', 'pub_time')


admin.site.register(Convert, BaseAdmin)
