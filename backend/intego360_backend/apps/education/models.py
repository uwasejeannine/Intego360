from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

# Import District and Sector from authentication app
from apps.authentication.models import District, Sector

class SchoolType(models.Model):
    """Model for school types"""
    name = models.CharField(max_length=50, unique=True)
    level = models.CharField(max_length=20, choices=[
        ('pre_primary', _('Pre-Primary')),
        ('primary', _('Primary')),
        ('lower_secondary', _('Lower Secondary')),
        ('upper_secondary', _('Upper Secondary')),
        ('tvet', _('TVET')),
        ('university', _('University')),
    ])
    description = models.TextField(blank=True)
    minimum_age = models.IntegerField(default=6)
    maximum_age = models.IntegerField(default=18)
    duration_years = models.IntegerField(default=6)
    
    class Meta:
        verbose_name = _("School Type")
        verbose_name_plural = _("School Types")
        ordering = ['name']

    def __str__(self):
        return self.name

class School(models.Model):
    """Model for schools"""
    name = models.CharField(max_length=100)
    school_code = models.CharField(max_length=20, unique=True)
    school_type = models.ForeignKey(SchoolType, on_delete=models.CASCADE, related_name='schools')
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='schools')
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='schools')
    
    # Location
    cell = models.CharField(max_length=50)
    village = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    
    # Contact Information
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    
    # Infrastructure
    total_classrooms = models.IntegerField(default=0)
    usable_classrooms = models.IntegerField(default=0)
    has_electricity = models.BooleanField(default=False)
    has_internet = models.BooleanField(default=False)
    has_library = models.BooleanField(default=False)
    has_laboratory = models.BooleanField(default=False)
    has_computer_lab = models.BooleanField(default=False)
    has_sanitation = models.BooleanField(default=False)
    has_clean_water = models.BooleanField(default=False)
    has_playground = models.BooleanField(default=False)
    has_dormitory = models.BooleanField(default=False)
    has_canteen = models.BooleanField(default=False)
    
    # Capacity and Enrollment
    student_capacity = models.IntegerField(default=0)
    current_enrollment = models.IntegerField(default=0)
    total_teachers = models.IntegerField(default=0)
    qualified_teachers = models.IntegerField(default=0)
    
    # School Management
    headteacher_name = models.CharField(max_length=100, blank=True)
    headteacher_phone = models.CharField(max_length=15, blank=True)
    deputy_headteacher_name = models.CharField(max_length=100, blank=True)
    
    # Academic Information
    languages_of_instruction = models.CharField(max_length=100, blank=True, help_text="e.g., Kinyarwanda, English, French")
    grade_levels_offered = models.CharField(max_length=100, blank=True, help_text="e.g., P1-P6, S1-S6")
    
    # Status and Accreditation
    is_active = models.BooleanField(default=True)
    is_government_school = models.BooleanField(default=True)
    is_boarding_school = models.BooleanField(default=False)
    accreditation_status = models.CharField(max_length=20, choices=[
        ('pending', _('Pending')),
        ('accredited', _('Accredited')),
        ('conditional', _('Conditional')),
        ('suspended', _('Suspended')),
    ], default='pending')
    established_year = models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("School")
        verbose_name_plural = _("Schools")
        ordering = ['district__name', 'name']

    def __str__(self):
        return f"{self.name} - {self.district.name}"

    @property
    def enrollment_rate(self):
        if self.student_capacity > 0:
            return (self.current_enrollment / self.student_capacity) * 100
        return 0

    @property
    def teacher_student_ratio(self):
        if self.total_teachers > 0:
            return self.current_enrollment / self.total_teachers
        return 0

    @property
    def qualified_teacher_percentage(self):
        if self.total_teachers > 0:
            return (self.qualified_teachers / self.total_teachers) * 100
        return 0

class Subject(models.Model):
    """Model for academic subjects"""
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=10, unique=True)
    category = models.CharField(max_length=30, choices=[
        ('core', _('Core Subject')),
        ('optional', _('Optional Subject')),
        ('vocational', _('Vocational Subject')),
        ('language', _('Language Subject')),
        ('science', _('Science Subject')),
        ('arts', _('Arts Subject')),
        ('sports', _('Sports/Physical Education')),
    ])
    description = models.TextField(blank=True)
    school_levels = models.ManyToManyField(SchoolType, related_name='subjects')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")
        ordering = ['name']

    def __str__(self):
        return self.name

