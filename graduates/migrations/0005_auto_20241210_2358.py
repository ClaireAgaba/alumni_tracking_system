# Generated by Django 4.2 on 2024-12-10 20:58

from django.db import migrations, models
import django.db.models.deletion
from django.utils import timezone

class Migration(migrations.Migration):

    dependencies = [
        ('graduates', '0004_alter_graduate_model'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='graduate',
            options={'ordering': ['-graduation_date', 'last_name', 'first_name']},
        ),
        migrations.AddIndex(
            model_name='graduate',
            index=models.Index(fields=['graduation_date'], name='grad_graduation_date_idx'),
        ),
        migrations.AddIndex(
            model_name='graduate',
            index=models.Index(fields=['registration_number'], name='grad_registration_number_idx'),
        ),
    ]
