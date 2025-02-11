from django.db import models
# from Masters.models import *
from django.db.models import Max
from datetime import datetime

from django.http import JsonResponse
# from Masters.models import Title_Detials, BloodGroup_Detials, Location_Detials, Department_Detials, Designation_Detials,Hospital_Detials
from Masters.models import *


# Employee

# class Employee_PersonalInformation_Detials(models.Model):
#     Employee_Id = models.CharField(primary_key=True,max_length=50)
#     Title = models.ForeignKey('Masters.Title_Detials',on_delete=models.CASCADE,blank=True,null=True)
#     FirstName = models.CharField(max_length=30,blank=True,null=True)
#     MiddleName = models.CharField(max_length=30,blank=True,null=True)
#     SurName = models.CharField(max_length=30,blank=True,null=True)
#     Gender = models.CharField(max_length=30,blank=True,null=True)
#     DOB = models.CharField(max_length=30,blank=True,null=True)
#     Age = models.CharField(max_length=30,blank=True,null=True)
#     BloodGroup = models.ForeignKey('Masters.BloodGroup_Detials',on_delete=models.CASCADE,blank=True,null=True)
#     Phone = models.CharField(max_length=30,blank=True,null=True)
#     AlternatePhone = models.CharField(max_length=30,blank=True,null=True)
#     Email = models.CharField(max_length=30,blank=True,null=True)
#     Qualification = models.CharField(max_length=30,blank=True,null=True)
#     SkillSet = models.CharField(max_length=30,blank=True,null=True)
#     IdProofType = models.CharField(max_length=30,blank=True,null=True)
#     IdProofNo = models.CharField(max_length=30,blank=True,null=True)
#     maritalStatus = models.CharField(max_length=30,blank=True,null=True)
#     MarriagePlan = models.CharField(max_length=30,blank=True,null=True)
#     FatherName = models.CharField(max_length=30,blank=True,null=True)
#     FatherContact = models.CharField(max_length=30,blank=True,null=True)
#     FatherWorking = models.CharField(max_length=30,blank=True,null=True)
#     FatherWorkPlace = models.CharField(max_length=100,blank=True,null=True)
#     MotherName = models.CharField(max_length=30,blank=True,null=True)
#     MotherContact = models.CharField(max_length=30,blank=True,null=True)
#     MotherWorking = models.CharField(max_length=30,blank=True,null=True)
#     MotherWorkPlace = models.CharField(max_length=100,blank=True,null=True)
#     SpouseName = models.CharField(max_length=30,blank=True,null=True)
#     SpouseContact = models.CharField(max_length=30,blank=True,null=True)
#     SpouseWorking = models.CharField(max_length=30,blank=True,null=True)
#     SpouseWorkPlace = models.CharField(max_length=100,blank=True,null=True)
#     Child = models.CharField(max_length=30,blank=True,null=True)
#     TotalNoChild = models.CharField(max_length=30,blank=True,null=True)
#     DoorNo = models.CharField(max_length=30,blank=True,null=True)
#     Street = models.CharField(max_length=30,blank=True,null=True)
#     Area = models.CharField(max_length=30,blank=True,null=True)
#     City = models.CharField(max_length=30,blank=True,null=True)
#     District = models.CharField(max_length=30,blank=True,null=True)
#     State = models.CharField(max_length=30,blank=True,null=True)
#     Country = models.CharField(max_length=30,blank=True,null=True)
#     Pincode = models.CharField(max_length=30,blank=True,null=True)
#     EmergencyContactName1 = models.CharField(max_length=30,blank=True,null=True)
#     EmergencyContactNo1 = models.CharField(max_length=30,blank=True,null=True)
#     EmergencyContactName2 = models.CharField(max_length=30,blank=True,null=True)
#     EmergencyContactNo2 = models.CharField(max_length=30,blank=True,null=True)
#     Photo = models.BinaryField(blank=True,null=True)
#     status = models.CharField(max_length=30,blank=True,null=True)    
#     Location = models.ForeignKey('Masters.Location_Detials', on_delete=models.CASCADE)
#     Department = models.ForeignKey('Masters.Department_Detials', on_delete=models.CASCADE,blank=True,null=True)
#     Designation = models.ForeignKey('Masters.Designation_Detials', on_delete=models.CASCADE,blank=True,null=True)
#     created_by = models.CharField(max_length=30)
#     updated_by = models.CharField(max_length=30,default='')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


