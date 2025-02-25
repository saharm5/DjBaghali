# C:\Users\Sanay\PycharmProjects\DjBaghali\AddCart\views.py

from django.urls import path
from .views import AddToCart, dataCartProduct

urlpatterns = [
    path('Cart/', AddToCart, name='AddToCart'),
    path('list/', dataCartProduct, name='CartProduct'),
]
