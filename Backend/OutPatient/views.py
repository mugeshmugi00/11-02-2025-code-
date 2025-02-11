
from Frontoffice.models import *
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import  Q
from django.http import JsonResponse
import base64
# import magic
import filetype
from .models import *

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
def get_workbenchquelist_doctor(request):
    try:
        # Get query parameters
        RegistrationId = request.GET.get('RegistrationId', '').strip()
        type = request.GET.get('Type', '').strip()

        if not RegistrationId:
            return JsonResponse({'error': 'RegistrationId is required'}, status=400)

        # Check if patient exists based on type
        LabRequest = None
        if type == 'OP':
            patient_instance = Patient_Appointment_Registration_Detials.objects.filter(pk=RegistrationId).first()
            LabRequest = Lab_Request_Details.objects.filter(OP_Register_Id=patient_instance.id).first()
        elif type == 'IP':
            patient_instance = Patient_IP_Registration_Detials.objects.filter(pk=RegistrationId).first()
        elif type == 'Casuality':
            patient_instance = Patient_Emergency_Registration_Detials.objects.filter(pk=RegistrationId).first()
        else:
            return JsonResponse({'error': 'Invalid type'}, status=400)

        if not patient_instance:
            return JsonResponse({'error': 'Patient not found'}, status=404)

        # Safely handle BloodGroup
        BloodGroup = patient_instance.PatientId.BloodGroup.pk if patient_instance.PatientId.BloodGroup else None

        # Safely handle PatientProfile
        PatientProfile = get_file_image(patient_instance.PatientId.Patient_profile) if patient_instance.PatientId.Patient_profile else None

        # Safely build Address
        Address = f"{patient_instance.PatientId.DoorNo or ''} {patient_instance.PatientId.Street or ''} {patient_instance.PatientId.Area or ''} {patient_instance.PatientId.City or ''} {patient_instance.PatientId.State or ''} {patient_instance.PatientId.Country or ''} {patient_instance.PatientId.Pincode or ''}".strip()
        category_name = ''
        if patient_instance.PatientCategory == 'Insurance':
            category_name = patient_instance.InsuranceName.Insurance_Name if patient_instance.InsuranceName else None
        elif patient_instance.PatientCategory == 'Client':
            category_name = patient_instance.ClientName.Client_Name if patient_instance.ClientName else None
 
        # Build the response dictionary
        OPRegistration_dict = {
            'pk': patient_instance.pk,
            'PatientProfile': PatientProfile,
            'RegistrationId': patient_instance.Registration_Id,
            'PatientId': patient_instance.PatientId.PatientId,
            'VisitId': patient_instance.VisitId if type == 'OP' else None,
            'PatientName': f"{patient_instance.PatientId.Title.Title_Name if patient_instance.PatientId.Title else None}.{patient_instance.PatientId.FirstName if patient_instance.PatientId else None} {patient_instance.PatientId.MiddleName if patient_instance.PatientId else None} {patient_instance.PatientId.SurName if patient_instance.PatientId else None}",
            'PhoneNo': patient_instance.PatientId.PhoneNo,
            'Title': patient_instance.PatientId.Title.pk if patient_instance.PatientId.Title else None,
            'FirstName': patient_instance.PatientId.FirstName,
            'MiddleName': patient_instance.PatientId.MiddleName,
            'SurName': patient_instance.PatientId.SurName,
            'Gender': patient_instance.PatientId.Gender,
            # 'AliasName': patient_instance.PatientId.AliasName,
            'DOB': patient_instance.PatientId.DOB,
            'Age': patient_instance.PatientId.Age,
            'Address': Address,
            'BloodGroup': BloodGroup,
            'PatientType': patient_instance.PatientId.PatientType,
            'VisitPurpose': patient_instance.VisitPurpose if type == 'OP' else None,
            'Specialization': patient_instance.Specialization.Speciality_Id if patient_instance.Specialization else '',
            'DoctorName' : (
                f"{patient_instance.PrimaryDoctor.Tittle.Title_Name if patient_instance.PrimaryDoctor and patient_instance.PrimaryDoctor.Tittle else ''}."
                f"{patient_instance.PrimaryDoctor.First_Name if patient_instance.PrimaryDoctor else ''} "
                f"{patient_instance.PrimaryDoctor.Last_Name if patient_instance.PrimaryDoctor else ''}"
            ),

            
            # 'DoctorName': patient_instance.PrimaryDoctor.Doctor_ID if patient_instance.PrimaryDoctor else '',
            'DoctorId': patient_instance.PrimaryDoctor.Doctor_ID if patient_instance.PrimaryDoctor else '',
            'Complaint': patient_instance.Complaint,
            'PatientCategory': patient_instance.PatientCategory,
            'PatientCategoryName' : category_name,
            'IsMLC': patient_instance.IsMLC,
            'CurrDate': patient_instance.PatientId.created_at.strftime('%d-%m-%y') if patient_instance.PatientId.created_at else "",
            'CurrTime': patient_instance.PatientId.created_at.strftime('%I:%M %p') if patient_instance.PatientId.created_at else "",
            "LabRequestId": LabRequest.Request_Id if LabRequest is not None else None
        }

        # Log the final dictionary
        print(f"OPRegistration_dict: {OPRegistration_dict}")

        return JsonResponse(OPRegistration_dict, safe=False)

    except Exception as e:
        # Log the error with traceback
        import traceback
        print(f"Error in get_workbenchquelist_doctor: {str(e)}\n{traceback.format_exc()}")
        return JsonResponse({'error': str(e)}, status=500)





