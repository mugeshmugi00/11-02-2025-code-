# Generated by Django 5.1.4 on 2025-02-11 11:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor_drug_prescription',
            fields=[
                ('Prescription_Id', models.IntegerField(primary_key=True, serialize=False)),
                ('Department', models.CharField(max_length=30)),
                ('Route', models.TextField()),
                ('FrequencyMethod', models.CharField(max_length=60)),
                ('Duration', models.CharField(max_length=60)),
                ('DurationType', models.CharField(max_length=60)),
                ('Quantity', models.CharField(max_length=60)),
                ('AdminisDose', models.CharField(max_length=60)),
                ('Date', models.DateTimeField(auto_now=True)),
                ('Time', models.CharField(max_length=60)),
                ('Instruction', models.CharField(max_length=60)),
                ('Status', models.CharField(max_length=60)),
                ('CapturedBy', models.CharField(max_length=60)),
                ('IssuedBy', models.CharField(max_length=60)),
                ('OrderType', models.CharField(max_length=60)),
                ('RequestType', models.CharField(max_length=60)),
                ('RequestQuantity', models.CharField(max_length=60)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'Doctor_drug_prescription',
            },
        ),
        migrations.CreateModel(
            name='IP_BillingItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ItemName', models.CharField(max_length=100)),
                ('Billing_Quantity', models.PositiveIntegerField()),
                ('BatchNo', models.CharField(max_length=50)),
                ('Exp_Date', models.DateField()),
                ('Unit_Price', models.FloatField()),
                ('Amount', models.FloatField()),
                ('Total', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ip_drug_request_table',
            fields=[
                ('Nurse_Prescription_Id', models.IntegerField(primary_key=True, serialize=False)),
                ('Department', models.CharField(max_length=30)),
                ('Route', models.TextField()),
                ('FrequencyMethod', models.CharField(max_length=60)),
                ('Duration', models.CharField(max_length=60)),
                ('DurationType', models.CharField(max_length=60)),
                ('Quantity', models.CharField(max_length=60)),
                ('AdminisDose', models.CharField(max_length=60)),
                ('Date', models.DateTimeField(auto_now=True)),
                ('Time', models.CharField(max_length=60)),
                ('Instruction', models.CharField(max_length=60)),
                ('Status', models.CharField(max_length=60)),
                ('CapturedBy', models.CharField(max_length=60)),
                ('IssuedBy', models.CharField(max_length=60)),
                ('Complete_Date', models.DateField(auto_now=True)),
                ('Complete_Time', models.TimeField(auto_now=True)),
                ('Completed_Remarks', models.CharField(blank=True, max_length=60)),
                ('OrderType', models.CharField(max_length=60)),
                ('RequestType', models.CharField(max_length=60)),
                ('RequestQuantity', models.CharField(max_length=60)),
                ('RemainingQuantity', models.CharField(max_length=25)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'ip_drug_request_table',
            },
        ),
        migrations.CreateModel(
            name='Ip_Nurse_Drug_Completed_Administration',
            fields=[
                ('Nurse_Prescription_Id', models.AutoField(primary_key=True, serialize=False)),
                ('Department', models.CharField(max_length=30)),
                ('Dosage', models.CharField(max_length=60)),
                ('Route', models.CharField(max_length=60)),
                ('FrequencyIssued', models.CharField(max_length=60)),
                ('FrequencyMethod', models.CharField(max_length=60)),
                ('Quantity', models.CharField(max_length=60)),
                ('Issued_Date', models.DateField(auto_now_add=True)),
                ('Complete_Date', models.DateField(auto_now=True)),
                ('Complete_Time', models.TimeField(auto_now=True)),
                ('Completed_Remarks', models.CharField(blank=True, max_length=60)),
                ('Status', models.CharField(max_length=60)),
                ('CapturedBy', models.CharField(max_length=60, null=True)),
                ('AdminisDose', models.CharField(blank=True, max_length=60)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'Ip_Nurse_Drug_Completed_Administration',
            },
        ),
        migrations.CreateModel(
            name='IP_Pharmacy_Billing_Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Billpay_method', models.CharField(max_length=50)),
                ('CardType', models.CharField(blank=True, max_length=50, null=True)),
                ('BankName', models.CharField(blank=True, max_length=100, null=True)),
                ('ChequeNo', models.CharField(blank=True, max_length=100, null=True)),
                ('paidamount', models.FloatField()),
                ('Additionalamount', models.FloatField(blank=True, null=True)),
                ('transactionFee', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='IP_Pharmacy_Billing_Table_Detials',
            fields=[
                ('Billing_Invoice_No', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('Billing_Date', models.DateField()),
                ('Billing_Type', models.CharField(max_length=150)),
                ('Select_Discount', models.CharField(max_length=50)),
                ('Discount_Type', models.CharField(max_length=30)),
                ('Discount_Amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Total_Items', models.CharField(max_length=30)),
                ('Total_Qty', models.CharField(max_length=30)),
                ('Total_Amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('SGST_val', models.DecimalField(decimal_places=2, max_digits=10)),
                ('CGST_val', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Total_GSTAmount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Net_Amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Round_Off', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Paid_Amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Balance_Amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Bill_Status', models.CharField(max_length=20)),
                ('created_by', models.CharField(max_length=100)),
                ('updated_by', models.CharField(default='', max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='medical_productmaster_information',
            fields=[
                ('ProductCode', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('Productcategory', models.CharField(max_length=25)),
                ('ProductName', models.CharField(max_length=155)),
                ('GenericName', models.CharField(max_length=86)),
                ('Strength', models.CharField(max_length=50)),
                ('UOM', models.CharField(max_length=25)),
                ('ProductType', models.CharField(max_length=75)),
                ('ProductQuantity', models.IntegerField()),
                ('SellingPriceWithoutGST', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Status', models.CharField(max_length=55)),
                ('Created_By', models.CharField(max_length=65)),
                ('Location', models.CharField(max_length=75)),
                ('Productcategory_Type', models.CharField(max_length=100)),
                ('UpdatedAt', models.DateTimeField(auto_now=True)),
                ('CreatedAt', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'medical_productmaster_information',
            },
        ),
        migrations.CreateModel(
            name='Nurse_drug_prescription',
            fields=[
                ('Nurse_Prescription_Id', models.IntegerField(primary_key=True, serialize=False)),
                ('Route', models.TextField()),
                ('FrequencyMethod', models.CharField(max_length=60)),
                ('Duration', models.CharField(max_length=60)),
                ('DurationType', models.CharField(max_length=60)),
                ('Quantity', models.CharField(max_length=60)),
                ('AdminisDose', models.CharField(max_length=60)),
                ('Date', models.DateTimeField(auto_now=True)),
                ('Time', models.CharField(max_length=60)),
                ('Instruction', models.CharField(max_length=60)),
                ('Status', models.CharField(max_length=60)),
                ('CapturedBy', models.CharField(max_length=60)),
                ('IssuedBy', models.CharField(max_length=60)),
                ('Complete_Date', models.DateField(auto_now=True)),
                ('Complete_Time', models.TimeField(auto_now=True)),
                ('Completed_Remarks', models.CharField(blank=True, max_length=60)),
                ('OrderType', models.CharField(max_length=60)),
                ('RequestType', models.CharField(max_length=60)),
                ('RequestQuantity', models.CharField(max_length=60)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'Nurse_drug_prescription',
            },
        ),
        migrations.CreateModel(
            name='OP_BillingItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ItemName', models.CharField(max_length=100)),
                ('Billing_Quantity', models.PositiveIntegerField()),
                ('BatchNo', models.CharField(max_length=50)),
                ('Exp_Date', models.DateField()),
                ('Unit_Price', models.FloatField()),
                ('Amount', models.FloatField()),
                ('Total', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='OP_Pharmacy_Billing_Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Billpay_method', models.CharField(max_length=50)),
                ('CardType', models.CharField(blank=True, max_length=50, null=True)),
                ('BankName', models.CharField(blank=True, max_length=100, null=True)),
                ('ChequeNo', models.CharField(blank=True, max_length=100, null=True)),
                ('paidamount', models.FloatField()),
                ('Additionalamount', models.FloatField(blank=True, null=True)),
                ('transactionFee', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OP_Pharmacy_Billing_Table_Detials',
            fields=[
                ('Billing_Invoice_No', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('Billing_Date', models.DateField()),
                ('Billing_Type', models.CharField(max_length=150)),
                ('Select_Discount', models.CharField(max_length=50)),
                ('Discount_Type', models.CharField(max_length=30)),
                ('Discount_Amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Total_Items', models.CharField(max_length=30)),
                ('Total_Qty', models.CharField(max_length=30)),
                ('Total_Amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('SGST_val', models.DecimalField(decimal_places=2, max_digits=10)),
                ('CGST_val', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Total_GSTAmount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Net_Amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Round_Off', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Paid_Amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Balance_Amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Bill_Status', models.CharField(max_length=20)),
                ('created_by', models.CharField(max_length=100)),
                ('updated_by', models.CharField(default='', max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OP_Pharmacy_Walkin_Billing_Table_Detials',
            fields=[
                ('PatientName', models.CharField(max_length=100)),
                ('Billing_Invoice_No', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('PatientId', models.CharField(max_length=30)),
                ('Billing_Date', models.DateField()),
                ('Doctor_Id', models.CharField(blank=True, max_length=30, null=True)),
                ('Billing_Type', models.CharField(max_length=150)),
                ('Select_Discount', models.CharField(max_length=50)),
                ('Discount_Type', models.CharField(max_length=30)),
                ('Discount_Amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Total_Items', models.CharField(max_length=30)),
                ('Total_Qty', models.CharField(max_length=30)),
                ('Total_Amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('SGST_val', models.DecimalField(decimal_places=2, max_digits=10)),
                ('CGST_val', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Total_GSTAmount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Net_Amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Round_Off', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Paid_Amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Balance_Amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('Bill_Status', models.CharField(max_length=20)),
                ('created_by', models.CharField(max_length=100)),
                ('updated_by', models.CharField(default='', max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'OP_Pharmacy_Billing_Table_Detials',
            },
        ),
        migrations.CreateModel(
            name='OP_Walkin_BillingItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ItemName', models.CharField(max_length=100)),
                ('Billing_Quantity', models.PositiveIntegerField()),
                ('BatchNo', models.CharField(max_length=50)),
                ('Exp_Date', models.DateField()),
                ('Unit_Price', models.FloatField()),
                ('Amount', models.FloatField()),
                ('Total', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='OP_Walkin_Pharmacy_Billing_Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Billpay_method', models.CharField(max_length=50)),
                ('CardType', models.CharField(blank=True, max_length=50, null=True)),
                ('BankName', models.CharField(blank=True, max_length=100, null=True)),
                ('ChequeNo', models.CharField(blank=True, max_length=100, null=True)),
                ('paidamount', models.FloatField()),
                ('Additionalamount', models.FloatField(blank=True, null=True)),
                ('transactionFee', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]
