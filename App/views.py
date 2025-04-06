import json
import os
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import re
import sqlite3
import pandas as pd
from dateutil.relativedelta import relativedelta

from django.http import JsonResponse
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


def get_file_path(file_name):
    return os.path.join(settings.BASE_DIR, 'App', file_name)


def data_merge(user_id=None):
    try:
        database_path = 'db.sqlite3'
        with sqlite3.connect(database_path) as conn:
            df_products = pd.read_sql_query("SELECT * FROM App_product", conn)
            df_images = pd.read_sql_query("SELECT * FROM App_productimage", conn)
            df_favorites = pd.read_sql_query("SELECT * FROM AddFavorite_favoriteproduct", conn)
            df_addcart = pd.read_sql_query("SELECT * FROM AddCart_addcartproduct", conn)

        if 'id' not in df_products.columns:
            raise Exception("Missing 'id' column in products.")
        if 'product_id' not in df_images.columns:
            raise Exception("Missing 'product_id' column in images.")

        if user_id is not None:
            if not df_favorites.empty:
                df_favorites = df_favorites[df_favorites['user_id'] == user_id]
            if not df_addcart.empty:
                df_addcart = df_addcart[df_addcart['user_id'] == user_id]

        grouped_images = (
            df_images.groupby('product_id')['productImageSrc']
            .apply(lambda x: [{"productImageSrc": src} for src in x])
            .reset_index()
        )

        merged_df_f = pd.merge(df_products, grouped_images, left_on='id', right_on='product_id', how='left')
        merged_df_f['productImageSrc'] = merged_df_f.get('productImageSrc', []).apply(
            lambda x: x if isinstance(x, list) else []
        )

        if not df_favorites.empty:
            merged_df_f = pd.merge(
                merged_df_f,
                df_favorites[['product_id', 'is_favorite']],
                left_on='id',
                right_on='product_id',
                how='left'
            )
        merged_df_f['is_favorite'] = merged_df_f['is_favorite'].fillna(0).astype(int)
        if 'product_id_y' in merged_df_f.columns:
            merged_df_f = merged_df_f.drop(columns=['product_id_y'])

        merged_df_C = pd.merge(df_products, grouped_images, left_on='id', right_on='product_id', how='left')
        merged_df_C['productImageSrc'] = merged_df_C.get('productImageSrc', []).apply(
            lambda x: x if isinstance(x, list) else []
        )
        if not df_addcart.empty:
            merged_df_C = pd.merge(
                merged_df_C,
                df_addcart[['product_id', 'quantity']],
                left_on='id',
                right_on='product_id',
                how='left'
            )
        merged_df_C['quantity'] = merged_df_C['quantity'].fillna(0).astype(int)
        if 'product_id_x' in merged_df_C.columns:
            merged_df_C = merged_df_C.drop(columns=['product_id_x'])
        if 'quantity' not in merged_df_C.columns:
            merged_df_C['quantity'] = 0
        else:
            merged_df_C['quantity'] = merged_df_C['quantity'].fillna(0).astype(int)

        final_df = pd.merge(
            merged_df_C,
            merged_df_f[['id', 'is_favorite']],
            how='left',
            left_on='id',
            right_on='id'
        )
        final_df['is_favorite'] = final_df['is_favorite'].fillna(0).astype(int)
        final_df['quantity'] = final_df['quantity'].fillna(0).astype(int)
        if 'product_id_y' in final_df.columns:
            final_df = final_df.drop(columns=['product_id_y'])
        if 'is_favorite' not in final_df.columns:
            final_df['is_favorite'] = 0
        else:
            final_df['is_favorite'] = final_df['is_favorite'].fillna(0).astype(int)

        final_df = final_df.where(pd.notnull(final_df), None)

        return final_df

    except Exception as e:
        raise e


