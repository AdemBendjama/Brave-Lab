# Generated by Django 4.2 on 2023-06-03 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_home', '0032_alter_payment_appointment_fee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='appointment_fee',
            field=models.DecimalField(decimal_places=2, default=5.0, max_digits=10),
        ),
    ]
