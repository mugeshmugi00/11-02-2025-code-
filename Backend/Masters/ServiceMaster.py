from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from .models import *
from Frontoffice.models import *
from django.db.models import Q

@csrf_exempt
@require_http_methods(['GET'])
def Services_List(request):

    if request.method == "GET":

         try:
             
            Services_data_list = []
            consultaion_ins = Doctor_Ratecard_Master.objects.all()
            for datas in consultaion_ins:
                
                Doctor_speciality_ins = Doctor_ProfessForm_Detials.objects.get(Doctor_ID=datas.Doctor_ID)  
                speciality_ins = Speciality_Detials.objects.get(Speciality_Id=Doctor_speciality_ins.Specialization.Speciality_Id)
                doctor_ins = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=datas.Doctor_ID.Doctor_ID)
                
                service_data = {
                     
                    'pk': datas.pk,
                    'service_category' : 'Dr.Consultation',
                    'service_subcategory' : f'{datas.Doctor_ID.Doctor_ID} - Dr.{doctor_ins.First_Name}{doctor_ins.Middle_Name}({speciality_ins.Speciality_Name})',     
                }
                Services_data_list.append(service_data)
            print('0000000')
            labtest_ins = Testmaster_Cost_List.objects.all()
            for datas in labtest_ins:
              
                service_data = {
                    'pk' : datas.pk,
                    'service_category' : 'Lab',
                    'service_subcategory': f'{datas.Test_Code.Test_Code} - {datas.Test_Code.Test_Name}' if datas.Test_Code else f'{datas.Group_Code.Group_Code}-f{datas.Group_Code.Group_Name}',
                }
                Services_data_list.append(service_data)
            # group_ins = Group_Master.objects.all()
            # print('111111111')
            # for datas in labtest_ins:
            #     service_data = {
            #         'pk': datas.pk,
            #         'service_category': 'Lab',
            #         'service_subcategory': f'{datas.Group_Code.Group_Code}-{datas.Group_Code.Group_Name}' if datas.Group_Code else None,
            #     }
            #     Services_data_list.append(service_data)
            print('22222222222')
            Radiology_ins = TestName_Details.objects.all()
            for datas in Radiology_ins:
                
                service_data = {
                    'pk':datas.pk,
                    'service_category' : 'Radiology',
                    'service_subcategory':f'{datas.Test_Code} - {datas.Test_Name}',
                }
                Services_data_list.append(service_data)
            Room_ins = Room_Master_Detials.objects.all()
            for datas in Room_ins:
                
                ward_ins = WardType_Master_Detials.objects.get(pk=datas.Ward_Name.Room_Id)
                service_data = {
                    
                    'pk':datas.pk,
                    'service_subcategory':f'{datas.Room_No} - {datas.Bed_No} -{ward_ins.Ward_Name}'
                    
                }
                Services_data_list.append(service_data)
            service_ins = Service_Master_Details.objects.all()
            for datas in service_ins:
                service_data = {
                    
                    'pk' : datas.pk,
                    'service_category' : 'general services',
                    'service_subcategory' : datas.Service_Name
                }
                Services_data_list.append(service_data)
                
            return JsonResponse(Services_data_list,safe=False)

         except Exception as e:
            return JsonResponse({"error": str(e)})
         
         
@csrf_exempt
@require_http_methods(['POST', 'GET', 'OPTIONS'])
def service_map_details(request):

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("data", data)

            category = data.get('Categoryid')
            subcategory = data.get('Subcategorypk')

            category_ins = Service_Category_Masters.objects.get(Serviceid=category)
            service_name = category_ins.ServiceCategory
            print(service_name)

            if service_name == 'CONSULTATION':
                 print('consultaion')
                 content_type = ContentType.objects.get_for_model(Doctor_Ratecard_Master)
                 print(content_type)
                 identification_object = Doctor_Ratecard_Master.objects.get(pk=subcategory)
                 print(identification_object,'kjhgf')
                 print(type(identification_object)) 
                

            elif service_name == 'LAB':
                 print('LAB')
                 content_type = ContentType.objects.get_for_model(Testmaster_Cost_List)
                 identification_object = Testmaster_Cost_List.objects.get(pk=subcategory)
               
        
            elif service_name == 'RADIOLOGY':
                
                 content_type = ContentType.objects.get_for_model(TestName_Details)
                 identification_object = TestName_Details.objects.get(pk=subcategory)
               

            elif service_name == 'ROOMSERVICES':
                 print('ROOMSERVICES')
                 content_type = ContentType.objects.get_for_model(Room_Master_Detials)
                 #identification_object = RoomTypeFee.objects.get(pk=subcategory)
                 identification_object = Room_Master_Detials.objects.get(pk=subcategory)
                  
            else :
                print('General Services')
                content_type = ContentType.objects.get_for_model(Service_Master_Details)
                identification_object = Service_Master_Details.objects.get(pk=subcategory)
               
        
            try:
                Services_Group_Details.objects.create(

                    content_type = content_type,
                    object_id = subcategory,
                    service_category = category_ins,
                    service_sub_category = identification_object,

                )
            except Exception as e:
                print("Error occurred:", e)

            

            return JsonResponse({'success':'Service Subcategory Added successfully'})

        except Exception as e:
            # Handle and return the error message in the response
            return JsonResponse({'error': str(e)})

