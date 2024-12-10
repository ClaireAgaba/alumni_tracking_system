from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Graduate, GraduateBulkUpload

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'user_type']

class GraduateForm(forms.ModelForm):
    class Meta:
        model = Graduate
        fields = [
            'first_name', 'last_name', 'gender', 'date_of_birth',
            'contact_number', 'email', 'registration_number',
            'course_name', 'graduation_year', 'is_employed',
            'employer_name', 'job_title', 'employment_date'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'employment_date': forms.DateInput(attrs={'type': 'date'}),
        }

class GraduateBulkUploadForm(forms.ModelForm):
    class Meta:
        model = GraduateBulkUpload
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file.name.endswith('.xlsx'):
            raise forms.ValidationError('Only Excel files (.xlsx) are allowed.')
        return file
