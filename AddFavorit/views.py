from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import FavoriteProduct

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def toggle_favorite(request):
    data = request.data
    product_id = data.get('id')
    user = request.user

    try:
        favorite = FavoriteProduct.objects.get(user=user, product_id=product_id)
        favorite.is_favorite = not favorite.is_favorite
        favorite.save()
        status_message = "updated"
    except FavoriteProduct.DoesNotExist:
        favorite = FavoriteProduct.objects.create(user=user, product_id=product_id, is_favorite=True)
        status_message = "created"

    return Response({
        'status': status_message,
        'product_id': product_id,
        'is_favorite': favorite.is_favorite
    })