#     class Meta:
#         db_table = 'Employee_PersonalInformation_Detials'    


#     def save(self, *args, **kwargs):
       

#         if not self.Employee_Id:
#             from Masters.models import Hospital_Detials
#             hospital_details = Hospital_Detials.objects.first()
#             if not hospital_details:
#                 raise ValueError("No Hospital_Details records found.")
            
#             clinic_name = hospital_details.Hospital_Name[:3].upper()
#             today_date = datetime.now().strftime('%y%m%d')
#             prefix = f'{clinic_name}EMP{today_date}'
            
#             # Find the maximum numeric part from existing PatientId with the same prefix
#             max_Employee_Id = Employee_PersonalInformation_Detials.objects.aggregate(max_id=Max('Employee_Id'))['max_id']
#             if max_Employee_Id:
#                 numeric_part = int(max_Employee_Id[-4:]) + 1
#             else:
#                 numeric_part = 1
#             self.Employee_Id = f'{prefix}{numeric_part:04}'
       
#         super(Employee_PersonalInformation_Detials, self).save(*args, **kwargs)



class Employee_Skills_Detials(models.Model):
    Skill_Id = models.AutoField(primary_key=True)
    Employee = models.ForeignKey(Employee_Personal_Form_Detials,on_delete=models.CASCADE,blank=True,null=True)
    Skill = models.CharField(max_length=30,blank=True,null=True)
    Level = models.CharField(max_length=30,blank=True,null=True)
    created_by = models.CharField(max_length=30)
    Location = models.ForeignKey(Location_Detials, on_delete=models.CASCADE,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=30,default='')

    class Meta:
        db_table = 'Employee_Skills_Detials'
        unique_together = ('Employee', 'Skill', 'Level')  

        

class Employeement_History_Detials(models.Model):
    EmpHistory_Id = models.AutoField(primary_key=True)
    Employee = models.ForeignKey(Employee_Personal_Form_Detials,on_delete=models.CASCADE,blank=True,null=True)
    PreviousWorkExperience = models.CharField(max_length=30,blank=True,null=True)
    PreviousWorkPFNumber = models.CharField(max_length=30,blank=True,null=True)
    PreviousWorkESINumber = models.CharField(max_length=30,blank=True,null=True)
    PFNumber = models.CharField(max_length=30,blank=True,null=True)
    ESINumber = models.CharField(max_length=30,blank=True,null=True)
    NoOfYears = models.CharField(max_length=30,blank=True,null=True)
    WorkStationNameAddress = models.TextField(blank=True,null=True)
    ReasonForLeft = models.CharField(max_length=50,blank=True,null=True)
    WorkStationPhoneNo = models.CharField(max_length=30,blank=True,null=True)
    EmployeePaySlip = models.BinaryField(blank=True,null=True)
    EmployeeOfferLetter = models.BinaryField(blank=True,null=True)
    EmployeeReliveLetter = models.BinaryField(blank=True,null=True)
    ConfirmedBy = models.CharField(max_length=50,blank=True,null=True)
    created_by = models.CharField(max_length=30)
    Location = models.ForeignKey(Location_Detials, on_delete=models.CASCADE,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=30,default='')

    class Meta:
        db_table = 'Employeement_History_Detials'


class Employee_Medical_Information_Detials(models.Model):
    EmpHistory_Id = models.AutoField(primary_key=True)
    EmployeementHistory = models.ForeignKey(Employeement_History_Detials,on_delete=models.CASCADE,blank=True,null=True)
    Employee = models.ForeignKey(Employee_Personal_Form_Detials,on_delete=models.CASCADE,blank=True,null=True)
    PreExisiting_Medical_Condition = models.CharField(max_length=100,blank=True,null=True)
    PsychiatricMedicines = models.CharField(max_length=30,blank=True,null=True)
    PsychiatricMedicinesDetails = models.TextField(blank=True,null=True)
    PreviousOperation = models.CharField(max_length=30,blank=True,null=True)
    SurgeriesDetails = models.TextField(blank=True,null=True)
    VaccinationStatus = models.CharField(max_length=30,blank=True,null=True)
    VaccinationStatusDetails = models.TextField(blank=True,null=True)
    MedicalFitnessCertificate = models.BinaryField(blank=True,null=True)
    AnnualMedicalCheckup = models.BinaryField(blank=True,null=True)
    created_by = models.CharField(max_length=30)
    Location = models.ForeignKey(Location_Detials, on_delete=models.CASCADE,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=30,default='')

    class Meta:
        db_table = 'Employee_Medical_Information_Detials'


