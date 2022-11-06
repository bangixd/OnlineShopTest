from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.Category)

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    raw_id_fields = ('category',)

