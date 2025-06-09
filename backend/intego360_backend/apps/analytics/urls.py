from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnalyticsReportViewSet, AIModelViewSet, PredictionViewSet, AnalyticsDashboardViewSet

router = DefaultRouter()
router.register(r'reports', AnalyticsReportViewSet)
router.register(r'models', AIModelViewSet)
router.register(r'predictions', PredictionViewSet)
router.register(r'dashboard', AnalyticsDashboardViewSet, basename='analytics-dashboard')

urlpatterns = [
    path('', include(router.urls)),
]