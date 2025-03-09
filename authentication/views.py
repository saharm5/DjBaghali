import os

from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from DjBaghali import settings
from .models import User
from .serializers import AuthSerializer

User = get_user_model()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


@api_view(['POST'])
def login_or_register(request):
    phone = request.data.get('phone_number')
    if not phone:
        return Response({'error': 'شماره تلفن الزامی است!'}, status=status.HTTP_400_BAD_REQUEST)

    user, created = User.objects.get_or_create(phone_number=phone, defaults={'is_active': False})

    if created:
        otp = user.generate_otp()
        print(f"OTP : {otp}")
        file_path = os.path.join(settings.BASE_DIR, 'authentication', 'OTP')

        OTP = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                OTP = file.readlines()

        OTP.append(f"{phone} : {otp}\n")

        with open(file_path, 'w') as file:
            file.writelines(OTP)

        return Response({'isregister': 1}, status=status.HTTP_201_CREATED)

    return Response({'isregister': 2}, status=status.HTTP_200_OK)


@api_view(['POST'])
def verify_otp(request):
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

        return Response({"Status": "ok", 'message': 'رمز عبور تنظیم شد.', **get_tokens_for_user(user)},
                        status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'OTP نامعتبر است!'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_with_password(request):
    phone = request.data.get('phone_number')
    password = request.data.get('password')

    if not phone or not password:
        return Response({'error': 'شماره تلفن و رمز عبور الزامی است!'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(phone_number=phone, password=password)

    if user:
        return Response({"Status": "ok", 'message': 'ورود موفق.', **get_tokens_for_user(user)},
                        status=status.HTTP_200_OK)
    return Response({'error': 'شماره تلفن یا رمز عبور نادرست است!'}, status=status.HTTP_400_BAD_REQUEST)


class ConfirmCodeView(APIView):
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
