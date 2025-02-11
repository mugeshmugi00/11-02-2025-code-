from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from Insurance.models import *
from django.db.models import Q
import json








@csrf_exempt
@require_http_methods(['GET'])
def Signal_PatientEntry_Get_Details(request):
    try:
        Patient_arr = []

        Status=request.GET.get('Filterby')
        ServiceType=request.GET.get('ServiceType')
        PatientId=request.GET.get('PatientId')
        PatientName=request.GET.get('PatientName')

        query = Q()

        if Status:
            if Status !='ALL':
                query &= Q(Papersstatus=Status)
        if ServiceType:
            query &= Q(Patient_ServiesType=ServiceType)

        insurance_entries = Insuranse_Patient_Entery_Details.objects.filter(query)

        for entry in insurance_entries:
            related_instance = entry.IP_Registration  
            Patient_inst = getattr(related_instance, 'PatientId', None)  

            if Patient_inst is not None:
                Patient_dec = {
                    'id': entry.pk,
                    'PatientServiesType': getattr(entry, 'Patient_ServiesType',''),
                    'RegistrationId': related_instance.pk,
                    'PatientId': getattr(Patient_inst, 'PatientId',''),
                    'PatientName': f"{getattr(Patient_inst, 'FirstName', '')} {getattr(Patient_inst, 'MiddleName', '')} {getattr(Patient_inst, 'SurName', '')}",
                    'PhoneNo': getattr(Patient_inst, 'PhoneNo',''),
                    'InsuranceId': getattr(getattr(related_instance, 'InsuranceName',''), 'pk',''),
                    'InsuranceName': getattr(getattr(related_instance, 'InsuranceName',''), 'Insurance_Name',''),
                    'Papersstatus':entry.Papersstatus,
                    'CreatedAt':entry.Created_at.strftime('%d-%m-%Y')
                }
                # print('Patient Data:', Patient_dec)
                Patient_arr.append(Patient_dec)

        if PatientId:
            Patient_arr = [p for p in Patient_arr if PatientId in p.get('PatientId', '')]
        if PatientName:
            Patient_arr = [p for p in Patient_arr if PatientName.lower() in p.get('PatientName', '').lower()]



        return JsonResponse(Patient_arr, safe=False)

    except Exception as e:
        print(f'An error occurred: {str(e)}')
        return JsonResponse ({'error': f'An error occurred: {str(e)}'}, status=500)



@csrf_exempt
@require_http_methods(['GET'])
def Get_StatusCount(request):
    try:

        All_count = Insuranse_Patient_Entery_Details.objects.all().count()
        Pending_count = Insuranse_Patient_Entery_Details.objects.filter(Papersstatus='PENDING').count()
        APPROVED_count = Insuranse_Patient_Entery_Details.objects.filter(Papersstatus='APPROVED').count()
        REJECTED_count = Insuranse_Patient_Entery_Details.objects.filter(Papersstatus='REJECTED').count()
        COMPLETED_count = Insuranse_Patient_Entery_Details.objects.filter(Papersstatus='COMPLETED').count()

        Count_data={
            
            'Allcount':All_count,
            'Pendingcount':Pending_count,
            'ApprovedCount':APPROVED_count,
            'RejectedCount':REJECTED_count,
            'CompletedCount':COMPLETED_count
            }

        return JsonResponse (Count_data,safe=False)
    
    except Exception as e:
        print(f'An error occurred: {str(e)}')
        return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)





def parse_date_safe(date_str):
    """Safely parse a date string to a date object."""
    if date_str:
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            print(f"Invalid date format: {date_str}")
            return None
    return None



