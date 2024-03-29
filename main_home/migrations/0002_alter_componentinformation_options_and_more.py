# Generated by Django 4.2 on 2023-05-16 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_home', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='componentinformation',
            options={'verbose_name_plural': 'Component Info'},
        ),
        migrations.AlterModelOptions(
            name='laboratory',
            options={'verbose_name_plural': 'Laboratories'},
        ),
        migrations.AlterModelOptions(
            name='test',
            options={'verbose_name_plural': 'Tests Preformed'},
        ),
        migrations.AlterModelOptions(
            name='testoffered',
            options={'verbose_name_plural': 'Offered Tests'},
        ),
        migrations.RenameField(
            model_name='componentinformation',
            old_name='hf_range',
            new_name='high_female_range',
        ),
        migrations.RenameField(
            model_name='componentinformation',
            old_name='hm_range',
            new_name='high_male_range',
        ),
        migrations.RenameField(
            model_name='componentinformation',
            old_name='lf_range',
            new_name='low_female_range',
        ),
        migrations.RenameField(
            model_name='componentinformation',
            old_name='lm_range',
            new_name='low_male_range',
        ),
    ]
