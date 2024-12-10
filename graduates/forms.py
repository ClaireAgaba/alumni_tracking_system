from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from .models import User, Graduate, GraduateBulkUpload, Course, District, ExamCenter

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'user_type']

class GraduateForm(forms.ModelForm):
    class Meta:
        model = Graduate
        fields = [
            'first_name', 'last_name', 'gender', 'date_of_birth', 'contact_number',
            'email', 'registration_number', 'course', 'graduation_year',
            'is_employed', 'employer_name', 'job_title', 'employment_start_date',
            'current_district', 'exam_center'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'employment_start_date': forms.DateInput(attrs={'type': 'date'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'current_district': forms.Select(attrs={'class': 'form-select'}),
            'exam_center': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Sort choices alphabetically
        self.fields['course'].queryset = Course.objects.all().order_by('name')
        self.fields['current_district'].queryset = District.objects.all().order_by('name')
        self.fields['exam_center'].queryset = ExamCenter.objects.all().order_by('name')

class GraduateBulkUploadForm(forms.ModelForm):
    class Meta:
        model = GraduateBulkUpload
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={
                'accept': '.xlsx',
                'class': 'form-control'
            })
        }
        
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if not file.name.endswith('.xlsx'):
                raise ValidationError('Only Excel (XLSX) files are allowed.')
        return file
