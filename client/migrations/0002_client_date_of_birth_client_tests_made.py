# Generated by Django 4.2 on 2023-05-15 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='date_of_birth',
            field=models.DateField(default='2003-03-08'),
        ),
        migrations.AddField(
            model_name='client',
            name='tests_made',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
