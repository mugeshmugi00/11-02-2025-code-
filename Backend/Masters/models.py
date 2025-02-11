# models.py
from django.db import models
from django.db.models import Max
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from datetime import datetime
from Inventory.models import *
from django.contrib.contenttypes.models import ContentType
#   Locations\

class LongTextField(models.TextField):
    def db_type(self, connection):
        if connection.vendor == 'mysql':
            return 'LONGTEXT'
        return super().db_type(connection)

 
class Location_Detials(models.Model):
    Location_Id = models.AutoField(primary_key=True)
    Location_Name = models.CharField(max_length=30)
    Bed_Count = models.IntegerField()
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Location_Detials'

    
class Hospital_Detials(models.Model):
    Hospital_Id = models.AutoField(primary_key=True)
    Hospital_Name = models.CharField(max_length=30)
    Hospital_Logo = models.BinaryField()
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Hospital_Detials'
        
    def clean(self):
        super().clean()
        errors = []

        # Validate length of all CharField fields
        char_fields = ['Hospital_Name', 'created_by']
        for field in char_fields:
            value = getattr(self, field, '')
            max_length = self._meta.get_field(field).max_length
            if len(value) > max_length:
                errors.append(f"{field} cannot be more than {max_length} characters.") 

        # If there are errors, raise a ValidationError with all errors
        if errors:
            raise ValidationError({'error':errors})


# Title
 
class Title_Detials(models.Model):
    Title_Id = models.AutoField(primary_key=True)
    Title_Name = models.CharField(max_length=30)
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)
 
    class Meta:
        db_table = 'Title_Detials'  
 
    
    
class Clinic_Detials(models.Model):
    Clinic_Id = models.AutoField(primary_key=True)
    Clinic_Mail = models.CharField(max_length=30)
    Clinic_PhoneNo = models.CharField(max_length=30)
    Clinic_LandlineNo = models.CharField(max_length=30)
    Clinic_GstNo = models.CharField(max_length=30)
    Clinic_DoorNo = models.CharField(max_length=30)
    Clinic_Street = models.CharField(max_length=30)
    Clinic_Area = models.CharField(max_length=30)
    Clinic_City = models.CharField(max_length=30)
    Clinic_State = models.CharField(max_length=30)
    Clinic_Country = models.CharField(max_length=30)
    Clinic_Pincode = models.CharField(max_length=30)
    created_by = models.CharField(max_length=30)
    Location = models.ForeignKey(Location_Detials, on_delete=models.CASCADE,related_name='Clinic_location',null=True,blank=True,default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Clinic_Detials'
    
    
        
# Flagg color

class Flaggcolor_Detials(models.Model):
    Flagg_Id = models.AutoField(primary_key=True)
    Flagg_Name = models.CharField(max_length=70)
    Flagg_Color = models.CharField(max_length=30)
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Flaggcolor_Detials'

    

        
#   Departments
class Department_Detials(models.Model):
    Department_Id = models.AutoField(primary_key=True)
    Department_Name = models.CharField(max_length=30)
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Department_Detials'



class Designation_Detials(models.Model):
    Designation_Id = models.AutoField(primary_key=True)
    Designation_Name = models.CharField(max_length=30)
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Designation_Detials'

   
    def __str__(self):
        return self.Designation_Name

class ConsentName_Detials(models.Model):
    ConsentName_Id = models.AutoField(primary_key=True)
    DepartmentName = models.ForeignKey(Department_Detials, on_delete=models.CASCADE, related_name='Consent')
    ConsentName = models.CharField(max_length=300)
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ConsentName_Detials'
        
        
class Category_Detials(models.Model):
    Category_Id = models.AutoField(primary_key=True)
    #Designation_Name = models.ForeignKey(Designation_Detials, on_delete=models.CASCADE, related_name='categories')
    Category_Name = models.CharField(max_length=30)
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Category_Detials'
    
    




class Speciality_Detials(models.Model):
    Speciality_Id = models.AutoField(primary_key=True)
    Category_Name  = models.ForeignKey(Category_Detials,on_delete=models.CASCADE, related_name='specialities')
    Speciality_Name = models.CharField(max_length=30)
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Speciality_Detials'
        
class Classification_Detials(models.Model):
    Classification_Id = models.AutoField(primary_key=True)
    Classification_Name  = models.CharField(max_length=30)
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Classification_Detials'
        
    

# Religion

class Religion_Detials(models.Model):
    Religion_Id = models.AutoField(primary_key=True)
    Religion_Name = models.CharField(max_length=30)
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)

    class Meta:
        db_table = 'Religion_Detials'
    
    

# referal doctor

class Route_Master_Detials(models.Model):
    Route_Id = models.AutoField(primary_key=True)
    Route_No = models.CharField(max_length=30)
    Route_Name = models.CharField(max_length=30)
    Teshil_Name = models.CharField(max_length=30)
    Village_Name = models.CharField(max_length=30)
    created_by = models.CharField(max_length=30)
    location = models.ForeignKey(Location_Detials, on_delete=models.CASCADE)
    Status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Route_Master_Detials'

    def str(self):
        return self.Route_No



# cast


class Cast_Detials(models.Model):
    Cast_Id = models.AutoField(primary_key=True)
    Cast_Name = models.CharField(max_length=30)
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)

    class Meta:
        db_table = 'Cast_Detials'    



# BloodGroup

class BloodGroup_Detials(models.Model):
    BloodGroup_Id = models.AutoField(primary_key=True)
    BloodGroup_Name = models.CharField(max_length=30)
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)

    class Meta:
        db_table = 'BloodGroup_Detials'


# Triage

class TriageCategory_Detials(models.Model):
    Triage_Id = models.AutoField(primary_key=True)
    Description = models.TextField()
    Category = models.CharField(max_length=100,blank=True,null=True)
    Colour = models.CharField(max_length=50)
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'TriageCategory_Detials'
   
  
# ----------------------------------------- Building Masters   ------------------------------------------------------------------



# building master
class  Building_Master_Detials(models.Model):
    Building_Id = models.AutoField(primary_key=True)
    Building_Name = models.CharField(max_length=30)
    Location_Name = models.ForeignKey(Location_Detials,on_delete=models.CASCADE,related_name='Building_location')
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Building_Master_Detials5'
        
    def str(self):
        return self.Building_Name



# blockMaster
class  Block_Master_Detials(models.Model):
    Block_Id = models.AutoField(primary_key=True)
    Block_Name = models.CharField(max_length=30)
    Building_Name = models.ForeignKey(Building_Master_Detials,on_delete=models.CASCADE,related_name='Block_Building_name')
    Location_Name = models.ForeignKey(Location_Detials,on_delete=models.CASCADE,related_name='Block_location')
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Block_Master_Detials'
        
    def str(self):
        return self.Block_Name
    

# Floor Master
class  Floor_Master_Detials(models.Model):
    Floor_Id = models.AutoField(primary_key=True)
    Floor_Name = models.CharField(max_length=30)
    Building_Name = models.ForeignKey(Building_Master_Detials,on_delete=models.CASCADE,related_name='Floor_Building_name')
    Block_Name = models.ForeignKey(Block_Master_Detials,on_delete=models.CASCADE,related_name='Floor_block_name')
    Location_Name = models.ForeignKey(Location_Detials,on_delete=models.CASCADE,related_name='Floor_location')
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Floor_Master_Detials'
        
    def str(self):
        return self.Floor_Name


# floor master
# ----------------------------------------- Room Masters   ------------------------------------------------------------------

# Ward Type
class WardType_Master_Detials(models.Model):
    Ward_Id = models.AutoField(primary_key=True)
    Ward_Name = models.CharField(max_length=30)
    Building_Name = models.ForeignKey(Building_Master_Detials,on_delete=models.CASCADE,related_name='ward_Building_name')
    Block_Name = models.ForeignKey(Block_Master_Detials,on_delete=models.CASCADE,related_name='ward_Block_name')
    Floor_Name = models.ForeignKey(Floor_Master_Detials,on_delete=models.CASCADE,related_name='ward_Floor_name')
    Location_Name = models.ForeignKey(Location_Detials,on_delete=models.CASCADE,related_name='ward_location_name')
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'WardType_Master_Detials'
        
    def str(self):
        return self.Ward_Name


# Room Type
class RoomType_Master_Detials(models.Model):
    Room_Id = models.AutoField(primary_key=True)
    # Room_Name = models.CharField(max_length=30)
    Building_Name = models.ForeignKey(Building_Master_Detials,on_delete=models.CASCADE,related_name='room_Building_name')
    Block_Name = models.ForeignKey(Block_Master_Detials,on_delete=models.CASCADE,related_name='room_Block_name')
    Floor_Name = models.ForeignKey(Floor_Master_Detials,on_delete=models.CASCADE,related_name='room_Floor_name')
    Ward_Name = models.ForeignKey(WardType_Master_Detials, on_delete=models.CASCADE, related_name='room_ward_name')
    Location_Name = models.ForeignKey(Location_Detials,on_delete=models.CASCADE,related_name='room_location_name')
    Prev_Charge = models.DecimalField(max_digits=10, decimal_places=3,default=0)
    Current_Charge = models.DecimalField(max_digits=10, decimal_places=3)
    # GST_Charge = models.CharField(max_length=30)
    isAC = models.BooleanField(default=False)
    Doctorcharges = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    Nursecharges = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    SpecDoctorcharges = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    SpecNursecharges = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    Total_Prev_Charge = models.DecimalField(max_digits=10, decimal_places=3,default=0)
    Total_Current_Charge = models.DecimalField(max_digits=10, decimal_places=3)
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'RoomType_Master_Detials'
        
    def str(self):
        return self.Ward_Name

# Room Master

 
class Room_Master_Detials(models.Model):
    Room_Id = models.AutoField(primary_key=True)
    Building_Name = models.ForeignKey(Building_Master_Detials,on_delete=models.CASCADE,related_name='room_master_Building_name')
    Block_Name = models.ForeignKey(Block_Master_Detials,on_delete=models.CASCADE,related_name='room_master_Block_name')
    Floor_Name = models.ForeignKey(Floor_Master_Detials,on_delete=models.CASCADE,related_name='room_master_Floor_name')
    Ward_Name = models.ForeignKey(RoomType_Master_Detials, on_delete=models.CASCADE, related_name='room_master_ward_name')
    # Room_Name = models.ForeignKey(RoomType_Master_Detials, on_delete=models.CASCADE, related_name='room_master_room_name')
    Location_Name = models.ForeignKey(Location_Detials,on_delete=models.CASCADE,related_name='room_master_location_name')
    Room_No = models.CharField(max_length=30)
    Bed_No = models.CharField(max_length=30)
    Status = models.BooleanField(default=True)
    Booking_Status = models.CharField(max_length=30,default='Available')
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        db_table = 'Room_Master_Detials'
 
    def _str_(self):
        return self.Bed_No
 
 


class GradeName_Detials(models.Model):
    GradeName_Id = models.AutoField(primary_key=True)
    GradeName_Name = models.CharField(max_length=30)
    RoomName = models.ForeignKey(RoomType_Master_Detials, on_delete=models.CASCADE, null=True, blank=True)
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)

    class Meta:
        db_table = 'GradeName_Detials'

# role management and user register 


class Role_Master(models.Model):
    Role_Id = models.AutoField(primary_key=True)
    Role_Name = models.CharField(max_length=50)
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Role_Master'

    def __str__(self):
        return self.Role_Name

    
  


# OtTheater 
class OtTheaterMaster_Detials(models.Model):
    Ot_Id = models.AutoField(primary_key=True)
    Location = models.ForeignKey(Location_Detials,on_delete=models.CASCADE,related_name='OtTheater_location',blank=True,null=True)
    Building = models.ForeignKey(Building_Master_Detials,on_delete=models.CASCADE,related_name='OtTheater_Building',blank=True,null=True)
    Block = models.ForeignKey(Block_Master_Detials,on_delete=models.CASCADE,related_name='OtTheater_Block',blank=True,null=True)
   # Ward = models.ForeignKey(WardType_Master_Detials,on_delete=models.CASCADE,related_name='OtTheater_Ward',blank=True,null=True)
    TheatreName = models.CharField(max_length=30,blank=True,null=True)
    ShortName = models.CharField(max_length=30,blank=True,null=True)
    FloorName = models.ForeignKey(Floor_Master_Detials,on_delete=models.CASCADE,related_name='OtTheater_Floor_name',blank=True,null=True)
    Emergency = models.BooleanField(default=False)
    Speciality = models.ManyToManyField(Speciality_Detials,related_name='OtTheater_Speciality',blank=True)
    
    TheatreType = models.CharField(max_length=255,null=True,blank=True)
    Rent = models.CharField(max_length=255,null=True,blank=True)
    Details = models.TextField()
    Remarks = models.TextField()
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)

    class Meta:
        db_table = 'OtTheaterMaster_Detials'



 
        



