from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class District(models.Model):
    """District model for administrative divisions"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    province = models.CharField(max_length=50)
    population = models.IntegerField(default=0)
    area_km2 = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("District")
        verbose_name_plural = _("Districts")
        ordering = ['name']

    def __str__(self):
        return self.name

class Sector(models.Model):
    """Sector model for administrative subdivisions"""
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='sectors')
    code = models.CharField(max_length=15, unique=True)
    population = models.IntegerField(default=0)
    area_km2 = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Sector")
        verbose_name_plural = _("Sectors")
        ordering = ['district__name', 'name']
        unique_together = ['district', 'name']

    def __str__(self):
        return f"{self.name} - {self.district.name}"

class User(AbstractUser):
    """Extended User model for Intego360"""
    
    ROLE_CHOICES = [
        ('admin', _('System Administrator')),
        ('mayor', _('District Mayor')),
        ('vice_mayor', _('Vice Mayor')),
        ('sector_coordinator', _('Sector Coordinator')),
        ('agriculture_officer', _('Agriculture Officer')),
        ('health_officer', _('Health Officer')),
        ('education_officer', _('Education Officer')),
        ('data_analyst', _('Data Analyst')),
        ('viewer', _('Read-only Viewer')),
    ]
    
    LANGUAGE_CHOICES = [
        ('en', _('English')),
        ('rw', _('Kinyarwanda')),
        ('fr', _('French')),
    ]

    # Personal Information
    phone_number = models.CharField(max_length=15, blank=True)
    national_id = models.CharField(max_length=16, unique=True, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    
    # Professional Information
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    sectors = models.ManyToManyField(Sector, blank=True, related_name='users')
    department = models.CharField(max_length=100, blank=True)
    employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    
    # System Preferences
    preferred_language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')
    timezone = models.CharField(max_length=50, default='Africa/Kigali')
    receive_email_notifications = models.BooleanField(default=True)
    receive_sms_notifications = models.BooleanField(default=False)
    
    # Status and Tracking
    is_verified = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    failed_login_attempts = models.IntegerField(default=0)
    account_locked_until = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Fix the reverse accessor conflicts by providing custom related_name
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name='intego360_users',  # Custom related_name to avoid conflicts
        related_query_name='intego360_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='intego360_users',  # Custom related_name to avoid conflicts
        related_query_name='intego360_user',
    )

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"

    def get_full_name(self):
        """Return the user's full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    def get_role_display_verbose(self):
        """Get verbose role display with district/sector info"""
        role_name = self.get_role_display()
        if self.district:
            return f"{role_name} - {self.district.name}"
        return role_name

    def has_district_access(self, district):
        """Check if user has access to a specific district"""
        if self.role == 'admin':
            return True
        return self.district == district

    def has_sector_access(self, sector):
        """Check if user has access to a specific sector"""
        if self.role == 'admin':
            return True
        if self.role in ['mayor', 'vice_mayor'] and sector.district == self.district:
            return True
        return sector in self.sectors.all()

    def can_view_sector_data(self, sector_type):
        """Check if user can view specific sector data (agriculture, health, education)"""
        if self.role == 'admin':
            return True
        
        role_sector_mapping = {
            'agriculture_officer': 'agriculture',
            'health_officer': 'health',
            'education_officer': 'education',
        }
        
        if self.role in ['mayor', 'vice_mayor', 'data_analyst']:
            return True
        
        return role_sector_mapping.get(self.role) == sector_type

    def get_accessible_districts(self):
        """Get all districts accessible to this user"""
        if self.role == 'admin':
            return District.objects.all()
        if self.district:
            return District.objects.filter(id=self.district.id)
        return District.objects.none()

    def get_accessible_sectors(self):
        """Get all sectors accessible to this user"""
        if self.role == 'admin':
            return Sector.objects.all()
        if self.role in ['mayor', 'vice_mayor'] and self.district:
            return self.district.sectors.all()
        return self.sectors.all()

class UserProfile(models.Model):
    """Extended profile information for users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Contact Information
    work_phone = models.CharField(max_length=15, blank=True)
    personal_phone = models.CharField(max_length=15, blank=True)
    work_email = models.EmailField(blank=True)
    office_address = models.TextField(blank=True)
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True)
    
    # Professional Details
    education_background = models.TextField(blank=True)
    work_experience = models.TextField(blank=True)
    skills = models.TextField(blank=True, help_text="Comma-separated list of skills")
    certifications = models.TextField(blank=True)
    
    # System Usage Statistics
    total_logins = models.IntegerField(default=0)
    last_activity = models.DateTimeField(null=True, blank=True)
    dashboard_views = models.IntegerField(default=0)
    reports_generated = models.IntegerField(default=0)
    
    # Notifications Preferences
    alert_frequency = models.CharField(
        max_length=20,
        choices=[
            ('immediate', _('Immediate')),
            ('hourly', _('Hourly Digest')),
            ('daily', _('Daily Digest')),
            ('weekly', _('Weekly Digest')),
        ],
        default='immediate'
    )
    
    # Social/Professional Links
    linkedin_profile = models.URLField(blank=True)
    twitter_handle = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")

    def __str__(self):
        return f"Profile of {self.user.get_full_name()}"

class UserSession(models.Model):
    """Track user sessions for security and analytics"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    device_type = models.CharField(max_length=50, blank=True)  # mobile, tablet, desktop
    browser = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=100, blank=True)  # City, Country
    
    login_time = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Security flags
    is_suspicious = models.BooleanField(default=False)
    security_score = models.IntegerField(default=100)  # 0-100, lower is more suspicious
    
    class Meta:
        verbose_name = _("User Session")
        verbose_name_plural = _("User Sessions")
        ordering = ['-login_time']

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"

    @property
    def duration(self):
        """Calculate session duration"""
        end_time = self.logout_time or self.last_activity
        return end_time - self.login_time

class ActivityLog(models.Model):
    """Log user activities for audit trail"""
    ACTION_CHOICES = [
        ('login', _('Login')),
        ('logout', _('Logout')),
        ('view_dashboard', _('View Dashboard')),
        ('view_agriculture', _('View Agriculture Data')),
        ('view_health', _('View Health Data')),
        ('view_education', _('View Education Data')),
        ('generate_report', _('Generate Report')),
        ('export_data', _('Export Data')),
        ('create_alert', _('Create Alert')),
        ('modify_alert', _('Modify Alert')),
        ('delete_alert', _('Delete Alert')),
        ('update_profile', _('Update Profile')),
        ('change_password', _('Change Password')),
        ('data_entry', _('Data Entry')),
        ('data_modification', _('Data Modification')),
        ('system_admin', _('System Administration')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    description = models.TextField()
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    
    # Context information
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, null=True, blank=True)
    resource_type = models.CharField(max_length=50, blank=True)  # agriculture, health, education
    resource_id = models.CharField(max_length=50, blank=True)
    
    # Additional metadata
    metadata = models.JSONField(default=dict, blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Activity Log")
        verbose_name_plural = _("Activity Logs")
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.get_action_display()} - {self.timestamp}"