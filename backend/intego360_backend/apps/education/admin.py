from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Avg
from .models import (
    SchoolType, School, Subject, AcademicYear, Student, Teacher,
    Enrollment, ExamResult, EducationAlert, EducationTarget
)

@admin.register(SchoolType)
class SchoolTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'minimum_age', 'maximum_age', 'duration_years', 'schools_count']
    list_filter = ['level']
    search_fields = ['name', 'description']
    ordering = ['name']

    def schools_count(self, obj):
        return obj.schools.count()
    schools_count.short_description = 'Number of Schools'

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'school_code', 'school_type', 'district_name', 'sector_name',
        'current_enrollment', 'enrollment_rate_display', 'is_active', 'accreditation_status'
    ]
    list_filter = [
        'school_type', 'district', 'sector', 'is_active', 'accreditation_status',
        'is_government_school', 'has_electricity', 'has_internet'
    ]
    search_fields = ['name', 'school_code', 'headteacher_name']
    ordering = ['district__name', 'name']
    readonly_fields = ['enrollment_rate', 'teacher_student_ratio', 'qualified_teacher_percentage']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'school_code', 'school_type', 'district', 'sector')
        }),
        ('Location', {
            'fields': ('cell', 'village', 'latitude', 'longitude')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'email')
        }),
        ('Infrastructure', {
            'fields': (
                ('total_classrooms', 'usable_classrooms'),
                ('has_electricity', 'has_internet', 'has_library'),
                ('has_laboratory', 'has_computer_lab', 'has_sanitation'),
                ('has_clean_water', 'has_playground', 'has_dormitory', 'has_canteen')
            )
        }),
        ('Capacity & Staff', {
            'fields': (
                ('student_capacity', 'current_enrollment'),
                ('total_teachers', 'qualified_teachers'),
                ('enrollment_rate', 'teacher_student_ratio', 'qualified_teacher_percentage')
            )
        }),
        ('Management', {
            'fields': (
                'headteacher_name', 'headteacher_phone', 'deputy_headteacher_name'
            )
        }),
        ('Academic Information', {
            'fields': ('languages_of_instruction', 'grade_levels_offered')
        }),
        ('Status', {
            'fields': (
                ('is_active', 'is_government_school', 'is_boarding_school'),
                'accreditation_status', 'established_year'
            )
        }),
    )

    def district_name(self, obj):
        return obj.district.name
    district_name.short_description = 'District'

    def sector_name(self, obj):
        return obj.sector.name
    sector_name.short_description = 'Sector'

    def enrollment_rate_display(self, obj):
        rate = obj.enrollment_rate
        color = 'green' if rate >= 80 else 'orange' if rate >= 60 else 'red'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color, rate
        )
    enrollment_rate_display.short_description = 'Enrollment Rate'

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'category', 'school_levels_display']
    list_filter = ['category', 'school_levels']
    search_fields = ['name', 'code', 'description']
    ordering = ['name']
    filter_horizontal = ['school_levels']

    def school_levels_display(self, obj):
        return ", ".join([level.name for level in obj.school_levels.all()])
    school_levels_display.short_description = 'School Levels'

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current']
    ordering = ['-start_date']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'student_id', 'full_name', 'age', 'gender', 'current_school_name',
        'current_grade_level', 'completion_status', 'is_active'
    ]
    list_filter = [
        'gender', 'completion_status', 'is_active', 'has_special_needs',
        'fee_payment_status', 'home_district', 'current_school'
    ]
    search_fields = [
        'student_id', 'first_name', 'last_name', 'parent_guardian_name',
        'parent_guardian_phone'
    ]
    ordering = ['last_name', 'first_name']
    readonly_fields = ['full_name', 'age']

    fieldsets = (
        ('Personal Information', {
            'fields': (
                ('student_id', 'first_name', 'last_name'),
                ('date_of_birth', 'age', 'gender'),
                'national_id'
            )
        }),
        ('Family Information', {
            'fields': (
                'parent_guardian_name', 'parent_guardian_phone', 
                'parent_guardian_occupation'
            )
        }),
        ('Location', {
            'fields': (
                ('home_district', 'home_sector'),
                ('home_cell', 'home_village')
            )
        }),
        ('Current Enrollment', {
            'fields': (
                'current_school', 'current_grade_level', 'enrollment_date'
            )
        }),
        ('Status & Special Needs', {
            'fields': (
                ('is_active', 'completion_status'),
                ('has_special_needs', 'special_needs_description'),
                'fee_payment_status'
            )
        }),
    )

    def current_school_name(self, obj):
        return obj.current_school.name if obj.current_school else 'Not Enrolled'
    current_school_name.short_description = 'Current School'

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = [
        'teacher_id', 'full_name', 'qualification_level', 'current_school_name',
        'employment_type', 'teaching_experience_years', 'is_qualified', 'is_active'
    ]
    list_filter = [
        'qualification_level', 'employment_type', 'is_qualified', 'is_active',
        'current_school', 'subjects_taught'
    ]
    search_fields = [
        'teacher_id', 'first_name', 'last_name', 'email', 'phone_number'
    ]
    ordering = ['last_name', 'first_name']
    readonly_fields = ['full_name']
    filter_horizontal = ['subjects_taught']

    fieldsets = (
        ('Personal Information', {
            'fields': (
                ('teacher_id', 'first_name', 'last_name'),
                ('date_of_birth', 'gender'),
                ('national_id', 'phone_number', 'email')
            )
        }),
        ('Professional Information', {
            'fields': (
                ('qualification_level', 'teaching_experience_years'),
                'specialization', 'subjects_taught'
            )
        }),
        ('Employment', {
            'fields': (
                'current_school', 'employment_type', 'employment_start_date', 'salary'
            )
        }),
        ('Status', {
            'fields': ('is_active', 'is_qualified')
        }),
    )

    def current_school_name(self, obj):
        return obj.current_school.name if obj.current_school else 'Not Assigned'
    current_school_name.short_description = 'Current School'

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = [
        'student_name', 'school_name', 'academic_year_name', 'grade_level',
        'enrollment_status', 'pass_rate_display', 'attendance_rate_display'
    ]
    list_filter = [
        'enrollment_status', 'grade_level', 'academic_year', 'school'
    ]
    search_fields = [
        'student__first_name', 'student__last_name', 'student__student_id',
        'school__name'
    ]
    ordering = ['-academic_year__start_date', 'student__last_name']
    readonly_fields = ['pass_rate', 'attendance_rate']

    def student_name(self, obj):
        return obj.student.full_name
    student_name.short_description = 'Student'

    def school_name(self, obj):
        return obj.school.name
    school_name.short_description = 'School'

    def academic_year_name(self, obj):
        return obj.academic_year.name
    academic_year_name.short_description = 'Academic Year'

    def pass_rate_display(self, obj):
        rate = obj.pass_rate
        color = 'green' if rate >= 70 else 'orange' if rate >= 50 else 'red'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color, rate
        )
    pass_rate_display.short_description = 'Pass Rate'

    def attendance_rate_display(self, obj):
        rate = obj.attendance_rate
        color = 'green' if rate >= 80 else 'orange' if rate >= 60 else 'red'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color, rate
        )
    attendance_rate_display.short_description = 'Attendance Rate'

