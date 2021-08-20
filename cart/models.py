from django.db import models
from store.models import Product

# Create your models here.

class CartItem(models.Model):
    """"""
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity = models.IntegerField(default = 1)
    is_active = models.BooleanField(default = True)
    added_on = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.product

class Cart(models.Model):
    """"""
    cart_no = models.CharField(max_length = 250, blank = True)
    items = models.ForeignKey(CartItem, on_delete = models.CASCADE)
    created_on = models.DateTimeField(auto_now_add = True)
    

    def __str__(self):
        return self.cart_no