@csrf_exempt
@require_http_methods(['POST', 'GET', 'OPTIONS'])
def service_added_details(request):

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("data", data)

            category = data.get('Categoryid')
            subcategory = data.get('Subcategorypk')
            patient_category = data.get('PatientCategory')
            patient_subCat = data.get('PatientSubCat')
            registrationid = data.get('RegistrationId')
            units = int(data.get('Units', 1))

            category_ins = Service_Category_Masters.objects.get(Serviceid=category)
            service_name = category_ins.ServiceCategory
            rate = 0.00
            print(service_name)
            patient_ins = Patient_IP_Registration_Detials.objects.get(Registration_Id = registrationid)


            if service_name == 'CONSULTATION':
                print('consultaion')
                content_type = ContentType.objects.get_for_model(Doctor_Ratecard_Master)
                print(content_type)
                identification_object = Doctor_Ratecard_Master.objects.get(pk=subcategory)
                if patient_category == 'General' or 'GENERAL':
                    rate = identification_object.IP_General_Consultation_Fee
                elif patient_category == 'Insurance' or 'INSURANCE':
                    insurance_ins = InsuranceFee.objects.get(insurance = patient_subCat)
                    rate = insurance_ins.Consultation_Fee
                elif patient_category == 'Client' or 'CLIENT':
                    insurance_ins = ClientFee.objects.get(client = patient_subCat)
                    rate = insurance_ins.Consultation_Fee
                print(identification_object,'kjhgf')
                print(type(identification_object)) 
                

            elif service_name == 'LAB':
                print('LAB')
                content_type = ContentType.objects.get_for_model(Testmaster_Cost_List)
                identification_object = Testmaster_Cost_List.objects.get(pk=subcategory)
                rate = identification_object.Basic
                
               
        
            elif service_name == 'RADIOLOGY':
                
                content_type = ContentType.objects.get_for_model(TestName_Details)
                identification_object = TestName_Details.objects.get(pk=subcategory)
                rate = identification_object.Amount
               

            elif service_name == 'ROOMSERVICES':
                print('ROOMSERVICES')
                content_type = ContentType.objects.get_for_model(Room_Master_Detials)
                #identification_object = RoomTypeFee.objects.get(pk=subcategory)
                identification_object = Room_Master_Detials.objects.get(pk=subcategory)
                rate = 0


                  
            elif  service_name == 'GENERALSERVICES':
                print('GeneralServices')
                content_type = ContentType.objects.get_for_model(Service_Master_Details)
                print('conn',content_type)
                # identification_object = Service_Master_Details.objects.get(pk=subcategory)
                # rate = identification_object.IP_Amount if identification_object.IP_Amount else identification_object.OP_IP_Amount
                try:
                    subcategory = int(data.get('Subcategorypk'))
                    print(f"Subcategory value: {subcategory} (Type: {type(subcategory)})")
                    identification_object = Service_Master_Details.objects.get(pk=subcategory)
                    rate = identification_object.Amount if identification_object.Amount else identification_object.Amount
                    print('identttt',identification_object)
                except ValueError:  
                    return JsonResponse({'error': 'Invalid subcategory ID'})
                except Service_Master_Details.DoesNotExist:
                    return JsonResponse({'error': 'Service Subcategory not found'})
            
            total_rate = rate * units

            try:
                Services_SubCat_Requests_Details.objects.create(
                    content_type = content_type,
                    object_id = subcategory,
                    Registration_Id=patient_ins,
                    service_category = category_ins,
                    service_sub_category = identification_object,
                    rate =total_rate,
                    units = units,
                )
            except Exception as e:
                print("Error occurred:", e)

            

            return JsonResponse({'success':'Service Subcategory Added successfully'})

        except Exception as e:
            # Handle and return the error message in the response
            return JsonResponse({'error': str(e)})
    elif request.method == 'GET':

        try:
            registrationid = request.GET.get('RegistrationId')
            services_ins = Services_SubCat_Requests_Details.objects.filter(Registration_Id = registrationid)
            print("services_ins12",services_ins)
            services_list = []
            for datas in services_ins:

                serviceid = datas.service_category_id
                category_ins = Service_Category_Masters.objects.get(pk=serviceid)
                print("category_ins",category_ins)
                

                if category_ins.ServiceCategory == 'CONSULTATION':

                    consultaion_ins = Doctor_Ratecard_Master.objects.get(pk=datas.object_id)
                    
                    Doctor_speciality_ins = Doctor_ProfessForm_Detials.objects.get(Doctor_ID=consultaion_ins.Doctor_ID)  
                    speciality_ins = Speciality_Detials.objects.get(Speciality_Id=Doctor_speciality_ins.Specialization.Speciality_Id)
                    doctor_ins = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=consultaion_ins.Doctor_ID.Doctor_ID)
                    data_list = {
                             'id':datas.pk,
                             'category': category_ins.ServiceCategory,
                             'service_subcategory' : f'{consultaion_ins.Doctor_ID.Doctor_ID} - Dr.{doctor_ins.First_Name}{doctor_ins.Middle_Name}({speciality_ins.Speciality_Name})',
                             'rate':datas.rate,
                             'Units':datas.units,
                        }
                    services_list.append(data_list)

                elif category_ins.ServiceCategory == 'LAB':

                

                    labtest_ins = Testmaster_Cost_List.objects.get(pk=datas.object_id)
                    
                    data_list = {
                             'id':datas.pk,
                             'category': category_ins.ServiceCategory,
                             'service_subcategory': f'{labtest_ins.Test_Code.Test_Code} - {labtest_ins.Test_Code.Test_Name}' if labtest_ins.Test_Code else labtest_ins.Group_Code.Group_Name,
                             'rate':datas.rate,
                             'Units':datas.units,
                        }
                    services_list.append(data_list)

                elif category_ins.ServiceCategory == 'RADIOLOGY':

                

                    Radiology_ins = TestName_Details.objects.get(pk=datas.object_id)
                    
                    data_list = {
                             'id':datas.pk,
                             'category': category_ins.ServiceCategory,
                             'service_subcategory':f'{Radiology_ins.Test_Code} - {Radiology_ins.Test_Name}',
                             'rate':datas.rate,
                             'Units':datas.units,
                        }
                    services_list.append(data_list)

                elif category_ins.ServiceCategory == 'ROOMSERVICES':

               
                    Room_ins = Room_Master_Detials.objects.get(pk=datas.object_id)
                    ward_ins = WardType_Master_Detials.objects.get(pk=Room_ins.Ward_Name.Room_Id)        
                    data_list = {
                            'id':datas.pk,
                            'category': category_ins.ServiceCategory,
                            'service_subcategory' : f'{Room_ins.Room_No} - {Room_ins.Bed_No} -{ward_ins.Ward_Name}',         
                            'rate':datas.rate,
                            'Units':datas.units,
                    }
                    services_list.append(data_list)

                elif category_ins.ServiceCategory == 'GENERALSERVICES':
                    print("qw")
                    

                    General_services_ins  = Service_Master_Details.objects.get(pk=datas.object_id)
                    print("General_services_ins23",General_services_ins)
                    
                    data_list = {
                             'id':datas.pk,
                             'category': category_ins.ServiceCategory,
                             'service_subcategory':General_services_ins.Service_Name,
                             'rate':datas.rate,
                             'Units':datas.units,
                        }
                    services_list.append(data_list)
                
            for idx, services in enumerate(services_list, start=1):
                      services["Sno"] = idx 

            return JsonResponse(services_list,safe=False)

        except Exception as e:
            # Handle and return the error message in the response
            return JsonResponse({'error': str(e)})



