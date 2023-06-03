from django.core.validators import RegexValidator
from django.db import models
#from django.urls import reverse
from django.utils import timezone
from django_countries.fields import CountryField


class Alumni(models.Model):
    STATUS_CHOICES = [("graduated", "Graduated"), ("not graduated", "Not Graduated")]

    GENDER_CHOICES = [("male", "Male"), ("female", "Female")]
    
    PROGRAM_LEVEL_CHOICES =[("certificate", "Certificate"), ("diploma", "Diploma")]
    
    PROGRAM_CHOICES = [('ndict', 'NDICT'), ('ndbce', 'NDBCE')]
    
    TRANSCRIPT_CHOICES = [("recieved", "Recieved"), ("not recieved", "Not Recieved")]
    
    CERTIFICATE_CHOICES = [("recieved", "Recieved"), ("not recieved", "Not Recieved")]
    
    CENTER_CHOICES = [('mbi', 'MBI'), ('mubs', 'MUBS')]
    
    EMPLOYMENT_STATUS_CHOICES = [("yes", "Yes"), ("no", "No")]
    
    EMPLOYEMENT_ENTITY_CHOICES = [("government", "Government"), ("private", "Private")]

    current_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    
    
    surname = models.CharField(max_length=200, default=None)
    othernames = models.CharField(max_length=200, default=None)
    regNo = models.CharField(max_length=200, unique=True)
    dob = models.DateField(default=timezone.now)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="male")
    phone_number = RegexValidator(regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!")
    email=models.EmailField(max_length=50, unique=True)
    nationality = CountryField()
    district = models.CharField(max_length=30, blank=True)
    program_level = models.CharField(max_length=30, choices=PROGRAM_LEVEL_CHOICES, default='certificate')
    program = models.CharField(max_length=50, choices=PROGRAM_CHOICES, default='ndict')
    center = models.CharField(max_length=50, choices= CENTER_CHOICES, default='mbi')
    start_year = models.DateField(default=timezone.now)
    finish_year = models.DateField(default=timezone.now)
    transcript_status = models.CharField(max_length=30, choices=TRANSCRIPT_CHOICES, default='recieved')
    certificate_status = models.CharField(max_length=30, choices=CERTIFICATE_CHOICES, default='received')
    employment_status = models.CharField(max_length=10, choices=EMPLOYMENT_STATUS_CHOICES, default='yes')
    employment_entity = models.CharField(max_length=20, choices=EMPLOYEMENT_ENTITY_CHOICES, default='government')
    
    

    #mobile_num_regex = RegexValidator(regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!")
    #parent_mobile_number = models.CharField(validators=[mobile_num_regex], max_length=13, blank=True)

    
    #others = models.TextField(blank=True)
    #passport = models.ImageField(blank=True, upload_to="students/passports/")

    class Meta:
        ordering = ["regNo"]

    def __str__(self):
        return f"{self.regNo}"

    # def get_absolute_url(self):
    #     return reverse("alumni-detail", kwargs={"pk": self.pk})


