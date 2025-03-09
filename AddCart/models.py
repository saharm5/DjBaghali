from django.conf import settings
from django.db import models


class AddCartProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_id = models.IntegerField()
    quantity = models.IntegerField(default=1)  # Default should be 1

    def __str__(self):
        return f"{self.user.username} - {self.product_id} - {self.quantity}"