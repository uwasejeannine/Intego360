from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DashboardWidgetViewSet, UserDashboardPreferenceViewSet,
    DashboardSnapshotViewSet, DashboardAnalyticsViewSet
)

router = DefaultRouter()
router.register(r'widgets', DashboardWidgetViewSet)
router.register(r'preferences', UserDashboardPreferenceViewSet)
router.register(r'snapshots', DashboardSnapshotViewSet)
router.register(r'analytics', DashboardAnalyticsViewSet, basename='dashboard-analytics')

urlpatterns = [
    path('', include(router.urls)),
]