from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile
from django.utils.html import format_html

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

class UserProfileAdmin(admin.ModelAdmin):
    """"""
    def thumbnail(self, object):
        return format_html(f'<img src="{object.profile_pic.url}" width="30" style="border-radius:50%;">')

    thumbnail.short_description = 'PRofile Picture'
    list_display = [
        # 'thumbnail',
        'user',
        'city',
        'state',
        'country'
    ]

admin.site.register(User,NewUserAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
