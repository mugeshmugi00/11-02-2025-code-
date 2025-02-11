import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import *

@csrf_exempt
@require_http_methods(['GET'])
def Insurance_client_master_details(request):
    if request.method == 'GET':
        try:
            Insurance_ins = Insurance_Master_Detials.objects.all()
            Client_ins = Client_Master_Detials.objects.all()
            Corporate_ins = Corporate_Master_Detials.objects.all()

            insurance_names = []
            
            for ins in Insurance_ins:
                insurance_name = {
                    'id': ins.Insurance_Id,
                    'insurance_name': ins.Insurance_Name
                }
                insurance_names.append(insurance_name)

            for client in Client_ins:
                client_name = {
                    'id': client.Client_Id,
                    'insurance_name': client.Client_Name
                }
                insurance_names.append(client_name)
                
            for corp in Corporate_ins:
                corp_name = {
                    'id': corp.Corporate_Id,
                    'insurance_name': corp.Corporate_Name
                }
                insurance_names.append(corp_name)

            return JsonResponse(insurance_names, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)})

# @csrf_exempt
# @require_http_methods(['GET'])
# def Overall_services_link(request):
#     if request.method == 'GET':
#         try:
#             Doctor_ins = Doctor_Personal_Form_Detials.objects.all()
#             print('Doccccccc',Doctor_ins)
#             for doc in Doctor_ins:
#                 # doctor = Doctor_Personal_Form_Detials.objects.get(pk=doc.Doctor_ID)
#                 ratecard = Doctor_Ratecard_Master.objects.filter(Doctor_ID=doc).first()
#                 print('ratteeeeee',ratecard)
#                 room_fees = RoomTypeFee.objects.filter(doctor_ratecard=ratecard)
#                 print('ratteessss',room_fees)
#                 client_fees = ClientFee.objects.filter(doctor_ratecard=ratecard)
#                 print("client_fees",client_fees)
#                 corporate_fees = CorporateFee.objects.filter(doctor_ratecard=ratecard)
#                 print("corporate_fees",corporate_fees)
#                 insurance_fees = InsuranceFee.objects.filter(doctor_ratecard=ratecard)
#                 client_roomtype_fees = ClientRoomTypeFee.objects.filter(doctor_ratecard=ratecard)
#                 print("client_roomtype_fees",client_roomtype_fees)
#                 corporate_roomtype_fees = CorporateRoomTypeFee.objects.filter(doctor_ratecard=ratecard)
#                 print("corporate_roomtype_fees",corporate_roomtype_fees)
                
                
                
#                 doctor_data = {
#                     'id': doc.Doctor_ID,
#                     'doctor_name': f"{doc.Tittle}.{doc.First_Name} {doc.Middle_Name} {doc.Last_Name}",
#                     'DoctorType': doc.DoctorType,
#                     'Status': 'Active' if doc.Status else 'Inactive',
#                     'Roomtypes':[],
#                     'Ratecarddetials': [
#                         {
#                             'id': 1,
#                             'isrowgroup': False,
#                             'RatecardType': 'General',
#                             'RatecardShow': 'General',
#                             'RatecardName': None,
#                             'doctor_ratecard_id':ratecard.RateCard_Id,
#                             'consultation_Prev_fee': ratecard.General_Prev_Consultation_Fee,
#                             'consultation_curr_fee': ratecard.General_Consultation_Fee,
#                             'follow_up_Prev_fee': ratecard.General_Prev_Follow_Up_Fee,
#                             'follow_up_curr_fee': ratecard.General_Follow_Up_Fee,
#                             'emg_consultant_Prev_fee': ratecard.General_Prev_Emg_Consulting_Fee,
#                             'emg_consultant_curr_fee': ratecard.General_Emg_Consulting_Fee,
#                         },
#                         {
#                             'id':2,
#                             'isrowgroup': False,
#                             'RatecardType': 'Special',
#                             'RatecardShow': 'Special',
#                             'RatecardName': None,
#                             'doctor_ratecard_id':ratecard.RateCard_Id,
#                             'consultation_Prev_fee': ratecard.Special_Prev_Consultation_Fee,
#                             'consultation_curr_fee': ratecard.Special_Consultation_Fee,
#                             'follow_up_Prev_fee': ratecard.Special_Prev_Follow_Up_Fee,
#                             'follow_up_curr_fee': ratecard.Special_Follow_Up_Fee,
#                             'emg_consultant_Prev_fee': ratecard.Special_Prev_Emg_Consulting_Fee,
#                             'emg_consultant_curr_fee': ratecard.Special_Emg_Consulting_Fee,
#                         }
#                     ]
#                 }
#                 # Add room fees to ratecard details
            
