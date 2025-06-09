from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.authentication.models import District, Sector, User

class HealthFacilityType(models.Model):
    """Model for health facility types"""
    name = models.CharField(max_length=50, unique=True)
    level = models.IntegerField(help_text="1=Health Post, 2=Health Center, 3=District Hospital, 4=Referral Hospital")
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = _("Health Facility Type")
        verbose_name_plural = _("Health Facility Types")
        ordering = ['level', 'name']

    def __str__(self):
        return self.name

class HealthFacility(models.Model):
    """Model for health facilities"""
    name = models.CharField(max_length=100)
    facility_type = models.ForeignKey(HealthFacilityType, on_delete=models.CASCADE, related_name='facilities')
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='health_facilities')
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='health_facilities')
    
    # Location details
    cell = models.CharField(max_length=50)
    village = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    
    # Contact information
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    
    # Capacity and staffing
    bed_capacity = models.IntegerField(default=0)
    current_occupancy = models.IntegerField(default=0)
    doctors_count = models.IntegerField(default=0)
    nurses_count = models.IntegerField(default=0)
    midwives_count = models.IntegerField(default=0)
    other_staff_count = models.IntegerField(default=0)
    
    # Services
    emergency_services = models.BooleanField(default=False)
    maternity_services = models.BooleanField(default=False)
    laboratory_services = models.BooleanField(default=False)
    pharmacy_services = models.BooleanField(default=False)
    radiology_services = models.BooleanField(default=False)
    surgery_services = models.BooleanField(default=False)
    
    # Infrastructure
    has_electricity = models.BooleanField(default=False)
    has_generator = models.BooleanField(default=False)
    has_water = models.BooleanField(default=False)
    has_internet = models.BooleanField(default=False)
    has_ambulance = models.BooleanField(default=False)
    
    # Status
    is_operational = models.BooleanField(default=True)
    accreditation_status = models.CharField(max_length=20, choices=[
        ('pending', _('Pending')),
        ('accredited', _('Accredited')),
        ('conditional', _('Conditional')),
        ('suspended', _('Suspended')),
    ], default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Health Facility")
        verbose_name_plural = _("Health Facilities")
        ordering = ['district__name', 'name']

    def __str__(self):
        return f"{self.name} - {self.district.name}"

    @property
    def occupancy_rate(self):
        if self.bed_capacity > 0:
            return (self.current_occupancy / self.bed_capacity) * 100
        return 0

    @property
    def total_staff(self):
        return self.doctors_count + self.nurses_count + self.midwives_count + self.other_staff_count

class HealthIndicator(models.Model):
    """Model for health indicators"""
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, choices=[
        ('maternal', _('Maternal Health')),
        ('child', _('Child Health')),
        ('infectious', _('Infectious Diseases')),
        ('non_communicable', _('Non-Communicable Diseases')),
        ('nutrition', _('Nutrition')),
        ('immunization', _('Immunization')),
        ('family_planning', _('Family Planning')),
        ('mental_health', _('Mental Health')),
    ])
    description = models.TextField()
    unit_of_measurement = models.CharField(max_length=50)
    target_value = models.FloatField(help_text="Target value for this indicator")
    direction = models.CharField(max_length=10, choices=[
        ('increase', _('Higher is Better')),
        ('decrease', _('Lower is Better')),
    ])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Health Indicator")
        verbose_name_plural = _("Health Indicators")
        ordering = ['category', 'name']

    def __str__(self):
        return self.name

class HealthIndicatorData(models.Model):
    """Model for health indicator data"""
    indicator = models.ForeignKey(HealthIndicator, on_delete=models.CASCADE, related_name='data_points')
    facility = models.ForeignKey(HealthFacility, on_delete=models.CASCADE, related_name='indicator_data', null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='health_indicator_data')
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='health_indicator_data', null=True, blank=True)
    
    value = models.FloatField()
    reporting_period = models.CharField(max_length=20, choices=[
        ('monthly', _('Monthly')),
        ('quarterly', _('Quarterly')),
        ('annual', _('Annual')),
    ])
    year = models.IntegerField()
    month = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(12)])
    quarter = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(4)])
    
    # Data quality
    data_source = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    comments = models.TextField(blank=True)
    
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='recorded_health_data')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Health Indicator Data")
        verbose_name_plural = _("Health Indicator Data")
        ordering = ['-year', '-month', 'indicator__name']
        unique_together = ['indicator', 'district', 'facility', 'year', 'month', 'quarter']

    def __str__(self):
        period = f"{self.year}"
        if self.month:
            period += f"-{self.month:02d}"
        elif self.quarter:
            period += f"-Q{self.quarter}"
        
        location = self.facility.name if self.facility else self.district.name
        return f"{self.indicator.name} - {location} - {period}"

