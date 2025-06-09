from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CropViewSet, FarmerViewSet, CooperativeViewSet, SeasonViewSet,
    CropProductionViewSet, AgricultureExtensionViewSet, MarketPriceViewSet,
    AgricultureAlertViewSet, AgricultureTargetViewSet, AgricultureDashboardViewSet
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r'crops', CropViewSet)
router.register(r'farmers', FarmerViewSet)
router.register(r'cooperatives', CooperativeViewSet)
router.register(r'seasons', SeasonViewSet)
router.register(r'productions', CropProductionViewSet)
router.register(r'extensions', AgricultureExtensionViewSet)
router.register(r'market-prices', MarketPriceViewSet)
router.register(r'alerts', AgricultureAlertViewSet)
router.register(r'targets', AgricultureTargetViewSet)
router.register(r'dashboard', AgricultureDashboardViewSet, basename='agriculture-dashboard')

urlpatterns = [
    path('', include(router.urls)),
]