#                 # Add client fees as a grouped section
#                 if client_fees:
#                     doctor_data['Ratecarddetials'].append({
#                         'id': len(doctor_data['Ratecarddetials']) + 1,
#                         'isrowgroup': True,
#                         'RatecardType': 'Client',
#                         'RatecardShow': 'Client',
#                         'RatecardName': None,
#                         'consultation_Prev_fee': None,
#                         'consultation_curr_fee': None,
#                         'follow_up_Prev_fee': None,
#                         'follow_up_curr_fee': None,
#                         'emg_consultant_Prev_fee': None,
#                         'emg_consultant_curr_fee': None,
#                     })
#                 for client_fee in client_fees:
#                     client_ratecard = {
#                         'id': len(doctor_data['Ratecarddetials']) + 1,
#                         'isrowgroup': False,
#                         'RatecardType': 'Client',
#                         'RatecardShow': None,
#                         'doctor_ratecard_id':client_fee.doctor_ratecard.RateCard_Id,
#                         'RatecardName': client_fee.client.Client_Name,
#                         'Ratecardid': client_fee.client.Client_Id,
#                         'consultation_Prev_fee': client_fee.Prev_Consultation_Fee,
#                         'consultation_curr_fee': client_fee.Consultation_Fee,
#                         'follow_up_Prev_fee': client_fee.Prev_Follow_Up_Fee,
#                         'follow_up_curr_fee': client_fee.Follow_Up_Fee,
#                         'emg_consultant_Prev_fee': client_fee.Prev_Emg_Consulting_Fee,
#                         'emg_consultant_curr_fee': client_fee.Emg_Consulting_Fee,
#                     }
#                     doctor_data['Ratecarddetials'].append(client_ratecard)
                
#                 #Add corporate fees as a grouped section
#                 if corporate_fees:
#                     doctor_data['Ratecarddetials'].append({
#                         'id': len(doctor_data['Ratecarddetials']) + 1,
#                         'isrowgroup': True,
#                         'RatecardType': 'Corporate',
#                         'RatecardShow': 'Corporate',
#                         'RatecardName': None,
#                         'consultation_Prev_fee': None,
#                         'consultation_curr_fee': None,
#                         'follow_up_Prev_fee': None,
#                         'follow_up_curr_fee': None,
#                         'emg_consultant_Prev_fee': None,
#                         'emg_consultant_curr_fee': None,
#                     })
                
