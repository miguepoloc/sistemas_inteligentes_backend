# Generated by Django 4.2.7 on 2024-06-09 20:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0004_auto_20240609_2027'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='nodesstorage',
            unique_together={('node', 'date_time')},
        ),
    ]