#-------------------Doctor Master----------------------


# Doctor Personal Form

class Doctor_Personal_Form_Detials(models.Model):
    Doctor_ID = models.CharField(primary_key=True,max_length=30)
    DoctorType = models.CharField(max_length=30)
    Tittle = models.ForeignKey(Title_Detials,on_delete=models.CASCADE,blank=True,null=True,related_name='Doctor_Title')
    First_Name = models.CharField(max_length=30)
    Middle_Name = models.CharField(max_length=30)
    Last_Name = models.CharField(max_length=30)
    Gender = models.CharField(max_length=30)
    ShortName = models.CharField(max_length=30)
    DOB = models.CharField(max_length=30)
    Age = models.CharField(max_length=30)
    Duration = models.CharField(max_length=30)
    Marital_Status = models.CharField(max_length=30)
    Anniversary_Date = models.CharField(max_length=30)
    Spouse_Name = models.CharField(max_length=30)
    Nationality = models.CharField(max_length=30)
    E_mail = models.CharField(max_length=30)
    Contact_Number = models.CharField(max_length=15)
    Alternate_Number = models.CharField(max_length=15)
    Emergency_No1 = models.CharField(max_length=15)
    Emergency_No2 = models.CharField(max_length=15)
    Current_Address = models.CharField(max_length=500)
    Permanent_Address = models.CharField(max_length=500)
    Languages_Spoken = models.CharField(max_length=30)
    Mode_of_Communication = models.CharField(max_length=30)
    Emergency_Availablity = models.CharField(max_length=10)
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Doctor_Personal_Form_Detials'
        
    def _str_(self):
        return self.Doctor_ID

    def save(self, *args, **kwargs):
        if not self.Doctor_ID:  # Generate Mlc_Id if not set
            # Get the hospital name (clinic_name)
            clinic_name = Hospital_Detials.objects.first().Hospital_Name[:3].upper()
            
            # Fetch the maximum Mlc_Id
            max_Doctor_ID_row = Doctor_Personal_Form_Detials.objects.exclude(created_by="system").aggregate(max_id=Max('Doctor_ID'))['max_id']
            max_Doctor_ID = max_Doctor_ID_row if max_Doctor_ID_row else None

            # Calculate the numerical part
            numeric_part = int(str(max_Doctor_ID)[6:]) + 1 if max_Doctor_ID else 1

            # Construct the next Mlc_Id
            self.Doctor_ID = f'{clinic_name}DOC{numeric_part:04}'

        super(Doctor_Personal_Form_Detials, self).save(*args, **kwargs)


#-------------------DoctorProfessForm---------------------

#-------------------DoctorProfessForm---------------------


class Doctor_ProfessForm_Detials(models.Model):
    Doctor_ID = models.ForeignKey(Doctor_Personal_Form_Detials, on_delete=models.CASCADE, db_column='Doctor_ID')
    Qualification = models.CharField(max_length=30)
    RouteId=models.ForeignKey(Route_Master_Detials, on_delete=models.CASCADE, related_name='doctor_Route_details',null=True,blank=True)
    VisitingDoctorType = models.CharField(max_length=30)
    Department = models.ManyToManyField(Department_Detials,related_name='doctor_profess_form_details')
    Designation = models.ForeignKey(Designation_Detials, on_delete=models.CASCADE, related_name='doctor_profess_form_designations',null=True,blank=True)
    Specialization = models.ForeignKey(Speciality_Detials, on_delete=models.CASCADE, related_name='doctor_profess_form_specialities',null=True,blank=True)
    Category = models.ForeignKey(Category_Detials, on_delete=models.CASCADE, related_name='doctor_profess_form_categories',null=True,blank=True)
    Classification = models.ForeignKey(Classification_Detials,on_delete=models.CASCADE,related_name='doctor_profess_form_classification',null=True,blank=True)
    Role = models.ForeignKey(Role_Master,on_delete=models.CASCADE,related_name='doctor_profess_form_role',null=True,blank=True)
    MCI_Number = models.CharField(max_length=30)
    State_RegistrationNumber = models.CharField(max_length=30)
    License_ExpiryDate = models.CharField(max_length=30)
    Yearsof_Experience = models.CharField(max_length=30)
    Date_OfJoining = models.CharField(max_length=30,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Doctor_ProfessForm_Detials'
        
    def str(self):
        return str(self.Doctor_ID)
#-------------------DoctorInsuranceForm---------------------


class Doctor_InsuranceForm_Detials(models.Model):
    Doctor_ID = models.ForeignKey(Doctor_Personal_Form_Detials, on_delete=models.CASCADE, db_column='Doctor_ID')
    Insurance_DetailsFile = models.BinaryField(null=True, blank=True)    
    Insurance_RenewalDate = models.CharField(max_length=30)
    Malpractice_Insurance_ProviderName = models.CharField(max_length=30)
    Policy_Number = models.CharField(max_length=30)
    Coverage_Amount = models.CharField(max_length=30)
    Expiry_Date = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Doctor_InsuranceForm_Detials'
        
    def _str_(self):
        return self.Doctor_ID



#-------------------DoctorDocumentsForm---------------------


class Doctor_DocumentsForm_Detials(models.Model):
    Doctor_ID = models.ForeignKey(Doctor_Personal_Form_Detials, on_delete=models.CASCADE, db_column='Doctor_ID')
    Photo = models.BinaryField(null=True, blank=True)
    Signature = models.BinaryField(null=True, blank=True)
    Agreement_File = models.BinaryField(null=True, blank=True)
    AdhaarCard = models.BinaryField(null=True, blank=True)
    PanCard = models.BinaryField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Doctor_DocumentsForm_Detials'
        
    def _str_(self):
        return self.Doctor_ID


#-------------------DoctorBankForm---------------------


class Doctor_BankForm_Detials(models.Model):
    Doctor_ID = models.ForeignKey(Doctor_Personal_Form_Detials, on_delete=models.CASCADE, db_column='Doctor_ID')
    Account_Number = models.CharField(max_length=30)
    Bank_Name = models.CharField(max_length=30)
    Branch_Name = models.CharField(max_length=30)
    IFSC_Code = models.CharField(max_length=30)
    Pancard_Number = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Doctor_BankForm_Detials'
        
    def _str_(self):
        return self.Doctor_ID

#-------------------DoctorContractForm---------------------


class Doctor_ContractForm_Detials(models.Model):
    Doctor_ID = models.ForeignKey(Doctor_Personal_Form_Detials, on_delete=models.CASCADE, db_column='Doctor_ID')
    Previous_EmployeementHistory = models.CharField(max_length=30)
    Comission = models.CharField(max_length=30)
    Contract_StartDate = models.CharField(max_length=30)
    Contract_EndDate = models.CharField(max_length=30)
    Contract_RenewalTerms = models.CharField(max_length=500)
    Remarks = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Doctor_ContractForm_Detials'
        
    def _str_(self):
        return self.Doctor_ID
#-------------------DoctorScheduleForm---------------------

class Doctor_Schedule_Details(models.Model):
    Doctor_ID = models.ForeignKey(Doctor_Personal_Form_Detials, on_delete=models.CASCADE, db_column='Doctor_ID')
    Day = models.CharField(max_length=30)
    Location = models.ForeignKey(Location_Detials, on_delete=models.CASCADE,null=True)
    LocationName = models.CharField(max_length=30,null=True,blank=True)
    IsWorking = models.CharField(max_length=30)
    Shift = models.CharField(max_length=30,default='Single')
    Starting_Time = models.TimeField(null=True,blank=True)
    End_Time = models.TimeField(blank=True, null=True)
    Starting_Time_F = models.TimeField(blank=True,null=True)
    End_Time_F = models.TimeField(blank=True,null=True)
    Starting_Time_A = models.TimeField(blank=True,null=True)
    End_Time_A = models.TimeField(blank=True,null=True)
    Working_Hours_F = models.CharField(max_length=30,null=True) 
    Working_Hours_A = models.CharField(max_length=30,null=True) 
    Working_Hours_S = models.CharField(max_length=30,null=True) 
    Total_Working_Hours_S = models.CharField(max_length=30, null=True,blank=True)
    Total_Working_Hours = models.CharField(max_length=30, null=True,blank=True)  
    Status = models.CharField(max_length=30,default='Active')     
    class Meta:
        db_table = 'Doctor_Schedule_Details'
    
    def _str_(self):
        return self.Doctor_ID
    

    


#  employee register 

class Employee_Personal_Form_Detials(models.Model):
    Employee_ID = models.CharField(primary_key=True, max_length=30)
    Tittle = models.ForeignKey(Title_Detials,on_delete=models.CASCADE,blank=True,null=True)
    First_Name = models.CharField(max_length=30)
    Middle_Name = models.CharField(max_length=30,blank=True,null=True)
    Last_Name = models.CharField(max_length=30,blank=True,null=True)
    Gender = models.CharField(max_length=30)
    DOB = models.CharField(max_length=30)
    Age = models.CharField(max_length=30)
    BloodGroup = models.ForeignKey(BloodGroup_Detials,on_delete=models.CASCADE,blank=True,null=True)
    Contact_Number = models.CharField(max_length=15,blank=True,null=True)
    Alternate_Number = models.CharField(max_length=15,blank=True,null=True)
    E_mail = models.CharField(max_length=50,blank=True,null=True)
    Qualification = models.CharField(max_length=30,blank=True,null=True)
    SkillSet = models.CharField(max_length=30,blank=True,null=True)
    IdProofType = models.CharField(max_length=30,blank=True,null=True)
    IdProofNo = models.CharField(max_length=100,blank=True,null=True)
    Marital_Status = models.CharField(max_length=30,blank=True,null=True)
    MarriagePlan = models.CharField(max_length=30,blank=True,null=True)
    AnniversaryDate = models.CharField(max_length=30, blank=True, null=True)
    Residence = models.CharField(max_length=30, blank=True, null=True)
    FatherName = models.CharField(max_length=30,blank=True,null=True)
    FatherContact = models.CharField(max_length=30,blank=True,null=True)
    FatherWorking = models.CharField(max_length=30,blank=True,null=True)
    FatherWorkPlace = models.CharField(max_length=100,blank=True,null=True)
    MotherName = models.CharField(max_length=30,blank=True,null=True)
    MotherContact = models.CharField(max_length=30,blank=True,null=True)
    MotherWorking = models.CharField(max_length=30,blank=True,null=True)
    MotherWorkPlace = models.CharField(max_length=100,blank=True,null=True)
    Spouse_Name = models.CharField(max_length=30,blank=True,null=True)
    SpouseContact = models.CharField(max_length=30,blank=True,null=True)
    SpouseWorking = models.CharField(max_length=30,blank=True,null=True)
    SpouseWorkPlace = models.CharField(max_length=100,blank=True,null=True)
    Child = models.CharField(max_length=30,blank=True,null=True)
    TotalNoChild = models.CharField(max_length=30,blank=True,null=True)
    DoorNo = models.CharField(max_length=30,blank=True,null=True)
    Street = models.CharField(max_length=30,blank=True,null=True)
    Area = models.CharField(max_length=30,blank=True,null=True)
    City = models.CharField(max_length=30,blank=True,null=True)
    District = models.CharField(max_length=30,blank=True,null=True)
    State = models.CharField(max_length=30,blank=True,null=True)
    Country = models.CharField(max_length=30,blank=True,null=True)
    Pincode = models.CharField(max_length=30,blank=True,null=True)
    PermanentAddressSameAsAbove = models.CharField(max_length=30,blank=True,null=True)
    PermanentDoorNo = models.CharField(max_length=30,blank=True,null=True)
    PermanentStreet = models.CharField(max_length=30,blank=True,null=True)
    PermanentArea = models.CharField(max_length=30,blank=True,null=True)
    PermanentCity = models.CharField(max_length=30,blank=True,null=True)
    PermanentDistrict = models.CharField(max_length=30,blank=True,null=True)
    PermanentState = models.CharField(max_length=30,blank=True,null=True)
    PermanentCountry = models.CharField(max_length=30,blank=True,null=True)
    PermanentPincode = models.CharField(max_length=30,blank=True,null=True)
    EmergencyContactName1 = models.CharField(max_length=30,blank=True,null=True)
    EmergencyContactNo1 = models.CharField(max_length=30,blank=True,null=True)
    EmergencyContactName2 = models.CharField(max_length=30,blank=True,null=True)
    EmergencyContactNo2 = models.CharField(max_length=30,blank=True,null=True)
    Classification = models.ForeignKey(Classification_Detials, on_delete=models.CASCADE,blank=True,null=True)
    Category = models.ForeignKey(Category_Detials, on_delete=models.CASCADE,blank=True,null=True)
    Speciality = models.ForeignKey(Speciality_Detials, on_delete=models.CASCADE,blank=True,null=True)
    Department = models.ManyToManyField(Department_Detials,blank=True)
    Designation = models.ForeignKey(Designation_Detials,on_delete=models.CASCADE,null=True,blank=True)
    Role = models.ForeignKey(Role_Master,on_delete=models.CASCADE,null=True,blank=True)
    Photo = models.BinaryField(blank=True,null=True)
    CaptureImage = models.BinaryField(blank=True,null=True)
    ActiveStatus = models.CharField(max_length=30,blank=True,null=True)    
    RequirementSource = models.CharField(max_length=50,blank=True,null=True)    
    Source = models.CharField(max_length=50,blank=True,null=True)    
    Status = models.BooleanField(default=True,null=True)
    Location = models.ForeignKey(Location_Detials, on_delete=models.CASCADE,blank=True,null=True)
    Anniversary_Date = models.CharField(max_length=30,blank=True,null=True)
    Nationality = models.CharField(max_length=30,blank=True,null=True)
    Languages_Spoken = models.CharField(max_length=30,blank=True,null=True)
    Mode_of_Communication = models.CharField(max_length=30,blank=True,null=True)
    Emergency_Availablity = models.CharField(max_length=10,blank=True,null=True)
    created_by = models.CharField(max_length=30)
    Signature = models.BinaryField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=30,default='')
 
    class Meta:
        db_table = 'Employee_Personal_Form_Detials'
       
    def save(self, *args, **kwargs):
        if not self.Employee_ID:
            prefix = 'CRTEMPL'
           
            max_id = Employee_Personal_Form_Detials.objects.filter(Employee_ID__startswith=prefix).aggregate(max_id=Max('Employee_ID'))['max_id']
           
            if max_id:
                numeric_part = int(max_id.replace(prefix, '')) + 1
            else:
                numeric_part = 1
           
            self.Employee_ID = f'{prefix}{numeric_part:03}'
       
        super().save(*args, **kwargs)
        
