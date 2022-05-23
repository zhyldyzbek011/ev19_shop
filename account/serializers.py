from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils.text import gettext_lazy as _
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(min_length=6, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')
    
    def validate(self, attrs):
        password2 = attrs.pop('password2')
        if attrs.get('password') != password2:
            raise serializers.ValidationError(
                'Passwords did not match!')
        if not attrs.get('password').isalnum(): 
            raise serializers.ValidationError(
                'Password field must be contain alpha and nums!')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(TokenObtainPairSerializer):
    password = serializers.CharField(min_length=6, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User not found')
        user = authenticate(username=email, password=password)
        if user and user.is_active:
            refresh = self.get_token(user)
            attrs['refresh'] = str(refresh)
            attrs['access'] = str(refresh.access_token)
        return attrs


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': _('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class PasswordResetApiSerializer(serializers.Serializer):
    email = serializers.EmailField()


class CreateNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=25, required=True)
    code = serializers.CharField(max_length=250, required=True)
    password = serializers.CharField(min_length=6, required=True)
    password2 = serializers.CharField(min_length=6, required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email does not exist')
        return email

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('Passwords do not match')
        return attrs

    def validate_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Activation code is not correct')
        return code

    def save(self, **kwargs):
        data = self.validated_data
        email = data.get('email')
        code = data.get('code')
        password = data.get('password')
        try:
            user = User.objects.get(email=email, activation_code=code)
        except User.DoesNotExist:
            raise serializers.ValidationError('User does not exist or code is not correct')
        user.activation_code = ''
        user.is_active = True
        user.set_password(password)
        user.save()
        return user