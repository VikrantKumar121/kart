from django.db import models
from store.models import Product

# Create your models here.

class Cart(models.Model):
    """"""
    cart_no = models.CharField(max_length = 250, blank = True)
    # items = models.ManyToManyField(CartItem, on_delete = models.CASCADE)
    created_on = models.DateTimeField(auto_now_add = True)


    def __str__(self):
        return self.cart_no

class CartItem(models.Model):
    """"""
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.IntegerField(default = 1)
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE, null = True)
    is_active = models.BooleanField(default = True)
    added_on = models.DateTimeField(auto_now_add = True)

    def sub_total(self):
        return self.quantity * self.product.price

    def __str__(self):
        return self.product.product_name
