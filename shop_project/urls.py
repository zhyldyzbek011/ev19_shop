from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from order.views import CreateOrderView, UserOrderList, UpdateOrderStatusView

schema_view = get_schema_view(openapi.Info(
      title="Blog project API",
      default_version='v1',
      description="This is test blog project.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)




urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('product.urls')),
    path('api/v1/basket/', include('basket.urls')), #cart
    path('api/v1/account/', include('account.urls')),
    path('api/v1/orders/', CreateOrderView.as_view()),
    path('api/v1/orders/own/', UserOrderList.as_view()),
    path('api/v1/orders/<int:pk>/', UpdateOrderStatusView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

