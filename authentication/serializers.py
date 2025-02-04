from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

class AuthSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone_number = data.get("phone_number")
        password = data.get("password")

        user = User.objects.filter(phone_number=phone_number).first()

        if user:
            # اگر کاربر قبلاً ثبت شده باشد، رمز عبور را بررسی کن
            if not user.check_password(password):
                raise serializers.ValidationError("رمز عبور اشتباه است")
        else:
            # اگر کاربر جدید باشد، آن را ایجاد کن و منتظر رمز عبور بمان
            user = User(phone_number=phone_number)
            user.set_password(password)
            user.save()

        # تولید توکن
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
