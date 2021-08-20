from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    """"""
    category_name = models.CharField(max_length = 20, unique = True)
    slug = models.SlugField(max_length = 100, unique = True)
    description = models.CharField(max_length = 250, blank = True, null = True)
    category_img = models.ImageField(upload_to = 'images/category', blank = True)

    def get_link(self):
        return reverse('search_category', args = [self.slug])

    def __str__(self):
        return self.category_name
