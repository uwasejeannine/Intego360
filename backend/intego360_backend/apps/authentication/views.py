from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import login, logout
from django.utils import timezone
from django.db.models import Count, Q
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging
import traceback

from .models import User, District, Sector, UserProfile, UserSession, ActivityLog
from .serializers import (
    UserSerializer, DistrictSerializer, SectorSerializer,
    LoginSerializer, ChangePasswordSerializer, UserSessionSerializer,
    ActivityLogSerializer, UserStatsSerializer, DashboardStatsSerializer
)
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin

logger = logging.getLogger('intego360')

class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT token view with additional user info"""
    
    @swagger_auto_schema(
        operation_description="Obtain JWT tokens for authentication",
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="Successful authentication",
                examples={
                    "application/json": {
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "user": {
                            "id": 1,
                            "username": "mayor_gasabo",
                            "full_name": "John Doe",
                            "role": "mayor",
                            "district": "Gasabo"
                        }
                    }
                }
            ),
            400: "Invalid credentials"
        }
    )
    def post(self, request, *args, **kwargs):
        # Add debugging
        logger.info(f"Login attempt - Headers: {dict(request.headers)}")
        logger.info(f"Login attempt - Body: {request.body}")
        logger.info(f"Login attempt - Data: {request.data}")
        logger.info(f"Login attempt - Content-Type: {request.content_type}")
        
        try:
            serializer = LoginSerializer(data=request.data)
            logger.info(f"Serializer data: {serializer.initial_data}")
            
            if not serializer.is_valid():
                logger.error(f"Serializer validation errors: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            user = serializer.validated_data['user']
            
            # Reset failed login attempts on successful login
            user.failed_login_attempts = 0
            user.last_login_ip = self.get_client_ip(request)
            user.save()
            
            # Clean up old sessions for this user (optional - keep only last 5 sessions)
            self.cleanup_old_sessions(user)
            
            # Create user session
            self.create_user_session(request, user)
            
            # Log the login activity
            ActivityLog.objects.create(
                user=user,
                action='login',
                description='User logged in successfully',
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            # Update profile login count
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.total_logins += 1
            profile.last_activity = timezone.now()
            profile.save()
            
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'full_name': user.get_full_name(),
                    'role': user.role,
                    'role_verbose': user.get_role_display(),
                    'district': user.district.name if user.district else None,
                    'permissions': self.get_user_permissions(user),
                    'preferred_language': user.preferred_language,
                }
            })
            
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            logger.error(f"Login error traceback: {traceback.format_exc()}")
            return Response(
                {'error': 'Internal server error'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def create_user_session(self, request, user):
        """Create user session record"""
        import uuid
        from django.utils import timezone
        
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        device_type = self.detect_device_type(user_agent)
        browser = self.detect_browser(user_agent)
        
        # Generate a unique session key
        session_key = request.session.session_key
        if not session_key:
            # Create a unique session key using user ID and timestamp
            session_key = f"api_session_{user.id}_{int(timezone.now().timestamp())}_{uuid.uuid4().hex[:8]}"
        
        # Check if session already exists and update it instead of creating new
        session, created = UserSession.objects.get_or_create(
            user=user,
            session_key=session_key,
            defaults={
                'ip_address': self.get_client_ip(request),
                'user_agent': user_agent,
                'device_type': device_type,
                'browser': browser,
                'is_active': True,
                'login_time': timezone.now(),
            }
        )
        
        # If session already exists, update it
        if not created:
            session.ip_address = self.get_client_ip(request)
            session.user_agent = user_agent
            session.device_type = device_type
            session.browser = browser
            session.is_active = True
            session.login_time = timezone.now()
            session.save()
    
    def cleanup_old_sessions(self, user, keep_count=5):
        """Clean up old sessions for a user, keeping only the most recent ones"""
        old_sessions = UserSession.objects.filter(user=user).order_by('-login_time')[keep_count:]
        if old_sessions.exists():
            UserSession.objects.filter(
                id__in=[session.id for session in old_sessions]
            ).delete()
    
    def detect_device_type(self, user_agent):
        """Detect device type from user agent"""
        user_agent = user_agent.lower()
        if 'mobile' in user_agent or 'android' in user_agent or 'iphone' in user_agent:
            return 'mobile'
        elif 'tablet' in user_agent or 'ipad' in user_agent:
            return 'tablet'
        else:
            return 'desktop'
    
    def detect_browser(self, user_agent):
        """Detect browser from user agent"""
        user_agent = user_agent.lower()
        if 'chrome' in user_agent:
            return 'Chrome'
        elif 'firefox' in user_agent:
            return 'Firefox'
        elif 'safari' in user_agent:
            return 'Safari'
        elif 'edge' in user_agent:
            return 'Edge'
        else:
            return 'Other'
    
    def get_user_permissions(self, user):
        """Get user permissions based on role"""
        permissions = {
            'can_view_agriculture': user.can_view_sector_data('agriculture'),
            'can_view_health': user.can_view_sector_data('health'),
            'can_view_education': user.can_view_sector_data('education'),
            'can_manage_users': user.role == 'admin',
            'can_generate_reports': user.role in ['admin', 'mayor', 'vice_mayor', 'data_analyst'],
            'can_manage_alerts': user.role in ['admin', 'mayor', 'vice_mayor'],
            'can_export_data': user.role in ['admin', 'mayor', 'vice_mayor', 'data_analyst'],
        }
        return permissions

class DistrictViewSet(viewsets.ModelViewSet):
    """ViewSet for District management"""
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['province']
    search_fields = ['name', 'code', 'province']
    ordering_fields = ['name', 'population', 'area_km2']
    ordering = ['name']

    @swagger_auto_schema(
        operation_description="Get district statistics",
        responses={200: "District statistics"}
    )
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get statistics for a specific district"""
        district = self.get_object()
        
        stats = {
            'total_sectors': district.sectors.count(),
            'total_users': district.users.count(),
            'users_by_role': dict(
                district.users.values('role').annotate(count=Count('role')).values_list('role', 'count')
            ),
            'population': district.population,
            'area_km2': district.area_km2,
            'population_density': district.population / district.area_km2 if district.area_km2 > 0 else 0,
        }
        
        return Response(stats)

