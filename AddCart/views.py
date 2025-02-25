import pandas as pd
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import AddCartProduct
import sqlite3
from django.contrib.auth import get_user_model


# C:\Users\Sanay\PycharmProjects\DjBaghali\AddCart\views.py

@api_view(['POST'])
def AddToCart(request):
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
        cart = AddCartProduct.objects.get(user=user, product_id=product_id)
        cart.quantity += 1  # Increase quantity by 1
        cart.save()
        status_message = "updated"
    except AddCartProduct.DoesNotExist:
        cart = AddCartProduct.objects.create(user=user, product_id=product_id, quantity=1)
        status_message = "added"

    return Response({
        'status': status_message,
        'product_id': product_id,
        'quantity': cart.quantity  # Return updated quantity
    })


@api_view(['GET'])
def dataCartProduct(request):
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
            df_addcart = pd.read_sql_query("SELECT * FROM AddCart_addcartproduct", conn)

        if not all(col in df_products.columns for col in ['id']):
            return JsonResponse({"status": "error", "message": "Missing 'id' column in products."}, status=400)
        if not all(col in df_images.columns for col in ['product_id', 'productImageSrc']):
            return JsonResponse({"status": "error", "message": "Missing required columns in images."}, status=400)
        if not all(col in df_addcart.columns for col in ['user_id', 'product_id']):
            return JsonResponse({"status": "error", "message": "Missing required columns in favorites."}, status=400)

        df_addcart_filtered = df_addcart[
            (df_addcart['user_id'] == user_id) &
            (df_addcart['quantity'] == 1)
            ]

        grouped_images = (
            df_images.groupby('product_id')['productImageSrc']
            .apply(lambda x: [{"productImageSrc": src} for src in x])
            .reset_index()
        )

        merged_df = pd.merge(df_products, grouped_images, left_on='id', right_on='product_id', how='left')
        add_cart_products = merged_df[merged_df['id'].isin(df_addcart_filtered['product_id'])]
        add_cart_products_json = add_cart_products.to_dict(orient='records')

        return JsonResponse(add_cart_products_json, safe=False)

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
