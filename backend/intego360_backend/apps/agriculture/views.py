from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Avg, Count, Q, F
from django.utils import timezone
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import timedelta, date
import logging

from .models import (
    Crop, Farmer, Cooperative, Season, CropProduction,
    AgricultureExtension, MarketPrice, AgricultureAlert, AgricultureTarget
)
from .serializers import (
    CropSerializer, FarmerSerializer, CooperativeSerializer, SeasonSerializer,
    CropProductionSerializer, AgricultureExtensionSerializer, MarketPriceSerializer,
    AgricultureAlertSerializer, AgricultureTargetSerializer, AgricultureStatsSerializer,
    AgricultureDashboardSerializer
)
from apps.authentication.permissions import (
    IsAdminOrReadOnly, CanViewSectorData, HasDistrictAccess
)

logger = logging.getLogger('intego360')

class CropViewSet(viewsets.ModelViewSet):
    """ViewSet for Crop management"""
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['category', 'growing_season']
    search_fields = ['name', 'scientific_name']
    ordering_fields = ['name', 'category', 'average_yield_per_hectare']
    ordering = ['name']

    @swagger_auto_schema(
        operation_description="Get crop production statistics",
        responses={200: "Crop statistics"}
    )
    @action(detail=True, methods=['get'])
    def production_stats(self, request, pk=None):
        """Get production statistics for a specific crop"""
        crop = self.get_object()
        current_year = timezone.now().year
        
        # Get current season productions
        current_season_productions = crop.productions.filter(
            season__year=current_year
        )
        
        stats = {
            'total_farmers_current_season': current_season_productions.values('farmer').distinct().count(),
            'total_area_planted': current_season_productions.aggregate(
                total=Sum('area_planted_hectares')
            )['total'] or 0,
            'total_production': current_season_productions.aggregate(
                total=Sum('quantity_harvested_kg')
            )['total'] or 0,
            'average_yield': current_season_productions.aggregate(
                avg=Avg('quantity_harvested_kg')
            )['avg'] or 0,
            'districts_growing': current_season_productions.values(
                'farmer__district__name'
            ).distinct().count(),
            'price_trend': self.get_price_trend(crop),
            'seasonal_performance': self.get_seasonal_performance(crop),
        }
        
        return Response(stats)

    def get_price_trend(self, crop):
        """Get price trend for the crop over last 6 months"""
        six_months_ago = date.today() - timedelta(days=180)
        prices = MarketPrice.objects.filter(
            crop=crop,
            date_recorded__gte=six_months_ago
        ).values('date_recorded', 'price_per_kg').order_by('date_recorded')
        
        return list(prices)

    def get_seasonal_performance(self, crop):
        """Get performance across different seasons"""
        seasons = Season.objects.filter(
            year__gte=timezone.now().year - 2
        ).order_by('-year', 'name')
        
        performance = []
        for season in seasons:
            productions = crop.productions.filter(season=season)
            if productions.exists():
                performance.append({
                    'season': str(season),
                    'total_area': productions.aggregate(Sum('area_planted_hectares'))['area_planted_hectares__sum'] or 0,
                    'total_production': productions.aggregate(Sum('quantity_harvested_kg'))['quantity_harvested_kg__sum'] or 0,
                    'farmers_count': productions.values('farmer').distinct().count(),
                    'average_yield': productions.aggregate(Avg('quantity_harvested_kg'))['quantity_harvested_kg__avg'] or 0,
                })
        
        return performance

