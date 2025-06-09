# backend/apps/alerts/serializers.py
from rest_framework import serializers
from django.db.models import Count, Avg
from .models import AlertType, SystemAlert, AlertSubscription, AlertNotification, AlertAction, AlertRule

class AlertTypeSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    alerts_count = serializers.SerializerMethodField()

    class Meta:
        model = AlertType
        fields = ['id', 'name', 'code', 'category', 'category_display', 'description', 'default_severity', 'is_active', 'alerts_count']

    def get_alerts_count(self, obj):
        return obj.alerts.filter(status='active').count()

class SystemAlertSerializer(serializers.ModelSerializer):
    alert_type_name = serializers.CharField(source='alert_type.name', read_only=True)
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    districts_names = serializers.SerializerMethodField()
    sectors_names = serializers.SerializerMethodField()
    is_overdue = serializers.ReadOnlyField()
    acknowledgment_rate = serializers.ReadOnlyField()
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)

    class Meta:
        model = SystemAlert
        fields = [
            'id', 'title', 'description', 'alert_type', 'alert_type_name',
            'severity', 'severity_display', 'status', 'status_display',
            'districts', 'districts_names', 'sectors', 'sectors_names',
            'target_roles', 'is_public', 'start_time', 'end_time',
            'action_required', 'action_description', 'immediate_actions',
            'recommended_actions', 'contact_person', 'contact_phone',
            'priority_score', 'impact_level', 'users_notified', 'acknowledgments',
            'acknowledgment_rate', 'is_overdue', 'created_by', 'created_by_name',
            'created_at', 'updated_at'
        ]

    def get_districts_names(self, obj):
        return [district.name for district in obj.districts.all()]

    def get_sectors_names(self, obj):
        return [sector.name for sector in obj.sectors.all()]

class AlertNotificationSerializer(serializers.ModelSerializer):
    alert_title = serializers.CharField(source='alert.title', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    notification_type_display = serializers.CharField(source='get_notification_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = AlertNotification
        fields = [
            'id', 'alert', 'alert_title', 'user', 'user_name',
            'notification_type', 'notification_type_display', 'status', 'status_display',
            'sent_at', 'delivered_at', 'read_at', 'delivery_attempts',
            'error_message', 'created_at'
        ]

class AlertStatsSerializer(serializers.Serializer):
    total_alerts = serializers.IntegerField()
    active_alerts = serializers.IntegerField()
    critical_alerts = serializers.IntegerField()
    resolved_today = serializers.IntegerField()
    average_resolution_time = serializers.FloatField()
    alerts_by_type = serializers.DictField()
    alerts_by_severity = serializers.DictField()
    recent_alerts = SystemAlertSerializer(many=True)