@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = [
        'student_name', 'subject_name', 'exam_type', 'exam_date',
        'percentage_display', 'grade', 'passed'
    ]
    list_filter = [
        'exam_type', 'passed', 'subject', 'exam_date',
        'enrollment__school', 'enrollment__academic_year'
    ]
    search_fields = [
        'enrollment__student__first_name', 'enrollment__student__last_name',
        'subject__name'
    ]
    ordering = ['-exam_date']
    readonly_fields = ['percentage']

    def student_name(self, obj):
        return obj.enrollment.student.full_name
    student_name.short_description = 'Student'

    def subject_name(self, obj):
        return obj.subject.name
    subject_name.short_description = 'Subject'

    def percentage_display(self, obj):
        percentage = obj.percentage
        color = 'green' if percentage >= 70 else 'orange' if percentage >= 50 else 'red'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color, percentage
        )
    percentage_display.short_description = 'Percentage'

@admin.register(EducationAlert)
class EducationAlertAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'alert_type', 'severity_display', 'schools_affected',
        'students_affected', 'is_active', 'start_date'
    ]
    list_filter = [
        'alert_type', 'severity', 'is_active', 'districts', 'school_types'
    ]
    search_fields = ['title', 'description', 'contact_person']
    ordering = ['-created_at', '-severity']
    filter_horizontal = ['districts', 'schools', 'school_types']

    fieldsets = (
        ('Alert Information', {
            'fields': (
                'title', 'description', 'alert_type', 'severity'
            )
        }),
        ('Targeting', {
            'fields': ('districts', 'schools', 'school_types')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'is_active')
        }),
        ('Action Items', {
            'fields': (
                'recommended_actions', 'resources_available',
                'contact_person', 'contact_phone'
            )
        }),
        ('Impact & Tracking', {
            'fields': (
                ('schools_affected', 'students_affected'),
                'actions_taken', 'effectiveness_score'
            )
        }),
    )

    def severity_display(self, obj):
        colors = {
            'low': 'green',
            'medium': 'orange',
            'high': 'red',
            'critical': 'darkred'
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.severity, 'black'),
            obj.get_severity_display()
        )
    severity_display.short_description = 'Severity'

