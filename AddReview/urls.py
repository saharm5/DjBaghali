# C:\Users\Sanay\PycharmProjects\DjBaghali\AddReview\urls.py

from django.urls import path
from App.views import DataReviewProduct
from .views import AddToReview

urlpatterns = [
    path('review/', AddToReview, name='add_to_Review'),
    path('list/', DataReviewProduct, name='ReviewProduct'),
#     حتما باید id خصوص فرستاده شه
#     AddReview/list?id =${value}
]
