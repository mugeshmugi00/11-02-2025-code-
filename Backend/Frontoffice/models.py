from django.db import models
from django.db.models import Max
from Masters.models import *
from django.core.exceptions import ValidationError
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.timezone import now





# Create your models here.
class EmergencyRegister(models.Model):
    EmergencyRegister_Id = models.IntegerField(primary_key=True)
    PatientName = models.CharField(max_length=50)
    PatientPhone = models.CharField(max_length=50)
    Speciality = models.ForeignKey(Speciality_Detials, on_delete=models.CASCADE, related_name='emg_register_specialities',null=True,blank=True)
    PrimaryDoctor = models.ForeignKey(Doctor_Personal_Form_Detials, on_delete=models.CASCADE, related_name='emg_register_Doctor')
    ReferalDoctor = models.CharField(max_length=50)
    Status = models.CharField(max_length=30, default='Pending')
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'EmergencyRegister'

    
    
    def save(self, *args, **kwargs):
        if not self.EmergencyRegister_Id:  # Check if accountsetting_id is not set
            max_id = EmergencyRegister.objects.aggregate(max_id=Max('EmergencyRegister_Id'))['max_id']
            self.EmergencyRegister_Id = (max_id or 0) + 1
        super(EmergencyRegister, self).save(*args,**kwargs)



