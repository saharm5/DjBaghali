from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from rest_framework.views import APIView
from .serializers import AuthSerializer
from django.contrib.auth import get_user_model, authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

User = get_user_model()


def get_tokens_for_user(user):
    """تولید توکن JWT"""
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


@api_view(['POST'])
def login_or_register(request):
    # برسی وجود کاربر در دیتابیس
    # اگه بود (ورود و 2) اگه نبود (ثبت نام و 1)
    phone = request.data.get('phone_number')
    if not phone:
        return Response({'error': 'شماره تلفن الزامی است!'}, status=status.HTTP_400_BAD_REQUEST)

    user, created = User.objects.get_or_create(phone_number=phone, defaults={'is_active': False})

    if created:
        otp = user.generate_otp()
        print(f"OTP : {otp}")
        return Response({'isregister': 1}, status=status.HTTP_201_CREATED)

    return Response({'isregister': 2}, status=status.HTTP_200_OK)


@api_view(['POST'])
def verify_otp(request):
    # برای ثبت نام
    phone = request.data.get('phone_number')
    otp = request.data.get('otp')
    password = request.data.get('password')

    if not phone or not otp or not password:
        return Response({'error': 'شماره تلفن، OTP و رمز عبور الزامی است!'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(phone_number=phone, otp=otp)
        user.set_password(password)
        user.otp = None
        user.is_active = True
        user.save()

        return Response({'message': 'رمز عبور تنظیم شد.', **get_tokens_for_user(user)}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'OTP نامعتبر است!'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_with_password(request):
    # ورود با رمز عبور
    phone = request.data.get('phone_number')
    password = request.data.get('password')

    if not phone or not password:
        return Response({'error': 'شماره تلفن و رمز عبور الزامی است!'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(phone_number=phone, password=password)

    if user:
        return Response({'message': 'ورود موفق.', **get_tokens_for_user(user)}, status=status.HTTP_200_OK)
    return Response({'error': 'شماره تلفن یا رمز عبور نادرست است!'}, status=status.HTTP_400_BAD_REQUEST)


class ConfirmCodeView(APIView):
    # بررسی کد تأیید و فعال‌سازی حساب
    def post(self, request):
        phone_number = request.data.get('phone_number')
        confirm_code = request.data.get('confirm_code')

        if not phone_number or not confirm_code:
            return Response({"error": "شماره تلفن و کد تأیید الزامی است!"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone_number=phone_number)

            if user.confirm_code == confirm_code:
                user.is_active = True
                user.confirm_code = ""
                user.save()
                return Response({"message": "حساب تأیید شد.", **get_tokens_for_user(user)}, status=status.HTTP_200_OK)
            return Response({"error": "کد تأیید اشتباه است!"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "کاربر پیدا نشد!"}, status=status.HTTP_400_BAD_REQUEST)
