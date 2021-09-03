from django.db import models
from store.models import Product, Variation
from user.models import User

# Create your models here.

class Cart(models.Model):
    """"""
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    cart_no = models.CharField(max_length = 250, blank = True)
    # items = models.ManyToManyField(CartItem, on_delete = models.CASCADE)
    created_on = models.DateTimeField(auto_now_add = True)


    def __str__(self):
        return self.user.first_name

class CartItem(models.Model):
    """"""
    # user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    variation = models.ForeignKey(Variation, on_delete = models.CASCADE, null=True)
    quantity = models.IntegerField(default = 1)
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE, null = True)
    is_active = models.BooleanField(default = True)
    added_on = models.DateTimeField(auto_now_add = True)

    def sub_total(self):
        return self.quantity * self.product.price

    def __str__(self):
        return self.product.product_name
