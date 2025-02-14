# Generated by Django 5.1.4 on 2025-02-13 18:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('LeninManagement', '0001_initial'),
        ('Masters', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dept_wise_lenin_min_max_details',
            name='Department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lenin_departments', to='Masters.department_detials'),
        ),
        migrations.AddField(
            model_name='dept_wise_lenin_min_max_details',
            name='Location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lenin_locations', to='Masters.location_detials'),
        ),
        migrations.AddField(
            model_name='dept_wise_lenin_min_max_details',
            name='LeninCategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lenin_Dept_Categories', to='LeninManagement.lenin_catg_master_details'),
        ),
        migrations.AddField(
            model_name='lenin_stock_details',
            name='LeninCategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lenin_Stock_Categories', to='LeninManagement.lenin_catg_master_details'),
        ),
        migrations.AddField(
            model_name='leninmaster_details',
            name='LeninCategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lenin_Category', to='LeninManagement.lenin_catg_master_details'),
        ),
        migrations.AddField(
            model_name='lenin_stock_details',
            name='LeninType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lenin_Stock_Types', to='LeninManagement.leninmaster_details'),
        ),
        migrations.AddField(
            model_name='dept_wise_lenin_min_max_details',
            name='LeninType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lenin_types', to='LeninManagement.leninmaster_details'),
        ),
    ]
