from django.db import models
from django.conf import settings


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # کاربری که محصول را پسندیده
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # محصولی که لایک شده
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # جلوگیری از اضافه شدن یک محصول چند بار توسط یک کاربر

    def __str__(self):
        return f"{self.user.phone_number} -> {self.product.name}"