# UserRegister_Master_Details

class UserRegister_Master_Details(models.Model):
    User_Id = models.AutoField(primary_key=True)
    auth_user_id = models.OneToOneField(User,on_delete=models.CASCADE, related_name='user_details', null=True, blank=True)
    EmployeeType = models.CharField(max_length=50)
    Doctor_Id = models.ForeignKey(Doctor_Personal_Form_Detials, on_delete=models.CASCADE, related_name='users', null=True, blank=True)
    Employee_Id = models.ForeignKey(Employee_Personal_Form_Detials, on_delete=models.SET_NULL, related_name='Employeeusers', null=True, blank=True)    
    Locations = models.ManyToManyField('Location_Detials', related_name='users')
    role = models.ForeignKey(Role_Master, on_delete=models.CASCADE, related_name='users')
    Access = models.TextField()
    SubAccess = models.TextField()
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'UserRegister_Master_Details'

    def _str_(self):
        return self.auth_user_id.username if self.auth_user_id else "No Username"
   
    
class UserLoginSession(models.Model):
    user = models.ForeignKey(UserRegister_Master_Details, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    device_name = models.CharField(max_length=255, null=True, blank=True) 
    device_id = models.CharField(max_length=80)
    Status = models.BooleanField(default=True)
    api_key = models.CharField(max_length=255, null=True, blank=True)  # To store the API key
    api_password = models.CharField(max_length=255, null=True, blank=True)  # To store the API 
    plain_password=models.CharField(max_length=255, null=True, blank=True)

    
    class Meta:
        db_table = 'UserLoginSession'

    def _str_(self):
        return f"{self.user.auth_user_id.username} (User {self.user.User_Id}) logged in at {self.login_time} from {self.device_name}"


class Insurance_Master_Detials(models.Model):
    Insurance_Id = models.AutoField(primary_key=True)
    Insurance_Name = models.CharField(max_length=50)
    Payer_Zone = models.CharField(max_length=50)
    PayerMember_Id = models.CharField(max_length=50)
    ContactPerson = models.CharField(max_length=50)
    MailId = models.CharField(max_length=50)
    PhoneNumber = models.CharField(max_length=50)
    AlternateNumber = models.CharField(max_length=50,default='',null=True, blank=True)
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        db_table = 'Insurance_Master_Detials'
 
    def __str__(self):
        return self.Insurance_Name
 

 
class Insurance_File_Detials(models.Model):
    InsuranceFile_Id = models.AutoField(primary_key=True)
    InsuranceFile_Name = models.CharField(max_length=50)
    InsuranceMaster_Name= models.ForeignKey(Insurance_Master_Detials, on_delete=models.CASCADE,null=True,blank=True)
    FileDocuments = models.BinaryField(null=True, blank=True)
    Status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Insurance_File_Detials'

    def __str__(self):
        return self.InsuranceFile_Name




class Client_Master_Detials(models.Model):
    Client_Id = models.AutoField(primary_key=True)
    Client_Name = models.CharField(max_length=50)
    ContactPerson = models.CharField(max_length=50)
    MailId = models.CharField(max_length=50)
    PhoneNumber = models.CharField(max_length=50)
    AlternateNumber = models.CharField(max_length=50,default='',null=True, blank=True)
    Address = models.TextField(default='')
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Client_Master_Detials'

    def __str__(self):
        return self.Client_Name


class Client_File_Detials(models.Model):
    ClientFile_Id = models.AutoField(primary_key=True)
    ClientFile_Name = models.CharField(max_length=50)
    ClientMaster_Name= models.ForeignKey(Client_Master_Detials, on_delete=models.CASCADE,null=True,blank=True)
    FileDocuments = models.BinaryField(null=True, blank=True)
    Status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Client_File_Detials'

    def __str__(self):
        return self.ClientFile_Name



class Corporate_Master_Detials(models.Model):
    Corporate_Id = models.AutoField(primary_key=True)
    Corporate_Name = models.CharField(max_length=50)
    ContactPerson = models.CharField(max_length=50)
    MailId = models.CharField(max_length=50)
    PhoneNumber = models.CharField(max_length=50)
    AlternateNumber = models.CharField(max_length=50,default='',null=True, blank=True)
    Address = models.TextField(default='')
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Corporate_Master_Detials'

    def __str__(self):
        return self.Corporate_Name


class Corporate_File_Detials(models.Model):
    CorporateFile_Id = models.AutoField(primary_key=True)
    CorporateFile_Name = models.CharField(max_length=50)
    CorporateMaster_Name= models.ForeignKey(Corporate_Master_Detials, on_delete=models.CASCADE,null=True,blank=True)
    FileDocuments = models.BinaryField(null=True, blank=True)
    Status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Corporate_File_Detials'

    def __str__(self):
        return self.CorporateFile_Name






class Donation_Master_Detials(models.Model):
    Donation_Id = models.AutoField(primary_key=True)
    Donation_Name = models.CharField(max_length=50)
    Type = models.CharField(max_length=50 ,default='')
    ContactPerson = models.CharField(max_length=50)
    Designation = models.CharField(max_length=50)
    PancardNo = models.CharField(max_length=50)
    CIN = models.CharField(max_length=50)
    TAN = models.CharField(max_length=50)
    MailId = models.CharField(max_length=50)
    PhoneNumber = models.CharField(max_length=50)
    AlternateNumber = models.CharField(max_length=50,default='',null=True, blank=True)
    Address = models.TextField()
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Donation_Master_Detials'

    def __str__(self):
        return self.Donation_Name



class Donation_File_Detials(models.Model):
    DonationFile_Id = models.AutoField(primary_key=True)
    DonationFile_Name = models.CharField(max_length=50)
    DonationMaster_Name= models.ForeignKey(Donation_Master_Detials, on_delete=models.CASCADE,null=True,blank=True)
    FileDocuments = models.BinaryField(null=True, blank=True)
    Status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Donation_File_Detials'

    def __str__(self):
        return self.DonationFile_Name





#    Ratecard Masters----------------------


class Doctor_Ratecard_Master(models.Model):
    RateCard_Id = models.AutoField(primary_key=True)
    Doctor_ID = models.ForeignKey(Doctor_Personal_Form_Detials, on_delete=models.CASCADE, db_column='Doctor_ID')
    General_Prev_Consultation_Fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    General_Consultation_Fee = models.DecimalField(max_digits=10, decimal_places=2, default=300)
    General_Prev_Follow_Up_Fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    General_Follow_Up_Fee = models.DecimalField(max_digits=10, decimal_places=2, default=300)
    General_Prev_Emg_Consulting_Fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    General_Emg_Consulting_Fee = models.DecimalField(max_digits=10, decimal_places=2, default=300)
    Special_Prev_Consultation_Fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Special_Consultation_Fee = models.DecimalField(max_digits=10, decimal_places=2, default=300)
    Special_Prev_Follow_Up_Fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Special_Follow_Up_Fee = models.DecimalField(max_digits=10, decimal_places=2, default=300)
    Special_Prev_Emg_Consulting_Fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Special_Emg_Consulting_Fee = models.DecimalField(max_digits=10, decimal_places=2, default=300)
    Doctor_Contribution_OP = models.DecimalField(max_digits=10, decimal_places=2, default=30)
    Doctor_Contribution_IP = models.DecimalField(max_digits=10, decimal_places=2, default=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Doctor_Ratecard_Master'

    def _str_(self):
        return self.Doctor_ID.Doctor_ID
    
    
class RoomTypeFee(models.Model):
    doctor_ratecard = models.ForeignKey(Doctor_Ratecard_Master, on_delete=models.CASCADE, related_name='room_fees')
    room_type = models.ForeignKey(RoomType_Master_Detials, on_delete=models.CASCADE)
    General_Prev_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    General_fee = models.DecimalField(max_digits=10, decimal_places=2, default=300)
    Special_Prev_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Special_fee = models.DecimalField(max_digits=10, decimal_places=2, default=300)

    class Meta:
        unique_together = ('doctor_ratecard', 'room_type')
        db_table = 'room_type_fee'

    def __str__(self):
        return f"{self.doctor_ratecard.Doctor_ID} - {self.room_type.Ward_Name} Fee"


class InsuranceFee(models.Model):
    doctor_ratecard = models.ForeignKey(Doctor_Ratecard_Master, on_delete=models.CASCADE, related_name='insurance_fees')
    insurance = models.ForeignKey(Insurance_Master_Detials, on_delete=models.CASCADE)
    Prev_Consultation_Fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Consultation_Fee = models.DecimalField(max_digits=10, decimal_places=2, default=300)
    Prev_Follow_Up_Fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Follow_Up_Fee = models.DecimalField(max_digits=10, decimal_places=2, default=300)
    Prev_Emg_Consulting_Fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Emg_Consulting_Fee = models.DecimalField(max_digits=10, decimal_places=2, default=300)

    class Meta:
        unique_together = ('doctor_ratecard', 'insurance')
        db_table = 'insurance_fee'

    def __str__(self):
        return f"{self.doctor_ratecard.Doctor_ID} - {self.insurance.Insurance_Name} Fee"


class ClientFee(models.Model):
    doctor_ratecard = models.ForeignKey(Doctor_Ratecard_Master, on_delete=models.CASCADE, related_name='client_fees')
    client = models.ForeignKey(Client_Master_Detials, on_delete=models.CASCADE)
    Prev_Consultation_Fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Consultation_Fee = models.DecimalField(max_digits=10, decimal_places=2, default=300)
    Prev_Follow_Up_Fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Follow_Up_Fee = models.DecimalField(max_digits=10, decimal_places=2, default=300)
    Prev_Emg_Consulting_Fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Emg_Consulting_Fee = models.DecimalField(max_digits=10, decimal_places=2, default=300)

    class Meta:
        unique_together = ('doctor_ratecard', 'client')
        db_table = 'client_fee'

    def __str__(self):
        return f"{self.doctor_ratecard.Doctor_ID} - {self.client.Client_Name} Fee"


class CorporateFee(models.Model):
    doctor_ratecard = models.ForeignKey(Doctor_Ratecard_Master, on_delete=models.CASCADE, related_name='corporate_fees')
    corporate = models.ForeignKey(Corporate_Master_Detials, on_delete=models.CASCADE)
    Prev_Consultation_Fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Consultation_Fee = models.DecimalField(max_digits=10, decimal_places=2, default=300)
    Prev_Follow_Up_Fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Follow_Up_Fee = models.DecimalField(max_digits=10, decimal_places=2, default=300)
    Prev_Emg_Consulting_Fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Emg_Consulting_Fee = models.DecimalField(max_digits=10, decimal_places=2, default=300)

    class Meta:
        unique_together = ('doctor_ratecard', 'corporate')
        db_table = 'corporate_fee'

    def __str__(self):
        return f"{self.doctor_ratecard.Doctor_ID} - {self.corporate.Corporate_Name} Fee"


class InsuranceRoomTypeFee(models.Model):
    doctor_ratecard = models.ForeignKey(Doctor_Ratecard_Master, on_delete=models.CASCADE, related_name='doctor_insurance_RoomType_Fee')
    room_type_fee = models.ForeignKey(RoomTypeFee, on_delete=models.CASCADE, related_name='insurance_fees')
    insurance = models.ForeignKey(Insurance_Master_Detials, on_delete=models.CASCADE)
    Prev_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=300)

    class Meta:
        unique_together = ('room_type_fee', 'insurance','doctor_ratecard')
        db_table = 'insurance_room_type_fee'

    def __str__(self):
        return f"{self.room_type_fee.doctor_ratecard.Doctor_ID} - {self.room_type_fee.room_type.Ward_Name} - {self.insurance.Insurance_Name} Fee"


class ClientRoomTypeFee(models.Model):
    doctor_ratecard = models.ForeignKey(Doctor_Ratecard_Master, on_delete=models.CASCADE, related_name='doctor_client_RoomType_Fee')
    room_type_fee = models.ForeignKey(RoomTypeFee, on_delete=models.CASCADE, related_name='client_fees')
    client = models.ForeignKey(Client_Master_Detials, on_delete=models.CASCADE)
    Prev_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=300)

    class Meta:
        unique_together = ('room_type_fee', 'client','doctor_ratecard')
        db_table = 'client_room_type_fee'

    def __str__(self):
        return f"{self.room_type_fee.doctor_ratecard.Doctor_ID} - {self.room_type_fee.room_type.Ward_Name} - {self.client.Client_Name} Fee"


