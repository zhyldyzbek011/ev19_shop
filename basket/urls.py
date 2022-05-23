from django.urls import path
from basket import views

urlpatterns = [
    path('order/', views.BasketApiView.as_view())
]
