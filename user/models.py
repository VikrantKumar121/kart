from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
# Create your models here.

class User(AbstractBaseUser):
    """"""
    user_name = models.CharField(max_length = 30,unique = True)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    email = models.EmailField(max_length = 125, unique = True)
    phone_no = models.IntegerField(null = True, blank = True)

    date_joined = models.DateTimeField(auto_now_add = True)
    last_login = models.DateTimeField(auto_now = True)
    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = False)
    is_superadmin = models.BooleanField(default = False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name','first_name','last_name']

    objects = UserManager()

    def __str__(self):
        return self.user_name

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_user_email(self):
        return self.email

    def has_perm(self, perm, obj = None):
        return self.is_admin

    def has_module_perms(self, module=None):
        return True
