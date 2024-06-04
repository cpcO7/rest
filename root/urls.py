from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from root.settings import MEDIA_ROOT, MEDIA_URL, STATIC_URL, STATIC_ROOT

schema_view = get_schema_view(
    openapi.Info(
        title="Samarrrr's API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api-auth/', include('rest_framework.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.urls')),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
