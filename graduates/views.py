from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Count
import pandas as pd
from reportlab.pdfgen import canvas
from .models import Graduate, GraduateBulkUpload
from .forms import GraduateForm, GraduateBulkUploadForm

def is_admin(user):
    return user.user_type == 'admin'

def is_field_officer(user):
    return user.user_type == 'field_officer'

@login_required
def dashboard(request):
    total_graduates = Graduate.objects.count()
    employed_graduates = Graduate.objects.filter(is_employed=True).count()
    graduates_by_year = Graduate.objects.values('graduation_year').annotate(count=Count('id'))
    
    context = {
        'total_graduates': total_graduates,
        'employed_graduates': employed_graduates,
        'graduates_by_year': graduates_by_year,
    }
    return render(request, 'graduates/dashboard.html', context)

@login_required
@user_passes_test(lambda u: is_admin(u) or is_field_officer(u))
def add_graduate(request):
    if request.method == 'POST':
        form = GraduateForm(request.POST)
        if form.is_valid():
            graduate = form.save(commit=False)
            graduate.created_by = request.user
            graduate.save()
            messages.success(request, 'Graduate added successfully!')
            return redirect('dashboard')
    else:
        form = GraduateForm()
    
    return render(request, 'graduates/graduate_form.html', {'form': form})

@login_required
def graduate_list(request):
    graduates = Graduate.objects.all().order_by('-created_at')
    return render(request, 'graduates/graduate_list.html', {'graduates': graduates})

@login_required
@user_passes_test(lambda u: is_admin(u) or is_field_officer(u))
def upload_graduates(request):
    if request.method == 'POST':
        form = GraduateBulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.uploaded_by = request.user
            upload.save()
            
            # Process Excel file
            try:
                df = pd.read_excel(upload.file.path)
                for _, row in df.iterrows():
                    Graduate.objects.create(
                        first_name=row['First Name'],
                        last_name=row['Last Name'],
                        gender=row['Gender'],
                        date_of_birth=row['Date of Birth'],
                        contact_number=row['Contact Number'],
                        email=row['Email'],
                        registration_number=row['Registration Number'],
                        course_name=row['Course Name'],
                        graduation_year=row['Graduation Year'],
                        is_employed=row['Is Employed'],
                        employer_name=row.get('Employer Name', ''),
                        job_title=row.get('Job Title', ''),
                        employment_date=row.get('Employment Date', None),
                        created_by=request.user
                    )
                upload.is_processed = True
                upload.save()
                messages.success(request, 'Graduates uploaded successfully!')
            except Exception as e:
                messages.error(request, f'Error processing file: {str(e)}')
            return redirect('graduate_list')
    else:
        form = GraduateBulkUploadForm()
    
    return render(request, 'graduates/upload_graduates.html', {'form': form})

@login_required
def download_excel_template(request):
    # Create Excel template
    df = pd.DataFrame(columns=[
        'First Name', 'Last Name', 'Gender', 'Date of Birth',
        'Contact Number', 'Email', 'Registration Number',
        'Course Name', 'Graduation Year', 'Is Employed',
        'Employer Name', 'Job Title', 'Employment Date'
    ])
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=graduate_template.xlsx'
    df.to_excel(response, index=False)
    return response

@login_required
def export_graduates_excel(request):
    graduates = Graduate.objects.all()
    df = pd.DataFrame(list(graduates.values()))
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=graduates.xlsx'
    df.to_excel(response, index=False)
    return response

@login_required
def export_graduates_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=graduates.pdf'
    
    # Create PDF
    p = canvas.Canvas(response)
    p.drawString(100, 800, "UBTEB Graduates Report")
    
    y = 750
    for graduate in Graduate.objects.all():
        p.drawString(100, y, f"{graduate.first_name} {graduate.last_name} - {graduate.registration_number}")
        y -= 20
        if y < 50:
            p.showPage()
            y = 750
    
    p.showPage()
    p.save()
    return response
