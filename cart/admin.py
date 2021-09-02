from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'id'
    ]

admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem)
