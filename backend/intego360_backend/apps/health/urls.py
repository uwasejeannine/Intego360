from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    HealthFacilityTypeViewSet, HealthFacilityViewSet, HealthIndicatorViewSet,
    HealthIndicatorDataViewSet, DiseaseViewSet, DiseaseCaseViewSet,
    VaccinationCampaignViewSet, HealthAlertViewSet, HealthDashboardViewSet
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r'facility-types', HealthFacilityTypeViewSet)
router.register(r'facilities', HealthFacilityViewSet)
router.register(r'indicators', HealthIndicatorViewSet)
router.register(r'indicator-data', HealthIndicatorDataViewSet)
router.register(r'diseases', DiseaseViewSet)
router.register(r'disease-cases', DiseaseCaseViewSet)
router.register(r'vaccination-campaigns', VaccinationCampaignViewSet)
router.register(r'alerts', HealthAlertViewSet)
router.register(r'dashboard', HealthDashboardViewSet, basename='health-dashboard')

urlpatterns = [
    path('', include(router.urls)),
]