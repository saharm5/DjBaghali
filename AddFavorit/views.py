from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Favorite, Product
from .serializers import FavoriteSerializer


class AddFavoriteView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = FavoriteSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "محصول به لیست علاقه‌مندی‌ها اضافه شد."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserFavoritesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favorites = Favorite.objects.filter(user=request.user)
        products = [fav.product for fav in favorites]
        return Response({"favorites": [product.name for product in products]})
