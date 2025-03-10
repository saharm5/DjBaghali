# C:\Users\Sanay\PycharmProjects\DjBaghali\DjBaghali\urls.py

from django.contrib import admin
from django.urls import include, path
from App.views import data_products, post_review_request, isLoggedIn

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/data/', data_products, name='data_products'),
    path('api/isLoggedIn/', isLoggedIn, name='isLoggedIn'),
    path('favorites/', include('AddFavorite.urls')),
    path('AddCart/', include('AddCart.urls')),
    path('api/reviews/', post_review_request, name='post_review'),
]
