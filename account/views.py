from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LogoutView
from .send_email import send_confirmation_email
from . import serializers
# from account import serializers

User = get_user_model()


class RegistrationApiView(APIView):
    def post(self, request):
        serializer = serializers.RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                send_confirmation_email(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ActivationView(APIView):
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({'msg':'Successfully activated!'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'msg':'Link expired!'}, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(TokenObtainPairView):
    serializer = serializers.LoginSerializer


class LogoutApiView(LogoutView):
    permission_classes = (permissions.IsAuthenticated,)
