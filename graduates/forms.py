from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from .models import User, Graduate, GraduateBulkUpload, Course, District, ExamCenter, UserGroup

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'user_type']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number',
                 'user_type', 'group', 'profile_image')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name in ['first_name', 'last_name', 'email']:
                field.required = True

class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number',
                 'user_type', 'group', 'profile_image', 'is_active')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name in ['first_name', 'last_name', 'email']:
                field.required = True

class GraduateForm(forms.ModelForm):
    class Meta:
        model = Graduate
        fields = [
            'registration_number', 'first_name', 'last_name', 'gender',
            'date_of_birth', 'email', 'phone_number', 'course',
            'graduation_date', 'is_employed', 'employer_name', 'job_title',
            'employment_date', 'current_district', 'exam_center'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'graduation_date': forms.DateInput(attrs={'type': 'date'}),
            'employment_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_registration_number(self):
        registration_number = self.cleaned_data.get('registration_number')
        if registration_number:
            registration_number = registration_number.upper()
        return registration_number

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
