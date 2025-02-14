import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import *
from django.db.models import  Q
from django.db import transaction
from PIL import Image
from io import BytesIO
import base64
# import magic
from PyPDF2 import PdfReader, PdfWriter
from Masters.models import *
from Workbench.models import Op_to_Ip_Convertion_Table
from .task import schedule_status_update
from Masters.Login import authenticate_request
from django.db import transaction
from PIL import Image
from io import BytesIO
import base64
# import magic
import filetype
from PyPDF2 import PdfReader, PdfWriter
from Workbench.models import Op_to_Ip_Convertion_Table
from datetime import datetime
from .task import schedule_status_update
from django.utils import timezone
from OutPatient.models import *
from datetime import date
from Workbench.models import *
from Ip_Workbench.models import *

# ABHA
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import base64
from datetime import datetime
import uuid
import json
# from rest_framework.exceptions import IntegrityError
from .models import *
from django.db.models import Max
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q

# @csrf_exempt
# @require_http_methods(["POST", "OPTIONS", "GET"])
# def Patient_Registration(request):
    
#     @transaction.atomic
#     def generate_or_update_visit_id(patient, register_type):
#         # Get today's date
#         today = datetime.now().date()
        
#         # Find the maximum VisitId for the given patient and date
#         existing_visit = Patient_Visit_Detials.objects.filter(
#             PatientId=patient,
#             created_at__date=today
#         ).first()
        
#         if existing_visit:
#             # If a visit record exists for today, you might want to update or perform other actions.
#             # For example, you might just return the existing record or update certain fields.
#             # Here, we simply return the existing record's ID.
#             return existing_visit.VisitId
#         else:
#             # If no visit record exists for today, create a new one
#             max_visit_id = Patient_Visit_Detials.objects.filter(
#                 PatientId=patient
#             ).aggregate(max_id=Max('VisitId'))['max_id']
            
#             next_visit_id = 1 if max_visit_id is None else max_visit_id + 1
            
#             patient_visit = Patient_Visit_Detials.objects.create(
#                 PatientId=patient,
#                 VisitId=next_visit_id,
#                 RegisterType=register_type
#             )
            
#             return patient_visit.VisitId
    
    
   
#     @transaction.atomic
#     def create_or_update_referral(is_referral, referral_source, referral_doctor_instance, register_type, register_id, newdata, created_by):
#         if is_referral == 'Yes':
#             try:
                
#                 if register_id:
#                     filters = {
#                         'OP': 'OP_Register_Id__pk',
#                         'IP': 'IP_Register_Id__pk',
#                         'Casuality': 'Casuality_Register_Id__pk',
#                         'Diagnosis': 'Diagnosis_Register_Id__pk',
#                         'Laboratory': 'Laboratory_Register_Id__pk'
#                     }
#                     filter_key = filters.get(register_type)
#                     if not filter_key:
#                         raise ValueError("Invalid register_type provided.")
#                     if Patient_Referral_Detials.objects.filter(**{filter_key: register_id}).exists():
#                         referral = Patient_Referral_Detials.objects.get(**{filter_key: register_id})
#                         referral.ReferralSource = referral_source
#                         referral.ReferredBy = referral_doctor_instance
#                         referral.save()
#                     else:
#                         Patient_Referral_Detials.objects.create(
#                             **{
#                                 'OP_Register_Id': newdata if register_type == 'OP' else None,
#                                 'IP_Register_Id': newdata if register_type == 'IP' else None,
#                                 'Casuality_Register_Id': newdata if register_type == 'Casuality' else None,
#                                 'Laboratory_Register_Id': newdata if register_type == 'Laboratory' else None,
#                                 'Diagnosis_Register_Id': newdata if register_type == 'Diagnosis' else None
#                             },
#                             ReferralRegisteredBy=register_type,
#                             ReferralSource=referral_source,
#                             ReferredBy=referral_doctor_instance,
#                             created_by=created_by
#                         )
                    
#                 else:
#                     Patient_Referral_Detials.objects.create(
#                         **{
#                             'OP_Register_Id': newdata if register_type == 'OP' else None,
#                             'IP_Register_Id': newdata if register_type == 'IP' else None,
#                             'Casuality_Register_Id': newdata if register_type == 'Casuality' else None,
#                             'Laboratory_Register_Id': newdata if register_type == 'Laboratory' else None,
#                             'Diagnosis_Register_Id': newdata if register_type == 'Diagnosis' else None
#                         },
#                         ReferralRegisteredBy=register_type,
#                         ReferralSource=referral_source,
#                         ReferredBy=referral_doctor_instance,
#                         created_by=created_by
#                     )
#             except ValueError as e:
#                 # Handle invalid register_type
#                 pass
       
#     @transaction.atomic
#     def validate_and_process_file(file):
    
        
#         def get_file_type(file):
#             if file.startswith('data:application/pdf;base64'):
#                 return 'application/pdf'
#             elif file.startswith('data:image/jpeg;base64') or file.startswith('data:image/jpg;base64'):
#                 return 'image/jpeg'
#             elif file.startswith('data:image/png;base64'):
#                 return 'image/png'
#             else:
#                 return 'unknown'

#         def compress_image(image, min_quality=10, step=5):
#             output = BytesIO()
#             quality = 95
#             compressed_data = None
#             while quality >= min_quality:
#                 output.seek(0)
#                 image.save(output, format='PNG', quality=quality)
#                 compressed_data = output.getvalue()
#                 quality -= step
#             output.seek(0)
#             compressed_size = len(compressed_data)
#             return compressed_data, compressed_size

#         def compress_pdf(file):
#             output = BytesIO()
#             reader = PdfReader(file)
#             writer = PdfWriter()
#             for page_num in range(len(reader.pages)):
#                 writer.add_page(reader.pages[page_num])
#             writer.write(output)
#             compressed_data = output.getvalue()
#             compressed_size = len(compressed_data)
#             return compressed_data, compressed_size

#         if file:
#             file_data = file.split(',')[1]
#             file_content = base64.b64decode(file_data)
#             file_size = len(file_content)
            
#             max_size_mb = 5

#             if file_size > max_size_mb * 1024 * 1024:
#                 print('maximum mb')
#                 return JsonResponse({'warn': f'File size exceeds the maximum allowed size ({max_size_mb}MB)'})

#             file_type = get_file_type(file)
            
#             if file_type == 'image/jpeg' or file_type == 'image/png':
#                 try:
#                     image = Image.open(BytesIO(file_content))
#                     if image.mode in ('RGBA', 'P'):
#                         image = image.convert('RGB')
#                     compressed_image_data, compressed_size = compress_image(image)
#                     return compressed_image_data
#                 except Exception as e:
#                     return JsonResponse({'error': f'Error processing image: {str(e)}'})

#             elif file_type == 'application/pdf':
#                 try:
#                     compressed_pdf_data, compressed_size = compress_pdf(BytesIO(file_content))

#                     return compressed_pdf_data
#                 except Exception as e:
#                     return JsonResponse({'error': f'Error processing PDF: {str(e)}'})

#             else:
#                 return JsonResponse({'warn': 'Unsupported file format'})

#         return None
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             print(data,'data')
            
#             # Extract and validate data
            
#             Patient_profile_photo = data.get('PatientPhoto', None)
#             Patient_profile_photo_prossed = validate_and_process_file(Patient_profile_photo) if Patient_profile_photo else None
#             register_type = data.get('RegisterType', '')
#             register_Id = data.get('RegisterId', None)
#             optoip_id = data.get('optoip_id', None)
#             patient_id = data.get('PatientId')
#             phone_no = data.get('PhoneNo', '')
#             title = data.get('Title', '')
#             first_name = data.get('FirstName', '')
#             middle_name = data.get('MiddleName', '')
#             sur_name = data.get('SurName', '')
#             gender = data.get('Gender', '')
#             alias_name = data.get('AliasName', '')
#             MaritalStatus = data.get('MaritalStatus', '')
#             SpouseName = data.get('SpouseName', '')
#             FatherName = data.get('FatherName', '')
#             dob = data.get('DOB', '')
#             age = data.get('Age', '')
#             email = data.get('Email', '')
#             blood_group = data.get('BloodGroup', '')
#             occupation = data.get('Occupation', '')
#             religion = data.get('Religion', '')
#             nationality = data.get('Nationality', '')
#             unique_id_type = data.get('UniqueIdType', '')
#             unique_id_no = data.get('UniqueIdNo', '')
#             Location_Id = data.get('Location', None)
#             visit_purpose = data.get('VisitPurpose', '')
#             specialization = data.get('Specialization', '')
#             doctor_name = data.get('DoctorName', '')
#             complaint = data.get('Complaint', '')
#             patient_type = data.get('PatientType', '')
#             patient_category = data.get('PatientCategory', '')
#             insurance_name = data.get('InsuranceName', '')
#             insurance_type = data.get('InsuranceType', '')
#             client_name = data.get('ClientName', '')
#             client_type = data.get('ClientType', '')
#             client_employee_id = data.get('ClientEmployeeId', '')
#             client_employee_designation = data.get('ClientEmployeeDesignation', '')
#             client_employee_relation = data.get('ClientEmployeeRelation', '')
#             employee_id = data.get('EmployeeId', '')
#             employee_relation = data.get('EmployeeRelation', '')
#             doctor_id = data.get('DoctorId', '')
#             doctor_relation = data.get('DoctorRelation', '')
#             donation_type = data.get('DonationType', '')
#             is_mlc = data.get('IsMLC', 'No')
#             flagging = data.get('Flagging', '')
#             is_referral = data.get('IsReferral', 'No')
#             referral_source = data.get('ReferralSource', '')
#             referred_by = data.get('ReferredBy', '')
#             apptoreg = data.get('apptoreg','')
            
#             door_no = data.get('DoorNo', '')
#             street = data.get('Street', '')
#             area = data.get('Area', '')
#             city = data.get('City', '')
#             District = data.get('District', '')
#             state = data.get('State', '')
#             country = data.get('Country', '')
#             pincode = data.get('Pincode', '')

#             IsConsciousness = data.get('IsConsciousness','')
#             IsConsciousness=True if IsConsciousness=='Yes' else False
            
            
#             IsCasualityPatient = data.get('IsCasualityPatient','')
#             IsCasualityPatientID = data.get('IsCasualityPatientID','')
#             AdmissionPurpose = data.get('AdmissionPurpose','')
#             DrInchargeatTimeofAdmission = data.get('DrInchargeAtTimeOfAdmission','')
#             NexttokinName = data.get('NextToKinName','')
#             relation = data.get('Relation','')
#             relativePhoneno = data.get('RelativePhoneNo','')
#             personLiableforpayment = data.get('PersonLiableForBillPayment','')
#             familyhead = data.get('FamilyHead','')
#             familyheadName = data.get('FamilyHeadName','')
#             ipKitGiven = data.get('IpKitGiven','')

#             created_by = data.get('Created_by', '')
            
            
#             RoomId = data.get('RoomId', '')

#             addedTests=data.get('addedTests',[])
#             TestNames=data.get('TestNames',[])

#             specialization_instance = Speciality_Detials.objects.get(Speciality_Id=specialization) if specialization else None
#             doctor_name_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=doctor_name) if doctor_name else None
#             DrInchargeatTimeofAdmission_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=DrInchargeatTimeofAdmission) if DrInchargeatTimeofAdmission else None
#             referral_doctor_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=referred_by) if referred_by else None
#             employee_instance = Employee_Personal_Form_Detials.objects.get(Employee_ID=employee_id) if employee_id else None
#             doctor_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=doctor_id) if doctor_id else None
#             religion_instance = Religion_Detials.objects.get(Religion_Id=religion) if religion else None
#             location_instance = Location_Detials.objects.get(Location_Id=Location_Id) if Location_Id else None
#             roomid_instance = Room_Master_Detials.objects.get(Room_Id=RoomId) if RoomId else None
#             Flagging_instance = Flaggcolor_Detials.objects.get(Flagg_Id=flagging) if flagging else None
#             BloodGroup_instance = BloodGroup_Detials.objects.get(BloodGroup_Id=blood_group) if blood_group else None
            

#             Insurance_instance = None
#             if insurance_name:
#               Insurance_instance = Insurance_Master_Detials.objects.get(Insurance_Id=insurance_name) 
             
#             print(Insurance_instance,'Insurance_instanceqqqqqqqqqqqq')
            
#             Client_instance = None

#             if client_name:
#                Client_instance = Client_Master_Detials.objects.get(Client_Id=client_name) 
            
#             print(Client_instance,'Client_instanceqqqqqqqqqqq')
            
#             Flagging_instance = None
#             if flagging:
#                 Flagging_instance = Flaggcolor_Detials.objects.get(Flagg_Id=flagging)
            
#             print(Flagging_instance,'Client_instanceqqqqqqqqqqq')

#             # BloodGroup_instance = None
#             # if blood_group:
#             #     BloodGroup_instance = BloodGroup_Detials.objects.get(BloodGroup_Id=blood_group)
            
#             # print(BloodGroup_instance,'blood_groupqqqqqqqqqqq')



#             casuality_patient_instance=None
#             if IsCasualityPatient =='Yes':
#                 casuality_patient_instance = Patient_Casuality_Registration_Detials.objects.get(pk= IsCasualityPatientID) if IsCasualityPatientID else None
            
#             OP_regis_ins =None
#             if optoip_id:
#                 OP_regis_ins = Patient_Appointment_Registration_Detials.objects.get(pk = optoip_id)
                
#             with transaction.atomic():
#                 patient=None
#                 if patient_id :
#                     patient = Patient_Detials.objects.get(PatientId=patient_id)
#                     if not patient:
#                         return JsonResponse({'warn': f"The Patient Id is not valid"})
                    
#                     if Patient_Detials.objects.filter(PhoneNo=phone_no, FirstName=first_name).exclude(PatientId=patient_id).exists():
#                         patient = Patient_Detials.objects.get(PhoneNo=phone_no, FirstName=first_name)

#                         return JsonResponse({'warn': f"The Patient {patient.PatientId} is already registered with {phone_no} and {first_name}"})
                    
                    
                   
#                     patient = Patient_Detials.objects.get(PatientId=patient_id)
#                     patient.Patient_profile = Patient_profile_photo_prossed
#                     patient.PhoneNo = phone_no
#                     patient.Title = title
#                     patient.FirstName = first_name
#                     patient.MiddleName = middle_name
#                     patient.SurName = sur_name
#                     patient.Gender = gender
#                     patient.AliasName = alias_name
#                     patient.MaritalStatus = MaritalStatus
#                     patient.SpouseName = SpouseName
#                     patient.FatherName = FatherName
#                     patient.DOB = dob
#                     patient.Age = age
#                     patient.Email = email
#                     patient.BloodGroup = BloodGroup_instance
#                     patient.Occupation = occupation
#                     patient.Religion = religion_instance
#                     patient.Nationality = nationality
#                     patient.UniqueIdType = unique_id_type
#                     patient.UniqueIdNo = unique_id_no
#                     patient.DoorNo = door_no
#                     patient.Street = street
#                     patient.Area = area
#                     patient.City = city
#                     patient.District = District
#                     patient.State = state
#                     patient.Country = country
#                     patient.Pincode = pincode
#                     patient.updated_by = created_by
#                     patient.save()

#                 else:
#                     if phone_no and first_name:
#                         if Patient_Detials.objects.filter(PhoneNo=phone_no, FirstName=first_name).exists():
#                             patient = Patient_Detials.objects.get(PhoneNo=phone_no, FirstName=first_name)
#                             return JsonResponse({'warn': f"The Patient {patient.PatientId} is already registered with {phone_no} and {first_name}"})
                
#                         patient = Patient_Detials.objects.create(
#                             Patient_profile = Patient_profile_photo_prossed,
#                             PhoneNo=phone_no,
#                             Title=title,
#                             FirstName=first_name,
#                             MiddleName=middle_name, 
#                             SurName=sur_name, 
#                             Gender=gender, 
#                             AliasName=alias_name, 
#                             MaritalStatus=MaritalStatus, 
#                             SpouseName=SpouseName, 
#                             FatherName=FatherName, 
#                             DOB=dob, 
#                             Age=age, 
#                             Email=email, 
#                             BloodGroup=BloodGroup_instance, 
#                             Occupation=occupation, 
#                             Religion=religion_instance, 
#                             Nationality=nationality, 
#                             UniqueIdType=unique_id_type, 
#                             UniqueIdNo=unique_id_no, 
#                             DoorNo=door_no, 
#                             Street=street, 
#                             Area=area, 
#                             City=city, 
#                             District=District, 
#                             State=state, 
#                             Country=country, 
#                             Pincode=pincode, 
#                             created_by=created_by
#                         )
                        
                
#                 # visit id
#                 patient_visit_id=None
#                 if patient:
#                     patient_visit_id = generate_or_update_visit_id(patient,register_type)
                
#                 if not register_Id and not optoip_id:
#                     registration_tables = {
#                         'OP': {'model': Patient_Appointment_Registration_Detials, 'status_field': 'Status', 'statuses': ['completed','Shifted_to_IP']},
#                         'IP': {'model': Patient_IP_Registration_Detials, 'status_field': 'Status', 'statuses': ['discharged']},
#                         'Casuality': {'model': Patient_Casuality_Registration_Detials, 'status_field': 'Status', 'statuses': ['admitted', 'discharged']},
#                         'Diagnosis': {'model': Patient_Diagnosis_Registration_Detials, 'status_field': 'Status', 'statuses': ['completed']},
#                         'Laboratory': {'model': Patient_Laboratory_Registration_Detials, 'status_field': 'Status', 'statuses': ['completed']},
#                     }

#                     # Iterate through each registration type and its corresponding model and statuses
#                     for reg_type, details in registration_tables.items():
#                         model = details['model']
#                         status_field = details['status_field']
#                         statuses = details['statuses']

#                         if patient:
#                             # Check if the patient instance is already present in the current model/table
#                             if model.objects.filter(PatientId=patient).exists():
#                                 # Check if the required statuses do not exist
#                                 if not model.objects.filter(PatientId=patient, **{status_field+'__in': statuses}).exists():
#                                     return JsonResponse({'warn': f"The patient is already available in the {reg_type} "})
                         

#                 if register_Id :
#                     if register_type == 'OP':
#                         OP_appointment_details = Patient_Appointment_Registration_Detials.objects.get(pk = register_Id)
#                         OP_appointment_details.VisitPurpose = visit_purpose
#                         OP_appointment_details.Specialization = specialization_instance
#                         OP_appointment_details.PrimaryDoctor = doctor_name_instance
#                         OP_appointment_details.Complaint = complaint
#                         OP_appointment_details.PatientType = patient_type
#                         OP_appointment_details.PatientCategory = patient_category
#                         OP_appointment_details.InsuranceName = Insurance_instance
#                         OP_appointment_details.InsuranceType = insurance_type
#                         OP_appointment_details.ClientName = Client_instance
#                         OP_appointment_details.ClientType = client_type
#                         OP_appointment_details.ClientEmployeeId = client_employee_id
#                         OP_appointment_details.ClientEmployeeDesignation = client_employee_designation
#                         OP_appointment_details.ClientEmployeeRelation = client_employee_relation
#                         OP_appointment_details.EmployeeId = employee_instance
#                         OP_appointment_details.EmployeeRelation = employee_relation
#                         OP_appointment_details.DoctorId = doctor_instance
#                         OP_appointment_details.DoctorRelation = doctor_relation
#                         OP_appointment_details.DonationType = donation_type
#                         OP_appointment_details.IsMLC = is_mlc
#                         OP_appointment_details.Flagging = Flagging_instance
#                         OP_appointment_details.IsReferral = is_referral
#                         OP_appointment_details.updated_by = created_by
#                         OP_appointment_details.save()
                        
#                         create_or_update_referral(is_referral,referral_source,referral_doctor_instance,register_type,register_Id,OP_appointment_details,created_by)
                        
#                         return JsonResponse({'success': 'Patient Appointment Register Updated successfully'})
#                     elif register_type == 'IP':
#                         ip_details = Patient_IP_Registration_Detials.objects.get(pk=register_Id)
#                         ip_details.Specialization=specialization_instance  
#                         ip_details.PrimaryDoctor=doctor_name_instance
#                         ip_details.Complaint=complaint  
#                         # ip_details.PatientType=patient_type  
#                         # ip_details.PatientCategory=patient_category  
#                         # ip_details.InsuranceName=Insurance_instance  
#                         # ip_details.InsuranceType=insurance_type  
#                         # ip_details.ClientName=Client_instance  
#                         # ip_details.ClientType=client_type  
#                         # ip_details.ClientEmployeeId=client_employee_id  
#                         # ip_details.ClientEmployeeDesignation=client_employee_designation  
#                         # ip_details.ClientEmployeeRelation=client_employee_relation  
#                         # ip_details.EmployeeId=employee_instance  
#                         # ip_details.EmployeeRelation=employee_relation  
#                         # ip_details.DoctorId=doctor_instance  
#                         # ip_details.DoctorRelation=doctor_relation  
#                         # ip_details.DonationType=donation_type  
#                         ip_details.IsMLC=is_mlc  
#                         ip_details.Flagging=Flagging_instance  
#                         ip_details.IsReferral=is_referral  
#                         ip_details.updated_by = created_by
#                         ip_details.save()
                        
#                         ip_admission = Patient_Admission_Detials.objects.get(IP_Registration_Id__pk = ip_details.pk)
#                         ip_admission.AdmissionPurpose = AdmissionPurpose 
#                         ip_admission.DrInchargeAtTimeOfAdmission = DrInchargeatTimeofAdmission_instance 
#                         ip_admission.NextToKinName = NexttokinName 
#                         ip_admission.Relation = relation 
#                         ip_admission.RelativePhoneNo = relativePhoneno 
#                         ip_admission.PersonLiableForPayment = personLiableforpayment 
#                         ip_admission.FamilyHead = familyhead 
#                         ip_admission.FamilyHeadName = familyheadName 
#                         ip_admission.IpKitGiven = ipKitGiven 
#                         ip_admission.updated_by = created_by
#                         ip_admission.save()
                        
#                         create_or_update_referral(is_referral,referral_source,referral_doctor_instance,register_type,register_Id,ip_details,created_by)
                        
#                         return JsonResponse({'success': 'Patient Admission Detials Updated successfully'})
                    
#                     elif register_type == 'Casuality':
#                         casuality_details = Patient_Casuality_Registration_Detials.objects.get(Registration_Id=register_Id)
#                         casuality_details.PatientId= patient if phone_no and first_name else None
#                         casuality_details.VisitId=patient_visit_id  
#                         casuality_details.IsConsciousness=IsConsciousness  
#                         casuality_details.Specialization=specialization_instance  
#                         casuality_details.PrimaryDoctor=doctor_name_instance  
#                         casuality_details.Complaint=complaint  
#                         casuality_details.PatientType=patient_type  
#                         casuality_details.PatientCategory=patient_category  
#                         casuality_details.InsuranceName=Insurance_instance  
#                         casuality_details.InsuranceType=insurance_type  
#                         casuality_details.ClientName=Client_instance
#                         casuality_details.ClientType=client_type  
#                         casuality_details.ClientEmployeeId=client_employee_id  
#                         casuality_details.ClientEmployeeDesignation=client_employee_designation  
#                         casuality_details.ClientEmployeeRelation=client_employee_relation  
#                         casuality_details.EmployeeId=employee_instance  
#                         casuality_details.EmployeeRelation=employee_relation  
#                         casuality_details.DoctorId=doctor_instance  
#                         casuality_details.DoctorRelation=doctor_relation  
#                         casuality_details.DonationType=donation_type  
#                         casuality_details.IsMLC=is_mlc  
#                         casuality_details.Flagging=Flagging_instance  
#                         casuality_details.IsReferral=is_referral 
#                         casuality_details.updated_by =created_by
#                         casuality_details.save()

#                         casuality_admission = Patient_Admission_Detials.objects.get(Casuality_Registration_Id__pk = casuality_details.pk)
#                         casuality_admission.NextToKinName = NexttokinName 
#                         casuality_admission.Relation = relation 
#                         casuality_admission.RelativePhoneNo = relativePhoneno 
#                         casuality_admission.updated_by = created_by
#                         casuality_admission.save()
                        
                        
                        
#                         create_or_update_referral(is_referral,referral_source,referral_doctor_instance,register_type,register_Id,casuality_details,created_by)
                        
#                         return JsonResponse({'success': 'Casuality Register Updated successfully'})
                    
#                     elif register_type == 'Diagnosis':
#                         diagnosis_details = Patient_Diagnosis_Registration_Detials.objects.get(PatientId=patient)
#                         diagnosis_details.VisitId=patient_visit_id  
#                         diagnosis_details.Specialization = specialization_instance
#                         diagnosis_details.PrimaryDoctor = doctor_name_instance
#                         diagnosis_details.Complaint=complaint  
#                         diagnosis_details.PatientType=patient_type  
#                         diagnosis_details.PatientCategory=patient_category  
#                         diagnosis_details.InsuranceName=Insurance_instance  
#                         diagnosis_details.InsuranceType=insurance_type  
#                         diagnosis_details.ClientName=Client_instance  
#                         diagnosis_details.ClientType=client_type  
#                         diagnosis_details.ClientEmployeeId=client_employee_id  
#                         diagnosis_details.ClientEmployeeDesignation=client_employee_designation  
#                         diagnosis_details.ClientEmployeeRelation=client_employee_relation  
#                         diagnosis_details.EmployeeId=employee_instance  
#                         diagnosis_details.EmployeeRelation=employee_relation  
#                         diagnosis_details.DoctorId=doctor_instance  
#                         diagnosis_details.DoctorRelation=doctor_relation  
#                         diagnosis_details.DonationType=donation_type  
#                         diagnosis_details.IsMLC=is_mlc  
#                         diagnosis_details.Flagging=Flagging_instance  
#                         diagnosis_details.IsReferral=is_referral  
#                         diagnosis_details.updated_by = created_by
#                         diagnosis_details.save()

#                         diagnosis_admission = Patient_Admission_Detials.objects.get(Diagnosis_Registration_Id__pk = diagnosis_details.pk)
#                         diagnosis_admission.NextToKinName = NexttokinName 
#                         diagnosis_admission.Relation = relation 
#                         diagnosis_admission.RelativePhoneNo = relativePhoneno 
#                         diagnosis_admission.updated_by = created_by
#                         diagnosis_admission.save()
                        
#                         create_or_update_referral(is_referral,referral_source,referral_doctor_instance,register_type,register_Id,diagnosis_details,created_by)
                        
#                         return JsonResponse({'success': 'Diagnosis Register Updated successfully'})
                    
#                     elif register_type == 'Laboratory':
#                         laboratory_details = Patient_Laboratory_Registration_Detials.objects.get(PatientId=patient)
#                         laboratory_details.VisitId=patient_visit_id 
#                         laboratory_details.Specialization = specialization_instance
#                         laboratory_details.PrimaryDoctor = doctor_name_instance 
#                         laboratory_details.Complaint=complaint  
#                         laboratory_details.PatientType=patient_type  
#                         laboratory_details.PatientCategory=patient_category  
#                         laboratory_details.InsuranceName=Insurance_instance  
#                         laboratory_details.InsuranceType=insurance_type  
#                         laboratory_details.ClientName=Client_instance  
#                         laboratory_details.ClientType=client_type  
#                         laboratory_details.ClientEmployeeId=client_employee_id  
#                         laboratory_details.ClientEmployeeDesignation=client_employee_designation  
#                         laboratory_details.ClientEmployeeRelation=client_employee_relation  
#                         laboratory_details.EmployeeId=employee_instance  
#                         laboratory_details.EmployeeRelation=employee_relation  
#                         laboratory_details.DoctorId=doctor_instance  
#                         laboratory_details.DoctorRelation=doctor_relation  
#                         laboratory_details.DonationType=donation_type  
#                         laboratory_details.IsMLC=is_mlc  
#                         laboratory_details.Flagging=Flagging_instance  
#                         laboratory_details.IsReferral=is_referral  
#                         laboratory_details.updated_by = created_by
                        
#                         laboratory_details.save()

#                         laboratory_admission = Patient_Admission_Detials.objects.get(Laboratory_Registration_Id__pk = laboratory_details.pk)
#                         laboratory_admission.NextToKinName = NexttokinName 
#                         laboratory_admission.Relation = relation 
#                         laboratory_admission.RelativePhoneNo = relativePhoneno 
#                         laboratory_admission.updated_by = created_by
#                         laboratory_admission.save()
#                         create_or_update_referral(is_referral,referral_source,referral_doctor_instance,register_type,register_Id,laboratory_details,created_by)
                        
#                         return JsonResponse({'success': 'Laboratory Register Updated successfully'})
#                 else:
#                     if register_type == 'OP': 
#                         appointment_instance = None
#                         if apptoreg:
#                             appointment_instance = Appointment_Request_List.objects.get(appointment_id = apptoreg)
#                         if Patient_Appointment_Registration_Detials.objects.filter(PatientId = patient,Status = 'Pending').exists():
#                             return JsonResponse({'warn': 'Patient Request is already in pending'})
                                                
#                         else:
#                             Patient_OP = Patient_Appointment_Registration_Detials.objects.create(
#                             PatientId = patient,
#                             VisitId = patient_visit_id,  
#                             VisitPurpose = visit_purpose, 
#                             Specialization = specialization_instance, 
#                             PrimaryDoctor = doctor_name_instance, 
#                             Complaint = complaint, 
#                             PatientType = patient_type, 
#                             PatientCategory = patient_category, 
#                             InsuranceName = Insurance_instance,
#                             InsuranceType = insurance_type, 
#                             ClientName = Client_instance, 
#                             ClientType = client_type, 
#                             ClientEmployeeId = client_employee_id, 
#                             ClientEmployeeDesignation = client_employee_designation, 
#                             ClientEmployeeRelation = client_employee_relation, 
#                             EmployeeId = employee_instance, 
#                             EmployeeRelation = employee_relation, 
#                             DoctorId = doctor_instance, 
#                             DoctorRelation = doctor_relation, 
#                             DonationType = donation_type, 
#                             IsMLC = is_mlc, 
#                             Flagging = Flagging_instance, 
#                             IsReferral = is_referral, 
#                             created_by = created_by,
#                             Location=location_instance,
#                             ApptoRegId = appointment_instance,
#                             )
#                             if apptoreg:
#                                 appstatus= Appointment_Request_List.objects.get(pk=apptoreg)
                                
#                                 appstatus.status = 'REGISTERED'
#                                 appstatus.save()
                                
#                             create_or_update_referral(is_referral,referral_source,referral_doctor_instance,register_type,register_Id,Patient_OP,created_by)
#                         return JsonResponse({'success': 'Patient Appointment registered successfully'})
                    
#                     elif register_type == 'IP':
#                         Patient_IP = Patient_IP_Registration_Detials.objects.create(
#                             PatientId=patient,
#                             VisitId=patient_visit_id,
#                             Specialization=specialization_instance, 
#                             PrimaryDoctor=doctor_name_instance, 
#                             Complaint=complaint, 
#                             # PatientType=patient_type, 
#                             # PatientCategory=patient_category, 
#                             # InsuranceName=Insurance_instance, 
#                             # InsuranceType=insurance_type, 
#                             # ClientName=Client_instance, 
#                             # ClientType=client_type, 
#                             # ClientEmployeeId=client_employee_id, 
#                             # ClientEmployeeDesignation=client_employee_designation, 
#                             # ClientEmployeeRelation=client_employee_relation, 
#                             # EmployeeId=employee_instance, 
#                             # EmployeeRelation=employee_relation, 
#                             # DoctorId=doctor_instance, 
#                             # DoctorRelation=doctor_relation, 
#                             # DonationType=donation_type, 
#                             IsMLC=is_mlc, 
#                             Flagging=Flagging_instance, 
#                             IsReferral=is_referral, 
#                             created_by=created_by,
#                             Location=location_instance
#                         )
                        
#                         Patient_Admission_Detials.objects.create(
#                             IsConverted = True if optoip_id else False,
#                             OP_Registration_Id = OP_regis_ins,
#                             IsCasualityPatient = True if IsCasualityPatient =='Yes' else False  ,
#                             IP_Registration_Id = Patient_IP,
#                             Casuality_Registration_Id = casuality_patient_instance,
#                             AdmissionPurpose = AdmissionPurpose,
#                             DrInchargeAtTimeOfAdmission = DrInchargeatTimeofAdmission_instance,
#                             NextToKinName = NexttokinName,
#                             Relation = relation,
#                             RelativePhoneNo = relativePhoneno,
#                             PersonLiableForPayment = personLiableforpayment,
#                             FamilyHead = familyhead,
#                             FamilyHeadName = familyheadName,
#                             IpKitGiven = ipKitGiven,
#                         )
#                         if OP_regis_ins and optoip_id:
                                                    
#                             opip_ins = Op_to_Ip_Convertion_Table.objects.get(Registration_id = OP_regis_ins)
#                             opip_ins.Status = 'Completed'
#                             opip_ins.save()
                            
#                         Patient_Admission_Room_Detials.objects.create(
#                             RegisterType = register_type,
#                             IP_Registration_Id = Patient_IP,
#                             Casuality_Registration_Id = None,
#                             RoomId = roomid_instance,
#                             created_by=created_by
#                         )
#                         create_or_update_referral(is_referral,referral_source,referral_doctor_instance,register_type,register_Id,Patient_IP,created_by)
                        
#                         return JsonResponse({'success': 'Patient Admitted successfully'})
                    
#                     elif register_type == 'Casuality':
#                         print('---',patient)
#                         Patient_Casuality = Patient_Casuality_Registration_Detials.objects.create(
#                             PatientId= patient if phone_no and first_name else None,
#                             VisitId=patient_visit_id,
#                             IsConsciousness=IsConsciousness,
#                             Specialization=specialization_instance, 
#                             PrimaryDoctor=doctor_name_instance, 
#                             Complaint=complaint, 
#                             PatientType=patient_type, 
#                             PatientCategory=patient_category, 
#                             InsuranceName=Insurance_instance, 
#                             InsuranceType=insurance_type, 
#                             ClientName=Client_instance, 
#                             ClientType=client_type, 
#                             ClientEmployeeId=client_employee_id, 
#                             ClientEmployeeDesignation=client_employee_designation, 
#                             ClientEmployeeRelation=client_employee_relation, 
#                             EmployeeId=employee_instance, 
#                             EmployeeRelation=employee_relation, 
#                             DoctorId=doctor_instance, 
#                             DoctorRelation=doctor_relation, 
#                             DonationType=donation_type, 
#                             IsMLC=is_mlc, 
#                             Flagging=Flagging_instance, 
#                             IsReferral=is_referral, 
#                             created_by=created_by,
#                             Location=location_instance
#                         )

                        

                        
                        
#                         Patient_Admission_Room_Detials.objects.create(
#                             RegisterType = register_type,
#                             IP_Registration_Id = None,
#                             Casuality_Registration_Id = Patient_Casuality,
#                             RoomId = roomid_instance
#                         )
                        
#                         create_or_update_referral(is_referral,referral_source,referral_doctor_instance,register_type,register_Id,Patient_Casuality,created_by)

#                         Patient_Admission_Detials.objects.create(
#                             IsConverted = True if optoip_id else False,
#                             IsCasualityPatient = True if IsCasualityPatient =='Yes' else False,
#                             IP_Registration_Id = None,
#                             OP_Registration_Id = None,
#                             Casuality_Registration_Id = Patient_Casuality,
#                             Diagnosis_Registration_Id = None,
#                             Laboratory_Registration_Id = None,
#                             NextToKinName = NexttokinName,
#                             Relation = relation,
#                             RelativePhoneNo = relativePhoneno,
                            
#                         )
#                         return JsonResponse({'success': 'Casuality Registered successfully'})
#                     elif register_type == 'Diagnosis':
#                         Patient_Diagnosis = Patient_Diagnosis_Registration_Detials.objects.create(
#                             PatientId=patient,
#                             VisitId=patient_visit_id,
#                             Specialization = specialization_instance,
#                             PrimaryDoctor = doctor_name_instance,
#                             Complaint=complaint, 
#                             PatientType=patient_type, 
#                             PatientCategory=patient_category, 
#                             InsuranceName=Insurance_instance, 
#                             InsuranceType=insurance_type, 
#                             ClientName=Client_instance, 
#                             ClientType=client_type, 
#                             ClientEmployeeId=client_employee_id, 
#                             ClientEmployeeDesignation=client_employee_designation, 
#                             ClientEmployeeRelation=client_employee_relation, 
#                             EmployeeId=employee_instance, 
#                             EmployeeRelation=employee_relation, 
#                             DoctorId=doctor_instance, 
#                             DoctorRelation=doctor_relation, 
#                             DonationType=donation_type, 
#                             IsMLC=is_mlc, 
#                             Flagging=Flagging_instance, 
#                             IsReferral=is_referral, 
#                             created_by=created_by,
#                             Location=location_instance
#                         )


#                         if addedTests:
#                             print("addedTests", addedTests)
#                             for add in addedTests:
#                                 radiologyid = add.get('id', '')
#                                 testid = add.get('testid', '')
#                                 if radiologyid and testid:
#                                     try:
#                                         radiology_instance = RadiologyNames_Details.objects.get(pk=radiologyid)
#                                         if not radiology_instance:
#                                             return JsonResponse({'warn': f'Radiologyname {radiologyid} does not exist'})
#                                     except RadiologyNames_Details.DoesNotExist:
#                                         return JsonResponse({'warn': f'Radiologyname {radiologyid} does not exist'})
#                                     try:
#                                         subtest_instance = TestName_Details.objects.get(Test_Code=testid)
#                                         if not subtest_instance:
#                                             return JsonResponse({'warn': f'testname {testid} does not exist'})
#                                     except TestName_Details.DoesNotExist:
#                                         return JsonResponse({'warn': f'testname {testid} does not exist'})
                                
#                                 print("Patient_Diagnosis", Patient_Diagnosis)
#                                 Radiology_Request_Details.objects.create(
#                                     RegisterType="ExternalRadiology",
#                                     Diagnosis_Register_Id=Patient_Diagnosis,
#                                     TestCode=radiology_instance.Radiology_Id,
#                                     SubTestCode=subtest_instance.Test_Code,
#                                     Status="Request",
#                                     created_by=created_by
                                   
#                                 )
#                         create_or_update_referral(is_referral,referral_source,referral_doctor_instance,register_type,register_Id,Patient_Diagnosis,created_by)

#                         Patient_Admission_Detials.objects.create(
#                             IsConverted = True if optoip_id else False,
#                             IsCasualityPatient = True if IsCasualityPatient =='Yes' else False  ,
#                             IP_Registration_Id = None,
#                             OP_Registration_Id = None,
#                             Casuality_Registration_Id = None,
#                             Laboratory_Registration_Id = None,
#                             Diagnosis_Registration_Id = Patient_Diagnosis,
#                             NextToKinName = NexttokinName,
#                             Relation = relation,
#                             RelativePhoneNo = relativePhoneno,
                            
#                         )
#                         return JsonResponse({'success': 'Diagnosis Registered successfully'})
                    
#                     elif register_type == 'Laboratory':

#                         Patient_Laboratory = Patient_Laboratory_Registration_Detials.objects.create(
#                             PatientId=patient,
#                             VisitId=patient_visit_id, 
#                             Specialization = specialization_instance,
#                             PrimaryDoctor = doctor_name_instance,
#                             Complaint=complaint, 
#                             PatientType=patient_type, 
#                             PatientCategory=patient_category, 
#                             InsuranceName=Insurance_instance, 
#                             InsuranceType=insurance_type, 
#                             ClientName=Client_instance, 
#                             ClientType=client_type, 
#                             ClientEmployeeId=client_employee_id, 
#                             ClientEmployeeDesignation=client_employee_designation, 
#                             ClientEmployeeRelation=client_employee_relation, 
#                             EmployeeId=employee_instance, 
#                             EmployeeRelation=employee_relation, 
#                             DoctorId=doctor_instance, 
#                             DoctorRelation=doctor_relation, 
#                             DonationType=donation_type, 
#                             IsMLC=is_mlc, 
#                             Flagging=Flagging_instance, 
#                             IsReferral=is_referral, 
#                             created_by=created_by,
#                             Location=location_instance
#                         )

#                         lab_request = Lab_Request_Details.objects.create(
#                         created_by=created_by,
#                         Location=location_instance,
#                         Lab_Register_Id = Patient_Laboratory, 
#                         )

#                         if TestNames:
#                             print("TestNames",TestNames)
#                             for test in TestNames:
#                                 testcode = test.get('TestCode', '')
#                                 testtype = "Indivitual"
#                                 try:
#                                     testcode_ins = Lab_Request_Details.objects.get(TestCode=testcode)
#                                 except LabTestName_Details.DoesNotExist:
#                                     return JsonResponse({'warn': f'Test code {testcode} does not exist'})
                               
#                                 print("Patient_Laboratory",Patient_Laboratory)
#                                 Lab_Request_Details.objects.create(
#                                     RegisterType="ExternalLab",
#                                     Laboratory_Register_Id=Patient_Laboratory,
#                                     TestType=testtype,
#                                     IndivitualCode=testcode_ins,
#                                     created_by=created_by,
#                                     Status='Request'
#                                 )    
                                   
#                         create_or_update_referral(is_referral,referral_source,referral_doctor_instance,register_type,register_Id,Patient_Laboratory,created_by)
                        
#                         Patient_Admission_Detials.objects.create(
#                             IsConverted = True if optoip_id else False,
#                             IsCasualityPatient = True if IsCasualityPatient =='Yes' else False  ,
#                             IP_Registration_Id = None,
#                             OP_Registration_Id = None,
#                             Casuality_Registration_Id = None,
#                             Diagnosis_Registration_Id = None,
#                             Laboratory_Registration_Id = Patient_Laboratory,
#                             NextToKinName = NexttokinName,
#                             Relation = relation,
#                             RelativePhoneNo = relativePhoneno,
                            
#                         )
#                         return JsonResponse({'success': 'Laboratory Registered successfully'})
                    
#                 return JsonResponse({'success': 'Patient Detials updated successfully'})

           

#         except Patient_Detials.DoesNotExist:
#             return JsonResponse({'error': 'Patient with the given ID does not exist'})
#         except Doctor_Personal_Form_Detials.DoesNotExist:
#             return JsonResponse({'error': 'Doctor or referred doctor does not exist'})
#         except Exception as e:
#             return JsonResponse({'error': str(e)})

#     elif request.method == 'GET':
#         try:
#             patient_id = request.GET.get('PatientId')
#             if patient_id:
#                 patient = Patient_Detials.objects.get(PatientId=patient_id)
#                 return JsonResponse({
#                     'id': patient.PatientId,
#                     'phoneNo': patient.PhoneNo,
#                     'firstName': patient.FirstName,
#                     'lastName': patient.SurName,
#                 })
#             else:
#                 patients = list(Patient_Detials.objects.values())
#                 return JsonResponse(patients, safe=False)
#         except Patient_Detials.DoesNotExist:
#             return JsonResponse({'error': 'Patient with the given ID does not exist'})
#         except Exception as e:
#             return JsonResponse({'error': str(e)})
        
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=405)



@csrf_exempt
@require_http_methods(["POST", "OPTIONS", "GET"])
def Patient_Registration(request):
       
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
                image.save(output, format='PNG', quality=quality)
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
            file_data = file.split(',')[1]
            file_content = base64.b64decode(file_data)
            file_size = len(file_content)
            
            max_size_mb = 5

            if file_size > max_size_mb * 1024 * 1024:
                print('maximum mb')
                return JsonResponse({'warn': f'File size exceeds the maximum allowed size ({max_size_mb}MB)'})

            file_type = get_file_type(file)
            
            if file_type == 'image/jpeg' or file_type == 'image/png':
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
            print(data,'data')
            
            # Extract and validate data
            
            Patient_profile_photo = data.get('Photo', None)
            Patient_profile_photo_prossed = validate_and_process_file(Patient_profile_photo) if Patient_profile_photo else None
            patient_id = data.get('PatientId','')
            title = data.get('Title', '')
            first_name = data.get('FirstName', '')
            middle_name = data.get('MiddleName', '')
            sur_name = data.get('SurName', '')
            gender = data.get('Gender', '')
            MaritalStatus = data.get('MaritalStatus', '')
            SpouseName = data.get('SpouseName', '')
            FatherName = data.get('FatherName', '')
            dob = data.get('DOB', '')
            age = data.get('Age', '')
            phone_no = data.get('PhoneNo', '')
            email = data.get('Email', '')
            blood_group = data.get('BloodGroup', '')
            occupation = data.get('Occupation', '')
            religion = data.get('Religion', '')
            nationality = data.get('Nationality', '')
            unique_id_type = data.get('UHIDType', '')
            unique_id_no = data.get('UHIDNo', '')
            patient_type = data.get('PatientType', '')
            patient_category = data.get('PatientCategory', '')
            insurance_name = data.get('InsuranceName', '')
            insurance_type = data.get('InsuranceType', '')
            client_name = data.get('ClientName', '')
            client_type = data.get('ClientType', '')
            client_employee_id = data.get('ClientEmployeeId', '')
            client_employee_designation = data.get('ClientEmployeeDesignation', '')
            client_employee_relation = data.get('ClientEmployeeRelation', '')
            CorporateName = data.get('CorporateName', '')
            CorporateType = data.get('CorporateType', '')
            CorporateEmployeeId = data.get('CorporateEmployeeId', '')
            CorporateEmployeeDesignation = data.get('CorporateEmployeeDesignation', '')
            CorporateEmployeeRelation = data.get('CorporateEmployeeRelation', '')
            employee_id = data.get('EmployeeId', '')
            employee_relation = data.get('EmployeeRelation', '')
            doctor_id = data.get('DoctorId', '')
            referdocid = data.get('referdocid', '')

            doctor_relation = data.get('DoctorRelation', '')
            donation_type = data.get('DonationType', '')
            flagging = data.get('Flagging', '')
            
            pincode = data.get('Pincode', '')
            door_no = data.get('DoorNo', '')
            street = data.get('Street', '')
            area = data.get('Area', '')
            city = data.get('City', '')
            District = data.get('District', '')
            state = data.get('State', '')
            country = data.get('Country', '')

            PermanentAddressSameAsAbove = data.get('PermanentAddressSameAsAbove', '')
            
            PermanentPincode = data.get('PermanentPincode', '')
            PermanentdoorNo = data.get('PermanentdoorNo', '')
            PermanentStreet = data.get('PermanentStreet', '')
            PermanentArea = data.get('PermanentArea', '')
            PermanentCity = data.get('PermanentCity', '')
            PermanentDistrict = data.get('PermanentDistrict', '')
            PermanentState = data.get('PermanentState', '')
            PermanentCountry = data.get('PermanentCountry', '')
            Appointment_Id = data.get('AppointmentToRegistrationId', '')


            doctor_name = data.get('DoctorName', '')
            IsConsciousness = data.get('IsConsciousness','')
            IsConsciousness=True if IsConsciousness=='Yes' else False
            created_by = data.get('Created_by', '')
            ABHA = data.get('ABHA', '')
            

            doctor_name = data.get('DoctorID', '')
            specialization = data.get('SpecializationId', '')
            
            specialization_instance = Speciality_Detials.objects.get(Speciality_Id=specialization) if specialization else None
            doctor_name_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=doctor_name) if doctor_name else None
            # DrInchargeatTimeofAdmission_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=DrInchargeatTimeofAdmission) if DrInchargeatTimeofAdmission else None
            # referral_doctor_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=referred_by) if referred_by else None
            employee_instance = Employee_Personal_Form_Detials.objects.get(Employee_ID=employee_id) if employee_id else None
            doctor_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=doctor_id) if doctor_id else None
            religion_instance = Religion_Detials.objects.get(Religion_Id=religion) if religion else None
            # location_instance = Location_Detials.objects.get(Location_Id=Location_Id) if Location_Id else None
            # roomid_instance = Room_Master_Detials.objects.get(Room_Id=RoomId) if RoomId else None
            # Flagging_instance = Flaggcolor_Detials.objects.get(Flagg_Id=flagging) if flagging else None
            # BloodGroup_instance = BloodGroup_Detials.objects.get(BloodGroup_Id=blood_group) if blood_group else None
            Title_instance = Title_Detials.objects.get(Title_Id=title) if title else None
            referral_doctor_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=referdocid) if referdocid else None

            Insurance_instance = None
            if insurance_name:
              Insurance_instance = Insurance_Master_Detials.objects.get(Insurance_Id=insurance_name) 
             
            print(Insurance_instance,'Insurance_instanceqqqqqqqqqqqq')
            
            Client_instance = None
            if client_name:
               Client_instance = Client_Master_Detials.objects.get(Client_Id=client_name) 
            
            Donation_instance = None
            if donation_type:
               Donation_instance = Donation_Master_Detials.objects.get(Donation_Id=donation_type) 
            
            Corporate_instance = None
            if CorporateName:
               Corporate_instance = Corporate_Master_Detials.objects.get(Corporate_Id=CorporateName) 
            
            print(Client_instance,'Client_instanceqqqqqqqqqqq')
            
            Flagging_instance = None
            if flagging:
                Flagging_instance = Flaggcolor_Detials.objects.get(Flagg_Id=flagging)
            
            print(Flagging_instance,'Flagging_instance')

            BloodGroup_instance = None
            if blood_group:
                BloodGroup_instance = BloodGroup_Detials.objects.get(BloodGroup_Id=blood_group)
            
            print(BloodGroup_instance,'blood_groupqqqqqqqqqqq')


            with transaction.atomic():
                patient=None
                if patient_id :
                    patient = Patient_Detials.objects.get(PatientId=patient_id)
                    if not patient:
                        return JsonResponse({'warn': f"The Patient Id is not valid"})
                    
                    if Patient_Detials.objects.filter(PhoneNo=phone_no, FirstName=first_name).exclude(PatientId=patient_id).exists():
                        patient = Patient_Detials.objects.get(PhoneNo=phone_no, FirstName=first_name)

                        return JsonResponse({'warn': f"The Patient {patient.PatientId} is already registered with {phone_no} and {first_name}"})
                    
                    
                   
                    patient = Patient_Detials.objects.get(PatientId=patient_id)
                    patient.Patient_profile = Patient_profile_photo_prossed
                    patient.Title = Title_instance
                    patient.FirstName = first_name
                    patient.MiddleName = middle_name
                    patient.SurName = sur_name
                    patient.Gender = gender
                    patient.MaritalStatus = MaritalStatus
                    patient.SpouseName = SpouseName
                    patient.FatherName = FatherName
                    patient.DOB = dob
                    patient.Age = age
                    patient.PhoneNo = phone_no
                    patient.Email = email
                    patient.BloodGroup = BloodGroup_instance
                    patient.Occupation = occupation
                    patient.Religion = religion_instance
                    patient.Nationality = nationality
                    patient.UniqueIdType = unique_id_type
                    patient.UniqueIdNo = unique_id_no
                    patient.PatientType = patient_type
                    # patient.PatientCategory = patient_category
                    # patient.InsuranceName = Insurance_instance
                    # patient.InsuranceType = insurance_type
                    # patient.ClientName = Client_instance
                    # patient.ClientType = client_type
                    # patient.ClientEmployeeId = client_employee_id
                    # patient.ClientEmployeeDesignation = client_employee_designation
                    # patient.ClientEmployeeRelation = client_employee_relation
                    # patient.CorporateName = Corporate_instance
                    # patient.CorporateType = CorporateType
                    # patient.CorporateEmployeeId = CorporateEmployeeId
                    # patient.CorporateEmployeeDesignation = CorporateEmployeeDesignation
                    # patient.CorporateEmployeeRelation = CorporateEmployeeRelation
                    # patient.EmployeeId = employee_instance
                    # patient.EmployeeRelation = employee_relation
                    # patient.DoctorId = doctor_instance
                    # patient.DoctorRelation = doctor_relation
                    # patient.DonationType = Donation_instance
                    # patient.Flagging = Flagging_instance
                   
                    patient.Pincode = pincode
                    patient.DoorNo = door_no
                    patient.Street = street
                    patient.Area = area
                    patient.City = city
                    patient.District = District
                    patient.State = state
                    patient.Country = country

                    patient.PermanentAddressSameAsAbove = PermanentAddressSameAsAbove
                   
                    patient.PermanentPincode = PermanentPincode
                    patient.PermanentdoorNo = PermanentdoorNo
                    patient.PermanentStreet = PermanentStreet
                    patient.PermanentArea = PermanentArea
                    patient.PermanentCity = PermanentCity
                    patient.PermanentDistrict = PermanentDistrict
                    patient.PermanentState = PermanentState
                    patient.PermanentCountry = PermanentCountry


                    patient.ABHA = ABHA
                    patient.updated_by = created_by
                    patient.save()

                else:
                    if phone_no and first_name:
                        if Patient_Detials.objects.filter(PhoneNo=phone_no, FirstName=first_name).exists():
                            patient = Patient_Detials.objects.get(PhoneNo=phone_no, FirstName=first_name)
                            return JsonResponse({'warn': f"The Patient {patient.PatientId} is already registered with {phone_no} and {first_name}"})
                
                        patient = Patient_Detials.objects.create(
                            Patient_profile = Patient_profile_photo_prossed,
                            Title=Title_instance,
                            FirstName=first_name,
                            MiddleName=middle_name, 
                            SurName=sur_name, 
                            Gender=gender, 
                            # AliasName=alias_name, 
                            MaritalStatus=MaritalStatus, 
                            SpouseName=SpouseName, 
                            FatherName=FatherName, 
                            DOB=dob, 
                            Age=age, 
                            PhoneNo=phone_no,
                            Email=email, 
                            BloodGroup=BloodGroup_instance, 
                            Occupation=occupation, 
                            Religion=religion_instance, 
                            Nationality=nationality, 
                            UniqueIdType=unique_id_type, 
                            UniqueIdNo=unique_id_no, 

                            PatientType = patient_type, 
                            
                            # PatientCategory = patient_category,
                            # InsuranceName = Insurance_instance,
                            # InsuranceType = insurance_type, 
                            # ClientName = Client_instance, 
                            # ClientType = client_type, 
                            # ClientEmployeeId = client_employee_id, 
                            # ClientEmployeeDesignation = client_employee_designation, 
                            # ClientEmployeeRelation = client_employee_relation, 
                           
                            # CorporateName = CorporateName, 
                            # CorporateType = CorporateType, 
                            # CorporateEmployeeId = CorporateEmployeeId, 
                            # CorporateEmployeeDesignation = CorporateEmployeeDesignation, 
                            # CorporateEmployeeRelation = CorporateEmployeeRelation, 
                            
                            # EmployeeId = employee_instance, 
                            # EmployeeRelation = employee_relation, 
                            # DoctorId = doctor_instance, 
                            # DoctorRelation = doctor_relation, 
                            # DonationType = donation_type, 
                            # Flagging = Flagging_instance, 
                            
                            Pincode=pincode, 
                            DoorNo=door_no, 
                            Street=street, 
                            Area=area, 
                            City=city, 
                            District=District, 
                            State=state, 
                            Country=country, 
                           
                            PermanentAddressSameAsAbove=PermanentAddressSameAsAbove, 
                            PermanentPincode=PermanentPincode, 
                            PermanentdoorNo=PermanentdoorNo, 
                            PermanentStreet=PermanentStreet, 
                            PermanentArea=PermanentArea, 
                            PermanentCity=PermanentCity, 
                            PermanentDistrict=PermanentDistrict, 
                            PermanentState=PermanentState, 
                            PermanentCountry=PermanentCountry, 
                            ABHA=ABHA,
                            DoctorID=doctor_name_instance,
                            SpecializationId=specialization_instance,
                            created_by=created_by,
                            ReferredBy = referral_doctor_instance
                           
                        )

                        if Appointment_Id:
                            AppointmentRequest = Appointment_Request_List.objects.get(appointment_id = Appointment_Id)
                            AppointmentRequest.status = "REGISTERED"
                            AppointmentRequest.save()
                    
                    data['patient_id'] = patient.PatientId
                    return JsonResponse({'success': 'Patient Detials Saved successfully','data': [data]},safe=False)

        except Patient_Detials.DoesNotExist:
            return JsonResponse({'error': 'Patient with the given ID does not exist'})
        except Doctor_Personal_Form_Detials.DoesNotExist:
            return JsonResponse({'error': 'Doctor or referred doctor does not exist'})
        except Exception as e:
            return JsonResponse({'error': str(e)})

    elif request.method == 'GET':
        try:
            patient_id = request.GET.get('PatientId')

            if patient_id:
                patient = Patient_Detials.objects.get(PatientId=patient_id)

                Patients_dict = {
                    'id': patient.PatientId,
                    'phoneNo': patient.PhoneNo,
                    'firstName': patient.FirstName,
                    'lastName': patient.SurName,
                }

                return JsonResponse(Patients_dict, safe=False)
            else:
                # If no patient_id is provided, return all patients
                patients = list(Patient_Detials.objects.values())

                # Ensure byte fields are properly converted
                for patient in patients:
                    for key, value in patient.items():
                        if isinstance(value, bytes):
                            patient[key] = value.decode()

                return JsonResponse(patients, safe=False)

        except Patient_Detials.DoesNotExist:
            return JsonResponse({'error': 'Patient with the given ID does not exist'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # Ensure a response is always returned
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# @csrf_exempt
# @require_http_methods(["POST", "OPTIONS", "GET"])
# def Patient_OP_Registration(request):


#     @transaction.atomic
#     def generate_or_update_visit_id(patient, register_type):
#         # Get today's date
#         today = datetime.now().date()
        
#         # Find the maximum VisitId for the given patient and date
#         existing_visit = Patient_Visit_Detials.objects.filter(
#             PatientId=patient,
#             created_at__date=today
#         ).first()
        
#         if existing_visit:
#             return existing_visit.VisitId
#         else:
#             max_visit_id = Patient_Visit_Detials.objects.filter(
#                 PatientId=patient
#             ).aggregate(max_id=Max('VisitId'))['max_id']
            
#             next_visit_id = 1 if max_visit_id is None else max_visit_id + 1
            
#             patient_visit = Patient_Visit_Detials.objects.create(
#                 PatientId=patient,
#                 VisitId=next_visit_id,
#                 RegisterType=register_type
#             )
            
#             return patient_visit.VisitId
    
    
    
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             print(data,'data')
            
#             # Extract and validate data
            
#             patient_id = data.get('PatientId','')
#             RegistrationId = data.get('RegistrationId','')
#             register_type = data.get('RegisterType', '') #visit purpose
#             VisitType = data.get('VisitType', '')
#             Speciality = data.get('Speciality', '')
#             DoctorName = data.get('DoctorName', '')
#             TokenNo = data.get('TokenNo', '')
#             Complaint = data.get('Complaint', '')
#             IsMLC = data.get('IsMLC', '')
#             IsReferral = data.get('IsReferral', '')
#             ReferralSource = data.get('ReferralSource', '')
#             ReferredBy = data.get('ReferredBy', '')
#             NextToKinName = data.get('NextToKinName', '')
#             Relation = data.get('Relation', '')
#             RelativePhoneNo = data.get('RelativePhoneNo', '')
         
#             patient_category = data.get('PatientCategory', '')
#             insurance_name = data.get('InsuranceName', '')
#             insurance_type = data.get('InsuranceType', '')
           
#             client_name = data.get('ClientName', '')
#             client_type = data.get('ClientType', '')
#             client_employee_id = data.get('ClientEmployeeId', '')
#             client_employee_designation = data.get('ClientEmployeeDesignation', '')
#             client_employee_relation = data.get('ClientEmployeeRelation', '')
           
#             CorporateName = data.get('CorporateName', '')
#             CorporateType = data.get('CorporateType', '')
#             CorporateEmployeeId = data.get('CorporateEmployeeId', '')
#             CorporateEmployeeDesignation = data.get('CorporateEmployeeDesignation', '')
#             CorporateEmployeeRelation = data.get('CorporateEmployeeRelation', '')
           
#             employee_id = data.get('EmployeeId', '')
#             employee_relation = data.get('EmployeeRelation', '')
           
#             doctor_id = data.get('DoctorId', '')
#             doctor_relation = data.get('DoctorRelation', '')
            
#             donation_type = data.get('DonationType', '')
#             ServiceCategory = data.get('ServiceCategory', '')
#             ServiceSubCategory = data.get('ServiceSubCategory', '')
            
          
#             created_by = data.get('Created_by', '')
            
#             specialization_instance = Speciality_Detials.objects.get(Speciality_Id=Speciality) if Speciality else None
#             doctor_name_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=DoctorName) if DoctorName else None
#             # DrInchargeatTimeofAdmission_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=DrInchargeatTimeofAdmission) if DrInchargeatTimeofAdmission else None
#             referral_doctor_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=ReferredBy) if ReferredBy else None
#             employee_instance = Employee_Personal_Form_Detials.objects.get(Employee_ID=employee_id) if employee_id else None
#             doctor_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=doctor_id) if doctor_id else None
#             # religion_instance = Religion_Detials.objects.get(Religion_Id=religion) if religion else None
#             # location_instance = Location_Detials.objects.get(Location_Id=Location_Id) if Location_Id else None
#             # roomid_instance = Room_Master_Detials.objects.get(Room_Id=RoomId) if RoomId else None
#             # Flagging_instance = Flaggcolor_Detials.objects.get(Flagg_Id=flagging) if flagging else None
#             # BloodGroup_instance = BloodGroup_Detials.objects.get(BloodGroup_Id=blood_group) if blood_group else None
#             # Title_instance = Title_Detials.objects.get(Title_Id=title) if title else None
            

#             Insurance_instance = None
#             if insurance_name:
#               Insurance_instance = Insurance_Master_Detials.objects.get(Insurance_Id=insurance_name) 
             
#             print(Insurance_instance,'Insurance_instanceqqqqqqqqqqqq')
            
#             Client_instance = None
#             if client_name:
#                Client_instance = Client_Master_Detials.objects.get(Client_Id=client_name) 
            
#             Donation_instance = None
#             if donation_type:
#                Donation_instance = Donation_Master_Detials.objects.get(Donation_Id=donation_type) 
            
#             Corporate_instance = None
#             if CorporateName:
#                Corporate_instance = Corporate_Master_Detials.objects.get(Corporate_Id=CorporateName) 
            
#             print(Client_instance,'Client_instanceqqqqqqqqqqq')


#             with transaction.atomic():
#                 patient=None
#                 if patient_id :
#                     patient = Patient_Detials.objects.get(PatientId=patient_id)
#                     if not patient:
#                         return JsonResponse({'warn': f"The Patient Id is not valid"})
                    
#                     patient_visit_id=None
#                     if patient:
#                         patient_visit_id = generate_or_update_visit_id(patient,register_type)
                    
#                     if register_type == 'OP':

                        
#                         OP_Patient =  Patient_Appointment_Registration_Detials.objects.filter(Registration_Id = RegistrationId).first()
                        
#                         if OP_Patient:
#                             OP_Patient.VisitPurpose =  register_type,
#                             # OP_Patient.VisitType = VisitType,
#                             OP_Patient.Specialization = specialization_instance,
#                             OP_Patient.PrimaryDoctor = doctor_name_instance,
#                             OP_Patient.Complaint = Complaint,
#                             OP_Patient.IsMLC = IsMLC,
#                             OP_Patient.IsReferral = IsReferral,
#                             OP_Patient.NextToKinName = NextToKinName,
#                             OP_Patient.Relation = Relation,
#                             OP_Patient.RelativePhNo = RelativePhoneNo,
#                             OP_Patient.PatientCategory = patient_category,
#                             OP_Patient.InsuranceName = Insurance_instance,
#                             OP_Patient.InsuranceType = insurance_type,
#                             OP_Patient.ClientName = Client_instance,
#                             OP_Patient.ClientType = client_type,
#                             OP_Patient.ClientEmployeeId = client_employee_id,
#                             OP_Patient.ClientEmployeeDesignation = client_employee_designation,
#                             OP_Patient.ClientEmployeeRelation = client_employee_relation,
#                             OP_Patient.CorporateName = Corporate_instance,
#                             OP_Patient.CorporateType = CorporateType,
#                             OP_Patient.CorporateEmployeeId = CorporateEmployeeId,
#                             OP_Patient.CorporateEmployeeDesignation = CorporateEmployeeDesignation,
#                             OP_Patient.CorporateEmployeeRelation = CorporateEmployeeRelation,
#                             OP_Patient.EmployeeId = employee_instance,
#                             OP_Patient.EmployeeRelation = employee_relation,
#                             OP_Patient.DoctorId = doctor_instance,
#                             OP_Patient.DoctorRelation = doctor_relation,
#                             OP_Patient.DonationType = Donation_instance,
#                             OP_Patient.ServiceCategory = ServiceCategory,
#                             OP_Patient.ServiceSubCategory = ServiceSubCategory,
#                             OP_Patient.created_by = created_by,
#                             OP_Patient.save()

#                             referral = Patient_Referral_Detials.objects.create(
#                             OP_Register_Id=Patient_OP,
#                             ReferralRegisteredBy=register_type,
#                             ReferralSource=ReferralSource,
#                             ReferredBy=referral_doctor_instance,
#                             )
#                             referral.save()

#                             return JsonResponse({'success': 'OP Patient details updated successfully'})

#                         else:
                            
#                             # patient = Patient_Detials.objects.get(PatientId=patient_id)

#                             if Patient_Appointment_Registration_Detials.objects.filter(PatientId = patient,Status = 'Registered').exists():
#                                 return JsonResponse({'warn': 'Patient is already Registered'})
                            

#                             Patient_OP = Patient_Appointment_Registration_Detials.objects.create(
#                             PatientId = patient,
#                             VisitId = patient_visit_id,  
#                             VisitPurpose = register_type, 
#                             VisitType = VisitType, 
#                             Specialization = specialization_instance, 
#                             PrimaryDoctor = doctor_name_instance, 
#                             TokenNo = TokenNo, 
#                             Complaint = Complaint, 
#                             IsMLC = IsMLC, 
#                             IsReferral = IsReferral, 
#                             # ReferralSource = ReferralSource, 
#                             # ReferredBy = ReferredBy, 
#                             NextToKinName = NextToKinName, 
#                             Relation = Relation, 
#                             RelativePhNo = RelativePhoneNo, 
#                             PatientCategory = patient_category, 
#                             InsuranceName = Insurance_instance,
#                             InsuranceType = insurance_type, 
#                             ClientName = Client_instance, 
#                             ClientType = client_type, 
#                             ClientEmployeeId = client_employee_id, 
#                             ClientEmployeeDesignation = client_employee_designation, 
#                             ClientEmployeeRelation = client_employee_relation, 
                            
#                             CorporateName = Corporate_instance, 
#                             CorporateType = CorporateType, 
#                             CorporateEmployeeId = CorporateEmployeeId, 
#                             CorporateEmployeeDesignation = CorporateEmployeeDesignation, 
#                             CorporateEmployeeRelation = CorporateEmployeeRelation, 

#                             EmployeeId = employee_instance, 
#                             EmployeeRelation = employee_relation, 
#                             DoctorId = doctor_instance, 
#                             DoctorRelation = doctor_relation, 
#                             DonationType = Donation_instance, 
#                             ServiceCategory = ServiceCategory, 
#                             ServiceSubCategory = ServiceSubCategory, 
#                             created_by = created_by,
                           
#                             )
#                             Patient_OP.save()

#                             referral = Patient_Referral_Detials.objects.create(
#                             OP_Register_Id = Patient_OP,
#                             ReferralRegisteredBy = register_type,
#                             ReferralSource = ReferralSource,
#                             ReferredBy = referral_doctor_instance,
                        
#                             )
#                             referral.save()


                           
#                         return JsonResponse({'success': 'Patient Appointment registered successfully'})
                    
#         except Patient_Detials.DoesNotExist:
#             return JsonResponse({'error': 'Patient with the given ID does not exist'})
#         except Doctor_Personal_Form_Detials.DoesNotExist:
#             return JsonResponse({'error': 'Doctor or referred doctor does not exist'})
#         except Exception as e:
#             return JsonResponse({'error': str(e)})

#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=405)



# @csrf_exempt
# @require_http_methods(["POST", "OPTIONS", "GET"])
# def Patient_OP_Registration(request):

#     @transaction.atomic
#     def generate_or_update_visit_id(patient, register_type):
#         today = datetime.now().date()
#         existing_visit = Patient_Visit_Detials.objects.filter(
#             PatientId=patient,
#             created_at__date=today
#         ).first()

#         if existing_visit:
#             print('VisitWorkk')
#             return existing_visit.VisitId
#         else:
#             max_visit_id = Patient_Visit_Detials.objects.filter(
#                 PatientId=patient
#             ).aggregate(max_id=Max('VisitId'))['max_id']

#             next_visit_id = 1 if max_visit_id is None else max_visit_id + 1

#             patient_visit = Patient_Visit_Detials.objects.create(
#                 PatientId=patient,
#                 VisitId=next_visit_id,
#                 RegisterType=register_type
#             )
#             print('VisitWorkk')
#             return patient_visit.VisitId


#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             # Extract and validate data
#             patient_id = data.get('PatientId', '')
#             RegistrationId = data.get('RegistrationId', '')

#             print(RegistrationId,'RegistrationId')
#             register_type = data.get('RegisterType', '')  # visit purpose
#             VisitType = data.get('VisitType', '')
#             Speciality = data.get('Speciality', '')
#             DoctorName = data.get('DoctorName', '')
#             TokenNo = data.get('TokenNo', '')
#             Complaint = data.get('Complaint', '')
#             IsMLC = data.get('IsMLC', '')
#             IsReferral = data.get('IsReferral', '')
#             ReferralSource = data.get('ReferralSource', '')
#             ReferredBy = data.get('ReferredBy', '')
#             NextToKinName = data.get('NextToKinName', '')
#             Relation = data.get('Relation', '')
#             RelativePhoneNo = data.get('RelativePhoneNo', '')
#             patient_category = data.get('PatientCategory', '')
#             insurance_name = data.get('InsuranceName', '')
#             insurance_type = data.get('InsuranceType', '')
#             client_name = data.get('ClientName', '')
#             client_type = data.get('ClientType', '')
#             client_employee_id = data.get('ClientEmployeeId', '')
#             client_employee_designation = data.get('ClientEmployeeDesignation', '')
#             client_employee_relation = data.get('ClientEmployeeRelation', '')
#             CorporateName = data.get('CorporateName', '')
#             CorporateType = data.get('CorporateType', '')
#             CorporateEmployeeId = data.get('CorporateEmployeeId', '')
#             CorporateEmployeeDesignation = data.get('CorporateEmployeeDesignation', '')
#             CorporateEmployeeRelation = data.get('CorporateEmployeeRelation', '')
#             employee_id = data.get('EmployeeId', '')
#             employee_relation = data.get('EmployeeRelation', '')
#             doctor_id = data.get('DoctorId', '')
#             doctor_relation = data.get('DoctorRelation', '')
#             donation_type = data.get('DonationType', '')
#             ServiceCategory = data.get('ServiceCategory', '')
#             ServiceSubCategory = data.get('ServiceSubCategory', '')
#             created_by = data.get('Created_by', '')

#             # Fetch related instances
#             specialization_instance = Speciality_Detials.objects.get(Speciality_Id=Speciality) if Speciality else None
#             doctor_name_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=DoctorName) if DoctorName else None
#             referral_doctor_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=ReferredBy) if ReferredBy else None
#             employee_instance = Employee_Personal_Form_Detials.objects.get(Employee_ID=employee_id) if employee_id else None
#             doctor_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=doctor_id) if doctor_id else None
#             Insurance_instance = Insurance_Master_Detials.objects.get(Insurance_Id=insurance_name) if insurance_name else None
#             Client_instance = Client_Master_Detials.objects.get(Client_Id=client_name) if client_name else None
#             Donation_instance = Donation_Master_Detials.objects.get(Donation_Id=donation_type) if donation_type else None
#             Corporate_instance = Corporate_Master_Detials.objects.get(Corporate_Id=CorporateName) if CorporateName else None

#             # Initialize patient and patient_visit_id
            
           
#             # Check if the registration exists
#             OP_Patient = Patient_Appointment_Registration_Detials.objects.filter(pk=RegistrationId).first()
#             print(f"OP_Patient found: {OP_Patient}")
            
           
#             if OP_Patient:
#                 # Update existing OP patient details
#                 OP_Patient.VisitPurpose = register_type
#                 OP_Patient.Specialization = specialization_instance
#                 OP_Patient.PrimaryDoctor = doctor_name_instance
#                 OP_Patient.Complaint = Complaint
#                 OP_Patient.IsMLC = IsMLC
#                 OP_Patient.TokenNo = TokenNo
#                 OP_Patient.IsReferral = IsReferral
#                 OP_Patient.NextToKinName = NextToKinName
#                 OP_Patient.Relation = Relation
#                 OP_Patient.RelativePhNo = RelativePhoneNo
#                 OP_Patient.PatientCategory = patient_category
#                 OP_Patient.InsuranceName = Insurance_instance
#                 OP_Patient.InsuranceType = insurance_type
#                 OP_Patient.ClientName = Client_instance
#                 OP_Patient.ClientType = client_type
#                 OP_Patient.ClientEmployeeId = client_employee_id
#                 OP_Patient.ClientEmployeeDesignation = client_employee_designation
#                 OP_Patient.ClientEmployeeRelation = client_employee_relation
#                 OP_Patient.CorporateName = Corporate_instance
#                 OP_Patient.CorporateType = CorporateType
#                 OP_Patient.CorporateEmployeeId = CorporateEmployeeId
#                 OP_Patient.CorporateEmployeeDesignation = CorporateEmployeeDesignation
#                 OP_Patient.CorporateEmployeeRelation = CorporateEmployeeRelation
#                 OP_Patient.EmployeeId = employee_instance
#                 OP_Patient.EmployeeRelation = employee_relation
#                 OP_Patient.DoctorId = doctor_instance
#                 OP_Patient.DoctorRelation = doctor_relation
#                 OP_Patient.DonationType = Donation_instance
#                 OP_Patient.ServiceCategory = ServiceCategory
#                 OP_Patient.ServiceSubCategory = ServiceSubCategory
#                 OP_Patient.created_by = created_by
#                 OP_Patient.save()

#                 # Create referral
#                 referral = Patient_Referral_Detials.objects.create(
#                     OP_Register_Id=OP_Patient,
#                     ReferralRegisteredBy=register_type,
#                     ReferralSource=ReferralSource,
#                     ReferredBy=referral_doctor_instance,
#                 )
#                 referral.save()

#                 return JsonResponse({'success': 'OP Patient details updated successfully'})

#             else:

#                 patient = None
#                 patient_visit_id = None

                
#                 if patient_id:
#                     patient = Patient_Detials.objects.get(PatientId=patient_id)
#                     if not patient:
#                         return JsonResponse({'warn': f"The Patient Id is not valid"})

#                     # Generate or update visit ID
#                     patient_visit_id = generate_or_update_visit_id(patient, register_type)

#                 # Check if the patient is already registered
#                 if Patient_Appointment_Registration_Detials.objects.filter(PatientId=patient, Status='Registered').exists():
#                     return JsonResponse({'warn': 'Patient is already Registered'})

#                 if register_type == 'OP':
#                     # Create new OP patient appointment
#                     Patient_OP = Patient_Appointment_Registration_Detials.objects.create(
#                         PatientId=patient,
#                         VisitId=patient_visit_id,
#                         VisitPurpose=register_type,
#                         VisitType=VisitType,
#                         Specialization=specialization_instance,
#                         PrimaryDoctor=doctor_name_instance,
#                         TokenNo=TokenNo,
#                         Complaint=Complaint,
#                         IsMLC=IsMLC,
#                         IsReferral=IsReferral,
#                         NextToKinName=NextToKinName,
#                         Relation=Relation,
#                         RelativePhNo=RelativePhoneNo,
#                         PatientCategory=patient_category,
#                         InsuranceName=Insurance_instance,
#                         InsuranceType=insurance_type,
#                         ClientName=Client_instance,
#                         ClientType=client_type,
#                         ClientEmployeeId=client_employee_id,
#                         ClientEmployeeDesignation=client_employee_designation,
#                         ClientEmployeeRelation=client_employee_relation,
#                         CorporateName=Corporate_instance,
#                         CorporateType=CorporateType,
#                         CorporateEmployeeId=CorporateEmployeeId,
#                         CorporateEmployeeDesignation=CorporateEmployeeDesignation,
#                         CorporateEmployeeRelation=CorporateEmployeeRelation,
#                         EmployeeId=employee_instance,
#                         EmployeeRelation=employee_relation,
#                         DoctorId=doctor_instance,
#                         DoctorRelation=doctor_relation,
#                         DonationType=Donation_instance,
#                         ServiceCategory=ServiceCategory,
#                         ServiceSubCategory=ServiceSubCategory,
#                         created_by=created_by,
#                     )
#                     Patient_OP.save()

#                     # Create referral
#                     referral = Patient_Referral_Detials.objects.create(
#                         OP_Register_Id=Patient_OP,
#                         ReferralRegisteredBy=register_type,
#                         ReferralSource=ReferralSource,
#                         ReferredBy=referral_doctor_instance,
#                     )
#                     referral.save()

#                     return JsonResponse({'success': 'Patient Appointment registered successfully'})

#         except Patient_Detials.DoesNotExist:
#             return JsonResponse({'error': 'Patient with the given ID does not exist'})
#         except Doctor_Personal_Form_Detials.DoesNotExist:
#             return JsonResponse({'error': 'Doctor or referred doctor does not exist'})
#         except Exception as e:
#             return JsonResponse({'error': str(e)})

#     return JsonResponse({'error': 'Invalid request method'}, status=405)


#=======31-12-2024======================

# @csrf_exempt
# @require_http_methods(["POST", "OPTIONS", "GET"])
# def Patient_OP_Registration(request):


#     @transaction.atomic
#     def generate_or_update_visit_id(patient, register_type):
#         # Get today's date
#         today = datetime.now().date()
        
#         # Find the maximum VisitId for the given patient and date
#         existing_visit = Patient_Visit_Detials.objects.filter(
#             PatientId=patient,
#             created_at__date=today
#         ).first()
        
#         if existing_visit:
#             return existing_visit.VisitId
#         else:
#             max_visit_id = Patient_Visit_Detials.objects.filter(
#                 PatientId=patient
#             ).aggregate(max_id=Max('VisitId'))['max_id']
            
#             next_visit_id = 1 if max_visit_id is None else max_visit_id + 1
            
#             patient_visit = Patient_Visit_Detials.objects.create(
#                 PatientId=patient,
#                 VisitId=next_visit_id,
#                 RegisterType=register_type
#             )
            
#             return patient_visit.VisitId
    
    
    
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             # print(data,'data')
            
#             # Extract and validate data
            
#             patient_id = data.get('PatientId','')
#             print(patient_id,'patient_id')

#             RegistrationId = data.get('RegistrationId', '')
#             print(RegistrationId,'RegistrationId1111111111')
#             register_type = data.get('RegisterType', '') #visit purpose
#             VisitType = data.get('VisitType', '')
#             Speciality = data.get('Speciality', '')
#             DoctorName = data.get('DoctorName', '')
#             TokenNo = data.get('TokenNo', '')
#             Complaint = data.get('Complaint', '')
#             IsMLC = data.get('IsMLC', '')
#             IsReferral = data.get('IsReferral', '')
#             ReferralSource = data.get('ReferralSource', '')
#             ReferredBy = data.get('ReferredBy', '')
#             NextToKinName = data.get('NextToKinName', '')
#             Relation = data.get('Relation', '')
#             RelativePhoneNo = data.get('RelativePhoneNo', '')
         
#             patient_category = data.get('PatientCategory', '')
#             insurance_name = data.get('InsuranceName', '')
#             insurance_type = data.get('InsuranceType', '')
           
#             client_name = data.get('ClientName', '')
#             client_type = data.get('ClientType', '')
#             client_employee_id = data.get('ClientEmployeeId', '')
#             client_employee_designation = data.get('ClientEmployeeDesignation', '')
#             client_employee_relation = data.get('ClientEmployeeRelation', '')
           
#             CorporateName = data.get('CorporateName', '')
#             CorporateType = data.get('CorporateType', '')
#             CorporateEmployeeId = data.get('CorporateEmployeeId', '')
#             CorporateEmployeeDesignation = data.get('CorporateEmployeeDesignation', '')
#             CorporateEmployeeRelation = data.get('CorporateEmployeeRelation', '')
           
#             employee_id = data.get('EmployeeId', '')
#             employee_relation = data.get('EmployeeRelation', '')
           
#             doctor_id = data.get('DoctorId', '')
#             doctor_relation = data.get('DoctorRelation', '')
            
#             donation_type = data.get('DonationType', '')
#             ServiceCategory = data.get('ServiceCategory', '')
#             ServiceSubCategory = data.get('ServiceSubCategory', '')
            
          
#             created_by = data.get('Created_by', '')
            
#             specialization_instance = Speciality_Detials.objects.get(Speciality_Id=Speciality) if Speciality else None
#             doctor_name_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=DoctorName) if DoctorName else None
#             referral_doctor_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=ReferredBy) if ReferredBy else None
#             employee_instance = Employee_Personal_Form_Detials.objects.get(Employee_ID=employee_id) if employee_id else None
#             doctor_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=doctor_id) if doctor_id else None
#             Insurance_instance = Insurance_Master_Detials.objects.get(Insurance_Id=insurance_name) if insurance_name else None
#             Client_instance = Client_Master_Detials.objects.get(Client_Id=client_name) if client_name else None
#             Donation_instance = Donation_Master_Detials.objects.get(Donation_Id=donation_type) if donation_type else None
#             Corporate_instance = Corporate_Master_Detials.objects.get(Corporate_Id=CorporateName) if CorporateName else None
            
#             # Insurance_instance = None
#             # if insurance_name:
#             #   Insurance_instance = Insurance_Master_Detials.objects.get(Insurance_Id=insurance_name) 
             
#             # print(Insurance_instance,'Insurance_instanceqqqqqqqqqqqq')
            
#             # Client_instance = None
#             # if client_name:
#             #    Client_instance = Client_Master_Detials.objects.get(Client_Id=client_name) 
            
#             # Donation_instance = None
#             # if donation_type:
#             #    Donation_instance = Donation_Master_Detials.objects.get(Donation_Id=donation_type) 
            
#             # Corporate_instance = None
#             # if CorporateName:
#             #    Corporate_instance = Corporate_Master_Detials.objects.get(Corporate_Id=CorporateName) 
            
#             # patient = Patient_Detials.objects.get(PatientId=patient_id)
#             # print("patient",patient)
#             print("RegistrationId",RegistrationId)
#             if RegistrationId :
#                 OP_Patient = Patient_Appointment_Registration_Detials.objects.get(pk=RegistrationId)
#                 print("OP_Patient",OP_Patient)
                
#                 print("hello")
#                 # OP_Patient.PatientId = patient
#                 OP_Patient.VisitPurpose = register_type
#                 OP_Patient.Specialization = specialization_instance
#                 OP_Patient.PrimaryDoctor = doctor_name_instance
#                 OP_Patient.Complaint = Complaint
#                 OP_Patient.IsMLC = IsMLC
#                 OP_Patient.TokenNo = TokenNo
#                 OP_Patient.IsReferral = IsReferral
#                 OP_Patient.NextToKinName = NextToKinName
#                 OP_Patient.Relation = Relation
#                 OP_Patient.RelativePhNo = RelativePhoneNo
#                 OP_Patient.PatientCategory = patient_category
#                 OP_Patient.InsuranceName = Insurance_instance
#                 OP_Patient.InsuranceType = insurance_type
#                 OP_Patient.ClientName = Client_instance
#                 OP_Patient.ClientType = client_type
#                 OP_Patient.ClientEmployeeId = client_employee_id
#                 OP_Patient.ClientEmployeeDesignation = client_employee_designation
#                 OP_Patient.ClientEmployeeRelation = client_employee_relation
#                 OP_Patient.CorporateName = Corporate_instance
#                 OP_Patient.CorporateType = CorporateType
#                 OP_Patient.CorporateEmployeeId = CorporateEmployeeId
#                 OP_Patient.CorporateEmployeeDesignation = CorporateEmployeeDesignation
#                 OP_Patient.CorporateEmployeeRelation = CorporateEmployeeRelation
#                 OP_Patient.EmployeeId = employee_instance
#                 OP_Patient.EmployeeRelation = employee_relation
#                 OP_Patient.DoctorId = doctor_instance
#                 OP_Patient.DoctorRelation = doctor_relation
#                 OP_Patient.DonationType = Donation_instance
#                 OP_Patient.ServiceCategory = ServiceCategory
#                 OP_Patient.ServiceSubCategory = ServiceSubCategory
#                 OP_Patient.created_by = created_by
#                 OP_Patient.save()

                
#                 referral = Patient_Referral_Detials.objects.filter(OP_Register_Id__pk = RegistrationId).first()
#                 referral.OP_Register_Id=OP_Patient
#                 referral.ReferralRegisteredBy=register_type
#                 referral.ReferralSource=ReferralSource
#                 referral.ReferredBy=referral_doctor_instance
#                 referral.save()

#                 return JsonResponse({'success': 'OP Patient Details Updated Successfully'})


#             else:
#                 print("hhhhhhh")
#                 patient = None
#                 patient_visit_id = None
#                 print(patient_id,'patient_iddddddddddddddd')

                
                
#                 patient = Patient_Detials.objects.get(pk=patient_id)
#                 print(patient,'patienttttttttttttt')
                    
#                 if not patient:
#                     return JsonResponse({'warn': f"The Patient Id is not valid"})

#                     # Generate or update visit ID
#                 patient_visit_id = generate_or_update_visit_id(patient, register_type)

#                 # Check if the patient is already registered
#                 if Patient_Appointment_Registration_Detials.objects.filter(PatientId=patient, Status='Registered').exists():
#                     return JsonResponse({'warn': 'Patient is already Registered'})
                
#                 print(specialization_instance,'specialization_instance')
#                 print(doctor_name_instance,'doctor_name_instance')
                
#                 Patient_OP = Patient_Appointment_Registration_Detials.objects.create(
#                 PatientId = patient,
#                 VisitId = patient_visit_id,  
#                 VisitPurpose = register_type, 
#                 VisitType = VisitType, 
#                 Specialization = specialization_instance, 
#                 PrimaryDoctor = doctor_name_instance, 
#                 TokenNo = TokenNo, 
#                 Complaint = Complaint, 
#                 IsMLC = IsMLC, 
#                 IsReferral = IsReferral, 
#                 NextToKinName = NextToKinName, 
#                 Relation = Relation, 
#                 RelativePhNo = RelativePhoneNo, 
#                 PatientCategory = patient_category, 
#                 InsuranceName = Insurance_instance,
#                 InsuranceType = insurance_type, 
#                 ClientName = Client_instance, 
#                 ClientType = client_type, 
#                 ClientEmployeeId = client_employee_id, 
#                 ClientEmployeeDesignation = client_employee_designation, 
#                 ClientEmployeeRelation = client_employee_relation, 
                
#                 CorporateName = Corporate_instance, 
#                 CorporateType = CorporateType, 
#                 CorporateEmployeeId = CorporateEmployeeId, 
#                 CorporateEmployeeDesignation = CorporateEmployeeDesignation, 
#                 CorporateEmployeeRelation = CorporateEmployeeRelation, 

#                 EmployeeId = employee_instance, 
#                 EmployeeRelation = employee_relation, 
#                 DoctorId = doctor_instance, 
#                 DoctorRelation = doctor_relation, 
#                 DonationType = Donation_instance, 
#                 ServiceCategory = ServiceCategory, 
#                 ServiceSubCategory = ServiceSubCategory, 
#                 created_by = created_by,
                
#                 )
#                 Patient_OP.save()

#                 patient_details = Patient_Detials.objects.get(pk=patient_id)
#                 patient_details.Status = 'Registered'
#                 patient_details.save()


#                 referral = Patient_Referral_Detials.objects.create(
#                 OP_Register_Id = Patient_OP,
#                 ReferralRegisteredBy = register_type,
#                 ReferralSource = ReferralSource,
#                 ReferredBy = referral_doctor_instance,
            
#                 )
#                 referral.save()


                
#             return JsonResponse({'success': 'Patient Appointment registered successfully'})
                
        
#         except Exception as e:
#             return JsonResponse({'error': str(e)})

#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=405)




@csrf_exempt
@require_http_methods(["POST", "OPTIONS", "GET"])
def Patient_OP_Registration(request):


    @transaction.atomic
    def generate_or_update_visit_id(patient, register_type):
        # Get today's date
        today = datetime.now().date()
        
        # Find the maximum VisitId for the given patient and date
        existing_visit = Patient_Visit_Detials.objects.filter(
            PatientId=patient,
            created_at__date=today
        ).first()
        
        if existing_visit:
            return existing_visit.VisitId
        else:
            max_visit_id = Patient_Visit_Detials.objects.filter(
                PatientId=patient
            ).aggregate(max_id=Max('VisitId'))['max_id']
            
            next_visit_id = 1 if max_visit_id is None else max_visit_id + 1
            
            patient_visit = Patient_Visit_Detials.objects.create(
                PatientId=patient,
                VisitId=next_visit_id,
                RegisterType=register_type
            )
            
            return patient_visit.VisitId
    
    
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # print(data,'data')
            
            # Extract and validate data
            
            patient_id = data.get('PatientId','')
            print(patient_id,'patient_id')

            RegistrationId = data.get('RegistrationId', '')
            print(RegistrationId,'RegistrationId1111111111')
            register_type = data.get('RegisterType', '') #visit purpose

            print(register_type,'register_type')
            VisitType = data.get('VisitType', '')

            Speciality = data.get('Speciality', '')
            DoctorName = data.get('DoctorName', '')
            TokenNo = data.get('TokenNo', '')
            Complaint = data.get('Complaint', '')
            IsMLC = data.get('IsMLC', '')
            IsReferral = data.get('IsReferral', '')
            ReferralSource = data.get('ReferralSource', '')
            ReferredBy = data.get('ReferredBy', '')
            NextToKinName = data.get('NextToKinName', '')
            Relation = data.get('Relation', '')
            RelativePhoneNo = data.get('RelativePhoneNo', '')
         
            patient_category = data.get('PatientCategory', '')
            insurance_name = data.get('InsuranceName', '')
            insurance_type = data.get('InsuranceType', '')
           
            client_name = data.get('ClientName', '')
            client_type = data.get('ClientType', '')
            client_employee_id = data.get('ClientEmployeeId', '')
            client_employee_designation = data.get('ClientEmployeeDesignation', '')
            client_employee_relation = data.get('ClientEmployeeRelation', '')
           
            CorporateName = data.get('CorporateName', '')
            CorporateType = data.get('CorporateType', '')
            CorporateEmployeeId = data.get('CorporateEmployeeId', '')
            CorporateEmployeeDesignation = data.get('CorporateEmployeeDesignation', '')
            CorporateEmployeeRelation = data.get('CorporateEmployeeRelation', '')
           
            employee_id = data.get('EmployeeId', '')
            employee_relation = data.get('EmployeeRelation', '')
           
            doctor_id = data.get('DoctorId', '')
            doctor_relation = data.get('DoctorRelation', '')
            
            donation_type = data.get('DonationType', '')
            ServiceCategory = data.get('ServiceCategory', '')
            ServiceSubCategory = data.get('ServiceSubCategory', '')
            
          
            created_by = data.get('Created_by', '')

            Testname_arr = data.get('SubtestNoArr', [])

            print(Testname_arr,'Testname_arr')
            
            specialization_instance = Speciality_Detials.objects.get(Speciality_Id=Speciality) if Speciality else None
            doctor_name_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=DoctorName) if DoctorName else None
            referral_doctor_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=ReferredBy) if ReferredBy else None
            employee_instance = Employee_Personal_Form_Detials.objects.get(Employee_ID=employee_id) if employee_id else None
            doctor_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=doctor_id) if doctor_id else None
            Insurance_instance = Insurance_Master_Detials.objects.get(Insurance_Id=insurance_name) if insurance_name else None
            Client_instance = Client_Master_Detials.objects.get(Client_Id=client_name) if client_name else None
            Donation_instance = Donation_Master_Detials.objects.get(Donation_Id=donation_type) if donation_type else None
            Corporate_instance = Corporate_Master_Detials.objects.get(Corporate_Id=CorporateName) if CorporateName else None
            
            # Insurance_instance = None
            # if insurance_name:
            #   Insurance_instance = Insurance_Master_Detials.objects.get(Insurance_Id=insurance_name) 
             
            # print(Insurance_instance,'Insurance_instanceqqqqqqqqqqqq')
            
            # Client_instance = None
            # if client_name:
            #    Client_instance = Client_Master_Detials.objects.get(Client_Id=client_name) 
            
            # Donation_instance = None
            # if donation_type:
            #    Donation_instance = Donation_Master_Detials.objects.get(Donation_Id=donation_type) 
            
            # Corporate_instance = None
            # if CorporateName:
            #    Corporate_instance = Corporate_Master_Detials.objects.get(Corporate_Id=CorporateName) 
            
            # patient = Patient_Detials.objects.get(PatientId=patient_id)
            # print("patient",patient)
            print("RegistrationId",RegistrationId)
            if RegistrationId :
                OP_Patient = Patient_Appointment_Registration_Detials.objects.get(pk=RegistrationId)
                print("OP_Patient",OP_Patient)
                
                print("hello")
                # OP_Patient.PatientId = patient
                OP_Patient.VisitPurpose = register_type
                OP_Patient.Specialization = specialization_instance
                OP_Patient.PrimaryDoctor = doctor_name_instance
                OP_Patient.Complaint = Complaint
                OP_Patient.IsMLC = IsMLC
                OP_Patient.TokenNo = TokenNo
                OP_Patient.IsReferral = IsReferral
                OP_Patient.NextToKinName = NextToKinName
                OP_Patient.Relation = Relation
                OP_Patient.RelativePhNo = RelativePhoneNo
                OP_Patient.PatientCategory = patient_category
                OP_Patient.InsuranceName = Insurance_instance
                OP_Patient.InsuranceType = insurance_type
                OP_Patient.ClientName = Client_instance
                OP_Patient.ClientType = client_type
                OP_Patient.ClientEmployeeId = client_employee_id
                OP_Patient.ClientEmployeeDesignation = client_employee_designation
                OP_Patient.ClientEmployeeRelation = client_employee_relation
                OP_Patient.CorporateName = Corporate_instance
                OP_Patient.CorporateType = CorporateType
                OP_Patient.CorporateEmployeeId = CorporateEmployeeId
                OP_Patient.CorporateEmployeeDesignation = CorporateEmployeeDesignation
                OP_Patient.CorporateEmployeeRelation = CorporateEmployeeRelation
                OP_Patient.EmployeeId = employee_instance
                OP_Patient.EmployeeRelation = employee_relation
                OP_Patient.DoctorId = doctor_instance
                OP_Patient.DoctorRelation = doctor_relation
                OP_Patient.DonationType = Donation_instance
                OP_Patient.ServiceCategory = ServiceCategory
                OP_Patient.ServiceSubCategory = ServiceSubCategory
                OP_Patient.created_by = created_by
                OP_Patient.save()

                
                referral = Patient_Referral_Detials.objects.filter(OP_Register_Id__pk = RegistrationId).first()
                referral.OP_Register_Id=OP_Patient
                referral.ReferralRegisteredBy=register_type
                referral.ReferralSource=ReferralSource
                referral.ReferredBy=referral_doctor_instance
                referral.save()

                return JsonResponse({'success': 'OP Patient Details Updated Successfully'})


            else:
                print("hhhhhhh")
                patient = None
                patient_visit_id = None
                print(patient_id,'patient_iddddddddddddddd')

                
                
                patient = Patient_Detials.objects.get(pk=patient_id)
                print(patient,'patienttttttttttttt')
                    
                if not patient:
                    return JsonResponse({'warn': f"The Patient Id is not valid"})

                    # Generate or update visit ID
                patient_visit_id = generate_or_update_visit_id(patient, register_type)

                # Check if the patient is already registered
                if Patient_Appointment_Registration_Detials.objects.filter(PatientId=patient, Status='Registered').exists():
                    return JsonResponse({'warn': 'Patient is already Registered'})
                
                print(specialization_instance,'specialization_instance')
                print(doctor_name_instance,'doctor_name_instance')
                
                Patient_OP = Patient_Appointment_Registration_Detials.objects.create(
                PatientId = patient,
                VisitId = patient_visit_id,  
                VisitPurpose = register_type, 
                VisitType = VisitType, 
                Specialization = specialization_instance, 
                PrimaryDoctor = doctor_name_instance, 
                TokenNo = TokenNo, 
                Complaint = Complaint, 
                IsMLC = IsMLC, 
                IsReferral = IsReferral, 
                NextToKinName = NextToKinName, 
                Relation = Relation, 
                RelativePhNo = RelativePhoneNo, 
                PatientCategory = patient_category, 
                InsuranceName = Insurance_instance,
                InsuranceType = insurance_type, 
                ClientName = Client_instance, 
                ClientType = client_type, 
                ClientEmployeeId = client_employee_id, 
                ClientEmployeeDesignation = client_employee_designation, 
                ClientEmployeeRelation = client_employee_relation, 
                
                CorporateName = Corporate_instance, 
                CorporateType = CorporateType, 
                CorporateEmployeeId = CorporateEmployeeId, 
                CorporateEmployeeDesignation = CorporateEmployeeDesignation, 
                CorporateEmployeeRelation = CorporateEmployeeRelation, 

                EmployeeId = employee_instance, 
                EmployeeRelation = employee_relation, 
                DoctorId = doctor_instance, 
                DoctorRelation = doctor_relation, 
                DonationType = Donation_instance, 
                ServiceCategory = ServiceCategory, 
                ServiceSubCategory = ServiceSubCategory, 
                created_by = created_by,
                
                )
                Patient_OP.save()

                patient_details = Patient_Detials.objects.get(pk=patient_id)
                patient_details.Status = 'Registered'
                patient_details.save()


                referral = Patient_Referral_Detials.objects.create(
                OP_Register_Id = Patient_OP,
                ReferralRegisteredBy = register_type,
                ReferralSource = ReferralSource,
                ReferredBy = referral_doctor_instance,
            
                )
                referral.save()

                registration_id = Patient_OP.pk
                rad_ins = Patient_Appointment_Registration_Detials.objects.get(pk=registration_id)

                print(registration_id,'registration_id')

                if register_type == 'RADIOLOGY' or register_type == 'OP':


                    print("RADIOLOGY RADIOLOGY")

                    for testname in Testname_arr:
                        Radiologyid = testname.get('Radiologyid', None)
                        TestCode = testname.get('TestCode', None)

                        print(Radiologyid,'Radiologyid')
                        print(TestCode,'TestCode')

                        
                        if Radiologyid and TestCode:  # Ensure required fields are present
                            Radiology_Request_Details.objects.create(
                                RegisterType = register_type,
                                OP_Register_Id= rad_ins ,
                                IP_Register_Id=  None,
                                Casuality_Register_Id= None,
                                Diagnosis_Register_Id=  None,
                                TestCode=Radiologyid,
                                SubTestCode=TestCode,
                                created_by=created_by
                            )

                    
            return JsonResponse({'success': 'Patient Appointment registered successfully'})
                
        
        except Exception as e:
            return JsonResponse({'error': str(e)})

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
@require_http_methods(["GET"])
def get_OP_patient_details(request):
    try:
       
        RegistrationId = request.GET.get('RegistrationId')
        
        print(RegistrationId,'RegistrationId')
        # Start with all records
        queryset = Patient_Appointment_Registration_Detials.objects.get(pk = RegistrationId)
        
        referral_details = None

        # Check for referral details by OP, IP, and Emergency Register IDs
        try:
            referral_details = Patient_Referral_Detials.objects.filter(
                OP_Register_Id=RegistrationId
            ).first() or Patient_Referral_Detials.objects.filter(
                IP_Register_Id=RegistrationId
            ).first() or Patient_Referral_Detials.objects.filter(
                Emergency_Register_Id=RegistrationId
            ).first()
        except Patient_Referral_Detials.DoesNotExist:
            referral_details = None
        print(queryset,'queryset')
        # Serialize the filtered queryset
        
           
            # Flagging_name = register.Flagging.Flagg_Name if register.Flagging else None
            # Flagging_color = register.Flagging.Flagg_Color if register.Flagging else None
            
        appointment_dict = {
            
            'PatientProfile': get_file_image(queryset.PatientId.Patient_profile) if queryset.PatientId.Patient_profile else None,
            'PatientId': queryset.PatientId.PatientId,
            'PatientName': f"{queryset.PatientId.Title.Title_Name}.{queryset.PatientId.FirstName} {queryset.PatientId.MiddleName} {queryset.PatientId.SurName}",
            'Title': queryset.PatientId.Title.pk,
            'FirstName': queryset.PatientId.FirstName,
            'MiddleName': queryset.PatientId.MiddleName,
            'SurName': queryset.PatientId.SurName,
            'PhoneNo': queryset.PatientId.PhoneNo,
            'Age': queryset.PatientId.Age,
            'Gender': queryset.PatientId.Gender,
            'MaritalStatus': queryset.PatientId.MaritalStatus,
            'SpouseName': queryset.PatientId.SpouseName,
            'FatherName': queryset.PatientId.FatherName,
            'DOB': queryset.PatientId.DOB,
            'Email': queryset.PatientId.Email,
            'BloodGroup': queryset.PatientId.BloodGroup.BloodGroup_Id if queryset.PatientId.BloodGroup else None,
            'Occupation': queryset.PatientId.Occupation,
            'Religion': queryset.PatientId.Religion.Religion_Id if queryset.PatientId.Religion else None,
            'Nationality': queryset.PatientId.Nationality,
            'UHIDType': queryset.PatientId.UniqueIdType,
            'UHIDNo': queryset.PatientId.UniqueIdNo,
            'DoorNo': queryset.PatientId.DoorNo,
            'Street': queryset.PatientId.Street,
            'Area': queryset.PatientId.Area,
            'City': queryset.PatientId.City,
            'District': queryset.PatientId.District,
            'State': queryset.PatientId.State,
            'Country': queryset.PatientId.Country,
            'Pincode': queryset.PatientId.Pincode,
            'PatientType': queryset.PatientId.PatientType,
            'ABHA': queryset.PatientId.ABHA,
            'AppointmentId': queryset.AppointmentId,
            'VisitId': queryset.VisitId,
            # 'Complaint': queryset.Complaint,
            'IsMLC': queryset.IsMLC,
            'VisitType': queryset.VisitType,
            'Complaint': queryset.Complaint,
            'NextToKinName': queryset.NextToKinName,
            # 'Flagging': Flagging_name,
            # 'FlaggingColour': Flagging_color,
            'IsReferral': queryset.IsReferral,
            'Relation': queryset.Relation,
            'RelativePhNo': queryset.RelativePhNo,
            'PatientCategory': queryset.PatientCategory,
            'InsuranceName': queryset.InsuranceName.pk if queryset.InsuranceName else None,
            'InsuranceType': queryset.InsuranceType,
            'ClientName': queryset.ClientName.pk if queryset.ClientName else None,
            'ClientType': queryset.ClientType,
            'ClientEmployeeId': queryset.ClientEmployeeId,
            'ClientEmployeeDesignation': queryset.ClientEmployeeDesignation,
            'ClientEmployeeRelation': queryset.ClientEmployeeRelation,
           
            'CorporateName': queryset.CorporateName.Corporate_Id if queryset.CorporateName else None,
            'CorporateType': queryset.CorporateType,
            'CorporateEmployeeId': queryset.CorporateEmployeeId,
            'CorporateEmployeeDesignation': queryset.CorporateEmployeeDesignation,
            'CorporateEmployeeRelation': queryset.CorporateEmployeeRelation,
        
            'EmployeeId': queryset.EmployeeId.pk if queryset.EmployeeId else None,
            'EmployeeRelation': queryset.EmployeeRelation,
            'DoctorId': queryset.DoctorId.pk if queryset.DoctorId else None,
            'DoctorRelation': queryset.DoctorRelation,
            'DonationType': queryset.DonationType.Donation_Id if queryset.DonationType else None,
            'ServiceCategory': queryset.ServiceCategory,
            'ServiceSubCategory': queryset.ServiceSubCategory,
            'TokenNo': queryset.TokenNo,
            'Status': queryset.Status,
            'RegistrationId': queryset.pk,
            'PrimaryDoctor': queryset.PrimaryDoctor.pk if queryset.PrimaryDoctor else None,
            # 'PrimaryDoctor': f"{queryset.PrimaryDoctor.Tittle.Title_Name}.{queryset.PrimaryDoctor.First_Name} {queryset.PrimaryDoctor.Last_Name}",

            'SpecilizationId': queryset.Specialization.Speciality_Id if queryset.Specialization else None,
            'DoctorName': f"{queryset.PrimaryDoctor.Tittle.Title_Name}.{queryset.PrimaryDoctor.First_Name} {queryset.PrimaryDoctor.Last_Name}" if queryset.PrimaryDoctor else None,
            'Speciality': queryset.Specialization.pk if queryset.Specialization else None,
        }

        if referral_details:
            appointment_dict.update({
                'ReferralSource': referral_details.ReferralSource,
                'ReferredBy': f"{referral_details.ReferredBy.Tittle.Title_Name}.{referral_details.ReferredBy.First_Name} {referral_details.ReferredBy.Last_Name}" if referral_details.ReferredBy else None,
            })

    
    
        print(appointment_dict,'appointment_register_data')
        return JsonResponse(appointment_dict, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)})




@csrf_exempt
@require_http_methods(["GET"])
def get_patient_appointment_details_withoutcancelled(request):
    try:
        # Get query parameters
        query = request.GET.get('query', '')
        status = request.GET.get('status', '')
        doctor_id = request.GET.get('DoctorId', '')
        from_date = request.GET.get('fromDate', '')  
        to_date = request.GET.get('toDate', '')  
        particular_date = request.GET.get('ParticularDate', '')
        Current_date = request.GET.get('CurrentDate', '')


        # Start with all records
        queryset = Patient_Appointment_Registration_Detials.objects.all()
        
        print(queryset,'queryset')
        # Apply filters based on the query parameters
        if query:
            queryset = queryset.filter(
                Q(PatientId__FirstName__icontains=query) |
                Q(PatientId__MiddleName__icontains=query) |
                Q(PatientId__SurName__icontains=query) |
                Q(PatientId__PatientId__icontains=query) |
                Q(PatientId__PhoneNo__icontains=query)
            )
        if from_date and to_date:
            queryset = queryset.filter(created_at__date__range=[from_date, to_date])

        # Particular date filter
        elif particular_date:
            queryset = queryset.filter(created_at__date=particular_date)
        
        # Current Date filter (Ensure it's a valid date)
        elif Current_date and Current_date != "":  
            queryset = queryset.filter(created_at__date=Current_date)

        # Filter by DoctorId
        if not doctor_id:
             pass
        else:
            queryset = queryset.filter(PrimaryDoctor__pk=doctor_id)
            print(queryset,'patientqueryset1111111111111111s') 
            print(doctor_id,'queryset222222222222')
        # Filter by status if specified
        if status:
            queryset = queryset.filter(Q(Status__icontains=status))
        else:
            # Exclude 'Cancelled' status if no status is specified
            queryset = queryset.exclude(Status='Cancelled')
        
        
        # Serialize the filtered queryset
        appointment_register_data = []
        for idx, register in enumerate(queryset, start=1):
           
            # Flagging_name = register.Flagging.Flagg_Name if register.Flagging else None
            # Flagging_color = register.Flagging.Flagg_Color if register.Flagging else None
            
            appointment_dict = {
                'id': idx,
                'PatientProfile': get_file_image(register.PatientId.Patient_profile) if register.PatientId.Patient_profile else None,
                'PatientId': register.PatientId.PatientId,
                'PatientName': f"{register.PatientId.Title.Title_Name}.{register.PatientId.FirstName} {register.PatientId.MiddleName} {register.PatientId.SurName}",
                'PhoneNo': register.PatientId.PhoneNo,
                'Age': register.PatientId.Age,
                'Gender': register.PatientId.Gender,
                'AppointmentId': register.AppointmentId,
                'VisitId': register.VisitId,
                'Complaint': register.Complaint,
                'isMLC': register.IsMLC,
                'VisitType': register.VisitType,
                'Complaint': register.Complaint,
                # 'Flagging': Flagging_name,
                # 'FlaggingColour': Flagging_color,
                'isRefferal': register.IsReferral,
                'Status': register.Status,
                'RegistrationId': register.pk,
                'DoctorId': register.PrimaryDoctor.pk if register.PrimaryDoctor else None,
                'SpecilizationId': register.Specialization.Speciality_Id if register.Specialization else None,
                'DoctorName': (
                    f"{register.PrimaryDoctor.Tittle.Title_Name if register.PrimaryDoctor and register.PrimaryDoctor.Tittle else None}."
                    f"{register.PrimaryDoctor.First_Name if register.PrimaryDoctor else None} "
                    f"{register.PrimaryDoctor.Last_Name if register.PrimaryDoctor else None}"
                ),

                # 'DoctorName': f"{register.PrimaryDoctor.Tittle.Title_Name if register.PrimaryDoctor.Tittle else None}.{register.PrimaryDoctor.First_Name if register.PrimaryDoctor else None} {register.PrimaryDoctor.Last_Name if register.PrimaryDoctor else None}",
                'Specilization': str(register.Specialization.Speciality_Name) if register.Specialization else '',
            }
            appointment_register_data.append(appointment_dict)
        print(appointment_register_data,'appointment_register_data')
        return JsonResponse(appointment_register_data, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)})



@csrf_exempt
@require_http_methods(['POST','GET'])
def IP_Patient_Registration_Details_Link(request):
   
    @transaction.atomic
    def create_or_update_referral(is_referral, referral_source, referral_doctor_instance, register_type, register_id, newdata, created_by):
        if is_referral == 'Yes':
            try:
               
                if register_id:
                    filters = {
                        'IP': 'IP_Register_Id__pk',
                    }
                    filter_key = filters.get(register_type)
                    if not filter_key:
                        raise ValueError("Invalid register_type provided.")
                    if Patient_Referral_Detials.objects.filter(**{filter_key: register_id}).exists():
                        referral = Patient_Referral_Detials.objects.get(**{filter_key: register_id})
                        referral.ReferralSource = referral_source
                        referral.ReferredBy = referral_doctor_instance
                        referral.save()
                    else:
                        Patient_Referral_Detials.objects.create(
                            **{
                                'IP_Register_Id': newdata if register_type == 'IP' else None,
                            },
                            ReferralRegisteredBy=register_type,
                            ReferralSource=referral_source,
                            ReferredBy=referral_doctor_instance,
                            created_by=created_by
                        )
                   
                else:
                    Patient_Referral_Detials.objects.create(
                        **{
                            'IP_Register_Id': newdata if register_type == 'IP' else None,
                        },
                        ReferralRegisteredBy=register_type,
                        ReferralSource=referral_source,
                        ReferredBy=referral_doctor_instance,
                        created_by=created_by
                    )
            except ValueError as e:
                # Handle invalid register_type
                pass
   
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data,'data')
            register_Id = data.get('RegistrationId', '')
            register_type = data.get('RegisterType', '')
            patient = data.get('PatientId', '')
            Speciality = data.get('Speciality', '')
            doctor_name = data.get('DoctorName', '')
            complaint = data.get('Complaint', '')
            is_mlc = data.get('IsMLC', 'No')
            # flagging = data.get('Flagging', '')
            is_referral = data.get('IsReferral', 'No')
            ReferralSource = data.get('ReferralSource', '')
            ReferredBy = data.get('ReferredBy', '')
            AdmissionPurpose = data.get('AdmissionPurpose','')
            DrInchargeatTimeofAdmission = data.get('DrInchargeAtTimeOfAdmission','')
            NexttokinName = data.get('NextToKinName','')
            relation = data.get('Relation','')
            relativePhoneno = data.get('RelativePhoneNo','')
            personLiableforpayment = data.get('PersonLiableForBillPayment','')
            familyhead = data.get('FamilyHead','')
            familyheadName = data.get('FamilyHeadName','')
            ipKitGiven = data.get('IpKitGiven','No')
            created_by = data.get('Created_by', '')
            Location_Id = data.get('Location', None)
            RoomId = data.get('RoomId', '')
 
            patient_category = data.get('PatientCategory', '')
            insurance_name = data.get('InsuranceName', '')
            insurance_type = data.get('InsuranceType', '')
           
            client_name = data.get('ClientName', '')
            client_type = data.get('ClientType', '')
            client_employee_id = data.get('ClientEmployeeId', '')
            client_employee_designation = data.get('ClientEmployeeDesignation', '')
            client_employee_relation = data.get('ClientEmployeeRelation', '')
           
            CorporateName = data.get('CorporateName', '')
            CorporateType = data.get('CorporateType', '')
            CorporateEmployeeId = data.get('CorporateEmployeeId', '')
            CorporateEmployeeDesignation = data.get('CorporateEmployeeDesignation', '')
            CorporateEmployeeRelation = data.get('CorporateEmployeeRelation', '')
           
            employee_id = data.get('EmployeeId', '')
            employee_relation = data.get('EmployeeRelation', '')
           
            doctor_id = data.get('DoctorId', '')
            doctor_relation = data.get('DoctorRelation', '')
           
            donation_type = data.get('DonationType', '')
 
 
            patient_ins = Patient_Detials.objects.get(PatientId=patient) if patient else None
            
            specialization_instance = Speciality_Detials.objects.get(Speciality_Id=Speciality) if Speciality else None
            doctor_name_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=doctor_name) if doctor_name else None
            DrInchargeatTimeofAdmission_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=DrInchargeatTimeofAdmission) if DrInchargeatTimeofAdmission else None
            referral_doctor_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=ReferredBy) if ReferredBy else None
            location_instance = Location_Detials.objects.get(Location_Id=Location_Id) if Location_Id else None
            roomid_instance = Room_Master_Detials.objects.get(Room_Id=RoomId) if RoomId else None
            # Flagging_instance = Flaggcolor_Detials.objects.get(Flagg_Id=flagging) if flagging else None
           
            employee_instance = Employee_Personal_Form_Detials.objects.get(Employee_ID=employee_id) if employee_id else None
            doctor_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=doctor_id) if doctor_id else None
            # Insurance_instance = Insurance_Master_Detials.objects.get(Insurance_Id=insurance_name) if insurance_name else None
            # Client_instance = Client_Master_Detials.objects.get(Client_Id=client_name) if client_name else None
            # Donation_instance = Donation_Master_Detials.objects.get(Donation_Id=donation_type) if donation_type else None
            # Corporate_instance = Corporate_Master_Detials.objects.get(Corporate_Id=CorporateName) if CorporateName else None
           
            Insurance_instance = None
            if insurance_name:
              Insurance_instance = Insurance_Master_Detials.objects.get(Insurance_Id=insurance_name)
             
            print(Insurance_instance,'Insurance_instanceqqqqqqqqqqqq')
           
            Client_instance = None
            if client_name:
               Client_instance = Client_Master_Detials.objects.get(Client_Id=client_name)
           
            Donation_instance = None
            if donation_type:
               Donation_instance = Donation_Master_Detials.objects.get(Donation_Id=donation_type)
           
            Corporate_instance = None
            if CorporateName:
               Corporate_instance = Corporate_Master_Detials.objects.get(Corporate_Id=CorporateName)
           
            # print(Client_instance,'Client_instanceqqqqqqqqqqq')
 
            if register_Id :
               
                ip_details = Patient_IP_Registration_Detials.objects.get(pk=register_Id)
                print(ip_details,'ip_details')
               
                ip_details.Specialization=specialization_instance  
                ip_details.PrimaryDoctor=doctor_name_instance
                ip_details.Complaint=complaint  
                ip_details.IsMLC=is_mlc  
                # ip_details.Flagging=Flagging_instance  
                ip_details.IsReferral=is_referral
 
 
 
                ip_details.PatientCategory = patient_category
                ip_details.InsuranceName = Insurance_instance if Insurance_instance else None
                ip_details.InsuranceType = insurance_type
                ip_details.ClientName = Client_instance if Client_instance else None
                ip_details.ClientType = client_type
                ip_details.ClientEmployeeId = client_employee_id
                ip_details.ClientEmployeeDesignation = client_employee_designation
                ip_details.ClientEmployeeRelation = client_employee_relation
               
                ip_details.CorporateName = Corporate_instance if Corporate_instance else None
                ip_details.CorporateType = CorporateType
                ip_details.CorporateEmployeeId = CorporateEmployeeId
                ip_details.CorporateEmployeeDesignation = CorporateEmployeeDesignation
                ip_details.CorporateEmployeeRelation = CorporateEmployeeRelation
 
                ip_details.EmployeeId = employee_instance if employee_instance else None
                ip_details.EmployeeRelation = employee_relation
                ip_details.DoctorId = doctor_instance if doctor_instance else None
                ip_details.DoctorRelation = doctor_relation
                ip_details.DonationType = Donation_instance if Donation_instance else None
                ip_details.updated_by = created_by
                ip_details.save()
               
                ip_admission = Patient_Admission_Detials.objects.get(IP_Registration_Id__pk = ip_details.pk)
                ip_admission.AdmissionPurpose = AdmissionPurpose
                ip_admission.DrInchargeAtTimeOfAdmission = DrInchargeatTimeofAdmission_instance
                ip_admission.NextToKinName = NexttokinName
                ip_admission.Relation = relation
                ip_admission.RelativePhoneNo = relativePhoneno
                ip_admission.PersonLiableForPayment = personLiableforpayment
                ip_admission.FamilyHead = familyhead
                ip_admission.FamilyHeadName = familyheadName
                ip_admission.IpKitGiven = ipKitGiven
                ip_admission.updated_by = created_by
                ip_admission.save()
               
                create_or_update_referral(is_referral,ReferralSource,referral_doctor_instance,register_type,register_Id,ip_details,created_by)
               
                return JsonResponse({'success': 'IP Patient Detials Updated Successfully'})
            else:    
               
                print('NewwwwwReggggg')
                Patient_IP = Patient_IP_Registration_Detials.objects.create(
                    PatientId = patient_ins,
                    Specialization=specialization_instance,
                    PrimaryDoctor=doctor_name_instance,
                    Complaint=complaint,
                    IsMLC=is_mlc,
                    # Flagging=Flagging_instance,
                    IsReferral=is_referral,
                    # ReferralSource=ReferralSource,
                    # ReferredBy=ReferredBy,
                    PatientCategory = patient_category,
                    InsuranceName = Insurance_instance,
                    InsuranceType = insurance_type,
                    ClientName = Client_instance,
                    ClientType = client_type,
                    ClientEmployeeId = client_employee_id,
                    ClientEmployeeDesignation = client_employee_designation,
                    ClientEmployeeRelation = client_employee_relation,
                   
                    CorporateName = Corporate_instance,
                    CorporateType = CorporateType,
                    CorporateEmployeeId = CorporateEmployeeId,
                    CorporateEmployeeDesignation = CorporateEmployeeDesignation,
                    CorporateEmployeeRelation = CorporateEmployeeRelation,
 
                    EmployeeId = employee_instance,
                    EmployeeRelation = employee_relation,
                    DoctorId = doctor_instance,
                    DoctorRelation = doctor_relation,
                    DonationType = Donation_instance,
                    created_by=created_by,
                    Location=location_instance
                )
                print('333333333333333333')


                patient_details = Patient_Detials.objects.get(PatientId=patient)
                patient_details.Status = 'Registered'
                patient_details.save()


                
                print('444444444444444444')
               
               
                Patient_Admission_Detials.objects.create(
                    IP_Registration_Id = Patient_IP,
                    AdmissionPurpose = AdmissionPurpose,
                    DrInchargeAtTimeOfAdmission = DrInchargeatTimeofAdmission_instance,
                    NextToKinName = NexttokinName,
                    Relation = relation,
                    RelativePhoneNo = relativePhoneno,
                    PersonLiableForPayment = personLiableforpayment,
                    FamilyHead = familyhead,
                    FamilyHeadName = familyheadName,
                    IpKitGiven = ipKitGiven,
                )
                print('55555555555555')
                   
                Patient_Admission_Room_Detials.objects.create(
                    RegisterType = register_type,
                    IP_Registration_Id = Patient_IP,
                    Casuality_Registration_Id = None,
                    RoomId = roomid_instance,
                    created_by=created_by
                )

                print('666666666666')
                print('666666666666',patient_ins)
                Emg_patient_details = Emg_to_IP_Convertion_Table.objects.get(Patient_Id=patient_ins)
                print(Emg_patient_details,'Emg_patient_details---------')
                
                Emg_patient_details.Status = 'Completed'
                Emg_patient_details.save()

                print('77777777777777777')

                print(Emg_patient_details,'Emg_patient_details---------')

                create_or_update_referral(is_referral,ReferralSource,referral_doctor_instance,register_type,register_Id,Patient_IP,created_by)
               
                return JsonResponse({'success': 'Patient Admitted successfully'})
                       
        except Exception as e:
            return JsonResponse({'error': str(e)})
 


@csrf_exempt
@require_http_methods(["GET"])
def get_ip_Patient_registration_details_for_workbench(request):
    try:
        query = request.GET.get('query', '')
        status = request.GET.get('status', '')
        DoctorId = request.GET.get('DoctorId', '')
 
        # Map status to Booking_Status
        Booking_Status = 'Booked' if status == 'Pending' else ('Occupied' if status == 'Admitted' else 'Cancelled')
       
       
        queryset = Patient_IP_Registration_Detials.objects.all()
       
        print(queryset,'queryset')
        # Apply filters based on the query parameters
        if query:
            queryset = queryset.filter(
                Q(PatientId_FirstName_icontains=query) |
                Q(PatientId_MiddleName_icontains=query) |
                Q(PatientId_SurName_icontains=query) |
                Q(PatientId_PatientId_icontains=query) |
                Q(PatientId_PhoneNo_icontains=query)
            ).filter(Booking_Status=Booking_Status)
       
        if DoctorId:
            queryset = queryset.filter(PrimaryDoctor__pk = DoctorId)
       
 
        if status:
            queryset = queryset.filter(Q(Status__icontains=status)).filter(Booking_Status=Booking_Status)
 
        # Serialize the filtered queryset
        ip_register_data = []
        for idx, register in enumerate(queryset, start=1):
            # client_name = register.ClientName.Client_Name if register.ClientName else None
            # insurance_name = register.InsuranceName.Insurance_Name if register.InsuranceName else None
            # Flagging_name = register.Flagging.Flagg_Name if register.Flagging else None
            # Flagging_color = register.Flagging.Flagg_Color if register.Flagging else None
            BloodGroup_name = register.PatientId.BloodGroup.BloodGroup_Name if register.PatientId.BloodGroup else None
           
            appointment_dict = {
                'id': idx,
                'PatientProfile': get_file_image(register.PatientId.Patient_profile) if register.PatientId.Patient_profile else None,
                'RegistrationId': register.Registration_Id,
                'PatientId': register.PatientId.PatientId,
                'PatientName': f"{register.PatientId.Title.Title_Name}.{register.PatientId.FirstName} {register.PatientId.MiddleName} {register.PatientId.SurName}",
                'PhoneNo': register.PatientId.PhoneNo,
                'Age': register.PatientId.Age,
                'Gender': register.PatientId.Gender,
                'BloodGroup': BloodGroup_name,
                'Complaint': register.Complaint,
                'isMLC': register.IsMLC,
                # 'Flagging': Flagging_name,
                # 'FlaggingColour': Flagging_color,
                # 'Flagging': register.Flagging,
                'isRefferal': register.IsReferral,
                # 'ClientName': client_name,  # Fixed reference
                # 'InsuranceName': insurance_name,  # Fixed reference
                'Status': register.Status,
                'DoctorName': f"{register.PrimaryDoctor.Tittle.Title_Name}.{register.PrimaryDoctor.First_Name} {register.PrimaryDoctor.Last_Name}" if register.PrimaryDoctor else '',
                'Specilization': str(register.Specialization.Speciality_Name) if register.Specialization else '',
            }
 
            # Add room details if Booking_Status is 'Booked' or 'Occupied'
           
            if register.Booking_Status in ['Booked', 'Occupied']:
                roomdetials = Patient_Admission_Room_Detials.objects.filter(IP_Registration_Id=register).order_by('-created_by').first()
                print(roomdetials.RoomId,'roomdetials.RoomId')
                if roomdetials:
                    appointment_dict['BuildingName'] = roomdetials.RoomId.Building_Name.Building_Name if roomdetials.RoomId else None
                    appointment_dict['BlockName'] = roomdetials.RoomId.Block_Name.Block_Name if roomdetials.RoomId else None
                    appointment_dict['FloorName'] = roomdetials.RoomId.Floor_Name.Floor_Name if roomdetials.RoomId else None
                    appointment_dict['WardName'] = roomdetials.RoomId.Ward_Name.Ward_Name.Ward_Name if roomdetials.RoomId else None
                    # appointment_dict['RoomName'] = roomdetials.RoomId.Room_Name.Room_Name if roomdetials.RoomId.Room_Name else None
                    appointment_dict['RoomNo'] = roomdetials.RoomId.Room_No if roomdetials.RoomId else None
                    appointment_dict['BedNo'] = roomdetials.RoomId.Bed_No if roomdetials.RoomId else None
                    appointment_dict['RoomId'] = roomdetials.RoomId.Room_Id if roomdetials.RoomId else None
 
            ip_register_data.append(appointment_dict)
 
        return JsonResponse(ip_register_data, safe=False)
 
    except Exception as e:
        return JsonResponse({'error': str(e)})




@csrf_exempt
@require_http_methods(["GET"])
def get_IP_Registration_edit_details(request):
    try:
        RegistrationId = request.GET.get('RegistrationId', None)
        # RegistrationType = request.GET.get('RegistrationType', None)
        IP_Patient = Patient_IP_Registration_Detials.objects.get(pk = RegistrationId)
        admission_instance = Patient_Admission_Detials.objects.get(IP_Registration_Id__pk = RegistrationId)
        admission_room_instance = Patient_Admission_Room_Detials.objects.get(IP_Registration_Id__pk = RegistrationId)
        # referral_instance = Patient_Referral_Detials.objects.get(IP_Register_Id__pk = RegistrationId)
        referral_details = None

        # Check for referral details by OP, IP, and Emergency Register IDs
        try:
            referral_details = Patient_Referral_Detials.objects.filter(
                OP_Register_Id__Registration_Id=RegistrationId
            ).first() or Patient_Referral_Detials.objects.filter(
                IP_Register_Id__Registration_Id=RegistrationId
            ).first() or Patient_Referral_Detials.objects.filter(
                Emergency_Register_Id__Registration_Id=RegistrationId
            ).first()
        except Patient_Referral_Detials.DoesNotExist:
            referral_details = None

        # print(referral_instance,'referral_instance')
        print(admission_instance,'admission_instance')
        print(admission_instance.AdmissionPurpose,'admission_instance.AdmissionPurpose')
        
        
        Registration_dict = {
            'Title': IP_Patient.PatientId.Title.Title_Id if IP_Patient.PatientId.Title else None,
            'PatientId': IP_Patient.PatientId.PatientId if IP_Patient.PatientId else "",
            'FirstName': IP_Patient.PatientId.FirstName if IP_Patient.PatientId else "",
            'MiddleName': IP_Patient.PatientId.MiddleName if IP_Patient.PatientId else "",
            'SurName': IP_Patient.PatientId.SurName if IP_Patient.PatientId else "",
            'Gender': IP_Patient.PatientId.Gender if IP_Patient.PatientId else "",
            'MaritalStatus': IP_Patient.PatientId.MaritalStatus if IP_Patient.PatientId else "",
            'SpouseName': IP_Patient.PatientId.SpouseName if IP_Patient.PatientId else "",
            'FatherName': IP_Patient.PatientId.FatherName if IP_Patient.PatientId else "",
            'DOB': IP_Patient.PatientId.DOB if IP_Patient.PatientId else "",
            'Age': IP_Patient.PatientId.Age if IP_Patient.PatientId else "",
            'PhoneNo': IP_Patient.PatientId.PhoneNo if IP_Patient.PatientId else "",
            'Email': IP_Patient.PatientId.Email if IP_Patient.PatientId else "",
            'BloodGroup': IP_Patient.PatientId.BloodGroup.BloodGroup_Id if IP_Patient.PatientId.BloodGroup else None,
            'Occupation': IP_Patient.PatientId.Occupation if IP_Patient.PatientId else "",
            'Religion': IP_Patient.PatientId.Religion.Religion_Id if IP_Patient.PatientId.Religion else None,
            'ReligionName': IP_Patient.PatientId.Religion.Religion_Name if IP_Patient.PatientId.Religion else None,
            'Nationality': IP_Patient.PatientId.Nationality if IP_Patient.PatientId else "",
            'UniqueIdType': IP_Patient.PatientId.UniqueIdType if IP_Patient.PatientId else "",
            'UniqueIdNo': IP_Patient.PatientId.UniqueIdNo if IP_Patient.PatientId else "",
            'PatientType': IP_Patient.PatientId.PatientType if IP_Patient.PatientId else "",
            'DoorNo': IP_Patient.PatientId.DoorNo if IP_Patient.PatientId else "",
            'Street': IP_Patient.PatientId.Street if IP_Patient.PatientId else "",
            'Area': IP_Patient.PatientId.Area if IP_Patient.PatientId else "",
            'City': IP_Patient.PatientId.City if IP_Patient.PatientId else "",
            'State': IP_Patient.PatientId.State if IP_Patient.PatientId else "",
            'Country': IP_Patient.PatientId.Country if IP_Patient.PatientId else "",
            'Pincode': IP_Patient.PatientId.Pincode if IP_Patient.PatientId else "",
            'ABHA': IP_Patient.PatientId.ABHA if IP_Patient.PatientId else "",
        
            'Speciality': IP_Patient.Specialization.Speciality_Id if IP_Patient.Specialization else None,
            'DoctorName': f"{IP_Patient.PrimaryDoctor.Tittle.Title_Name if IP_Patient.PrimaryDoctor and IP_Patient.PrimaryDoctor.Tittle else None}.{IP_Patient.PrimaryDoctor.ShortName}" if IP_Patient.PrimaryDoctor else None,
            'PrimaryDoctor': IP_Patient.PrimaryDoctor.Doctor_ID if IP_Patient.PrimaryDoctor else None,
            
            'Complaint': IP_Patient.Complaint,
            'IsMLC': IP_Patient.IsMLC,
            'IsReferral': IP_Patient.IsReferral,
            'PatientCategory': IP_Patient.PatientCategory,
            'InsuranceName': IP_Patient.InsuranceName.Insurance_Id if IP_Patient.InsuranceName else None,
            'InsuranceType': IP_Patient.InsuranceType,
            'ClientName': IP_Patient.ClientName.Client_Id if IP_Patient.ClientName else None,
            'ClientType': IP_Patient.ClientType,
            'ClientEmployeeId': IP_Patient.ClientEmployeeId,
            'ClientEmployeeDesignation': IP_Patient.ClientEmployeeDesignation,
            'ClientEmployeeRelation': IP_Patient.ClientEmployeeRelation,

            'CorporateName': IP_Patient.CorporateName.Corporate_Id if IP_Patient.CorporateName else None,
            'CorporateType': IP_Patient.CorporateType,
            'CorporateEmployeeId': IP_Patient.CorporateEmployeeId,
            'CorporateEmployeeDesignation': IP_Patient.CorporateEmployeeDesignation,
            'CorporateEmployeeRelation': IP_Patient.CorporateEmployeeRelation,
        
            'EmployeeId': IP_Patient.EmployeeId.Employee_ID if IP_Patient.EmployeeId else "",
            'EmployeeRelation': IP_Patient.EmployeeRelation,
            
            'DoctorId': IP_Patient.DoctorId.pk if IP_Patient.DoctorId else "",
            'DoctorRelation': IP_Patient.DoctorRelation,
            'DonationType': IP_Patient.DonationType.Donation_Id if IP_Patient.DonationType else None,

            'AdmissionPurpose': admission_instance.AdmissionPurpose if admission_instance else '',
            'DrInchargeAtTimeOfAdmission': admission_instance.DrInchargeAtTimeOfAdmission.Doctor_ID if admission_instance and admission_instance.DrInchargeAtTimeOfAdmission else '',
            'NextToKinName': admission_instance.NextToKinName if admission_instance else '',
            'Relation': admission_instance.Relation if admission_instance else '',
            'RelativePhoneNo': admission_instance.RelativePhoneNo if admission_instance else '',
            'PersonLiableForBillPayment': admission_instance.PersonLiableForPayment if admission_instance else '',
            
            'FamilyHead': admission_instance.FamilyHead if admission_instance else '',
            'FamilyHeadName': admission_instance.FamilyHeadName if admission_instance else '',
            
            'IpKitGiven': admission_instance.IpKitGiven if admission_instance else '',
        
            'IsReferal': IP_Patient.IsReferral,
            'Building': admission_room_instance.RoomId.Building_Name.pk if admission_room_instance else "",
            'Block': admission_room_instance.RoomId.Block_Name.pk if admission_room_instance else "",
            'Floor': admission_room_instance.RoomId.Floor_Name.pk if admission_room_instance else "",
            'WardType': admission_room_instance.RoomId.Ward_Name.Ward_Name.pk if admission_room_instance else "",
            'RoomNo': admission_room_instance.RoomId.Room_No if admission_room_instance else "",
            'BedNo': admission_room_instance.RoomId.Bed_No if admission_room_instance else "",
        
            'BuildingName': admission_room_instance.RoomId.Building_Name.Building_Name if admission_room_instance else "",
            'BlockName': admission_room_instance.RoomId.Block_Name.Block_Name if admission_room_instance else "",
            'FloorName': admission_room_instance.RoomId.Floor_Name.Floor_Name if admission_room_instance else "",
            'WardTypeName': admission_room_instance.RoomId.Ward_Name.Ward_Name.Ward_Name if admission_room_instance else "",
            'RoomId': admission_room_instance.RoomId.pk if admission_room_instance else "",
        }

        if referral_details:
            Registration_dict.update({
                'ReferralSource': referral_details.ReferralSource,
                'ReferredBy': f"{referral_details.ReferredBy.Tittle.Title_Name}.{referral_details.ReferredBy.First_Name} {referral_details.ReferredBy.Last_Name}" if referral_details.ReferredBy else None,
            })

        print(Registration_dict,'Registration_dict')
        
            
        return JsonResponse(Registration_dict,safe=False)
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST", "OPTIONS", "GET"])
def Emergency_Patient_Registration(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data, 'data')

            patient_id = data.get('PatientId', '')
            FirstName = data.get('FirstName', '')
            PhoneNumber = data.get('PhoneNumber', '')
            Gender = data.get('Gender', '')
            IdentificationMark1 = data.get('IdentificationMark1', '')
            IdentificationMark2 = data.get('IdentificationMark2', '')
            IsConscious = data.get('IsConscious', '')
            Instructions = data.get('Instructions', '')
            IsMLC = data.get('IsMLC', '')
            created_by = data.get('Created_by', '')
            Location = data.get('Location', '')
            RoomId = data.get('RoomId', '')
            register_type = data.get('RegisterType', '')



            location_instance = Location_Detials.objects.get(Location_Id=Location) if Location else None
            roomid_instance = Room_Master_Detials.objects.get(Room_Id=RoomId) if RoomId else None

            with transaction.atomic():
                patient = None
                if patient_id:
                    # Validate Patient ID
                    try:
                        patient = Patient_Detials.objects.get(PatientId=patient_id)
                    except Patient_Detials.DoesNotExist:
                        return JsonResponse({'warn': "The Patient ID is not valid"})

                    # Check for duplicate patients if any identifier is provided
                    if FirstName or PhoneNumber:
                        if Patient_Detials.objects.filter(
                            Q(PhoneNo=PhoneNumber) & Q(FirstName=FirstName)
                        ).exclude(PatientId=patient_id).exists():
                            existing_patient = Patient_Detials.objects.filter(
                                Q(PhoneNo=PhoneNumber) & Q(FirstName=FirstName)
                            ).first()
                            return JsonResponse({'warn': f"The Patient {existing_patient.PatientId} is already registered with {PhoneNumber} and {FirstName}"})

                    # Update patient details
                    patient.FirstName = FirstName
                    patient.Gender = Gender
                    patient.PhoneNo = PhoneNumber
                    patient.updated_by = created_by
                    patient.save()

                else:
                    print('Creating new patient')

                    # Check for duplicates only if identifiers are provided
                    if FirstName or PhoneNumber:
                        if Patient_Detials.objects.filter(
                            Q(PhoneNo=PhoneNumber) & Q(FirstName=FirstName)
                        ).exists():
                            existing_patient = Patient_Detials.objects.filter(
                                Q(PhoneNo=PhoneNumber) & Q(FirstName=FirstName)
                            ).first()
                            return JsonResponse({'warn': f"The Patient {existing_patient.PatientId} is already registered with {PhoneNumber} and {FirstName}"})

                    # Create new patient
                    patient = Patient_Detials.objects.create(
                        FirstName=FirstName,
                        Gender=Gender,
                        PhoneNo=PhoneNumber,
                        Status = 'EmgPatientSaved',
                        created_by=created_by
                    )
                    patient.save()



                    # patient_details = Patient_Detials.objects.get(PatientId=patient)
                    # patient_details.Status = 'EmgPatientSaved'
                    # patient_details.save()

                  

                    print(patient, 'patient')

                    # Create Emergency Registration Details
                Emergency = Patient_Emergency_Registration_Detials.objects.create(
                    PatientId=patient,
                    IdentificationMark1=IdentificationMark1,
                    IdentificationMark2=IdentificationMark2,
                    Instructions=Instructions,
                    IsConscious=IsConscious,
                    IsMLC=IsMLC,
                    Location=location_instance,
                    created_by=created_by,
                )

                Emergency.save()

                EmgPatientAdmission = Patient_Admission_Room_Detials.objects.create(
                    RegisterType=register_type,
                    Emergency_Registration_Id=Emergency,
                    RoomId=roomid_instance,
                    created_by=created_by
                )
                EmgPatientAdmission.save()


                data['patient_id'] = patient.PatientId
                data['RegistrationId'] = Emergency.Registration_Id
                # return JsonResponse({'success': 'Emergency Patient Details Saved successfully'},safe=False)
                return JsonResponse({'success': 'Emergency Patient Details Saved successfully','data': [data]},safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': str(e)})

    elif request.method == 'GET':
        try:
            patient_id = request.GET.get('PatientId')
            if patient_id:
                try:
                    patient = Patient_Detials.objects.get(PatientId=patient_id)
                    return JsonResponse({
                        'id': patient.PatientId,
                        'phoneNo': patient.PhoneNo,
                        'firstName': patient.FirstName,
                        'lastName': patient.SurName,
                    })
                except Patient_Detials.DoesNotExist:
                    return JsonResponse({'error': 'Patient with the given ID does not exist'})
            else:
                patients = list(Patient_Detials.objects.values())
                return JsonResponse(patients, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Invalid request method'}, status=405)







@csrf_exempt
@require_http_methods(['POST', 'GET'])
def Emergency_Patient_With_Room_Registration_Details_Link(request):
    
    @transaction.atomic
    def create_or_update_referral(is_referral, referral_source, referral_doctor_instance, register_type, register_id, newdata, created_by):
        if is_referral == 'Yes':
            try:
                if register_id:
                    filters = {
                        'Emergency': 'Emergency_Register_Id__pk',
                    }
                    filter_key = filters.get(register_type)
                    if not filter_key:
                        raise ValueError("Invalid register_type provided.")
                    if Patient_Referral_Detials.objects.filter(**{filter_key: register_id}).exists():
                        referral = Patient_Referral_Detials.objects.get(**{filter_key: register_id})
                        referral.ReferralSource = referral_source
                        referral.ReferredBy = referral_doctor_instance
                        referral.save()
                    else:
                        Patient_Referral_Detials.objects.create(
                            **{
                                'Emergency_Register_Id': newdata if register_type == 'Emergency' else None,
                            },
                            ReferralRegisteredBy=register_type,
                            ReferralSource=referral_source,
                            ReferredBy=referral_doctor_instance,
                            created_by=created_by
                        )
                    
                else:
                    Patient_Referral_Detials.objects.create(
                        **{
                            'Emergency_Register_Id': newdata if register_type == 'Emergency' else None,
                        },
                        ReferralRegisteredBy=register_type,
                        ReferralSource=referral_source,
                        ReferredBy=referral_doctor_instance,
                        created_by=created_by
                    )
            except ValueError as e:
                # Handle invalid register_type
                pass

    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Extracting all input data
            register_Id = data.get('RegistrationId', '')
            register_type = data.get('RegisterType', '')
            patient = data.get('PatientId', '')
            print(patient,'patienttttttttt')
            Speciality = data.get('Speciality', '')
            doctor_name = data.get('DoctorName', '')
            complaint = data.get('Complaint', '')
            is_mlc = data.get('IsMLC', 'No')
            is_referral = data.get('IsReferral', 'No')
            ReferralSource = data.get('ReferralSource', '')
            ReferredBy = data.get('ReferredBy', '')
            AdmissionPurpose = data.get('AdmissionPurpose', '')
            DrInchargeatTimeofAdmission = data.get('DrInchargeAtTimeOfAdmission', '')
            NexttokinName = data.get('NextToKinName', '')
            relation = data.get('Relation', '')
            relativePhoneno = data.get('RelativePhoneNo', '')
            personLiableforpayment = data.get('PersonLiableForBillPayment', '')
            familyhead = data.get('FamilyHead', '')
            familyheadName = data.get('FamilyHeadName', '')
            ipKitGiven = data.get('IpKitGiven', 'No')
            created_by = data.get('Created_by', '')
            Location_Id = data.get('Location', None)
            RoomId = data.get('RoomId', '')
            insurance_name = data.get('InsuranceName', '')
            insurance_type = data.get('InsuranceType', '')
           
            client_name = data.get('ClientName', '')
            client_type = data.get('ClientType', '')
            client_employee_id = data.get('ClientEmployeeId', '')
            client_employee_designation = data.get('ClientEmployeeDesignation', '')
            client_employee_relation = data.get('ClientEmployeeRelation', '')
           
            CorporateName = data.get('CorporateName', '')
            CorporateType = data.get('CorporateType', '')
            CorporateEmployeeId = data.get('CorporateEmployeeId', '')
            CorporateEmployeeDesignation = data.get('CorporateEmployeeDesignation', '')
            CorporateEmployeeRelation = data.get('CorporateEmployeeRelation', '')
           
            employee_id = data.get('EmployeeId', '')
            employee_relation = data.get('EmployeeRelation', '')
           
            doctor_id = data.get('DoctorId', '')
            doctor_relation = data.get('DoctorRelation', '')
            
            donation_type = data.get('DonationType', '')

            print(register_Id,'register_Id')

            # Fetch related objects
            patient_instance = Patient_Detials.objects.get(PatientId=patient) if patient else None
            print(patient_instance,'patient_instance')
            specialization_instance = Speciality_Detials.objects.get(Speciality_Id=Speciality) if Speciality else None
            doctor_name_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=doctor_name) if doctor_name else None
            DrInchargeatTimeofAdmission_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=DrInchargeatTimeofAdmission) if DrInchargeatTimeofAdmission else None
            referral_doctor_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=ReferredBy) if ReferredBy else None
            location_instance = Location_Detials.objects.get(Location_Id=Location_Id) if Location_Id else None
            roomid_instance = Room_Master_Detials.objects.get(Room_Id=RoomId) if RoomId else None

            employee_instance = Employee_Personal_Form_Detials.objects.get(Employee_ID=employee_id) if employee_id else None
            doctor_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=doctor_id) if doctor_id else None
            Insurance_instance = Insurance_Master_Detials.objects.get(Insurance_Id=insurance_name) if insurance_name else None
            Client_instance = Client_Master_Detials.objects.get(Client_Id=client_name) if client_name else None
            Donation_instance = Donation_Master_Detials.objects.get(Donation_Id=donation_type) if donation_type else None
            Corporate_instance = Corporate_Master_Detials.objects.get(Corporate_Id=CorporateName) if CorporateName else None
            
            # Handle patient emergency registration details
            if register_Id and Patient_Emergency_Registration_Detials.objects.filter(pk=register_Id).exists():
                print('rrrrrrrrrrrrrrrrrrrrrrrrrr')

                ip_details = Patient_Emergency_Registration_Detials.objects.get(pk=register_Id)
                ip_details.Specialization = specialization_instance
                ip_details.PrimaryDoctor = doctor_name_instance
                ip_details.Complaint = complaint
                ip_details.IsMLC = is_mlc
                ip_details.IsReferral = is_referral
                ip_details.PatientCategory = data.get('PatientCategory', '')
                ip_details.InsuranceName = Insurance_instance
                # ip_details.InsuranceName = Insurance_Master_Detials.objects.get(Insurance_Id=data.get('InsuranceName', '')) if data.get('InsuranceName') else None
                ip_details.InsuranceType = insurance_type 
                
                ip_details.ClientName = Client_instance
                # ip_details.ClientName = Client_Master_Detials.objects.get(Client_Id=data.get('ClientName', '')) if data.get('ClientName') else None
                ip_details.ClientType = client_type 
                ip_details.ClientEmployeeId = client_employee_id
                ip_details.ClientEmployeeDesignation = client_employee_designation 
                ip_details.ClientEmployeeRelation = client_employee_relation 
                
                ip_details.CorporateName = Corporate_instance
                # ip_details.CorporateName = Corporate_Master_Detials.objects.get(Corporate_Id=data.get('CorporateName', '')) if data.get('CorporateName') else None
                ip_details.CorporateType = CorporateType 
                ip_details.CorporateEmployeeId = CorporateEmployeeId 
                ip_details.CorporateEmployeeDesignation = CorporateEmployeeDesignation 
                ip_details.CorporateEmployeeRelation = CorporateEmployeeRelation 

                ip_details.EmployeeId = employee_instance
                # ip_details.EmployeeId = Employee_Personal_Form_Detials.objects.get(Employee_ID=data.get('EmployeeId', '')) if data.get('EmployeeId') else None
                ip_details.EmployeeRelation = employee_relation 
                

                ip_details.DoctorId = doctor_instance
                # ip_details.DoctorId = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=data.get('DoctorId', '')) if data.get('DoctorId') else None
                ip_details.DoctorRelation = doctor_relation
                
                ip_details.DonationType = Donation_instance
                # ip_details.DonationType = Donation_Master_Detials.objects.get(Donation_Id=data.get('DonationType', '')) if data.get('DonationType') else None
                ip_details.updated_by = created_by
                ip_details.SavedStatus = 'Registered'
                ip_details.save()

                print('33333333333333333')
                patient_details = Patient_Detials.objects.get(PatientId=patient)
                patient_details.Status = 'Registered'
                patient_details.save()
                print('222222222222222')


                # Handle patient admission details
                ip_admission = Patient_Admission_Detials.objects.filter(Emergency_Registration_Id__Registration_Id=ip_details.pk).first()
                if ip_admission is None:
                    ip_admission = Patient_Admission_Detials(
                        Emergency_Registration_Id=ip_details,
                        AdmissionPurpose=AdmissionPurpose,
                        DrInchargeAtTimeOfAdmission=DrInchargeatTimeofAdmission_instance,
                        NextToKinName=NexttokinName,
                        Relation=relation,
                        RelativePhoneNo=relativePhoneno,
                        PersonLiableForPayment=personLiableforpayment,
                        FamilyHead=familyhead,
                        FamilyHeadName=familyheadName,
                        IpKitGiven=ipKitGiven,
                        updated_by=created_by
                    )
                    ip_admission.save()
                else:
                    ip_admission.AdmissionPurpose = AdmissionPurpose
                    ip_admission.DrInchargeAtTimeOfAdmission = DrInchargeatTimeofAdmission_instance
                    ip_admission.NextToKinName = NexttokinName
                    ip_admission.Relation = relation
                    ip_admission.RelativePhoneNo = relativePhoneno
                    ip_admission.PersonLiableForPayment = personLiableforpayment
                    ip_admission.FamilyHead = familyhead
                    ip_admission.FamilyHeadName = familyheadName
                    ip_admission.IpKitGiven = ipKitGiven
                    ip_admission.updated_by = created_by
                    ip_admission.save()

                # patient_details = Patient_Detials.objects.get(PatientId=patient)
                # patient_details.Status = 'Registered'
                # patient_details.save()

                # Referral handling
                create_or_update_referral(is_referral, ReferralSource, referral_doctor_instance, register_type, register_Id, ip_details, created_by)

                return JsonResponse({'success': 'Emergency Patient Details Updated successfully'})

            # For new registrations
            else:
                print('mmmmmmmmmmmmmmmmmmmmmmmm')
                # Create new emergency registration and related data
                Patient_Emg = Patient_Emergency_Registration_Detials.objects.create(
                    PatientId=patient_instance,
                    Specialization=specialization_instance,
                    PrimaryDoctor=doctor_name_instance,
                    Complaint=complaint,
                    IsMLC=is_mlc,
                    IsReferral=is_referral,
                    PatientCategory=data.get('PatientCategory', ''),
                    InsuranceName=Insurance_Master_Detials.objects.get(Insurance_Id=data.get('InsuranceName', '')) if data.get('InsuranceName') else None,
                    created_by=created_by,
                    Location=location_instance
                )

                # Create patient admission details
                Patient_Admission_Detials.objects.create(
                    Emergency_Registration_Id=Patient_Emg,
                    AdmissionPurpose=AdmissionPurpose,
                    DrInchargeAtTimeOfAdmission=DrInchargeatTimeofAdmission_instance,
                    NextToKinName=NexttokinName,
                    Relation=relation,
                    RelativePhoneNo=relativePhoneno,
                    PersonLiableForPayment=personLiableforpayment,
                    FamilyHead=familyhead,
                    FamilyHeadName=familyheadName,
                    IpKitGiven=ipKitGiven,
                )

                patient_details = Patient_Detials.objects.get(PatientId=patient)
                patient_details.Status = 'Registered'
                patient_details.save()

                

                # Referral handling
                create_or_update_referral(is_referral, ReferralSource, referral_doctor_instance, register_type, register_Id, Patient_Emg, created_by)

                return JsonResponse({'success': 'Patient Admission Details Added successfully'})

        except Exception as e:
            print(str(e),'vvvvvvvvvv')
            return JsonResponse({'error': str(e)})





@csrf_exempt
@require_http_methods(["GET"])
def get_Emergency_patient_details_for_Quelist(request):
    try:
        query = request.GET.get('query', '')
        status = request.GET.get('status', '')
        print(status,'statussssssssssssss')
        DoctorId = request.GET.get('DoctorId', '')

        # Map status to Booking_Status
        Booking_Status = 'Occupied' if status == 'Admitted' else 'Completed'
        
       
        queryset = Patient_Emergency_Registration_Detials.objects.all()
        
        print(queryset,'queryset')
        # Apply filters based on the query parameters
        if query:
            queryset = queryset.filter(
                Q(PatientId_FirstName_icontains=query) |
                Q(PatientId_MiddleName_icontains=query) |
                Q(PatientId_SurName_icontains=query) |
                Q(PatientId_PatientId_icontains=query) |
                Q(PatientId_PhoneNo_icontains=query)
            ).filter(Booking_Status=Booking_Status)
        
        if DoctorId:
            queryset = queryset.filter(PrimaryDoctor__pk = DoctorId)
        

        if status:
            queryset = queryset.filter(Q(Status__icontains=status)).filter(Booking_Status=Booking_Status)
        
        
        # Serialize the filtered queryset
        Emg_register_data = []
        for idx, register in enumerate(queryset, start=1):
            # client_name = register.ClientName.Client_Name if register.ClientName else None
            # insurance_name = register.InsuranceName.Insurance_Name if register.InsuranceName else None
            # Flagging_name = register.Flagging.Flagg_Name if register.Flagging else None
            # Flagging_color = register.Flagging.Flagg_Color if register.Flagging else None
            # BloodGroup_name = register.PatientId.BloodGroup.BloodGroup_Id if register.PatientId.BloodGroup else None
            
            appointment_dict = {
                'id': idx,
                # 'PatientProfile': get_file_image(register.PatientId.Patient_profile) if register.PatientId.Patient_profile else None,
                'RegistrationId': register.Registration_Id,
                'PatientId': register.PatientId.PatientId if register.PatientId else None,
                'PatientName': f"{register.PatientId.Title.Title_Name if register.PatientId.Title else None}.{register.PatientId.FirstName} {register.PatientId.MiddleName} {register.PatientId.SurName}" if register.PatientId else None,
                'PhoneNo': register.PatientId.PhoneNo if register.PatientId else None,
                'Age': register.PatientId.Age if register.PatientId else None,
                'Gender': register.PatientId.Gender if register.PatientId else None,
                'UHIDNO' : register.PatientId.UniqueIdNo if register.PatientId else None,
                # 'BloodGroup': BloodGroup_name,
                'Complaint': register.Complaint,
                'isMLC': register.IsMLC,
                # 'Flagging': Flagging_name,
                # 'FlaggingColour': Flagging_color,
                # 'Flagging': register.Flagging,
                'isRefferal': register.IsReferral,
                # 'ClientName': client_name,  # Fixed reference
                # 'InsuranceName': insurance_name,  # Fixed reference
                'Status': register.Status,
                'DoctorName': f"{register.PrimaryDoctor.Tittle.Title_Name}.{register.PrimaryDoctor.First_Name} {register.PrimaryDoctor.Last_Name}" if register.PrimaryDoctor else None,
                'Specilization': str(register.Specialization.Speciality_Name) if register.Specialization else None,
            }

            if register.Booking_Status in 'Occupied':
                roomdetials = Patient_Admission_Room_Detials.objects.filter(Emergency_Registration_Id=register).order_by('-created_by').first()

                if roomdetials:
                    appointment_dict['BuildingName'] = roomdetials.RoomId.Building_Name.Building_Name if roomdetials.RoomId.Building_Name else None
                    appointment_dict['BlockName'] = roomdetials.RoomId.Block_Name.Block_Name if roomdetials.RoomId.Block_Name else None
                    appointment_dict['FloorName'] = roomdetials.RoomId.Floor_Name.Floor_Name if roomdetials.RoomId.Floor_Name else None
                    appointment_dict['WardName'] = roomdetials.RoomId.Ward_Name.Ward_Name.Ward_Name if roomdetials.RoomId.Ward_Name else None
                    # appointment_dict['RoomName'] = roomdetials.RoomId.Room_Name.Room_Name if roomdetials.RoomId.Room_Name else None
                    appointment_dict['RoomNo'] = roomdetials.RoomId.Room_No if roomdetials.RoomId.Room_No else None
                    appointment_dict['BedNo'] = roomdetials.RoomId.Bed_No if roomdetials.RoomId.Bed_No else None
                    appointment_dict['RoomId'] = roomdetials.RoomId.Room_Id if roomdetials.RoomId.Room_Id else None

            Emg_register_data.append(appointment_dict)

        return JsonResponse(Emg_register_data, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)})


# @csrf_exempt
# @require_http_methods(["GET"])
# def get_Emergency_patient_list(request):
#     try:
#         query = request.GET.get('query', '')
#         status = request.GET.get('status', '')
#         SavedStatus = request.GET.get('SavedStatus', '')
#         DoctorId = request.GET.get('DoctorId', '')

#         # Map status to Booking_Status
#         Booking_Status = 'Occupied' if status == 'Admitted' else 'Completed'
        
       
#         queryset = Patient_Emergency_Registration_Detials.objects.all()
        
#         print(queryset,'queryset')
#         # Apply filters based on the query parameters
#         if query:
#             queryset = queryset.filter(
#                 Q(PatientId_FirstName_icontains=query) |
#                 Q(PatientId_MiddleName_icontains=query) |
#                 Q(PatientId_SurName_icontains=query) |
#                 Q(PatientId_PatientId_icontains=query) |
#                 Q(PatientId_PhoneNo_icontains=query)
#             ).filter(Booking_Status=Booking_Status)
        
#         if DoctorId:
#             queryset = queryset.filter(PrimaryDoctor__pk = DoctorId)
        

#         if status:
#             queryset = queryset.filter(Q(Status__icontains=status)).filter(Booking_Status=Booking_Status)
        
#         if SavedStatus:
#             queryset = queryset.filter(Q(SavedStatus__icontains=SavedStatus))
#         else:
#             queryset = queryset.exclude(SavedStatus='Registered')

#         # Serialize the filtered queryset
#         Emg_register_data = []
#         for idx, register in enumerate(queryset, start=1):
#             # client_name = register.ClientName.Client_Name if register.ClientName else None
#             # insurance_name = register.InsuranceName.Insurance_Name if register.InsuranceName else None
#             # Flagging_name = register.Flagging.Flagg_Name if register.Flagging else None
#             # Flagging_color = register.Flagging.Flagg_Color if register.Flagging else None
#             # BloodGroup_name = register.PatientId.BloodGroup.BloodGroup_Id if register.PatientId.BloodGroup else None
            
#             appointment_dict = {
#                 'id': idx,
#                 # 'PatientProfile': get_file_image(register.PatientId.Patient_profile) if register.PatientId.Patient_profile else None,
#                 'RegistrationId': register.Registration_Id,
#                 'PatientId': register.PatientId.PatientId if register.PatientId else None,
#                 'PatientName': f"{register.PatientId.Title.Title_Name if register.PatientId.Title else None}.{register.PatientId.FirstName} {register.PatientId.MiddleName} {register.PatientId.SurName}" if register.PatientId else None,
#                 'PhoneNo': register.PatientId.PhoneNo if register.PatientId else None,
#                 'Age': register.PatientId.Age if register.PatientId else None,
#                 'Gender': register.PatientId.Gender if register.PatientId else None,
#                 # 'BloodGroup': BloodGroup_name,
#                 'Complaint': register.Complaint,
#                 'isMLC': register.IsMLC,
#                 # 'Flagging': Flagging_name,
#                 # 'FlaggingColour': Flagging_color,
#                 # 'Flagging': register.Flagging,
#                 'isRefferal': register.IsReferral,
#                 # 'ClientName': client_name,  # Fixed reference
#                 # 'InsuranceName': insurance_name,  # Fixed reference
#                 'Status': register.Status,
#                 'DoctorName': f"{register.PrimaryDoctor.Tittle.Title_Name}.{register.PrimaryDoctor.First_Name} {register.PrimaryDoctor.Last_Name}" if register.PrimaryDoctor else None,
#                 'Specilization': str(register.Specialization.Speciality_Name) if register.Specialization else None,
#             }

#             # if register.Booking_Status in 'Occupied':
#             #     roomdetials = Patient_Admission_Room_Detials.objects.filter(Emergency_Registration_Id=register).order_by('-created_by').first()

#             #     if roomdetials:
#             #         appointment_dict['BuildingName'] = roomdetials.RoomId.Building_Name.Building_Name if roomdetials.RoomId.Building_Name else None
#             #         appointment_dict['BlockName'] = roomdetials.RoomId.Block_Name.Block_Name if roomdetials.RoomId.Block_Name else None
#             #         appointment_dict['FloorName'] = roomdetials.RoomId.Floor_Name.Floor_Name if roomdetials.RoomId.Floor_Name else None
#             #         appointment_dict['WardName'] = roomdetials.RoomId.Ward_Name.Ward_Name.Ward_Name if roomdetials.RoomId.Ward_Name else None
#             #         # appointment_dict['RoomName'] = roomdetials.RoomId.Room_Name.Room_Name if roomdetials.RoomId.Room_Name else None
#             #         appointment_dict['RoomNo'] = roomdetials.RoomId.Room_No if roomdetials.RoomId.Room_No else None
#             #         appointment_dict['BedNo'] = roomdetials.RoomId.Bed_No if roomdetials.RoomId.Bed_No else None
#             #         appointment_dict['RoomId'] = roomdetials.RoomId.Room_Id if roomdetials.RoomId.Room_Id else None

#             Emg_register_data.append(appointment_dict)

#         return JsonResponse(Emg_register_data, safe=False)

#     except Exception as e:
#         return JsonResponse({'error': str(e)})


@csrf_exempt #---show grid in the Emergency register page
@require_http_methods(["GET"])
def get_Emergency_patient_list(request):  
    try:
        
        status = request.GET.get('status', '')
        

        queryset = Patient_Emergency_Registration_Detials.objects.all()
        
        print(queryset,'queryset')
        
        if status:
            queryset = queryset.filter(PatientId__Status__iexact=status)  # Match 'Saved' exactly, case-insensitive

        Emg_register_data = []
        for idx, register in enumerate(queryset, start=1):
              
            appointment_dict = {
                'id': idx,
                # 'PatientProfile': get_file_image(register.PatientId.Patient_profile) if register.PatientId.Patient_profile else None,
                'RegistrationId': register.Registration_Id,
                'PatientId': register.PatientId.PatientId if register.PatientId else None,
                'PatientName': f"{register.PatientId.Title.Title_Name if register.PatientId.Title else None}.{register.PatientId.FirstName} {register.PatientId.MiddleName} {register.PatientId.SurName}" if register.PatientId else None,
                'PhoneNo': register.PatientId.PhoneNo if register.PatientId else None,
                'Age': register.PatientId.Age if register.PatientId else None,
                'Gender': register.PatientId.Gender if register.PatientId else None,
                # 'BloodGroup': BloodGroup_name,
                'Complaint': register.Complaint,
                'isMLC': register.IsMLC,
                # 'Flagging': Flagging_name,
                # 'FlaggingColour': Flagging_color,
                # 'Flagging': register.Flagging,
                'isRefferal': register.IsReferral,
                # 'ClientName': client_name,  # Fixed reference
                # 'InsuranceName': insurance_name,  # Fixed reference
                'Status': register.Status,
                'DoctorName': f"{register.PrimaryDoctor.Tittle.Title_Name}.{register.PrimaryDoctor.First_Name} {register.PrimaryDoctor.Last_Name}" if register.PrimaryDoctor else None,
                'Specilization': str(register.Specialization.Speciality_Name) if register.Specialization else None,
            }

           
            Emg_register_data.append(appointment_dict)

        return JsonResponse(Emg_register_data, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)})



# @csrf_exempt
# @require_http_methods(["GET"])
# def get_Emergency_Registration_edit_details(request):
#     try:
#         RegistrationId = request.GET.get('RegistrationId', None)
#         # RegistrationType = request.GET.get('RegistrationType', None)
#         Emergency_Patient = Patient_Emergency_Registration_Detials.objects.get(pk = RegistrationId)
#         admission_instance = Patient_Admission_Detials.objects.get(Emergency_Registration_Id__pk = RegistrationId)
#         admission_room_instance = Patient_Admission_Room_Detials.objects.get(Emergency_Registration_Id__pk = RegistrationId)
#         # referral_instance = Patient_Referral_Detials.objects.get(IP_Register_Id__pk = RegistrationId)
        
#         # print(referral_instance,'referral_instance')
#         print(admission_instance,'admission_instance')
#         print(admission_instance.AdmissionPurpose,'admission_instance.AdmissionPurpose')
#         Registration_dict = {
#             'Title': Emergency_Patient.PatientId.Title.Title_Id if Emergency_Patient.PatientId else "",
#             'PatientId': Emergency_Patient.PatientId.PatientId if Emergency_Patient.PatientId else "",
#             'FirstName': Emergency_Patient.PatientId.FirstName if Emergency_Patient.PatientId else "",
#             'MiddleName': Emergency_Patient.PatientId.MiddleName if Emergency_Patient.PatientId else "",
#             'SurName': Emergency_Patient.PatientId.SurName if Emergency_Patient.PatientId else "",
#             'Gender': Emergency_Patient.PatientId.Gender if Emergency_Patient.PatientId else "",
#             'MaritalStatus': Emergency_Patient.PatientId.MaritalStatus if Emergency_Patient.PatientId else "",
#             'SpouseName': Emergency_Patient.PatientId.SpouseName if Emergency_Patient.PatientId else "",
#             'FatherName': Emergency_Patient.PatientId.FatherName if Emergency_Patient.PatientId else "",
#             'DOB': Emergency_Patient.PatientId.DOB if Emergency_Patient.PatientId else "",
#             'Age': Emergency_Patient.PatientId.Age if Emergency_Patient.PatientId else "",
#             'PhoneNo': Emergency_Patient.PatientId.PhoneNo if Emergency_Patient.PatientId else "",
#             'Email': Emergency_Patient.PatientId.Email if Emergency_Patient.PatientId else "",
#             'BloodGroup': Emergency_Patient.PatientId.BloodGroup.BloodGroup_Id if Emergency_Patient.PatientId else "",
#             'Occupation': Emergency_Patient.PatientId.Occupation if Emergency_Patient.PatientId else "",
#             'Religion': Emergency_Patient.PatientId.Religion.Religion_Id if Emergency_Patient.PatientId else "",
#             'ReligionName': Emergency_Patient.PatientId.Religion.Religion_Name if Emergency_Patient.PatientId else "",
#             'Nationality': Emergency_Patient.PatientId.Nationality if Emergency_Patient.PatientId else "",
#             'UniqueIdType': Emergency_Patient.PatientId.UniqueIdType if Emergency_Patient.PatientId else "",
#             'UniqueIdNo': Emergency_Patient.PatientId.UniqueIdNo if Emergency_Patient.PatientId else "",
#             'PatientType': Emergency_Patient.PatientId.PatientType if Emergency_Patient.PatientId else "",
#             'DoorNo': Emergency_Patient.PatientId.DoorNo if Emergency_Patient.PatientId else "",
#             'Street': Emergency_Patient.PatientId.Street if Emergency_Patient.PatientId else "",
#             'Area': Emergency_Patient.PatientId.Area if Emergency_Patient.PatientId else "",
#             'City': Emergency_Patient.PatientId.City if Emergency_Patient.PatientId else "",
#             'State': Emergency_Patient.PatientId.State if Emergency_Patient.PatientId else "",
#             'Country': Emergency_Patient.PatientId.Country if Emergency_Patient.PatientId else "",
#             'Pincode': Emergency_Patient.PatientId.Pincode if Emergency_Patient.PatientId else "",
#             'ABHA': Emergency_Patient.PatientId.ABHA if Emergency_Patient.PatientId else "",
           
#             'Speciality': Emergency_Patient.Specialization.pk if Emergency_Patient.Specialization else None,
#             # 'DoctorName': Emergency_Patient.PrimaryDoctor.Doctor_ID if Emergency_Patient.PrimaryDoctor else "",
#             'DoctorName': f"{Emergency_Patient.PrimaryDoctor.Tittle.Title_Name}.{Emergency_Patient.PrimaryDoctor.ShortName}",
#             'PrimaryDoctor': Emergency_Patient.PrimaryDoctor.pk,
            
#             'Complaint': Emergency_Patient.Complaint,
#             'IsMLC': Emergency_Patient.IsMLC,
#             'IsReferral': Emergency_Patient.IsReferral,
#             'PatientCategory': Emergency_Patient.PatientCategory,
#             'InsuranceName': Emergency_Patient.InsuranceName.Insurance_Id if Emergency_Patient.InsuranceName else None,
#             'InsuranceType': Emergency_Patient.InsuranceType,
#             'ClientName': Emergency_Patient.ClientName.Client_Id if Emergency_Patient.ClientName else None,
#             'ClientType': Emergency_Patient.ClientType,
#             'ClientEmployeeId': Emergency_Patient.ClientEmployeeId,
#             'ClientEmployeeDesignation': Emergency_Patient.ClientEmployeeDesignation,
#             'ClientEmployeeRelation': Emergency_Patient.ClientEmployeeRelation,

#             'CorporateName': Emergency_Patient.CorporateName.Corporate_Id if Emergency_Patient.CorporateName else None,
#             'CorporateType': Emergency_Patient.CorporateType,
#             'CorporateEmployeeId': Emergency_Patient.CorporateEmployeeId,
#             'CorporateEmployeeDesignation': Emergency_Patient.CorporateEmployeeDesignation,
#             'CorporateEmployeeRelation': Emergency_Patient.CorporateEmployeeRelation,
#             'EmployeeId': Emergency_Patient.EmployeeId.Employee_ID if Emergency_Patient.EmployeeId else "",
#             'EmployeeRelation': Emergency_Patient.EmployeeRelation,
            
#             'DoctorId': Emergency_Patient.DoctorId.Doctor_ID if Emergency_Patient.PatientCategory == 'Doctor'and Emergency_Patient.DoctorId else "",
#             'DoctorRelation': Emergency_Patient.DoctorRelation,
#             'DonationType': Emergency_Patient.DonationType.Donation_Id if Emergency_Patient.DonationType else None,

#             'AdmissionPurpose': admission_instance.AdmissionPurpose if admission_instance else '' ,
#             'DrInchargeAtTimeOfAdmission': admission_instance.DrInchargeAtTimeOfAdmission.Doctor_ID if admission_instance and admission_instance.DrInchargeAtTimeOfAdmission else '' ,
#             'NextToKinName': admission_instance.NextToKinName if admission_instance else '',
#             'Relation': admission_instance.Relation if admission_instance else '',
#             'RelativePhoneNo': admission_instance.RelativePhoneNo if admission_instance else '',
#             'PersonLiableForBillPayment': admission_instance.PersonLiableForPayment if admission_instance else '',
            
#             'FamilyHead': admission_instance.FamilyHead if admission_instance else '',
#             'FamilyHeadName': admission_instance.FamilyHeadName if admission_instance else '',
            
#             'IpKitGiven': admission_instance.IpKitGiven if admission_instance else '',
           
           
#             'IsReferal': Emergency_Patient.IsReferral,
#             # 'ReferralSource': referral_instance.ReferralSource if referral_instance else None,
#             # 'ReferredBy': referral_instance.ReferredBy.Doctor_ID if referral_instance.ReferredBy else None,
             

#             'Building': admission_room_instance.RoomId.Building_Name.pk if admission_room_instance else "" ,
#             'Block': admission_room_instance.RoomId.Block_Name.pk  if admission_room_instance else "", 
#             'Floor': admission_room_instance.RoomId.Floor_Name.pk  if admission_room_instance else "", 
#             'WardType': admission_room_instance.RoomId.Ward_Name.Ward_Name.pk  if admission_room_instance else "", 
#             'RoomNo': admission_room_instance.RoomId.Room_No  if admission_room_instance else "", 
#             'BedNo': admission_room_instance.RoomId.Bed_No  if admission_room_instance else "", 
           
#             'BuildingName': admission_room_instance.RoomId.Building_Name.Building_Name if admission_room_instance else "" ,
#             'BlockName': admission_room_instance.RoomId.Block_Name.Block_Name  if admission_room_instance else "", 
#             'FloorName': admission_room_instance.RoomId.Floor_Name.Floor_Name  if admission_room_instance else "", 
#             'WardTypeName': admission_room_instance.RoomId.Ward_Name.Ward_Name.Ward_Name  if admission_room_instance else "", 
#             'RoomId': admission_room_instance.RoomId.pk if admission_room_instance else "",  
       
              
#         }
#         print(Registration_dict,'Registration_dict')
        
            
#         return JsonResponse(Registration_dict,safe=False)
    
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_Emergency_Registration_edit_details(request):
    try:
        RegistrationId = request.GET.get('RegistrationId', None)
        print(RegistrationId, 'RegistrationIdddddddd11111111111')

        # Fetch the Emergency Patient record
        Emergency_Patient = Patient_Emergency_Registration_Detials.objects.get(pk=RegistrationId)
        
        # Attempt to fetch the associated admission record (if any)
        admission_instance = Patient_Admission_Detials.objects.filter(Emergency_Registration_Id__Registration_Id=RegistrationId).first()
        referral_details = None

        # Check for referral details by OP, IP, and Emergency Register IDs
        try:
            referral_details = Patient_Referral_Detials.objects.filter(
                OP_Register_Id__Registration_Id=RegistrationId
            ).first() or Patient_Referral_Detials.objects.filter(
                IP_Register_Id__Registration_Id=RegistrationId
            ).first() or Patient_Referral_Detials.objects.filter(
                Emergency_Register_Id__Registration_Id=RegistrationId
            ).first()
        except Patient_Referral_Detials.DoesNotExist:
            referral_details = None

        # Check if admission_instance exists
        if admission_instance is None:
            print(f"No admission record found for RegistrationId: {RegistrationId}")
            admission_instance = {}  # Return an empty dictionary if no admission found
        
        print(admission_instance, 'admission_instance')

        # Create the registration dictionary
        Registration_dict = {
            'Title': Emergency_Patient.PatientId.Title.Title_Id if Emergency_Patient.PatientId.Title else '',
            'PatientId': Emergency_Patient.PatientId.PatientId if Emergency_Patient.PatientId else "",
            'FirstName': Emergency_Patient.PatientId.FirstName if Emergency_Patient.PatientId else "",
            'MiddleName': Emergency_Patient.PatientId.MiddleName if Emergency_Patient.PatientId else "",
            'SurName': Emergency_Patient.PatientId.SurName if Emergency_Patient.PatientId else "",
            'Gender': Emergency_Patient.PatientId.Gender if Emergency_Patient.PatientId else "",
            'MaritalStatus': Emergency_Patient.PatientId.MaritalStatus if Emergency_Patient.PatientId else "",
            'SpouseName': Emergency_Patient.PatientId.SpouseName if Emergency_Patient.PatientId else "",
            'FatherName': Emergency_Patient.PatientId.FatherName if Emergency_Patient.PatientId else "",
            'DOB': Emergency_Patient.PatientId.DOB if Emergency_Patient.PatientId else "",
            'Age': Emergency_Patient.PatientId.Age if Emergency_Patient.PatientId else "",
            'PhoneNo': Emergency_Patient.PatientId.PhoneNo if Emergency_Patient.PatientId else "",
            'Email': Emergency_Patient.PatientId.Email if Emergency_Patient.PatientId else "",
            'BloodGroup': Emergency_Patient.PatientId.BloodGroup.BloodGroup_Id if Emergency_Patient.PatientId.BloodGroup else "",
            'Occupation': Emergency_Patient.PatientId.Occupation if Emergency_Patient.PatientId else "",
            'Religion': Emergency_Patient.PatientId.Religion.Religion_Id if Emergency_Patient.PatientId.Religion else None,
            'ReligionName': Emergency_Patient.PatientId.Religion.Religion_Name if Emergency_Patient.PatientId.Religion else None,
            'Nationality': Emergency_Patient.PatientId.Nationality if Emergency_Patient.PatientId else "",
            'UniqueIdType': Emergency_Patient.PatientId.UniqueIdType if Emergency_Patient.PatientId else "",
            'UniqueIdNo': Emergency_Patient.PatientId.UniqueIdNo if Emergency_Patient.PatientId else "",
            'PatientType': Emergency_Patient.PatientId.PatientType if Emergency_Patient.PatientId else "",
            'DoorNo': Emergency_Patient.PatientId.DoorNo if Emergency_Patient.PatientId else "",
            'Street': Emergency_Patient.PatientId.Street if Emergency_Patient.PatientId else "",
            'Area': Emergency_Patient.PatientId.Area if Emergency_Patient.PatientId else "",
            'City': Emergency_Patient.PatientId.City if Emergency_Patient.PatientId else "",
            'State': Emergency_Patient.PatientId.State if Emergency_Patient.PatientId else "",
            'Country': Emergency_Patient.PatientId.Country if Emergency_Patient.PatientId else "",
            'Pincode': Emergency_Patient.PatientId.Pincode if Emergency_Patient.PatientId else "",
            'ABHA': Emergency_Patient.PatientId.ABHA if Emergency_Patient.PatientId else "",
            'RegistrationId': Emergency_Patient.pk,
            'Speciality': Emergency_Patient.Specialization.pk if Emergency_Patient.Specialization else None,
            'PrimaryDoctor': Emergency_Patient.PrimaryDoctor.pk if Emergency_Patient.PrimaryDoctor else None,
            'DoctorName': (
                f"{Emergency_Patient.PrimaryDoctor.Tittle.Title_Name if Emergency_Patient.PrimaryDoctor and Emergency_Patient.PrimaryDoctor.Tittle else ''}."
                f"{Emergency_Patient.PrimaryDoctor.ShortName if Emergency_Patient.PrimaryDoctor else ''}"),
            'Complaint': Emergency_Patient.Complaint,
            'IsMLC': Emergency_Patient.IsMLC,
            'IsReferral': Emergency_Patient.IsReferral,
            'PatientCategory': Emergency_Patient.PatientCategory,
            'InsuranceName': Emergency_Patient.InsuranceName.Insurance_Id if Emergency_Patient.InsuranceName else None,
            'InsuranceType': Emergency_Patient.InsuranceType,
            'ClientName': Emergency_Patient.ClientName.Client_Id if Emergency_Patient.ClientName else None,
            'ClientType': Emergency_Patient.ClientType,
            'ClientEmployeeId': Emergency_Patient.ClientEmployeeId,
            'ClientEmployeeDesignation': Emergency_Patient.ClientEmployeeDesignation,
            'ClientEmployeeRelation': Emergency_Patient.ClientEmployeeRelation,
            'CorporateName': Emergency_Patient.CorporateName.Corporate_Id if Emergency_Patient.CorporateName else None,
            'CorporateType': Emergency_Patient.CorporateType,
            'CorporateEmployeeId': Emergency_Patient.CorporateEmployeeId,
            'CorporateEmployeeDesignation': Emergency_Patient.CorporateEmployeeDesignation,
            'CorporateEmployeeRelation': Emergency_Patient.CorporateEmployeeRelation,
            'EmployeeId': Emergency_Patient.EmployeeId.Employee_ID if Emergency_Patient.EmployeeId else "",
            'EmployeeRelation': Emergency_Patient.EmployeeRelation,
            'DoctorId': Emergency_Patient.DoctorId.pk if Emergency_Patient.DoctorId else "",
            'DoctorRelation': Emergency_Patient.DoctorRelation,
            'DonationType': Emergency_Patient.DonationType.Donation_Id if Emergency_Patient.DonationType else None,
            'AdmissionPurpose': admission_instance.AdmissionPurpose if admission_instance else '',
            'DrInchargeAtTimeOfAdmission': admission_instance.DrInchargeAtTimeOfAdmission.Doctor_ID if admission_instance and admission_instance.DrInchargeAtTimeOfAdmission else '',
            'NextToKinName': admission_instance.NextToKinName if admission_instance else '',
            'Relation': admission_instance.Relation if admission_instance else '',
            'RelativePhoneNo': admission_instance.RelativePhoneNo if admission_instance else '',
            'PersonLiableForBillPayment': admission_instance.PersonLiableForPayment if admission_instance else '',
            'FamilyHead': admission_instance.FamilyHead if admission_instance else '',
            'FamilyHeadName': admission_instance.FamilyHeadName if admission_instance else '',
            'IpKitGiven': admission_instance.IpKitGiven if admission_instance else '',
            'IsReferal': Emergency_Patient.IsReferral,
        }

        if referral_details:
            Registration_dict.update({
                'ReferralSource': referral_details.ReferralSource,
                'ReferredBy': f"{referral_details.ReferredBy.Tittle.Title_Name}.{referral_details.ReferredBy.First_Name} {referral_details.ReferredBy.Last_Name}" if referral_details.ReferredBy else None,
            })

        print(Registration_dict, 'Registration_dict')

        return JsonResponse(Registration_dict, safe=False)
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)




@csrf_exempt
@require_http_methods(["GET"])
def Patients_Management_Filter(request):
    try:
        search_query = request.GET.get('search', '')
        gender = request.GET.get('gender', '')  
        from_date = request.GET.get('fromDate', '')  
        to_date = request.GET.get('toDate', '')  
        particular_date = request.GET.get('ParticularDate', '')
        Current_date = request.GET.get('CurrentDate', '')

        queryset = Patient_Detials.objects.all()

        # Search query filter
        if search_query:
            queryset = queryset.filter(
                Q(FirstName__icontains=search_query) |
                Q(MiddleName__icontains=search_query) |
                Q(SurName__icontains=search_query) |
                Q(PatientId__icontains=search_query) |
                Q(PhoneNo__icontains=search_query) |
                Q(UniqueIdNo__icontains=search_query)
            )
        
        # Gender filter
        if gender:
            queryset = queryset.filter(Gender__iexact=gender)  

        # Custom date range filter
        if from_date and to_date:
            queryset = queryset.filter(created_at__date__range=[from_date, to_date])

        # Particular date filter
        elif particular_date:
            queryset = queryset.filter(created_at__date=particular_date)
        
        # Current Date filter (Ensure it's a valid date)
        elif Current_date and Current_date != "":  
            queryset = queryset.filter(created_at__date=Current_date)

        # Prepare response data
        patient_data = [
            {
                'id': idx,
                'PatientId': patient.PatientId,
                'PhoneNo': int(patient.PhoneNo) if patient.PhoneNo else None,
                'FirstName': patient.FirstName,
                'MiddleName': patient.MiddleName,
                'SurName': patient.SurName,
                'FullName': f'{patient.FirstName} {patient.MiddleName} {patient.SurName}',
                'Gender': patient.Gender,
                'Email': patient.Email,
                'date': patient.created_at.strftime('%Y-%m-%d'),
                'CurrDate': patient.created_at.strftime('%d-%m-%y'),
                'CurrTime': patient.created_at.strftime('%H:%M:%S'),
            
            } for idx, patient in enumerate(queryset, start=1)
        ]

        return JsonResponse(patient_data, safe=False)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'An internal server error occurred'}, status=500)




@csrf_exempt
@require_http_methods(["GET"])
def Register_Patients_Details(request):
    try:
        # Get the 'status' parameter from the request
        status = request.GET.get('status', '')

        # Filter patients based on the 'status' parameter
        queryset = Patient_Detials.objects.all()
        if status:
            queryset = queryset.filter(Status__iexact=status)  # Match 'Saved' exactly, case-insensitive

        # Prepare patient data for the response
        patient_data = [
            {
                'id': idx,
                'PatientId': patient.PatientId,
                'Title': patient.Title.Title_Id if patient.Title else None,
                'PhoneNo': int(patient.PhoneNo) if patient.PhoneNo else None,
                'FirstName': patient.FirstName,
                'MiddleName': patient.MiddleName,
                'SurName': patient.SurName,
                'FullName': f'{patient.FirstName} {patient.MiddleName} {patient.SurName}',
                'Gender': patient.Gender,
                'MaritalStatus': patient.MaritalStatus,
                'SpouseName': patient.SpouseName,
                'FatherName': patient.FatherName,
                'DOB': patient.DOB,
                'Age': patient.Age,
                'BloodGroup': patient.BloodGroup.BloodGroup_Name if patient.BloodGroup else None,
                'Occupation': patient.Occupation,
                'Religion': patient.Religion.Religion_Name if patient.Religion else None,
                'Nationality': patient.Nationality,
                'UHIDType': patient.UniqueIdType,
                'UHIDNo': patient.UniqueIdNo,
                'PatientType': patient.PatientType,
                'Pincode': patient.Pincode,
                'DoorNo': patient.DoorNo,
                'Street': patient.Street,
                'Area': patient.Area,
                'City': patient.City,
                'District': patient.District,
                'State': patient.State,
                'Country': patient.Country,
                'ABHA': patient.ABHA,
                'Email': patient.Email,
                'Status': patient.Status,
                'DoctorID': patient.DoctorID.Doctor_ID if patient.DoctorID else None,
                'SpecializationId': patient.SpecializationId.Speciality_Id if patient.SpecializationId else None,
               
                'date': patient.created_at.strftime('%Y-%m-%d'),
                'CurrDate': patient.created_at.strftime('%d-%m-%y'),
                'CurrTime': patient.created_at.strftime('%H:%M:%S'),
            }
            for idx, patient in enumerate(queryset, start=1)
        ]

        return JsonResponse(patient_data, safe=False)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'An internal server error occurred'}, status=500)







@csrf_exempt
@require_http_methods(["GET"])
def Fetch_Register_Patients_Details(request):
    try:
        # Get the PatientId from the query parameters
        patient_id = request.GET.get('PatientId')

        if not patient_id:
            return JsonResponse({'error': 'PatientId parameter is required'}, status=400)

        # Fetch the patient details based on the provided PatientId
        patient = Patient_Detials.objects.filter(PatientId=patient_id).first()

        if not patient:
            return JsonResponse({'error': 'Patient not found'}, status=404)
        
        # idx = 1
        # Prepare patient data for the response
        patient_data = {
            # 'id': idx,
            'PatientId': patient.PatientId,
            'Title': patient.Title.Title_Id if patient.Title else None,
            'PhoneNo': int(patient.PhoneNo) if patient.PhoneNo else None,
            'FirstName': patient.FirstName,
            'MiddleName': patient.MiddleName,
            'SurName': patient.SurName,
            'FullName': f'{patient.FirstName} {patient.MiddleName} {patient.SurName}',
            'Gender': patient.Gender,
            'MaritalStatus': patient.MaritalStatus,
            'SpouseName': patient.SpouseName,
            'FatherName': patient.FatherName,
            'DOB': patient.DOB,
            'Age': patient.Age,
            'BloodGroup': patient.BloodGroup.BloodGroup_Id if patient.BloodGroup else None,
            'Occupation': patient.Occupation,
            'Religion': patient.Religion.Religion_Id if patient.Religion else None,
            'Nationality': patient.Nationality,
            'UHIDType': patient.UniqueIdType,
            'UHIDNo': patient.UniqueIdNo,
            'PatientType': patient.PatientType,
            'PermanentPincode': patient.PermanentPincode,
            'PermanentdoorNo': patient.PermanentdoorNo,
            'PermanentStreet': patient.PermanentStreet,
            'PermanentArea': patient.PermanentArea,
            'PermanentCity': patient.PermanentCity,
            'PermanentDistrict': patient.PermanentDistrict,
            'PermanentState': patient.PermanentState,
            'PermanentCountry': patient.PermanentCountry,
            'Pincode': patient.Pincode,
            'DoorNo': patient.DoorNo,
            'Street': patient.Street,
            'Area': patient.Area,
            'City': patient.City,
            'District': patient.District,
            'State': patient.State,
            'Country': patient.Country,
            'ABHA': patient.ABHA,
            'Email': patient.Email,
            'DoctorID': patient.DoctorID.Doctor_ID if patient.DoctorID else None,
            'referdoctorid': patient.ReferredBy.Doctor_ID if patient.ReferredBy else None,
            'SpecializationId': patient.SpecializationId.Speciality_Id if patient.SpecializationId else None,
            'date': patient.created_at.strftime('%Y-%m-%d'),
            'CurrDate': patient.created_at.strftime('%d-%m-%y'),
            'CurrTime': patient.created_at.strftime('%H:%M:%S'),
        }
        # idx+=1

        return JsonResponse(patient_data, safe=False)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'An internal server error occurred'}, status=500)

# @csrf_exempt
# @require_http_methods(['GET'])
# def Patient_Master_List(request):
#     if request.method == 'GET':
#         try:
#             patient_id = request.GET.get('PatientId')
#             # Ensure patient_id is provided
#             if not patient_id:
#                 return JsonResponse({'error': 'PatientId is required'}, status=400)

#             # Retrieve the patient details
#             patient_data = Patient_Detials.objects.get(pk=patient_id)
#             OP_patient_data = Patient_Appointment_Registration_Detials.objects.filter(PatientId__PatientId=patient_id)
#             IP_patient_data = Patient_IP_Registration_Detials.objects.filter(PatientId__PatientId=patient_id)
#             Casuality_patient_data = Patient_Casuality_Registration_Detials.objects.filter(PatientId__PatientId=patient_id)
#             Diagnosis_patient_data = Patient_Diagnosis_Registration_Detials.objects.filter(PatientId__PatientId=patient_id)
#             Laboratory_patient_data = Patient_Laboratory_Registration_Detials.objects.filter(PatientId__PatientId=patient_id)
             
#             print(IP_patient_data,'eeeeeeeeeeeeeeeeee') 
#             patient_detailsList=[]
#             for patient in  patient_data:
#             # Prepare the response data
#                 patient_dict = {
#                     'PatientId': patient.PatientId,
#                     'PhoneNo': patient.PhoneNo,
#                     'Title': patient.Title,
#                     'FirstName': patient.FirstName,
#                     'MiddleName': patient.MiddleName,
#                     'SurName': patient.SurName,
#                     'Gender': patient.Gender,
#                     'MaritalStatus': patient.MaritalStatus,
#                     'SpouseName': patient.SpouseName,
#                     'FatherName': patient.FatherName,
#                     'AliasName': patient.AliasName,
#                     'DOB': patient.DOB,
#                     'Age': patient.Age,
#                     'Email': patient.Email,
#                     'BloodGroup': patient.BloodGroup.pk if patient.BloodGroup else None,
#                     'Occupation': patient.Occupation,
#                     'Religion': patient.Religion.pk if patient.Religion else None,  # Assuming Religion has a Name field
#                     'Nationality': patient.Nationality,
#                     'UniqueIdType': patient.UniqueIdType,
#                     'UniqueIdNo': patient.UniqueIdNo,
#                     'DoorNo': patient.DoorNo,
#                     'Street': patient.Street,
#                     'Area': patient.Area,
#                     'City': patient.City,
#                     'District': patient.District,
#                     'State': patient.State,
#                     'Country': patient.Country,
#                     'Pincode': patient.Pincode,
#                     'Createdby': patient.created_by,
#                     'CurrDate': patient.created_at.strftime('%d-%m-%y'),
#                     'CurrTime': patient.created_at.strftime('%H:%M:%S'),
#                     'OP_details':[],
#                     'IP_details':[],
#                     'Casuality_details':[],
#                     'Diagnosis_details':[],
#                     'Laboratory_details':[],
#                 }
#                 for  patientBasic in  OP_patient_data:
#                     patient_dict['OP_details'].append({
#                         'OP_Patient' : 1,
#                         'PatientId':patientBasic.PatientId.pk,
#                         'PatientType':patientBasic.PatientType,
#                         'PatientCategory':patientBasic.PatientCategory,
#                         'InsuranceName':patientBasic.InsuranceName.pk if patientBasic.InsuranceName else None,
#                         'InsuranceType':patientBasic.InsuranceType,
#                         'ClientName':patientBasic.ClientName.pk if patientBasic.ClientName else None,
#                         'ClientType':patientBasic.ClientType,
#                         'ClientEmployeeId':patientBasic.ClientEmployeeId,
#                         'ClientEmployeeDesignation':patientBasic.ClientEmployeeDesignation,
#                         'ClientEmployeeRelation':patientBasic.ClientEmployeeRelation,
#                         'EmployeeId':patientBasic.EmployeeId.pk if patientBasic.EmployeeId else None,
#                         'EmployeeRelation':patientBasic.EmployeeRelation,
#                         'DoctorId':patientBasic.DoctorId.pk if patientBasic.DoctorId else None,
#                         'DoctorRelation':patientBasic.DoctorRelation,
#                         'DonationType':patientBasic.DonationType,
#                         'Flagging':patientBasic.Flagging.pk if patientBasic.Flagging else None,
#                     })
#                 for  patientBasic in  IP_patient_data:
#                     patient_dict['IP_details'].append({
#                         'IP_Patient' : 1,
#                         'PatientId':patientBasic.PatientId.pk,
#                         'PatientType':patientBasic.PatientType,
#                         'PatientCategory':patientBasic.PatientCategory,
#                         'InsuranceName':patientBasic.InsuranceName.pk if patientBasic.InsuranceName else None,
#                         'InsuranceType':patientBasic.InsuranceType,
#                         'ClientName':patientBasic.ClientName.pk if patientBasic.ClientName else None,
#                         'ClientType':patientBasic.ClientType,
#                         'ClientEmployeeId':patientBasic.ClientEmployeeId,
#                         'ClientEmployeeDesignation':patientBasic.ClientEmployeeDesignation,
#                         'ClientEmployeeRelation':patientBasic.ClientEmployeeRelation,
#                         'EmployeeId':patientBasic.EmployeeId.pk if patientBasic.EmployeeId else None,
#                         'EmployeeRelation':patientBasic.EmployeeRelation,
#                         'DoctorId':patientBasic.DoctorId.pk if patientBasic.DoctorId else None,
#                         'DoctorRelation':patientBasic.DoctorRelation,
#                         'DonationType':patientBasic.DonationType,
#                         'Flagging':patientBasic.Flagging.pk if patientBasic.Flagging else None,

#                     })
#                 for  patientBasic in  Casuality_patient_data:
#                     patient_dict['Casuality_details'].append({
#                         'PatientType':patientBasic.PatientType,
#                         # 'PatientId':patientBasic.PatientId.pk,
#                         'PatientCategory':patientBasic.PatientCategory,
#                         'InsuranceName':patientBasic.InsuranceName.pk if patientBasic.InsuranceName else None,
#                         'InsuranceType':patientBasic.InsuranceType,
#                         'ClientName':patientBasic.ClientName.pk if patientBasic.ClientName else None,
#                         'ClientType':patientBasic.ClientType,
#                         'ClientEmployeeId':patientBasic.ClientEmployeeId,
#                         'ClientEmployeeDesignation':patientBasic.ClientEmployeeDesignation,
#                         'ClientEmployeeRelation':patientBasic.ClientEmployeeRelation,
#                         'EmployeeId':patientBasic.EmployeeId.pk if patientBasic.EmployeeId else None,
#                         'EmployeeRelation':patientBasic.EmployeeRelation,
#                         'DoctorId':patientBasic.DoctorId.pk if patientBasic.DoctorId else None,
#                         'DoctorRelation':patientBasic.DoctorRelation,
#                         'DonationType':patientBasic.DonationType,
#                         'Flagging':patientBasic.Flagging.pk if patientBasic.Flagging else None,

#                     })    
#                 for  patientBasic in  Diagnosis_patient_data:
#                     patient_dict['Diagnosis_details'].append({
#                         'PatientType':patientBasic.PatientType,
#                         # 'PatientId':patientBasic.PatientId.pk,
#                         'PatientCategory':patientBasic.PatientCategory,
#                         'InsuranceName':patientBasic.InsuranceName.pk if patientBasic.InsuranceName else None,
#                         'InsuranceType':patientBasic.InsuranceType,
#                         'ClientName':patientBasic.ClientName.pk if patientBasic.ClientName else None,
#                         'ClientType':patientBasic.ClientType,
#                         'ClientEmployeeId':patientBasic.ClientEmployeeId,
#                         'ClientEmployeeDesignation':patientBasic.ClientEmployeeDesignation,
#                         'ClientEmployeeRelation':patientBasic.ClientEmployeeRelation,
#                         'EmployeeId':patientBasic.EmployeeId.pk if patientBasic.EmployeeId else None,
#                         'EmployeeRelation':patientBasic.EmployeeRelation,
#                         'DoctorId':patientBasic.DoctorId.pk if patientBasic.DoctorId else None,
#                         'DoctorRelation':patientBasic.DoctorRelation,
#                         'DonationType':patientBasic.DonationType,
#                         'Flagging':patientBasic.Flagging.pk if patientBasic.Flagging else None,

#                     })    
#                 for  patientBasic in  Laboratory_patient_data:
#                     patient_dict['Laboratory_details'].append({
#                         'PatientType':patientBasic.PatientType,
#                         # 'PatientId':patientBasic.PatientId.pk,
#                         'PatientCategory':patientBasic.PatientCategory,
#                         'InsuranceName':patientBasic.InsuranceName.pk if patientBasic.InsuranceName else None,
#                         'InsuranceType':patientBasic.InsuranceType,
#                         'ClientName':patientBasic.ClientName.pk if patientBasic.ClientName else None,
#                         'ClientType':patientBasic.ClientType,
#                         'ClientEmployeeId':patientBasic.ClientEmployeeId,
#                         'ClientEmployeeDesignation':patientBasic.ClientEmployeeDesignation,
#                         'ClientEmployeeRelation':patientBasic.ClientEmployeeRelation,
#                         'EmployeeId':patientBasic.EmployeeId.pk if patientBasic.EmployeeId else None,
#                         'EmployeeRelation':patientBasic.EmployeeRelation,
#                         'DoctorId':patientBasic.DoctorId.pk if patientBasic.DoctorId else None,
#                         'DoctorRelation':patientBasic.DoctorRelation,
#                         'DonationType':patientBasic.DonationType,
#                         'Flagging':patientBasic.Flagging.pk if patientBasic.Flagging else None,

#                     })    

#                 patient_detailsList.append(patient_dict)


#             return JsonResponse(patient_dict)

#         except Patient_Detials.DoesNotExist:
#             return JsonResponse({'error': 'Patient not found'}, status=404)
#         except Exception as e:
#             print(f"An error occurred: {str(e)}")
#             return JsonResponse({'error': 'An internal server error occurred'}, status=500)


@csrf_exempt
@require_http_methods(['GET'])
def Patient_Master_List(request):
    if request.method == 'GET':
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
            



            patient_id = request.GET.get('PatientId')
            # Ensure patient_id is provided
            if not patient_id:
                return JsonResponse({'error': 'PatientId is required'}, status=400)

            # Retrieve the patient details
            patient = Patient_Detials.objects.get(pk=patient_id)
            OP_patient_data = Patient_Appointment_Registration_Detials.objects.filter(PatientId__PatientId=patient_id)
            IP_patient_data = Patient_IP_Registration_Detials.objects.filter(PatientId__PatientId=patient_id)
            Casuality_patient_data = Patient_Casuality_Registration_Detials.objects.filter(PatientId__PatientId=patient_id)
            Diagnosis_patient_data = Patient_Diagnosis_Registration_Detials.objects.filter(PatientId__PatientId=patient_id)
            Laboratory_patient_data = Patient_Laboratory_Registration_Detials.objects.filter(PatientId__PatientId=patient_id)
             
           
            patient_dict = {
                'Photo': get_file_image(patient.Patient_profile) if patient.Patient_profile else None,
                'PatientId': patient.PatientId,
                'PhoneNo': patient.PhoneNo,
                'Title': patient.Title.pk if patient.Title else None,
                'FirstName': patient.FirstName,
                'MiddleName': patient.MiddleName,
                'SurName': patient.SurName,
                'Gender': patient.Gender,
                'MaritalStatus': patient.MaritalStatus,
                'SpouseName': patient.SpouseName,
                'FatherName': patient.FatherName,
                # 'AliasName': patient.AliasName,
                'DOB': patient.DOB,
                'Age': patient.Age,
                'Email': patient.Email,
                'BloodGroup': patient.BloodGroup.pk if patient.BloodGroup else None,
                'Occupation': patient.Occupation,
                'Religion': patient.Religion.pk if patient.Religion else None,  # Assuming Religion has a Name field
                'Nationality': patient.Nationality,
                'UniqueIdType': patient.UniqueIdType,
                'UniqueIdNo': patient.UniqueIdNo,
                'PatientType': patient.PatientType,
                'Flagging': patient.Flagging.pk if patient.Flagging else None,
                'DoorNo': patient.DoorNo,
                'Street': patient.Street,
                'Area': patient.Area,
                'City': patient.City,
                'District': patient.District,
                'State': patient.State,
                'Country': patient.Country,
                'Pincode': patient.Pincode,
                'ABHA': patient.ABHA,
                'PermanentAddressSameAsAbove': patient.PermanentAddressSameAsAbove,
                'PermanentPincode': patient.PermanentPincode,
                'PermanentdoorNo': patient.PermanentdoorNo,
                'PermanentStreet': patient.PermanentStreet,
                'PermanentArea': patient.PermanentArea,
                'PermanentCity': patient.PermanentCity,
                'PermanentDistrict': patient.PermanentDistrict,
                'PermanentState': patient.PermanentState,
                'PermanentCountry': patient.PermanentCountry,
                'Createdby': patient.created_by,
                'CurrDate': patient.created_at.strftime('%d-%m-%y'),
                'CurrTime': patient.created_at.strftime('%H:%M:%S'),
                
                # 'OP_details':[{
                #     'OP_Patient' : 1,
                #     'PatientId':patientBasic.PatientId.pk,
                #     # 'PatientType':patientBasic.PatientType,
                #     'PatientCategory':patientBasic.PatientCategory,
                #     'InsuranceName':patientBasic.InsuranceName.pk if patientBasic.InsuranceName else None,
                #     'InsuranceType':patientBasic.InsuranceType,
                #     'ClientName':patientBasic.ClientName.pk if patientBasic.ClientName else None,
                #     'ClientType':patientBasic.ClientType,
                #     'ClientEmployeeId':patientBasic.ClientEmployeeId,
                #     'ClientEmployeeDesignation':patientBasic.ClientEmployeeDesignation,
                #     'ClientEmployeeRelation':patientBasic.ClientEmployeeRelation,
                #     'EmployeeId':patientBasic.EmployeeId.pk if patientBasic.EmployeeId else None,
                #     'EmployeeRelation':patientBasic.EmployeeRelation,
                #     'DoctorId':patientBasic.DoctorId.pk if patientBasic.DoctorId else None,
                #     'DoctorRelation':patientBasic.DoctorRelation,
                #     'DonationType':patientBasic.DonationType,
                #     # 'Flagging':patientBasic.Flagging.pk if patientBasic.Flagging else None,

                #     }for  patientBasic in  OP_patient_data
                # ],
                # 'IP_details':[{
                #     'IP_Patient' : 1,
                #     'PatientId':patientBasic.PatientId.pk,
                #     # 'PatientType':patientBasic.PatientType,
                #     'PatientCategory':patientBasic.PatientCategory,
                #     'InsuranceName':patientBasic.InsuranceName.pk if patientBasic.InsuranceName else None,
                #     'InsuranceType':patientBasic.InsuranceType,
                #     'ClientName':patientBasic.ClientName.pk if patientBasic.ClientName else None,
                #     'ClientType':patientBasic.ClientType,
                #     'ClientEmployeeId':patientBasic.ClientEmployeeId,
                #     'ClientEmployeeDesignation':patientBasic.ClientEmployeeDesignation,
                #     'ClientEmployeeRelation':patientBasic.ClientEmployeeRelation,
                #     'EmployeeId':patientBasic.EmployeeId.pk if patientBasic.EmployeeId else None,
                #     'EmployeeRelation':patientBasic.EmployeeRelation,
                #     'DoctorId':patientBasic.DoctorId.pk if patientBasic.DoctorId else None,
                #     'DoctorRelation':patientBasic.DoctorRelation,
                #     'DonationType':patientBasic.DonationType,
                #     # 'Flagging':patientBasic.Flagging.pk if patientBasic.Flagging else None,


                #     }for  patientBasic in  IP_patient_data
                # ],
                # 'Casuality_details':[{
                #     # 'PatientType':patientBasic.PatientType,
                #     'PatientId':patientBasic.PatientId.pk,
                #     'PatientCategory':patientBasic.PatientCategory,
                #     'InsuranceName':patientBasic.InsuranceName.pk if patientBasic.InsuranceName else None,
                #     'InsuranceType':patientBasic.InsuranceType,
                #     'ClientName':patientBasic.ClientName.pk if patientBasic.ClientName else None,
                #     'ClientType':patientBasic.ClientType,
                #     'ClientEmployeeId':patientBasic.ClientEmployeeId,
                #     'ClientEmployeeDesignation':patientBasic.ClientEmployeeDesignation,
                #     'ClientEmployeeRelation':patientBasic.ClientEmployeeRelation,
                #     'EmployeeId':patientBasic.EmployeeId.pk if patientBasic.EmployeeId else None,
                #     'EmployeeRelation':patientBasic.EmployeeRelation,
                #     'DoctorId':patientBasic.DoctorId.pk if patientBasic.DoctorId else None,
                #     'DoctorRelation':patientBasic.DoctorRelation,
                #     'DonationType':patientBasic.DonationType,
                #     # 'Flagging':patientBasic.Flagging.pk if patientBasic.Flagging else None,

                #     }for  patientBasic in  Casuality_patient_data
                # ],
                # 'Diagnosis_details':[{
                #     # 'PatientType':patientBasic.PatientType,
                #     'PatientId':patientBasic.PatientId.pk,
                #     'PatientCategory':patientBasic.PatientCategory,
                #     'InsuranceName':patientBasic.InsuranceName.pk if patientBasic.InsuranceName else None,
                #     'InsuranceType':patientBasic.InsuranceType,
                #     'ClientName':patientBasic.ClientName.pk if patientBasic.ClientName else None,
                #     'ClientType':patientBasic.ClientType,
                #     'ClientEmployeeId':patientBasic.ClientEmployeeId,
                #     'ClientEmployeeDesignation':patientBasic.ClientEmployeeDesignation,
                #     'ClientEmployeeRelation':patientBasic.ClientEmployeeRelation,
                #     'EmployeeId':patientBasic.EmployeeId.pk if patientBasic.EmployeeId else None,
                #     'EmployeeRelation':patientBasic.EmployeeRelation,
                #     'DoctorId':patientBasic.DoctorId.pk if patientBasic.DoctorId else None,
                #     'DoctorRelation':patientBasic.DoctorRelation,
                #     'DonationType':patientBasic.DonationType,
                #     # 'Flagging':patientBasic.Flagging.pk if patientBasic.Flagging else None,

                #     }for  patientBasic in  Diagnosis_patient_data
                # ],
                # 'Laboratory_details':[{
                #     # 'PatientType':patientBasic.PatientType,
                #     'PatientId':patientBasic.PatientId.pk,
                #     'PatientCategory':patientBasic.PatientCategory,
                #     'InsuranceName':patientBasic.InsuranceName.pk if patientBasic.InsuranceName else None,
                #     'InsuranceType':patientBasic.InsuranceType,
                #     'ClientName':patientBasic.ClientName.pk if patientBasic.ClientName else None,
                #     'ClientType':patientBasic.ClientType,
                #     'ClientEmployeeId':patientBasic.ClientEmployeeId,
                #     'ClientEmployeeDesignation':patientBasic.ClientEmployeeDesignation,
                #     'ClientEmployeeRelation':patientBasic.ClientEmployeeRelation,
                #     'EmployeeId':patientBasic.EmployeeId.pk if patientBasic.EmployeeId else None,
                #     'EmployeeRelation':patientBasic.EmployeeRelation,
                #     'DoctorId':patientBasic.DoctorId.pk if patientBasic.DoctorId else None,
                #     'DoctorRelation':patientBasic.DoctorRelation,
                #     'DonationType':patientBasic.DonationType,
                #     'Flagging':patientBasic.Flagging.pk if patientBasic.Flagging else None,

                #     }for  patientBasic in  Laboratory_patient_data
                # ],
            
            }
           
            return JsonResponse(patient_dict)

        except Patient_Detials.DoesNotExist:
            return JsonResponse({'error': 'Patient not found'}, status=404)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)



@csrf_exempt
@require_http_methods(["GET"])
def Patients_Counts(request):
    try:
        # Calculate today's, monthly, and yearly counts
        today = date.today()
        current_year = today.year
        current_month = today.month

        total_today_count = Patient_Detials.objects.filter(created_at__date=today).count()
        total_month_count = Patient_Detials.objects.filter(
            created_at__year=current_year,
            created_at__month=current_month
        ).count()
        total_year_count = Patient_Detials.objects.filter(
            created_at__year=current_year
        ).count()

        count_data = {
            'today_count': total_today_count,
            'month_count': total_month_count,
            'year_count': total_year_count,
        }

        return JsonResponse(count_data)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'An internal server error occurred'}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_IP_Patient_Details_by_patientId(request):
    try:
        PatientId = request.GET.get("PatientId", "").strip()
        FirstName = request.GET.get("FirstName", "").strip()
        PhoneNumber = request.GET.get("PhoneNumber", "").strip()

        patient = None
        
        if PatientId:
            patient = Patient_IP_Registration_Detials.objects.filter(
                Q(PatientId_PatientId=PatientId) & Q(PatientId_DuplicateId=False)
            ).first()
        elif FirstName and PhoneNumber:
            patient = Patient_Detials.objects.filter(
                Q(FirstName=FirstName) & Q(PhoneNo=PhoneNumber) & Q(DuplicateId=False)
            ).first()

        if not patient:
            return JsonResponse({'warn': 'Patient does not exist'})

        patient_id = patient.PatientId  # Ensure this is a Patient_Detials instance

        # Fix: Ensure we're filtering by patient_id, not the patient object
        roomdata = Patient_Admission_Room_Detials.objects.filter(
            IP_Registration_Id__PatientId=patient_id, Status=True, IsStayed=True
        ).exclude(Iscanceled=True, CurrentlyStayed=True).first()

        # Construct Address dynamically, ensuring no extra commas
        if patient_id.DoorNo:
            address_parts = filter(None, [
                patient_id.DoorNo,
                patient_id.Street,
                patient_id.Area,
                patient_id.City,
                patient_id.State,
                patient_id.Country,
                patient_id.Pincode
            ])
            full_address = ", ".join(address_parts)
        else:
            full_address = "No address available"

        # Get Ward Name & Bed Number if available
        ward_name = None
        if roomdata and roomdata.RoomId:
            ward_name = f"{roomdata.RoomId.Ward_Name.Ward_Name.Ward_Name}{"/"} {roomdata.RoomId.Bed_No}"

        Patient_data = {
            'PatientProfile': get_file_image(patient_id.Patient_profile) if patient_id.Patient_profile else None,
            'PatientName': f'{patient_id.Title.Title_Name}.{patient_id.FirstName} {patient_id.MiddleName} {patient_id.SurName}' if patient_id.FirstName else None,
            'PatientId': patient_id.PatientId,
            'RegistrationId': patient.Registration_Id,
            'PhoneNo': int(patient_id.PhoneNo) if patient_id.PhoneNo and patient_id.PhoneNo.isdigit() else None,
            'Title': getattr(patient_id.Title, 'Title_Name', None),
            'FirstName': patient_id.FirstName,
            'MiddleName': patient_id.MiddleName,
            'SurName': patient_id.SurName,
            'AgeGender': f'{patient_id.Age}/{patient_id.Gender}' if patient_id.Age else None,
            'Gender': patient_id.Gender,
            'MaritalStatus': patient_id.MaritalStatus,
            'SpouseName': patient_id.SpouseName,
            'FatherName': patient_id.FatherName,
            'DOB': patient_id.DOB,
            'Age': patient_id.Age,
            'ABHA': patient_id.ABHA,
            'Email': patient_id.Email,
            'BloodGroup': getattr(patient_id.BloodGroup, 'BloodGroup_Id', None),
            'Occupation': patient_id.Occupation,
            'Religion': getattr(patient_id.Religion, 'Religion_Id', None),
            'Nationality': patient_id.Nationality,
            'UHIDType': patient_id.UniqueIdType,
            'UHIDNo': patient_id.UniqueIdNo,
            'PatientType': patient_id.PatientType,
            'PatientCategory': getattr(patient, 'PatientCategory', None),
            'DoorNo': patient_id.DoorNo,
            'Street': patient_id.Street,
            'Area': patient_id.Area,
            'City': patient_id.City,
            'District': patient_id.District,
            'State': patient_id.State,
            'Country': patient_id.Country,
            'Pincode': patient_id.Pincode,
            'Address': full_address,
            "WardName": ward_name,
            'Ipno':patient.Registration_Id if patient.Registration_Id else None,
            'AdmissionDate': patient.created_at.strftime("%d/%M/%Y %I:%M %p"),

        }

        return JsonResponse(Patient_data)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': f'An internal server error occurred: {str(e)}'})

# @csrf_exempt
# @require_http_methods(["GET"])
# def get_IP_Patient_Details_by_patientId(request):
#     try:
#         PatientId = request.GET.get("PatientId", '').strip()
#         FirstName = request.GET.get("FirstName", '').strip()
#         PhoneNumber = request.GET.get("PhoneNumber", '').strip()

#         print(PatientId, 'PatientId')
#         print(FirstName, 'FirstName')
#         print(PhoneNumber, 'PhoneNumber')

#         if Patient_Detials.objects.exists():
#             patient = None
#             print('hiiiii')

#             if PatientId:
#                 patient = Patient_IP_Registration_Detials.objects.get(Q(PatientId__PatientId=PatientId) & Q(PatientId__DuplicateId=False))
#             elif FirstName and PhoneNumber:
#                 print('hiiiii')
#                 if Patient_Detials.objects.filter(Q(FirstName=FirstName) & Q(PhoneNo=PhoneNumber) & Q(DuplicateId=False)).exists():
#                     patient = Patient_Detials.objects.get(Q(FirstName=FirstName) & Q(PhoneNo=PhoneNumber) & Q(DuplicateId=False))
#                 else:
#                     return JsonResponse({'warn': 'Patient does not exist'})

#             print('hiiiii')
#             if patient:
#                 Patient_data = {
#                     'PatientProfile': get_file_image(patient.PatientId.Patient_profile) if patient.PatientId.Patient_profile else None,
#                     'PatientName': f'{patient.PatientId.Title.Title_Name}.{patient.PatientId.FirstName} {patient.PatientId.MiddleName} {patient.PatientId.SurName}' if patient.PatientId.FirstName else None,
#                     'PatientId': patient.PatientId.PatientId,
#                     'RegistrationId':patient.Registration_Id,
#                     'ABHA': '',
#                     'PhoneNo': int(patient.PatientId.PhoneNo) if patient.PatientId.PhoneNo and patient.PatientId.PhoneNo.isdigit() else None,
#                     'Title': patient.PatientId.Title.Title_Name if patient.PatientId.Title else None,
#                     'FirstName': patient.PatientId.FirstName,
#                     'MiddleName': patient.PatientId.MiddleName,
#                     'SurName': patient.PatientId.SurName,
#                     'AgeGender': f'{patient.PatientId.Age}/{patient.PatientId.Gender}' if patient.PatientId.Age else None,
#                     'Gender': patient.PatientId.Gender,
#                     'MaritalStatus': patient.PatientId.MaritalStatus,
#                     'SpouseName': patient.PatientId.SpouseName,
#                     'FatherName': patient.PatientId.FatherName,
#                     'DOB': patient.PatientId.DOB,
#                     'Age': patient.PatientId.Age,
#                     'ABHA': patient.PatientId.ABHA,
#                     'Email': patient.PatientId.Email,
#                     'BloodGroup': patient.PatientId.BloodGroup.BloodGroup_Id if patient.PatientId.BloodGroup else None,
#                     'Occupation': patient.PatientId.Occupation,
#                     'Religion': patient.PatientId.Religion.Religion_Id if patient.PatientId.Religion else None,
#                     'Nationality': patient.PatientId.Nationality,
#                     'UHIDType': patient.PatientId.UniqueIdType,
#                     'UHIDNo': patient.PatientId.UniqueIdNo,
#                     'PatientType': patient.PatientId.PatientType,
#                     'PatientCategory': patient.PatientCategory if patient.PatientCategory else None,
#                     'DoorNo': patient.PatientId.DoorNo,
#                     'Street': patient.PatientId.Street,
#                     'Area': patient.PatientId.Area,
#                     'City': patient.PatientId.City,
#                     'District': patient.PatientId.District,
#                     'State': patient.PatientId.State,
#                     'Country': patient.PatientId.Country,
#                     'Pincode': patient.PatientId.Pincode,
#                 }
                
#                 return JsonResponse(Patient_data)
#             else:
#                 return JsonResponse({'warn': 'Patient does not exist'})
#         else:
#             return JsonResponse({'warn': 'Patient does not exist'})

#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         return JsonResponse({'error': 'An internal server error occurred'})

@csrf_exempt
@require_http_methods(["GET"])
def Filter_IP_Patient_by_Multiple_Criteria(request):
    try:
        # Fetch query parameters
        first_name = request.GET.get("FirstName", '').strip()
        phone_no = request.GET.get("PhoneNo", '').strip()
        patient_id = request.GET.get("PatientId", '').strip()

        print(first_name, 'FirstName')
        print(phone_no, 'PhoneNo')
        print(patient_id, 'PatientId')

        # Build filter conditions
        filter_conditions = Q()
        if first_name:
            filter_conditions &= Q(FirstName__icontains=first_name)
        if phone_no:
            filter_conditions &= Q(PhoneNo__icontains=phone_no)
        if patient_id:
            filter_conditions &= Q(PatientId__icontains=patient_id)

        # Query the database
        patients = Patient_IP_Registration_Detials.objects.filter(filter_conditions)

        # Prepare patient data
        patient_data = [
            {
                'PatientId': patient.PatientId.PatientId,
                'PhoneNo': int(patient.PatientId.PhoneNo) if patient.PatientId.PhoneNo and patient.PatientId.PhoneNo.isdigit() else None,
                'FirstName': patient.PatientId.FirstName,
            } for patient in patients
        ]

        return JsonResponse(patient_data, safe=False)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'An internal server error occurred'}, status=500)



# @csrf_exempt
# @require_http_methods(["POST", "OPTIONS"])
# def Patient_BasicDetails_Update(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             print(data,'data')
#             patient_id = data.get('PatientId')
#             print(patient_id,'patient_id')
#             patient_type = data.get('PatientType', '')
#             patient_category = data.get('PatientCategory', '')
#             insurance_name = data.get('InsuranceName', '')
#             insurance_type = data.get('InsuranceType', '')
#             client_name = data.get('ClientName', '')
#             client_type = data.get('ClientType', '')
#             client_employee_id = data.get('ClientEmployeeId', '')
#             client_employee_designation = data.get('ClientEmployeeDesignation', '')
#             client_employee_relation = data.get('ClientEmployeeRelation', '')
#             employee_id = data.get('EmployeeId', '')
#             employee_relation = data.get('EmployeeRelation', '')
#             doctor_id = data.get('DoctorId', '')
#             doctor_relation = data.get('DoctorRelation', '')
#             donation_type = data.get('DonationType', '')
#             flagging = data.get('Flagging', '')

#             employee_instance = Employee_Personal_Form_Detials.objects.get(Employee_ID=employee_id) if employee_id else None
#             doctor_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=doctor_id) if doctor_id else None
           
#             Insurance_instance = None
#             if insurance_name:
#               Insurance_instance = Insurance_Master_Detials.objects.get(Insurance_Id=insurance_name) 
             
#             print(Insurance_instance,'Insurance_instanceqqqqqqqqqqqq')
            
#             Client_instance = None

#             if client_name:
#                Client_instance = Client_Master_Detials.objects.get(Client_Id=client_name) 
            
#             print(Client_instance,'Client_instanceqqqqqqqqqqq')
            
#             Flagging_instance = None
#             if flagging:
#                 Flagging_instance = Flaggcolor_Detials.objects.get(Flagg_Id=flagging)
            
#             print(Flagging_instance,'Client_instanceqqqqqqqqqqq')

#             Donation_instance = None
#             if donation_type:
#                Donation_instance = Donation_Master_Detials.objects.get(Donation_Id=donation_type) 
            

#             if not patient_id:
#                 return JsonResponse({'error': 'Patient ID is required'}, status=400)

#             # Retrieve patient and related instances
#             patient = Patient_Detials.objects.filter(PatientId=patient_id).first()
#             if not patient:
#                 return JsonResponse({'error': 'Patient with the given ID does not exist'}, status=404)

#             # Update patient details
#             patient.PhoneNo = data.get('PhoneNo', '')
#             patient.Title = data.get('Title', '')
#             patient.FirstName = data.get('FirstName', '')
#             patient.MiddleName = data.get('MiddleName', '')
#             patient.SurName = data.get('SurName', '')
#             patient.Gender = data.get('Gender', '')
#             # patient.AliasName = data.get('AliasName', '')
#             patient.MaritalStatus = data.get('MaritalStatus', '')
#             patient.SpouseName = data.get('SpouseName', '')
#             patient.FatherName = data.get('FatherName', '')
#             patient.DOB = data.get('DOB', '')
#             patient.Age = data.get('Age', '')
#             patient.Email = data.get('Email', '')
#             patient.BloodGroup = BloodGroup_Detials.objects.filter(BloodGroup_Id=data.get('BloodGroup')).first()
#             patient.Occupation = data.get('Occupation', '')
#             patient.Religion = Religion_Detials.objects.filter(Religion_Id=data.get('Religion')).first()
#             patient.Nationality = data.get('Nationality', '')
#             patient.UniqueIdType = data.get('UniqueIdType', '')
#             patient.UniqueIdNo = data.get('UniqueIdNo', '')
#             patient.PatientType = data.get('PatientType', '')
#             patient.DoorNo = data.get('DoorNo', '')
#             patient.Street = data.get('Street', '')
#             patient.Area = data.get('Area', '')
#             patient.City = data.get('City', '')
#             patient.District = data.get('District', '')
#             patient.State = data.get('State', '')
#             patient.Country = data.get('Country', '')
#             patient.Pincode = data.get('Pincode', '')
#             patient.updated_by = data.get('Created_by', '')
#             patient.Flagging = Flagging_instance
#             patient.save()
            
#             print(patient,'patient')
#             # Prepare related model instances

           
#             # employee_instance = Employee_Personal_Form_Detials.objects.filter(Employee_ID=data.get('EmployeeId')).first()
#             # doctor_instance = Doctor_Personal_Form_Detials.objects.filter(Doctor_ID=data.get('DoctorId')).first()
#             # insurance_instance = Insurance_Master_Detials.objects.filter(Insurance_Id=data.get('InsuranceName')).first()
#             # client_instance = Client_Master_Detials.objects.filter(Client_Id=data.get('ClientName')).first()
#             # flagging_instance = Flaggcolor_Detials.objects.filter(Flagg_Id=data.get('Flagging')).first()

#             # Update OP patient details
#             for op_data in Patient_Appointment_Registration_Detials.objects.filter(PatientId__PatientId=patient_id):
#                 # op_data.PatientType = data.get('PatientType', '')
#                 op_data.PatientCategory = data.get('PatientCategory', '')
#                 op_data.InsuranceName = Insurance_instance
#                 op_data.InsuranceType = data.get('InsuranceType', '')
#                 op_data.ClientName = Client_instance
#                 op_data.ClientType = data.get('ClientType', '')
#                 op_data.ClientEmployeeId = data.get('ClientEmployeeId', '')
#                 op_data.ClientEmployeeDesignation = data.get('ClientEmployeeDesignation', '')
#                 op_data.ClientEmployeeRelation = data.get('ClientEmployeeRelation', '')
#                 op_data.EmployeeId = employee_instance
#                 op_data.EmployeeRelation = data.get('EmployeeRelation', '')
#                 op_data.DoctorId = doctor_instance
#                 op_data.DoctorRelation = data.get('DoctorRelation', '')
#                 op_data.DonationType = Donation_instance
#                 # op_data.Flagging = Flagging_instance
#                 op_data.save()

#                 print(op_data,'op_data')

#             # Similarly update IP, Casualty, Diagnosis, and Laboratory details
#             for ip_data in Patient_IP_Registration_Detials.objects.filter(PatientId__PatientId=patient_id):
#                 # ip_data.PatientType = data.get('PatientType', '')
#                 ip_data.PatientCategory = data.get('PatientCategory', '')
#                 ip_data.InsuranceName = Insurance_instance
#                 ip_data.InsuranceType = data.get('InsuranceType', '')
#                 ip_data.ClientName = Client_instance
#                 ip_data.ClientType = data.get('ClientType', '')
#                 ip_data.ClientEmployeeId = data.get('ClientEmployeeId', '')
#                 ip_data.ClientEmployeeDesignation = data.get('ClientEmployeeDesignation', '')
#                 ip_data.ClientEmployeeRelation = data.get('ClientEmployeeRelation', '')
#                 ip_data.EmployeeId = employee_instance
#                 ip_data.EmployeeRelation = data.get('EmployeeRelation', '')
#                 ip_data.DoctorId = doctor_instance
#                 ip_data.DoctorRelation = data.get('DoctorRelation', '')
#                 ip_data.DonationType = Donation_instance
#                 # ip_data.Flagging = Flagging_instance
#                 ip_data.save()
            
#             for casuality_data in Patient_Casuality_Registration_Detials.objects.filter(PatientId__PatientId=patient_id):
#                 # casuality_data.PatientType = data.get('PatientType', '')
#                 casuality_data.PatientCategory = data.get('PatientCategory', '')
#                 casuality_data.InsuranceName = Insurance_instance
#                 casuality_data.InsuranceType = data.get('InsuranceType', '')
#                 casuality_data.ClientName = Client_instance
#                 casuality_data.ClientType = data.get('ClientType', '')
#                 casuality_data.ClientEmployeeId = data.get('ClientEmployeeId', '')
#                 casuality_data.ClientEmployeeDesignation = data.get('ClientEmployeeDesignation', '')
#                 casuality_data.ClientEmployeeRelation = data.get('ClientEmployeeRelation', '')
#                 casuality_data.EmployeeId = employee_instance
#                 casuality_data.EmployeeRelation = data.get('EmployeeRelation', '')
#                 casuality_data.DoctorId = doctor_instance
#                 casuality_data.DoctorRelation = data.get('DoctorRelation', '')
#                 casuality_data.DonationType = Donation_instance
#                 # casuality_data.Flagging = Flagging_instance
#                 casuality_data.save()
            
#             for diagnosis_data in Patient_Diagnosis_Registration_Detials.objects.filter(PatientId__PatientId=patient_id):
#                 # diagnosis_data.PatientType = data.get('PatientType', '')
#                 diagnosis_data.PatientCategory = data.get('PatientCategory', '')
#                 diagnosis_data.InsuranceName = Insurance_instance
#                 diagnosis_data.InsuranceType = data.get('InsuranceType', '')
#                 diagnosis_data.ClientName = Client_instance
#                 diagnosis_data.ClientType = data.get('ClientType', '')
#                 diagnosis_data.ClientEmployeeId = data.get('ClientEmployeeId', '')
#                 diagnosis_data.ClientEmployeeDesignation = data.get('ClientEmployeeDesignation', '')
#                 diagnosis_data.ClientEmployeeRelation = data.get('ClientEmployeeRelation', '')
#                 diagnosis_data.EmployeeId = employee_instance
#                 diagnosis_data.EmployeeRelation = data.get('EmployeeRelation', '')
#                 diagnosis_data.DoctorId = doctor_instance
#                 diagnosis_data.DoctorRelation = data.get('DoctorRelation', '')
#                 diagnosis_data.DonationType = Donation_instance
#                 # diagnosis_data.Flagging = Flagging_instance
#                 diagnosis_data.save()
            
#             for laboratory_data in Patient_Laboratory_Registration_Detials.objects.filter(PatientId__PatientId=patient_id):
#                 # laboratory_data.PatientType = data.get('PatientType', '')
#                 laboratory_data.PatientCategory = data.get('PatientCategory', '')
#                 laboratory_data.InsuranceName = Insurance_instance
#                 laboratory_data.InsuranceType = data.get('InsuranceType', '')
#                 laboratory_data.ClientName = Client_instance
#                 laboratory_data.ClientType = data.get('ClientType', '')
#                 laboratory_data.ClientEmployeeId = data.get('ClientEmployeeId', '')
#                 laboratory_data.ClientEmployeeDesignation = data.get('ClientEmployeeDesignation', '')
#                 laboratory_data.ClientEmployeeRelation = data.get('ClientEmployeeRelation', '')
#                 laboratory_data.EmployeeId = employee_instance
#                 laboratory_data.EmployeeRelation = data.get('EmployeeRelation', '')
#                 laboratory_data.DoctorId = doctor_instance
#                 laboratory_data.DoctorRelation = data.get('DoctorRelation', '')
#                 laboratory_data.DonationType = Donation_instance
#                 # laboratory_data.Flagging = Flagging_instance
#                 laboratory_data.save()


#             return JsonResponse({'success': 'Patient details updated successfully'})
        
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def Patient_BasicDetails_Update(request):

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
                image.save(output, format='PNG', quality=quality)
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
            file_data = file.split(',')[1]
            file_content = base64.b64decode(file_data)
            file_size = len(file_content)
            
            max_size_mb = 5

            if file_size > max_size_mb * 1024 * 1024:
                print('maximum mb')
                return JsonResponse({'warn': f'File size exceeds the maximum allowed size ({max_size_mb}MB)'})

            file_type = get_file_type(file)
            
            if file_type == 'image/jpeg' or file_type == 'image/png':
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
            print(data, 'data222222222222wwwwwwwwwww')

            # Fetch data from request

            Patient_profile_photo = data.get('Photo', None)
            Patient_profile_photo_prossed = validate_and_process_file(Patient_profile_photo) if Patient_profile_photo else None
           
            patient_id = data.get('PatientId')
            print(patient_id, 'patient_id')

            # Initialize optional fields
            patient_type = data.get('PatientType', '')
            # patient_category = data.get('PatientCategory', '')
            # insurance_name = data.get('InsuranceName', '')
            # insurance_type = data.get('InsuranceType', '')
            # client_name = data.get('ClientName', '')
            # client_type = data.get('ClientType', '')
            # client_employee_id = data.get('ClientEmployeeId', '')
            # client_employee_designation = data.get('ClientEmployeeDesignation', '')
            # client_employee_relation = data.get('ClientEmployeeRelation', '')
            # employee_id = data.get('EmployeeId', '')
            # employee_relation = data.get('EmployeeRelation', '')
            # doctor_id = data.get('DoctorId', '')
            # doctor_relation = data.get('DoctorRelation', '')
            # donation_type = data.get('DonationType', '')
            flagging = data.get('Flagging', '')
            Title = data.get('Title', '')
            BloodGroup = data.get('BloodGroup', '')
            Religion = data.get('Religion', '')

            # Fetch related instances
            # employee_instance = Employee_Personal_Form_Detials.objects.get(Employee_ID=employee_id) if employee_id else None
            # doctor_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=doctor_id) if doctor_id else None
            # Insurance_instance = Insurance_Master_Detials.objects.get(Insurance_Id=insurance_name) if insurance_name else None
            # Client_instance = Client_Master_Detials.objects.get(Client_Id=client_name) if client_name else None
            # Donation_instance = Donation_Master_Detials.objects.get(Donation_Id=donation_type) if donation_type else None
            Title_instance = Title_Detials.objects.get(Title_Id=Title) if Title else None
            Flagging_instance = Flaggcolor_Detials.objects.get(Flagg_Id=flagging) if flagging else None
            BloodGroup_instance = BloodGroup_Detials.objects.get(BloodGroup_Id=BloodGroup) if BloodGroup else None
            Religion_instance = Religion_Detials.objects.get(Religion_Id=Religion) if Religion else None

            # Ensure Patient ID exists
            if not patient_id:
                return JsonResponse({'error': 'Patient ID is required'}, status=400)

            # Fetch the patient record
            patient = Patient_Detials.objects.get(PatientId=patient_id)
            print(patient.PatientType,'patient.PatientType')
            if not patient:
                return JsonResponse({'error': 'Patient with the given ID does not exist'}, status=400)

            # Update patient details

            patient.Patient_profile = Patient_profile_photo_prossed
            patient.PhoneNo = data.get('PhoneNo', '')
            patient.Title = Title_instance
            patient.FirstName = data.get('FirstName', '')
            patient.MiddleName = data.get('MiddleName', '')
            patient.SurName = data.get('SurName', '')
            patient.Gender = data.get('Gender', '')
            patient.MaritalStatus = data.get('MaritalStatus', '')
            patient.SpouseName = data.get('SpouseName', '')
            patient.FatherName = data.get('FatherName', '')
            patient.DOB = data.get('DOB', '')
            patient.Age = data.get('Age', '')
            patient.Email = data.get('Email', '')
            patient.BloodGroup = BloodGroup_instance
            # patient.BloodGroup = BloodGroup_Detials.objects.filter(BloodGroup_Id=data.get('BloodGroup','')).first()
            patient.Occupation = data.get('Occupation', '')
            patient.Religion = Religion_instance
            # patient.Religion = Religion_Detials.objects.filter(Religion_Id=data.get('Religion','')).first()
            patient.Nationality = data.get('Nationality', '')
            patient.UniqueIdType = data.get('UniqueIdType', '')
            patient.UniqueIdNo = data.get('UniqueIdNo', '')
            patient.PatientType = data.get('PatientType', '')
            patient.DoorNo = data.get('DoorNo', '')
            patient.Street = data.get('Street', '')
            patient.Area = data.get('Area', '')
            patient.City = data.get('City', '')
            patient.District = data.get('District', '')
            patient.State = data.get('State', '')
            patient.Country = data.get('Country', '')
            patient.Pincode = data.get('Pincode', '')
            patient.ABHA = data.get('ABHA', '')
            patient.PermanentAddressSameAsAbove = data.get('PermanentAddressSameAsAbove', '')
            patient.PermanentPincode = data.get('PermanentPincode', '')
            patient.PermanentdoorNo = data.get('PermanentdoorNo', '')
            patient.PermanentStreet = data.get('PermanentStreet', '')
            patient.PermanentArea = data.get('PermanentArea', '')
            patient.PermanentCity = data.get('PermanentCity', '')
            patient.PermanentDistrict = data.get('PermanentDistrict', '')
            patient.PermanentState = data.get('PermanentState', '')
            patient.PermanentCountry = data.get('PermanentCountry', '')
            patient.updated_by = data.get('Created_by', '')
            patient.PatientType = patient_type
            patient.Flagging = Flagging_instance
            patient.save()

            print(patient, 'patient')

            # def update_related_data(model_class, patient_id):
            #     for data_instance in model_class.objects.filter(PatientId__PatientId=patient_id):
            #         data_instance.PatientCategory = patient_category
            #         data_instance.InsuranceName = Insurance_instance
            #         data_instance.InsuranceType = insurance_type
            #         data_instance.ClientName = Client_instance
            #         data_instance.ClientType = client_type
            #         data_instance.ClientEmployeeId = client_employee_id
            #         data_instance.ClientEmployeeDesignation = client_employee_designation
            #         data_instance.ClientEmployeeRelation = client_employee_relation
            #         data_instance.EmployeeId = employee_instance
            #         data_instance.EmployeeRelation = employee_relation
            #         data_instance.DoctorId = doctor_instance
            #         data_instance.DoctorRelation = doctor_relation
            #         data_instance.DonationType = Donation_instance
            #         data_instance.save()

            # update_related_data(Patient_Appointment_Registration_Detials, patient_id)
            # update_related_data(Patient_IP_Registration_Detials, patient_id)
            # update_related_data(Patient_Casuality_Registration_Detials, patient_id)
            # update_related_data(Patient_Diagnosis_Registration_Detials, patient_id)
            # update_related_data(Patient_Laboratory_Registration_Detials, patient_id)

            return JsonResponse({'success': 'Patient details updated successfully'})

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'error': str(e)}, status=500)




@csrf_exempt
def get_Employee_by_PatientCategory(request):
    if request.method == 'GET':
        try:
            
            # Retrieve all employees, you might want to filter this based on specific criteria
            employee_query_set = Employee_Personal_Form_Detials.objects.all()
            
            # Check if any employee records exist
            if not employee_query_set.exists():
                return JsonResponse({'error': 'No employees found'})
            
            emp_datas = []
            for emp in employee_query_set:
                emp_dict = {
                    'id': emp.Employee_ID,
                    'Name': f'{emp.Tittle}.{emp.First_Name} {emp.Middle_Name} {emp.Last_Name}',
                    # 'ShortName': f'{emp.Tittle}.{emp.First_Name} {emp.Last_Name}',
                }
                emp_datas.append(emp_dict)
            
            # Return JSON response
            return JsonResponse(emp_datas, safe=False)
        
        except Exception as e:
            # Handle exceptions and return error response
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)




@csrf_exempt
def get_DoctorId_by_PatientCategory(request):
    if request.method == 'GET':
        try:
            

            # Retrieve all employees, you might want to filter this based on specific criteria
            Doctor_query_set = Doctor_Personal_Form_Detials.objects.all()
            
            # Check if any employee records exist
            if not Doctor_query_set.exists():
                return JsonResponse({'error': 'No Doctor found'})
            
            Doc_datas = []
            for Doc in Doctor_query_set:
                Doc_dict = {
                    'id': Doc.Doctor_ID,
                    'Name': f'{Doc.Tittle}.{Doc.First_Name} {Doc.Middle_Name} {Doc.Last_Name}',
                    'ShortName': f'{Doc.Tittle}.{Doc.ShortName} ',
                }
                Doc_datas.append(Doc_dict)
            
            # Return JSON response
            return JsonResponse(Doc_datas, safe=False)
        
        except Exception as e:
            # Handle exceptions and return error response
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


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

@csrf_exempt
@require_http_methods(["GET"])
def get_Patient_Details_by_patientId(request):
    try:
        PatientId = request.GET.get("PatientId", '').strip()
        FirstName = request.GET.get("FirstName", '').strip()
        PhoneNumber = request.GET.get("PhoneNumber", '').strip()

        print(PatientId, 'PatientId')
        print(FirstName, 'FirstName')
        print(PhoneNumber, 'PhoneNumber')



        if Patient_Detials.objects.exists():
            patient = None
            print('hiiiii')

            if PatientId:
                
                if Patient_IP_Registration_Detials.objects.filter(
                    PatientId=PatientId, Status__in=['Registered', 'Admitted']
                ).exists():
                    return JsonResponse({'warn': 'This patient is already in IP and process is not completed'})
                
                if Patient_Appointment_Registration_Detials.objects.filter(
                    PatientId=PatientId, Status__in=['Registered', 'InProgress']
                ).exists():
                    return JsonResponse({'warn': 'This patient is already in OP and process is not completed'})
                
                if Patient_Emergency_Registration_Detials.objects.filter(
                    PatientId=PatientId, Status__in=['Registered', 'Admitted']
                ).exists():
                    return JsonResponse({'warn': 'This patient is already in OP and process is not completed'})

                

                patient = Patient_Detials.objects.get(Q(PatientId=PatientId) & Q(DuplicateId=False))
            elif FirstName and PhoneNumber:
                print('hiiiii')
                if Patient_Detials.objects.filter(Q(FirstName=FirstName) & Q(PhoneNo=PhoneNumber) & Q(DuplicateId=False)).exists():
                    patient = Patient_Detials.objects.get(Q(FirstName=FirstName) & Q(PhoneNo=PhoneNumber) & Q(DuplicateId=False))
                else:
                    return JsonResponse({'warn': 'Patient does not exist'})

            print('hiiiii')
            if patient:
                Patient_data = {
                    'PatientProfile': get_file_image(patient.Patient_profile) if patient.Patient_profile else None,
                    'PatientId': patient.PatientId,
                    'ABHA': patient.ABHA,
                    'PhoneNo': int(patient.PhoneNo) if patient.PhoneNo and patient.PhoneNo.isdigit() else None,
                    'Title': patient.Title.Title_Id if patient.Title else None,
                    'FirstName': patient.FirstName,
                    'MiddleName': patient.MiddleName,
                    'SurName': patient.SurName,
                    'Gender': patient.Gender,
                    'MaritalStatus': patient.MaritalStatus,
                    'SpouseName': patient.SpouseName,
                    'FatherName': patient.FatherName,
                    'DOB': patient.DOB,
                    'Age': patient.Age,
                    'ABHA': patient.ABHA,
                    'Email': patient.Email,
                    'BloodGroup': patient.BloodGroup.BloodGroup_Id if patient.BloodGroup else None,
                    'Occupation': patient.Occupation,
                    'Religion': patient.Religion.Religion_Id if patient.Religion else None,
                    'Nationality': patient.Nationality,
                    'UHIDType': patient.UniqueIdType,
                    'UHIDNo': patient.UniqueIdNo,
                    'PatientType': patient.PatientType,
                    'DoorNo': patient.DoorNo,
                    'Street': patient.Street,
                    'Area': patient.Area,
                    'City': patient.City,
                    'District': patient.District,
                    'State': patient.State,
                    'Country': patient.Country,
                    'Pincode': patient.Pincode,
                    'Status': patient.Status,
                    'DoctorID': patient.DoctorID.Doctor_ID if patient.DoctorID else None,
                }
                return JsonResponse(Patient_data)
            else:
                return JsonResponse({'warn': 'Patient does not exist'})
        else:
            return JsonResponse({'warn': 'Patient does not exist'})

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'An internal server error occurred'})



@csrf_exempt
@require_http_methods(["GET"])
def get_registered_patient_details(request):
    if request.method == 'GET':
        try:
            RegistrationId = request.GET.get("RegistrationId", '').strip()

            if RegistrationId:
                reg = Patient_Appointment_Registration_Detials.objects.get(Registration_Id=RegistrationId)

                full_name = f"{reg.PatientId.FirstName} {reg.PatientId.MiddleName} {reg.PatientId.SurName}"
                formatted_date = reg.created_at.strftime("%d/%b/%Y")
                reg_data = {
                    'RegistrationId': reg.Registration_Id,
                    'PatientId': reg.PatientId.PatientId,
                    'DoctorId': reg.PrimaryDoctor.Doctor_ID if reg.PrimaryDoctor else None,
                    'PhoneNo': int(reg.PatientId.PhoneNo) if reg.PatientId.PhoneNo and reg.PatientId.PhoneNo.isdigit() else None,
                    'Patient_Name':full_name.strip(),
                    'AgeGender': f'{reg.PatientId.Age}/{reg.PatientId.Gender}',
                    'Address': f'{reg.PatientId.DoorNo}, {reg.PatientId.Street}, {reg.PatientId.Area}, {reg.PatientId.City}, {reg.PatientId.State}, {reg.PatientId.Country}, {reg.PatientId.Pincode}',
                    'VisitId': reg.VisitId,
                    'VisitPurpose':reg.VisitPurpose,
                    # 'PatientType':row.Registration_Id.PatientType,
                    'PatientCategory':reg.PatientCategory,
                    'Doctor_ShortName':reg.PrimaryDoctor.ShortName if reg.PrimaryDoctor else None,
                    'Title' : reg.PatientId.Title.Title_Name,
                    'FirstName' : reg.PatientId.FirstName,
                    'MiddleName' : reg.PatientId.MiddleName,
                    'SurName' : reg.PatientId.SurName,
                    'Gender' : reg.PatientId.Gender,
                    'DOB' : reg.PatientId.DOB,
                    'Age' : reg.PatientId.Age,
                    'Email' : reg.PatientId.Email,
                    'BloodGroup' : reg.PatientId.BloodGroup.BloodGroup_Name if reg.PatientId.BloodGroup else None,
                    'Occupation' : reg.PatientId.Occupation,
                    'Religion' : reg.PatientId.Religion.Religion_Id if reg.PatientId.Religion else None,
                    'Nationality' :reg.PatientId.Nationality,
                    'UniqueIdType' : reg.PatientId.UniqueIdType,
                    'UniqueIdNo' : reg.PatientId.UniqueIdNo,
                    # 'CaseSheetNo' : row.Registration_Id.PatientId.CasesheetNo,
                    'Complaint' : reg.Complaint,
                    # 'PatientType' : row.Registration_Id.PatientType,
                    # 'PatientCategory': row.Registration_Id.PatientCategory,
                    'DoorNo' : reg.PatientId.DoorNo,
                    'Street' :reg.PatientId.Street,
                    'Area' :reg.PatientId.Area,
                    'City' :reg.PatientId.City,
                    'State' :reg.PatientId.State,
                    'Country' :reg.PatientId.Country,
                    'Pincode' :reg.PatientId.Pincode,   
                    'Date':formatted_date,
                }
            return JsonResponse(reg_data,safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)})



@csrf_exempt
@require_http_methods(["GET"])
def Filter_Patient_by_Multiple_Criteria(request):
    try:
        # Fetch query parameters
        first_name = request.GET.get("FirstName", '').strip()
        phone_no = request.GET.get("PhoneNo", '').strip()
        DoctorId = request.GET.get("DoctorId", '').strip()
        patient_id = request.GET.get("PatientId", '').strip()

        print(first_name, 'FirstName')
        print(phone_no, 'PhoneNo')
        print(DoctorId, 'DoctorId')
        print(patient_id, 'PatientId')

        # Build filter conditions
        filter_conditions = Q()
        if first_name:
            filter_conditions &= Q(FirstName__icontains=first_name)
        if phone_no:
            filter_conditions &= Q(PhoneNo__icontains=phone_no)
        if DoctorId:
            filter_conditions &= Q(DoctorID__icontains=DoctorId)
        if patient_id:
            filter_conditions &= Q(PatientId__icontains=patient_id)

        # Query the database
        registration = Patient_Appointment_Registration_Detials.objects.all()

        patient_datas = []
        for reg in registration:
            patient_data = {
                'PatientId': reg.PatientId.PatientId,
                'RegistrationId': reg.Registration_Id,
                'DoctorId': reg.PrimaryDoctor.Doctor_ID if reg.PrimaryDoctor else None,
                'PhoneNo': int(reg.PatientId.PhoneNo) if reg.PatientId.PhoneNo and reg.PatientId.PhoneNo.isdigit() else None,
                'FirstName': reg.PatientId.FirstName,
            } 
            patient_datas.append(patient_data)

        return JsonResponse(patient_datas, safe=False)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'An internal server error occurred'}, status=500)



@csrf_exempt
@require_http_methods(["GET"])
def Filter_Patients_using_Multiple_Criteria(request):
    try:
        # Extract parameters from the request
        first_name = request.GET.get("FirstName", None)
        phone_no = request.GET.get("PhoneNo", None)
        patient_id = request.GET.get("PatientId", None)
        middle_name = request.GET.get("MiddleName", None)
        sur_name = request.GET.get("SurName", None)

        print(first_name, 'FirstName')
        print(phone_no, 'PhoneNo')
        print(patient_id, 'PatientId')
        print(middle_name, 'MiddleName')
        print(sur_name, 'SurName')

        # Build filter conditions dynamically
        filter_conditions = Q()
        if first_name:
            filter_conditions &= Q(FirstName__icontains=first_name)
        if middle_name:
            filter_conditions &= Q(MiddleName__icontains=middle_name)
        if sur_name:
            filter_conditions &= Q(SurName__icontains=sur_name)
        if phone_no:
            filter_conditions &= Q(PhoneNo__icontains=phone_no)
        if patient_id:
            filter_conditions &= Q(PatientId__icontains=patient_id)

        # Filter patient details based on conditions, limiting to 10 results
        patients = Patient_Detials.objects.filter(filter_conditions, DuplicateId=False)[:10]

        # Prepare patient data for the response
        patient_data = [
            {
                'PatientId': patient.PatientId,
                'PhoneNo': int(patient.PhoneNo) if patient.PhoneNo else None,
                'FirstName': patient.FirstName,
                'MiddleName': patient.MiddleName,
                'SurName': patient.SurName,
            } for patient in patients
        ]

        return JsonResponse(patient_data, safe=False)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'An internal server error occurred'}, status=500)



@csrf_exempt
@require_http_methods(["GET"])
def get_patient_appointment_details(request):
    try:
        SearchbyDate=request.GET.get('SearchbyDate')
        SearchbyFirstName=request.GET.get('SearchbyFirstName')
        SearchbyPhoneNumber=request.GET.get('SearchbyPhoneNumber')
        SearchSpecialization=request.GET.get('SearchSpecialization')
        SearchDoctor=request.GET.get('SearchDoctor')
        SearchStatus=request.GET.get('SearchStatus')

        
        Searchquery= Q()
        
        if SearchbyDate:
            search_date = datetime.strptime(SearchbyDate, "%Y-%m-%d").date()
            Searchquery &= Q(created_at__date=search_date)
        if SearchbyFirstName :
            Searchquery &= Q(PatientId__FirstName__icontains=SearchbyFirstName)
        if SearchbyPhoneNumber :
            Searchquery &= Q(PatientId__PhoneNo__icontains=SearchbyPhoneNumber)
        if SearchSpecialization:
            Searchquery &= Q(Specialization__pk=SearchSpecialization)
        if SearchDoctor:
            Searchquery &= Q(PrimaryDoctor__pk=SearchDoctor)
        if SearchStatus:
            Searchquery &= Q(Status__icontains=SearchStatus)

        print('Searchquery',Searchquery)

        queryset = Patient_Appointment_Registration_Detials.objects.filter(Searchquery)

        
        appointment_register_data = []
        for idx, register in enumerate(queryset, start=1):
            
            # Flagging_name = register.Flagging.Flagg_Name if register.Flagging else None
            # Flagging_color = register.Flagging.Flagg_Color if register.Flagging else None
            
            # Prepare the appointment data dictionary
            appointment_dict = {
                
                'id': idx,
                'PatientProfile': get_file_image(register.PatientId.Patient_profile) if register.PatientId.Patient_profile else None,
                'PatientId': register.PatientId.PatientId,
                'PatientName': f"{register.PatientId.Title.Title_Name}.{register.PatientId.FirstName} {register.PatientId.MiddleName} {register.PatientId.SurName}",
                'PhoneNo': register.PatientId.PhoneNo,
                'AppointmentId': register.AppointmentId,
                'VisitId': register.VisitId,
                'AppointmentSlot_by_Doctor':register.AppointmentSlot_by_Doctor,
                'Complaint': register.Complaint,
                'isMLC': register.IsMLC,
                # 'Flagging': Flagging_name,
                # 'FlaggingColour': Flagging_color,
                'isRefferal': register.IsReferral,
                'Status': register.Status,
                'DoctorId': register.PrimaryDoctor.Doctor_ID if register.PrimaryDoctor.Doctor_ID else None, 
                'RegistrationId': register.pk,
                'DoctorName': f"{register.PrimaryDoctor.Tittle.Title_Name}.{register.PrimaryDoctor.ShortName}",
                'Specilization': str(register.Specialization.Speciality_Name) if register.Specialization else '',
                'UniqueIdType' : register.PatientId.UniqueIdType,
                'UniqueIdNo' : register.PatientId.UniqueIdNo,
            }

            # Add reason if status is "Cancelled"
            if register.Status == "Cancelled":
                cancel_details = Patient_Appointment_Registration_Cancel_Details.objects.filter(
                    Registration_Id=register.pk
                ).first()
                appointment_dict['Reason'] = cancel_details.Cancel_Reason if cancel_details else None

            # Fetch reschedule reason if available
            reschedule_details = Patient_Registration_Reshedule_Details.objects.filter(
                Registration_Id=register.pk
            ).first()
            if reschedule_details:
                appointment_dict['ChangingReason'] = reschedule_details.ChangingReason

            appointment_register_data.append(appointment_dict)

        return JsonResponse(appointment_register_data, safe=False)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def get_patient_unique_id(request):
    api_key = request.headers.get('Apikey')
    api_password = request.headers.get('Apipassword')
    sessionid = request.headers.get('Sessionid')
    if authenticate_request(sessionid, api_key, api_password):       
        if request.method == 'GET':
            try:
                patient_instance = Patient_Detials.objects.all()
                
                patient_details_data = []   
                for patient in patient_instance:
                    patient_dict ={
                        'PatientId' : patient.PatientId,
                        'PatientName': f"{patient.Title}.{patient.FirstName} {patient.MiddleName} {patient.SurName}",
                        'PhoneNo': patient.PhoneNo,
                        'UniqueIdType' : patient.UniqueIdType,
                        'UniqueIdNo' : patient.UniqueIdNo,
                    }
                patient_details_data.append(patient_dict)
                return JsonResponse(patient_details_data,safe=False)
            except Exception as e:
                return JsonResponse({"error" : str(e)})
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=200)


@csrf_exempt
@require_http_methods(["GET"])
def get_patient_ip_registration_details(request):
    try:
        query = request.GET.get('query', '')
        status = request.GET.get('status', '')

        queryset = Patient_IP_Registration_Detials.objects.all()

        # Apply filters based on the query parameters
        if query:
            queryset = queryset.filter(
                Q(PatientId__FirstName__icontains=query) |
                Q(PatientId__MiddleName__icontains=query) |
                Q(PatientId__SurName__icontains=query) |
                Q(PatientId__PatientId__icontains=query) |
                Q(PatientId__PhoneNo__icontains=query)
            )

        if status:
            queryset = queryset.filter(Q(Status__icontains=status))

        # Serialize the filtered queryset
        ip_register_data = []
        for idx, register in enumerate(queryset, start=1):
            patient = register.PatientId
            client_name = register.ClientName.Client_Name if register.ClientName else None
            insurance_name = register.InsuranceName.Insurance_Name if register.InsuranceName else None
            Flagging_name = register.Flagging.Flagg_Name if register.Flagging else None
            Flagging_color = register.Flagging.Flagg_Color if register.Flagging else None
            
            appointment_dict = {
                'id': idx,
                'PatientProfile': get_file_image(patient.Patient_profile) if patient.Patient_profile else None,
                'RegistrationId': register.Registration_Id,
                'PatientId': patient.PatientId,
                'PatientName': f"{patient.Title}.{patient.FirstName} {patient.MiddleName} {patient.SurName}",
                'PhoneNo': patient.PhoneNo,
                'Age': patient.Age,
                'Gender': patient.Gender,
                'Address': f"{patient.DoorNo}.{patient.Street}.{patient.Area}.{patient.City}.{patient.State}.{patient.Country}.{patient.Pincode}",
                'BloodGroup': patient.BloodGroup,
                'Complaint': register.Complaint,
                'isMLC': register.IsMLC,
                'Flagging': Flagging_name,
                'FlaggingColour': Flagging_color,
                # 'Flagging': register.Flagging,
                'isRefferal': register.IsReferral,
                'ClientName': client_name,  # Handle None case
                'InsuranceName': insurance_name,  # Handle None case
                'Status': register.Status,
                'userName': register.created_by,
                'DoctorName': f"{register.PrimaryDoctor.Tittle}.{register.PrimaryDoctor.First_Name} {register.PrimaryDoctor.Last_Name}" if register.PrimaryDoctor else '',
                'Specialization': str(register.Specialization.Speciality_Name) if register.Specialization else '',
                'CurrDate': register.created_at.strftime('%d-%m-%y') if register.created_at else "",
                'CurrTime': register.created_at.strftime('%I:%M %p') if register.created_at else "",
            }
            ip_register_data.append(appointment_dict)

        return JsonResponse(ip_register_data, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)})


# @csrf_exempt
# @require_http_methods(["GET"])
# def get_patient_casuality_details(request):
#         try:
           
#             query = request.GET.get('query', '')
#             status = request.GET.get('status', '')

#             queryset = Patient_Casuality_Registration_Detials.objects.all()

#             # Apply filters based on the query parameters
#             if query:
#                 queryset = queryset.filter(
#                     Q(PatientId__FirstName__icontains=query)|
#                     Q(PatientId__MiddleName__icontains=query)|
#                     Q(PatientId__SurName__icontains=query)|
#                     Q(PatientId__PatientId__icontains=query)|
#                     Q(PatientId__PhoneNo__icontains=query))
           
#             if status:
#                 queryset = queryset.filter(Q(Status__icontains=status))


#             # Serialize the filtered queryset
#             casuality_register_data = []
#             for idx, register in enumerate(queryset, start=1):
#                 Flagging_name = register.Flagging.Flagg_Name if register.Flagging else None
#                 Flagging_color = register.Flagging.Flagg_Color if register.Flagging else None
             
#                 appointment_dict = {
#                     'id' : idx,
#                     'PatientProfile': get_file_image(register.PatientId.Patient_profile) if register.PatientId and register.PatientId.Patient_profile else None,
#                     'RegistrationId':register.pk,
#                     'PatientId': register.PatientId.PatientId if register.PatientId else None,
#                     'PatientName': f"{register.PatientId.Title}.{register.PatientId.FirstName} {register.PatientId.MiddleName} {register.PatientId.SurName}" if register.PatientId else None,
#                     'PhoneNo': register.PatientId.PhoneNo if register.PatientId else None,
#                     'VisitId': register.VisitId,
#                     'Complaint': register.Complaint,
#                     'isMLC': register.IsMLC,
#                     'Flagging': Flagging_name,
#                     'FlaggingColour': Flagging_color,
#                     # 'Flagging': register.Flagging,
#                     'isRefferal': register.IsReferral,
#                     'Status': register.Status,
#                     'DoctorName': f"{register.PrimaryDoctor.Tittle}.{register.PrimaryDoctor.First_Name} {register.PrimaryDoctor.Last_Name}" if register.PrimaryDoctor else None,
#                     'Specilization': str(register.Specialization.Speciality_Name) if register.Specialization else '',
#                 }
#                 casuality_register_data.append(appointment_dict)

#             return JsonResponse(casuality_register_data, safe=False)

#         except Exception as e:
#             return JsonResponse({'error': str(e)})


@csrf_exempt
@require_http_methods(["GET"])
def get_patient_casuality_details(request):
        try:
           
            query = request.GET.get('query', '')
            status = request.GET.get('status', '')
 
            queryset = Patient_Casuality_Registration_Detials.objects.all()
 
            # Apply filters based on the query parameters
            if query:
                queryset = queryset.filter(
                    Q(PatientId__FirstName__icontains=query)|
                    Q(PatientId__MiddleName__icontains=query)|
                    Q(PatientId__SurName__icontains=query)|
                    Q(PatientId__PatientId__icontains=query)|
                    Q(PatientId__PhoneNo__icontains=query))
           
            if status:
                queryset = queryset.filter(Q(Status__icontains=status))
 
 
            # Serialize the filtered queryset
            casuality_register_data = []
            for idx, register in enumerate(queryset, start=1):
                Flagging_name = register.Flagging.Flagg_Name if register.Flagging else None
                Flagging_color = register.Flagging.Flagg_Color if register.Flagging else None
 
                patient_instance = Patient_Casuality_Registration_Detials.objects.filter(PatientId_id=register.PatientId.PatientId)
 
                for patient_ins in patient_instance:
 
 
                 PatientType_ins = Flaggcolor_Detials.objects.get(Flagg_Name=patient_ins.PatientType)
                 patientCategory_ins = Flaggcolor_Detials.objects.get(Flagg_Name=patient_ins.PatientCategory)
               
                 try:
                  specialtype_ins = Flaggcolor_Detials.objects.get(Flagg_Id=patient_ins.Flagging_id)
 
                 except Flaggcolor_Detials.DoesNotExist:
                    continue
               
 
                 specialtypelist = ['GENERAL','VIP','GOVT','INSURANCE','MLC','CLIENT','CORPORATE','DONATION','EMPLOYEE','EMPLOYEERELATION','DOCTOR','DOCTORRELATION']
           
                 if patient_ins.IsMLC == 'Yes':
 
                      mlc_ins = Flaggcolor_Detials.objects.get(Flagg_Name= 'MLC')
 
                      appointment_dict = {
                        'id' : idx,
                        'PatientProfile': get_file_image(register.PatientId.Patient_profile) if register.PatientId and register.PatientId.Patient_profile else None,
                        'RegistrationId':register.pk,
                        'PatientId': register.PatientId.PatientId if register.PatientId else None,
                        'PatientName': f"{register.PatientId.Title}.{register.PatientId.FirstName} {register.PatientId.MiddleName} {register.PatientId.SurName}" if register.PatientId else None,
                        'PhoneNo': register.PatientId.PhoneNo if register.PatientId else None,
                        'Age': register.PatientId.Age,
                        'Gender': register.PatientId.Gender,
                        'VisitId': register.VisitId,
                        'Complaint': register.Complaint,
                        # 'isMLC': register.IsMLC,
                        # 'Flagging': Flagging_name,
                        # 'FlaggingColour': Flagging_color,
                        # 'Flagging': register.Flagging,
                        'isRefferal': register.IsReferral,
                        'Status': register.Status,
                        'DoctorName': f"{register.PrimaryDoctor.Tittle}.{register.PrimaryDoctor.First_Name} {register.PrimaryDoctor.Last_Name}" if register.PrimaryDoctor else None,
                        'Specilization': str(register.Specialization.Speciality_Name) if register.Specialization else '',
                     
                       
                        'PatientType': patient_ins.PatientType,
                        'patientTypeColor':PatientType_ins.Flagg_Color,
                        'PatientCategory':patient_ins.PatientCategory,
                        'patientCategoryColor':patientCategory_ins.Flagg_Color,
                        'IsMLC':   'MLC',
                        'MLCColor': mlc_ins.Flagg_Color,
                        'specialtype' : specialtype_ins.Flagg_Name if specialtype_ins.Flagg_Name  not in specialtypelist else 'GENERAL',
                        'specialtypecolor':specialtype_ins.Flagg_Color if specialtype_ins.Flagg_Name  not in specialtypelist else '#fff'
                       
                     }
                      casuality_register_data.append(appointment_dict)
 
                 else:
                    appointment_dict = {
                    'id' : idx,
                    'PatientProfile': get_file_image(register.PatientId.Patient_profile) if register.PatientId and register.PatientId.Patient_profile else None,
                    'RegistrationId':register.pk,
                    'PatientId': register.PatientId.PatientId if register.PatientId else None,
                    'PatientName': f"{register.PatientId.Title}.{register.PatientId.FirstName} {register.PatientId.MiddleName} {register.PatientId.SurName}" if register.PatientId else None,
                    'PhoneNo': register.PatientId.PhoneNo if register.PatientId else None,
                    'Age': register.PatientId.Age,
                    'Gender': register.PatientId.Gender,
                    'VisitId': register.VisitId,
                    'Complaint': register.Complaint,
                    # 'isMLC': register.IsMLC,
                    # 'Flagging': Flagging_name,
                    # 'FlaggingColour': Flagging_color,
                    # 'Flagging': register.Flagging,
                    'isRefferal': register.IsReferral,
                    'Status': register.Status,
                    'DoctorName': f"{register.PrimaryDoctor.Tittle}.{register.PrimaryDoctor.First_Name} {register.PrimaryDoctor.Last_Name}" if register.PrimaryDoctor else None,
                    'Specilization': str(register.Specialization.Speciality_Name) if register.Specialization else '',
                   
                   
                    'PatientType': patient_ins.PatientType,
                    'patientTypeColor':PatientType_ins.Flagg_Color,
                    'PatientCategory':patient_ins.PatientCategory,
                    'patientCategoryColor':patientCategory_ins.Flagg_Color,
                    'IsMLC':   None,
                    'MLCColor': None,
                    'specialtype' : specialtype_ins.Flagg_Name if specialtype_ins.Flagg_Name  not in specialtypelist else 'GENERAL',
                    'specialtypecolor':specialtype_ins.Flagg_Color if specialtype_ins.Flagg_Name  not in specialtypelist else '#fff'
                   
                    }
                    casuality_register_data.append(appointment_dict)
               
                   
 
            return JsonResponse(casuality_register_data, safe=False)
 
        except Exception as e:
            return JsonResponse({'error': str(e)})
 


@csrf_exempt
@require_http_methods(["GET"])
def get_patient_diagnosis_details(request):
        try:
           
            query = request.GET.get('query', '')
            status = request.GET.get('status', '')

            queryset = Patient_Diagnosis_Registration_Detials.objects.all()

            # Apply filters based on the query parameters
            if query:
                queryset = queryset.filter(
                    Q(PatientId__FirstName__icontains=query)|
                    Q(PatientId__MiddleName__icontains=query)|
                    Q(PatientId__SurName__icontains=query)|
                    Q(PatientId__PatientId__icontains=query)|
                    Q(PatientId__PhoneNo__icontains=query))
           
            if status:
                queryset = queryset.filter(Q(Status__icontains=status))


            # Serialize the filtered queryset
            diagnosis_register_data = []
            for idx, register in enumerate(queryset, start=1): 
                Flagging_name = register.Flagging.Flagg_Name if register.Flagging else None
                Flagging_color = register.Flagging.Flagg_Color if register.Flagging else None
            
                appointment_dict = {
                    'id' : idx,
                    'PatientProfile': get_file_image(register.PatientId.Patient_profile) if register.PatientId.Patient_profile else None,
                    'RegistrationId':register.pk,
                    'PatientId': register.PatientId.PatientId,
                    'PatientName': f"{register.PatientId.Title}.{register.PatientId.FirstName} {register.PatientId.MiddleName} {register.PatientId.SurName}",
                    'VisitId': register.VisitId,
                    'PhoneNo': register.PatientId.PhoneNo,
                    'Complaint': register.Complaint,
                    'isMLC': register.IsMLC,
                    'Flagging': Flagging_name,
                    'FlaggingColour': Flagging_color,
                    # 'Flagging': register.Flagging,
                    'isRefferal': register.IsReferral,
                    'Status': register.Status,
                }
                diagnosis_register_data.append(appointment_dict)

            return JsonResponse(diagnosis_register_data, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)})
        


@csrf_exempt
@require_http_methods(["GET"])
def get_patient_laboratory_details(request):
        try:
           
            query = request.GET.get('query', '')
            status = request.GET.get('status', '')

            queryset = Patient_Laboratory_Registration_Detials.objects.all()

            # Apply filters based on the query parameters
            if query:
                queryset = queryset.filter(
                    Q(PatientId__FirstName__icontains=query)|
                    Q(PatientId__MiddleName__icontains=query)|
                    Q(PatientId__SurName__icontains=query)|
                    Q(PatientId__PatientId__icontains=query)|
                    Q(PatientId__PhoneNo__icontains=query))
           
            if status:
                queryset = queryset.filter(Q(Status__icontains=status))


            # Serialize the filtered queryset
            laboratory_register_data = []
            for idx, register in enumerate(queryset, start=1): 
                Flagging_name = register.Flagging.Flagg_Name if register.Flagging else None
                Flagging_color = register.Flagging.Flagg_Color if register.Flagging else None
            
                appointment_dict = {
                    'id' : idx,
                    'PatientProfile': get_file_image(register.PatientId.Patient_profile) if register.PatientId.Patient_profile else None,
                    'RegistrationId':register.pk,
                    'PatientId': register.PatientId.PatientId,
                    'PatientName': f"{register.PatientId.Title}.{register.PatientId.FirstName} {register.PatientId.MiddleName} {register.PatientId.SurName}",
                    'PhoneNo': register.PatientId.PhoneNo,
                    'VisitId': register.VisitId,
                    'Complaint': register.Complaint,
                    'isMLC': register.IsMLC,
                    'Flagging': Flagging_name,
                    'FlaggingColour': Flagging_color,
                    # 'Flagging': register.Flagging,
                    'isRefferal': register.IsReferral,
                    'Status': register.Status,
                }
                laboratory_register_data.append(appointment_dict)

            return JsonResponse(laboratory_register_data, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)})
        
      
      
      
      

# @csrf_exempt
# @require_http_methods(["GET"])
# def get_Registration_edit_details(request):
#     try:
#         RegistrationId = request.GET.get('RegistrationId', None)
#         RegistrationType = request.GET.get('RegistrationType', None)
        
#         if not RegistrationId:
#             return JsonResponse({'error': 'RegistrationId is required'}, status=400)
        
#         if not RegistrationType:
#             return JsonResponse({'error': 'RegistrationType is required'}, status=400)
        
#         try:
#             model_class = {
#                 'OP': Patient_Appointment_Registration_Detials,
#                 'IP': Patient_IP_Registration_Detials,
#                 'Casuality': Patient_Casuality_Registration_Detials,
#                 'Diagnosis': Patient_Diagnosis_Registration_Detials,
#                 'Laboratory': Patient_Laboratory_Registration_Detials
#             }.get(RegistrationType)
                
#             if not model_class:
#                 raise ValueError("Invalid RegistrationType provided.")
            
#             RegisterModel = model_class
           
#             filters = {
#                 'OP': 'OP_Register_Id__pk',
#                 'IP': 'IP_Register_Id__pk',
#                 'Casuality': 'Casuality_Register_Id__pk',
#                 'Diagnosis': 'Diagnosis_Register_Id__pk',
#                 'Laboratory': 'Laboratory_Register_Id__pk'
#             }
#             filter_key = filters.get(RegistrationType)
#             if not filter_key:
#                 raise ValueError("Invalid RegistrationType provided.")
            
#             patient_instance = RegisterModel.objects.get(pk=RegistrationId)
#             admission_instance=None
#             admission_room_instance=None
            
#             try:
#                 referral_instance = Patient_Referral_Detials.objects.get(**{filter_key: RegistrationId})
#             except Patient_Referral_Detials.DoesNotExist:
#                 referral_instance = None
            
#             route_details = {}
            
#             if referral_instance and referral_instance.ReferredBy:
#                 doctor_profess_form_instance = Doctor_ProfessForm_Detials.objects.filter(
#                     Doctor_ID=referral_instance.ReferredBy.Doctor_ID
#                 ).first()

#                 if doctor_profess_form_instance and doctor_profess_form_instance.RouteId:
#                     route_instance = doctor_profess_form_instance.RouteId

#                     route_details = {
#                         'RouteNo': route_instance.Route_No,
#                         'RouteName': route_instance.Route_Name,
#                         'TehsilName': route_instance.Teshil_Name,
#                         'VillageName': route_instance.Village_Name,
#                     }
                
#             if RegistrationType == 'IP':
#                 admission_instance = Patient_Admission_Detials.objects.get(IP_Registration_Id__pk = RegistrationId)
#                 admission_room_instance = Patient_Admission_Room_Detials.objects.get(IP_Registration_Id__pk = RegistrationId)
             
#             IsConsciousness = "No"
#             if RegistrationType == 'Casuality':
#                 admission_room_instance = Patient_Admission_Room_Detials.objects.get(Casuality_Registration_Id__pk = RegistrationId)
#                 IsConsciousness ='Yes' if patient_instance.IsConsciousness else 'No'
            
#             Registration_dict = {
#                 'IsConsciousness':IsConsciousness,
#                 'PatientProfile': get_file_image(patient_instance.PatientId.Patient_profile) if patient_instance.PatientId.Patient_profile else None,
#                 'PatientId': patient_instance.PatientId.PatientId if patient_instance.PatientId else "",
#                 'PhoneNo': patient_instance.PatientId.PhoneNo if patient_instance.PatientId else "",
#                 'Title': patient_instance.PatientId.Title if patient_instance.PatientId else "",
#                 'FirstName': patient_instance.PatientId.FirstName if patient_instance.PatientId else "",
#                 'MiddleName': patient_instance.PatientId.MiddleName if patient_instance.PatientId else "",
#                 'SurName': patient_instance.PatientId.SurName if patient_instance.PatientId else "",
#                 'Gender': patient_instance.PatientId.Gender if patient_instance.PatientId else "",
#                 'AliasName': patient_instance.PatientId.AliasName if patient_instance.PatientId else "",
#                 'DOB': patient_instance.PatientId.DOB if patient_instance.PatientId else "",
#                 'Age': patient_instance.PatientId.Age if patient_instance.PatientId else "",
#                 'Email': patient_instance.PatientId.Email if patient_instance.PatientId else "",
#                 'BloodGroup': patient_instance.PatientId.BloodGroup if patient_instance.PatientId else "",
#                 'Occupation': patient_instance.PatientId.Occupation if patient_instance.PatientId else "",
#                 'Religion': patient_instance.PatientId.Religion.Religion_Id if patient_instance.PatientId else "",
#                 'ReligionName': patient_instance.PatientId.Religion.Religion_Name if patient_instance.PatientId else "",
#                 'Nationality': patient_instance.PatientId.Nationality if patient_instance.PatientId else "",
#                 'UniqueIdType': patient_instance.PatientId.UniqueIdType if patient_instance.PatientId else "",
#                 'UniqueIdNo': patient_instance.PatientId.UniqueIdNo if patient_instance.PatientId else "",
#                 'VisitPurpose': patient_instance.VisitPurpose if RegistrationType == 'OP' else '',
#                 'Specialization': patient_instance.Specialization.Speciality_Id if patient_instance.Specialization else '',
#                 'DoctorName': patient_instance.PrimaryDoctor.Doctor_ID if patient_instance.PrimaryDoctor else "",
#                 'Complaint': patient_instance.Complaint,
#                 'PatientType': patient_instance.PatientType,
#                 # 'PatientCategory': patient_instance.PatientCategory,
#                 'InsuranceName': patient_instance.Insurance_instance.Insurance_Name,
#                 'InsuranceType': patient_instance.insurance_type,
#                 'ClientName': patient_instance.Client_instance,
#                 'ClientType': patient_instance.ClientType,
#                 'ClientEmployeeId': patient_instance.ClientEmployeeId,
#                 'ClientEmployeeDesignation': patient_instance.ClientEmployeeDesignation,
#                 'ClientEmployeeRelation': patient_instance.ClientEmployeeRelation,
#                 'EmployeeId': patient_instance.EmployeeId.Employee_ID if patient_instance.EmployeeId else "",
#                 # 'DoctorId': patient_instance.DoctorId.Doctor_ID if patient_instance.PatientCategory == 'Doctor'and patient_instance.DoctorId else "",
#                 'DoctorRelation': patient_instance.DoctorRelation,
#                 'DonationType': patient_instance.DonationType,
#                 'IsMLC': patient_instance.IsMLC,
#                 'IsCasualityPatient': admission_instance.IsCasualityPatient if admission_instance else '' ,
#                 'Casuality_Registration_Id': admission_instance.Casuality_Registration_Id if admission_instance else '' ,
#                 'AdmissionPurpose': admission_instance.AdmissionPurpose if admission_instance else '' ,
#                 'DrInchargeAtTimeOfAdmission': admission_instance.DrInchargeAtTimeOfAdmission.Doctor_ID if admission_instance and admission_instance.DrInchargeAtTimeOfAdmission else '' ,
#                 'NextToKinName': admission_instance.NextToKinName if admission_instance else '',
#                 'Relation': admission_instance.Relation if admission_instance else '',
#                 'RelativePhoneNo': admission_instance.RelativePhoneNo if admission_instance else '',
#                 'PersonLiableForBillPayment': admission_instance.PersonLiableForPayment if admission_instance else '',
#                 'FamilyHead': admission_instance.FamilyHead if admission_instance else '',
#                 'FamilyHeadName': admission_instance.FamilyHeadName if admission_instance else '',
#                 'IpKitGiven': admission_instance.IpKitGiven if admission_instance else '',
#                 'Flagging': patient_instance.Flagging,
#                 'IsReferal': patient_instance.IsReferral,
#                 'DoorNo': patient_instance.PatientId.DoorNo if patient_instance.PatientId else "",
#                 'Street': patient_instance.PatientId.Street if patient_instance.PatientId else "",
#                 'Area': patient_instance.PatientId.Area if patient_instance.PatientId else "",
#                 'City': patient_instance.PatientId.City if patient_instance.PatientId else "",
#                 'State': patient_instance.PatientId.State if patient_instance.PatientId else "",
#                 'Country': patient_instance.PatientId.Country if patient_instance.PatientId else "",
#                 'Pincode': patient_instance.PatientId.Pincode if patient_instance.PatientId else "",
#                 'Building': admission_room_instance.RoomId.Building_Name.pk if admission_room_instance else "" ,
#                 'Block': admission_room_instance.RoomId.Block_Name.pk  if admission_room_instance else "", 
#                 'Floor': admission_room_instance.RoomId.Floor_Name.pk  if admission_room_instance else "", 
#                 'WardType': admission_room_instance.RoomId.Ward_Name.pk  if admission_room_instance else "", 
#                 'RoomType': admission_room_instance.RoomId.Room_Name.pk  if admission_room_instance else "", 
#                 'BuildingName': admission_room_instance.RoomId.Building_Name.Building_Name if admission_room_instance else "" ,
#                 'BlockName': admission_room_instance.RoomId.Block_Name.Block_Name  if admission_room_instance else "", 
#                 'FloorName': admission_room_instance.RoomId.Floor_Name.Floor_Name  if admission_room_instance else "", 
#                 'WardTypeName': admission_room_instance.RoomId.Ward_Name.Ward_Name  if admission_room_instance else "", 
#                 'RoomTypeName': admission_room_instance.RoomId.Room_Name.Room_Name  if admission_room_instance else "", 
#                 'RoomNo': admission_room_instance.RoomId.Room_No  if admission_room_instance else "", 
#                 'BedNo': admission_room_instance.RoomId.Bed_No  if admission_room_instance else "", 
#                 'RoomId': admission_room_instance.RoomId.pk if admission_room_instance else ""  
#             }
#             if referral_instance:
#                 Registration_dict.update({
#                     'ReferralSource': referral_instance.ReferralSource,
#                     'ReferredBy': referral_instance.ReferredBy.Doctor_ID if referral_instance.ReferredBy else '',
#                     'ReferralRegisteredBy': referral_instance.ReferralRegisteredBy,
#                 })
#             Registration_dict.update(route_details)
                
#             return JsonResponse(Registration_dict)
#         except RegisterModel.DoesNotExist:
#             return JsonResponse({'error': 'Record not found'}, status=404)
      
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)

  





# @csrf_exempt
# @require_http_methods(["GET"])
# def get_patient_visit_details(request):
#     try:
#         PatientId = request.GET.get('PatientId', '')
#         FirstName = request.GET.get('FirstName', '')
#         PhoneNo = request.GET.get('PhoneNo', '')
#         DoctorId = request.GET.get('DoctorId','')
#         Speciality = request.GET.get('Speciality','')
        
#         print('DoctorIddddddd',DoctorId)

#         # Fetch the patient record
#         patient = Patient_Detials.objects.filter(Q(PhoneNo=PhoneNo, FirstName=FirstName) | Q(PatientId=PatientId)).first()
#         print('111111',patient)
#         if patient:
#             # Fetch the latest appointment for the patient
#             # latest_appointment = Patient_Appointment_Registration_Detials.objects.filter(PatientId=patient,VisitPurpose='NewConsultation', PrimaryDoctor__Doctor_ID = DoctorId,Specialization__pk=Speciality).order_by('-created_at').first()
#             # print('---',latest_appointment.pk)
#             latest_appointment = Patient_Appointment_Registration_Detials.objects.filter(
#                 PatientId=patient,
#                 # VisitPurpose='NewConsultation',
#                 PrimaryDoctor__Doctor_ID=DoctorId,
#                 Specialization__Speciality_Id=Speciality
#             ).order_by('-created_at').first()
           
#             print(f"Query Parameters - PatientId: {patient}, DoctorId: {DoctorId}, Speciality: {Speciality}")
#             print(f"Latest Appointment: {latest_appointment}")

#             # if latest_appointment and latest_appointment.VisitPurpose != 'NewConsultation':
#             if latest_appointment:
#                 # if Patient_Appointment_Registration_Detials.objects.exclude(pk = latest_appointment.pk,Status= 'Cancelled' or 'Registered').exists():
                    
#                 # if Patient_Appointment_Registration_Detials.objects.exclude(pk=latest_appointment.pk).filter(~Q(Status='Cancelled') & ~Q(Status='Registered')).exists():
#                 print('4444444444444444444444')
#                 excluded_appointments = Patient_Appointment_Registration_Detials.objects.exclude(pk=latest_appointment.pk)
#                 print(f"Excluded Appointments: {excluded_appointments}")

#                 valid_appointments = excluded_appointments.filter(~Q(Status='Cancelled') & ~Q(Status='Registered'))
#                 print(f"Valid Appointments: {valid_appointments}")
                
#                 if valid_appointments.exists():

#                     print('--00')
#                     # Calculate the time difference between now and the last visit
#                     days_since_last_visit = (datetime.now() - latest_appointment.created_at).days
#                     print(f"Days Since Last Visit: {days_since_last_visit}")
#                     if days_since_last_visit <= 5:
#                         pat_ins = 'FollowUp - No Fee'
#                     elif days_since_last_visit <= 60:
#                         pat_ins = 'FollowUp - FollowUp Fee'
#                     else:
#                         pat_ins = 'NewConsultation'
#                 else:
#                         pat_ins = 'NewConsultation'
#             else:
#                 pat_ins = 'NewConsultation'
#         else:
#             pat_ins = 'NewConsultation'

#         print(f"Latest Appointment: {latest_appointment}")
#         print(f"Excluded Appointments: {excluded_appointments}")
#         print(f"Valid Appointments: {valid_appointments}")
#         print(f"Visit Purpose: {pat_ins}")
    

#         return JsonResponse({'VisitPurpose': pat_ins})

#     except Exception as e:
#         return JsonResponse({'error': str(e)})




@csrf_exempt
@require_http_methods(["GET"])
def get_patient_visit_details(request):
    try:
        # Extract query parameters
        PatientId = request.GET.get('PatientId', '')
        FirstName = request.GET.get('FirstName', '')
        PhoneNo = request.GET.get('PhoneNo', '')
        DoctorId = request.GET.get('DoctorId', '')
        Speciality = request.GET.get('Speciality', '')

        print('DoctorId:', DoctorId)

        # Fetch the patient record
        patient = Patient_Detials.objects.filter(
            Q(PhoneNo=PhoneNo, FirstName=FirstName) | Q(PatientId=PatientId)
        ).first()
        print('Patient Record:', patient)

        if patient:
            # Fetch the latest appointment for the patient
            latest_appointment = Patient_Appointment_Registration_Detials.objects.filter(
                PatientId=patient,
                PrimaryDoctor__Doctor_ID=DoctorId,
                Specialization__Speciality_Id=Speciality
            ).order_by('-created_at').first()

            print(f"Query Parameters - PatientId: {patient}, DoctorId: {DoctorId}, Speciality: {Speciality}")
            print(f"Latest Appointment: {latest_appointment}")

            if latest_appointment:
                # Calculate the time difference between now and the last visit
                days_since_last_visit = (datetime.now() - latest_appointment.created_at).days
                print(f"Days Since Last Visit: {days_since_last_visit}")

                # Determine the Visit Purpose based on Status and Days
                if latest_appointment.Status not in ['Cancelled', 'Registered']:
                    if days_since_last_visit <= 5:
                        pat_ins = 'FollowUp - No Fee'
                    elif days_since_last_visit <= 60:
                        pat_ins = 'FollowUp-FolUp Fee'
                    else:
                        pat_ins = 'NewConsultation'
                else:
                    pat_ins = 'NewConsultation'
            else:
                pat_ins = 'NewConsultation'
        else:
            pat_ins = 'NewConsultation'

        print(f"Visit Purpose: {pat_ins}")
        return JsonResponse({'VisitPurpose': pat_ins})

    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'error': str(e)})




# @csrf_exempt
# @require_http_methods(["GET"])
# def get_ip_registration_before_handover_details(request):
#         try:
           
#             query = request.GET.get('query', '')
#             status = request.GET.get('status', '')
#             Booking_Status = 'Booked' if status == 'Pending' else ('Occupied' if status == 'Admitted' else 'Cancelled')

#             queryset = Patient_IP_Registration_Detials.objects.all()
            
#             Insurance_instance = Insurance_Master_Detials.objects.all() 
#             print(Insurance_instance,'Insurance_instance')
            
#             Client_instance = Client_Master_Detials.objects.all()
#             print(Client_instance,'Client_instance')
            
#             # Apply filters based on the query parameters
#             if query:
#                 queryset = queryset.filter(
#                     Q(PatientId_FirstName_icontains=query)|
#                     Q(PatientId_MiddleName_icontains=query)|
#                     Q(PatientId_SurName_icontains=query)|
#                     Q(PatientId_PatientId_icontains=query)|
#                     Q(PatientId_PhoneNo_icontains=query)
#                     ).filter(Booking_Status=Booking_Status)
           
#             if status:
#                 queryset = queryset.filter(Q(Status__icontains=status)).filter(Booking_Status=Booking_Status)
            
            

#             # Serialize the filtered queryset
#             ip_register_data = []
#             for idx, register in enumerate(queryset,start=1): 
#                 client_name = register.ClientName.Client_Name if register.ClientName else None
#                 insurance_name = register.InsuranceName.Insurance_Name if register.InsuranceName else None

#                 appointment_dict = {
#                     'id' : idx,
#                     'PatientProfile': get_file_image(register.PatientId.Patient_profile) if register.PatientId.Patient_profile else None,
#                     'RegistrationId':register.Registration_Id,
#                     'PatientId': register.PatientId.PatientId,
#                     'PatientName': f"{register.PatientId.Title}.{register.PatientId.FirstName} {register.PatientId.MiddleName} {register.PatientId.SurName}",
#                     'PhoneNo': register.PatientId.PhoneNo,
#                     'Age': register.PatientId.Age,
#                     'Gender': register.PatientId.Gender,
#                     'BloodGroup': register.PatientId.BloodGroup,
#                     'Complaint': register.Complaint,
#                     'isMLC': register.IsMLC,
#                     'Flagging': register.Flagging,
#                     'isRefferal': register.IsReferral,
#                     'ClientName': register.client_name,
#                     'InsuranceName': register.insurance_name,
#                     'Status': register.Status,
#                     'DoctorName': f"{register.PrimaryDoctor.Tittle}.{register.PrimaryDoctor.First_Name} {register.PrimaryDoctor.Last_Name}",
#                     'Specilization': str(register.Specialization.Speciality_Name) if register.Specialization else '',
#                 }
#                 if register.Booking_Status in ['Booked','Occupied']:
#                     roomdetials=Patient_Admission_Room_Detials.objects.filter(IP_Registration_Id=register).order_by('-created_by').first()
#                     appointment_dict['BuildingName']=roomdetials.RoomId.Building_Name.Building_Name
#                     appointment_dict['BlockName']=roomdetials.RoomId.Block_Name.Block_Name
#                     appointment_dict['FloorName']=roomdetials.RoomId.Floor_Name.Floor_Name
#                     appointment_dict['WardName']=roomdetials.RoomId.Ward_Name.Ward_Name
#                     appointment_dict['RoomName']=roomdetials.RoomId.Room_Name.Room_Name
#                     appointment_dict['RoomNo']=roomdetials.RoomId.Room_No
#                     appointment_dict['BedNo']=roomdetials.RoomId.Bed_No
#                     appointment_dict['RoomId']=roomdetials.RoomId.Room_Id
#                 ip_register_data.append(appointment_dict)

#             return JsonResponse(ip_register_data, safe=False)

#         except Exception as e:
#             return JsonResponse({'error': str(e)})

# @csrf_exempt
# @require_http_methods(["GET"])
# def get_ip_registration_before_handover_details(request):
#     try:
#         query = request.GET.get('query', '')
#         status = request.GET.get('status', '')

#         # Map status to Booking_Status
#         Booking_Status = 'Booked' if status == 'Pending' else ('Occupied' if status == 'Admitted' else 'Cancelled')

#         queryset = Patient_IP_Registration_Detials.objects.all()

#         # Apply filters based on the query parameters
#         if query:
#             queryset = queryset.filter(
#                 Q(PatientId_FirstName_icontains=query) |
#                 Q(PatientId_MiddleName_icontains=query) |
#                 Q(PatientId_SurName_icontains=query) |
#                 Q(PatientId_PatientId_icontains=query) |
#                 Q(PatientId_PhoneNo_icontains=query)
#             ).filter(Booking_Status=Booking_Status)

#         if status:
#             queryset = queryset.filter(Q(Status__icontains=status)).filter(Booking_Status=Booking_Status)

#         # Serialize the filtered queryset
#         ip_register_data = []
#         for idx, register in enumerate(queryset, start=1):
#             client_name = register.ClientName.Client_Name if register.ClientName else None
#             insurance_name = register.InsuranceName.Insurance_Name if register.InsuranceName else None
#             Flagging_name = register.Flagging.Flagg_Name if register.Flagging else None
#             Flagging_color = register.Flagging.Flagg_Color if register.Flagging else None
#             BloodGroup_name = register.PatientId.BloodGroup.BloodGroup_Name if register.PatientId.BloodGroup else None
            
#             appointment_dict = {
#                 'id': idx,
#                 'PatientProfile': get_file_image(register.PatientId.Patient_profile) if register.PatientId.Patient_profile else None,
#                 'RegistrationId': register.Registration_Id,
#                 'PatientId': register.PatientId.PatientId,
#                 'PatientName': f"{register.PatientId.Title}.{register.PatientId.FirstName} {register.PatientId.MiddleName} {register.PatientId.SurName}",
#                 'PhoneNo': register.PatientId.PhoneNo,
#                 'Age': register.PatientId.Age,
#                 'Gender': register.PatientId.Gender,
#                 'BloodGroup': BloodGroup_name,
#                 'Complaint': register.Complaint,
#                 'isMLC': register.IsMLC,
#                 'Flagging': Flagging_name,
#                 'FlaggingColour': Flagging_color,
#                 # 'Flagging': register.Flagging,
#                 'isRefferal': register.IsReferral,
#                 'ClientName': client_name,  # Fixed reference
#                 'InsuranceName': insurance_name,  # Fixed reference
#                 'Status': register.Status,
#                 'DoctorName': f"{register.PrimaryDoctor.Tittle}.{register.PrimaryDoctor.First_Name} {register.PrimaryDoctor.Last_Name}" if register.PrimaryDoctor else '',
#                 'Specilization': str(register.Specialization.Speciality_Name) if register.Specialization else '',
#             }

#             # Add room details if Booking_Status is 'Booked' or 'Occupied'
#             if register.Booking_Status in ['Booked', 'Occupied']:
#                 roomdetials = Patient_Admission_Room_Detials.objects.filter(IP_Registration_Id=register).order_by('-created_by').first()

#                 if roomdetials:
#                     appointment_dict['BuildingName'] = roomdetials.RoomId.Building_Name.Building_Name if roomdetials.RoomId.Building_Name else None
#                     appointment_dict['BlockName'] = roomdetials.RoomId.Block_Name.Block_Name if roomdetials.RoomId.Block_Name else None
#                     appointment_dict['FloorName'] = roomdetials.RoomId.Floor_Name.Floor_Name if roomdetials.RoomId.Floor_Name else None
#                     appointment_dict['WardName'] = roomdetials.RoomId.Ward_Name.Ward_Name if roomdetials.RoomId.Ward_Name else None
#                     appointment_dict['RoomName'] = roomdetials.RoomId.Room_Name.Room_Name if roomdetials.RoomId.Room_Name else None
#                     appointment_dict['RoomNo'] = roomdetials.RoomId.Room_No if roomdetials.RoomId.Room_No else None
#                     appointment_dict['BedNo'] = roomdetials.RoomId.Bed_No if roomdetials.RoomId.Bed_No else None
#                     appointment_dict['RoomId'] = roomdetials.RoomId.Room_Id if roomdetials.RoomId.Room_Id else None

#             ip_register_data.append(appointment_dict)

#         return JsonResponse(ip_register_data, safe=False)

#     except Exception as e:
#         return JsonResponse({'error': str(e)})




@csrf_exempt
@require_http_methods(["GET"])
def get_ip_registration_before_handover_details(request):
    try:
        query = request.GET.get('query', '')
        status = request.GET.get('status', '')

        # Map status to Booking_Status
        Booking_Status = 'Booked' if status == 'Pending' else ('Occupied' if status == 'Admitted' else 'Cancelled')

        queryset = Patient_IP_Registration_Detials.objects.all()

        # Apply filters based on the query parameters
        if query:
            queryset = queryset.filter(
                Q(PatientId_FirstName_icontains=query) |
                Q(PatientId_MiddleName_icontains=query) |
                Q(PatientId_SurName_icontains=query) |
                Q(PatientId_PatientId_icontains=query) |
                Q(PatientId_PhoneNo_icontains=query)
            ).filter(Booking_Status=Booking_Status)

        if status:
            queryset = queryset.filter(Q(Status__icontains=status)).filter(Booking_Status=Booking_Status)

        # Serialize the filtered queryset
        ip_register_data = []
        for idx, register in enumerate(queryset, start=1):
            # client_name = register.ClientName.Client_Name if register.ClientName else None
            # insurance_name = register.InsuranceName.Insurance_Name if register.InsuranceName else None
            Flagging_name = register.Flagging.Flagg_Name if register.Flagging else None
            Flagging_color = register.Flagging.Flagg_Color if register.Flagging else None
            BloodGroup_name = register.PatientId.BloodGroup.BloodGroup_Name if register.PatientId.BloodGroup else None
            
            appointment_dict = {
                'id': idx,
                'PatientProfile': get_file_image(register.PatientId.Patient_profile) if register.PatientId.Patient_profile else None,
                'RegistrationId': register.Registration_Id,
                'PatientId': register.PatientId.PatientId,
                'PatientName': f"{register.PatientId.Title.Title_Name}.{register.PatientId.FirstName} {register.PatientId.MiddleName} {register.PatientId.SurName}",
                'PhoneNo': register.PatientId.PhoneNo,
                'Age': register.PatientId.Age,
                'Gender': register.PatientId.Gender,
                'BloodGroup': BloodGroup_name,
                'Complaint': register.Complaint,
                'isMLC': register.IsMLC,
                'Flagging': Flagging_name,
                'FlaggingColour': Flagging_color,
                # 'Flagging': register.Flagging,
                'isRefferal': register.IsReferral,
                # 'ClientName': client_name,  # Fixed reference
                # 'InsuranceName': insurance_name,  # Fixed reference
                'Status': register.Status,
                'DoctorName': f"{register.PrimaryDoctor.Tittle.Title_Name}.{register.PrimaryDoctor.First_Name} {register.PrimaryDoctor.Last_Name}" if register.PrimaryDoctor else '',
                'Specilization': str(register.Specialization.Speciality_Name) if register.Specialization else '',
            }

            # Add room details if Booking_Status is 'Booked' or 'Occupied'
            if register.Booking_Status in ['Booked', 'Occupied']:
                roomdetials = Patient_Admission_Room_Detials.objects.filter(IP_Registration_Id=register).order_by('-created_by').first()

                if roomdetials:
                    appointment_dict['BuildingName'] = roomdetials.RoomId.Building_Name.Building_Name if roomdetials.RoomId else None
                    appointment_dict['BlockName'] = roomdetials.RoomId.Block_Name.Block_Name if roomdetials.RoomId else None
                    appointment_dict['FloorName'] = roomdetials.RoomId.Floor_Name.Floor_Name if roomdetials.RoomId else None
                    appointment_dict['WardName'] = roomdetials.RoomId.Ward_Name.Ward_Name.Ward_Name if roomdetials.RoomId else None
                    # appointment_dict['RoomName'] = roomdetials.RoomId.Room_Name.Room_Name if roomdetials.RoomId.Room_Name else None
                    appointment_dict['RoomNo'] = roomdetials.RoomId.Room_No if roomdetials.RoomId else None
                    appointment_dict['BedNo'] = roomdetials.RoomId.Bed_No if roomdetials.RoomId else None
                    appointment_dict['RoomId'] = roomdetials.RoomId.Room_Id if roomdetials.RoomId else None

            ip_register_data.append(appointment_dict)

        return JsonResponse(ip_register_data, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)})






@csrf_exempt
@require_http_methods(["GET"])
def get_ip_roomdetials_before_handover_details(request):
    try:
        RegistrationId = request.GET.get('RegistrationId', '')

        # Get the first room detail entry
        roomdetials = Patient_Admission_Room_Detials.objects.filter(IP_Registration_Id__pk=RegistrationId).earliest('created_at')
       
        ip_register_data = {
            'ip_register_data':[],
            'Roomsdata':[],
        }
        if roomdetials:
            data={
            'BuildingName': roomdetials.RoomId.Building_Name.Building_Name,
            'BlockName': roomdetials.RoomId.Block_Name.Block_Name,
            'FloorName': roomdetials.RoomId.Floor_Name.Floor_Name,
            'WardName': roomdetials.RoomId.Ward_Name.Ward_Name.Ward_Name,
            # 'RoomName': roomdetials.RoomId.Room_Name.Room_Name,
            'RoomNo': roomdetials.RoomId.Room_No,
            'BedNo': roomdetials.RoomId.Bed_No,
            'RoomId': roomdetials.RoomId.pk,
            'DateTime': roomdetials.created_at.strftime('%d-%m-%y - %H-%M'),
            'id':1
            }
            ip_register_data['ip_register_data'].append(data)
            

        # Fetch all room details and add the remaining ones to the Roomsdata list
        roomdatass = Patient_Admission_Room_Detials.objects.filter(IP_Registration_Id__pk=RegistrationId).order_by('created_at')[1:]  # Skip the first entry
        index=0
        for roomdetials in roomdatass:
            data = {}
            data['BuildingName'] = roomdetials.RoomId.Building_Name.Building_Name
            data['BlockName'] = roomdetials.RoomId.Block_Name.Block_Name
            data['FloorName'] = roomdetials.RoomId.Floor_Name.Floor_Name
            data['WardName'] = roomdetials.RoomId.Ward_Name.Ward_Name.Ward_Name
            # data['RoomName'] = roomdetials.RoomId.Room_Name.Room_Name
            data['RoomNo'] = roomdetials.RoomId.Room_No
            data['BedNo'] = roomdetials.RoomId.Bed_No
            data['RoomId'] = roomdetials.RoomId.Room_Id
            data['DateTime'] = roomdetials.created_at.strftime('%d-%m-%y - %H-%M')
            data['id'] = index+1
            
            
            ip_register_data['Roomsdata'].append(data)
            index += 1

        return JsonResponse(ip_register_data, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def post_ip_roomdetials_before_handover_details(request):
    try:
        data = json.loads(request.body)
        RegistrationId = data.get('RegistrationId', '')
        RoomId = data.get('RoomId', '')
        createdby = data.get('createdby', '')
        
        if RoomId:
            room_ins = Room_Master_Detials.objects.get(pk=RoomId)
        else:
            return JsonResponse({'error': 'RoomId is required'}, status=400)

        if RegistrationId:
            register_ins = Patient_IP_Registration_Detials.objects.get(pk=RegistrationId)
        else:
            return JsonResponse({'error': 'RegistrationId is required'}, status=400)
        
        if room_ins and register_ins:
            previous_room_detail = Patient_Admission_Room_Detials.objects.filter(
                    IP_Registration_Id=register_ins
                ).order_by('-created_at').first()
            if previous_room_detail:
                                
                previous_room_detail.RoomId.Booking_Status = 'Available'
                previous_room_detail.RoomId.save()
                
            # Create a new Patient_Admission_Room_Detials entry
            Patient_Admission_Room_Detials.objects.create(
                RegisterType='IP',
                IP_Registration_Id=register_ins,  # Corrected field name
                Casuality_Registration_Id=None,
                RoomId=room_ins,
                created_by=createdby
            )
            
            

        return JsonResponse({'success': 'Room changed successfully'}, safe=False)

    except Room_Master_Detials.DoesNotExist:
        return JsonResponse({'error': 'Room does not exist'}, status=404)

    except Patient_IP_Registration_Detials.DoesNotExist:
        return JsonResponse({'error': 'IP Registration does not exist'}, status=404)

    except Exception as e:
        return JsonResponse({'error': str(e)},status=500)



@csrf_exempt
@require_http_methods(["POST","GET","OPTIONS"])
def post_ip_handover_details(request):
    if request.method=="POST":
        try:
            data = json.loads(request.body)
            RegistrationId = data.get('RegistrationId', '')
            ReasonForAdmission = data.get('ReasonForAdmission', '')
            PatientConditionOnAdmission = data.get('PatientConditionOnAdmission', '')
            PatientFileGiven = data.get('PatientFileGiven', '')
            AadharGiven = data.get('AadharGiven', '')
            created_by = data.get('created_by', '')
            
            
            if RegistrationId:
                register_ins = Patient_IP_Registration_Detials.objects.get(pk=RegistrationId)
            else:
                return JsonResponse({'error': 'RegistrationId is required'}, status=400)
            
            
            Handover_detials_Ip.objects.create(
                RegistrationId=register_ins, 
                ReasonForAdmission=ReasonForAdmission,
                PatientConditionOnAdmission=PatientConditionOnAdmission,
                PatientFileGiven= True if PatientFileGiven=='Yes' else False,
                AadharGiven=True if AadharGiven=='Yes' else False,
                created_by=created_by
            )
                
                

            return JsonResponse({'success': 'Detials added successfully'}, safe=False)

        except Patient_IP_Registration_Detials.DoesNotExist:
            return JsonResponse({'error': 'IP Registration does not exist'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    elif request.method=='GET':
        try:
            RegistrationId=request.GET.get('RegistrationId')
            
            handoverdetial_ins = Handover_detials_Ip.objects.filter(RegistrationId__pk = RegistrationId).first()
            if handoverdetial_ins:
                data={
                    'ReasonForAdmission':handoverdetial_ins.ReasonForAdmission,
                    'PatientConditionOnAdmission':handoverdetial_ins.PatientConditionOnAdmission,
                    'PatientFileGiven': 'Yes' if handoverdetial_ins.ReasonForAdmission else 'No',
                    'AadharGiven': 'Yes' if handoverdetial_ins.AadharGiven else 'No',
                    'created_by':handoverdetial_ins.created_by,
                    'RegistrationId':handoverdetial_ins.RegistrationId.pk,
                    'Date': handoverdetial_ins.created_at.strftime('%d-%m-%y'), 
                    'Time' : handoverdetial_ins.created_at.strftime('%H:%M:%S')
                }
                return JsonResponse(data)
            else:
                return JsonResponse({})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)





@csrf_exempt
@require_http_methods(["POST"])
def post_ip_submit_handover_or_cancel_details(request):
    try:
        data = json.loads(request.body)
        RegistrationId = data.get('RegistrationId', '')
        Type = data.get('type', '')
        Reason = data.get('Reason', '')
        createdby = data.get('createdby', '')

        if not RegistrationId:
            return JsonResponse({'error': 'RegistrationId is required'}, status=400)

        try:
            ip_regis_ins = Patient_IP_Registration_Detials.objects.get(pk=RegistrationId)
        except Patient_IP_Registration_Detials.DoesNotExist:
            return JsonResponse({'error': 'IP Registration does not exist'}, status=404)

        if Type != 'cancel':
            # If not cancel, admit the patient
            ip_regis_ins.Status = 'Admitted'
            ip_regis_ins.Booking_Status = 'Occupied'
            ip_regis_ins.save()  # Save the changes

            # Get the latest room details
            ip_add_room_ins = Patient_Admission_Room_Detials.objects.filter(
                RegisterType="IP",
                IP_Registration_Id=ip_regis_ins
            ).order_by('-created_at').first()

            if ip_add_room_ins:
                ip_add_room_ins.Status = True
                ip_add_room_ins.IsStayed = True
                ip_add_room_ins.CurrentlyStayed = True
                ip_add_room_ins.Approved_by = createdby
                ip_add_room_ins.Admitted_Date = datetime.now()
                ip_add_room_ins.save()

                room_ins = Room_Master_Detials.objects.get(pk=ip_add_room_ins.RoomId.pk)
                room_ins.Booking_Status = 'Occupied'
                room_ins.save()

            return JsonResponse({'success': 'Patient admitted successfully'})

        else:
            # If cancel, cancel the admission if the status is pending
            if ip_regis_ins.Status == 'Pending':
                ip_regis_ins.Status = 'Cancelled'
                ip_regis_ins.Booking_Status = 'Cancelled'
                ip_regis_ins.Reason = Reason
                ip_regis_ins.save()  # Save the changes

                # Get the latest room details
                ip_add_room_ins = Patient_Admission_Room_Detials.objects.filter(
                    RegisterType="IP",
                    IP_Registration_Id=ip_regis_ins
                ).order_by('-created_at').first()

                if ip_add_room_ins:
                    ip_add_room_ins.Iscanceled = True
                    ip_add_room_ins.Approved_by = createdby
                    ip_add_room_ins.save()

                    room_ins = Room_Master_Detials.objects.get(pk=ip_add_room_ins.RoomId.pk)
                    room_ins.Booking_Status = 'Available'
                    room_ins.save()

                return JsonResponse({'success': 'Patient admission cancelled successfully'})
            else:
                return JsonResponse({'warn': 'Patient is already admitted, cannot cancel the admission'}, status=400)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# @csrf_exempt
# @require_http_methods(["POST", "GET", "OPTIONS"])
# def insert_op_ip_convertion(request):
#     if request.method == "POST":
#         try:
#             # Load the request body as JSON
#             data = json.loads(request.body)

#             # Ensure data is a dictionary
#             if isinstance(data, dict):
#                 patient_id_str = data.get('Patient_id')
#                 registration_id = data.get('Registration_id')
#                 reason = data.get('Reason')
#                 created_by = data.get('Created_by')

#                 # Retrieve the Patient_Detials instance
#                 try:
#                     patient_instance = Patient_Detials.objects.get(pk=patient_id_str)
#                 except Patient_Detials.DoesNotExist:
#                     return JsonResponse({'error': 'Patient ID not found'}, status=404)

#                 # Check if the patient has already been admitted
#                 alertdata = Op_to_Ip_Convertion_Table.objects.filter(Registration_id=registration_id)

#                 if alertdata.exists():
#                     return JsonResponse({'warn': 'Patient already admitted'})

#                 # Retrieve the Patient_Appointment_Registration_Detials instance
#                 try:
#                     registration_instance = Patient_Appointment_Registration_Detials.objects.get(pk=registration_id)
#                 except Patient_Appointment_Registration_Detials.DoesNotExist:
#                     return JsonResponse({'error': 'Registration ID not found'}, status=404)

#                 # Save the data in the Op_to_Ip_Convertion_Table if the patient is not already admitted
#                 convertion_data = Op_to_Ip_Convertion_Table(
#                     Patient_Id=patient_instance,  # Use the instance instead of the ID
#                     Registration_id=registration_instance,  # Use the instance instead of the ID
#                     Reason=reason,
#                     created_by=created_by,  # Assuming Created_by is just a string or user ID
#                     Status = 'Pending'
#                 )
#                 convertion_data.save()
                
#                 return JsonResponse({'success': 'Request Que added successfully'})
#             else:
#                 # If data is not a dictionary, it's an error in the request format
#                 return JsonResponse({'error': 'Invalid data format'}, status=400)
        
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON format'}, status=400)

#         except Exception as e:
#             print(f"An error occurred: {str(e)}")
#             return JsonResponse({'error': 'An internal server error occurred'}, status=500)
        
#     elif request.method == 'GET':
#         try:
#             status = request.GET.get('status')
            
#             requestdata = Op_to_Ip_Convertion_Table.objects.filter(Status=status)
#             Requestlist = []

#             for data in requestdata:
#                 patient_details = data.Registration_id.PatientId  # Assuming this is a ForeignKey to Patient_Detials
#                 request = {
#                     'id' : data.id,
#                     'PatientId': patient_details.pk,  # Use the primary key of the patient
#                     'RegistrationId': data.Registration_id.pk,  # Use the primary key of the registration
#                     'Reason': data.Reason,
#                     'Patient_Name': f'{patient_details.FirstName} {patient_details.MiddleName} {patient_details.SurName}',
#                     'Age': patient_details.Age,
#                     'Status' : data.Status
#                 }
#                 Requestlist.append(request)

#             return JsonResponse(Requestlist, safe=False)

#         except Exception as e:
#             print(f'An error occurred: {str(e)}')
#             return JsonResponse({'error': 'An internal server error occurred'}, status=500)





@csrf_exempt
@require_http_methods(["POST", "GET", "OPTIONS"])
def insert_op_ip_convertion(request):
    if request.method == "POST":
        try:
            # Load the request body as JSON
            data = json.loads(request.body)

            # Ensure data is a dictionary
            if isinstance(data, dict):
                patient_id_str = data.get('Patient_id')
                registration_id = data.get('Registration_id')
                reason = data.get('Reason')
                IpNotes = data.get('IpNotes')
                created_by = data.get('Created_by')

                # Retrieve the Patient_Detials instance
                try:
                    patient_instance = Patient_Detials.objects.get(pk=patient_id_str)
                except Patient_Detials.DoesNotExist:
                    return JsonResponse({'error': 'Patient ID not found'}, status=404)

                # Check if the patient has already been admitted
                alertdata = Op_to_Ip_Convertion_Table.objects.filter(Registration_id=registration_id)

                if alertdata.exists():
                    return JsonResponse({'warn': 'Patient already admitted'})

                # Retrieve the Patient_Appointment_Registration_Detials instance
                try:
                    registration_instance = Patient_Appointment_Registration_Detials.objects.get(pk=registration_id)
                except Patient_Appointment_Registration_Detials.DoesNotExist:
                    return JsonResponse({'error': 'Registration ID not found'}, status=404)

                # Save the data in the Op_to_Ip_Convertion_Table if the patient is not already admitted
                convertion_data = Op_to_Ip_Convertion_Table(
                    Patient_Id=patient_instance,  # Use the instance instead of the ID
                    Registration_id=registration_instance,  # Use the instance instead of the ID
                    Reason=reason,
                    IpNotes=IpNotes,
                    created_by=created_by,  # Assuming Created_by is just a string or user ID
                    Status = 'Pending'
                )
                convertion_data.save()
                
                return JsonResponse({'success': 'Request Que added successfully'})
            else:
                # If data is not a dictionary, it's an error in the request format
                return JsonResponse({'error': 'Invalid data format'}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
        
    elif request.method == 'GET':
        try:
            requestdata = Op_to_Ip_Convertion_Table.objects.filter(Status='Pending')
            Requestlist = []

            for data in requestdata:
                patient_details = data.Registration_id.PatientId  # Assuming this is a ForeignKey to Patient_Detials
                request = {
                    'id' : data.id,
                    'PatientId': patient_details.pk,  # Use the primary key of the patient
                    'Registration_id': data.Registration_id.pk,  # Use the primary key of the registration
                    'Reason': data.Reason,
                    'IpNotes': data.IpNotes,
                    'Patient_Name': f'{patient_details.FirstName} {patient_details.MiddleName} {patient_details.SurName}',
                    'Age': patient_details.Age,
                    'Status' : data.Status
                }
                Requestlist.append(request)

            return JsonResponse(Requestlist, safe=False)

        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)






@csrf_exempt
@require_http_methods(["GET"])
def get_ip_roomdetials_for_bedtransfer_details(request):
    try:
        RegistrationId = request.GET.get('RegistrationId', '')

        # Get the first room detail entry
        roomdetials = Patient_Admission_Room_Detials.objects.filter(IP_Registration_Id__pk=RegistrationId,Status=True,IsStayed=True,CurrentlyStayed=True).order_by('-created_at').first()
       
        ip_register_data = {
            'ip_register_data':[],
            'Roomsdata':[],
        }
        if roomdetials:
            data={
            'BuildingName': roomdetials.RoomId.Building_Name.Building_Name,
            'BlockName': roomdetials.RoomId.Block_Name.Block_Name,
            'FloorName': roomdetials.RoomId.Floor_Name.Floor_Name,
            'WardName': roomdetials.RoomId.Ward_Name.Ward_Name.Ward_Name,
            # 'RoomName': roomdetials.RoomId.Room_Name.Room_Name,
            'RoomNo': roomdetials.RoomId.Room_No,
            'BedNo': roomdetials.RoomId.Bed_No,
            'RoomId': roomdetials.RoomId.pk,
            'Admitted_Date': roomdetials.Admitted_Date,
            'DateTime': roomdetials.created_at.strftime('%d-%m-%y / %H-%M'),
            'AdmitDate': roomdetials.Admitted_Date.strftime('%d-%m-%y'),
            'pk':roomdetials.pk,
            'id':1,
            
            }
            ip_register_data['ip_register_data'].append(data)
            

        # Fetch all room details and add the remaining ones to the Roomsdata list
        roomdatass = Patient_Admission_Room_Detials.objects.filter(IP_Registration_Id__pk=RegistrationId,Status=True).exclude(CurrentlyStayed=True).order_by('-created_at')  # Skip the first entry
        index=0
        for roomdetials in roomdatass:
            ststusss=''
            if  roomdetials.IsStayed and not roomdetials.Iscanceled:
                ststusss='Transfered'
            elif not roomdetials.IsStayed and not roomdetials.Iscanceled:
                ststusss='Requested'
            elif not roomdetials.IsStayed and  roomdetials.Iscanceled :
                ststusss='Requested Cancelled'
            data = {}
            data['BuildingName'] = roomdetials.RoomId.Building_Name.Building_Name
            data['BlockName'] = roomdetials.RoomId.Block_Name.Block_Name
            data['FloorName'] = roomdetials.RoomId.Floor_Name.Floor_Name
            data['WardName'] = roomdetials.RoomId.Ward_Name.Ward_Name.Ward_Name
            # data['RoomName'] = roomdetials.RoomId.Room_Name.Room_Name
            data['RoomNo'] = roomdetials.RoomId.Room_No
            data['BedNo'] = roomdetials.RoomId.Bed_No
            data['RoomId'] = roomdetials.RoomId.Room_Id
            data['Admitted_Date'] = roomdetials.Admitted_Date.strftime('%d-%m-%y /  %I-%M %p') if roomdetials.Admitted_Date else ""
            data['Discharge_Date'] = roomdetials.Discharge_Date.strftime('%d-%m-%y / %I-%M %p') if roomdetials.Discharge_Date else ""
            data['Status'] = ststusss
            data['pk'] = roomdetials.pk
            data['DateTime'] = roomdetials.created_at.strftime('%d-%m-%y / %I-%M %p')
            data['id'] = index+1
            
            
            ip_register_data['Roomsdata'].append(data)
            index += 1

        return JsonResponse(ip_register_data, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)})





@csrf_exempt
@require_http_methods(["POST"])
def post_ip_bed_transfer_details(request):
    try:
        data = json.loads(request.body)
        RegistrationId = data.get('RegistrationId', '')
        RoomId = data.get('RoomId', '')
        Reason = data.get('Reason', '')
        createdby = data.get('createdby', '')
        
        if RoomId:
            room_ins = Room_Master_Detials.objects.get(pk=RoomId)
        else:
            return JsonResponse({'error': 'RoomId is required'}, status=400)

        if RegistrationId:
            register_ins = Patient_IP_Registration_Detials.objects.get(pk=RegistrationId)
        else:
            return JsonResponse({'error': 'RegistrationId is required'}, status=400)
        
        if room_ins and register_ins:
           
            # Create a new Patient_Admission_Room_Detials entry
            Patient_Admission_Room_Detials.objects.create(
                RegisterType='IP',
                IP_Registration_Id=register_ins,  # Corrected field name
                Casuality_Registration_Id=None,
                RoomId=room_ins,
                Status=True,
                bedtransferReason=Reason,
                created_by=createdby
            )
            room_ins.Booking_Status='Requested'
            room_ins.save()
            
            

        return JsonResponse({'success': 'Bed Request send successfully successfully'}, safe=False)

    except Room_Master_Detials.DoesNotExist:
        return JsonResponse({'error': 'Room does not exist'}, status=404)

    except Patient_IP_Registration_Detials.DoesNotExist:
        return JsonResponse({'error': 'IP Registration does not exist'}, status=404)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)





@csrf_exempt
@require_http_methods(["POST"])
def bed_transfer_approve_cancel_details(request):
    try:
        data = json.loads(request.body)
        RegistrationId = data.get('RegistrationId', '')
        RoomId = data.get('RoomId', '')
        Type = data.get('Type', '')
        Reason = data.get('Reason', '')
        PatientFileRecieved = data.get('PatientFileRecieved', False)
        MedicineTransfered = data.get('MedicineTransfered', False)
        AnyMedicalRecordError = data.get('AnyMedicalRecordError', False)
        ConfirmationFromRelatives = data.get('ConfirmationFromRelatives', False)
        RelativeName = data.get('RelativeName', '')
        createdby = data.get('createdby', '')
        print(data,'-----')
        if RoomId:
            room_ins = Room_Master_Detials.objects.get(pk=RoomId)
        else:
            return JsonResponse({'error': 'RoomId is required'}, status=400)

        if RegistrationId:
            register_ins = Patient_IP_Registration_Detials.objects.get(pk=RegistrationId)
        else:
            return JsonResponse({'error': 'RegistrationId is required'}, status=400)
        
        if room_ins and register_ins:
            disdate = datetime.now()
            if Type =='Approve':
                previous_room = Patient_Admission_Room_Detials.objects.get(
                    IP_Registration_Id__pk=RegistrationId, Status=True, IsStayed=True, CurrentlyStayed=True
                )
                
                previous_room.CurrentlyStayed=False
                previous_room.Discharge_Date = disdate
                previous_room.save()
                
                previous_room_master_ins =Room_Master_Detials.objects.get(pk =previous_room.RoomId.pk,Booking_Status='Occupied')
                if previous_room_master_ins:
                    previous_room_master_ins.Booking_Status='Maintenance'
                    previous_room_master_ins.save()
                    schedule_status_update(previous_room_master_ins.pk,30)
                    
                
                
                roomdatass = Patient_Admission_Room_Detials.objects.filter(IP_Registration_Id__pk=RegistrationId,Status=True,CurrentlyStayed=False,IsStayed=False).exclude(Iscanceled=True).order_by('-created_by').first()
                roomdatass.IsStayed=True
                roomdatass.CurrentlyStayed=True
                roomdatass.Admitted_Date=disdate
                roomdatass.PatientfileRecieved=PatientFileRecieved
                roomdatass.MedicineTransfered=MedicineTransfered
                roomdatass.AnyMedicalRecordError=AnyMedicalRecordError
                roomdatass.ConfirmationfromReletives=ConfirmationFromRelatives
                roomdatass.ReletiveName=RelativeName
                roomdatass.MedRecReason=Reason
                roomdatass.save()
                
                curr_previous_room_master_ins =Room_Master_Detials.objects.get(pk =roomdatass.RoomId.pk,Booking_Status='Requested')
                if curr_previous_room_master_ins:
                    curr_previous_room_master_ins.Booking_Status='Occupied'
                    curr_previous_room_master_ins.save()

                return JsonResponse({'success': 'Bed Request Approved successfully '}, safe=False)
            elif Type =='Cancel':
                roomdatass = Patient_Admission_Room_Detials.objects.filter(IP_Registration_Id__pk=RegistrationId,Status=True,CurrentlyStayed=False,IsStayed=False).exclude(Iscanceled=True).order_by('-created_by').first()
                roomdatass.IsStayed=False
                roomdatass.Iscanceled=True
                roomdatass.CancelReason=Reason
                roomdatass.Approved_by=createdby
                roomdatass.save()
                
                room_master_ins =Room_Master_Detials.objects.get(pk = roomdatass.RoomId.pk,Booking_Status='Requested')
                if room_master_ins:
                    room_master_ins.Booking_Status='Available'
                    room_master_ins.save()
                
                
                return JsonResponse({'success': 'Bed Request cancelled successfully '}, safe=False)
            else:
                return JsonResponse({'error':'type not exist'})
    except Room_Master_Detials.DoesNotExist:
        return JsonResponse({'error': 'Room does not exist'}, status=404)

    except Patient_IP_Registration_Detials.DoesNotExist:
        return JsonResponse({'error': 'IP Registration does not exist'}, status=404)

    except Exception as e:
        print('error', str(e))
        return JsonResponse({'error': str(e)}, status=500)




@csrf_exempt
@require_http_methods(["POST", "GET", 'OPTIONS'])
def service_procedure_request(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            RegistrationId = data.get('RegistrationId', '')
            MasterType = data.get('MasterType', '')
            Id = data.get('id', '')
            units = data.get('Units', '')
            createdby = data.get('createdby', '')

            if not RegistrationId:
                return JsonResponse({'error': 'RegistrationId is required'}, status=400)

            # Fetch the related patient registration and room details
            register_ins = Patient_IP_Registration_Detials.objects.get(pk=RegistrationId)

            room_inss = Patient_Admission_Room_Detials.objects.get(
                IP_Registration_Id__pk=register_ins.pk, Status=True, IsStayed=True, CurrentlyStayed=True
            )

            service_ins = None
            procedure_ins = None

            if MasterType == 'Service':
                service_ins = Service_Master_Details.objects.get(pk=Id)
            elif MasterType == 'Procedure':
                procedure_ins = Procedure_Master_Details.objects.get(pk=Id)
            else:
                return JsonResponse({'error': 'Invalid MasterType. Must be either "Service" or "Procedure".'}, status=400)

            # Create the service/procedure request
            Service_Procedure_request_Ip.objects.create(
                MasterType=MasterType,
                Service_ratecard=service_ins,
                Procedure_ratecard=procedure_ins,
                RegistrationId=register_ins,
                RoomId=room_inss.RoomId,
                Units=units,
                created_by=createdby
            )

            return JsonResponse({'success': f'{MasterType} Added Successfully'}, status=201)

        except Patient_IP_Registration_Detials.DoesNotExist:
            return JsonResponse({'error': 'IP Registration does not exist'}, status=404)
        except Patient_Admission_Room_Detials.DoesNotExist:
            return JsonResponse({'error': 'Room details not found for this registration'}, status=404)
        except Service_Master_Details.DoesNotExist:
            return JsonResponse({'error': 'Service not found'}, status=404)
        except Procedure_Master_Details.DoesNotExist:
            return JsonResponse({'error': 'Procedure not found'}, status=404)
        except Exception as e:
            print('error', str(e))
            return JsonResponse({'error': str(e)}, status=500)

    elif request.method == 'GET':
        try:
            MasterType = request.GET.get('MasterType')
            RegistrationId = request.GET.get('RegistrationId')
            status = request.GET.get('status')

            # Querying Service_Procedure_request_Ip based on status if provided
            if status:
                service_ins = Service_Procedure_request_Ip.objects.filter(
                    RegistrationId__pk=RegistrationId, MasterType=MasterType, Status=status
                )
            else:
                service_ins = Service_Procedure_request_Ip.objects.filter(
                    RegistrationId__pk=RegistrationId, MasterType=MasterType
                )

            servicedata = []
            index = 1

            for inss in service_ins:
                data = {
                    'id': index,
                    'ServiceId': inss.Service_ratecard.pk if inss.Service_ratecard else inss.Procedure_ratecard.pk,
                    'ServiceType': inss.Service_ratecard.Service_Type if inss.Service_ratecard else inss.Procedure_ratecard.Type,
                    'ServiceName': inss.Service_ratecard.Service_Name if inss.Service_ratecard else inss.Procedure_ratecard.Procedure_Name,
                    "Units": f"{inss.Units} hrs" if inss.Service_ratecard and inss.Service_ratecard.Service_Type == 'Hourly' else inss.Units,
                    "DateTime": inss.created_at.strftime('%d-%m-%y / %I-%M %p'),
                    "Status": "Not Paid" if not inss.Status else "Paid"
                }
                servicedata.append(data)
                index += 1

            return JsonResponse(servicedata, safe=False)

        except Exception as e:
            print('error', str(e))
            return JsonResponse({'error': str(e)}, status=500)





@csrf_exempt
def get_ip_billing_datasss(request):
    if request.method == 'GET':
        try:
            RegistrationId = request.GET.get('RegistrationId')
            # Retrieve all room details
            roomdatas = Patient_Admission_Room_Detials.objects.filter(
                IP_Registration_Id__pk=RegistrationId, Status=True, IsStayed=True
            ).exclude(Iscanceled=True, CurrentlyStayed=True)

            service_ins = Service_Procedure_request_Ip.objects.filter(
                RegistrationId__pk=RegistrationId, Status=False
            )

            emp_datas = {
                'RoomDatas': [],
                'ServiceDetials': []
            }

            for room in roomdatas:
                # Calculate the difference between Admitted_Date and Discharge_Date
                admitted_date = room.Admitted_Date  # Assuming datetime object
                discharge_date = room.Discharge_Date if room.Discharge_Date else None

                if discharge_date:
                    difference = discharge_date - admitted_date
                    days = difference.days  # Total number of days
                    hours, remainder = divmod(difference.seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    difff = f"{days} days, {hours} hours"
                else:
                    difff = "Still Admitted"  # Handle cases where Discharge_Date is None

                roomdetials = {
                    'id': len(emp_datas['RoomDatas']) + 1,
                    "WardName": room.RoomId.Ward_Name.Ward_Name,
                    # "RoomName": room.RoomId.Room_Name.Room_Name,
                    "Room_No": room.RoomId.Room_No,
                    "Bed_No": room.RoomId.Bed_No,
                    "Charge": room.RoomId.Ward_Name.Current_Charge,
                    "GST": room.RoomId.Ward_Name.GST_Charge,
                    "Total_Current_Charge": room.RoomId.Ward_Name.Total_Current_Charge,
                    "Admitted_Date": admitted_date.strftime('%d-%m-%y / %I-%M %p'),
                    "Discharge_Date": discharge_date.strftime('%d-%m-%y / %I-%M %p') if discharge_date else None,
                    "Days": difff
                }
                emp_datas['RoomDatas'].append(roomdetials)

            for inss in service_ins:
                data = {
                    'id': len(emp_datas['ServiceDetials']) + 1,
                    'ServiceId': inss.Service_ratecard.pk if inss.Service_ratecard else inss.Procedure_ratecard.pk,
                    'ServiceType': inss.Service_ratecard.Service_Type if inss.Service_ratecard else inss.Procedure_ratecard.Type,
                    'ServiceName': inss.Service_ratecard.Service_Name if inss.Service_ratecard else inss.Procedure_ratecard.Procedure_Name,
                    "Units": f"{inss.Units} hrs" if inss.Service_ratecard and inss.Service_ratecard.Service_Type == 'Hourly' else inss.Units,
                    "DateTime": inss.created_at.strftime('%d-%m-%y / %I-%M %p'),
                    "Status": "Not Paid" if not inss.Status else "Paid"
                }
                # Additional logic for calculating charges, etc.
                emp_datas["ServiceDetials"].append(data)

            # Return JSON response
            return JsonResponse(emp_datas, safe=False)

        except Exception as e:
            # Handle exceptions and return error response
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)




# @csrf_exempt
# @require_http_methods(["GET"])
# def get_patient_appointment_details_specifydoctor(request):
#     try:
#         Doctor = request.GET.get('Doctor')
#         doctor_id = request.GET.get('DoctorId', '')
#         print("doctor-", Doctor)

#         # Define a function to build the appointment data dictionary
#         def build_appointment_dict(register, idx):
#             Flagging_name = register.Flagging.Flagg_Name if register.Flagging else None
#             Flagging_color = register.Flagging.Flagg_Color if register.Flagging else None
            
#             return {
#                 'id': idx,
#                 'PatientProfile': get_file_image(register.PatientId.Patient_profile) if register.PatientId.Patient_profile else None,
#                 'PatientId': register.PatientId.PatientId,
#                 'PatientName': f"{register.PatientId.Title}.{register.PatientId.FirstName} {register.PatientId.MiddleName} {register.PatientId.SurName}",
#                 'PhoneNo': register.PatientId.PhoneNo,
#                 'Age': register.PatientId.Age,
#                 'Gender': register.PatientId.Gender,
#                 'AppointmentId': register.AppointmentId,
#                 'VisitId': register.VisitId,
#                 'Complaint': register.Complaint,
#                 'isMLC': register.IsMLC,
#                 'Flagging': Flagging_name,
#                 'FlaggingColour': Flagging_color,
#                 # 'Flagging': register.Flagging,
#                 'isRefferal': register.IsReferral,
#                 'Status': register.Status,
#                 'RegistrationId': register.pk,
#                 'DoctorName': f"{register.PrimaryDoctor.Tittle}.{register.PrimaryDoctor.First_Name} {register.PrimaryDoctor.Last_Name}",
#                 'Specilization': str(register.Specialization.Speciality_Name) if register.Specialization else '',
#             }

#         if Doctor:
#             queryset = Patient_Appointment_Registration_Detials.objects.filter(PrimaryDoctor=Doctor).exclude(Status='Cancelled')
#         else:
#             queryset = Patient_Appointment_Registration_Detials.objects.exclude(Status='Cancelled')
        
#         if doctor_id:
#             queryset = queryset.filter(PrimaryDoctor__pk=doctor_id)
#             print(queryset,'patientqueryset1111111111111111s') 
#             print(doctor_id,'queryset222222222222')

            
#         appointment_register_data = [
#             build_appointment_dict(register, idx)
#             for idx, register in enumerate(queryset, start=1)
#         ]

#         return JsonResponse(appointment_register_data, safe=False)

#     except Exception as e:
#         print(f"Error: {str(e)}")  # Optional: log the error message
#         return JsonResponse({'error': str(e)})


# @csrf_exempt
# @require_http_methods(["GET"])
# def get_patient_appointment_details_specifydoctor(request):
#     try:
#         Doctor = request.GET.get('Doctor')
#         print("doctor-", Doctor)
 
#         # Define a function to build the appointment data dictionary
#         def build_appointment_dict(register, idx):
#             Flagging_name = register.Flagging.Flagg_Name if register.Flagging else None
#             Flagging_color = register.Flagging.Flagg_Color if register.Flagging else None
 
#             patient_instance = Patient_Appointment_Registration_Detials.objects.filter(PatientId_id=register.PatientId.PatientId)
#             for patient_ins in patient_instance:
#                 PatientType_ins = Flaggcolor_Detials.objects.get(Flagg_Name=patient_ins.PatientType)
#                 patientCategory_ins = Flaggcolor_Detials.objects.get(Flagg_Name=patient_ins.PatientCategory)
               
#                 try:
#                  specialtype_ins = Flaggcolor_Detials.objects.get(Flagg_Id=patient_ins.Flagging_id)
 
#                 except Flaggcolor_Detials.DoesNotExist:
#                     continue
               
 
#                 specialtypelist = ['GENERAL','VIP','GOVT','INSURANCE','MLC','CLIENT','CORPORATE','DONATION','EMPLOYEE','EMPLOYEERELATION','DOCTOR','DOCTORRELATION']
 
#                 if patient_ins.IsMLC == 'Yes':
 
#                    mlc_ins = Flaggcolor_Detials.objects.get(Flagg_Name= 'MLC')
               
#                    return {
#                     'id': idx,
#                     'PatientProfile': get_file_image(register.PatientId.Patient_profile) if register.PatientId.Patient_profile else None,
#                     'PatientId': register.PatientId.PatientId,
#                     'PatientName': f"{register.PatientId.Title}.{register.PatientId.FirstName} {register.PatientId.MiddleName} {register.PatientId.SurName}",
#                     'PhoneNo': register.PatientId.PhoneNo,
#                     'Age': register.PatientId.Age,
#                     'Gender': register.PatientId.Gender,
#                     'AppointmentId': register.AppointmentId,
#                     'VisitId': register.VisitId,
#                     'Complaint': register.Complaint,
#                     'isMLC': register.IsMLC,
#                     'Flagging': Flagging_name,
#                     # 'FlaggingColour': PatientType_ins.Flagg_Color,
#                     # 'Flagging': register.Flagging,
#                     'isRefferal': register.IsReferral,
#                     'Status': register.Status,
#                     'RegistrationId': register.pk,
#                     'DoctorName': f"{register.PrimaryDoctor.Tittle}.{register.PrimaryDoctor.First_Name} {register.PrimaryDoctor.Last_Name}",
#                     'Specilization': str(register.Specialization.Speciality_Name) if register.Specialization else '',
#                     'PatientType': patient_ins.PatientType,
#                     'patientTypeColor':PatientType_ins.Flagg_Color,
#                     'PatientCategory':patient_ins.PatientCategory,
#                     'patientCategoryColor':patientCategory_ins.Flagg_Color,
#                     'IsMLC':   'MLC',
#                     'MLCColor': mlc_ins.Flagg_Color,
#                     'specialtype' : specialtype_ins.Flagg_Name if specialtype_ins.Flagg_Name  not in specialtypelist else 'GENERAL',
#                     'specialtypecolor':specialtype_ins.Flagg_Color if specialtype_ins.Flagg_Name  not in specialtypelist else '#fff'
#                     }
               
#                 else:
#                   return {
#                     'id': idx,
#                     'PatientProfile': get_file_image(register.PatientId.Patient_profile) if register.PatientId.Patient_profile else None,
#                     'PatientId': register.PatientId.PatientId,
#                     'PatientName': f"{register.PatientId.Title}.{register.PatientId.FirstName} {register.PatientId.MiddleName} {register.PatientId.SurName}",
#                     'PhoneNo': register.PatientId.PhoneNo,
#                     'Age': register.PatientId.Age,
#                     'Gender': register.PatientId.Gender,
#                     'AppointmentId': register.AppointmentId,
#                     'VisitId': register.VisitId,
#                     'Complaint': register.Complaint,
#                     'isMLC': register.IsMLC,
#                     'Flagging': Flagging_name,
#                     #'FlaggingColour': PatientType_ins.Flagg_Color,
#                     # 'Flagging': register.Flagging,
#                     'isRefferal': register.IsReferral,
#                     'Status': register.Status,
#                     'RegistrationId': register.pk,
#                     'DoctorName': f"{register.PrimaryDoctor.Tittle}.{register.PrimaryDoctor.First_Name} {register.PrimaryDoctor.Last_Name}",
#                     'Specilization': str(register.Specialization.Speciality_Name) if register.Specialization else '',
#                     'PatientType': patient_ins.PatientType,
#                     'patientTypeColor':PatientType_ins.Flagg_Color,
#                     'PatientCategory':patient_ins.PatientCategory,
#                     'patientCategoryColor':patientCategory_ins.Flagg_Color,
#                     'IsMLC':   None,
#                     'MLCColor': None,
#                     'specialtype' : specialtype_ins.Flagg_Name if specialtype_ins.Flagg_Name  not in specialtypelist else 'GENERAL',
#                     'specialtypecolor':specialtype_ins.Flagg_Color if specialtype_ins.Flagg_Name  not in specialtypelist else '#fff'
#                 }
 
 
#         if Doctor:
#             queryset = Patient_Appointment_Registration_Detials.objects.filter(PrimaryDoctor_id=Doctor).exclude(Status='Cancelled')
#         else:
#             queryset = Patient_Appointment_Registration_Detials.objects.exclude(Status='Cancelled')
 
#         appointment_register_data = [
#             build_appointment_dict(register, idx)
#             for idx, register in enumerate(queryset, start=1)
#         ]
 
#         return JsonResponse(appointment_register_data, safe=False)
 
#     except Exception as e:
#         print(f"Error: {str(e)}")  # Optional: log the error message
#         return JsonResponse({'error': str(e)})
 

# @csrf_exempt
# @require_http_methods(["GET"])
# def get_patient_appointment_details_specifydoctor(request):
#     try:
#         Doctor = request.GET.get('Doctor')
#         doctor_id = request.GET.get('DoctorId', '')
#         print("doctor-", Doctor)
 
#         # Define a function to build the appointment data dictionary
#         def build_appointment_dict(register, idx):
#             Flagging_name = register.Flagging.Flagg_Name if register.Flagging else None
#             Flagging_color = register.Flagging.Flagg_Color if register.Flagging else None
           
#             return {
#                 'id': idx,
#                 'PatientProfile': get_file_image(register.PatientId.Patient_profile) if register.PatientId.Patient_profile else None,
#                 'PatientId': register.PatientId.PatientId,
#                 'PatientName': f"{register.PatientId.Title}.{register.PatientId.FirstName} {register.PatientId.MiddleName} {register.PatientId.SurName}",
#                 'PhoneNo': register.PatientId.PhoneNo,
#                 'Age': register.PatientId.Age,
#                 'Gender': register.PatientId.Gender,
#                 'AppointmentId': register.AppointmentId,
#                 'VisitId': register.VisitId,
#                 'Complaint': register.Complaint,
#                 'isMLC': register.IsMLC,
#                 'Flagging': Flagging_name,
#                 'FlaggingColour': Flagging_color,
#                 # 'Flagging': register.Flagging,
#                 'isRefferal': register.IsReferral,
#                 'Status': register.Status,
#                 'RegistrationId': register.pk,
#                 'DoctorName': f"{register.PrimaryDoctor.Tittle}.{register.PrimaryDoctor.First_Name} {register.PrimaryDoctor.Last_Name}",
#                 'Specilization': str(register.Specialization.Speciality_Name) if register.Specialization else '',
#             }
 
#         if Doctor:
#             queryset = Patient_Appointment_Registration_Detials.objects.filter(PrimaryDoctor=Doctor).exclude(Status='Cancelled')
#         else:
#             queryset = Patient_Appointment_Registration_Detials.objects.exclude(Status='Cancelled')
       
#         if doctor_id:
#             queryset = queryset.filter(PrimaryDoctor__pk=doctor_id)
#             print(queryset,'patientqueryset1111111111111111s')
#             print(doctor_id,'queryset222222222222')
 
           
#         appointment_register_data = [
#             build_appointment_dict(register, idx)
#             for idx, register in enumerate(queryset, start=1)
#         ]
 
#         return JsonResponse(appointment_register_data, safe=False)
 
#     except Exception as e:
#         print(f"Error: {str(e)}")  # Optional: log the error message
#         return JsonResponse({'error': str(e)})
 
 

 
@csrf_exempt
@require_http_methods(["GET"])
def get_patient_appointment_details_specifydoctor(request):
    try:
        # Extract query parameters
        Doctor = request.GET.get('Doctor')
        doctor_id = request.GET.get('DoctorId', '')
        status = request.GET.get('status', '')
        print("status",status)
 
        print("Doctor:", Doctor)
 
        # Build the queryset
        queryset = Patient_Appointment_Registration_Detials.objects.exclude(Status='Cancelled')
       
        if Doctor:
            queryset = queryset.filter(PrimaryDoctor__pk=Doctor)
        if doctor_id:
            queryset = queryset.filter(PrimaryDoctor__pk=doctor_id)
            print("Filtered Queryset:", queryset)
            print("Doctor ID:", doctor_id)
        if status:
            queryset = queryset.filter(Q(Status__icontains=status))
        else:
            # Exclude 'Cancelled' status if no status is specified
            queryset = queryset.exclude(Status='Cancelled')
   
 
        # Prepare response data
        DocWisePatient = []
        for idx, register in enumerate(queryset, start=1):
            # Flagging_name = register.Flagging.Flagg_Name if register.Flagging else None
            # # Flagging_color = register.Flagging.Flagg_Color if register.Flagging else None
 
            # Build the patient dictionary
            RegisterPatient = {
                'id': idx,
                'PatientProfile': get_file_image(register.PatientId.Patient_profile) if register.PatientId.Patient_profile else None,
                'PatientId': register.PatientId.PatientId,
                'PatientName': f"{register.PatientId.Title.Title_Name}.{register.PatientId.FirstName} {register.PatientId.MiddleName} {register.PatientId.SurName}",
                'PhoneNo': register.PatientId.PhoneNo,
                'Age': register.PatientId.Age,
                'Gender': register.PatientId.Gender,
                'AppointmentId': register.AppointmentId,
                'VisitId': register.VisitId,
                'Complaint': register.Complaint,
                'isMLC': register.IsMLC,
                'VisitType':register.VisitType,
                # 'Flagging': Flagging_name,
                # 'FlaggingColour': Flagging_color,
                'isRefferal': register.IsReferral,
                'Status': register.Status,
                'RegistrationId': register.pk,
                'Doctorid': register.PrimaryDoctor.Doctor_ID if register.PrimaryDoctor and register.PrimaryDoctor.Doctor_ID is not None else None,
                'DoctorName': f"{register.PrimaryDoctor.Tittle.Title_Name}.{register.PrimaryDoctor.First_Name} {register.PrimaryDoctor.Last_Name}" if register.PrimaryDoctor else None,
                'Specilization': str(register.Specialization.Speciality_Name) if register.Specialization else '',
            }
            DocWisePatient.append(RegisterPatient)
 
        # Return the response
        return JsonResponse(DocWisePatient, safe=False)
 
    except Exception as e:
        # Log and return the error
        print(f"Error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
 

@csrf_exempt
@require_http_methods(["GET"])
def get_OP_patient_Filter_SpecialityWise(request):
    try:
        # Get query parameters
        query = request.GET.get('query', '')
        doctor_id = request.GET.get('DoctorId', '')
        speciality_id = request.GET.get('SpecialityId', '')
        status = request.GET.get('status', '')

        # queryset = Patient_Appointment_Registration_Detials.objects.exclude(Status='Cancelled')
        queryset = Patient_Appointment_Registration_Detials.objects.exclude(Status='Cancelled').filter(Specialization__Speciality_Id=speciality_id)
       
        # if speciality_id:
        #     queryset = queryset.filter(Specialization__Speciality_Id=speciality_id)
        
        # if speciality_id:
        #     queryset = queryset.filter(Specialization__Speciality_Id=speciality_id)

        if query:
            queryset = queryset.filter(
                Q(PatientId__FirstName__icontains=query) |
                Q(PatientId__MiddleName__icontains=query) |
                Q(PatientId__SurName__icontains=query) |
                Q(PatientId__PatientId__icontains=query) |
                Q(PatientId__PhoneNo__icontains=query)
            )

        if doctor_id:
            queryset = queryset.filter(PrimaryDoctor__pk=doctor_id)

        if status:
            queryset = queryset.filter(Q(Status__icontains=status))
        else:
            # Exclude 'Cancelled' status if no status is specified
            queryset = queryset.exclude(Status='Cancelled')


        # Serialize the filtered queryset
        appointment_register_data = [
            {
                'id': idx,
                'PatientProfile': get_file_image(register.PatientId.Patient_profile) if register.PatientId.Patient_profile else None,
                'PatientId': register.PatientId.PatientId,
                'PatientName': f"{register.PatientId.Title.Title_Name if register.PatientId.Title else None}.{register.PatientId.FirstName} {register.PatientId.MiddleName} {register.PatientId.SurName}",
                'PhoneNo': register.PatientId.PhoneNo,
                'Age': register.PatientId.Age,
                'Gender': register.PatientId.Gender,
                'AppointmentId': register.AppointmentId,
                'VisitId': register.VisitId,
                'Complaint': register.Complaint,
                'isMLC': register.IsMLC,
                # 'Flagging': register.Flagging.Flagg_Name if register.Flagging else None,
                # 'FlaggingColour': register.Flagging.Flagg_Color if register.Flagging else None,
                'isRefferal': register.IsReferral,
                'Status': register.Status,
                'RegistrationId': register.pk,
                'DoctorId': register.PrimaryDoctor.pk,
                'SpecilizationId': register.Specialization.Speciality_Id if register.Specialization else None,
                'DoctorName': f"{register.PrimaryDoctor.Tittle.Title_Name if register.PrimaryDoctor.Tittle else None}.{register.PrimaryDoctor.First_Name} {register.PrimaryDoctor.Last_Name}",
                'Specilization': str(register.Specialization.Speciality_Name) if register.Specialization else '',
            }
            for idx, register in enumerate(queryset, start=1)
        ]

        return JsonResponse(appointment_register_data, safe=False)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST", "GET", "OPTIONS"])
def Register_Request_Cancel(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            RegistrationId = data.get('RegistrationId', None)
            CancelReason = data.get('CancelReason', '')
            Createdby = data.get('created_by', '')
            Status = "Cancelled"

            if RegistrationId is None:
                return JsonResponse({'warn': 'Missing RegistrationId'})
            
            Register_instance = Patient_Appointment_Registration_Detials.objects.filter(pk=RegistrationId).first()
            Register_instance.Status = Status
            Register_instance.save()
            # Create a new cancelation record
            Patient_Appointment_Registration_Cancel_Details.objects.create(
                Registration_Id=Register_instance,
                Cancel_Reason=CancelReason,
                Status = Status,
                created_by=Createdby,
                updated_by = Createdby,
            )
            
            return JsonResponse({'success': 'Cancellation request registered successfully'})

        except Exception as e:
            print("Exception:", e)
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)



@csrf_exempt
@require_http_methods(["POST", "GET", "OPTIONS"])
def Registration_Reshedule_Details(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            RegistrationId = data.get('RegistrationId', None)
            Createdby = data.get('created_by', '')
            DoctorName = data.get('DoctorName', None)
            Specialization = data.get('Specialization', None)
            Status = "Pending"
            PreviousDoctor = data.get('PreviousDoctor',None)
            changeReason = data.get('ChangingReason', '')

            if RegistrationId is None:
                return JsonResponse({'warn': 'Missing RegistrationId'})
            if DoctorName is None:
                return JsonResponse({'warn': 'Missing DoctorName'})
            if Specialization is None:
                return JsonResponse({'warn': 'Missing Specialization'})

            # Fetch the related instances properly
            Register_instance = Patient_Appointment_Registration_Detials.objects.filter(pk=RegistrationId).first()
            if not Register_instance:
                return JsonResponse({'warn': 'Invalid RegistrationId'})

            Speciality_instance = Speciality_Detials.objects.filter(pk=Specialization).first()
            Doctor_instance = Doctor_Personal_Form_Detials.objects.filter(pk=DoctorName).first()
            Doctor_instances = Doctor_Personal_Form_Detials.objects.filter(pk=PreviousDoctor).first()
            
            if not Speciality_instance:
                return JsonResponse({'warn': 'Invalid Specialization'})
            if not Doctor_instance:
                return JsonResponse({'warn': 'Invalid DoctorName'})
            
            # Update the Register instance
            Register_instance.Specialization = Speciality_instance
            Register_instance.PrimaryDoctor = Doctor_instance
            Register_instance.Status = Status
            Register_instance.save()

            # Create the reschedule entry
            Patient_Registration_Reshedule_Details.objects.create(
                Registration_Id=Register_instance,
                ChangingReason=changeReason,
                specialization=Speciality_instance,
                doctor_name=Doctor_instance,
                AppointmentDoctor=Doctor_instances,
                Status=Status,
                created_by=Createdby,
                updated_by = Createdby,
            )

            return JsonResponse({'success': 'Reschedule request registered successfully'})

        except Exception as e:
            print("Exception:", e)
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

    return JsonResponse({'error': 'Invalid request method'},status=405)


# @csrf_exempt
# @require_http_methods(["GET"])
# def get_patient_appointment_details_withoutcancelled(request):
#     try:
#         # Get query parameters
#         query = request.GET.get('query', '')
#         status = request.GET.get('status', '')
#         location = request.GET.get('location','')
#         print("status90",status)
#         print("workbenchlocation",location)
#         if not location:
#             return JsonResponse({'warn': 'Missing Location Details'})
#         # Start with all records
#         queryset = Patient_Appointment_Registration_Detials.objects.filter(Location__Location_Id=location)
#         print("queryset",queryset)

#         # Apply filters based on the query parameters
#         if query:
#             queryset = queryset.filter(
#                 Q(PatientId_FirstName_icontains=query) |
#                 Q(PatientId_MiddleName_icontains=query) |
#                 Q(PatientId_SurName_icontains=query) |
#                 Q(PatientId_PatientId_icontains=query) |
#                 Q(PatientId_PhoneNo_icontains=query)
#             )
        
#         # Filter by status if specified
#         if status:
#             queryset = queryset.filter(Q(Status__icontains=status))
#         else:
#             # Exclude 'Cancelled' status if no status is specified
#             queryset = queryset.exclude(Status='Cancelled')

#         # Serialize the filtered queryset
#         appointment_register_data = []
#         for idx, register in enumerate(queryset, start=1):
#             Flagging_name = register.Flagging.Flagg_Name if register.Flagging else None
#             Flagging_color = register.Flagging.Flagg_Color if register.Flagging else None
            
#             appointment_dict = {
#                 'id': idx,
#                 'PatientProfile': get_file_image(register.PatientId.Patient_profile) if register.PatientId.Patient_profile else None,
#                 'PatientId': register.PatientId.PatientId,
#                 'PatientName': f"{register.PatientId.Title}.{register.PatientId.FirstName} {register.PatientId.MiddleName} {register.PatientId.SurName}",
#                 'PhoneNo': register.PatientId.PhoneNo,
#                 'AppointmentId': register.AppointmentId,
#                 'VisitId': register.VisitId,
#                 'Complaint': register.Complaint,
#                 'isMLC': register.IsMLC,
#                 'Flagging': Flagging_name,
#                 'FlaggingColour': Flagging_color,
#                 'isRefferal': register.IsReferral,
#                 'Status': register.Status,
#                 'RegistrationId': register.pk,
#                 'DoctorName': f"{register.PrimaryDoctor.Tittle}.{register.PrimaryDoctor.First_Name} {register.PrimaryDoctor.Last_Name}",
#                 'Specilization': str(register.Specialization.Speciality_Name) if register.Specialization else '',
#             }
#             appointment_register_data.append(appointment_dict)

#         return JsonResponse(appointment_register_data, safe=False)

#     except Exception as e:
#         return JsonResponse({'error': str(e)})








@csrf_exempt
def get_unique_id_no_validation(request):
    if request.method == 'GET':
        try:
            unique_id = request.GET.get('UniqueIdNo')
            # Check if the patient with the given UniqueIdNo exists
            patient = Patient_Detials.objects.filter(UniqueIdNo=unique_id).exists()

            if patient:
                return JsonResponse({'error': f"The {unique_id} is already exists for another patient"})
            else:
                return JsonResponse({'message': 'UniqueIdNo is available'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Invalid request method'})


  
@csrf_exempt
def get_AdmissionDetails(request):
    if request.method == 'GET':
        try:
            RegistrationId = request.GET.get('RegistrationId')

            # Validate if unique_id was provided
            if not RegistrationId:
               return JsonResponse({'error': 'RegistrationId is required'}, status=400)
        
            # Check if the patient with the given UniqueIdNo exists
            patient_AdmissionDetails = Patient_Admission_Detials.objects.filter(IP_Registration_Id__pk=RegistrationId)
             
            Admission_Data = []
            for Admission in patient_AdmissionDetails:
                Admission_dict = {
                    'RegistrationId': Admission.IP_Registration_Id.pk,
                    'AdmissionPurpose': Admission.AdmissionPurpose,

                } 
                Admission_Data.append(Admission_dict)
            return JsonResponse(Admission_Data,safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Invalid request method'})




@csrf_exempt
def get_available_tokenno_by_speciality(request):
    if request.method == 'GET':
        try:
            date = request.GET.get('Date')
            speciality_id = request.GET.get('Speciality')

            # Validate input parameters
            if not speciality_id:
                return JsonResponse({'warn': 'Speciality parameter is missing'})
            if not date:
                return JsonResponse({'warn': 'Date parameter is missing'})

            # Check if the specified speciality exists
            try:
                speciality = Speciality_Detials.objects.get(pk=speciality_id)
            except Speciality_Detials.DoesNotExist:  
                return JsonResponse({'warn': 'Speciality not found'})

            # Retrieve the speciality abbreviation (e.g., "NEU" for Neurology, "ONC" for Oncology)
            speciality_abbr = speciality.Speciality_Name[:3].upper()  # Use the first 3 characters of the speciality name as abbreviation

            # Parse date and filter appointments by created_at date and speciality
            try:
                date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            except ValueError:
                return JsonResponse({'warn': 'Invalid date format. Use YYYY-MM-DD.'})

            speciality_patient_queryset = Patient_Appointment_Registration_Detials.objects.filter(
                Specialization=speciality_id,
                created_at__date=date_obj  # Filters by the date portion of created_at
            ).order_by('created_at')  # Order by created_at

            # Count the appointments
            speciality_patient_count = speciality_patient_queryset.count()

            # Increment the count for the response
            token_no = speciality_patient_count + 1

            # Format the token number as a 3-digit number
            formatted_token_no = f"{speciality_abbr}{token_no:03d}"

            return JsonResponse({
                'date': date,
                'current_count': speciality_patient_count,
                'next_available_token_no': formatted_token_no,
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)




@csrf_exempt
def Patient_management_details(request):
    if request.method == 'GET':
        try:
            # Retrieve GET parameters
            PatientID = request.GET.get('PatientId')
            date = request.GET.get('date', None)

            if not PatientID:
                return JsonResponse({'warn': 'Patient ID is required'}, safe=False)

            # Parse date if provided
            filter_date = None
            if date:
                try:
                    filter_date = datetime.strptime(date, '%Y-%m-%d').date()
                except ValueError:
                    return JsonResponse({'warn': 'Invalid date format. Expected YYYY-MM-DD.'}, safe=False)

            # Query patient appointments
            if filter_date:
                # Fetch records for the specified date
                patient_appointments = Patient_Appointment_Registration_Detials.objects.filter(
                    PatientId=PatientID,
                    created_at__date=filter_date
                )
            else:
                # Fetch the last 3 completed appointments if no date is provided
                patient_appointments = Patient_Appointment_Registration_Detials.objects.filter(
                    PatientId=PatientID,
                    Status="Completed"
                ).order_by('-created_at')[:3]

            if not patient_appointments.exists():
                return JsonResponse({'warn': 'No data available for the selected patient or date.'}, safe=False)

            records = []

            # Iterate through appointments
            for index, appointment in enumerate(patient_appointments, start=1):
                appointment_date = appointment.created_at.strftime('%d %b %Y')

                # Prepare complaint details
                complaint = {
                    'index': index,
                    'PatientId': appointment.PatientId.PatientId,
                    'date': appointment_date,
                    'Date': appointment.created_at.strftime('%Y-%m-%d'),
                    'complaint': appointment.Complaint,
                    'VisitPurpose': appointment.VisitPurpose,
                    'PatientType': appointment.PatientType,
                    'PatientCategory': appointment.PatientCategory,
                }

                # Fetch related General Evaluation details
                general_evaluation = Workbench_GeneralEvaluation.objects.filter(
                    Registration_Id__PatientId_id=PatientID,
                    created_at__date=appointment.created_at.date()
                ).last()

                if general_evaluation:
                    complaint.update({
                        'KeyComplaint': general_evaluation.KeyComplaint,
                        'CheifComplaint': general_evaluation.CheifComplaint,
                        'Diagnosis': general_evaluation.Diagnosis,
                        'Examine': general_evaluation.Examine,
                        'History': general_evaluation.History,
                    })

                # Fetch related Vital Details
                vital_details = Patient_Vital_Details.objects.filter(
                    Registration_Id__PatientId_id=PatientID,
                    created_at__date=appointment.created_at.date()
                ).last()

                if vital_details:
                    complaint.update({
                        'Temperature': vital_details.Temperature,
                        'Pulse_Rate': vital_details.Pulse_Rate,
                        'Heart_Rate': vital_details.Heart_Rate,
                        'SPO2': vital_details.SPO2,
                        'Respiratory_Rate': vital_details.Respiratory_Rate,
                        'SBP': vital_details.SBP,
                        'DBP': vital_details.DBP,
                        'Height': vital_details.Height,
                        'Weight': vital_details.Weight,
                        'BMI': vital_details.BMI,
                        'WC': vital_details.WC,
                        'HC': vital_details.HC,
                    })

                # Fetch Prescription Details
                prescriptions = OPD_Prescription_Details.objects.filter(
                    Registration_Id__PatientId_id=PatientID,
                    created_at__date=appointment.created_at.date()
                )
                prescription_items = {prescription.ItemId.ItemName for prescription in prescriptions if prescription.ItemId}
                if prescription_items:
                    complaint['Prescriptions'] = list(prescription_items)

                # Avoid duplicate entries by checking the date
                if not any(record['date'] == complaint['date'] for record in records):
                    records.append(complaint)

            return JsonResponse(records, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, safe=False)


@csrf_exempt
def Patient_Datewise_Annotedimage_details(request):
    if request.method == 'GET':
        try:
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
                
            # Get query parameters
            PatientID = request.GET.get('PatientId')
            Date = request.GET.get('Date')

            # Log for debugging
            print("PatientID:", PatientID)
            print("Date:", Date)

            # Validate inputs
            if not PatientID:
                return JsonResponse({'warn': 'Patient Id required'}, safe=False)
            if not Date:
                return JsonResponse({'warn': 'Date is required'}, safe=False)

            # Parse the date string to a datetime object
            try:
                filter_date = datetime.strptime(Date, '%Y-%m-%d').date()
            except ValueError:
                return JsonResponse({'warn': 'Invalid Date format. Expected YYYY-MM-DD.'}, safe=False)

            # Query the database
            GeneralEvaluations = Workbench_GeneralEvaluation.objects.filter(
                Registration_Id__PatientId=PatientID,
                created_at__date=filter_date
            )
            print("GeneralEvaluations", GeneralEvaluations)

            # Check if any records found
            if not GeneralEvaluations.exists():
                return JsonResponse({'warn': 'No records found for the given PatientId and Date'}, safe=False)

            # Prepare the response data
            GeneralEvaluation_data = []
            for evaluation in GeneralEvaluations:
                try:
                    GeneralEvaluation_data.append({
                        'PrimaryDoctorId': evaluation.Registration_Id.PrimaryDoctor.Doctor_ID if evaluation.Registration_Id.PrimaryDoctor else None,
                        'PrimaryDoctorName': evaluation.Registration_Id.PrimaryDoctor.ShortName if evaluation.Registration_Id.PrimaryDoctor else None,
                        'currentAnnotation': get_file_image(evaluation.AnnotationDocument) if evaluation.AnnotationDocument else None,
                        'Date': evaluation.created_at.strftime('%Y-%m-%d'),
                        'Id': evaluation.Id  # Changed this from evaluation.id to evaluation.Id
                    })
                except Exception as e:
                    print(f"Error processing evaluation {evaluation.Id}: {e}")
                    continue  # Skip the problematic record

            return JsonResponse(GeneralEvaluation_data, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, safe=False)
        

@csrf_exempt
def patient_appointment_details_link(request):
    if request.method == 'GET':
        try:
            PatientID = request.GET.get('PatientId')
            print("PatientIDAppointment", PatientID)

            if not PatientID:
                return JsonResponse({'warn': 'Patient Id required'}, safe=False)

            # Fetch patient appointments
            patient_appointments = Patient_Appointment_Registration_Detials.objects.filter(PatientId=PatientID)
            print("patient_appointments", patient_appointments)

            patient_records = []

            for index, appointment in enumerate(patient_appointments, start=1):
                # Safely access PrimaryDoctor fields with getattr, avoiding AttributeError
                primary_doctor = appointment.PrimaryDoctor
                doctor_name = f"{getattr(primary_doctor, 'Tittle', '')} {getattr(primary_doctor, 'First_Name', '')} {getattr(primary_doctor, 'Middle_Name', '')} {getattr(primary_doctor, 'Last_Name', '')}".strip()
                
                # Safely access Location fields
                location_name = getattr(appointment.Location, 'Location_Name', 'Trichy') if appointment.Location else 'Trichy'

                # Appointment data
                appointment_data = {
                    'id': index,
                    'Visitid': appointment.VisitId,
                    'VisitPurpose': appointment.VisitPurpose,
                    'PrimaryDoctorName': doctor_name,
                    'PrimaryDoctorShortName': getattr(primary_doctor, 'ShorName', 'Unknown'),
                    'Date': appointment.created_at.strftime('%Y-%m-%d'),
                    'Status': appointment.Status,
                    'Location': location_name,
                }

                patient_records.append(appointment_data)

            return JsonResponse(patient_records, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, safe=False)



@csrf_exempt
def Patient_Datewise_Casesheet_details(request):
    if request.method == 'GET':
        try:
            PatientID = request.GET.get('PatientId')
            Date = request.GET.get('Date')
            if not PatientID:
                return JsonResponse({'warn': 'Patient Id required'}, safe=False)
            if not Date:
                return JsonResponse({'warn': 'Date is required'}, safe=False)
            
            try:
                filter_date = datetime.strptime(Date, '%Y-%m-%d').date()
            except ValueError:
                return JsonResponse({'warn': 'Invalid Date format. Expected YYYY-MM-DD.'}, safe=False)
            
            # Check if a GeneralEvaluation entry exists for the given PatientId and Date
            general_evaluation = Workbench_GeneralEvaluation.objects.filter(
                Registration_Id__PatientId=PatientID,
                created_at__date=filter_date
            ).last()

            # Check if a VitalDetail entry exists for the given PatientId and Date
            vital_detail = Patient_Vital_Details.objects.filter(
                Registration_Id__PatientId=PatientID,
                created_at__date=filter_date
            ).last()
            prescription_detail = OPD_Prescription_Details.objects.filter(
                Registration_Id__PatientId=PatientID,
                created_at__date=filter_date                
            )
            lab_details = Lab_Request_Details.objects.filter(
                Q(OP_Register_Id__PatientId=PatientID) |
                Q(IP_Register_Id__PatientId=PatientID) |
                Q(Casuality_Register_Id__PatientId=PatientID) |
                Q(Laboratory_Register_Id__PatientId=PatientID),
                created_at__date=filter_date
            )


            radiology_details = Radiology_Request_Details.objects.filter(
                Q(OP_Register_Id__PatientId=PatientID) |
                Q(IP_Register_Id__PatientId=PatientID) |
                Q(Casuality_Register_Id__PatientId=PatientID) |
                Q(Diagnosis_Register_Id__PatientId=PatientID),
                created_at__date=filter_date
            )

            
            general_advice = OPD_GeneralAdviceFollowUp.objects.filter(
                Registration_Id__PatientId=PatientID,
                created_at__date=filter_date,
                AdviceDataCheck=1
            )
            print("general_advice",general_advice)
            nextreview_date = OPD_GeneralAdviceFollowUp.objects.filter(
                Registration_Id__PatientId=PatientID,
                created_at__date=filter_date,
                FollowUpDataCheck=1
                
            ) 


            # Fetch referral details based on Patient ID and filter date
            refer_doctor = OPD_Referal_Details.objects.filter(
                Registration_Id__PatientId=PatientID,
                created_at__date=filter_date,
            )

            refer_data = []

            if refer_doctor.exists():  # Ensure queryset is not empty
                indexs = 1  # Initialize index
                for refer_doctor_ins in refer_doctor:  # Loop through each referral instance
                    Doctortype = refer_doctor_ins.ReferDoctorType

                    # Check for valid DoctorType and ReferDoctorCheck
                    if Doctortype in ["InHouse", "Visiting"] and refer_doctor_ins.ReferDoctorCheck:
                        response_dict = {
                            'id': indexs,
                            'Refer_Id': refer_doctor_ins.Refer_Id,
                            'VisitId': refer_doctor_ins.VisitId,
                            'ReferDoctorSpeciality': refer_doctor_ins.Speciality.Speciality_Name,
                            'PrimaryDoctorId': f"{refer_doctor_ins.PrimaryDoctorId.Tittle} {refer_doctor_ins.PrimaryDoctorId.ShortName}",
                            'ReferDoctorId': f"{refer_doctor_ins.ReferDoctorId.Tittle} {refer_doctor_ins.ReferDoctorId.ShortName}",
                            'ReferDoctorType': refer_doctor_ins.ReferDoctorType,
                            'Remarks': refer_doctor_ins.Remarks or "No Remarks",
                            'ReferDoctorCheck': refer_doctor_ins.ReferDoctorCheck,
                        }
                        refer_data.append(response_dict)
                        indexs += 1  # Increment index for each valid referral
            else:
                refer_data = None  # No referral data found

                
                
            
            # Process the general evaluation data
            general_evaluation_datas = []
            if general_evaluation:
                # If record exists, update it
                general_evaluation_data = {
                    'RegistrationId': general_evaluation.Registration_Id.pk,
                    'PatientId':general_evaluation.Registration_Id.PatientId.pk,
                    'PatientName': f"{general_evaluation.Registration_Id.PatientId.Title} {general_evaluation.Registration_Id.PatientId.FirstName} {general_evaluation.Registration_Id.PatientId.MiddleName} {general_evaluation.Registration_Id.PatientId.SurName}".strip(),
                    'gender':general_evaluation.Registration_Id.PatientId.Gender,
                    'Age':general_evaluation.Registration_Id.PatientId.Age,
                    'VisitId': general_evaluation.Registration_Id.VisitId,
                    'PrimaryDoctorId': general_evaluation.Registration_Id.PrimaryDoctor.Doctor_ID,
                    'PrimaryDoctorName': general_evaluation.Registration_Id.PrimaryDoctor.ShortName,
                    'KeyComplaint': general_evaluation.KeyComplaint,
                    'ChiefComplaint': general_evaluation.CheifComplaint,
                    'History': general_evaluation.History,
                    'Examine': general_evaluation.Examine,
                    'Diagnosis': general_evaluation.Diagnosis,
                    'created_by': general_evaluation.created_by,
                    'Date': general_evaluation.created_at.strftime('%Y-%m-%d'),
                }
                general_evaluation_datas.append(general_evaluation_data)
            else:
                # If no record found, create a new entry
                # You can modify this to add new data for a new general evaluation if needed
                general_evaluation_datas = None  # or other fields to show a new case
                
            # Process the vital details data
            vital_data = []
            if vital_detail:
                # If record exists, update it
                vital_details_data = {
                    'PrimaryDoctorName': vital_detail.Registration_Id.PrimaryDoctor.ShortName,
                    'Temperature': vital_detail.Temperature,
                    'temperature_status': vital_detail.Temperature_Status,
                    'PulseRate': vital_detail.Pulse_Rate,
                    'SPO2': vital_detail.SPO2,
                    'spo2_status': vital_detail.SPO2_Status,
                    'HeartRate': vital_detail.Heart_Rate,
                    'heartrate_status': vital_detail.Heart_Rate_Status,
                    'RespiratoryRate': vital_detail.Respiratory_Rate,
                    'RespiratoryStatus': vital_detail.Respiratory_Status,
                    'SBP': vital_detail.SBP,
                    'sbp_status': vital_detail.SBP_Status,
                    'DBP': vital_detail.DBP,
                    'Height': vital_detail.Height,
                    'Weight': vital_detail.Weight,
                    'BMI': vital_detail.BMI,
                    'WC': vital_detail.WC,
                    'HC': vital_detail.HC,
                    'BSL': vital_detail.BSL,
                    'Painscore': vital_detail.Painscore,
                    'SupplementalOxygen': vital_detail.SupplementalOxygen,
                    'SupplementalOxygen_status': vital_detail.SupplementalOxygen_Status,
                    'LevelOfConsiousness': vital_detail.LevelOfConsiousness,
                    'LevelOfConsiousness_Status': vital_detail.LevelOfConsiousness_Status,
                    'CapillaryRefillTime': vital_detail.CapillaryRefillTime,
                    'CapillaryRefillTime_Status': vital_detail.CapillaryRefillTime_Status,
                    'Type': vital_detail.Type,
                    'Date': vital_detail.created_at.strftime('%d-%m-%y'),
                    'Time': vital_detail.created_at.strftime('%H:%M:%S'),
                }
                vital_data.append(vital_details_data)
            else:
                # If no vital detail is found, you can create a new entry if needed
                vital_data = None  # or other fields to show a new case
            
            prescription_list = []
            index=1
            if prescription_detail:
                prescription_list = []  # Initialize the list
                added_item_ids = set()  # To keep track of already added ItemIds

                for detail in prescription_detail:
                    # Check if the combination of Patient_Id, ItemId, and Date already exists
                    unique_key = (detail.Patient_Id.PatientId, detail.ItemId.pk if detail.ItemId else None, detail.created_at.strftime('%Y-%m-%d'))

                    if unique_key not in added_item_ids:
                        # Create the prescription data
                        prescription_data = {
                            'Id': index,
                            'Patient_Id': detail.Patient_Id.PatientId,
                            'VisitId': detail.VisitId,
                            'ItemId': detail.ItemId.pk if detail.ItemId else None,
                            'ItemType': detail.ItemId.ProductType.ProductType_Name if detail.ItemId else None,
                            'ItemName': detail.ItemId.ItemName if detail.ItemId else None,
                            'FrequencyId': detail.FrequencyId.pk if detail.FrequencyId else None,
                            'FrequencyName': detail.FrequencyId.FrequencyName if detail.FrequencyId else None,
                            'FrequencyType': detail.FrequencyId.FrequencyType if detail.FrequencyId else None,
                            'Frequency': detail.FrequencyId.Frequency if detail.FrequencyId else None,
                            'Prescription_Id': detail.Prescription_Id,
                            'Dosage': detail.Dosage,
                            'Route': detail.Route,
                            'DurationNumber': detail.DurationNumber,
                            'DurationUnit': detail.DurationUnit,
                            'Frequencys': detail.Frequency,
                            'Qty': detail.Qty,
                            'Instruction': detail.Instruction,
                            'created_by': detail.created_by,
                            'Status': detail.Status,
                            'Date': detail.created_at.strftime('%Y-%m-%d'),
                            'Time': detail.created_at.strftime('%H:%M:%S'),
                        }

                        # Add the unique key to the set so we don't add duplicates
                        added_item_ids.add(unique_key)

                        # Increment index for the next item and append to the list
                        index += 1
                        prescription_list.append(prescription_data)
            else:
                prescription_list = None
            response_data=[]
            indexx = 1
            response_data = []

            if lab_details:
                seen_test_names = set()  # To track unique test names

                for request_item in lab_details:
                    if request_item.TestType == 'Individual':
                        # Process Individual tests
                        if request_item.IndivitualCode:
                            test_code = request_item.IndivitualCode.TestCode
                            test_name = request_item.IndivitualCode.Test_Name

                            # Only add if the test_name is unique
                            if test_name not in seen_test_names:
                                response_data.append({
                                    'id': indexx,
                                    'TestCode': test_code,
                                    'TestName': test_name,
                                    'created_at': request_item.created_at.strftime('%Y-%m-%d %H:%M:%S'), 
                                })
                                seen_test_names.add(test_name)  # Add to the set of seen test names
                                indexx += 1
                            else:
                                print(f"Duplicate Individual test: {test_name} skipped for request ID {request_item.Request_Id}")
                        else:
                            print(f"Warn: Individual test missing IndivitualCode for request ID {request_item.Request_Id}")

                    elif request_item.TestType == 'Favourites':
                        # Process Favourites tests
                        favourite = request_item.FavouriteCode
                        if favourite:
                            for test in favourite.TestName.all():
                                test_code = test.TestCode
                                test_name = test.Test_Name

                                # Only add if the test_name is unique
                                if test_name not in seen_test_names:
                                    response_data.append({
                                        'id': indexx,
                                        'FavouriteCode': favourite.Favourite_Code,
                                        'FavouriteName': favourite.FavouriteName,
                                        'TestCode': test_code,
                                        'TestName': test_name,
                                        'created_at': request_item.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                                    })
                                    seen_test_names.add(test_name)  # Add to the set of seen test names
                                    indexx += 1
                                else:
                                    print(f"Duplicate Favourite test: {test_name} skipped for request ID {request_item.Request_Id}")
                        else:
                            print(f"Warning: Favourites test missing FavouriteCode for request ID {request_item.Request_Id}")

            else:
                response_data = None

            # Final response data
            print(response_data)
            response_datas = []
            indexxxx = 1  # Initialize the index

            if radiology_details:
                for radiology in radiology_details:
                    # Fetch related test and radiology details
                    testname = TestName_Details.objects.filter(Test_Code=radiology.SubTestCode).first()
                    radiologyname = RadiologyNames_Details.objects.filter(Radiology_Id=radiology.TestCode).first()

                    # Ensure both related records exist before appending
                    if radiologyname and testname:
                        response_datas.append({
                            'id': indexxxx,
                            'Radiologyid': radiologyname.Radiology_Id,
                            'RadiologyName': radiologyname.Radiology_Name,
                            'TestCode': testname.Test_Code,
                            'TestName': testname.Test_Name,
                            'created_at': radiology.created_at,
                        })
                        indexxxx += 1  # Increment the index
            else:
                response_datas = None
                         

            advice_list = []
            indexa = 1
            if general_advice:
                print("123",general_advice)
                for advice in general_advice:
                    print("advice",advice)
                    advicedata = {
                        'id': index,
                        'Advice': advice.GeneralAdivice if advice.GeneralAdivice else None,
                        'created_at': advice.created_at,
                        
                    }
                    advice_list.append(advicedata)
                    index += 1
            else:
                advice_list = None

            
            review_list = []
            inde = 1
            if nextreview_date:
                for detail in nextreview_date:
                    reviewdata = {
                        'id':inde,
                        'NoOfDays': detail.NoOfDays if detail.NoOfDays else None,
                        'TimeInterval': detail.TimeInterval if detail.TimeInterval else None,
                        'Date': detail.Date if detail.TimeInterval else None,
                        'created_at': advice.created_at,
                        
                    }
                    review_list.append(reviewdata)
                    inde +=1
            else:
                review_list = None
                
                      
                    
                
            
                    
                
            
            
                            
                
                
            # Return the data
            return JsonResponse({
                'general_evaluation_data': general_evaluation_datas,
                'vital_details_data': vital_data,
                'prescription_list':prescription_list,
                'Lab_details':response_data,
                'Radiology_Testname':response_datas,
                'advice':advice_list,
                'referdoctor':refer_data,
                'next_reviewdate':review_list,
            }, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, safe=False)
 

#==================== patient Profile =====================================



@csrf_exempt
def patient_details_management_get_link(request):
    if request.method == 'GET':
        try:
            
            PatientID = request.GET.get('PatientId')
            print("PatientID",PatientID)
            if not PatientID:
                return JsonResponse({'warn':'Patient Id required'}, safe=False)
            print('Patientttt',PatientID)
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
            
          
            
            patient_ins = Patient_Detials.objects.get(PatientId = PatientID)
            print('Pattiiiieeeee',patient_ins)
            full_name =  f'{patient_ins.Title}.{patient_ins.FirstName} {patient_ins.MiddleName} {patient_ins.SurName}'
            patient = {
                'PatientId' : patient_ins.PatientId,
                'PatientName': full_name,
                'PhoneNo': patient_ins.PhoneNo,
                'Email':patient_ins.Email,
                'PatientProfile':get_file_image(patient_ins.Patient_profile) if patient_ins.Patient_profile else None
            }
            return JsonResponse(patient, safe=False)
        except Exception as e:
            return JsonResponse({'error':str(e)})
 
 
 
 #--------filter Phone and Aadhar No

@csrf_exempt
@require_http_methods(["GET"])
def Get_Patient_by_PhoneNo_Using_AbhaRegister(request):
    try:
        # Fetch query parameters
        first_name = request.GET.get("FirstName", '').strip()
        phone_no = request.GET.get("PhoneNo", '').strip()
        

        print(first_name, 'FirstName')
        print(phone_no, 'PhoneNo')
        
        # Build filter conditions
        filter_conditions = Q()
        if first_name:
            filter_conditions &= Q(name__icontains=first_name)
        if phone_no:
            filter_conditions &= Q(mobile__iexact=phone_no)
        
        # Query the database
        registration = ABHA_Collectin_Data.objects.filter(filter_conditions)

        patient_datas = []
        for reg in registration:
            patient_data = {
                'PhoneNo': reg.mobile,
                'FirstName': reg.name,
            } 
            patient_datas.append(patient_data)

        return JsonResponse(patient_datas, safe=False)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'An internal server error occurred'}, status=500)

 
 
        
# -----------------------------------ABHA------------------------------------------------------
@api_view(['POST'])
@csrf_exempt
def abha_register(request):
    # Extract public key from the request
    data = json.loads(request.body)
    aadhar = data.get('aadhaar_number')
    # publickey = data.get('public_key')
    
    public_key_pem  = """-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAstWB95C5pHLXiYW59qyO
4Xb+59KYVm9Hywbo77qETZVAyc6VIsxU+UWhd/k/YtjZibCznB+HaXWX9TVTFs9N
wgv7LRGq5uLczpZQDrU7dnGkl/urRA8p0Jv/f8T0MZdFWQgks91uFffeBmJOb58u
68ZRxSYGMPe4hb9XXKDVsgoSJaRNYviH7RgAI2QhTCwLEiMqIaUX3p1SAc178ZlN
8qHXSSGXvhDR1GKM+y2DIyJqlzfik7lD14mDY/I4lcbftib8cv7llkybtjX1Aayf
Zp4XpmIXKWv8nRM488/jOAF81Bi13paKgpjQUUuwq9tb5Qd/DChytYgBTBTJFe7i
rDFCmTIcqPr8+IMB7tXA3YXPp3z605Z6cGoYxezUm2Nz2o6oUmarDUntDhq/PnkN
ergmSeSvS8gD9DHBuJkJWZweG3xOPXiKQAUBr92mdFhJGm6fitO5jsBxgpmulxpG
0oKDy9lAOLWSqK92JMcbMNHn4wRikdI9HSiXrrI7fLhJYTbyU3I4v5ESdEsayHXu
iwO/1C8y56egzKSw44GAtEpbAkTNEEfK5H5R0QnVBIXOvfeF4tzGvmkfOO6nNXU3
o/WAdOyV3xSQ9dqLY5MEL4sJCGY1iJBIAQ452s8v0ynJG5Yq+8hNhsCVnklCzAls
IzQpnSVDUVEzv17grVAw078CAwEAAQ==
-----END PUBLIC KEY-----
"""

    
    public_key = serialization.load_pem_public_key(public_key_pem.encode())
    data_to_encrypt= aadhar
    
    encrypted_data = public_key.encrypt(
    data_to_encrypt.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None
        )
    )

    # Convert encrypted data to base64 for easier handling
    encrypted_base64 = base64.b64encode(encrypted_data).decode()

    # Output the encrypted data
    print("Encrypted Data (Base64):")
    print(encrypted_base64)
    # Generate a unique UUID
    request_id = str(uuid.uuid4())

    # Print or use the request ID as needed
    print("Request ID:", request_id)
    
    timestamp = datetime.utcnow().isoformat() + 'Z'
    print("timestamp",timestamp)

    # Step 2: Get Access Token
    token_response = requests.post(
        "https://dev.abdm.gov.in/api/hiecm/gateway/v3/sessions",
        json={
            "clientId": "SBXID_007255",
            "clientSecret": "286ced98-3001-41ac-8c32-7d9f5ca9cc3d",
            "grantType": "client_credentials"
        },
        headers={
            "Content-Type": "application/json",
            "REQUEST-ID": request_id,
            "TIMESTAMP": timestamp,
            "X-CM-ID": "sbx"
        }
    )        
        
    if token_response:
        token_data = token_response.json()
        
        access_token = token_data.get('accessToken')

        if access_token:
            print("Access Token:", access_token)
            aadhaar_number = aadhar
            print("aadhaar_number",aadhaar_number)
            
            otp_payload = {
                "txnId": "",
                "scope": ["abha-enrol"],
                "loginHint": "aadhaar",
                "loginId": encrypted_base64,
                "otpSystem": "aadhaar"
            }

            otp_response = requests.post(
                "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/request/otp",
                json=otp_payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {access_token}",
                    "REQUEST-ID": request_id,
                    "TIMESTAMP": timestamp,
                    "X-CM-ID": "sbx"
                }
            )

            print("OTP API Response:", otp_response.text)

            # Step 3: Return OTP response
            if otp_response:
                return JsonResponse({
                "otp_response": otp_response.json(),
                "access_token": access_token
            }, status=200)
            else:
                print("OTP API Error:", otp_response.json())
                return Response(otp_response.json(), status=400)
        else:
            print("Error: Access token not found")
            return Response({"error": "Access token not found"}, status=400)

    else:
        print("Token API Error:", token_response.json())
        return Response(token_response.json(), status=400)


def load_public_key(pem_data):
    return serialization.load_pem_public_key(
        pem_data.encode('utf-8'),
        backend=default_backend()
    )
def encrypt_aadhaar(aadhaar_number, public_key):
    # Convert the Aadhaar number to bytes
    aadhaar_bytes = aadhaar_number.encode('utf-8')

    # Encrypt the Aadhaar number using RSA encryption
    encrypted_aadhaar = public_key.encrypt(
        aadhaar_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Return the encrypted Aadhaar as a base64 encoded string
    return base64.b64encode(encrypted_aadhaar).decode('utf-8')

    
#-------------------------------abha_OTP_register--------------------------------------- 
    
@api_view(['POST'])
@csrf_exempt
def abha_OTP_register(request):
    
    data = json.loads(request.body)
    access_token = data.get('acctoken')
    request_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat() + 'Z'
    phone_no = data.get('PhoneNo')
    otp = data.get('otp')
    txn_id = data.get('txnId')
    
  

    
    if access_token:
        
        # Load Public Key
        public_key_pem = """-----BEGIN PUBLIC KEY-----
        MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAstWB95C5pHLXiYW59qyO
        4Xb+59KYVm9Hywbo77qETZVAyc6VIsxU+UWhd/k/YtjZibCznB+HaXWX9TVTFs9N
        wgv7LRGq5uLczpZQDrU7dnGkl/urRA8p0Jv/f8T0MZdFWQgks91uFffeBmJOb58u
        68ZRxSYGMPe4hb9XXKDVsgoSJaRNYviH7RgAI2QhTCwLEiMqIaUX3p1SAc178ZlN
        8qHXSSGXvhDR1GKM+y2DIyJqlzfik7lD14mDY/I4lcbftib8cv7llkybtjX1Aayf
        Zp4XpmIXKWv8nRM488/jOAF81Bi13paKgpjQUUuwq9tb5Qd/DChytYgBTBTJFe7i
        rDFCmTIcqPr8+IMB7tXA3YXPp3z605Z6cGoYxezUm2Nz2o6oUmarDUntDhq/PnkN
        ergmSeSvS8gD9DHBuJkJWZweG3xOPXiKQAUBr92mdFhJGm6fitO5jsBxgpmulxpG
        0oKDy9lAOLWSqK92JMcbMNHn4wRikdI9HSiXrrI7fLhJYTbyU3I4v5ESdEsayHXu
        iwO/1C8y56egzKSw44GAtEpbAkTNEEfK5H5R0QnVBIXOvfeF4tzGvmkfOO6nNXU3
        o/WAdOyV3xSQ9dqLY5MEL4sJCGY1iJBIAQ452s8v0ynJG5Yq+8hNhsCVnklCzAls
        IzQpnSVDUVEzv17grVAw078CAwEAAQ==
        -----END PUBLIC KEY-----
        """
        
        try:
            # Encrypt OTP
            public_key = serialization.load_pem_public_key(public_key_pem.encode())
            encrypted_data = public_key.encrypt(
                otp.encode(),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA1()),
                    algorithm=hashes.SHA1(),
                    label=None
                )
            )
            encrypted_base64 = base64.b64encode(encrypted_data).decode()
            

            # Prepare the request payload for ABHA API
            payload = {
                "authData": {
                    "authMethods": ["otp"],
                    "otp": {
                        "txnId": txn_id,
                        "otpValue": encrypted_base64,
                        "mobile": phone_no
                    }
                },
                "consent": {
                    "code": "abha-enrollment",
                    "version": "1.4"
                }
            }

            # Send OTP verification request to ABHA API
            response = requests.post(
                "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/byAadhaar",
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {access_token}",
                    "REQUEST-ID": request_id,
                    "TIMESTAMP": timestamp,
                    "X-CM-ID": "sbx"
                }
            )
            print("response",response.json())
            
            if response:
                return JsonResponse({
                "response": response.json()
            }, status=200)
            else:
                print("OTP API Error:", response.json())
                return Response(response.json(), status=400)

            
        except Exception as e:
            print(str(e))
            return JsonResponse({"error": "Failed in block", "details": str(e)}, status=500)

    else:
        print("Token API Error:", access_token)
        return JsonResponse({"error": "Failed to retrieve access token"})
    
# ------------------------------
@api_view(['POST'])
@csrf_exempt
def verifyOtpSubmit(request):
        data = json.loads(request.body)
        access_token = data.get('acctoken')
        request_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat() + 'Z'
        phone_no = data.get('PhoneNo')
        txn_id = data.get('txnId')
    
     # Load Public Key
        public_key_pem = """-----BEGIN PUBLIC KEY-----
        MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAstWB95C5pHLXiYW59qyO
        4Xb+59KYVm9Hywbo77qETZVAyc6VIsxU+UWhd/k/YtjZibCznB+HaXWX9TVTFs9N
        wgv7LRGq5uLczpZQDrU7dnGkl/urRA8p0Jv/f8T0MZdFWQgks91uFffeBmJOb58u
        68ZRxSYGMPe4hb9XXKDVsgoSJaRNYviH7RgAI2QhTCwLEiMqIaUX3p1SAc178ZlN
        8qHXSSGXvhDR1GKM+y2DIyJqlzfik7lD14mDY/I4lcbftib8cv7llkybtjX1Aayf
        Zp4XpmIXKWv8nRM488/jOAF81Bi13paKgpjQUUuwq9tb5Qd/DChytYgBTBTJFe7i
        rDFCmTIcqPr8+IMB7tXA3YXPp3z605Z6cGoYxezUm2Nz2o6oUmarDUntDhq/PnkN
        ergmSeSvS8gD9DHBuJkJWZweG3xOPXiKQAUBr92mdFhJGm6fitO5jsBxgpmulxpG
        0oKDy9lAOLWSqK92JMcbMNHn4wRikdI9HSiXrrI7fLhJYTbyU3I4v5ESdEsayHXu
        iwO/1C8y56egzKSw44GAtEpbAkTNEEfK5H5R0QnVBIXOvfeF4tzGvmkfOO6nNXU3
        o/WAdOyV3xSQ9dqLY5MEL4sJCGY1iJBIAQ452s8v0ynJG5Yq+8hNhsCVnklCzAls
        IzQpnSVDUVEzv17grVAw078CAwEAAQ==
        -----END PUBLIC KEY-----
        """
        
        data_to_encrypt = phone_no
        print("data_to_encrypt_PhoneNo:",data_to_encrypt)
        
        public_key = serialization.load_pem_public_key(public_key_pem.encode())
        # Encrypt the phone number
        encrypted_phoneNo = public_key.encrypt(
            data_to_encrypt.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
            )
        )
        encrypted_base64mobile = base64.b64encode(encrypted_phoneNo).decode()
        print("encrypted_base64mobile",encrypted_base64mobile)

        # Prepare the request payload for mobile update
        payload = {
            "txnId": txn_id,
            "scope": [
                "abha-enrol",
                "mobile-verify"
            ],
            "loginHint": "mobile",
            "loginId": encrypted_base64mobile,
            "otpSystem": "abdm"
        }

        print("Payload for mobile_update_OTP:", payload)

        # Send mobile update request
        response = requests.post(
            "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/request/otp",
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
                "REQUEST-ID": request_id,
                "TIMESTAMP": timestamp,
                
            }
        )
        if response:
            response = response.json()
            
            x_token = response.get('xToken')
            print("x_token:",x_token)
            
            print(response)
            return JsonResponse(response, status=200)
        else:
            print("Failed to parse mobile update OTP response:", response.json())
            return Response(response.json(), status=400)

        
# -------------------ABHA_Mobile_OTP----------------------

@api_view(['POST'])
@csrf_exempt
def ABHA_Mobile_OTP(request):
    print("Received Payload:", request.body)

    request_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat() + 'Z'

    # Public Key for OTP Encryption
    public_key_pem = """-----BEGIN PUBLIC KEY-----
    MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAstWB95C5pHLXiYW59qyO
    4Xb+59KYVm9Hywbo77qETZVAyc6VIsxU+UWhd/k/YtjZibCznB+HaXWX9TVTFs9N
    wgv7LRGq5uLczpZQDrU7dnGkl/urRA8p0Jv/f8T0MZdFWQgks91uFffeBmJOb58u
    68ZRxSYGMPe4hb9XXKDVsgoSJaRNYviH7RgAI2QhTCwLEiMqIaUX3p1SAc178ZlN
    8qHXSSGXvhDR1GKM+y2DIyJqlzfik7lD14mDY/I4lcbftib8cv7llkybtjX1Aayf
    Zp4XpmIXKWv8nRM488/jOAF81Bi13paKgpjQUUuwq9tb5Qd/DChytYgBTBTJFe7i
    rDFCmTIcqPr8+IMB7tXA3YXPp3z605Z6cGoYxezUm2Nz2o6oUmarDUntDhq/PnkN
    ergmSeSvS8gD9DHBuJkJWZweG3xOPXiKQAUBr92mdFhJGm6fitO5jsBxgpmulxpG
    0oKDy9lAOLWSqK92JMcbMNHn4wRikdI9HSiXrrI7fLhJYTbyU3I4v5ESdEsayHXu
    iwO/1C8y56egzKSw44GAtEpbAkTNEEfK5H5R0QnVBIXOvfeF4tzGvmkfOO6nNXU3
    o/WAdOyV3xSQ9dqLY5MEL4sJCGY1iJBIAQ452s8v0ynJG5Yq+8hNhsCVnklCzAls
    IzQpnSVDUVEzv17grVAw078CAwEAAQ==
    -----END PUBLIC KEY-----"""

    # Load the public key
    public_key = serialization.load_pem_public_key(public_key_pem.encode())

    data = json.loads(request.body)

    access_token = data.get('acctoken')
    txn_id = data.get('txnId')
    mobile_otp = data.get('MobileOtp')

    print("Parsed Data:", data)

    # Encrypt the OTP
    encrypted_data = public_key.encrypt(
        mobile_otp.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None
        )
    )
    encrypted_base64 = base64.b64encode(encrypted_data).decode()

    # Prepare payload for OTP verification
    payload = {
        "scope": ["abha-enrol", "mobile-verify"],
        "authData": {
            "authMethods": ["otp"],
            "otp": {
                "timeStamp": timestamp,
                "txnId": txn_id,
                "otpValue": encrypted_base64
            }
        }
    }

    # Send OTP verification request
    responsed = requests.post(
        "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/auth/byAbdm",
        json=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
            "REQUEST-ID": request_id,
            "TIMESTAMP": timestamp,
        }
    )
    
    if responsed:
        response_data = responsed.json()
        print(response_data)
        return JsonResponse(response_data)
    else:
        print("Failed to parse mobile update OTP response:", responsed.text)
        return JsonResponse({"error": "OTP Verification Failed", "details": responsed.text}, status=400)

# ---------------------------------------------------------

@api_view(['GET', 'POST'])
@csrf_exempt
def ABHA_Address_Suggestion_API(request):
    
    print("Received Payload:", request.body)
    
    data = json.loads(request.body)
    
    access_token = data.get('acctoken')  
    txn_id = data.get('txnId')
    abha_address=data.get("abhaaddress")

    print(f"Received access_token: {access_token}")
    print(f"Received txn_id: {txn_id}")
    print(f"Received txn_id: {abha_address}")

    request_id = str(uuid.uuid4())
    timestampww = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    print("timestampww",timestampww)

    # if request.method == 'POST':
    print("GET method called: Making the request to ABHA API for address suggestion")
    

    # suggestion_response = requests.get(
    #     "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/suggestion",
    #     headers={
    #         "Authorization": f"Bearer {access_token}",
    #         "txnId": txn_id,
    #         "REQUEST-ID": request_id,
    #         "TIMESTAMP": timestampww,
    #     }
    # )
    
    # print("ABHA API Response Status:", suggestion_response)
    # print("ABHA API Response Headers:", suggestion_response.content)
    # print("ABHA API Response Content:", suggestion_response.text)

    # if suggestion_response:
    #     response_data = suggestion_response.json()
        
    #     abha_address_list = response_data.get('abhaAddressList', [])
    #     if abha_address_list:
    #         abha_address = abha_address_list[0]  # Use the first address
    #         print("Selected ABHA Address:", abha_address)

    #         print("GET request completed successfully, making the POST request now")

    try:
        post_data = {
            "txnId": txn_id,
            "abhaAddress": abha_address,
            "preferred": 1,
        }

        post_response = requests.post(
            "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/abha-address",
            json=post_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
                "REQUEST-ID": request_id,
                "TIMESTAMP": timestampww,
            },
            
        )

        print("ABHA API POST Response Status:", post_response)
        print("ABHA API POST Response Content:", post_response.text)

        if post_response:
            return JsonResponse(post_response.json())  # Return the successful response from POST
        else:
            return JsonResponse({"error": post_response.text}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

        # else:
        #     return JsonResponse({"error": "No ABHA addresses found in response"}, status=400)

    # else:
    #     return JsonResponse({"error": suggestion_response.text}, status=400)

    # Logic for POST method (this part can be omitted as it is already handled after GET)
    # elif request.method == 'POST':
    #     return JsonResponse({"error": "POST method should not be directly called in this scenario"}, status=400)
    
    # if suggestion_response:
    #     return JsonResponse(suggestion_response.json())  # Return the successful response from POST
    # else:
    #     return JsonResponse({"error": suggestion_response.text}, status=400)
    
    
    
# -----------------------------------ABHA_card-----------------------------------------


@api_view(['POST'])
@csrf_exempt
def ABHA_card(request):
    data = json.loads(request.body)
    access_token = data.get('acctoken')
    X_token = data.get('xToken')
    
    print("X_token:", X_token)
    print("access_token:", access_token)
    
    request_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat() + 'Z'
    
    # First GET request to fetch ABHA data
    response_1 = requests.get(
        "https://abhasbx.abdm.gov.in/abha/api/v3/profile/account",
        headers={
            "Authorization": f"Bearer {access_token}",
            "REQUEST-ID": request_id,
            "TIMESTAMP": timestamp,
            "X-Token": f"Bearer {X_token}"
        }
    )

    # if response_1:
    response_data = response_1.json()
    
    print("Response from API:", response_1.json())


    # Extracting the necessary data to save into the database
    abha_Number = response_data.get('ABHANumber', '')
    print("abha_Number:",abha_Number)
    
    abha_address = response_data.get('preferredAbhaAddress', '')
    name = response_data.get('name', '')
    address = response_data.get('address', '')
    created_date = response_data.get('createdDate', '')

    created_date_obj = datetime.strptime(created_date, "%d-%m-%Y").date() if created_date else None
    
    day_of_birth = response_data.get('dayOfBirth', '')
    month_of_birth = response_data.get('monthOfBirth', '')
    year_of_birth = response_data.get('yearOfBirth', '')
    
    print("day_of_birth:",day_of_birth)
    print("month_of_birth:",month_of_birth)
    print("year_of_birth:",year_of_birth)
    
    district_name = response_data.get('districtName', '')
    email = response_data.get('email', '')
    gender = response_data.get('gender', '')
    pincode = response_data.get('pincode', '')
    mobile = response_data.get('mobile', '')
    mobile_verified = response_data.get('mobileVerified', False)
    state_name = response_data.get('stateName', '')
    status = response_data.get('status', '')
    subdistrict_name = response_data.get('subdistrictName', '')
    town_name = response_data.get('townName', '')
    verification_type = response_data.get('verificationType', '')
    birth_date = datetime(year=int(year_of_birth), month=int(month_of_birth), day=int(day_of_birth)).date()
    
    existing_data = ABHA_Collectin_Data.objects.filter(mobile=mobile).first()
    if existing_data:
        print("Record already exists for mobile:", mobile)
        return JsonResponse({"message": "Record already exists for the given mobile number."}, status=400)


    # Create a new ABHA record in the database
    abha_data = ABHA_Collectin_Data.objects.create(
        ABHA_RegID=None,  # Let the save method handle auto-increment
        ABHANumber=abha_Number,
        preferredAbhaAddress=abha_address,
        mobile=mobile,
        name=name,
        address=address,
        createdDate=created_date_obj,
        
        dayOfBirth=birth_date,  
        
        districtName=district_name,
        email=email,
        gender=gender,
        pincode=pincode,
        mobileVerified=mobile_verified,
        stateName=state_name,
        status=status,
        subdistrictName=subdistrict_name,
        townName=town_name,
        verificationType=verification_type
    )
    abha_data.save()
    print("abha_data:", abha_data)

    # Return the saved data as a success response
    if response_1:
        return JsonResponse(response_1.json())  # Return the successful response from POST
    else:
        return JsonResponse({"error": response_1.text}, status=400)
    
    # else:
    #     return JsonResponse({"error": response_1.json()}, status=400)

# ---------------------------------
@api_view(['GET'])
@csrf_exempt
def ABHA_card_get(request):
    if request.method == 'GET':
        try:
            MobileNo = request.GET.get('Mobile_No', None)
            ip_request_ins = ABHA_Collectin_Data.objects.filter(mobile=MobileNo)
            iprequest_list = []
            for datas in ip_request_ins:
                print(datas.mobile)
                data_list = {

                    'ABHA_RegID':datas.ABHA_RegID,
                    'ABHANumber':datas.ABHANumber,
                    'preferredAbhaAddress':datas.preferredAbhaAddress,
                    'name':datas.name,
                    'address':datas.address,
                    'createdDate':datas.createdDate,
                    'dayOfBirth':datas.dayOfBirth,
                    'districtName':datas.districtName,
                    'email':datas.email,
                    'gender':datas.gender,
                    'pincode':datas.pincode,
                    'mobile':datas.mobile,
                    'mobileVerified':datas.mobileVerified,
                    'stateName':datas.stateName,
                    'status':datas.status,
                    'subdistrictName':datas.subdistrictName,
                    'townName':datas.townName,
                    'verificationType':datas.verificationType,

                }
                iprequest_list.append(data_list)

            return JsonResponse(iprequest_list,safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
# -----------------------------------ABHA------------------------------------------------------
@api_view(['POST'])
@csrf_exempt
def abha_register(request):
    # Extract public key from the request
    data = json.loads(request.body)
    aadhar = data.get('aadhaar_number')
    # publickey = data.get('public_key')
    
    public_key_pem  = """-----BEGIN PUBLIC KEY-----
MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAstWB95C5pHLXiYW59qyO
4Xb+59KYVm9Hywbo77qETZVAyc6VIsxU+UWhd/k/YtjZibCznB+HaXWX9TVTFs9N
wgv7LRGq5uLczpZQDrU7dnGkl/urRA8p0Jv/f8T0MZdFWQgks91uFffeBmJOb58u
68ZRxSYGMPe4hb9XXKDVsgoSJaRNYviH7RgAI2QhTCwLEiMqIaUX3p1SAc178ZlN
8qHXSSGXvhDR1GKM+y2DIyJqlzfik7lD14mDY/I4lcbftib8cv7llkybtjX1Aayf
Zp4XpmIXKWv8nRM488/jOAF81Bi13paKgpjQUUuwq9tb5Qd/DChytYgBTBTJFe7i
rDFCmTIcqPr8+IMB7tXA3YXPp3z605Z6cGoYxezUm2Nz2o6oUmarDUntDhq/PnkN
ergmSeSvS8gD9DHBuJkJWZweG3xOPXiKQAUBr92mdFhJGm6fitO5jsBxgpmulxpG
0oKDy9lAOLWSqK92JMcbMNHn4wRikdI9HSiXrrI7fLhJYTbyU3I4v5ESdEsayHXu
iwO/1C8y56egzKSw44GAtEpbAkTNEEfK5H5R0QnVBIXOvfeF4tzGvmkfOO6nNXU3
o/WAdOyV3xSQ9dqLY5MEL4sJCGY1iJBIAQ452s8v0ynJG5Yq+8hNhsCVnklCzAls
IzQpnSVDUVEzv17grVAw078CAwEAAQ==
-----END PUBLIC KEY-----
"""

    
    public_key = serialization.load_pem_public_key(public_key_pem.encode())
    data_to_encrypt= aadhar
    
    encrypted_data = public_key.encrypt(
    data_to_encrypt.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None
        )
    )

    # Convert encrypted data to base64 for easier handling
    encrypted_base64 = base64.b64encode(encrypted_data).decode()

    # Output the encrypted data
    print("Encrypted Data (Base64):")
    print(encrypted_base64)
    # Generate a unique UUID
    request_id = str(uuid.uuid4())

    # Print or use the request ID as needed
    print("Request ID:", request_id)
    
    timestamp = datetime.utcnow().isoformat() + 'Z'
    print("timestamp",timestamp)

    # Step 2: Get Access Token
    token_response = requests.post(
        "https://dev.abdm.gov.in/api/hiecm/gateway/v3/sessions",
        json={
            "clientId": "SBXID_007255",
            "clientSecret": "286ced98-3001-41ac-8c32-7d9f5ca9cc3d",
            "grantType": "client_credentials"
        },
        headers={
            "Content-Type": "application/json",
            "REQUEST-ID": request_id,
            "TIMESTAMP": timestamp,
            "X-CM-ID": "sbx"
        }
    )        
        
    if token_response:
        token_data = token_response.json()
        
        access_token = token_data.get('accessToken')

        if access_token:
            print("Access Token:", access_token)
            aadhaar_number = aadhar
            print("aadhaar_number",aadhaar_number)
            
            otp_payload = {
                "txnId": "",
                "scope": ["abha-enrol"],
                "loginHint": "aadhaar",
                "loginId": encrypted_base64,
                "otpSystem": "aadhaar"
            }

            otp_response = requests.post(
                "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/request/otp",
                json=otp_payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {access_token}",
                    "REQUEST-ID": request_id,
                    "TIMESTAMP": timestamp,
                    "X-CM-ID": "sbx"
                }
            )

            print("OTP API Response:", otp_response.text)

            # Step 3: Return OTP response
            if otp_response:
                return JsonResponse({
                "otp_response": otp_response.json(),
                "access_token": access_token
            }, status=200)
            else:
                print("OTP API Error:", otp_response.json())
                return Response(otp_response.json(), status=400)
        else:
            print("Error: Access token not found")
            return Response({"error": "Access token not found"}, status=400)

    else:
        print("Token API Error:", token_response.json())
        return Response(token_response.json(), status=400)


def load_public_key(pem_data):
    return serialization.load_pem_public_key(
        pem_data.encode('utf-8'),
        backend=default_backend()
    )
def encrypt_aadhaar(aadhaar_number, public_key):
    # Convert the Aadhaar number to bytes
    aadhaar_bytes = aadhaar_number.encode('utf-8')

    # Encrypt the Aadhaar number using RSA encryption
    encrypted_aadhaar = public_key.encrypt(
        aadhaar_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Return the encrypted Aadhaar as a base64 encoded string
    return base64.b64encode(encrypted_aadhaar).decode('utf-8')

    
#-------------------------------abha_OTP_register--------------------------------------- 
    
@api_view(['POST'])
@csrf_exempt
def abha_OTP_register(request):
    
    data = json.loads(request.body)
    access_token = data.get('acctoken')
    request_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat() + 'Z'
    phone_no = data.get('PhoneNo')
    otp = data.get('otp')
    txn_id = data.get('txnId')
    
  

    
    if access_token:
        
        # Load Public Key
        public_key_pem = """-----BEGIN PUBLIC KEY-----
        MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAstWB95C5pHLXiYW59qyO
        4Xb+59KYVm9Hywbo77qETZVAyc6VIsxU+UWhd/k/YtjZibCznB+HaXWX9TVTFs9N
        wgv7LRGq5uLczpZQDrU7dnGkl/urRA8p0Jv/f8T0MZdFWQgks91uFffeBmJOb58u
        68ZRxSYGMPe4hb9XXKDVsgoSJaRNYviH7RgAI2QhTCwLEiMqIaUX3p1SAc178ZlN
        8qHXSSGXvhDR1GKM+y2DIyJqlzfik7lD14mDY/I4lcbftib8cv7llkybtjX1Aayf
        Zp4XpmIXKWv8nRM488/jOAF81Bi13paKgpjQUUuwq9tb5Qd/DChytYgBTBTJFe7i
        rDFCmTIcqPr8+IMB7tXA3YXPp3z605Z6cGoYxezUm2Nz2o6oUmarDUntDhq/PnkN
        ergmSeSvS8gD9DHBuJkJWZweG3xOPXiKQAUBr92mdFhJGm6fitO5jsBxgpmulxpG
        0oKDy9lAOLWSqK92JMcbMNHn4wRikdI9HSiXrrI7fLhJYTbyU3I4v5ESdEsayHXu
        iwO/1C8y56egzKSw44GAtEpbAkTNEEfK5H5R0QnVBIXOvfeF4tzGvmkfOO6nNXU3
        o/WAdOyV3xSQ9dqLY5MEL4sJCGY1iJBIAQ452s8v0ynJG5Yq+8hNhsCVnklCzAls
        IzQpnSVDUVEzv17grVAw078CAwEAAQ==
        -----END PUBLIC KEY-----
        """
        
        try:
            # Encrypt OTP
            public_key = serialization.load_pem_public_key(public_key_pem.encode())
            encrypted_data = public_key.encrypt(
                otp.encode(),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA1()),
                    algorithm=hashes.SHA1(),
                    label=None
                )
            )
            encrypted_base64 = base64.b64encode(encrypted_data).decode()
            

            # Prepare the request payload for ABHA API
            payload = {
                "authData": {
                    "authMethods": ["otp"],
                    "otp": {
                        "txnId": txn_id,
                        "otpValue": encrypted_base64,
                        "mobile": phone_no
                    }
                },
                "consent": {
                    "code": "abha-enrollment",
                    "version": "1.4"
                }
            }

            # Send OTP verification request to ABHA API
            response = requests.post(
                "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/byAadhaar",
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {access_token}",
                    "REQUEST-ID": request_id,
                    "TIMESTAMP": timestamp,
                    "X-CM-ID": "sbx"
                }
            )
            print("response",response.json())
            
            if response:
                return JsonResponse({
                "response": response.json()
            }, status=200)
            else:
                print("OTP API Error:", response.json())
                return Response(response.json(), status=400)

            
        except Exception as e:
            print(str(e))
            return JsonResponse({"error": "Failed in block", "details": str(e)}, status=500)

    else:
        print("Token API Error:", access_token)
        return JsonResponse({"error": "Failed to retrieve access token"})
    
# ------------------------------
@api_view(['POST'])
@csrf_exempt
def verifyOtpSubmit(request):
        data = json.loads(request.body)
        access_token = data.get('acctoken')
        request_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat() + 'Z'
        phone_no = data.get('PhoneNo')
        txn_id = data.get('txnId')
    
     # Load Public Key
        public_key_pem = """-----BEGIN PUBLIC KEY-----
        MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAstWB95C5pHLXiYW59qyO
        4Xb+59KYVm9Hywbo77qETZVAyc6VIsxU+UWhd/k/YtjZibCznB+HaXWX9TVTFs9N
        wgv7LRGq5uLczpZQDrU7dnGkl/urRA8p0Jv/f8T0MZdFWQgks91uFffeBmJOb58u
        68ZRxSYGMPe4hb9XXKDVsgoSJaRNYviH7RgAI2QhTCwLEiMqIaUX3p1SAc178ZlN
        8qHXSSGXvhDR1GKM+y2DIyJqlzfik7lD14mDY/I4lcbftib8cv7llkybtjX1Aayf
        Zp4XpmIXKWv8nRM488/jOAF81Bi13paKgpjQUUuwq9tb5Qd/DChytYgBTBTJFe7i
        rDFCmTIcqPr8+IMB7tXA3YXPp3z605Z6cGoYxezUm2Nz2o6oUmarDUntDhq/PnkN
        ergmSeSvS8gD9DHBuJkJWZweG3xOPXiKQAUBr92mdFhJGm6fitO5jsBxgpmulxpG
        0oKDy9lAOLWSqK92JMcbMNHn4wRikdI9HSiXrrI7fLhJYTbyU3I4v5ESdEsayHXu
        iwO/1C8y56egzKSw44GAtEpbAkTNEEfK5H5R0QnVBIXOvfeF4tzGvmkfOO6nNXU3
        o/WAdOyV3xSQ9dqLY5MEL4sJCGY1iJBIAQ452s8v0ynJG5Yq+8hNhsCVnklCzAls
        IzQpnSVDUVEzv17grVAw078CAwEAAQ==
        -----END PUBLIC KEY-----
        """
        
        data_to_encrypt = phone_no
        print("data_to_encrypt_PhoneNo:",data_to_encrypt)
        
        public_key = serialization.load_pem_public_key(public_key_pem.encode())
        # Encrypt the phone number
        encrypted_phoneNo = public_key.encrypt(
            data_to_encrypt.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
            )
        )
        encrypted_base64mobile = base64.b64encode(encrypted_phoneNo).decode()
        print("encrypted_base64mobile",encrypted_base64mobile)

        # Prepare the request payload for mobile update
        payload = {
            "txnId": txn_id,
            "scope": [
                "abha-enrol",
                "mobile-verify"
            ],
            "loginHint": "mobile",
            "loginId": encrypted_base64mobile,
            "otpSystem": "abdm"
        }

        print("Payload for mobile_update_OTP:", payload)

        # Send mobile update request
        response = requests.post(
            "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/request/otp",
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
                "REQUEST-ID": request_id,
                "TIMESTAMP": timestamp,
                
            }
        )
        if response:
            response = response.json()
            
            x_token = response.get('xToken')
            print("x_token:",x_token)
            
            print(response)
            return JsonResponse(response, status=200)
        else:
            print("Failed to parse mobile update OTP response:", response.json())
            return Response(response.json(), status=400)

        
# -------------------ABHA_Mobile_OTP----------------------

@api_view(['POST'])
@csrf_exempt
def ABHA_Mobile_OTP(request):
    print("Received Payload:", request.body)

    request_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat() + 'Z'

    # Public Key for OTP Encryption
    public_key_pem = """-----BEGIN PUBLIC KEY-----
    MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAstWB95C5pHLXiYW59qyO
    4Xb+59KYVm9Hywbo77qETZVAyc6VIsxU+UWhd/k/YtjZibCznB+HaXWX9TVTFs9N
    wgv7LRGq5uLczpZQDrU7dnGkl/urRA8p0Jv/f8T0MZdFWQgks91uFffeBmJOb58u
    68ZRxSYGMPe4hb9XXKDVsgoSJaRNYviH7RgAI2QhTCwLEiMqIaUX3p1SAc178ZlN
    8qHXSSGXvhDR1GKM+y2DIyJqlzfik7lD14mDY/I4lcbftib8cv7llkybtjX1Aayf
    Zp4XpmIXKWv8nRM488/jOAF81Bi13paKgpjQUUuwq9tb5Qd/DChytYgBTBTJFe7i
    rDFCmTIcqPr8+IMB7tXA3YXPp3z605Z6cGoYxezUm2Nz2o6oUmarDUntDhq/PnkN
    ergmSeSvS8gD9DHBuJkJWZweG3xOPXiKQAUBr92mdFhJGm6fitO5jsBxgpmulxpG
    0oKDy9lAOLWSqK92JMcbMNHn4wRikdI9HSiXrrI7fLhJYTbyU3I4v5ESdEsayHXu
    iwO/1C8y56egzKSw44GAtEpbAkTNEEfK5H5R0QnVBIXOvfeF4tzGvmkfOO6nNXU3
    o/WAdOyV3xSQ9dqLY5MEL4sJCGY1iJBIAQ452s8v0ynJG5Yq+8hNhsCVnklCzAls
    IzQpnSVDUVEzv17grVAw078CAwEAAQ==
    -----END PUBLIC KEY-----"""

    # Load the public key
    public_key = serialization.load_pem_public_key(public_key_pem.encode())

    data = json.loads(request.body)

    access_token = data.get('acctoken')
    txn_id = data.get('txnId')
    mobile_otp = data.get('MobileOtp')

    print("Parsed Data:", data)

    # Encrypt the OTP
    encrypted_data = public_key.encrypt(
        mobile_otp.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None
        )
    )
    encrypted_base64 = base64.b64encode(encrypted_data).decode()

    # Prepare payload for OTP verification
    payload = {
        "scope": ["abha-enrol", "mobile-verify"],
        "authData": {
            "authMethods": ["otp"],
            "otp": {
                "timeStamp": timestamp,
                "txnId": txn_id,
                "otpValue": encrypted_base64
            }
        }
    }

    # Send OTP verification request
    responsed = requests.post(
        "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/auth/byAbdm",
        json=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
            "REQUEST-ID": request_id,
            "TIMESTAMP": timestamp,
        }
    )
    
    if responsed:
        response_data = responsed.json()
        print(response_data)
        return JsonResponse(response_data)
    else:
        print("Failed to parse mobile update OTP response:", responsed.text)
        return JsonResponse({"error": "OTP Verification Failed", "details": responsed.text}, status=400)

# ---------------------------------------------------------

@api_view(['GET', 'POST'])
@csrf_exempt
def ABHA_Address_Suggestion_API(request):
    
    print("Received Payload:", request.body)
    
    data = json.loads(request.body)
    
    access_token = data.get('acctoken')  
    txn_id = data.get('txnId')
    abha_address=data.get("abhaaddress")

    print(f"Received access_token: {access_token}")
    print(f"Received txn_id: {txn_id}")
    print(f"Received txn_id: {abha_address}")

    request_id = str(uuid.uuid4())
    timestampww = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    print("timestampww",timestampww)

    # if request.method == 'POST':
    print("GET method called: Making the request to ABHA API for address suggestion")
    

    # suggestion_response = requests.get(
    #     "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/suggestion",
    #     headers={
    #         "Authorization": f"Bearer {access_token}",
    #         "txnId": txn_id,
    #         "REQUEST-ID": request_id,
    #         "TIMESTAMP": timestampww,
    #     }
    # )
    
    # print("ABHA API Response Status:", suggestion_response)
    # print("ABHA API Response Headers:", suggestion_response.content)
    # print("ABHA API Response Content:", suggestion_response.text)

    # if suggestion_response:
    #     response_data = suggestion_response.json()
        
    #     abha_address_list = response_data.get('abhaAddressList', [])
    #     if abha_address_list:
    #         abha_address = abha_address_list[0]  # Use the first address
    #         print("Selected ABHA Address:", abha_address)

    #         print("GET request completed successfully, making the POST request now")

    try:
        post_data = {
            "txnId": txn_id,
            "abhaAddress": abha_address,
            "preferred": 1,
        }

        post_response = requests.post(
            "https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/abha-address",
            json=post_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}",
                "REQUEST-ID": request_id,
                "TIMESTAMP": timestampww,
            },
            
        )

        print("ABHA API POST Response Status:", post_response)
        print("ABHA API POST Response Content:", post_response.text)

        if post_response:
            return JsonResponse(post_response.json())  # Return the successful response from POST
        else:
            return JsonResponse({"error": post_response.text}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

        # else:
        #     return JsonResponse({"error": "No ABHA addresses found in response"}, status=400)

    # else:
    #     return JsonResponse({"error": suggestion_response.text}, status=400)

    # Logic for POST method (this part can be omitted as it is already handled after GET)
    # elif request.method == 'POST':
    #     return JsonResponse({"error": "POST method should not be directly called in this scenario"}, status=400)
    
    # if suggestion_response:
    #     return JsonResponse(suggestion_response.json())  # Return the successful response from POST
    # else:
    #     return JsonResponse({"error": suggestion_response.text}, status=400)
    
    
    
# -----------------------------------ABHA_card-----------------------------------------


@api_view(['POST'])
@csrf_exempt
def ABHA_card(request):
    data = json.loads(request.body)
    access_token = data.get('acctoken')
    X_token = data.get('xToken')
    
    print("X_token:", X_token)
    print("access_token:", access_token)
    
    request_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat() + 'Z'
    
    # First GET request to fetch ABHA data
    response_1 = requests.get(
        "https://abhasbx.abdm.gov.in/abha/api/v3/profile/account",
        headers={
            "Authorization": f"Bearer {access_token}",
            "REQUEST-ID": request_id,
            "TIMESTAMP": timestamp,
            "X-Token": f"Bearer {X_token}"
        }
    )

    # if response_1:
    response_data = response_1.json()
    
    print("Response from API:", response_1.json())


    # Extracting the necessary data to save into the database
    abha_Number = response_data.get('ABHANumber', '')
    print("abha_Number:",abha_Number)
    
    abha_address = response_data.get('preferredAbhaAddress', '')
    name = response_data.get('name', '')
    address = response_data.get('address', '')
    created_date = response_data.get('createdDate', '')

    created_date_obj = datetime.strptime(created_date, "%d-%m-%Y").date() if created_date else None
    
    day_of_birth = response_data.get('dayOfBirth', '')
    month_of_birth = response_data.get('monthOfBirth', '')
    year_of_birth = response_data.get('yearOfBirth', '')
    
    print("day_of_birth:",day_of_birth)
    print("month_of_birth:",month_of_birth)
    print("year_of_birth:",year_of_birth)
    
    district_name = response_data.get('districtName', '')
    email = response_data.get('email', '')
    gender = response_data.get('gender', '')
    pincode = response_data.get('pincode', '')
    mobile = response_data.get('mobile', '')
    mobile_verified = response_data.get('mobileVerified', False)
    state_name = response_data.get('stateName', '')
    status = response_data.get('status', '')
    subdistrict_name = response_data.get('subdistrictName', '')
    town_name = response_data.get('townName', '')
    verification_type = response_data.get('verificationType', '')
    birth_date = datetime(year=int(year_of_birth), month=int(month_of_birth), day=int(day_of_birth)).date()
    
    existing_data = ABHA_Collectin_Data.objects.filter(mobile=mobile).first()
    if existing_data:
        print("Record already exists for mobile:", mobile)
        return JsonResponse({"message": "Record already exists for the given mobile number."}, status=400)


    # Create a new ABHA record in the database
    abha_data = ABHA_Collectin_Data.objects.create(
        ABHA_RegID=None,  # Let the save method handle auto-increment
        ABHANumber=abha_Number,
        preferredAbhaAddress=abha_address,
        mobile=mobile,
        name=name,
        address=address,
        createdDate=created_date_obj,
        
        dayOfBirth=birth_date,  
        
        districtName=district_name,
        email=email,
        gender=gender,
        pincode=pincode,
        mobileVerified=mobile_verified,
        stateName=state_name,
        status=status,
        subdistrictName=subdistrict_name,
        townName=town_name,
        verificationType=verification_type
    )
    abha_data.save()
    print("abha_data:", abha_data)

    # Return the saved data as a success response
    if response_1:
        return JsonResponse(response_1.json())  # Return the successful response from POST
    else:
        return JsonResponse({"error": response_1.text}, status=400)
    
    # else:
    #     return JsonResponse({"error": response_1.json()}, status=400)

# ---------------------------------
@api_view(['GET'])
@csrf_exempt
def ABHA_card_get(request):
    if request.method == 'GET':
        try:
            MobileNo = request.GET.get('Mobile_No', None)
            ip_request_ins = ABHA_Collectin_Data.objects.filter(mobile=MobileNo)
            iprequest_list = []
            for datas in ip_request_ins:
                print(datas.mobile)
                data_list = {

                    'ABHA_RegID':datas.ABHA_RegID,
                    'ABHANumber':datas.ABHANumber,
                    'preferredAbhaAddress':datas.preferredAbhaAddress,
                    'name':datas.name,
                    'address':datas.address,
                    'createdDate':datas.createdDate,
                    'dayOfBirth':datas.dayOfBirth,
                    'districtName':datas.districtName,
                    'email':datas.email,
                    'gender':datas.gender,
                    'pincode':datas.pincode,
                    'mobile':datas.mobile,
                    'mobileVerified':datas.mobileVerified,
                    'stateName':datas.stateName,
                    'status':datas.status,
                    'subdistrictName':datas.subdistrictName,
                    'townName':datas.townName,
                    'verificationType':datas.verificationType,

                }
                iprequest_list.append(data_list)

            return JsonResponse(iprequest_list,safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
        
# ------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------
@api_view(['GET'])
@csrf_exempt
def search_patients_by_phone(request):
    phone = request.GET.get('phone', '').strip()
    print("phone:",phone)
    if not phone:
        return Response({'error': 'Phone number is required'}, status=400)
    
    patients = Patient_Detials.objects.filter(PhoneNo=phone)
    print("patients:",patients)
    data = [{
        'PatientId': p.PatientId,
        'FirstName': p.FirstName,
        'MiddleName': p.MiddleName or '',
        'SurName': p.SurName or '',
        'PhoneNo': p.PhoneNo,
        'Status': p.Status or 'Unknown'
    } for p in patients]
    print("data:",data)
    return Response(data if data else [], status=200)
from django.shortcuts import get_object_or_404

@api_view(['POST'])
@csrf_exempt
def add_family_members(request):
    try:
        primary_patient_id = request.data.get('primary_patient_id')
        family_member_ids = request.data.get('family_member_ids', [])

        if not primary_patient_id:
            return Response({'error': 'Primary patient ID is required'}, status=400)

        print("primary_patient_id:", primary_patient_id)
        print('family_member_ids:', family_member_ids)

        primary_patient = get_object_or_404(Patient_Detials, PatientId=primary_patient_id)

        # Create family member relationships
        for member_id in family_member_ids:
            if member_id != primary_patient_id: 
                family_member = get_object_or_404(Patient_Detials, PatientId=member_id)
                FamilyMember.objects.get_or_create(primary_patient=primary_patient, family_member=family_member)

        family_members = FamilyMember.objects.filter(primary_patient=primary_patient)
        print("family_members:",family_members)
        data = [{
            'id': fm.family_member.PatientId,
            'name': f"{fm.family_member.FirstName} {fm.family_member.MiddleName or ''} {fm.family_member.SurName or ''}".strip(),
            'mobileNumber': fm.family_member.PhoneNo,
        } for fm in family_members]

        print("Updated family members:", data)
        return Response(data, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['PUT'])
@csrf_exempt
def update_family_members(request, patient_id):
    try:
        patient = Patient_Detials.objects.get(PatientId=patient_id)
        
        family_member_ids = request.data.get("family_member_ids", [])

        if not family_member_ids:
            return Response({'error': 'No family members provided'}, status=400)

        FamilyMember.objects.filter(primary_patient=patient).delete()

        for member_id in family_member_ids:
            if member_id != patient_id:  
                family_member = get_object_or_404(Patient_Detials, PatientId=member_id)
                FamilyMember.objects.create(primary_patient=patient, family_member=family_member)

        family_members = FamilyMember.objects.filter(primary_patient=patient)
        data = [{
            'id': fm.family_member.PatientId,
            'name': f"{fm.family_member.FirstName} {fm.family_member.MiddleName or ''} {fm.family_member.SurName or ''}".strip(),
            'mobileNumber': fm.family_member.PhoneNo,
        } for fm in family_members]
        
        return Response(data, status=200)
        
    except Patient_Detials.DoesNotExist:
        return Response({'error': 'Patient not found'}, status=404)
