from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from account import views


urlpatterns = [
    path('register/', views.RegistrationApiView.as_view()),
    path('activate/<uuid:activation_code>/', views.ActivationView.as_view()),
    path('login/', views.LoginApiView.as_view()),
    path('logout/', views.LogoutApiView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('password_reset/', views.PasswordResetApiView.as_view()),
    path('change_password/', views.NewPasswordApiView.as_view()),
]
