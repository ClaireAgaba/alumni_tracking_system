from django.db import migrations, models
import django.db.models.deletion
from django.utils import timezone

class Migration(migrations.Migration):

    dependencies = [
        ('graduates', '0003_usergroup_user_created_at_user_failed_login_attempts_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='graduate',
            old_name='contact_number',
            new_name='phone_number',
        ),
        migrations.RenameField(
            model_name='graduate',
            old_name='employment_start_date',
            new_name='employment_date',
        ),
        migrations.RemoveField(
            model_name='graduate',
            name='graduation_year',
        ),
        migrations.AddField(
            model_name='graduate',
            name='graduation_date',
            field=models.DateField(default=timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='graduate',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='graduate',
            name='employer_name',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='graduate',
            name='job_title',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='graduate',
            name='current_district',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='graduates.district'),
        ),
        migrations.AlterField(
            model_name='graduate',
            name='exam_center',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='graduates.examcenter'),
        ),
        migrations.AlterField(
            model_name='graduate',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='graduates.course'),
        ),
        migrations.AlterModelOptions(
            name='graduate',
            options={'ordering': ['-graduation_date', 'last_name', 'first_name']},
        ),
        migrations.AddIndex(
            model_name='graduate',
            index=models.Index(fields=['graduation_date'], name='graduates_g_graduat_e6a6ac_idx'),
        ),
        migrations.AddIndex(
            model_name='graduate',
            index=models.Index(fields=['registration_number'], name='graduates_g_registr_f21543_idx'),
        ),
    ]
