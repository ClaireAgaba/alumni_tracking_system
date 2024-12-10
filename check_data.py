import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ubteb_system.settings')
django.setup()

from graduates.models import ExamCenter, District, Course

print("\nExam Centers:")
print("-" * 50)
for center in ExamCenter.objects.all():
    print(f"ID: {center.id}, Name: {center.name}, Code: {center.code}, District: {center.district.name}")

print("\nDistricts:")
print("-" * 50)
for district in District.objects.all():
    print(f"ID: {district.id}, Name: {district.name}, Region: {district.region}")

print("\nCourses:")
print("-" * 50)
for course in Course.objects.all():
    print(f"ID: {course.id}, Name: {course.name}, Code: {course.code}")