@csrf_exempt
def services_Group_list_details(request):
    if request.method == "GET":

        try:
            services_ins = Services_Group_Details.objects.all()
            
            services_list = []

            for datas in services_ins:

                data_list = {

                    "id" : datas.pk,
                    "object_id" : datas.object_id,
                    "service_category_id" : datas.service_category_id,
                    "service_name" : datas.service_category.ServiceCategory
                }

                services_list.append(data_list)
            seen_service_categories = set()
            unique_data = []
            for entry in services_list:
                if entry["service_category_id"] not in seen_service_categories:
                    seen_service_categories.add(entry["service_category_id"])
                    unique_data.append(entry)
            print(unique_data)
            return JsonResponse(unique_data,safe=False)
           # return JsonResponse(services_list,safe=False)
        except Exception as e:
            return JsonResponse({"error":str(e)})

@csrf_exempt
def services_Subcategory_details_by_category(request):
 
    if request.method == 'GET':
        try:
            ServiceCategory = request.GET.get('ServiceCategory')
            
            category_ins = Service_Category_Masters.objects.get(Serviceid=ServiceCategory)
            services_ins = Services_Group_Details.objects.filter(service_category_id=ServiceCategory)
            Services_List = []

            if category_ins.ServiceCategory == 'CONSULTATION':


                for datas in services_ins:

                    consultaion_ins = Doctor_Ratecard_Master.objects.get(pk=datas.object_id)
                    
                    Doctor_speciality_ins = Doctor_ProfessForm_Detials.objects.get(Doctor_ID=consultaion_ins.Doctor_ID)  
                    speciality_ins = Speciality_Detials.objects.get(Speciality_Id=Doctor_speciality_ins.Specialization.Speciality_Id)
                    doctor_ins = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=consultaion_ins.Doctor_ID.Doctor_ID)
                    data_list = {
                             'pk': datas.object_id,
                             'service_subcategory' : f'{consultaion_ins.Doctor_ID.Doctor_ID} - Dr.{doctor_ins.First_Name}{doctor_ins.Middle_Name}({speciality_ins.Speciality_Name})',
                        }
                    Services_List.append(data_list)
                   
            elif category_ins.ServiceCategory == 'LAB':

                for datas in services_ins:

                    labtest_ins = Testmaster_Cost_List.objects.get(pk=datas.object_id)
                    
                    data_list = {
                             'pk': datas.object_id,
                             'service_subcategory': f'{labtest_ins.Test_Code.Test_Code} - {labtest_ins.Test_Code.Test_Name}' if labtest_ins.Test_Code else labtest_ins.Group_Code.Group_Name,
                        }
                    Services_List.append(data_list)

            elif category_ins.ServiceCategory == 'RADIOLOGY':

                for datas in services_ins:

                    Radiology_ins = TestName_Details.objects.get(pk=datas.object_id)
                    
                    data_list = {
                             'pk': datas.object_id,
                             'service_subcategory':f'{Radiology_ins.Test_Code} - {Radiology_ins.Test_Name}',
                        }
                    Services_List.append(data_list)

            elif category_ins.ServiceCategory == 'ROOMSERVICES':

                for datas in services_ins:

                #     Room_ins = RoomTypeFee.objects.get(pk=datas.object_id)
                #    # for roomdata in Room_ins:
                        
                #     room_no_ins = Room_Master_Detials.objects.filter(Ward_Name_id=Room_ins.room_type_id)
                #     for rni in room_no_ins:
                #             print(rni.Room_No)
                #             print(rni.Bed_No)    

                    Room_ins = Room_Master_Detials.objects.get(pk=datas.object_id)
                    ward_ins = WardType_Master_Detials.objects.get(pk=Room_ins.Ward_Name.Room_Id)        
                    data_list = {
                            'pk':datas.object_id,
                            'pk1':datas.object_id,
                            'Roomid':Room_ins.Room_Id,
                            'service_subcategory' : f'{Room_ins.Room_No} - {Room_ins.Bed_No} -{ward_ins.Ward_Name}'         
                    }
                    Services_List.append(data_list)
  
            elif category_ins.ServiceCategory == 'GENERALSERVICES':

                for datas in services_ins:

                    General_services_ins = Service_Master_Details.objects.get(pk=datas.object_id)
                    
                    data_list = {
                             'pk': datas.object_id,
                             'pk1':datas.object_id,
                             'service_subcategory':General_services_ins.Service_Name
                        }
                    Services_List.append(data_list)

            return JsonResponse(Services_List, safe=False)

        except Exception as e:
                return JsonResponse({"error":str(e)})

