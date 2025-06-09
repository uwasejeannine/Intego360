from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

class DashboardWidget(models.Model):
    """Model for dashboard widgets"""
    WIDGET_TYPES = [
        ('metric_card', _('Metric Card')),
        ('chart_line', _('Line Chart')),
        ('chart_bar', _('Bar Chart')),
        ('chart_pie', _('Pie Chart')),
        ('chart_area', _('Area Chart')),
        ('table', _('Data Table')),
        ('alert_list', _('Alert List')),
        ('progress_bar', _('Progress Bar')),
        ('map', _('Geographic Map')),
        ('calendar', _('Calendar')),
        ('news_feed', _('News Feed')),
        ('weather', _('Weather Widget')),
    ]

    DATA_SOURCES = [
        ('agriculture', _('Agriculture Data')),
        ('health', _('Health Data')),
        ('education', _('Education Data')),
        ('analytics', _('Analytics Data')),
        ('alerts', _('Alerts Data')),
        ('custom', _('Custom Data')),
        ('external', _('External API')),
    ]

    # Basic Information
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPES)
    
    # Data Configuration
    data_source = models.CharField(max_length=20, choices=DATA_SOURCES)
    data_endpoint = models.CharField(max_length=200, help_text="API endpoint or data source")
    data_parameters = models.JSONField(default=dict, help_text="Parameters for data fetching")
    refresh_interval_minutes = models.IntegerField(default=15)
    
    # Display Configuration
    chart_config = models.JSONField(default=dict, help_text="Chart-specific configuration")
    styling_config = models.JSONField(default=dict, help_text="CSS and styling configuration")
    size_config = models.JSONField(default=dict, help_text="Widget size and dimensions")
    
    # Access Control
    is_public = models.BooleanField(default=True)
    allowed_roles = models.JSONField(default=list, help_text="Roles that can view this widget")
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Performance
    average_load_time_ms = models.FloatField(default=0.0)
    usage_count = models.IntegerField(default=0)
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_widgets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Dashboard Widget")
        verbose_name_plural = _("Dashboard Widgets")
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_widget_type_display()})"

class UserDashboardPreference(models.Model):
    """Model for user dashboard preferences"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dashboard_preferences')
    
    # Layout Preferences
    default_view = models.CharField(max_length=20, choices=[
        ('overview', _('Overview')),
        ('agriculture', _('Agriculture')),
        ('health', _('Health')),
        ('education', _('Education')),
        ('analytics', _('Analytics')),
        ('custom', _('Custom')),
    ], default='overview')
    
    # Widget Configuration
    enabled_widgets = models.ManyToManyField(DashboardWidget, related_name='enabled_by_users')
    widget_layout = models.JSONField(default=dict, help_text="Widget positions and sizes")
    widget_order = models.JSONField(default=list, help_text="Widget display order")
    
    # Display Preferences
    theme = models.CharField(max_length=10, choices=[
        ('light', _('Light Theme')),
        ('dark', _('Dark Theme')),
        ('auto', _('Auto (System)')),
    ], default='light')
    
    density = models.CharField(max_length=15, choices=[  # FIXED: Changed from 10 to 15
        ('compact', _('Compact')),
        ('comfortable', _('Comfortable')),  # 11 characters
        ('spacious', _('Spacious')),
    ], default='comfortable')
    
    # Refresh and Updates
    auto_refresh_enabled = models.BooleanField(default=True)
    refresh_interval_minutes = models.IntegerField(default=5)
    show_notifications = models.BooleanField(default=True)
    notification_position = models.CharField(max_length=15, choices=[
        ('top-right', _('Top Right')),
        ('top-left', _('Top Left')),
        ('bottom-right', _('Bottom Right')),
        ('bottom-left', _('Bottom Left')),
    ], default='top-right')
    
    # Navigation
    sidebar_collapsed = models.BooleanField(default=False)
    show_breadcrumbs = models.BooleanField(default=True)
    show_quick_actions = models.BooleanField(default=True)
    
    # Data Preferences
    default_date_range_days = models.IntegerField(default=30)
    preferred_chart_type = models.CharField(max_length=20, default='line')
    show_data_tables = models.BooleanField(default=True)
    
    # Performance
    enable_animations = models.BooleanField(default=True)
    reduce_motion = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("User Dashboard Preference")
        verbose_name_plural = _("User Dashboard Preferences")

    def __str__(self):
        return f"Dashboard preferences for {self.user.username}"

class DashboardSnapshot(models.Model):
    """Model for dashboard snapshots"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dashboard_snapshots')
    
    # Snapshot Data
    snapshot_data = models.JSONField(default=dict, help_text="Dashboard state at snapshot time")
    widgets_data = models.JSONField(default=dict, help_text="Widget data at snapshot time")
    parameters = models.JSONField(default=dict, help_text="Parameters used for snapshot")
    
    # Time Information
    snapshot_date = models.DateTimeField()
    data_period_start = models.DateField()
    data_period_end = models.DateField()
    
    # Sharing
    is_public = models.BooleanField(default=False)
    shared_with_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='shared_snapshots')
    shared_with_roles = models.JSONField(default=list)
    
    # File Information
    file_path = models.CharField(max_length=500, blank=True)
    file_format = models.CharField(max_length=10, choices=[
        ('json', 'JSON'),
        ('pdf', 'PDF'),
        ('png', 'PNG'),
        ('html', 'HTML'),
    ], default='json')
    file_size_mb = models.FloatField(default=0.0)
    
    # Usage
    view_count = models.IntegerField(default=0)
    download_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Dashboard Snapshot")
        verbose_name_plural = _("Dashboard Snapshots")
        ordering = ['-snapshot_date']

    def __str__(self):
        return f"{self.name} - {self.snapshot_date.date()}"

class DashboardUsageAnalytics(models.Model):
    """Model for tracking dashboard usage analytics"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dashboard_usage')
    
    # Session Information
    session_id = models.CharField(max_length=50)
    device_type = models.CharField(max_length=20, choices=[
        ('desktop', _('Desktop')),
        ('tablet', _('Tablet')),
        ('mobile', _('Mobile')),
    ])
    browser = models.CharField(max_length=50, blank=True)
    
    # Usage Metrics
    login_time = models.DateTimeField()
    logout_time = models.DateTimeField(null=True, blank=True)
    total_session_duration_minutes = models.IntegerField(default=0)
    
    # Page Views
    pages_visited = models.JSONField(default=list, help_text="List of pages visited")
    page_view_count = models.IntegerField(default=0)
    most_viewed_section = models.CharField(max_length=30, blank=True)
    
    # Widget Interactions
    widgets_interacted = models.JSONField(default=list, help_text="Widgets user interacted with")
    widget_interaction_count = models.IntegerField(default=0)
    
    # Actions Performed
    actions_performed = models.JSONField(default=list, help_text="Actions performed during session")
    reports_generated = models.IntegerField(default=0)
    data_exports = models.IntegerField(default=0)
    
    # Performance Metrics
    average_page_load_time_ms = models.FloatField(default=0.0)
    bounce_rate = models.FloatField(default=0.0)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Dashboard Usage Analytics")
        verbose_name_plural = _("Dashboard Usage Analytics")
        ordering = ['-login_time']

    def __str__(self):
        return f"Usage by {self.user.username} on {self.login_time.date()}"

    @property
    def session_duration_hours(self):
        if self.logout_time:
            duration = self.logout_time - self.login_time
            return duration.total_seconds() / 3600
        return 0