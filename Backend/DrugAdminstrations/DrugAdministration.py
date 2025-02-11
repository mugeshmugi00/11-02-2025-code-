from django.http import JsonResponse,HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import *
from Masters.models import *
from Inventory.models import *
from django.db.models import Q
from django.core.files.base import ContentFile
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta, time
import pytz
from django.db import transaction
from .scheduler import job_function
from Workbench.models import *

import json
from collections import defaultdict



@csrf_exempt
@require_http_methods(['POST'])
def doctor_drug_prescription_link(request):
    try:
        # Parse JSON data from request body
        prescriptions = json.loads(request.body)
        posstttttt = []  # To store responses for each prescription

        # Iterate over each prescription entry from the frontend
        for data in prescriptions:
            try:
                # Extract fields from each data entry
                booking_id = data.get('Booking_Id')
                Department = data.get('Department')
                DoctorName = data.get('DoctorName')
                GenericName = data.get('GenericName')
                MedicineCode = data.get('MedicineCode')
                MedicineName = data.get('MedicineName')
                Dosage = data.get('Dosage')
                Route = data.get('Route')
                FrequencyMethod = data.get('FrequencyMethod')
                FrequencyName = data.get('FrequencyName')
                FrequencyType = data.get('FrequencyType')
                Frequency = data.get('Frequency')
                FrequencyTime = data.get('FrequencyTime')
                Duration = data.get('Duration')
                DurationType = data.get('DurationType')
                Quantity = data.get('Quantity')
                AdminisDose = data.get('AdminisDose')
                Date = data.get('Date')
                Time = data.get('Time')
                Instruction = data.get('Instruction')
                Prescribedby = data.get('Prescribedby')
                Location = data.get('Location')
                CapturedBy = data.get('CapturedBy')
                Status = 'Pending'
                RequestType = 'Pending'
                Specialization = data.get('Specialization')
                batch_no = data.get('BatchNo')

                # Retrieve related instances for foreign key fields
                booking_instance = Patient_IP_Registration_Detials.objects.get(Registration_Id=booking_id)
                product_instance = Stock_Maintance_Table_Detials.objects.get(Product_Detials__pk=MedicineCode, Batch_No = batch_no)
                frequency_instance = Frequency_Master_Drug.objects.get(FrequencyId=FrequencyName)
                speciality_instance = Speciality_Detials.objects.get(Speciality_Id=Specialization)
                doctor_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=DoctorName)
                location_instance = Location_Detials.objects.get(Location_Id=Location)

                # Create and save a new prescription instance
                prescription_instance = Doctor_drug_prescription(
                    Booking_Id=booking_instance,
                    Department=Department,
                    DoctorName=doctor_instance,
                    ProductCode=product_instance,
                    Route=Route,
                    FrequencyMethod=FrequencyMethod,
                    Frequency=frequency_instance,
                    Duration=Duration,
                    DurationType=DurationType,
                    Quantity=Quantity,
                    AdminisDose=AdminisDose,
                    Date=Date,
                    Time=Time,
                    Instruction=Instruction,
                    Status=Status,
                    CapturedBy=CapturedBy,
                    Specialization=speciality_instance,
                    IssuedBy=Prescribedby,
                    Location=location_instance,
                )
                prescription_instance.save()
                
                # Add success response
                posstttttt.append({
                    'success': True,
                    'message': f'Prescription for {MedicineName} added successfully',
                    'medicine_name': MedicineName
                })

            except Exception as e:
                # Add error response
                posstttttt.append({
                    'success': False,
                    'message': f'Failed to add prescription for {MedicineName}',
                    'error': str(e),
                    'medicine_name': MedicineName
                })

        # Return the list of JSON responses
        return JsonResponse({'responses': posstttttt}, safe=False)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500) 
    

# @csrf_exempt
# @require_http_methods(["POST"])
# def doctor_drug_prescription_link(request):
#     if request.method == "POST":
#         try:
#             prescriptions = json.loads(request.body)
#             posstttttt = []
            
            
#             for data in prescriptions:
                
#                 booking_id = data.get('Booking_Id')
#                 Department = data.get('Department')
#                 DoctorName = data.get('DoctorName')
#                 GenericName = data.get('GenericName')
#                 MedicineCode = data.get('MedicineCode')
#                 MedicineName = data.get('MedicineName')
#                 Dosage = data.get('Dosage')
#                 Route = data.get('Route')
#                 FrequencyMethod = data.get('FrequencyMethod')
#                 FrequencyName = data.get('FrequencyName')
#                 FrequencyType = data.get('FrequencyType')
#                 Frequency = data.get('Frequency')
#                 FrequencyTime = data.get('FrequencyTime')
#                 Duration = data.get('Duration')
#                 DurationType = data.get('DurationType')
#                 Quantity = data.get('Quantity')
#                 AdminisDose = data.get('AdminisDose')
#                 Date = data.get('Date')
#                 Time = data.get('Time')
#                 Instruction = data.get('Instruction')
#                 Prescribedby = data.get('Prescribedby')
#                 Location = data.get('Location')
#                 CapturedBy = data.get('CapturedBy')
#                 Status = 'Pending'
#                 RequestType = 'Pending'
#                 Specialization = data.get('Specialization')
#                 batch_no = data.get('BatchNo')

#                 # Retrieve related instances for foreign key fields
#                 booking_instance = Patient_IP_Registration_Detials.objects.get(Registration_Id=booking_id)
#                 product_instance = Stock_Maintance_Table_Detials.objects.get(Product_Detials__pk=MedicineCode, Batch_No = batch_no)
#                 frequency_instance = Frequency_Master_Drug.objects.get(FrequencyId=FrequencyName)
#                 speciality_instance = Speciality_Detials.objects.get(Speciality_Id=Specialization)
#                 doctor_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=DoctorName)
#                 location_instance = Location_Detials.objects.get(Location_Id=Location)

#                 print('11111111',booking_instance)
#                 print('2222222',product_instance)
#                 print('3333333',frequency_instance)
#                 print('4444444444',speciality_instance)
#                 print('55555555',doctor_instance)
#                 print('666666666666',location_instance)
#                 # Create and save a new prescription instance
#                 prescription_instance = Doctor_drug_prescription(
#                     Booking_Id=booking_instance,
#                     Department=Department,
#                     DoctorName=doctor_instance,
#                     ProductCode=product_instance,
#                     Route=Route,
#                     FrequencyMethod=FrequencyMethod,
#                     Frequency=frequency_instance,
#                     Duration=Duration,
#                     DurationType=DurationType,
#                     Quantity=Quantity,
#                     AdminisDose=AdminisDose,
#                     Date=Date,
#                     Time=Time,
#                     Instruction=Instruction,
#                     Status=Status,
#                     CapturedBy=CapturedBy,
#                     Specialization=speciality_instance,
#                     IssuedBy=Prescribedby,
#                     Location=location_instance,
#                 )
#                 prescription_instance.save()
                
#                 posstttttt.append({
#                     'success': True,
#                     'message': f'Prescription for {MedicineName} added successfully',
#                     'medicine_name': MedicineName
#                 })
                
        
#         except Exception as e:
#             print(f'An error occurred:{str(e)}')
#             return JsonResponse({'error': str(e)}, status=500) 
    

    
    
@csrf_exempt
@require_http_methods(['GET'])
def Nurse_drug_prescription_link(request):
    if request.method == 'GET':
        try:
            booking_id = request.GET.get('Registration_Id')
            
            presc_instance = Doctor_drug_prescription.objects.filter(Booking_Id=booking_id, RequestType='')
            nurse_pres = Nurse_drug_prescription.objects.filter(Booking_Id=booking_id, RequestType='')
            
            presc_data_list = []
            id_counter = 1  # Initialize counter starting from 1
            
            # Add Doctor's prescription data with incremented id
            for pres in presc_instance:
                presc_dat = {
                    'id': id_counter,
                    'Billing_Id': pres.Booking_Id.Registration_Id,
                    'Prescription_Id': pres.Prescription_Id,
                    'Department': pres.Department,
                    'Specialization': pres.Specialization.Speciality_Name if pres.Specialization else None,
                    'DoctorName': pres.DoctorName.ShortName if pres.DoctorName else None,
                    'ProductCode': pres.ProductCode.Product_Detials.ItemName,
                    'GenericName': pres.ProductCode.Product_Detials.GenericName.GenericName,
                    'MedicineCode': pres.ProductCode.Product_Detials.pk,
                    'Dosage': pres.ProductCode.Product_Detials.Strength,
                    'DrugType': pres.ProductCode.Product_Detials.ProductType.ProductType_Name,
                    'Route': pres.Route,
                    'FrequencyMethod': pres.FrequencyMethod,
                    'Frequency': pres.Frequency.FrequencyName,
                    'FrequencyType': pres.Frequency.FrequencyType,
                    'FrequencyTime': pres.Frequency.FrequencyTime,
                    'Duration': pres.Duration,
                    'DurationType': pres.DurationType,
                    'Quantity': pres.Quantity,
                    'AdminisDose': pres.AdminisDose,
                    'Date': pres.Date,
                    'Time': pres.Time,
                    'Instruction': pres.Instruction,
                    'Status': pres.Status,
                    'CapturedBy': pres.CapturedBy,
                    'MedicalCat' : pres.ProductCode.Product_Detials.ProductCategory.ProductCategory_Name,
                }
                presc_data_list.append(presc_dat)
                id_counter += 1  # Increment counter for next entry

            # Add Nurse's prescription data with incremented id
            for nurse in nurse_pres:
                presc_data = {
                    'id': id_counter,
                    'Billing_Id': nurse.Booking_Id.Registration_Id,
                    'Prescription_Id': nurse.Prescription_Id,
                    'ProductCode': nurse.ProductCode.Product_Detials.ItemName,
                    'GenericName': nurse.ProductCode.Product_Detials.GenericName.GenericName,
                    'MedicineCode': nurse.ProductCode.Product_Detials.pk,
                    'Dosage': nurse.ProductCode.Product_Detials.Strength,
                    'DrugType': nurse.ProductCode.Product_Detials.ProductType.ProductType_Name,
                    'Route': nurse.Route,
                    'FrequencyMethod': nurse.FrequencyMethod if nurse.FrequencyMethod else None,
                    'Frequency': nurse.Frequency.FrequencyName if nurse.Frequency else None,
                    'FrequencyType': nurse.Frequency.FrequencyType if nurse.Frequency else None,
                    'FrequencyTime': nurse.Frequency.FrequencyTime if nurse.Frequency else None,
                    'Duration': nurse.Duration,
                    'DurationType': nurse.DurationType,
                    'Quantity': nurse.Quantity,
                    'AdminisDose': nurse.AdminisDose,
                    'Date': nurse.Date,
                    'Time': nurse.Time,
                    'Instruction': nurse.Instruction,
                    'Status': nurse.Status,
                    'CapturedBy': nurse.CapturedBy,
                    'MedicalCat' : nurse.ProductCode.Product_Detials.ProductCategory.ProductCategory_Name,
                }
                presc_data_list.append(presc_data)
                id_counter += 1  # Increment counter for next entry

            return JsonResponse(presc_data_list, safe=False)
        
        except Exception as e:
            return JsonResponse({'error': str(e)})
