# Generated by Django 4.2 on 2023-06-05 21:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_home', '0036_diabetesprediction'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysisrequest',
            name='diabetes',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_home.diabetesprediction'),
        ),
    ]
