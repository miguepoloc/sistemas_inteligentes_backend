# Generated by Django 4.2.5 on 2023-10-23 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_alter_visitors_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visitors',
            name='city',
        ),
        migrations.RemoveField(
            model_name='visitors',
            name='country',
        ),
        migrations.RemoveField(
            model_name='visitors',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='visitors',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='visitors',
            name='region',
        ),
        migrations.AddField(
            model_name='visitors',
            name='page',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]