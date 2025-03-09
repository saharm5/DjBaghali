from django.urls import path

from .views import (ConfirmCodeView, login_or_register, login_with_password,
                    verify_otp)

urlpatterns = [
    path('login-or-register/', login_or_register, name='login_or_register'),
    path('login-with-password/', login_with_password, name='login_with_password'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('confirm-code/', ConfirmCodeView.as_view(), name='confirm_code'),
]

