# C:\Users\Sanay\PycharmProjects\DjBaghali\AddReview\models.py
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class AddReviewProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_id = models.IntegerField()
    rating = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    customer_name = models.CharField(max_length=255, default="ناشناس")
    comment = models.CharField(max_length=255, default="")
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product_id} - {self.rating} - {self.customer_name} - {self.comment} - {self.created_date}"
