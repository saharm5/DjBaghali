from django.db import models

class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=255)
    product_details = models.TextField()
    main_price = models.IntegerField()
    Discount = models.IntegerField(null=True, blank=True)
    final_price = models.IntegerField()
    brand = models.CharField(max_length=255)
    brand_image_src = models.URLField()
    category = models.CharField(max_length=255)
    sub_category = models.CharField(max_length=255)
    category_image_src = models.URLField()
    size = models.CharField(max_length=50)
    production_date = models.CharField(max_length=50, null=True, blank=True)
    expiration_date = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.product_name

class ProductImage(models.Model):
    products = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    productsImageSrc = models.URLField()

    def __str__(self):
        return f"Image for {self.products.product_name}"