from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Graduate, GraduateBulkUpload, District, Course, ExamCenter

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_active')
    list_filter = ('user_type', 'is_active')
    search_fields = ('username', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        ('Permissions', {'fields': ('user_type', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'user_type', 'email', 'first_name', 'last_name', 'phone_number'),
        }),
    )

class GraduateAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'first_name', 'last_name', 'course', 'graduation_year', 'is_employed')
    list_filter = ('graduation_year', 'is_employed', 'course', 'district')
    search_fields = ('registration_number', 'first_name', 'last_name', 'course__name')
    date_hierarchy = 'created_at'

class GraduateBulkUploadAdmin(admin.ModelAdmin):
    list_display = ('uploaded_by', 'uploaded_at', 'is_processed')
    list_filter = ('is_processed', 'uploaded_at')

class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'region')
    list_filter = ('region',)
    search_fields = ('name', 'region')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'department')
    list_filter = ('department',)
    search_fields = ('code', 'name', 'department')

class ExamCenterAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'district')
    list_filter = ('district',)
    search_fields = ('code', 'name', 'district__name')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Graduate, GraduateAdmin)
admin.site.register(GraduateBulkUpload, GraduateBulkUploadAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(ExamCenter, ExamCenterAdmin)
