from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger API Documentation Setup
schema_view = get_schema_view(
    openapi.Info(
        title="Intego360 API",
        default_version='v1',
        description="Comprehensive API for Rwanda Local Government Digital Platform",
        terms_of_service="https://www.intego360.rw/terms/",
        contact=openapi.Contact(email="support@intego360.rw"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
    # API Endpoints
    path('api/v1/auth/', include('apps.authentication.urls')),
    path('api/v1/dashboard/', include('apps.dashboard.urls')),
    path('api/v1/agriculture/', include('apps.agriculture.urls')),
    path('api/v1/health/', include('apps.health.urls')),
    path('api/v1/education/', include('apps.education.urls')),
    path('api/v1/analytics/', include('apps.analytics.urls')),
    path('api/v1/alerts/', include('apps.alerts.urls')),
]

# Static and Media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom Admin Configuration
admin.site.site_header = "Intego360 Administration"
admin.site.site_title = "Intego360 Admin Portal"
admin.site.index_title = "Welcome to Intego360 Administration"