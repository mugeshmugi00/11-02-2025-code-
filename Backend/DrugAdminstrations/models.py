from django.db import models
from django.db.models import Max
from django.core.exceptions import ValidationError
from Frontoffice.models import *
from Inventory.models import *
# Create your models here.


# class Ip_Drug_Administration(models.Model):
#     Prescription_Id = models.IntegerField(primary_key=True)
#     Booking_Id = models.CharField(max_length=25, default= '')
#     Department = models.CharField(max_length=60)
#     DoctorName = models.CharField(max_length=60)
#     GenericName = models.CharField(max_length=60)
#     MedicineCode = models.CharField(max_length=60)
#     MedicineName = models.CharField(max_length=60)
#     Dosage = models.CharField(max_length=60)
#     Route = models.CharField(max_length=60)
#     FrequencyMethod = models.CharField(max_length=60)
#     FrequencyType = models.CharField(max_length=60)
#     Frequency = models.CharField(max_length=60)
#     FrequencyTime = models.CharField(max_length=30, default='')
#     Duration = models.CharField(max_length=60)
#     DurationType = models.CharField(max_length=60)
#     Quantity = models.CharField(max_length=60)
#     AdminisDose = models.CharField(max_length=60)
#     Date = models.DateTimeField(auto_now=True)
#     Time = models.CharField(max_length=60)
#     Instruction = models.CharField(max_length=60)
#     Status = models.CharField(max_length=60)
#     CapturedBy = models.CharField(max_length=60)
#     RequestType = models.CharField(max_length=60)
#     RequestQuantity = models.CharField(max_length=60)
#     RequestDate = models.DateField(auto_now=True)
#     BillingMethod = models.CharField(max_length=60)
#     PrescriptionBarcode = models.CharField(max_length=60)
#     Specialization = models.CharField(max_length=60)
#     IssuedType = models.CharField(max_length=60)
#     IssuedBy = models.CharField(max_length=60)
#     Location = models.CharField(max_length=65, default="")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         db_table = 'Ip_Drug_Administration'
#     def save(self, *args, **kwargs):
#         if not self.Prescription_Id:
#             max_id = Ip_Drug_Administration.objects.aggregate(max_id=Max('Prescription_Id'))['max_id']
#             self.Prescription_Id = (max_id or 0) + 1
#         super(Ip_Drug_Administration, self).save(*args, **kwargs)
    
    
    
# class Ip_Nurse_Drug_Completed_Administration(models.Model):
#     Nurse_Prescription_Id = models.AutoField(primary_key=True)
#     Prescription_Id = models.CharField(max_length=25, default='')  # New field added
#     Booking_Id = models.CharField(max_length=25, blank=True, default='')
#     Department = models.CharField(max_length=60)
#     DoctorName = models.CharField(max_length=60)
#     GenericName = models.CharField(max_length=60)
#     MedicineCode = models.CharField(max_length=60)
#     MedicineName = models.CharField(max_length=60)
#     Dosage = models.CharField(max_length=60)
#     Route = models.CharField(max_length=60)
#     FrequencyIssued = models.CharField(max_length=60)
#     FrequencyMethod = models.CharField(max_length=60)
#     Quantity = models.CharField(max_length=60)
#     Issued_Date = models.DateField(auto_now_add=True)
#     Complete_Date = models.DateField(auto_now=True)
#     Complete_Time = models.TimeField(auto_now=True)
#     Completed_Remarks = models.CharField(max_length=60, blank=True)
#     Status = models.CharField(max_length=60)
#     Location = models.CharField(max_length=100, default='')
#     CapturedBy = models.CharField(max_length=60)
#     AdminisDose = models.CharField(max_length=60, blank=True)
#     updated_at = models.DateTimeField(default=datetime.now)
#     created_at = models.DateTimeField(default=datetime.now)

#     class Meta:
#         db_table = 'Ip_Nurse_Drug_Completed_Administration'

