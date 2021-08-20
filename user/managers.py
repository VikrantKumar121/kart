from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    """"""
    def create_user(self, email, user_name, first_name, last_name, password = None, **extra_fields):
        if not email:
            raise ValueError('No email provided')
        if not user_name:
            raise ValueError('no user name provided')

        user = self.model(
            email = self.normalize_email(email),
            user_name = user_name,
            first_name = first_name,
            last_name = last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, user_name, first_name, last_name, password = None, **extra_fields):
        user = self.create_user(email, user_name, first_name, last_name, password, **extra_fields)
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save()
        return user