#                 for corporate_fee in corporate_fees:
#                     corporate_ratecard = {
#                         'id': len(doctor_data['Ratecarddetials']) + 1,
#                         'isrowgroup': False,
#                         'RatecardType': 'Corporate',
#                         'RatecardShow': None,
#                         'doctor_ratecard_id':corporate_fee.doctor_ratecard.RateCard_Id,
#                         'RatecardName': corporate_fee.corporate.Corporate_Name,
#                         'Ratecardid': corporate_fee.corporate.Corporate_Id,
#                         'consultation_Prev_fee': corporate_fee.Prev_Consultation_Fee,
#                         'consultation_curr_fee': corporate_fee.Consultation_Fee,
#                         'follow_up_Prev_fee': corporate_fee.Prev_Follow_Up_Fee,
#                         'follow_up_curr_fee': corporate_fee.Follow_Up_Fee,
#                         'emg_consultant_Prev_fee': corporate_fee.Prev_Emg_Consulting_Fee,
#                         'emg_consultant_curr_fee': corporate_fee.Emg_Consulting_Fee,
#                     }
#                     doctor_data['Ratecarddetials'].append(corporate_ratecard)
                    
                
#                 # Add insurance fees as a grouped section
#                 if insurance_fees:
#                     doctor_data['Ratecarddetials'].append({
#                         'id': len(doctor_data['Ratecarddetials']) + 1,
#                         'isrowgroup': True,
#                         'RatecardType': 'Insurance',
#                         'RatecardShow': 'Insurance',
#                         'RatecardName': None,
#                         'consultation_Prev_fee': None,
#                         'consultation_curr_fee': None,
#                         'follow_up_Prev_fee': None,
#                         'follow_up_curr_fee': None,
#                         'emg_consultant_Prev_fee': None,
#                         'emg_consultant_curr_fee': None,
#                     })
#                 for insurance_fee in insurance_fees:
#                     insurance_ratecard = {
#                         'id': len(doctor_data['Ratecarddetials']) + 1,
#                         'isrowgroup': False,
#                         'RatecardType': 'Insurance',
#                         'RatecardShow': None,
#                         'doctor_ratecard_id':insurance_fee.doctor_ratecard.RateCard_Id,
#                         'RatecardName': insurance_fee.insurance.Insurance_Name,
#                         'Ratecardid': insurance_fee.insurance.Insurance_Id,
#                         'consultation_Prev_fee': insurance_fee.Prev_Consultation_Fee,
#                         'consultation_curr_fee': insurance_fee.Consultation_Fee,
#                         'follow_up_Prev_fee': insurance_fee.Prev_Follow_Up_Fee,
#                         'follow_up_curr_fee': insurance_fee.Follow_Up_Fee,
#                         'emg_consultant_Prev_fee': insurance_fee.Prev_Emg_Consulting_Fee,
#                         'emg_consultant_curr_fee': insurance_fee.Emg_Consulting_Fee,
#                     }
#                     doctor_data['Ratecarddetials'].append(insurance_ratecard)
                    
#                     for room_fee in room_fees:
#                         room_name = room_fee.room_type.Ward_Name.Ward_Name
#                         room_id = room_fee.room_type.Room_Id
#                         if {'id':room_id,'name':room_name} not in doctor_data['Roomtypes']:
#                             doctor_data['Roomtypes'].append({'id':room_id,'name':room_name})
                    
#                     for dat in doctor_data['Ratecarddetials']:
                    
#                         for room_fee in room_fees:
#                             room_name = room_fee.room_type.Ward_Name.Ward_Name
#                             room_id = room_fee.room_type.Room_Id
#                             if dat['RatecardType'] == 'General':
#                                 dat[f'{room_name}_{room_id}_prev_fee'] = room_fee.General_Prev_fee
#                                 dat[f'{room_name}_{room_id}_curr_fee'] = room_fee.General_fee
#                             elif dat['RatecardType'] == 'Special':
#                                 dat[f'{room_name}_{room_id}_prev_fee'] = room_fee.Special_Prev_fee
#                                 dat[f'{room_name}_{room_id}_curr_fee'] = room_fee.Special_fee
#                             elif dat['RatecardType'] == 'Insurance':
#                                 if dat['isrowgroup']:
#                                     dat[f'{room_name}_{room_id}_prev_fee'] = None
#                                     dat[f'{room_name}_{room_id}_curr_fee'] = None
#                                 else:
#                                     if dat['Ratecardid']:
#                                         ins_id=dat['Ratecardid']
#                                         ins_roomtype_fees = InsuranceRoomTypeFee.objects.get(doctor_ratecard=ratecard,room_type_fee=room_fee,insurance__pk=ins_id)
                                    
#                                         if ins_roomtype_fees:
#                                             dat[f'{room_name}_{room_id}_prev_fee'] = ins_roomtype_fees.Prev_fee
#                                             dat[f'{room_name}_{room_id}_curr_fee'] = ins_roomtype_fees.fee
#                                         else:
#                                             dat[f'{room_name}_{room_id}_prev_fee'] = None
#                                             dat[f'{room_name}_{room_id}_curr_fee'] = None
                            
#                             elif dat['RatecardType'] == 'Client':
                                
#                                 if dat['isrowgroup']:
#                                     dat[f'{room_name}_{room_id}_prev_fee'] = None
#                                     dat[f'{room_name}_{room_id}_curr_fee'] = None
#                                 else:
#                                     if dat['Ratecardid']:
#                                         client_id=dat['Ratecardid']
#                                         client_roomtype_fees = ClientRoomTypeFee.objects.get(doctor_ratecard=ratecard,room_type_fee=room_fee,client__pk=client_id)
                                    
