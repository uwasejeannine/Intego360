from rest_framework import serializers
from django.db.models import Count, Avg, Sum
from .models import (
    HealthFacilityType, HealthFacility, HealthIndicator, HealthIndicatorData,
    Disease, DiseaseCase, VaccinationCampaign, HealthAlert
)

class HealthFacilityTypeSerializer(serializers.ModelSerializer):
    """Serializer for HealthFacilityType model"""
    facilities_count = serializers.SerializerMethodField()

    class Meta:
        model = HealthFacilityType
        fields = ['id', 'name', 'level', 'description', 'facilities_count']

    def get_facilities_count(self, obj):
        return obj.facilities.count()

class HealthFacilitySerializer(serializers.ModelSerializer):
    """Serializer for HealthFacility model"""
    facility_type_name = serializers.CharField(source='facility_type.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)
    sector_name = serializers.CharField(source='sector.name', read_only=True)
    occupancy_rate = serializers.ReadOnlyField()
    total_staff = serializers.ReadOnlyField()
    
    class Meta:
        model = HealthFacility
        fields = [
            'id', 'name', 'facility_type', 'facility_type_name', 'district', 'district_name',
            'sector', 'sector_name', 'cell', 'village', 'latitude', 'longitude',
            'phone_number', 'email', 'bed_capacity', 'current_occupancy', 'occupancy_rate',
            'doctors_count', 'nurses_count', 'midwives_count', 'other_staff_count', 'total_staff',
            'emergency_services', 'maternity_services', 'laboratory_services', 'pharmacy_services',
            'radiology_services', 'surgery_services', 'has_electricity', 'has_generator',
            'has_water', 'has_internet', 'has_ambulance', 'is_operational', 'accreditation_status',
            'created_at', 'updated_at'
        ]

class HealthIndicatorSerializer(serializers.ModelSerializer):
    """Serializer for HealthIndicator model"""
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    direction_display = serializers.CharField(source='get_direction_display', read_only=True)
    latest_value = serializers.SerializerMethodField()

    class Meta:
        model = HealthIndicator
        fields = [
            'id', 'name', 'category', 'category_display', 'description',
            'unit_of_measurement', 'target_value', 'direction', 'direction_display',
            'latest_value', 'created_at', 'updated_at'
        ]

    def get_latest_value(self, obj):
        latest = obj.data_points.order_by('-year', '-month').first()
        return latest.value if latest else None

class HealthIndicatorDataSerializer(serializers.ModelSerializer):
    """Serializer for HealthIndicatorData model"""
    indicator_name = serializers.CharField(source='indicator.name', read_only=True)
    facility_name = serializers.CharField(source='facility.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)
    sector_name = serializers.CharField(source='sector.name', read_only=True)
    
    class Meta:
        model = HealthIndicatorData
        fields = [
            'id', 'indicator', 'indicator_name', 'facility', 'facility_name',
            'district', 'district_name', 'sector', 'sector_name', 'value',
            'reporting_period', 'year', 'month', 'quarter', 'data_source',
            'is_verified', 'comments', 'recorded_by', 'created_at', 'updated_at'
        ]

class DiseaseSerializer(serializers.ModelSerializer):
    """Serializer for Disease model"""
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    total_cases = serializers.SerializerMethodField()
    recent_cases = serializers.SerializerMethodField()

    class Meta:
        model = Disease
        fields = [
            'id', 'name', 'icd_code', 'category', 'category_display',
            'is_notifiable', 'is_epidemic_prone', 'prevention_measures',
            'total_cases', 'recent_cases', 'created_at', 'updated_at'
        ]

    def get_total_cases(self, obj):
        return obj.cases.count()

    def get_recent_cases(self, obj):
        from django.utils import timezone
        from datetime import timedelta
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        return obj.cases.filter(case_date__gte=thirty_days_ago).count()

class DiseaseCaseSerializer(serializers.ModelSerializer):
    """Serializer for DiseaseCase model"""
    disease_name = serializers.CharField(source='disease.name', read_only=True)
    facility_name = serializers.CharField(source='facility.name', read_only=True)
    sector_name = serializers.CharField(source='patient_residence_sector.name', read_only=True)
    age_group_display = serializers.CharField(source='get_age_group_display', read_only=True)
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    case_type_display = serializers.CharField(source='get_case_type_display', read_only=True)
    outcome_display = serializers.CharField(source='get_outcome_display', read_only=True)

    class Meta:
        model = DiseaseCase
        fields = [
            'id', 'disease', 'disease_name', 'facility', 'facility_name',
            'age_group', 'age_group_display', 'gender', 'gender_display',
            'case_date', 'case_type', 'case_type_display', 'outcome', 'outcome_display',
            'patient_residence_sector', 'sector_name', 'is_outbreak_related', 'outbreak_id',
            'reported_by', 'created_at', 'updated_at'
        ]

class VaccinationCampaignSerializer(serializers.ModelSerializer):
    """Serializer for VaccinationCampaign model"""
    target_disease_name = serializers.CharField(source='target_disease.name', read_only=True)
    districts_names = serializers.SerializerMethodField()
    facilities_names = serializers.SerializerMethodField()
    coverage_rate = serializers.ReadOnlyField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = VaccinationCampaign
        fields = [
            'id', 'name', 'vaccine_type', 'target_disease', 'target_disease_name',
            'start_date', 'end_date', 'target_population', 'target_age_groups',
            'districts', 'districts_names', 'facilities', 'facilities_names',
            'doses_administered', 'people_vaccinated', 'adverse_events',
            'coverage_rate', 'campaign_manager', 'budget_allocated', 'budget_spent',
            'status', 'status_display', 'created_at', 'updated_at'
        ]

    def get_districts_names(self, obj):
        return [district.name for district in obj.districts.all()]

    def get_facilities_names(self, obj):
        return [facility.name for facility in obj.facilities.all()]

class HealthAlertSerializer(serializers.ModelSerializer):
    """Serializer for HealthAlert model"""
    alert_type_display = serializers.CharField(source='get_alert_type_display', read_only=True)
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)
    districts_names = serializers.SerializerMethodField()
    facilities_names = serializers.SerializerMethodField()
    affected_diseases_names = serializers.SerializerMethodField()

    class Meta:
        model = HealthAlert
        fields = [
            'id', 'title', 'description', 'alert_type', 'alert_type_display',
            'severity', 'severity_display', 'districts', 'districts_names',
            'facilities', 'facilities_names', 'affected_diseases', 'affected_diseases_names',
            'start_date', 'end_date', 'is_active', 'recommended_actions',
            'response_contact', 'contact_phone', 'people_affected', 'facilities_affected',
            'response_actions_taken', 'created_by', 'created_at', 'updated_at'
        ]

    def get_districts_names(self, obj):
        return [district.name for district in obj.districts.all()]

    def get_facilities_names(self, obj):
        return [facility.name for facility in obj.facilities.all()]

    def get_affected_diseases_names(self, obj):
        return [disease.name for disease in obj.affected_diseases.all()]

class HealthStatsSerializer(serializers.Serializer):
    """Serializer for health statistics"""
    total_facilities = serializers.IntegerField()
    total_beds = serializers.IntegerField()
    total_staff = serializers.IntegerField()
    average_occupancy_rate = serializers.FloatField()
    facilities_by_type = serializers.DictField()
    facilities_by_district = serializers.DictField()
    recent_disease_cases = serializers.IntegerField()
    active_alerts = serializers.IntegerField()
    vaccination_coverage = serializers.FloatField()
    key_indicators_performance = serializers.ListField()

class HealthDashboardSerializer(serializers.Serializer):
    """Serializer for health dashboard data"""
    overview_stats = HealthStatsSerializer()
    facility_performance = HealthFacilitySerializer(many=True)
    recent_disease_cases = DiseaseCaseSerializer(many=True)
    active_alerts = HealthAlertSerializer(many=True)
    key_indicators = HealthIndicatorDataSerializer(many=True)
    vaccination_campaigns = VaccinationCampaignSerializer(many=True)