@csrf_exempt
@require_http_methods(['GET'])
def Nurse_drug_prescription_Completed(request):
    if request.method == 'GET':
        try:
            booking_id = request.GET.get('Registration_Id')
            
            presc_instance = ip_drug_request_table.objects.filter(Booking_Id=booking_id, Status='Pending')
            # nurse_pres = Nurse_drug_prescription.objects.filter(Booking_Id=booking_id, Status='Pending')
            
            presc_data_list = []
            id_counter = 1  # Initialize counter starting from 1
            
            # Add Doctor's prescription data with incremented id
            for pres in presc_instance:
                presc_dat = {
                    'id': id_counter,
                    'Billing_Id': pres.Booking_Id.Registration_Id,
                    'Prescription_Id': pres.Prescription_Id.Prescription_Id,
                    'Department': pres.Department,
                    'DoctorName': pres.DoctorName.ShortName if pres.DoctorName else None,
                    'ProductCode': pres.ProductCode.Product_Detials.ItemName,
                    'GenericName': pres.ProductCode.Product_Detials.GenericName.GenericName,
                    'MedicineCode': pres.ProductCode.Product_Detials.pk,
                    'Dosage': pres.ProductCode.Product_Detials.Strength,
                    'DrugType': pres.ProductCode.Product_Detials.ProductType.ProductType_Name,
                    'Route': pres.Route,
                    'FrequencyMethod': pres.FrequencyMethod,
                    'Frequency': pres.Frequency.FrequencyName,
                    'FrequencyType': pres.Frequency.FrequencyType,
                    'FrequencyTime': pres.Frequency.FrequencyTime,
                    'Duration': pres.Duration,
                    'DurationType': pres.DurationType,
                    'Quantity': pres.Quantity,
                    'RecievedQuantity': pres.RequestQuantity,
                    'AdminisDose': pres.AdminisDose,
                    'Date': pres.Date,
                    'Time': pres.Time,
                    'Instruction': pres.Instruction,
                    'Status': pres.Status,
                    'CapturedBy': pres.CapturedBy,
                    'MedicalCat' : pres.ProductCode.Product_Detials.ProductCategory.ProductCategory_Name,
                }
                presc_data_list.append(presc_dat)
                id_counter += 1  # Increment counter for next entry

            return JsonResponse(presc_data_list, safe=False)
        
        except Exception as e:
            return JsonResponse({'error': str(e)})

@csrf_exempt
@require_http_methods(['POST'])
def Nurse_drug_prescription_Recieved(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            booking_id = data.get('Billing_Id','')
            prescription_id = data.get('Prescription_Id','')
            print('111111111',data)
            
            presc_instance = ip_drug_request_table.objects.get(Booking_Id=booking_id, Status='Pending',Prescription_Id = prescription_id)
            print('111111',presc_instance)
            if presc_instance: 
                presc_instance.Status = 'Recieved'
                presc_instance.save()
                job_function()
            else:
                return JsonResponse({'error': 'Select Valid Drug to Approve '})
                
            return JsonResponse({'success' : 'Drug Details Approved Successfully'})
        
        except Exception as e:
            return JsonResponse({'error': str(e)})




@csrf_exempt
@require_http_methods(['GET'])
def Pharmacy_drug_quelist_link(request):
    try:
        booking_id = request.GET.get('Registration_Id')
        
        if not booking_id:
            return JsonResponse({'error': 'Registration_Id parameter is required'}, status=400)
        
        # Query without distinct
        presc_data = Doctor_drug_prescription.objects.filter(
            Booking_Id=booking_id, Status='Pending'
        ).values(
            'Booking_Id__Registration_Id',
            'Prescription_Id',
            'Department',
            'Specialization__Speciality_Name',
            'DoctorName__ShortName',
            'ProductCode__Product_Detials__ItemName',
            'ProductCode__Product_Detials__GenericName__GenericName',
            'ProductCode__Product_Detials__pk',
            'ProductCode__Product_Detials__Strength',
            'ProductCode__Product_Detials__ProductType__ProductType_Name',
            'Route',
            'FrequencyMethod',
            'Frequency__FrequencyName',
            'Frequency__FrequencyType',
            'Frequency__FrequencyTime',
            'Duration',
            'DurationType',
            'Quantity',
            'AdminisDose',
            'created_at',
            'Instruction',
            'Status',
            'CapturedBy'
        )

        # Filter for distinct created_at in Python
        distinct_data = []
        seen_dates = set()
        for item in presc_data:
            if item['created_at'] not in seen_dates:
                distinct_data.append(item)
                seen_dates.add(item['created_at'])

        # Format data for response
        presc_data_list = [
            {
                'Billing_Id': item['Booking_Id__Registration_Id'],
                'Prescription_Id': item['Prescription_Id'],
                'Department': item['Department'],
                'Specialization': item['Specialization__Speciality_Name'],
                'DoctorName': item['DoctorName__ShortName'],
                'ProductCode': item['ProductCode__Product_Detials__ItemName'],
                'GenericName': item['ProductCode__Product_Detials__GenericName__GenericName'],
                'MedicineCode': item['ProductCode__Product_Detials__pk'],
                'Dosage': item['ProductCode__Product_Detials__Strength'],
                'DrugType': item['ProductCode__Product_Detials__ProductType__ProductType_Name'],
                'Route': item['Route'],
                'FrequencyMethod': item['FrequencyMethod'],
                'Frequency': item['Frequency__FrequencyName'],
                'FrequencyType': item['Frequency__FrequencyType'],
                'FrequencyTime': item['Frequency__FrequencyTime'],
                'Duration': item['Duration'],
                'DurationType': item['DurationType'],
                'Quantity': item['Quantity'],
                'AdminisDose': item['AdminisDose'],
                'Date': item['created_at'].date(),  # format created_at as Date and Time
                'Time': item['created_at'].time(),
                'Instruction': item['Instruction'],
                'Status': item['Status'],
                'CapturedBy': item['CapturedBy'],
            }
            for item in distinct_data
        ]
        
        return JsonResponse(presc_data_list, safe=False)
    
    except Doctor_drug_prescription.DoesNotExist:
        return JsonResponse({'error': 'No pending prescriptions found for this booking ID'}, status=404)
    
    except Exception as e:
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)

# @csrf_exempt
# @require_http_methods(['GET'])
# def Nurse_drug_prescription_link(request):
#     try:
#         booking_id = request.GET.get('Registration_Id')
        
#         if not booking_id:
#             return JsonResponse({'error': 'Registration_Id parameter is required'}, status=400)
        
#         # Filter prescriptions by booking_id and status, retrieving distinct date and time fields
#         presc_data = Doctor_drug_prescription.objects.filter(
#             Booking_Id=booking_id, Status='Pending'
#         ).values(
#             'Booking_Id__Registration_Id',
#             'Prescription_Id',
#             'Department',
#             'Specialization__Speciality_Name',
#             'DoctorName__ShortName',
#             'ProductCode__ItemName',
#             'ProductCode__GenericName__GenericName',
#             'ProductCode__pk',
#             'ProductCode__Strength',
#             'ProductCode__ProductType__ProductType_Name',
#             'Route',
#             'FrequencyMethod',
#             'Frequency__FrequencyName',
#             'Frequency__FrequencyType',
#             'Frequency__FrequencyTime',
#             'Duration',
#             'DurationType',
#             'Quantity',
#             'AdminisDose',
#             'created_at',
#             'Instruction',
#             'Status',
#             'CapturedBy'
#         ).distinct('created_at')  # Ensuring distinct Date and Time entries

#         # Format data for response
#         presc_data_list = [
#             {
#                 'Billing_Id': item['Booking_Id__Registration_Id'],
#                 'Prescription_Id': item['Prescription_Id'],
#                 'Department': item['Department'],
#                 'Specialization': item['Specialization__Speciality_Name'],
#                 'DoctorName': item['DoctorName__ShortName'],
#                 'ProductCode': item['ProductCode__ItemName'],
#                 'GenericName': item['ProductCode__GenericName__GenericName'],
#                 'MedicineCode': item['ProductCode__pk'],
#                 'Dosage': item['ProductCode__Strength'],
#                 'DrugType': item['ProductCode__ProductType__ProductType_Name'],
#                 'Route': item['Route'],
#                 'FrequencyMethod': item['FrequencyMethod'],
#                 'Frequency': item['Frequency__FrequencyName'],
#                 'FrequencyType': item['Frequency__FrequencyType'],
#                 'FrequencyTime': item['Frequency__FrequencyTime'],
#                 'Duration': item['Duration'],
#                 'DurationType': item['DurationType'],
#                 'Quantity': item['Quantity'],
#                 'AdminisDose': item['AdminisDose'],
#                 'Date': item['Date'],
#                 'Time': item['Time'],
#                 'Instruction': item['Instruction'],
#                 'Status': item['Status'],
#                 'CapturedBy': item['CapturedBy'],
#             }
#             for item in presc_data
#         ]
        
#         return JsonResponse(presc_data_list, safe=False)
    
#     except Doctor_drug_prescription.DoesNotExist:
#         return JsonResponse({'error': 'No pending prescriptions found for this booking ID'}, status=404)
    
#     except Exception as e:
#         return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)



