# Generated by Django 4.2 on 2023-05-16 16:51

from django.db import migrations, models
import django.db.models.deletion
import main_home.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0002_client_date_of_birth_client_tests_made'),
        ('nurse', '0002_nurse_date_of_birth'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalysisRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('finish_time', models.DateTimeField(blank=True, null=True)),
                ('accepted', models.BooleanField(default=False)),
                ('finished', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('working-on', 'Working On'), ('finished', 'Finished')], default='pending', max_length=45)),
            ],
            options={
                'db_table': 'analysis_request',
            },
        ),
        migrations.CreateModel(
            name='BloodBank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blood_type', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=3)),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.client')),
            ],
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
            ],
            options={
                'db_table': 'component',
            },
        ),
        migrations.CreateModel(
            name='ComponentInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('unit', models.CharField(blank=True, max_length=45, null=True)),
                ('lm_range', models.FloatField(blank=True, null=True)),
                ('hm_range', models.FloatField(blank=True, null=True)),
                ('lf_range', models.FloatField(blank=True, null=True)),
                ('hf_range', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'component_info',
            },
        ),
        migrations.CreateModel(
            name='Laboratory',
            fields=[
                ('name', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('location', models.CharField(max_length=45)),
                ('description', models.CharField(max_length=45)),
                ('monthly_revenue', models.FloatField()),
                ('tests_made', models.FloatField()),
            ],
            options={
                'db_table': 'laboratory',
            },
        ),
        migrations.CreateModel(
            name='MedicalDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='medical_documents/')),
            ],
            options={
                'db_table': 'medical_document',
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('confirmed', models.BooleanField(default=False)),
                ('components', models.ManyToManyField(to='main_home.component')),
            ],
            options={
                'db_table': 'test',
            },
        ),
        migrations.CreateModel(
            name='TestOffered',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'db_table': 'test_offered',
            },
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('duration', models.DurationField(blank=True, null=True)),
                ('approved', models.BooleanField(default=False)),
                ('blood_sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_home.bloodbank')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_home.analysisrequest')),
                ('tests', models.ManyToManyField(to='main_home.test')),
            ],
            options={
                'db_table': 'test_result',
            },
        ),
        migrations.AddField(
            model_name='test',
            name='test_offered',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_home.testoffered'),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
                ('test_result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_home.testresult')),
            ],
            options={
                'db_table': 'report',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_option', models.CharField(choices=[('PP', 'Pre-Pay'), ('OR', 'On-Receive')], max_length=2)),
                ('payment_status', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.client')),
                ('laboratory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_home.laboratory')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_home.report')),
            ],
            options={
                'db_table': 'invoice',
            },
        ),
        migrations.AddField(
            model_name='component',
            name='info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_home.componentinformation'),
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('topic', models.CharField(choices=[('Billing', 'Billing'), ('Customer Service', 'Customer Service'), ('Facilities', 'Facilities'), ('Quality of Service', 'Quality of Service'), ('Other', 'Other')], max_length=20)),
                ('description', models.CharField(max_length=1000)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.client')),
            ],
            options={
                'db_table': 'complaint',
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(validators=[main_home.models.validate_date_not_past])),
                ('description', models.CharField(max_length=1000)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_option', models.CharField(choices=[('PP', 'Pre-Pay'), ('OR', 'On-Receive')], max_length=2)),
                ('payment_status', models.BooleanField(default=False)),
                ('attended', models.BooleanField(default=False)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.client')),
                ('documents', models.ManyToManyField(to='main_home.medicaldocument')),
                ('tests_requested', models.ManyToManyField(to='main_home.test')),
            ],
            options={
                'db_table': 'appointment',
            },
        ),
        migrations.AddField(
            model_name='analysisrequest',
            name='appointment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_home.appointment'),
        ),
        migrations.AddField(
            model_name='analysisrequest',
            name='nurse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nurse.nurse'),
        ),
    ]