#     def save(self, *args, **kwargs):
#         # The primary key is handled by AutoField, so no need to manually set it
#         super().save(*args, **kwargs)



# class ip_drug_request_table(models.Model):
#     Drug_Request_Id  = models.AutoField(primary_key=True)
#     Booking_Id =  models.CharField(max_length=25)
#     Prescibtion_Id = models.CharField(max_length=25)
#     Department = models.CharField(max_length=25)
#     DoctorName = models.CharField(max_length= 150)
#     GenericName = models.CharField(max_length=100)
#     MedicineCode = models.CharField(max_length=25)
#     MedicineName = models.CharField(max_length=100)
#     Dosage = models.CharField(max_length=25)
#     Route = models.CharField(max_length=12)
#     Duration = models.CharField(max_length=25)
#     DurationType = models.CharField(max_length=25)
#     RequestType = models.CharField(max_length=50)
#     Quantity = models.CharField(max_length=25)
#     RequestQuantity = models.CharField(max_length=25)
#     RemainingQuantity = models.CharField(max_length=25)
#     RecivedQuantity = models.CharField(max_length=25)
#     Location = models.CharField(max_length=45)
#     CreatedBy = models.CharField(max_length=100)
#     Status = models.CharField(max_length=60)
#     Priscription_Barcode = models.CharField(max_length=25)
#     Date	 = models.CharField(max_length=25)
#     Time = models.CharField(max_length=25)
#     Canceled_Reason = models.CharField(max_length=250)
#     UpdatedAt = models.DateTimeField(auto_now=True)
#     CreatedAt = models.DateTimeField(auto_now=True)

    

#     class Meta:
#         db_table = 'ip_drug_request_table'
#     def save(self, *args, **kwargs):
#         if not self.Drug_Request_Id:
#             max_id = ip_drug_request_table.objects.aggregate(max_id=Max('Drug_Request_Id')) ['max_id']
#             self.Drug_Request_Id = (max_id or 0) + 1
#         super(ip_drug_request_table, self).save(*args, **kwargs)



class medical_productmaster_information(models.Model):
    ProductCode = models.CharField(max_length=25,primary_key=True)
    Productcategory = models.CharField(max_length=25)
    ProductName = models.CharField(max_length=155)
    GenericName = models.CharField(max_length=86)
    Strength = models.CharField(max_length=50)
    UOM = models.CharField(max_length=25)
    ProductType = models.CharField(max_length=75)
    ProductQuantity = models.IntegerField()
    SellingPriceWithoutGST = models.DecimalField(max_digits=10, decimal_places=2)
    Status = models.CharField(max_length=55)
    Created_By = models.CharField(max_length=65)
    Location = models.CharField(max_length=75)
    Productcategory_Type = models.CharField(max_length=100)
    UpdatedAt = models.DateTimeField(auto_now= True)
    CreatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'medical_productmaster_information'   
    def _str_(self):
        return self.ProductCode
    