@csrf_exempt
@require_http_methods(["POST","GET"])
def Post_Insurance_Patient_Detailes(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
          
            
            TableId=data.get('TableId')

            print('11111',TableId)
            
            PreAuthDate=data.get('PreAuthDate')
            PreAuthAmount=data.get('PreAuthAmount')
            DischargeDate=data.get('DischargeDate')
            FinalBillAmount=data.get('FinalBillAmount')
            RaisedAmount=data.get('RaisedAmount')
            ApprovedAmount=data.get('ApprovedAmount')
            CourierDate=data.get('CourierDate')
            SettlementDateCount=data.get('SettlementDateCount')
            
            Created_By=data.get('Created_By')

            Status=data.get('Status')


            AmountArray=data.get('AmountArray')
            
            insurance_type_data = data.get('insurancetype', {})

            insurancetype =  insurance_type_data.get('insurancetype','')
            PolicyNumber = insurance_type_data.get('policynumber','')

            employee_data = data.get('Employee', {})
            print("employee_data",employee_data)
            IsEmployee = employee_data.get('IsEmployee', 'No')
            CompanyName = employee_data.get('CompanyName',None)
            EmployeeID = employee_data.get('Employeeid',None)
            EmployeeDesignation = employee_data.get('EmployeeDesignation',None)


            copayment_details = data.get('CoPaymentDetails', {})
            print("copayment_details",copayment_details)
            CoPaymentType = copayment_details.get('CoPaymentType','')
            CoPaymentTypeValuestr = copayment_details.get('CoPaymentTypeValue',0)
            CoPaymentTypeValue = float(CoPaymentTypeValuestr) if CoPaymentTypeValuestr !='' else 0
            CoPaymentBillAmountstr = copayment_details.get('CoPaymentBillAmount',0)
            CoPaymentBillAmount = float(CoPaymentBillAmountstr) if CoPaymentBillAmountstr !='' else 0
            CoPaymentFinalAmountstr = copayment_details.get('CoPaymentFinalAmount',0)
            CoPaymentFinalAmount = float(CoPaymentFinalAmountstr) if CoPaymentFinalAmountstr !='' else 0

            CoPaymentCoverage= data.get('CoPaymentCoverage','No')
            print("CoPaymentCoverage",CoPaymentCoverage)
            TdsPercentagestr = data.get('TdsPercentage',0)
            print("TdsPercentage",TdsPercentagestr)
            TdsPercentage = float(TdsPercentagestr) if TdsPercentagestr !='' else 0
            print("TdsPercentage",TdsPercentage)
            TdsAmountstr = data.get('TdsAmount',0)
            print("TdsAmount",TdsAmountstr)
            TdsAmount = float(TdsAmountstr) if TdsAmountstr !='' else 0 
            FinalSettlementAmountstr = data.get('FinalSettlementAmount',0)
            print('FinalSettlementAmount',FinalSettlementAmountstr)
            FinalSettlementAmount = float(FinalSettlementAmountstr) if FinalSettlementAmountstr !='' else 0 



            Insuranse_Patient_Entery=Insuranse_Patient_Entery_Details.objects.get(pk=TableId)

            if Insuranse_Patient_Entery:
                # Common updates
                Insuranse_Patient_Entery.PreAuthDate = parse_date_safe(PreAuthDate)
                Insuranse_Patient_Entery.PreAuthAmount = PreAuthAmount
                Insuranse_Patient_Entery.DischargeDate = parse_date_safe(DischargeDate)
                Insuranse_Patient_Entery.FinalBillAmount = FinalBillAmount
                Insuranse_Patient_Entery.RaisedAmount = RaisedAmount
                Insuranse_Patient_Entery.ApprovedAmount = ApprovedAmount
                Insuranse_Patient_Entery.CourierDate = parse_date_safe(CourierDate)
                Insuranse_Patient_Entery.SettlementDateCount = SettlementDateCount
                Insuranse_Patient_Entery.TdsPercentage = TdsPercentage
                Insuranse_Patient_Entery.TdsAmount = TdsAmount
                Insuranse_Patient_Entery.FinalSettlementAmount = FinalSettlementAmount
                Insuranse_Patient_Entery.InsuranceType = insurancetype
                Insuranse_Patient_Entery.PolicyNumber = PolicyNumber

                # Conditional employee information update
                if IsEmployee == 'Yes':
                    Insuranse_Patient_Entery.IsEmployee = IsEmployee
                    Insuranse_Patient_Entery.CompanyName = CompanyName
                    Insuranse_Patient_Entery.Employeeid = EmployeeID
                    Insuranse_Patient_Entery.EmployeeDesignation = EmployeeDesignation
                else:
                    Insuranse_Patient_Entery.IsEmployee = 'No'
                    Insuranse_Patient_Entery.CompanyName = None
                    Insuranse_Patient_Entery.Employeeid = None
                    Insuranse_Patient_Entery.EmployeeDesignation = None

                # Conditional copayment information update
                if CoPaymentCoverage == 'Yes':
                    Insuranse_Patient_Entery.IsCopayment = CoPaymentCoverage
                    Insuranse_Patient_Entery.CopaymentBillAmount = CoPaymentBillAmount
                    Insuranse_Patient_Entery.CopaymentType = CoPaymentType
                    Insuranse_Patient_Entery.CopaymentTypeValue = CoPaymentTypeValue
                    Insuranse_Patient_Entery.CoPaymentFinalAmount = CoPaymentFinalAmount
                else:
                    Insuranse_Patient_Entery.IsCopayment = 'No'
                    Insuranse_Patient_Entery.CopaymentBillAmount = 0
                    Insuranse_Patient_Entery.CopaymentType = ''
                    Insuranse_Patient_Entery.CopaymentTypeValue = 0
                    Insuranse_Patient_Entery.CoPaymentFinalAmount = 0

                if Status:
                    Insuranse_Patient_Entery.Papersstatus = Status

                Insuranse_Patient_Entery.save()

                if AmountArray:
                    Insuranse_Patient_Amount_Details.objects.filter(
                        Insurance_Entry=Insuranse_Patient_Entery
                    ).delete()
                    for row in AmountArray:
                        Insuranse_Patient_Amount_Details.objects.create(
                            Insurance_Entry=Insuranse_Patient_Entery,
                            SettlementDate=parse_date_safe(row.get('SettlementDate')),
                            SettlementAmount=row.get('SettlementAmount'),
                            UTR_Number=row.get('UTRNumber'),
                            Created_By=Created_By
                        )

            else:
                return JsonResponse ({'warn': 'Patient Entery Find.Patient Not Found'})


            return JsonResponse ({'success': 'Save successfully'})
        except Exception as e:
            print(f'An error Accurred :{str(e)}')
            return JsonResponse({'error': f'An error occurred: {str(e)}'})

    if request.method == 'GET':
        try:
            get_id = request.GET.get('GetId')
            if not get_id:
                return JsonResponse({'warn': 'GetId is required'})

            try:
                single_ins = Insuranse_Patient_Entery_Details.objects.get(pk=get_id)
            except Insuranse_Patient_Entery_Details.DoesNotExist:
                return JsonResponse({'warn': 'Patient entry not found'})

            patient_details = {
                'PreAuthDate': single_ins.PreAuthDate,
                'PreAuthAmount': single_ins.PreAuthAmount,
                'DischargeDate': single_ins.DischargeDate,
                'FinalBillAmount': single_ins.FinalBillAmount,
                'RaisedAmount': single_ins.RaisedAmount,
                'ApprovedAmount': single_ins.ApprovedAmount,
                'CourierDate': single_ins.CourierDate,
                'SettlementDateCount': single_ins.SettlementDateCount,
                'TdsPercentage': single_ins.TdsPercentage,
                'TdsAmount': single_ins.TdsAmount,
                'FinalSettlementAmount': single_ins.FinalSettlementAmount,
                'CoPaymentCoverage': single_ins.IsCopayment,
                'insurancetype': single_ins.InsuranceType or '',
                'policynumber': single_ins.PolicyNumber or '',
                'AmountArray': [
                    {
                        'id': idx + 1,
                        'SettlementDate': row.SettlementDate,
                        'SettlementAmount': row.SettlementAmount,
                        'UTRNumber': row.UTR_Number,
                    } for idx, row in enumerate(Insuranse_Patient_Amount_Details.objects.filter(Insurance_Entry=single_ins))
                ]
            }

            if single_ins.IsCopayment == 'Yes':
                patient_details.update({
                    'CoPaymentType': single_ins.CopaymentType,
                    'CoPaymentTypeValue': single_ins.CopaymentTypeValue,
                    'CoPaymentBillAmount': single_ins.CopaymentBillAmount,
                    'CoPaymentFinalAmount': single_ins.CoPaymentFinalAmount,
                })

            if single_ins.IsEmployee == 'Yes':
                patient_details.update({
                    'IsEmployee': single_ins.IsEmployee,
                    'CompanyName': single_ins.CompanyName,
                    'Employeeid': single_ins.Employeeid,
                    'EmployeeDesignation': single_ins.EmployeeDesignation,
                })

            return JsonResponse(patient_details, safe=False)
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)