# Create your views here.

# @csrf_exempt
# @require_http_methods(["GET"])
# def get_workbenchquelist_doctor(request):
#     try:
#         RegistrationId = request.GET.get('RegistrationId', '').strip()
#         type = request.GET.get('Type', '').strip()

#         if not RegistrationId :
#             return JsonResponse({'error': 'PatientId and VisitId are required'}, status=400)
        
#         if type == 'OP':
#             # Query the appointment details
#             try:
#                 patient_instance = Patient_Appointment_Registration_Detials.objects.get(pk = RegistrationId)
#             except Patient_Appointment_Registration_Detials.DoesNotExist:
#                 return JsonResponse({'error': 'Patient not found'}, status=404)

#         elif type == 'IP':
#             try:
#                 patient_instance = Patient_IP_Registration_Detials.objects.get(pk = RegistrationId)
#             except Patient_IP_Registration_Detials.DoesNotExist:
#                 return JsonResponse({'error': 'Patient not found'}, status=404)
        
#         elif type == 'Casuality':
#             try:
#                 patient_instance = Patient_Casuality_Registration_Detials.objects.get(pk = RegistrationId)
#             except Patient_Casuality_Registration_Detials.DoesNotExist:
#                 return JsonResponse({'error': 'Patient not found'}, status=404)

#         else:
#             return JsonResponse({'error': 'Invalid type'}, status=400)
       
#         Flagging_name = patient_instance.Flagging.Flagg_Name if patient_instance.Flagging else None
#         Flagging_color = patient_instance.Flagging.Flagg_Color if patient_instance.Flagging else None
            
#         # Serialize the filtered queryset
#         OPRegistration_dict = {
#             'pk':patient_instance.pk,
#             'PatientProfile':get_file_image(patient_instance.PatientId.Patient_profile),
#             'RegistrationId': patient_instance.Registration_Id,
#             'PatientId': patient_instance.PatientId.PatientId,
#             'VisitId': patient_instance.VisitId,
#             'PatientName': f'{patient_instance.PatientId.Title}.{patient_instance.PatientId.FirstName} {patient_instance.PatientId.MiddleName} {patient_instance.PatientId.SurName}',
#             'PhoneNo': patient_instance.PatientId.PhoneNo,
#             'Title': patient_instance.PatientId.Title,
#             'FirstName': patient_instance.PatientId.FirstName,
#             'MiddleName': patient_instance.PatientId.MiddleName,
#             'SurName': patient_instance.PatientId.SurName,
#             'Gender': patient_instance.PatientId.Gender,
#             'AliasName': patient_instance.PatientId.AliasName,
#             'DOB': patient_instance.PatientId.DOB,
#             'Age': patient_instance.PatientId.Age,
#             'Address': f'{patient_instance.PatientId.DoorNo}.{patient_instance.PatientId.Street}.{patient_instance.PatientId.Area}.{patient_instance.PatientId.City}.{patient_instance.PatientId.State}.{patient_instance.PatientId.Country}.{patient_instance.PatientId.Pincode}',
#             'BloodGroup': patient_instance.PatientId.BloodGroup,
#             'VisitPurpose': patient_instance.VisitPurpose if type == 'OP' else None,
#             'Specialization': patient_instance.Specialization.Speciality_Id if patient_instance.Specialization else '',
#             'DoctorName': patient_instance.PrimaryDoctor.Doctor_ID,
#             'DoctorId': patient_instance.PrimaryDoctor.Doctor_ID,
#             'Complaint': patient_instance.Complaint,
#             'PatientType': patient_instance.PatientType,
#             'PatientCategory': patient_instance.PatientCategory,
#             'IsMLC': patient_instance.IsMLC,
#             'Flagging': patient_instance.Flagging,
#             'Flagging': Flagging_name,
#             'FlaggingColour': Flagging_color,
#             'CurrDate': patient_instance.PatientId.created_at.strftime('%d-%m-%y') if patient_instance.PatientId.created_at else "",
#             'CurrTime': patient_instance.PatientId.created_at.strftime('%I:%M %p') if patient_instance.PatientId.created_at else "",
                    
#         }



#         return JsonResponse(OPRegistration_dict)
        
        

#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)






