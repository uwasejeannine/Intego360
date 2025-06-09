# backend/apps/alerts/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.authentication.models import District, Sector, User

class AlertType(models.Model):
    """Model for alert types"""
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=20, unique=True)
    category = models.CharField(max_length=30, choices=[
        ('system', _('System')),
        ('security', _('Security')),
        ('agriculture', _('Agriculture')),
        ('health', _('Health')),
        ('education', _('Education')),
        ('infrastructure', _('Infrastructure')),
        ('emergency', _('Emergency')),
        ('performance', _('Performance')),
    ])
    description = models.TextField(blank=True)
    default_severity = models.CharField(max_length=10, choices=[
        ('low', _('Low')),
        ('medium', _('Medium')),
        ('high', _('High')),
        ('critical', _('Critical')),
    ], default='medium')
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Alert Type")
        verbose_name_plural = _("Alert Types")
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class SystemAlert(models.Model):
    """Model for system-wide alerts"""
    SEVERITY_LEVELS = [
        ('low', _('Low')),
        ('medium', _('Medium')),
        ('high', _('High')),
        ('critical', _('Critical')),
    ]

    STATUS_CHOICES = [
        ('active', _('Active')),
        ('resolved', _('Resolved')),
        ('dismissed', _('Dismissed')),
        ('escalated', _('Escalated')),
        ('pending', _('Pending Review')),
    ]

    # Basic Information
    title = models.CharField(max_length=200)
    description = models.TextField()
    alert_type = models.ForeignKey(AlertType, on_delete=models.CASCADE, related_name='alerts')
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Targeting and Scope
    districts = models.ManyToManyField(District, blank=True, related_name='system_alerts')
    sectors = models.ManyToManyField(Sector, blank=True, related_name='system_alerts')
    target_roles = models.JSONField(default=list, blank=True, help_text="List of user roles to notify")
    is_public = models.BooleanField(default=False, help_text="Visible to all users")
    
    # Timeline
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    resolved_time = models.DateTimeField(null=True, blank=True)
    estimated_resolution_time = models.DateTimeField(null=True, blank=True)
    
    # Actions and Response
    action_required = models.BooleanField(default=False)
    action_description = models.TextField(blank=True)
    immediate_actions = models.TextField(blank=True, help_text="Actions to take immediately")
    recommended_actions = models.TextField(blank=True, help_text="Recommended follow-up actions")
    resolution_notes = models.TextField(blank=True)
    
    # Contact Information
    contact_person = models.CharField(max_length=100, blank=True)
    contact_phone = models.CharField(max_length=15, blank=True)
    contact_email = models.EmailField(blank=True)
    escalation_contact = models.CharField(max_length=100, blank=True)
    
    # Impact Assessment
    priority_score = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(10)])
    impact_level = models.CharField(max_length=20, choices=[
        ('minimal', _('Minimal Impact')),
        ('low', _('Low Impact')),
        ('moderate', _('Moderate Impact')),
        ('high', _('High Impact')),
        ('severe', _('Severe Impact')),
    ], default='moderate')
    affected_systems = models.JSONField(default=list, blank=True)
    estimated_affected_users = models.IntegerField(default=0)
    
    # Tracking and Metrics
    users_notified = models.IntegerField(default=0)
    acknowledgments = models.IntegerField(default=0)
    views_count = models.IntegerField(default=0)
    escalation_count = models.IntegerField(default=0)
    
    # Automation
    is_automated = models.BooleanField(default=False)
    auto_resolve = models.BooleanField(default=False)
    auto_escalate_hours = models.IntegerField(null=True, blank=True)
    
    # Metadata
    source_system = models.CharField(max_length=50, blank=True)
    source_identifier = models.CharField(max_length=100, blank=True)
    tags = models.JSONField(default=list, blank=True)
    custom_data = models.JSONField(default=dict, blank=True)
    
    # System Information
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_alerts')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_alerts')
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_alerts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("System Alert")
        verbose_name_plural = _("System Alerts")
        ordering = ['-created_at', '-priority_score', '-severity']
        indexes = [
            models.Index(fields=['status', 'severity']),
            models.Index(fields=['created_at', 'priority_score']),
            models.Index(fields=['alert_type', 'status']),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_severity_display()})"

    @property
    def is_overdue(self):
        from django.utils import timezone
        if self.estimated_resolution_time and self.status in ['active', 'pending']:
            return timezone.now() > self.estimated_resolution_time
        return False

    @property
    def acknowledgment_rate(self):
        if self.users_notified > 0:
            return (self.acknowledgments / self.users_notified) * 100
        return 0

    def mark_as_resolved(self, user, resolution_notes=""):
        from django.utils import timezone
        self.status = 'resolved'
        self.resolved_time = timezone.now()
        self.resolved_by = user
        if resolution_notes:
            self.resolution_notes = resolution_notes
        self.save()

    def escalate(self, user, reason=""):
        self.status = 'escalated'
        self.escalation_count += 1
        if reason:
            self.custom_data['escalation_reason'] = reason
        self.custom_data['escalated_by'] = user.username
        self.save()

