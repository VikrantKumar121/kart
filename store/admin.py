from django.contrib import admin
from .models import Product, Variation, Review, ProductGallery
import admin_thumbnails

# Register your models here.
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    """"""
    model = ProductGallery
    extra = 1

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

class VarirationAdmin(admin.ModelAdmin):

    list_display = [
        'product',
        'stock',
        'color',
        'gender',
        'size',
        'is_avail',
        'modified_date',
        'id'
    ]
    list_filter = (
        'product',
        'color',
        'size',
        'is_avail',
    )
    inlines = [ProductGalleryInline]

admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VarirationAdmin)
admin.site.register(Review)
admin.site.register(ProductGallery)
