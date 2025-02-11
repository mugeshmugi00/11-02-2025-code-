

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import *
from Ip_Workbench.models import *
from Workbench.models import *
from Inventory.models import *
from django.db.models import Sum, Q
from .serializers import *
import pandas as pd
from django.db.models import Q
from datetime import datetime


@csrf_exempt   
@require_http_methods(["POST","OPTIONS","GET"])
def OtTheaterMaster_Detials_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            print(f"Received data: {data}")
            
            # Extract and validate data
            OtId = data.get('OtId')
            Location = data.get('Location')
            TheatreName = data.get('TheatreName')
            ShortName = data.get('ShortName')
            FloorName = data.get('FloorName')
            Building = data.get('Building')
            Block = data.get('Block')

           
            
            speciality = data.get('Speciality')
            SpecialityId = data.get("SpecialityId", [])

          
            SpecialityId= SpecialityId.split(', ') if SpecialityId else None

            
            TheatreType = data.get('TheatreType')
            Rent = data.get('Rent')
            Emergency = data.get('Emergency',False)
            Details = data.get('Details')
            Remarks = data.get('Remarks')
            Statusedit = data.get('Statusedit',False)
            created_by = data.get('created_by','')
      
            try:
                location_instance = Location_Detials.objects.get(pk=Location)
                floor_instance = Floor_Master_Detials.objects.get(pk=FloorName)
                Buiding_ins = Building_Master_Detials.objects.get(pk=Building)
                Block_ins = Block_Master_Detials.objects.get(pk=Block)

          

                if not SpecialityId:
                        
                        SpecialityId = []

                Speciality_instance = Speciality_Detials.objects.filter(Speciality_Id__in=SpecialityId)
              
                
                
            except (Location_Detials.DoesNotExist, Floor_Master_Detials.DoesNotExist,Building_Master_Detials.DoesNotExist,Block_Master_Detials.DoesNotExist,WardType_Master_Detials.DoesNotExist):
                return JsonResponse({'error': 'Invalid Location or FloorName'})

            
            
           
            if OtId:
                if Statusedit:
                   
                    OtTheater_instance = OtTheaterMaster_Detials.objects.get(Ot_Id=OtId)
                    OtTheater_instance.Status = not OtTheater_instance.Status
                    OtTheater_instance.save()
                      
                    
                else:  
                    
                        OtTheater_instance = OtTheaterMaster_Detials.objects.get(Ot_Id=OtId)
                        
                        OtTheater_instance.Location=location_instance
                        OtTheater_instance.TheatreName=TheatreName
                        OtTheater_instance.ShortName=ShortName
                        OtTheater_instance.FloorName=floor_instance
                        OtTheater_instance.Building = Buiding_ins
                        OtTheater_instance.Block = Block_ins
                    
                        OtTheater_instance.TheatreType = TheatreType
                        OtTheater_instance.Rent = Rent
                        OtTheater_instance.Emergency=Emergency
                        OtTheater_instance.Details=Details
                        OtTheater_instance.Remarks=Remarks
                        OtTheater_instance.save()

                        OtTheater_instance.Speciality.set(Speciality_instance)
                        

                return JsonResponse({'success': 'OtTheater Updated successfully'})
            else:
                
                if OtTheaterMaster_Detials.objects.filter(TheatreName=TheatreName).exists():
                    return JsonResponse({'warn': f"The TheatreName  are already present in the name of {TheatreName} "})
                else:
                    
                    OtTheater_instance = OtTheaterMaster_Detials.objects.create(
                        Location=location_instance,
                        TheatreName=TheatreName,
                        ShortName=ShortName,
                        FloorName=floor_instance,
                        Building = Buiding_ins,
                        Block = Block_ins,
                          
                        TheatreType = TheatreType,
                        Rent = Rent,
                        Emergency=Emergency,
                        Details=Details,
                        Remarks=Remarks,
                        created_by=created_by
                    )

                if Speciality_instance:
                    OtTheater_instance.Speciality.set(Speciality_instance)
                else:
                    OtTheater_instance.Speciality.set([])
                
            return JsonResponse({'success': 'OtTheater added successfully'})
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
        
    elif request.method == 'GET':
        try:
            
            OtTheaters = OtTheaterMaster_Detials.objects.all()
            print(OtTheaters)
            
            
            OtTheaters_Master_data = []
            for OtTheater in OtTheaters:


                SpecialityID = ', '.join(str(Speciality.Speciality_Id) for Speciality in OtTheater.Speciality.all())
                Specialitynames = ', '.join(Speciality.Speciality_Name for Speciality in OtTheater.Speciality.all())
               

                OtTheater_dict = {
                    'id': OtTheater.pk,
                    'LocationId': OtTheater.Location.Location_Id,
                    'Location': OtTheater.Location.Location_Name,
                    'TheatreName': OtTheater.TheatreName,
                    'ShortName': OtTheater.ShortName,
                    'FloorId': OtTheater.FloorName.Floor_Id,
                    'FloorName': OtTheater.FloorName.Floor_Name,
                    'BuidingId':OtTheater.Building.Building_Id,
                    'BuildingName':OtTheater.Building.Building_Name,
                    'BlockId':OtTheater.Block.Block_Id,
                    'BlockName':OtTheater.Block.Block_Name,
                    'SpecialityID':SpecialityID,
                    'Specialityname':Specialitynames,
                      
                    'TheatreType':OtTheater.TheatreType,
                    'Rent':OtTheater.Rent,
                    'Emergency': OtTheater.Emergency,
                    'Details': OtTheater.Details,
                    'Remarks': OtTheater.Remarks,
                    'Status': 'Active' if OtTheater.Status else 'Inactive',
                    'created_by': OtTheater.created_by,
                    
                }
                OtTheaters_Master_data.append(OtTheater_dict)

                for idx, theatre in enumerate(OtTheaters_Master_data, start=1):
                        theatre["sno"] = idx 

            return JsonResponse(OtTheaters_Master_data, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'})

@csrf_exempt
@require_http_methods(["GET"])
def Theatrename_all(request):

      if request.method == 'GET':
          
          try:
              
              Speciality = request.GET.get('Speciality', None)
              
              theatre_ins = OtTheaterMaster_Detials.objects.all()
              
              theatre_list = []
              for datas in theatre_ins:
                  
                  data_list = {
                      
                      'id':datas.Ot_Id,
                      'Theatrename':datas.TheatreName
                  }
                  theatre_list.append(data_list)
                  

              return JsonResponse(theatre_list,safe=False)
              





          except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def Doctorname_for_OTBooking(request):

    if request.method == 'GET':

        try:

         
            specialityid = request.GET.get('Speciality', None)
            
            doct_list = []
        
              
            Doc_ins = Doctor_ProfessForm_Detials.objects.filter(Category_id=4,Specialization_id=specialityid)
           
            for datas in Doc_ins:
                
                data_list={
                    'id':datas.Doctor_ID.Doctor_ID,
                    'Doctorname':f'{datas.Doctor_ID.Tittle.Title_Name}.{datas.Doctor_ID.First_Name}.{datas.Doctor_ID.Last_Name}'
                }
                doct_list.append(data_list)

            return JsonResponse(doct_list,safe=False)
            


        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def Surgeon_list(request):

    if request.method == 'GET':

        try:

            des_ins = Designation_Detials.objects.get(Designation_Name='SENIORSURGEON')

            Surgeon_list=[]
            Doc_ins = Doctor_ProfessForm_Detials.objects.filter(Designation_id = des_ins.Designation_Id)
            for datas in Doc_ins:
                
                data_list={
                    'id':datas.Doctor_ID.Doctor_ID,
                    'Doctorname':f'{datas.Doctor_ID.Tittle.Title_Name}.{datas.Doctor_ID.First_Name}.{datas.Doctor_ID.Last_Name}'
                }
                Surgeon_list.append(data_list)

            return JsonResponse(Surgeon_list,safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def Surgeon_list_for_calendar(request):

    if request.method == 'GET':

        try:

            desname = request.GET.get('desname','')
            print(desname)

            if desname == 'SENIORSURGEON' or desname == 'JUNIORSURGEON':

                des_ins = Designation_Detials.objects.get(Designation_Name = desname)

                Surgeon_list=[]
                Doc_ins = Doctor_ProfessForm_Detials.objects.filter(Designation_id = des_ins.Designation_Id)
                for datas in Doc_ins:
                    
                    data_list={
                        'id':datas.Doctor_ID.Doctor_ID,
                        'Doctorname':f'{datas.Doctor_ID.Tittle.Title_Name}.{datas.Doctor_ID.First_Name}.{datas.Doctor_ID.Last_Name}'
                    }
                    Surgeon_list.append(data_list)

                return JsonResponse(Surgeon_list,safe=False)
            
            elif desname == 'ANAESTHESIOLOGIST':

                spe_ins = Speciality_Detials.objects.get(Speciality_Name = desname)

                Anaesthesiologist_list=[]
                Doc_ins = Doctor_ProfessForm_Detials.objects.filter(Specialization_id = spe_ins.Speciality_Id)
                
                for datas in Doc_ins:
                        
                        data_list={
                        'id':datas.Doctor_ID.Doctor_ID,
                        'Doctorname':f'{datas.Doctor_ID.Tittle.Title_Name}.{datas.Doctor_ID.First_Name}.{datas.Doctor_ID.Last_Name}'
                        }

                        Anaesthesiologist_list.append(data_list)

                return JsonResponse(Anaesthesiologist_list,safe=False)


        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def Assistant_Surgeon_list(request):

    if request.method == 'GET':

        try:


            des_ins = Designation_Detials.objects.get(Designation_Name='JUNIORSURGEON')
            Surgeon_list=[]
            Doc_ins = Doctor_ProfessForm_Detials.objects.filter(Designation_id = des_ins.Designation_Id)
            for datas in Doc_ins:
                
                data_list={
                    'id':datas.Doctor_ID.Doctor_ID,
                    'Doctorname':f'{datas.Doctor_ID.Tittle.Title_Name}.{datas.Doctor_ID.First_Name}.{datas.Doctor_ID.Last_Name}'
                }
                Surgeon_list.append(data_list)

            return JsonResponse(Surgeon_list,safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def Anaesthesiologist_list(request):

    if request.method == 'GET':

        try:

            

            spe_ins = Speciality_Detials.objects.get(Speciality_Name='ANAESTHESIOLOGIST')

            Anaesthesiologist_list=[]
            Doc_ins = Doctor_ProfessForm_Detials.objects.filter(Specialization_id = spe_ins.Speciality_Id)
            
            for datas in Doc_ins:
                    
                    data_list={
                    'id':datas.Doctor_ID.Doctor_ID,
                    'Doctorname':f'{datas.Doctor_ID.Tittle.Title_Name}.{datas.Doctor_ID.First_Name}.{datas.Doctor_ID.Last_Name}'
                     }

                    Anaesthesiologist_list.append(data_list)

            return JsonResponse(Anaesthesiologist_list,safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def Scrub_Nurse_list(request):

    if request.method == 'GET':

        try:

            des_ins = Designation_Detials.objects.get(Designation_Name='SCRUBNURSE')
            Scrub_Nurse_list=[]
            emp_ins = Employee_Personal_Form_Detials.objects.filter(Designation_id=des_ins.Designation_Id)
            
            
            for datas in emp_ins:

                    data_list={
                        'id':datas.Employee_ID,
                        'Employeename':f'{datas.Tittle.Title_Name}.{datas.First_Name}.{datas.Last_Name}'
                    }
                    Scrub_Nurse_list.append(data_list)

            return JsonResponse(Scrub_Nurse_list,safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def Circulating_Nurse_list(request):

    if request.method == 'GET':

        try:
            des_ins = Designation_Detials.objects.get(Designation_Name='CIRCULATINGNURSE')
            Circulating_Nurse_list=[]
            emp_ins = Employee_Personal_Form_Detials.objects.filter(Designation_id=des_ins.Designation_Id)
            
            
            for datas in emp_ins:


                    data_list={
                        'id':datas.Employee_ID,
                        'Employeename':f'{datas.Tittle.Title_Name}.{datas.First_Name}.{datas.Last_Name}'
                    }
                    Circulating_Nurse_list.append(data_list)

            return JsonResponse(Circulating_Nurse_list,safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def Technician_list(request):

    if request.method == 'GET':

        try:
            cat_ins = Category_Detials.objects.get(Category_Name='TECHNICIAN')
            Technician_list=[]
            emp_ins = Employee_Personal_Form_Detials.objects.filter(Category_id=cat_ins.Category_Id)
            
            
            for datas in emp_ins:

                    data_list={
                        'id':datas.Employee_ID,
                        'Employeename':f'{datas.Tittle.Title_Name}.{datas.First_Name}{datas.Last_Name}'
                    }
                    Technician_list.append(data_list)

            return JsonResponse(Technician_list,safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def Helper_list(request):


    if request.method == 'GET':

        try:

            cat_ins = Category_Detials.objects.get(Category_Name='HELPER')
            Helper_list=[]
            emp_ins = Employee_Personal_Form_Detials.objects.filter(Category_id=cat_ins.Category_Id)
            
            
            for datas in emp_ins:


                    data_list={
                        'id':datas.Employee_ID,
                        'Employeename':f'{datas.Tittle.Title_Name}.{datas.First_Name}{datas.Last_Name}'
                    }
                    Helper_list.append(data_list)

            return JsonResponse(Helper_list,safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

@csrf_exempt
@require_http_methods(["POST","OPTIONS","GET"])
def Theatre_booking_request_details(request):

    if request.method == 'POST':

        try:

            data = json.loads(request.body) 
            print(data)
            id = data.get('Booking_Id','')
            Theatreid =data.get('Theatreid','')
            ReqDate = data.get('reqDate','')
            ReqTime = data.get('reqTime','')
            BookingType = data.get('bookingType','')
            BookingDate = data.get('bookingDate','')
            BookingTime = data.get('bookingTime','')
            Duration = data.get('duration','')
            OperationType = data.get('operationType','')
            priority = data.get('priority','')
            patientId = data.get('patientId','')
            patientName = data.get('patientName','')
            Age = data.get('age','')
            Gender = data.get('gender','')
            UHIDno = data.get('uhidNo','')
            Createdby = data.get('created_by','')
            Specializtion = data.get('specialization','')
            bdate = data.get('BookingDate','')
            SurgeryName = data.get('surgeryName','')
            OTName = data.get('OTName','')
            DoctorName = data.get('doctorName','')
            Status = data.get('Status','')
            Statusedit = data.get('Statusedit','')
            Reason = data.get('Reason','')
            OPD_Id = data.get('OPD_Id','')
            opregistrationnid = data.get('opregistrationnid','')
            ipregistrationid = data.get('ipregistrationid','')
            emgregistrationid = data.get('emgregistrationid','')


            Specialization_ins = Speciality_Detials.objects.get(pk=Specializtion) if Specializtion else None
            Surgery_ins = SurgeryName_Details.objects.get(pk=SurgeryName) if SurgeryName else None
            Theatre_ins = OtTheaterMaster_Detials.objects.get(pk=OTName) if OTName else None
            Doctor_ins = Doctor_Personal_Form_Detials.objects.get(pk=DoctorName) if DoctorName else None
            Patient_ins = Patient_Detials.objects.get(pk=patientId) if patientId else None
            booking_ins = Theatre_Booking_Request_Details.objects.get(pk=id) if id else None
            op_reg_id_ins = Patient_Appointment_Registration_Detials.objects.get(Registration_Id=opregistrationnid) if opregistrationnid else None
            ip_reg_id_ins = Patient_IP_Registration_Detials.objects.get(Registration_Id = ipregistrationid ) if ipregistrationid else None
            emg_reg_id_ins = Patient_Emergency_Registration_Detials.objects.get(Registration_Id = emgregistrationid) if emgregistrationid else None
            

            if BookingType == 'OP' and OPD_Id:
                    
                    OPD_Otrequest = OPD_OtRequest_Details.objects.get(pk=OPD_Id)
                    OPD_Otrequest.Status = not OPD_Otrequest.Status
                    OPD_Otrequest.save()
                    
                    Theatre_request_ins = Theatre_Booking_Request_Details(
                
                    ReqDate = ReqDate,
                    ReqTime = ReqTime,
                    BookingType = BookingType,
                    BookingDate = BookingDate,
                    BookingTime = BookingTime,
                    Duration = Duration,
                    OperationType = OperationType,
                    Priority = priority,
                    PatientName = patientName,
                    Age = Age,
                    Gender = Gender,
                    UHIDNO = UHIDno,
                    CreatedBy =Createdby,
                    Status=Status,
                    Specialization = Specialization_ins,
                    SurgeryName = Surgery_ins,
                    TheatreName = Theatre_ins,
                    Patientid = Patient_ins,
                    DoctorName = Doctor_ins,
                    OP_Registration_Id = op_reg_id_ins,
                    IP_Registration_Id = ip_reg_id_ins,
                    EMR_Registration_Id = emg_reg_id_ins

                    )

                    Theatre_request_ins.save()

                    return JsonResponse({'success': 'Booking Request Added successfully'})
           
            elif id:  
               
               if Statusedit == True:
                    
                   
                    Theatre_request_ins =  Theatre_Booking_Request_Details.objects.get(Booking_Id=id)
                    
                    Theatre_request_ins.Status = Status
                    Theatre_request_ins.Reason = Reason
                    Theatre_request_ins.save()

                    return JsonResponse({'success': f'Booking Request {Status} successfully'})
                   
               Theatre_request_ins =  Theatre_Booking_Request_Details.objects.get(Booking_Id=id)

               Theatre_request_ins.ReqDate = ReqDate
               Theatre_request_ins.ReqTime = ReqTime
               Theatre_request_ins.BookingType = BookingType
               Theatre_request_ins.BookingDate = BookingDate
               Theatre_request_ins.BookingTime = BookingTime
               Theatre_request_ins.Duration = Duration
               Theatre_request_ins.OperationType = OperationType
               Theatre_request_ins.Priority = priority
               Theatre_request_ins.Patientid = Patient_ins
               Theatre_request_ins.PatientName = patientName
               Theatre_request_ins.Age = Age
               Theatre_request_ins.Gender = Gender
               Theatre_request_ins.UHIDNO = UHIDno
               Theatre_request_ins.CreatedBy = Createdby
               Theatre_request_ins.Status = Status
               Theatre_request_ins.Specialization = Specialization_ins
               Theatre_request_ins.SurgeryName = Surgery_ins
               Theatre_request_ins.TheatreName = Theatre_ins
               Theatre_request_ins.DoctorName = Doctor_ins
               Theatre_request_ins.OP_Registration_Id = op_reg_id_ins
               Theatre_request_ins.IP_Registration_Id = ip_reg_id_ins
               Theatre_request_ins.EMR_Registration_Id = emg_reg_id_ins

               Theatre_request_ins.save()

               return JsonResponse({'success':'Booking Request Updated successfully'})


            Theatre_request_ins = Theatre_Booking_Request_Details(
                
                ReqDate = ReqDate,
                ReqTime = ReqTime,
                BookingType = BookingType,
                BookingDate = BookingDate,
                BookingTime = BookingTime,
                Duration = Duration,
                OperationType = OperationType,
                Priority = priority,
                Patientid = Patient_ins,
                PatientName = patientName,
                Age = Age,
                Gender = Gender,
                UHIDNO = UHIDno,
                CreatedBy =Createdby,
                Status=Status,
                Reason = Reason,

                Specialization = Specialization_ins,
                SurgeryName = Surgery_ins,
                TheatreName = Theatre_ins,
                DoctorName = Doctor_ins,
                OP_Registration_Id = op_reg_id_ins,
                IP_Registration_Id = ip_reg_id_ins,
                EMR_Registration_Id = emg_reg_id_ins

                )

            Theatre_request_ins.save()

            return JsonResponse({'success': 'Booking Request Added successfully'})

        except Exception as e:
        
           return JsonResponse({'error': str(e)})

    elif request.method == 'GET':

        try:

            Theatrerequest_list = []
            Theatre_ins = Theatre_Booking_Request_Details.objects.all()

            print(Theatre_ins)
            
            
            for datas in Theatre_ins:

                formatted_rdate =  datas.ReqDate.strftime('%d-%m-%y')
                
                formatted_bdate = datas.BookingDate.strftime('%d-%m-%y')


                if datas.BookingType == 'OP':

                     data_list = {

                    'Booking_Id':datas.Booking_Id,
                    'ReqDate':formatted_rdate,
                    'ReqTime':datas.ReqTime,
                    'BookingType':datas.BookingType,
                    'Specialization_name':datas.Specialization.Speciality_Name,
                    'Specializationid':datas.Specialization.Speciality_Id,
                    'SurgeryName':datas.SurgeryName.Surgery_Name,
                    'Surgeryid':datas.SurgeryName.Surgery_Id,
                    'TheatreName':datas.TheatreName.TheatreName,
                    'Theatreid':datas.TheatreName.Ot_Id,
                    'theatrerent' : int(datas.TheatreName.Rent),
                    'DoctorID':datas.DoctorName.Doctor_ID,
                    'DoctorName':datas.DoctorName.First_Name,
                    'BookingDate':datas.BookingDate,
                    'bookingdate':formatted_bdate,
                    'BookingTime':datas.BookingTime,
                    'Duration':int(datas.Duration),
                    'OperationType':datas.OperationType,
                    'Priority':datas.Priority,
                    'patientId': datas.OP_Registration_Id.PatientId.PatientId if datas.OP_Registration_Id else None,
                    'PatientName':datas.OP_Registration_Id.PatientId.FirstName if datas.OP_Registration_Id else None,
                    'Age':datas.OP_Registration_Id.PatientId.Age if datas.OP_Registration_Id else None,
                    'Gender':datas.OP_Registration_Id.PatientId.Gender if datas.OP_Registration_Id else None,
                    'UHIDNO':datas.OP_Registration_Id.PatientId.UniqueIdNo if datas.OP_Registration_Id else None,
                    'Status':datas.Status,
                    'Reason' : datas.Reason,
                    'CreatedBy':datas.CreatedBy,
                    'opregid' : datas.OP_Registration_Id.id if datas.OP_Registration_Id else None,
                    'RegistrationId' : datas.OP_Registration_Id.Registration_Id if datas.OP_Registration_Id else None,
                    

                }
                     Theatrerequest_list.append(data_list)

                elif  datas.BookingType == 'IP':

                     data_list = {

                    'Booking_Id':datas.Booking_Id,
                    'ReqDate':formatted_rdate,
                    'ReqTime':datas.ReqTime,
                    'BookingType':datas.BookingType,
                    'Specialization_name':datas.Specialization.Speciality_Name,
                    'Specializationid':datas.Specialization.Speciality_Id,
                    'SurgeryName':datas.SurgeryName.Surgery_Name,
                    'Surgeryid':datas.SurgeryName.Surgery_Id,
                    'TheatreName':datas.TheatreName.TheatreName,
                    'Theatreid':datas.TheatreName.Ot_Id,
                    'theatrerent' : int(datas.TheatreName.Rent),
                    'DoctorID':datas.DoctorName.Doctor_ID,
                    'DoctorName':datas.DoctorName.First_Name,
                    'BookingDate':datas.BookingDate,
                    'bookingdate':formatted_bdate,
                    'BookingTime':datas.BookingTime,
                    'Duration':int(datas.Duration),
                    'OperationType':datas.OperationType,
                    'Priority':datas.Priority,
                    'patientId': datas.IP_Registration_Id.PatientId.PatientId if datas.IP_Registration_Id else None,
                    'PatientName':datas.IP_Registration_Id.PatientId.FirstName if datas.IP_Registration_Id else None,
                    'Age':datas.IP_Registration_Id.PatientId.Age if datas.IP_Registration_Id else None,
                    'Gender':datas.IP_Registration_Id.PatientId.Gender if datas.IP_Registration_Id else None,
                    'UHIDNO':datas.IP_Registration_Id.PatientId.UniqueIdNo if datas.IP_Registration_Id else None,
                    'Status':datas.Status,
                    'Reason' : datas.Reason,
                    'CreatedBy':datas.CreatedBy,
                    'RegistrationId' : datas.IP_Registration_Id.Registration_Id if datas.IP_Registration_Id else None,
                    

                }
                     Theatrerequest_list.append(data_list)

                elif  datas.BookingType == 'EMERGENCY':

                     data_list = {

                    'Booking_Id':datas.Booking_Id,
                    'ReqDate':formatted_rdate,
                    'ReqTime':datas.ReqTime,
                    'BookingType':datas.BookingType,
                    'Specialization_name':datas.Specialization.Speciality_Name,
                    'Specializationid':datas.Specialization.Speciality_Id,
                    'SurgeryName':datas.SurgeryName.Surgery_Name,
                    'Surgeryid':datas.SurgeryName.Surgery_Id,
                    'TheatreName':datas.TheatreName.TheatreName,
                    'Theatreid':datas.TheatreName.Ot_Id,
                    'DoctorID':datas.DoctorName.Doctor_ID,
                    'DoctorName':datas.DoctorName.First_Name,
                    'BookingDate':datas.BookingDate,
                    'bookingdate':formatted_bdate,
                    'BookingTime':datas.BookingTime,
                    'Duration':int(datas.Duration),
                    'OperationType':datas.OperationType,
                    'Priority':datas.Priority,
                    'patientId': datas.EMR_Registration_Id.PatientId.PatientId if datas.EMR_Registration_Id else None,
                    'PatientName':datas.EMR_Registration_Id.PatientId.FirstName if datas.EMR_Registration_Id else None,
                    'Age':datas.EMR_Registration_Id.PatientId.Age if datas.EMR_Registration_Id else None,
                    'Gender':datas.EMR_Registration_Id.PatientId.Gender if datas.EMR_Registration_Id else None,
                    'UHIDNO':datas.EMR_Registration_Id.PatientId.UniqueIdNo if datas.EMR_Registration_Id else None,
                    'Status':datas.Status,
                    'Reason' : datas.Reason,
                    'CreatedBy':datas.CreatedBy,
                    'RegistrationId' : datas.EMR_Registration_Id.Registration_Id if datas.EMR_Registration_Id else None,
                    

                }
                     Theatrerequest_list.append(data_list)

            opd_request_ins = OPD_OtRequest_Details.objects.all()
            
            for datas in opd_request_ins:

               if datas.Status == True:
                    
        
                    created_at = datas.created_at 
                    formatted_bdate = datas.SurgeryRequestedDate.strftime('%d-%m-%y')
                    formatted_date =  created_at.strftime('%d-%m-%y')
                    formatted_time = created_at.strftime('%H:%M:%S')
                    
                    data_list = {

                        'OPD_Id' : datas.OtRequest_Id,
                        'BookingDate':datas.SurgeryRequestedDate,
                        'bookingdate' : formatted_bdate,
                        'ReqDate' : formatted_date,
                        'ReqTime' : formatted_time,
                        'SurgeryName' : datas.SurgeryName.Surgery_Name,
                        'Surgeryid' : datas.SurgeryName.Surgery_Id,
                        'patientId':datas.Patient_Id.PatientId,
                        'RegistrationId' :datas.Registration_Id.Registration_Id,
                        'PatientName':datas.Patient_Id.FirstName,
                        'Age':datas.Patient_Id.Age,
                        'Gender':datas.Patient_Id.Gender,
                        'BookingType':'OP',
                        'Specialization_name':datas.Speciality.Speciality_Name,
                        'Specializationid':datas.Speciality.Speciality_Id,
                        'UHIDNO':datas.Patient_Id.UniqueIdNo,
                        'Status' : 'Requested',
                        

                    }
                    Theatrerequest_list.append(data_list)  
            
            for idx, Theatre in enumerate(Theatrerequest_list, start=1):
                        Theatre["Sno"] = idx 
                      
            return JsonResponse(Theatrerequest_list,safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

@csrf_exempt
@require_http_methods(["POST","OPTIONS","GET"])
def OTCalendar_Booking_Status(request):

    if request.method == 'POST':

        try:

            data = json.loads(request.body)

            print(data)

            bdate = data.get('BookingDate','')
            btime = data.get('BookingTime','')
            Booking_Id = data.get('Booking_Id','')
            CreatedBy = data.get('CreatedBy','')
            Theatreid = data.get('Theatreid','')
            Status = data.get('Status','')
            opregid = data.get('opregid','')
            patientId = data.get('patientId','')
            RegistrationId = data.get('RegistrationId','')
            BookingType = data.get('BookingType','')


            booking_ins = Theatre_Booking_Request_Details.objects.get(Booking_Id=Booking_Id) if Booking_Id else None
            theatre_ins = OtTheaterMaster_Detials.objects.get(Ot_Id = Theatreid) if Theatreid else None

            existsdata = OTTheatrecalendar.objects.filter(date=bdate,time=btime).first()
           

            if Status == 'Completed':

                print(Status,'status')

                booking_ins = Theatre_Booking_Request_Details.objects.get(Booking_Id=Booking_Id)

                booking_ins.Status = Status
                booking_ins.save()

            if existsdata:

                return JsonResponse({'success': 'already exists'})

            calendar_ins = OTTheatrecalendar(

                Theatre = theatre_ins,
                booking = booking_ins,
                date = bdate,
                time = btime,
            )

            calendar_ins.save()

            if BookingType == 'OP':

                crew_ins = Surgical_Team_Details.objects.get(OP_Registration_Id = opregid)

                print(crew_ins)

                surgeonId = [ Surgeon.Doctor_ID for Surgeon in crew_ins.Surgeon.all() ]

                for datas in surgeonId:
                    
                    print(datas)

                    sur_ins = Doctor_Personal_Form_Detials.objects.get(Doctor_ID = datas)

                    doc_ins = OTDoctorcalendar(

                        Theatre = theatre_ins,
                        booking = booking_ins,
                        date = bdate,
                        time = btime,
                        Doctorid = sur_ins
                    )

                    doc_ins.save()

                assistantSurgeonId = [ Surgeon.Doctor_ID for Surgeon in crew_ins.Assistant_Surgeon.all() ]

                for datas in assistantSurgeonId:

                    print(datas)

                    sur_ins = Doctor_Personal_Form_Detials.objects.get(Doctor_ID = datas)

                    doc_ins = OTDoctorcalendar(

                        Theatre = theatre_ins,
                        booking = booking_ins,
                        date = bdate,
                        time = btime,
                        Doctorid = sur_ins
                    )

                    doc_ins.save()

                anaesthesiologistId = [ Surgeon.Doctor_ID for Surgeon in crew_ins.Anaesthesiologist.all() ]
                for datas in anaesthesiologistId:

                    print(datas)

                    sur_ins = Doctor_Personal_Form_Detials.objects.get(Doctor_ID = datas)

                    doc_ins = OTDoctorcalendar(

                        Theatre = theatre_ins,
                        booking = booking_ins,
                        date = bdate,
                        time = btime,
                        Doctorid = sur_ins
                    )

                    doc_ins.save()

            if BookingType == 'IP':

                crew_ins = Surgical_Team_Details.objects.get(IP_Registration_Id = RegistrationId)

                print(crew_ins)

                surgeonId = [ Surgeon.Doctor_ID for Surgeon in crew_ins.Surgeon.all() ]

                for datas in surgeonId:
                    
                    print(datas)

                    sur_ins = Doctor_Personal_Form_Detials.objects.get(Doctor_ID = datas)

                    doc_ins = OTDoctorcalendar(

                        Theatre = theatre_ins,
                        booking = booking_ins,
                        date = bdate,
                        time = btime,
                        Doctorid = sur_ins
                    )

                    doc_ins.save()

                assistantSurgeonId = [ Surgeon.Doctor_ID for Surgeon in crew_ins.Assistant_Surgeon.all() ]

                for datas in assistantSurgeonId:

                    print(datas)

                    sur_ins = Doctor_Personal_Form_Detials.objects.get(Doctor_ID = datas)

                    doc_ins = OTDoctorcalendar(

                        Theatre = theatre_ins,
                        booking = booking_ins,
                        date = bdate,
                        time = btime,
                        Doctorid = sur_ins
                    )

                    doc_ins.save()

                anaesthesiologistId = [ Surgeon.Doctor_ID for Surgeon in crew_ins.Anaesthesiologist.all() ]
                for datas in anaesthesiologistId:

                    print(datas)

                    sur_ins = Doctor_Personal_Form_Detials.objects.get(Doctor_ID = datas)

                    doc_ins = OTDoctorcalendar(

                        Theatre = theatre_ins,
                        booking = booking_ins,
                        date = bdate,
                        time = btime,
                        Doctorid = sur_ins
                    )

                    doc_ins.save()

            if BookingType == 'EMERGENCY':

                crew_ins = Surgical_Team_Details.objects.get(EMR_Registration_Id = RegistrationId)

                print(crew_ins)

                surgeonId = [ Surgeon.Doctor_ID for Surgeon in crew_ins.Surgeon.all() ]

                for datas in surgeonId:
                    
                    print(datas)

                    sur_ins = Doctor_Personal_Form_Detials.objects.get(Doctor_ID = datas)

                    doc_ins = OTDoctorcalendar(

                        Theatre = theatre_ins,
                        booking = booking_ins,
                        date = bdate,
                        time = btime,
                        Doctorid = sur_ins
                    )

                    doc_ins.save()

                assistantSurgeonId = [ Surgeon.Doctor_ID for Surgeon in crew_ins.Assistant_Surgeon.all() ]

                for datas in assistantSurgeonId:

                    print(datas)

                    sur_ins = Doctor_Personal_Form_Detials.objects.get(Doctor_ID = datas)

                    doc_ins = OTDoctorcalendar(

                        Theatre = theatre_ins,
                        booking = booking_ins,
                        date = bdate,
                        time = btime,
                        Doctorid = sur_ins
                    )

                    doc_ins.save()

                anaesthesiologistId = [ Surgeon.Doctor_ID for Surgeon in crew_ins.Anaesthesiologist.all() ]
                for datas in anaesthesiologistId:

                    print(datas)

                    sur_ins = Doctor_Personal_Form_Detials.objects.get(Doctor_ID = datas)

                    doc_ins = OTDoctorcalendar(

                        Theatre = theatre_ins,
                        booking = booking_ins,
                        date = bdate,
                        time = btime,
                        Doctorid = sur_ins
                    )

                    doc_ins.save()

            return JsonResponse({'success': 'details addes successfully'})





        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def OTCompletepatient_details(request):


    if request.method == 'GET':

        try:
            
            pat_ins = Theatre_Booking_Request_Details.objects.filter(Status = 'Completed')
            completed_list = []

            for datas in pat_ins:

                formatted_rdate =  datas.ReqDate.strftime('%d-%m-%y')
                
                formatted_bdate = datas.BookingDate.strftime('%d-%m-%y')

                data_list = {

                    'id':datas.id,
                    'ReqDate':formatted_rdate,
                    'ReqTime':datas.ReqTime,
                    'BookingType':datas.BookingType,
                    'Specialization_name':datas.Specialization.Speciality_Name,
                    'Specializationid':datas.Specialization.Speciality_Id,
                    'SurgeryName':datas.SurgeryName.Surgery_Name,
                    'Surgeryid':datas.SurgeryName.Surgery_Id,
                    'TheatreName':datas.TheatreName.TheatreName,
                    'Theatreid':datas.TheatreName.Ot_Id,
                    'theatrerent' : int(datas.TheatreName.Rent),
                    'DoctorID':datas.DoctorName.Doctor_ID,
                    'DoctorName':datas.DoctorName.First_Name,
                    'BookingDate':datas.BookingDate,
                    'bookingdate':formatted_bdate,
                    'BookingTime':datas.BookingTime,
                    'Duration':int(datas.Duration),
                    'OperationType':datas.OperationType,
                    'Priority':datas.Priority,
                    'Patientid':datas.Patientid.PatientId if datas.Patientid else None ,
                    'PatientName':datas.PatientName,
                    'Age':datas.Age,
                    'Gender':datas.Gender,
                    'UHIDNO':datas.UHIDNO,
                    'Status':datas.Status,
                    'Reason' : datas.Reason,
                    'CreatedBy':datas.CreatedBy
                }

                completed_list.append(data_list)

            for idx, Theatre in enumerate(completed_list, start=1):
                        Theatre["Sno"] = idx 

            return JsonResponse(completed_list,safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def OTConfirmedpatient_details(request):


    if request.method == 'GET':

        try:
            status = request.GET.get('status','')

            print(status)

            if status :

                pat_ins = Theatre_Booking_Request_Details.objects.filter(Status = status)
                print(pat_ins)
                completed_list = []

                for datas in pat_ins:

                    formatted_rdate =  datas.ReqDate.strftime('%d-%m-%y')
                    
                    formatted_bdate = datas.BookingDate.strftime('%d-%m-%y')


                    if datas.BookingType == 'OP':
                       data_list = {

                            'Booking_Id':datas.Booking_Id,
                            'ReqDate':formatted_rdate,
                            'ReqTime':datas.ReqTime,
                            'BookingType':datas.BookingType,
                            'Specialization_name':datas.Specialization.Speciality_Name,
                            'Specializationid':datas.Specialization.Speciality_Id,
                            'SurgeryName':datas.SurgeryName.Surgery_Name,
                            'Surgeryid':datas.SurgeryName.Surgery_Id,
                            'TheatreName':datas.TheatreName.TheatreName,
                            'Theatreid':datas.TheatreName.Ot_Id,
                            'theatrerent' : int(datas.TheatreName.Rent),
                            'DoctorID':datas.DoctorName.Doctor_ID,
                            'DoctorName':datas.DoctorName.First_Name,
                            'BookingDate':datas.BookingDate,
                            'bookingdate':formatted_bdate,
                            'BookingTime':datas.BookingTime,
                            'Duration':int(datas.Duration),
                            'OperationType':datas.OperationType,
                            'Priority':datas.Priority,
                            'patientId': datas.OP_Registration_Id.PatientId.PatientId,
                            'PatientName':datas.OP_Registration_Id.PatientId.FirstName,
                            'Age':datas.OP_Registration_Id.PatientId.Age,
                            'Gender':datas.OP_Registration_Id.PatientId.Gender,
                            'UHIDNO':datas.OP_Registration_Id.PatientId.UniqueIdNo,
                            'Status':datas.Status,
                            'Reason' : datas.Reason,
                            'CreatedBy':datas.CreatedBy,
                            'opregid' : datas.OP_Registration_Id.id,
                            'RegistrationId' : datas.OP_Registration_Id.Registration_Id if datas.OP_Registration_Id else None,
                            

                        }
                       completed_list.append(data_list)
                    elif  datas.BookingType == 'IP':
                
                        data_list = {

                            'Booking_Id':datas.Booking_Id,
                            'ReqDate':formatted_rdate,
                            'ReqTime':datas.ReqTime,
                            'BookingType':datas.BookingType,
                            'Specialization_name':datas.Specialization.Speciality_Name,
                            'Specializationid':datas.Specialization.Speciality_Id,
                            'SurgeryName':datas.SurgeryName.Surgery_Name,
                            'Surgeryid':datas.SurgeryName.Surgery_Id,
                            'TheatreName':datas.TheatreName.TheatreName,
                            'Theatreid':datas.TheatreName.Ot_Id,
                            'theatrerent' : int(datas.TheatreName.Rent),
                            'DoctorID':datas.DoctorName.Doctor_ID,
                            'DoctorName':datas.DoctorName.First_Name,
                            'BookingDate':datas.BookingDate,
                            'bookingdate':formatted_bdate,
                            'BookingTime':datas.BookingTime,
                            'Duration':int(datas.Duration),
                            'OperationType':datas.OperationType,
                            'Priority':datas.Priority,
                            'patientId': datas.IP_Registration_Id.PatientId.PatientId,
                            'PatientName':datas.IP_Registration_Id.PatientId.FirstName,
                            'Age':datas.IP_Registration_Id.PatientId.Age,
                            'Gender':datas.IP_Registration_Id.PatientId.Gender,
                            'UHIDNO':datas.IP_Registration_Id.PatientId.UniqueIdNo,
                            'Status':datas.Status,
                            'Reason' : datas.Reason,
                            'CreatedBy':datas.CreatedBy,
                            
                            'RegistrationId' : datas.IP_Registration_Id.Registration_Id if datas.IP_Registration_Id else None,
                            

                        }
                        completed_list.append(data_list)
                    elif  datas.BookingType == 'EMERGENCY':
                
                        data_list = {

                            'Booking_Id':datas.Booking_Id,
                            'ReqDate':formatted_rdate,
                            'ReqTime':datas.ReqTime,
                            'BookingType':datas.BookingType,
                            'Specialization_name':datas.Specialization.Speciality_Name,
                            'Specializationid':datas.Specialization.Speciality_Id,
                            'SurgeryName':datas.SurgeryName.Surgery_Name,
                            'Surgeryid':datas.SurgeryName.Surgery_Id,
                            'TheatreName':datas.TheatreName.TheatreName,
                            'Theatreid':datas.TheatreName.Ot_Id,
                            'theatrerent' : int(datas.TheatreName.Rent),
                            'DoctorID':datas.DoctorName.Doctor_ID,
                            'DoctorName':datas.DoctorName.First_Name,
                            'BookingDate':datas.BookingDate,
                            'bookingdate':formatted_bdate,
                            'BookingTime':datas.BookingTime,
                            'Duration':int(datas.Duration),
                            'OperationType':datas.OperationType,
                            'Priority':datas.Priority,
                            'patientId': datas.EMR_Registration_Id.PatientId.PatientId,
                            'PatientName':datas.EMR_Registration_Id.PatientId.FirstName,
                            'Age':datas.EMR_Registration_Id.PatientId.Age,
                            'Gender':datas.EMR_Registration_Id.PatientId.Gender,
                            'UHIDNO':datas.EMR_Registration_Id.PatientId.UniqueIdNo,
                            'Status':datas.Status,
                            'Reason' : datas.Reason,
                            'CreatedBy':datas.CreatedBy,
                            
                            'RegistrationId' : datas.EMR_Registration_Id.Registration_Id if datas.EMR_Registration_Id else None,
                            

                        }
                        completed_list.append(data_list)

                for idx, Theatre in enumerate(completed_list, start=1):
                            Theatre["Sno"] = idx 

                return JsonResponse(completed_list,safe=False)








            pat_ins = Theatre_Booking_Request_Details.objects.filter(Status = 'Confirmed')
            completed_list = []

            for datas in pat_ins:

                formatted_rdate =  datas.ReqDate.strftime('%d-%m-%y')
                
                formatted_bdate = datas.BookingDate.strftime('%d-%m-%y')

                if datas.BookingType == 'OP':
                       data_list = {

                            'Booking_Id':datas.Booking_Id,
                            'ReqDate':formatted_rdate,
                            'ReqTime':datas.ReqTime,
                            'BookingType':datas.BookingType,
                            'Specialization_name':datas.Specialization.Speciality_Name,
                            'Specializationid':datas.Specialization.Speciality_Id,
                            'SurgeryName':datas.SurgeryName.Surgery_Name,
                            'Surgeryid':datas.SurgeryName.Surgery_Id,
                            'TheatreName':datas.TheatreName.TheatreName,
                            'Theatreid':datas.TheatreName.Ot_Id,
                            'theatrerent' : int(datas.TheatreName.Rent),
                            'DoctorID':datas.DoctorName.Doctor_ID,
                            'DoctorName':datas.DoctorName.First_Name,
                            'BookingDate':datas.BookingDate,
                            'bookingdate':formatted_bdate,
                            'BookingTime':datas.BookingTime,
                            'Duration':int(datas.Duration),
                            'OperationType':datas.OperationType,
                            'Priority':datas.Priority,
                            'patientId': datas.OP_Registration_Id.PatientId.PatientId,
                            'PatientName':datas.OP_Registration_Id.PatientId.FirstName,
                            'Age':datas.OP_Registration_Id.PatientId.Age,
                            'Gender':datas.OP_Registration_Id.PatientId.Gender,
                            'UHIDNO':datas.OP_Registration_Id.PatientId.UniqueIdNo,
                            'Status':datas.Status,
                            'Reason' : datas.Reason,
                            'CreatedBy':datas.CreatedBy,
                            'opregid' : datas.OP_Registration_Id.id,
                            'RegistrationId' : datas.OP_Registration_Id.Registration_Id if datas.OP_Registration_Id else None,
                            

                        }
                       completed_list.append(data_list)
                elif  datas.BookingType == 'IP':
                
                        data_list = {

                            'Booking_Id':datas.Booking_Id,
                            'ReqDate':formatted_rdate,
                            'ReqTime':datas.ReqTime,
                            'BookingType':datas.BookingType,
                            'Specialization_name':datas.Specialization.Speciality_Name,
                            'Specializationid':datas.Specialization.Speciality_Id,
                            'SurgeryName':datas.SurgeryName.Surgery_Name,
                            'Surgeryid':datas.SurgeryName.Surgery_Id,
                            'TheatreName':datas.TheatreName.TheatreName,
                            'Theatreid':datas.TheatreName.Ot_Id,
                            'theatrerent' : int(datas.TheatreName.Rent),
                            'DoctorID':datas.DoctorName.Doctor_ID,
                            'DoctorName':datas.DoctorName.First_Name,
                            'BookingDate':datas.BookingDate,
                            'bookingdate':formatted_bdate,
                            'BookingTime':datas.BookingTime,
                            'Duration':int(datas.Duration),
                            'OperationType':datas.OperationType,
                            'Priority':datas.Priority,
                            'patientId': datas.IP_Registration_Id.PatientId.PatientId,
                            'PatientName':datas.IP_Registration_Id.PatientId.FirstName,
                            'Age':datas.IP_Registration_Id.PatientId.Age,
                            'Gender':datas.IP_Registration_Id.PatientId.Gender,
                            'UHIDNO':datas.IP_Registration_Id.PatientId.UniqueIdNo,
                            'Status':datas.Status,
                            'Reason' : datas.Reason,
                            'CreatedBy':datas.CreatedBy,
                            
                            'RegistrationId' : datas.IP_Registration_Id.Registration_Id if datas.IP_Registration_Id else None,
                            

                        }
                        completed_list.append(data_list)
                elif  datas.BookingType == 'EMERGENCY':
                
                        data_list = {

                            'Booking_Id':datas.Booking_Id,
                            'ReqDate':formatted_rdate,
                            'ReqTime':datas.ReqTime,
                            'BookingType':datas.BookingType,
                            'Specialization_name':datas.Specialization.Speciality_Name,
                            'Specializationid':datas.Specialization.Speciality_Id,
                            'SurgeryName':datas.SurgeryName.Surgery_Name,
                            'Surgeryid':datas.SurgeryName.Surgery_Id,
                            'TheatreName':datas.TheatreName.TheatreName,
                            'Theatreid':datas.TheatreName.Ot_Id,
                            'theatrerent' : int(datas.TheatreName.Rent),
                            'DoctorID':datas.DoctorName.Doctor_ID,
                            'DoctorName':datas.DoctorName.First_Name,
                            'BookingDate':datas.BookingDate,
                            'bookingdate':formatted_bdate,
                            'BookingTime':datas.BookingTime,
                            'Duration':int(datas.Duration),
                            'OperationType':datas.OperationType,
                            'Priority':datas.Priority,
                            'patientId': datas.EMR_Registration_Id.PatientId.PatientId,
                            'PatientName':datas.EMR_Registration_Id.PatientId.FirstName,
                            'Age':datas.EMR_Registration_Id.PatientId.Age,
                            'Gender':datas.EMR_Registration_Id.PatientId.Gender,
                            'UHIDNO':datas.EMR_Registration_Id.PatientId.UniqueIdNo,
                            'Status':datas.Status,
                            'Reason' : datas.Reason,
                            'CreatedBy':datas.CreatedBy,
                            
                            'RegistrationId' : datas.EMR_Registration_Id.Registration_Id if datas.EMR_Registration_Id else None,
                            

                        }
                        completed_list.append(data_list)

            for idx, Theatre in enumerate(completed_list, start=1):
                        Theatre["Sno"] = idx 

            return JsonResponse(completed_list,safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def OTQueuelist_details(request):

    if request.method  == 'GET':

        try:

            opd_request_ins = OPD_OtRequest_Details.objects.all()
            Theatrerequest_list = []
            
            
            for datas in opd_request_ins:
                print(datas.Status)


                if datas.Status == True:
                
                    created_at = datas.created_at 
                    formatted_bdate = datas.SurgeryRequestedDate.strftime('%d-%m-%y')
                    formatted_date =  created_at.strftime('%d-%m-%y')
                    formatted_time = created_at.strftime('%H:%M:%S')
                    
                    data_list = {

                        'id' : datas.OtRequest_Id,
                        'BookingDate' : formatted_bdate,
                        'ReqDate' : formatted_date,
                        'ReqTime' : formatted_time,
                        'SurgeryName' : datas.SurgeryName.Surgery_Name,
                        'PatientId':datas.Patient_Id.PatientId,
                        'PatientName':datas.Patient_Id.FirstName,
                        'BookingType':'OP'

                    }
                    Theatrerequest_list.append(data_list)



            return JsonResponse(Theatrerequest_list,safe=False)
            






        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def Theatre_booking_request_detail_by_Patient(request):

    if request.method == 'GET':

        try:

            Patientid = request.GET.get('Patientid', None)
           

            ip_request_ins = Theatre_Booking_Request_Details.objects.filter(Patientid=Patientid)
            
           
            iprequest_list = []
            
            
            for datas in ip_request_ins:

                
                
                created_at = datas.created_at 
              #  formatted_bdate = 
                formatted_rdate =  datas.ReqDate.strftime('%d-%m-%y')
                formatted_time = created_at.strftime('%H:%M:%S')
                formatted_bdate = datas.BookingDate.strftime('%d-%m-%y')
                
                data_list = {

                    'Booking_Id':datas.Booking_Id,
                    'ReqDate':formatted_rdate,
                    'ReqTime':datas.ReqTime,
                    'BookingType':datas.BookingType,
                    'Specialization_name':datas.Specialization.Speciality_Name,
                    'Specializationid':datas.Specialization.Speciality_Id,
                    'SurgeryName':datas.SurgeryName.Surgery_Name,
                    'Surgeryid':datas.SurgeryName.Surgery_Id,
                    'TheatreName':datas.TheatreName.TheatreName,
                    'Theatreid':datas.TheatreName.Ot_Id,
                    'DoctorID':datas.DoctorName.Doctor_ID,
                    'DoctorName':datas.DoctorName.First_Name,
                    'BookingDate':datas.BookingDate,
                    'bookingdate':formatted_bdate,
                    'BookingTime':datas.BookingTime,
                    'Duration':datas.Duration,
                    'OperationType':datas.OperationType,
                    'Priority':datas.Priority,
                    'Patientid':datas.Patientid.PatientId,
                    'PatientName':datas.PatientName,
                    'Age':datas.Age,
                    'Gender':datas.Gender,
                    'UHIDNO':datas.Patientid.UniqueIdNo,
                    'Status':datas.Status,
                    'OP_Registration_Id' : datas.OP_Registration_Id.Registration_Id if datas.OP_Registration_Id else None,
                    'IP_Registration_Id' : datas.IP_Registration_Id.Registration_Id if datas.IP_Registration_Id else None,
                    'EMR_Registration_Id' : datas.EMR_Registration_Id.Registration_Id if datas.EMR_Registration_Id else None,
                    'CreatedBy':datas.CreatedBy

                }
                iprequest_list.append(data_list)

                for idx,request in enumerate(iprequest_list,start=1):
                     request['Sno'] = idx

            return JsonResponse(iprequest_list,safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
   
@csrf_exempt
@require_http_methods(["GET"])
def Theatre_booking_request_Outside_details(request):

    if request.method == 'GET':

        try:

            Theatrerequest_list = []
            Theatre_ins = Theatre_Booking_Request_Details.objects.filter(BookingType='OutSide')
            
            for datas in Theatre_ins:

                formatted_rdate =  datas.ReqDate.strftime('%d-%m-%y')
                
                formatted_bdate = datas.BookingDate.strftime('%d-%m-%y')

                data_list = {

                    'id':datas.id,
                    'ReqDate':formatted_rdate,
                    'ReqTime':datas.ReqTime,
                    'BookingType':datas.BookingType,
                    'Specialization_name':datas.Specialization.Speciality_Name,
                    'Specializationid':datas.Specialization.Speciality_Id,
                    'SurgeryName':datas.SurgeryName.Surgery_Name,
                    'Surgeryid':datas.SurgeryName.Surgery_Id,
                    'TheatreName':datas.TheatreName.TheatreName,
                    'Theatreid':datas.TheatreName.Ot_Id,
                    'DoctorID':datas.DoctorName.Doctor_ID,
                    'DoctorName':datas.DoctorName.First_Name,
                    'BookingDate':datas.BookingDate,
                    'bookingdate':formatted_bdate,
                    'BookingTime':datas.BookingTime,
                    'Duration':datas.Duration,
                    'OperationType':datas.OperationType,
                    'Priority':datas.Priority,
                    'Patientid':datas.Patientid,
                    'PatientName':datas.PatientName,
                    'Age':datas.Age,
                    'Gender':datas.Gender,
                    'UHIDNO':datas.UHIDNO,
                    'Status':datas.Status,
                    'CreatedBy':datas.CreatedBy
                }

                Theatrerequest_list.append(data_list)
                for idx, Theatre in enumerate(Theatrerequest_list, start=1):
                        Theatre["Sno"] = idx 
            return JsonResponse(Theatrerequest_list,safe=False)




        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_item_details_for_consumables(request):

    if request.method == 'GET':

        try:
            location = request.GET.get('location', None)
            item_ins = Stock_Maintance_Table_Detials.objects.filter(Store_location_id = location )
            item_list = []
            for datas in item_ins:
                data_list = {
                    'id' : datas.id,
                    'Batch' : datas.Batch_No,
                    'productid' : datas.Product_Detials.id,
                    'productname' : f"{datas.Product_Detials.ItemName} {datas.Product_Detials.Strength}",
                    
                }
                item_list.append(data_list)
            

            return JsonResponse(item_list,safe=False)

        except Exception as e:

            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
        
@csrf_exempt
@require_http_methods(["GET"])
def get_store_name_for_OT(request):

    if request.method == 'GET':

        try:
            store_ins =  Inventory_Location_Master_Detials.objects.filter(Status=1).exclude(Store_Name__in=['OTPHARMACY'])
            
            store_list = []
            for datas in store_ins:
                data_list = {
                    'id':datas.Store_Id,
                    'Storetype':datas.Store_Type,
                    'Storename':datas.Store_Name,
                   
                }
                store_list.append(data_list)

            return JsonResponse(store_list,safe=False)

        except Exception as e:

            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_Theatre_name_for_OT_Calendar(request):

    if request.method == 'GET':

        try:
            ot_ins = OtTheaterMaster_Detials.objects.all()  
            ot_list = []
            for datas in ot_ins:
                SpecialityID = ', '.join(str(Speciality.Speciality_Id) for Speciality in datas.Speciality.all())
                Specialitynames = ', '.join(Speciality.Speciality_Name for Speciality in datas.Speciality.all())
                
                data_list = {
                    'id':datas.Ot_Id,
                    'otname':f'{datas.TheatreName} ({Specialitynames})',   
                }
                ot_list.append(data_list)

            return JsonResponse(ot_list,safe=False)

        except Exception as e:

            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

@csrf_exempt
def get_ot_availability(request):
    
    if request.method == 'GET':

        try:
            id = request.GET.get('id','')
            ot_avail_list = []
            print(id,'id')

            if id:
                Ot_avail_ins = OTTheatrecalendar.objects.filter(Theatre_id = id)
                
                for datas in Ot_avail_ins:
                    formatted_time = datetime.strptime(str(datas.time), "%H:%M:%S").strftime("%I:%M %p")
                    print(formatted_time)

                    data_list = {

                        'id' : datas.id,
                        'bdate' : datas.date,
                        'btime' : formatted_time,
                        'status' : datas.Status,
                        'Theatrename' : datas.Theatre.TheatreName,
                        'Theatreid' : datas.Theatre.Ot_Id,
                        'bookingid' : datas.booking.Booking_Id,
                        'bookingtype' : datas.booking.BookingType,
                        'priority' : datas.booking.Priority,
                        'operationtype' : datas.booking.OperationType,
                        'patientname' : datas.booking.PatientName
                    }
                    ot_avail_list.append(data_list)

                return JsonResponse(ot_avail_list,safe=False)
            
            else:

                 return JsonResponse(ot_avail_list,safe=False)

        except Exception as e:

            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

@csrf_exempt
def get_ot_doctor_availability(request):
    
    if request.method == 'GET':
        
        try:
            
            docid = request.GET.get('docid','')
            ot_doc_list = []

            if docid:
                
                 Ot_avail_ins = OTDoctorcalendar.objects.filter(Doctorid_id = docid)
                
                 for datas in Ot_avail_ins:
                    formatted_time = datetime.strptime(str(datas.time), "%H:%M:%S").strftime("%I:%M %p")
                    print(formatted_time)

                    data_list = {

                        'id' : datas.id,
                        'bdate' : datas.date,
                        'btime' : formatted_time,
                        'status' : datas.Status,
                        'Theatrename' : datas.Theatre.TheatreName,
                        'Theatreid' : datas.Theatre.Ot_Id,
                        'bookingid' : datas.booking.Booking_Id,
                        'bookingtype' : datas.booking.BookingType,
                        'priority' : datas.booking.Priority,
                        'operationtype' : datas.booking.OperationType,
                        'patientname' : datas.booking.PatientName,
                        'doctorname' : datas.Doctorid.First_Name,
                    }
                    ot_doc_list.append(data_list)

                 return JsonResponse(ot_doc_list,safe=False)
            
            else:

                 return JsonResponse(ot_doc_list,safe=False)
                









    
        except Exception as e:

            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

@csrf_exempt
@require_http_methods(["POST","OPTIONS","GET"])
def Consumable_details(request):

    if request.method == 'POST':

        try:


            data = json.loads(request.body)

            print(data)

            quantity = data.get('quantity','')
            Patientid = data.get('Patientid','')
            created_by = data.get('created_by','')
            categoryid = data.get('categoryid','')
            subcategoryid = data.get('subcategoryid','')
            tostoreid = data.get('tostoreid','')
            itemid = data.get('itemid','')
            id = data.get('id','')
            RegistrationId = data.get('RegistrationId','')
            BookingType = data.get('BookingType','')
            


            patient_ins = Patient_Detials.objects.get(pk=Patientid)
            category_ins = Product_Category_Product_Details.objects.get(pk=categoryid)
            subcategory_ins = SubCategory_Detailes.objects.get(pk=subcategoryid)
            store_ins = Inventory_Location_Master_Detials.objects.get(pk=tostoreid)
            item_ins = Stock_Maintance_Table_Detials.objects.get(pk=itemid)
            op_reg_id_ins = Patient_Appointment_Registration_Detials.objects.filter(Registration_Id=RegistrationId).first()  if RegistrationId else None
            ip_reg_id_ins = Patient_IP_Registration_Detials.objects.filter(Registration_Id = RegistrationId) .first() if RegistrationId else None
            emg_reg_id_ins = Patient_Emergency_Registration_Detials.objects.filter(Registration_Id = RegistrationId).first()  if RegistrationId else None


            consumable_ins = OTConsumable_Details(

                Category = category_ins,
                Subcategory = subcategory_ins,
                Store = store_ins,
                Product = item_ins,
                Patientid = patient_ins,
                Quantity = quantity,
                CreatedBy = created_by,
                BookingType = BookingType,
                OP_Registration_Id = op_reg_id_ins,
                IP_Registration_Id = ip_reg_id_ins,
                EMR_Registration_Id = emg_reg_id_ins,

            )

            consumable_ins.save()

            return JsonResponse({'success': 'consumable added successfully'})

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

    if request.method == 'GET':

        try:

            RegistrationId = request.GET.get('RegistrationId', None)
            BookingType = request.GET.get('BookingType', None)

            if BookingType == "OP":

                con_ins = OTConsumable_Details.objects.filter(OP_Registration_Id = RegistrationId)
                consumable_list = []
                print(con_ins)

                for datas in con_ins:
                    data_list = {

                    'id' : datas.id,
                    'category' : datas.Category.id,
                    'Categoryname' : datas.Category.ProductCategory_Name,
                    'Subcategory' : datas.Subcategory.SubCategory_Id,
                    'Subcategoryname' : datas.Subcategory.SubCategoryName,
                    'ToStoreid' : datas.Store.Store_Id,
                    'ToStorename' : datas.Store.Store_Name,
                    'Productname' : f'{datas.Product.Product_Detials.ItemName} {datas.Product.Product_Detials.Strength}',
                    'productid' : datas.Product.Product_Detials.id,
                    'Batchno' : datas.Product.Batch_No,
                    'Quantity' : datas.Quantity,
                    'isEditing' : False,
                    'price' : datas.Product.Sellable_qty_price,
                    'checkboxes' : ['false' for i in range(int(datas.Quantity))],
                    'OP_Registration_Id' : datas.OP_Registration_Id.Registration_Id if datas.OP_Registration_Id else None,
                    'IP_Registration_Id' : datas.IP_Registration_Id.Registration_Id if datas.IP_Registration_Id else None,
                    'EMR_Registration_Id' : datas.EMR_Registration_Id.Registration_Id if datas.EMR_Registration_Id else None


                }
                consumable_list.append(data_list)

            elif BookingType == "IP":

                con_ins = OTConsumable_Details.objects.filter(IP_Registration_Id = RegistrationId)
                consumable_list = []
                print(con_ins)

                for datas in con_ins:
                    data_list = {

                    'id' : datas.id,
                    'category' : datas.Category.id,
                    'Categoryname' : datas.Category.ProductCategory_Name,
                    'Subcategory' : datas.Subcategory.SubCategory_Id,
                    'Subcategoryname' : datas.Subcategory.SubCategoryName,
                    'ToStoreid' : datas.Store.Store_Id,
                    'ToStorename' : datas.Store.Store_Name,
                    'Productname' : f'{datas.Product.Product_Detials.ItemName} {datas.Product.Product_Detials.Strength}',
                    'productid' : datas.Product.Product_Detials.id,
                    'Batchno' : datas.Product.Batch_No,
                    'Quantity' : datas.Quantity,
                    'isEditing' : False,
                    'price' : datas.Product.Sellable_qty_price,
                    'checkboxes' : ['false' for i in range(int(datas.Quantity))],
                    'OP_Registration_Id' : datas.OP_Registration_Id.Registration_Id if datas.OP_Registration_Id else None,
                    'IP_Registration_Id' : datas.IP_Registration_Id.Registration_Id if datas.IP_Registration_Id else None,
                    'EMR_Registration_Id' : datas.EMR_Registration_Id.Registration_Id if datas.EMR_Registration_Id else None


                         }
                    consumable_list.append(data_list)

            elif BookingType == "EMERGENCY":

                con_ins = OTConsumable_Details.objects.filter(EMR_Registration_Id = RegistrationId)
                consumable_list = []
                print(con_ins)

                for datas in con_ins:
                    data_list = {

                    'id' : datas.id,
                    'category' : datas.Category.id,
                    'Categoryname' : datas.Category.ProductCategory_Name,
                    'Subcategory' : datas.Subcategory.SubCategory_Id,
                    'Subcategoryname' : datas.Subcategory.SubCategoryName,
                    'ToStoreid' : datas.Store.Store_Id,
                    'ToStorename' : datas.Store.Store_Name,
                    'Productname' : f'{datas.Product.Product_Detials.ItemName} {datas.Product.Product_Detials.Strength}',
                    'productid' : datas.Product.Product_Detials.id,
                    'Batchno' : datas.Product.Batch_No,
                    'Quantity' : datas.Quantity,
                    'isEditing' : False,
                    'price' : datas.Product.Sellable_qty_price,
                    'checkboxes' : ['false' for i in range(int(datas.Quantity))],
                    'OP_Registration_Id' : datas.OP_Registration_Id.Registration_Id if datas.OP_Registration_Id else None,
                    'IP_Registration_Id' : datas.IP_Registration_Id.Registration_Id if datas.IP_Registration_Id else None,
                    'EMR_Registration_Id' : datas.EMR_Registration_Id.Registration_Id if datas.EMR_Registration_Id else None


                }
                    consumable_list.append(data_list)


                

            return JsonResponse(consumable_list,safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

@csrf_exempt
@require_http_methods(["POST","OPTIONS","GET"])
def Consignment_details(request):

    if request.method == 'POST':

        try:


            data = json.loads(request.body)

            print(data)

            consignment = data.get('consignment','')
            Patientid = data.get('Patientid','')
            quantity = data.get('quantity','')
            id = data.get('id','')
            created_by = data.get('created_by','')
            RegistrationId = data.get('RegistrationId','')
            BookingType = data.get('BookingType','')
            


            patient_ins = Patient_Detials.objects.get(pk=Patientid)
            op_reg_id_ins = Patient_Appointment_Registration_Detials.objects.filter(Registration_Id=RegistrationId).first()  if RegistrationId else None
            ip_reg_id_ins = Patient_IP_Registration_Detials.objects.filter(Registration_Id = RegistrationId) .first() if RegistrationId else None
            emg_reg_id_ins = Patient_Emergency_Registration_Detials.objects.filter(Registration_Id = RegistrationId).first()  if RegistrationId else None

            

            consignment_ins = OTConsignment_Details(

                Consignment = consignment,
                Quantity = quantity,
                CreatedBy = created_by,
                Patientid = patient_ins,
                BookingType= BookingType,
                OP_Registration_Id = op_reg_id_ins,
                IP_Registration_Id = ip_reg_id_ins,
                EMR_Registration_Id = emg_reg_id_ins,
            )

            consignment_ins.save()

            return JsonResponse({'success': 'consignment added successfully'})

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

    if request.method == 'GET':

        try:

            RegistrationId = request.GET.get('RegistrationId', None)
            BookingType = request.GET.get('BookingType', None)

            if BookingType == "OP":


                con_ins = OTConsignment_Details.objects.filter(OP_Registration_Id = RegistrationId)
                Consignment_list = []
                print(con_ins)

                for datas in con_ins:


                    data_list = {

                        'id' : datas.id,
                        'consignmentname' : datas.Consignment,
                        'quantity' : datas.Quantity,
                        'patientid' : datas.Patientid.PatientId,
                        'OP_Registration_Id' : datas.OP_Registration_Id.Registration_Id if datas.OP_Registration_Id else None,
                        'IP_Registration_Id' : datas.IP_Registration_Id.Registration_Id if datas.IP_Registration_Id else None,
                        'EMR_Registration_Id' : datas.EMR_Registration_Id.Registration_Id if datas.EMR_Registration_Id else None

                    }
                    Consignment_list.append(data_list)

            if BookingType == "IP":


                con_ins = OTConsignment_Details.objects.filter(IP_Registration_Id = RegistrationId)
                Consignment_list = []
                print(con_ins)

                for datas in con_ins:


                    data_list = {

                        'id' : datas.id,
                        'consignmentname' : datas.Consignment,
                        'quantity' : datas.Quantity,
                        'patientid' : datas.Patientid.PatientId,
                        'OP_Registration_Id' : datas.OP_Registration_Id.Registration_Id if datas.OP_Registration_Id else None,
                        'IP_Registration_Id' : datas.IP_Registration_Id.Registration_Id if datas.IP_Registration_Id else None,
                        'EMR_Registration_Id' : datas.EMR_Registration_Id.Registration_Id if datas.EMR_Registration_Id else None

                    }
                    Consignment_list.append(data_list)

            if BookingType == "EMERGENCY":


                con_ins = OTConsignment_Details.objects.filter(EMR_Registration_Id = RegistrationId)
                Consignment_list = []
                print(con_ins)

                for datas in con_ins:


                    data_list = {

                        'id' : datas.id,
                        'consignmentname' : datas.Consignment,
                        'quantity' : datas.Quantity,
                        'patientid' : datas.Patientid.PatientId,
                        'OP_Registration_Id' : datas.OP_Registration_Id.Registration_Id if datas.OP_Registration_Id else None,
                        'IP_Registration_Id' : datas.IP_Registration_Id.Registration_Id if datas.IP_Registration_Id else None,
                        'EMR_Registration_Id' : datas.EMR_Registration_Id.Registration_Id if datas.EMR_Registration_Id else None

                    }
                    Consignment_list.append(data_list)









            return JsonResponse(Consignment_list,safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

@csrf_exempt
@require_http_methods(["POST","OPTIONS","GET"])
def Equipment_details(request):

    if request.method == 'POST':

        try:


            data = json.loads(request.body)

            print(data)

            equipment = data.get('equipment','')
            Patientid = data.get('Patientid','')
            quantity = data.get('quantity','')
            id = data.get('id','')
            created_by = data.get('created_by','')
            RegistrationId = data.get('RegistrationId','')
            BookingType = data.get('BookingType','')
            


            patient_ins = Patient_Detials.objects.get(pk=Patientid)
            op_reg_id_ins = Patient_Appointment_Registration_Detials.objects.filter(Registration_Id=RegistrationId).first()  if RegistrationId else None
            ip_reg_id_ins = Patient_IP_Registration_Detials.objects.filter(Registration_Id = RegistrationId) .first() if RegistrationId else None
            emg_reg_id_ins = Patient_Emergency_Registration_Detials.objects.filter(Registration_Id = RegistrationId).first()  if RegistrationId else None


            equipment_ins = OTEquipment_Details(

                Equipment = equipment,
                Quantity = quantity,
                CreatedBy = created_by,
                Patientid = patient_ins,
                BookingType = BookingType,
                OP_Registration_Id = op_reg_id_ins,
                IP_Registration_Id = ip_reg_id_ins,
                EMR_Registration_Id = emg_reg_id_ins,
            )

            equipment_ins.save()

            return JsonResponse({'success': 'Equipment added successfully'})

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

    if request.method == 'GET':

        try:

            RegistrationId = request.GET.get('RegistrationId', None)
            BookingType = request.GET.get('BookingType', None)

            if BookingType == 'OP':

                con_ins = OTEquipment_Details.objects.filter(OP_Registration_Id = RegistrationId)
                Consignment_list = []
                print(con_ins)

                for datas in con_ins:


                    data_list = {

                        'id' : datas.id,
                        'equipmentname' : datas.Equipment,
                        'quantity' : datas.Quantity,
                        'patientid' : datas.Patientid.PatientId,
                        'OP_Registration_Id' : datas.OP_Registration_Id.Registration_Id if datas.OP_Registration_Id else None,
                        'IP_Registration_Id' : datas.IP_Registration_Id.Registration_Id if datas.IP_Registration_Id else None,
                        'EMR_Registration_Id' : datas.EMR_Registration_Id.Registration_Id if datas.EMR_Registration_Id else None

                    }
                    Consignment_list.append(data_list)

            if BookingType == 'IP':

                con_ins = OTEquipment_Details.objects.filter(IP_Registration_Id = RegistrationId)
                Consignment_list = []
                print(con_ins)

                for datas in con_ins:


                    data_list = {

                        'id' : datas.id,
                        'equipmentname' : datas.Equipment,
                        'quantity' : datas.Quantity,
                        'patientid' : datas.Patientid.PatientId,
                        'OP_Registration_Id' : datas.OP_Registration_Id.Registration_Id if datas.OP_Registration_Id else None,
                        'IP_Registration_Id' : datas.IP_Registration_Id.Registration_Id if datas.IP_Registration_Id else None,
                        'EMR_Registration_Id' : datas.EMR_Registration_Id.Registration_Id if datas.EMR_Registration_Id else None

                    }
                    Consignment_list.append(data_list)

            if BookingType == 'EMERGENCY':

                con_ins = OTEquipment_Details.objects.filter(EMR_Registration_Id = RegistrationId)
                Consignment_list = []
                print(con_ins)

                for datas in con_ins:


                    data_list = {

                        'id' : datas.id,
                        'equipmentname' : datas.Equipment,
                        'quantity' : datas.Quantity,
                        'patientid' : datas.Patientid.PatientId,
                        'OP_Registration_Id' : datas.OP_Registration_Id.Registration_Id if datas.OP_Registration_Id else None,
                        'IP_Registration_Id' : datas.IP_Registration_Id.Registration_Id if datas.IP_Registration_Id else None,
                        'EMR_Registration_Id' : datas.EMR_Registration_Id.Registration_Id if datas.EMR_Registration_Id else None

                    }
                    Consignment_list.append(data_list)




            return JsonResponse(Consignment_list,safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

@csrf_exempt
@require_http_methods(["POST","OPTIONS","GET"])
def Surgical_Team_details(request):
    

    if request.method == 'POST':

        try:
            data = json.loads(request.body)
            print(data)
            id = data.get('id','')
            surgeonId = data.get('surgeon','')
           # surgeonId = surgeon.split(', ') if surgeon else None
            
            assistantSurgeonId = data.get('assistantSurgeon','')
           # assistantSurgeonId = assistantSurgeon.split(', ') if assistantSurgeon else None
            anaesthesiologistId = data.get('anaesthesiologist','')
           # anaesthesiologistId = anaesthesiologist.split(', ') if anaesthesiologist else None
            scrubNurseId = data.get('scrubNurse','')
           # scrubNurseId = scrubNurse.split(', ') if scrubNurse else None
            technicianId = data.get('technician','')
           # technicianId = technician.split(', ') if technician else None
            circulatingNurseId = data.get('circulatingNurse','')
           # circulatingNurseId = circulatingNurse.split(', ') if circulatingNurse else None
            othersId = data.get('others','')
           # othersId = others.split(', ') if others else None
            created_by = data.get('created_by','')
            Patientid = data.get('Patientid','')
            RegistrationId = data.get('RegistrationId','')
            BookingType = data.get('BookingType','')
            
            


            try:

                surgeon_ins = None
                assistantSurgeon_ins = None
                anaesthesiologist_ins = None
                scrubNurse_ins = None
                technician_ins = None
                circulatingNurse_ins = None
                others_ins = None

                surgeon_ins = Doctor_Personal_Form_Detials.objects.filter(Doctor_ID__in = surgeonId)
                assistantSurgeon_ins = Doctor_Personal_Form_Detials.objects.filter(Doctor_ID__in = assistantSurgeonId)
                anaesthesiologist_ins = Doctor_Personal_Form_Detials.objects.filter(Doctor_ID__in=anaesthesiologistId)
                scrubNurse_ins = Employee_Personal_Form_Detials.objects.filter(Employee_ID__in = scrubNurseId)
                technician_ins = Employee_Personal_Form_Detials.objects.filter(Employee_ID__in = technicianId)
                circulatingNurse_ins = Employee_Personal_Form_Detials.objects.filter(Employee_ID__in = circulatingNurseId)
                others_ins = Employee_Personal_Form_Detials.objects.filter(Employee_ID__in = othersId)
                Patient_ins = Patient_Detials.objects.get(pk=Patientid)
                op_reg_id_ins = Patient_Appointment_Registration_Detials.objects.filter(Registration_Id=RegistrationId).first()  if RegistrationId else None
                ip_reg_id_ins = Patient_IP_Registration_Detials.objects.filter(Registration_Id = RegistrationId).first()  if RegistrationId else None
                emg_reg_id_ins = Patient_Emergency_Registration_Detials.objects.filter(Registration_Id = RegistrationId).first()  if RegistrationId else None

            except (Doctor_Personal_Form_Detials.DoesNotExist, Employee_Personal_Form_Detials.DoesNotExist):
                return JsonResponse({'error': 'Invalid Doctor or Employee'})

            if id:

                crew_ins = Surgical_Team_Details.objects.get(pk=id)

                crew_ins.CreatedBy = created_by
                crew_ins.save()

                crew_ins.Surgeon.set(surgeon_ins)
                crew_ins.Assistant_Surgeon.set(assistantSurgeon_ins)
                crew_ins.Anaesthesiologist.set(anaesthesiologist_ins)
                crew_ins.Scrub_Nurse.set(scrubNurse_ins)
                crew_ins.Circulating_Nurse.set(circulatingNurse_ins)
                crew_ins.Helper.set(others_ins)

                return JsonResponse({'success': 'CREW Updated Successfully'})

            Crew_ins = Surgical_Team_Details.objects.create(

                    Patientid = Patient_ins,
                    OP_Registration_Id = op_reg_id_ins,
                    IP_Registration_Id = ip_reg_id_ins,
                    EMR_Registration_Id = emg_reg_id_ins,
                    BookingType = BookingType,
                    CreatedBy = created_by  )


            try:
                if surgeon_ins.exists() :   
                    Crew_ins.Surgeon.set(surgeon_ins) 
            except Exception as e:
                print(f"An error occurred: {str(e)}")

            try:
                if assistantSurgeon_ins.exists():
                    Crew_ins.Assistant_Surgeon.set(assistantSurgeon_ins) 
            except Exception as e:
                print(f"An error occurred: {str(e)}")
            try:
                if anaesthesiologist_ins.exists():
                    Crew_ins.Anaesthesiologist.set(anaesthesiologist_ins)
            except Exception as e:
                print(f"An error occurred: {str(e)}")

            try:
                if scrubNurse_ins.exists():
                    Crew_ins.Scrub_Nurse.set(scrubNurse_ins)
            except Exception as e:
                print(f"An error occurred: {str(e)}")

            try:
                if technician_ins.exists():
                    Crew_ins.Technician.set(technician_ins)
            except Exception as e:
                print(f"An error occurred: {str(e)}")

            try:
                if circulatingNurse_ins.exists():
                    Crew_ins.Circulating_Nurse.set(circulatingNurse_ins)
            except Exception as e:
                print(f"An error occurred: {str(e)}")

            try:
                if others_ins.exists():
                    Crew_ins.Helper.set(others_ins)
            except Exception as e:
                print(f"An error occurred: {str(e)}")
        


            return JsonResponse({'success': 'CREW Added Successfully'})

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

    if request.method == 'GET':

        try:

         RegistrationId = request.GET.get('RegistrationId', None)
         BookingType = request.GET.get('BookingType', None)

         if BookingType == "OP":
         
            crew_ins = Surgical_Team_Details.objects.get(OP_Registration_Id=RegistrationId)
            
            crew_list = []
            surgeonId = ', '.join(str(Surgeon.Doctor_ID) for Surgeon in crew_ins.Surgeon.all())
            surgeon = ', '.join(str(Surgeon.First_Name) for Surgeon in crew_ins.Surgeon.all())

            assistantSurgeonId = ', '.join(str(Surgeon.Doctor_ID) for Surgeon in crew_ins.Assistant_Surgeon.all())
            assistantSurgeon = ', '.join(str(Surgeon.First_Name) for Surgeon in crew_ins.Assistant_Surgeon.all())

            anaesthesiologistId = ', '.join(str(Surgeon.Doctor_ID) for Surgeon in crew_ins.Anaesthesiologist.all())
            anaesthesiologist = ', '.join(str(Surgeon.First_Name) for Surgeon in crew_ins.Anaesthesiologist.all())

            scrubNurseId = ', '.join(str(Surgeon.Employee_ID) for Surgeon in crew_ins.Scrub_Nurse.all())
            scrubNurse = ', '.join(str(Surgeon.First_Name) for Surgeon in crew_ins.Scrub_Nurse.all())

            circulatingNurseId= ', '.join(str(Surgeon.Employee_ID) for Surgeon in crew_ins.Circulating_Nurse.all())
            circulatingNurse= ', '.join(str(Surgeon.First_Name) for Surgeon in crew_ins.Circulating_Nurse.all())

            technicianId = ', '.join(str(Surgeon.Employee_ID) for Surgeon in crew_ins.Technician.all())
            technician = ', '.join(str(Surgeon.First_Name) for Surgeon in crew_ins.Technician.all())

            othersId = ', '.join(str(Surgeon.Employee_ID) for Surgeon in crew_ins.Helper.all())
            others = ', '.join(str(Surgeon.First_Name) for Surgeon in crew_ins.Helper.all())

            Crew_dict = {
                'id': crew_ins.id,
                'surgeonId' : surgeonId,
                'surgeon' : surgeon,
                'assistantSurgeonId' : assistantSurgeonId,
                'assistantSurgeon' : assistantSurgeon,
                'anaesthesiologistId' : anaesthesiologistId,
                'anaesthesiologist' : anaesthesiologist,
                'scrubNurseId' : scrubNurseId,
                'scrubNurse' : scrubNurse,
                'circulatingNurseId' : circulatingNurseId,
                'circulatingNurse' : circulatingNurse,
                'technicianId' : technicianId,
                'technician' : technician,
                'othersId' : othersId,
                'others' : others,
                'patientid' : crew_ins.Patientid.PatientId,
                'OP_Registration_Id' : crew_ins.OP_Registration_Id.Registration_Id if crew_ins.OP_Registration_Id else None,
                'IP_Registration_Id' : crew_ins.IP_Registration_Id.Registration_Id if crew_ins.IP_Registration_Id else None,
                'EMR_Registration_Id' : crew_ins.EMR_Registration_Id.Registration_Id if crew_ins.EMR_Registration_Id else None
                

            }
            crew_list.append(Crew_dict)

         if BookingType == "IP":
         
            crew_ins = Surgical_Team_Details.objects.get(IP_Registration_Id=RegistrationId)
            
            crew_list = []
            surgeonId = ', '.join(str(Surgeon.Doctor_ID) for Surgeon in crew_ins.Surgeon.all())
            surgeon = ', '.join(str(Surgeon.First_Name) for Surgeon in crew_ins.Surgeon.all())

            assistantSurgeonId = ', '.join(str(Surgeon.Doctor_ID) for Surgeon in crew_ins.Assistant_Surgeon.all())
            assistantSurgeon = ', '.join(str(Surgeon.First_Name) for Surgeon in crew_ins.Assistant_Surgeon.all())

            anaesthesiologistId = ', '.join(str(Surgeon.Doctor_ID) for Surgeon in crew_ins.Anaesthesiologist.all())
            anaesthesiologist = ', '.join(str(Surgeon.First_Name) for Surgeon in crew_ins.Anaesthesiologist.all())

            scrubNurseId = ', '.join(str(Surgeon.Employee_ID) for Surgeon in crew_ins.Scrub_Nurse.all())
            scrubNurse = ', '.join(str(Surgeon.First_Name) for Surgeon in crew_ins.Scrub_Nurse.all())

            circulatingNurseId= ', '.join(str(Surgeon.Employee_ID) for Surgeon in crew_ins.Circulating_Nurse.all())
            circulatingNurse= ', '.join(str(Surgeon.First_Name) for Surgeon in crew_ins.Circulating_Nurse.all())

            technicianId = ', '.join(str(Surgeon.Employee_ID) for Surgeon in crew_ins.Technician.all())
            technician = ', '.join(str(Surgeon.First_Name) for Surgeon in crew_ins.Technician.all())

            othersId = ', '.join(str(Surgeon.Employee_ID) for Surgeon in crew_ins.Helper.all())
            others = ', '.join(str(Surgeon.First_Name) for Surgeon in crew_ins.Helper.all())

            Crew_dict = {
                'id': crew_ins.id,
                'surgeonId' : surgeonId,
                'surgeon' : surgeon,
                'assistantSurgeonId' : assistantSurgeonId,
                'assistantSurgeon' : assistantSurgeon,
                'anaesthesiologistId' : anaesthesiologistId,
                'anaesthesiologist' : anaesthesiologist,
                'scrubNurseId' : scrubNurseId,
                'scrubNurse' : scrubNurse,
                'circulatingNurseId' : circulatingNurseId,
                'circulatingNurse' : circulatingNurse,
                'technicianId' : technicianId,
                'technician' : technician,
                'othersId' : othersId,
                'others' : others,
                'patientid' : crew_ins.Patientid.PatientId,
                'OP_Registration_Id' : crew_ins.OP_Registration_Id.Registration_Id if crew_ins.OP_Registration_Id else None,
                'IP_Registration_Id' : crew_ins.IP_Registration_Id.Registration_Id if crew_ins.IP_Registration_Id else None,
                'EMR_Registration_Id' : crew_ins.EMR_Registration_Id.Registration_Id if crew_ins.EMR_Registration_Id else None
                

            }
            crew_list.append(Crew_dict)

         if BookingType == "EMERGENCY":
         
            crew_ins = Surgical_Team_Details.objects.get(EMR_Registration_Id=RegistrationId)
            
            crew_list = []
            surgeonId = ', '.join(str(Surgeon.Doctor_ID) for Surgeon in crew_ins.Surgeon.all())
            surgeon = ', '.join(str(Surgeon.First_Name) for Surgeon in crew_ins.Surgeon.all())

            assistantSurgeonId = ', '.join(str(Surgeon.Doctor_ID) for Surgeon in crew_ins.Assistant_Surgeon.all())
            assistantSurgeon = ', '.join(str(Surgeon.First_Name) for Surgeon in crew_ins.Assistant_Surgeon.all())

            anaesthesiologistId = ', '.join(str(Surgeon.Doctor_ID) for Surgeon in crew_ins.Anaesthesiologist.all())
            anaesthesiologist = ', '.join(str(Surgeon.First_Name) for Surgeon in crew_ins.Anaesthesiologist.all())

            scrubNurseId = ', '.join(str(Surgeon.Employee_ID) for Surgeon in crew_ins.Scrub_Nurse.all())
            scrubNurse = ', '.join(str(Surgeon.First_Name) for Surgeon in crew_ins.Scrub_Nurse.all())

            circulatingNurseId= ', '.join(str(Surgeon.Employee_ID) for Surgeon in crew_ins.Circulating_Nurse.all())
            circulatingNurse= ', '.join(str(Surgeon.First_Name) for Surgeon in crew_ins.Circulating_Nurse.all())

            technicianId = ', '.join(str(Surgeon.Employee_ID) for Surgeon in crew_ins.Technician.all())
            technician = ', '.join(str(Surgeon.First_Name) for Surgeon in crew_ins.Technician.all())

            othersId = ', '.join(str(Surgeon.Employee_ID) for Surgeon in crew_ins.Helper.all())
            others = ', '.join(str(Surgeon.First_Name) for Surgeon in crew_ins.Helper.all())

            Crew_dict = {
                'id': crew_ins.id,
                'surgeonId' : surgeonId,
                'surgeon' : surgeon,
                'assistantSurgeonId' : assistantSurgeonId,
                'assistantSurgeon' : assistantSurgeon,
                'anaesthesiologistId' : anaesthesiologistId,
                'anaesthesiologist' : anaesthesiologist,
                'scrubNurseId' : scrubNurseId,
                'scrubNurse' : scrubNurse,
                'circulatingNurseId' : circulatingNurseId,
                'circulatingNurse' : circulatingNurse,
                'technicianId' : technicianId,
                'technician' : technician,
                'othersId' : othersId,
                'others' : others,
                'patientid' : crew_ins.Patientid.PatientId,
                'OP_Registration_Id' : crew_ins.OP_Registration_Id.Registration_Id if crew_ins.OP_Registration_Id else None,
                'IP_Registration_Id' : crew_ins.IP_Registration_Id.Registration_Id if crew_ins.IP_Registration_Id else None,
                'EMR_Registration_Id' : crew_ins.EMR_Registration_Id.Registration_Id if crew_ins.EMR_Registration_Id else None
                

            }
            crew_list.append(Crew_dict)

         return JsonResponse(crew_list,safe=False)


        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_Ward_details_by_floor_for_ot(request):
    try:
        if request.method == 'GET':
            Floor = request.GET.get('Floor')
            
            Ward_ins = WardType_Master_Detials.objects.filter(Floor_Name_id=Floor).exclude(Ward_Name="GENERAL")
            
            bed_details = []
            for datas in Ward_ins:

                print(datas.Ward_Name,'wardname')
                if datas.Ward_Name not in ["ICU", "CASUALITY"]:
                    continue
                
                rooms = Room_Master_Detials.objects.filter(Ward_Name_id=datas.Ward_Id)
                unique_rooms = {}
                
                for room in rooms:
                    room_no = room.Room_No
                    if room_no not in unique_rooms:
                        unique_rooms[room_no] = {
                            "RoomNo": room_no,
                            "Beds": []
                        }
                    unique_rooms[room_no]["Beds"].append({
                        "BedId": room.Room_Id,
                        "BedNo": room.Bed_No,
                        "status": room.Booking_Status
                    })
                
                ward_data = {
                    'WardId': datas.Ward_Id,
                    'WardName': datas.Ward_Name,
                    "Rooms": list(unique_rooms.values())
                }
                bed_details.append(ward_data)
            
            return JsonResponse(bed_details, safe=False)
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'An internal server error occurred'}, status=500)


@csrf_exempt
@require_http_methods(["POST","OPTIONS","GET"])
def OT_Billing_details(request):

    if request.method == 'POST':

        try:

            data_list = json.loads(request.body)

            # Extract RegistrationId
            RegistrationId = data_list.get('RegistrationId', '')

            print(RegistrationId, 'RegistrationId')
            print(data_list)

            # Validate RegistrationId
            if not RegistrationId:
                return JsonResponse({"error": "RegistrationId is required"}, status=400)

            # Get related registration details
            op_reg_id_ins = Patient_Appointment_Registration_Detials.objects.filter(Registration_Id=RegistrationId).first()
            ip_reg_id_ins = Patient_IP_Registration_Detials.objects.filter(Registration_Id=RegistrationId).first()
            emg_reg_id_ins = Patient_Emergency_Registration_Detials.objects.filter(Registration_Id=RegistrationId).first()

            print(op_reg_id_ins,'op_reg_id_ins')
            print(ip_reg_id_ins,'ip_reg_id_ins')
            print(emg_reg_id_ins,'emg_reg_id_ins')

            entries = []

            ot_charges = [value for key, value in data_list.items() if key != "RegistrationId"]
            for data in ot_charges:

                print(data, 'data')

              
                service_name = data.get("serviceName", "")
                name = data.get("units", "")
                per_hr_unit_cost = data.get("perHourCost", "")
                quantity = data.get("quantity", "")
                amount = data.get("amount", "")

              
                ot_billing = OT_Billing(
                    Service_name=service_name,
                    Name=name,
                    Per_hr_unit_cost=per_hr_unit_cost,
                    Quantity=quantity,
                    Amount=amount,
                    OP_Registration_Id=op_reg_id_ins,
                    IP_Registration_Id=ip_reg_id_ins,
                    EMR_Registration_Id=emg_reg_id_ins,
                )
                entries.append(ot_billing)

            # Bulk insert the entries
            OT_Billing.objects.bulk_create(entries)

            return JsonResponse({"message": "Data saved successfully"})
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
