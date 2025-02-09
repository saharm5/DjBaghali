#
# import os
# import django
# import json
#
# # Set up Django environment
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjBaghali.settings")
# django.setup()
#
# from App.models import Product, ProductImage
#
#
# def load_data():
#     json_path = "App/data.json"  # Ensure this file exists
#     with open(json_path, "r", encoding="utf-8") as file:
#         data = json.load(file)
#
#     for item in data:
#         product, created = Product.objects.update_or_create(
#             id=item["id"],
#             defaults={
#                 "product_name": item["product_name"],
#                 "product_details": item.get("product_details", ""),
#                 "main_price": item["main_price"],
#                 "Discount": item.get("Discount", 0),
#                 "final_price": item.get("final_price"),
#                 "brand": item["brand"],
#                 "brand_image_src": item["brand_image_src"],
#                 "category": item["category"],
#                 "sub_category": item["sub_category"],
#                 "category_image_src": item["category_image_src"],
#                 "size": item["size"],
#                 "production_date": item.get("production_date", ""),
#                 "expiration_date": item.get("expiration_date", ""),
#             }
#         )
#
#         # Remove old images and insert new ones
#         ProductImage.objects.filter(product=product).delete()
#         images = item.get("SubproductImages", item.get("productImageSrc", []))
#         for img in images:
#             ProductImage.objects.create(product=product, productImageSrc=img["productImageSrc"])
#
#     print("✅ All data inserted successfully!")
#
#
# if __name__ == "__main__":
#     load_data()
