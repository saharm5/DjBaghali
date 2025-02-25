# C:\Users\Sanay\PycharmProjects\DjBaghali\DjBaghali\urls.py

from django.contrib import admin
from django.urls import path, include
from App.views import data_products, post_favorite_request, post_review_request

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/data/', data_products, name='data_products'),
    path('favorites/', include('AddFavorite.urls')),
    path('AddCart/', include('AddCart.urls')),
    path('api/save-data/', post_favorite_request, name='save_favorite'),
    path('api/reviews/', post_review_request, name='post_review'),
]
