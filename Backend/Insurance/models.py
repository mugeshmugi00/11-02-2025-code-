from django.db import models
from Frontoffice.models import *
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType






class Insuranse_Patient_Entery_Details(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    IP_Registration = GenericForeignKey('content_type', 'object_id')
    Patient_ServiesType=models.CharField(max_length=40)
    PreAuthDate=models.DateField(null=True,default=None)
    PreAuthAmount=models.DecimalField(max_digits=10,decimal_places=2,null=True,default=None)
    DischargeDate=models.DateField(null=True,default=None)
    FinalBillAmount=models.DecimalField(max_digits=10,decimal_places=2,null=True,default=None)
    RaisedAmount=models.DecimalField(max_digits=10,decimal_places=2,null=True,default=None)
    ApprovedAmount=models.DecimalField(max_digits=10,decimal_places=2,null=True,default=None)
    CourierDate=models.DateField(null=True,default=None)
    SettlementDateCount=models.IntegerField(null=True,default=None)
    Papersstatus=models.CharField(default='PENDING',max_length=80)
    SubmittedBy=models.CharField(max_length=100,null=True,default=None)
    CompletedBy=models.CharField(max_length=100,null=True,default=None)
    RejectedBy=models.CharField(max_length=100,null=True,default=None)
    TdsPercentage=models.FloatField(blank=True, null=True)
    TdsAmount=models.FloatField(blank=True, null=True)
    FinalSettlementAmount=models.FloatField(blank=True, null=True)
    InsuranceType=models.CharField(max_length=100,null=True,default=None)
    PolicyNumber=models.CharField(max_length=100,null=True,default=None)
    IsEmployee=models.CharField(max_length=100,null=True,default=None)
    CompanyName=models.CharField(max_length=100,null=True,default=None)
    Employeeid=models.CharField(max_length=100,null=True,default=None)
    EmployeeDesignation=models.CharField(max_length=100,null=True,default=None)
    IsCopayment=models.CharField(max_length=100,null=True,default=None)
    CopaymentBillAmount=models.FloatField(blank=True, null=True)
    CopaymentType=models.CharField(max_length=100,null=True,default=None)
    CopaymentTypeValue=models.FloatField(blank=True, null=True)
    CoPaymentFinalAmount=models.FloatField(blank=True, null=True)
    Updated_by=models.CharField(max_length=100)
    Created_at=models.DateTimeField(auto_now_add=True)
    Update_at=models.DateTimeField(auto_now=True) 



class Insuranse_Patient_Amount_Details(models.Model):
    Insurance_Entry=models.ForeignKey(Insuranse_Patient_Entery_Details,on_delete=models.CASCADE,related_name='AmountTableInsuranceDetailes')
    SettlementDate=models.DateField()
    SettlementAmount=models.DecimalField(max_digits=10,decimal_places=2)
    UTR_Number=models.CharField(max_length=200)
    Created_By=models.CharField(max_length=100)
    Updated_by=models.CharField(max_length=100)
    Created_at=models.DateTimeField(auto_now_add=True)
    Update_at=models.DateTimeField(auto_now=True) 

class Client_Patient_Entry_Details(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    IP_Registration = GenericForeignKey('content_type', 'object_id')
    Patient_ServiesType=models.CharField(max_length=40)
    PreAuthDate=models.DateField(null=True,default=None)
    PreAuthAmount=models.DecimalField(max_digits=10,decimal_places=2,null=True,default=None)
    DischargeDate=models.DateField(null=True,default=None)
    FinalBillAmount=models.DecimalField(max_digits=10,decimal_places=2,null=True,default=None)
    RaisedAmount=models.DecimalField(max_digits=10,decimal_places=2,null=True,default=None)
    ApprovedAmount=models.DecimalField(max_digits=10,decimal_places=2,null=True,default=None)
    CourierDate=models.DateField(null=True,default=None)
    SettlementDateCount=models.IntegerField(null=True,default=None)
    Papersstatus=models.CharField(default='PENDING',max_length=80)
    SubmittedBy=models.CharField(max_length=100,null=True,default=None)
    CompletedBy=models.CharField(max_length=100,null=True,default=None)
    RejectedBy=models.CharField(max_length=100,null=True,default=None)
    TdsPercentage=models.FloatField(blank=True, null=True)
    TdsAmount=models.FloatField(blank=True, null=True)
    FinalSettlementAmount=models.FloatField(blank=True, null=True)   
    IsCopayment=models.CharField(max_length=100,null=True,default=None)
    CopaymentBillAmount=models.FloatField(blank=True, null=True)
    CopaymentType=models.CharField(max_length=100,null=True,default=None)
    CopaymentTypeValue=models.FloatField(blank=True, null=True)
    CoPaymentFinalAmount=models.FloatField(blank=True, null=True)
    Updated_by=models.CharField(max_length=100)
    Created_at=models.DateTimeField(auto_now_add=True)
    Update_at=models.DateTimeField(auto_now=True) 

class Client_Patient_Amount_Details(models.Model):
    Client_Entry=models.ForeignKey(Client_Patient_Entry_Details,on_delete=models.CASCADE,related_name='AmountTableClientDetailes')
    SettlementDate=models.DateField()
    SettlementAmount=models.DecimalField(max_digits=10,decimal_places=2)
    UTR_Number=models.CharField(max_length=200)
    Created_By=models.CharField(max_length=100)
    Updated_by=models.CharField(max_length=100)
    Created_at=models.DateTimeField(auto_now_add=True)
    Update_at=models.DateTimeField(auto_now=True) 


