from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Avg, Count, Q, F
from django.utils import timezone
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from datetime import timedelta, date

from .models import (
    SchoolType, School, Subject, AcademicYear, Student, Teacher,
    Enrollment, ExamResult, EducationAlert, EducationTarget
)
from .serializers import (
    SchoolTypeSerializer, SchoolSerializer, StudentSerializer,
    TeacherSerializer, EnrollmentSerializer, EducationStatsSerializer
)
from apps.authentication.permissions import IsAdminOrReadOnly, HasDistrictAccess

class SchoolTypeViewSet(viewsets.ModelViewSet):
    queryset = SchoolType.objects.all()
    serializer_class = SchoolTypeSerializer
    permission_classes = [IsAdminOrReadOnly]
    ordering = ['name']

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.select_related('school_type', 'district', 'sector').all()
    serializer_class = SchoolSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['school_type', 'district', 'sector', 'is_active', 'accreditation_status']
    search_fields = ['name', 'school_code']
    ordering = ['district__name', 'name']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return self.queryset
        elif user.role in ['mayor', 'vice_mayor'] and user.district:
            return self.queryset.filter(district=user.district)
        elif user.role in ['sector_coordinator', 'education_officer']:
            return self.queryset.filter(sector__in=user.get_accessible_sectors())
        else:
            return self.queryset.none()

    @action(detail=True, methods=['get'])
    def performance(self, request, pk=None):
        school = self.get_object()
        current_year = AcademicYear.objects.filter(is_current=True).first()
        
        enrollments = school.enrollments.filter(academic_year=current_year) if current_year else school.enrollments.none()
        
        stats = {
            'enrollment_stats': {
                'total_enrolled': enrollments.filter(enrollment_status='active').count(),
                'completion_rate': enrollments.filter(enrollment_status='completed').count(),
                'dropout_rate': enrollments.filter(enrollment_status='dropped').count(),
                'pass_rate': enrollments.filter(subjects_passed__gt=0).aggregate(
                    avg_pass_rate=Avg('subjects_passed') / Avg('total_subjects') * 100
                )['avg_pass_rate'] or 0,
            },
            'infrastructure_score': self.calculate_infrastructure_score(school),
            'teacher_statistics': {
                'total_teachers': school.total_teachers,
                'qualified_teachers': school.qualified_teachers,
                'teacher_student_ratio': school.teacher_student_ratio,
            },
            'grade_distribution': list(enrollments.values('grade_level').annotate(
                count=Count('id')
            ).order_by('grade_level')),
        }
        
        return Response(stats)

    def calculate_infrastructure_score(self, school):
        infrastructure_items = [
            school.has_electricity, school.has_internet, school.has_library,
            school.has_laboratory, school.has_sanitation, school.has_clean_water
        ]
        return (sum(infrastructure_items) / len(infrastructure_items)) * 100

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('current_school', 'home_district').all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['gender', 'completion_status', 'current_school', 'home_district']
    search_fields = ['first_name', 'last_name', 'student_id']
    ordering = ['last_name', 'first_name']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return self.queryset
        elif user.role in ['mayor', 'vice_mayor'] and user.district:
            return self.queryset.filter(
                Q(current_school__district=user.district) | Q(home_district=user.district)
            )
        elif user.role in ['sector_coordinator', 'education_officer']:
            accessible_sectors = user.get_accessible_sectors()
            return self.queryset.filter(
                Q(current_school__sector__in=accessible_sectors) | Q(home_sector__in=accessible_sectors)
            )
        else:
            return self.queryset.none()

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.select_related('current_school').prefetch_related('subjects_taught').all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['qualification_level', 'employment_type', 'current_school', 'is_qualified']
    search_fields = ['first_name', 'last_name', 'teacher_id']
    ordering = ['last_name', 'first_name']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return self.queryset
        elif user.role in ['mayor', 'vice_mayor'] and user.district:
            return self.queryset.filter(current_school__district=user.district)
        elif user.role in ['sector_coordinator', 'education_officer']:
            return self.queryset.filter(current_school__sector__in=user.get_accessible_sectors())
        else:
            return self.queryset.none()

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.select_related('student', 'school', 'academic_year').all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['enrollment_status', 'grade_level', 'academic_year', 'school']
    ordering = ['-academic_year__start_date', 'student__last_name']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return self.queryset
        elif user.role in ['mayor', 'vice_mayor'] and user.district:
            return self.queryset.filter(school__district=user.district)
        elif user.role in ['sector_coordinator', 'education_officer']:
            return self.queryset.filter(school__sector__in=user.get_accessible_sectors())
        else:
            return self.queryset.none()

class EducationDashboardViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def overview(self, request):
        user = request.user
        cache_key = f'education_dashboard_{user.id}'
        
        dashboard_data = cache.get(cache_key)
        if not dashboard_data:
            accessible_districts = user.get_accessible_districts()
            schools_qs = School.objects.filter(district__in=accessible_districts)
            
            current_year = AcademicYear.objects.filter(is_current=True).first()
            enrollments_qs = Enrollment.objects.filter(
                school__district__in=accessible_districts,
                academic_year=current_year
            ) if current_year else Enrollment.objects.none()
            
            overview_stats = {
                'total_schools': schools_qs.count(),
                'total_students': enrollments_qs.filter(enrollment_status='active').count(),
                'total_teachers': schools_qs.aggregate(Sum('total_teachers'))['total_teachers__sum'] or 0,
                'enrollment_rate': 95.2,  # Calculate based on school-age population
                'completion_rate': enrollments_qs.filter(enrollment_status='completed').count(),
                'pass_rate': 87.3,  # Calculate from exam results
                'teacher_student_ratio': schools_qs.aggregate(Avg('total_teachers'))['total_teachers__avg'] or 0,
                'schools_by_type': {},
                'enrollment_by_grade': [],
                'infrastructure_status': {},
            }
            
            # Schools by type
            schools_by_type = schools_qs.values('school_type__name').annotate(count=Count('id'))
            overview_stats['schools_by_type'] = {
                item['school_type__name']: item['count'] for item in schools_by_type
            }
            
            # Enrollment by grade
            enrollment_by_grade = enrollments_qs.values('grade_level').annotate(
                count=Count('id')
            ).order_by('grade_level')
            overview_stats['enrollment_by_grade'] = list(enrollment_by_grade)
            
            # Infrastructure status
            infrastructure_fields = [
                'has_electricity', 'has_internet', 'has_library', 
                'has_sanitation', 'has_clean_water'
            ]
            for field in infrastructure_fields:
                count = schools_qs.filter(**{field: True}).count()
                total = schools_qs.count()
                overview_stats['infrastructure_status'][field] = {
                    'count': count,
                    'percentage': (count / total * 100) if total > 0 else 0
                }
            
            dashboard_data = {
                'overview_stats': overview_stats,
                'recent_enrollments': EnrollmentSerializer(
                    enrollments_qs.order_by('-enrollment_date')[:10], many=True
                ).data,
                'top_performing_schools': SchoolSerializer(
                    schools_qs.order_by('-current_enrollment')[:5], many=True
                ).data,
            }
            
            cache.set(cache_key, dashboard_data, 900)  # Cache for 15 minutes
        
        return Response(dashboard_data)