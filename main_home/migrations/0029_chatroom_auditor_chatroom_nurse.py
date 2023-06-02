# Generated by Django 4.2 on 2023-06-02 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auditor', '0002_auditor_date_of_birth'),
        ('nurse', '0002_nurse_date_of_birth'),
        ('main_home', '0028_chatroom_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='auditor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auditor.auditor'),
        ),
        migrations.AddField(
            model_name='chatroom',
            name='nurse',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='nurse.nurse'),
        ),
    ]