class CorporateRoomTypeFee(models.Model):
    doctor_ratecard = models.ForeignKey(Doctor_Ratecard_Master, on_delete=models.CASCADE, related_name='doctor_corporate_RoomType_Fee')
    room_type_fee = models.ForeignKey(RoomTypeFee, on_delete=models.CASCADE, related_name='corporate_fees')
    corporate = models.ForeignKey(Corporate_Master_Detials, on_delete=models.CASCADE)
    Prev_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=300)

    class Meta:
        unique_together = ('room_type_fee', 'corporate','doctor_ratecard')
        db_table = 'corporate_room_type_fee'

    def __str__(self):
        return f"{self.room_type_fee.doctor_ratecard.Doctor_ID} - {self.room_type_fee.room_type.Ward_Name} - {self.corporate.Client_Name} Fee"




# ---------------------- service Procedure master ---------------
 
#  Service Category Master
 
class Service_Category_Masters(models.Model):
    Serviceid = models.AutoField(primary_key=True)
    Servicegroup = models.CharField(max_length=100)
    ServiceCategory = models.CharField(max_length=140)
    Createdby = models.CharField(max_length=70)
    Location = models.ForeignKey(Location_Detials, on_delete=models.CASCADE)
    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)
 
 
    class Meta:
        db_table = 'Service_Category_Masters'  
        
class Service_Master_Details(models.Model):
    Service_Id = models.AutoField(primary_key=True)
    Service_Name = models.CharField(max_length=100)
    Service_Type = models.CharField(max_length=100,default='Quantity')
    Department = models.CharField(max_length=20,default='OP')
  #  IsGst = models.CharField(max_length=10)
   # GstValue = models.CharField(max_length=50)
    Amount = models.DecimalField(max_digits=10,decimal_places=3,default=0)
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Service_Master_Details'

    def _str_(self):
        return self.Service_Name


class Procedure_Master_Details(models.Model):
    Procedure_Id = models.AutoField(primary_key=True)
    Procedure_Name = models.CharField(max_length=100)
    Amount = models.DecimalField(max_digits=10,decimal_places=3,default=0)
    Type = models.CharField(max_length=30,default='Interventional')
  #  IsGst = models.CharField(max_length=10)
  # GstValue = models.CharField(max_length=20)
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Procedure_Master_Details'

    def _str_(self):
        return self.Procedure_Name

class Service_Procedure_Charges(models.Model):
    MASTER_TYPE_CHOICES = [
        ('Service', 'Service'),
        ('Procedure', 'Procedure'),
    ]

    MasterType = models.CharField(max_length=10, choices=MASTER_TYPE_CHOICES)
    Service_ratecard = models.ForeignKey(Service_Master_Details, on_delete=models.CASCADE, related_name='Service_charges', null=True, blank=True)
    Procedure_ratecard = models.ForeignKey(Procedure_Master_Details, on_delete=models.CASCADE, related_name='Procedure_charges', null=True, blank=True)
    Location = models.ForeignKey('Location_Detials', on_delete=models.CASCADE)
   
    class Meta:
        unique_together = ('MasterType', 'Service_ratecard', 'Procedure_ratecard', 'Location')
        db_table = 'Service_Procedure_Charges'

    def __str__(self):
        if self.MasterType == 'Service' and self.Service_ratecard:
            return f"Service: {self.Service_ratecard.Service_Name} - Location: {self.Location}"
        elif self.MasterType == 'Procedure' and self.Procedure_ratecard:
            return f"Procedure: {self.Procedure_ratecard.Procedure_Name} - Location: {self.Location}"
        return f"Service/Procedure - Location: {self.Location}"


class Service_Procedure_Rate_Charges(models.Model):
    Service_Procedure_ratecard = models.ForeignKey(Service_Procedure_Charges, on_delete=models.CASCADE, related_name='Service_Procedure_rates_charges')
    General_Prev_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    General_fee = models.DecimalField(max_digits=10, decimal_places=2, default=300)
    Special_Prev_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Special_fee = models.DecimalField(max_digits=10, decimal_places=2, default=300)

    class Meta:
        db_table = 'Service_Procedure_Rate_Charges'

   


class Service_Procedure_RoomTypeFee(models.Model):
    Service_Procedure_ratecard = models.ForeignKey(Service_Procedure_Charges, on_delete=models.CASCADE, related_name='Service_Procedure_room_type_fees')
    room_type = models.ForeignKey(RoomType_Master_Detials, on_delete=models.CASCADE,related_name='Service_Procedure_room_type_fees_room_type')
    General_Prev_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    General_fee = models.DecimalField(max_digits=10, decimal_places=2, default=300)
    Special_Prev_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    Special_fee = models.DecimalField(max_digits=10, decimal_places=2, default=300)

    class Meta:
        unique_together = ('Service_Procedure_ratecard', 'room_type')
        db_table = 'Service_Procedure_RoomTypeFee'

    

class Service_Procedure_InsuranceFee(models.Model):
    Service_Procedure_ratecard = models.ForeignKey(Service_Procedure_Charges, on_delete=models.CASCADE, related_name='insurance_fees')
    insurance = models.ForeignKey(Insurance_Master_Detials, on_delete=models.CASCADE,related_name='insurance_fees_insurance')
    Prev_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=300)

    class Meta:
        unique_together = ('Service_Procedure_ratecard', 'insurance')
        db_table = 'Service_Procedure_InsuranceFee'

    
class Service_Procedure_ClientFee(models.Model):
    Service_Procedure_ratecard = models.ForeignKey(Service_Procedure_Charges, on_delete=models.CASCADE, related_name='client_fees')
    client = models.ForeignKey(Client_Master_Detials, on_delete=models.CASCADE,related_name='client_fees_client')
    Prev_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=300)

    class Meta:
        unique_together = ('Service_Procedure_ratecard', 'client')
        db_table = 'Service_Procedure_ClientFee'

    
class Service_Procedure_InsuranceRoomTypeFee(models.Model):
    Service_Procedure_ratecard = models.ForeignKey(Service_Procedure_Charges, on_delete=models.CASCADE, related_name='insurance_room_type_fees')
    room_type_fee = models.ForeignKey(RoomType_Master_Detials, on_delete=models.CASCADE,related_name='insurance_room_type_fees_room_type_fee')
    insurance = models.ForeignKey(Insurance_Master_Detials, on_delete=models.CASCADE,related_name='insurance_room_type_fees_insurance')
    Prev_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=300)

    class Meta:
        unique_together = ('Service_Procedure_ratecard', 'room_type_fee', 'insurance')
        db_table = 'Service_Procedure_InsuranceRoomTypeFee'

   

class Service_Procedure_ClientRoomTypeFee(models.Model):
    Service_Procedure_ratecard = models.ForeignKey(Service_Procedure_Charges, on_delete=models.CASCADE, related_name='client_room_type_fees')
    room_type_fee = models.ForeignKey(RoomType_Master_Detials, on_delete=models.CASCADE,related_name='client_room_type_fees_room_type_fee')
    client = models.ForeignKey(Client_Master_Detials, on_delete=models.CASCADE,related_name='client_room_type_fees_client')
    Prev_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=300)

    class Meta:
        unique_together = ('Service_Procedure_ratecard', 'room_type_fee', 'client')
        db_table = 'Service_Procedure_ClientRoomTypeFee'

    
    
#   Radiology