@admin.register(EducationTarget)
class EducationTargetAdmin(admin.ModelAdmin):
    list_display = [
        'district_name', 'school_type_name', 'academic_year_name',
        'target_enrollment', 'achievement_rate_display', 'budget_utilization_display'
    ]
    list_filter = [
        'district', 'school_type', 'academic_year'
    ]
    search_fields = ['district__name', 'school_type__name']
    ordering = ['-academic_year__start_date', 'district__name']
    readonly_fields = ['enrollment_achievement_rate', 'budget_utilization_rate']

    fieldsets = (
        ('Target Information', {
            'fields': ('district', 'school_type', 'academic_year')
        }),
        ('Enrollment Targets', {
            'fields': (
                'target_enrollment', 'target_completion_rate',
                'target_pass_rate', 'target_attendance_rate'
            )
        }),
        ('Infrastructure Targets', {
            'fields': (
                'target_classrooms', 'target_teacher_student_ratio',
                'target_qualified_teachers_percentage'
            )
        }),
        ('Budget Allocation', {
            'fields': (
                'allocated_budget', 'budget_for_infrastructure',
                'budget_for_teaching_materials', 'budget_for_teacher_training'
            )
        }),
        ('Achievement Tracking', {
            'fields': (
                ('achieved_enrollment', 'enrollment_achievement_rate'),
                'achieved_completion_rate', 'achieved_pass_rate',
                'achieved_attendance_rate', ('budget_utilized', 'budget_utilization_rate')
            )
        }),
    )

    def district_name(self, obj):
        return obj.district.name
    district_name.short_description = 'District'

    def school_type_name(self, obj):
        return obj.school_type.name
    school_type_name.short_description = 'School Type'

    def academic_year_name(self, obj):
        return obj.academic_year.name
    academic_year_name.short_description = 'Academic Year'

    def achievement_rate_display(self, obj):
        rate = obj.enrollment_achievement_rate
        color = 'green' if rate >= 90 else 'orange' if rate >= 70 else 'red'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color, rate
        )
    achievement_rate_display.short_description = 'Achievement Rate'

    def budget_utilization_display(self, obj):
        rate = obj.budget_utilization_rate
        color = 'green' if 80 <= rate <= 100 else 'orange' if rate >= 60 else 'red'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color, rate
        )
    budget_utilization_display.short_description = 'Budget Utilization'

# Custom admin site configuration
admin.site.site_header = "Education Management System"
admin.site.site_title = "EMS Admin"
admin.site.index_title = "Welcome to Education Management System Administration"