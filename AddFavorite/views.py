import pandas as pd
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FavoriteProduct
import sqlite3
from django.contrib.auth import get_user_model


@api_view(['POST'])
def toggle_favorite(request):
    data = request.data
    product_id = data.get('id')

    if not request.user.is_authenticated:
        User = get_user_model()
        user = User.objects.first()
        if not user:
            return Response({"error": "No user available for operation."}, status=400)
    else:
        user = request.user

    try:
        favorite = FavoriteProduct.objects.get(user=user, product_id=product_id)
        favorite.is_favorite = not favorite.is_favorite
        favorite.save()
        status_message = "updated"
    except FavoriteProduct.DoesNotExist:
        favorite = FavoriteProduct.objects.create(user=user, product_id=product_id, is_favorite=True)
        status_message = "created"

    return Response({
        'status': status_message,
        'product_id': product_id,
        'is_favorite': favorite.is_favorite
    })
