# Generated by Django 4.2.7 on 2023-12-03 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_user_document_alter_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='document',
            field=models.CharField(blank=True, default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=50),
            preserve_default=False,
        ),
    ]
