from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
import json

class UserGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Administrator'),
        ('field_officer', 'Field Officer'),
        ('officer', 'Officer'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='officer')
    phone_number = models.CharField(max_length=20, blank=True)
    group = models.ForeignKey(UserGroup, on_delete=models.SET_NULL, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    last_password_change = models.DateTimeField(default=timezone.now)
    must_change_password = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    # Add related_name to avoid clashes
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set'
    )

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
    def save(self, *args, **kwargs):
        # Set is_staff based on user type
        self.is_staff = self.user_type in ['admin', 'field_officer']
        # Set is_superuser for admin
        self.is_superuser = self.user_type == 'admin'
        # Update the updated_at timestamp
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        # Log the save action
        UserAuditLog.objects.create(
            user=self,
            action='user_updated',
            details=f'User profile updated: {self.username}'
        )

class UserAuditLog(models.Model):
    ACTION_CHOICES = (
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('login_failed', 'Login Failed'),
        ('password_change', 'Password Change'),
        ('user_created', 'User Created'),
        ('user_updated', 'User Updated'),
        ('user_deleted', 'User Deleted'),
        ('group_changed', 'Group Changed'),
        ('role_changed', 'Role Changed'),
        ('permission_changed', 'Permission Changed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    details = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    additional_data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.created_at}"

    @classmethod
    def log_action(cls, user, action, details='', ip_address=None, user_agent='', additional_data=None):
        return cls.objects.create(
            user=user,
            action=action,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
            additional_data=additional_data or {}
        )

class District(models.Model):
    name = models.CharField(max_length=100, unique=True)
    region = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Course(models.Model):
    name = models.CharField(max_length=200, unique=True)
    department = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class ExamCenter(models.Model):
    name = models.CharField(max_length=200, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Graduate(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    
    # Personal Information
    registration_number = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    
    # Academic Information
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    graduation_date = models.DateField()
    exam_center = models.ForeignKey(ExamCenter, on_delete=models.SET_NULL, null=True)
    
    # Employment Information
    is_employed = models.BooleanField(default=False)
    employer_name = models.CharField(max_length=200, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    employment_date = models.DateField(null=True, blank=True)
    current_district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    
    # System Information
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.registration_number})"

    @property
    def graduation_year(self):
        return self.graduation_date.year if self.graduation_date else None

    class Meta:
        ordering = ['-graduation_date', 'last_name', 'first_name']
        indexes = [
            models.Index(fields=['graduation_date']),
            models.Index(fields=['registration_number']),
        ]

class GraduateBulkUpload(models.Model):
    file = models.FileField(upload_to='graduate_uploads/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Bulk upload by {self.uploaded_by.username} at {self.uploaded_at}"
