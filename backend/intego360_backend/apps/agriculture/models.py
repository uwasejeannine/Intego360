from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.authentication.models import District, Sector, User

class Crop(models.Model):
    """Model for different crop types"""
    name = models.CharField(max_length=100, unique=True)
    scientific_name = models.CharField(max_length=150, blank=True)
    category = models.CharField(max_length=50, choices=[
        ('cereals', _('Cereals')),
        ('legumes', _('Legumes')),
        ('tubers', _('Tubers')),
        ('vegetables', _('Vegetables')),
        ('fruits', _('Fruits')),
        ('cash_crops', _('Cash Crops')),
    ])
    growing_season = models.CharField(max_length=20, choices=[
        ('season_a', _('Season A (Sep-Jan)')),
        ('season_b', _('Season B (Feb-Jun)')),
        ('season_c', _('Season C (Jul-Aug)')),
        ('year_round', _('Year Round')),
    ])
    growth_period_days = models.IntegerField(help_text="Days from planting to harvest")
    ideal_rainfall_mm = models.FloatField(help_text="Ideal annual rainfall in mm")
    ideal_temperature_min = models.FloatField(help_text="Minimum temperature in Celsius")
    ideal_temperature_max = models.FloatField(help_text="Maximum temperature in Celsius")
    
    # Economic data
    average_yield_per_hectare = models.FloatField(default=0.0, help_text="Average yield in tons per hectare")
    market_price_per_kg = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Crop")
        verbose_name_plural = _("Crops")
        ordering = ['name']

    def __str__(self):
        return self.name

class Farmer(models.Model):
    """Model for farmer registration"""
    GENDER_CHOICES = [
        ('M', _('Male')),
        ('F', _('Female')),
    ]
    
    EDUCATION_CHOICES = [
        ('none', _('No formal education')),
        ('primary', _('Primary education')),
        ('secondary', _('Secondary education')),
        ('vocational', _('Vocational training')),
        ('university', _('University education')),
    ]

    # Personal Information
    farmer_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    national_id = models.CharField(max_length=16, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    
    # Location
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='farmers')
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='farmers')
    cell = models.CharField(max_length=50)
    village = models.CharField(max_length=50)
    
    # Agricultural Information
    total_land_hectares = models.FloatField(default=0.0)
    farming_experience_years = models.IntegerField(default=0)
    education_level = models.CharField(max_length=20, choices=EDUCATION_CHOICES, default='primary')
    main_crops = models.ManyToManyField(Crop, related_name='main_farmers')
    
    # Cooperative Information
    is_cooperative_member = models.BooleanField(default=False)
    cooperative_name = models.CharField(max_length=100, blank=True)
    
    # Financial Information
    has_bank_account = models.BooleanField(default=False)
    bank_name = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=20, blank=True)
    
    # System Information
    registered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='registered_farmers')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Farmer")
        verbose_name_plural = _("Farmers")
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.farmer_id})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        from django.utils import timezone
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

