# C:\Users\Sanay\PycharmProjects\DjBaghali\authentication\views.py
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AuthSerializer


class AuthView(APIView):
    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
                user.confirm_code = ""  # مقدار `confirm_code` را خالی کنید
                user.save()

                # تولید توکن JWT
                refresh = RefreshToken.for_user(user)
                return Response({
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "کد تأیید اشتباه است!"}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"error": "کاربر پیدا نشد!"}, status=status.HTTP_400_BAD_REQUEST)
