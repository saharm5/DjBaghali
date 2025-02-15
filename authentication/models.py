# C:\Users\Sanay\PycharmProjects\DjBaghali\authentication\models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import random


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
        if not phone_number:
            raise ValueError("شماره تلفن اجباری است")
        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.is_active = False  # کاربر غیر فعال است تا وقتی که کد تایید وارد بشه
        user.save(using=self._db)
        return user

    # def create_superuser(self, phone_number, password):
    #     user = self.create_user(phone_number, password)
    #     user.is_admin = True
    #     user.is_staff = True
    #     user.is_superuser = True
    #     user.save(using=self._db)
    #     return user


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    confirm_code = models.CharField(max_length=6, default="", blank=True)

    # باقی فیلدها و متدها

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",
        blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return self.phone_number

    def generate_confirm_code(self):
        self.confirm_code = str(random.randint(100000, 999999))  # تولید کد ۶ رقمی
        self.save()
        print(f"کد تأیید برای {self.phone_number}: {self.confirm_code}")  # نمایش کد تأیید در ترمینال