# @csrf_exempt
# @require_http_methods(["GET"])
# def get_workbenchquelist_doctor(request):
#     try:
#         # Get query parameters
#         RegistrationId = request.GET.get('RegistrationId', '').strip()
#         type = request.GET.get('Type', '').strip()

#         if not RegistrationId:
#             return JsonResponse({'error': 'PatientId and VisitId are required'}, status=400)

#         # Check if patient exists based on type
#         if type == 'OP':
#             try:
#                 patient_instance = Patient_Appointment_Registration_Detials.objects.get(pk=RegistrationId)
#             except Patient_Appointment_Registration_Detials.DoesNotExist:
#                 return JsonResponse({'error': 'Patient not found'}, status=404)

#         elif type == 'IP':
#             try:
#                 patient_instance = Patient_IP_Registration_Detials.objects.get(pk=RegistrationId)
#             except Patient_IP_Registration_Detials.DoesNotExist:
#                 return JsonResponse({'error': 'Patient not found'}, status=404)

#         elif type == 'Casuality':
#             try:
#                 patient_instance = Patient_Casuality_Registration_Detials.objects.get(pk=RegistrationId)
#             except Patient_Casuality_Registration_Detials.DoesNotExist:
#                 return JsonResponse({'error': 'Patient not found'}, status=404)

#         else:
#             return JsonResponse({'error': 'Invalid type'}, status=400)

#         # Safe handling of Flagging and BloodGroup (added logging)
#         Flagging_name = patient_instance.Flagging.Flagg_Name if patient_instance.Flagging else None
#         Flagging_color = patient_instance.Flagging.Flagg_Color if patient_instance.Flagging else None

#         # Safely handling BloodGroup
#         BloodGroup = None
#         if patient_instance.PatientId.BloodGroup:
#             BloodGroup = patient_instance.PatientId.BloodGroup.pk

#         # Debugging logs
#         print(f"Flagging: {Flagging_name}, {Flagging_color}")
#         print(f"BloodGroup: {BloodGroup}")
        
#         # Build the response dictionary safely
#         OPRegistration_dict = {
#             'pk': patient_instance.pk,
#             'PatientProfile': get_file_image(patient_instance.PatientId.Patient_profile),
#             'RegistrationId': patient_instance.Registration_Id,
#             'PatientId': patient_instance.PatientId.PatientId,
#             'VisitId': patient_instance.VisitId,
#             'PatientName': f'{patient_instance.PatientId.Title}.{patient_instance.PatientId.FirstName} {patient_instance.PatientId.MiddleName} {patient_instance.PatientId.SurName}',
#             'PhoneNo': patient_instance.PatientId.PhoneNo,
#             'Title': patient_instance.PatientId.Title,
#             'FirstName': patient_instance.PatientId.FirstName,
#             'MiddleName': patient_instance.PatientId.MiddleName,
#             'SurName': patient_instance.PatientId.SurName,
#             'Gender': patient_instance.PatientId.Gender,
#             'AliasName': patient_instance.PatientId.AliasName,
#             'DOB': patient_instance.PatientId.DOB,
#             'Age': patient_instance.PatientId.Age,
#             'Address': f'{patient_instance.PatientId.DoorNo}.{patient_instance.PatientId.Street}.{patient_instance.PatientId.Area}.{patient_instance.PatientId.City}.{patient_instance.PatientId.State}.{patient_instance.PatientId.Country}.{patient_instance.PatientId.Pincode}',
#             'BloodGroup': BloodGroup,  # Safely passing BloodGroup as None if it doesn't exist
#             'VisitPurpose': patient_instance.VisitPurpose if type == 'OP' else None,
#             'Specialization': patient_instance.Specialization.Speciality_Id if patient_instance.Specialization else '',
#             'DoctorName': patient_instance.PrimaryDoctor.Doctor_ID,
#             'DoctorId': patient_instance.PrimaryDoctor.Doctor_ID,
#             'Complaint': patient_instance.Complaint,
#             'PatientType': patient_instance.PatientType,
#             'PatientCategory': patient_instance.PatientCategory,
#             'IsMLC': patient_instance.IsMLC,
#             'Flagging': Flagging_name,
#             'FlaggingColour': Flagging_color,
#             'CurrDate': patient_instance.PatientId.created_at.strftime('%d-%m-%y') if patient_instance.PatientId.created_at else "",
#             'CurrTime': patient_instance.PatientId.created_at.strftime('%I:%M %p') if patient_instance.PatientId.created_at else "",
#         }

#         # Log the final dictionary to ensure it's correct before returning the response
#         print(f"OPRegistration_dict: {OPRegistration_dict}")

#         return JsonResponse(OPRegistration_dict, safe=False)

#     except Exception as e:
#         # Log the error for debugging purposes
#         print(f"Error in get_workbenchquelist_doctor: {str(e)}")
#         return JsonResponse({'error': str(e)}, status=500)