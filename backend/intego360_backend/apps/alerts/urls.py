# backend/apps/alerts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlertTypeViewSet, SystemAlertViewSet

router = DefaultRouter()
router.register(r'types', AlertTypeViewSet)
router.register(r'alerts', SystemAlertViewSet)

urlpatterns = [
    path('', include(router.urls)),
]