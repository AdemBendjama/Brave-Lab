# Generated by Django 4.2 on 2023-05-16 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_home', '0002_alter_componentinformation_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='description',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
