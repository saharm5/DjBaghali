import json
import os
import sqlite3
import pandas as pd
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


def get_file_path(file_name):
    return os.path.join(settings.BASE_DIR, 'App', file_name)


def data_products(request):
    try:
        database_path = 'db.sqlite3'
        with sqlite3.connect(database_path) as conn:
            df_products = pd.read_sql_query("SELECT * FROM App_product", conn)
            df_images = pd.read_sql_query("SELECT * FROM App_productimage", conn)
            df_favorites = pd.read_sql_query("SELECT * FROM AddFavorite_favoriteproduct", conn)

        if 'id' not in df_products.columns:
            return JsonResponse({"status": "error", "message": "Missing 'id' column in products."}, status=400)
        if 'product_id' not in df_images.columns:
            return JsonResponse({"status": "error", "message": "Missing 'product_id' column in images."}, status=400)

        grouped_images = (
            df_images.groupby('product_id')['productImageSrc']
            .apply(lambda x: [{"productImageSrc": src} for src in x])
            .reset_index()
        )

        merged_df = pd.merge(df_products, grouped_images, left_on='id', right_on='product_id', how='left')
        merged_df['productImageSrc'] = merged_df.get('productImageSrc', []).apply(
            lambda x: x if isinstance(x, list) else [])

        if not df_favorites.empty:
            merged_df = pd.merge(
                merged_df,
                df_favorites[['product_id', 'is_favorite']],
                left_on='id',
                right_on='product_id',
                how='left'
            )
            merged_df['is_favorite'] = merged_df['is_favorite'].fillna(0)
        merged_df['is_favorite'] = merged_df['is_favorite'].fillna(0).astype(int)
        if 'product_id_y' in merged_df.columns:
            merged_df = merged_df.drop(columns=['product_id_y'])

        data = merged_df.to_dict(orient='records')

        id_param = request.GET.get('id')
        if id_param:
            try:
                id_param = int(id_param)
                data = [item for item in data if item.get('id') == id_param]
            except ValueError:
                return JsonResponse({"error": "Invalid id value"}, status=400)

        sort_param = request.GET.get('sort')
        if sort_param:
            if sort_param == 'Cheapest':
                data = sorted(data, key=lambda x: x.get('main_price', 0))
            elif sort_param == 'Expensive':
                data = sorted(data, key=lambda x: x.get('main_price', 0), reverse=True)
            elif sort_param == 'Discounted':
                data = sorted(data, key=lambda x: x.get('discount', 0), reverse=True)

        limit = request.GET.get('limit')
        if limit:
            try:
                limit = int(limit)
                data = data[:limit]
            except ValueError:
                return JsonResponse({"error": "Invalid limit value"}, status=400)

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@csrf_exempt
def post_favorite_request(request):
    try:
        data = json.loads(request.body)
        file_path = get_file_path('favorit.json')

        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                try:
                    favorites = json.load(f)
                except json.JSONDecodeError:
                    favorites = []
        else:
            favorites = []

        favorites.append(data)

        with open(file_path, 'w') as f:
            json.dump(favorites, f, indent=4)

        return JsonResponse({"status": "ok", "message": "Favorite saved successfully"})
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@csrf_exempt
def post_review_request(request):
    try:
        data = json.loads(request.body)
        file_path = get_file_path('review.json')

        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                try:
                    reviews = json.load(f)
                except json.JSONDecodeError:
                    reviews = []
        else:
            reviews = []

        reviews.append(data)

        with open(file_path, 'w') as f:
            json.dump(reviews, f, indent=4)

        return JsonResponse({"status": "ok", "message": "Review saved successfully"})
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)
