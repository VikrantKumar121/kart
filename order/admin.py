from django.contrib import admin
from .models import Payment, Order, OrderProduct

# Register your models here.

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'full_name',
        'order_no',
        'email',
        'city',
        'order_total',
        'tax',
        'status',
        'ip',
        'is_ordered'
    ]
    list_filter = [
        'status',
        'is_ordered'
    ]
    search_field = [
        'order_no',
        'first_name',
        'last_name',
        'email'
    ]
    inlines = [OrderProductInline]

admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct)
