# Generated by Django 4.2 on 2023-05-17 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_home', '0008_remove_appointment_documents_appointment_document'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='attended',
            new_name='arrived',
        ),
        migrations.AlterField(
            model_name='appointment',
            name='payment_option',
            field=models.CharField(choices=[('PP', 'Pre-Pay'), ('OR', 'On-Receive')], default='OR', max_length=2),
        ),
    ]
