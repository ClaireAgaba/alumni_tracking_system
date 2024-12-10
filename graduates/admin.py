from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.urls import path, reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from .models import User, UserGroup, UserAuditLog, Graduate, District, Course, ExamCenter, GraduateBulkUpload
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Unregister the default Group admin
admin.site.unregister(Group)

@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'user_count')
    search_fields = ('name', 'description')
    ordering = ('name',)

    def user_count(self, obj):
        return obj.user_set.count()
    user_count.short_description = 'Users'

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('username', 'email', 'full_name', 'user_type', 'group', 'is_active', 'last_login', 'action_buttons')
    list_filter = ('user_type', 'group', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    
    fieldsets = (
        ('Personal Info', {
            'fields': (
                'username', 'password', 'email', 'first_name', 'last_name', 
                'phone_number', 'profile_image'
            )
        }),
        ('Role & Group', {
            'fields': ('user_type', 'group')
        }),
        ('Status', {
            'fields': ('is_active', 'must_change_password')
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined', 'last_password_change')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'first_name', 'last_name',
                'password1', 'password2', 'user_type', 'group'
            ),
        }),
    )
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Name'
    
    def action_buttons(self, obj):
        view_logs_url = reverse('admin:view-user-logs', args=[obj.pk])
        reset_password_url = reverse('admin:reset-user-password', args=[obj.pk])
        
        return format_html(
            '<a class="button" href="{}">View Logs</a> '
            '<a class="button" href="{}">Reset Password</a>',
            view_logs_url, reset_password_url
        )
    action_buttons.short_description = 'Actions'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:user_id>/logs/', self.view_user_logs, name='view-user-logs'),
            path('<int:user_id>/reset-password/', self.reset_user_password, name='reset-user-password'),
        ]
        return custom_urls + urls
    
    def view_user_logs(self, request, user_id):
        user = User.objects.get(pk=user_id)
        logs = UserAuditLog.objects.filter(user=user).order_by('-created_at')
        
        context = {
            'opts': self.model._meta,
            'title': f'Audit Logs for {user.username}',
            'user_obj': user,
            'logs': logs,
        }
        return render(request, 'admin/graduates/user/audit_logs.html', context)
    
    def reset_user_password(self, request, user_id):
        user = User.objects.get(pk=user_id)
        if request.method == 'POST':
            # Generate random password
            new_password = User.objects.make_random_password()
            user.set_password(new_password)
            user.must_change_password = True
            user.save()
            
            # Log the action
            UserAuditLog.objects.create(
                user=user,
                action='password_change',
                details='Password reset by admin',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            messages.success(request, f'Password reset for {user.username}. New password: {new_password}')
            return redirect('admin:graduates_user_changelist')
        
        context = {
            'opts': self.model._meta,
            'title': f'Reset Password for {user.username}',
            'user_obj': user,
        }
        return render(request, 'admin/graduates/user/reset_password.html', context)

@admin.register(UserAuditLog)
class UserAuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'details', 'ip_address', 'created_at')
    list_filter = ('action', 'created_at', 'user')
    search_fields = ('user__username', 'details', 'ip_address')
    ordering = ('-created_at',)
    readonly_fields = ('user', 'action', 'details', 'ip_address', 'user_agent', 'created_at', 'additional_data')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Graduate)
class GraduateAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'full_name', 'course', 
                   'graduation_date', 'graduation_year', 'is_employed', 'employer_name')
    list_filter = ('graduation_date', 'course', 'is_employed', 'current_district', 'exam_center')
    search_fields = ('registration_number', 'first_name', 'last_name', 'employer_name')
    date_hierarchy = 'graduation_date'
    readonly_fields = ('graduation_year', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Personal Information', {
            'fields': (
                'registration_number', 'first_name', 'last_name', 'gender',
                'date_of_birth', 'email', 'phone_number'
            )
        }),
        ('Academic Information', {
            'fields': ('course', 'graduation_date', 'graduation_year', 'exam_center')
        }),
        ('Employment Information', {
            'fields': (
                'is_employed', 'employer_name', 'job_title', 
                'employment_date', 'current_district'
            )
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Name'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If this is a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

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

@admin.register(GraduateBulkUpload)
class GraduateBulkUploadAdmin(admin.ModelAdmin):
    list_display = ('uploaded_by', 'uploaded_at', 'is_processed')
    list_filter = ('is_processed', 'uploaded_at')
    search_fields = ('uploaded_by__username',)
