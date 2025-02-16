import json
import os
import sqlite3
import pandas as pd
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# File path helper function
def get_file_path(file_name):
    return os.path.join(settings.BASE_DIR, 'App', file_name)

# Fetch product and product image data from SQLite database
def data_products(request):
    try:
        database_path = 'db.sqlite3'

        with sqlite3.connect(database_path) as conn:
            df_products = pd.read_sql_query("SELECT * FROM App_product", conn)
            df_images = pd.read_sql_query("SELECT * FROM App_productimage", conn)

        # Ensure required columns exist
        if 'id' not in df_products.columns:
            return JsonResponse({"status": "error", "message": "Missing 'id' column in products."}, status=400)
        if 'product_id' not in df_images.columns:
            return JsonResponse({"status": "error", "message": "Missing 'product_id' column in images."}, status=400)

        # Group images by product_id
        grouped_images = (
            df_images.groupby('product_id')['productImageSrc']
            .apply(lambda x: [{"productImageSrc": src} for src in x])
            .reset_index()
        )

        # Merge product data with grouped images
        merged_df = pd.merge(df_products, grouped_images, left_on='id', right_on='product_id', how='left')

        # Ensure NaN values are replaced with an empty list
        merged_df['productImageSrc'] = merged_df.get('productImageSrc', []).apply(lambda x: x if isinstance(x, list) else [])

        # Convert DataFrame to JSON
        data = merged_df.to_dict(orient='records')

        # Apply optional filters
        limit = request.GET.get('limit')
        if limit:
            try:
                limit = int(limit)
            except ValueError:
                return JsonResponse({"error": "Invalid limit value"}, status=400)

        id_param = request.GET.get('id')
        if id_param:
            try:
                id_param = int(id_param)
                data = [item for item in data if item['id'] == id_param]
            except ValueError:
                return JsonResponse({"error": "Invalid id value"}, status=400)

        if limit:
            data = data[:limit]

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

@csrf_exempt
def post_favorite_request (request):
    try:
        data = json.loads(request.body)
        file_path = get_file_path('favorit.json')

        # Load existing data
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

        # Load existing data
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
