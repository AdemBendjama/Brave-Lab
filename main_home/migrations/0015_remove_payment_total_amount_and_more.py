# Generated by Django 4.2 on 2023-05-18 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_home', '0014_payment_nurse_tests_fee_alter_payment_tests_fee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='total_amount',
        ),
        migrations.AddField(
            model_name='payment',
            name='total_amount_payed',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='payment',
            name='appointment_fee',
            field=models.DecimalField(decimal_places=2, default=200.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='payment',
            name='nurse_tests_fee',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='payment',
            name='tests_fee',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]