class AcademicYear(models.Model):
    """Model for academic years"""
    name = models.CharField(max_length=20, unique=True)  # e.g., "2024-2025"
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Academic Year")
        verbose_name_plural = _("Academic Years")
        ordering = ['-start_date']

    def __str__(self):
        return self.name

class Student(models.Model):
    """Model for students"""
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=[
        ('M', _('Male')),
        ('F', _('Female')),
    ])
    national_id = models.CharField(max_length=16, blank=True)
    
    # Family Information
    parent_guardian_name = models.CharField(max_length=100)
    parent_guardian_phone = models.CharField(max_length=15)
    parent_guardian_occupation = models.CharField(max_length=50, blank=True)
    
    # Location
    home_district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='resident_students')
    home_sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='resident_students')
    home_cell = models.CharField(max_length=50)
    home_village = models.CharField(max_length=50)
    
    # Current Enrollment
    current_school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students', null=True, blank=True)
    current_grade_level = models.CharField(max_length=10, blank=True)
    enrollment_date = models.DateField(null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    completion_status = models.CharField(max_length=20, choices=[
        ('enrolled', _('Currently Enrolled')),
        ('completed', _('Completed')),
        ('transferred', _('Transferred')),
        ('dropped_out', _('Dropped Out')),
        ('deceased', _('Deceased')),
    ], default='enrolled')
    
    # Special Needs
    has_special_needs = models.BooleanField(default=False)
    special_needs_description = models.TextField(blank=True)
    
    # Financial
    fee_payment_status = models.CharField(max_length=20, choices=[
        ('paid', _('Fully Paid')),
        ('partial', _('Partially Paid')),
        ('unpaid', _('Unpaid')),
        ('exempt', _('Exempt')),
    ], default='unpaid')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        from django.utils import timezone
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

class Teacher(models.Model):
    """Model for teachers"""
    teacher_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=[
        ('M', _('Male')),
        ('F', _('Female')),
    ])
    national_id = models.CharField(max_length=16, unique=True)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    
    # Professional Information
    qualification_level = models.CharField(max_length=30, choices=[
        ('certificate', _('Certificate')),
        ('diploma', _('Diploma')),
        ('bachelor', _('Bachelor\'s Degree')),
        ('master', _('Master\'s Degree')),
        ('phd', _('PhD')),
    ])
    teaching_experience_years = models.IntegerField(default=0)
    specialization = models.CharField(max_length=100, blank=True)
    subjects_taught = models.ManyToManyField(Subject, related_name='teachers')
    
    # Employment
    current_school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='teachers', null=True, blank=True)
    employment_type = models.CharField(max_length=20, choices=[
        ('permanent', _('Permanent')),
        ('contract', _('Contract')),
        ('volunteer', _('Volunteer')),
        ('temporary', _('Temporary')),
    ])
    employment_start_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_qualified = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.teacher_id})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Enrollment(models.Model):
    """Model for student enrollments"""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='enrollments')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='enrollments')
    grade_level = models.CharField(max_length=10)
    
    # Enrollment details
    enrollment_date = models.DateField()
    completion_date = models.DateField(null=True, blank=True)
    enrollment_status = models.CharField(max_length=20, choices=[
        ('active', _('Active')),
        ('completed', _('Completed')),
        ('transferred', _('Transferred')),
        ('dropped', _('Dropped Out')),
        ('suspended', _('Suspended')),
    ], default='active')
    
    # Academic performance
    total_subjects = models.IntegerField(default=0)
    subjects_passed = models.IntegerField(default=0)
    overall_grade = models.CharField(max_length=2, blank=True)
    class_rank = models.IntegerField(null=True, blank=True)
    
    # Attendance
    total_days = models.IntegerField(default=0)
    days_attended = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Enrollment")
        verbose_name_plural = _("Enrollments")
        ordering = ['-academic_year__start_date', 'student__last_name']
        unique_together = ['student', 'school', 'academic_year']

    def __str__(self):
        return f"{self.student.full_name} - {self.school.name} ({self.academic_year.name})"

    @property
    def pass_rate(self):
        if self.total_subjects > 0:
            return (self.subjects_passed / self.total_subjects) * 100
        return 0

    @property
    def attendance_rate(self):
        if self.total_days > 0:
            return (self.days_attended / self.total_days) * 100
        return 0

