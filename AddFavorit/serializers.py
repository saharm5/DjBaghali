from rest_framework import serializers
from .models import Favorite, Product


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['product']

    def create(self, validated_data):
        user = self.context['request'].user  # گرفتن کاربر از درخواست
        product = validated_data['product']
        favorite, created = Favorite.objects.get_or_create(user=user, product=product)

        if not created:
            raise serializers.ValidationError("این محصول قبلاً به علاقه‌مندی‌ها اضافه شده است.")

        return favorite
