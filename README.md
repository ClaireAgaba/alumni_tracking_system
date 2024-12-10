# UBTEB Graduate Tracking System

A Django-based web application for tracking UBTEB graduates. The system allows field officers to collect and manage graduate data, while providing comprehensive reporting and visualization features.

## Features

- Multi-user role system (Admin, Field Officer, Officer)
- Graduate data collection through web forms
- Bulk data import via Excel sheets
- Excel template generation
- Dashboard with data visualization
- Export functionality (PDF and Excel)
- Secure authentication and authorization

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## User Roles

1. **Admin**
   - Create and manage user accounts
   - Access all system features
   - Generate reports
   - Manage system settings

2. **Field Officer**
   - Collect graduate data
   - Input data manually through forms
   - Upload data via Excel sheets
   - View and edit their submitted data

3. **Officer**
   - View collected data
   - Generate reports
   - Export data to PDF/Excel
   - Access dashboard analytics

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details
