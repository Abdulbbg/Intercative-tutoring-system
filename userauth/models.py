from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, name, reg_number, password=None):
        if not reg_number:
            raise ValueError('Users must have a registration number')
        user = self.model(name=name, reg_number=reg_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, reg_number, password=None):
        user = self.create_user(name=name, reg_number=reg_number, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    reg_number = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'reg_number'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.reg_number

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return True  # You can customize this based on your permissions logic

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        return True  # You can customize this as well
