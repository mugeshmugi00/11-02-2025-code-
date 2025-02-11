from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from Masters.models import *
from .models import *
import json
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
# import magic
import filetype
import base64
from django.db.models import Q
from django.db import transaction







@csrf_exempt
@require_http_methods(["POST", "OPTIONS", "GET"])
def Employee_Registration_Details(request):
    
    @transaction.atomic
    def validate_and_process_file(file):
        def get_file_type(file):
            if file.startswith('data:application/pdf;base64'):
                return 'application/pdf'
            elif file.startswith('data:image/jpeg;base64') or file.startswith('data:image/jpg;base64'):
                return 'image/jpeg'
            elif file.startswith('data:image/png;base64'):
                return 'image/png'
            else:
                return 'unknown'

        def compress_image(image, min_quality=10, step=5):
            output = BytesIO()
            quality = 95
            compressed_data = None
            while quality >= min_quality:
                output.seek(0)
                image.save(output, format='JPEG', quality=quality)
                compressed_data = output.getvalue()
                quality -= step
            output.seek(0)
            compressed_size = len(compressed_data)
            return compressed_data, compressed_size

        def compress_pdf(file):
            output = BytesIO()
            reader = PdfReader(file)
            writer = PdfWriter()
            for page_num in range(len(reader.pages)):
                writer.add_page(reader.pages[page_num])
            writer.write(output)
            compressed_data = output.getvalue()
            compressed_size = len(compressed_data)
            return compressed_data, compressed_size

        if file:
            file_data = file.split(',')[1] if ',' in file else file
            file_content = base64.b64decode(file_data)
            file_size = len(file_content)
            max_size_mb = 5

            if file_size > max_size_mb * 1024 * 1024:
                return JsonResponse({'warn': f'File size exceeds the maximum allowed size ({max_size_mb}MB)'})

            file_type = get_file_type(file)

            if file_type in ['image/jpeg', 'image/png']:
                try:
                    image = Image.open(BytesIO(file_content))
                    if image.mode in ('RGBA', 'P'):
                        image = image.convert('RGB')
                    compressed_image_data, compressed_size = compress_image(image)
                    return compressed_image_data
                except Exception as e:
                    return JsonResponse({'error': f'Error processing image: {str(e)}'})

            elif file_type == 'application/pdf':
                try:
                    compressed_pdf_data, compressed_size = compress_pdf(BytesIO(file_content))
                    return compressed_pdf_data
                except Exception as e:
                    return JsonResponse({'error': f'Error processing PDF: {str(e)}'})

            else:
                return JsonResponse({'warn': 'Unsupported file format'})

        return None
    
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            print(data,'dataaa')
            
            # Extract and validate data
            Title = data.get('Title','')
            FirstName = data.get('FirstName','')
            MiddleName = data.get('MiddleName','')
            SurName = data.get('SurName','')
            Gender = data.get('gender','')
            Dob = data.get('dob','')
            Age = data.get('Age','')
            BloodGroup = data.get('bloodgroup','')
            Phone = data.get('phone','')
            AlternatePhone = data.get('alternatePhone','')
            Email = data.get('email','')
            Qualification = data.get('qualification','')
            SkillSet = data.get('SkillSet','')
            IdProofType = data.get('IdProofType','')
            IdProofNo = data.get('IdProofNo','')
            maritalStatus = data.get('maritalStatus','')
            MarriagePlan = data.get('MarriagePlan','')
            AnniversaryDate = data.get('AnniversaryDate','')
            Residence = data.get('Residence','')
            FatherName = data.get('FatherName','')
            FatherContact = data.get('FatherContact','')
            FatherWorking = data.get('FatherWorking','')
            FatherWorkPlace = data.get('FatherWorkPlace','')
            MotherName = data.get('MotherName','')
            MotherContact = data.get('MotherContact','')
            MotherWorking = data.get('MotherWorking','')
            MotherWorkPlace = data.get('MotherWorkPlace','')
            SpouseName = data.get('SpouseName','')
            SpouseContact = data.get('SpouseContact','')
            SpouseWorking = data.get('SpouseWorking','')
            SpouseWorkPlace = data.get('SpouseWorkPlace','')
            Child = data.get('Child','')
            TotalNoChild = data.get('TotalNoChild','')
            DoorNo = data.get('doorNo','')
            Street = data.get('Street','')
            Area = data.get('Area','')
            City = data.get('City','')
            District = data.get('District','')
            State = data.get('State','')
            Country = data.get('Country','')
            Pincode = data.get('Pincode','')
            PermanentAddressSameAsAbove = data.get('PermanentAddressSame','')
            PermanentDoorNo = data.get('PermanentdoorNo','')
            PermanentStreet = data.get('PermanentStreet','')
            PermanentArea = data.get('PermanentArea','')
            PermanentCity = data.get('PermanentCity','')
            PermanentDistrict = data.get('PermanentDistrict','')
            PermanentState = data.get('PermanentState','')
            PermanentCountry = data.get('PermanentCountry','')
            PermanentPincode = data.get('PermanentPincode','')            
            EmergencyContactName1 = data.get('EmergencyContactName1','')
            EmergencyContactNo1 = data.get('EmergencyContactNo1','')
            EmergencyContactName2 = data.get('EmergencyContactName2','')
            EmergencyContactNo2 = data.get('EmergencyContactNo2','')
            status = True
            Photo = data.get('Photo', None)
            CaptureImage = data.get('CaptureImage', None)
            ActiveStatus = data.get('ActiveStatus', '')
            RequirementSource = data.get('RequirementSource', '')
            Source = data.get('Source', '')


            PreExistingMedicalCondition = data.get('PreExistingMedicalCondition', '')
            PsychiatricMedicines = data.get('PsychiatricMedicines', '')
            PsychiatricMedicinesDetails = data.get('PsychiatricMedicinesDetails', '')
            PreviousOperation = data.get('PreviousOperation', '')
            SurgeriesDetails = data.get('SurgeriesDetails', '')
            VaccinationStatus = data.get('VaccinationStatus', '')
            VaccinationStatusDetails = data.get('VaccinationStatusDetails', '')
            MedicalFitnessCertificate = data.get('MedicalFitnessCertificate', None)
            AnnualMedicalCheckup = data.get('AnnualMedicalCheckup', None)
            PreviousWorkPFNumber = str(data.get('PreviousPfnumber', '')).strip()
            PreviousWorkESINumber = str(data.get('PreviousESInumber', '')).strip()
            PFNumber = str(data.get('PFnumber', '')).strip()
            ESINumber = str(data.get('ESInumber', '')).strip()
            PreviousWorkExperience = str(data.get('PreviousWorkExperience', '')).strip()

        
            NoOfYears = data.get('NoOfYears', '')
            WorkStationNameAddress = data.get('WorkStationNameAddress', '')
            WorkStationPhoneNo = data.get('WorkStationPhoneNo', '')
            ReasonForLeft = data.get('ReasonForLeft', '')
            ConfirmedBy = data.get('ConfirmedBy', '')
            EmployeePaySlip = data.get('EmployeePaySlip', None)
            EmployeeOfferLetter = data.get('EmployeeOfferLetter', None)
            EmployeeReliveLetter = data.get('EmployeeReliveLetter', None)
           
            DateOfJoining = data.get('DateOfJoining', '')
            Classification = data.get('Classification','')
            Role = data.get('Role','')
            DepartmentId = data.get('DepartmentId',"")
            DepartmentId= DepartmentId.split(', ') if DepartmentId else None
            Category = data.get('Category', '')
            Speciality = data.get('Speciality', '')
            
            Designation = data.get('Designation', '')
            Locations = data.get('Locations', '')
            WorkEmail = data.get('WorkEmail', '')
            ReportingManager = data.get('ReportingManager', '')
            GovtLeave = data.get('GovtLeave', '')
            CasualLeave = data.get('CasualLeave', '')
            SickLeave = data.get('SickLeave', '')
            TotalLeave = data.get('TotalLeave', '')
            ProbationPeriod = data.get('ProbationPeriod', '')
            Months = data.get('months', '')
            Years = data.get('years', '')
            TrainingGivenBy = data.get('TrainingGivenBy', '')
            TrainingVerifiedBy = data.get('TrainingVerifiedBy', '')
            TrainingCompletedDate = data.get('TrainingCompletedDate', '')
            IsPF_Applicable = data.get('IsPF_Applicable',0)
            print("IsPF_Applicable",IsPF_Applicable)
   
            BasicSalarystr = data.get('BasicSalary', 0)
            BasicSalary = float(BasicSalarystr) if BasicSalarystr != '' else 0
 
            Salarystr = data.get('Salary', 0)
            Salary = float(Salarystr) if Salarystr !='' else 0

            strAllowance = data.get('Allowance', 0)
            Allowance = float(strAllowance) if strAllowance != '' else 0

          
            FinalAllowancestr = data.get('FinalAllowance',0)
            FinalAllowance = float(FinalAllowancestr) if FinalAllowancestr !='' else 0
            
            PfForEmployeestr = data.get('PfForEmployee', 0) 
            print("bharathi",PfForEmployeestr)

            SecurityDepositestr = data.get('SecurityDeposite', 0)
            SecurityDeposite = float(SecurityDepositestr) if SecurityDepositestr !='' else 0

      
            AccountHolderName = data.get('AccountHolderName', '')
            AccountNumber = data.get('AccountNumber', '')
            BankName = data.get('BankName', '')
            Branch = data.get('Branch', '')
            IfscCode = data.get('IfscCode', '')
            PanNumber = data.get('PanNumber', '')
            UploadCsvFile = data.get('UploadCsvFile', None)

            Resume = data.get('Resume', None)
            PanCard = data.get('PanCard', None)
            AadharCard = data.get('AadharCard', None)
            BankPassbook = data.get('BankPassbook', None)
            ExperienceCertificate = data.get('ExperienceCertificate', None)
            MedicalFitness = data.get('MedicalFitness', None)
            Offerletter = data.get('Offerletter', None)
            Signature = data.get('Signature', None)
            created_by = data.get('Createdby', '')
            Location = data.get('Location', '')
            Employee_Id = data.get('Employee_Id', '')
            
            location_instance = Location_Detials.objects.get(Location_Id=Location) if Location else None
            Emp_location_instance = Location_Detials.objects.get(Location_Id=Locations) if Locations else None
            Title_instance = Title_Detials.objects.get(Title_Id=Title) if Title else None
            BloodGroup_instance = BloodGroup_Detials.objects.get(BloodGroup_Id=BloodGroup) if BloodGroup else None
            Classification_instance = Classification_Detials.objects.get(pk=Classification) if Classification else None
            Role_instance = Role_Master.objects.get(pk=Role) if Role else None
            Designation_instance = Designation_Detials.objects.get(pk=Designation) if Designation else None
            Speciality_instance = Speciality_Detials.objects.get(Speciality_Id=Speciality) if Speciality else None
            Category_instance = Category_Detials.objects.get(pk=Category) if Category else None

            Department_instance =None
            print('DepartmentId11111',DepartmentId)
            if DepartmentId and DepartmentId not in ['null', 'undefined','']:
                print('DepartmentId222222',DepartmentId)
                Department_instance = Department_Detials.objects.filter(Department_Id__in = DepartmentId)
                print('Department_instance111111',Department_instance)    


            if IsPF_Applicable == True:
                PfForEmployee = float(PfForEmployeestr) if PfForEmployeestr else 0
            elif IsPF_Applicable == False:
                
                PfForEmployee = 0.0  # Set to 0 when PF is not applicable

           

            
            CaptureImageDocument = validate_and_process_file(CaptureImage) if Photo  else None

            PhotoChooseDocument = validate_and_process_file(Photo) if Photo  else None
            MedicalFitnessCertificateDocument = validate_and_process_file(MedicalFitnessCertificate) if MedicalFitnessCertificate  else None
            AnnualMedicalCheckupDocument = validate_and_process_file(AnnualMedicalCheckup) if AnnualMedicalCheckup  else None
            EmployeePaySlipDocument = validate_and_process_file(EmployeePaySlip) if EmployeePaySlip  else None
            EmployeeOfferLetterDocument = validate_and_process_file(EmployeeOfferLetter) if EmployeeOfferLetter  else None
            EmployeeReliveLetterDocument = validate_and_process_file(EmployeeReliveLetter) if EmployeeReliveLetter  else None
            UploadCsvFileDocument = validate_and_process_file(UploadCsvFile) if UploadCsvFile  else None

            ResumeDocument = validate_and_process_file(Resume) if Resume  else None
            PanCardDocument = validate_and_process_file(PanCard) if PanCard  else None
            AadharCardDocument = validate_and_process_file(AadharCard) if AadharCard  else None
            BankPassbookDocument = validate_and_process_file(BankPassbook) if BankPassbook  else None
            ExperienceCertificateDocument = validate_and_process_file(ExperienceCertificate) if ExperienceCertificate  else None
            MedicalFitnessDocument = validate_and_process_file(MedicalFitness) if MedicalFitness  else None
            OfferletterDocument = validate_and_process_file(Offerletter) if Offerletter  else None
            SignatureDocument = validate_and_process_file(Signature) if Signature  else None
            
            with transaction.atomic():
                if Employee_Id:
                   

                    Employee = Employee_Personal_Form_Detials.objects.get(Employee_ID=Employee_Id)
                    
                    if not Employee:
                        return JsonResponse({'warn': f"The Employee Id is not valid"})

                    if Employee_Personal_Form_Detials.objects.filter(First_Name=FirstName,Contact_Number=Phone).exclude(Employee_ID=Employee_Id).exists():
                        Employee =  Employee_Personal_Form_Detials.objects.get(First_Name=FirstName,Contact_Number=Phone)    
                        return JsonResponse({'warn': f"The Employee {Employee.Employee_ID} is already registered with {Phone} and {FirstName}"})

                    Employee =  Employee_Personal_Form_Detials.objects.get(Employee_ID=Employee_Id)
                    Employee.Tittle = Title_instance
                    Employee.First_Name = FirstName
                    Employee.Middle_Name = MiddleName
                    Employee.Last_Name = SurName
                    Employee.Gender = Gender
                    Employee.DOB = Dob
                    Employee.Age = Age
                    Employee.BloodGroup = BloodGroup_instance
                    Employee.Contact_Number = Phone
                    Employee.Alternate_Number = AlternatePhone
                    Employee.E_mail = Email
                    Employee.Qualification = Qualification
                    # Employee.SkillSet = SkillSet
                    Employee.IdProofType = IdProofType
                    Employee.IdProofNo = IdProofNo
                    Employee.Marital_Status = maritalStatus
                    Employee.MarriagePlan = MarriagePlan
                    Employee.AnniversaryDate = AnniversaryDate
                    Employee.Residence = Residence
                    Employee.FatherName = FatherName
                    Employee.FatherContact = FatherContact
                    Employee.FatherWorking = FatherWorking
                    Employee.FatherWorkPlace = FatherWorkPlace
                    Employee.MotherName = MotherName
                    Employee.MotherContact = MotherContact
                    Employee.MotherWorking = MotherWorking
                    Employee.MotherWorkPlace = MotherWorkPlace
                    Employee.Spouse_Name = SpouseName
                    Employee.SpouseContact = SpouseContact
                    Employee.SpouseWorking = SpouseWorking
                    Employee.SpouseWorkPlace = SpouseWorkPlace
                    Employee.Child = Child
                    Employee.TotalNoChild = TotalNoChild
                    Employee.DoorNo = DoorNo
                    Employee.Street = Street
                    Employee.Area = Area
                    Employee.City = City
                    Employee.District = District
                    Employee.State = State
                    Employee.Country = Country
                    Employee.Pincode = Pincode
                    Employee.PermanentAddressSameAsAbove = PermanentAddressSameAsAbove
                    Employee.PermanentDoorNo = PermanentDoorNo
                    Employee.PermanentStreet = PermanentStreet
                    Employee.PermanentArea = PermanentArea
                    Employee.PermanentCity = PermanentCity
                    Employee.PermanentDistrict = PermanentDistrict
                    Employee.PermanentState = PermanentState
                    Employee.PermanentCountry = PermanentCountry
                    Employee.PermanentPincode = PermanentPincode
                    Employee.EmergencyContactName1 = EmergencyContactName1
                    Employee.EmergencyContactNo1 = EmergencyContactNo1
                    Employee.EmergencyContactName2 = EmergencyContactName2
                    Employee.EmergencyContactNo2 = EmergencyContactNo2
                    Employee.Photo = PhotoChooseDocument
                    Employee.CaptureImage = CaptureImageDocument
                    Employee.ActiveStatus = ActiveStatus
                    Employee.RequirementSource = RequirementSource
                    Employee.Source = Source
                    Employee.Status = status
                   
                    Employee.Location = location_instance
                    Employee.Category = Category_instance
                    Employee.Speciality = Speciality_instance
                    Employee.Classification = Classification_instance
                    Employee.Role = Role_instance
                    Employee.Designation = Designation_instance
                    Employee.created_by = created_by
                    Employee.Signature = SignatureDocument
                    Employee.save()

                    Employee.Department.set(Department_instance)
             

                    
                    skill_objects_to_create = []
                    for skill in SkillSet:
                        skill_name = skill.get("name")
                        skill_level = skill.get("level")

                        if skill_name and skill_level:
                            # Fetch the EmployeeSkillSets for the employee with the same skill name
                            employee_skill = Employee_Skills_Detials.objects.filter(Employee=Employee, Skill=skill_name).first()

                            if employee_skill:
                                # Update the skill level for existing skill
                                employee_skill.Level = skill_level
                                employee_skill.created_by = created_by
                                employee_skill.save()
                            else:
                                # If the skill does not exist, create a new skill record
                                skill_objects_to_create.append(Employee_Skills_Detials(Employee=Employee, Skill=skill_name, Level=skill_level, created_by=created_by))

                    # Bulk create new skill entries
                    if skill_objects_to_create:
                        Employee_Skills_Detials.objects.bulk_create(skill_objects_to_create)

                    EmployeeHistory = Employeement_History_Detials.objects.get(Employee__pk = Employee_Id)
                    EmployeeHistory.PreviousWorkExperience = PreviousWorkExperience
                    EmployeeHistory.PreviousWorkPFNumber=PreviousWorkPFNumber
                    EmployeeHistory.PreviousWorkESINumber=PreviousWorkESINumber
                    EmployeeHistory.PFNumber=PFNumber
                    EmployeeHistory.ESINumber=ESINumber
                    EmployeeHistory.NoOfYears = NoOfYears
                    EmployeeHistory.WorkStationNameAddress = WorkStationNameAddress
                    EmployeeHistory.ReasonForLeft = ReasonForLeft
                    EmployeeHistory.WorkStationPhoneNo = WorkStationPhoneNo
                    EmployeeHistory.EmployeePaySlip = EmployeePaySlipDocument
                    EmployeeHistory.EmployeeOfferLetter = EmployeeOfferLetterDocument
                    EmployeeHistory.EmployeeReliveLetter = EmployeeReliveLetterDocument
                    EmployeeHistory.ConfirmedBy = ConfirmedBy
                    EmployeeHistory.Location = location_instance
                    EmployeeHistory.created_by = created_by
                    EmployeeHistory.save()

                    EmpMedicalInfo = Employee_Medical_Information_Detials.objects.get(Employee__pk = Employee_Id)
                    EmpMedicalInfo.PreExisiting_Medical_Condition = PreExistingMedicalCondition
                    EmpMedicalInfo.PsychiatricMedicines = PsychiatricMedicines
                    EmpMedicalInfo.PsychiatricMedicinesDetails = PsychiatricMedicinesDetails
                    EmpMedicalInfo.PreviousOperation = PreviousOperation
                    EmpMedicalInfo.SurgeriesDetails = SurgeriesDetails
                    EmpMedicalInfo.VaccinationStatus = VaccinationStatus
                    EmpMedicalInfo.VaccinationStatusDetails = VaccinationStatusDetails
                    EmpMedicalInfo.MedicalFitnessCertificate = MedicalFitnessCertificateDocument
                    EmpMedicalInfo.AnnualMedicalCheckup = AnnualMedicalCheckupDocument
                    EmpMedicalInfo.Location = location_instance
                    EmpMedicalInfo.created_by = created_by
                    EmpMedicalInfo.save()

                    EmpCurrentHistory = Current_History_Detials.objects.get(Employee__pk = Employee_Id)
                    EmpCurrentHistory.DateOfJoining = DateOfJoining
                    EmpCurrentHistory.CurrentEmployeementLocations = Emp_location_instance
                    EmpCurrentHistory.ReportingManager = ReportingManager
                    EmpCurrentHistory.GovtLeave = GovtLeave
                    EmpCurrentHistory.CasualLeave = CasualLeave
                    EmpCurrentHistory.SickLeave = SickLeave
                    EmpCurrentHistory.TotalLeave = TotalLeave
                    EmpCurrentHistory.WorkEmail = WorkEmail
                    EmpCurrentHistory.ProbationPeriod = ProbationPeriod
                    EmpCurrentHistory.Months = Months
                    EmpCurrentHistory.Years = Years
                    EmpCurrentHistory.TrainingGivenBy = TrainingGivenBy
                    EmpCurrentHistory.TrainingVerifiedBy = TrainingVerifiedBy
                    EmpCurrentHistory.TrainingCompletedDate = TrainingCompletedDate
                    EmpCurrentHistory.IsPF_Applicable=IsPF_Applicable
                    EmpCurrentHistory.Location = location_instance
                    EmpCurrentHistory.created_by = created_by
                    EmpCurrentHistory.save()

                    EmpFinancialHistory = Financial_History_Detials.objects.get(Employee__pk = Employee_Id)
                    EmpFinancialHistory.Salary = Salary
                    EmpFinancialHistory.BasicSalary = BasicSalary
                    EmpFinancialHistory.Allowance = Allowance
                    EmpFinancialHistory.Allowancefinal = FinalAllowance
                    EmpFinancialHistory.PfForEmployee = PfForEmployee
                    EmpFinancialHistory.SecurityDeposite = SecurityDeposite
                    EmpFinancialHistory.AccountHolderName = AccountHolderName
                    EmpFinancialHistory.AccountNumber = AccountNumber
                    EmpFinancialHistory.BankName = BankName
                    EmpFinancialHistory.Branch = Branch
                    EmpFinancialHistory.IfscCode = IfscCode
                    EmpFinancialHistory.PanNumber = PanNumber
                    EmpFinancialHistory.UploadCsvFile = UploadCsvFileDocument
                    EmpFinancialHistory.Location = location_instance
                    EmpFinancialHistory.created_by = created_by
                    EmpFinancialHistory.save()


                    EmpDocuments = Document_Checklist_Detials.objects.get(Employee__pk = Employee_Id)
                    EmpDocuments.Resume = ResumeDocument 
                    EmpDocuments.PanCard = PanCardDocument 
                    EmpDocuments.AadharCard = AadharCardDocument 
                    EmpDocuments.BankPassbook = BankPassbookDocument 
                    EmpDocuments.ExperienceCertificate = ExperienceCertificateDocument 
                    EmpDocuments.MedicalFitness = MedicalFitnessDocument 
                    EmpDocuments.Offerletter = OfferletterDocument 
                    EmpDocuments.Location = location_instance 
                    EmpDocuments.created_by = created_by
                    EmpDocuments.save() 

                    return JsonResponse({'success': 'Employee Details updated successfully'})
                    
                else:
                    print("987")

                    Employee_instance = Employee_Personal_Form_Detials(
                    
                        Tittle=Title_instance,
                        First_Name=FirstName,
                        Middle_Name=MiddleName,
                        Last_Name=SurName,
                        Gender=Gender,
                        DOB=Dob,
                        Age=Age,
                        BloodGroup=BloodGroup_instance,
                        Contact_Number=Phone,
                        Alternate_Number=AlternatePhone,
                        E_mail=Email,
                        Qualification=Qualification,
                        # SkillSet=SkillSet,
                        IdProofType=IdProofType,
                        IdProofNo=IdProofNo,
                        Marital_Status=maritalStatus,
                        MarriagePlan=MarriagePlan,
                        AnniversaryDate=AnniversaryDate,
                        Residence=Residence,
                        FatherName=FatherName,
                        FatherContact=FatherContact,
                        FatherWorking=FatherWorking,
                        FatherWorkPlace=FatherWorkPlace,
                        MotherName=MotherName,
                        MotherContact=MotherContact,
                        MotherWorking=MotherWorking,
                        MotherWorkPlace=MotherWorkPlace,
                        Spouse_Name=SpouseName,
                        SpouseContact=SpouseContact,
                        SpouseWorking=SpouseWorking,
                        SpouseWorkPlace=SpouseWorkPlace,
                        Child=Child,
                        TotalNoChild=TotalNoChild,
                        DoorNo=DoorNo,
                        Street=Street,
                        Area=Area,
                        City=City,
                        District=District,
                        State=State,
                        Country=Country,
                        Pincode=Pincode,
                        PermanentAddressSameAsAbove=PermanentAddressSameAsAbove,
                        PermanentDoorNo=PermanentDoorNo,
                        PermanentStreet=PermanentStreet,
                        PermanentArea=PermanentArea,
                        PermanentCity=PermanentCity,
                        PermanentDistrict=PermanentDistrict,
                        PermanentState=PermanentState,
                        PermanentCountry=PermanentCountry,
                        PermanentPincode=PermanentPincode,
                        EmergencyContactName1=EmergencyContactName1,
                        EmergencyContactNo1=EmergencyContactNo1,
                        EmergencyContactName2=EmergencyContactName2,
                        EmergencyContactNo2=EmergencyContactNo2,
                        Photo=PhotoChooseDocument,
                        CaptureImage=CaptureImageDocument,
                        ActiveStatus=ActiveStatus,
                        RequirementSource=RequirementSource,
                        Source=Source,
                        Status=status,
                        Classification = Classification_instance,
                        Role = Role_instance,
                        Location=location_instance,
                        Category=Category_instance,
                        Speciality=Speciality_instance,
                       
                        Designation=Designation_instance,
                        created_by=created_by,
                        Signature=SignatureDocument,
                    )
                    Employee_instance.save()
                    print('vvvvvvveeeeee')
                    print('kkkkk-----',Department_instance)
                    Employee_instance.Department.set(Department_instance)
                    print("check2")
                    for skill in SkillSet:
                        skill_name = skill.get("name")
                        skill_level = skill.get("level")

                        if skill_name and skill_level:  # Ensure both fields are provided
                            Employee_Skills_Detials.objects.create(
                                Employee=Employee_instance,
                                Skill=skill_name,
                                Level=skill_level,
                                created_by=created_by
                            )

                    EmployeementHistory_instance = Employeement_History_Detials(
                        Employee=Employee_instance,
                        PreviousWorkExperience=PreviousWorkExperience,
                        PreviousWorkPFNumber=PreviousWorkPFNumber,
                        PreviousWorkESINumber=PreviousWorkESINumber,
                        PFNumber=PFNumber,
                        ESINumber=ESINumber,
                        NoOfYears=NoOfYears,
                        WorkStationNameAddress=WorkStationNameAddress,
                        ReasonForLeft=ReasonForLeft,
                        WorkStationPhoneNo=WorkStationPhoneNo,
                        EmployeePaySlip=EmployeePaySlipDocument,
                        EmployeeOfferLetter=EmployeeOfferLetterDocument,
                        EmployeeReliveLetter=EmployeeReliveLetterDocument,
                        ConfirmedBy=ConfirmedBy,
                        Location=location_instance,
                        created_by=created_by
                    )
                    EmployeementHistory_instance.save()

                    Employee_Medical_instance = Employee_Medical_Information_Detials(
                        EmployeementHistory = EmployeementHistory_instance,
                        Employee=Employee_instance,
                        PreExisiting_Medical_Condition = PreExistingMedicalCondition,
                        PsychiatricMedicines = PsychiatricMedicines,
                        PsychiatricMedicinesDetails = PsychiatricMedicinesDetails,
                        PreviousOperation = PreviousOperation,
                        SurgeriesDetails = SurgeriesDetails,
                        VaccinationStatus = VaccinationStatus,
                        VaccinationStatusDetails = VaccinationStatusDetails,
                        MedicalFitnessCertificate = MedicalFitnessCertificateDocument,
                        AnnualMedicalCheckup = AnnualMedicalCheckupDocument,
                        Location = location_instance,
                        created_by = created_by
                    )
                    Employee_Medical_instance.save()

                    CurrentEmployee_History_instance = Current_History_Detials(
                        EmployeeMedicalInfo = Employee_Medical_instance,
                        EmployeementHistory = EmployeementHistory_instance,
                        Employee=Employee_instance,
                        DateOfJoining = DateOfJoining,
                        CurrentEmployeementLocations=Emp_location_instance,
                        ReportingManager=ReportingManager,
                        GovtLeave=GovtLeave,
                        CasualLeave=CasualLeave,
                        SickLeave=SickLeave,
                        TotalLeave=TotalLeave,
                        WorkEmail=WorkEmail,
                        ProbationPeriod=ProbationPeriod,
                        Months=Months,
                        Years=Years,
                        TrainingGivenBy=TrainingGivenBy,
                        TrainingVerifiedBy=TrainingVerifiedBy,
                        TrainingCompletedDate=TrainingCompletedDate,
                        IsPF_Applicable=IsPF_Applicable,
                        Location = location_instance,
                        created_by = created_by
                    )
                    CurrentEmployee_History_instance.save()

                    Financial_History_instance = Financial_History_Detials(
                        EmployeeMedicalInfo = Employee_Medical_instance,
                        EmployeementHistory = EmployeementHistory_instance,
                        Employee=Employee_instance,
                        EmployeeCurrentHistoryInfo = CurrentEmployee_History_instance,
                        Salary = Salary,
                        BasicSalary = BasicSalary,
                        Allowance = Allowance,
                        Allowancefinal = FinalAllowance,

                        PfForEmployee = PfForEmployee,
                        SecurityDeposite = SecurityDeposite,
                        AccountHolderName = AccountHolderName,
                        AccountNumber = AccountNumber,
                        BankName = BankName,
                        Branch = Branch,
                        IfscCode = IfscCode,
                        PanNumber = PanNumber,
                        UploadCsvFile = UploadCsvFileDocument,
                        Location = location_instance,
                        created_by = created_by
                    )
                    Financial_History_instance.save()


                    Document_Checklist_instance = Document_Checklist_Detials(
                        EmployeeMedicalInfo = Employee_Medical_instance,
                        EmployeementHistory = EmployeementHistory_instance,
                        Employee=Employee_instance,
                        EmployeeCurrentHistoryInfo = CurrentEmployee_History_instance,
                        EmployeeFinancialHistory = Financial_History_instance,
                        Resume = ResumeDocument,
                        PanCard = PanCardDocument,
                        AadharCard = AadharCardDocument,
                        BankPassbook = BankPassbookDocument,
                        ExperienceCertificate = ExperienceCertificateDocument,
                        MedicalFitness = MedicalFitnessDocument,
                        Offerletter = OfferletterDocument,
                        Location = location_instance,
                        created_by = created_by
                    )
                    Document_Checklist_instance.save()

                    return JsonResponse({'success': 'Employees Details added successfully'})
    
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
            
   
    elif request.method == 'GET':
        try:
            def get_file_image(filedata):
                # Detect the file type using file content
                kind = filetype.guess(filedata)
                
                # Default to PDF if the type is undetermined
                contenttype1 = 'application/pdf'
                if kind and kind.mime == 'image/jpeg':
                    contenttype1 = 'image/jpeg'
                elif kind and kind.mime == 'image/png':
                    contenttype1 = 'image/png'

                # Return base64 encoded data with MIME type
                return f'data:{contenttype1};base64,{base64.b64encode(filedata).decode("utf-8")}'
            
          
            # Fetch all records from the Location_Detials model
            Employee_Personal_Info = Employee_Personal_Form_Detials.objects.all()
            print(Employee_Personal_Info)
            
            idx=1
            # Construct a list of dictionaries containing location data

            Employees_data = []  # Initialize the list before the loop
    
            for i, employee in enumerate(Employee_Personal_Info):
                departmentId = ', '.join(str(department.Department_Id) for department in employee.Department.all())
                departments = ', '.join(department.Department_Name for department in employee.Department.all())

                employee_data = {
                    'id': idx + i,
                    'Employee_Id': employee.pk,
                    'Title': employee.Tittle.Title_Name if employee.Tittle else None,
                    'FirstName': employee.First_Name,
                    'MiddleName': employee.Middle_Name,
                    'LastName': employee.Last_Name,
                    'FullName': f"{employee.Tittle.Title_Name + ' ' if employee.Tittle else ''}{"."}{employee.First_Name} {employee.Middle_Name or ''} {employee.Last_Name}".strip(),
                    'Gender': employee.Gender,
                    'DOB': employee.DOB,
                    'Age': employee.Age,
                    'BloodGroup': employee.BloodGroup.BloodGroup_Id if employee.BloodGroup else None,
                    'BloodGroupName': employee.BloodGroup.BloodGroup_Name if employee.BloodGroup else None,
                    'Phone': employee.Contact_Number,
                    'Alternate_Number': employee.Alternate_Number,
                    'Email': employee.E_mail,
                    'Qualification': employee.Qualification,
                    'SkillSet': employee.SkillSet,
                    'IdProofType': employee.IdProofType,
                    'IdProofNo': employee.IdProofNo,
                    'Marital_Status': employee.Marital_Status,
                    'MarriagePlan': employee.MarriagePlan,
                    'AnniversaryDate': employee.AnniversaryDate,
                    'Residence':employee.Residence,
                    'FatherName': employee.FatherName,
                    'FatherContact': employee.FatherContact,
                    'FatherWorking': employee.FatherWorking,
                    'FatherWorkPlace': employee.FatherWorkPlace,
                    'MotherName': employee.MotherName,
                    'MotherContact': employee.MotherContact,
                    'MotherWorking': employee.MotherWorking,
                    'MotherWorkPlace': employee.MotherWorkPlace,
                    'Spouse_Name': employee.Spouse_Name,
                    'SpouseContact': employee.SpouseContact,
                    'SpouseWorking': employee.SpouseWorking,
                    'SpouseWorkPlace': employee.SpouseWorkPlace,
                    'Child': employee.Child,
                    'TotalNoChild': employee.TotalNoChild,
                    'DoorNo': employee.DoorNo,
                    'Street': employee.Street,
                    'Area': employee.Area,
                    'City': employee.City,
                    'District': employee.District,
                    'State': employee.State,
                    'Country': employee.Country,
                    'Pincode': employee.Pincode,
                    'PermanentAddressSameAsAbove':employee.PermanentAddressSameAsAbove,
                    'Category': employee.Category.Category_Name if employee.Category else None,
                    'Speciality': employee.Speciality.Speciality_Name if employee.Speciality else None,
                    'Department': departments,
                    'Department_Id' : departmentId,
                    'Designation': employee.Designation.Designation_Name if employee.Designation else None,
                    'EmergencyContactName1': employee.EmergencyContactName1,
                    'EmergencyContactNo1': employee.EmergencyContactNo1,
                    'EmergencyContactName2': employee.EmergencyContactName2,
                    'EmergencyContactNo2': employee.EmergencyContactNo2,
                    'ActiveStatus': employee.ActiveStatus,
                    'RequirementSource': employee.RequirementSource,
                    'Source': employee.Source,
                    'Created_by': employee.created_by,
                    'Photo': get_file_image(employee.Photo) if employee.Photo else None,
                    'Signature': get_file_image(employee.Signature) if employee.Signature else None,
                    'CaptureImage': get_file_image(employee.CaptureImage) if employee.CaptureImage else None,
                    'Date': employee.created_at.strftime('%Y-%m-%d'),  # Format date
                    'Time': employee.created_at.strftime('%H:%M:%S'),  # Format time
                    'EmployeeHistory': [],
                    'EmployeeSkillset': [],
                    'EmployeeMedicalInfo': [],
                    'EmployeeCurrentDetails': [],
                    'EmployeeFinancialHistory': [],
                    'EmployeeDocumentChecklist': [],
                }

                EmployeeHistory_Data = Employeement_History_Detials.objects.filter(Employee=employee.pk)
                for table1 in EmployeeHistory_Data:
                    employee_data['EmployeeHistory'].append({
                        'id':table1.Employee.pk,
                        'PreviousWorkExperience':table1.PreviousWorkExperience,
                        'PreviousWorkPFNumber':table1.PreviousWorkPFNumber,
                        'PreviousWorkESINumber':table1.PreviousWorkESINumber,
                        'PFNumber':table1.PFNumber,
                        'ESINumber':table1.ESINumber,
                        'NoOfYears':table1.NoOfYears,
                        'WorkStationNameAddress':table1.WorkStationNameAddress,
                        'ReasonForLeft':table1.ReasonForLeft,
                        'WorkStationPhoneNo':table1.WorkStationPhoneNo,
                        'EmployeePaySlip': get_file_image(table1.EmployeePaySlip) if table1.EmployeePaySlip else None,
                        'EmployeeOfferLetter': get_file_image(table1.EmployeeOfferLetter) if table1.EmployeeOfferLetter else None,
                        'EmployeeReliveLetter': get_file_image(table1.EmployeeReliveLetter) if table1.EmployeeReliveLetter else None,
                        'ConfirmedBy':table1.ConfirmedBy,
                        'Created_by': table1.created_by,
                        # 'Location': table1.Location,
                        # 'LocationName': table1.Location.Location_Name,

                    })

                EmployeeMedicalInfo_Data =  Employee_Medical_Information_Detials.objects.filter(Employee=employee.pk) 
                for table2 in EmployeeMedicalInfo_Data:
                    employee_data['EmployeeMedicalInfo'].append({
                        'id':table2.Employee.pk,
                        'PreExisiting_Medical_Condition':table2.PreExisiting_Medical_Condition,
                        'PsychiatricMedicines':table2.PsychiatricMedicines,
                        'PsychiatricMedicinesDetails':table2.PsychiatricMedicinesDetails,
                        'PreviousOperation':table2.PreviousOperation,
                        'SurgeriesDetails':table2.SurgeriesDetails,
                        'VaccinationStatus':table2.VaccinationStatus,
                        'VaccinationStatusDetails':table2.VaccinationStatusDetails,
                        'MedicalFitnessCertificate': get_file_image(table2.MedicalFitnessCertificate) if table2.MedicalFitnessCertificate else None,
                        'AnnualMedicalCheckup': get_file_image(table2.AnnualMedicalCheckup) if table2.AnnualMedicalCheckup else None,
                        'Created_by': table2.created_by,


                    })

                CurrentHistory_Data =  Current_History_Detials.objects.filter(Employee=employee.pk)  
                for table3 in CurrentHistory_Data:
                    employee_data['EmployeeCurrentDetails'].append({
                        'id':table3.Employee.pk,
                        'DateOfJoining':table3.DateOfJoining,
                        'CurrentEmployeementLocations':table3.CurrentEmployeementLocations.Location_Id if table3.CurrentEmployeementLocations else None,
                        'ReportingManager':table3.ReportingManager,
                        'GovtLeave':table3.GovtLeave,
                        'CasualLeave':table3.CasualLeave,
                        'SickLeave':table3.SickLeave,
                        'TotalLeave':table3.TotalLeave,
                        'WorkEmail':table3.WorkEmail,
                        'ProbationPeriod':table3.ProbationPeriod,
                        'Months':table3.Months,
                        'Years':table3.Years,
                        'TrainingGivenBy':table3.TrainingGivenBy,
                        'TrainingVerifiedBy':table3.TrainingVerifiedBy,
                        'TrainingCompletedDate':table3.TrainingCompletedDate,
                        'IsPF_Applicable':table3.IsPF_Applicable if table3.IsPF_Applicable else 0,
                        'Created_by': table3.created_by,
                    })

                FinancialHistory_Data =  Financial_History_Detials.objects.filter(Employee=employee.pk)
                for table4 in FinancialHistory_Data:
                    employee_data['EmployeeFinancialHistory'].append({
                        'id':table4.Employee.pk,
                        'Salary':table4.Salary,
                        'BasicSalary':table4.BasicSalary,
                        'Allowance':table4.Allowance,
                        'FinalAllowance':table4.Allowancefinal,
                        'PfForEmployee':table4.PfForEmployee,
                        'SecurityDeposite':table4.SecurityDeposite,
                        'AccountHolderName':table4.AccountHolderName,
                        'AccountNumber':table4.AccountNumber,
                        'BankName':table4.BankName,
                        'Branch':table4.Branch,
                        'IfscCode':table4.IfscCode,
                        'PanNumber':table4.PanNumber,
                        'UploadCsvFile': get_file_image(table4.UploadCsvFile) if table4.UploadCsvFile else None,
                        'Created_by': table4.created_by,


                    })

                EmployeeDocument_Chicklist_Data =  Document_Checklist_Detials.objects.filter(Employee=employee.pk)
                for table5 in EmployeeDocument_Chicklist_Data:
                    employee_data['EmployeeFinancialHistory'].append({
                        'id':table5.Employee.pk,
                        'Resume': get_file_image(table5.Resume) if table5.Resume else None,
                        'PanCard': get_file_image(table5.PanCard) if table5.PanCard else None,
                        'AadharCard': get_file_image(table5.AadharCard) if table5.AadharCard else None,
                        'BankPassbook': get_file_image(table5.BankPassbook) if table5.BankPassbook else None,
                        'ExperienceCertificate': get_file_image(table5.ExperienceCertificate) if table5.ExperienceCertificate else None,
                        'MedicalFitness': get_file_image(table5.MedicalFitness) if table5.MedicalFitness else None,
                        'Offerletter': get_file_image(table5.Offerletter) if table5.Offerletter else None,
                        'Created_by': table5.created_by,
                    })


                EmployeeSkill_Data =  Employee_Skills_Detials.objects.filter(Employee=employee.pk)   
                for table6 in EmployeeSkill_Data:
                    employee_data['EmployeeSkillset'].append({
                        'id':table6.Employee.pk,
                        'skill_name':table6.Skill,
                        'skill_level':table6.Level,
                        'Created_by': table6.created_by,
                    })      


                Employees_data.append(employee_data)
            
            return JsonResponse(Employees_data, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
    




@csrf_exempt
def get_User_Employee_Details(request):
    if request.method == 'GET':
        try:
            
            Employee_Id = request.GET.get('EmployeeId')
            if not Employee_Id:
                return JsonResponse({'warn': 'Employee_Id is required'}, status=400)
            
            
            # Fetch all records from the Location_Detials model
            employee = Employee_Personal_Form_Detials.objects.get(pk=Employee_Id)
            print(employee.Tittle.Title_Name,'----++++')

            EmployeeDepartment = Current_History_Detials.objects.get(Employee__pk = Employee_Id)
            
            idx=1
            # Construct a list of dictionaries containing location data
            Employees_data = {
                    # 'id': idx + i,
                    'Employee_Id': employee.Employee_ID,
                    'Title': employee.Tittle.Title_Name,
                    'FirstName': employee.First_Name,
                    'MiddleName': employee.Middle_Name,
                    'lastName': employee.Last_Name,
                    'Email': employee.E_mail,
                    'Phone': employee.Contact_Number,
                    'Gender': employee.Gender,
                    'Qualification': employee.Qualification,
                    # 'Department': EmployeeDepartment.Department.Department_Name,
                    # 'Designation': EmployeeDepartment.Designation.Designation_Name,
                    'Created_by': employee.created_by,
                    'Date': employee.created_at.strftime('%Y-%m-%d'),  # Format date
                    'Time': employee.created_at.strftime('%H:%M:%S'),  # Format time
                }
            
            
            print(Employees_data,'Employees_data')
            return JsonResponse(Employees_data, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
    





@csrf_exempt
def Get_Employee_Registered_Details(request):
    if request.method == 'GET':
        try:
            Employee_Id = request.GET.get('Employee')
            # print(Employee_Id,'Employee_Id')

            def get_file_image(filedata):
                kind = filetype.guess(filedata)
                # Default to PDF if the type is undetermined
                contenttype1 = 'application/pdf'
                if kind and kind.mime == 'image/jpeg':
                    contenttype1 = 'image/jpeg'
                elif kind and kind.mime == 'image/png':
                    contenttype1 = 'image/png'

                # Return base64 encoded data with MIME type
                return f'data:{contenttype1};base64,{base64.b64encode(filedata).decode("utf-8")}'
            
            Employee = Employee_Personal_Form_Detials.objects.get(pk=Employee_Id)
            print(Employee,'Employee_Personal_Info')
            EmployeeSkillset_Data = Employee_Skills_Detials.objects.filter(Employee__pk=Employee_Id)
            print(EmployeeSkillset_Data,'EmployeeSkillset_Data')
            
            EmployeeHistory_Data = Employeement_History_Detials.objects.filter(Employee__pk=Employee_Id)
            EmployeeMedicalInfo_Data =  Employee_Medical_Information_Detials.objects.filter(Employee__pk=Employee_Id) 
            CurrentHistory_Data =  Current_History_Detials.objects.filter(Employee__pk=Employee_Id)
            FinancialHistory_Data =  Financial_History_Detials.objects.filter(Employee__pk=Employee_Id)
            EmployeeDocument_Chicklist_Data =  Document_Checklist_Detials.objects.filter(Employee__pk=Employee_Id)
  
            departmentId = ', '.join(str(department.Department_Id) for department in Employee.Department.all())
            departments = ', '.join(department.Department_Name for department in Employee.Department.all())
            
           

            employee_data = {
                
                'Employee_Id': Employee.pk,
                'Title': Employee.Tittle.Title_Id if Employee.Tittle else None,
                'FirstName': Employee.First_Name,
                'MiddleName': Employee.Middle_Name,
                'LastName': Employee.Last_Name,
                'Gender': Employee.Gender,
                'DOB': Employee.DOB,
                'Age': Employee.Age,
                'BloodGroup': Employee.BloodGroup.BloodGroup_Id if Employee.BloodGroup else None,
                'BloodGroupName': Employee.BloodGroup.BloodGroup_Name if Employee.BloodGroup else None,
                'Phone': Employee.Contact_Number,
                'Alternate_Number': Employee.Alternate_Number,
                'Email': Employee.E_mail,
                'Qualification': Employee.Qualification,
                'IdProofType': Employee.IdProofType,
                'IdProofNo': Employee.IdProofNo,
                'Marital_Status': Employee.Marital_Status,
                'MarriagePlan': Employee.MarriagePlan,
                'AnniversaryDate':Employee.AnniversaryDate,
                'Residence':Employee.Residence,
                'FatherName': Employee.FatherName,
                'FatherContact': Employee.FatherContact,
                'FatherWorking': Employee.FatherWorking,
                'FatherWorkPlace': Employee.FatherWorkPlace,
                'MotherName': Employee.MotherName,
                'MotherContact': Employee.MotherContact,
                'MotherWorking': Employee.MotherWorking,
                'MotherWorkPlace': Employee.MotherWorkPlace,
                'Spouse_Name': Employee.Spouse_Name,
                'SpouseContact': Employee.SpouseContact,
                'SpouseWorking': Employee.SpouseWorking,
                'SpouseWorkPlace': Employee.SpouseWorkPlace,
                'Child': Employee.Child,
                'TotalNoChild': Employee.TotalNoChild,
                'DoorNo': Employee.DoorNo,
                'Street': Employee.Street,
                'Area': Employee.Area,
                'City': Employee.City,
                'District': Employee.District,
                'State': Employee.State,
                'Country': Employee.Country,
                'Pincode': Employee.Pincode,
                'PermanentAddressSameAsAbove':Employee.PermanentAddressSameAsAbove,
                'PermanentDoorNo':Employee.PermanentDoorNo,
                'PermanentStreet':Employee.PermanentStreet,
                'PermanentArea':Employee.PermanentArea,
                'PermanentCity':Employee.PermanentCity,
                'PermanentDistrict':Employee.PermanentDistrict,
                'PermanentState':Employee.PermanentState,
                'PermanentCountry':Employee.PermanentCountry,
                'PermanentPincode':Employee.PermanentPincode,
                'Department' : departments,
                'departments' : departmentId,
                'Category': Employee.Category.Category_Id if Employee.Category else None,
                'Speciality': Employee.Speciality.Speciality_Id if Employee.Speciality else None,
                'Designation': Employee.Designation.Designation_Id if Employee.Designation else None,
                'Classification' : Employee.Classification.Classification_Id if Employee.Classification else None,
                'Role' : Employee.Role.Role_Id if Employee.Role else None,
                'EmergencyContactName1': Employee.EmergencyContactName1,
                'EmergencyContactNo1': Employee.EmergencyContactNo1,
                'EmergencyContactName2': Employee.EmergencyContactName2,
                'EmergencyContactNo2': Employee.EmergencyContactNo2,
                'ActiveStatus': Employee.ActiveStatus,
                'RequirementSource': Employee.RequirementSource,
                'Source': Employee.Source,
                'Created_by': Employee.created_by,
                'Photo': get_file_image(Employee.Photo) if Employee.Photo else None,
                'Signature': get_file_image(Employee.Signature) if Employee.Signature else None,
                'Date': Employee.created_at.strftime('%Y-%m-%d'),  # Format date
                'Time': Employee.created_at.strftime('%H:%M:%S'),  # Format time
                'EmployeeHistory': [{

                    'id':table1.Employee.pk,
                    'PreviousWorkExperience':table1.PreviousWorkExperience,
                    'PreviousWorkPFNumber':table1.PreviousWorkPFNumber,
                    'PreviousWorkESINumber':table1.PreviousWorkESINumber,
                    'PFNumber':table1.PFNumber,
                    'ESINumber':table1.ESINumber,
                    'NoOfYears':table1.NoOfYears,
                    'WorkStationNameAddress':table1.WorkStationNameAddress,
                    'ReasonForLeft':table1.ReasonForLeft,
                    'WorkStationPhoneNo':table1.WorkStationPhoneNo,
                    'EmployeePaySlip': get_file_image(table1.EmployeePaySlip) if table1.EmployeePaySlip else None,
                    'EmployeeOfferLetter': get_file_image(table1.EmployeeOfferLetter) if table1.EmployeeOfferLetter else None,
                    'EmployeeReliveLetter': get_file_image(table1.EmployeeReliveLetter) if table1.EmployeeReliveLetter else None,
                    'ConfirmedBy':table1.ConfirmedBy,
                    'Created_by': table1.created_by,

                
                    } for table1 in EmployeeHistory_Data
                ],
                'EmployeeMedicalInfo': [{
                    'id':table2.Employee.pk,
                    'PreExisiting_Medical_Condition':table2.PreExisiting_Medical_Condition,
                    'PsychiatricMedicines':table2.PsychiatricMedicines,
                    'PsychiatricMedicinesDetails':table2.PsychiatricMedicinesDetails,
                    'PreviousOperation':table2.PreviousOperation,
                    'SurgeriesDetails':table2.SurgeriesDetails,
                    'VaccinationStatus':table2.VaccinationStatus,
                    'VaccinationStatusDetails':table2.VaccinationStatusDetails,
                    'MedicalFitnessCertificate': get_file_image(table2.MedicalFitnessCertificate) if table2.MedicalFitnessCertificate else None,
                    'AnnualMedicalCheckup': get_file_image(table2.AnnualMedicalCheckup) if table2.AnnualMedicalCheckup else None,
                    'Created_by': table2.created_by,

                }for table2 in EmployeeMedicalInfo_Data
                ],
                'EmployeeCurrentDetails': [{
                    'id':table3.Employee.pk,
                    'DateOfJoining':table3.DateOfJoining,
                    'CurrentEmployeementLocations':table3.CurrentEmployeementLocations.Location_Id if table3.CurrentEmployeementLocations else None,
                    'ReportingManager':table3.ReportingManager,
                    'GovtLeave':table3.GovtLeave,
                    'CasualLeave':table3.CasualLeave,
                    'SickLeave':table3.SickLeave,
                    'TotalLeave':table3.TotalLeave,
                    'WorkEmail':table3.WorkEmail,
                    'ProbationPeriod':table3.ProbationPeriod,
                    'Months':table3.Months,
                    'Years':table3.Years,
                    'TrainingGivenBy':table3.TrainingGivenBy,
                    'TrainingVerifiedBy':table3.TrainingVerifiedBy,
                    'TrainingCompletedDate':table3.TrainingCompletedDate,
                    'IsPF_Applicable':table3.IsPF_Applicable if table3.IsPF_Applicable else 0,
                    'Created_by': table3.created_by,
                }for table3 in CurrentHistory_Data
                ],
                'EmployeeFinancialHistory': [{
                    'id':table4.Employee.pk,
                    'Salary':table4.Salary,
                    'BasicSalary':table4.BasicSalary,
                    'Allowance':table4.Allowance,
                    'FinalAllowance':table4.Allowancefinal,
                    'PfForEmployee':table4.PfForEmployee,
                    'SecurityDeposite':table4.SecurityDeposite,
                    'AccountHolderName':table4.AccountHolderName,
                    'AccountNumber':table4.AccountNumber,
                    'BankName':table4.BankName,
                    'Branch':table4.Branch,
                    'IfscCode':table4.IfscCode,
                    'PanNumber':table4.PanNumber,
                    'UploadCsvFile': get_file_image(table4.UploadCsvFile) if table4.UploadCsvFile else None,
                    'Created_by': table4.created_by,
                }for table4 in FinancialHistory_Data
                ],
                'EmployeeDocumentChecklist': [{
                    'id':table5.Employee.pk,
                    'Resume': get_file_image(table5.Resume) if table5.Resume else None,
                    'PanCard': get_file_image(table5.PanCard) if table5.PanCard else None,
                    'AadharCard': get_file_image(table5.AadharCard) if table5.AadharCard else None,
                    'BankPassbook': get_file_image(table5.BankPassbook) if table5.BankPassbook else None,
                    'ExperienceCertificate': get_file_image(table5.ExperienceCertificate) if table5.ExperienceCertificate else None,
                    'MedicalFitness': get_file_image(table5.MedicalFitness) if table5.MedicalFitness else None,
                    'Offerletter': get_file_image(table5.Offerletter) if table5.Offerletter else None,
                    'Created_by': table5.created_by,
                }for table5 in EmployeeDocument_Chicklist_Data
                ],

                'EmployeeSkillset': [{
                    'id': skill.Employee.pk,
                    'skill_name': skill.Skill,
                    'skill_level': skill.Level,
                    'Created_by': skill.created_by,
                } for skill in EmployeeSkillset_Data
                ],
            }

           
            return JsonResponse(employee_data, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
    



@csrf_exempt
def filter_Sourcewise_Employee_Details(request):
    if request.method == 'GET':
        try:
            # Retrieve the 'RequirementSource' parameter from the request
            RequirementSource = request.GET.get('RequirementSource')
            
            # Filter employees by 'RequirementSource'
            employees = Employee_Personal_Form_Detials.objects.filter(RequirementSource=RequirementSource)
            
            # If no employee is found, return an empty response
            if not employees.exists():
                return JsonResponse({'error': 'No employees found for the selected source'})
            
            # Prepare data for the response
            Employees_data = []
            for employee in employees:
                employee_data = {
                    'Employee_Id': employee.Employee_ID,
                    'Title': employee.Tittle.Title_Name,
                    'FirstName': employee.First_Name,
                    'MiddleName': employee.Middle_Name,
                    'LastName': employee.Last_Name,
                    'Email': employee.E_mail,
                    'Phone': employee.Contact_Number,
                    'Gender': employee.Gender,
                    'Qualification': employee.Qualification,
                    'Department': employee.Department.Department_Name,
                    'Designation': employee.Designation.Designation_Name,
                    'Created_by': employee.created_by,
                    'Date': employee.created_at.strftime('%Y-%m-%d'),  # Format date
                    'Time': employee.created_at.strftime('%H:%M:%S'),  # Format time
                }
                Employees_data.append(employee_data)
            
            # Return the employee data as JSON
            return JsonResponse(Employees_data, safe=False)
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)




from datetime import datetime
from calendar import monthrange

def getforemployeepayrolllist(request):
    try:
        # Get request parameters
        fromdate = request.GET.get('fromdate')
        todate = request.GET.get('todate')
        location = request.GET.get('location')

        # Parse dates
        from_date = datetime.strptime(fromdate, "%Y-%m-%d").date()
        to_date = datetime.strptime(todate, "%Y-%m-%d").date()
        total_days = (to_date - from_date).days + 1

        # Get the number of days in the from_date month
        _, days_in_month = monthrange(from_date.year, from_date.month)

        # Filter employees by location
        employees = Employee_Personal_Form_Detials.objects.filter(Location_id=location)
        if not employees.exists():
            return JsonResponse({"message": "No employees found for the given location."})

        # Prepare final results
        final_results = []
        def get_file_image(filedata):
                # Detect the file type using file content
                kind = filetype.guess(filedata)
                
                # Default to PDF if the type is undetermined
                contenttype1 = 'application/pdf'
                if kind and kind.mime == 'image/jpeg':
                    contenttype1 = 'image/jpeg'
                elif kind and kind.mime == 'image/png':
                    contenttype1 = 'image/png'

                # Return base64 encoded data with MIME type
                return f'data:{contenttype1};base64,{base64.b64encode(filedata).decode("utf-8")}'

        for employee in employees:
            emp_id = employee.Employee_ID,

            # Fetch financial details
            try:
                finance_details = Financial_History_Detials.objects.get(Employee_id=emp_id)
            except Financial_History_Detials.DoesNotExist:
                continue
            
            try:
                CurrentHistoryDetials = Current_History_Detials.objects.get(Employee_id=emp_id)
            except Current_History_Detials.DoesNotExist:
                continue

            try:
                PFdetails = Employeement_History_Detials.objects.get(Employee_id=emp_id)
            except Employeement_History_Detials.DoesNotExist:
                continue

            print('employee.Department :',employee.Department)
            summa = employee.Department.all()
            for i in summa:
                print('i:',i)
                try:
                    department = Department_Detials.objects.get(Department_Id=i.Department_Id)
                except Department_Detials.DoesNotExist:
                    continue

            try:
                title = Title_Detials.objects.get(Title_Id=employee.Tittle.Title_Id)
            except Title_Detials.DoesNotExist:
                continue

            try:
                designation = Designation_Detials.objects.get(Designation_Id=employee.Designation.Designation_Id)
            except Designation_Detials.DoesNotExist:
                continue

            

            # Initialize advance details
            AmountDeduct_PerMonth = 0
            Repayment_Due = 0
            Installment_Status = None
            No_of_MonthPaid = 0
            PaidAmount = 0

            advancedetails = Employee_Advance_Request.objects.filter(
                Employee_Id_id=finance_details.EmpHistory_Id,
                Installment_Status="Pending",
                Status="Approved"
            ).last()
            
            PayslipStatus = Employee_PaySlips.objects.filter(
                Employee_id=finance_details.EmpHistory_Id
            ).last()
            
            PayslipStatus1 = "Pending"
            if PayslipStatus:
                PayslipStatus1 = "Completed"
                

            advanceid = None,
            AmountDeduct_PerMonth = 0
            Repayment_Due = None
            Installment_Status = None
            No_of_MonthPaid = 0
            PaidAmount = 0
            # print('advancedetails :',advancedetails)
            if advancedetails is not None:
     
                advanceid = advancedetails.Advance_RequestId,
                AmountDeduct_PerMonth = advancedetails.AmountDeduct_PerMonth if advancedetails.AmountDeduct_PerMonth else 0
                Repayment_Due = advancedetails.Repayment_Due
                Installment_Status = advancedetails.Installment_Status
                No_of_MonthPaid = advancedetails.No_of_MonthPaid
                PaidAmount = advancedetails.PaidAmount

            SalaryType = finance_details.SalaryType
            StipendAmount = 0
            if SalaryType == 'Stipend':
                StipendAmount = finance_details.StipendAmount

       
            # Calculate per day salary
            basic_salary = finance_details.BasicSalary or 0
            per_day_salary = basic_salary / days_in_month

            # Fetch attendance data
            attendance_records = Employee_Attendance.objects.filter(
                Employee_id=emp_id,
                Date__range=[from_date, to_date]
            )
            present_days = attendance_records.filter(Attendance_Status="Present").count()
            leave_days = attendance_records.filter(
                Attendance_Status__in=["Absent", "On Leave"]
            ).count()

            if leave_days == 0:
                leave_days1 = total_days - present_days
            else:
                leave_days1 = leave_days
            # Calculate payable salary based on attendance

            payable_salary = total_days * per_day_salary

            finalpayable = payable_salary - AmountDeduct_PerMonth

            # Calculate Allowances
            allowances = sum([
                finance_details.Allowancefinal or 0,
            ])

            # PfForEmployeer_Amount = (finance_details.PfForEmployeer / 100) * basic_salary
            PfForEmployee_Amount = (finance_details.PfForEmployee / 100) * basic_salary
            # Tds_Amount = (TDS_Per / 100) * basic_salary
            # EsiAmount = (finance_details.EsiAmount / 100) * basic_salary

            # Professional Tax Calculation
            professional_tax = 0
            if basic_salary <= 21000:
                professional_tax = 0
            elif 21001 <= basic_salary <= 30000:
                professional_tax = 135
            elif 30001 <= basic_salary <= 45000:
                professional_tax = 315
            elif 45001 <= basic_salary <= 60000:
                professional_tax = 690
            elif 60001 <= basic_salary <= 75000:
                professional_tax = 1025
            else:
                professional_tax = 1250

            earnings = finalpayable + allowances
            deductions = sum([
                # PfForEmployeer_Amount or 0,
                # EsiAmount or 0,
                # Tds_Amount or 0,
                professional_tax,
            ])
            net_salary = earnings - deductions

   

            # Compile employee details with calculated salary
            result = {
                "Employee_ID": emp_id[0],
                'advanceid':advanceid[0],
                'Photo': get_file_image(employee.Photo) if employee.Photo else None,
                'CaptureImage': get_file_image(employee.CaptureImage) if employee.CaptureImage else None,
                "EmployeeName": f"{title.Title_Name}.{employee.First_Name} {employee.Last_Name}",
                "PayableSalary": round(payable_salary, 2) if SalaryType == "fixed" else StipendAmount,
                "TotalDays": total_days,
                "PresentDays": present_days,   
                "leave_days": leave_days1,
                "earnings": round(earnings,2),
                "deductions": round(deductions,2),
                "NetSalary": round(net_salary, 2) if SalaryType == "fixed" else StipendAmount,
                "Department_Name": department.Department_Name,
                "Designation": designation.Designation_Name,
                "PhoneNumber": employee.Contact_Number,
                "HRAfinal": finance_details.Allowancefinal or 0,
                "MedicalAllowancefinal": finance_details.MedicalAllowancefinal or 0,
                "SpecialAllowancefinal": finance_details.SpecialAllowancefinal or 0,
                "TravelAllowancefinal": finance_details.TravelAllowancefinal or 0,
                "PfForEmployee_Amount": round(PfForEmployee_Amount,2),
                "ProfessionalTax": professional_tax,
                "AmountDeduct_PerMonth": AmountDeduct_PerMonth,
                "Repayment_Due": Repayment_Due,
                "Installment_Status": Installment_Status,
                "No_of_MonthPaid": No_of_MonthPaid,
                "PaidAmount": PaidAmount,
                "AccountHolderName": finance_details.AccountHolderName,
                "AccountNumber": finance_details.AccountNumber,
                "BankName": finance_details.BankName,
                "Branch": finance_details.Branch,
                "IfscCode": finance_details.IfscCode,
                "PanNumber": finance_details.PanNumber,
                "PayslipStatus1": PayslipStatus1,
                "BasicSalary": finance_details.BasicSalary,
                "LossofPay": 0,
                "DateofJoining": CurrentHistoryDetials.DateOfJoining,
                "WorkEmail": CurrentHistoryDetials.WorkEmail,
                "PFNumber":PFdetails.PFNumber,
                "ESINumber":PFdetails.ESINumber,
                'fromdate': fromdate
               
            }

            final_results.append(result)

        return JsonResponse(final_results, safe=False)

    except Exception as e:
        print('Error:', e)
        return JsonResponse({"error": str(e)},status=500)






@csrf_exempt
@require_http_methods(["POST", "OPTIONS", "GET"])
def insert_employee_performance(request):
    if request.method == 'POST':
        try:
            # Parse POST data (handle form-data or JSON content)
            data = json.loads(request.body)

            # Extract data fields
            employee_id = data.get('employeeId')
            hike_amount = float(data.get('amount', 0))
            new_pay = float(data.get('newpay', 0))
            approved_by = data.get('approvedby', '')
            created_by = data.get('createdby', '')
            date = data.get('date', '')
            performance = int(data.get('performance', 0))
            current = float(data.get('current', 0))
            hike = float(data.get('hike', 0))
            location = data.get('location', '')
            remarks = data.get('remarks', '')

            # Validate required fields
            if not employee_id:
                return JsonResponse({'warn': "Employee ID is required"}, status=400)
            if not location:
                return JsonResponse({'warn': "Location is required"}, status=400)

            # Fetch the employee and location data
            try:
                Employee_instance = Employee_Personal_Form_Detials.objects.get(Employee_ID=employee_id)
            except Employee_Personal_Form_Detials.DoesNotExist:
                return JsonResponse({'warn': 'Employee not found'})
            except Exception as e:
                print(f"Error fetching employee: {str(e)}")
                return JsonResponse({'error': f"Error fetching employee: {str(e)}"})

            try:
                location_ins = Location_Detials.objects.get(Location_Id=location)
            except Location_Detials.DoesNotExist:
                return JsonResponse({'warn': 'Location not found'})
            except Exception as e:
                print(f"Error fetching location: {str(e)}")
                return JsonResponse({'error': f"Error fetching location: {str(e)}"})

            # Create performance record
            performance_record = Employee_Performance.objects.create(
                Employee=Employee_instance,
                Date=date,
                Current_Payment=current,
                Performance_Rate=performance,
                Hike_Percentage=hike,
                Hike_Amount=hike_amount,
                New_Pay=new_pay,
                Remarks=remarks,
                ApprovedBy=approved_by,
                Location_Name=location_ins,
                CreatedBy=created_by
            )

            # Now update the financial history table
            try:
                # Fetch the existing financial history for the employee
                financial_history = Financial_History_Detials.objects.get(Employee=Employee_instance)
                
                # Basic Salary is 70% of New Pay
                basic_salary = new_pay * 0.70

                # HRA is 20% of Basic Salary
                hra = basic_salary * 0.20

                # Special Allowance is 5% of Basic Salary
                special_allowance = basic_salary * 0.05

                # Medical Allowance is 2% of Basic Salary
                medical_allowance = basic_salary * 0.02

                # Gross Salary is the sum of Basic Salary, HRA, Special Allowance, and Medical Allowance
                gross_salary = basic_salary + hra + special_allowance + medical_allowance

                # Provident Fund (PF) is 12% of Basic Salary
                pf_contribution = basic_salary * 0.12

                # Bonus is 10% of Basic Salary
                bonus = basic_salary * 0.10

                # CTC is the sum of Gross Salary, PF contribution, and Bonus
                ctc = gross_salary + pf_contribution + bonus

                # Update the Financial History with the new values
                financial_history.BasicSalary = basic_salary
                financial_history.GrossSalary = gross_salary
                financial_history.Ctc = ctc

                # Save the updated record
                financial_history.save()

            except Financial_History_Detials.DoesNotExist:
                return JsonResponse({'warn': 'Financial record not found for this employee'}, status=404)

            # Return success response
            return JsonResponse({'success': 'Employee performance data inserted and financial details updated successfully'}, status=201)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': f'An internal server error occurred: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def get_username_details(request):
    if request.method == 'GET':
        try:
            users = UserRegister_Master_Details.objects.all()
            user_data = []
            for user in users:
                user = {
                    'id': user.Employee_Id.Employee_ID,
                    'userid' : user.User_Id,
                    'username' : user.auth_user_id.username,
                }
                user_data.append(user)
            return JsonResponse(user_data,safe=False)
        except Exception as e:
            return JsonResponse({'error':str(e)})