class Patient_Detials(models.Model):
    PatientId = models.CharField(primary_key=True,max_length=30)
    DuplicateId = models.BooleanField(default=False)
    Patient_profile = models.BinaryField(null=True,blank=True,default=True)
    Title = models.ForeignKey(Title_Detials,on_delete=models.CASCADE,null=True,blank=True,related_name='patientId_Title')
    # Title = models.CharField(max_length=30,blank=True,null=True)
    FirstName = models.CharField(max_length=30,blank=True,null=True)
    MiddleName = models.CharField(max_length=30,blank=True,null=True)
    SurName = models.CharField(max_length=30,blank=True,null=True)
    Gender = models.CharField(max_length=30,blank=True,null=True)
    # AliasName = models.CharField(max_length=30)
    MaritalStatus = models.CharField(max_length=30,blank=True,null=True)
    SpouseName = models.CharField(max_length=50,blank=True,null=True)
    FatherName = models.CharField(max_length=50,blank=True,null=True)
    DOB = models.CharField(max_length=20,blank=True,null=True)
    Age = models.CharField(max_length=20,blank=True,null=True)
    PhoneNo = models.CharField(max_length=30,blank=True,null=True)
    Email = models.CharField(max_length=30,blank=True,null=True)
    BloodGroup = models.ForeignKey(BloodGroup_Detials,on_delete=models.CASCADE,null=True,blank=True,related_name='patientId_Bloodgroup')
    Occupation = models.CharField(max_length=30,blank=True,null=True)
    Religion = models.ForeignKey(Religion_Detials, on_delete=models.CASCADE, related_name='Orgional_patientId',null=True,blank=True)
    Nationality = models.CharField(max_length=30,blank=True,null=True)
    UniqueIdType = models.CharField(max_length=30,blank=True,null=True)
    UniqueIdNo = models.CharField(max_length=30,blank=True,null=True)
 
    PatientType = models.CharField(max_length=30,blank=True,null=True)
    ABHA = models.CharField(max_length=30,blank=True,null=True)
    Flagging = models.ForeignKey(Flaggcolor_Detials,on_delete=models.CASCADE,null=True, blank=True)
    
    DoorNo = models.CharField(max_length=20,blank=True,null=True)
    Street = models.CharField(max_length=30,blank=True,null=True)
    Area = models.CharField(max_length=30,blank=True,null=True)
    City = models.CharField(max_length=30,blank=True,null=True)
    District = models.CharField(max_length=50,blank=True,null=True)
    State = models.CharField(max_length=30,blank=True,null=True)
    Country = models.CharField(max_length=30,blank=True,null=True)
    Pincode = models.CharField(max_length=20,blank=True,null=True)
    
    PermanentAddressSameAsAbove = models.CharField(max_length=20,blank=True,null=True)
   
    PermanentdoorNo = models.CharField(max_length=20,blank=True,null=True)
    PermanentStreet = models.CharField(max_length=30,blank=True,null=True)
    PermanentArea = models.CharField(max_length=30,blank=True,null=True)
    PermanentCity = models.CharField(max_length=30,blank=True,null=True)
    PermanentDistrict = models.CharField(max_length=50,blank=True,null=True)
    PermanentState = models.CharField(max_length=30,blank=True,null=True)
    PermanentCountry = models.CharField(max_length=30,blank=True,null=True)
    PermanentPincode = models.CharField(max_length=20,blank=True,null=True)
   
    DoctorID = models.ForeignKey(Doctor_Personal_Form_Detials,on_delete=models.CASCADE,null=True, blank=True)
    SpecializationId = models.ForeignKey(Speciality_Detials,on_delete=models.CASCADE,null=True, blank=True)
    ReferredBy = models.ForeignKey(Doctor_Personal_Form_Detials,on_delete=models.CASCADE,related_name='appprefer',null=True,blank=True)
   
   
   
    created_by = models.CharField(max_length=30)
    Status = models.CharField(max_length=20, default='Saved')
    updated_by = models.CharField(max_length=30,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        db_table = 'Patient_Detials'
   
   
    def save(self, *args, **kwargs):
       
 
        if not self.PatientId:
            hospital_details = Hospital_Detials.objects.first()
            if not hospital_details:
                raise ValueError("No Hospital_Details records found.")
           
            clinic_name = hospital_details.Hospital_Name[:3].upper()
            today_date = datetime.now().strftime('%y%m%d')
            prefix = f'{clinic_name}{today_date}'
           
            # Find the maximum numeric part from existing PatientId with the same prefix
            max_patient_id = Patient_Detials.objects.aggregate(max_id=Max('PatientId'))['max_id']
            if max_patient_id:
                numeric_part = int(max_patient_id[-4:]) + 1
            else:
                numeric_part = 1
            self.PatientId = f'{prefix}{numeric_part:04}'
       
        super(Patient_Detials, self).save(*args, **kwargs)
 




# # --------------Appointment Request List

class Appointment_Request_List(models.Model):
    appointment_id = models.IntegerField(primary_key=True)
    title = models.ForeignKey(Title_Detials,on_delete=models.CASCADE,blank=True,null=True,related_name='Appointment_title')
    PatientId = models.ForeignKey(Patient_Detials,on_delete=models.CASCADE,blank=True,null=True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    request_date = models.DateField()
    appointment_type = models.CharField(max_length=10)
    request_time = models.TimeField()
    visit_purpose = models.CharField(max_length=30)
    specialization = models.ForeignKey(Speciality_Detials, on_delete=models.CASCADE,related_name='appointment_request_list_specialization',null=True,blank=True)
    doctor_name = models.ForeignKey(Doctor_Personal_Form_Detials, on_delete=models.CASCADE,related_name='appointment_request_list_doctor_name',null=True,blank=True)
    Location =models.ForeignKey(Location_Detials ,on_delete=models.CASCADE)
    status = models.CharField(max_length=30, default='PENDING')
    created_by = models.CharField(max_length=30)
    updated_by = models.CharField(max_length=30,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cancelReason = models.CharField(max_length=200)
    ReferredBy = models.ForeignKey(Doctor_Personal_Form_Detials,on_delete=models.CASCADE,related_name='appreferallldoctor',null=True,blank=True)
    def __str__(self):
        return f"{self.title} {self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        if not self.appointment_id:  # Check if appointment_id is not set (i.e., new instance)
            max_id = Appointment_Request_List.objects.aggregate(max_id=Max('appointment_id'))['max_id']
            self.appointment_id = (max_id or 0) + 1
        super(Appointment_Request_List, self).save(*args, **kwargs)


class Appointment_ReSchedule_Request(models.Model):
    appointmentId = models.ForeignKey(Appointment_Request_List,on_delete=models.CASCADE,null=True,blank=True)
    RadioOption = models.CharField(max_length=30)
    RequestDate = models.DateField()
    ChangingReason = models.TextField(default='')
    specialization = models.ForeignKey(Speciality_Detials, on_delete=models.CASCADE,related_name='appointment_reschedule_list_specialization',null=True,blank=True)
    doctor_name = models.ForeignKey(Doctor_Personal_Form_Detials, on_delete=models.CASCADE,related_name='appointment_reschedule_list_doctor_name',null=True,blank=True)
    created_by = models.CharField(max_length=30, default='')
    updated_by = models.CharField(max_length=30,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ReferredBy = models.ForeignKey(Doctor_Personal_Form_Detials,on_delete=models.CASCADE,related_name='appointmentreferal',null=True,blank=True)

# # --------------patient registration

# class Patient_Detials(models.Model):
#     PatientId = models.CharField(primary_key=True,max_length=30)
#     DuplicateId = models.BooleanField(default=False)
#     Patient_profile = models.BinaryField(null=True,blank=True,default=True)
#     PhoneNo = models.CharField(max_length=30)
#     Title = models.CharField(max_length=30)
#     FirstName = models.CharField(max_length=30)
#     MiddleName = models.CharField(max_length=30)
#     SurName = models.CharField(max_length=30)
#     Gender = models.CharField(max_length=30)
#     AliasName = models.CharField(max_length=30)
#     MaritalStatus = models.CharField(max_length=30,blank=True,null=True)
#     SpouseName = models.CharField(max_length=50,blank=True,null=True)
#     FatherName = models.CharField(max_length=50,blank=True,null=True)
#     DOB = models.CharField(max_length=20)
#     Age = models.CharField(max_length=20)
#     Email = models.CharField(max_length=30)
#     BloodGroup = models.ForeignKey(BloodGroup_Detials,on_delete=models.CASCADE,null=True,blank=True,related_name='patientId_Bloodgroup')
#     Occupation = models.CharField(max_length=30)
#     Religion = models.ForeignKey(Religion_Detials, on_delete=models.CASCADE, related_name='Orgional_patientId',null=True,blank=True)
#     Nationality = models.CharField(max_length=30)
#     UniqueIdType = models.CharField(max_length=30)
#     UniqueIdNo = models.CharField(max_length=30)
#     DoorNo = models.CharField(max_length=20)
#     Street = models.CharField(max_length=30)
#     Area = models.CharField(max_length=30)
#     City = models.CharField(max_length=30)
#     District = models.CharField(max_length=50,blank=True,null=True)
#     State = models.CharField(max_length=30)
#     Country = models.CharField(max_length=30)
#     Pincode = models.CharField(max_length=20)
#     created_by = models.CharField(max_length=30)
#     updated_by = models.CharField(max_length=30,default='')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = 'Patient_Detials'
    
    
#     def save(self, *args, **kwargs):
       

#         if not self.PatientId:
#             hospital_details = Hospital_Detials.objects.first()
#             if not hospital_details:
#                 raise ValueError("No Hospital_Details records found.")
            
#             clinic_name = hospital_details.Hospital_Name[:3].upper()
#             today_date = datetime.now().strftime('%y%m%d')
#             prefix = f'{clinic_name}{today_date}'
            
#             # Find the maximum numeric part from existing PatientId with the same prefix
#             max_patient_id = Patient_Detials.objects.aggregate(max_id=Max('PatientId'))['max_id']
#             if max_patient_id:
#                 numeric_part = int(max_patient_id[-4:]) + 1
#             else:
#                 numeric_part = 1
#             self.PatientId = f'{prefix}{numeric_part:04}'
       
#         super(Patient_Detials, self).save(*args, **kwargs)





class Duplicates_patients(models.Model):
    Orgional_patientId = models.ForeignKey(Patient_Detials, on_delete=models.CASCADE, related_name='Orgional_patientId')
    Duplicates_patientId = models.ForeignKey(Patient_Detials, on_delete=models.CASCADE, related_name='Duplicates_patientId')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Duplicates_patients'
   


class Patient_Visit_Detials(models.Model):
    PatientId = models.ForeignKey(Patient_Detials, on_delete=models.CASCADE, related_name='Patient_Visit_patient_detials')
    VisitId = models.IntegerField(default=1)
    RegisterType = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Patient_Visit_Detials'
   





class Patient_Appointment_Registration_Detials(models.Model):  
    Registration_Id = models.CharField(max_length=30, unique=True)
    PatientId = models.ForeignKey(Patient_Detials, on_delete=models.CASCADE, related_name='appointment_details')
    VisitId = models.IntegerField()
    VisitPurpose = models.CharField(max_length=30,blank=True,null=True)
    VisitType = models.CharField(max_length=30,blank=True,null=True)
    Specialization = models.ForeignKey(Speciality_Detials, on_delete=models.CASCADE, related_name='appointment_speciality', null=True, blank=True)
    PrimaryDoctor = models.ForeignKey(Doctor_Personal_Form_Detials, on_delete=models.CASCADE, related_name='appointment_doctor', null=True, blank=True)
    AppointmentId = models.IntegerField()
    ApptoRegId = models.ForeignKey(Appointment_Request_List, on_delete=models.CASCADE, null=True, blank=True)
    AppointmentSlot_by_Specialization = models.IntegerField()
    AppointmentSlot_by_Doctor = models.IntegerField()
    Complaint = models.TextField(default='')
    PatientCategory = models.CharField(max_length=30,blank=True,null=True)
    InsuranceName = models.ForeignKey(Insurance_Master_Detials,on_delete=models.CASCADE,null=True,blank=True)
    # InsuranceName = models.CharField(max_length=30)
    # PatientType = models.CharField(max_length=30,blank=True,null=True)
    InsuranceType = models.CharField(max_length=30,blank=True,null=True)
    # ClientName = models.CharField(max_length=30)
    TokenNo = models.CharField(max_length=30,blank=True,null=True)
    ClientName = models.ForeignKey(Client_Master_Detials,on_delete=models.CASCADE,null=True,blank=True)
    ClientType = models.CharField(max_length=30,blank=True,null=True)
    ClientEmployeeId = models.CharField(max_length=30,blank=True,null=True)
    ClientEmployeeDesignation = models.CharField(max_length=30,blank=True,null=True)
    ClientEmployeeRelation = models.CharField(max_length=30,blank=True,null=True)
    CorporateName = models.ForeignKey(Corporate_Master_Detials, on_delete=models.CASCADE, related_name='patient_details_CorporateId', null=True, blank=True)
    CorporateType = models.CharField(max_length=30,blank=True,null=True)
    CorporateEmployeeId = models.CharField(max_length=30,blank=True,null=True)
    CorporateEmployeeDesignation = models.CharField(max_length=30,blank=True,null=True)
    CorporateEmployeeRelation = models.CharField(max_length=30,blank=True,null=True)
   
    EmployeeId = models.ForeignKey(Employee_Personal_Form_Detials, on_delete=models.CASCADE, related_name='appointment_EmployeeId', null=True, blank=True)
    EmployeeRelation = models.CharField(max_length=40,blank=True,null=True)
    DoctorId = models.ForeignKey(Doctor_Personal_Form_Detials, on_delete=models.CASCADE, related_name='appointment_DoctorId', null=True, blank=True)
    DoctorRelation = models.CharField(max_length=30,blank=True,null=True)
    # DonationType = models.CharField(max_length=30,blank=True,null=True)
    DonationType = models.ForeignKey(Donation_Master_Detials, on_delete=models.CASCADE, related_name='patient_details_DonationId', null=True, blank=True)
    IsMLC = models.CharField(max_length=20,blank=True,null=True)
    # Flagging = models.ForeignKey(Flaggcolor_Detials,on_delete=models.CASCADE,null=True, blank=True)
    IsReferral = models.CharField(max_length=20,blank=True,null=True)
    Status = models.CharField(max_length=20, default='Registered')
    ConsultingTime = models.DateTimeField(null=True, blank=True)
    CompletedTime = models.DateTimeField(null=True, blank=True)
    FinalCompletedTime = models.DateTimeField(null=True, blank=True)
    CancelTime = models.DateTimeField(null=True, blank=True)
    CancelReason = models.TextField(null=True, blank=True)
    ResheduleDoctor = models.ForeignKey(Doctor_Personal_Form_Detials, on_delete=models.CASCADE, null=True, blank=True)
    ResheduleSpeciality = models.ForeignKey(Speciality_Detials, on_delete=models.CASCADE, null=True, blank=True)
    ResheduleReason = models.TextField(null=True, blank=True)
    ResheduleTime = models.DateTimeField(null=True, blank=True)    
    Reason = models.TextField()
    IP_Request_status = models.CharField(max_length=20, default='No')
    Location = models.ForeignKey(Location_Detials, on_delete=models.CASCADE,blank=True,null=True)
    NextToKinName = models.CharField(max_length=50,blank=True,null=True)
    Relation = models.CharField(max_length=50,blank=True,null=True)
    RelativePhNo = models.CharField(max_length=30,blank=True,null=True)
    ServiceCategory = models.CharField(max_length=30,blank=True,null=True)
    ServiceSubCategory = models.CharField(max_length=30,blank=True,null=True)
    created_by = models.CharField(max_length=30)
    updated_by = models.CharField(max_length=30,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Patient_Appointment_Registration_Detials'


    def save(self, *args, **kwargs):
            # Check if this is a new instance (when self.pk is None)
            if not self.pk:
                current_date = datetime.now().strftime('%Y-%m-%d')
                start_id = 1

                # AppointmentId logic
                max_id_today = Patient_Appointment_Registration_Detials.objects.filter(
                    created_at__date=current_date
                ).aggregate(max_id=Max('AppointmentId'))['max_id']
                self.AppointmentId = (max_id_today or 0) + start_id
                
                # AppointmentSlot by specialization logic
                max_spi_slot_today = Patient_Appointment_Registration_Detials.objects.filter(
                    created_at__date=current_date,
                    Specialization=self.Specialization
                ).aggregate(max_slot=Max('AppointmentSlot_by_Specialization'))['max_slot']
                self.AppointmentSlot_by_Specialization = (max_spi_slot_today or 0) + start_id
                
                # AppointmentSlot by doctor logic
                max_doc_slot_today = Patient_Appointment_Registration_Detials.objects.filter(
                    created_at__date=current_date,
                    PrimaryDoctor=self.PrimaryDoctor
                ).aggregate(max_slot=Max('AppointmentSlot_by_Doctor'))['max_slot']
                self.AppointmentSlot_by_Doctor = (max_doc_slot_today or 0) + start_id
                
                # Generate Registration_Id
                hospital_details = Hospital_Detials.objects.first()
                if not hospital_details:
                    raise ValueError("No Hospital_Details records found.")
                
                clinic_name = hospital_details.Hospital_Name[:3].upper()
                today_date = datetime.now().strftime('%y%m%d')
                prefix = f'{clinic_name}{today_date}OP'
                
                # Find the maximum numeric part from existing PatientId with the same prefix
                max_Registration_Id = Patient_Appointment_Registration_Detials.objects.aggregate(max_id=Max('Registration_Id'))['max_id']
                if max_Registration_Id:
                    numeric_part = int(max_Registration_Id[-5:]) + 1
                else:
                    numeric_part = 1
                self.Registration_Id = f'{prefix}{numeric_part:05}'
                
            super(Patient_Appointment_Registration_Detials, self).save(*args, **kwargs)

    
    def clean(self):
        super().clean()
        # Validate length of all CharField fields
        char_fields = [
            'VisitPurpose', 'CaseSheetNo', 'ANCNumber', 'MCTSNo', 'Complaint', 'PatientType',
            'InsuranceName', 'InsuranceType', 'ClientName', 'ClientType', 'ClientEmployeeId', 'ClientEmployeeDesignation',
            'ClientEmployeeRelation', 'EmployeeRelation', 'DoctorRelation', 'DonationType', 'IsMLC', 'Flagging', 'IsReferral',
            'Status', 'created_by'
        ]
        for field in char_fields:
            value = getattr(self, field, '')
            if len(value) > self._meta.get_field(field).max_length:
                raise ValidationError({'error': f"{field} cannot be more than {self._meta.get_field(field).max_length} characters."})

        # Validate length of Reason field if needed
        if len(self.Reason) > 1000:  # assuming a max length for Reason
            raise ValidationError({'error': "Reason cannot be more than 1000 characters."})


 
class Patient_IP_Registration_Detials(models.Model):
    Registration_Id = models.CharField(primary_key=True,max_length=30)
    PatientId = models.ForeignKey(Patient_Detials, on_delete=models.CASCADE,)
    # VisitId = models.IntegerField()
    Specialization = models.ForeignKey(Speciality_Detials,on_delete=models.CASCADE,null=True,blank=True)
    PrimaryDoctor = models.ForeignKey(Doctor_Personal_Form_Detials,on_delete=models.CASCADE,related_name='Primary_doctor_ip_details',null=True,blank=True)
    Complaint = models.TextField(default='')
    IsMLC = models.CharField(max_length=20)
    Flagging = models.ForeignKey(Flaggcolor_Detials,on_delete=models.CASCADE,null=True, blank=True)
    IsReferral = models.CharField(max_length=20)
    
    PatientCategory = models.CharField(max_length=30,blank=True,null=True)
    InsuranceName = models.ForeignKey(Insurance_Master_Detials,on_delete=models.CASCADE,null=True,blank=True)
    InsuranceType = models.CharField(max_length=30,blank=True,null=True)
    ClientName = models.ForeignKey(Client_Master_Detials,on_delete=models.CASCADE,null=True,blank=True)
    ClientType = models.CharField(max_length=30,blank=True,null=True)
    ClientEmployeeId = models.CharField(max_length=30,blank=True,null=True)
    ClientEmployeeDesignation = models.CharField(max_length=30,blank=True,null=True)
    ClientEmployeeRelation = models.CharField(max_length=30,blank=True,null=True)
    CorporateName = models.ForeignKey(Corporate_Master_Detials, on_delete=models.CASCADE, related_name='IP_patient_details_CorporateId', null=True, blank=True)
    CorporateType = models.CharField(max_length=30,blank=True,null=True)
    CorporateEmployeeId = models.CharField(max_length=30,blank=True,null=True)
    CorporateEmployeeDesignation = models.CharField(max_length=30,blank=True,null=True)
    CorporateEmployeeRelation = models.CharField(max_length=30,blank=True,null=True)
   
    EmployeeId = models.ForeignKey(Employee_Personal_Form_Detials, on_delete=models.CASCADE, related_name='IP_appointment_EmployeeId', null=True, blank=True)
    EmployeeRelation = models.CharField(max_length=40,blank=True,null=True)
    DoctorId = models.ForeignKey(Doctor_Personal_Form_Detials, on_delete=models.CASCADE, related_name='IP_appointment_DoctorId', null=True, blank=True)
    DoctorRelation = models.CharField(max_length=30,blank=True,null=True)
    DonationType = models.ForeignKey(Donation_Master_Detials, on_delete=models.CASCADE, related_name='IP_patient_details_DonationId', null=True, blank=True)
    # DonationType = models.CharField(max_length=30,blank=True,null=True)
    Status = models.CharField(max_length=20,default='Pending')
    Booking_Status = models.CharField(max_length=30, default='Booked')
    Reason =models.TextField(default='')
    Location =models.ForeignKey(Location_Detials ,on_delete=models.CASCADE)
    created_by = models.CharField(max_length=30)
    updated_by = models.CharField(max_length=30,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Patient_IP_Registration_Detials'
    def save(self, *args, **kwargs):
        if not self.Registration_Id:
            hospital_details = Hospital_Detials.objects.first()
            if not hospital_details:
                raise ValueError("No Hospital_Details records found.")
            
            clinic_name = hospital_details.Hospital_Name[:3].upper()
            today_date = datetime.now().strftime('%y%m%d')
            prefix = f'{clinic_name}{today_date}IP'
            
            # Find the maximum numeric part from existing PatientId with the same prefix
            max_Registration_Id = Patient_IP_Registration_Detials.objects.aggregate(max_id=Max('Registration_Id'))['max_id']
            if max_Registration_Id:
                numeric_part = int(max_Registration_Id[-5:]) + 1
            else:
                numeric_part = 1
            self.Registration_Id = f'{prefix}{numeric_part:05}'
       
        super(Patient_IP_Registration_Detials, self).save(*args, **kwargs)


class Patient_Emergency_Registration_Detials(models.Model):
    Registration_Id = models.CharField(primary_key=True,max_length=30)
    PatientId = models.ForeignKey(Patient_Detials, on_delete=models.CASCADE,blank=True,null=True)
    IdentificationMark1 = models.TextField(default='')
    IdentificationMark2 = models.TextField(default='')
    Instructions = models.TextField(default='')
    IsConscious = models.CharField(max_length=20,blank=True,null=True)
    IsMLC = models.CharField(max_length=20,blank=True,null=True)

    Specialization = models.ForeignKey(Speciality_Detials,on_delete=models.CASCADE,null=True,blank=True)
    PrimaryDoctor = models.ForeignKey(Doctor_Personal_Form_Detials,on_delete=models.CASCADE,related_name='Primary_doctor_Emergency_details',null=True,blank=True)
    Complaint = models.TextField(default='')
    Flagging = models.ForeignKey(Flaggcolor_Detials,on_delete=models.CASCADE,null=True, blank=True)
    IsReferral = models.CharField(max_length=20,blank=True,null=True)

    PatientCategory = models.CharField(max_length=30,blank=True,null=True)
    InsuranceName = models.ForeignKey(Insurance_Master_Detials,on_delete=models.CASCADE,null=True,blank=True)
    InsuranceType = models.CharField(max_length=30,blank=True,null=True)
    ClientName = models.ForeignKey(Client_Master_Detials,on_delete=models.CASCADE,null=True,blank=True)
    ClientType = models.CharField(max_length=30,blank=True,null=True)
    ClientEmployeeId = models.CharField(max_length=30,blank=True,null=True)
    ClientEmployeeDesignation = models.CharField(max_length=30,blank=True,null=True)
    ClientEmployeeRelation = models.CharField(max_length=30,blank=True,null=True)
    CorporateName = models.ForeignKey(Corporate_Master_Detials, on_delete=models.CASCADE, related_name='Emergency_patient_details_CorporateId', null=True, blank=True)
    CorporateType = models.CharField(max_length=30,blank=True,null=True)
    CorporateEmployeeId = models.CharField(max_length=30,blank=True,null=True)
    CorporateEmployeeDesignation = models.CharField(max_length=30,blank=True,null=True)
    CorporateEmployeeRelation = models.CharField(max_length=30,blank=True,null=True)
   
    EmployeeId = models.ForeignKey(Employee_Personal_Form_Detials, on_delete=models.CASCADE, related_name='Emergency_appointment_EmployeeId', null=True, blank=True)
    EmployeeRelation = models.CharField(max_length=40,blank=True,null=True)
    DoctorId = models.ForeignKey(Doctor_Personal_Form_Detials, on_delete=models.CASCADE, related_name='Emergency_appointment_DoctorId', null=True, blank=True)
    DoctorRelation = models.CharField(max_length=30,blank=True,null=True)
    DonationType = models.ForeignKey(Donation_Master_Detials, on_delete=models.CASCADE, related_name='Emergency_patient_details_DonationId', null=True, blank=True)
    Booking_Status = models.CharField(max_length=30, default='Occupied')
    Reason =models.TextField(default='')

    Status = models.CharField(max_length=20,default='Admitted')
    SavedStatus = models.CharField(max_length=20,default='Saved')
    Location =models.ForeignKey(Location_Detials ,on_delete=models.CASCADE)
    created_by = models.CharField(max_length=30)
    updated_by = models.CharField(max_length=30,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Patient_Emergency_Registration_Detials'
    def save(self, *args, **kwargs):
        if not self.Registration_Id:
            hospital_details = Hospital_Detials.objects.first()
            if not hospital_details:
                raise ValueError("No Hospital_Details records found.")
            
            clinic_name = hospital_details.Hospital_Name[:3].upper()
            today_date = datetime.now().strftime('%y%m%d')
            prefix = f'{clinic_name}{today_date}EMG'
            
            # Find the maximum numeric part from existing PatientId with the same prefix
            max_Registration_Id = Patient_Emergency_Registration_Detials.objects.aggregate(max_id=Max('Registration_Id'))['max_id']
            if max_Registration_Id:
                numeric_part = int(max_Registration_Id[-5:]) + 1
            else:
                numeric_part = 1
            self.Registration_Id = f'{prefix}{numeric_part:05}'
       
        super(Patient_Emergency_Registration_Detials, self).save(*args, **kwargs)
 

  
class Patient_Casuality_Registration_Detials(models.Model):
    Registration_Id = models.CharField(max_length=30,unique=True)
    IsConsciousness = models.BooleanField(default=True) 
    PatientId = models.ForeignKey(Patient_Detials, on_delete=models.CASCADE, related_name='casuality_appointment_details',null=True,blank=True,default=None)
    VisitId = models.IntegerField(null=True,blank=True)
    Specialization = models.ForeignKey(Speciality_Detials,on_delete=models.CASCADE,related_name='casuality_appointment_speciality',null=True,blank=True)
    PrimaryDoctor = models.ForeignKey(Doctor_Personal_Form_Detials,on_delete=models.CASCADE,related_name='casuality_appointment_doctor',null=True,blank=True)
    Complaint = models.TextField(default="")
    PatientType = models.CharField(max_length=30)
    PatientCategory = models.CharField(max_length=30)
    InsuranceName = models.ForeignKey(Insurance_Master_Detials,on_delete=models.CASCADE,null=True,blank=True)
    # InsuranceName = models.CharField(max_length=30)
    InsuranceType = models.CharField(max_length=30)
    ClientName = models.ForeignKey(Client_Master_Detials,on_delete=models.CASCADE,null=True,blank=True)
    # ClientName = models.CharField(max_length=30)
    ClientType = models.CharField(max_length=30)
    ClientEmployeeId = models.CharField(max_length=30)
    ClientEmployeeDesignation = models.CharField(max_length=30)
    ClientEmployeeRelation = models.CharField(max_length=30)
    EmployeeId = models.ForeignKey(Employee_Personal_Form_Detials,on_delete=models.CASCADE,related_name='casuality_appointment_EmployeeId',null=True,blank=True)
    EmployeeRelation = models.CharField(max_length=30)
    DoctorId = models.ForeignKey(Doctor_Personal_Form_Detials,on_delete=models.CASCADE,related_name='casuality_appointment_DoctorId',null=True,blank=True)
    DoctorRelation = models.CharField(max_length=30)
    DonationType = models.CharField(max_length=30)
    IsMLC = models.CharField(max_length=20)
    Flagging = models.ForeignKey(Flaggcolor_Detials,on_delete=models.CASCADE,null=True, blank=True)
    IsReferral = models.CharField(max_length=20)
    Status = models.CharField(max_length=20,default='Pending')
    Booking_Status = models.CharField(max_length=30, default='Booked')
    Reason =models.CharField(max_length=200)
    Location =models.ForeignKey(Location_Detials ,on_delete=models.CASCADE)
    created_by = models.CharField(max_length=30)
    updated_by = models.CharField(max_length=30,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Patient_Casuality_Registration_Detials'
    def save(self, *args, **kwargs):
       

        if not self.Registration_Id:
            hospital_details = Hospital_Detials.objects.first()
            if not hospital_details:
                raise ValueError("No Hospital_Details records found.")
            
            clinic_name = hospital_details.Hospital_Name[:3].upper()
            today_date = datetime.now().strftime('%y%m%d')
            prefix = f'{clinic_name}{today_date}CAS'
            
            # Find the maximum numeric part from existing PatientId with the same prefix
            max_patient_id = Patient_Casuality_Registration_Detials.objects.aggregate(max_id=Max('Registration_Id'))['max_id']
            if max_patient_id:
                numeric_part = int(max_patient_id[-5:]) + 1
            else:
                numeric_part = 1
            self.Registration_Id = f'{prefix}{numeric_part:05}'
       
        super(Patient_Casuality_Registration_Detials, self).save(*args, **kwargs)
    

class Patient_Diagnosis_Registration_Detials(models.Model):
    Registration_Id = models.CharField(max_length=30,unique=True)
    PatientId = models.ForeignKey(Patient_Detials, on_delete=models.CASCADE, related_name='Diagnosis_appointment_details')
    VisitId = models.IntegerField(null= True)
    Specialization = models.ForeignKey(Speciality_Detials,on_delete=models.CASCADE,related_name='Diagnosis_appointment_speciality',null=True,blank=True)
    PrimaryDoctor = models.ForeignKey(Doctor_Personal_Form_Detials,on_delete=models.CASCADE,related_name='Diagnosis_appointment_doctor',null=True,blank=True)
    Complaint = models.TextField(default='')
    PatientType = models.CharField(max_length=30)
    PatientCategory = models.CharField(max_length=30)
    InsuranceName = models.ForeignKey(Insurance_Master_Detials,on_delete=models.CASCADE,null=True,blank=True)
    # InsuranceName = models.CharField(max_length=30)
    InsuranceType = models.CharField(max_length=30)
    ClientName = models.ForeignKey(Client_Master_Detials,on_delete=models.CASCADE,null=True,blank=True)
    # ClientName = models.CharField(max_length=30)
    ClientType = models.CharField(max_length=30)
    ClientEmployeeId = models.CharField(max_length=30)
    ClientEmployeeDesignation = models.CharField(max_length=30)
    ClientEmployeeRelation = models.CharField(max_length=30)
    EmployeeId = models.ForeignKey(Employee_Personal_Form_Detials,on_delete=models.CASCADE,related_name='Diagnosis_appointment_EmployeeId',null=True,blank=True)
    EmployeeRelation = models.CharField(max_length=30)
    DoctorId = models.ForeignKey(Doctor_Personal_Form_Detials,on_delete=models.CASCADE,related_name='Diagnosis_appointment_DoctorId',null=True,blank=True)
    DoctorRelation = models.CharField(max_length=30)
    DonationType = models.CharField(max_length=30)
    IsMLC = models.CharField(max_length=20)
    Flagging = models.ForeignKey(Flaggcolor_Detials,on_delete=models.CASCADE,null=True, blank=True)
    IsReferral = models.CharField(max_length=20)
    Status = models.CharField(max_length=20,default='Pending')
    Reason =models.CharField(max_length=200)
    Location =models.ForeignKey(Location_Detials ,on_delete=models.CASCADE)
    created_by = models.CharField(max_length=30)
    updated_by = models.CharField(max_length=30,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Patient_Diagnosis_Registration_Detials'
    
    def save(self, *args, **kwargs):
       

        if not self.Registration_Id:
            hospital_details = Hospital_Detials.objects.first()
            if not hospital_details:
                raise ValueError("No Hospital_Details records found.")
            
            clinic_name = hospital_details.Hospital_Name[:3].upper()
            today_date = datetime.now().strftime('%y%m%d')
            prefix = f'{clinic_name}{today_date}DIAG'
            
            # Find the maximum numeric part from existing PatientId with the same prefix
            max_Registration_Id = Patient_Diagnosis_Registration_Detials.objects.aggregate(max_id=Max('Registration_Id'))['max_id']
            if max_Registration_Id:
                numeric_part = int(max_Registration_Id[-5:]) + 1
            else:
                numeric_part = 1
            self.Registration_Id = f'{prefix}{numeric_part:05}'
       
        super(Patient_Diagnosis_Registration_Detials, self).save(*args, **kwargs)



class Patient_Laboratory_Registration_Detials(models.Model):
    Registration_Id = models.CharField(max_length=30,unique=True)
    PatientId = models.ForeignKey(Patient_Detials, on_delete=models.CASCADE, related_name='Laboratory_appointment_details')
    VisitId = models.IntegerField()
    Specialization = models.ForeignKey(Speciality_Detials,on_delete=models.CASCADE,related_name='laboratory_appointment_speciality',null=True,blank=True)
    PrimaryDoctor = models.ForeignKey(Doctor_Personal_Form_Detials,on_delete=models.CASCADE,related_name='laboratory_appointment_doctor',null=True,blank=True)
    Complaint = models.TextField(default='')
    PatientType = models.CharField(max_length=30)
    PatientCategory = models.CharField(max_length=30)
    InsuranceName = models.ForeignKey(Insurance_Master_Detials,on_delete=models.CASCADE,null=True,blank=True)
    # InsuranceName = models.CharField(max_length=30)
    InsuranceType = models.CharField(max_length=30)
    ClientName = models.ForeignKey(Client_Master_Detials,on_delete=models.CASCADE,null=True,blank=True)
    # ClientName = models.CharField(max_length=30)
    ClientType = models.CharField(max_length=30)
    ClientEmployeeId = models.CharField(max_length=30)
    ClientEmployeeDesignation = models.CharField(max_length=30)
    ClientEmployeeRelation = models.CharField(max_length=30)
    EmployeeId = models.ForeignKey(Employee_Personal_Form_Detials,on_delete=models.CASCADE,related_name='Laboratory_appointment_EmployeeId',null=True,blank=True)
    EmployeeRelation = models.CharField(max_length=30)
    DoctorId = models.ForeignKey(Doctor_Personal_Form_Detials,on_delete=models.CASCADE,related_name='Laboratory_appointment_DoctorId',null=True,blank=True)
    DoctorRelation = models.CharField(max_length=30)
    DonationType = models.CharField(max_length=30)
    IsMLC = models.CharField(max_length=20)
    Flagging = models.ForeignKey(Flaggcolor_Detials,on_delete=models.CASCADE,null=True, blank=True)
    IsReferral = models.CharField(max_length=20)
    Status = models.CharField(max_length=20,default='Pending')
    Reason =models.CharField(max_length=200)
    Location =models.ForeignKey(Location_Detials ,on_delete=models.CASCADE)
    created_by = models.CharField(max_length=30)
    updated_by = models.CharField(max_length=30,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Patient_Laboratory_Registration_Detials'
    def save(self, *args, **kwargs):
       

        if not self.Registration_Id:
            hospital_details = Hospital_Detials.objects.first()
            if not hospital_details:
                raise ValueError("No Hospital_Details records found.")
            
            clinic_name = hospital_details.Hospital_Name[:3].upper()
            today_date = datetime.now().strftime('%y%m%d')
            prefix = f'{clinic_name}{today_date}LAB'
            
            # Find the maximum numeric part from existing PatientId with the same prefix
            max_Registration_Id = Patient_Laboratory_Registration_Detials.objects.aggregate(max_id=Max('Registration_Id'))['max_id']
            if max_Registration_Id:
                numeric_part = int(max_Registration_Id[-5:]) + 1
            else:
                numeric_part = 1
            self.Registration_Id = f'{prefix}{numeric_part:05}'
       
        super(Patient_Laboratory_Registration_Detials, self).save(*args, **kwargs)
    
  

class Patient_Admission_Detials(models.Model):
    IsConverted=models.BooleanField(default=False)
    IsCasualityPatient= models.BooleanField(default=False)
    IP_Registration_Id = models.ForeignKey(Patient_IP_Registration_Detials, on_delete=models.CASCADE,null=True,blank=True,default=None)
    OP_Registration_Id = models.ForeignKey(Patient_Appointment_Registration_Detials, on_delete=models.CASCADE,null=True,blank=True,default=None)
    Emergency_Registration_Id = models.ForeignKey(Patient_Emergency_Registration_Detials, on_delete=models.CASCADE,null=True,blank=True,default=None)
    Casuality_Registration_Id = models.ForeignKey(Patient_Casuality_Registration_Detials, on_delete=models.CASCADE,null=True,blank=True,default=None)
    Diagnosis_Registration_Id = models.ForeignKey(Patient_Diagnosis_Registration_Detials,on_delete=models.CASCADE,null=True,blank=True,default=None)
    Laboratory_Registration_Id = models.ForeignKey(Patient_Laboratory_Registration_Detials, on_delete=models.CASCADE,null=True,blank=True,default=None)
    AdmissionPurpose = models.CharField(max_length=30,default='')
    DrInchargeAtTimeOfAdmission = models.ForeignKey(Doctor_Personal_Form_Detials, on_delete=models.CASCADE, null=True,blank=True)
    NextToKinName = models.CharField(max_length=30,null=True,blank=True,)
    Relation = models.CharField(max_length=30,null=True,blank=True,)
    RelativePhoneNo = models.CharField(max_length=30,null=True,blank=True,)
    PersonLiableForPayment = models.CharField(max_length=30,null=True,blank=True,)
    FamilyHead = models.CharField(max_length=30,null=True,blank=True,)
    FamilyHeadName = models.CharField(max_length=30,null=True,blank=True,)
    IpKitGiven = models.CharField(max_length=30,null=True,blank=True,)    
    created_by = models.CharField(max_length=30,null=True,blank=True,)
    updated_by = models.CharField(max_length=30,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Patient_Admission_Detials'
    
  

class Patient_Admission_Room_Detials(models.Model):
    RegisterType= models.CharField(max_length=30)
    IP_Registration_Id = models.ForeignKey(Patient_IP_Registration_Detials, on_delete=models.CASCADE, null=True,blank=True)
    Emergency_Registration_Id = models.ForeignKey(Patient_Emergency_Registration_Detials, on_delete=models.CASCADE, null=True,blank=True)
    Casuality_Registration_Id = models.ForeignKey(Patient_Casuality_Registration_Detials, on_delete=models.CASCADE,null=True,blank=True)
    RoomId =models.ForeignKey(Room_Master_Detials,on_delete=models.CASCADE,null=True,blank=True)
    Admitted_Date = models.DateTimeField(null=True,blank=True,default=None)
    Discharge_Date = models.DateTimeField(null=True,blank=True,default=None)
    Status=models.BooleanField(default=False)
    IsStayed=models.BooleanField(default=False)
    CurrentlyStayed=models.BooleanField(default=False)
    Iscanceled=models.BooleanField(default=False)
    created_by = models.CharField(max_length=30)
    updated_by = models.CharField(max_length=30,default='')
    Approved_by = models.CharField(max_length=30,default='')
    CancelReason=models.TextField(default='')
    PatientfileRecieved=models.BooleanField(default=False)
    MedicineTransfered=models.BooleanField(default=False)
    AnyMedicalRecordError=models.BooleanField(default=False)
    ConfirmationfromReletives=models.BooleanField(default=False)
    ReletiveName=models.CharField(max_length=30,default="")
    MedRecReason=models.TextField(default='')
    bedtransferReason=models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Patient_Admission_Room_Detials'
    def __str__(self):
        return f"{self.RegisterType} - {self.RoomId}"



class Op_to_Ip_Convertion_Table(models.Model):
    id = models.AutoField(primary_key=True)
    Patient_Id = models.ForeignKey(Patient_Detials, on_delete=models.CASCADE)
    Registration_id = models.ForeignKey(Patient_Appointment_Registration_Detials, on_delete=models.CASCADE)
    created_by = models.CharField(max_length=30)
    Reason = models.CharField(max_length=400, default= 'None')
    IpNotes = models.CharField(max_length=400, default= 'None')
    OptoIpCheck = models.BooleanField(default=True)
    Status = models.CharField(max_length=40, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Op_to_Ip_Convertion_Table'




class Patient_Referral_Detials(models.Model):
    ReferralRegisteredBy = models.CharField(max_length=30)
    OP_Register_Id = models.ForeignKey(Patient_Appointment_Registration_Detials,on_delete=models.CASCADE,null=True,blank=True)
    IP_Register_Id = models.ForeignKey(Patient_IP_Registration_Detials,on_delete=models.CASCADE,null=True,blank=True)
    Emergency_Register_Id = models.ForeignKey(Patient_Emergency_Registration_Detials,on_delete=models.CASCADE,null=True,blank=True)
    Casuality_Register_Id = models.ForeignKey(Patient_Casuality_Registration_Detials,on_delete=models.CASCADE,null=True,blank=True)
    Laboratory_Register_Id = models.ForeignKey(Patient_Laboratory_Registration_Detials,on_delete=models.CASCADE,null=True,blank=True)
    Diagnosis_Register_Id = models.ForeignKey(Patient_Diagnosis_Registration_Detials,on_delete=models.CASCADE,null=True,blank=True)
    ReferralSource = models.CharField(max_length=30)
    ReferredBy = models.ForeignKey(Doctor_Personal_Form_Detials,on_delete=models.CASCADE,related_name='referral_doctorname',null=True,blank=True)
    created_by = models.CharField(max_length=30)
    updated_by = models.CharField(max_length=30,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Patient_Referral_Detials'


# -------------------------------ForBilling------------------






class OP_Billing_QueueList_Detials(models.Model):
    BillingQueueList_ID=models.AutoField(primary_key=True)
    Billing_Type=models.CharField(max_length=100)
    Registration_Id=models.ForeignKey(Patient_Appointment_Registration_Detials,on_delete=models.CASCADE,related_name='OP_Billing_QueueList_Registration_Id')
    Doctor_Ratecard_Id=models.ForeignKey(Doctor_Ratecard_Master,on_delete=models.CASCADE,related_name='OP_Billing_Doctor_Ratecard_Id',null=True,blank=True)
    Status=models.CharField(max_length=50)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'OP_Billing_QueueList_Detials'

    def __str__(self):
        return self.Billing_Type
    


class General_Billing_Table_Detials(models.Model):
    Billing_Invoice_No=models.CharField(primary_key=True,max_length=30)
    Billing_Date=models.DateField()
    Doctor_Id=models.ForeignKey(Doctor_Personal_Form_Detials,on_delete=models.CASCADE,related_name='Billing_Doctor_Id')
    Patient_Id=models.ForeignKey(Patient_Detials,on_delete=models.CASCADE,related_name='Billing_Patient_Id')
    Register_Id=models.ForeignKey(Patient_Appointment_Registration_Detials,on_delete=models.CASCADE,related_name='Billing_Patient_Id')
    Visit_Id=models.ForeignKey(Patient_Visit_Detials,on_delete=models.CASCADE,related_name='Billing_Visit_Id')
    Billing_Type=models.CharField(max_length=150)
    Select_Discount=models.CharField(max_length=50)
    Discount_Type=models.CharField(max_length=30)
    Discount_Value=models.DecimalField(max_digits=10, decimal_places=2)
    Discount_Amount=models.DecimalField(max_digits=10, decimal_places=2)
    Total_Items=models.IntegerField()
    Total_Qty=models.IntegerField()
    Total_Amount=models.DecimalField(max_digits=10, decimal_places=2)
    Total_GSTAmount=models.DecimalField(max_digits=10, decimal_places=2)
    Net_Amount=models.DecimalField(max_digits=10, decimal_places=2)
    Round_Off=models.DecimalField(max_digits=10, decimal_places=2)
    Net_Paid_Amount=models.DecimalField(max_digits=10, decimal_places=2)
    Paid_Amount=models.DecimalField(max_digits=10, decimal_places=2)
    Balance_Amount=models.DecimalField(max_digits=10, decimal_places=2)
    Bill_Status=models.CharField(max_length=20)
    Location=models.ForeignKey(Location_Detials,on_delete=models.CASCADE,related_name='Location_id',blank=True, null=True)
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class meta:
        db_table='General_Billing_Table_Detials'

    def save(self, *args, **kwargs):
        if not self.Billing_Invoice_No:
            Add_Invoice_Char = 'OPDR/'
            Max_Invoice_No_row = General_Billing_Table_Detials.objects.exclude(created_by='system').aggregate(max_id=Max('Billing_Invoice_No'))['max_id']
            Max_Invoice_No = Max_Invoice_No_row if Max_Invoice_No_row else None
            numeric_part = int(str(Max_Invoice_No)[5:]) + 1 if Max_Invoice_No else 1
            self.Billing_Invoice_No = f'{Add_Invoice_Char}{numeric_part:04}'
        
        super(General_Billing_Table_Detials, self).save(*args, **kwargs)


class General_Billing_Items_Table_Detials(models.Model):
    Items_Id=models.AutoField(primary_key=True)
    Billing_Invoice_No=models.ForeignKey(General_Billing_Table_Detials,on_delete=models.CASCADE,related_name='Items_Table_Billing_Invoice_No')
    Service_Type=models.CharField(max_length=100)
    Service_Code=models.CharField(max_length=30,null=True)
    Service_Name=models.CharField(max_length=350)
    Rate=models.DecimalField(max_digits=10, decimal_places=2)
    Charge=models.DecimalField(max_digits=10, decimal_places=2)
    Quantity=models.IntegerField()
    Amount=models.DecimalField(max_digits=10, decimal_places=2)
    Discount_Type=models.CharField(max_length=30,null=True,blank=True)
    Discount_Value=models.DecimalField(max_digits=10, decimal_places=2)
    Discount_Amount=models.DecimalField(max_digits=10, decimal_places=2,null=True)
    Taxable_Amount=models.DecimalField(max_digits=10,decimal_places=2)
    # Tax_Percentage=models.IntegerField()
    Tax_Amount=models.DecimalField(max_digits=10,decimal_places=2)
    Total_Amount=models.DecimalField(max_digits=10,decimal_places=2)
    Item_Status=models.CharField(max_length=30)

    class Meta:
        db_table = 'General_Billing_Items_Table_Detials'

    def __str__(self):
        return self.Service_Name


class Multiple_Payment_Table_Detials(models.Model):
    S_No=models.AutoField(primary_key=True)
    Invoice_No_Paid = models.CharField(max_length=30)
    Payment_Type=models.CharField(max_length=70)
    Cart_Type=models.CharField(max_length=30)
    Card_No = models.CharField(max_length=4,default=0000)
    TransactionId = models.CharField(max_length=50,default='')
    upiid = models.CharField(max_length=50,default='')
    Cheque_No=models.CharField(max_length=20)
    Bank_Name=models.CharField(max_length=50)
    Transaction_Amount = models.DecimalField(max_digits=10,decimal_places=2)
    AdditionalAmount = models.DecimalField(max_digits=10,decimal_places=2)
    Amount=models.DecimalField(max_digits=10,decimal_places=2)

    class Meta:
        db_table = 'Multiple_Payment_Table_Detials'

    def __str__(self):
        return self.Payment_Type



class GeneralBillingReceipt(models.Model):
    Invoice_NO = models.ForeignKey(
        General_Billing_Table_Detials, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        related_name='Receipt_invoice') 
    PatientID = models.CharField(max_length=50)
    PhoneNumber = models.CharField(max_length=50)
    Patient_Name = models.CharField(max_length=50)
    TotalAmount = models.CharField(max_length=50)
    TotalPaidAmount = models.CharField(max_length=50)
    BalanceAmount = models.CharField(max_length=50)
    Billing_Date = models.DateField()
    Voucher_Number = models.CharField(max_length=50, blank=True, null=True)  # This will be auto-incremented
    PaidAmount = models.CharField(max_length=50)
    Billedby = models.CharField(max_length=50)
    UpdatedAt = models.DateTimeField(auto_now=True)  # Automatically updates the timestamp when the row is updated
    CreatedAt = models.DateTimeField(auto_now_add=True)  # Sets the timestamp when the row is created

    class Meta:
        db_table = 'General_Billing_Receipt_Table'

    def save(self, *args, **kwargs):
        if not self.Voucher_Number:
            # Find the last voucher number for the given invoice number
            last_receipt = GeneralBillingReceipt.objects.filter(Invoice_NO=self.Invoice_NO).order_by('-id').first()

            if last_receipt and last_receipt.Voucher_Number:
                # Increment the last voucher number
                last_voucher_number = int(last_receipt.Voucher_Number.split('-')[-1])
                self.Voucher_Number = f"{self.Invoice_NO.Billing_Invoice_No}-{last_voucher_number + 1}"
            else:
                # If no previous voucher exists, start with 1
                self.Voucher_Number = f"{self.Invoice_NO.Billing_Invoice_No}-1"

        super().save(*args, **kwargs)



class Advanceamounttable(models.Model):
    adInvoice_NO = models.CharField(primary_key=True,max_length=30)
    Patient_Id=models.ForeignKey(Patient_Detials,on_delete=models.CASCADE,related_name='Advance_Patient_Id')
    Register_Id=models.ForeignKey(Patient_Appointment_Registration_Detials,on_delete=models.CASCADE,related_name='Advance_Patient_Id')
    Visit_Id=models.ForeignKey(Patient_Visit_Detials,on_delete=models.CASCADE,related_name='Advance_Visit_Id')
    Billing_Date=models.DateField()
    Billing_Type=models.CharField(max_length=150)
    Department=models.CharField(max_length=50)
    Amount=models.DecimalField(max_digits=10,decimal_places=2)
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    Locations=models.CharField(max_length=100,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Advanceamounttable'

    def save(self, *args, **kwargs):
        if not self.adInvoice_NO:
            Add_Invoice_Char = 'ADV/'
            Max_Invoice_No_row = Advanceamounttable.objects.exclude(created_by='system').aggregate(max_id=Max('adInvoice_NO'))['max_id']
            Max_Invoice_No = Max_Invoice_No_row if Max_Invoice_No_row else None
            numeric_part = int(str(Max_Invoice_No)[5:]) + 1 if Max_Invoice_No else 1
            self.adInvoice_NO = f'{Add_Invoice_Char}{numeric_part:04}'
        
        super(Advanceamounttable, self).save(*args, **kwargs)

class advancemaintaintable(models.Model):
    adInvoice_NO = models.ForeignKey(Advanceamounttable,on_delete=models.CASCADE,related_name='advmaintaininv')
    Patient_Id=models.ForeignKey(Patient_Detials,on_delete=models.CASCADE,related_name='Advmaintain_Patient_Id')
    Register_Id=models.ForeignKey(Patient_Appointment_Registration_Detials,on_delete=models.CASCADE,related_name='Advmaintain_Patient_Id')
    Visit_Id=models.ForeignKey(Patient_Visit_Detials,on_delete=models.CASCADE,related_name='Advmaintain_Visit_Id')
    Billing_Date=models.DateField()
    Billing_Type=models.CharField(max_length=150)
    Department=models.CharField(max_length=50)
    fullAmount=models.DecimalField(max_digits=10,decimal_places=2)
    paidamount=models.DecimalField(max_digits=10,decimal_places=2)
    Remaining_amount=models.DecimalField(max_digits=10,decimal_places=2)
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    Locations=models.CharField(max_length=100,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'advancemaintaintable'

       

       


class Handover_detials_Ip(models.Model):
    RegistrationId=models.ForeignKey(Patient_IP_Registration_Detials,on_delete=models.CASCADE,related_name='Handover_Ip_register')
    ReasonForAdmission=models.TextField()
    PatientConditionOnAdmission=models.TextField()
    PatientFileGiven=models.BooleanField(default=False)
    AadharGiven=models.BooleanField(default=False)
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Handover_detials_Ip'


class Service_Procedure_request_Ip(models.Model):
    MASTER_TYPE_CHOICES = [
        ('Service', 'Service'),
        ('Procedure', 'Procedure'),
    ]

    MasterType = models.CharField(max_length=10, choices=MASTER_TYPE_CHOICES)
    Service_ratecard = models.ForeignKey(Service_Master_Details, on_delete=models.CASCADE, related_name='Service_charges_ip', null=True, blank=True,default=None)
    Procedure_ratecard = models.ForeignKey(Procedure_Master_Details, on_delete=models.CASCADE, related_name='Procedure_charges_ip', null=True, blank=True,default=None)
    RegistrationId=models.ForeignKey(Patient_IP_Registration_Detials,on_delete=models.CASCADE,related_name='Service_Procedure_request_Ip')
    RoomId =models.ForeignKey(Room_Master_Detials,on_delete=models.CASCADE,related_name='RoomId_service_procedure',null=True,blank=True)
    Units = models.DecimalField(max_digits=10,decimal_places=2)
    Status = models.BooleanField(default=False)
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Service_Procedure_request_Ip' 

   
        
class OPD_Flow(models.Model):
    OPD_Id = models.AutoField(primary_key=True)
    Patient_Id = models.ForeignKey(Patient_Detials,on_delete=models.CASCADE,null=True,blank=True)
    Specialization = models.ForeignKey(Speciality_Detials,on_delete=models.CASCADE,null=True,blank=True)
    DoctorId = models.ForeignKey(Doctor_Personal_Form_Detials,on_delete=models.CASCADE,related_name='registration_doctor_name',null=True,blank=True)
    RegisterType = models.CharField(max_length=30)
    Registration_Id = models.ForeignKey(Patient_Appointment_Registration_Detials,on_delete=models.CASCADE,null=True,blank=True)
    Registration_Cancel_Reason = models.TextField(default='')
    Appointment_Cancel_Reason = models.TextField(default='')
    Appointment_Reschedule_Reason = models.TextField(default='')
    RegistrationReshedule_Reason = models.TextField(default='')
    AppointmentDoctor = models.ForeignKey(Doctor_Personal_Form_Detials,on_delete=models.CASCADE,related_name='appointment_previous_doctor_name',null=True,blank=True)
    Registration_Status = models.CharField(max_length=40, default='Pending')
    AppointmentType = models.CharField(max_length=40)
    Appointment_Id = models.ForeignKey(Appointment_Request_List,on_delete=models.CASCADE,null=True,blank=True)
    Appointment_Status = models.CharField(max_length=40, default='Pending')
    created_by = models.CharField(max_length=40)
    updated_by = models.CharField(max_length=30,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'OPD_Flow'
    
    def save(self, *args, **kwargs):
        if not self.OPD_Id:
            max_id_dict = OPD_Flow.objects.aggregate(max_id=Max('OPD_Id'))
            max_id = max_id_dict.get('max_id', 0)  # Extract max_id from the dict
            self.OPD_Id = (max_id or 0) + 1
        super(OPD_Flow, self).save(*args, **kwargs)

        
# class Appointment_to_Registration(models.Model):
#     ApptoRegId = models.AutoField(primary_key=True)
#     Appointment_Id = models.ForeignKey(Appointment_Request_List,on_delete=models.CASCADE,null=True,blank=True)
#     Registration_Id = models.ForeignKey(Patient_Appointment_Registration_Detials,on_delete=models.CASCADE,null=True,blank=True)
#     created_by = models.CharField(max_length=40)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     class Meta:
#         db_table = 'Appointment_to_Registration'
#     def save(self, *args, **kwargs):
#         if not self.ApptoRegId:
#             max_id_dict = Appointment_to_Registration.objects.aggregate(max_id=Max('ApptoRegId'))
#             max_id = max_id_dict.get('max_id', 0)  # Extract max_id from the dict
#             self.ApptoRegId = (max_id or 0) + 1
#         super(Appointment_to_Registration, self).save(*args,**kwargs)
    


class Patient_Appointment_Registration_Cancel_Details(models.Model):
    Cancel_Id = models.IntegerField(primary_key=True)
    Registration_Id = models.ForeignKey(
        Patient_Appointment_Registration_Detials, 
        on_delete=models.CASCADE, 
        related_name='cancel_registration_details'
    )
    Cancel_Reason = models.TextField()
    Status = models.CharField(max_length=30, default = 'Cancelled')
    created_by = models.CharField(max_length=30)
    updated_by = models.CharField(max_length=30,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'Patient_Appointment_Registration_Cancel_Details'
        
    def save(self, *args, **kwargs):
        if not self.Cancel_Id:
            max_id = Patient_Appointment_Registration_Cancel_Details.objects.aggregate(
                max_id=Max('Cancel_Id')
            )['max_id']
            self.Cancel_Id = (max_id or 0) + 1
        super().save(*args, **kwargs)
    
        
class Patient_Registration_Reshedule_Details(models.Model):
    Reshedule_Id = models.IntegerField(primary_key=True)
    Registration_Id = models.ForeignKey(
        'Patient_Appointment_Registration_Detials', 
        on_delete=models.CASCADE, 
        related_name='reshedule_registration_details'
    )
    ChangingReason = models.TextField(default='')
    specialization = models.ForeignKey(Speciality_Detials, on_delete=models.CASCADE,related_name='registration_reschedule_list_specialization',null=True,blank=True)
    doctor_name = models.ForeignKey(Doctor_Personal_Form_Detials, on_delete=models.CASCADE,related_name='registration_reschedule_list_doctor_name',null=True,blank=True)
    AppointmentDoctor = models.ForeignKey(Doctor_Personal_Form_Detials, on_delete=models.CASCADE,related_name='registration_reschedule_previous_doctor',null=True,blank=True)
    Status = models.CharField(max_length=30, default = 'Pending')
    created_by = models.CharField(max_length=30)
    updated_by = models.CharField(max_length=30,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
    class Meta:
        db_table = 'Patient_Registration_Reshedule_Details'
    
    def save(self, *args, **kwargs):
        if not self.Reshedule_Id:
            max_id = Patient_Registration_Reshedule_Details.objects.aggregate(
                max_id=Max('Reshedule_Id')
            )['max_id']
            self.Reshedule_Id = (max_id or 0) + 1
        super().save(*args,**kwargs)


# -------------------------------ForBilling------------------

class IP_Billing_QueueList_Detials(models.Model):
    BillingQueueList_ID=models.AutoField(primary_key=True)
    Billing_Type=models.CharField(max_length=100)
    Registration_Id=models.ForeignKey(Patient_IP_Registration_Detials,on_delete=models.CASCADE,related_name='IP_Billing_Registration_Id')
    Doctor_Ratecard_Id=models.ForeignKey(Doctor_Ratecard_Master,on_delete=models.CASCADE,related_name='IP_Billing_Queue_Doctor_Ratecard_Id',null=True)
    Status=models.CharField(max_length=50)
    created_by = models.CharField(max_length=30)
    updated_by = models.CharField(max_length=30,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'IP_Billing_QueueList_Detials'

    def __str__(self):
        return self.Billing_Type
    
class IP_Billing_Add_Services(models.Model):
    BillingDataList_ID = models.ForeignKey(IP_Billing_QueueList_Detials,on_delete= models.CASCADE)
    Service_Type = models.CharField(max_length=30)
    Service_Name = models.CharField(max_length=30)
    Service_Code = models.CharField(max_length=30)
    Charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Quantity = models.IntegerField()
    Amount = models.IntegerField()
    Discount_Type = models.CharField(max_length=30)
    Discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Taxable_Amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    GST_Charge = models.CharField(max_length=30)
    NetAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Location =models.ForeignKey(Location_Detials ,on_delete=models.CASCADE,default="",null=True)
    created_by = models.CharField(max_length=30)
    updated_by = models.CharField(max_length=30,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class IP_Billing_Table_Detials(models.Model):
    Billing_Invoice_No=models.CharField(primary_key=True,max_length=30)
    Billing_Date=models.DateField()
    Doctor_Id=models.ForeignKey(Doctor_Personal_Form_Detials,on_delete=models.CASCADE,related_name='IP_Billing_Doctor_Id')
    Patient_Id=models.ForeignKey(Patient_Detials,on_delete=models.CASCADE,related_name='IP_Billing_Patient_Id')
    Register_Id=models.ForeignKey(Patient_IP_Registration_Detials,on_delete=models.CASCADE,related_name='IP_Billing_Patient_Id')
    # Visit_Id=models.ForeignKey(Patient_Visit_Detials,on_delete=models.CASCADE,related_name='IP_Billing_Visit_Id')
    Billing_Type=models.CharField(max_length=150)
    Select_Discount=models.CharField(max_length=50)
    Discount_Type=models.CharField(max_length=30)
    Discount_Value=models.DecimalField(max_digits=10, decimal_places=2)
    Discount_Amount=models.DecimalField(max_digits=10, decimal_places=2)
    Total_Items=models.IntegerField()
    Total_Qty=models.IntegerField()
    Total_Amount=models.DecimalField(max_digits=10, decimal_places=2)
    Total_GSTAmount=models.DecimalField(max_digits=10, decimal_places=2)
    Net_Amount=models.DecimalField(max_digits=10, decimal_places=2)
    Round_Off=models.DecimalField(max_digits=10, decimal_places=2)
    Net_Paid_Amount=models.DecimalField(max_digits=10, decimal_places=2)
    Paid_Amount=models.DecimalField(max_digits=10, decimal_places=2)
    Balance_Amount=models.DecimalField(max_digits=10, decimal_places=2)
    Bill_Status=models.CharField(max_length=20)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=30,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class meta:
        db_table='IP_Billing_Table_Detials'

    def save(self, *args, **kwargs):
        if not self.Billing_Invoice_No:
            Add_Invoice_Char = 'IPDR/'
            Max_Invoice_No_row = IP_Billing_Table_Detials.objects.exclude(created_by='system').aggregate(max_id=Max('Billing_Invoice_No'))['max_id']
            Max_Invoice_No = Max_Invoice_No_row if Max_Invoice_No_row else None
            numeric_part = int(str(Max_Invoice_No)[5:]) + 1 if Max_Invoice_No else 1
            self.Billing_Invoice_No = f'{Add_Invoice_Char}{numeric_part:04}'
        
        super(IP_Billing_Table_Detials, self).save(*args, **kwargs)



class IP_Billing_Items_Table_Detials(models.Model):
    Items_Id=models.AutoField(primary_key=True)
    Billing_Invoice_No=models.ForeignKey(IP_Billing_Table_Detials,on_delete=models.CASCADE,related_name='Items_Table_IP_Billing_Invoice_No')
    Service_Type=models.CharField(max_length=100)
    Service_Name=models.CharField(max_length=350)
    Rate=models.DecimalField(max_digits=10, decimal_places=2)
    Charge=models.DecimalField(max_digits=10, decimal_places=2)
    Quantity=models.CharField(max_length=30, default="")
    Amount=models.DecimalField(max_digits=10, decimal_places=2)
    Discount_Type=models.CharField(max_length=30, null=True,blank=True)
    Discount_Value=models.DecimalField(max_digits=10, decimal_places=2)
    Discount_Amount=models.DecimalField(max_digits=10, decimal_places=2)
    Taxable_Amount=models.DecimalField(max_digits=10,decimal_places=2)
    Tax_Percentage=models.IntegerField()
    Tax_Amount=models.DecimalField(max_digits=10,decimal_places=2)
    Total_Amount=models.DecimalField(max_digits=10,decimal_places=2)
    Item_Status=models.CharField(max_length=30)

    class Meta:
        db_table = 'IP_Billing_Items_Table_Detials'

    def __str__(self):
        return self.Service_Name


class Multiple_Payment_Table_IP_Detials(models.Model):
    S_No=models.AutoField(primary_key=True)
    Invoice_No=models.ForeignKey(IP_Billing_Table_Detials,on_delete=models.CASCADE,related_name='Multiple_Payment_IP_Billing_Invoice')
    Payment_Type=models.CharField(max_length=70)
    Cart_Type=models.CharField(max_length=30)
    Card_No = models.CharField(max_length=4,default=0000,null=True,blank=True)
    TransactionId = models.CharField(max_length=50,default='',null=True,blank=True)
    upiid = models.CharField(max_length=50,default='',null=True,blank=True)
    Cheque_No=models.CharField(max_length=20)
    Bank_Name=models.CharField(max_length=50)
    Transaction_Amount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    AdditionalAmount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    Amount=models.DecimalField(max_digits=10,decimal_places=2)

    class Meta:
        db_table = 'Multiple_Payment_Table_IP_Detials'

    def __str__(self):
        return self.Payment_Type
   


class Patient_Client_Insurance_details(models.Model):
    Patient_Id = models.ForeignKey(Patient_Detials,on_delete= models.CASCADE,null=True,blank=True)
    isClient = models.CharField(max_length=30)
    CoPaymentType = models.CharField(max_length=30)
    CoPaymentTypeinp = models.CharField(max_length=30)
    CoPaymentLogic = models.CharField(max_length=30)
    CoPaymentdeducted = models.CharField(max_length=30)
    PreAuthType = models.CharField(max_length=30)
    PreAuthTypeinp = models.CharField(max_length=30)
    PreAuthAmount = models.CharField(max_length=30)
    PreAuthApprovalNo = models.CharField(max_length=30)
    PolicyNo = models.CharField(max_length=30)
    PolicyStartDate = models.DateField()
    PolicyEndDate = models.DateField()
    Location = models.ForeignKey(Location_Detials,on_delete= models.CASCADE,null=True,blank=True)
    created_by = models.CharField(max_length=30)
    updated_by = models.CharField(max_length=30,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'Patient_Client_Insurance_details'


class Advance_Collection_IP(models.Model):
    RegistrationId = models.ForeignKey(Patient_IP_Registration_Detials,on_delete=models.CASCADE,null=True,blank=True)
    AdvanceAmount = models.DecimalField(max_digits=10,decimal_places=2)
    created_by = models.CharField(max_length=30)
    updated_by = models.CharField(max_length=30,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Services_SubCat_Requests_Details(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    Registration_Id = models.ForeignKey(Patient_IP_Registration_Detials, on_delete=models.CASCADE, to_field='Registration_Id')
    service_category = models.ForeignKey(Service_Category_Masters, on_delete=models.CASCADE)
    service_sub_category = GenericForeignKey('content_type', 'object_id')
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    units = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Services_SubCat_Requests_Details'




class ABHA_Collectin_Data(models.Model):
    ABHA_RegID = models.IntegerField(primary_key=True)
    
    ABHANumber = models.CharField(max_length=20)
    preferredAbhaAddress = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    address = models.TextField()
    createdDate = models.DateField()
    
    dayOfBirth = models.DateField()
    
    districtName = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    gender = models.CharField(max_length=1)
    pincode = models.CharField(max_length=255,null=True,blank=True)
    mobile=models.CharField(max_length=255,null=True,blank=True)
    mobileVerified = models.BooleanField()
    stateName = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    subdistrictName = models.CharField(max_length=100)
    townName = models.CharField(max_length=100)
    verificationType = models.CharField(max_length=20)
    
    
    class Meta:
        db_table = 'ABHA_Collectin_Data'
    
    def save(self, *args, **kwargs):
        if not self.ABHA_RegID:
            max_id = ABHA_Collectin_Data.objects.aggregate(
                max_id=Max('ABHA_RegID')
            )['max_id']
            self.ABHA_RegID = (max_id or 0) + 1
        super().save(*args, **kwargs)
    
class Theatre_Booking_Request_Details(models.Model):
    
    Booking_Id = models.CharField(primary_key=True,max_length=30)
    ReqDate = models.DateField()
    ReqTime = models.TimeField()
    BookingType = models.CharField(max_length=255,null=True,blank=True)
    Specialization = models.ForeignKey(Speciality_Detials,on_delete=models.CASCADE,null=True,blank=True)
    SurgeryName = models.ForeignKey(SurgeryName_Details,on_delete=models.CASCADE,null=True,blank=True)
    TheatreName = models.ForeignKey(OtTheaterMaster_Detials,on_delete=models.CASCADE,null=True,blank=True)
    DoctorName = models.ForeignKey(Doctor_Personal_Form_Detials,on_delete=models.CASCADE,null=True,blank=True)
    OP_Registration_Id = models.ForeignKey(Patient_Appointment_Registration_Detials,on_delete=models.CASCADE,related_name='OP_otrequest',null=True,blank=True)
    IP_Registration_Id = models.ForeignKey(Patient_IP_Registration_Detials,on_delete=models.CASCADE,related_name='IP_otrequest',null=True,blank=True)
    EMR_Registration_Id = models.ForeignKey(Patient_Emergency_Registration_Detials,on_delete=models.CASCADE,related_name='EMR_otrequest',null=True,blank=True) 
    BookingDate = models.DateField()
    BookingTime = models.TimeField()
    Duration = models.CharField(max_length=255,null=True,blank=True)
    OperationType = models.CharField(max_length=255,null=True,blank=True)
    Priority = models.CharField(max_length=255,null=True,blank=True)
    PatientName = models.CharField(max_length=255,null=True,blank=True)
    Patientid = models.ForeignKey(Patient_Detials,on_delete=models.CASCADE,null=True,blank=True)
    Age = models.CharField(max_length=255,null=True,blank=True)
    Gender = models.CharField(max_length=255,null=True,blank=True)
    UHIDNO = models.CharField(max_length=255,null=True,blank=True)
    Status = models.CharField(max_length=255,null=True,blank=True)
    Reason = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    CreatedBy = models.CharField(max_length=50)
       

    class Meta:
         db_table = 'Theatre_Booking_Request_Details'

    def save(self, *args, **kwargs):
        if not self.Booking_Id:
            hospital_details = Hospital_Detials.objects.first()
            if not hospital_details:
                raise ValueError("No Hospital_Details records found.")
            
            clinic_name = hospital_details.Hospital_Name[:3].upper()
            today_date = datetime.now().strftime('%y%m%d')
            prefix = f'{clinic_name}{today_date}OT'
            
            # Find the maximum numeric part from existing PatientId with the same prefix
            max_Booking_Id = Theatre_Booking_Request_Details.objects.aggregate(max_id=Max('Booking_Id'))['max_id']
            if max_Booking_Id:
                numeric_part = int(max_Booking_Id[-5:]) + 1
            else:
                numeric_part = 1
            self.Booking_Id = f'{prefix}{numeric_part:05}'
       
        super(Theatre_Booking_Request_Details, self).save(*args, **kwargs)
 
class OTTheatrecalendar(models.Model):

    Theatre = models.ForeignKey(OtTheaterMaster_Detials,on_delete=models.CASCADE,null=True,blank=True)
    booking = models.ForeignKey(Theatre_Booking_Request_Details,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField()
    time = models.TimeField()
    Status = models.CharField(max_length=255,default='Booked')

    class Meta:
        db_table = 'OTTheatrecalendar'

class OTDoctorcalendar(models.Model):

    Theatre = models.ForeignKey(OtTheaterMaster_Detials,on_delete=models.CASCADE,null=True,blank=True)
    booking = models.ForeignKey(Theatre_Booking_Request_Details,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField()
    time = models.TimeField()
    Status = models.CharField(max_length=255,default='Booked')
    Doctorid = models.ForeignKey(Doctor_Personal_Form_Detials,on_delete=models.CASCADE,null=True,blank=True)

    class Meta:
        db_table = 'OTDoctorcalendar'

class OTConsumable_Details(models.Model):

    Category = models.ForeignKey(Product_Category_Product_Details,on_delete=models.CASCADE,null=True,blank=True)
    Subcategory = models.ForeignKey(SubCategory_Detailes,on_delete=models.CASCADE,null=True,blank=True)
    Store = models.ForeignKey(Inventory_Location_Master_Detials,on_delete=models.CASCADE,null=True,blank=True)
    Product = models.ForeignKey(Stock_Maintance_Table_Detials,on_delete=models.CASCADE,null=True,blank=True)
    OP_Registration_Id= models.ForeignKey(Patient_Appointment_Registration_Detials,on_delete=models.CASCADE,related_name='OP_otconsumable',null=True,blank=True)
    IP_Registration_Id = models.ForeignKey(Patient_IP_Registration_Detials,on_delete=models.CASCADE,related_name='IP_otconsumable',null=True,blank=True)
    EMR_Registration_Id = models.ForeignKey(Patient_Emergency_Registration_Detials,on_delete=models.CASCADE,related_name='EMR_otconsumable',null=True,blank=True)
    Patientid = models.ForeignKey(Patient_Detials,on_delete=models.CASCADE,null=True,blank=True) 
    BookingType = models.CharField(max_length=255,null=True,blank=True)
    Quantity = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    CreatedBy = models.CharField(max_length=50)

    class Meta:
         db_table = 'OTConsumable_Details'

class OTConsignment_Details(models.Model):

    Consignment = models.CharField(max_length=255,null=True,blank=True)
    Quantity = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    CreatedBy = models.CharField(max_length=50)
    BookingType = models.CharField(max_length=255,null=True,blank=True)
    Patientid = models.ForeignKey(Patient_Detials,on_delete=models.CASCADE,null=True,blank=True) 
    OP_Registration_Id = models.ForeignKey(Patient_Appointment_Registration_Detials,on_delete=models.CASCADE,related_name='OP_otconsignment',null=True,blank=True)
    IP_Registration_Id = models.ForeignKey(Patient_IP_Registration_Detials,on_delete=models.CASCADE,related_name='IP_otconsignment',null=True,blank=True)
    EMR_Registration_Id = models.ForeignKey(Patient_Emergency_Registration_Detials,on_delete=models.CASCADE,related_name='EMR_otconsignment',null=True,blank=True)  

    class Meta:
         db_table = 'OTConsignment_Details'

class OTEquipment_Details(models.Model):

    Equipment = models.CharField(max_length=255,null=True,blank=True)
    Quantity = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    CreatedBy = models.CharField(max_length=50)
    BookingType = models.CharField(max_length=255,null=True,blank=True)
    Patientid = models.ForeignKey(Patient_Detials,on_delete=models.CASCADE,null=True,blank=True) 
    OP_Registration_Id = models.ForeignKey(Patient_Appointment_Registration_Detials,on_delete=models.CASCADE,related_name='OP_otequipment',null=True,blank=True)
    IP_Registration_Id = models.ForeignKey(Patient_IP_Registration_Detials,on_delete=models.CASCADE,related_name='IP_otequipment',null=True,blank=True)
    EMR_Registration_Id = models.ForeignKey(Patient_Emergency_Registration_Detials,on_delete=models.CASCADE,related_name='EMR_otequipment',null=True,blank=True) 

    class Meta:
         db_table = 'OTEquipment_Details'

class Surgical_Team_Details(models.Model):

    Surgeon = models.ManyToManyField(Doctor_Personal_Form_Detials,related_name='surgeon_teams',blank=True)
    Assistant_Surgeon = models.ManyToManyField(Doctor_Personal_Form_Detials,related_name='assistant_surgeon_teams',blank=True)
    Anaesthesiologist = models.ManyToManyField(Doctor_Personal_Form_Detials,related_name='anaesthesiologist_teams',blank=True)
    Scrub_Nurse = models.ManyToManyField(Employee_Personal_Form_Detials,related_name='scrub_nurse_teams',blank=True)
    Circulating_Nurse = models.ManyToManyField(Employee_Personal_Form_Detials,related_name='circulating_nurse_teams',blank=True)
    Technician = models.ManyToManyField(Employee_Personal_Form_Detials,related_name='technician_teams',blank=True)
    Helper = models.ManyToManyField(Employee_Personal_Form_Detials,related_name='helper_teams',blank=True)
    Patientid = models.ForeignKey(Patient_Detials,on_delete=models.CASCADE,null=True,blank=True) 
    OP_Registration_Id = models.ForeignKey(Patient_Appointment_Registration_Detials,on_delete=models.CASCADE,related_name='OP_otcrew',null=True,blank=True)
    IP_Registration_Id = models.ForeignKey(Patient_IP_Registration_Detials,on_delete=models.CASCADE,related_name='IP_otcrew',null=True,blank=True)
    EMR_Registration_Id = models.ForeignKey(Patient_Emergency_Registration_Detials,on_delete=models.CASCADE,related_name='EMR_otcrew',null=True,blank=True)  
    BookingType = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    CreatedBy = models.CharField(max_length=50)

    class Meta:
         db_table = 'Surgical_Team_Details'

class OT_Billing(models.Model):

    Service_name = models.CharField(max_length=255,null=True,blank=True)
    Name = models.CharField(max_length=255,null=True,blank=True)
    Per_hr_unit_cost = models.CharField(max_length=255,null=True,blank=True)
    Quantity = models.CharField(max_length=255,null=True,blank=True)
    Amount = models.CharField(max_length=255,null=True,blank=True)
    OP_Registration_Id = models.ForeignKey(Patient_Appointment_Registration_Detials,on_delete=models.CASCADE,related_name='OP_otbill',null=True,blank=True)
    IP_Registration_Id = models.ForeignKey(Patient_IP_Registration_Detials,on_delete=models.CASCADE,related_name='IP_otbill',null=True,blank=True)
    EMR_Registration_Id = models.ForeignKey(Patient_Emergency_Registration_Detials,on_delete=models.CASCADE,related_name='EMR_otbill',null=True,blank=True) 

    class Meta:
         db_table = 'OT_Billing'


class Radiology_Billing_Table_Detials(models.Model):
    Billing_Invoice_No=models.CharField(primary_key=True,max_length=30)
    Billing_Date=models.DateField()
    Doctor_Id=models.ForeignKey(Doctor_Personal_Form_Detials,on_delete=models.CASCADE,related_name='Radiology_Billing_Doctor_Id',null=True,blank=True)
    Patient_Id=models.ForeignKey(Patient_Detials,on_delete=models.CASCADE,related_name='Radiology_Billing_Patient_Id',null=True,blank=True)
    OP_Register_Id=models.ForeignKey(Patient_Appointment_Registration_Detials,on_delete=models.CASCADE,related_name='Radiology_Billing_OP_Patient_Id',null=True,blank=True)
    IP_Register_Id = models.ForeignKey(Patient_IP_Registration_Detials,on_delete=models.CASCADE,related_name='Radiology_Billing_IP_Patient_Id',null=True,blank=True)
    Billing_Type=models.CharField(max_length=150,null=True,blank=True)
    Select_Discount=models.CharField(max_length=50)
    Discount_Type=models.CharField(max_length=30)
    Discount_Value=models.DecimalField(max_digits=10, decimal_places=2)
    Discount_Amount=models.DecimalField(max_digits=10, decimal_places=2)
    Total_Items=models.IntegerField()
    Total_Qty=models.IntegerField()
    Total_Amount=models.DecimalField(max_digits=10, decimal_places=2)
    Total_GSTAmount=models.DecimalField(max_digits=10, decimal_places=2)
    Net_Amount=models.DecimalField(max_digits=10, decimal_places=2)
    Round_Off=models.DecimalField(max_digits=10, decimal_places=2)
    Net_Paid_Amount=models.DecimalField(max_digits=10, decimal_places=2)
    Paid_Amount=models.DecimalField(max_digits=10, decimal_places=2)
    Balance_Amount=models.DecimalField(max_digits=10, decimal_places=2)
    Bill_Status=models.CharField(max_length=20)
    Location=models.ForeignKey(Location_Detials,on_delete=models.CASCADE,related_name='Radiology_Location_id',blank=True, null=True)
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class meta:
        db_table='Radiology_Billing_Table_Detials'

    def save(self, *args, **kwargs):
        if not self.Billing_Invoice_No:
            Add_Invoice_Char = 'RADR/'
            Max_Invoice_No_row = Radiology_Billing_Table_Detials.objects.exclude(created_by='system').aggregate(max_id=Max('Billing_Invoice_No'))['max_id']
            Max_Invoice_No = Max_Invoice_No_row if Max_Invoice_No_row else None
            numeric_part = int(str(Max_Invoice_No)[5:]) + 1 if Max_Invoice_No else 1
            self.Billing_Invoice_No = f'{Add_Invoice_Char}{numeric_part:04}'
        
        super(Radiology_Billing_Table_Detials, self).save(*args, **kwargs)

class Radiology_Billing_Items_Table_Detials(models.Model):
    Items_Id=models.AutoField(primary_key=True)
    Billing_Invoice_No=models.ForeignKey(Radiology_Billing_Table_Detials,on_delete=models.CASCADE,related_name='Radiology_Items_Table_Billing_Invoice_No')
    Service_Type = models.CharField(max_length=100)
    Service_Code=models.CharField(max_length=30,null=True)
    Service_Name = models.CharField(max_length=30,null=True)
    Rate=models.DecimalField(max_digits=10, decimal_places=2)
    Charge=models.DecimalField(max_digits=10, decimal_places=2)
    Quantity=models.IntegerField()
    Amount=models.DecimalField(max_digits=10, decimal_places=2)
    Discount_Type=models.CharField(max_length=30,null=True,blank=True)
    Discount_Value=models.DecimalField(max_digits=10, decimal_places=2)
    Discount_Amount=models.DecimalField(max_digits=10, decimal_places=2,null=True)
    Taxable_Amount=models.DecimalField(max_digits=10,decimal_places=2)
    Tax_Percentage=models.IntegerField(null=True,blank=True)
    Tax_Amount=models.DecimalField(max_digits=10,decimal_places=2)
    Total_Amount=models.DecimalField(max_digits=10,decimal_places=2)
    Item_Status=models.CharField(max_length=30)

    class Meta:
        db_table = 'Radiology_Billing_Items_Table_Detials'

    def __str__(self):
        return self.Service_Name

class Multiple_Payment_Radiology_Table_Detials(models.Model):
    S_No=models.AutoField(primary_key=True)
    Invoice_No_Paid = models.CharField(max_length=30)
    Payment_Type=models.CharField(max_length=70)
    Cart_Type=models.CharField(max_length=30)
    Card_No = models.CharField(max_length=4,default=0000)
    TransactionId = models.CharField(max_length=50,default='')
    upiid = models.CharField(max_length=50,default='')
    Cheque_No=models.CharField(max_length=20)
    Bank_Name=models.CharField(max_length=50)
    Transaction_Amount = models.DecimalField(max_digits=10,decimal_places=2)
    AdditionalAmount = models.DecimalField(max_digits=10,decimal_places=2)
    Amount=models.DecimalField(max_digits=10,decimal_places=2)

    class Meta:
        db_table = 'Multiple_Payment_Radiology_Table_Detials'

    def __str__(self):
        return self.Payment_Type
    
                