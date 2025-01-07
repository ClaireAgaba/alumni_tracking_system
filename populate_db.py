import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ubteb_system.settings')
django.setup()

from graduates.models import Course, District, ExamCenter

def populate_database():
    # Create Districts
    districts = [
        'Kampala', 'Wakiso', 'Mukono', 'Jinja', 'Mbarara',
        'Gulu', 'Arua', 'Mbale', 'Masaka', 'Lira'
    ]
    
    for district_name in districts:
        District.objects.get_or_create(name=district_name)
        print(f"Created district: {district_name}")

    # Create Courses
    courses = [
        'Technical Drawing',
        'Electrical Installation',
        'Motor Vehicle Mechanics',
        'Building Construction',
        'Plumbing',
        'Carpentry and Joinery',
        'Metal Fabrication',
        'Computer Science',
        'Business Studies',
        'Agriculture'
    ]
    
    for course_name in courses:
        Course.objects.get_or_create(
            name=course_name,
            code=course_name.replace(' ', '').upper()[:6]
        )
        print(f"Created course: {course_name}")

    # Create Exam Centers
    exam_centers = [
        ('Uganda Technical College, Kyambogo', 'Kampala'),
        ('Uganda Technical College, Bushenyi', 'Mbarara'),
        ('Uganda Technical College, Lira', 'Lira'),
        ('Uganda Technical College, Elgon', 'Mbale'),
        ('Uganda Technical College, Kichwamba', 'Mbarara'),
        ('Buganda Technical Institute', 'Kampala'),
        ('Masaka Technical Institute', 'Masaka'),
        ('Nyakatare Technical Institute', 'Mbarara'),
        ('Iganga Technical Institute', 'Jinja'),
        ('Kaliro Technical Institute', 'Jinja')
    ]
    
    for center_name, district_name in exam_centers:
        district = District.objects.get(name=district_name)
        ExamCenter.objects.get_or_create(
            name=center_name,
            district=district,
            code=center_name.replace(' ', '').upper()[:6]
        )
        print(f"Created exam center: {center_name}")

if __name__ == "__main__":
    print("Starting database population...")
    populate_database()
    print("Database population completed!")
