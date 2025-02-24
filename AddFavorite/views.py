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


@api_view(['GET'])
def data_favorite_products(request):
    try:
        if not request.user.is_authenticated:
            User = get_user_model()
            user = User.objects.first()
            if not user:
                return JsonResponse({"error": "No user available."}, status=400)
        else:
            user = request.user

        user_id = user.id
        database_path = 'db.sqlite3'
        with sqlite3.connect(database_path) as conn:
            df_products = pd.read_sql_query("SELECT * FROM App_product", conn)
            df_images = pd.read_sql_query("SELECT * FROM App_productimage", conn)
            df_favorites = pd.read_sql_query("SELECT * FROM AddFavorite_favoriteproduct", conn)

        if not all(col in df_products.columns for col in ['id']):
            return JsonResponse({"status": "error", "message": "Missing 'id' column in products."}, status=400)
        if not all(col in df_images.columns for col in ['product_id', 'productImageSrc']):
            return JsonResponse({"status": "error", "message": "Missing required columns in images."}, status=400)
        if not all(col in df_favorites.columns for col in ['user_id', 'product_id']):
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

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
