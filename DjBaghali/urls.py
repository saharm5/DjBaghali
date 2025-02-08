from django.contrib import admin
from django.urls import path, include
from authentication.views import AuthView
from App.views import data_products, post_favorit_request, post_review_request

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('login/', AuthView.as_view(), name='login'),
    path("auth/", AuthView.as_view(), name="auth"),
    path('data/', data_products),
    path('save-data/', post_favorit_request),
    path('regmsg/', post_review_request),

]