@csrf_exempt
def services_Subcategory_details_by_Patient_category(request):
 
    if request.method == 'GET':
        try:
            ServiceCategory = request.GET.get('ServiceCategory') 
            ServicesubCategory = request.GET.get('ServicesubCategory')
            Patientcategory = request.GET.get('Patientcategory') # general insurance
            patientid = request.GET.get('patientid') # op ip

            op_patient = None
            ip_patient = None
            print('111111',ServiceCategory,ServicesubCategory,Patientcategory,patientid)
           
           # op_patient = Patient_Appointment_Registration_Detials.objects.get(PatientId_id = patientid)
            try:
                op_patient = Patient_Appointment_Registration_Detials.objects.get(PatientId_id = patientid)
                    
            except Patient_Appointment_Registration_Detials.DoesNotExist:
                print("OP Patient not found")
            
            try:
                ip_patient = Patient_IP_Registration_Detials.objects.get(PatientId_id = patientid)
            except Patient_IP_Registration_Detials.DoesNotExist:
                print("IP patient not found")
            
            category_ins = Service_Category_Masters.objects.get(Serviceid=ServiceCategory)
            
            services_ins = Services_Group_Details.objects.filter(pk=ServicesubCategory)
            
            Services_List = []

            if category_ins.ServiceCategory == 'CONSULTATION':

                

                if Patientcategory == 'General' and op_patient:

                    for datas in services_ins:

                        consultaion_ins = Doctor_Ratecard_Master.objects.get(pk=datas.object_id)
                        Doctor_speciality_ins = Doctor_ProfessForm_Detials.objects.get(Doctor_ID=consultaion_ins.Doctor_ID)  
                        speciality_ins = Speciality_Detials.objects.get(Speciality_Id=Doctor_speciality_ins.Specialization.Speciality_Id)
                        doctor_ins = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=consultaion_ins.Doctor_ID.Doctor_ID)
                        data_list = {
                                'pk': datas.pk,
                                'service_subcategory' : f'{consultaion_ins.Doctor_ID.Doctor_ID} - Dr.{doctor_ins.First_Name}{doctor_ins.Middle_Name}({speciality_ins.Speciality_Name})',
                                'amt' : consultaion_ins.General_Consultation_Fee
                            }
                        Services_List.append(data_list)
                
                elif Patientcategory == 'General' and ip_patient:

                    for datas in services_ins:

                        consultaion_ins = Doctor_Ratecard_Master.objects.get(pk=datas.object_id)

                        
                        Doctor_speciality_ins = Doctor_ProfessForm_Detials.objects.get(Doctor_ID=consultaion_ins.Doctor_ID)  
                        speciality_ins = Speciality_Detials.objects.get(Speciality_Id=Doctor_speciality_ins.Specialization.Speciality_Id)
                        doctor_ins = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=consultaion_ins.Doctor_ID.Doctor_ID)
                        data_list = {
                            'pk': datas.pk,
                            'service_subcategory' : f'{consultaion_ins.Doctor_ID.Doctor_ID} - Dr.{doctor_ins.First_Name}{doctor_ins.Middle_Name}({speciality_ins.Speciality_Name})',
                            'amt' : consultaion_ins.General_Consultation_Fee
                        }
                        Services_List.append(data_list)
                   
                elif Patientcategory == 'Insurance' and op_patient :

                    for datas in services_ins:

                        consultaion_ins = Doctor_Ratecard_Master.objects.get(pk=datas.object_id)
                        Doctor_speciality_ins = Doctor_ProfessForm_Detials.objects.get(Doctor_ID=consultaion_ins.Doctor_ID)  
                        speciality_ins = Speciality_Detials.objects.get(Speciality_Id=Doctor_speciality_ins.Specialization.Speciality_Id)
                        doctor_ins = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=consultaion_ins.Doctor_ID.Doctor_ID)       
                        insurance_ins = Insurance_Master_Detials.objects.get(pk=op_patient.InsuranceName_id)
                        insurance_fee_ins = InsuranceFee.objects.get(doctor_ratecard_id=consultaion_ins.pk,insurance_id=insurance_ins.pk)

                        data_list = {
                            'pk': datas.pk,
                            'service_subcategory' : f'{consultaion_ins.Doctor_ID.Doctor_ID} - Dr.{doctor_ins.First_Name}{doctor_ins.Middle_Name}({speciality_ins.Speciality_Name})',
                            'insurancename': insurance_ins.Insurance_Name,
                            'amt' : insurance_fee_ins.Consultation_Fee
                        }
                        Services_List.append(data_list)

                elif Patientcategory == 'Insurance' and ip_patient :
                        
                        for datas in services_ins:

                            consultaion_ins = Doctor_Ratecard_Master.objects.get(pk=datas.object_id)
                            Doctor_speciality_ins = Doctor_ProfessForm_Detials.objects.get(Doctor_ID=consultaion_ins.Doctor_ID)  
                            speciality_ins = Speciality_Detials.objects.get(Speciality_Id=Doctor_speciality_ins.Specialization.Speciality_Id)
                            doctor_ins = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=consultaion_ins.Doctor_ID.Doctor_ID)
                            insurance_ins = Insurance_Master_Detials.objects.get(pk=ip_patient.InsuranceName_id)
                            insurance_fee_ins = InsuranceFee.objects.get(doctor_ratecard_id=consultaion_ins.pk,insurance_id=insurance_ins.pk)

                            data_list = {
                                'pk': datas.pk,
                                'service_subcategory' : f'{consultaion_ins.Doctor_ID.Doctor_ID} - Dr.{doctor_ins.First_Name}{doctor_ins.Middle_Name}({speciality_ins.Speciality_Name})',
                                'insurancename': insurance_ins.Insurance_Name,
                                'amt' : insurance_fee_ins.Consultation_Fee
                            }
                            Services_List.append(data_list)

                elif Patientcategory == 'Client' and op_patient:

                    for datas in services_ins:

                        consultaion_ins = Doctor_Ratecard_Master.objects.get(pk=datas.object_id)

                        Doctor_speciality_ins = Doctor_ProfessForm_Detials.objects.get(Doctor_ID=consultaion_ins.Doctor_ID)  
                        speciality_ins = Speciality_Detials.objects.get(Speciality_Id=Doctor_speciality_ins.Specialization.Speciality_Id)
                        doctor_ins = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=consultaion_ins.Doctor_ID.Doctor_ID)
                        Client_ins = Client_Master_Detials.objects.get(pk=op_patient.ClientName_id)
                        client_fee_ins = ClientFee.objects.get(doctor_ratecard_id=consultaion_ins.pk,client_id=Client_ins.pk)

                        data_list = {
                            'pk': datas.pk,
                            'service_subcategory' : f'{consultaion_ins.Doctor_ID.Doctor_ID} - Dr.{doctor_ins.First_Name}{doctor_ins.Middle_Name}({speciality_ins.Speciality_Name})',
                            'clientname': Client_ins.Client_Name,
                            'amt' : client_fee_ins.Consultation_Fee,
                        }
                        Services_List.append(data_list)

                elif Patientcategory == 'Client' and ip_patient:
                        
                        for datas in services_ins:

                            consultaion_ins = Doctor_Ratecard_Master.objects.get(pk=datas.object_id)
                            Doctor_speciality_ins = Doctor_ProfessForm_Detials.objects.get(Doctor_ID=consultaion_ins.Doctor_ID)  
                            speciality_ins = Speciality_Detials.objects.get(Speciality_Id=Doctor_speciality_ins.Specialization.Speciality_Id)
                            doctor_ins = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=consultaion_ins.Doctor_ID.Doctor_ID)
                            Client_ins = Client_Master_Detials.objects.get(pk=ip_patient.ClientName_id)
                            client_fee_ins = ClientFee.objects.get(doctor_ratecard_id=consultaion_ins.pk,client_id=Client_ins.pk)

                            data_list = {
                            'pk': datas.pk,
                            'service_subcategory' : f'{consultaion_ins.Doctor_ID.Doctor_ID} - Dr.{doctor_ins.First_Name}{doctor_ins.Middle_Name}({speciality_ins.Speciality_Name})',
                            'clientname': Client_ins.Client_Name,
                            'amt' : client_fee_ins.Consultation_Fee,
                            }
                            Services_List.append(data_list)
 
                elif Patientcategory == 'Corporate' and op_patient:

                    for datas in services_ins:

                        consultaion_ins = Doctor_Ratecard_Master.objects.get(pk=datas.object_id)
                        Doctor_speciality_ins = Doctor_ProfessForm_Detials.objects.get(Doctor_ID=consultaion_ins.Doctor_ID)  
                        speciality_ins = Speciality_Detials.objects.get(Speciality_Id=Doctor_speciality_ins.Specialization.Speciality_Id)
                        doctor_ins = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=consultaion_ins.Doctor_ID.Doctor_ID)
                        corporate_ins = Corporate_Master_Detials.objects.get(pk=op_patient.CorporateName_id)
                        corporate_fee_ins = CorporateFee.objects.get(doctor_ratecard_id=consultaion_ins.pk,corporate_id=corporate_ins.Corporate_Id)

                        data_list = {
                            'pk': datas.pk,
                            'service_subcategory' : f'{consultaion_ins.Doctor_ID.Doctor_ID} - Dr.{doctor_ins.First_Name}{doctor_ins.Middle_Name}({speciality_ins.Speciality_Name})',
                            'corporatename': corporate_ins.Corporate_Name,
                            'amt' : corporate_fee_ins.Consultation_Fee,
                        }
                        Services_List.append(data_list)

                elif Patientcategory == 'Corporate' and ip_patient:

                    for datas in services_ins:

                        consultaion_ins = Doctor_Ratecard_Master.objects.get(pk=datas.object_id)
                        Doctor_speciality_ins = Doctor_ProfessForm_Detials.objects.get(Doctor_ID=consultaion_ins.Doctor_ID)  
                        speciality_ins = Speciality_Detials.objects.get(Speciality_Id=Doctor_speciality_ins.Specialization.Speciality_Id)
                        doctor_ins = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=consultaion_ins.Doctor_ID.Doctor_ID)
                        corporate_ins = Corporate_Master_Detials.objects.get(pk=ip_patient.CorporateName_id)
                        corporate_fee_ins = CorporateFee.objects.get(doctor_ratecard_id=consultaion_ins.pk,corporate_id=corporate_ins.Corporate_Id)

                        data_list = {
                            'pk': datas.pk,
                            'service_subcategory' : f'{consultaion_ins.Doctor_ID.Doctor_ID} - Dr.{doctor_ins.First_Name}{doctor_ins.Middle_Name}({speciality_ins.Speciality_Name})',
                            'corporatename': corporate_ins.Corporate_Name,
                            'amt' : corporate_fee_ins.Consultation_Fee,
                        }
                        Services_List.append(data_list)
                    
            elif category_ins.ServiceCategory == 'LAB':

                for datas in services_ins:
                    
                    labtest_ins = Testmaster_Cost_List.objects.get(Test_Id=datas.object_id)
                    
                    
                    data_list = {
                            'pk': datas.pk,
                            'service_subcategory': f'{labtest_ins.Test_Code.Test_Code} - {labtest_ins.Test_Code.Test_Name}',
                            'amt' : labtest_ins.Basic
                    }
                    Services_List.append(data_list)

            elif category_ins.ServiceCategory == 'RADIOLOGY':

                for datas in services_ins:

                    Radiology_ins = TestName_Details.objects.get(pk=datas.object_id)
                   
                    
                    data_list = {
                            'pk': datas.pk,
                            'service_subcategory':f'{Radiology_ins.Test_Code} - {Radiology_ins.Test_Name}',
                            'amt':Radiology_ins.Amount
                    }
                    Services_List.append(data_list)

            elif category_ins.ServiceCategory == 'ROOMSERVICES':

                for datas in services_ins:



                    if Patientcategory == 'General' and op_patient:

                        fee_ins = RoomTypeFee.objects.get(pk=datas.object_id)
                        room_ins =  Room_Master_Detials.objects.get(pk=datas.object_id)
                        ward_ins = WardType_Master_Detials.objects.get(pk=room_ins.Ward_Name.Room_Id) 
                        data_list = {
                            'pk':datas.pk,
                            'Roomfee_op':fee_ins.General_fee, 
                          #  'wardname':fee_ins.room_type.Ward_Name.Ward_Name
                            'Roomdetails' : f'{room_ins.Room_No} - {room_ins.Bed_No} -{ward_ins.Ward_Name}'
                        }
                        Services_List.append(data_list)

                    if Patientcategory == 'General' and ip_patient:

                        fee_ins = RoomTypeFee.objects.get(pk=datas.object_id)
                        room_ins =  Room_Master_Detials.objects.get(pk=datas.object_id)
                        ward_ins = WardType_Master_Detials.objects.get(pk=room_ins.Ward_Name.Room_Id) 
                        data_list = {
                            'pk':datas.pk,
                            'Roomfee_ip':fee_ins.Special_fee, 
                          #  'wardname':fee_ins.room_type.Ward_Name.Ward_Name
                            'Roomdetails' : f'{room_ins.Room_No} - {room_ins.Bed_No} -{ward_ins.Ward_Name}'
                        }
                        Services_List.append(data_list)

                    elif Patientcategory == 'Insurance' and op_patient:

                        fee_ins = RoomTypeFee.objects.get(pk=datas.object_id)
                        room_ins =  Room_Master_Detials.objects.get(pk=datas.object_id)
                        ward_ins = WardType_Master_Detials.objects.get(pk=room_ins.Ward_Name.Room_Id)
                        insurance_ins = Insurance_Master_Detials.objects.get(pk=op_patient.InsuranceName_id)
                        insurance_fee = InsuranceRoomTypeFee.objects.get(room_type_fee_id=fee_ins.pk,insurance_id=insurance_ins.Insurance_Id)
                        data_list = {
                            'pk':datas.pk,
                            'insurance_Roomfee':insurance_fee.fee, 
                            'insurancename' : insurance_ins.Insurance_Name,
                            'Roomdetails' : f'{room_ins.Room_No} - {room_ins.Bed_No} -{ward_ins.Ward_Name}'
                        }
                        Services_List.append(data_list)

                    elif Patientcategory == 'Insurance' and ip_patient:

                        fee_ins = RoomTypeFee.objects.get(pk=datas.object_id)
                        room_ins =  Room_Master_Detials.objects.get(pk=datas.object_id)
                        ward_ins = WardType_Master_Detials.objects.get(pk=room_ins.Ward_Name.Room_Id)
                        insurance_ins = Insurance_Master_Detials.objects.get(pk=ip_patient.InsuranceName_id)
                        insurance_fee = InsuranceRoomTypeFee.objects.get(room_type_fee_id=fee_ins.pk,insurance_id=insurance_ins.Insurance_Id)
                        data_list = {
                            'pk':datas.pk,
                            'insurance_Roomfee':insurance_fee.fee, 
                            'insurancename' : insurance_ins.Insurance_Name,
                            'Roomdetails' : f'{room_ins.Room_No} - {room_ins.Bed_No} -{ward_ins.Ward_Name}'
                        }
                        Services_List.append(data_list)

                    elif Patientcategory == 'Client' and op_patient:

                        fee_ins = RoomTypeFee.objects.get(pk=datas.object_id)
                        room_ins =  Room_Master_Detials.objects.get(pk=datas.object_id)
                        ward_ins = WardType_Master_Detials.objects.get(pk=room_ins.Ward_Name.Room_Id)
                        client_ins = Client_Master_Detials.objects.get(pk=op_patient.ClientName_id)
                        client_fee = ClientRoomTypeFee.objects.get(room_type_fee_id=fee_ins.pk,client_id=client_ins.Client_Id)
                        data_list = {
                            'pk':datas.pk,
                            'client_Roomfee':client_fee.fee, 
                            'clientname' : client_ins.Client_Name,
                            'Roomdetails' : f'{room_ins.Room_No} - {room_ins.Bed_No} -{ward_ins.Ward_Name}'
                        }
                        Services_List.append(data_list)

                    elif Patientcategory == 'Client' and ip_patient:

                        fee_ins = RoomTypeFee.objects.get(pk=datas.object_id)
                        room_ins =  Room_Master_Detials.objects.get(pk=datas.object_id)
                        ward_ins = WardType_Master_Detials.objects.get(pk=room_ins.Ward_Name.Room_Id)
                        client_ins = Client_Master_Detials.objects.get(pk=ip_patient.ClientName_id)
                        client_fee = ClientRoomTypeFee.objects.get(room_type_fee_id=fee_ins.pk,client_id=client_ins.Client_Id)
                        data_list = {
                            'pk':datas.pk,
                            'client_Roomfee':client_fee.fee, 
                            'clientname' : client_ins.Client_Name,
                            'Roomdetails' : f'{room_ins.Room_No} - {room_ins.Bed_No} -{ward_ins.Ward_Name}'
                        }
                        Services_List.append(data_list)

                    elif Patientcategory == 'Corporate' and op_patient:

                        fee_ins = RoomTypeFee.objects.get(pk=datas.object_id)
                        room_ins =  Room_Master_Detials.objects.get(pk=datas.object_id)
                        ward_ins = WardType_Master_Detials.objects.get(pk=room_ins.Ward_Name.Room_Id)
                        corporate_ins = Corporate_Master_Detials.objects.get(pk=op_patient.CorporateName_id)
                        corporate_fee = CorporateRoomTypeFee.objects.get(room_type_fee_id=fee_ins.pk,corporate_id=corporate_ins.Corporate_Id)
                        data_list = {
                            'pk':datas.pk,
                            'corporate_Roomfee':corporate_fee.fee, 
                            'corporatename' : corporate_ins.Corporate_Name,
                            'Roomdetails' : f'{room_ins.Room_No} - {room_ins.Bed_No} -{ward_ins.Ward_Name}'
                        }
                        Services_List.append(data_list)

                    elif Patientcategory == 'Corporate' and ip_patient:

                        fee_ins = RoomTypeFee.objects.get(pk=datas.object_id)
                        room_ins =  Room_Master_Detials.objects.get(pk=datas.object_id)
                        ward_ins = WardType_Master_Detials.objects.get(pk=room_ins.Ward_Name.Room_Id)
                        corporate_ins = Corporate_Master_Detials.objects.get(pk=ip_patient.CorporateName_id)
                        corporate_fee = CorporateRoomTypeFee.objects.get(room_type_fee_id=fee_ins.pk,corporate_id=corporate_ins.Corporate_Id)
                        data_list = {
                            'pk':datas.pk,
                            'corporate_Roomfee':corporate_fee.fee, 
                            'corporatename' : corporate_ins.Corporate_Name,
                            'Roomdetails' : f'{room_ins.Room_No} - {room_ins.Bed_No} -{ward_ins.Ward_Name}'
                        }
                        Services_List.append(data_list)

            elif category_ins.ServiceCategory == 'GENERALSERVICES':

                for datas in services_ins:

                    if op_patient:
                        General_services_ins = Service_Master_Details.objects.get(pk=datas.object_id)                        
                        data_list = {
                                'pk': datas.pk,
                                'service_subcategory':f'{General_services_ins.Service_Id} - {General_services_ins.Service_Name}',
                                'amt':General_services_ins.Amount,
                        }
                        Services_List.append(data_list)
                    elif ip_patient:
                        General_services_ins = Service_Master_Details.objects.get(pk=datas.object_id)                        
                        data_list = {
                                'pk': datas.pk,
                                'service_subcategory':f'{General_services_ins.Service_Id} - {General_services_ins.Service_Name}',
                                'amt':General_services_ins.Amount,
                        }
                        Services_List.append(data_list)

            return JsonResponse(Services_List, safe=False)

        except Exception as e:
                return JsonResponse({"error":str(e)})


