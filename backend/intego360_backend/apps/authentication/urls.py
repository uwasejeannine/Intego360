from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomTokenObtainPairView, DistrictViewSet, SectorViewSet,
    UserViewSet, UserSessionViewSet, ActivityLogViewSet, DashboardViewSet
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r'districts', DistrictViewSet)
router.register(r'sectors', SectorViewSet)
router.register(r'users', UserViewSet)
router.register(r'sessions', UserSessionViewSet)
router.register(r'activities', ActivityLogViewSet)
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = [
    # JWT Authentication
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Router URLs
    path('', include(router.urls)),
]