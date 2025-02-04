from django.urls import path
from .views import AuthView

urlpatterns = [
    path('login/', AuthView.as_view(), name='login'),
    path("auth/", AuthView.as_view(), name="auth"),

]