@csrf_exempt
@require_http_methods(['POST', 'GET', 'OPTIONS'])
def packege_master_details(request):

     if request.method == 'POST':
        try:
            data = json.loads(request.body)
           
            
            id = data.get('currentPackage').get('id')
            Package_Name= data.get("currentPackage").get('PackageName')
            PackageType = data.get("currentPackage").get('PackageType')
            Price = data.get("currentPackage").get('Price')
            Status = data.get("currentPackage").get('Status')
            Discount = data.get("currentPackage").get('AllowDiscount')
            Fromdate = data.get("currentPackage").get('FromDate')
            Todate = data.get("currentPackage").get('ToDate')
            Specialist = data.get("currentPackage").get('Specialist')
            Services_details =  data.get("services")
            
            if id:


                package_ins = Package_Master.objects.get(pk=id)
                Specialist_ins = Speciality_Detials.objects.get(pk=Specialist)
               
                package_ins.Package_Name = Package_Name
                package_ins.PackageType = PackageType
                package_ins.Price = Price
                package_ins.Status = Status
                package_ins.Discount = Discount
                package_ins.Fromdate = Fromdate
                package_ins.Todate = Todate
                package_ins.Specialist = Specialist_ins
                package_ins.Services_details = Services_details

                package_ins.save()

                return JsonResponse({'success':'Package Updated  successfully'})


            Specialist_ins = Speciality_Detials.objects.get(Speciality_Id=Specialist) 

            Package_ins = Package_Master(
                Package_Name = Package_Name,
                PackageType = PackageType,
                Price = Price,
                Status = Status,
                Discount = Discount,
                Fromdate = Fromdate,
                Todate = Todate,
                Specialist = Specialist_ins,
                Services_details = Services_details,
            )
            Package_ins.save()
            
           
            return JsonResponse({'success':'Package Added successfully'})
        except Exception as e:
            # Handle and return the error message in the response
            return JsonResponse({'error': str(e)})
        
     if request.method == "GET":
         
         try:
             
             Package_ins = Package_Master.objects.all()

             package_data_list = []

             for datas in Package_ins:
                 data_list={
                     "id":datas.id,
                     "PackageName":datas.Package_Name,
                     "PackageType":datas.PackageType,
                     "Price":datas.Price,
                     "Status":datas.Status,
                     "AllowDiscount":datas.Discount,
                     "FromDate":datas.Fromdate,
                     "ToDate":datas.Todate,
                     "Specialist":datas.Specialist.Speciality_Id,
                     "Specialistname":datas.Specialist.Speciality_Name,
                     "Services_details":datas.Services_details
                 }
                 package_data_list.append(data_list)
         
             return JsonResponse(package_data_list,safe=False)

         except Exception as e:
            # Handle and return the error message in the response
            return JsonResponse({'error': str(e)})