#                                         if client_roomtype_fees:
#                                             dat[f'{room_name}_{room_id}_prev_fee'] = client_roomtype_fees.Prev_fee
#                                             dat[f'{room_name}_{room_id}_curr_fee'] = client_roomtype_fees.fee
#                                         else:
#                                             dat[f'{room_name}_{room_id}_prev_fee'] = None
#                                             dat[f'{room_name}_{room_id}_curr_fee'] = None
#                             elif dat['RatecardType'] == 'Corporate':
#                                 if dat['isrowgroup']:
#                                     dat[f'{room_name}_{room_id}_prev_fee'] = None
#                                     dat[f'{room_name}_{room_id}_curr_fee'] = None
#                                 else:
#                                     if dat['Ratecardid']:
#                                         corporate_id=dat['Ratecardid']
#                                         corporate_roomtype_fees = CorporateRoomTypeFee.objects.get(doctor_ratecard=ratecard,room_type_fee=room_fee,corporate__pk=corporate_id)
                                        
#                                         if corporate_roomtype_fees:
#                                             dat[f'{room_name}_{room_id}_prev_fee'] = corporate_roomtype_fees.Prev_fee
#                                             dat[f'{room_name}_{room_id}_curr_fee'] = corporate_roomtype_fees.fee
#                                         else:
#                                             dat[f'{room_name}_{room_id}_prev_fee'] = None
#                                             dat[f'{room_name}_{room_id}_curr_fee'] = None
                                            
                                            
                                            
                                    
                                
                            
#                 return JsonResponse(doctor_data, safe=False)
            
#         except Exception as e:
#             return JsonResponse({'error': str(e)})




