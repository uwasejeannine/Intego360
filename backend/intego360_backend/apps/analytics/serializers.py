from rest_framework import serializers
from django.db.models import Count, Avg
from .models import AnalyticsReport, DataSource, AIModel, Prediction, DataQualityCheck

class AnalyticsReportSerializer(serializers.ModelSerializer):
    report_type_display = serializers.CharField(source='get_report_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    districts_names = serializers.SerializerMethodField()
    is_recent = serializers.ReadOnlyField()
    generated_by_name = serializers.CharField(source='generated_by.get_full_name', read_only=True)

    class Meta:
        model = AnalyticsReport
        fields = [
            'id', 'name', 'description', 'report_type', 'report_type_display',
            'status', 'status_display', 'sectors_covered', 'districts', 'districts_names',
            'date_range_start', 'date_range_end', 'parameters', 'executive_summary',
            'key_findings', 'recommendations', 'confidence_score', 'is_automated',
            'generation_frequency', 'file_format', 'file_size_mb', 'is_public',
            'access_count', 'is_recent', 'generated_by', 'generated_by_name',
            'created_at', 'generated_at'
        ]

    def get_districts_names(self, obj):
        return [district.name for district in obj.districts.all()]

class AIModelSerializer(serializers.ModelSerializer):
    model_type_display = serializers.CharField(source='get_model_type_display', read_only=True)
    framework_display = serializers.CharField(source='get_framework_display', read_only=True)
    deployment_status_display = serializers.CharField(source='get_deployment_status_display', read_only=True)

    class Meta:
        model = AIModel
        fields = [
            'id', 'name', 'description', 'model_type', 'model_type_display',
            'algorithm', 'version', 'framework', 'framework_display',
            'accuracy_score', 'precision_score', 'recall_score', 'f1_score',
            'is_active', 'predictions_count', 'deployment_status',
            'deployment_status_display', 'created_at', 'updated_at'
        ]

class PredictionSerializer(serializers.ModelSerializer):
    model_name = serializers.CharField(source='model.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)
    sector_display = serializers.CharField(source='get_sector_display', read_only=True)
    prediction_type_display = serializers.CharField(source='get_prediction_type_display', read_only=True)

    class Meta:
        model = Prediction
        fields = [
            'id', 'model', 'model_name', 'sector', 'sector_display',
            'district', 'district_name', 'prediction_result', 'confidence_score',
            'prediction_type', 'prediction_type_display', 'prediction_period_start',
            'prediction_period_end', 'is_validated', 'accuracy_assessment',
            'is_actionable', 'action_taken', 'created_at'
        ]

class AnalyticsStatsSerializer(serializers.Serializer):
    total_reports = serializers.IntegerField()
    active_models = serializers.IntegerField()
    recent_predictions = serializers.IntegerField()
    average_accuracy = serializers.FloatField()
    reports_by_type = serializers.DictField()
    predictions_by_sector = serializers.DictField()
    data_quality_score = serializers.FloatField()