# Generated by Django 4.2 on 2023-06-09 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_home', '0054_alter_bloodbank_capacity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
