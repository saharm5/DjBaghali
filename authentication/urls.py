# C:\Users\Sanay\PycharmProjects\DjBaghali\authentication\urls.py
from django.urls import path
from .views import AuthView, ConfirmCodeView

urlpatterns = [
    path('login/', AuthView.as_view(), name='login'),
    path("auth/", AuthView.as_view(), name="auth"),
    path('confirm-code/', ConfirmCodeView.as_view(), name='confirm_code'),  # مسیر جدید
]