class Doctor_drug_prescription(models.Model):
    Prescription_Id = models.IntegerField(primary_key=True)
    Booking_Id = models.ForeignKey(Patient_IP_Registration_Detials,on_delete=models.CASCADE,null=True,blank=True)
    Department = models.CharField(max_length=30)
    DoctorName = models.ForeignKey(Doctor_Personal_Form_Detials,on_delete=models.CASCADE,null=True,blank=True,related_name='Doctor_drug_docname')
    ProductCode = models.ForeignKey(Stock_Maintance_Table_Detials,on_delete=models.CASCADE,null=True,blank=True,related_name='Doctor_drug_med_code')
    Route = models.TextField()
    FrequencyMethod = models.CharField(max_length=60)
    Frequency = models.ForeignKey(Frequency_Master_Drug,on_delete=models.CASCADE,null=True,blank=True)
    Duration = models.CharField(max_length=60)
    DurationType = models.CharField(max_length=60)
    Quantity = models.CharField(max_length=60)
    AdminisDose = models.CharField(max_length=60)
    Date = models.DateTimeField(auto_now=True)
    Time = models.CharField(max_length=60)
    Instruction = models.CharField(max_length=60)
    Status = models.CharField(max_length=60)
    CapturedBy = models.CharField(max_length=60)
    Specialization = models.ForeignKey(Speciality_Detials, on_delete=models.CASCADE,null=True,blank=True)
    IssuedBy = models.CharField(max_length=60)
    OrderType = models.CharField(max_length=60)
    RequestType = models.CharField(max_length=60)
    RequestQuantity = models.CharField(max_length=60)
    Location = models.ForeignKey(Location_Detials, on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'Doctor_drug_prescription'
    def save(self, *args, **kwargs):
        if not self.Prescription_Id:
            max_id = Doctor_drug_prescription.objects.aggregate(max_id=Max('Prescription_Id'))['max_id']
            self.Prescription_Id = (max_id or 0) + 1
        super(Doctor_drug_prescription, self).save(*args, **kwargs)
    
class Nurse_drug_prescription(models.Model):
    Nurse_Prescription_Id = models.IntegerField(primary_key=True)
    Booking_Id = models.ForeignKey(Patient_IP_Registration_Detials,on_delete=models.CASCADE,null=True,blank=True)
    ProductCode = models.ForeignKey(Stock_Maintance_Table_Detials,on_delete=models.CASCADE,null=True,blank=True,related_name='Nurse_drug_med_code')
    Route = models.TextField()
    FrequencyMethod = models.CharField(max_length=60)
    Frequency = models.ForeignKey(Frequency_Master_Drug,on_delete=models.CASCADE,null=True,blank=True)
    Duration = models.CharField(max_length=60)
    DurationType = models.CharField(max_length=60)
    Quantity = models.CharField(max_length=60)
    AdminisDose = models.CharField(max_length=60)
    Date = models.DateTimeField(auto_now=True)
    Time = models.CharField(max_length=60)
    Instruction = models.CharField(max_length=60)
    Status = models.CharField(max_length=60)
    CapturedBy = models.CharField(max_length=60)
    IssuedBy = models.CharField(max_length=60)
    Complete_Date = models.DateField(auto_now=True)
    Complete_Time = models.TimeField(auto_now=True)
    Completed_Remarks = models.CharField(max_length=60, blank=True)
    OrderType = models.CharField(max_length=60)
    RequestType = models.CharField(max_length=60)
    RequestQuantity = models.CharField(max_length=60)
    Location = models.ForeignKey(Location_Detials, on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'Nurse_drug_prescription'
    def save(self, *args, **kwargs):
        if not self.Prescription_Id:
            max_id = Nurse_drug_prescription.objects.aggregate(max_id=Max('Prescription_Id'))['max_id']
            self.Prescription_Id = (max_id or 0) + 1
        super(Nurse_drug_prescription, self).save(*args, **kwargs)
    
class ip_drug_request_table(models.Model):
    Nurse_Prescription_Id = models.IntegerField(primary_key=True)
    Prescription_Id = models.ForeignKey(Doctor_drug_prescription,on_delete=models.CASCADE, null=True, blank=True)
    Booking_Id = models.ForeignKey(Patient_IP_Registration_Detials,on_delete=models.CASCADE,null=True,blank=True)
    Department = models.CharField(max_length=30)
    DoctorName = models.ForeignKey(Doctor_Personal_Form_Detials,on_delete=models.CASCADE,null=True,blank=True,related_name='Doctor_drug_docname_request')
    ProductCode = models.ForeignKey(Stock_Maintance_Table_Detials,on_delete=models.CASCADE,null=True,blank=True,related_name='Doctor_drug_med_code_request')
    Route = models.TextField()
    FrequencyMethod = models.CharField(max_length=60)
    Frequency = models.ForeignKey(Frequency_Master_Drug,on_delete=models.CASCADE,null=True,blank=True)
    Duration = models.CharField(max_length=60)
    DurationType = models.CharField(max_length=60)
    Quantity = models.CharField(max_length=60)
    AdminisDose = models.CharField(max_length=60)
    Date = models.DateTimeField(auto_now=True)
    Time = models.CharField(max_length=60)
    Instruction = models.CharField(max_length=60)
    Status = models.CharField(max_length=60)
    CapturedBy = models.CharField(max_length=60)
    IssuedBy = models.CharField(max_length=60)
    Complete_Date = models.DateField(auto_now=True)
    Complete_Time = models.TimeField(auto_now=True)
    Completed_Remarks = models.CharField(max_length=60, blank=True)
    OrderType = models.CharField(max_length=60)
    RequestType = models.CharField(max_length=60)
    RequestQuantity = models.CharField(max_length=60)
    RemainingQuantity = models.CharField(max_length=25)
    Location = models.ForeignKey(Location_Detials, on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'ip_drug_request_table'
    def save(self, *args, **kwargs):
        if not self.Nurse_Prescription_Id:
            max_id = ip_drug_request_table.objects.aggregate(max_id=Max('Nurse_Prescription_Id'))['max_id']
            self.Nurse_Prescription_Id = (max_id or 0) + 1
        super(ip_drug_request_table, self).save(*args, **kwargs)


class Ip_Nurse_Drug_Completed_Administration(models.Model):
    Nurse_Prescription_Id = models.AutoField(primary_key=True)
    Prescription_Id = models.ForeignKey(Doctor_drug_prescription,on_delete=models.CASCADE, null=True, blank=True)
    Booking_Id = models.ForeignKey(Patient_IP_Registration_Detials,on_delete=models.CASCADE,null=True,blank=True)
    Department = models.CharField(max_length=30)
    DoctorName = models.ForeignKey(Doctor_Personal_Form_Detials,on_delete=models.CASCADE,null=True,blank=True,related_name='Doctor_drug_docname_adminis')
    ProductCode = models.ForeignKey(Stock_Maintance_Table_Detials,on_delete=models.CASCADE,null=True,blank=True,related_name='Doctor_drug_med_code_adminis')
    Dosage = models.CharField(max_length=60)
    Route = models.CharField(max_length=60)
    FrequencyIssued = models.CharField(max_length=60)
    FrequencyMethod = models.CharField(max_length=60)
    Quantity = models.CharField(max_length=60)
    Issued_Date = models.DateField(auto_now_add=True)
    Complete_Date = models.DateField(auto_now=True)
    Complete_Time = models.TimeField(auto_now=True)
    Completed_Remarks = models.CharField(max_length=60, blank=True)
    Status = models.CharField(max_length=60)
    Location = models.ForeignKey(Location_Detials, on_delete=models.CASCADE,null=True,blank=True)
    CapturedBy = models.CharField(max_length=60, null=True)
    AdminisDose = models.CharField(max_length=60, blank=True)
    updated_at = models.DateTimeField(default=datetime.now)
    created_at = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = 'Ip_Nurse_Drug_Completed_Administration'
    def save(self, *args, **kwargs):
        if not self.Nurse_Prescription_Id:
            max_id = Ip_Nurse_Drug_Completed_Administration.objects.aggregate(max_id=Max('Nurse_Prescription_Id'))['max_id']
            self.Nurse_Prescription_Id = (max_id or 0) + 1
        super(Ip_Nurse_Drug_Completed_Administration, self).save(*args, **kwargs)


class IP_Pharmacy_Billing_Table_Detials(models.Model):
    Billing_Invoice_No=models.CharField(primary_key=True,max_length=30)
    Billing_Date=models.DateField()
    Doctor_Id=models.ForeignKey(Doctor_Personal_Form_Detials,on_delete=models.CASCADE,related_name='IP_Pharmacy_Billing_Doctor_Id')
    Patient_Id=models.ForeignKey(Patient_Detials,on_delete=models.CASCADE,related_name='IP_Pharmacy_Billing_Patient_Id')
    Billing_Type=models.CharField(max_length=150)
    Select_Discount=models.CharField(max_length=50)
    Discount_Type=models.CharField(max_length=30)
    Discount_Amount=models.DecimalField(max_digits=10, decimal_places=2)
    Total_Items=models.CharField(max_length=30)
    Total_Qty=models.CharField(max_length=30)
    Total_Amount=models.DecimalField(max_digits=10, decimal_places=2)
    SGST_val= models.DecimalField(max_digits=10, decimal_places=2)
    CGST_val= models.DecimalField(max_digits=10, decimal_places=2)
    Total_GSTAmount=models.DecimalField(max_digits=10, decimal_places=2)
    Net_Amount=models.DecimalField(max_digits=10, decimal_places=2)
    Round_Off=models.DecimalField(max_digits=10, decimal_places=2)
    Paid_Amount=models.DecimalField(max_digits=10, decimal_places=2)
    Balance_Amount=models.DecimalField(max_digits=10, decimal_places=2)
    Location = models.ForeignKey(Location_Detials, on_delete=models.CASCADE, null=True, blank= True)
    Bill_Status=models.CharField(max_length=20)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=30,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class meta:
        db_table='IP_Pharmacy_Billing_Table_Detials'

    def save(self, *args, **kwargs):    
        if not self.Billing_Invoice_No:
            Add_Invoice_Char = 'PHAIPDR/'
            
            # Fetch the latest Billing_Invoice_No, excluding those created by the system
            Max_Invoice_No_row = IP_Pharmacy_Billing_Table_Detials.objects.exclude(created_by='system').aggregate(max_id=Max('Billing_Invoice_No'))['max_id']
            
            # Extract the numeric part after 'PHADR/' and handle cases where max_id is None
            if Max_Invoice_No_row:
                numeric_part = int(str(Max_Invoice_No_row).split('/')[-1]) + 1
            else:
                numeric_part = 1
            
            # Format the new Billing_Invoice_No with leading zeros
            self.Billing_Invoice_No = f'{Add_Invoice_Char}{numeric_part:04}'
        
        super(IP_Pharmacy_Billing_Table_Detials, self).save(*args, **kwargs)

class IP_BillingItem(models.Model):
    Billing = models.ForeignKey(IP_Pharmacy_Billing_Table_Detials, on_delete=models.CASCADE, related_name="IP_billing_items")
    ItemName = models.CharField(max_length=100)
    Billing_Quantity = models.PositiveIntegerField()
    BatchNo = models.CharField(max_length=50)
    Exp_Date = models.DateField()
    Unit_Price = models.FloatField()
    Amount = models.FloatField()
    Total = models.FloatField()

    def __str__(self):
        return f"{self.ItemName} - Quantity: {self.Billing_Quantity}"


class IP_Pharmacy_Billing_Payments(models.Model):
    Billing = models.ForeignKey(IP_Pharmacy_Billing_Table_Detials, on_delete=models.CASCADE, related_name='IP_billing_payments')
    Billpay_method = models.CharField(max_length=50)
    CardType = models.CharField(max_length=50, blank=True, null=True)
    BankName = models.CharField(max_length=100, blank=True, null=True)
    ChequeNo = models.CharField(max_length=100, blank=True, null=True)
    paidamount = models.FloatField()
    Additionalamount = models.FloatField(blank=True, null=True)
    transactionFee = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.Billpay_method} - {self.paidamount}"
    



class OP_Pharmacy_Billing_Table_Detials(models.Model):
    Billing_Invoice_No=models.CharField(primary_key=True,max_length=30)
    Billing_Date=models.DateField()
    Doctor_Id=models.ForeignKey(Doctor_Personal_Form_Detials,on_delete=models.CASCADE,related_name='OP_Pharmacy_Billing_Doctor_Id',null=True,blank=True)
    Patient_Id=models.ForeignKey(Patient_Detials,on_delete=models.CASCADE,related_name='OP_Pharmacy_Billing_Patient_Id',null=True,blank=True)
    Billing_Type=models.CharField(max_length=150)
    Select_Discount=models.CharField(max_length=50)
    Discount_Type=models.CharField(max_length=30)
    Discount_Amount=models.DecimalField(max_digits=10, decimal_places=2)
    Total_Items=models.CharField(max_length=30)
    Total_Qty=models.CharField(max_length=30)
    Total_Amount=models.DecimalField(max_digits=10, decimal_places=2)
    SGST_val= models.DecimalField(max_digits=10, decimal_places=2)
    CGST_val= models.DecimalField(max_digits=10, decimal_places=2)
    Total_GSTAmount=models.DecimalField(max_digits=10, decimal_places=2)
    Net_Amount=models.DecimalField(max_digits=10, decimal_places=2)
    Round_Off=models.DecimalField(max_digits=10, decimal_places=2)
    Paid_Amount=models.DecimalField(max_digits=10, decimal_places=2)
    Balance_Amount=models.DecimalField(max_digits=10, decimal_places=2)
    Location = models.ForeignKey(Location_Detials, on_delete=models.CASCADE, null=True, blank= True)
    Bill_Status=models.CharField(max_length=20)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=30,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class meta:
        db_table='OP_Pharmacy_Billing_Table_Detials'

    def save(self, *args, **kwargs):
        if not self.Billing_Invoice_No:
            Add_Invoice_Char = 'PHAOPDR/'
            
            # Fetch the latest Billing_Invoice_No, excluding those created by the system
            Max_Invoice_No_row = OP_Pharmacy_Billing_Table_Detials.objects.exclude(created_by='system').aggregate(max_id=Max('Billing_Invoice_No'))['max_id']
            
            # Extract the numeric part after 'PHADR/' and handle cases where max_id is None
            if Max_Invoice_No_row:
                numeric_part = int(str(Max_Invoice_No_row).split('/')[-1]) + 1
            else:
                numeric_part = 1
            
            # Format the new Billing_Invoice_No with leading zeros
            self.Billing_Invoice_No = f'{Add_Invoice_Char}{numeric_part:04}'
        
        super(OP_Pharmacy_Billing_Table_Detials, self).save(*args, **kwargs)



class OP_BillingItem(models.Model):
    Billing = models.ForeignKey(OP_Pharmacy_Billing_Table_Detials, on_delete=models.CASCADE, related_name="OP_billing_items")
    ItemName = models.CharField(max_length=100)
    Billing_Quantity = models.PositiveIntegerField()
    BatchNo = models.CharField(max_length=50)
    Exp_Date = models.DateField()
    Unit_Price = models.FloatField()
    Amount = models.FloatField()
    Total = models.FloatField()

    def __str__(self):
        return f"{self.ItemName} - Quantity: {self.Billing_Quantity}"


class OP_Pharmacy_Billing_Payments(models.Model):
    Billing = models.ForeignKey(OP_Pharmacy_Billing_Table_Detials, on_delete=models.CASCADE, related_name='billing_payments')
    Billpay_method = models.CharField(max_length=50)
    CardType = models.CharField(max_length=50, blank=True, null=True)
    BankName = models.CharField(max_length=100, blank=True, null=True)
    ChequeNo = models.CharField(max_length=100, blank=True, null=True)
    paidamount = models.FloatField()
    Additionalamount = models.FloatField(blank=True, null=True)
    transactionFee = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.Billpay_method} - {self.paidamount}"


 
    
class OP_Pharmacy_Walkin_Billing_Table_Detials(models.Model):
    PatientName = models.CharField(max_length=100)
    Billing_Invoice_No = models.CharField(primary_key=True, max_length=30)
    PatientId = models.CharField(max_length=30)
    Billing_Date = models.DateField()
    Doctor_Id = models.CharField(max_length=30,null=True,blank=True)
    Billing_Type = models.CharField(max_length=150)
    Select_Discount = models.CharField(max_length=50)
    Discount_Type = models.CharField(max_length=30)
    Discount_Amount = models.DecimalField(max_digits=10, decimal_places=2)
    Total_Items = models.CharField(max_length=30)
    Total_Qty = models.CharField(max_length=30)
    Total_Amount = models.DecimalField(max_digits=10, decimal_places=2)
    SGST_val = models.DecimalField(max_digits=10, decimal_places=2)
    CGST_val = models.DecimalField(max_digits=10, decimal_places=2)
    Total_GSTAmount = models.DecimalField(max_digits=10, decimal_places=2)
    Net_Amount = models.DecimalField(max_digits=10, decimal_places=2)
    Round_Off = models.DecimalField(max_digits=10, decimal_places=2)
    Paid_Amount = models.DecimalField(max_digits=10, decimal_places=2)
    Balance_Amount = models.DecimalField(max_digits=10, decimal_places=2)
    Location = models.ForeignKey(Location_Detials, on_delete=models.CASCADE, null=True, blank=True)
    Bill_Status = models.CharField(max_length=20)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=30, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:  # Corrected typo
        db_table = 'OP_Pharmacy_Billing_Table_Detials'

    def save(self, *args, **kwargs):
        if not self.Billing_Invoice_No:
            Add_Invoice_Char = 'PHAOPDR/'
            Max_Invoice_No_row = OP_Pharmacy_Walkin_Billing_Table_Detials.objects.exclude(
                created_by='system'
            ).aggregate(max_id=Max('Billing_Invoice_No'))['max_id']

            if Max_Invoice_No_row:
                numeric_part = int(str(Max_Invoice_No_row).split('/')[-1]) + 1
            else:
                numeric_part = 1

            self.Billing_Invoice_No = f'{Add_Invoice_Char}{numeric_part:04}'

        if not self.PatientId:
            hospital_details = Hospital_Detials.objects.first()
            if not hospital_details:
                raise ValueError("No Hospital_Details records found.")

            clinic_name = hospital_details.Hospital_Name[:3].upper()
            today_date = datetime.now().strftime('%y%m%d')
            prefix = f'{clinic_name}{today_date}'

            max_patient_id = Patient_Detials.objects.aggregate(max_id=Max('PatientId'))['max_id']
            if max_patient_id:
                numeric_part = int(max_patient_id[-4:]) + 1
            else:
                numeric_part = 1
            self.PatientId = f'{prefix}{numeric_part:04}'
        super(OP_Pharmacy_Walkin_Billing_Table_Detials, self).save(*args, **kwargs)  # Corrected model name


class OP_Walkin_BillingItem(models.Model):
    Billing = models.ForeignKey(OP_Pharmacy_Walkin_Billing_Table_Detials, on_delete=models.CASCADE, related_name="OP_Walkin_billing_items")
    ItemName = models.CharField(max_length=100)
    Billing_Quantity = models.PositiveIntegerField()
    BatchNo = models.CharField(max_length=50)
    Exp_Date = models.DateField()
    Unit_Price = models.FloatField()
    Amount = models.FloatField()
    Total = models.FloatField()

    def __str__(self):
        return f"{self.ItemName} - Quantity: {self.Billing_Quantity}"


class OP_Walkin_Pharmacy_Billing_Payments(models.Model):
    Billing = models.ForeignKey(OP_Pharmacy_Walkin_Billing_Table_Detials, on_delete=models.CASCADE, related_name='billing_payments_Walkin')
    Billpay_method = models.CharField(max_length=50)
    CardType = models.CharField(max_length=50, blank=True, null=True)
    BankName = models.CharField(max_length=100, blank=True, null=True)
    ChequeNo = models.CharField(max_length=100, blank=True, null=True)
    paidamount = models.FloatField()
    Additionalamount = models.FloatField(blank=True, null=True)
    transactionFee = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.Billpay_method} - {self.paidamount}"
    