class SectorViewSet(viewsets.ModelViewSet):
    """ViewSet for Sector management"""
    queryset = Sector.objects.select_related('district').all()
    serializer_class = SectorSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['district']
    search_fields = ['name', 'code', 'district__name']
    ordering_fields = ['name', 'population', 'area_km2']
    ordering = ['district__name', 'name']

    def get_queryset(self):
        """Filter sectors based on user permissions"""
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
            return user.get_accessible_sectors()

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User management"""
    queryset = User.objects.select_related('district').prefetch_related('sectors').all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['role', 'district', 'is_active', 'is_verified']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering_fields = ['username', 'first_name', 'last_name', 'created_at']
    ordering = ['-created_at']

    def get_permissions(self):
        """Set permissions based on action"""
        if self.action in ['create', 'destroy']:
            self.permission_classes = [permissions.IsAdminUser]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsOwnerOrAdmin]
        return super().get_permissions()

    def get_queryset(self):
        """Filter users based on permissions"""
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
            return self.queryset.filter(id=user.id)

    @swagger_auto_schema(
        operation_description="Get current user profile",
        responses={200: UserSerializer}
    )
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update current user profile",
        request_body=UserSerializer,
        responses={200: UserSerializer}
    )
    @action(detail=False, methods=['patch'])
    def update_profile(self, request):
        """Update current user's profile"""
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # Log the activity
        ActivityLog.objects.create(
            user=request.user,
            action='update_profile',
            description='User updated their profile',
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Change user password",
        request_body=ChangePasswordSerializer,
        responses={200: "Password changed successfully"}
    )
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Change user password"""
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # Log the activity
        ActivityLog.objects.create(
            user=user,
            action='change_password',
            description='User changed their password',
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return Response({'message': 'Password changed successfully'})

    @swagger_auto_schema(
        operation_description="Get user statistics",
        responses={200: UserStatsSerializer}
    )
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def stats(self, request):
        """Get user statistics (admin only)"""
        cache_key = 'user_stats'
        stats = cache.get(cache_key)
        
        if not stats:
            total_users = User.objects.count()
            active_users = User.objects.filter(is_active=True).count()
            verified_users = User.objects.filter(is_verified=True).count()
            
            users_by_role = dict(
                User.objects.values('role').annotate(count=Count('role')).values_list('role', 'count')
            )
            
            users_by_district = dict(
                User.objects.filter(district__isnull=False)
                .values('district__name').annotate(count=Count('district'))
                .values_list('district__name', 'count')
            )
            
            recent_registrations = User.objects.filter(
                created_at__gte=timezone.now() - timezone.timedelta(days=30)
            ).count()
            
            current_sessions = UserSession.objects.filter(is_active=True).count()
            
            stats = {
                'total_users': total_users,
                'active_users': active_users,
                'verified_users': verified_users,
                'users_by_role': users_by_role,
                'users_by_district': users_by_district,
                'recent_registrations': recent_registrations,
                'current_sessions': current_sessions,
            }
            
            # Cache for 15 minutes
            cache.set(cache_key, stats, 900)
        
        serializer = UserStatsSerializer(stats)
        return Response(serializer.data)

    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class UserSessionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for UserSession management (read-only)"""
    queryset = UserSession.objects.select_related('user').all()
    serializer_class = UserSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['user', 'is_active', 'device_type', 'browser']
    search_fields = ['user__username', 'ip_address', 'location']
    ordering_fields = ['login_time', 'last_activity']
    ordering = ['-login_time']

    def get_queryset(self):
        """Filter sessions based on user permissions"""
        # Skip authentication/filtering during schema generation
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()
            
        user = self.request.user
        if not user.is_authenticated or not hasattr(user, 'role'):
            return self.queryset.none()
            
        if user.role == 'admin':
            return self.queryset
        else:
            return self.queryset.filter(user=user)

    @swagger_auto_schema(
        operation_description="Get current user sessions",
        responses={200: UserSessionSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def current_user_sessions(self, request):
        """Get current user's sessions"""
        sessions = self.queryset.filter(user=request.user, is_active=True)
        serializer = self.get_serializer(sessions, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Terminate a user session",
        responses={200: "Session terminated successfully"}
    )
    @action(detail=True, methods=['post'])
    def terminate(self, request, pk=None):
        """Terminate a specific session"""
        session = self.get_object()
        
        # Only allow users to terminate their own sessions or admins to terminate any
        if session.user != request.user and request.user.role != 'admin':
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        session.is_active = False
        session.logout_time = timezone.now()
        session.save()
        
        # Log the activity
        ActivityLog.objects.create(
            user=request.user,
            action='logout',
            description=f'Session terminated for user {session.user.username}',
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return Response({'message': 'Session terminated successfully'})

    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class ActivityLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for ActivityLog management (read-only)"""
    queryset = ActivityLog.objects.select_related('user', 'district', 'sector').all()
    serializer_class = ActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['user', 'action', 'district', 'sector', 'resource_type']
    search_fields = ['user__username', 'description', 'action']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']

    def get_queryset(self):
        """Filter activity logs based on user permissions"""
        # Skip authentication/filtering during schema generation
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()
            
        user = self.request.user
        if not user.is_authenticated or not hasattr(user, 'role'):
            return self.queryset.none()
            
        if user.role == 'admin':
            return self.queryset
        elif user.role in ['mayor', 'vice_mayor'] and user.district:
            return self.queryset.filter(
                Q(district=user.district) | Q(user=user)
            )
        else:
            return self.queryset.filter(user=user)

    @swagger_auto_schema(
        operation_description="Get current user's activity logs",
        responses={200: ActivityLogSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def my_activities(self, request):
        """Get current user's activity logs"""
        activities = self.queryset.filter(user=request.user)[:50]  # Last 50 activities
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Get activity statistics",
        responses={200: "Activity statistics"}
    )
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def stats(self, request):
        """Get activity statistics (admin only)"""
        from django.db.models import Count
        from django.utils import timezone
        from datetime import timedelta
        
        # Get date range from query params
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        activities = self.queryset.filter(timestamp__gte=start_date)
        
        stats = {
            'total_activities': activities.count(),
            'activities_by_action': dict(
                activities.values('action').annotate(count=Count('action')).values_list('action', 'count')
            ),
            'activities_by_user': dict(
                activities.values('user__username').annotate(count=Count('user'))
                .values_list('user__username', 'count')[:10]  # Top 10 users
            ),
            'activities_by_day': [],
            'most_active_districts': dict(
                activities.exclude(district__isnull=True)
                .values('district__name').annotate(count=Count('district'))
                .values_list('district__name', 'count')[:5]
            ),
        }
        
        # Get daily activity counts
        for i in range(days):
            date = (timezone.now() - timedelta(days=i)).date()
            count = activities.filter(timestamp__date=date).count()
            stats['activities_by_day'].append({
                'date': date.isoformat(),
                'count': count
            })
        
        return Response(stats)

class DashboardViewSet(viewsets.ViewSet):
    """ViewSet for dashboard data"""
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get dashboard overview statistics",
        responses={200: DashboardStatsSerializer}
    )
    @action(detail=False, methods=['get'])
    def overview(self, request):
        """Get dashboard overview statistics"""
        user = request.user
        
        # Check authentication for non-schema generation
        if not user.is_authenticated or not hasattr(user, 'role'):
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
            
        cache_key = f'dashboard_overview_{user.id}'
        stats = cache.get(cache_key)
        
        if not stats:
            # Get accessible districts and sectors
            accessible_districts = user.get_accessible_districts()
            accessible_sectors = user.get_accessible_sectors()
            
            # Get basic counts
            total_districts = accessible_districts.count()
            total_sectors = accessible_sectors.count()
            total_users = User.objects.filter(
                Q(district__in=accessible_districts) if accessible_districts.exists() else Q()
            ).count()
            
            # Get active alerts (this will be implemented in alerts app)
            active_alerts = 0  # Placeholder
            
            # System health check
            system_health = 'Good'  # Placeholder - implement actual health check
            
            # Last data sync (placeholder)
            last_data_sync = timezone.now()
            
            # Performance score (placeholder)
            performance_score = 85.5
            
            stats = {
                'total_districts': total_districts,
                'total_sectors': total_sectors,
                'total_users': total_users,
                'active_alerts': active_alerts,
                'system_health': system_health,
                'last_data_sync': last_data_sync,
                'performance_score': performance_score,
            }
            
            # Cache for 5 minutes
            cache.set(cache_key, stats, 300)
        
        serializer = DashboardStatsSerializer(stats)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Get user's recent activities",
        responses={200: ActivityLogSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def recent_activities(self, request):
        """Get user's recent activities for dashboard"""
        activities = ActivityLog.objects.filter(user=request.user).order_by('-timestamp')[:10]
        serializer = ActivityLogSerializer(activities, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Log user dashboard view",
        responses={200: "Activity logged"}
    )
    @action(detail=False, methods=['post'])
    def log_view(self, request):
        """Log dashboard view activity"""
        # Update user profile dashboard views
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.dashboard_views += 1
        profile.last_activity = timezone.now()
        profile.save()
        
        # Log the activity
        ActivityLog.objects.create(
            user=request.user,
            action='view_dashboard',
            description='User viewed dashboard',
            ip_address=self.get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            district=request.user.district,
        )
        
        return Response({'message': 'Dashboard view logged'})

    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip