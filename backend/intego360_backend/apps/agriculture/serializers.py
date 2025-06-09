from rest_framework import serializers
from django.db.models import Sum, Avg, Count
from .models import (
    Crop, Farmer, Cooperative, Season, CropProduction, 
    AgricultureExtension, MarketPrice, AgricultureAlert, AgricultureTarget
)

class CropSerializer(serializers.ModelSerializer):
    """Serializer for Crop model"""
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    growing_season_display = serializers.CharField(source='get_growing_season_display', read_only=True)
    total_farmers = serializers.SerializerMethodField()
    total_production = serializers.SerializerMethodField()

    class Meta:
        model = Crop
        fields = [
            'id', 'name', 'scientific_name', 'category', 'category_display',
            'growing_season', 'growing_season_display', 'growth_period_days',
            'ideal_rainfall_mm', 'ideal_temperature_min', 'ideal_temperature_max',
            'average_yield_per_hectare', 'market_price_per_kg', 'total_farmers',
            'total_production', 'created_at', 'updated_at'
        ]

    def get_total_farmers(self, obj):
        return obj.main_farmers.count()

    def get_total_production(self, obj):
        return obj.productions.aggregate(
            total=Sum('quantity_harvested_kg')
        )['total'] or 0

class FarmerSerializer(serializers.ModelSerializer):
    """Serializer for Farmer model"""
    full_name = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)
    sector_name = serializers.CharField(source='sector.name', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    education_display = serializers.CharField(source='get_education_level_display', read_only=True)
    main_crops_names = serializers.SerializerMethodField()
    total_productions = serializers.SerializerMethodField()
    average_yield = serializers.SerializerMethodField()

    class Meta:
        model = Farmer
        fields = [
            'id', 'farmer_id', 'first_name', 'last_name', 'full_name',
            'national_id', 'date_of_birth', 'age', 'gender', 'gender_display',
            'phone_number', 'email', 'district', 'district_name', 
            'sector', 'sector_name', 'cell', 'village', 'total_land_hectares',
            'farming_experience_years', 'education_level', 'education_display',
            'main_crops', 'main_crops_names', 'is_cooperative_member',
            'cooperative_name', 'has_bank_account', 'bank_name', 'account_number',
            'is_active', 'total_productions', 'average_yield', 'created_at', 'updated_at'
        ]
        read_only_fields = ['full_name', 'age']

    def get_main_crops_names(self, obj):
        return [crop.name for crop in obj.main_crops.all()]

    def get_total_productions(self, obj):
        return obj.productions.count()

    def get_average_yield(self, obj):
        avg_yield = obj.productions.aggregate(
            avg_yield=Avg('quantity_harvested_kg')
        )['avg_yield']
        return round(avg_yield, 2) if avg_yield else 0

class CooperativeSerializer(serializers.ModelSerializer):
    """Serializer for Cooperative model"""
    district_name = serializers.CharField(source='district.name', read_only=True)
    sector_name = serializers.CharField(source='sector.name', read_only=True)
    certification_display = serializers.CharField(source='get_certification_status_display', read_only=True)
    crops_names = serializers.SerializerMethodField()
    member_farmers = serializers.SerializerMethodField()

    class Meta:
        model = Cooperative
        fields = [
            'id', 'name', 'registration_number', 'district', 'district_name',
            'sector', 'sector_name', 'phone_number', 'email', 'physical_address',
            'chairperson_name', 'chairperson_phone', 'secretary_name', 'treasurer_name',
            'date_established', 'total_members', 'active_members', 'female_members',
            'youth_members', 'total_assets', 'annual_revenue', 'primary_activities',
            'crops_handled', 'crops_names', 'is_active', 'certification_status',
            'certification_display', 'member_farmers', 'created_at', 'updated_at'
        ]

    def get_crops_names(self, obj):
        return [crop.name for crop in obj.crops_handled.all()]

    def get_member_farmers(self, obj):
        # Get farmers who are members of this cooperative
        return Farmer.objects.filter(
            is_cooperative_member=True,
            cooperative_name=obj.name
        ).count()

class SeasonSerializer(serializers.ModelSerializer):
    """Serializer for Season model"""
    name_display = serializers.CharField(source='get_name_display', read_only=True)
    duration_days = serializers.SerializerMethodField()
    total_farmers = serializers.SerializerMethodField()
    crops_grown = serializers.SerializerMethodField()

    class Meta:
        model = Season
        fields = [
            'id', 'name', 'name_display', 'year', 'start_date', 'end_date',
            'duration_days', 'total_rainfall_mm', 'average_temperature',
            'drought_periods', 'flood_incidents', 'total_production_tons',
            'total_area_cultivated', 'average_yield', 'total_farmers',
            'crops_grown', 'is_active', 'created_at', 'updated_at'
        ]

    def get_duration_days(self, obj):
        return (obj.end_date - obj.start_date).days

    def get_total_farmers(self, obj):
        return obj.productions.values('farmer').distinct().count()

    def get_crops_grown(self, obj):
        return obj.productions.values('crop__name').distinct().count()

class CropProductionSerializer(serializers.ModelSerializer):
    """Serializer for CropProduction model"""
    farmer_name = serializers.CharField(source='farmer.full_name', read_only=True)
    crop_name = serializers.CharField(source='crop.name', read_only=True)
    season_name = serializers.CharField(source='season.__str__', read_only=True)
    seed_source_display = serializers.CharField(source='get_seed_source_display', read_only=True)
    quality_grade_display = serializers.CharField(source='get_quality_grade_display', read_only=True)
    yield_per_hectare = serializers.ReadOnlyField()
    total_revenue = serializers.ReadOnlyField()
    loss_percentage = serializers.ReadOnlyField()

    class Meta:
        model = CropProduction
        fields = [
            'id', 'farmer', 'farmer_name', 'crop', 'crop_name', 'season', 'season_name',
            'area_planted_hectares', 'planting_date', 'seed_variety', 'seed_source',
            'seed_source_display', 'fertilizer_used', 'fertilizer_type', 'fertilizer_quantity_kg',
            'pesticide_used', 'pesticide_type', 'irrigation_used', 'irrigation_type',
            'harvest_date', 'quantity_harvested_kg', 'quality_grade', 'quality_grade_display',
            'quantity_consumed_kg', 'quantity_sold_kg', 'quantity_stored_kg',
            'quantity_lost_kg', 'average_selling_price', 'challenges_faced',
            'pest_diseases', 'weather_impact', 'yield_per_hectare', 'total_revenue',
            'loss_percentage', 'recorded_by', 'created_at', 'updated_at'
        ]

class AgricultureExtensionSerializer(serializers.ModelSerializer):
    """Serializer for AgricultureExtension model"""
    district_name = serializers.CharField(source='district.name', read_only=True)
    service_type_display = serializers.CharField(source='get_service_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    sectors_names = serializers.SerializerMethodField()
    target_crops_names = serializers.SerializerMethodField()
    participation_rate = serializers.ReadOnlyField()
    budget_utilization = serializers.ReadOnlyField()

    class Meta:
        model = AgricultureExtension
        fields = [
            'id', 'title', 'description', 'service_type', 'service_type_display',
            'district', 'district_name', 'sectors', 'sectors_names', 'target_crops',
            'target_crops_names', 'start_date', 'end_date', 'venue', 'facilitator',
            'facilitator_organization', 'target_participants', 'actual_participants',
            'male_participants', 'female_participants', 'youth_participants',
            'budget_allocated', 'budget_spent', 'materials_provided', 'knowledge_gained',
            'practices_adopted', 'feedback', 'success_rate', 'participation_rate',
            'budget_utilization', 'organized_by', 'status', 'status_display',
            'created_at', 'updated_at'
        ]

    def get_sectors_names(self, obj):
        return [sector.name for sector in obj.sectors.all()]

    def get_target_crops_names(self, obj):
        return [crop.name for crop in obj.target_crops.all()]

class MarketPriceSerializer(serializers.ModelSerializer):
    """Serializer for MarketPrice model"""
    crop_name = serializers.CharField(source='crop.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)
    quality_grade_display = serializers.CharField(source='get_quality_grade_display', read_only=True)
    supply_level_display = serializers.CharField(source='get_supply_level_display', read_only=True)
    demand_level_display = serializers.CharField(source='get_demand_level_display', read_only=True)
    price_trend_display = serializers.CharField(source='get_price_trend_display', read_only=True)
    data_source_display = serializers.CharField(source='get_data_source_display', read_only=True)

    class Meta:
        model = MarketPrice
        fields = [
            'id', 'crop', 'crop_name', 'district', 'district_name', 'market_name',
            'price_per_kg', 'currency', 'quality_grade', 'quality_grade_display',
            'supply_level', 'supply_level_display', 'demand_level', 'demand_level_display',
            'quantity_available_kg', 'price_trend', 'price_trend_display',
            'data_source', 'data_source_display', 'collected_by', 'date_recorded',
            'created_at', 'updated_at'
        ]

class AgricultureAlertSerializer(serializers.ModelSerializer):
    """Serializer for AgricultureAlert model"""
    alert_type_display = serializers.CharField(source='get_alert_type_display', read_only=True)
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)
    districts_names = serializers.SerializerMethodField()
    sectors_names = serializers.SerializerMethodField()
    affected_crops_names = serializers.SerializerMethodField()

    class Meta:
        model = AgricultureAlert
        fields = [
            'id', 'title', 'description', 'alert_type', 'alert_type_display',
            'severity', 'severity_display', 'districts', 'districts_names',
            'sectors', 'sectors_names', 'affected_crops', 'affected_crops_names',
            'start_date', 'end_date', 'is_active', 'recommended_actions',
            'resources_available', 'contact_person', 'contact_phone',
            'farmers_reached', 'cooperatives_notified', 'actions_taken',
            'effectiveness_score', 'created_by', 'created_at', 'updated_at'
        ]

    def get_districts_names(self, obj):
        return [district.name for district in obj.districts.all()]

    def get_sectors_names(self, obj):
        return [sector.name for sector in obj.sectors.all()]

    def get_affected_crops_names(self, obj):
        return [crop.name for crop in obj.affected_crops.all()]

class AgricultureTargetSerializer(serializers.ModelSerializer):
    """Serializer for AgricultureTarget model"""
    district_name = serializers.CharField(source='district.name', read_only=True)
    sector_name = serializers.CharField(source='sector.name', read_only=True)
    crop_name = serializers.CharField(source='crop.name', read_only=True)
    season_name = serializers.CharField(source='season.__str__', read_only=True)
    area_achievement_rate = serializers.ReadOnlyField()
    production_achievement_rate = serializers.ReadOnlyField()
    farmer_participation_rate = serializers.ReadOnlyField()
    budget_utilization_rate = serializers.ReadOnlyField()
    actual_yield_per_hectare = serializers.ReadOnlyField()

    class Meta:
        model = AgricultureTarget
        fields = [
            'id', 'district', 'district_name', 'sector', 'sector_name',
            'crop', 'crop_name', 'season', 'season_name', 'target_area_hectares',
            'target_production_tons', 'target_yield_tons_per_hectare', 'target_farmers',
            'allocated_budget', 'budget_for_seeds', 'budget_for_fertilizers',
            'budget_for_extension', 'achieved_area_hectares', 'achieved_production_tons',
            'farmers_participating', 'budget_utilized', 'area_achievement_rate',
            'production_achievement_rate', 'farmer_participation_rate',
            'budget_utilization_rate', 'actual_yield_per_hectare', 'set_by',
            'created_at', 'updated_at'
        ]

class AgricultureStatsSerializer(serializers.Serializer):
    """Serializer for agriculture statistics"""
    total_farmers = serializers.IntegerField()
    total_cooperatives = serializers.IntegerField()
    total_crops = serializers.IntegerField()
    total_production_current_season = serializers.FloatField()
    total_area_cultivated = serializers.FloatField()
    average_yield = serializers.FloatField()
    top_crops = serializers.ListField()
    farmers_by_district = serializers.DictField()
    production_by_season = serializers.ListField()
    market_prices_trend = serializers.ListField()
    active_alerts = serializers.IntegerField()
    extension_services_count = serializers.IntegerField()

class AgricultureDashboardSerializer(serializers.Serializer):
    """Serializer for agriculture dashboard data"""
    overview_stats = AgricultureStatsSerializer()
    recent_productions = CropProductionSerializer(many=True)
    active_alerts = AgricultureAlertSerializer(many=True)
    current_season_targets = AgricultureTargetSerializer(many=True)
    market_prices = MarketPriceSerializer(many=True)
    upcoming_extensions = AgricultureExtensionSerializer(many=True)