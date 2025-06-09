from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import User, District, Sector, UserProfile, UserSession, ActivityLog

class DistrictSerializer(serializers.ModelSerializer):
    """Serializer for District model"""
    sectors_count = serializers.SerializerMethodField()
    users_count = serializers.SerializerMethodField()

    class Meta:
        model = District
        fields = [
            'id', 'name', 'code', 'province', 'population', 
            'area_km2', 'sectors_count', 'users_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_sectors_count(self, obj):
        return obj.sectors.count()

    def get_users_count(self, obj):
        return obj.users.count()

class SectorSerializer(serializers.ModelSerializer):
    """Serializer for Sector model"""
    district_name = serializers.CharField(source='district.name', read_only=True)
    users_count = serializers.SerializerMethodField()

    class Meta:
        model = Sector
        fields = [
            'id', 'name', 'code', 'district', 'district_name',
            'population', 'area_km2', 'users_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_users_count(self, obj):
        return obj.users.count()

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model"""
    
    class Meta:
        model = UserProfile
        fields = [
            'work_phone', 'personal_phone', 'work_email', 'office_address',
            'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship',
            'education_background', 'work_experience', 'skills', 'certifications',
            'total_logins', 'last_activity', 'dashboard_views', 'reports_generated',
            'alert_frequency', 'linkedin_profile', 'twitter_handle'
        ]
        read_only_fields = [
            'total_logins', 'last_activity', 'dashboard_views', 'reports_generated'
        ]

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    profile = UserProfileSerializer(required=False)
    district_name = serializers.CharField(source='district.name', read_only=True)
    sectors_names = serializers.SerializerMethodField()
    role_verbose = serializers.CharField(source='get_role_display', read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'phone_number', 'national_id', 'date_of_birth', 'profile_picture',
            'role', 'role_verbose', 'district', 'district_name', 'sectors', 'sectors_names',
            'department', 'employee_id', 'preferred_language', 'timezone',
            'receive_email_notifications', 'receive_sms_notifications',
            'is_verified', 'is_active', 'is_staff', 'date_joined', 'last_login',
            'created_at', 'updated_at', 'profile', 'password', 'confirm_password'
        ]
        read_only_fields = [
            'id', 'date_joined', 'last_login', 'created_at', 'updated_at',
            'full_name', 'role_verbose', 'district_name', 'sectors_names'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'national_id': {'required': False},
        }

    def get_sectors_names(self, obj):
        return [sector.name for sector in obj.sectors.all()]

    def validate_password(self, value):
        """Validate password using Django's password validation"""
        if value:
            try:
                validate_password(value)
            except ValidationError as e:
                raise serializers.ValidationError(list(e.messages))
        return value

    def validate(self, attrs):
        """Validate password confirmation"""
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError({
                'confirm_password': 'Password confirmation does not match.'
            })
        
        return attrs

    def create(self, validated_data):
        """Create user with profile"""
        profile_data = validated_data.pop('profile', {})
        password = validated_data.pop('password', None)
        validated_data.pop('confirm_password', None)
        
        user = User.objects.create(**validated_data)
        
        if password:
            user.set_password(password)
            user.save()
        
        # Create or update profile
        UserProfile.objects.create(user=user, **profile_data)
        
        return user

    def update(self, instance, validated_data):
        """Update user and profile"""
        profile_data = validated_data.pop('profile', {})
        password = validated_data.pop('password', None)
        validated_data.pop('confirm_password', None)
        
        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        
        # Update or create profile
        if profile_data:
            profile, created = UserProfile.objects.get_or_create(user=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        
        return instance

class LoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    remember_me = serializers.BooleanField(default=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            
            if not user:
                raise serializers.ValidationError('Invalid credentials.')
            
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            
            # Check if account is locked
            if user.account_locked_until and user.account_locked_until > timezone.now():
                raise serializers.ValidationError(
                    f'Account is locked until {user.account_locked_until}.'
                )
            
            attrs['user'] = user
            return attrs
        
        raise serializers.ValidationError('Must include username and password.')

class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        """Validate new password"""
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def validate(self, attrs):
        """Validate password change"""
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': 'Password confirmation does not match.'
            })
        return attrs

    def validate_old_password(self, value):
        """Validate old password"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect.')
        return value

class UserSessionSerializer(serializers.ModelSerializer):
    """Serializer for UserSession model"""
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    duration = serializers.SerializerMethodField()

    class Meta:
        model = UserSession
        fields = [
            'id', 'user', 'user_name', 'session_key', 'ip_address',
            'user_agent', 'device_type', 'browser', 'location',
            'login_time', 'last_activity', 'logout_time', 'is_active',
            'is_suspicious', 'security_score', 'duration'
        ]
        read_only_fields = ['duration']

    def get_duration(self, obj):
        """Get session duration in minutes"""
        duration = obj.duration
        return duration.total_seconds() / 60 if duration else 0

class ActivityLogSerializer(serializers.ModelSerializer):
    """Serializer for ActivityLog model"""
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    action_verbose = serializers.CharField(source='get_action_display', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)
    sector_name = serializers.CharField(source='sector.name', read_only=True)

    class Meta:
        model = ActivityLog
        fields = [
            'id', 'user', 'user_name', 'action', 'action_verbose', 'description',
            'ip_address', 'user_agent', 'district', 'district_name',
            'sector', 'sector_name', 'resource_type', 'resource_id',
            'metadata', 'timestamp'
        ]
        read_only_fields = ['id', 'timestamp']

class UserStatsSerializer(serializers.Serializer):
    """Serializer for user statistics"""
    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    verified_users = serializers.IntegerField()
    users_by_role = serializers.DictField()
    users_by_district = serializers.DictField()
    recent_registrations = serializers.IntegerField()
    current_sessions = serializers.IntegerField()

class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard statistics"""
    total_districts = serializers.IntegerField()
    total_sectors = serializers.IntegerField()
    total_users = serializers.IntegerField()
    active_alerts = serializers.IntegerField()
    system_health = serializers.CharField()
    last_data_sync = serializers.DateTimeField()
    performance_score = serializers.FloatField()