@csrf_exempt
def Services_Group_details(request):

    if request.method == 'GET':

        try:
            services_ins = Services_Group_Details.objects.all()
            services_list = []
            for datas in services_ins:

                serviceid = datas.service_category_id
                category_ins = Service_Category_Masters.objects.get(pk=serviceid)
                

                if category_ins.ServiceCategory == 'CONSULTATION':

                    consultaion_ins = Doctor_Ratecard_Master.objects.get(pk=datas.object_id)
                    
                    Doctor_speciality_ins = Doctor_ProfessForm_Detials.objects.get(Doctor_ID=consultaion_ins.Doctor_ID)  
                    speciality_ins = Speciality_Detials.objects.get(Speciality_Id=Doctor_speciality_ins.Specialization.Speciality_Id)
                    doctor_ins = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=consultaion_ins.Doctor_ID.Doctor_ID)
                    data_list = {
                             'id':datas.pk,
                             'category': category_ins.ServiceCategory,
                             'service_subcategory' : f'{consultaion_ins.Doctor_ID.Doctor_ID} - Dr.{doctor_ins.First_Name}{doctor_ins.Middle_Name}({speciality_ins.Speciality_Name})',
                        }
                    services_list.append(data_list)

                elif category_ins.ServiceCategory == 'LAB':

                

                    labtest_ins = Testmaster_Cost_List.objects.get(pk=datas.object_id)
                    
                    data_list = {
                             'id':datas.pk,
                             'category': category_ins.ServiceCategory,
                             'service_subcategory': f'{labtest_ins.Test_Code.Test_Code} - {labtest_ins.Test_Code.Test_Name}' if labtest_ins.Test_Code else labtest_ins.Group_Code.Group_Name,
                        }
                    services_list.append(data_list)

                elif category_ins.ServiceCategory == 'RADIOLOGY':

                

                    Radiology_ins = TestName_Details.objects.get(pk=datas.object_id)
                    
                    data_list = {
                             'id':datas.pk,
                             'category': category_ins.ServiceCategory,
                             'service_subcategory':f'{Radiology_ins.Test_Code} - {Radiology_ins.Test_Name}',
                        }
                    services_list.append(data_list)

                elif category_ins.ServiceCategory == 'ROOMSERVICES':

               
                    Room_ins = Room_Master_Detials.objects.get(pk=datas.object_id)
                    ward_ins = WardType_Master_Detials.objects.get(pk=Room_ins.Ward_Name.Room_Id)        
                    data_list = {
                            'id':datas.pk,
                            'category': category_ins.ServiceCategory,
                            'service_subcategory' : f'{Room_ins.Room_No} - {Room_ins.Bed_No} -{ward_ins.Ward_Name}'         
                    }
                    services_list.append(data_list)

                elif category_ins.ServiceCategory == 'GENERALSERVICES':

                    General_services_ins  = Service_Master_Details.objects.get(pk=datas.object_id)
                    
                    data_list = {
                             'id':datas.pk,
                             'category': category_ins.ServiceCategory,
                             'service_subcategory':General_services_ins.Service_Name
                        }
                    services_list.append(data_list)
                
            for idx, services in enumerate(services_list, start=1):
                      services["Sno"] = idx 

            return JsonResponse(services_list,safe=False)

        except Exception as e:
            # Handle and return the error message in the response
            return JsonResponse({'error': str(e)})