@csrf_exempt
@require_http_methods(['GET'])
def Overall_services_link(request):
    if request.method == 'GET':
        try:
            Doctor_ins = Doctor_Personal_Form_Detials.objects.all()
            doctors_data = []

            for doc in Doctor_ins:
                doc_specs = Doctor_ProfessForm_Detials.objects.get(Doctor_ID=doc.Doctor_ID)
                ratecard = Doctor_Ratecard_Master.objects.filter(Doctor_ID=doc).first()
                if not ratecard:
                    continue

                room_fees = RoomTypeFee.objects.filter(doctor_ratecard=ratecard)
                client_fees = ClientFee.objects.filter(doctor_ratecard=ratecard)
                corporate_fees = CorporateFee.objects.filter(doctor_ratecard=ratecard)
                insurance_fees = InsuranceFee.objects.filter(doctor_ratecard=ratecard)

                doctor_data = {
                    'id': doc.Doctor_ID,
                    'Service': "Consultation",
                    'doctor_name': f"{doc.Tittle}.{doc.First_Name} {doc.Middle_Name} {doc.Last_Name}",
                    'Specialization': doc_specs.Specialization.Speciality_Name,
                    'Status': 'Active' if doc.Status else 'Inactive',
                    'Roomtypes': [],
                    'Contribution': [
                        {
                            'id': 1,
                            'isrowgroup': False,
                            'RatecardType': 'Doctor_Contribution_OP',
                            'RatecardShow': 'Doctor Contribution_OP',
                            'RatecardName': None,
                            'doctor_ratecard_id': ratecard.RateCard_Id,
                            'doctor_contribution_OP': ratecard.Doctor_Contribution_OP,
                        },
                        {
                            'id': 2,
                            'isrowgroup': False,
                            'RatecardType': 'Doctor_Contribution_IP',
                            'RatecardShow': 'Doctor Contribution_IP',
                            'RatecardName': None,
                            'doctor_ratecard_id': ratecard.RateCard_Id,
                            'doctor_contribution_IP': ratecard.Doctor_Contribution_IP,
                        }
                    ],
                    'Ratecarddetails': {
                        'OP': [
                            {
                                'RatecardType': 'General',
                                'RatecardShow': 'General',
                                'RatecardName': None,
                                'consultation_Prev_fee': ratecard.OP_General_Prev_Consultation_Fee,
                                'consultation_curr_fee': ratecard.OP_General_Consultation_Fee,
                                'follow_up_Prev_fee': ratecard.OP_General_Prev_Follow_Up_Fee,
                                'follow_up_curr_fee': ratecard.OP_General_Follow_Up_Fee,
                                'emg_consultant_Prev_fee': ratecard.OP_General_Prev_Emg_Consulting_Fee,
                                'emg_consultant_curr_fee': ratecard.OP_General_Emg_Consulting_Fee,
                            },
                            {
                                'RatecardType': 'Special',
                                'RatecardShow': 'Special',
                                'RatecardName': None,
                                'consultation_Prev_fee': ratecard.OP_Special_Prev_Consultation_Fee,
                                'consultation_curr_fee': ratecard.OP_Special_Consultation_Fee,
                                'follow_up_Prev_fee': ratecard.OP_Special_Prev_Follow_Up_Fee,
                                'follow_up_curr_fee': ratecard.OP_Special_Follow_Up_Fee,
                                'emg_consultant_Prev_fee': ratecard.OP_Special_Prev_Emg_Consulting_Fee,
                                'emg_consultant_curr_fee': ratecard.OP_Special_Emg_Consulting_Fee,
                            }
                        ],
                        'IP': [
                            {
                                'RatecardType': 'General',
                                'RatecardShow': 'General',
                                'RatecardName': None,
                                'consultation_Prev_fee': ratecard.IP_General_Prev_Consultation_Fee,
                                'consultation_curr_fee': ratecard.IP_General_Consultation_Fee,
                                'follow_up_Prev_fee': ratecard.IP_General_Prev_Follow_Up_Fee,
                                'follow_up_curr_fee': ratecard.IP_General_Follow_Up_Fee,
                                'emg_consultant_Prev_fee': ratecard.IP_General_Prev_Emg_Consulting_Fee,
                                'emg_consultant_curr_fee': ratecard.IP_General_Emg_Consulting_Fee,
                            },
                            {
                                'RatecardType': 'Special',
                                'RatecardShow': 'Special',
                                'RatecardName': None,
                                'consultation_Prev_fee': ratecard.IP_Special_Prev_Consultation_Fee,
                                'consultation_curr_fee': ratecard.IP_Special_Consultation_Fee,
                                'follow_up_Prev_fee': ratecard.IP_Special_Prev_Follow_Up_Fee,
                                'follow_up_curr_fee': ratecard.IP_Special_Follow_Up_Fee,
                                'emg_consultant_Prev_fee': ratecard.IP_Special_Prev_Emg_Consulting_Fee,
                                'emg_consultant_curr_fee': ratecard.IP_Special_Emg_Consulting_Fee,
                            }
                        ]
                    },
                    'InsuranceDetails': [],
                    'ClientDetails': [],
                    'CorporateDetails': []
                }

                # Add insurance fees to InsuranceDetails
                for insurance_fee in insurance_fees:
                    doctor_data['InsuranceDetails'].append({
                        'id': len(doctor_data['InsuranceDetails']) + 1,
                        'RatecardName': insurance_fee.insurance.Insurance_Name,
                        'Ratecardid': insurance_fee.insurance.Insurance_Id,
                        'consultation_Prev_fee': insurance_fee.Prev_Consultation_Fee,
                        'consultation_curr_fee': insurance_fee.Consultation_Fee,
                        'follow_up_Prev_fee': insurance_fee.Prev_Follow_Up_Fee,
                        'follow_up_curr_fee': insurance_fee.Follow_Up_Fee,
                        'emg_consultant_Prev_fee': insurance_fee.Prev_Emg_Consulting_Fee,
                        'emg_consultant_curr_fee': insurance_fee.Emg_Consulting_Fee,
                    })

                # Add client fees to ClientDetails
                for client_fee in client_fees:
                    doctor_data['ClientDetails'].append({
                        'id': len(doctor_data['ClientDetails']) + 1,
                        'RatecardName': client_fee.client.Client_Name,
                        'Ratecardid': client_fee.client.Client_Id,
                        'consultation_Prev_fee': client_fee.Prev_Consultation_Fee,
                        'consultation_curr_fee': client_fee.Consultation_Fee,
                        'follow_up_Prev_fee': client_fee.Prev_Follow_Up_Fee,
                        'follow_up_curr_fee': client_fee.Follow_Up_Fee,
                        'emg_consultant_Prev_fee': client_fee.Prev_Emg_Consulting_Fee,
                        'emg_consultant_curr_fee': client_fee.Emg_Consulting_Fee,
                    })

                # Add corporate fees to CorporateDetails
                for corporate_fee in corporate_fees:
                    doctor_data['CorporateDetails'].append({
                        'id': len(doctor_data['CorporateDetails']) + 1,
                        'RatecardName': corporate_fee.corporate.Corporate_Name,
                        'Ratecardid': corporate_fee.corporate.Corporate_Id,
                        'consultation_Prev_fee': corporate_fee.Prev_Consultation_Fee,
                        'consultation_curr_fee': corporate_fee.Consultation_Fee,
                        'follow_up_Prev_fee': corporate_fee.Prev_Follow_Up_Fee,
                        'follow_up_curr_fee': corporate_fee.Follow_Up_Fee,
                        'emg_consultant_Prev_fee': corporate_fee.Prev_Emg_Consulting_Fee,
                        'emg_consultant_curr_fee': corporate_fee.Emg_Consulting_Fee,
                    })

                # Add room fees
                for room_fee in room_fees:
                    room_name = room_fee.room_type.Ward_Name.Ward_Name
                    room_id = room_fee.room_type.Room_Id
                    if {'id': room_id, 'name': room_name} not in doctor_data['Roomtypes']:
                        doctor_data['Roomtypes'].append({'id': room_id, 'name': room_name})

                doctors_data.append(doctor_data)

            return JsonResponse(doctors_data, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)})