def data_products(request):
    try:
        user = request.user
        user_id = user.id if user and user.is_authenticated else None

        df = data_merge(user_id=user_id)
        data = df.to_dict(orient='records')

        # search

        # پیش نهاد ai ولی من دوسش ندارم
        # search_query = request.GET.get('search')
        #
        # if search_query:
        #     search_query_lower = search_query.lower()
        #     search_fields = ['product_name', 'sub_category', 'category', 'brand', 'product_details']
        #
        #     data = [
        #         item for item in data
        #         if any(search_query_lower in str(item.get(field, '')).lower() for field in search_fields)
        #     ]

        # و یا

        # search_query = request.GET.get('search')
        #
        # if search_query:
        #     search_query_lower = search_query.lower()
        #     search_fields = ['product_name', 'sub_category', 'category', 'brand', 'product_details']
        #
        #     data = list(filter(
        #         lambda item: any(search_query_lower in str(item.get(field, '')).lower() for field in search_fields),
        #         data))

        search_query = request.GET.get('search')
        if search_query:
            search_query_lower = search_query.lower()
            data = [
                item for item in data
                if (
                        search_query_lower in str(item.get('product_name', '')).lower() or
                        search_query_lower in str(item.get('sub_category', '')).lower() or
                        search_query_lower in str(item.get('category', '')).lower() or
                        search_query_lower in str(item.get('brand', '')).lower() or
                        search_query_lower in str(item.get('product_details', '')).lower()
                )
            ]

        # id
        id_param = request.GET.get('id')
        if id_param:
            try:
                id_param = int(id_param)
                data = [item for item in data if item.get('id') == id_param]
            except ValueError:
                return JsonResponse({"error": "Invalid id value"}, status=400)

        # sorting
        sort_param = request.GET.get('sort')
        if sort_param:
            if sort_param == 'Cheapest':
                data = sorted(data, key=lambda x: x.get('main_price', 0))
            elif sort_param == 'Expensive':
                data = sorted(data, key=lambda x: x.get('main_price', 0), reverse=True)
            elif sort_param == 'Discounted':
                data = sorted(data, key=lambda x: x.get('Discount', 0), reverse=True)

        # paging
        page_param = request.GET.get('page')
        limit_param = request.GET.get('limit')
        if page_param and limit_param:
            try:
                page = int(page_param)
                limit = int(limit_param)
                offset = (page - 1) * limit
                data = data[offset:offset + limit]
            except ValueError:
                return JsonResponse({"error": "Invalid page or limit value"}, status=400)
        elif limit_param:
            try:
                limit = int(limit_param)
                data = data[:limit]
            except ValueError:
                return JsonResponse({"error": "Invalid limit value"}, status=400)

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@api_view(['GET'])
def dataCartProduct(request):
    try:
        user = request.user
        if not user or not user.is_authenticated:
            return JsonResponse({"status": "error", "message": "Authentication required"}, status=401)
        user_id = user.id

        df_addcart_filtered = data_merge(user_id=user_id)
        df_addcart_filtered = df_addcart_filtered[df_addcart_filtered['quantity'] >= 1]
        data = df_addcart_filtered.to_dict(orient='records')
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@api_view(['GET'])
def isLoggedIn(request):
    try:
        user = request.user
        if not user or not user.is_authenticated:
            return JsonResponse({"status": "error", "message": "Authentication required"}, status=401)

        return JsonResponse({"status": "success", "is_logged_in": True})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@api_view(['GET'])
def data_favorite_products(request):
    try:
        user = request.user
        if not user or not user.is_authenticated:
            return JsonResponse({"status": "error", "message": "Authentication required"}, status=401)
        user_id = user.id

        df_favorites_filtered = data_merge(user_id=user_id)
        df_favorites_filtered = df_favorites_filtered[df_favorites_filtered['is_favorite'] == 1]
        data = df_favorites_filtered.to_dict(orient='records')
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
def DataReviewProduct(request):
    try:
        database_path = 'db.sqlite3'

        with sqlite3.connect(database_path) as conn:
            df_data_Product = pd.read_sql_query("SELECT id, product_name FROM App_product", conn)
            df_Review_Product = pd.read_sql_query("SELECT * FROM AddReview_addreviewproduct", conn)

        df_data_Review_Product = pd.merge(
            df_Review_Product,
            df_data_Product,
            how='left',
            left_on='product_id',
            right_on='id'
        )

        if 'id_y' in df_data_Review_Product.columns:
            df_data_Review_Product = df_data_Review_Product.drop(columns=['id_y'])
        df_data_Review_Product = df_data_Review_Product.rename(columns={'id_x': 'id'})

        def parse_mixed_date(date_value):

            if pd.isna(date_value):
                return pd.NaT

            date_str = str(date_value).strip()

            if re.match(r'^\d+$', date_str):

                return pd.to_datetime(int(date_str), unit='ms', errors='coerce')
            else:
                return pd.to_datetime(date_str, errors='coerce')

        df_data_Review_Product['created_date'] = df_data_Review_Product['created_date'].apply(parse_mixed_date)

        def convert_date(created_date):

            if pd.isna(created_date):
                return "زمان نامعتبر"

            if timezone.is_naive(created_date):
                created_date = timezone.make_aware(created_date, timezone.get_default_timezone())

            now = timezone.now()
            rd = relativedelta(now, created_date)

            if rd.years == 0 and rd.months == 0 and rd.days == 0:
                if rd.hours > 0:
                    return f"{rd.hours} ساعت پیش "
                elif rd.minutes > 0:
                    return f"{rd.minutes} دقیقه پیش "
                else:
                    return "همین الان"
            if rd.years > 0:
                return f"{rd.years} سال پیش "
            if rd.days < 30:
                return f"{rd.days} روز پیش "
            return f"{rd.months} ماه پیش "

        df_data_Review_Product['created_date'] = df_data_Review_Product['created_date'].apply(convert_date)

        data = df_data_Review_Product.to_dict(orient='records')

        id_param = request.GET.get('id')
        if id_param:
            try:
                product_id = int(id_param)
                data = [item for item in data if item.get('product_id') == product_id]
            except ValueError:
                return JsonResponse({"error": "Invalid id value"}, status=400)

        return JsonResponse(data, safe=False)
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
