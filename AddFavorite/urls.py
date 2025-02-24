# C:\Users\Sanay\PycharmProjects\DjBaghali\AddFavorite\views.py
from django.urls import path
from .views import toggle_favorite, data_favorite_products

urlpatterns = [
    path('toggle/', toggle_favorite, name='toggle_favorite'),
    path('list/', data_favorite_products, name='favorite_list'),
]