class ExamResult(models.Model):
    """Model for exam results"""
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='exam_results')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exam_results')
    
    # Exam details
    exam_type = models.CharField(max_length=20, choices=[
        ('monthly', _('Monthly Test')),
        ('midterm', _('Midterm Exam')),
        ('final', _('Final Exam')),
        ('national', _('National Exam')),
    ])
    exam_date = models.DateField()
    
    # Scores
    marks_obtained = models.FloatField(validators=[MinValueValidator(0)])
    total_marks = models.FloatField(validators=[MinValueValidator(0)])
    grade = models.CharField(max_length=2, blank=True)
    passed = models.BooleanField(default=False)
    
    # Additional info
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='graded_exams')
    comments = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Exam Result")
        verbose_name_plural = _("Exam Results")
        ordering = ['-exam_date']

    def __str__(self):
        return f"{self.enrollment.student.full_name} - {self.subject.name} ({self.exam_date})"

    @property
    def percentage(self):
        if self.total_marks > 0:
            return (self.marks_obtained / self.total_marks) * 100
        return 0

class EducationAlert(models.Model):
    """Model for education-related alerts"""
    ALERT_TYPES = [
        ('enrollment', _('Enrollment Alert')),
        ('performance', _('Performance Alert')),
        ('attendance', _('Attendance Alert')),
        ('infrastructure', _('Infrastructure Alert')),
        ('staffing', _('Staffing Alert')),
        ('dropout', _('Dropout Alert')),
        ('budget', _('Budget Alert')),
        ('examination', _('Examination Alert')),
    ]
    
    SEVERITY_LEVELS = [
        ('low', _('Low')),
        ('medium', _('Medium')),
        ('high', _('High')),
        ('critical', _('Critical')),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS)
    
    # Targeting
    districts = models.ManyToManyField(District, related_name='education_alerts')
    schools = models.ManyToManyField(School, blank=True, related_name='education_alerts')
    school_types = models.ManyToManyField(SchoolType, blank=True, related_name='alerts')
    
    # Timeline
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Action Items
    recommended_actions = models.TextField()
    resources_available = models.TextField(blank=True)
    contact_person = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15)
    
    # Tracking
    schools_affected = models.IntegerField(default=0)
    students_affected = models.IntegerField(default=0)
    actions_taken = models.TextField(blank=True)
    effectiveness_score = models.FloatField(default=0.0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    
    # System Information
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_education_alerts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Education Alert")
        verbose_name_plural = _("Education Alerts")
        ordering = ['-created_at', '-severity']

    def __str__(self):
        return f"{self.title} ({self.get_severity_display()})"

class EducationTarget(models.Model):
    """Model for education targets and goals"""
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='education_targets')
    school_type = models.ForeignKey(SchoolType, on_delete=models.CASCADE, related_name='targets')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='targets')
    
    # Enrollment Targets
    target_enrollment = models.IntegerField()
    target_completion_rate = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    target_pass_rate = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    target_attendance_rate = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    # Infrastructure Targets
    target_classrooms = models.IntegerField(default=0)
    target_teacher_student_ratio = models.FloatField(default=35.0)
    target_qualified_teachers_percentage = models.FloatField(default=100.0)
    
    # Budget
    allocated_budget = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    budget_for_infrastructure = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    budget_for_teaching_materials = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    budget_for_teacher_training = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Progress Tracking
    achieved_enrollment = models.IntegerField(default=0)
    achieved_completion_rate = models.FloatField(default=0.0)
    achieved_pass_rate = models.FloatField(default=0.0)
    achieved_attendance_rate = models.FloatField(default=0.0)
    budget_utilized = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    # System Information
    set_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='set_education_targets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Education Target")
        verbose_name_plural = _("Education Targets")
        ordering = ['-academic_year__start_date', 'district__name']
        unique_together = ['district', 'school_type', 'academic_year']

    def __str__(self):
        return f"{self.district.name} - {self.school_type.name} ({self.academic_year.name})"

    @property
    def enrollment_achievement_rate(self):
        if self.target_enrollment > 0:
            return (self.achieved_enrollment / self.target_enrollment) * 100
        return 0

    @property
    def budget_utilization_rate(self):
        if self.allocated_budget > 0:
            return (float(self.budget_utilized) / float(self.allocated_budget)) * 100
        return 0