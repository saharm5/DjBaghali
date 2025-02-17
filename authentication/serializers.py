from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken


class AuthSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate(self, data):
        phone_number = data.get("phone_number")

        user, created = User.objects.get_or_create(phone_number=phone_number)

        if created:
            # اگر کاربر جدید است، OTP تولید شود
            user.generate_otp()
            message = "کد تأیید ارسال شد، لطفاً OTP را وارد کنید."
        else:
            message = "کاربر موجود است، لطفاً رمز عبور خود را وارد کنید."

        return {
            "message": message,
            "phone_number": user.phone_number
        }


class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone_number = data.get("phone_number")
        otp = data.get("otp")
        password = data.get("password")

        try:
            user = User.objects.get(phone_number=phone_number, otp=otp)
        except User.DoesNotExist:
            raise serializers.ValidationError("OTP نامعتبر است یا کاربر یافت نشد!")

        # ذخیره رمز عبور و فعال کردن کاربر
        user.set_password(password)
        user.otp = None  # حذف OTP پس از تأیید
        user.is_active = True
        user.save()

        refresh = RefreshToken.for_user(user)

        return {
            "message": "رمز عبور تنظیم شد.",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone_number = data.get("phone_number")
        password = data.get("password")

        user = authenticate(phone_number=phone_number, password=password)
        if not user:
            raise serializers.ValidationError("شماره تلفن یا رمز عبور اشتباه است.")

        refresh = RefreshToken.for_user(user)

        return {
            "message": "ورود موفقیت‌آمیز بود.",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
