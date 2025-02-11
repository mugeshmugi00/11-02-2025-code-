

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import *
import json
from django.forms.models import model_to_dict



@csrf_exempt
@require_http_methods(["POST", "GET", "OPTIONS"])
def insert_Emg_To_IP_convertion(request):
    if request.method == "POST":
        try:
            # Load the request body as JSON
            data = json.loads(request.body)
            
            print(data,'dataaaaaaaaaaaaaa')
            if isinstance(data, dict):

                patient_id_str = data.get('Patient_id')
                registration_id = data.get('Registration_id')
                reason = data.get('Reason')
                IpNotes = data.get('IpNotes')
                DischargePerson = data.get('DischargePerson')
                created_by = data.get('Created_by')
                Employeeid = data.get('Employeeid')

                # Retrieve the Patient_Detials instance
                try:
                    patient_instance = Patient_Detials.objects.get(pk=patient_id_str)
                except Patient_Detials.DoesNotExist:
                    return JsonResponse({'error': 'Patient ID not found'})

                # Check if the patient has already been admitted
               
                # Retrieve the Patient_Emergency_Registration_Detials instance
            
                registration_instance = Patient_Emergency_Registration_Detials.objects.get(Registration_Id=registration_id) if registration_id else None
                Employee_instance = Employee_Personal_Form_Detials.objects.get(Employee_ID=Employeeid) if Employeeid else None
                
                if registration_instance:  # Ensure instance is not None before updating
                    # Update the Status field before insertion
                    alertdata = Emg_to_IP_Convertion_Table.objects.filter(EmgRegistration_id=registration_instance)

                    if alertdata.exists():
                        return JsonResponse({'warn': 'Patient already admitted'})

                    
                    
                    registration_instance.Status = 'Completed'
                    registration_instance.save()


                # Save the data in the Emg_to_IP_Convertion_Table if the patient is not already admitted
                convertion_data = Emg_to_IP_Convertion_Table(
                    Patient_Id=patient_instance,  # Use the instance instead of the ID
                    EmgRegistration_id=registration_instance,  # Use the instance instead of the ID
                    Reason=reason,
                    IpNotes=IpNotes,
                    DischargePerson=DischargePerson,
                    Employeeid=Employee_instance,
                    created_by=created_by,  # Assuming Created_by is just a string or user ID
                    Status = 'Pending'
                )
                convertion_data.save()

                

                response_data = model_to_dict(convertion_data)
                return JsonResponse({'success': 'Emergency to IP Request Que added successfully','data':response_data})
            else:
                # If data is not a dictionary, it's an error in the request format
                return JsonResponse({'error': 'Invalid data format'})
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'})

        
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
        
    elif request.method == 'GET':
        try:
            requestdata = Emg_to_IP_Convertion_Table.objects.filter(Status='Pending')
            Requestlist = []

            for data in requestdata:
                patient_details = data.EmgRegistration_id.PatientId  # Assuming this is a ForeignKey to Patient_Detials
                request = {
                    'id' : data.id,
                    'PatientId': patient_details.pk,  # Use the primary key of the patient
                    'Registration_id': data.EmgRegistration_id.pk,  # Use the primary key of the registration
                    'Reason': data.Reason,
                    'IpNotes': data.IpNotes,
                    'Patient_Name': f'{patient_details.Title.Title_Name if patient_details.Title else ''}.{patient_details.FirstName if patient_details else ''} {patient_details.MiddleName if patient_details else ''} {patient_details.SurName if patient_details else ''}',
                    'ABHA': patient_details.ABHA,
                    'Age': patient_details.Age,
                    'DOB': patient_details.DOB,
                    'TitleId': patient_details.Title.Title_Id if patient_details.Title else '',
                    'FirstName': patient_details.FirstName,
                    'MiddleName': patient_details.MiddleName,
                    'LastName': patient_details.SurName,
                    'Gender': patient_details.Gender,
                    'PhoneNumber': patient_details.PhoneNo,
                    'Status' : data.Status,
                }
                Requestlist.append(request)

            return JsonResponse(Requestlist, safe=False)

        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)































