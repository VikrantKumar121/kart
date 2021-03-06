from django.db import models
from django.urls import reverse
from category.models import Category
from user.models import User
from django.db.models import Avg

# Create your models here.
GENDER_LIST = [
    ('M','Male'),
    ('F','Female'),
    ('U','Unisex')
]
SIZE_LIST = [
    ('S','Small'),
    ('M','Medium'),
    ('L','Large'),
    ('XL','Extra Large')
]

class Product(models.Model):
    """"""
    product_name = models.CharField(max_length = 125, unique = True)
    slug = models.CharField(max_length = 125, unique = True)
    description = models.CharField(max_length = 250)
    price = models.IntegerField()
    stock = models.IntegerField()
    color = models.CharField(max_length = 30)
    gender = models.CharField(max_length = 30, choices = GENDER_LIST)
    size = models.CharField(max_length = 30, choices = SIZE_LIST)
    image = models.ImageField(upload_to = 'images/products')
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    is_avail = models.BooleanField(default = True)
    created_date = models.DateTimeField(auto_now_add = True)
    modified_date = models.DateTimeField(auto_now = True)

    def get_link(self):
        return reverse('search_product', args = [self.id])

    def __str__(self):
        return self.product_name

    def avg_review(self):
        """"""
        reviews = Review.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] != None:
            avg = float(reviews['average'])

        return avg

class Variation(models.Model):
    """"""
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    color = models.CharField(max_length = 30)
    gender = models.CharField(max_length = 30, choices = GENDER_LIST)
    size = models.CharField(max_length = 30, choices = SIZE_LIST)
    stock = models.IntegerField()
    is_avail = models.BooleanField(default = True)
    created_date = models.DateTimeField(auto_now_add = True)
    modified_date = models.DateTimeField(auto_now = True)

    class Meta:
        unique_together = ('product','color','size',)

    def __str__(self):
        return self.product.product_name+' '+self.color+' '+self.size

    def get_link(self):
        return reverse('variation', args = [self.product.id, self.color, self.size])

class Review(models.Model):
    """"""
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    # variation = models.ForeignKey(Variation, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    subject = models.CharField(max_length = 100, blank=True)
    review = models.CharField(max_length = 100, blank=True)
    ip = models.CharField(max_length = 100, blank=True)
    rating = models.FloatField()
    status = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.subject

class ProductGallery(models.Model):
    """"""
    # product = models.ForeignKey(Product, on_delete = models.CASCADE, null = True)
    variation = models.ForeignKey(Variation, on_delete = models.CASCADE)
    image = models.ImageField(upload_to='store/products/variations', max_length = 255)
    uploaded_on = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.variation.product.product_name+' '+self.variation.color+' '+self.variation.size

    # def __inti__(self):
    #     self.product = self.variation.product
