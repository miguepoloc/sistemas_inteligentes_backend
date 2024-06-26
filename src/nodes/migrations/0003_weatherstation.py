# Generated by Django 4.2.7 on 2024-02-05 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0002_nodesstorage_battery_level_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherStation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('date', models.DateTimeField(unique=True)),
                ('temperature', models.FloatField()),
                ('dew_point', models.FloatField()),
                ('solar_radiation', models.IntegerField()),
                ('vapor_pressure_deficit', models.FloatField()),
                ('relative_humidity', models.FloatField()),
                ('precipitation', models.FloatField()),
                ('wind_speed', models.FloatField()),
                ('wind_gust', models.FloatField()),
                ('wind_direction', models.IntegerField()),
                ('solar_panel', models.IntegerField()),
                ('battery', models.IntegerField()),
                ('delta_t', models.IntegerField()),
                ('sun_duration', models.IntegerField()),
                ('evapotranspiration', models.FloatField(null=True)),
                ('units', models.JSONField()),
            ],
            options={
                'db_table': 'weather_station',
                'ordering': ['-date'],
            },
        ),
    ]
