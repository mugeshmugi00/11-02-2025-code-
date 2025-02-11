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

from django.http import JsonResponse
from django.db.models import Q, Max
from rest_framework.decorators import api_view
from .models import Trainee_Personal_Form_Details  # ✅ Use this model

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

@csrf_exempt
@require_http_methods(["POST", "OPTIONS", "GET"])
def Trainee_Registration_Details(request):


    
    if request.method == 'POST':
      try:
            data = json.loads(request.body)

            print(data,'dataaa')
            
            # Extract and validate data
            Title = data.get('Title','')
            FirstName = data.get('FirstName','')
            MiddleName = data.get('MiddleName','')
            SurName = data.get('SurName','')
            Gender = data.get('Gender','')
            Dob = data.get('Dob','')
            Age = data.get('Age','')
            BloodGroup = data.get('BloodGroup','')
            Phone = data.get('Phone','')
            
            Email = data.get('Email','')
            Qualification = data.get('Qualification','')
           
            IdProofType = data.get('IdProofType','')
            IdProofNo = data.get('IdProofNo','')
            MaritalStatus = data.get('MaritalStatus','')
            SpouseName = data.get('SpouseName','')
            SpouseContact = data.get('SpouseContact','')
            FatherName = data.get('FatherName','')
            FatherContact = data.get('FatherContact','')
            EmergencyContactName = data.get('EmergencyContactName','')
            EmergencyContactNo = data.get('EmergencyContactNo','')
            InstitutionalName = data.get('InstitutionalName','')
            InchargePerson = data.get('InchargePerson','')
            traineeStartDate = data.get('TraineeStartdate','')
            InductionGivenBy = data.get('InductionGivenby','')
            traineeEndDate = data.get('TraineeEnddate','')
            CertifiedBy = data.get('Certifiedby','')
            Residence = data.get('Residence','')
            Photo = data.get('Photo', None)
            TraineeCertificate = data.get('TraineeCertificate', None)
            Status=data.get('Status','')
            
            # Status = True if Status == "Active" else False
            
            Pincode = data.get('Pincode','')
            DoorNo = data.get('DoorNo','')
            Street = data.get('Street','')
            Area = data.get('Area','')
            City = data.get('City','')
            District = data.get('District','')
            State = data.get('State','')
            Country = data.get('Country','')
            Createdby = data.get('Createdby','')
            Trainee_Id = data.get('Trainee_Id','')

            print(Trainee_Id,'Trainee_Id')

            Title_instance = Title_Detials.objects.get(Title_Id=Title) if Title else None
            BloodGroup_instance = BloodGroup_Detials.objects.get(BloodGroup_Id=BloodGroup) if BloodGroup else None

            TraineeCertificateDocument = validate_and_process_file(TraineeCertificate) if TraineeCertificate  else None
            PhotoChooseDocument = validate_and_process_file(Photo) if Photo  else None

            print(BloodGroup_instance)

            if Trainee_Id:
                   

                    Trainee = Trainee_Personal_Form_Details.objects.get(Trainee_ID=Trainee_Id)

                    print(Trainee,'Trainee')
                    
                    if not Trainee:
                        return JsonResponse({'warn': f"The Trainee Id is not valid"})

                    if Trainee_Personal_Form_Details.objects.filter(First_Name=FirstName,Phone=Phone).exclude(Trainee_ID=Trainee_Id).exists():
                        Trainee = Trainee_Personal_Form_Details.objects.get(First_Name=FirstName,Phone=Phone)    
                        return JsonResponse({'warn': f"The Trainee {Trainee.Trainee_ID} is already registered with {Phone} and {FirstName}"})

                   
                     # Update trainee details
                    Trainee.Tittle = Title_instance
                    Trainee.First_Name = FirstName
                    Trainee.Middle_Name = MiddleName
                    Trainee.Sur_Name = SurName
                    Trainee.Gender = Gender
                    Trainee.DOB = Dob
                    Trainee.Age = Age
                    Trainee.BloodGroup = BloodGroup_instance
                    Trainee.Phone = Phone
                    Trainee.E_mail = Email
                    Trainee.Qualification = Qualification
                    Trainee.IdProofType = IdProofType
                    Trainee.IdProofNo = IdProofNo
                    Trainee.Marital_Status = MaritalStatus
                    Trainee.SpouseName = SpouseName
                    Trainee.SpouseContact = SpouseContact
                    Trainee.FatherName = FatherName
                    Trainee.FatherContact = FatherContact
                    Trainee.EmergencyContactName = EmergencyContactName
                    Trainee.EmergencyContactNo = EmergencyContactNo
                    Trainee.InstitutionalName = InstitutionalName
                    Trainee.InchargePerson = InchargePerson
                    Trainee.Trainee_Startdate = traineeStartDate
                    Trainee.InductionGivenby = InductionGivenBy
                    Trainee.Trainee_Enddate = traineeEndDate
                    Trainee.Certifiedby = CertifiedBy
                    Trainee.Residence = Residence
                    Trainee.Photo = PhotoChooseDocument
                    Trainee.TraineeCertificate = TraineeCertificateDocument
                    Trainee.Status = Status
                    Trainee.Pincode = Pincode
                    Trainee.DoorNo = DoorNo
                    Trainee.Street = Street
                    Trainee.Area = Area
                    Trainee.City = City
                    Trainee.District = District
                    Trainee.State = State
                    Trainee.Country = Country
                    Trainee.Createdby = Createdby

            # Save the updated trainee record
                    Trainee.save()

                    return JsonResponse({'success': 'Trainee Details updated successfully'})
                    

            Trainee_instance = Trainee_Personal_Form_Details(                   
                                          
                        Tittle=Title_instance,
                        First_Name=FirstName,
                        Middle_Name=MiddleName,
                        Sur_Name=SurName,
                        Gender=Gender,
                        DOB=Dob,
                        Age=Age,
                        BloodGroup=BloodGroup_instance,
                        Phone=Phone,
                        E_mail=Email,
                        Qualification=Qualification,
                        IdProofType=IdProofType,
                        IdProofNo=IdProofNo,
                        Marital_Status=MaritalStatus,
                        SpouseName=SpouseName,
                        SpouseContact=SpouseContact,
                        FatherName=FatherName,
                        FatherContact=FatherContact,
                        EmergencyContactName=EmergencyContactName,
                        EmergencyContactNo=EmergencyContactNo,
                        InstitutionalName=InstitutionalName,
                        InchargePerson=InchargePerson,
                        Trainee_Startdate=traineeStartDate,
                        InductionGivenby=InductionGivenBy,
                        Trainee_Enddate=traineeEndDate,
                        Certifiedby=CertifiedBy,
                        Residence=Residence,
                        Photo=PhotoChooseDocument,
                        TraineeCertificate=TraineeCertificateDocument,
                        Status=Status,

                        DoorNo=DoorNo,
                        Street=Street,
                        Area=Area,
                        City=City,
                        District=District,
                        State=State,
                        Country=Country,
                        Pincode=Pincode,
                        Createdby = Createdby
            )



            Trainee_instance.save() 

            return JsonResponse({'success': 'Trainee Details added successfully'})
    
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
            
            # Employee_Id = request.GET.get('Employee_Id')
            # if not Employee_Id:
            #     return JsonResponse({'warn': 'Employee_Id is required'}, status=400)
            
            
            # Fetch all records from the Location_Detials model
            Trainee_Personal_Info = Trainee_Personal_Form_Details.objects.all()
            print(Trainee_Personal_Info)
            
            idx=1
            # Construct a list of dictionaries containing location data

            Trainees_data = []  # Initialize the list before the loop
    
            for i, Trainee in enumerate(Trainee_Personal_Info): 

                # print('09990',Trainee.First_Name)

                
            #     departmentId = ', '.join(str(department.Department_Id) for department in employee.Department.all())
            #     departments = ', '.join(department.Department_Name for department in employee.Department.all())
            #     print('Deptttt',departments)
            #     print('DeptIDDDD',departmentId)

                Trainee_data = {
                    'id': idx + i,
                    'Trainee_Id': Trainee.Trainee_ID,
                    'Title': Trainee.Tittle.Title_Id if Trainee.Tittle else None,
                    'FirstName':Trainee.First_Name,
                    'MiddleName':Trainee.Middle_Name,
                    'SurName':Trainee.Sur_Name,
                    'Gender':Trainee.Gender,
                    'Dob':Trainee.DOB,
                    'Age':Trainee.Age,
                    'BloodGroup' : Trainee.BloodGroup.BloodGroup_Id if Trainee.BloodGroup else None,
                    'Phone': Trainee.Phone,
                    'Email': Trainee.E_mail,
                    'Qualification': Trainee.Qualification,
                    'IdProofType': Trainee.IdProofType,
                    'IdProofNo': Trainee.IdProofNo,
                    'MaritalStatus': Trainee.Marital_Status,
                    'SpouseName': Trainee.SpouseName,
                    'SpouseContact': Trainee.SpouseContact,
                    'FatherName': Trainee.FatherName,
                    'FatherContact': Trainee.FatherContact,
                    'EmergencyContactName': Trainee.EmergencyContactName,
                    'EmergencyContactNo': Trainee.EmergencyContactNo,
                    'InstitutionalName': Trainee.InstitutionalName,
                    'InchargePerson': Trainee.InchargePerson,
                    'TraineeStartdate': Trainee.Trainee_Startdate,
                    'InductionGivenby': Trainee.InductionGivenby,
                    'TraineeEnddate': Trainee.Trainee_Enddate,
                    'Certifiedby': Trainee.Certifiedby,
                    'Residence': Trainee.Residence,
                    'Photo': get_file_image(Trainee.Photo) if Trainee.Photo else None,
                    'TraineeCertificate': get_file_image(Trainee.TraineeCertificate) if Trainee.TraineeCertificate else None,
                    'Status': Trainee.Status,

                    # Communication Address
                    'Pincode': Trainee.Pincode,
                    'DoorNo': Trainee.DoorNo,
                    'Street': Trainee.Street,
                    'Area': Trainee.Area,
                    'City': Trainee.City,
                    'District': Trainee.District,
                    'State': Trainee.State,
                    'Country': Trainee.Country,
                    'CreatedAt': Trainee.created_at,
                    'UpdatedAt': Trainee.updated_at,
                    'CreatedBy': Trainee.Createdby

                    
                  #   'EmployeeHistory': [],
                  #   'EmployeeSkillset': [],
                  #   'EmployeeMedicalInfo': [],
                  #   'EmployeeCurrentDetails': [],
                  #   'EmployeeFinancialHistory': [],
                  #   'EmployeeDocumentChecklist': [],
                }
                
                Trainees_data.append(Trainee_data)
                
            return JsonResponse(Trainees_data, safe=False)
      except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
        


# @api_view(['GET'])
# def Trainee_Registration_Details(request):
#     search_query = request.GET.get("search", "")

#     if search_query:  
#         trainees = Trainee_Personal_Form_Details.objects.filter(
#             Q(First_Name__icontains=search_query) |  
#             Q(Phone__icontains=search_query)            
#         )
#     else:
#         trainees = Trainee_Personal_Form_Details.objects.all() 

#     results = [
#         {"id": index + 1, **trainee}  
#         for index, trainee in enumerate(trainees.values())  
#     ]  

#     return JsonResponse(results, safe=False)

