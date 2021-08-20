from django.contrib import admin
from .models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug":("product_name",)
    }
    list_display = [
        'product_name',
        'description',
        'price',
        'stock',
        'color',
        'gender',
        'size',
        'category',
        'is_avail',
        'modified_date',
        'id'
    ]

admin.site.register(Product,ProductAdmin)
