# C:\Users\Sanay\PycharmProjects\DjBaghali\AddFavorite\models.py
from django.db import models
from django.conf import settings

class FavoriteProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_id = models.IntegerField()
    is_favorite = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.product_id} - {self.is_favorite}"
