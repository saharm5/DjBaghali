# C:\Users\Sanay\PycharmProjects\DjBaghali\AddReview\urls.py

from django.urls import path
from App.views import dataReviewProduct
from .views import AddToReview

urlpatterns = [
    path('review/', AddToReview, name='add_to_Review'),
    path('list/', dataReviewProduct, name='ReviewProduct'),
]
