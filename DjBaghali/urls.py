# C:\Users\Sanay\PycharmProjects\DjBaghali\DjBaghali\urls.py
from django.contrib import admin
from django.urls import path, include
from authentication.views import AuthView, ConfirmCodeView
from App.views import data_products, post_favorit_request, post_review_request
from AddFavorit.views import AddFavoriteView, UserFavoritesView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('login/', AuthView.as_view(), name='login'),
    path('confirm-code/', ConfirmCodeView.as_view(), name='confirm-code'),
    path("auth/", AuthView.as_view(), name="auth"),
    path('data/', data_products),
    path('save-data/', post_favorit_request),
    path('regmsg/', post_review_request),
    path('favorites/add/', AddFavoriteView.as_view(), name='add_favorite'),
    path('favorites/', UserFavoritesView.as_view(), name='user_favorites'),

]
