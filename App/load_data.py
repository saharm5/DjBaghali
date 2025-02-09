def load_data():
    import json
    from App.models import Product, ProductImage

    json_path = "App/data.json"
    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    for item in data:
        product = Product.objects.create(
            id=item["id"],
            product_name=item["product_name"],
            product_details=item["product_details"],
            main_price=item["main_price"],
            final_price=item["final_price"],
            brand=item["brand"],
            brand_image_src=item["brand_image_src"],
            category=item["category"],
            sub_category=item["sub_category"],
            category_image_src=item["category_image_src"],
            size=item["size"],
            production_date=item["Production"],
            expiration_date=item["expiration_date"],
        )

        for img in item.get("SubproductImages", []):
            ProductImage.objects.create(product=product, productImageSrc=img["productImageSrc"])

    print("Data successfully inserted!")
