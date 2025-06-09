from django.contrib import admin
from .models import (
    Crop, Farmer, Cooperative, Season, CropProduction,
    AgricultureExtension, MarketPrice, AgricultureAlert, AgricultureTarget
)

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'growing_season', 'average_yield_per_hectare', 'market_price_per_kg']
    list_filter = ['category', 'growing_season']
    search_fields = ['name', 'scientific_name']
    ordering = ['name']

@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ['farmer_id', 'full_name', 'district', 'sector', 'total_land_hectares', 'is_cooperative_member', 'is_active']
    list_filter = ['district', 'sector', 'gender', 'education_level', 'is_cooperative_member', 'is_active']
    search_fields = ['farmer_id', 'first_name', 'last_name', 'phone_number', 'national_id']
    readonly_fields = ['farmer_id', 'full_name', 'age']
    filter_horizontal = ['main_crops']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('farmer_id', 'first_name', 'last_name', 'national_id', 'date_of_birth', 'gender', 'phone_number', 'email')
        }),
        ('Location', {
            'fields': ('district', 'sector', 'cell', 'village')
        }),
        ('Agricultural Information', {
            'fields': ('total_land_hectares', 'farming_experience_years', 'education_level', 'main_crops')
        }),
        ('Cooperative Information', {
            'fields': ('is_cooperative_member', 'cooperative_name')
        }),
        ('Financial Information', {
            'fields': ('has_bank_account', 'bank_name', 'account_number')
        }),
        ('System Information', {
            'fields': ('registered_by', 'is_active')
        }),
    )

@admin.register(Cooperative)
class CooperativeAdmin(admin.ModelAdmin):
    list_display = ['name', 'registration_number', 'district', 'sector', 'total_members', 'active_members', 'certification_status', 'is_active']
    list_filter = ['district', 'sector', 'certification_status', 'is_active']
    search_fields = ['name', 'registration_number', 'chairperson_name']
    filter_horizontal = ['crops_handled']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'registration_number', 'district', 'sector')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'email', 'physical_address')
        }),
        ('Leadership', {
            'fields': ('chairperson_name', 'chairperson_phone', 'secretary_name', 'treasurer_name')
        }),
        ('Membership', {
            'fields': ('date_established', 'total_members', 'active_members', 'female_members', 'youth_members')
        }),
        ('Financial Information', {
            'fields': ('total_assets', 'annual_revenue')
        }),
        ('Activities', {
            'fields': ('primary_activities', 'crops_handled')
        }),
        ('Status', {
            'fields': ('is_active', 'certification_status')
        }),
    )

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'start_date', 'end_date', 'total_production_tons', 'average_yield', 'is_active']
    list_filter = ['name', 'year', 'is_active']
    ordering = ['-year', 'name']

@admin.register(CropProduction)
class CropProductionAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'crop', 'season', 'area_planted_hectares', 'quantity_harvested_kg', 'yield_per_hectare', 'quality_grade']
    list_filter = ['crop', 'season', 'quality_grade', 'fertilizer_used', 'irrigation_used']
    search_fields = ['farmer__first_name', 'farmer__last_name', 'crop__name']
    readonly_fields = ['yield_per_hectare', 'total_revenue', 'loss_percentage']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('farmer', 'crop', 'season')
        }),
        ('Planting Information', {
            'fields': ('area_planted_hectares', 'planting_date', 'seed_variety', 'seed_source')
        }),
        ('Farming Practices', {
            'fields': ('fertilizer_used', 'fertilizer_type', 'fertilizer_quantity_kg', 'pesticide_used', 'pesticide_type', 'irrigation_used', 'irrigation_type')
        }),
        ('Harvest Information', {
            'fields': ('harvest_date', 'quantity_harvested_kg', 'quality_grade')
        }),
        ('Post-Harvest', {
            'fields': ('quantity_consumed_kg', 'quantity_sold_kg', 'quantity_stored_kg', 'quantity_lost_kg', 'average_selling_price')
        }),
        ('Challenges', {
            'fields': ('challenges_faced', 'pest_diseases', 'weather_impact')
        }),
        ('Calculations', {
            'fields': ('yield_per_hectare', 'total_revenue', 'loss_percentage'),
            'classes': ('collapse',)
        }),
    )

@admin.register(AgricultureExtension)
class AgricultureExtensionAdmin(admin.ModelAdmin):
    list_display = ['title', 'service_type', 'district', 'start_date', 'actual_participants', 'participation_rate', 'status']
    list_filter = ['service_type', 'district', 'status', 'start_date']
    search_fields = ['title', 'facilitator', 'venue']
    filter_horizontal = ['sectors', 'target_crops', 'target_farmers']
    readonly_fields = ['participation_rate', 'budget_utilization']

@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display = ['crop', 'district', 'market_name', 'price_per_kg', 'quality_grade', 'date_recorded', 'price_trend']
    list_filter = ['crop', 'district', 'quality_grade', 'price_trend', 'date_recorded']
    search_fields = ['crop__name', 'market_name']
    ordering = ['-date_recorded']

@admin.register(AgricultureAlert)
class AgricultureAlertAdmin(admin.ModelAdmin):
    list_display = ['title', 'alert_type', 'severity', 'start_date', 'farmers_reached', 'is_active']
    list_filter = ['alert_type', 'severity', 'is_active', 'start_date']
    search_fields = ['title', 'description']
    filter_horizontal = ['districts', 'sectors', 'affected_crops', 'target_cooperatives']

@admin.register(AgricultureTarget)
class AgricultureTargetAdmin(admin.ModelAdmin):
    list_display = ['district', 'crop', 'season', 'target_production_tons', 'achieved_production_tons', 'production_achievement_rate']
    list_filter = ['district', 'crop', 'season']
    search_fields = ['district__name', 'crop__name']
    readonly_fields = ['area_achievement_rate', 'production_achievement_rate', 'farmer_participation_rate', 'budget_utilization_rate', 'actual_yield_per_hectare']