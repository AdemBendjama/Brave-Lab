# Generated by Django 4.2 on 2023-06-06 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_home', '0046_remove_analysisrequest_evaluation_evaluation_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='request',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main_home.analysisrequest'),
        ),
    ]
