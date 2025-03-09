# C:\Users\Sanay\PycharmProjects\DjBaghali\AddCart\views.py

from django.urls import path

from App.views import dataCartProduct

from .views import AddToCart

urlpatterns = [
    path('cart/', AddToCart, name='add_to_cart'),
    path('list/', dataCartProduct, name='CartProduct'),
]
