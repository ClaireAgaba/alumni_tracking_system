from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Administrator'),
        ('field_officer', 'Field Officer'),
        ('viewer', 'Viewer'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='viewer')
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

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
    )
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    
    # Academic Information
    registration_number = models.CharField(max_length=50, unique=True)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    graduation_year = models.IntegerField()
    
    # Employment Information
    is_employed = models.BooleanField(default=False)
    employer_name = models.CharField(max_length=200, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    employment_start_date = models.DateField(blank=True, null=True)
    
    # System Information
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Location and Institution
    current_district = models.ForeignKey(District, on_delete=models.PROTECT, null=True, help_text="Current district of residence")
    exam_center = models.ForeignKey(ExamCenter, on_delete=models.PROTECT, help_text="Institution attended")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.registration_number}"

class GraduateBulkUpload(models.Model):
    file = models.FileField(upload_to='graduate_uploads/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Bulk upload by {self.uploaded_by.username} at {self.uploaded_at}"
