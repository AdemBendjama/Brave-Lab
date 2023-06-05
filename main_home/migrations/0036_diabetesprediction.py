# Generated by Django 4.2 on 2023-06-05 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_home', '0035_remove_bloodbank_blood_type_remove_bloodbank_client_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiabetesPrediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.FloatField(choices=[(0.0, 'Male'), (1.0, 'Female')])),
                ('age', models.FloatField()),
                ('hypertension', models.FloatField(choices=[(0.0, 'No'), (1.0, 'Yes')])),
                ('heart_disease', models.FloatField(choices=[(0.0, 'No'), (1.0, 'Yes')])),
                ('smoking_history', models.FloatField(choices=[(0.0, 'Never'), (1.0, 'No Info'), (2.0, 'Former'), (3.0, 'Not Current'), (4.0, 'Ever'), (5.0, 'Current')])),
                ('bmi', models.FloatField()),
                ('hba1c_level', models.FloatField()),
                ('blood_glucose_level', models.FloatField()),
            ],
        ),
    ]
