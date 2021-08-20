from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
class NewUserAdmin(UserAdmin):
    list_display = [
        'user_name',
        'first_name',
        'last_name',
        'email',
        'phone_no',
        'date_joined',
        'last_login',
        'is_admin',
        'is_staff',
        'is_active',
        'is_superadmin'
    ]
    list_display_links = [
        'user_name',
        'first_name',
        'last_name',
        'email'
    ]
    readonly_fields = [
        'date_joined',
        'last_login'
    ]
    ordering = [
        'date_joined'
    ]
    filter_horizontal = []
    list_filter = []
    fieldsets = []

admin.site.register(User,NewUserAdmin)
