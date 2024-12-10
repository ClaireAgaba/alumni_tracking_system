from django.contrib import admin
from .models import User, Graduate, Course, District, ExamCenter, GraduateBulkUpload

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type')
    list_filter = ('user_type', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')
    list_filter = ('department',)
    search_fields = ('name', 'department')

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'region')
    list_filter = ('region',)
    search_fields = ('name', 'region')

@admin.register(ExamCenter)
class ExamCenterAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Graduate)
class GraduateAdmin(admin.ModelAdmin):
    list_display = (
        'registration_number', 'first_name', 'last_name',
        'course', 'graduation_year', 'is_employed',
        'current_district', 'exam_center'
    )
    list_filter = (
        'graduation_year', 'is_employed',
        'course', 'current_district', 'exam_center'
    )
    search_fields = (
        'registration_number', 'first_name', 'last_name',
        'employer_name', 'job_title'
    )
    date_hierarchy = 'created_at'

@admin.register(GraduateBulkUpload)
class GraduateBulkUploadAdmin(admin.ModelAdmin):
    list_display = ('uploaded_by', 'uploaded_at', 'is_processed')
    list_filter = ('is_processed', 'uploaded_at')
    search_fields = ('uploaded_by__username',)
