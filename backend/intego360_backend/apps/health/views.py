from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Avg, Count, Q, F
from django.utils import timezone
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from datetime import timedelta, date
import logging

from .models import (
    HealthFacilityType, HealthFacility, HealthIndicator, HealthIndicatorData,
    Disease, DiseaseCase, VaccinationCampaign, HealthAlert
)
from .serializers import (
    HealthFacilityTypeSerializer, HealthFacilitySerializer, HealthIndicatorSerializer,
    HealthIndicatorDataSerializer, DiseaseSerializer, DiseaseCaseSerializer,
    VaccinationCampaignSerializer, HealthAlertSerializer, HealthStatsSerializer,
    HealthDashboardSerializer
)
from apps.authentication.permissions import IsAdminOrReadOnly, HasDistrictAccess

logger = logging.getLogger('intego360')

class HealthFacilityTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for HealthFacilityType management"""
    queryset = HealthFacilityType.objects.all()
    serializer_class = HealthFacilityTypeSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['name']
    ordering = ['level', 'name']

class HealthFacilityViewSet(viewsets.ModelViewSet):
    """ViewSet for HealthFacility management"""
    queryset = HealthFacility.objects.select_related('facility_type', 'district', 'sector').all()
    serializer_class = HealthFacilitySerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['facility_type', 'district', 'sector', 'is_operational', 'accreditation_status']
    search_fields = ['name', 'cell', 'village']
    ordering_fields = ['name', 'bed_capacity', 'occupancy_rate']
    ordering = ['district__name', 'name']

    def get_queryset(self):
        """Filter facilities based on user permissions"""
        user = self.request.user
        if user.role == 'admin':
            return self.queryset
        elif user.role in ['mayor', 'vice_mayor'] and user.district:
            return self.queryset.filter(district=user.district)
        elif user.role in ['sector_coordinator', 'health_officer']:
            return self.queryset.filter(sector__in=user.get_accessible_sectors())
        else:
            return self.queryset.none()

    @swagger_auto_schema(
        operation_description="Get facility performance statistics",
        responses={200: "Facility statistics"}
    )
    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        """Get performance statistics for a specific facility"""
        facility = self.get_object()
        
        # Get recent disease cases (last 30 days)
        thirty_days_ago = date.today() - timedelta(days=30)
        recent_cases = facility.disease_cases.filter(case_date__gte=thirty_days_ago)
        
        # Get health indicators for this facility
        recent_indicators = facility.indicator_data.filter(
            year=timezone.now().year
        ).order_by('-month')
        
        stats = {
            'facility_info': {
                'name': facility.name,
                'type': facility.facility_type.name,
                'bed_capacity': facility.bed_capacity,
                'current_occupancy': facility.current_occupancy,
                'occupancy_rate': facility.occupancy_rate,
                'total_staff': facility.total_staff,
            },
            'recent_cases': {
                'total_cases': recent_cases.count(),
                'by_disease': list(recent_cases.values('disease__name').annotate(
                    count=Count('id')
                ).order_by('-count')),
                'by_age_group': list(recent_cases.values('age_group').annotate(
                    count=Count('id')
                )),
                'outcomes': list(recent_cases.values('outcome').annotate(
                    count=Count('id')
                )),
            },
            'services_available': {
                'emergency_services': facility.emergency_services,
                'maternity_services': facility.maternity_services,
                'laboratory_services': facility.laboratory_services,
                'pharmacy_services': facility.pharmacy_services,
                'radiology_services': facility.radiology_services,
                'surgery_services': facility.surgery_services,
            },
            'infrastructure': {
                'has_electricity': facility.has_electricity,
                'has_generator': facility.has_generator,
                'has_water': facility.has_water,
                'has_internet': facility.has_internet,
                'has_ambulance': facility.has_ambulance,
            },
            'key_indicators': HealthIndicatorDataSerializer(recent_indicators[:5], many=True).data,
        }
        
        return Response(stats)

class HealthIndicatorViewSet(viewsets.ModelViewSet):
    """ViewSet for HealthIndicator management"""
    queryset = HealthIndicator.objects.all()
    serializer_class = HealthIndicatorSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['category', 'direction']
    search_fields = ['name', 'description']
    ordering = ['category', 'name']

class HealthIndicatorDataViewSet(viewsets.ModelViewSet):
    """ViewSet for HealthIndicatorData management"""
    queryset = HealthIndicatorData.objects.select_related('indicator', 'facility', 'district', 'sector').all()
    serializer_class = HealthIndicatorDataSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['indicator', 'facility', 'district', 'sector', 'year', 'reporting_period']
    search_fields = ['indicator__name']
    ordering_fields = ['year', 'month', 'value']
    ordering = ['-year', '-month']

    def get_queryset(self):
        """Filter indicator data based on user permissions"""
        user = self.request.user
        if user.role == 'admin':
            return self.queryset
        elif user.role in ['mayor', 'vice_mayor'] and user.district:
            return self.queryset.filter(district=user.district)
        elif user.role in ['sector_coordinator', 'health_officer']:
            return self.queryset.filter(sector__in=user.get_accessible_sectors())
        else:
            return self.queryset.none()

    @swagger_auto_schema(
        operation_description="Get indicator trends",
        responses={200: "Indicator trends"}
    )
    @action(detail=False, methods=['get'])
    def trends(self, request):
        """Get trends for health indicators"""
        indicator_id = request.query_params.get('indicator')
        district_id = request.query_params.get('district')
        months = int(request.query_params.get('months', 12))
        
        queryset = self.filter_queryset(self.get_queryset())
        
        # Apply filters
        if indicator_id:
            queryset = queryset.filter(indicator_id=indicator_id)
        if district_id:
            queryset = queryset.filter(district_id=district_id)
        
        # Get trends for the specified period
        start_date = date.today().replace(day=1) - timedelta(days=30 * months)
        current_year = start_date.year
        current_month = start_date.month
        
        trends = []
        for i in range(months):
            month_data = queryset.filter(year=current_year, month=current_month).aggregate(
                avg_value=Avg('value'),
                count=Count('id')
            )
            
            trends.append({
                'year': current_year,
                'month': current_month,
                'average_value': month_data['avg_value'] or 0,
                'data_points': month_data['count']
            })
            
            current_month += 1
            if current_month > 12:
                current_month = 1
                current_year += 1
        
        return Response(trends)

class DiseaseViewSet(viewsets.ModelViewSet):
    """ViewSet for Disease management"""
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['category', 'is_notifiable', 'is_epidemic_prone']
    search_fields = ['name', 'icd_code']
    ordering = ['name']

    @swagger_auto_schema(
        operation_description="Get disease statistics",
        responses={200: "Disease statistics"}
    )
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get statistics for a specific disease"""
        disease = self.get_object()
        
        # Get user's accessible areas
        user = request.user
        cases_queryset = disease.cases.all()
        
        if user.role != 'admin':
            if user.role in ['mayor', 'vice_mayor'] and user.district:
                cases_queryset = cases_queryset.filter(facility__district=user.district)
            elif user.role in ['sector_coordinator', 'health_officer']:
                accessible_sectors = user.get_accessible_sectors()
                cases_queryset = cases_queryset.filter(facility__sector__in=accessible_sectors)
        
        # Time-based statistics
        current_year = timezone.now().year
        current_month = timezone.now().month
        
        stats = {
            'total_cases': cases_queryset.count(),
            'current_year_cases': cases_queryset.filter(case_date__year=current_year).count(),
            'current_month_cases': cases_queryset.filter(
                case_date__year=current_year, 
                case_date__month=current_month
            ).count(),
            'deaths': cases_queryset.filter(outcome='dead').count(),
            'case_fatality_rate': 0,
            'age_distribution': list(cases_queryset.values('age_group').annotate(
                count=Count('id')
            )),
            'gender_distribution': list(cases_queryset.values('gender').annotate(
                count=Count('id')
            )),
            'geographic_distribution': list(cases_queryset.values(
                'facility__district__name'
            ).annotate(count=Count('id')).order_by('-count')),
            'monthly_trends': self.get_monthly_trends(cases_queryset),
        }
        
        # Calculate case fatality rate
        if stats['total_cases'] > 0:
            stats['case_fatality_rate'] = (stats['deaths'] / stats['total_cases']) * 100
        
        return Response(stats)

    def get_monthly_trends(self, queryset):
        """Get monthly trends for disease cases"""
        trends = []
        current_date = date.today().replace(day=1)
        
        for i in range(12):
            month_start = current_date.replace(month=current_date.month - i if current_date.month > i else 12 + current_date.month - i,
                                            year=current_date.year if current_date.month > i else current_date.year - 1)
            month_end = (month_start.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
            
            month_cases = queryset.filter(
                case_date__gte=month_start,
                case_date__lte=month_end
            ).count()
            
            trends.append({
                'year': month_start.year,
                'month': month_start.month,
                'cases': month_cases
            })
        
        return reversed(trends)

class DiseaseCaseViewSet(viewsets.ModelViewSet):
    """ViewSet for DiseaseCase management"""
    queryset = DiseaseCase.objects.select_related('disease', 'facility', 'patient_residence_sector').all()
    serializer_class = DiseaseCaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['disease', 'facility', 'age_group', 'gender', 'case_type', 'outcome']
    search_fields = ['disease__name', 'facility__name']
    ordering_fields = ['case_date']
    ordering = ['-case_date']

    def get_queryset(self):
        """Filter disease cases based on user permissions"""
        user = self.request.user
        if user.role == 'admin':
            return self.queryset
        elif user.role in ['mayor', 'vice_mayor'] and user.district:
            return self.queryset.filter(facility__district=user.district)
        elif user.role in ['sector_coordinator', 'health_officer']:
            return self.queryset.filter(facility__sector__in=user.get_accessible_sectors())
        else:
            return self.queryset.none()

class VaccinationCampaignViewSet(viewsets.ModelViewSet):
    """ViewSet for VaccinationCampaign management"""
    queryset = VaccinationCampaign.objects.select_related('target_disease').prefetch_related('districts', 'facilities').all()
    serializer_class = VaccinationCampaignSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['target_disease', 'status']
    search_fields = ['name', 'vaccine_type']
    ordering_fields = ['start_date', 'coverage_rate']
    ordering = ['-start_date']

    def get_queryset(self):
        """Filter campaigns based on user permissions"""
        user = self.request.user
        if user.role == 'admin':
            return self.queryset
        elif user.role in ['mayor', 'vice_mayor'] and user.district:
            return self.queryset.filter(districts=user.district)
        elif user.role in ['sector_coordinator', 'health_officer']:
            accessible_districts = user.get_accessible_sectors().values_list('district', flat=True).distinct()
            return self.queryset.filter(districts__in=accessible_districts).distinct()
        else:
            return self.queryset.none()

class HealthAlertViewSet(viewsets.ModelViewSet):
    """ViewSet for HealthAlert management"""
    queryset = HealthAlert.objects.prefetch_related('districts', 'facilities', 'affected_diseases').all()
    serializer_class = HealthAlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['alert_type', 'severity', 'is_active']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'severity']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter alerts based on user permissions"""
        user = self.request.user
        if user.role == 'admin':
            return self.queryset
        elif user.role in ['mayor', 'vice_mayor'] and user.district:
            return self.queryset.filter(districts=user.district)
        elif user.role in ['sector_coordinator', 'health_officer']:
            accessible_districts = user.get_accessible_sectors().values_list('district', flat=True).distinct()
            return self.queryset.filter(districts__in=accessible_districts).distinct()
        else:
            return self.queryset.filter(is_active=True, districts__in=user.get_accessible_districts())

class HealthDashboardViewSet(viewsets.ViewSet):
    """ViewSet for health dashboard data"""
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get health dashboard overview",
        responses={200: HealthDashboardSerializer}
    )
    @action(detail=False, methods=['get'])
    def overview(self, request):
        """Get health dashboard overview"""
        user = request.user
        cache_key = f'health_dashboard_{user.id}'
        
        # Try to get from cache
        dashboard_data = cache.get(cache_key)
        
        if not dashboard_data:
            # Get accessible districts
            accessible_districts = user.get_accessible_districts()
            
            # Base querysets
            facilities_qs = HealthFacility.objects.filter(district__in=accessible_districts)
            
            # Overview statistics
            overview_stats = {
                'total_facilities': facilities_qs.count(),
                'total_beds': facilities_qs.aggregate(Sum('bed_capacity'))['bed_capacity__sum'] or 0,
                'total_staff': facilities_qs.aggregate(
                    total=Sum(F('doctors_count') + F('nurses_count') + F('midwives_count') + F('other_staff_count'))
                )['total'] or 0,
                'average_occupancy_rate': facilities_qs.aggregate(Avg('current_occupancy'))['current_occupancy__avg'] or 0,
                'facilities_by_type': {},
                'facilities_by_district': {},
                'recent_disease_cases': 0,
                'active_alerts': 0,
                'vaccination_coverage': 0,
                'key_indicators_performance': [],
            }
            
            # Facilities by type
            facilities_by_type = facilities_qs.values('facility_type__name').annotate(
                count=Count('id')
            )
            overview_stats['facilities_by_type'] = {
                item['facility_type__name']: item['count'] for item in facilities_by_type
            }
            
            # Facilities by district
            facilities_by_district = facilities_qs.values('district__name').annotate(
                count=Count('id')
            )
            overview_stats['facilities_by_district'] = {
                item['district__name']: item['count'] for item in facilities_by_district
            }
            
            # Recent disease cases (last 30 days)
            thirty_days_ago = date.today() - timedelta(days=30)
            overview_stats['recent_disease_cases'] = DiseaseCase.objects.filter(
                facility__district__in=accessible_districts,
                case_date__gte=thirty_days_ago
            ).count()
            
            # Active alerts
            overview_stats['active_alerts'] = HealthAlert.objects.filter(
                is_active=True,
                districts__in=accessible_districts
            ).distinct().count()
            
            # Recent data
            top_facilities = facilities_qs.order_by('-bed_capacity')[:10]
            recent_cases = DiseaseCase.objects.filter(
                facility__district__in=accessible_districts
            ).select_related('disease', 'facility').order_by('-case_date')[:20]
            
            active_alerts = HealthAlert.objects.filter(
                is_active=True,
                districts__in=accessible_districts
            ).distinct()[:5]
            
            # Key indicators
            current_year = timezone.now().year
            key_indicators = HealthIndicatorData.objects.filter(
                district__in=accessible_districts,
                year=current_year
            ).select_related('indicator').order_by('-month')[:10]
            
            # Active vaccination campaigns
            active_campaigns = VaccinationCampaign.objects.filter(
                districts__in=accessible_districts,
                status='ongoing'
            ).select_related('target_disease')[:5]
            
            dashboard_data = {
                'overview_stats': overview_stats,
                'facility_performance': HealthFacilitySerializer(top_facilities, many=True).data,
                'recent_disease_cases': DiseaseCaseSerializer(recent_cases, many=True).data,
                'active_alerts': HealthAlertSerializer(active_alerts, many=True).data,
                'key_indicators': HealthIndicatorDataSerializer(key_indicators, many=True).data,
                'vaccination_campaigns': VaccinationCampaignSerializer(active_campaigns, many=True).data,
            }
            
            # Cache for 15 minutes
            cache.set(cache_key, dashboard_data, 900)
        
        return Response(dashboard_data)