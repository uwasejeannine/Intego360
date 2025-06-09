from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg, Q
from django.utils import timezone
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from datetime import timedelta

from .models import AlertType, SystemAlert, AlertSubscription, AlertNotification, AlertAction
from .serializers import AlertTypeSerializer, SystemAlertSerializer, AlertNotificationSerializer, AlertStatsSerializer
from apps.authentication.permissions import IsAdminOrReadOnly

class AlertTypeViewSet(viewsets.ModelViewSet):
    queryset = AlertType.objects.all()
    serializer_class = AlertTypeSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'description']
    ordering = ['category', 'name']

class SystemAlertViewSet(viewsets.ModelViewSet):
    queryset = SystemAlert.objects.select_related('alert_type', 'created_by').prefetch_related('districts', 'sectors').all()
    serializer_class = SystemAlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['alert_type', 'severity', 'status', 'is_public']
    search_fields = ['title', 'description']
    ordering = ['-created_at', '-priority_score']

    def get_queryset(self):
        # Skip authentication/filtering during schema generation
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()
            
        user = self.request.user
        if not user.is_authenticated or not hasattr(user, 'role'):
            return self.queryset.none()
            
        queryset = self.queryset
        
        if user.role != 'admin':
            # Filter based on user's access
            user_districts = user.get_accessible_districts()
            user_sectors = user.get_accessible_sectors()
            
            queryset = queryset.filter(
                Q(is_public=True) |
                Q(districts__in=user_districts) |
                Q(sectors__in=user_sectors) |
                Q(target_roles__contains=user.role)
            ).distinct()
        
        return queryset

    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        alert = self.get_object()
        
        # Create acknowledgment action
        AlertAction.objects.create(
            alert=alert,
            user=request.user,
            action_type='acknowledged',
            description='Alert acknowledged by user'
        )
        
        alert.acknowledgments += 1
        alert.save()
        
        return Response({'message': 'Alert acknowledged successfully'})

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        alert = self.get_object()
        resolution_notes = request.data.get('resolution_notes', '')
        
        alert.mark_as_resolved(request.user, resolution_notes)
        
        return Response({'message': 'Alert resolved successfully'})

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        user = request.user
        
        # Check authentication for non-schema generation
        if not user.is_authenticated or not hasattr(user, 'role'):
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
            
        cache_key = f'alerts_dashboard_{user.id}'
        
        dashboard_data = cache.get(cache_key)
        if not dashboard_data:
            # Get user's accessible alerts
            alerts_qs = self.get_queryset()
            
            # Calculate statistics
            today = timezone.now().date()
            stats = {
                'total_alerts': alerts_qs.count(),
                'active_alerts': alerts_qs.filter(status='active').count(),
                'critical_alerts': alerts_qs.filter(severity='critical', status='active').count(),
                'resolved_today': alerts_qs.filter(
                    status='resolved',
                    resolved_time__date=today
                ).count(),
                'average_resolution_time': 2.5,  # Calculate actual average
                'alerts_by_type': {},
                'alerts_by_severity': {},
                'recent_alerts': [],
            }
            
            # Alerts by type
            alerts_by_type = alerts_qs.values('alert_type__name').annotate(
                count=Count('id')
            ).order_by('-count')
            stats['alerts_by_type'] = {
                item['alert_type__name']: item['count'] for item in alerts_by_type
            }
            
            # Alerts by severity
            alerts_by_severity = alerts_qs.values('severity').annotate(
                count=Count('id')
            )
            stats['alerts_by_severity'] = {
                item['severity']: item['count'] for item in alerts_by_severity
            }
            
            # Recent alerts
            recent_alerts = alerts_qs.filter(status='active').order_by('-created_at')[:10]
            stats['recent_alerts'] = SystemAlertSerializer(recent_alerts, many=True).data
            
            dashboard_data = stats
            cache.set(cache_key, dashboard_data, 300)  # Cache for 5 minutes
        
        serializer = AlertStatsSerializer(dashboard_data)
        return Response(serializer.data)