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
    
    return render(request, 'graduates/add_graduate.html', {'form': form})

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
                
                # Debug: Print column names and first row
                print("Columns in Excel:", df.columns.tolist())
                if not df.empty:
                    print("First row:", df.iloc[0].to_dict())
                
                required_columns = [
                    'first_name', 'last_name', 'gender', 'date_of_birth',
                    'contact_number', 'email', 'registration_number',
                    'course_name', 'graduation_year', 'is_employed'
                ]
                
                # Convert column names to lowercase and strip whitespace
                df.columns = df.columns.str.lower().str.strip()
                
                # Debug: Print columns after conversion
                print("Columns after conversion:", df.columns.tolist())
                
                # Verify required columns
                missing_columns = [col for col in required_columns if col not in df.columns]
                if missing_columns:
                    raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
                
                # Process each row
                successful_imports = 0
                for index, row in df.iterrows():
                    try:
                        # Convert 'Yes'/'No' to boolean for is_employed
                        is_employed = str(row['is_employed']).lower() in ['yes', 'true', '1', 'y']
                        
                        # Convert date fields
                        try:
                            date_of_birth = pd.to_datetime(row['date_of_birth']).date()
                        except:
                            date_of_birth = None
                            print(f"Invalid date_of_birth format in row {index + 2}")
                        
                        try:
                            employment_date = pd.to_datetime(row['employment_date']).date() if pd.notna(row.get('employment_date')) else None
                        except:
                            employment_date = None
                            print(f"Invalid employment_date format in row {index + 2}")
                        
                        Graduate.objects.create(
                            first_name=str(row['first_name']),
                            last_name=str(row['last_name']),
                            gender=str(row['gender']),
                            date_of_birth=date_of_birth,
                            contact_number=str(row['contact_number']),
                            email=str(row['email']),
                            registration_number=str(row['registration_number']),
                            course_name=str(row['course_name']),
                            graduation_year=int(float(row['graduation_year'])),
                            is_employed=is_employed,
                            employer_name=str(row.get('employer_name', '')),
                            job_title=str(row.get('job_title', '')),
                            employment_date=employment_date,
                            created_by=request.user
                        )
                        successful_imports += 1
                    except Exception as row_error:
                        print(f"Error in row {index + 2}: {str(row_error)}")
                        continue
                
                upload.is_processed = True
                upload.save()
                
                if successful_imports > 0:
                    messages.success(request, f'Successfully imported {successful_imports} graduates!')
                else:
                    messages.warning(request, 'No graduates were imported. Please check the file format.')
                return redirect('graduate_list')
            except ValueError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f'Error processing file: {str(e)}')
    else:
        form = GraduateBulkUploadForm()
    
    return render(request, 'graduates/upload_graduates.html', {'form': form})

@login_required
def download_excel_template(request):
    # Create Excel template
    df = pd.DataFrame(columns=[
        'first_name', 'last_name', 'gender', 'date_of_birth',
        'contact_number', 'email', 'registration_number',
        'course_name', 'graduation_year', 'is_employed',
        'employer_name', 'job_title', 'employment_date'
    ])
    
    # Add example data
    example_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'gender': 'M',
        'date_of_birth': '1995-01-01',
        'contact_number': '1234567890',
        'email': 'john.doe@example.com',
        'registration_number': 'REG001',
        'course_name': 'Computer Science',
        'graduation_year': 2023,
        'is_employed': 'Yes',
        'employer_name': 'Tech Company Ltd',
        'job_title': 'Software Developer',
        'employment_date': '2023-06-01'
    }
    df = pd.concat([df, pd.DataFrame([example_data])], ignore_index=True)
    
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

@login_required
@user_passes_test(lambda u: is_admin(u) or is_field_officer(u))
def edit_graduate(request, pk):
    graduate = get_object_or_404(Graduate, pk=pk)
    if request.method == 'POST':
        form = GraduateForm(request.POST, instance=graduate)
        if form.is_valid():
            form.save()
            messages.success(request, 'Graduate updated successfully!')
            return redirect('graduate_list')
    else:
        form = GraduateForm(instance=graduate)
    
    return render(request, 'graduates/add_graduate.html', {
        'form': form,
        'edit_mode': True,
        'graduate': graduate
    })