@csrf_exempt
@require_http_methods(['POST'])
def Nurse_drug_prescription_Add_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            Booking_Id = data.get('Booking_Id', '')
            Prescription_Id = data.get('Prescription_Id', '')
            OrderType = data.get('OrderType', '')
            Quantity = data.get('Quantity', '')
            RequestType = data.get('RequestType', '')
            RequestQuantity = data.get('RequestQuantity', '')
            MedCat = data.get('MedicalCat','')
            print('Received data:', data)

            if Booking_Id and Prescription_Id and MedCat == 'MEDICAL':
                pres = Doctor_drug_prescription.objects.get(Booking_Id=Booking_Id, Prescription_Id=Prescription_Id)
                print('Prescription found:', pres)

                # Update fields
                pres.Quantity = Quantity
                pres.OrderType = OrderType
                pres.RequestType = RequestType
                pres.RequestQuantity = RequestQuantity
                # pres.Status = 'Requested'
                pres.save()
                job_function()
                
                return JsonResponse({'success': 'Drug details added successfully'})
            elif Booking_Id and Prescription_Id and not MedCat == 'MEDICAL':
                pres = Nurse_drug_prescription.objects.get(Booking_Id=Booking_Id, Prescription_Id=Prescription_Id)
                print('Prescription found:', pres)

                # Update fields
                pres.Quantity = Quantity
                pres.OrderType = OrderType
                pres.RequestType = RequestType
                pres.RequestQuantity = RequestQuantity
                # pres.Status = 'Requested'
                pres.save()
                
                return JsonResponse({'success': 'Drug details added successfully'})                
            else:
                # Return an error if Booking_Id or Prescription_Id are missing
                return JsonResponse({'error': 'Booking_Id and Prescription_Id are required'})

        except Doctor_drug_prescription.DoesNotExist:
            return JsonResponse({'error': 'Prescription not found'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
        
@csrf_exempt
@require_http_methods(['POST'])
def Nurse_drug_prescription_update_link(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from request body
            prescriptions = json.loads(request.body)
            responses = []  # To store responses for each prescription

            # Iterate over each prescription entry from the frontend
            for data in prescriptions:
                try:
                    # Extract fields from each data entry
                    booking_id = data.get('Billing_Id')
                    Medical_Category = data.get('Medical_Category')                    
                    GenericName = data.get('GenericName')
                    MedicineCode = data.get('MedicineCode')
                    Dosage = data.get('Dosage')
                    Route = data.get('Route')
                    FrequencyMethod = data.get('FrequencyMethod')
                    FrequencyName = data.get('FrequencyName')
                    FrequencyType = data.get('FrequencyType')
                    Frequency = data.get('Frequency')
                    FrequencyTime = data.get('FrequencyTime')
                    Duration = data.get('Duration')
                    DurationType = data.get('DurationType')
                    Quantity = data.get('Quantity')
                    AdminisDose = data.get('AdminisDose')
                    Instruction = data.get('Instruction')
                    Prescribedby = data.get('Prescribedby')
                    Location = data.get('Location')
                    CapturedBy = data.get('CapturedBy')
                    Status = 'Pending'
                    RequestType = 'Pending'

                    print('111111',data)
                    # Retrieve related instances for foreign key fields
                    booking_instance = Patient_IP_Registration_Detials.objects.get(Registration_Id=booking_id)
                    product_instance = Stock_Maintance_Table_Detials.objects.get(Product_Detials__pk=MedicineCode)
                    location_instance = Location_Detials.objects.get(Location_Id=Location)

                    if Medical_Category == 'MEDICAL':
                        frequency_instance = Frequency_Master_Drug.objects.get(FrequencyId=FrequencyName)
                        # Create and save a new prescription instance
                        prescription_instance = Doctor_drug_prescription(
                            Booking_Id=booking_instance,
                            ProductCode=product_instance,
                            Route=Route,
                            FrequencyMethod=FrequencyMethod,
                            Frequency=frequency_instance,
                            Duration=Duration,
                            DurationType=DurationType,
                            Quantity=Quantity,
                            AdminisDose=AdminisDose,
                            Instruction=Instruction,
                            Status=Status,
                            CapturedBy=CapturedBy,
                            IssuedBy=Prescribedby,
                            Location=location_instance,
                        )
                        prescription_instance.save()
                        responses.append({'success': f'Prescription added successfully'})
                    else:
                        # Create and save a new prescription instance
                        prescription_instance = Nurse_drug_prescription(
                            Booking_Id=booking_instance,
                            ProductCode=product_instance,
                            Route=Route,
                            # Duration=Duration,
                            # DurationType=DurationType,
                            Quantity=Quantity,
                            AdminisDose=AdminisDose,
                            Instruction=Instruction,
                            Status=Status,
                            CapturedBy=CapturedBy,
                            IssuedBy=Prescribedby,
                            Location=location_instance,
                        )
                        prescription_instance.save()
                        responses.append({'success': f'Prescription added successfully'})
                except Exception as e:
                    responses.append({'error': f'Failed to add prescription : {str(e)}'})

            # Return a response after processing all entries
            return JsonResponse(responses, safe=False)
    
        except Doctor_drug_prescription.DoesNotExist:
            return JsonResponse({'error': 'Prescription not found'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
        
        
@csrf_exempt
@require_http_methods(['GET'])
def get_for_ip_durgs_doctor_show(request):
    try:
        booking_id = request.GET.get('Booking_id')
        print('11111',booking_id)
        
        booking_instance = Doctor_drug_prescription.objects.filter(Booking_Id = booking_id)
        print('22222',booking_instance)
        # frequency_instance = Frequency_Master_Drug.objects.get()
        booking_instance_data = []
        for booking in booking_instance:
            book ={
                'Prescibtion_Id' : booking.Prescription_Id,
                'Booking_Id' : booking.Booking_Id.Registration_Id,
                'Department' : booking.Department,
                'DoctorName' : booking.DoctorName.ShortName,
                'GenericName' : booking.ProductCode.Product_Detials.GenericName.GenericName,
                'MedicineCode' : booking.ProductCode.Product_Detials.pk,
                'MedicineName' : booking.ProductCode.Product_Detials.ItemName,
                'Route' : booking.Route,
                'FrequencyIssued' : booking.Frequency.Frequency,
                'FrequencyMethod' : booking.FrequencyMethod,
                'PrescribedDate' : booking.Date,
                'IssuedDate' : booking.created_at,
                'AdminisDose' : booking.AdminisDose,
                'Location' : booking.Location.Location_Name,
            }
            print('3333333',book)
            booking_instance_data.append(book)
        return JsonResponse(booking_instance_data,safe=False)
    except Exception as e:
        return JsonResponse({'error':str(e)})
    
    
    
from django.core.exceptions import ObjectDoesNotExist


def inhouse_pharmacy_queue_list_prescrib(request):
    try:
        location = request.GET.get('location')
        drug_requests = (
            ip_drug_request_table.objects.filter(Location=location, Status='Pending')
            if location
            else ip_drug_request_table.objects.filter(Status='Pending')
        )

        datafetch = []
        processed_patients = set()
        record_id = 1

        for drug_request in drug_requests:
            registration_id = drug_request.Booking_Id
            print('regggg',registration_id)
            print('reggidddd',registration_id.Registration_Id)
            if not registration_id:
                continue

            try:
                room_detail = Patient_Admission_Room_Detials.objects.filter(
                    IP_Registration_Id_id=registration_id
                ).last()
                print('000000',room_detail)
                if not room_detail or not room_detail.RoomId:
                    continue

                room_status = Room_Master_Detials.objects.filter(
                    Room_Id=room_detail.RoomId.Room_Id, Booking_Status='Occupied'
                ).first()
                print('00110011',room_status)
                if not room_status:
                    continue
                patient_data = Patient_IP_Registration_Detials.objects.filter(
                    Registration_Id=registration_id.Registration_Id
                ).first()
                print('111111',patient_data)
                if not patient_data:
                    continue

                personal_data = Patient_Detials.objects.filter(
                    PatientId=patient_data.PatientId.PatientId
                ).first()
                print('2222222',personal_data.PatientId)
                if not personal_data or personal_data.PatientId in processed_patients:
                    continue

                processed_patients.add(personal_data.PatientId)

                patient_name = " ".join(
                    filter(None, [personal_data.FirstName, personal_data.MiddleName, personal_data.SurName])
                )
                print('333333333')

                datafetch.append({
                    'id': record_id,
                    'Booking_Id': registration_id.Registration_Id,
                    'PatientName': patient_name or "Unknown Patient",
                    'RoomId': room_status.Room_Id,
                    'RoomNo': room_status.Room_No,
                    'PatientId': personal_data.PatientId,
                    'PatientPhoneNo': personal_data.PhoneNo,
                    'DoctorName': str(getattr(drug_request.DoctorName, 'ShortName', "Unknown Doctor"))
                })

                record_id += 1

            except Exception as e:
                print(f"Error processing registration_id {registration_id}: {str(e)}")
                continue

        return JsonResponse(datafetch, safe=False)

    except Exception as e:
        return JsonResponse({"Error": str(e)}, status=500)
    
    
def get_prescription_forIP(request):
    try:
        # Retrieve PatientID from request
        PatientID = request.GET.get('PatientID')
        VisitID = request.GET.get('VisitID')
        
        print('12212211',PatientID,VisitID)

        # Check if PatientID and VisitID are provided
        if not PatientID:
            return JsonResponse({"error": "PatientID parameter is required"}, status=400)
        if not VisitID:
            return JsonResponse({"error": "VisitID parameter is required"}, status=400)

        # Fetch patient details to get the Patient Name
        patient = Patient_Detials.objects.get(PatientId=PatientID)
        PatientName = f"{patient.FirstName} {patient.MiddleName} {patient.SurName}"
        print('33322223333',PatientName)
        # Query the prescriptions related to the VisitID (Registration_Id_id)
        prescriptions = ip_drug_request_table.objects.filter(Booking_Id=VisitID , Status = 'Pending')
        print('0000000',prescriptions)
        nurse_pres = Nurse_drug_prescription.objects.filter(Booking_Id=VisitID , Status = 'Pending')
        print('111111',nurse_pres)
        # Prepare the list of prescriptions in the specified format
        prescription_list = []
        for prescription in prescriptions:
            prescription_dict = {
                'PrescriptionID': prescription.Prescription_Id.Prescription_Id,
                'PatientID': PatientID,
                'VisitID': VisitID,  # Mapping VisitID as Registration_Id
                'Booking_Id': prescription.Booking_Id.Registration_Id,
                # 'AppointmentDate': prescription.CreatedAt.date().isoformat(),  # Date of prescription creation
                'DoctorId': prescription.DoctorName.Doctor_ID if prescription.DoctorName else None,
                'DoctorName': prescription.DoctorName.ShortName if prescription.DoctorName else None,
                'GenericName': prescription.ProductCode.Product_Detials.GenericName.GenericName,
                'ItemId': prescription.ProductCode.Product_Detials.pk,
                'ItemName': prescription.ProductCode.Product_Detials.ItemName,
                'Dose': prescription.ProductCode.Product_Detials.Strength,
                'Route': prescription.Route,
                'Frequency': prescription.Frequency.Frequency,  # Assuming Frequency is in Duration
                'FrequencyMethod': prescription.Frequency.FrequencyType,  # Assuming Frequency is in Duration
                'Duration': f'{prescription.Duration} {prescription.DurationType}',
                'Qty': prescription.RequestQuantity,
                'Instruction': prescription.RequestType,  # Assuming RequestType includes instructions
                'Status': prescription.Status,
                'LoggedBy': prescription.CapturedBy,
                # 'CreatedAt': prescription.CreatedAt.date().isoformat(),
                'Patient_Name': PatientName,
                'MRP' : int(prescription.ProductCode.Sellable_price),
                'BatchNo' : prescription.ProductCode.Batch_No,
                'Exp_Date' : prescription.ProductCode.Expiry_Date,
            }
            prescription_list.append(prescription_dict)
            
        for prescription in nurse_pres:
            prescription_dict = {
                'PrescriptionID': prescription.Prescription_Id,
                'PatientID': PatientID,
                'VisitID': VisitID,  # Mapping VisitID as Registration_Id
                'Booking_Id': prescription.Booking_Id.Registration_Id,
                # 'AppointmentDate': prescription.CreatedAt.date().isoformat(),  # Date of prescription creation
                # 'DoctorName': prescription.DoctorName.ShortName if prescription.DoctorName else None,
                'GenericName': prescription.ProductCode.Product_Detials.GenericName.GenericName,
                'ItemId': prescription.ProductCode.Product_Detials.pk,
                'ItemName': prescription.ProductCode.Product_Detials.ItemName,
                'Dose': prescription.ProductCode.Product_Detials.Strength,
                'Route': prescription.Route,
                'Frequency': prescription.Duration,  # Assuming Frequency is in Duration
                'Duration': prescription.DurationType,
                'Qty': prescription.RequestQuantity,
                'Instruction': prescription.RequestType,  # Assuming RequestType includes instructions
                'Status': prescription.Status,
                'LoggedBy': prescription.CapturedBy,
                # 'CreatedAt': prescription.CreatedAt.date().isoformat(),
                'Patient_Name': PatientName,
                'MRP' : int(prescription.ProductCode.Sellable_price),
                'BatchNo' : prescription.ProductCode.Batch_No,
                'Exp_Date' : prescription.ProductCode.Expiry_Date,
            }
            prescription_list.append(prescription_dict)

        return JsonResponse(prescription_list, safe=False)

    except Patient_Detials.DoesNotExist:
        return JsonResponse({"error": "Patient not found"})
    except Exception as e:
        print('error:', str(e))
        return JsonResponse({"error": "Internal Server Error: " + str(e)})

def get_last_prescription_forIP(request):
    try:
        # Retrieve PatientID from request
        VisitID = request.GET.get('VisitID')

        # Check if VisitID is provided
        if not VisitID:
            return JsonResponse({"error": "VisitID parameter is required"}, status=400)

        # Query the prescriptions related to the VisitID (Registration_Id_id)
        prescriptions = Doctor_drug_prescription.objects.filter(Booking_Id=VisitID, Status='Pending')

        print('11111111', prescriptions)
        # Prepare the list of prescriptions in the specified format
        prescription_list = []
        id = 1  # Initialize id as an integer, not a tuple
        for prescription in prescriptions:
            prescription_dict = {
                'id': id,
                'PrescriptionID': prescription.Prescription_Id,
                'Booking_Id': prescription.Booking_Id.Registration_Id,
                'Department' : prescription.Department,
                'Specialization': prescription.Specialization.Speciality_Id,
                'DoctorName': prescription.DoctorName.ShortName if prescription.DoctorName else None,
                'GenericName': prescription.ProductCode.Product_Detials.GenericName.GenericName,
                'MedicineCode': prescription.ProductCode.Product_Detials.pk,
                'MedicineName': prescription.ProductCode.Product_Detials.ItemName,
                'Dosage': prescription.ProductCode.Product_Detials.Strength,
                'Route': prescription.Route,
                'FrequencyMethod': prescription.FrequencyMethod,  # Assuming Frequency is in Duration
                'FrequencyName': prescription.Frequency.FrequencyName,  # Assuming Frequency is in Duration
                'FrequencyType': prescription.Frequency.FrequencyType,  # Assuming Frequency is in Duration
                'Frequency': prescription.Frequency.Frequency,  # Assuming Frequency is in Duration
                'FrequencyTime': prescription.Frequency.FrequencyTime,  # Assuming Frequency is in Duration
                'DurationType': prescription.DurationType,
                'AdminisDose' : prescription.AdminisDose,
                'Quantity': prescription.RequestQuantity,
                'Instruction': prescription.Instruction,  # Assuming RequestType includes instructions
                'Status': prescription.Status,
                'LoggedBy': prescription.CapturedBy,
                'MRP': int(prescription.ProductCode.Sellable_price),
                'BatchNo': prescription.ProductCode.Batch_No,
                'Exp_Date': prescription.ProductCode.Expiry_Date,
            }
            prescription_list.append(prescription_dict)
            id += 1  # Increment id by 1

        return JsonResponse(prescription_list, safe=False)

    except Exception as e:
        print('error:', str(e))
        return JsonResponse({"error": "Internal Server Error: " + str(e)})



@csrf_exempt
@require_http_methods(['POST'])
def IP_Pharmacy_Billing_link(request):
    if request.method == 'POST':
        try:
            # Extract main billing data
            selected_patient_data = json.loads(request.POST.get('SelectedPatient_list'))
            billing_date = request.POST.get('Billing_date')
            billpay_method = json.loads(request.POST.get('Billpay_method'))
            bill_Items = json.loads(request.POST.get('Bill_Items'))
            user_name = request.POST.get('User_Name')
            location_id = request.POST.get('location')
            
            # Extract PDF data
            pdf_data = request.FILES.get('pdfData')
            
            # Debug output to ensure data is received correctly
            print('Selected Patient Data:', selected_patient_data)
            print('Billing Date:', billing_date)
            print('Billing Method:', billpay_method)
            print('Bill_Items:', bill_Items)
            print('PDF Data:', pdf_data)

            # Fetch related foreign key objects
            try:
                doctor = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=selected_patient_data.get('Doctor_Id'))
                print('Doctor:', doctor)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Doctor not found'})

            try:
                patient = Patient_Detials.objects.get(PatientId=selected_patient_data.get('PatientId'))
                print('Patient:', patient)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Patient not found'})

            try:
                location = Location_Detials.objects.get(Location_Id=location_id)
                print('Location:', location)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Location not found'})
            print('111111111111')
            # Parse billing item details with safe integer and float conversion
            try:
                discount_amount = float(bill_Items.get('Discount', 0))
                sgst_val = float(bill_Items.get('SGSTval', 0))
                cgst_val = float(bill_Items.get('CGSTval', 0))
                gst_amount = float(bill_Items.get('GSTAmount', 0))
                
                total_items = int(bill_Items.get('totalItems', 0))
                total_qty = int(bill_Items.get('totalQty', 0))
                total_amount = float(bill_Items.get('Amount', 0))
                net_amount = float(bill_Items.get('totalAmount', 0))
                paid_amount = float(bill_Items.get('PaidAmount', 0))
                balance_amount = float(bill_Items.get('BalanceAmount', 0))
                round_off = float(bill_Items.get('Roundoff', 0))
            except ValueError as ve:
                print(f"Invalid value in Bill_Items: {ve}")
                return JsonResponse({'error': 'Invalid value in Bill_Items'})

            print('22222222222')
            # Create the main billing entry
            billing = IP_Pharmacy_Billing_Table_Detials.objects.create(
                Doctor_Id=doctor,
                Patient_Id=patient,
                Billing_Date=billing_date,
                Billing_Type="IPPharmacy",
                Discount_Amount=discount_amount,
                SGST_val=sgst_val,
                CGST_val=cgst_val,
                Total_GSTAmount=gst_amount,
                Total_Items=total_items,
                Total_Qty=total_qty,
                Total_Amount=total_amount,
                Net_Amount=net_amount,
                Paid_Amount=paid_amount,
                Balance_Amount=balance_amount,
                Round_Off=round_off,
                created_by=user_name,
                Location=location
            )
            billing.save()
            print('billingggg',billing)
            
            drug_status = Doctor_drug_prescription.objects.filter(Booking_Id__PatientId__PatientId = selected_patient_data.get('PatientId'), Status = 'Requested')
            print('12212112',drug_status)
            
            for drug in drug_status:
                drug.Status = 'Completed'
                
                drug.save()

            try:
                bill_itemtable = json.loads(request.POST.get('Billing_itemtable', '[]'))  # Parse JSON string to list
                
                if not isinstance(bill_itemtable, list):
                    return JsonResponse({'error': 'Invalid format for Billing_itemtable. Expected a list of items.'})
                
                for item in bill_itemtable:
                    if not isinstance(item, dict):
                        print(f"Invalid item format: {item}")
                        continue  # Skip invalid items
                    
                    print("Processing item:", item)  # Debugging statement
                    
                    items_bill = IP_BillingItem.objects.create(
                        Billing=billing,
                        ItemName=str(item.get('ItemName')),
                        Billing_Quantity=int(item.get('Billing_Quantity', 0)),
                        BatchNo=item.get('BatchNo'),
                        Exp_Date=datetime.strptime(item.get('Exp_Date'), "%Y-%m-%d").date(),
                        Unit_Price=float(item.get('Unit_Price', 0)),
                        Amount=float(item.get('Amount', 0)),
                        Total=float(item.get('Total', 0))
                    )
                    items_bill.save()
                    print('items_bill:', items_bill)  # Debugging statement
            except Exception as e:
                print(f"Error while processing item: {item}, Error: {e}")  # Capture any errors
                return JsonResponse({'error': f"Failed to process item: {item}. Error: {str(e)}"})
            
                    # Save each payment method
            for payment in billpay_method:
                payment_bill = IP_Pharmacy_Billing_Payments.objects.create(
                    Billing=billing,
                    Billpay_method=payment.get('Billpay_method', ''),
                    CardType=payment.get('CardType', ''),
                    BankName=payment.get('BankName', ''),
                    ChequeNo=payment.get('ChequeNo', ''),
                    paidamount=float(payment.get('paidamount', 0)),
                    Additionalamount=float(payment.get('Additionalamount', 0)) if payment.get('Additionalamount') else 0,
                    transactionFee=payment.get('transactionFee', '') if payment.get('transactionFee') else '',
                )
            payment_bill.save()
            # # Save the PDF to the database
            # if pdf_data:
            #     billing.pdf_data.save(f"{billing.Billing_Invoice_No}.pdf", ContentFile(pdf_data.read()))

            # Assuming the additional billing items need to be saved here if there’s a model for that
            # Uncomment and adapt the following if applicable
            # index = 0
            # while f'ItemId_{index}' in request.POST:
            #     item_id = request.POST.get(f'ItemId_{index}')
            #     quantity = int(request.POST.get(f'Billing_Quantity_{index}'))
            #     BillingItem.objects.create(
            #         billing=billing,
            #         ItemId=item_id,
            #         Billing_Quantity=quantity
            #     )
            #     index += 1

            return JsonResponse({'status': 'success', 'message': 'Data saved successfully','InvoiceNo': billing.Billing_Invoice_No})

        except Exception as e:
            print(f"Error occurred: {e}")
            return JsonResponse({'error': str(e)})  
        
        
@csrf_exempt
@require_http_methods(['POST'])
def OP_Pharmacy_Billing_link(request):
    if request.method == 'POST':
        try:
            # Extract main billing data
            selected_patient_data = json.loads(request.POST.get('SelectedPatient_list'))
            billing_date = request.POST.get('Billing_date')
            billpay_method = json.loads(request.POST.get('Billpay_method'))
            bill_Items = json.loads(request.POST.get('Bill_Items',{}))
            user_name = request.POST.get('User_Name')
            location_id = request.POST.get('location')
            # bill_itemtable = json.loads(request.POST.get('Billing_itemtable', '[]'))  # Parse JSON string to list            
            # Extract PDF data
            pdf_data = request.FILES.get('pdfData')
            
            # Debug output to ensure data is received correctly
            print('Selected Patient Data:', selected_patient_data)
            print('Billing Date:', billing_date)
            print('Billing Method:', billpay_method)
            print('Bill_Items:', bill_Items)
            print('PDF Data:', pdf_data)
            # print("Billing Item Table:", bill_itemtable)
            # Fetch related foreign key objects
            try:
                doctor_id = selected_patient_data.get('Doctor_Id','')
                doctor_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=doctor_id) if doctor_id else None                
                print('Doctor:', doctor_instance)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Doctor not found'})

            try:
                patient = Patient_Detials.objects.get(PatientId=selected_patient_data.get('PatientId')) if selected_patient_data.get('PatientId') else None
                print('Patient:', patient)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Patient not found'})

            try:
                location = Location_Detials.objects.get(Location_Id=location_id) if location_id else None
                print('Location:', location)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Location not found'})
            print('111111111111')
            # Parse billing item details with safe integer and float conversion
            try:
                discount_amount = float(bill_Items.get('Discount', 0))
                sgst_val = float(bill_Items.get('SGSTval', 0))
                cgst_val = float(bill_Items.get('CGSTval', 0))
                gst_amount = float(bill_Items.get('GSTAmount', 0))
                
                total_items = int(bill_Items.get('totalItems', 0))
                total_qty = int(bill_Items.get('totalQty', 0))
                total_amount = float(bill_Items.get('Amount', 0))
                net_amount = float(bill_Items.get('totalAmount', 0))
                paid_amount = float(bill_Items.get('PaidAmount', 0))
                balance_amount = float(bill_Items.get('BalanceAmount', 0))
                round_off = float(bill_Items.get('Roundoff', 0))
            except ValueError as ve:
                print(f"Invalid value in Bill_Items: {ve}")
                return JsonResponse({'error': 'Invalid value in Bill_Items'})

            print('22222222222')
            # Create the main billing entry
            billing = OP_Pharmacy_Billing_Table_Detials.objects.create(
                Doctor_Id=doctor_instance if doctor_id else None,
                Patient_Id=patient,
                Billing_Date=billing_date,
                Billing_Type="OPPharmacy",
                Discount_Amount=discount_amount,
                SGST_val=sgst_val,
                CGST_val=cgst_val,
                Total_GSTAmount=gst_amount,
                Total_Items=total_items,
                Total_Qty=total_qty,
                Total_Amount=total_amount,
                Net_Amount=net_amount,
                Paid_Amount=paid_amount,
                Balance_Amount=balance_amount,
                Round_Off=round_off,
                created_by=user_name,
                Location=location
            )
            billing.save()
            print('billingggg',billing)
            
            drug_status = OPD_Prescription_Details.objects.filter(Patient_Id__PatientId = selected_patient_data.get('PatientId'), Status = True) if selected_patient_data.get('PatientId') else None
            print('12212112',drug_status)
            
            for drug in drug_status:
                drug.Status = False
                
                drug.save()
            try:
                bill_itemtable = json.loads(request.POST.get('Billing_itemtable', '[]'))  # Parse JSON string to list
                
                if not isinstance(bill_itemtable, list):
                    return JsonResponse({'error': 'Invalid format for Billing_itemtable. Expected a list of items.'})
                
                for item in bill_itemtable:
                    if not isinstance(item, dict):
                        print(f"Invalid item format: {item}")
                        continue  # Skip invalid items
                    
                    print("Processing item:", item)  # Debugging statement
                    
                    items_bill = OP_BillingItem.objects.create(
                        Billing=billing,
                        ItemName=str(item.get('ItemName')),
                        Billing_Quantity=int(item.get('Billing_Quantity', 0)),
                        BatchNo=item.get('BatchNo'),
                        Exp_Date=datetime.strptime(item.get('Exp_Date'), "%Y-%m-%d").date(),
                        Unit_Price=float(item.get('Unit_Price', 0)),
                        Amount=float(item.get('Amount', 0)),
                        Total=float(item.get('Total', 0))
                    )
                    items_bill.save()
                    print('items_bill:', items_bill)  # Debugging statement
            except Exception as e:
                print(f"Error while processing item: {item}, Error: {e}")  # Capture any errors
                return JsonResponse({'error': f"Failed to process item: {item}. Error: {str(e)}"})
            
                    # Save each payment method
            for payment in billpay_method:
                payment_bill = OP_Pharmacy_Billing_Payments.objects.create(
                    Billing=billing,
                    Billpay_method=payment.get('Billpay_method', ''),
                    CardType=payment.get('CardType', ''),
                    BankName=payment.get('BankName', ''),
                    ChequeNo=payment.get('ChequeNo', ''),
                    paidamount=float(payment.get('paidamount', 0)),
                    Additionalamount=float(payment.get('Additionalamount', 0), ) if payment.get('Additionalamount') else 0,
                    transactionFee=payment.get('transactionFee', '') if payment.get('transactionFee') else 0,
                )
            payment_bill.save()
        
            # if pdf_data:
            #     billing.pdf_data.save(f"{billing.Billing_Invoice_No}.pdf", ContentFile(pdf_data.read()))

            # Assuming the additional billing items need to be saved here if there’s a model for that
            # Uncomment and adapt the following if applicable
            # index = 0
            # while f'ItemId_{index}' in request.POST:
            #     item_id = request.POST.get(f'ItemId_{index}')
            #     quantity = int(request.POST.get(f'Billing_Quantity_{index}'))
            #     BillingItem.objects.create(
            #         billing=billing,
            #         ItemId=item_id,
            #         Billing_Quantity=quantity
            #     )
            #     index += 1

            return JsonResponse({'status': 'success', 'message': 'OP Data saved successfully','InvoiceNo': billing.Billing_Invoice_No})

        except Exception as e:
            print(f"Error occurred: {e}")
            return JsonResponse({'error': str(e)})  
        
        
@csrf_exempt
@require_http_methods(['POST'])
def OP_Pharmacy_Walkin_Billing_link(request):
    if request.method == 'POST':
        try:
            # Extract main billing data
            selected_patient_data = json.loads(request.POST.get('SelectedPatient_list'))
            billing_date = request.POST.get('Billing_date')
            billpay_method = json.loads(request.POST.get('Billpay_method'))
            bill_Items = json.loads(request.POST.get('Bill_Items',{}))
            user_name = request.POST.get('User_Name')
            location_id = request.POST.get('location')
            # bill_itemtable = json.loads(request.POST.get('Billing_itemtable', '[]'))  # Parse JSON string to list            
            # Extract PDF data
            pdf_data = request.FILES.get('pdfData')
            
            # Debug output to ensure data is received correctly
            print('Selected Patient Data:', selected_patient_data)
            print('Billing Date:', billing_date)
            print('Billing Method:', billpay_method)
            print('Bill_Items:', bill_Items)
            print('PDF Data:', pdf_data)
            # print("Billing Item Table:", bill_itemtable)
            # Fetch related foreign key objects
            try:
                location = Location_Detials.objects.get(Location_Id=location_id) if location_id else None
                print('Location:', location)
            except ObjectDoesNotExist:
                return JsonResponse({'error': 'Location not found'})
            print('111111111111')
            # Parse billing item details with safe integer and float conversion
            try:
                discount_amount = float(bill_Items.get('Discount', 0))
                sgst_val = float(bill_Items.get('SGSTval', 0))
                cgst_val = float(bill_Items.get('CGSTval', 0))
                gst_amount = float(bill_Items.get('GSTAmount', 0))
                
                total_items = int(bill_Items.get('totalItems', 0))
                total_qty = int(bill_Items.get('totalQty', 0))
                total_amount = float(bill_Items.get('Amount', 0))
                net_amount = float(bill_Items.get('totalAmount', 0))
                paid_amount = float(bill_Items.get('PaidAmount', 0))
                balance_amount = float(bill_Items.get('BalanceAmount', 0))
                round_off = float(bill_Items.get('Roundoff', 0))
            except ValueError as ve:
                print(f"Invalid value in Bill_Items: {ve}")
                return JsonResponse({'error': 'Invalid value in Bill_Items'})

            print('22222222233333333')
            doctor_name = selected_patient_data.get('DoctorName') if selected_patient_data.get('DoctorName') else None
            patient_name = selected_patient_data.get('PatientName') if selected_patient_data.get('PatientName') else None
            print('33333444444',doctor_name,patient_name)
            # Create the main billing entry
            billing = OP_Pharmacy_Walkin_Billing_Table_Detials.objects.create(
                Doctor_Id= doctor_name,
                PatientName=patient_name,
                Billing_Date=billing_date,
                Billing_Type="OPPharmacyWalkin",
                Discount_Amount=discount_amount,
                SGST_val=sgst_val,
                CGST_val=cgst_val,
                Total_GSTAmount=gst_amount,
                Total_Items=total_items,
                Total_Qty=total_qty,
                Total_Amount=total_amount,
                Net_Amount=net_amount,
                Paid_Amount=paid_amount,
                Balance_Amount=balance_amount,
                Round_Off=round_off,
                created_by=user_name,
                Location=location
            )
            billing.save()
            print('billingggg',billing)
            
            # drug_status = OPD_Prescription_Details.objects.filter(Patient_Id__PatientId = selected_patient_data.get('PatientId'), Status = True) if selected_patient_data.get('PatientId') else None
            # print('12212112',drug_status)
            
            # for drug in drug_status:
            #     drug.Status = False
                
            #     drug.save()
            try:
                bill_itemtable = json.loads(request.POST.get('Billing_itemtable', '[]'))  # Parse JSON string to list
                
                if not isinstance(bill_itemtable, list):
                    return JsonResponse({'error': 'Invalid format for Billing_itemtable. Expected a list of items.'})
                
                for item in bill_itemtable:
                    if not isinstance(item, dict):
                        print(f"Invalid item format: {item}")
                        continue  # Skip invalid items
                    
                    # Debugging statement
                    print("Processing item:", item)
                    
                    # Extract and validate item fields
                    item_name = str(item.get('ItemName', 'Unknown Item'))
                    billing_quantity = int(item.get('Billing_Quantity', 0))
                    batch_no = item.get('BatchNo', 'N/A')
                    exp_date = item.get('Exp_Date', None)
                    
                    # Validate float fields
                    try:
                        unit_price = float(item.get('Unit_Price', 0) or 0.0)
                    except ValueError:
                        print(f"Invalid Unit_Price value: {item.get('Unit_Price')}")
                        unit_price = 0.0  # Default to 0.0

                    try:
                        amount = float(item.get('Amount', 0) or 0.0)
                    except ValueError:
                        print(f"Invalid Amount value: {item.get('Amount')}")
                        amount = 0.0  # Default to 0.0

                    try:
                        total = float(item.get('Total', 0) or 0.0)
                    except ValueError:
                        print(f"Invalid Total value: {item.get('Total')}")
                        total = 0.0  # Default to 0.0

                    # Validate and parse date
                    if exp_date:
                        try:
                            exp_date = datetime.strptime(exp_date, "%Y-%m-%d").date()
                        except ValueError:
                            print(f"Invalid Exp_Date format: {exp_date}")
                            exp_date = None  # Set to None if invalid
                    
                    # Debugging output
                    print(f"Validated item: Name={item_name}, Quantity={billing_quantity}, Unit_Price={unit_price}, Total={total}")
                    
                    # Create billing item
                    items_bill = OP_Walkin_BillingItem.objects.create(
                        Billing=billing,
                        ItemName=item_name,
                        Billing_Quantity=billing_quantity,
                        BatchNo=batch_no,
                        Exp_Date=exp_date,
                        Unit_Price=unit_price,
                        Amount=amount,
                        Total=total
                    )
                    items_bill.save()
                    print('Saved item:', items_bill)
            except Exception as e:
                print(f"Error while processing item: {item}, Error: {e}")  # Capture any errors
                return JsonResponse({'error': f"Failed to process item. Error: {str(e)}"})

            print('444444444444')
                    # Save each payment method
            for payment in billpay_method:
                payment_bill = OP_Walkin_Pharmacy_Billing_Payments.objects.create(
                    Billing=billing,
                    Billpay_method=payment.get('Billpay_method', ''),
                    CardType=payment.get('CardType', ''),
                    BankName=payment.get('BankName', ''),
                    ChequeNo=payment.get('ChequeNo', ''),
                    paidamount=float(payment.get('paidamount', 0)),
                    Additionalamount=float(payment.get('Additionalamount', 0)) if payment.get('Additionalamount') else 0,
                    transactionFee=payment.get('transactionFee', '') if payment.get('transactionFee') else '',
                )
            payment_bill.save()
        
            # if pdf_data:
            #     billing.pdf_data.save(f"{billing.Billing_Invoice_No}.pdf", ContentFile(pdf_data.read()))

            # Assuming the additional billing items need to be saved here if there’s a model for that
            # Uncomment and adapt the following if applicable
            # index = 0
            # while f'ItemId_{index}' in request.POST:
            #     item_id = request.POST.get(f'ItemId_{index}')
            #     quantity = int(request.POST.get(f'Billing_Quantity_{index}'))
            #     BillingItem.objects.create(
            #         billing=billing,
            #         ItemId=item_id,
            #         Billing_Quantity=quantity
            #     )
            #     index += 1

            return JsonResponse({'status': 'success', 'message': 'OP Data saved successfully','InvoiceNo': billing.Billing_Invoice_No})

        except Exception as e:
            print(f"Error occurred: {e}")
            return JsonResponse({'error': str(e)})  
        

def get_OP_Pharmacy_Billing_datas(request):
    if request.method == 'GET':
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

            print('Searchquery',Searchquery)
            queryset = OP_Pharmacy_Walkin_Billing_Table_Detials.objects.filter(Searchquery)
            # Fetch the OP Pharmacy billing records
            print('11111111111')
            datafetch = []
            for idx,billing in enumerate(queryset,start=1):
                datafetch.append({
                    'id': idx,
                    'Billing_Invoice_No': billing.Billing_Invoice_No,
                    'DoctorName': billing.Doctor_Id,
                    'PatientID': billing.PatientId,
                    'PatientName': billing.PatientName,
                    'Billing_Date': billing.Billing_Date,
                    'Billing_Type': billing.Billing_Type,
                    'Discount_Amount': billing.Discount_Amount,
                    'SGST_val': billing.SGST_val,
                    'CGST_val': billing.CGST_val,
                    'Total_GSTAmount': billing.Total_GSTAmount,
                    'Total_Items': billing.Total_Items,
                    'Total_Qty': billing.Total_Qty,
                    'Total_Amount': billing.Total_Amount,
                    'Net_Amount': billing.Net_Amount,
                    'Paid_Amount': billing.Paid_Amount,
                    'Balance_Amount': billing.Balance_Amount,
                    'Round_Off': billing.Round_Off,
                    'created_by': billing.created_by,
                    'Location': billing.Location.Location_Name if billing.Location else None
                })

            return JsonResponse(datafetch, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)})




def get_Drug_Administration_datas(request):
    if request.method == 'GET':
        try:
            booking_id = request.GET.get('Booking_Id')
            current_date_str = request.GET.get('Date')
            current_date = datetime.strptime(current_date_str, '%Y-%m-%d').date()
            current_datetime = datetime.now().date()

            # Fetch the drug administration records
            drug_administrations = Doctor_drug_prescription.objects.filter(Booking_Id=booking_id)
            regular = []
            sos = []
            print('11111111111')
            print('2222222222',current_datetime)
            for admin in drug_administrations:
                if admin.FrequencyMethod == 'Regular':
                    # Fetch related nurse drug completed administration records
                    nurse_completed_admins = Ip_Nurse_Drug_Completed_Administration.objects.filter(
                        Prescription_Id=admin.Prescription_Id,
                        Issued_Date=current_datetime
                    ).values('FrequencyIssued', 'Status', 'Issued_Date')
                    
                    # Prepare data if there are nurse completed administrations
                    if nurse_completed_admins:
                        data = [
                            {
                                "FrequencyIssued": nca['FrequencyIssued'],
                                "Status": nca['Status'],
                                "Date": nca['Issued_Date']
                            }
                            for nca in nurse_completed_admins
                        ]
                        common_data = {
                            "Prescription_Id": admin.Prescription_Id,
                            "Department": admin.Department,
                            "DoctorName": admin.DoctorName.ShortName,
                            "GenericName": admin.ProductCode.Product_Detials.GenericName.GenericName,
                            "MedicineCode": admin.ProductCode.Product_Detials.pk,
                            "MedicineName": f'{admin.ProductCode.Product_Detials.ItemName}{admin.ProductCode.Product_Detials.Strength}',
                            "FrequencyMethod": admin.FrequencyMethod,
                            "FrequencyType": admin.Frequency.FrequencyType,
                            "FrequencyTime": admin.Frequency.FrequencyTime,
                            "FrequencyName": admin.Frequency.FrequencyName,
                            "PrescribedDate": admin.Date.strftime('%Y-%m-%d'),
                            "AdminisDose": admin.AdminisDose,
                            "Instruction": admin.Instruction,
                            "FrequencyIssued": data,
                            "CurrentDate": data[0]['Date'] if data else None
                        }
                        regular.append(common_data)
                
                else:  # Handle non-regular frequency (SOS)
                    completed_count = Ip_Nurse_Drug_Completed_Administration.objects.filter(
                        FrequencyMethod=admin.FrequencyMethod,
                        Prescription_Id=admin.Prescription_Id
                    ).count()
                    
                    if completed_count != int(admin.Quantity):
                        common_data1 = {
                            "Prescription_Id": admin.Prescription_Id,
                            "Route": admin.Route,
                            "Department": admin.Department,
                            "DoctorName": admin.DoctorName.ShortName,
                            "GenericName": admin.ProductCode.Product_Detials.GenericName.GenericName,
                            "MedicineCode": admin.ProductCode.Product_Detials.pk,
                            "MedicineName": f'{admin.ProductCode.Product_Detials.ItemName}{admin.ProductCode.Product_Detials.Strength}',
                            "FrequencyMethod": admin.FrequencyMethod,
                            "FrequencyType": admin.Frequency.FrequencyType,
                            "FrequencyTime": admin.Frequency.FrequencyTime,
                            "FrequencyName": admin.Frequency.FrequencyName,
                            "Dosage": admin.ProductCode.Product_Detials.Strength,
                            "Date": admin.Date,
                            "AdminisDose": admin.AdminisDose,
                            "Instruction": admin.Instruction,
                        }
                        sos.append(common_data1)

            return JsonResponse({'Regular': regular, 'SOS': sos}, safe=False)

        except Exception as e:
            print("Error", e)
            return JsonResponse({"Error Acquired:": str(e)}, status=500)    
        
        
# @csrf_exempt
# def insert_Drug_Administration_nurse_frequencywise_datas(request):
#     if request.method == 'POST':
#         try:
#             # Load JSON data from the request body
#             json_data = json.loads(request.body)
#             print('json_data', json_data)
            
            
#             for prescription in json_data:
#                 FrequencyMethod = prescription.get('FrequencyMethod')
#                 Prescription_Id = prescription.get('Prescription_Id')
#                 Completed_Date = prescription.get('Completed_Date')
#                 Completed_Time = prescription.get('Completed_Time')
#                 CapturedBy = prescription.get('CapturedBy')
#                 Completed_Remarks = prescription.get('Remarks')
#                 FrequencyIssued = prescription.get('FrequencyIssued')

#                 if FrequencyMethod == 'Regular':
#                     FrequencyIssued_str = f"{FrequencyIssued}:00:00"
#                     completed_time = datetime.strptime(Completed_Time, '%H:%M:%S')
#                     FrequencyIssued_time = datetime.strptime(FrequencyIssued_str, "%H:%M:%S")

#                     before_time = FrequencyIssued_time - timedelta(minutes=30)
#                     after_time = FrequencyIssued_time + timedelta(minutes=30)

#                     # Determine Status based on time comparison
#                     if before_time <= completed_time <= after_time:
#                         Status = 'Issued'
#                     elif completed_time < before_time:
#                         Status = 'Before'
#                     else:
#                         Status = 'Delay'

#                     # Update existing records using Django ORM
#                     updated_records = Ip_Nurse_Drug_Completed_Administration.objects.filter(
#                         Frequency=FrequencyIssued,
#                         Nurse_Prescription_Id=Prescription_Id,
#                         Status='Pending'
#                     ).update(
#                         Status=Status,
#                         Complete_Date=Completed_Date,
#                         Complete_Time=Completed_Time,
#                         Completed_Remarks=Completed_Remarks,
#                         CapturedBy=CapturedBy
#                     )
#                     print(f"Updated {updated_records} records.")

#                 else:
#                     # Insert new records using Django ORM
#                     issued_time = Completed_Time.split(':')[0]  # Use the hour part
#                     Nurse_drug_prescription.objects.create(
#                         Prescription_Id=Prescription_Id,
#                         Booking_Id=prescription.get('Booking_Id'),
#                         Department=prescription.get('Department'),
#                         DoctorName=prescription.get('DoctorName'),
#                         GenericName=prescription.get('GenericName'),
#                         MedicineCode=prescription.get('MedicineCode'),
#                         MedicineName=prescription.get('MedicineName'),
#                         Dosage=prescription.get('Dosage'),
#                         Route=prescription.get('Route'),
#                         FrequencyIssued=FrequencyIssued,
#                         FrequencyMethod=FrequencyMethod,
#                         Quantity=prescription.get('Quantity'),
#                         Issued_Date=prescription.get('Date'),
#                         Complete_Date=Completed_Date,
#                         Complete_Time=Completed_Time,
#                         Completed_Remarks=Completed_Remarks,
#                         Status='Issued',
#                         Location=prescription.get('Location'),
#                         CapturedBy=CapturedBy,
#                         AdminisDose=prescription.get('AdminisDose')
#                     )
            
#             return JsonResponse({'message': 'Data inserted successfully'})

#         except Exception as e:
#             print(f"An error occurred: {str(e)}")
#             return JsonResponse({'error': 'An internal server error occurred'})

@csrf_exempt
def insert_Drug_Administration_nurse_frequencywise_datas(request):
    if request.method == 'POST':
        try:
            # Load JSON data from the request body
            json_data = json.loads(request.body)
            print('json_data', json_data)

            # # Fetch the maximum Nurse_Prescription_Id
            # max_id = Ip_Nurse_Drug_Completed_Administration.objects.aggregate(max_id=models.Max('Nurse_Prescription_Id'))['max_id']
            # next_id = (max_id + 1) if max_id is not None else 1

            for prescription in json_data:
                FrequencyMethod = prescription.get('FrequencyMethod')
                Prescription_Id = prescription.get('Prescription_Id')
                Completed_Date = prescription.get('Completed_Date')
                Completed_Time = prescription.get('Completed_Time')
                CapturedBy = prescription.get('CapturedBy')
                Completed_Remarks = prescription.get('Remarks')
                FrequencyIssued = prescription.get('FrequencyIssued')

                if FrequencyMethod == 'Regular':
                    print('freqq111')
                    FrequencyIssued_str = f"{FrequencyIssued}:00:00"
                    completed_time = datetime.strptime(Completed_Time, '%H:%M:%S')
                    FrequencyIssued_time = datetime.strptime(FrequencyIssued_str, "%H:%M:%S")

                    before_time = FrequencyIssued_time - timedelta(minutes=30)
                    after_time = FrequencyIssued_time + timedelta(minutes=30)
                    print('freqq1112323', before_time, after_time, completed_time)
                    if before_time <= completed_time <= after_time:
                        Status = 'Issued'
                    elif completed_time < before_time:
                        Status = 'Before'
                    else:
                        Status = 'Delay'
                    print('freqq2222', Status)

                    # Test filtering by each condition individually
                    check_frequency_issued = Ip_Nurse_Drug_Completed_Administration.objects.filter(FrequencyIssued=FrequencyIssued)
                    check_prescription_id = Ip_Nurse_Drug_Completed_Administration.objects.filter(Prescription_Id=Prescription_Id)
                    check_status_pending = Ip_Nurse_Drug_Completed_Administration.objects.filter(Status='Pending')

                    print('Records with matching FrequencyIssued:', check_frequency_issued.count())
                    print('Records with matching Prescription_Id:', check_prescription_id.count())
                    print('Records with matching Status Pending:', check_status_pending.count())

                    # Update existing records
                    updated_count = Ip_Nurse_Drug_Completed_Administration.objects.filter(
                        FrequencyIssued=FrequencyIssued,
                        Prescription_Id=Prescription_Id,
                        Status='Pending'
                    ).update(
                        Status=Status,
                        Complete_Date=Completed_Date,
                        Complete_Time=Completed_Time,
                        Completed_Remarks=Completed_Remarks,
                        CapturedBy=CapturedBy
                    )

                    # Debug output
                    if updated_count == 0:
                        print("No matching records found for update.")
                    else:
                        print(f"Records updated: {updated_count}")

                else:
                    print('freqq4444')
                    # Insert new records
                    Issued_Time = Completed_Time.split(':')[0]  # Use the hour part
                    Department = prescription.get('Department')
                    DoctorName = prescription.get('DoctorName')
                    GenericName = prescription.get('GenericName')
                    MedicineCode = prescription.get('MedicineCode')
                    MedicineName = prescription.get('MedicineName')
                    Dosage = prescription.get('Dosage')
                    Route = prescription.get('Route')
                    Quantity = prescription.get('Quantity')
                    Location = prescription.get('Location')
                    AdminisDose = prescription.get('AdminisDose')
                    Date = prescription.get('Date')  # Use Date if provided
                    Status = 'Issued'

                    # Create a new record
                    Ip_Nurse_Drug_Completed_Administration.objects.create(
                        Nurse_Prescription_Id=next_id,
                        Prescription_Id=Prescription_Id,
                        Booking_Id=prescription.get('Booking_Id'),
                        Department=Department,
                        DoctorName=DoctorName,
                        ProductCode=MedicineCode,
                        Route=Route,
                        FrequencyIssued=FrequencyIssued,
                        FrequencyMethod=FrequencyMethod,
                        Quantity=Quantity,
                        Issued_Date=Date,
                        Complete_Date=Completed_Date,
                        Complete_Time=Completed_Time,
                        Completed_Remarks=Completed_Remarks,
                        Status=Status,
                        Location=Location,
                        CapturedBy=CapturedBy,
                        AdminisDose=AdminisDose
                    )
                    next_id += 1

            return JsonResponse({'message': 'Data inserted successfully'})

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

    else:
        # Handle GET or other HTTP methods
        return HttpResponseBadRequest("This endpoint only accepts POST requests.")


def get_for_ip_drugs_doctor_show(request):
    if request.method == 'GET':
        try:
            booking_id = request.GET.get('Booking_id')
            current_date = datetime.now().date()
            
            # First query to get distinct prescriptions for the given Booking ID
            prescriptions = Ip_Nurse_Drug_Completed_Administration.objects.filter(
                Booking_Id=booking_id
            ).select_related(
                'Prescription_Id', 'DoctorName', 'ProductCode', 'Location'
            ).values(
                'Prescription_Id', 'Booking_Id', 'Department', 'DoctorName__ShortName',
                'ProductCode__Product_Detials__ItemName', 'Route', 'FrequencyMethod',
                'Issued_Date', 'Location__Location_Id', 'AdminisDose'
            ).distinct()
            
            show_list = []
            for prescription in prescriptions:
                # Nested query to get FrequencyIssued details for each Prescription_Id and Booking_Id
                frequency_issued_data = Ip_Nurse_Drug_Completed_Administration.objects.filter(
                    Prescription_Id=prescription['Prescription_Id'],
                    Booking_Id=prescription['Booking_Id'],
                    Issued_Date=prescription['Issued_Date']
                ).values(
                    'FrequencyIssued', 'Complete_Time', 'Completed_Remarks', 'Status', 'CapturedBy', 'Complete_Date'
                )
                
                # Create a list of frequency data
                frequency_data = [
                    {
                        'FrequencyIssued': data['FrequencyIssued'],
                        'Completed_Time': data['Complete_Time'],
                        'Completed_Remarks': data['Completed_Remarks'],
                        'Status': data['Status'],
                        'CapturedBy': data['CapturedBy'],
                        'Completed_Date': data['Complete_Date'],
                    }
                    for data in frequency_issued_data
                ]
                
                # Format each prescription data with associated frequency issued data
                show_data = {
                    "Prescription_Id": prescription['Prescription_Id'],
                    "Booking_Id": prescription['Booking_Id'],
                    "Department": prescription['Department'],
                    "DoctorName": prescription['DoctorName__ShortName'],
                    "GenericName": prescription['ProductCode__Product_Detials__ItemName'],
                    "MedicineName": prescription['ProductCode__Product_Detials__ItemName'],
                    "Route": prescription['Route'],
                    "FrequencyIssued": frequency_data,
                    "FrequencyMethod": prescription['FrequencyMethod'],
                    "PrescribedDate": prescription['Issued_Date'],
                    "IssuedDate": prescription['Issued_Date'],
                    "Location": prescription['Location__Location_Id'],
                    "AdminisDose": prescription['AdminisDose'],
                }
                
                show_list.append(show_data)
            
            return JsonResponse(show_list, safe=False)

        except Exception as er:
            return JsonResponse({"Error Acquired": str(er)}, status=500)

# def job_function():
#     try:
#         print('job function insert')
#         # Fetch drug administration details
#         administrations = Doctor_drug_prescription.objects.all()
#         print('Query result:', administrations)
    
#         for administration in administrations:
#             if administration.FrequencyMethod == 'Regular':
#                 tablet_duration_days = int(administration.Duration)
#                 frequency_times = administration.Frequency.split(',')
#                 print('frequency_times',frequency_times)
#                 tablet_frequency_time = [(int(hour), 0) for hour in frequency_times]
                
#                 # Ensure `StartDate` is a date object and `StartTime` is a time object
#                 start_date = administration.created_at.strftime('%Y-%m-%d') 
#                 start_time = administration.created_at.strftime('%H:%M:%S')

#                 print('111111111',start_date,start_time)
#                 for day_offset in range(tablet_duration_days):
#                     current_date = start_date + timedelta(days=day_offset)
#                     tablet_times = []

#                     for freq_time in tablet_frequency_time:
#                         tablet_datetime = datetime.combine(current_date, time(freq_time[0], freq_time[1]))
#                         if tablet_datetime.time() < start_time:
#                             tablet_datetime += timedelta(days=1)
#                         tablet_times.append(tablet_datetime)
                        
#                     print('tablet_times',tablet_times)

#                     if tablet_times:
#                         tablet_times.sort()
#                         today_date = timezone.now().date()

#                         # Update pending requests
#                         Ip_Nurse_Drug_Completed_Administration.objects.filter(
#                             Status='Pending', Issued_Date__lt=today_date
#                         ).update(Status='NotIssued')

#                         for tablet_time in tablet_times:
#                             if today_date == tablet_time.date():
#                                 tablet_issue = int(tablet_time.strftime("%H"))
#                                 tablet_date_issue = tablet_time.date()
#                                 print('Tablet issue date:', tablet_date_issue)

#                                 # Check pending status and handle accordingly
#                                 if administration.Status == 'Pending':
#                                     if administration.RequestType == 'Outsourced':
#                                         handle_outsourced_request(administration, tablet_issue, tablet_date_issue)
#                                     elif administration.RequestType == 'Inhouse':
#                                         handle_inhouse_request(administration, tablet_issue, tablet_date_issue)

#     except Exception as e:
#         print(f"Error in job_function: {e}")
#         # Use Django's logging for better error tracking

# # Define handle_outsourced_request and handle_inhouse_request functions here
# # They should use Django ORM to update relevant models as needed


# @transaction.atomic
# def handle_outsourced_request(row, tablet_issue, tablet_date_issue):
#     """Handles outsourced drug requests using Django ORM."""

#     exists = Ip_Nurse_Drug_Completed_Administration.objects.filter(
#         prescription_id=row.Prescription_Id, booking_id=row.Booking_Id,
#         frequency_issued=tablet_issue, issued_date=tablet_date_issue
#     ).exists()

#     if not exists:
#         Ip_Nurse_Drug_Completed_Administration.objects.create(
#             Prescription_Id=row.prescription_id,
#             Booking_Id=row.booking_id,
#             Department=row.department,
#             DoctorName=row.doctor_name,
#             ProductCode=row.generic_name,
#             Dosage=row.dosage,
#             Route=row.route,
#             FrequencyIssued=tablet_issue,
#             FrequencyMethod=row.frequency_method,
#             Quantity=1,  # Adjust as per actual requirement
#             Issued_Date=tablet_date_issue,
#             Complete_Date=None,
#             Complete_Time=None,
#             Completed_Remarks='',
#             Status='Pending',
#             Location=row.location,
#             CapturedBy='',  # Define as needed
#             AdminisDose=row.adminis_dose
#         )


# @transaction.atomic
# def handle_inhouse_request(row, tablet_issue, tablet_date_issue):
#     """Handles in-house drug requests using Django ORM."""

#     # Handling 'Daily' frequency
#     if row.FrequencyMethod == 'Daily':
#         # Check if the request already exists for the given prescription and booking on this date
#         existing_request = ip_drug_request_table.objects.filter(
#             Prescibtion_Id=row.Prescription_Id,
#             Booking_Id=row.Booking_Id,
#             Date=tablet_date_issue
#         ).first()

#         if existing_request is None:
#             remaining = int(row.Quantity) - int(row.RequestQuantity)
#             ip_drug_request_table.objects.create(
#                 Drug_Request_Id=next_id_req,
#                 Booking_Id=row.Booking_Id,
#                 Prescibtion_Id=row.Prescription_Id,
#                 Department=row.Department,
#                 DoctorName=row.DoctorName,
#                 GenericName=row.GenericName,
#                 MedicineCode=row.MedicineCode,
#                 MedicineName=row.MedicineName,
#                 Dosage=row.Dosage,
#                 Route=row.Route,
#                 RequestType=row.FrequencyMethod,
#                 Quantity=row.Quantity,
#                 RequestQuantity=row.RequestQuantity,
#                 RemainingQuantity=remaining,
#                 Location=row.Location,
#                 CreatedBy=row.Location,  # or the relevant user field
#                 Status='Pending',
#                 Priscription_Barcode=row.Prescription_Barcode,
#                 Duration=row.Duration,
#                 DurationType=row.DurationType,
#                 Date=tablet_date_issue
#             )
#         elif existing_request.Status == "Received":
#             # Ensure drug request entry for 'Daily' frequency
#             existing_administration = Ip_Nurse_Drug_Completed_Administration.objects.filter(
#                 Prescription_Id=row.Prescription_Id,
#                 Booking_Id=row.Booking_Id,
#                 FrequencyIssued=tablet_issue,
#                 Issued_Date=tablet_date_issue
#             ).first()

#             if existing_administration is None:
#                 next_id1 = Ip_Nurse_Drug_Completed_Administration.objects.aggregate(
#                     max_id=models.Max('Nurse_Prescription_Id')
#                 )['max_id']
#                 next_id1 = next_id1 + 1 if next_id1 is not None else 1

#                 Ip_Nurse_Drug_Completed_Administration.objects.create(
#                     Nurse_Prescription_Id=next_id1,
#                     Prescription_Id=row.Prescription_Id,
#                     Booking_Id=row.Booking_Id,
#                     Department=row.Department,
#                     DoctorName=row.DoctorName,
#                     GenericName=row.GenericName,
#                     MedicineCode=row.MedicineCode,
#                     MedicineName=row.MedicineName,
#                     Dosage=row.Dosage,
#                     Route=row.Route,
#                     FrequencyIssued=tablet_issue,
#                     FrequencyMethod=row.FrequencyMethod,
#                     Quantity=1,  # Adjust this as needed
#                     Issued_Date=tablet_date_issue,
#                     Status='Pending',
#                     Location=row.Location,
#                     CapturedBy='',  # Define appropriately
#                     AdminisDose=row.AdminisDose
#                 )

#     # Handling 'Total' frequency
#     elif row.FrequencyMethod == 'Total':
#         max_id_req = ip_drug_request_table.objects.aggregate(max_id=models.Max('Drug_Request_Id'))['max_id']
#         next_id_req = max_id_req + 1 if max_id_req is not None else 1

#         existing_request_total = ip_drug_request_table.objects.filter(
#             Prescibtion_Id=row.Prescription_Id,
#             Booking_Id=row.Booking_Id
#         ).first()

#         if existing_request_total is None:
#             remaining = int(row.Quantity) - int(row.RequestQuantity)
#             ip_drug_request_table.objects.create(
#                 Drug_Request_Id=next_id_req,
#                 Booking_Id=row.Booking_Id,
#                 Prescibtion_Id=row.Prescription_Id,
#                 Department=row.Department,
#                 DoctorName=row.DoctorName,
#                 GenericName=row.GenericName,
#                 MedicineCode=row.MedicineCode,
#                 MedicineName=row.MedicineName,
#                 Dosage=row.Dosage,
#                 Route=row.Route,
#                 RequestType=row.FrequencyMethod,
#                 Quantity=row.Quantity,
#                 RequestQuantity=row.RequestQuantity,
#                 RemainingQuantity=remaining,
#                 Location=row.Location,
#                 CreatedBy=row.Location,  # Adjust as per requirement
#                 Status='Pending',
#                 Priscription_Barcode=row.Prescription_Barcode,
#                 Duration=row.Duration,
#                 DurationType=row.DurationType,
#                 Date=tablet_date_issue
#             )
#         elif existing_request_total.Status == "Received":
#             existing_administration_total = Ip_Nurse_Drug_Completed_Administration.objects.filter(
#                 Prescription_Id=row.Prescription_Id,
#                 Booking_Id=row.Booking_Id,
#                 FrequencyIssued=tablet_issue,
#                 Issued_Date=tablet_date_issue
#             ).first()

#             if existing_administration_total is None:
#                 next_id1 = Ip_Nurse_Drug_Completed_Administration.objects.aggregate(
#                     max_id=models.Max('Prescibtion_Issue_Id')
#                 )['max_id']
#                 next_id1 = next_id1 + 1 if next_id1 is not None else 1

#                 Ip_Nurse_Drug_Completed_Administration.objects.create(
#                     Prescibtion_Issue_Id=next_id1,
#                     Prescription_Id=row.Prescription_Id,
#                     Booking_Id=row.Booking_Id,
#                     Department=row.Department,
#                     DoctorName=row.DoctorName,
#                     GenericName=row.GenericName,
#                     MedicineCode=row.MedicineCode,
#                     MedicineName=row.MedicineName,
#                     Dosage=row.Dosage,
#                     Route=row.Route,
#                     FrequencyIssued=tablet_issue,
#                     FrequencyMethod=row.FrequencyMethod,
#                     Quantity=1,  # Adjust as necessary
#                     Issued_Date=tablet_date_issue,
#                     Status='Pending',
#                     Location=row.Location,
#                     CapturedBy='',  # Adjust as needed
#                     AdminisDose=row.AdminisDose
#                 )

# # Create and configure scheduler
# sched = BackgroundScheduler()

# # Calculate next run time for 08:08
# now = timezone.now()
# next_run_time = datetime.combine(now, time(13,54))

# # Schedule the job function
# sched.add_job(job_function, "date", run_date=next_run_time)
# print('Scheduler started successfully,DrugAdministration')