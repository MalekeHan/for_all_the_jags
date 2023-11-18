# Generated by Django 4.2.7 on 2023-11-18 21:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('spot', '0003_survey_busy_str_survey_comfort_str_survey_noise_str_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survey',
            name='busy_str',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='comfort_str',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='noise_str',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='parking_str',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='wifi_str',
        ),
        migrations.AlterField(
            model_name='survey',
            name='busy_level',
            field=models.IntegerField(blank=True, choices=[(0, 'Very busy'), (1, 'Moderately Busy'), (2, 'Not busy')], default=None, null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='comfort_level',
            field=models.IntegerField(blank=True, choices=[(0, 'Not comfortable'), (1, 'Moderately comfortable'), (2, 'Very comfortable')], default=None, null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='noise_level',
            field=models.IntegerField(blank=True, choices=[(0, 'Very noisy'), (1, 'Moderate noise'), (2, 'Quiet enough for a zoom meeting')], default=None, null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='parking_situation',
            field=models.IntegerField(blank=True, choices=[(0, 'Very difficult parking'), (1, 'Moderate parking'), (2, 'Very easy parking')], default=None, null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='survey',
            name='wifi_situation',
            field=models.IntegerField(blank=True, choices=[(0, 'No WIFI'), (1, 'WIFI, but must be paid'), (2, 'WIFI, Free')], default=None, null=True),
        ),
    ]