@csrf_exempt
@require_http_methods(['POST'])
def UpdateRatecardDetails(request):
    try:
        # Parse the JSON payload from the request
        data = json.loads(request.body)
        print('daaaattaaa',data)
        
        for doctor in data:
            doctor_id = doctor.get("doctor_id")
            ratecard_details = doctor.get("Ratecarddetails", {})
            contributions = doctor.get("Contribution")
            insurance_details = doctor.get("InsuranceDetails", [])
            client_details = doctor.get("ClientDetails", [])
            corporate_details = doctor.get("CorporateDetails", [])

            # Update Ratecard Details for OP and IP
            for ratecard_type, ratecard_list in ratecard_details.items():
                for ratecard in ratecard_list:
                    ratecard_type_name = ratecard.get("RatecardType")
                    consultation_fee = ratecard.get("consultation_curr_fee")
                    follow_up_fee = ratecard.get("follow_up_curr_fee")
                    # emg_consultant_fee = ratecard.get("emg_consultant_curr_fee")

                    # Update based on RatecardType (General or Special) for both OP and IP
                    if ratecard_type == "OP":
                        if ratecard_type_name == "General":
                            print('22222222',consultation_fee)
                            print('22222222',follow_up_fee)
                            print('22222222',doctor_id)
                            Doctor_Ratecard_Master.objects.filter(Doctor_ID=doctor_id).update(
                                OP_General_Consultation_Fee=consultation_fee,
                                OP_General_Follow_Up_Fee=follow_up_fee,
                                # OP_General_Emg_Consultant_Fee=emg_consultant_fee
                            )
                            print('3333333')
                        elif ratecard_type_name == "Special":
                            Doctor_Ratecard_Master.objects.filter(Doctor_ID=doctor_id).update(
                                OP_Special_Consultation_Fee=consultation_fee,
                                OP_Special_Follow_Up_Fee=follow_up_fee,
                                # OP_Special_Emg_Consultant_Fee=emg_consultant_fee
                            )
                            print('4444444')
                    elif ratecard_type == "IP":
                        if ratecard_type_name == "General":
                            print('111111')
                            Doctor_Ratecard_Master.objects.filter(Doctor_ID__Doctor_ID=doctor_id).update(
                                IP_General_Consultation_Fee=consultation_fee,
                                IP_General_Follow_Up_Fee=follow_up_fee,
                                # IP_General_Emg_Consultant_Fee=emg_consultant_fee
                            )
                        elif ratecard_type_name == "Special":
                            Doctor_Ratecard_Master.objects.filter(Doctor_ID=doctor_id).update(
                                IP_Special_Consultation_Fee=consultation_fee,
                                IP_Special_Follow_Up_Fee=follow_up_fee,
                                # IP_Special_Emg_Consultant_Fee=emg_consultant_fee
                            )

                op_contribution = contributions.get("doctor_contribution_OP")
                ip_contribution = contributions.get("doctor_contribution_IP")
                print('op_contribution',op_contribution)
                print('ip_contribution',ip_contribution)
                # Update contribution values for OP and IP
                Doctor_Ratecard_Master.objects.filter(Doctor_ID=doctor_id).update(
                    Doctor_Contribution_OP=op_contribution,
                    Doctor_Contribution_IP=ip_contribution
                )

            # Update Insurance Details
            for insurance in insurance_details:
                ratecard_id = insurance.get("RatecardName")
                consultation_fee = insurance.get("consultation_curr_fee")
                # follow_up_fee = insurance.get("follow_up_curr_fee")
                # emg_consultant_fee = insurance.get("emg_consultant_curr_fee")
                print('ratecard_id',ratecard_id)
                # Update the insurance fee record
                InsuranceFee.objects.filter(insurance__Insurance_Name=ratecard_id, doctor_ratecard__Doctor_ID=doctor_id).update(
                    Consultation_Fee=consultation_fee,
                    # Follow_Up_Fee=follow_up_fee,
                    # Emg_Consultant_Fee=emg_consultant_fee
                )

            # Update Client Details
            for client in client_details:
                ratecard_id = client.get("Ratecardid")
                consultation_fee = client.get("consultation_curr_fee")
                # follow_up_fee = client.get("follow_up_curr_fee")
                # emg_consultant_fee = client.get("emg_consultant_curr_fee")

                # Update the client fee record
                ClientFee.objects.filter(client__Client_Name=ratecard_id, doctor_ratecard__Doctor_ID=doctor_id).update(
                    Consultation_Fee=consultation_fee,
                    # Follow_Up_Fee=follow_up_fee,
                    # Emg_Consultant_Fee=emg_consultant_fee
                )

            # Update Corporate Details
            for corporate in corporate_details:
                ratecard_id = corporate.get("Ratecardid")
                consultation_fee = corporate.get("consultation_curr_fee")
                # follow_up_fee = corporate.get("follow_up_curr_fee")
                # emg_consultant_fee = corporate.get("emg_consultant_curr_fee")

                # Update the corporate fee record
                CorporateFee.objects.filter(corporate__Corporate_Name=ratecard_id, doctor_ratecard__Doctor_ID=doctor_id).update(
                    Consultation_Fee=consultation_fee,
                    # Follow_Up_Fee=follow_up_fee,
                    # Emg_Consultant_Fee=emg_consultant_fee
                )

        return JsonResponse({"success": "Ratecard details updated successfully."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@csrf_exempt
@require_http_methods(['GET'])
def Get_RoomDetails_Ratecard(request):
    if request.method == 'GET':
        try:
            room_instance = RoomTypeFee.objects.select_related('room_type', 'room_type__Floor_Name', 'room_type__Ward_Name').all()
            insurance_fees = InsuranceRoomTypeFee.objects.select_related('room_type_fee').all()
            client_fees = ClientRoomTypeFee.objects.select_related('room_type_fee').all()
            corporate_fees = CorporateRoomTypeFee.objects.select_related('room_type_fee').all()

            floors_data = {}

            for room in room_instance:
                floor_name = room.room_type.Floor_Name.Floor_Name
                ward_name = room.room_type.Ward_Name.Ward_Name
                category_type = room.room_type.isAC

                if floor_name not in floors_data:
                    floors_data[floor_name] = {}

                if ward_name not in floors_data[floor_name]:
                    floors_data[floor_name][ward_name] = {
                        'CategoryType': category_type,
                        'Ratecarddetails': {
                            'General': [],
                            'Special': []
                        },
                        'InsuranceDetails': [],
                        'ClientDetails': [],
                        'CorporateDetails': [],
                        'InsuranceIds': set(),  # To track unique Insurance IDs
                        'ClientIds': set(),     # To track unique Client IDs
                        'CorporateIds': set()   # To track unique Corporate IDs
                    }

                floors_data[floor_name][ward_name]['Ratecarddetails']['General'] = [
                    {
                        'RatecardType': 'RoomCharges',
                        'consultation_curr_fee': room.General_fee
                    },
                    {
                        'RatecardType': 'DoctorCharges',
                        'consultation_curr_fee': room.room_type.Doctorcharges
                    },
                    {
                        'RatecardType': 'NurseCharges',
                        'consultation_curr_fee': room.room_type.Nursecharges
                    }
                ]
                floors_data[floor_name][ward_name]['Ratecarddetails']['Special'] = [
                    {
                        'RatecardType': 'RoomCharges',
                        'consultation_curr_fee': room.Special_fee
                    },
                    {
                        'RatecardType': 'DoctorCharges',
                        'consultation_curr_fee': room.room_type.Doctorcharges
                    },
                    {
                        'RatecardType': 'NurseCharges',
                        'consultation_curr_fee': room.room_type.Nursecharges
                    }
                ]

            # Add Insurance, Client, and Corporate details, avoiding duplicates
            for ins_fee in insurance_fees:
                floor_name = ins_fee.room_type_fee.room_type.Floor_Name.Floor_Name
                ward_name = ins_fee.room_type_fee.room_type.Ward_Name.Ward_Name
                if floor_name in floors_data and ward_name in floors_data[floor_name]:
                    ward_data = floors_data[floor_name][ward_name]
                    if ins_fee.insurance.Insurance_Id not in ward_data['InsuranceIds']:
                        ward_data['InsuranceDetails'].append({
                            'id': len(ward_data['InsuranceDetails']) + 1,
                            'RatecardName': ins_fee.insurance.Insurance_Name,
                            'Ratecardid': ins_fee.insurance.Insurance_Id,
                            'Fee': ins_fee.fee
                        })
                        ward_data['InsuranceIds'].add(ins_fee.insurance.Insurance_Id)

            for client_fee in client_fees:
                floor_name = client_fee.room_type_fee.room_type.Floor_Name.Floor_Name
                ward_name = client_fee.room_type_fee.room_type.Ward_Name.Ward_Name
                if floor_name in floors_data and ward_name in floors_data[floor_name]:
                    ward_data = floors_data[floor_name][ward_name]
                    if client_fee.client.Client_Id not in ward_data['ClientIds']:
                        ward_data['ClientDetails'].append({
                            'id': len(ward_data['ClientDetails']) + 1,
                            'RatecardName': client_fee.client.Client_Name,
                            'Ratecardid': client_fee.client.Client_Id,
                            'Fee': client_fee.fee
                        })
                        ward_data['ClientIds'].add(client_fee.client.Client_Id)

            for corporate_fee in corporate_fees:
                floor_name = corporate_fee.room_type_fee.room_type.Floor_Name.Floor_Name
                ward_name = corporate_fee.room_type_fee.room_type.Ward_Name.Ward_Name
                if floor_name in floors_data and ward_name in floors_data[floor_name]:
                    ward_data = floors_data[floor_name][ward_name]
                    if corporate_fee.corporate.Corporate_Id not in ward_data['CorporateIds']:
                        ward_data['CorporateDetails'].append({
                            'id': len(ward_data['CorporateDetails']) + 1,
                            'RatecardName': corporate_fee.corporate.Corporate_Name,
                            'Ratecardid': corporate_fee.corporate.Corporate_Id,
                            'Fee': corporate_fee.fee
                        })
                        ward_data['CorporateIds'].add(corporate_fee.corporate.Corporate_Id)

            # Convert the floors_data dictionary to a list for JSON response
            response_data = []
            for floor_name, wards in floors_data.items():
                floor_info = {
                    'FloorName': floor_name,
                    'ServiceName' : 'RoomCharges',
                    'Wards': []
                }
                for ward_name, ward_data in wards.items():
                    # Remove ID tracking sets before returning
                    del ward_data['InsuranceIds']
                    del ward_data['ClientIds']
                    del ward_data['CorporateIds']
                    floor_info['Wards'].append({
                        'WardName': ward_name,
                        **ward_data
                    })
                response_data.append(floor_info)

            return JsonResponse(response_data, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)})


