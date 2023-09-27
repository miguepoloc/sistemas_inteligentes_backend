# Generated by Django 4.2.5 on 2023-09-27 04:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Nodes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('master', 'Master'), ('worker', 'Worker')], max_length=255)),
                ('description', models.TextField(blank=True)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
            ],
            options={
                'db_table': 'nodes',
            },
        ),
        migrations.CreateModel(
            name='NodesStorage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('date_time', models.DateTimeField()),
                ('temperature', models.DecimalField(decimal_places=2, max_digits=5)),
                ('humidity', models.DecimalField(decimal_places=2, max_digits=5)),
                ('pressure', models.DecimalField(decimal_places=2, max_digits=5)),
                ('altitude', models.DecimalField(decimal_places=2, max_digits=5)),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nodes.nodes')),
            ],
            options={
                'db_table': 'nodes_storage',
                'ordering': ['-date_time'],
            },
        ),
    ]