class FarmerViewSet(viewsets.ModelViewSet):
    """ViewSet for Farmer management"""
    queryset = Farmer.objects.select_related('district', 'sector').prefetch_related('main_crops').all()
    serializer_class = FarmerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['district', 'sector', 'gender', 'education_level', 'is_cooperative_member']
    search_fields = ['first_name', 'last_name', 'farmer_id', 'phone_number']
    ordering_fields = ['last_name', 'created_at', 'total_land_hectares']
    ordering = ['last_name', 'first_name']

    def get_queryset(self):
        """Filter farmers based on user permissions"""
        user = self.request.user
        if user.role == 'admin':
            return self.queryset
        elif user.role in ['mayor', 'vice_mayor'] and user.district:
            return self.queryset.filter(district=user.district)
        elif user.role in ['sector_coordinator', 'agriculture_officer']:
            return self.queryset.filter(sector__in=user.get_accessible_sectors())
        else:
            return self.queryset.none()

    @swagger_auto_schema(
        operation_description="Get farmer production history",
        responses={200: CropProductionSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def production_history(self, request, pk=None):
        """Get production history for a specific farmer"""
        farmer = self.get_object()
        productions = farmer.productions.select_related('crop', 'season').order_by('-season__year', '-harvest_date')
        
        # Pagination
        page = self.paginate_queryset(productions)
        if page is not None:
            serializer = CropProductionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = CropProductionSerializer(productions, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Get farmer statistics",
        responses={200: "Farmer statistics"}
    )
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get statistics for a specific farmer"""
        farmer = self.get_object()
        
        productions = farmer.productions.all()
        current_season_productions = productions.filter(
            season__year=timezone.now().year
        )
        
        stats = {
            'total_seasons_participated': productions.values('season').distinct().count(),
            'total_crops_grown': productions.values('crop').distinct().count(),
            'lifetime_production': productions.aggregate(
                total=Sum('quantity_harvested_kg')
            )['total'] or 0,
            'lifetime_revenue': sum([p.total_revenue for p in productions]),
            'average_yield_per_hectare': productions.aggregate(
                avg=Avg('quantity_harvested_kg')
            )['avg'] or 0,
            'current_season_crops': current_season_productions.count(),
            'current_season_area': current_season_productions.aggregate(
                total=Sum('area_planted_hectares')
            )['total'] or 0,
            'fertilizer_usage_rate': (productions.filter(fertilizer_used=True).count() / 
                                    productions.count() * 100) if productions.count() > 0 else 0,
            'irrigation_usage_rate': (productions.filter(irrigation_used=True).count() / 
                                    productions.count() * 100) if productions.count() > 0 else 0,
        }
        
        return Response(stats)

class CooperativeViewSet(viewsets.ModelViewSet):
    """ViewSet for Cooperative management"""
    queryset = Cooperative.objects.select_related('district', 'sector').prefetch_related('crops_handled').all()
    serializer_class = CooperativeSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['district', 'sector', 'certification_status', 'is_active']
    search_fields = ['name', 'registration_number', 'chairperson_name']
    ordering_fields = ['name', 'total_members', 'date_established']
    ordering = ['name']

    def get_queryset(self):
        """Filter cooperatives based on user permissions"""
        user = self.request.user
        if user.role == 'admin':
            return self.queryset
        elif user.role in ['mayor', 'vice_mayor'] and user.district:
            return self.queryset.filter(district=user.district)
        elif user.role in ['sector_coordinator', 'agriculture_officer']:
            return self.queryset.filter(sector__in=user.get_accessible_sectors())
        else:
            return self.queryset.none()

    @swagger_auto_schema(
        operation_description="Get cooperative performance statistics",
        responses={200: "Cooperative statistics"}
    )
    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        """Get performance statistics for a specific cooperative"""
        cooperative = self.get_object()
        
        # Get member farmers
        member_farmers = Farmer.objects.filter(
            cooperative_name=cooperative.name,
            is_cooperative_member=True
        )
        
        # Get current season data
        current_year = timezone.now().year
        member_productions = CropProduction.objects.filter(
            farmer__in=member_farmers,
            season__year=current_year
        )
        
        stats = {
            'verified_members': member_farmers.count(),
            'active_farmers_current_season': member_productions.values('farmer').distinct().count(),
            'total_area_cultivated': member_productions.aggregate(
                total=Sum('area_planted_hectares')
            )['total'] or 0,
            'total_production': member_productions.aggregate(
                total=Sum('quantity_harvested_kg')
            )['total'] or 0,
            'crops_grown': member_productions.values('crop__name').distinct().count(),
            'average_yield': member_productions.aggregate(
                avg=Avg('quantity_harvested_kg')
            )['avg'] or 0,
            'total_revenue': sum([p.total_revenue for p in member_productions]),
            'female_participation_rate': (cooperative.female_members / cooperative.total_members * 100) 
                                       if cooperative.total_members > 0 else 0,
            'youth_participation_rate': (cooperative.youth_members / cooperative.total_members * 100) 
                                      if cooperative.total_members > 0 else 0,
        }
        
        return Response(stats)

class SeasonViewSet(viewsets.ModelViewSet):
    """ViewSet for Season management"""
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['name', 'year', 'is_active']
    search_fields = ['name', 'year']
    ordering_fields = ['year', 'name', 'start_date']
    ordering = ['-year', 'name']

    @swagger_auto_schema(
        operation_description="Get season performance statistics",
        responses={200: "Season statistics"}
    )
    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        """Get performance statistics for a specific season"""
        season = self.get_object()
        
        productions = season.productions.select_related('crop', 'farmer__district')
        
        stats = {
            'total_farmers': productions.values('farmer').distinct().count(),
            'total_area_planted': productions.aggregate(Sum('area_planted_hectares'))['area_planted_hectares__sum'] or 0,
            'total_production': productions.aggregate(Sum('quantity_harvested_kg'))['quantity_harvested_kg__sum'] or 0,
            'crops_grown': productions.values('crop__name').distinct().count(),
            'districts_participating': productions.values('farmer__district__name').distinct().count(),
            'average_yield': productions.aggregate(Avg('quantity_harvested_kg'))['quantity_harvested_kg__avg'] or 0,
            'fertilizer_adoption_rate': (productions.filter(fertilizer_used=True).count() / 
                                       productions.count() * 100) if productions.count() > 0 else 0,
            'irrigation_adoption_rate': (productions.filter(irrigation_used=True).count() / 
                                       productions.count() * 100) if productions.count() > 0 else 0,
            'crop_breakdown': list(productions.values('crop__name').annotate(
                farmers=Count('farmer', distinct=True),
                area=Sum('area_planted_hectares'),
                production=Sum('quantity_harvested_kg')
            )),
            'district_breakdown': list(productions.values('farmer__district__name').annotate(
                farmers=Count('farmer', distinct=True),
                area=Sum('area_planted_hectares'),
                production=Sum('quantity_harvested_kg')
            )),
        }
        
        return Response(stats)

class CropProductionViewSet(viewsets.ModelViewSet):
    """ViewSet for CropProduction management"""
    queryset = CropProduction.objects.select_related('farmer', 'crop', 'season').all()
    serializer_class = CropProductionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['farmer__district', 'farmer__sector', 'crop', 'season', 'quality_grade']
    search_fields = ['farmer__first_name', 'farmer__last_name', 'crop__name']
    ordering_fields = ['harvest_date', 'quantity_harvested_kg', 'created_at']
    ordering = ['-harvest_date']

    def get_queryset(self):
        """Filter productions based on user permissions"""
        user = self.request.user
        if user.role == 'admin':
            return self.queryset
        elif user.role in ['mayor', 'vice_mayor'] and user.district:
            return self.queryset.filter(farmer__district=user.district)
        elif user.role in ['sector_coordinator', 'agriculture_officer']:
            return self.queryset.filter(farmer__sector__in=user.get_accessible_sectors())
        else:
            return self.queryset.none()

    @swagger_auto_schema(
        operation_description="Get production analytics",
        responses={200: "Production analytics"}
    )
    @action(detail=False, methods=['get'])
    def analytics(self, request):
        """Get production analytics"""
        queryset = self.filter_queryset(self.get_queryset())
        
        # Get query parameters
        year = request.query_params.get('year', timezone.now().year)
        crop_id = request.query_params.get('crop')
        district_id = request.query_params.get('district')
        
        # Apply filters
        if year:
            queryset = queryset.filter(season__year=year)
        if crop_id:
            queryset = queryset.filter(crop_id=crop_id)
        if district_id:
            queryset = queryset.filter(farmer__district_id=district_id)
        
        analytics = {
            'total_productions': queryset.count(),
            'total_farmers': queryset.values('farmer').distinct().count(),
            'total_area': queryset.aggregate(Sum('area_planted_hectares'))['area_planted_hectares__sum'] or 0,
            'total_harvest': queryset.aggregate(Sum('quantity_harvested_kg'))['quantity_harvested_kg__sum'] or 0,
            'average_yield': queryset.aggregate(Avg('quantity_harvested_kg'))['quantity_harvested_kg__avg'] or 0,
            'total_revenue': sum([p.total_revenue for p in queryset]),
            'crop_distribution': list(queryset.values('crop__name').annotate(
                count=Count('id'),
                total_area=Sum('area_planted_hectares'),
                total_production=Sum('quantity_harvested_kg')
            ).order_by('-total_production')),
            'monthly_harvest_trend': self.get_monthly_harvest_trend(queryset),
            'yield_comparison': self.get_yield_comparison(queryset),
        }
        
        return Response(analytics)

    def get_monthly_harvest_trend(self, queryset):
        """Get monthly harvest trend"""
        from django.db.models import Extract
        
        monthly_data = queryset.filter(
            harvest_date__isnull=False
        ).annotate(
            month=Extract('harvest_date', 'month')
        ).values('month').annotate(
            total_harvest=Sum('quantity_harvested_kg'),
            farmers_count=Count('farmer', distinct=True)
        ).order_by('month')
        
        return list(monthly_data)

    def get_yield_comparison(self, queryset):
        """Get yield comparison by crop"""
        crop_yields = queryset.values('crop__name').annotate(
            avg_yield_per_hectare=Avg(F('quantity_harvested_kg') / F('area_planted_hectares')),
            target_yield=Avg('crop__average_yield_per_hectare')
        ).order_by('-avg_yield_per_hectare')
        
        return list(crop_yields)

class AgricultureExtensionViewSet(viewsets.ModelViewSet):
    """ViewSet for AgricultureExtension management"""
    queryset = AgricultureExtension.objects.select_related('district').prefetch_related('sectors', 'target_crops').all()
    serializer_class = AgricultureExtensionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['district', 'service_type', 'status']
    search_fields = ['title', 'facilitator', 'venue']
    ordering_fields = ['start_date', 'success_rate', 'actual_participants']
    ordering = ['-start_date']

    def get_queryset(self):
        """Filter extensions based on user permissions"""
        user = self.request.user
        if user.role == 'admin':
            return self.queryset
        elif user.role in ['mayor', 'vice_mayor'] and user.district:
            return self.queryset.filter(district=user.district)
        elif user.role in ['sector_coordinator', 'agriculture_officer']:
            return self.queryset.filter(sectors__in=user.get_accessible_sectors()).distinct()
        else:
            return self.queryset.none()

class MarketPriceViewSet(viewsets.ModelViewSet):
    """ViewSet for MarketPrice management"""
    queryset = MarketPrice.objects.select_related('crop', 'district').all()
    serializer_class = MarketPriceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['crop', 'district', 'quality_grade', 'price_trend']
    search_fields = ['crop__name', 'market_name']
    ordering_fields = ['date_recorded', 'price_per_kg']
    ordering = ['-date_recorded']

    def get_queryset(self):
        """Filter market prices based on user permissions"""
        user = self.request.user
        if user.role == 'admin':
            return self.queryset
        elif user.role in ['mayor', 'vice_mayor'] and user.district:
            return self.queryset.filter(district=user.district)
        elif user.role in ['sector_coordinator', 'agriculture_officer']:
            accessible_districts = user.get_accessible_sectors().values_list('district', flat=True).distinct()
            return self.queryset.filter(district__in=accessible_districts)
        else:
            return self.queryset.none()

    @swagger_auto_schema(
        operation_description="Get price trends for crops",
        responses={200: "Price trends"}
    )
    @action(detail=False, methods=['get'])
    def trends(self, request):
        """Get price trends for crops"""
        # Get query parameters
        crop_id = request.query_params.get('crop')
        days = int(request.query_params.get('days', 30))
        
        start_date = date.today() - timedelta(days=days)
        queryset = self.filter_queryset(self.get_queryset()).filter(
            date_recorded__gte=start_date
        )
        
        if crop_id:
            queryset = queryset.filter(crop_id=crop_id)
        
        # Group by crop and date
        trends = {}
        for price in queryset.order_by('crop__name', 'date_recorded'):
            crop_name = price.crop.name
            if crop_name not in trends:
                trends[crop_name] = []
            
            trends[crop_name].append({
                'date': price.date_recorded,
                'price': float(price.price_per_kg),
                'market': price.market_name,
                'district': price.district.name
            })
        
        return Response(trends)

class AgricultureAlertViewSet(viewsets.ModelViewSet):
    """ViewSet for AgricultureAlert management"""
    queryset = AgricultureAlert.objects.prefetch_related('districts', 'sectors', 'affected_crops').all()
    serializer_class = AgricultureAlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['alert_type', 'severity', 'is_active']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'severity', 'start_date']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter alerts based on user permissions"""
        user = self.request.user
        if user.role == 'admin':
            return self.queryset
        elif user.role in ['mayor', 'vice_mayor'] and user.district:
            return self.queryset.filter(districts=user.district)
        elif user.role in ['sector_coordinator', 'agriculture_officer']:
            accessible_districts = user.get_accessible_sectors().values_list('district', flat=True).distinct()
            return self.queryset.filter(districts__in=accessible_districts).distinct()
        else:
            return self.queryset.filter(is_active=True, districts__in=user.get_accessible_districts())

class AgricultureTargetViewSet(viewsets.ModelViewSet):
    """ViewSet for AgricultureTarget management"""
    queryset = AgricultureTarget.objects.select_related('district', 'sector', 'crop', 'season').all()
    serializer_class = AgricultureTargetSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['district', 'sector', 'crop', 'season']
    search_fields = ['crop__name', 'district__name']
    ordering_fields = ['season__year', 'target_production_tons']
    ordering = ['-season__year', 'district__name']

    def get_queryset(self):
        """Filter targets based on user permissions"""
        user = self.request.user
        if user.role == 'admin':
            return self.queryset
        elif user.role in ['mayor', 'vice_mayor'] and user.district:
            return self.queryset.filter(district=user.district)
        elif user.role in ['sector_coordinator', 'agriculture_officer']:
            return self.queryset.filter(sector__in=user.get_accessible_sectors())
        else:
            return self.queryset.none()

class AgricultureDashboardViewSet(viewsets.ViewSet):
    """ViewSet for agriculture dashboard data"""
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get agriculture dashboard overview",
        responses={200: AgricultureDashboardSerializer}
    )
    @action(detail=False, methods=['get'])
    def overview(self, request):
        """Get agriculture dashboard overview"""
        user = request.user
        cache_key = f'agriculture_dashboard_{user.id}'
        
        # Try to get from cache
        dashboard_data = cache.get(cache_key)
        
        if not dashboard_data:
            # Get accessible districts and sectors
            accessible_districts = user.get_accessible_districts()
            accessible_sectors = user.get_accessible_sectors()
            
            # Base querysets
            farmers_qs = Farmer.objects.filter(district__in=accessible_districts)
            cooperatives_qs = Cooperative.objects.filter(district__in=accessible_districts)
            current_year = timezone.now().year
            
            # Overview statistics
            overview_stats = {
                'total_farmers': farmers_qs.count(),
                'total_cooperatives': cooperatives_qs.filter(is_active=True).count(),
                'total_crops': Crop.objects.count(),
                'total_production_current_season': 0,
                'total_area_cultivated': 0,
                'average_yield': 0,
                'top_crops': [],
                'farmers_by_district': {},
                'production_by_season': [],
                'market_prices_trend': [],
                'active_alerts': 0,
                'extension_services_count': 0,
            }
            
            # Current season production data
            current_productions = CropProduction.objects.filter(
                farmer__district__in=accessible_districts,
                season__year=current_year
            )
            
            if current_productions.exists():
                production_stats = current_productions.aggregate(
                    total_production=Sum('quantity_harvested_kg'),
                    total_area=Sum('area_planted_hectares'),
                    avg_yield=Avg('quantity_harvested_kg')
                )
                
                overview_stats.update({
                    'total_production_current_season': production_stats['total_production'] or 0,
                    'total_area_cultivated': production_stats['total_area'] or 0,
                    'average_yield': production_stats['avg_yield'] or 0,
                })
                
                # Top crops by production
                top_crops = current_productions.values('crop__name').annotate(
                    total_production=Sum('quantity_harvested_kg'),
                    farmers_count=Count('farmer', distinct=True),
                    area=Sum('area_planted_hectares')
                ).order_by('-total_production')[:5]
                
                overview_stats['top_crops'] = list(top_crops)
            
            # Farmers by district
            farmers_by_district = farmers_qs.values('district__name').annotate(
                count=Count('id')
            )
            overview_stats['farmers_by_district'] = {
                item['district__name']: item['count'] for item in farmers_by_district
            }
            
            # Active alerts
            overview_stats['active_alerts'] = AgricultureAlert.objects.filter(
                is_active=True,
                districts__in=accessible_districts
            ).distinct().count()
            
            # Extension services
            overview_stats['extension_services_count'] = AgricultureExtension.objects.filter(
                district__in=accessible_districts,
                status__in=['planned', 'ongoing']
            ).count()
            
            # Recent data
            recent_productions = current_productions.select_related(
                'farmer', 'crop', 'season'
            ).order_by('-harvest_date')[:10]
            
            active_alerts = AgricultureAlert.objects.filter(
                is_active=True,
                districts__in=accessible_districts
            ).distinct()[:5]
            
            current_season_targets = AgricultureTarget.objects.filter(
                district__in=accessible_districts,
                season__year=current_year
            ).select_related('district', 'crop', 'season')[:10]
            
            # Market prices (last 7 days)
            recent_date = date.today() - timedelta(days=7)
            market_prices = MarketPrice.objects.filter(
                district__in=accessible_districts,
                date_recorded__gte=recent_date
            ).select_related('crop', 'district').order_by('-date_recorded')[:20]
            
            upcoming_extensions = AgricultureExtension.objects.filter(
                district__in=accessible_districts,
                start_date__gte=date.today(),
                status='planned'
            ).select_related('district').order_by('start_date')[:5]
            
            dashboard_data = {
                'overview_stats': overview_stats,
                'recent_productions': CropProductionSerializer(recent_productions, many=True).data,
                'active_alerts': AgricultureAlertSerializer(active_alerts, many=True).data,
                'current_season_targets': AgricultureTargetSerializer(current_season_targets, many=True).data,
                'market_prices': MarketPriceSerializer(market_prices, many=True).data,
                'upcoming_extensions': AgricultureExtensionSerializer(upcoming_extensions, many=True).data,
            }
            
            # Cache for 15 minutes
            cache.set(cache_key, dashboard_data, 900)
        
        return Response(dashboard_data)