class Cooperative(models.Model):
    """Model for farmer cooperatives"""
    name = models.CharField(max_length=100, unique=True)
    registration_number = models.CharField(max_length=20, unique=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='cooperatives')
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='cooperatives')
    
    # Contact Information
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    physical_address = models.TextField()
    
    # Leadership
    chairperson_name = models.CharField(max_length=100)
    chairperson_phone = models.CharField(max_length=15)
    secretary_name = models.CharField(max_length=100, blank=True)
    treasurer_name = models.CharField(max_length=100, blank=True)
    
    # Organizational Details
    date_established = models.DateField()
    total_members = models.IntegerField(default=0)
    active_members = models.IntegerField(default=0)
    female_members = models.IntegerField(default=0)
    youth_members = models.IntegerField(default=0)  # Under 35 years
    
    # Financial Information
    total_assets = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    annual_revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    # Activities
    primary_activities = models.TextField(help_text="Main activities of the cooperative")
    crops_handled = models.ManyToManyField(Crop, related_name='cooperatives')
    
    # Status
    is_active = models.BooleanField(default=True)
    certification_status = models.CharField(max_length=20, choices=[
        ('pending', _('Pending')),
        ('certified', _('Certified')),
        ('suspended', _('Suspended')),
        ('revoked', _('Revoked')),
    ], default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Cooperative")
        verbose_name_plural = _("Cooperatives")
        ordering = ['name']

    def __str__(self):
        return self.name

class Season(models.Model):
    """Model for agricultural seasons"""
    name = models.CharField(max_length=20, choices=[
        ('season_a', _('Season A')),
        ('season_b', _('Season B')),
        ('season_c', _('Season C')),
    ])
    year = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Weather data
    total_rainfall_mm = models.FloatField(default=0.0)
    average_temperature = models.FloatField(default=0.0)
    drought_periods = models.IntegerField(default=0, help_text="Number of drought periods")
    flood_incidents = models.IntegerField(default=0, help_text="Number of flood incidents")
    
    # Performance metrics
    total_production_tons = models.FloatField(default=0.0)
    total_area_cultivated = models.FloatField(default=0.0)
    average_yield = models.FloatField(default=0.0)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Season")
        verbose_name_plural = _("Seasons")
        ordering = ['-year', 'name']
        unique_together = ['name', 'year']

    def __str__(self):
        return f"{self.get_name_display()} {self.year}"

class CropProduction(models.Model):
    """Model for crop production records"""
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='productions')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='productions')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='productions')
    
    # Planting Information
    area_planted_hectares = models.FloatField(validators=[MinValueValidator(0)])
    planting_date = models.DateField()
    seed_variety = models.CharField(max_length=100, blank=True)
    seed_source = models.CharField(max_length=20, choices=[
        ('own', _('Own seeds')),
        ('purchased', _('Purchased')),
        ('government', _('Government supplied')),
        ('cooperative', _('Cooperative supplied')),
        ('ngo', _('NGO supplied')),
    ], default='own')
    
    # Farming Practices
    fertilizer_used = models.BooleanField(default=False)
    fertilizer_type = models.CharField(max_length=100, blank=True)
    fertilizer_quantity_kg = models.FloatField(default=0.0)
    pesticide_used = models.BooleanField(default=False)
    pesticide_type = models.CharField(max_length=100, blank=True)
    irrigation_used = models.BooleanField(default=False)
    irrigation_type = models.CharField(max_length=50, blank=True)
    
    # Harvest Information
    harvest_date = models.DateField(null=True, blank=True)
    quantity_harvested_kg = models.FloatField(default=0.0)
    quality_grade = models.CharField(max_length=10, choices=[
        ('A', _('Grade A - Excellent')),
        ('B', _('Grade B - Good')),
        ('C', _('Grade C - Fair')),
        ('D', _('Grade D - Poor')),
    ], blank=True)
    
    # Post-Harvest
    quantity_consumed_kg = models.FloatField(default=0.0)
    quantity_sold_kg = models.FloatField(default=0.0)
    quantity_stored_kg = models.FloatField(default=0.0)
    quantity_lost_kg = models.FloatField(default=0.0)
    average_selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Challenges
    challenges_faced = models.TextField(blank=True)
    pest_diseases = models.TextField(blank=True)
    weather_impact = models.TextField(blank=True)
    
    # System Information
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='recorded_productions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Crop Production")
        verbose_name_plural = _("Crop Productions")
        ordering = ['-season__year', '-harvest_date']
        unique_together = ['farmer', 'crop', 'season']

    def __str__(self):
        return f"{self.farmer.full_name} - {self.crop.name} ({self.season})"

    @property
    def yield_per_hectare(self):
        """Calculate yield per hectare"""
        if self.area_planted_hectares > 0:
            return self.quantity_harvested_kg / self.area_planted_hectares / 1000  # Convert to tons
        return 0

    @property
    def total_revenue(self):
        """Calculate total revenue from sales"""
        return float(self.quantity_sold_kg) * float(self.average_selling_price)

    @property
    def loss_percentage(self):
        """Calculate percentage of crop lost"""
        if self.quantity_harvested_kg > 0:
            return (self.quantity_lost_kg / self.quantity_harvested_kg) * 100
        return 0

