import csv
from django.core.management.base import BaseCommand
from graduates.models import District, Course, ExamCenter

class Command(BaseCommand):
    help = 'Load reference data from CSV files'

    def add_arguments(self, parser):
        parser.add_argument('--districts', type=str, help='Path to districts CSV file')
        parser.add_argument('--programs', type=str, help='Path to programs.csv file')
        parser.add_argument('--examCenters', type=str, help='Path to examCenters.csv file')

    def handle(self, *args, **options):
        if options['districts']:
            self.load_districts(options['districts'])
        if options['programs']:
            self.load_courses(options['programs'])
        if options['examCenters']:
            self.load_centers(options['examCenters'])

    def load_districts(self, filepath):
        """Load districts from CSV file"""
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
        """Load courses/programs from CSV file"""
        self.stdout.write('Loading courses...')
        with open(filepath, 'r', encoding='utf-8-sig') as file:
            # Skip the header and separator lines
            next(file)  # Skip "ProgramName"
            next(file)  # Skip "--------"
            
            for line in file:
                program_name = line.strip()
                if program_name:
                    Course.objects.get_or_create(
                        name=program_name,
                        defaults={'department': 'Default Department'}
                    )
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded courses from {filepath}'))

    def load_centers(self, filepath):
        """Load exam centers from CSV file"""
        self.stdout.write('Loading exam centers...')
        with open(filepath, 'r', encoding='utf-8-sig') as file:
            # Skip the header and separator lines
            next(file)  # Skip "CenterName"
            next(file)  # Skip "--------"
            
            for line in file:
                center_name = line.strip()
                if center_name:
                    ExamCenter.objects.get_or_create(name=center_name)
                    
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded exam centers from {filepath}'))
