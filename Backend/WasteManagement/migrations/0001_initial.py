# Generated by Django 5.1.4 on 2025-02-11 11:52

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='handOver',
            fields=[
                ('handOver_Id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('wasteCategory', models.CharField(max_length=20)),
                ('wasteColor', models.CharField(max_length=20)),
                ('weight', models.IntegerField()),
                ('collecter', models.CharField(max_length=50)),
                ('collecterCnt', models.BigIntegerField()),
                ('incharge', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'handOver',
            },
        ),
        migrations.CreateModel(
            name='WasteCount',
            fields=[
                ('WasteCount_Id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('wasteCategory', models.CharField(max_length=20)),
                ('wasteColor', models.CharField(max_length=20)),
                ('weight', models.IntegerField()),
                ('totalWst', models.IntegerField()),
                ('Status', models.BooleanField(default=True)),
                ('created_by', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'WasteCount',
            },
        ),
        migrations.CreateModel(
            name='wasteManagement',
            fields=[
                ('wasteManagement_Id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('wasteCategory', models.CharField(blank=True, max_length=20, null=True)),
                ('wasteColor', models.CharField(blank=True, max_length=20, null=True)),
                ('bagCount', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'wasteManagement',
            },
        ),
    ]
