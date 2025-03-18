from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import AddReviewProduct

@api_view(['POST'])
def AddToReview(request):
    data = request.data
    product_id = data.get('id')
    rating = data.get('rating')
    customer_name = data.get('customer_name')
    comment = data.get('comment')

    if not request.user.is_authenticated:
        return Response({"error": "لطفاً وارد حساب کاربری خود شوید."}, status=401)
    else:
        user = request.user

    try:
        review = AddReviewProduct.objects.create(
            user=user,
            product_id=product_id,
            rating=rating,
            customer_name=customer_name,
            comment=comment
        )

        return Response({
            "Status": "ok",
            "product_id": product_id,
        })
    except Exception as e:
        return Response({"error": str(e)}, status=500)