class AlertSubscription(models.Model):
    """Model for user alert subscriptions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alert_subscriptions')
    alert_types = models.ManyToManyField(AlertType, related_name='subscribers')
    
    # Subscription Settings
    districts = models.ManyToManyField(District, blank=True, related_name='alert_subscribers')
    sectors = models.ManyToManyField(Sector, blank=True, related_name='alert_subscribers')
    
    # Notification Preferences
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=True)
    in_app_notifications = models.BooleanField(default=True)
    
    # Delivery Preferences
    severity_threshold = models.CharField(max_length=10, choices=[
        ('low', _('Low and above')),
        ('medium', _('Medium and above')),
        ('high', _('High and above')),
        ('critical', _('Critical only')),
    ], default='medium')
    
    immediate_notification = models.BooleanField(default=True)
    digest_frequency = models.CharField(max_length=20, choices=[
        ('immediate', _('Immediate')),
        ('hourly', _('Hourly')),
        ('daily', _('Daily')),
        ('weekly', _('Weekly')),
    ], default='immediate')
    
    # Quiet Hours
    quiet_hours_enabled = models.BooleanField(default=False)
    quiet_start_time = models.TimeField(null=True, blank=True)
    quiet_end_time = models.TimeField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Alert Subscription")
        verbose_name_plural = _("Alert Subscriptions")

    def __str__(self):
        return f"Alert subscription for {self.user.username}"

class AlertNotification(models.Model):
    """Model for tracking alert notifications"""
    alert = models.ForeignKey(SystemAlert, on_delete=models.CASCADE, related_name='notifications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alert_notifications')
    
    # Notification Details
    notification_type = models.CharField(max_length=20, choices=[
        ('email', _('Email')),
        ('sms', _('SMS')),
        ('push', _('Push Notification')),
        ('in_app', _('In-App Notification')),
        ('webhook', _('Webhook')),
    ])
    
    # Status Tracking
    status = models.CharField(max_length=20, choices=[
        ('pending', _('Pending')),
        ('sent', _('Sent')),
        ('delivered', _('Delivered')),
        ('read', _('Read')),
        ('failed', _('Failed')),
        ('dismissed', _('Dismissed')),
    ], default='pending')
    
    # Timestamps
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    dismissed_at = models.DateTimeField(null=True, blank=True)
    
    # Delivery Information
    delivery_address = models.CharField(max_length=255, blank=True)  # email, phone, etc.
    delivery_attempts = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Alert Notification")
        verbose_name_plural = _("Alert Notifications")
        ordering = ['-created_at']
        unique_together = ['alert', 'user', 'notification_type']

    def __str__(self):
        return f"{self.notification_type} notification for {self.user.username} - {self.alert.title}"

    def mark_as_read(self):
        from django.utils import timezone
        if self.status in ['sent', 'delivered']:
            self.status = 'read'
            self.read_at = timezone.now()
            self.save()

class AlertAction(models.Model):
    """Model for tracking actions taken on alerts"""
    alert = models.ForeignKey(SystemAlert, on_delete=models.CASCADE, related_name='actions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alert_actions')
    
    action_type = models.CharField(max_length=30, choices=[
        ('acknowledged', _('Acknowledged')),
        ('assigned', _('Assigned')),
        ('escalated', _('Escalated')),
        ('resolved', _('Resolved')),
        ('dismissed', _('Dismissed')),
        ('comment_added', _('Comment Added')),
        ('status_changed', _('Status Changed')),
        ('severity_changed', _('Severity Changed')),
    ])
    
    description = models.TextField(blank=True)
    previous_value = models.CharField(max_length=100, blank=True)
    new_value = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Alert Action")
        verbose_name_plural = _("Alert Actions")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_action_type_display()} by {self.user.username} on {self.alert.title}"

class AlertRule(models.Model):
    """Model for automated alert rules"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    alert_type = models.ForeignKey(AlertType, on_delete=models.CASCADE, related_name='rules')
    
    # Rule Configuration
    is_active = models.BooleanField(default=True)
    source_system = models.CharField(max_length=50)
    trigger_conditions = models.JSONField(default=dict, help_text="Conditions that trigger this alert")
    severity_mapping = models.JSONField(default=dict, help_text="How to determine severity")
    
    # Auto Actions
    auto_assign = models.BooleanField(default=False)
    auto_assign_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='auto_assigned_alerts')
    auto_notify_roles = models.JSONField(default=list, blank=True)
    auto_escalate_after_hours = models.IntegerField(null=True, blank=True)
    
    # Throttling
    max_alerts_per_hour = models.IntegerField(default=10)
    cooldown_minutes = models.IntegerField(default=30)
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_alert_rules')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Alert Rule")
        verbose_name_plural = _("Alert Rules")
        ordering = ['name']

    def __str__(self):
        return self.name


