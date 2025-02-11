# Generated by Django 5.1.4 on 2025-02-11 11:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('HR_Management', '0001_initial'),
        ('Masters', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='circular_department',
            name='Department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.department_detials'),
        ),
        migrations.AddField(
            model_name='circular_department',
            name='Location_Name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.location_detials'),
        ),
        migrations.AddField(
            model_name='circular_details',
            name='CircularCreateEmployee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.employee_personal_form_detials'),
        ),
        migrations.AddField(
            model_name='circular_details',
            name='Location_Name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.location_detials'),
        ),
        migrations.AddField(
            model_name='circular_details',
            name='Venue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.administration_master_details'),
        ),
        migrations.AddField(
            model_name='circular_department',
            name='Circular',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='HR_Management.circular_details'),
        ),
        migrations.AddField(
            model_name='circular_employee',
            name='Circular',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='HR_Management.circular_details'),
        ),
        migrations.AddField(
            model_name='circular_employee',
            name='Employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.employee_personal_form_detials'),
        ),
        migrations.AddField(
            model_name='circular_employee',
            name='Location_Name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.location_detials'),
        ),
        migrations.AddField(
            model_name='current_history_detials',
            name='CurrentEmployeementLocations',
            field=models.ForeignKey(blank=True, db_column='current_employment_location_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='current_employment_locations', to='Masters.location_detials'),
        ),
        migrations.AddField(
            model_name='current_history_detials',
            name='Employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.employee_personal_form_detials'),
        ),
        migrations.AddField(
            model_name='current_history_detials',
            name='Location',
            field=models.ForeignKey(blank=True, db_column='location_history_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='location_history', to='Masters.location_detials'),
        ),
        migrations.AddField(
            model_name='document_checklist_detials',
            name='Employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.employee_personal_form_detials'),
        ),
        migrations.AddField(
            model_name='document_checklist_detials',
            name='EmployeeCurrentHistoryInfo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='HR_Management.current_history_detials'),
        ),
        migrations.AddField(
            model_name='document_checklist_detials',
            name='Location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.location_detials'),
        ),
        migrations.AddField(
            model_name='dutyroustermaster',
            name='Department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.department_detials'),
        ),
        migrations.AddField(
            model_name='dutyroustermaster',
            name='Location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='location_shift', to='Masters.location_detials'),
        ),
        migrations.AddField(
            model_name='employee_advance_request',
            name='Location_Name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.location_detials'),
        ),
        migrations.AddField(
            model_name='employee_attendance',
            name='Employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.employee_personal_form_detials'),
        ),
        migrations.AddField(
            model_name='employee_attendance',
            name='Location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.location_detials'),
        ),
        migrations.AddField(
            model_name='employee_complaint',
            name='AgainstEmployeeDepartment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.department_detials'),
        ),
        migrations.AddField(
            model_name='employee_complaint',
            name='AgainstEmployeeId',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='complaints_against', to='Masters.employee_personal_form_detials'),
        ),
        migrations.AddField(
            model_name='employee_complaint',
            name='EmployeeId',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='complaints', to='Masters.employee_personal_form_detials'),
        ),
        migrations.AddField(
            model_name='employee_complaint',
            name='Location_Name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.location_detials'),
        ),
        migrations.AddField(
            model_name='employee_leave_register',
            name='Employee_Id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='HR_Management.current_history_detials'),
        ),
        migrations.AddField(
            model_name='employee_leave_register',
            name='Location_Name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.location_detials'),
        ),
        migrations.AddField(
            model_name='employee_medical_information_detials',
            name='Employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.employee_personal_form_detials'),
        ),
        migrations.AddField(
            model_name='employee_medical_information_detials',
            name='Location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.location_detials'),
        ),
        migrations.AddField(
            model_name='document_checklist_detials',
            name='EmployeeMedicalInfo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='HR_Management.employee_medical_information_detials'),
        ),
        migrations.AddField(
            model_name='current_history_detials',
            name='EmployeeMedicalInfo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='HR_Management.employee_medical_information_detials'),
        ),
        migrations.AddField(
            model_name='employee_payslips',
            name='Employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.employee_personal_form_detials'),
        ),
        migrations.AddField(
            model_name='employee_payslips',
            name='Location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.location_detials'),
        ),
        migrations.AddField(
            model_name='employee_performance',
            name='Employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.employee_personal_form_detials'),
        ),
        migrations.AddField(
            model_name='employee_performance',
            name='Location_Name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.location_detials'),
        ),
        migrations.AddField(
            model_name='employee_skills_detials',
            name='Employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.employee_personal_form_detials'),
        ),
        migrations.AddField(
            model_name='employee_skills_detials',
            name='Location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.location_detials'),
        ),
        migrations.AddField(
            model_name='employeement_history_detials',
            name='Employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.employee_personal_form_detials'),
        ),
        migrations.AddField(
            model_name='employeement_history_detials',
            name='Location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.location_detials'),
        ),
        migrations.AddField(
            model_name='employee_medical_information_detials',
            name='EmployeementHistory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='HR_Management.employeement_history_detials'),
        ),
        migrations.AddField(
            model_name='document_checklist_detials',
            name='EmployeementHistory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='HR_Management.employeement_history_detials'),
        ),
        migrations.AddField(
            model_name='current_history_detials',
            name='EmployeementHistory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='HR_Management.employeement_history_detials'),
        ),
        migrations.AddField(
            model_name='financial_history_detials',
            name='Employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.employee_personal_form_detials'),
        ),
        migrations.AddField(
            model_name='financial_history_detials',
            name='EmployeeCurrentHistoryInfo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='HR_Management.current_history_detials'),
        ),
        migrations.AddField(
            model_name='financial_history_detials',
            name='EmployeeMedicalInfo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='HR_Management.employee_medical_information_detials'),
        ),
        migrations.AddField(
            model_name='financial_history_detials',
            name='EmployeementHistory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='HR_Management.employeement_history_detials'),
        ),
        migrations.AddField(
            model_name='financial_history_detials',
            name='Location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.location_detials'),
        ),
        migrations.AddField(
            model_name='employee_advance_request',
            name='Employee_Id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='HR_Management.financial_history_detials'),
        ),
        migrations.AddField(
            model_name='document_checklist_detials',
            name='EmployeeFinancialHistory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='HR_Management.financial_history_detials'),
        ),
        migrations.AddField(
            model_name='hr_complaintaction',
            name='Complaint',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='HR_Management.employee_complaint'),
        ),
        migrations.AddField(
            model_name='hr_complaintaction',
            name='Location_Name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.location_detials'),
        ),
        migrations.AddField(
            model_name='shiftdetails_master',
            name='Employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Masters.employee_personal_form_detials'),
        ),
        migrations.AddField(
            model_name='shiftdetails_master',
            name='Location_Name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.location_detials'),
        ),
        migrations.AddField(
            model_name='shiftdetails_master',
            name='Shift_Id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='HR_Management.dutyroustermaster'),
        ),
        migrations.AddField(
            model_name='trainee_personal_form_details',
            name='BloodGroup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.bloodgroup_detials'),
        ),
        migrations.AddField(
            model_name='trainee_personal_form_details',
            name='Tittle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Masters.title_detials'),
        ),
        migrations.AlterUniqueTogether(
            name='employee_skills_detials',
            unique_together={('Employee', 'Skill', 'Level')},
        ),
    ]