class RadiologyNames_Details(models.Model):
    Radiology_Id = models.IntegerField(primary_key=True)
    Radiology_Name = models.CharField(max_length=30)
    created_by = models.CharField(max_length=30)
    Location_Name = models.ForeignKey(Location_Detials,on_delete=models.CASCADE,related_name='Radiology_location',null=True)
    Status = models.BooleanField(default=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'RadiologyNames_Details'

    def save(self, *args, **kwargs):
        if not self.Radiology_Id:  # Check if Radiology_Id is not set
            max_id = RadiologyNames_Details.objects.aggregate(max_id=Max('Radiology_Id'))['max_id']
            self.Radiology_Id = (max_id or 0) + 1
        super(RadiologyNames_Details, self).save(*args, **kwargs)



class TestName_Details(models.Model):
    Test_Code = models.CharField(primary_key=True, max_length=30)  # Changed to CharField to store generated ID
    Radiology_Id = models.ForeignKey(RadiologyNames_Details, on_delete=models.CASCADE, related_name='testnames')
    Test_Name = models.CharField(max_length=30)
    Prev_Amount = models.DecimalField(max_digits=10, decimal_places=3,default=0)
    Amount = models.DecimalField(max_digits=10, decimal_places=3)
    Prev_BookingFees = models.DecimalField(max_digits=10, decimal_places=3)
    BookingFees = models.DecimalField(max_digits=10, decimal_places=3)
    Report_file = models.BinaryField(null=True, blank=True)
    Status = models.CharField(max_length=30)
    created_by = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'TestName_Details'

    def save(self, *args, **kwargs):
        if not self.Test_Code:  # Generate Mlc_Id if not set
            # Get the hospital name (clinic_name)
          
            
            # Fetch the maximum Mlc_Id
            max_Doctor_ID_row = TestName_Details.objects.aggregate(max_id=Max('Test_Code'))['max_id']
            max_Doctor_ID = max_Doctor_ID_row if max_Doctor_ID_row else None

            # Calculate the numerical part
            numeric_part = int(str(max_Doctor_ID)[7:]) + 1 if max_Doctor_ID else 1

            # Construct the next Mlc_Id
            self.Test_Code = f'TSTCODE{numeric_part:04}'

        super(TestName_Details, self).save(*args, **kwargs)

    def str(self):
        return self.Test_Name





# # Subtest-------------------------
# class SubTest_Details(models.Model):
#     SubTest_Code = models.CharField(primary_key=True, max_length=30)  # Changed to CharField to store generated ID
#     Test_Code = models.ForeignKey(TestName_Details, on_delete=models.CASCADE,null=True,blank=True)
#     SubTestName = models.CharField(max_length=20)
#     Prev_Amount = models.DecimalField(max_digits=10, decimal_places=3,default=0)
#     Amount = models.DecimalField(max_digits=10, decimal_places=3)
#     Prev_BookingFees = models.DecimalField(max_digits=10, decimal_places=3)
#     BookingFees = models.DecimalField(max_digits=10, decimal_places=3)
#     Report_file = models.BinaryField(null=True, blank=True)
#     Status = models.CharField(max_length=20)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         db_table = 'SubTest_Details'

#     def save(self, *args, **kwargs):
#         if not self.SubTest_Code:  # Generate Mlc_Id if not set
#             # Get the hospital name (clinic_name)
           
            
#             # Fetch the maximum Mlc_Id
#             max_Doctor_ID_row = SubTest_Details.objects.aggregate(max_id=Max('SubTest_Code'))['max_id']
#             max_Doctor_ID = max_Doctor_ID_row if max_Doctor_ID_row else None

#             # Calculate the numerical part
#             numeric_part = int(str(max_Doctor_ID)[7:]) + 1 if max_Doctor_ID else 1

#             # Construct the next Mlc_Id
#             self.SubTest_Code = f'STSCODE{numeric_part:04}'

#         super(SubTest_Details, self).save(*args, **kwargs)

#     def str(self):
#         return self.SubTestName
    


    
#LabMaster
class External_LabDetails(models.Model):
    External_Id = models.IntegerField(primary_key=True)  # Corrected from 'IntergerField'
    LabName = models.CharField(max_length=50)
    PhoneNo = models.CharField(max_length=30)  # Corrected from 'InterFiels'
    Address = models.TextField()
    Pincode = models.CharField(max_length=30)
    RegisterNo = models.CharField(max_length=40)
    Email = models.CharField(max_length=40)  # Corrected from 'CharFiels'
    Lablocation = models.CharField(max_length=30)
    location = models.ForeignKey(Location_Detials, on_delete=models.CASCADE,related_name='external_location',null=True)  # Corrected from 'Foreinkey'
    created_by = models.CharField(max_length=30)
    Status = models.CharField(max_length=30,default="Active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'External_LabDetails'

    def save(self, *args, **kwargs):
        if not self.External_Id:
            max_id = External_LabDetails.objects.aggregate(max_id=Max('External_Id'))['max_id']
            self.External_Id = (max_id or 0) + 1
        super(External_LabDetails, self).save(*args,**kwargs)

   
#LabMaster


class LabTestName_Details(models.Model):
    TestCode = models.CharField(max_length=50, primary_key=True)  # Changed to CharField to accommodate custom code
    Test_Name = models.CharField(max_length=50)
    Prev_Amount = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    Amount = models.DecimalField(max_digits=10, decimal_places=3)
    Types = models.CharField(max_length=30,default="")
    created_by = models.CharField(max_length=30)
    location = models.ForeignKey(Location_Detials, on_delete=models.CASCADE,related_name='testlocation',null=True)
    Status = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'LabTestName_Details'

    def save(self, *args, **kwargs):
        if not self.TestCode:
            # Fetch the maximum TestCode
            max_TestCode_row = LabTestName_Details.objects.aggregate(max_id=Max('TestCode'))['max_id']
            max_TestCode = max_TestCode_row if max_TestCode_row else None

            # Calculate the numerical part
            numeric_part = int(max_TestCode[7:]) + 1 if max_TestCode else 1

            # Construct the next TestCode
            self.TestCode = f'STSCODE{numeric_part:04}'

        super(LabTestName_Details, self).save(*args, **kwargs)

    def str(self):
        return self.Test_Name


class External_LabAmount_Details(models.Model):
    OutSource_Id = models.IntegerField(primary_key=True)
    Test_Name = models.ForeignKey(LabTestName_Details, on_delete=models.CASCADE, related_name='outsource', null=True)
    OutSourceLabName = models.ForeignKey(External_LabDetails, on_delete=models.CASCADE, related_name='outsource_location', null=True)
    OutSourcePrev_Amount = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    OutSourceLabAmount = models.DecimalField(max_digits=10, decimal_places=3) 
    created_by = models.CharField(max_length=30)
    Status = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'External_LabAmount_Details'

    def save(self, *args, **kwargs):
        if not self.OutSource_Id:
            max_id = External_LabAmount_Details.objects.aggregate(max_id=Max('OutSource_Id'))['max_id']
            self.OutSource_Id = (max_id or 0) + 1
        super(External_LabAmount_Details, self).save(*args,**kwargs)


class BookingFees_Details(models.Model):
    Basic_FeesId = models.CharField(primary_key=True, max_length=30)  # Primary key for booking fees
    Radiology_Id = models.ForeignKey('RadiologyNames_Details', on_delete=models.CASCADE, related_name='bookingfees')
    From = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    To = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Status = models.BooleanField(default=True) 
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'BookingFees_Details'
    
   

    def save(self, *args, **kwargs):
        if not self.Basic_FeesId:
            max_id = BookingFees_Details.objects.aggregate(max_id=Max('Basic_FeesId'))['max_id']
            if max_id:
                next_id = int(max_id[2:]) + 1
            else:
                next_id = 1
            self.Basic_FeesId = f"BF{next_id:04d}"
        super().save(*args, **kwargs)



class TestName_Favourites(models.Model):
    Favourite_Code = models.AutoField(primary_key=True)
    FavouriteName = models.CharField(max_length=50)
    TestName = models.ManyToManyField(LabTestName_Details, related_name='testNames')
    SumOfAmount = models.DecimalField(max_digits=10, decimal_places=3)
    Previous_Amount = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    Current_Amount = models.DecimalField(max_digits=10, decimal_places=3)
    created_by = models.CharField(max_length=30)
    Status = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'TestName_Favourites'

    def save(self, *args, **kwargs):
        if not self.Favourite_Code:
            max_code_row = TestName_Favourites.objects.aggregate(max_id=Max('Favourite_Code'))['max_id']
            max_code = max_code_row if max_code_row else 0
            self.Favourite_Code = max_code + 1
        super(TestName_Favourites, self).save(*args, **kwargs)

    def str(self):
        return self.FavouriteName
    
# instrument
from django.db import models
from django.db.models import Max

class Instrument_Details(models.Model):
    InstrumentCode = models.CharField(max_length=50, primary_key=True)  # Changed to CharField to accommodate custom code
    Instrument_Name = models.CharField(max_length=50)
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Instrument_Details'

    def save(self, *args, **kwargs):
        if not self.InstrumentCode:
            max_code_row = Instrument_Details.objects.aggregate(max_id=Max('InstrumentCode'))['max_id']
            max_code = int(max_code_row[4:]) if max_code_row else 0  # Assuming 'INST' prefix
            self.InstrumentCode = f"INST{max_code + 1:04}"
        super(Instrument_Details, self).save(*args, **kwargs)

    def str(self):
        return self.Instrument_Name



class Instrument_TrayNames(models.Model):
    Tray_Code = models.AutoField(primary_key=True)
    TrayName = models.CharField(max_length=50)
    TrayQuantity = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    created_by = models.CharField(max_length=30)
    Status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    Instrument = models.ManyToManyField(
        Instrument_Details,
        through='TrayInstrumentLink',
        related_name='trays'
    )

    class Meta:
        db_table = 'Instrument_TrayNames'

    def save(self, *args, **kwargs):
        if not self.Tray_Code:
            max_code_row = Instrument_TrayNames.objects.aggregate(max_id=Max('Tray_Code'))['max_id']
            max_code = max_code_row if max_code_row else 0
            self.Tray_Code = max_code + 1
        super(Instrument_TrayNames, self).save(*args, **kwargs)

    def _str_(self):
        return self.TrayName

class TrayInstrumentLink(models.Model):
    tray = models.ForeignKey(Instrument_TrayNames, on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument_Details, on_delete=models.CASCADE)
    Previous_Quantity = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    Current_Quantity = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    Status = models.BooleanField(default=True)

    class Meta:
        db_table = 'TrayInstrumentLink'
        unique_together = ('tray', 'instrument')
    
# ------------------------------------------------------------------------------------------------------------

class Doctor_Calender_Modal_Edit(models.Model):
    Doctor_ID = models.ForeignKey(Doctor_Personal_Form_Detials, on_delete=models.CASCADE, db_column='Doctor_ID')
    Day = models.CharField(max_length=30)
    Date = models.CharField(max_length=30)
    Location = models.ForeignKey(Location_Detials, on_delete=models.CASCADE,null=True)
    RadioOption = models.CharField(max_length=30,default='Shift')
    Shift = models.CharField(max_length=30,default='Single')
    Starting_Time = models.TimeField(null=True,blank=True)
    End_Time = models.TimeField(blank=True, null=True)
    Starting_Time_F = models.TimeField(blank=True,null=True)
    End_Time_F = models.TimeField(blank=True,null=True)
    Starting_Time_A = models.TimeField(blank=True,null=True)
    End_Time_A = models.TimeField(blank=True,null=True)
    Working_Hours_F = models.CharField(max_length=30,null=True) 
    Working_Hours_A = models.CharField(max_length=30,null=True) 
    Working_Hours_S = models.CharField(max_length=30,null=True) 
    Total_Working_Hours_S = models.CharField(max_length=30, null=True,blank=True)
    Total_Working_Hours = models.CharField(max_length=30, null=True,blank=True)     
    LeaveRemarks = models.CharField(max_length=30,null=True)  
    class Meta:
        db_table = 'Doctor_Calender_Modal_Edit'   
    def _str_(self):
        return self.Doctor_ID
    


# -------------------------------------------------------------------


class SurgeryName_Details(models.Model):
    Surgery_Id = models.IntegerField(primary_key=True)
    Surgery_Code = models.CharField(unique=True, max_length=30)
    Location_Name = models.ForeignKey(Location_Detials, on_delete=models.CASCADE, related_name='surgery_location', null=True)
    Speciality_Name = models.ForeignKey(Speciality_Detials, on_delete=models.CASCADE, related_name='surgery_speciality', null=True)
    Surgery_Type = models.CharField(max_length=40, default="")
    Surgery_Name = models.CharField(max_length=40)
    Duration_Hours = models.DecimalField(max_digits=5, decimal_places=2)
    Estimate_Cost = models.DecimalField(max_digits=10, decimal_places=2)
    Anesthesia_Type = models.CharField(max_length=30)
    Surgery_Description = models.TextField()
    Status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'SurgeryName_Details'

    def save(self, *args, **kwargs):
        if not self.Surgery_Id:
            max_id = SurgeryName_Details.objects.aggregate(max_id=Max('Surgery_Id'))['max_id']
            self.Surgery_Id = (max_id or 0) + 1
        if not self.Surgery_Code:
            hospital_details = Hospital_Detials.objects.first()
            if not hospital_details or len(hospital_details.Hospital_Name) < 3:
                raise ValueError("Hospital name must have at least 3 characters.")
            clinic_name = hospital_details.Hospital_Name[:3].upper()
            today_date = datetime.now().strftime('%y%m%d')
            prefix = f'{clinic_name}{today_date}SUR'
            max_surgery_code = SurgeryName_Details.objects.filter(
                Surgery_Code__startswith=prefix
            ).aggregate(max_id=Max('Surgery_Code'))['max_id']
            if max_surgery_code:
                numeric_part = int(max_surgery_code[-5:]) + 1
            else:
                numeric_part = 1
            self.Surgery_Code = f'{prefix}{numeric_part:05}'
        super(SurgeryName_Details, self).save(*args, **kwargs)

    def __str__(self):
        return self.Surgery_Name






class pharmacy_stock_location_information(models.Model):
    S_No = models.AutoField(primary_key=True)
    Issue_InvoiceNo = models.CharField(max_length=30)
    Item_Code = models.CharField(max_length=30)
    Item_Name = models.CharField(max_length=70)
    Generic_Name = models.CharField(max_length=50)
    Strength = models.CharField(max_length=25)
    UOM = models.CharField(max_length=25)
    Pack_type = models.CharField(max_length=25)
    Pack_Quantity = models.IntegerField()  # Removed max_length
    HSN_Code = models.CharField(max_length=25)
    Batch_No = models.CharField(max_length=25)
    ManufactureDate = models.DateField(null=True, blank=True)
    ExpiryDate = models.DateField(null=True, blank=True)
    ExpiryStatus = models.CharField(max_length=25)
    TotalQuantity = models.BigIntegerField()  # Removed max_length
    SoldQuantity = models.BigIntegerField()  # Removed max_length
    AvailableQuantity = models.BigIntegerField()  # Removed max_length
    MRP_Per_Quantity = models.DecimalField(max_digits=10, decimal_places=2)
    Selling_Rate = models.DecimalField(max_digits=10, decimal_places=2)
    Tax_Percentage = models.IntegerField()  # Removed max_length
    Taxable_Selling_Rate = models.DecimalField(max_digits=10, decimal_places=2)
    Created_By = models.CharField(max_length=150)
    Location = models.CharField(max_length=75)
    ProductCategory = models.CharField(max_length=50)
    ProductCategoryType = models.CharField(max_length=50)
    UpdatedAt = models.DateTimeField(auto_now_add=True)
    CreatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pharmacy_stock_location_information'

    def _str_(self):
        return str(self.S_No)
    
    
class Frequency_Master_Drug(models.Model):
    FrequencyId = models.AutoField(primary_key=True)
    FrequencyName = models.CharField(max_length=40)
    FrequencyType = models.CharField(max_length=55)
    Frequency = models.CharField(max_length=30)
    FrequencyTime = models.CharField(max_length=50)
    Status = models.CharField(max_length=30)
    # Location = models.ForeignKey(max_length=34)

    class Meta:
        db_table='Frequency_Master_Drug'
    def save(self, *args, **kwargs):
        if not self.FrequencyId:
            max_code_row = Frequency_Master_Drug.objects.aggregate(max_id=Max('FrequencyId'))['max_id']
            max_code = max_code_row if max_code_row else 0
            self.FrequencyId = max_code + 1
        super(Frequency_Master_Drug, self).save(*args, **kwargs)

        
class credentialapi(models.Model):
    api_id = models.AutoField(primary_key=True)  # Auto-incrementing field
    token_id = models.CharField(max_length=255, unique=True)
    password_hash = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'credentialapi'
    def _str_(self):
        return self.token_id
    
class appexpiry(models.Model):
    s_no =models.AutoField(primary_key=True)
    user = models.ForeignKey(UserRegister_Master_Details, on_delete=models.CASCADE,blank=True)
    subscriptiontype=models.CharField(max_length=50)
    duration=models.BigIntegerField()
    appstart_date = models.DateField()
    app_end_date = models.DateField()
    status=models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'appexpiry'
    def _str_(self):
        return self.status

# -------------------------------------INVENTORY--------------------------



class Inventory_Location_Master_Detials(models.Model):
 
    Store_Id = models.AutoField(primary_key=True)
    Store_Name = models.CharField(max_length=100)
    Store_Type=models.CharField(max_length=50)
    Building_Name = models.ForeignKey(Building_Master_Detials,on_delete=models.CASCADE,related_name='InveLoc_Building_name')
    Block_Name = models.ForeignKey(Block_Master_Detials,on_delete=models.CASCADE,related_name='InveLoc_Block_name')
    Floor_Name = models.ForeignKey(Floor_Master_Detials,on_delete=models.CASCADE,related_name='InveLoc_Floor_name')
    Location_Name = models.ForeignKey(Location_Detials,on_delete=models.CASCADE,related_name='InveLoc_location_name')
    IsPointOfSale= models.BooleanField(default=False)
    Departments=models.ManyToManyField(Department_Detials,related_name='Department_Pharmacy_Billing',blank=True)
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        db_table = 'Inventory_Location_Master_Detials'
       
    def str(self):
        return self.Store_Name
 
class Inventory_Page_Access_Detailes(models.Model):
    Access_StoreId=models.ForeignKey(Inventory_Location_Master_Detials,on_delete=models.CASCADE,related_name='Access_Inventory_Location_Master')
    IS_PurchaseOrder=models.BooleanField(default=False)
    IS_PurchaseOrder_Approve=models.BooleanField(default=False)
    IS_GRN=models.BooleanField(default=False)
    IS_GRN_Approve=models.BooleanField(default=False)
    IS_Quick_GRN=models.BooleanField(default=False)
    IS_Quick_GRN_Approve=models.BooleanField(default=False)
    IS_Purchase_Return=models.BooleanField(default=False)
    IS_Purchase_Return_Approve=models.BooleanField(default=False)
    IS_Indent=models.BooleanField(default=False)
    IS_Indent_Raise_Approve=models.BooleanField(default=False)
    IS_Indent_Issue_Approve=models.BooleanField(default=False)
    IS_Indent_Receive_Approve=models.BooleanField(default=False)
    IS_Indent_Return_Approve=models.BooleanField(default=False)
    updated_by = models.CharField(max_length=30)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Inventory_Page_Access_Detailes'



class  Rack_Master_Detials(models.Model):
    Rack_Id = models.AutoField(primary_key=True)
    Rack_Name = models.CharField(max_length=50)
    Location_Name = models.ForeignKey(Location_Detials,on_delete=models.CASCADE,related_name='Rack_Master_Location')
    Store_Location_Name=models.ForeignKey(Inventory_Location_Master_Detials,on_delete=models.CASCADE,related_name='Rack_Store_Location')
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Rack_Master_Detials'
        
    def str(self):
        return self.Rack_Name




class Shelf_Master_Detials(models.Model):
    Shelf_Id=models.AutoField(primary_key=True)
    Shelf_Name=models.CharField(max_length=70)
    Rack_Name=models.ForeignKey(Rack_Master_Detials,on_delete=models.CASCADE,related_name='Shelf_Rack_Name')
    Status=models.BooleanField(default=True)
    created_by=models.CharField(max_length=70)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class  Meta:
        db_table = 'Shelf_Master_Detials'
    
    def str(self):
        return(self.Shelf_Name)
    




class Tray_Master_Details(models.Model):
    Tray_Id=models.AutoField(primary_key=True)
    Tray_Name=models.CharField(max_length=70)
    Shelf_Name=models.ForeignKey(Shelf_Master_Detials,on_delete=models.CASCADE,related_name='Tray_Shelf_Name')
    Status=models.BooleanField(default=True)
    Booking_Status=models.CharField(max_length=30,default='Available')
    created_by=models.CharField(max_length=70)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Tray_Master_Details'
    def __str__(self):
        return(self.Tray_Name)
    

# ------------------------------------------------------------------


class ProductCategory_Details(models.Model):
    ProductCategory_Id=models.AutoField(primary_key=True)
    ProductCategory_Name=models.CharField(max_length=70)
    Status=models.BooleanField(default=True)
    Created_by=models.CharField(max_length=100)
    Created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ProductCategory_Details'
    
    def __str__(self):
        return(self.ProductCategory_Name)
    

# ----------------------------------------------------
# bharathi

class ProductType_Master_Details(models.Model):
    ProductType_Id=models.AutoField(primary_key=True)
    ProductCategory=models.ForeignKey('Inventory.Product_Category_Product_Details', on_delete=models.CASCADE, null=True, blank=True)
    SubProductCategory=models.ForeignKey('Inventory.SubCategory_Detailes', on_delete=models.CASCADE, null=True, blank=True)
    ProductType_Name=models.CharField(max_length=100)
    Status=models.BooleanField(default=True)
    Create_by=models.CharField(max_length=70)
    Created_at=models.DateTimeField(auto_now_add=True)
    Updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ProductType_Master_Details'
    def __str__(self):
        return(self.ProductType_Name)
        

class Product_Group_Master_Details(models.Model):
    ProductGroup_Id=models.AutoField(primary_key=True)
    ProductCategory=models.ForeignKey('Inventory.Product_Category_Product_Details', on_delete=models.CASCADE, null=True, blank=True)
    SubProductCategory=models.ForeignKey('Inventory.SubCategory_Detailes', on_delete=models.CASCADE, null=True, blank=True)
    ProductGroup_Name=models.CharField(max_length=100)
    Status=models.BooleanField(default=True)
    Create_by=models.CharField(max_length=70)
    Created_at=models.DateTimeField(auto_now_add=True)
    Updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Drug_Group_Master_Details'
    def __str__(self):
        return(self.ProductGroup_Name)
    

# --------------------------------------------------------
    
class Pack_Type_Master_Details(models.Model):
    PackType_Id=models.AutoField(primary_key=True)
    ProductCategory=models.ForeignKey('Inventory.Product_Category_Product_Details', on_delete=models.CASCADE, null=True, blank=True)
    SubProductCategory=models.ForeignKey('Inventory.SubCategory_Detailes', on_delete=models.CASCADE, null=True, blank=True)
    PackType_Name=models.CharField(max_length=100)
    Status=models.BooleanField(default=True)
    Create_by=models.CharField(max_length=70)
    Created_at=models.DateTimeField(auto_now_add=True)
    Updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Pack_Type_Master_Details'
    def __str__(self):
        return(self.PackType_Name)
    

class GenericName_Master_Details(models.Model):
    GenericName_Id=models.AutoField(primary_key=True)
    ProductCategory=models.ForeignKey('Inventory.Product_Category_Product_Details', on_delete=models.CASCADE, null=True, blank=True)
    SubProductCategory=models.ForeignKey('Inventory.SubCategory_Detailes', on_delete=models.CASCADE, null=True, blank=True)
    GenericName=models.CharField(max_length=150)
    Status=models.BooleanField(default=True)
    Create_by=models.CharField(max_length=70)
    Updated_by=models.CharField(max_length=70)
    Created_at=models.DateTimeField(auto_now_add=True)
    Updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'GenericName_Master_Details'
    def __str__(self):
        return(self.GenericName)
    

class CompanyName_mfg_Master_Details(models.Model):
    CompanyName_Id=models.AutoField(primary_key=True)
    ProductCategory=models.ForeignKey('Inventory.Product_Category_Product_Details', on_delete=models.CASCADE, null=True, blank=True)
    SubProductCategory=models.ForeignKey('Inventory.SubCategory_Detailes', on_delete=models.CASCADE, null=True, blank=True)
    CompanyName =models.CharField(max_length=255)
    Status=models.BooleanField(default=True)
    Create_by=models.CharField(max_length=70)
    Updated_by=models.CharField(max_length=70)
    Created_at=models.DateTimeField(auto_now_add=True)
    Updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'CompanyName_mfg_Master_Details'
    def __str__(self):
        return (self.CompanyName)




class Medical_Stock_FileUpload(models.Model):
    Product_Id=models.IntegerField(primary_key=True)
    Product_Name=models.CharField(max_length=200)
    Generic_Name=models.CharField(max_length=200)
    Item_Type = models.CharField(max_length=65, default="")
    Dosage = models.CharField(max_length=25, default="")
    Available_Qantity=models.IntegerField()

    class Meta:
        db_table='Medical_Stock_FileUpload'
    
    def __str__(self):
        return(self.Product_Name)
    


# --------------------------------------------------------------


class Tray_management_Details(models.Model):
    Tray_Management_Id=models.AutoField(primary_key=True)
    Tray_Name=models.ForeignKey(Tray_Master_Details,on_delete=models.CASCADE,related_name='Tray_management_Name')
    Product_Detials = models.ForeignKey('Inventory.Product_Master_All_Category_Details', on_delete=models.CASCADE,related_name='Tray_Product_Master_All_Category_Details') 
    Create_by=models.CharField(max_length=70)
    Created_at=models.DateTimeField(auto_now_add=True)
    Updated_at=models.DateTimeField(auto_now=True)


    class Meta:
        db_table='Tray_management_Details'
    
    



class Prev_Tray_management_Details(models.Model):
    Prev_Tray_Management_Id=models.AutoField(primary_key=True)
    Prev_Tray_Name=models.ForeignKey(Tray_Master_Details,on_delete=models.CASCADE,related_name='Tray_management_Prev_Tray_Name')
    Prev_Product_Detials = models.ForeignKey('Inventory.Product_Master_All_Category_Details', on_delete=models.CASCADE,related_name='Prev_Tray_Product_Master_All_Category_Details') 
    Create_by=models.CharField(max_length=70)
    Created_at=models.DateTimeField(auto_now_add=True)
    Updated_at=models.DateTimeField(auto_now=True)


    class Meta:
        db_table='Prev_Tray_management_Details'


class ICDCode_Masterdata_FileUpload (models.Model):
    ICDCode=models.CharField(max_length=50,primary_key=True)
    ICDCode_Description=models.TextField()
    Diagnosis=models.TextField(null=True,default=None)
    CreatedBy = models.CharField(max_length=50,default='admin')
    CreatedAt = models.DateTimeField(auto_now_add=True)

 
class TherapyType_Detials(models.Model):
    TherapyType_Id = models.AutoField(primary_key=True)
    TherapyType_Name = models.ForeignKey(Speciality_Detials,on_delete=models.CASCADE)
    Therapy_Name = models.CharField(max_length=130)
    Sub_Therapy_Name = models.CharField(max_length=150)
    Description = models.TextField()
    IsMedications = models.BooleanField(default=True)
    IpAmount = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    OpAmount = models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    OldIpAmount =  models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    OldOpAmount =  models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    IsGst = models.BooleanField(default=True)
    GSTvalue = models.IntegerField()
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        db_table = 'TherapyType_Detials'
 
 
 

class Service_Master_Table(models.Model):
    Service = models.CharField(max_length=100, blank=True,null=True)
    Category = models.CharField(max_length=100, blank=True,null=True)
    Category_Type = models.CharField(max_length=100, blank=True,null=True)
    OP_Basic = models.FloatField(blank=True, null=True)
    OP_VIP = models.FloatField(blank=True, null=True)
    OP_INS = models.FloatField(blank=True, null=True)
    OP_Client = models.FloatField(blank=True, null=True)
    IP_VIP = models.FloatField(blank=True, null=True)
    IP_INS = models.FloatField(blank=True, null=True)
    IP_Client = models.FloatField(blank=True, null=True)
    Doctor_Rate_Card = models.ForeignKey(Doctor_Ratecard_Master,blank=True,null=True,on_delete=models.CASCADE)
    # Doctor_Contribution = models.FloatField(blank=True, null=True)
    Hospital_Contribution = models.FloatField(blank=True, null=True)
    Insurance_fee = models.ForeignKey(InsuranceFee,blank=True,null=True,on_delete=models.CASCADE)
    Client_fee = models.ForeignKey(ClientFee,blank=True,null=True,on_delete=models.CASCADE)
    Corporate_fee = models.ForeignKey(CorporateFee,blank=True,null=True,on_delete=models.CASCADE)
    Insurance_room_fee = models.ForeignKey(InsuranceRoomTypeFee,blank=True,null=True,on_delete=models.CASCADE)
    Client_room_fee = models.ForeignKey(ClientRoomTypeFee,blank=True,null=True,on_delete=models.CASCADE)
    Corporate_room_fee = models.ForeignKey(CorporateRoomTypeFee,blank=True,null=True,on_delete=models.CASCADE)
    

class Feedback_Details_Form(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    Feedback_Id = models.AutoField(primary_key=True)
    Identificationid =  GenericForeignKey('content_type', 'object_id')
    Identificationname =  models.CharField(max_length=150)
    QrName = models.CharField(max_length=40)
    Ratings = models.IntegerField()
    Feedback = models.CharField(max_length=30)
    Comments = models.TextField()
    Name = models.CharField(max_length=150)
    Phone = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Feedback_Details_Form'



#--------------------Lab Masters---------------

        
class Lab_Department_Detials(models.Model):
    Department_Code = models.CharField(primary_key=True,max_length=10)
    Department_Name = models.CharField(max_length=30)
    Status = models.CharField(max_length=10)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Lab_Department_Detials'



class SubLab_Department_Detials(models.Model):
    SubDepartment_Code = models.CharField(primary_key=True, max_length=10)
    SubDepartment_Name = models.CharField(max_length=255)
    Status = models.CharField(max_length=10)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    department = models.ForeignKey(Lab_Department_Detials, on_delete=models.CASCADE, related_name='subdepartments')
    class Meta:
        db_table = 'SubLab_Department_Detials'


class DepartmentOrderMaster(models.Model):
    S_No = models.IntegerField(primary_key=True)
    SubDepartment_Code = models.ForeignKey('SubLab_Department_Detials', on_delete=models.CASCADE)  # Mandatory
    OrderID = models.IntegerField()
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'DepartmentOrderMaster'


  


    
    
class Lab_Details(models.Model):
    Lab_Id = models.IntegerField(primary_key=True)
    Lab_name = models.CharField(max_length=255)
    Lab_Mail = models.CharField(max_length=30)
    Lab_PhoneNo = models.CharField(max_length=30)
    Lab_LandlineNo = models.CharField(max_length=30)
    Lab_GstNo = models.CharField(max_length=30)
    Lab_DoorNo = models.CharField(max_length=30)
    Lab_Street = models.CharField(max_length=30)
    Clinic_Area = models.CharField(max_length=30)
    Clinic_City = models.CharField(max_length=30)
    Clinic_Pincode = models.CharField(max_length=30)
    Clinic_State = models.CharField(max_length=30)
    Clinic_Country = models.CharField(max_length=30)
    created_by = models.CharField(max_length=30)
    Location = models.ForeignKey(Location_Detials, on_delete=models.CASCADE,related_name='Lab_Clinic_location',null=True,blank=True,default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Lab_Details'


# class AccountMasterEntryDetails(models.Model):
#     AccountID = models.BigIntegerField(primary_key=True)
#     Account_Create_date = models.CharField(max_length=50)
#     Account_Name = models.CharField(max_length=50, unique=True)
#     Account_Type = models.CharField(max_length=50)
#     Opening_Balance = models.DecimalField(max_digits=10, decimal_places=3)
#     Current_Balance = models.DecimalField(max_digits=10, decimal_places=3)
#     Credit_Amount = models.DecimalField(max_digits=10, decimal_places=3)
#     Debit_Amount = models.DecimalField(max_digits=10, decimal_places=3)
#     BankDetailes = models.CharField(max_length=8)
#     PhoneNumber = models.CharField(max_length=255)
#     PAN_OR_IT_NO = models.CharField(max_length=100)
#     Account_Holder_Name = models.CharField(max_length=150)
#     Bank_Name = models.CharField(max_length=150)
#     Account_Number = models.CharField(max_length=100)
#     Branch = models.CharField(max_length=150)
#     IFSC_Code = models.CharField(max_length=100)
#     Pan_No = models.CharField(max_length=50)
#     CreatedBy = models.CharField(max_length=50)
#     Location = models.CharField(max_length=50)
#     UpdatedAt = models.DateTimeField(auto_now=True)
#     CreatedAt = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         db_table = 'AccountMaster_Entry_Details'



class Unit_Masters(models.Model):
    Unit_Code = models.CharField(primary_key=True,max_length=10)
    Unit_Name = models.CharField(max_length=30)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Unit_Masters'

class Specimen_Masters(models.Model):
    Specimen_Code = models.CharField(primary_key=True,max_length=10)
    Specimen_Name = models.CharField(max_length=255)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Specimen_Masters'
        
class Container_Masters(models.Model):
    Container_Code = models.CharField(primary_key=True,max_length=10)
    Container_Name = models.CharField(max_length=255)
    ColorFlag = models.CharField(max_length=15)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Container_Masters'

class Methods_Masters(models.Model):
    Method_Code = models.CharField(primary_key=True,max_length=10)
    Method_Name = models.CharField(max_length=255)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Methods_Masters'


class AntibioticMaster(models.Model):
    anti_biotic_id = models.IntegerField(primary_key=True)
    anti_biotic_group_code = models.CharField(max_length=10)
    anti_biotic_code = models.CharField(max_length=10)
    anti_biotic = models.CharField(max_length=255)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'AntibioticMaster'




class Organism_Masters(models.Model):
    Organism_Code = models.CharField(primary_key=True,max_length=10)
    Organism_Name = models.CharField(max_length=255)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Organism_Masters'

class LabRemarksMaster(models.Model):
    LabRemarkID = models.CharField(primary_key=True,max_length=10)
    Department = models.CharField(max_length=100)
    LabRemarks = models.TextField()
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'LabRemarksMaster'

        
class Remarks_master(models.Model):
    Remark_Id = models.CharField(primary_key=True,max_length=10)
    Remarks = models.TextField()
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Remarks_master'

class Reason_master(models.Model):
    Reason_Id = models.CharField(primary_key=True,max_length=10)
    Reason = models.TextField()
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Reason_Master'

class Qualification_master(models.Model):
    Qualification_Id = models.CharField(primary_key=True,max_length=10)
    Qualification = models.CharField(max_length=255)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Qualification_Master'



class Test_Descriptions(models.Model):
    Test_Code = models.CharField(primary_key=True, max_length=10)  # Mandatory
    Test_Name = models.TextField()  # Mandatory
    department = models.ForeignKey('Lab_Department_Detials', on_delete=models.CASCADE)  # Mandatory
    sub_department = models.ForeignKey('SubLab_Department_Detials', on_delete=models.CASCADE)  # Mandatory
    Header = models.TextField(null=True, blank=True)
    Billing_Name = models.TextField(null=True, blank=True)
    DisplayText = models.TextField(null=True, blank=True)
    Container_Name = models.ForeignKey('Container_Masters', on_delete=models.CASCADE,null=True, blank=True)
    Specimen_Name = models.ForeignKey('Specimen_Masters', on_delete=models.CASCADE, null=True, blank=True)
    Method_Name = models.ForeignKey('Methods_Masters', on_delete=models.CASCADE, null=True, blank=True)
    Gender = models.CharField(max_length=15)  # Mandatory
    Input_Type = models.CharField(max_length=25, null=True, blank=True)
    Decimal_Palces = models.IntegerField(null=True, blank=True)
    Input_Pattern_Type = models.CharField(max_length=25, null=True, blank=True)
    Test_Category = models.CharField(max_length=25, null=True, blank=True)
    Logical_Category = models.CharField(max_length=25, null=True, blank=True)
    Captured_Unit = models.IntegerField(null=True, blank=True)
    Captured_Unit_UOM = models.CharField(max_length=15, null=True, blank=True)
    UOM = models.ForeignKey('Unit_Masters', on_delete=models.CASCADE, null=True, blank=True)
    Report_Type = models.CharField(max_length=50, null=True, blank=True)
    Test_Instructions = models.CharField(max_length=255, null=True, blank=True)
    Loinc_Code = models.CharField(max_length=50, null=True, blank=True)
    Allow_Discount = models.CharField(max_length=20, null=True, blank=True)
    Oderable = models.CharField(max_length=30, null=True, blank=True)
    Show_Graph = models.CharField(max_length=30, null=True, blank=True)
    STAT = models.CharField(max_length=30, null=True, blank=True)
    Non_Reportable = models.CharField(max_length=30, null=True, blank=True)
    Calculated_Test = models.CharField(max_length=30, null=True, blank=True)
    Outsourced = models.CharField(max_length=30, null=True, blank=True)
    Processing_Time = models.CharField(max_length=30, null=True, blank=True)
    Emergency_Processing_Time = models.CharField(max_length=30, null=True, blank=True)
    Period_Type = models.CharField(max_length=20, null=True, blank=True)
    Formula = models.CharField(max_length=155, null=True, blank=True)
    Routine = models.CharField(max_length=200, null=True, blank=True)
    TimeGap = models.CharField(max_length=200, null=True, blank=True)
    Autocheck = models.CharField(max_length=20, null=True, blank=True)
    Culturetest = models.CharField(max_length=20, null=True, blank=True)
    Is_NABHL = models.CharField(max_length=20, null=True, blank=True)
    Is_CAP = models.CharField(max_length=20, null=True, blank=True)
    Is_Machine_Interfaced = models.CharField(max_length=20, null=True, blank=True)
    Machine_Name = models.CharField(max_length=254, null=True, blank=True)
    # Reagent_Level = models.CharField(max_length=50, null=True, blank=True)
    # Reagent_Level_UOM = models.CharField(max_length=15, null=True, blank=True)
    Assay_Code = models.CharField(max_length=25, null=True, blank=True)
    Status = models.CharField(max_length=20, null=True, blank=True)
    IsSubTest = models.CharField(max_length=10, null=True, blank=True)
    SubTestCodes = models.CharField(max_length=255, null=True, blank=True)
    ResultValues = models.TextField(null=True, blank=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Test_Descriptions'

        
class Testmaster_Remarks(models.Model):
    Test_Id = models.IntegerField(primary_key=True) 
    # Test_Name = models.CharField(max_length=255)  
    Test_Code = models.ForeignKey('Test_Descriptions', on_delete=models.CASCADE)  
    Validation = models.CharField(max_length=255,null=True, blank=True)
    Remark_Type = models.TextField(null=True, blank=True)
    Remark = LongTextField(null=True, blank=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Testmaster_Remarks'

class Testmaster_Reference_Range(models.Model):
    Test_Id = models.IntegerField(primary_key=True) 
    # Test_Name = models.CharField(max_length=255)  
    Test_Code = models.ForeignKey('Test_Descriptions', on_delete=models.CASCADE)  
    Analizer_Type = models.CharField(max_length=355,null=True, blank=True)
    validation = models.CharField(max_length=255,null=True, blank=True)
    Method_Type = models.CharField(max_length=255,null=True, blank=True)
    Gender = models.CharField(max_length=50,null=True, blank=True)
    Range_Lower_Limit = models.IntegerField(null=True, blank=True)
    Range_Higher_Limit = models.IntegerField(null=True, blank=True)
    Reference_Range_Text = models.TextField(null=True, blank=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Testmaster_Reference_Range'

class Group_Master(models.Model):
    Group_Code = models.CharField(primary_key=True,max_length=10)
    Group_Name = models.CharField(max_length=255)
    Display_Name = models.CharField(max_length=255)
    Billing_Code = models.CharField(max_length=10,null=True,blank=True)
    Billing_Name = models.CharField(max_length=255)
    Gender = models.CharField(max_length=255)
    Report_Type = models.CharField(max_length=255)
    Department = models.ForeignKey(SubLab_Department_Detials,on_delete=models.CASCADE)
    Test_Category = models.CharField(max_length=255,null=True,blank=True)
    Logical_Category = models.CharField(max_length=25,null=True,blank=True)
    AutoAuthorized_User = models.CharField(max_length=255,null=True,blank=True)
    Lonic_Code = models.CharField(max_length=255,null=True,blank=True)
    Status = models.CharField(max_length=15)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Group_Master'
        
class Group_Master_TestList(models.Model):
    Group_Master_TestList_Id = models.CharField(primary_key=True,max_length=10)
    Group_Code = models.ForeignKey(Group_Master,on_delete=models.CASCADE)
    Test_Code = models.ForeignKey(Test_Descriptions, on_delete=models.CASCADE)  
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Group_Master_TestList'
        
class Testmaster_Cost_List(models.Model):
    Test_Id = models.IntegerField(primary_key=True) 
    # Test_Name = models.CharField(max_length=255)  
    Test_Code = models.ForeignKey(Test_Descriptions, on_delete=models.CASCADE,null=True,blank=True)  
    Group_Code = models.ForeignKey(Group_Master,on_delete=models.CASCADE,null=True,blank=True)
    Basic = models.DecimalField(max_digits=10, decimal_places=3)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Testmaster_Cost_List' 
        

class Testmaster_Rule_Based(models.Model):
    Test_Id = models.IntegerField(primary_key=True) 
    # Test_Name = models.CharField(max_length=255)  
    Test_Code = models.ForeignKey('Test_Descriptions', on_delete=models.CASCADE)  
    Validation_type = models.CharField(max_length=255,null=True, blank=True)
    Gender = models.CharField(max_length=50,null=True, blank=True)
    Rule_Type = models.CharField(max_length=300,null=True, blank=True)
    Remark = models.TextField(null=True, blank=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Testmaster_Rule_Based' 

class Testmaster_Interpretation_table(models.Model):
    Test_Id = models.IntegerField(primary_key=True) 
    # Test_Name = models.CharField(max_length=255)  
    Test_Code = models.ForeignKey('Test_Descriptions', on_delete=models.CASCADE)  
    Header_interpretation = models.CharField(max_length=255,null=True, blank=True)
    Comments = LongTextField(null=True, blank=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Testmaster_Interpretation_table' 


class Testmaster_Reflex_Test(models.Model):
    Test_Id = models.IntegerField(primary_key=True) 
    # Test_Name = models.CharField(max_length=255)  
    Test_Code = models.ForeignKey('Test_Descriptions', on_delete=models.CASCADE)  
    Reflex_Test = models.CharField(max_length=255,null=True, blank=True)
    Reflex_Code = models.CharField(max_length=20,null=True, blank=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Testmaster_Reflex_Test' 

class Age_Setup_Master(models.Model):
    Test_Id = models.IntegerField(primary_key=True) 
    # Test_Name = models.CharField(max_length=255)  
    Test_Code = models.ForeignKey('Test_Descriptions', on_delete=models.CASCADE)  
    Gender = models.CharField(max_length=50)
    FromAge = models.IntegerField(null=True, blank=True)
    FromAgeType = models.CharField(max_length=50,null=True, blank=True)
    Toage = models.IntegerField(null=True, blank=True)
    ToAgeType = models.CharField(max_length=50,null=True, blank=True)
    From_Value = models.CharField(max_length=50,null=True, blank=True)
    To_Value = models.CharField(max_length=50,null=True, blank=True)
    PanicLow = models.CharField(max_length=50,null=True, blank=True)
    PanicHigh = models.CharField(max_length=50,null=True, blank=True)
    NormalValue = models.CharField(max_length=50,null=True, blank=True)
    Reference_Range = LongTextField(null=True, blank=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Age_Setup_Master' 


class External_Lab_Master(models.Model):

    LabCode = models.CharField(primary_key=True,max_length=10)
    LabName = models.CharField(max_length=255)
    RegisterNo = models.IntegerField(null=True,blank=True)
    Address = models.TextField()
    Email = models.CharField(max_length=255,null=True,blank=True)
    PhoneNo = models.CharField(max_length=255,null=True,blank=True)
    Pincode = models.IntegerField(null=True,blank=True)
    ReferenceCode = models.CharField(null=True,blank=True,max_length=255)
    Location = models.CharField(max_length=255)
    SourceType = models.CharField(max_length=255)
    Status = models.CharField(max_length=15)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'External_Lab_Master'


class Refering_Doctor_Details(models.Model):
    DoctorID = models.CharField(primary_key=True,max_length=10)
    Title = models.CharField(max_length=255)
    DoctorName = models.CharField(max_length=255)
    Qualification = models.ForeignKey(Qualification_master,on_delete=models.CASCADE,null=True,blank=True)
    DoctorType = models.CharField(max_length=255)
    PhoneNo = models.CharField(max_length=255)
    Commission_per = models.CharField(max_length=255)
    PaymentType = models.CharField(max_length=255)
    BankName = models.CharField(max_length=255,null=True,blank=True)
    HolderName = models.CharField(max_length=255,null=True,blank=True)
    AccountNo = models.CharField(max_length=255,null=True,blank=True)
    Address = models.TextField()
    Address2 = models.TextField()
    Status = models.CharField(max_length=15)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Refering_Doctor_Details'

 
class Alert_Message_Register(models.Model):
    Alert_id = models.AutoField(primary_key=True)
    Empolyee_id = models.ForeignKey(Employee_Personal_Form_Detials, on_delete= models.CASCADE,null=True,blank=True)
    Alert_Color = models.CharField(max_length=70)
    Alert_Message = models.CharField(max_length=200)
    created_by = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        db_table = 'Alert_Message_Register'
 
 
 

# class IP_DischargeSummary(models.Model):
#     Id = models.AutoField(primary_key=True)
#     Ip_Registration_Id = models.ForeignKey(Patient_IP_Registration_Detials, on_delete=models.CASCADE, related_name='IP_Discharge_Ip_Registration_Id',null=True,blank=True)
#     Casuality_Registration_Id = models.ForeignKey(Patient_Casuality_Registration_Detials, on_delete=models.CASCADE, related_name='IP_Discharge_Casuality_Registration_Id',null=True,blank=True)
#     FinalDiagnosis = models.TextField()
#     PresentingComplaints = models.TextField()
#     PastMedicalHistory = models.TextField()
#     AllergyHistory = models.TextField()
#     Vitals = models.TextField()
#     DischargeNotes = models.TextField()
#     Referdoctor = models.TextField()
#     ConditionOnDischarge = models.TextField()
#     PrescriptionSummary = models.TextField()
#     NoOfDays = models.CharField(max_length=30,blank=True)
#     TimeInterval = models.CharField(max_length=30,blank=True)
#     Date = models.CharField(max_length=30,blank=True)
#     DietAdvice = models.CharField(max_length=300,blank=True)
#     Emergency = models.CharField(max_length=300,blank=True)
#     AdviceOnDischarge = models.TextField()
#     DoctorSchedule = models.TextField()
#     DepartmentType = models.CharField(max_length=30,blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     Created_by = models.CharField(max_length=30)
#     class Meta:
#         db_table = 'IP_DischargeSummary'
 
 
# Administration
class Administration_Master_Details(models.Model):
    Administration_Id = models.AutoField(primary_key=True)
    Administration_Name = models.CharField(max_length=50)
    Building_Name = models.ForeignKey(Building_Master_Detials,on_delete=models.CASCADE,related_name='Administration_Building_name')
    Block_Name = models.ForeignKey(Block_Master_Detials,on_delete=models.CASCADE,related_name='Administration_Block_name')
    Floor_Name = models.ForeignKey(Floor_Master_Detials,on_delete=models.CASCADE,related_name='Administration_Floor_name')
    Location_Name = models.ForeignKey(Location_Detials,on_delete=models.CASCADE,related_name='Administration_location_name')
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=80, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        db_table = 'Administration_Master_Details'
   
    def str(self):
        return self.Administration_Name
 
class NurseStationMaster(models.Model):
    NurseStationid = models.AutoField(primary_key=True)
    NurseStationName = models.CharField(max_length=255)
    Building_Name = models.ForeignKey(Building_Master_Detials,on_delete=models.CASCADE)
    Block_Name = models.ForeignKey(Block_Master_Detials,on_delete=models.CASCADE)
    Floor_Name = models.ForeignKey(Floor_Master_Detials,on_delete=models.CASCADE)
    Location_Name = models.ForeignKey(Location_Detials,on_delete=models.CASCADE)
    Status = models.BooleanField(default=True)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "NurseStationMaster"

class NurseStationMasterDetails(models.Model):
    NurseStationDetailsid = models.AutoField(primary_key=True)
    NurseStationid = models.ForeignKey(NurseStationMaster,on_delete=models.CASCADE)
    Wardid = models.ForeignKey(WardType_Master_Detials,on_delete=models.CASCADE)
    created_by = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "NurseStationMasterDetails"



class Disease_Master (models.Model):
    DiseaseCode = models.CharField(max_length=50,primary_key=True)
    DiseaseName = models.CharField(max_length=50)
    IsChronicle = models.CharField(null=True,max_length=50)
    IsCommunicable = models.CharField(null=True,max_length=50)
    CreatedBy = models.CharField(max_length=50,default='admin')
    CreatedAt = models.DateTimeField(auto_now_add=True)
 
    class Meta:
         db_table = 'Disease_Master'
 


class Services_Group_Details(models.Model):
 
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    service_category = models.ForeignKey(Service_Category_Masters,on_delete=models.CASCADE)
    service_sub_category = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    class Meta:
        db_table = 'Services_Group_Details'
 
 
class Package_Master(models.Model):
 
      Package_Name = models.CharField(max_length=255,null=True,blank=True)
      PackageType = models.CharField(max_length=255,null=True,blank=True)
      Price = models.CharField(max_length=20,blank=True,null=True)
      Status = models.CharField(null=True,max_length=50)
      Discount = models.CharField(null=True,max_length=50)
      Validity = models.CharField(max_length=255,null=True,blank=True)
      Fromdate = models.DateField()
      Todate = models.DateField()
      Specialist = models.ForeignKey(Speciality_Detials,on_delete=models.CASCADE,null=True,blank=True)
 
      Services_details = models.JSONField(blank=True,null=True)
 
      class Meta:
         db_table = 'Package_Master'