@csrf_exempt
@require_http_methods(["POST","GET"])
def Update_StatusFor_Insurance_Patient_Detailes(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            print('+++++++++',data)
            
            InstId=data.get('InstId')
            Status=data.get('Status')

            

            Insuranse_Patient_Entery_Ins=Insuranse_Patient_Entery_Details.objects.get(pk=InstId)

            Insuranse_Patient_Entery_Ins.Papersstatus=Status

            Insuranse_Patient_Entery_Ins.save()

            return JsonResponse({'success': 'Update Status successfully'})
        
        except Exception as e:
            print(f'An error occurred :{str(e)}')
            return JsonResponse({'error':f'An error occurred :{str(e)}'})      




@csrf_exempt
@require_http_methods(['GET'])
def Insurance_Patient_Details(request):
    try:
        PatientId = request.GET.get('PatientId')
        RegistrationId = request.GET.get('RegistrationId')
        PatientServiesType = request.GET.get('PatientServiesType')

        if not RegistrationId:
            return JsonResponse({'warn': 'Registration id required'})
        if not PatientId:
            return JsonResponse({'warn': 'PatientId required'})
        if not PatientServiesType:
            return JsonResponse({'warn': 'Service Type required'})

        admission_instance = None
        admissiondate = None

        if PatientServiesType == 'OP':
            patient_ins = Patient_Appointment_Registration_Detials.objects.filter(pk=RegistrationId, PatientId=PatientId)
        elif PatientServiesType == 'IP':
            patient_ins = Patient_IP_Registration_Detials.objects.filter(Registration_Id=RegistrationId, PatientId=PatientId)
            admission_instance = Patient_Admission_Detials.objects.filter(IP_Registration_Id__pk=RegistrationId).first()
            if admission_instance:  # Correct the reference to admission_instance
                admissiondate = admission_instance.created_at.strftime('%d/%m/%Y')
        elif PatientServiesType == 'Casuality':
            patient_ins = Patient_Emergency_Registration_Detials.objects.filter(Registration_Id=RegistrationId, PatientId=PatientId)
            admission_instance = Patient_Admission_Detials.objects.filter(Emergency_Registration_Id__pk=RegistrationId).first()
            if admission_instance:
                admissiondate = admission_instance.created_at.strftime('%d/%m/%Y')
        else:
            return JsonResponse({'warn': 'Invalid Patient Services Type'})

        if patient_ins.exists():
            patient_data = []
            for idx, register in enumerate(patient_ins, start=1):
                patient_dict = {
                    'id': idx,
                    'PhoneNo': register.PatientId.PhoneNo,
                    'Gender': register.PatientId.Gender,
                    'Age': register.PatientId.Age,
                    'DoctorId': register.PrimaryDoctor.Doctor_ID if register.PrimaryDoctor else None,
                    'DoctorName': f"{register.PrimaryDoctor.Tittle.Title_Name if register.PrimaryDoctor and register.PrimaryDoctor.Tittle else ''} {register.PrimaryDoctor.ShortName if register.PrimaryDoctor else ''}".strip(),
                    'PurposeofAdmission': admission_instance.AdmissionPurpose if admission_instance else '',
                    'DateofAdmission': admissiondate if admissiondate else '',
                    'isMlc': 'Yes' if register.IsMLC else 'No'
                }
                patient_data.append(patient_dict)
            return JsonResponse(patient_data, safe=False)
        else:
            return JsonResponse({'warn': 'No matching records found'})

    except Exception as e:
        return JsonResponse({'error': str(e)})

# Insurance_Details_get
@csrf_exempt
@require_http_methods(['GET'])
def Insurance_Details_get(request):
    try:
        InsuranceId = request.GET.get('InsuranceId')

        if not InsuranceId:
            return JsonResponse({'warn': 'Insurance id not found'})

        # Fetch the single insurance detail by ID
        try:
            insurance_details = Insurance_Master_Detials.objects.get(Insurance_Id=InsuranceId)
        except Insurance_Master_Detials.DoesNotExist:
            return JsonResponse({'warn': 'Insurance details not found'})

        # Extract relevant fields into a dictionary
        insurance_data = [{
            'InsuranceId': insurance_details.Insurance_Id,
            'Insurance_Name': insurance_details.Insurance_Name,
            'Payer_Zone': insurance_details.Payer_Zone or '',
            'PayerMember_Id': insurance_details.PayerMember_Id or '',
            'ContactPerson': insurance_details.ContactPerson or '',
            'MailId': insurance_details.MailId or '',
            'PhoneNumber': insurance_details.PhoneNumber or ''
        }]

        return JsonResponse(insurance_data, safe=False)
    
    except Exception as e:
        return JsonResponse({'error': str(e)})
