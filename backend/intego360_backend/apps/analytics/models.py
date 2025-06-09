from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.authentication.models import District, Sector, User

class AnalyticsReport(models.Model):
    """Model for analytics reports"""
    REPORT_TYPES = [
        ('performance', _('Performance Report')),
        ('trends', _('Trends Analysis')),
        ('predictions', _('Predictions')),
        ('insights', _('AI Insights')),
        ('comparative', _('Comparative Analysis')),
        ('executive', _('Executive Summary')),
        ('detailed', _('Detailed Analysis')),
        ('custom', _('Custom Report')),
    ]
    
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('generating', _('Generating')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
        ('scheduled', _('Scheduled')),
    ]

    # Basic Information
    name = models.CharField(max_length=100)
    description = models.TextField()
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Scope and Targeting
    sectors_covered = models.JSONField(default=list, help_text="List of sectors: agriculture, health, education")
    districts = models.ManyToManyField(District, related_name='analytics_reports')
    sectors = models.ManyToManyField(Sector, blank=True, related_name='analytics_reports')
    
    # Time Period
    date_range_start = models.DateField()
    date_range_end = models.DateField()
    comparison_period_start = models.DateField(null=True, blank=True)
    comparison_period_end = models.DateField(null=True, blank=True)
    
    # Report Configuration
    parameters = models.JSONField(default=dict, help_text="Report generation parameters")
    filters = models.JSONField(default=dict, help_text="Data filters applied")
    metrics_included = models.JSONField(default=list, help_text="List of metrics to include")
    visualization_types = models.JSONField(default=list, help_text="Charts and visualizations")
    
    # Generated Content
    generated_data = models.JSONField(default=dict, help_text="Generated report data")
    executive_summary = models.TextField(blank=True)
    key_findings = models.JSONField(default=list, help_text="Key findings and insights")
    recommendations = models.JSONField(default=list, help_text="AI-generated recommendations")
    charts_data = models.JSONField(default=dict, help_text="Data for charts and visualizations")
    
    # AI Analysis
    ai_insights = models.JSONField(default=dict, help_text="AI-generated insights")
    confidence_score = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    data_quality_score = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    
    # Automation and Scheduling
    is_automated = models.BooleanField(default=False)
    generation_frequency = models.CharField(max_length=20, choices=[
        ('manual', _('Manual')),
        ('daily', _('Daily')),
        ('weekly', _('Weekly')),
        ('monthly', _('Monthly')),
        ('quarterly', _('Quarterly')),
        ('annually', _('Annually')),
    ], default='manual')
    next_generation_date = models.DateTimeField(null=True, blank=True)
    
    # File Management
    file_path = models.CharField(max_length=500, blank=True)
    file_format = models.CharField(max_length=10, choices=[
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('json', 'JSON'),
        ('csv', 'CSV'),
    ], default='pdf')
    file_size_mb = models.FloatField(default=0.0)
    
    # Access and Sharing
    is_public = models.BooleanField(default=False)
    shared_with_roles = models.JSONField(default=list, help_text="Roles that can access this report")
    access_count = models.IntegerField(default=0)
    
    # Performance Metrics
    generation_time_seconds = models.FloatField(default=0.0)
    data_points_processed = models.IntegerField(default=0)
    
    # System Information
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='generated_reports')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    generated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Analytics Report")
        verbose_name_plural = _("Analytics Reports")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'report_type']),
            models.Index(fields=['generated_at', 'is_automated']),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_report_type_display()})"

    @property
    def is_recent(self):
        from django.utils import timezone
        if self.generated_at:
            return timezone.now() - self.generated_at < timezone.timedelta(days=7)
        return False

