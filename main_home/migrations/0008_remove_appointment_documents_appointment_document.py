# Generated by Django 4.2 on 2023-05-16 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_home', '0007_alter_medicaldocument_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='documents',
        ),
        migrations.AddField(
            model_name='appointment',
            name='document',
            field=models.ImageField(null=True, upload_to='medical_documents'),
        ),
    ]
