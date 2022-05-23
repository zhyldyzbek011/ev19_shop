from rest_framework import views, permissions
from rest_framework.response import Response
from basket import serializers


class BasketApiView(views.APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        serializer = serializers.OrderSerializer(
            data=request.data
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data)

