from django import forms
from django.contrib.auth.forms import UserCreationForm
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
            'district', 'exam_center'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'employment_start_date': forms.DateInput(attrs={'type': 'date'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'district': forms.Select(attrs={'class': 'form-select'}),
            'exam_center': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Sort choices alphabetically
        self.fields['course'].queryset = Course.objects.all().order_by('name')
        self.fields['district'].queryset = District.objects.all().order_by('name')
        
        # Filter exam centers based on selected district
        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['exam_center'].queryset = ExamCenter.objects.filter(
                    district_id=district_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.district:
            self.fields['exam_center'].queryset = ExamCenter.objects.filter(
                district=self.instance.district).order_by('name')
        else:
            self.fields['exam_center'].queryset = ExamCenter.objects.none()

class GraduateBulkUploadForm(forms.ModelForm):
    class Meta:
        model = GraduateBulkUpload
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file.name.endswith('.xlsx'):
            raise forms.ValidationError('Only Excel files (.xlsx) are allowed.')
        return file
