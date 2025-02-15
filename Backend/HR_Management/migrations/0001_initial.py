# Generated by Django 5.1.4 on 2025-02-13 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Circular_Department',
            fields=[
                ('CircularDepartment_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Status', models.CharField(default='Pending', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'Circular_Department',
            },
        ),
        migrations.CreateModel(
            name='Circular_Details',
            fields=[
                ('Circular_Id', models.AutoField(primary_key=True, serialize=False)),
                ('CircularDate', models.DateField(blank=True, null=True)),
                ('CircularTime', models.TimeField(blank=True, null=True)),
                ('Subject', models.CharField(default='', max_length=100)),
                ('Remarks', models.CharField(default='', max_length=100)),
                ('CreatedBy', models.CharField(default='', max_length=100)),
                ('Status', models.CharField(default='Pending', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'Circular_Details',
            },
        ),
        migrations.CreateModel(
            name='Circular_Employee',
            fields=[
                ('CircularEmployee_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Status', models.CharField(default='Pending', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'Circular_Employee',
            },
        ),
        migrations.CreateModel(
            name='Current_History_Detials',
            fields=[
                ('EmpHistory_Id', models.AutoField(primary_key=True, serialize=False)),
                ('DateOfJoining', models.CharField(blank=True, max_length=30, null=True)),
                ('ReportingManager', models.CharField(blank=True, max_length=30, null=True)),
                ('GovtLeave', models.CharField(blank=True, max_length=30, null=True)),
                ('CasualLeave', models.CharField(blank=True, max_length=30, null=True)),
                ('SickLeave', models.CharField(blank=True, max_length=30, null=True)),
                ('TotalLeave', models.CharField(blank=True, max_length=30, null=True)),
                ('WorkEmail', models.CharField(blank=True, max_length=50, null=True)),
                ('ProbationPeriod', models.CharField(blank=True, max_length=50, null=True)),
                ('Months', models.CharField(blank=True, max_length=50, null=True)),
                ('Years', models.CharField(blank=True, max_length=50, null=True)),
                ('TrainingGivenBy', models.CharField(blank=True, max_length=50, null=True)),
                ('TrainingVerifiedBy', models.CharField(blank=True, max_length=50, null=True)),
                ('TrainingCompletedDate', models.CharField(blank=True, max_length=50, null=True)),
                ('IsPF_Applicable', models.BooleanField(default=False)),
                ('created_by', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(default='', max_length=30)),
            ],
            options={
                'db_table': 'Current_History_Detials',
            },
        ),
        migrations.CreateModel(
            name='Document_Checklist_Detials',
            fields=[
                ('EmpHistory_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Resume', models.BinaryField(blank=True, null=True)),
                ('PanCard', models.BinaryField(blank=True, null=True)),
                ('AadharCard', models.BinaryField(blank=True, null=True)),
                ('BankPassbook', models.BinaryField(blank=True, null=True)),
                ('ExperienceCertificate', models.BinaryField(blank=True, null=True)),
                ('MedicalFitness', models.BinaryField(blank=True, null=True)),
                ('Offerletter', models.BinaryField(blank=True, null=True)),
                ('created_by', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(default='', max_length=30)),
            ],
            options={
                'db_table': 'Document_Checklist_Detials',
            },
        ),
        migrations.CreateModel(
            name='DutyRousterMaster',
            fields=[
                ('ShiftId', models.CharField(max_length=70, primary_key=True, serialize=False)),
                ('ShiftName', models.CharField(default='', max_length=50)),
                ('StartTime', models.TimeField()),
                ('EndTime', models.TimeField()),
                ('Status', models.BooleanField(default=True)),
                ('Created_by', models.CharField(max_length=70)),
                ('Created_at', models.DateTimeField(auto_now_add=True)),
                ('Updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'DutyRousterMaster',
            },
        ),
        migrations.CreateModel(
            name='Employee_Advance_Request',
            fields=[
                ('Advance_RequestId', models.AutoField(primary_key=True, serialize=False)),
                ('Request_Date', models.DateField(blank=True, null=True)),
                ('Request_Amount', models.IntegerField()),
                ('Request_Reason', models.TextField()),
                ('Repayment_Due', models.IntegerField(blank=True, null=True)),
                ('Reject_Reason', models.TextField(default='')),
                ('IssuedDate', models.DateField(blank=True, null=True)),
                ('Issuever_Name', models.CharField(default='', max_length=100)),
                ('AmountDeduct_PerMonth', models.IntegerField(blank=True, null=True)),
                ('Installment_Status', models.CharField(default='Pending', max_length=100)),
                ('No_of_MonthPaid', models.IntegerField(blank=True, null=True)),
                ('PaidAmount', models.CharField(default='', max_length=200)),
                ('Status', models.CharField(default='Pending', max_length=50)),
                ('CreatedBy', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'Employee_Advance_Request',
            },
        ),
        migrations.CreateModel(
            name='Employee_Attendance',
            fields=[
                ('Attendance_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Date', models.DateField(blank=True, null=True)),
                ('In_Time', models.TimeField(blank=True, null=True)),
                ('Out_Time', models.TimeField(blank=True, null=True)),
                ('Working_Hours', models.FloatField(blank=True, null=True)),
                ('Attendance_Status', models.CharField(default='', max_length=50)),
                ('CreatedBy', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'Employee_Attendance',
            },
        ),
        migrations.CreateModel(
            name='Employee_Complaint',
            fields=[
                ('Complaint_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Complaint', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('IncidentDate', models.DateField(blank=True, null=True)),
                ('IncidentTime', models.TimeField(blank=True, null=True)),
                ('Description', models.TextField(blank=True, null=True)),
                ('Remarks', models.TextField(blank=True, null=True)),
                ('AgainstEmployeeName', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('Witness', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('CreatedBy', models.CharField(default='', max_length=100)),
                ('Status', models.CharField(default='Pending', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'Employee_Complaint',
            },
        ),
        migrations.CreateModel(
            name='Employee_Leave_Register',
            fields=[
                ('Leave_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Leave_Type', models.CharField(max_length=100)),
                ('PermissionDate', models.DateField(blank=True, null=True)),
                ('FromDate', models.DateField(blank=True, null=True)),
                ('ToDate', models.DateField(blank=True, null=True)),
                ('DaysCount', models.IntegerField(blank=True, null=True)),
                ('Medical_Certificate', models.BinaryField(blank=True, null=True)),
                ('FromTime', models.TimeField(blank=True, null=True)),
                ('ToTime', models.TimeField(blank=True, null=True)),
                ('HoursCount', models.CharField(blank=True, default='0', max_length=60, null=True)),
                ('Reason', models.TextField()),
                ('Status', models.CharField(default='Pending', max_length=50)),
                ('Reject_Reason', models.TextField()),
                ('CreatedBy', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'Employee_Leave_Register',
            },
        ),
        migrations.CreateModel(
            name='Employee_Medical_Information_Detials',
            fields=[
                ('EmpHistory_Id', models.AutoField(primary_key=True, serialize=False)),
                ('PreExisiting_Medical_Condition', models.CharField(blank=True, max_length=100, null=True)),
                ('PsychiatricMedicines', models.CharField(blank=True, max_length=30, null=True)),
                ('PsychiatricMedicinesDetails', models.TextField(blank=True, null=True)),
                ('PreviousOperation', models.CharField(blank=True, max_length=30, null=True)),
                ('SurgeriesDetails', models.TextField(blank=True, null=True)),
                ('VaccinationStatus', models.CharField(blank=True, max_length=30, null=True)),
                ('VaccinationStatusDetails', models.TextField(blank=True, null=True)),
                ('MedicalFitnessCertificate', models.BinaryField(blank=True, null=True)),
                ('AnnualMedicalCheckup', models.BinaryField(blank=True, null=True)),
                ('created_by', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(default='', max_length=30)),
            ],
            options={
                'db_table': 'Employee_Medical_Information_Detials',
            },
        ),
        migrations.CreateModel(
            name='Employee_PaySlips',
            fields=[
                ('PaySlip_Id', models.AutoField(primary_key=True, serialize=False)),
                ('EmployeePayslip', models.BinaryField()),
                ('PaySlip_Date', models.DateField(blank=True, null=True)),
                ('CreatedBy', models.CharField(max_length=100)),
                ('Paid_Salary', models.FloatField(blank=True, null=True)),
                ('Status', models.CharField(default='', max_length=50)),
                ('SalaryMonth', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'Employee_PaySlips',
            },
        ),
        migrations.CreateModel(
            name='Employee_Performance',
            fields=[
                ('Performance_Id', models.AutoField(primary_key=True, serialize=False)),
                ('HikeType', models.CharField(default='', max_length=100)),
                ('AllowanceName', models.CharField(default='', max_length=100)),
                ('PreviousAllowance', models.IntegerField(blank=True, null=True)),
                ('PreviousAllowanceAmount', models.FloatField(blank=True, null=True)),
                ('NewAllowance', models.IntegerField(blank=True, null=True)),
                ('NewAllowanceAmount', models.FloatField(blank=True, null=True)),
                ('FinalAllowanceAmount', models.FloatField(blank=True, null=True)),
                ('Date', models.DateField(blank=True, null=True)),
                ('Current_Payment', models.FloatField(blank=True, null=True)),
                ('Performance_Rate', models.CharField(default='', max_length=120)),
                ('Hike_Percentage', models.IntegerField(blank=True, null=True)),
                ('Hike_Amount', models.FloatField(blank=True, null=True)),
                ('New_Pay', models.FloatField(blank=True, null=True)),
                ('Remarks', models.CharField(default='', max_length=100)),
                ('ApprovedBy', models.CharField(default='', max_length=100)),
                ('CreatedBy', models.CharField(default='', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'Employee_Performance',
            },
        ),
        migrations.CreateModel(
            name='Employee_Skills_Detials',
            fields=[
                ('Skill_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Skill', models.CharField(blank=True, max_length=30, null=True)),
                ('Level', models.CharField(blank=True, max_length=30, null=True)),
                ('created_by', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(default='', max_length=30)),
            ],
            options={
                'db_table': 'Employee_Skills_Detials',
            },
        ),
        migrations.CreateModel(
            name='Employeement_History_Detials',
            fields=[
                ('EmpHistory_Id', models.AutoField(primary_key=True, serialize=False)),
                ('PreviousWorkExperience', models.CharField(blank=True, max_length=30, null=True)),
                ('PreviousWorkPFNumber', models.CharField(blank=True, max_length=30, null=True)),
                ('PreviousWorkESINumber', models.CharField(blank=True, max_length=30, null=True)),
                ('PFNumber', models.CharField(blank=True, max_length=30, null=True)),
                ('ESINumber', models.CharField(blank=True, max_length=30, null=True)),
                ('NoOfYears', models.CharField(blank=True, max_length=30, null=True)),
                ('WorkStationNameAddress', models.TextField(blank=True, null=True)),
                ('ReasonForLeft', models.CharField(blank=True, max_length=50, null=True)),
                ('WorkStationPhoneNo', models.CharField(blank=True, max_length=30, null=True)),
                ('EmployeePaySlip', models.BinaryField(blank=True, null=True)),
                ('EmployeeOfferLetter', models.BinaryField(blank=True, null=True)),
                ('EmployeeReliveLetter', models.BinaryField(blank=True, null=True)),
                ('ConfirmedBy', models.CharField(blank=True, max_length=50, null=True)),
                ('created_by', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(default='', max_length=30)),
            ],
            options={
                'db_table': 'Employeement_History_Detials',
            },
        ),
        migrations.CreateModel(
            name='Financial_History_Detials',
            fields=[
                ('EmpHistory_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Salary', models.FloatField(blank=True, null=True)),
                ('BasicSalary', models.FloatField(blank=True, null=True)),
                ('Allowance', models.FloatField(blank=True, default=0.0, null=True)),
                ('Allowancefinal', models.FloatField(blank=True, null=True)),
                ('PfForEmployee', models.FloatField(blank=True, default=0.0, null=True)),
                ('SecurityDeposite', models.FloatField(blank=True, default=0.0, null=True)),
                ('AccountHolderName', models.CharField(blank=True, max_length=100, null=True)),
                ('AccountNumber', models.CharField(blank=True, max_length=100, null=True)),
                ('BankName', models.CharField(blank=True, max_length=100, null=True)),
                ('Branch', models.CharField(blank=True, max_length=100, null=True)),
                ('IfscCode', models.CharField(blank=True, max_length=100, null=True)),
                ('PanNumber', models.CharField(blank=True, max_length=100, null=True)),
                ('UploadCsvFile', models.BinaryField(blank=True, null=True)),
                ('created_by', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('updated_by', models.CharField(default='', max_length=30)),
            ],
            options={
                'db_table': 'Financial_History_Detials',
            },
        ),
        migrations.CreateModel(
            name='HR_ComplaintAction',
            fields=[
                ('HrComplaint_Id', models.AutoField(primary_key=True, serialize=False)),
                ('HrAction', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('Remarks', models.TextField(blank=True, null=True)),
                ('FromDate', models.DateField(blank=True, null=True)),
                ('ToDate', models.DateField(blank=True, null=True)),
                ('CreatedBy', models.CharField(default='', max_length=100)),
                ('Status', models.CharField(default='Pending', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'HR_ComplaintAction',
            },
        ),
        migrations.CreateModel(
            name='ShiftDetails_Master',
            fields=[
                ('Employee_Shift_Id', models.AutoField(primary_key=True, serialize=False)),
                ('ShiftDate', models.DateField(blank=True, null=True)),
                ('Status', models.CharField(default='', max_length=70)),
                ('Create_by', models.CharField(max_length=70)),
                ('Created_at', models.DateTimeField(auto_now_add=True)),
                ('Updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'ShiftDetails_Master',
            },
        ),
        migrations.CreateModel(
            name='Trainee_Personal_Form_Details',
            fields=[
                ('Trainee_ID', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('First_Name', models.CharField(max_length=30)),
                ('Middle_Name', models.CharField(blank=True, max_length=30, null=True)),
                ('Sur_Name', models.CharField(blank=True, max_length=30, null=True)),
                ('Gender', models.CharField(max_length=30)),
                ('DOB', models.CharField(max_length=30)),
                ('Age', models.CharField(max_length=30)),
                ('Phone', models.CharField(blank=True, max_length=15, null=True)),
                ('E_mail', models.CharField(blank=True, max_length=50, null=True)),
                ('Qualification', models.CharField(blank=True, max_length=30, null=True)),
                ('IdProofType', models.CharField(blank=True, max_length=30, null=True)),
                ('IdProofNo', models.CharField(blank=True, max_length=100, null=True)),
                ('Marital_Status', models.CharField(blank=True, max_length=30, null=True)),
                ('SpouseName', models.CharField(blank=True, max_length=30, null=True)),
                ('SpouseContact', models.CharField(blank=True, max_length=30, null=True)),
                ('FatherName', models.CharField(blank=True, max_length=30, null=True)),
                ('FatherContact', models.CharField(blank=True, max_length=30, null=True)),
                ('EmergencyContactName', models.CharField(blank=True, max_length=30, null=True)),
                ('EmergencyContactNo', models.CharField(blank=True, max_length=30, null=True)),
                ('InstitutionalName', models.CharField(blank=True, max_length=100, null=True)),
                ('InchargePerson', models.CharField(blank=True, max_length=100, null=True)),
                ('Trainee_Startdate', models.CharField(max_length=30)),
                ('InductionGivenby', models.CharField(blank=True, max_length=100, null=True)),
                ('Trainee_Enddate', models.CharField(max_length=30)),
                ('Certifiedby', models.CharField(blank=True, max_length=100, null=True)),
                ('Residence', models.CharField(blank=True, max_length=30, null=True)),
                ('Photo', models.BinaryField(blank=True, null=True)),
                ('TraineeCertificate', models.BinaryField(blank=True, null=True)),
                ('Status', models.CharField(blank=True, max_length=30, null=True)),
                ('Pincode', models.CharField(blank=True, max_length=30, null=True)),
                ('DoorNo', models.CharField(blank=True, max_length=30, null=True)),
                ('Street', models.CharField(blank=True, max_length=255, null=True)),
                ('Area', models.CharField(blank=True, max_length=255, null=True)),
                ('City', models.CharField(blank=True, max_length=30, null=True)),
                ('District', models.CharField(blank=True, max_length=30, null=True)),
                ('State', models.CharField(blank=True, max_length=30, null=True)),
                ('Country', models.CharField(blank=True, max_length=30, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('Createdby', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'Trainee_Personal_Form_Details',
            },
        ),
    ]
