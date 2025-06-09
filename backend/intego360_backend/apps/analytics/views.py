from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg, Q
from django.utils import timezone
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from datetime import timedelta

from .models import AnalyticsReport, DataSource, AIModel, Prediction
from .serializers import (
    AnalyticsReportSerializer, AIModelSerializer, PredictionSerializer,
    AnalyticsStatsSerializer
)
from apps.authentication.permissions import IsAdminOrReadOnly

class AnalyticsReportViewSet(viewsets.ModelViewSet):
    queryset = AnalyticsReport.objects.prefetch_related('districts', 'sectors').all()
    serializer_class = AnalyticsReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['report_type', 'status', 'is_automated', 'is_public']
    search_fields = ['name', 'description']
    ordering = ['-created_at']

    def get_queryset(self):
        # Skip authentication/filtering during schema generation
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()
            
        user = self.request.user
        if not user.is_authenticated or not hasattr(user, 'role'):
            return self.queryset.none()
            
        queryset = self.queryset
        
        if user.role != 'admin':
            user_districts = user.get_accessible_districts()
            queryset = queryset.filter(
                Q(is_public=True) |
                Q(districts__in=user_districts) |
                Q(shared_with_roles__contains=user.role)
            ).distinct()
        
        return queryset

    @action(detail=True, methods=['post'])
    def generate(self, request, pk=None):
        report = self.get_object()
        
        # Here you would implement the actual report generation logic
        # For now, we'll simulate it
        
        report.status = 'generating'
        report.save()
        
        # In a real implementation, this would be an async task
        # generate_report_async.delay(report.id)
        
        return Response({'message': 'Report generation started'})

class AIModelViewSet(viewsets.ModelViewSet):
    queryset = AIModel.objects.all()
    serializer_class = AIModelSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['model_type', 'framework', 'deployment_status', 'is_active']
    search_fields = ['name', 'description', 'algorithm']
    ordering = ['name']

    @action(detail=True, methods=['post'])
    def predict(self, request, pk=None):
        model = self.get_object()
        input_data = request.data.get('input_data', {})
        
        if not model.is_active:
            return Response(
                {'error': 'Model is not active'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Here you would implement the actual prediction logic
        # For now, we'll create a dummy prediction
        
        prediction = Prediction.objects.create(
            model=model,
            sector=request.data.get('sector', 'cross_sector'),
            input_data=input_data,
            prediction_result={'dummy': 'prediction'},
            confidence_score=0.85,
            prediction_type='forecast',
            requested_by=request.user
        )
        
        serializer = PredictionSerializer(prediction)
        return Response(serializer.data)

class PredictionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Prediction.objects.select_related('model', 'district').all()
    serializer_class = PredictionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['model', 'sector', 'district', 'prediction_type', 'is_validated']
    ordering = ['-created_at']

    def get_queryset(self):
        # Skip authentication/filtering during schema generation
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()
            
        user = self.request.user
        if not user.is_authenticated or not hasattr(user, 'role'):
            return self.queryset.none()
            
        if user.role == 'admin':
            return self.queryset
        elif user.role in ['mayor', 'vice_mayor'] and user.district:
            return self.queryset.filter(district=user.district)
        else:
            accessible_districts = user.get_accessible_districts()
            return self.queryset.filter(district__in=accessible_districts)

class AnalyticsDashboardViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def overview(self, request):
        user = request.user
        
        # Check authentication for non-schema generation
        if not user.is_authenticated or not hasattr(user, 'role'):
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
            
        cache_key = f'analytics_dashboard_{user.id}'
        
        dashboard_data = cache.get(cache_key)
        if not dashboard_data:
            # Get accessible data based on user permissions
            accessible_districts = user.get_accessible_districts()
            
            # Calculate statistics
            reports_qs = AnalyticsReport.objects.filter(
                Q(is_public=True) |
                Q(districts__in=accessible_districts)
            ).distinct()
            
            predictions_qs = Prediction.objects.filter(
                district__in=accessible_districts
            )
            
            stats = {
                'total_reports': reports_qs.count(),
                'active_models': AIModel.objects.filter(is_active=True).count(),
                'recent_predictions': predictions_qs.filter(
                    created_at__gte=timezone.now() - timedelta(days=7)
                ).count(),
                'average_accuracy': predictions_qs.filter(
                    is_validated=True
                ).aggregate(Avg('accuracy_assessment'))['accuracy_assessment__avg'] or 0,
                'reports_by_type': {},
                'predictions_by_sector': {},
                'data_quality_score': 0.85,  # Calculate from actual data sources
            }
            
            # Reports by type
            reports_by_type = reports_qs.values('report_type').annotate(
                count=Count('id')
            )
            stats['reports_by_type'] = {
                item['report_type']: item['count'] for item in reports_by_type
            }
            
            # Predictions by sector
            predictions_by_sector = predictions_qs.values('sector').annotate(
                count=Count('id')
            )
            stats['predictions_by_sector'] = {
                item['sector']: item['count'] for item in predictions_by_sector
            }
            
            dashboard_data = stats
            cache.set(cache_key, dashboard_data, 900)  # Cache for 15 minutes
        
        serializer = AnalyticsStatsSerializer(dashboard_data)
        return Response(serializer.data)