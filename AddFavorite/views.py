# C:\Users\Sanay\PycharmProjects\DjBaghali\AddFavorite\views.py
import pandas as pd
from django.db.backends import sqlite3
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import FavoriteProduct
import sqlite3


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def toggle_favorite(request):
    data = request.data
    product_id = data.get('id')
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


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def data_favorite_products(request):
    try:
        user_id = request.user.id

        database_path = 'db.sqlite3'
        with sqlite3.connect(database_path) as conn:
            df_products = pd.read_sql_query("SELECT * FROM App_product", conn)
            df_images = pd.read_sql_query("SELECT * FROM App_productimage", conn)
            df_favorites = pd.read_sql_query("SELECT * FROM AddFavorite_favoriteproduct", conn)

        required_columns = ['id']
        if not all(col in df_products.columns for col in required_columns):
            return JsonResponse({"status": "error", "message": "Missing 'id' column in products."}, status=400)

        required_columns = ['product_id', 'productImageSrc']
        if not all(col in df_images.columns for col in required_columns):
            return JsonResponse({"status": "error", "message": "Missing required columns in images."}, status=400)

        required_columns = ['user_id', 'product_id']
        if not all(col in df_favorites.columns for col in required_columns):
            return JsonResponse({"status": "error", "message": "Missing required columns in favorites."}, status=400)

        df_favorites_filtered = df_favorites[
            (df_favorites['user_id'] == user_id) &
            (df_favorites['is_favorite'] == 1)
            ]

        grouped_images = (
            df_images.groupby('product_id')['productImageSrc']
            .apply(lambda x: [{"productImageSrc": src} for src in x])
            .reset_index()
        )

        merged_df = pd.merge(df_products, grouped_images, left_on='id', right_on='product_id', how='left')

        favorite_products = merged_df[merged_df['id'].isin(df_favorites_filtered['product_id'])]
        favorite_products_json = favorite_products.to_dict(orient='records')

        return JsonResponse(favorite_products_json, safe=False)
        # return JsonResponse({"status": "success", "data": favorite_products_json}, safe=False)

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
