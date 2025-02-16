from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import random


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
        if not phone_number:
            raise ValueError("شماره تلفن اجباری است")
        user = self.model(phone_number=phone_number)
        if password:
            user.set_password(password)
        user.is_active = False  # کاربر تا تأیید شماره غیرفعال است
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password):
        user = self.create_user(phone_number, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True  # ادمین نیاز به تأیید شماره تلفن ندارد
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=False)  # کاربران جدید غیرفعال هستند
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    confirm_code = models.CharField(max_length=6, blank=True, null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'

    def __str__(self):
        return self.phone_number

    def generate_confirm_code(self):
        """تولید و ذخیره کد تأیید ۶ رقمی"""
        self.confirm_code = str(random.randint(100000, 999999))
        self.save()
        return self.confirm_code  # مقدار برمی‌گرداند تا در صورت نیاز استفاده شود

    def generate_otp(self):
        """تولید و ذخیره OTP برای ورود بدون رمز"""
        self.otp = str(random.randint(100000, 999999))
        self.save()
        return self.otp  # مقدار برمی‌گرداند تا در ارسال پیامک استفاده شود
