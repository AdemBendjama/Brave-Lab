# Generated by Django 4.2 on 2023-06-06 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_home', '0044_rename_diabetesprediction_anemia_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='anemia',
            old_name='request',
            new_name='result',
        ),
        migrations.RenameField(
            model_name='diabetes',
            old_name='request',
            new_name='result',
        ),
    ]