@csrf_exempt
@require_http_methods(['POST', 'GET', 'OPTIONS'])
def service_map_delete(request):
    if request.method == 'POST':

        try:

            id = request.GET.get('id')
            services =  Services_Group_Details.objects.get(pk=id)
            services.delete()

            return JsonResponse({'success':'Data Deleted Successfully'})

        except Exception as e:
                return JsonResponse({"error":str(e)})

@csrf_exempt
@require_http_methods(['GET'])
def Services_List_by_servicecategory(request):

    if request.method == "GET":

         try:

            servicecategory = request.GET.get('servicecategory','')

            Services_data_list = []

            category_ins = Service_Category_Masters.objects.get(Serviceid = servicecategory)
            if category_ins.ServiceCategory == 'CONSULTATION':
                
                consultaion_ins = Doctor_Ratecard_Master.objects.all()
                for datas in consultaion_ins:
                    
                    Doctor_speciality_ins = Doctor_ProfessForm_Detials.objects.get(Doctor_ID=datas.Doctor_ID)  
                    speciality_ins = Speciality_Detials.objects.get(Speciality_Id=Doctor_speciality_ins.Specialization.Speciality_Id)
                    doctor_ins = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=datas.Doctor_ID.Doctor_ID)
                    
                    service_data = {
                        
                        'pk': datas.pk,
                        'service_category' : 'Dr.Consultation',
                        'service_subcategory' : f'{datas.Doctor_ID.Doctor_ID} - Dr.{doctor_ins.First_Name}{doctor_ins.Middle_Name}({speciality_ins.Speciality_Name})',     
                    }
                    Services_data_list.append(service_data)
            
            if category_ins.ServiceCategory == 'LAB':
                labtest_ins = Testmaster_Cost_List.objects.all()
                for datas in labtest_ins:
                
                    service_data = {
                        'pk' : datas.pk,
                        'service_category' : 'Lab',
                        'service_subcategory': f'{datas.Test_Code.Test_Code} - {datas.Test_Code.Test_Name}' if datas.Test_Code else f'{datas.Group_Code.Group_Code}-f{datas.Group_Code.Group_Name}',
                    }
                    Services_data_list.append(service_data)
            
            if category_ins.ServiceCategory == 'RADIOLOGY':
                Radiology_ins = TestName_Details.objects.all()
                for datas in Radiology_ins:
                    
                    service_data = {
                        'pk':datas.pk,
                        'service_category' : 'Radiology',
                        'service_subcategory':f'{datas.Test_Code} - {datas.Test_Name}',
                    }
                    Services_data_list.append(service_data)
            
            if category_ins.ServiceCategory == 'ROOMSERVICES':
                Room_ins = Room_Master_Detials.objects.all()
                for datas in Room_ins:
                    
                    ward_ins = WardType_Master_Detials.objects.get(pk=datas.Ward_Name.Room_Id)
                    service_data = {
                        
                        'pk':datas.pk,
                        'service_subcategory':f'{datas.Room_No} - {datas.Bed_No} -{ward_ins.Ward_Name}'
                        
                    }
                    Services_data_list.append(service_data)
            
            if category_ins.ServiceCategory == 'GENERALSERVICES':
                service_ins = Service_Master_Details.objects.all()
                for datas in service_ins:
                    service_data = {
                        
                        'pk' : datas.pk,
                        'service_category' : 'general services',
                        'service_subcategory' : datas.Service_Name
                    }
                    Services_data_list.append(service_data)
                    
            return JsonResponse(Services_data_list,safe=False)

         except Exception as e:
            return JsonResponse({"error": str(e)})
        