class Disease(models.Model):
    """Model for diseases and conditions"""
    name = models.CharField(max_length=100, unique=True)
    icd_code = models.CharField(max_length=20, blank=True, help_text="ICD-10 code")
    category = models.CharField(max_length=50, choices=[
        ('infectious', _('Infectious and Parasitic')),
        ('neoplasms', _('Neoplasms')),
        ('blood', _('Blood and Immune System')),
        ('endocrine', _('Endocrine and Metabolic')),
        ('mental', _('Mental and Behavioral')),
        ('nervous', _('Nervous System')),
        ('circulatory', _('Circulatory System')),
        ('respiratory', _('Respiratory System')),
        ('digestive', _('Digestive System')),
        ('genitourinary', _('Genitourinary System')),
        ('pregnancy', _('Pregnancy and Childbirth')),
        ('skin', _('Skin and Subcutaneous')),
        ('musculoskeletal', _('Musculoskeletal System')),
        ('congenital', _('Congenital Malformations')),
        ('injury', _('Injury and Poisoning')),
    ])
    is_notifiable = models.BooleanField(default=False, help_text="Requires immediate reporting")
    is_epidemic_prone = models.BooleanField(default=False)
    prevention_measures = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Disease")
        verbose_name_plural = _("Diseases")
        ordering = ['name']

    def __str__(self):
        return self.name

class DiseaseCase(models.Model):
    """Model for disease cases"""
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name='cases')
    facility = models.ForeignKey(HealthFacility, on_delete=models.CASCADE, related_name='disease_cases')
    
    # Patient demographics (anonymized)
    age_group = models.CharField(max_length=20, choices=[
        ('0-1', _('Under 1 year')),
        ('1-4', _('1-4 years')),
        ('5-14', _('5-14 years')),
        ('15-49', _('15-49 years')),
        ('50-64', _('50-64 years')),
        ('65+', _('65+ years')),
    ])
    gender = models.CharField(max_length=1, choices=[
        ('M', _('Male')),
        ('F', _('Female')),
    ])
    
    # Case details
    case_date = models.DateField()
    case_type = models.CharField(max_length=20, choices=[
        ('suspected', _('Suspected')),
        ('probable', _('Probable')),
        ('confirmed', _('Confirmed')),
    ])
    outcome = models.CharField(max_length=20, choices=[
        ('alive', _('Alive')),
        ('dead', _('Dead')),
        ('unknown', _('Unknown')),
    ], default='alive')
    
    # Location
    patient_residence_sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='disease_cases')
    
    # Epidemiological data
    is_outbreak_related = models.BooleanField(default=False)
    outbreak_id = models.CharField(max_length=50, blank=True)
    
    # System data
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reported_disease_cases')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Disease Case")
        verbose_name_plural = _("Disease Cases")
        ordering = ['-case_date']

    def __str__(self):
        return f"{self.disease.name} - {self.facility.name} - {self.case_date}"

class VaccinationCampaign(models.Model):
    """Model for vaccination campaigns"""
    name = models.CharField(max_length=100)
    vaccine_type = models.CharField(max_length=50)
    target_disease = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name='vaccination_campaigns')
    
    # Campaign details
    start_date = models.DateField()
    end_date = models.DateField()
    target_population = models.IntegerField()
    target_age_groups = models.CharField(max_length=200)
    
    # Coverage areas
    districts = models.ManyToManyField(District, related_name='vaccination_campaigns')
    facilities = models.ManyToManyField(HealthFacility, related_name='vaccination_campaigns')
    
    # Results
    doses_administered = models.IntegerField(default=0)
    people_vaccinated = models.IntegerField(default=0)
    adverse_events = models.IntegerField(default=0)
    
    # Campaign management
    campaign_manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='managed_campaigns')
    budget_allocated = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    budget_spent = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    status = models.CharField(max_length=20, choices=[
        ('planned', _('Planned')),
        ('ongoing', _('Ongoing')),
        ('completed', _('Completed')),
        ('suspended', _('Suspended')),
    ], default='planned')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Vaccination Campaign")
        verbose_name_plural = _("Vaccination Campaigns")
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.name} - {self.start_date}"

    @property
    def coverage_rate(self):
        if self.target_population > 0:
            return (self.people_vaccinated / self.target_population) * 100
        return 0

class HealthAlert(models.Model):
    """Model for health alerts and notifications"""
    ALERT_TYPES = [
        ('outbreak', _('Disease Outbreak')),
        ('shortage', _('Medicine/Supply Shortage')),
        ('equipment', _('Equipment Failure')),
        ('staffing', _('Staffing Issue')),
        ('infrastructure', _('Infrastructure Problem')),
        ('quality', _('Quality of Care Issue')),
        ('emergency', _('Emergency Situation')),
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
    
    # Affected areas
    districts = models.ManyToManyField(District, related_name='health_alerts')
    facilities = models.ManyToManyField(HealthFacility, blank=True, related_name='health_alerts')
    affected_diseases = models.ManyToManyField(Disease, blank=True, related_name='alerts')
    
    # Timeline
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Response
    recommended_actions = models.TextField()
    response_contact = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15)
    
    # Tracking
    people_affected = models.IntegerField(default=0)
    facilities_affected = models.IntegerField(default=0)
    response_actions_taken = models.TextField(blank=True)
    
    # System information
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_health_alerts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Health Alert")
        verbose_name_plural = _("Health Alerts")
        ordering = ['-created_at', '-severity']

    def __str__(self):
        return f"{self.title} ({self.get_severity_display()})"