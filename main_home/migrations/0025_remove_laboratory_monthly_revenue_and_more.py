# Generated by Django 4.2 on 2023-05-20 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_home', '0024_remove_invoice_payment_option'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='laboratory',
            name='monthly_revenue',
        ),
        migrations.AlterField(
            model_name='invoice',
            name='creation_time',
            field=models.DateField(auto_now_add=True),
        ),
    ]
