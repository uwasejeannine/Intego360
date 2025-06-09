from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Avg, Sum
from django.utils import timezone
from .models import (
    DashboardWidget, UserDashboardPreference, DashboardSnapshot, 
    DashboardUsageAnalytics
)

@admin.register(DashboardWidget)
class DashboardWidgetAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'title', 'widget_type_display', 'data_source_display',
        'usage_count', 'average_load_time_display', 'is_active_display',
        'is_featured', 'is_public'
    ]
    list_filter = [
        'widget_type', 'data_source', 'is_active', 'is_featured', 'is_public',
        'allowed_roles', 'created_at'
    ]
    search_fields = ['name', 'title', 'description', 'data_endpoint']
    ordering = ['name']
    readonly_fields = ['usage_count', 'average_load_time_ms', 'created_at', 'updated_at']
    filter_horizontal = ['districts'] if hasattr(DashboardWidget, 'districts') else []

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'title', 'description', 'widget_type')
        }),
        ('Data Configuration', {
            'fields': (
                'data_source', 'data_endpoint', 'data_parameters',
                'refresh_interval_minutes'
            )
        }),
        ('Display Configuration', {
            'fields': ('chart_config', 'styling_config', 'size_config'),
            'classes': ('collapse',)
        }),
        ('Access Control', {
            'fields': (
                ('is_public', 'is_active', 'is_featured'),
                'allowed_roles'
            )
        }),
        ('Performance Metrics', {
            'fields': ('usage_count', 'average_load_time_ms'),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def widget_type_display(self, obj):
        return obj.get_widget_type_display()
    widget_type_display.short_description = 'Widget Type'

    def data_source_display(self, obj):
        return obj.get_data_source_display()
    data_source_display.short_description = 'Data Source'

    def is_active_display(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">✓ Active</span>')
        return format_html('<span style="color: red;">✗ Inactive</span>')
    is_active_display.short_description = 'Status'

    def average_load_time_display(self, obj):
        load_time = obj.average_load_time_ms
        if load_time == 0:
            return 'N/A'
        color = 'green' if load_time < 1000 else 'orange' if load_time < 3000 else 'red'
        return format_html(
            '<span style="color: {};">{:.0f}ms</span>',
            color, load_time
        )
    average_load_time_display.short_description = 'Avg Load Time'

    def save_model(self, request, obj, form, change):
        if not change:  # Creating new widget
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(UserDashboardPreference)
class UserDashboardPreferenceAdmin(admin.ModelAdmin):
    list_display = [
        'user_name', 'default_view', 'theme', 'density',
        'enabled_widgets_count', 'auto_refresh_enabled', 'created_at'
    ]
    list_filter = [
        'default_view', 'theme', 'density', 'auto_refresh_enabled',
        'show_notifications', 'sidebar_collapsed', 'created_at'
    ]
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    ordering = ['user__username']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['enabled_widgets']

    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Layout Preferences', {
            'fields': (
                'default_view', 'widget_layout', 'widget_order'
            )
        }),
        ('Widget Configuration', {
            'fields': ('enabled_widgets',)
        }),
        ('Display Preferences', {
            'fields': (
                ('theme', 'density'),
                ('show_notifications', 'notification_position'),
                ('sidebar_collapsed', 'show_breadcrumbs', 'show_quick_actions')
            )
        }),
        ('Refresh and Updates', {
            'fields': (
                'auto_refresh_enabled', 'refresh_interval_minutes'
            )
        }),
        ('Data Preferences', {
            'fields': (
                'default_date_range_days', 'preferred_chart_type',
                'show_data_tables'
            )
        }),
        ('Performance', {
            'fields': ('enable_animations', 'reduce_motion'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    user_name.short_description = 'User'

    def enabled_widgets_count(self, obj):
        count = obj.enabled_widgets.count()
        return format_html(
            '<span style="font-weight: bold;">{}</span>',
            count
        )
    enabled_widgets_count.short_description = 'Widgets Count'

@admin.register(DashboardSnapshot)
class DashboardSnapshotAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'user_name', 'snapshot_date', 'data_period_range',
        'file_format_display', 'file_size_display', 'view_count',
        'download_count', 'is_public'
    ]
    list_filter = [
        'file_format', 'is_public', 'snapshot_date', 'data_period_start',
        'data_period_end'
    ]
    search_fields = ['name', 'description', 'user__username']
    ordering = ['-snapshot_date']
    readonly_fields = [
        'view_count', 'download_count', 'file_size_mb', 
        'created_at', 'updated_at'
    ]
    filter_horizontal = ['shared_with_users']

    fieldsets = (
        ('Snapshot Information', {
            'fields': ('name', 'description', 'user')
        }),
        ('Time Period', {
            'fields': (
                'snapshot_date', 'data_period_start', 'data_period_end'
            )
        }),
        ('Snapshot Data', {
            'fields': ('snapshot_data', 'widgets_data', 'parameters'),
            'classes': ('collapse',)
        }),
        ('File Information', {
            'fields': (
                'file_format', 'file_path', 'file_size_mb'
            )
        }),
        ('Sharing', {
            'fields': (
                'is_public', 'shared_with_users', 'shared_with_roles'
            )
        }),
        ('Usage Statistics', {
            'fields': ('view_count', 'download_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    user_name.short_description = 'User'

    def data_period_range(self, obj):
        return f"{obj.data_period_start} to {obj.data_period_end}"
    data_period_range.short_description = 'Data Period'

    def file_format_display(self, obj):
        colors = {
            'json': 'blue',
            'pdf': 'red',
            'png': 'green',
            'html': 'orange'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.file_format, 'black'),
            obj.get_file_format_display()
        )
    file_format_display.short_description = 'Format'

    def file_size_display(self, obj):
        if obj.file_size_mb == 0:
            return 'N/A'
        color = 'green' if obj.file_size_mb < 5 else 'orange' if obj.file_size_mb < 20 else 'red'
        return format_html(
            '<span style="color: {};">{:.2f} MB</span>',
            color, obj.file_size_mb
        )
    file_size_display.short_description = 'File Size'

    def save_model(self, request, obj, form, change):
        if not change:  # Creating new snapshot
            obj.user = request.user
        super().save_model(request, obj, form, change)

@admin.register(DashboardUsageAnalytics)
class DashboardUsageAnalyticsAdmin(admin.ModelAdmin):
    list_display = [
        'user_name', 'login_time', 'session_duration_display', 
        'device_type', 'page_view_count', 'widget_interaction_count',
        'most_viewed_section'
    ]
    list_filter = [
        'device_type', 'browser', 'login_time', 'most_viewed_section'
    ]
    search_fields = [
        'user__username', 'user__first_name', 'user__last_name',
        'session_id', 'browser'
    ]
    ordering = ['-login_time']
    readonly_fields = [
        'session_duration_hours', 'total_session_duration_minutes',
        'created_at'
    ]

    fieldsets = (
        ('User & Session', {
            'fields': (
                'user', 'session_id', 'device_type', 'browser'
            )
        }),
        ('Session Times', {
            'fields': (
                'login_time', 'logout_time', 'total_session_duration_minutes',
                'session_duration_hours'
            )
        }),
        ('Page Activity', {
            'fields': (
                'pages_visited', 'page_view_count', 'most_viewed_section'
            )
        }),
        ('Widget Activity', {
            'fields': (
                'widgets_interacted', 'widget_interaction_count'
            )
        }),
        ('Actions & Performance', {
            'fields': (
                'actions_performed', 'reports_generated', 'data_exports',
                'average_page_load_time_ms', 'bounce_rate'
            ),
            'classes': ('collapse',)
        }),
    )

    def user_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    user_name.short_description = 'User'

    def session_duration_display(self, obj):
        duration = obj.total_session_duration_minutes
        if duration == 0:
            return 'N/A'
        
        hours = duration // 60
        minutes = duration % 60
        
        if hours > 0:
            duration_text = f"{hours}h {minutes}m"
        else:
            duration_text = f"{minutes}m"
        
        # Color code based on session length
        color = 'green' if duration > 30 else 'orange' if duration > 10 else 'red'
        return format_html(
            '<span style="color: {};">{}</span>',
            color, duration_text
        )
    session_duration_display.short_description = 'Session Duration'

    def has_add_permission(self, request):
        # Usually analytics data is created programmatically
        return False

# Custom admin actions
def reset_widget_usage_count(modeladmin, request, queryset):
    """Reset usage count for selected widgets"""
    queryset.update(usage_count=0)
    modeladmin.message_user(request, f"Reset usage count for {queryset.count()} widgets.")
reset_widget_usage_count.short_description = "Reset usage count"

def mark_widgets_as_featured(modeladmin, request, queryset):
    """Mark selected widgets as featured"""
    queryset.update(is_featured=True)
    modeladmin.message_user(request, f"Marked {queryset.count()} widgets as featured.")
mark_widgets_as_featured.short_description = "Mark as featured"

def mark_widgets_as_not_featured(modeladmin, request, queryset):
    """Remove featured status from selected widgets"""
    queryset.update(is_featured=False)
    modeladmin.message_user(request, f"Removed featured status from {queryset.count()} widgets.")
mark_widgets_as_not_featured.short_description = "Remove featured status"

# Add actions to DashboardWidgetAdmin
DashboardWidgetAdmin.actions = [
    reset_widget_usage_count, 
    mark_widgets_as_featured, 
    mark_widgets_as_not_featured
]

# Custom admin site configuration (if not already set)
admin.site.site_header = "Dashboard Management System"
admin.site.site_title = "Dashboard Admin"
admin.site.index_title = "Welcome to Dashboard Administration"