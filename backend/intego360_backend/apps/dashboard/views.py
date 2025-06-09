from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg, Sum, Q
from django.utils import timezone
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from datetime import timedelta, date

from .models import DashboardWidget, UserDashboardPreference, DashboardSnapshot, DashboardUsageAnalytics
from .serializers import (
    DashboardWidgetSerializer, UserDashboardPreferenceSerializer,
    DashboardSnapshotSerializer, DashboardStatsSerializer
)
from apps.authentication.permissions import IsAdminOrReadOnly

class DashboardWidgetViewSet(viewsets.ModelViewSet):
    queryset = DashboardWidget.objects.prefetch_related('districts').all()
    serializer_class = DashboardWidgetSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['widget_type', 'data_source', 'is_active', 'is_featured', 'is_public']
    search_fields = ['name', 'title', 'description']
    ordering = ['name']

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
                Q(allowed_roles__contains=user.role)
            ).distinct()
        
        return queryset

    @action(detail=True, methods=['get'])
    def data(self, request, pk=None):
        """Get widget data from its configured data source"""
        widget = self.get_object()
        
        # Here you would implement the logic to fetch data from the widget's data source
        # This is a placeholder implementation
        
        if widget.data_source == 'agriculture':
            # Fetch agriculture data
            data = {
                'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                'datasets': [{
                    'label': 'Crop Production',
                    'data': [12, 19, 3, 5, 2, 3],
                    'backgroundColor': 'rgba(34, 197, 94, 0.2)',
                    'borderColor': 'rgba(34, 197, 94, 1)',
                }]
            }
        elif widget.data_source == 'health':
            # Fetch health data
            data = {
                'labels': ['Malaria', 'TB', 'Diarrhea', 'Respiratory'],
                'datasets': [{
                    'label': 'Cases',
                    'data': [300, 50, 100, 200],
                    'backgroundColor': ['#ef4444', '#f97316', '#eab308', '#22c55e'],
                }]
            }
        elif widget.data_source == 'education':
            # Fetch education data
            data = {
                'labels': ['Primary', 'Secondary', 'TVET', 'University'],
                'datasets': [{
                    'label': 'Enrollment',
                    'data': [85, 72, 45, 28],
                    'backgroundColor': 'rgba(59, 130, 246, 0.2)',
                    'borderColor': 'rgba(59, 130, 246, 1)',
                }]
            }
        else:
            data = {'message': 'No data available'}
        
        # Update usage count
        widget.usage_count += 1
        widget.save()
        
        return Response(data)

class UserDashboardPreferenceViewSet(viewsets.ModelViewSet):
    queryset = UserDashboardPreference.objects.select_related('user').prefetch_related('enabled_widgets').all()
    serializer_class = UserDashboardPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Skip authentication/filtering during schema generation
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()
            
        user = self.request.user
        if not user.is_authenticated:
            return self.queryset.none()
            
        # Users can only access their own preferences
        return self.queryset.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get', 'post'])
    def my_preferences(self, request):
        """Get or update current user's dashboard preferences"""
        try:
            preferences = UserDashboardPreference.objects.get(user=request.user)
        except UserDashboardPreference.DoesNotExist:
            preferences = UserDashboardPreference.objects.create(user=request.user)
        
        if request.method == 'GET':
            serializer = self.get_serializer(preferences)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            serializer = self.get_serializer(preferences, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class DashboardSnapshotViewSet(viewsets.ModelViewSet):
    queryset = DashboardSnapshot.objects.select_related('user').all()
    serializer_class = DashboardSnapshotSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['is_public', 'file_format']
    search_fields = ['name', 'description']
    ordering = ['-snapshot_date']

    def get_queryset(self):
        # Skip authentication/filtering during schema generation
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()
            
        user = self.request.user
        if not user.is_authenticated:
            return self.queryset.none()
            
        return self.queryset.filter(
            Q(user=user) |
            Q(is_public=True) |
            Q(shared_with_users=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def share(self, request, pk=None):
        """Share snapshot with other users"""
        snapshot = self.get_object()
        
        if snapshot.user != request.user:
            return Response(
                {'error': 'You can only share your own snapshots'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        user_ids = request.data.get('user_ids', [])
        roles = request.data.get('roles', [])
        
        if user_ids:
            from apps.authentication.models import User
            users = User.objects.filter(id__in=user_ids)
            snapshot.shared_with_users.set(users)
        
        if roles:
            snapshot.shared_with_roles = roles
            snapshot.save()
        
        return Response({'message': 'Snapshot shared successfully'})

class DashboardAnalyticsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def overview(self, request):
        """Get dashboard usage analytics overview"""
        user = request.user
        cache_key = f'dashboard_analytics_{user.id}'
        
        analytics_data = cache.get(cache_key)
        if not analytics_data:
            # Check if user is authenticated and has role attribute
            if not user.is_authenticated or not hasattr(user, 'role'):
                return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
                
            # Calculate analytics based on user's access level
            if user.role == 'admin':
                usage_qs = DashboardUsageAnalytics.objects.all()
            else:
                # Users can only see their own analytics or district-level aggregates
                usage_qs = DashboardUsageAnalytics.objects.filter(user=user)
            
            today = timezone.now().date()
            
            stats = {
                'total_users': usage_qs.values('user').distinct().count(),
                'active_users_today': usage_qs.filter(login_time__date=today).values('user').distinct().count(),
                'total_widgets': DashboardWidget.objects.filter(is_active=True).count(),
                'popular_widgets': [],
                'average_session_duration': usage_qs.aggregate(
                    avg_duration=Avg('total_session_duration_minutes')
                )['avg_duration'] or 0,
                'total_page_views': usage_qs.aggregate(
                    total_views=Sum('page_view_count')
                )['total_views'] or 0,
                'usage_by_device': {},
                'usage_by_section': {},
            }
            
            # Popular widgets
            popular_widgets = DashboardWidget.objects.filter(
                is_active=True
            ).order_by('-usage_count')[:5]
            stats['popular_widgets'] = DashboardWidgetSerializer(popular_widgets, many=True).data
            
            # Usage by device
            device_usage = usage_qs.values('device_type').annotate(
                count=Count('id')
            )
            stats['usage_by_device'] = {
                item['device_type']: item['count'] for item in device_usage
            }
            
            # Usage by section
            section_usage = usage_qs.values('most_viewed_section').annotate(
                count=Count('id')
            ).exclude(most_viewed_section='')
            stats['usage_by_section'] = {
                item['most_viewed_section']: item['count'] for item in section_usage
            }
            
            analytics_data = stats
            cache.set(cache_key, analytics_data, 1800)  # Cache for 30 minutes
        
        serializer = DashboardStatsSerializer(analytics_data)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def track_usage(self, request):
        """Track user dashboard usage"""
        data = request.data
        
        # Create or update usage analytics
        usage, created = DashboardUsageAnalytics.objects.get_or_create(
            user=request.user,
            session_id=data.get('session_id'),
            defaults={
                'device_type': data.get('device_type', 'desktop'),
                'browser': data.get('browser', ''),
                'login_time': timezone.now(),
            }
        )
        
        if not created:
            # Update existing usage record
            usage.logout_time = timezone.now()
            usage.total_session_duration_minutes = data.get('session_duration', 0)
            usage.page_view_count = data.get('page_views', 0)
            usage.widget_interaction_count = data.get('widget_interactions', 0)
            usage.most_viewed_section = data.get('most_viewed_section', '')
            usage.save()
        
        return Response({'message': 'Usage tracked successfully'})