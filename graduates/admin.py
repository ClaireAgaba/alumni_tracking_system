from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Graduate, GraduateBulkUpload

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser')
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
    list_display = ('registration_number', 'first_name', 'last_name', 'course_name', 'graduation_year', 'is_employed')
    list_filter = ('graduation_year', 'is_employed', 'course_name')
    search_fields = ('registration_number', 'first_name', 'last_name', 'course_name')

class GraduateBulkUploadAdmin(admin.ModelAdmin):
    list_display = ('uploaded_by', 'uploaded_at', 'is_processed')
    list_filter = ('is_processed', 'uploaded_at')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Graduate, GraduateAdmin)
admin.site.register(GraduateBulkUpload, GraduateBulkUploadAdmin)
