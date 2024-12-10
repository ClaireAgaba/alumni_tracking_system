import csv
from django.core.management.base import BaseCommand
from graduates.models import District, Course, ExamCenter

class Command(BaseCommand):
    help = 'Load reference data from CSV files'

    def add_arguments(self, parser):
        parser.add_argument('--districts', type=str, help='Path to districts CSV file')
        parser.add_argument('--courses', type=str, help='Path to courses CSV file')
        parser.add_argument('--centers', type=str, help='Path to exam centers CSV file')

    def handle(self, *args, **options):
        if options['districts']:
            self.load_districts(options['districts'])
        if options['courses']:
            self.load_courses(options['courses'])
        if options['centers']:
            self.load_centers(options['centers'])

    def load_districts(self, filepath):
        self.stdout.write('Loading districts...')
        with open(filepath, 'r', encoding='utf-8-sig') as file:
            # Skip the header and separator lines
            next(file)  # Skip "District"
            next(file)  # Skip "--------"
            
            for line in file:
                district_name = line.strip()
                if district_name:
                    District.objects.get_or_create(
                        name=district_name,
                        defaults={'region': 'Central'}  # Default region
                    )
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded districts from {filepath}'))

    def load_courses(self, filepath):
        self.stdout.write('Loading courses...')
        with open(filepath, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Course.objects.get_or_create(
                    code=row['code'],
                    defaults={
                        'name': row['name'],
                        'department': row.get('department', 'Default Department')
                    }
                )
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded courses from {filepath}'))

    def load_centers(self, filepath):
        self.stdout.write('Loading exam centers...')
        with open(filepath, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    district = District.objects.get(name=row['district'])
                    ExamCenter.objects.get_or_create(
                        code=row['code'],
                        defaults={
                            'name': row['name'],
                            'district': district
                        }
                    )
                except District.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(
                            f"District '{row['district']}' not found for center '{row['name']}'"
                        )
                    )
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded exam centers from {filepath}'))
