from rest_framework import serializers
from django.db.models import Count, Avg, Sum
from .models import DashboardWidget, UserDashboardPreference, DashboardSnapshot, DashboardUsageAnalytics

class DashboardWidgetSerializer(serializers.ModelSerializer):
    widget_type_display = serializers.CharField(source='get_widget_type_display', read_only=True)
    data_source_display = serializers.CharField(source='get_data_source_display', read_only=True)
    districts_names = serializers.SerializerMethodField()
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)

    class Meta:
        model = DashboardWidget
        fields = [
            'id', 'name', 'title', 'description', 'widget_type', 'widget_type_display',
            'data_source', 'data_source_display', 'data_endpoint', 'data_parameters',
            'refresh_interval_minutes', 'chart_config', 'styling_config', 'size_config',
            'is_public', 'allowed_roles', 'districts_names', 'is_active',
            'is_featured', 'average_load_time_ms', 'usage_count', 'created_by',
            'created_by_name', 'created_at', 'updated_at'
        ]

    def get_districts_names(self, obj):
        """Get district names for the widget"""
        try:
            return [district.name for district in obj.districts.all()]
        except AttributeError:
            # Handle case where districts field doesn't exist or is misconfigured
            return []

class UserDashboardPreferenceSerializer(serializers.ModelSerializer):
    enabled_widgets_data = DashboardWidgetSerializer(source='enabled_widgets', many=True, read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = UserDashboardPreference
        fields = [
            'id', 'user', 'user_name', 'default_view', 'enabled_widgets',
            'enabled_widgets_data', 'widget_layout', 'widget_order', 'theme',
            'density', 'auto_refresh_enabled', 'refresh_interval_minutes',
            'show_notifications', 'notification_position', 'sidebar_collapsed',
            'show_breadcrumbs', 'show_quick_actions', 'default_date_range_days',
            'preferred_chart_type', 'show_data_tables', 'enable_animations',
            'reduce_motion', 'created_at', 'updated_at'
        ]

class DashboardSnapshotSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    file_format_display = serializers.CharField(source='get_file_format_display', read_only=True)

    class Meta:
        model = DashboardSnapshot
        fields = [
            'id', 'name', 'description', 'user', 'user_name', 'snapshot_date',
            'data_period_start', 'data_period_end', 'is_public', 'file_format',
            'file_format_display', 'file_size_mb', 'view_count', 'download_count',
            'created_at', 'updated_at'
        ]

class DashboardStatsSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    active_users_today = serializers.IntegerField()
    total_widgets = serializers.IntegerField()
    popular_widgets = serializers.ListField()
    average_session_duration = serializers.FloatField()
    total_page_views = serializers.IntegerField()
    usage_by_device = serializers.DictField()
    usage_by_section = serializers.DictField()