class AgricultureExtension(models.Model):
    """Model for agricultural extension services"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    service_type = models.CharField(max_length=50, choices=[
        ('training', _('Training')),
        ('demonstration', _('Demonstration')),
        ('advisory', _('Advisory Service')),
        ('input_supply', _('Input Supply')),
        ('market_linkage', _('Market Linkage')),
        ('technology', _('Technology Transfer')),
    ])
    
    # Location and Targeting
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='extension_services')
    sectors = models.ManyToManyField(Sector, related_name='extension_services')
    target_crops = models.ManyToManyField(Crop, related_name='extension_services')
    target_farmers = models.ManyToManyField(Farmer, blank=True, related_name='extension_services')
    
    # Service Details
    start_date = models.DateField()
    end_date = models.DateField()
    venue = models.CharField(max_length=200)
    facilitator = models.CharField(max_length=100)
    facilitator_organization = models.CharField(max_length=100)
    
    # Participation
    target_participants = models.IntegerField()
    actual_participants = models.IntegerField(default=0)
    male_participants = models.IntegerField(default=0)
    female_participants = models.IntegerField(default=0)
    youth_participants = models.IntegerField(default=0)
    
    # Resources
    budget_allocated = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    budget_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    materials_provided = models.TextField(blank=True)
    
    # Outcomes
    knowledge_gained = models.TextField(blank=True)
    practices_adopted = models.TextField(blank=True)
    feedback = models.TextField(blank=True)
    success_rate = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    # System Information
    organized_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='organized_extensions')
    status = models.CharField(max_length=20, choices=[
        ('planned', _('Planned')),
        ('ongoing', _('Ongoing')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    ], default='planned')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Agriculture Extension")
        verbose_name_plural = _("Agriculture Extensions")
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.title} - {self.district.name}"

    @property
    def participation_rate(self):
        """Calculate participation rate"""
        if self.target_participants > 0:
            return (self.actual_participants / self.target_participants) * 100
        return 0

    @property
    def budget_utilization(self):
        """Calculate budget utilization percentage"""
        if self.budget_allocated > 0:
            return (float(self.budget_spent) / float(self.budget_allocated)) * 100
        return 0

class MarketPrice(models.Model):
    """Model for crop market prices"""
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='market_prices')
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='market_prices')
    market_name = models.CharField(max_length=100)
    
    # Price Information
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='RWF')
    quality_grade = models.CharField(max_length=10, choices=[
        ('A', _('Grade A')),
        ('B', _('Grade B')),
        ('C', _('Grade C')),
        ('mixed', _('Mixed')),
    ], default='mixed')
    
    # Market Conditions
    supply_level = models.CharField(max_length=20, choices=[
        ('low', _('Low Supply')),
        ('normal', _('Normal Supply')),
        ('high', _('High Supply')),
        ('oversupply', _('Oversupply')),
    ])
    demand_level = models.CharField(max_length=20, choices=[
        ('low', _('Low Demand')),
        ('normal', _('Normal Demand')),
        ('high', _('High Demand')),
    ])
    
    # Additional Information
    quantity_available_kg = models.FloatField(default=0.0)
    price_trend = models.CharField(max_length=20, choices=[
        ('increasing', _('Increasing')),
        ('stable', _('Stable')),
        ('decreasing', _('Decreasing')),
    ], default='stable')
    
    # Data Source
    data_source = models.CharField(max_length=50, choices=[
        ('market_survey', _('Market Survey')),
        ('trader_report', _('Trader Report')),
        ('government', _('Government Data')),
        ('cooperative', _('Cooperative Report')),
        ('online', _('Online Platform')),
    ])
    collected_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='collected_prices')
    
    date_recorded = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Market Price")
        verbose_name_plural = _("Market Prices")
        ordering = ['-date_recorded', 'crop__name']
        unique_together = ['crop', 'district', 'market_name', 'date_recorded', 'quality_grade']

    def __str__(self):
        return f"{self.crop.name} - {self.market_name} - {self.date_recorded}"

class AgricultureAlert(models.Model):
    """Model for agriculture-related alerts"""
    ALERT_TYPES = [
        ('weather', _('Weather Alert')),
        ('pest_disease', _('Pest/Disease Alert')),
        ('market', _('Market Alert')),
        ('input_shortage', _('Input Shortage')),
        ('extension', _('Extension Service')),
        ('policy', _('Policy Update')),
        ('emergency', _('Emergency')),
    ]
    
    SEVERITY_LEVELS = [
        ('low', _('Low')),
        ('medium', _('Medium')),
        ('high', _('High')),
        ('critical', _('Critical')),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS)
    
    # Targeting
    districts = models.ManyToManyField(District, related_name='agriculture_alerts')
    sectors = models.ManyToManyField(Sector, blank=True, related_name='agriculture_alerts')
    affected_crops = models.ManyToManyField(Crop, blank=True, related_name='alerts')
    target_cooperatives = models.ManyToManyField(Cooperative, blank=True, related_name='alerts')
    
    # Timeline
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Action Items
    recommended_actions = models.TextField()
    resources_available = models.TextField(blank=True)
    contact_person = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15)
    
    # Tracking
    farmers_reached = models.IntegerField(default=0)
    cooperatives_notified = models.IntegerField(default=0)
    actions_taken = models.TextField(blank=True)
    effectiveness_score = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    
    # System Information
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_agriculture_alerts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Agriculture Alert")
        verbose_name_plural = _("Agriculture Alerts")
        ordering = ['-created_at', '-severity']

    def __str__(self):
        return f"{self.title} ({self.get_severity_display()})"

class AgricultureTarget(models.Model):
    """Model for agricultural production targets"""
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='agriculture_targets')
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='agriculture_targets', null=True, blank=True)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='targets')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='targets')
    
    # Targets
    target_area_hectares = models.FloatField()
    target_production_tons = models.FloatField()
    target_yield_tons_per_hectare = models.FloatField()
    target_farmers = models.IntegerField()
    
    # Budget
    allocated_budget = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    budget_for_seeds = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    budget_for_fertilizers = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    budget_for_extension = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Progress Tracking
    achieved_area_hectares = models.FloatField(default=0.0)
    achieved_production_tons = models.FloatField(default=0.0)
    farmers_participating = models.IntegerField(default=0)
    budget_utilized = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    # System Information
    set_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='set_agriculture_targets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Agriculture Target")
        verbose_name_plural = _("Agriculture Targets")
        ordering = ['-season__year', 'district__name', 'crop__name']
        unique_together = ['district', 'crop', 'season', 'sector']

    def __str__(self):
        sector_name = f" - {self.sector.name}" if self.sector else ""
        return f"{self.district.name}{sector_name} - {self.crop.name} ({self.season})"

    @property
    def area_achievement_rate(self):
        """Calculate area achievement rate as percentage"""
        if self.target_area_hectares > 0:
            return (self.achieved_area_hectares / self.target_area_hectares) * 100
        return 0

    @property
    def production_achievement_rate(self):
        """Calculate production achievement rate as percentage"""
        if self.target_production_tons > 0:
            return (self.achieved_production_tons / self.target_production_tons) * 100
        return 0

    @property
    def farmer_participation_rate(self):
        """Calculate farmer participation rate as percentage"""
        if self.target_farmers > 0:
            return (self.farmers_participating / self.target_farmers) * 100
        return 0

    @property
    def budget_utilization_rate(self):
        """Calculate budget utilization rate as percentage"""
        if self.allocated_budget > 0:
            return (float(self.budget_utilized) / float(self.allocated_budget)) * 100
        return 0

    @property
    def actual_yield_per_hectare(self):
        """Calculate actual yield per hectare"""
        if self.achieved_area_hectares > 0:
            return self.achieved_production_tons / self.achieved_area_hectares
        return 0