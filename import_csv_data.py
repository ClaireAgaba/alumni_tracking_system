import os
import django
import pandas as pd
from django.db import transaction
import uuid

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ubteb_system.settings')
django.setup()

from graduates.models import District, Course, ExamCenter

def import_districts():
    print("Importing districts...")
    df = pd.read_csv('graduates/data/districts.csv')
    districts_created = 0
    
    for _, row in df.iterrows():
        district_name = row['District'].strip()
        district, created = District.objects.get_or_create(
            name=district_name,
            defaults={'region': 'Central'}  # Default region, update as needed
        )
        if created:
            districts_created += 1
    
    print(f"Created {districts_created} districts")

def import_courses():
    print("Importing courses...")
    df = pd.read_csv('graduates/data/programs.csv')
    courses_created = 0
    
    for _, row in df.iterrows():
        program_name = row['ProgramName'].strip()
        # Create a unique code by combining first letters and a random string
        words = program_name.split()
        if len(words) >= 3:
            code_base = ''.join(word[0] for word in words[:3]).upper()
        else:
            code_base = ''.join(word[0] for word in words).upper()
        
        # Add a unique suffix
        code = f"{code_base}-{str(uuid.uuid4())[:4]}"
        
        course, created = Course.objects.get_or_create(
            name=program_name,
            defaults={
                'code': code,
                'department': 'General'  # Default department, update as needed
            }
        )
        if created:
            courses_created += 1
    
    print(f"Created {courses_created} courses")

def import_exam_centers():
    print("Importing exam centers...")
    df = pd.read_csv('graduates/data/examCenters.csv')
    centers_created = 0
    
    # Get a default district (Kampala)
    default_district = District.objects.get_or_create(name='Kampala', defaults={'region': 'Central'})[0]
    
    for _, row in df.iterrows():
        center_name = row['CenterName'].strip()
        # Create a unique code
        words = center_name.split()
        if len(words) >= 3:
            code_base = ''.join(word[0] for word in words[:3]).upper()
        else:
            code_base = ''.join(word[0] for word in words).upper()
        
        # Add a unique suffix
        code = f"{code_base}-{str(uuid.uuid4())[:4]}"
        
        center, created = ExamCenter.objects.get_or_create(
            name=center_name,
            defaults={
                'code': code,
                'district': default_district
            }
        )
        if created:
            centers_created += 1
    
    print(f"Created {centers_created} exam centers")

@transaction.atomic
def import_all_data():
    print("Starting data import...")
    import_districts()
    import_courses()
    import_exam_centers()
    print("Data import completed!")

if __name__ == "__main__":
    import_all_data()
