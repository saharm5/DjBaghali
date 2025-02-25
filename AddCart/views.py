from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import AddCartProduct
from django.contrib.auth import get_user_model


# C:\Users\Sanay\PycharmProjects\DjBaghali\AddCart\views.py


@api_view(['POST'])
def AddToCart(request):
    data = request.data
    product_id = data.get('id')
    operation = data.get('operation', 'add')

    if not request.user.is_authenticated:
        User = get_user_model()
        user = User.objects.first()
        if not user:
            return Response({"error": "No user available for operation."}, status=400)
    else:
        user = request.user

    try:

        cart, created = AddCartProduct.objects.get_or_create(user=user, product_id=product_id)

        if operation == 'remove':
            if cart.quantity > 1:
                cart.quantity -= 1
                cart.save()
                status_message = "decremented"
            else:
                cart.delete()
                status_message = "removed"
        else:
            if created:
                status_message = "added"
            else:
                cart.quantity += 1
                cart.save()
                status_message = "updated"

        quantity = 0
        if AddCartProduct.objects.filter(user=user, product_id=product_id).exists():
            quantity = AddCartProduct.objects.get(user=user, product_id=product_id).quantity

        return Response({
            'status': status_message,
            'product_id': product_id,
            'quantity': quantity
        })
    except Exception as e:
        return Response({"error": str(e)}, status=500)