class DataSource(models.Model):
    """Model for data sources used in analytics"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    source_type = models.CharField(max_length=20, choices=[
        ('database', _('Database')),
        ('api', _('API')),
        ('file', _('File')),
        ('external', _('External Service')),
        ('manual', _('Manual Entry')),
    ])
    
    # Connection Details
    connection_string = models.TextField(blank=True, help_text="Encrypted connection details")
    api_endpoint = models.URLField(blank=True)
    authentication_method = models.CharField(max_length=20, choices=[
        ('none', _('None')),
        ('basic', _('Basic Auth')),
        ('token', _('Token')),
        ('oauth', _('OAuth')),
        ('key', _('API Key')),
    ], default='none')
    
    # Data Information
    table_name = models.CharField(max_length=100, blank=True)
    primary_key_field = models.CharField(max_length=50, blank=True)
    date_field = models.CharField(max_length=50, blank=True)
    available_fields = models.JSONField(default=list, help_text="List of available fields")
    
    # Quality and Status
    is_active = models.BooleanField(default=True)
    last_sync_time = models.DateTimeField(null=True, blank=True)
    sync_frequency_hours = models.IntegerField(default=24)
    data_quality_score = models.FloatField(default=1.0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    
    # Usage Statistics
    queries_count = models.IntegerField(default=0)
    last_query_time = models.DateTimeField(null=True, blank=True)
    average_response_time_ms = models.FloatField(default=0.0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Data Source")
        verbose_name_plural = _("Data Sources")
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.get_source_type_display()})"

class AIModel(models.Model):
    """Model for AI/ML models used in analytics"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    model_type = models.CharField(max_length=30, choices=[
        ('regression', _('Regression')),
        ('classification', _('Classification')),
        ('clustering', _('Clustering')),
        ('forecasting', _('Time Series Forecasting')),
        ('anomaly_detection', _('Anomaly Detection')),
        ('recommendation', _('Recommendation System')),
        ('nlp', _('Natural Language Processing')),
        ('computer_vision', _('Computer Vision')),
    ])
    
    # Model Information
    algorithm = models.CharField(max_length=50)
    version = models.CharField(max_length=20, default='1.0')
    framework = models.CharField(max_length=30, choices=[
        ('scikit_learn', _('Scikit-Learn')),
        ('tensorflow', _('TensorFlow')),
        ('pytorch', _('PyTorch')),
        ('xgboost', _('XGBoost')),
        ('custom', _('Custom')),
    ])
    
    # Training Information
    training_data_size = models.IntegerField(default=0)
    training_date = models.DateTimeField(null=True, blank=True)
    training_duration_minutes = models.FloatField(default=0.0)
    
    # Performance Metrics
    accuracy_score = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    precision_score = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    recall_score = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    f1_score = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    
    # Model Files
    model_file_path = models.CharField(max_length=500, blank=True)
    model_size_mb = models.FloatField(default=0.0)
    input_features = models.JSONField(default=list, help_text="List of input features")
    output_format = models.JSONField(default=dict, help_text="Output format description")
    
    # Usage and Performance
    is_active = models.BooleanField(default=True)
    predictions_count = models.IntegerField(default=0)
    last_prediction_time = models.DateTimeField(null=True, blank=True)
    average_prediction_time_ms = models.FloatField(default=0.0)
    
    # Deployment
    deployment_status = models.CharField(max_length=20, choices=[
        ('development', _('Development')),
        ('testing', _('Testing')),
        ('staging', _('Staging')),
        ('production', _('Production')),
        ('retired', _('Retired')),
    ], default='development')
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_ai_models')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("AI Model")
        verbose_name_plural = _("AI Models")
        ordering = ['name']

    def __str__(self):
        return f"{self.name} v{self.version} ({self.get_model_type_display()})"

class Prediction(models.Model):
    """Model for storing AI predictions"""
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE, related_name='predictions')
    
    # Prediction Context
    sector = models.CharField(max_length=20, choices=[
        ('agriculture', _('Agriculture')),
        ('health', _('Health')),
        ('education', _('Education')),
        ('cross_sector', _('Cross-Sector')),
    ])
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='predictions', null=True, blank=True)
    
    # Input Data
    input_data = models.JSONField(default=dict, help_text="Input data used for prediction")
    input_data_hash = models.CharField(max_length=64, help_text="Hash of input data for deduplication")
    
    # Prediction Results
    prediction_result = models.JSONField(default=dict, help_text="Prediction output")
    confidence_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    
    # Prediction Details
    prediction_type = models.CharField(max_length=30, choices=[
        ('forecast', _('Forecast')),
        ('classification', _('Classification')),
        ('anomaly', _('Anomaly Detection')),
        ('recommendation', _('Recommendation')),
        ('risk_assessment', _('Risk Assessment')),
    ])
    
    # Time Information
    prediction_period_start = models.DateField(null=True, blank=True)
    prediction_period_end = models.DateField(null=True, blank=True)
    prediction_horizon_days = models.IntegerField(default=30)
    
    # Validation
    is_validated = models.BooleanField(default=False)
    actual_outcome = models.JSONField(default=dict, blank=True, help_text="Actual outcome for validation")
    accuracy_assessment = models.FloatField(null=True, blank=True)
    
    # Usage
    is_actionable = models.BooleanField(default=True)
    action_taken = models.TextField(blank=True)
    impact_assessment = models.TextField(blank=True)
    
    # System Information
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='requested_predictions')
    processing_time_ms = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    validated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Prediction")
        verbose_name_plural = _("Predictions")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['sector', 'district']),
            models.Index(fields=['created_at', 'confidence_score']),
        ]

    def __str__(self):
        return f"{self.get_prediction_type_display()} for {self.sector} ({self.created_at.date()})"

class DataQualityCheck(models.Model):
    """Model for tracking data quality assessments"""
    data_source = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name='quality_checks')
    
    # Check Details
    check_type = models.CharField(max_length=30, choices=[
        ('completeness', _('Completeness')),
        ('accuracy', _('Accuracy')),
        ('consistency', _('Consistency')),
        ('timeliness', _('Timeliness')),
        ('validity', _('Validity')),
        ('uniqueness', _('Uniqueness')),
    ])
    
    # Results
    overall_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    detailed_results = models.JSONField(default=dict, help_text="Detailed quality check results")
    issues_found = models.JSONField(default=list, help_text="List of issues identified")
    recommendations = models.JSONField(default=list, help_text="Recommendations for improvement")
    
    # Check Configuration
    check_parameters = models.JSONField(default=dict, help_text="Parameters used for the check")
    records_checked = models.IntegerField(default=0)
    
    # Status
    status = models.CharField(max_length=20, choices=[
        ('running', _('Running')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
    ], default='completed')
    
    check_duration_seconds = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Data Quality Check")
        verbose_name_plural = _("Data Quality Checks")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_check_type_display()} check for {self.data_source.name}"

