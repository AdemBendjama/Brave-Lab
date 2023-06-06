# Generated by Django 4.2 on 2023-06-06 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_home', '0049_alter_evaluation_request'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluation',
            name='request',
        ),
        migrations.AddField(
            model_name='evaluation',
            name='appointment',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_home.appointment'),
        ),
    ]