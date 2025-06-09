from rest_framework import serializers
from django.db.models import Count, Avg, Sum
from .models import (
    SchoolType, School, Subject, AcademicYear, Student, Teacher,
    Enrollment, ExamResult, EducationAlert, EducationTarget
)

class SchoolTypeSerializer(serializers.ModelSerializer):
    schools_count = serializers.SerializerMethodField()

    class Meta:
        model = SchoolType
        fields = ['id', 'name', 'level', 'description', 'minimum_age', 'maximum_age', 'duration_years', 'schools_count']

    def get_schools_count(self, obj):
        return obj.schools.count()

class SchoolSerializer(serializers.ModelSerializer):
    school_type_name = serializers.CharField(source='school_type.name', read_only=True)
    district_name = serializers.CharField(source='district.name', read_only=True)
    sector_name = serializers.CharField(source='sector.name', read_only=True)
    enrollment_rate = serializers.ReadOnlyField()
    teacher_student_ratio = serializers.ReadOnlyField()
    qualified_teacher_percentage = serializers.ReadOnlyField()

    class Meta:
        model = School
        fields = [
            'id', 'name', 'school_code', 'school_type', 'school_type_name',
            'district', 'district_name', 'sector', 'sector_name', 'cell', 'village',
            'phone_number', 'email', 'total_classrooms', 'usable_classrooms',
            'has_electricity', 'has_internet', 'has_library', 'has_laboratory',
            'has_computer_lab', 'has_sanitation', 'has_clean_water', 'has_playground',
            'student_capacity', 'current_enrollment', 'enrollment_rate',
            'total_teachers', 'qualified_teachers', 'teacher_student_ratio',
            'qualified_teacher_percentage', 'headteacher_name', 'languages_of_instruction',
            'grade_levels_offered', 'is_active', 'is_government_school', 'accreditation_status',
            'established_year', 'created_at', 'updated_at'
        ]

class StudentSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)
    current_school_name = serializers.CharField(source='current_school.name', read_only=True)
    home_district_name = serializers.CharField(source='home_district.name', read_only=True)

    class Meta:
        model = Student
        fields = [
            'id', 'student_id', 'first_name', 'last_name', 'full_name',
            'date_of_birth', 'age', 'gender', 'parent_guardian_name',
            'parent_guardian_phone', 'home_district', 'home_district_name',
            'home_sector', 'current_school', 'current_school_name',
            'current_grade_level', 'enrollment_date', 'is_active',
            'completion_status', 'has_special_needs', 'fee_payment_status'
        ]

class TeacherSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    current_school_name = serializers.CharField(source='current_school.name', read_only=True)
    subjects_taught_names = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = [
            'id', 'teacher_id', 'first_name', 'last_name', 'full_name',
            'date_of_birth', 'gender', 'phone_number', 'email',
            'qualification_level', 'teaching_experience_years', 'specialization',
            'subjects_taught', 'subjects_taught_names', 'current_school',
            'current_school_name', 'employment_type', 'employment_start_date',
            'is_active', 'is_qualified'
        ]

    def get_subjects_taught_names(self, obj):
        return [subject.name for subject in obj.subjects_taught.all()]

class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    school_name = serializers.CharField(source='school.name', read_only=True)
    academic_year_name = serializers.CharField(source='academic_year.name', read_only=True)
    pass_rate = serializers.ReadOnlyField()
    attendance_rate = serializers.ReadOnlyField()

    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'student_name', 'school', 'school_name',
            'academic_year', 'academic_year_name', 'grade_level',
            'enrollment_date', 'completion_date', 'enrollment_status',
            'total_subjects', 'subjects_passed', 'pass_rate',
            'overall_grade', 'class_rank', 'total_days', 'days_attended',
            'attendance_rate', 'created_at', 'updated_at'
        ]

class EducationStatsSerializer(serializers.Serializer):
    total_schools = serializers.IntegerField()
    total_students = serializers.IntegerField()
    total_teachers = serializers.IntegerField()
    enrollment_rate = serializers.FloatField()
    completion_rate = serializers.FloatField()
    pass_rate = serializers.FloatField()
    teacher_student_ratio = serializers.FloatField()
    schools_by_type = serializers.DictField()
    enrollment_by_grade = serializers.ListField()
    infrastructure_status = serializers.DictField()