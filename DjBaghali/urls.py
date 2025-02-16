# C:\Users\Sanay\PycharmProjects\DjBaghali\DjBaghali\urls.py

from django.contrib import admin
from django.urls import path, include
from App.views import data_products, post_favorite_request, post_review_request
from AddFavorit.views import AddFavoriteView, UserFavoritesView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),  # همه مسیرهای احراز هویت اینجا
    path('api/data/', data_products, name='data_products'),
    path('api/favorites/add/', AddFavoriteView.as_view(), name='add_favorite'),
    path('api/favorites/', UserFavoritesView.as_view(), name='user_favorites'),
    path('api/save-data/', post_favorite_request, name='save_favorite'),
    path('api/reviews/', post_review_request, name='post_review'),
]