class Current_History_Detials(models.Model):
    EmpHistory_Id = models.AutoField(primary_key=True)
    Employee = models.ForeignKey(Employee_Personal_Form_Detials,on_delete=models.CASCADE,blank=True,null=True)
    EmployeementHistory = models.ForeignKey(Employeement_History_Detials,on_delete=models.CASCADE,blank=True,null=True)
    EmployeeMedicalInfo = models.ForeignKey(Employee_Medical_Information_Detials,on_delete=models.CASCADE,blank=True,null=True)
    DateOfJoining = models.CharField(max_length=30,blank=True,null=True)
    CurrentEmployeementLocations= models.ForeignKey(Location_Detials, on_delete=models.CASCADE, blank=True,null=True,related_name='current_employment_locations',db_column='current_employment_location_id') 
    ReportingManager = models.CharField(max_length=30,blank=True,null=True)
    GovtLeave = models.CharField(max_length=30,blank=True,null=True)
    CasualLeave = models.CharField(max_length=30,blank=True,null=True)
    SickLeave = models.CharField(max_length=30,blank=True,null=True)
    TotalLeave = models.CharField(max_length=30,blank=True,null=True)
    WorkEmail = models.CharField(max_length=50,blank=True,null=True)
    ProbationPeriod = models.CharField(max_length=50,blank=True,null=True)
    Months = models.CharField(max_length=50,blank=True,null=True)
    Years = models.CharField(max_length=50,blank=True,null=True)
    TrainingGivenBy = models.CharField(max_length=50,blank=True,null=True)
    TrainingVerifiedBy = models.CharField(max_length=50,blank=True,null=True)
    TrainingCompletedDate = models.CharField(max_length=50,blank=True,null=True)
    IsPF_Applicable =models.BooleanField(default=False)
    created_by = models.CharField(max_length=30)
    Location = models.ForeignKey(Location_Detials, on_delete=models.CASCADE,blank=True,null=True,related_name='location_history',db_column='location_history_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=30,default='')

    class Meta:
        db_table = 'Current_History_Detials'



class Financial_History_Detials(models.Model):
    EmpHistory_Id = models.AutoField(primary_key=True)
    Employee = models.ForeignKey(Employee_Personal_Form_Detials,on_delete=models.CASCADE,blank=True,null=True)
    EmployeementHistory = models.ForeignKey(Employeement_History_Detials,on_delete=models.CASCADE,blank=True,null=True)
    EmployeeMedicalInfo = models.ForeignKey(Employee_Medical_Information_Detials,on_delete=models.CASCADE,blank=True,null=True)
    EmployeeCurrentHistoryInfo = models.ForeignKey(Current_History_Detials,on_delete=models.CASCADE,blank=True,null=True)
    Salary = models.FloatField(blank=True, null=True)
    BasicSalary = models.FloatField(blank=True, null=True)
    Allowance = models.FloatField(blank=True, null=True,default=0.0)
    Allowancefinal = models.FloatField(blank=True, null=True)
    PfForEmployee = models.FloatField(blank=True, null=True,default=0.0)
    SecurityDeposite = models.FloatField(blank=True, null=True,default=0.0)
    AccountHolderName = models.CharField(max_length=100,blank=True,null=True)
    AccountNumber = models.CharField(max_length=100,blank=True,null=True)
    BankName = models.CharField(max_length=100,blank=True,null=True)
    Branch = models.CharField(max_length=100,blank=True,null=True)
    IfscCode = models.CharField(max_length=100,blank=True,null=True)
    PanNumber = models.CharField(max_length=100,blank=True,null=True)    
    UploadCsvFile = models.BinaryField(blank=True,null=True)
    created_by = models.CharField(max_length=30)
    Location = models.ForeignKey(Location_Detials, on_delete=models.CASCADE,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=30,default='')
 
    class Meta:
        db_table = 'Financial_History_Detials'

class Document_Checklist_Detials(models.Model):
    EmpHistory_Id = models.AutoField(primary_key=True)
    Employee = models.ForeignKey(Employee_Personal_Form_Detials,on_delete=models.CASCADE,blank=True,null=True)
    EmployeementHistory = models.ForeignKey(Employeement_History_Detials,on_delete=models.CASCADE,blank=True,null=True)
    EmployeeMedicalInfo = models.ForeignKey(Employee_Medical_Information_Detials,on_delete=models.CASCADE,blank=True,null=True)
    EmployeeCurrentHistoryInfo = models.ForeignKey(Current_History_Detials,on_delete=models.CASCADE,blank=True,null=True)
    EmployeeFinancialHistory = models.ForeignKey(Financial_History_Detials,on_delete=models.CASCADE,blank=True,null=True)
    Resume = models.BinaryField(blank=True,null=True)
    PanCard = models.BinaryField(blank=True,null=True)
    AadharCard = models.BinaryField(blank=True,null=True)
    BankPassbook = models.BinaryField(blank=True,null=True)
    ExperienceCertificate = models.BinaryField(blank=True,null=True)
    MedicalFitness = models.BinaryField(blank=True,null=True)
    Offerletter = models.BinaryField(blank=True,null=True)
    created_by = models.CharField(max_length=30)
    Location = models.ForeignKey(Location_Detials, on_delete=models.CASCADE,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=30,default='')

    class Meta:
        db_table = 'Document_Checklist_Detials'

class DutyRousterMaster(models.Model):
    ShiftId = models.CharField(primary_key=True,max_length=70)
    Department = models.ForeignKey(Department_Detials, on_delete=models.CASCADE, null=True, blank=True)
    Location = models.ForeignKey(Location_Detials, on_delete=models.CASCADE, null=True, blank=True,related_name="location_shift")
    ShiftName = models.CharField(max_length=50, default="") 
    StartTime = models.TimeField(null=False)  # Ensure no NULL for time
    EndTime = models.TimeField(null=False)    # Ensure no NULL for time
    Status = models.BooleanField(default=True)
    Created_by = models.CharField(max_length=70)
    Created_at = models.DateTimeField(auto_now_add=True)
    Updated_at = models.DateTimeField(auto_now=True)
   
    class Meta:
        db_table = 'DutyRousterMaster'  
   



# class ShiftDetails_Master(models.Model):
#     Employee_Shift_Id = models.AutoField(primary_key=True)
#     Employee = models.ForeignKey(Employee_Personal_Form_Detials,on_delete=models.CASCADE)
#     Shift_Id = models.ForeignKey(DutyRousterMaster, on_delete=models.CASCADE,blank=True,null=True)
#     # Intime = models.CharField(max_length=50,blank=True,null=True)  
#     # Outtime = models.CharField(max_length=50,blank=True,null=True) 
#     Shiftstartdate = models.DateField(null=True, blank=True)
#     Shiftenddate = models.DateField(null=True, blank=True)
#     Status = models.CharField(max_length=70, default='')
#     Create_by = models.CharField(max_length=70)
#     Location_Name = models.ForeignKey(Location_Detials,on_delete=models.CASCADE,blank=True,null=True)
#     Created_at = models.DateTimeField(auto_now_add=True)
#     Updated_at = models.DateTimeField(auto_now=True)
   
#     class Meta:
#         db_table = 'ShiftDetails_Master'  


class ShiftDetails_Master(models.Model):
    Employee_Shift_Id = models.AutoField(primary_key=True)
    Employee = models.ForeignKey(Employee_Personal_Form_Detials,on_delete=models.CASCADE)
    Shift_Id = models.ForeignKey(DutyRousterMaster, on_delete=models.CASCADE,blank=True,null=True)
    ShiftDate = models.DateField(null=True,blank=True)
    Status = models.CharField(max_length=70, default='')
    Create_by = models.CharField(max_length=70)
    Location_Name = models.ForeignKey(Location_Detials,on_delete=models.CASCADE,blank=True,null=True)
    Created_at = models.DateTimeField(auto_now_add=True)
    Updated_at = models.DateTimeField(auto_now=True)
   
    class Meta:
        db_table = 'ShiftDetails_Master'
   

# Employee Leave Request



class Employee_Leave_Register(models.Model):
    Leave_Id = models.AutoField(primary_key=True)
    Employee_Id = models.ForeignKey(Current_History_Detials,on_delete=models.CASCADE,blank=True,null=True)
    Leave_Type = models.CharField(max_length=100)
    PermissionDate = models.DateField(null=True, blank=True)
    FromDate = models.DateField(null=True, blank=True)
    ToDate = models.DateField(null=True, blank=True)
    DaysCount = models.IntegerField(null=True, blank=True)
    Medical_Certificate = models.BinaryField(null=True, blank=True)
    FromTime = models.TimeField(null=True, blank=True)
    ToTime = models.TimeField(null=True, blank=True)
    HoursCount = models.CharField(max_length=60, null=True, blank=True, default="0")
    Reason = models.TextField()
    Status = models.CharField(max_length=50, default="Pending")
    Reject_Reason = models.TextField()
    Location_Name = models.ForeignKey(Location_Detials,on_delete=models.CASCADE,blank=True,null=True)
    CreatedBy = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'Employee_Leave_Register'
    def clean(self):
        if self.FromDate and self.ToDate and self.FromDate > self.ToDate:
            return JsonResponse({"warn": "FromDate cannot be later than ToDate."})


    
    
       

# Employee Advance Request
class Employee_Advance_Request(models.Model):
    Advance_RequestId = models.AutoField(primary_key=True)
    Employee_Id = models.ForeignKey(Financial_History_Detials, on_delete=models.CASCADE, blank=True, null=True)
    Request_Date = models.DateField(null=True, blank=True)
    Request_Amount = models.IntegerField()
    Request_Reason = models.TextField()
    Repayment_Due = models.IntegerField(null=True, blank=True)
    Reject_Reason = models.TextField(default="")
    IssuedDate = models.DateField(null=True, blank=True)
    Issuever_Name = models.CharField(max_length=100, default="")
    AmountDeduct_PerMonth = models.IntegerField(null=True, blank=True)
    Installment_Status = models.CharField(max_length=100, default="Pending")
    No_of_MonthPaid = models.IntegerField(null=True, blank=True)
    PaidAmount = models.CharField(max_length=200, default="")
    Status = models.CharField(max_length=50, default="Pending")
    Location_Name = models.ForeignKey(Location_Detials,on_delete=models.CASCADE,blank=True,null=True)
    CreatedBy = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'Employee_Advance_Request'

class Employee_Attendance(models.Model):
    Attendance_Id = models.AutoField(primary_key=True)
    Employee = models.ForeignKey(Employee_Personal_Form_Detials, on_delete=models.CASCADE, blank=True, null=True)
    Date = models.DateField(null=True, blank=True)
    In_Time = models.TimeField(null=True, blank=True)
    Out_Time = models.TimeField(null=True, blank=True)
    Working_Hours = models.FloatField(null=True, blank=True)
    Attendance_Status = models.CharField(max_length=50, default="")
    Location = models.ForeignKey(Location_Detials,on_delete=models.CASCADE,blank=True,null=True)
    CreatedBy = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'Employee_Attendance'


# employee payslip

class Employee_PaySlips(models.Model):
    PaySlip_Id = models.AutoField(primary_key=True)
    Employee = models.ForeignKey(Employee_Personal_Form_Detials, on_delete=models.CASCADE, blank=True, null=True)
    EmployeePayslip = models.BinaryField()
    PaySlip_Date = models.DateField(null=True, blank=True)
    Location = models.ForeignKey(Location_Detials,on_delete=models.CASCADE,blank=True,null=True)
    CreatedBy = models.CharField(max_length=100)
    Paid_Salary = models.FloatField(null=True, blank=True)
    Status = models.CharField(max_length=50, default="")
    SalaryMonth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'Employee_PaySlips'
    
    # employee performance

class Employee_Performance(models.Model):
    Performance_Id = models.AutoField(primary_key=True)
    Employee = models.ForeignKey(Employee_Personal_Form_Detials, on_delete=models.CASCADE, blank=True, null=True)
    HikeType = models.CharField(max_length=100, default="")
    AllowanceName = models.CharField(max_length=100, default="")
    PreviousAllowance = models.IntegerField(null=True, blank=True)
    PreviousAllowanceAmount = models.FloatField(null=True, blank=True)
    NewAllowance = models.IntegerField(null=True, blank=True)
    NewAllowanceAmount = models.FloatField(null=True, blank=True)
    FinalAllowanceAmount = models.FloatField(null=True, blank=True)
    Date = models.DateField(null=True, blank=True)
    Current_Payment = models.FloatField(null=True, blank=True)
    Performance_Rate = models.CharField(max_length=120, default='')
    Hike_Percentage = models.IntegerField(null=True, blank=True)
    Hike_Amount = models.FloatField(null=True, blank=True)
    New_Pay = models.FloatField(null=True, blank=True)
    Remarks = models.CharField(max_length=100, default="")
    ApprovedBy = models.CharField(max_length=100, default="")
    Location_Name = models.ForeignKey(Location_Detials,on_delete=models.CASCADE,blank=True,null=True)
    CreatedBy = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'Employee_Performance'


# employee complaint

class Employee_Complaint(models.Model):
    Complaint_Id = models.AutoField(primary_key=True)
    EmployeeId = models.ForeignKey(Employee_Personal_Form_Detials, on_delete=models.CASCADE, blank=True, null=True, related_name="complaints")
    Complaint = models.CharField(max_length=200, null=True, blank=True, default="")
    IncidentDate = models.DateField(null=True, blank=True)
    IncidentTime = models.TimeField(null=True, blank=True)
    Description = models.TextField(null=True, blank=True)
    Remarks = models.TextField(null=True, blank=True)
    AgainstEmployeeId = models.ForeignKey(
        Employee_Personal_Form_Detials, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        related_name="complaints_against"
    )
    AgainstEmployeeName = models.CharField(max_length=200, null=True, blank=True, default="")
    AgainstEmployeeDepartment = models.ForeignKey(Department_Detials, on_delete=models.CASCADE, blank=True, null=True)
    Witness = models.CharField(max_length=200, null=True, blank=True, default="")
    Location_Name = models.ForeignKey(Location_Detials, on_delete=models.CASCADE, blank=True, null=True)
    CreatedBy = models.CharField(max_length=100, default='')
    Status = models.CharField(max_length=100, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Employee_Complaint'


# hr complaint actions
class HR_ComplaintAction(models.Model):
    HrComplaint_Id = models.AutoField(primary_key=True)
    Complaint = models.ForeignKey(Employee_Complaint, on_delete=models.CASCADE, blank=True, null=True)
    HrAction = models.CharField(max_length=200, null=True, blank=True, default="")
    Remarks = models.TextField(null=True, blank=True)
    FromDate = models.DateField(null=True, blank=True)
    ToDate = models.DateField(null=True, blank=True)
    Location_Name = models.ForeignKey(Location_Detials, on_delete=models.CASCADE, blank=True, null=True)
    CreatedBy = models.CharField(max_length=100, default='')
    Status = models.CharField(max_length=100, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'HR_ComplaintAction'

# circular


class Circular_Details(models.Model):
    Circular_Id = models.AutoField(primary_key=True)
    CircularCreateEmployee = models.ForeignKey(Employee_Personal_Form_Detials, on_delete=models.CASCADE, blank=True, null=True)
    CircularDate = models.DateField(null=True, blank=True)
    CircularTime = models.TimeField(null=True, blank=True)
    Venue = models.ForeignKey(Administration_Master_Details, on_delete=models.CASCADE, blank=True, null=True)
    Subject = models.CharField(max_length=100, default="")
    Remarks = models.CharField(max_length=100, default="")
    Location_Name = models.ForeignKey(Location_Detials, on_delete=models.CASCADE, blank=True, null=True)
    CreatedBy = models.CharField(max_length=100, default='')
    Status = models.CharField(max_length=100, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Circular_Details'

class Circular_Department(models.Model):
    CircularDepartment_Id = models.AutoField(primary_key=True)
    Circular = models.ForeignKey(Circular_Details, on_delete=models.CASCADE, null=True, blank=True)
    Department = models.ForeignKey(Department_Detials, on_delete=models.CASCADE, null=True, blank=True)
    Location_Name = models.ForeignKey(Location_Detials, on_delete=models.CASCADE, blank=True, null=True)
    Status = models.CharField(max_length=100, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Circular_Department'

class Circular_Employee(models.Model):
    CircularEmployee_Id = models.AutoField(primary_key=True)
    Circular = models.ForeignKey(Circular_Details, on_delete=models.CASCADE, null=True, blank=True)
    Location_Name = models.ForeignKey(Location_Detials, on_delete=models.CASCADE, blank=True, null=True)
    Employee = models.ForeignKey(Employee_Personal_Form_Detials, on_delete=models.CASCADE, blank=True, null=True)
    Status = models.CharField(max_length=100, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'Circular_Employee'
        
 
class Trainee_Personal_Form_Details(models.Model):
    Trainee_ID = models.CharField(primary_key=True, max_length=50)
    Tittle = models.ForeignKey(Title_Detials,on_delete=models.CASCADE,blank=True,null=True)
    First_Name = models.CharField(max_length=30)
    Middle_Name = models.CharField(max_length=30,blank=True,null=True)
    Sur_Name = models.CharField(max_length=30,blank=True,null=True)
    Gender = models.CharField(max_length=30)
    DOB = models.CharField(max_length=30)
    Age = models.CharField(max_length=30)
    BloodGroup = models.ForeignKey(BloodGroup_Detials,on_delete=models.CASCADE,blank=True,null=True)
    Phone = models.CharField(max_length=15,blank=True,null=True)
    E_mail = models.CharField(max_length=50,blank=True,null=True)
    Qualification = models.CharField(max_length=30,blank=True,null=True)
    IdProofType = models.CharField(max_length=30,blank=True,null=True)
    IdProofNo = models.CharField(max_length=100,blank=True,null=True)
    Marital_Status = models.CharField(max_length=30,blank=True,null=True)
    SpouseName = models.CharField(max_length=30,blank=True,null=True)
    SpouseContact = models.CharField(max_length=30,blank=True,null=True)
    FatherName = models.CharField(max_length=30,blank=True,null=True)
    FatherContact = models.CharField(max_length=30,blank=True,null=True)
    EmergencyContactName = models.CharField(max_length=30,blank=True,null=True)
    EmergencyContactNo = models.CharField(max_length=30,blank=True,null=True)
    InstitutionalName = models.CharField(max_length=100,blank=True,null=True)
    InchargePerson = models.CharField(max_length=100,blank=True,null=True)
    Trainee_Startdate = models.CharField(max_length=30)
    InductionGivenby = models.CharField(max_length=100,blank=True,null=True)
    Trainee_Enddate = models.CharField(max_length=30)
    Certifiedby = models.CharField(max_length=100,blank=True,null=True)
    Residence = models.CharField(max_length=30, blank=True, null=True)
    Photo = models.BinaryField(blank=True,null=True)
    TraineeCertificate = models.BinaryField(blank=True,null=True)
    Status = models.CharField(max_length=30, blank=True, null=True)
 
    #communication Address
    Pincode = models.CharField(max_length=30,blank=True,null=True)
    DoorNo = models.CharField(max_length=30,blank=True,null=True)
    Street = models.CharField(max_length=255,blank=True,null=True)
    Area = models.CharField(max_length=255,blank=True,null=True)
    City = models.CharField(max_length=30,blank=True,null=True)
    District = models.CharField(max_length=30,blank=True,null=True)
    State = models.CharField(max_length=30,blank=True,null=True)
    Country = models.CharField(max_length=30,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    Createdby = models.CharField(max_length=30)
   
    class Meta:
        db_table = 'Trainee_Personal_Form_Details'
 
 
    def save(self, *args, **kwargs):
        if not self.Trainee_ID:
            hospital_details = Hospital_Detials.objects.first()
            if not hospital_details:
                raise ValueError("No Hospital_Details records found.")
           
            clinic_name = hospital_details.Hospital_Name[:3].upper()
            today_date = datetime.now().strftime('%y%m%d')
            prefix = f'{clinic_name}{today_date}TRA'
           
            # Find the maximum numeric part from existing PatientId with the same prefix
            max_Registration_Id = Trainee_Personal_Form_Details.objects.aggregate(max_id=Max('Trainee_ID'))['max_id']
            # print(max_Registration_Id)
            if max_Registration_Id:
                numeric_part = int(max_Registration_Id[-5:]) + 1
            else:
                numeric_part = 1
            self.Trainee_ID = f'{prefix}{numeric_part:05}'
       
        super(Trainee_Personal_Form_Details, self).save(*args, **kwargs)

    
    




