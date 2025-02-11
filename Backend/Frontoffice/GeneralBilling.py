import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import *
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from Masters.models import *
from decimal import Decimal, InvalidOperation
from .models import Patient_Appointment_Registration_Detials
from django.shortcuts import render
from .models import Service_Master_Details, Service_Procedure_Charges
from django.db.models import  Q
from OutPatient.models import *


from django.db import connection, transaction
from .models import Patient_Appointment_Registration_Detials, Patient_Detials
from django.core.serializers import serialize
from Workbench.models import *
from django.db.models import Sum

# -------------------------------------------------------------------------------

     
@csrf_exempt
@require_http_methods(["GET"])
def Get_OP_Billing_Details(request):
    try:
        location = request.GET.get('location')
        Status = request.GET.get('Status','Pending')
        searchBy = request.GET.get('searchBy')
        
        print('222222',location,Status,searchBy)
         
            
        Get_OPBilling_instance=OP_Billing_QueueList_Detials.objects.filter(
           ( Q(Registration_Id__PatientId__PatientId__icontains=searchBy)|
            Q(Registration_Id__PatientId__PhoneNo__icontains=searchBy)|
            Q(Registration_Id__PatientId__FirstName__icontains=searchBy)) &
            Q(Status=Status) 
        )
        print('11111111',Get_OPBilling_instance)
        Billing_data=[]

        for row in Get_OPBilling_instance:
            full_name = f"{row.Registration_Id.PatientId.FirstName} {row.Registration_Id.PatientId.MiddleName} {row.Registration_Id.PatientId.SurName}"

            formatted_date = row.created_at.strftime("%d/%b/%Y")
            
            # referal_ins = ReferalDoctorDetails.objects.filter(PatientId = row.Registration_Id.PatientId.PatientId)
            # print('refff',referal_ins)

            categoryname = ''
            categoryid = ''
            if row.Registration_Id.PatientCategory == 'Insurance':
                categoryname = row.Registration_Id.InsuranceName.Insurance_Name if row.Registration_Id.InsuranceName else None
                categoryid = row.Registration_Id.InsuranceName.Insurance_Id if row.Registration_Id.InsuranceName else None
            elif row.Registration_Id.PatientCategory == 'Client':
                categoryname = row.Registration_Id.ClientName.Client_Name if row.Registration_Id.ClientName else None
                categoryid = row.Registration_Id.ClientName.Client_Id if row.Registration_Id.ClientName else None
            else:
                categoryname=None

            Billing_data.append({    
                'id':row.BillingQueueList_ID,
                'VisitType' : 'OP',
                'Status': row.Status,
                'Date': formatted_date,
                'Registration_Id':row.Registration_Id.Registration_Id,
                'PatientId':row.Registration_Id.PatientId.PatientId,
                'PhoneNo':row.Registration_Id.PatientId.PhoneNo,
                'Patient_Name':full_name.strip(),
                'AgeGender': f'{row.Registration_Id.PatientId.Age}/{row.Registration_Id.PatientId.Gender}',
                'Address': f'{row.Registration_Id.PatientId.DoorNo}, {row.Registration_Id.PatientId.Street}, {row.Registration_Id.PatientId.Area}, {row.Registration_Id.PatientId.City}, {row.Registration_Id.PatientId.State}, {row.Registration_Id.PatientId.Country}, {row.Registration_Id.PatientId.Pincode}',
                'VisitPurpose':row.Registration_Id.VisitPurpose,
                # 'PatientType':row.Registration_Id.PatientType,
                'PatientCategory':row.Registration_Id.PatientCategory,
                'PatientCategoryName':categoryname,
                'Doctor_ShortName':row.Doctor_Ratecard_Id.Doctor_ID.ShortName if row.Doctor_Ratecard_Id else None,
                'Doctor_Id':row.Doctor_Ratecard_Id.Doctor_ID.Doctor_ID if row.Doctor_Ratecard_Id else None,
                'Title' : row.Registration_Id.PatientId.Title.Title_Name,
                'FirstName' : row.Registration_Id.PatientId.FirstName,
                'MiddleName' : row.Registration_Id.PatientId.MiddleName,
                'SurName' : row.Registration_Id.PatientId.SurName,
                'Gender' : row.Registration_Id.PatientId.Gender,
                'DOB' : row.Registration_Id.PatientId.DOB,
                'Age' : row.Registration_Id.PatientId.Age,
                'Email' : row.Registration_Id.PatientId.Email,
                'BloodGroup' : row.Registration_Id.PatientId.BloodGroup.BloodGroup_Name if row.Registration_Id.PatientId.BloodGroup else None,
                'Occupation' : row.Registration_Id.PatientId.Occupation,
                'Religion' : row.Registration_Id.PatientId.Religion.Religion_Id if row.Registration_Id.PatientId.Religion else None,
                'Nationality' :row.Registration_Id.PatientId.Nationality,
                'UniqueIdType' : row.Registration_Id.PatientId.UniqueIdType,
                'UniqueIdNo' : row.Registration_Id.PatientId.UniqueIdNo,
                # 'CaseSheetNo' : row.Registration_Id.PatientId.CasesheetNo,
                'Complaint' : row.Registration_Id.Complaint,
                # 'PatientType' : row.Registration_Id.PatientType,
                # 'PatientCategory': row.Registration_Id.PatientCategory,
                'DoorNo' : row.Registration_Id.PatientId.DoorNo,
                'Street' :row.Registration_Id.PatientId.Street,
                'Area' :row.Registration_Id.PatientId.Area,
                'City' :row.Registration_Id.PatientId.City,
                'State' :row.Registration_Id.PatientId.State,
                'Country' :row.Registration_Id.PatientId.Country,
                'Pincode' :row.Registration_Id.PatientId.Pincode,   
                # 'ReferalDoctor': referal_ins 
            })

        return JsonResponse (Billing_data,safe=False)
    except Exception  as e:
        print({'error':str(e)})
        return JsonResponse ({'error':str(e)})

@csrf_exempt
@require_http_methods(["GET"])
def Get_OP_Billing_Details_SingleId(request):
    try:
        QueueList_ID = request.GET.get('QueueList_ID')

        if not QueueList_ID:
            return JsonResponse({'error': 'QueueList_ID is required'}, status=400)

        try:
            row = OP_Billing_QueueList_Detials.objects.get(BillingQueueList_ID=QueueList_ID)
        except OP_Billing_QueueList_Detials.DoesNotExist:
            return JsonResponse({'error': 'Billing data not found'}, status=404)

        # Prepare patient full name
        full_name = f"{row.Registration_Id.PatientId.FirstName}{row.Registration_Id.PatientId.MiddleName}{row.Registration_Id.PatientId.SurName}"
        formatted_date = row.created_at.strftime("%d/%b/%Y")

        # Fetch advance records for the patient
        # Fetch a single advance record for the patient
        remaining_amount = 0
        record_id = None  # Initialize record_id to handle case where no record exists

        # Fetch advance records for the patient
        if row.Registration_Id.PatientId:
            advance_record = advancemaintaintable.objects.filter(Patient_Id=row.Registration_Id.PatientId).first()
            
            # Check if advance record exists
            if advance_record:
                # Retrieve the ID of the record
                record_id = advance_record.id

                # Calculate total advance amount and total paid amount
                total_advance_amount = advance_record.fullAmount
                total_paid_amount = advance_record.paidamount

                # Calculate remaining amount
                full_amount = total_advance_amount
                if full_amount > total_paid_amount:
                    remaining_amount = full_amount - total_paid_amount
        categoryname = ''
        categoryid = ''
        if row.Registration_Id.PatientCategory == 'Insurance':
            categoryname = row.Registration_Id.InsuranceName.Insurance_Name
            categoryid = row.Registration_Id.InsuranceName.Insurance_Id
        elif row.Registration_Id.PatientCategory == 'Client':
            categoryname = row.Registration_Id.ClientName.Client_Name
            categoryid = row.Registration_Id.ClientName.Client_Id
        else:
            categoryname=None

        # Prepare the billing data
        Billing_data = {
            'id': row.BillingQueueList_ID,
            'Billing_Type': row.Billing_Type,
            'ServiceName': row.Registration_Id.VisitPurpose,
            'Status': row.Status,
            'Date': formatted_date,
            'Registration_Id': row.Registration_Id.Registration_Id,
            'PatientId': row.Registration_Id.PatientId.PatientId,
            'PhoneNo': row.Registration_Id.PatientId.PhoneNo,
            'Patient_Name': full_name.strip(),
            'Gender': row.Registration_Id.PatientId.Gender,
            'DoorNo': row.Registration_Id.PatientId.DoorNo,
            'Age': row.Registration_Id.PatientId.Age,
            'Street': row.Registration_Id.PatientId.Street,
            'Area': row.Registration_Id.PatientId.Area,
            'City': row.Registration_Id.PatientId.City,
            'State': row.Registration_Id.PatientId.State,
            'Country': row.Registration_Id.PatientId.Country,
            'Pincode': row.Registration_Id.PatientId.Pincode,
            'VisitId': row.Registration_Id.VisitId,
            # 'PatientType': row.Registration_Id.PatientType,
            'PatientCategory': row.Registration_Id.PatientCategory,
            'PatientCategoryName': categoryname,
            'Doctor_ID': row.Doctor_Ratecard_Id.Doctor_ID.Doctor_ID if row.Doctor_Ratecard_Id else None,
            'Doctor_ShortName': row.Doctor_Ratecard_Id.Doctor_ID.ShortName if row.Doctor_Ratecard_Id else None,
            'Advance_Amount':remaining_amount, # Add the total advance amount here
            'advanceid':record_id
            
        }

        # Add Service Fee based on PatientCategory and ServiceName
        if Billing_data['PatientCategory'] == 'General':
            if Billing_data['ServiceName'] == 'NewConsultation':
                Billing_data['Service_Fee'] = row.Doctor_Ratecard_Id.General_Consultation_Fee
            elif Billing_data['ServiceName'] == 'FollowUp':
                Billing_data['Service_Fee'] = row.Doctor_Ratecard_Id.General_Follow_Up_Fee
        elif Billing_data['PatientCategory'] == 'Special':
            if Billing_data['ServiceName'] == 'NewConsultation':
                Billing_data['Service_Fee'] = row.Doctor_Ratecard_Id.Special_Consultation_Fee
            elif Billing_data['ServiceName'] == 'FollowUp':
                Billing_data['Service_Fee'] = row.Doctor_Ratecard_Id.Special_Follow_Up_Fee

        return JsonResponse(Billing_data, safe=False)

    except Exception as e:
        print({'error': str(e)})
        return JsonResponse({'error': str(e)}, status=500)
        
@csrf_exempt
@require_http_methods(["GET"])
def Get_OP_Billing_Details_Due(request):
    try:
        QueueList_ID=request.GET.get('QueueList_ID')

        if not QueueList_ID:
            return JsonResponse({'error':'QueueList_ID is required'},status=400)
        try:
            row =OP_Billing_QueueList_Detials.objects.get(BillingQueueList_ID=QueueList_ID)
        
        except OP_Billing_QueueList_Detials.DoesNotExist:
            return JsonResponse ({'error': 'Billing data not found'}, status=404)


           
        full_name = f"{row.Registration_Id.PatientId.FirstName}"

        formatted_date = row.created_at.strftime("%d/%b/%Y")

        Billing_data={    
                'id':row.BillingQueueList_ID,
                'Billing_Type': row.Billing_Type,
                'ServiceName':row.Registration_Id.VisitPurpose,
                'Status': row.Status,
                'Date': formatted_date,
                'Registration_Id':row.Registration_Id.Registration_Id,
                'PatientId':row.Registration_Id.PatientId.PatientId,
                'PhoneNo':row.Registration_Id.PatientId.PhoneNo,
                'Patient_Name':full_name.strip(),
                'Gender':row.Registration_Id.PatientId.Gender,
                'DoorNo':row.Registration_Id.PatientId.DoorNo,
                'Age':row.Registration_Id.PatientId.Age,
                'Street':row.Registration_Id.PatientId.Street,
                'Area':row.Registration_Id.PatientId.Area,
                'City':row.Registration_Id.PatientId.City,
                'State':row.Registration_Id.PatientId.State,
                'Country':row.Registration_Id.PatientId.Country,
                'Pincode':row.Registration_Id.PatientId.Pincode,
                'VisitId':row.Registration_Id.VisitId,
                'PatientType':row.Registration_Id.PatientType,
                'PatientCategory':row.Registration_Id.PatientCategory,
                'Doctor_ID':row.Doctor_Ratecard_Id.Doctor_ID.Doctor_ID,
                'Doctor_ShortName':row.Doctor_Ratecard_Id.Doctor_ID.ShortName,
            }
        if Billing_data['PatientCategory'] == 'General':
            if Billing_data['ServiceName'] == 'NewConsultation':
                Billing_data['Service_Fee'] = row.Doctor_Ratecard_Id.General_Consultation_Fee
            elif Billing_data['ServiceName'] == 'FollowUp':
                Billing_data['Service_Fee'] = row.Doctor_Ratecard_Id.General_Follow_Up_Fee
        
        elif Billing_data['PatientCategory'] == 'Special':
            if Billing_data['ServiceName'] == 'NewConsultation':
                Billing_data['Service_Fee'] = row.Doctor_Ratecard_Id.Special_Consultation_Fee
            elif Billing_data['ServiceName'] == 'FollowUp':
                Billing_data['Service_Fee'] = row.Doctor_Ratecard_Id.Special_Follow_Up_Fee
        
        return JsonResponse(Billing_data, safe=False)
    except Exception  as e:
        print({'error':str(e)})
        return JsonResponse ({'error':str(e)})


@csrf_exempt
@require_http_methods(["POST", "OPTIONS", "GET"])
def advance_billing_link(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            # Extract data from the request
            SelectedPatient_list = data.get('SelectedPatient_list', {})
            advanceamount = data.get('advanceamount')
            department = data.get('department')
            Created_by = data.get('Created_by', '')
            Location = data.get('Location', '')
            Billing_Type = data.get('Billing_Type')
            billAmount = data.get('billAmount', [])
            BillingData = data.get('BillingData', {})
            advanceid =data.get('advanceid')
            remainingadvanceamount=data.get('remainingadvanceamount')
            # Fetch related foreign key objects
            try:
                patient = Patient_Detials.objects.get(PatientId=SelectedPatient_list.get('PatientId'))
                register = Patient_Appointment_Registration_Detials.objects.get(Registration_Id=SelectedPatient_list.get('RegisterId'))
                visit = Patient_Visit_Detials.objects.get(
                    PatientId=SelectedPatient_list.get('PatientId'),
                    VisitId=SelectedPatient_list.get('VisitId')
                )
                locationget = Location_Detials.objects.get(Location_Id=Location)
            except ObjectDoesNotExist as e:
                return JsonResponse({'error': f'{str(e).split(":")[1].strip()} not found'})
            except MultipleObjectsReturned:
                return JsonResponse({'error': 'Multiple instances found'})

            # Convert to Decimal with error handling
            def to_decimal(value):
                try:
                    return Decimal(str(value).strip())
                except (TypeError, ValueError):
                    return Decimal('0.00')
            
            # Begin an atomic transaction
            with transaction.atomic():
                # Create and save the AdvanceAmountTable entry
                advancetable = Advanceamounttable(
                    Billing_Date=BillingData.get('InvoiceDate'),
                    Patient_Id=patient,
                    Register_Id=register,
                    Visit_Id=visit,
                    Billing_Type=Billing_Type,
                    Department=department,
                    Amount=advanceamount,
                    created_by=Created_by,
                    Locations=Location  # This should reference the correct `locationget` object
                )
                advancetable.save()
                if advanceid :

                     # Fetch the existing record using get()
                    existing_record = advancemaintaintable.objects.get(id=advanceid)
                    
                    # Calculate the total amount
                    famount = existing_record.fullAmount
                    print(famount)
                    totalamount = int(famount) + int(advanceamount)  # Use float for consistency
                    
                    # Update the record and save it
                    existing_record.Remaining_amount = remainingadvanceamount
                    existing_record.fullAmount = totalamount
                    existing_record.save()
                    
                else:
                    maintaintable=advancemaintaintable(
                        adInvoice_NO=advancetable,
                        Patient_Id=patient,
                        Register_Id=register,
                        Visit_Id=visit,
                        Billing_Date=BillingData.get('InvoiceDate'),
                        Billing_Type=Billing_Type,
                        Department=department,
                        fullAmount=advanceamount,
                        paidamount=0,
                        Remaining_amount=advanceamount,
                        created_by=Created_by,
                        Locations=Location 
                    )
                    maintaintable.save()

                # Save multiple payment details
                for payment in billAmount:
                    multiple_payment = Multiple_Payment_Table_Detials(
                        Invoice_No_Paid=advancetable.adInvoice_NO,
                        Payment_Type=payment.get('Billpay_method'),
                        Cart_Type=payment.get('CardType'),
                        Cheque_No=payment.get('ChequeNo'),
                        Bank_Name=payment.get('BankName'),
                        Amount=to_decimal(payment.get('paidamount')),
                    )
                    multiple_payment.save()
                advanceinvoiceno = advancetable.adInvoice_NO
                
            return JsonResponse({'status': 'Success','InvoiceNo':advanceinvoiceno})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)





@csrf_exempt
@require_http_methods(["POST", "OPTIONS", "GET"])
def GeneralBilling_Link(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
           
            # Extract data from the request
            billAmount = data.get('billAmount', [])
            SelectedPatient_list = data.get('SelectedPatient_list', {})
            NetAmount_CDmethod = data.get('NetAmount_CDmethod', {})
            SelectDatalist = data.get('SelectDatalist', [])
            BillingData = data.get('BillingData', {})
            initialState = data.get('initialState', {})
            Created_by = data.get('Created_by', '')
            Location = data.get('Location', '')
            request_id = data.get('Request_Id','')
            service_type = data.get('ServiceProcedureForm','')
            editid = data.get('EditId','')

            # selectedOption = data.get('selectedOption', '')
            # remainingadvanceamount=data.get('remainingadvanceamount')
            # advanceid=data.get('advanceid')
            # Fetch related foreign key objects
            print('billAmount',billAmount)
            print('SelectedPatient_list',SelectedPatient_list)
            print('NetAmount_CDmethod',NetAmount_CDmethod)
            print('SelectDatalist',SelectDatalist)
            print('BillingData',BillingData)
            print('initialState',initialState)

            print('1111111')
            # Validate essential data
            if not billAmount:
                return JsonResponse({'error': 'billAmount is empty or missing'}, status=400)
            if not SelectDatalist:
                return JsonResponse({'error': 'SelectDatalist is empty or missing'}, status=400)

            try:
                doctor = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=BillingData.get('DoctorId'))
              
                patient = Patient_Detials.objects.get(PatientId=SelectedPatient_list.get('PatientId'))

                register = Patient_Appointment_Registration_Detials.objects.get(Registration_Id=SelectedPatient_list.get('RegisterId'))
                
                visit = Patient_Visit_Detials.objects.get(
                    PatientId=SelectedPatient_list.get('PatientId'),
                    VisitId=SelectedPatient_list.get('VisitId')
                )
                print('lajhdsjsks')
                locationget=Location_Detials.objects.get(Location_Id=Location)
            except ObjectDoesNotExist as e:
                return JsonResponse({'error': f'{str(e).split(":")[1].strip()} not found'})
            except MultipleObjectsReturned:
                return JsonResponse({'error': 'Multiple instances found'})
            print('jdjdjkdkdkd')
            # Convert to Decimal with error handling
            def safe_to_decimal(value, default=0.00):
                try:
                    return Decimal(value)
                except (InvalidOperation, TypeError, ValueError):
                    return Decimal(default)
            print('ueoejcjdjd')
            new_bill_status= 'Paid' if safe_to_decimal(initialState.get('BalanceAmount')) == 0 else 'Due'
            # Begin an atomic transaction
            
            # Create and save the General Billing entry
            print('hello')
            if editid:
                # Edit existing billing entry
                general_billing = General_Billing_Table_Detials.objects.get(Billing_Invoice_No=editid)
                general_billing.Billing_Date = BillingData.get('InvoiceDate')
                general_billing.Doctor_Id = doctor
                general_billing.Patient_Id = patient
                general_billing.Register_Id = register
                general_billing.Visit_Id = visit
                general_billing.Billing_Type = NetAmount_CDmethod.get('Method')
                general_billing.Select_Discount = NetAmount_CDmethod.get('Method')
                general_billing.Discount_Type = NetAmount_CDmethod.get('Method')
                general_billing.Discount_Value = safe_to_decimal(NetAmount_CDmethod.get('Amount'))
                general_billing.Discount_Amount = safe_to_decimal(initialState.get('totalDiscount'))
                general_billing.Total_Items = int(initialState.get('totalItems'))
                general_billing.Total_Qty = int(initialState.get('totalUnits'))
                general_billing.Total_Amount = safe_to_decimal(initialState.get('totalTaxable'))
                general_billing.Total_GSTAmount = safe_to_decimal(initialState.get('totalGstamount'))
                general_billing.Net_Amount = safe_to_decimal(initialState.get('totalNetAmount'))
                general_billing.Net_Paid_Amount=safe_to_decimal(initialState.get('totalAmountt'))
                general_billing.Round_Off = safe_to_decimal(initialState.get('Roundoff'))
                general_billing.Paid_Amount = safe_to_decimal(initialState.get('PaidAmount'))
                general_billing.Balance_Amount = safe_to_decimal(initialState.get('BalanceAmount'))
                general_billing.Bill_Status = new_bill_status
                general_billing.save()

                # Delete existing billing items and re-add them
                General_Billing_Items_Table_Detials.objects.filter(Billing_Invoice_No=editid).delete()
                for item in SelectDatalist:
                    print('item:', item)
                    service_cd = item.get('ServiceCode', '') if service_type != 'Lab' else (
                        item.get('Test_Code') if item.get('type') == "individual" else item.get("group")
                    )
                    general_billing_item_instance = General_Billing_Items_Table_Detials(
                        Billing_Invoice_No=general_billing,
                        Service_Type=item.get('ServiceType'),
                        Service_Code=service_cd,
                        Service_Name=item.get('SelectItemName'),
                        Rate=safe_to_decimal(item.get('Amount')),
                        Charge=safe_to_decimal(item.get('Charges')),
                        Quantity=int(item.get('Quantity', 1)),
                        Amount=safe_to_decimal(item.get('Amount')),
                        Discount_Type=item.get('DiscountType'),
                        Discount_Value=safe_to_decimal(item.get('Discount', 0.00)),
                        Taxable_Amount=safe_to_decimal(item.get('Amount')),
                        Tax_Amount=safe_to_decimal(item.get('GST', 0.00)),
                        Total_Amount=safe_to_decimal(item.get('NetAmount')),
                        Item_Status=new_bill_status,
                    )
                    general_billing_item_instance.save()

                # Delete existing payment details and re-add them
                Multiple_Payment_Table_Detials.objects.filter(Invoice_No_Paid=editid).delete()
                for payment in billAmount:
                    print('payment:', payment)
                    multiple_payment_instance = Multiple_Payment_Table_Detials(
                        Invoice_No_Paid=editid,
                        Payment_Type=payment.get('Billpay_method'),
                        Cart_Type=payment.get('CardType'),
                        Card_No=payment.get('CardNo'),
                        TransactionId=payment.get('TransactionId'),
                        upiid=payment.get('upiid'),
                        Cheque_No=payment.get('ChequeNo'),
                        Bank_Name=payment.get('BankName'),
                        Amount=safe_to_decimal(payment.get('paidamount')),
                        Transaction_Amount=safe_to_decimal(payment.get('transactionFee')),
                        AdditionalAmount=safe_to_decimal(payment.get('Additionalamount')),
                    )
                    multiple_payment_instance.save()

                # Handle lab queue status update if applicable
                if service_type == 'Lab':
                    lab_queue_instance = Lab_Request_Details.objects.get(
                        Request_Id=request_id, OP_Register_Id__Registration_Id=SelectedPatient_list.get('RegisterId')
                    )
                    lab_queue_instance.Billing_Status = 'Completed'
                    lab_queue_instance.Billing_Invoice_No = general_billing
                    lab_queue_instance.save()

                return JsonResponse({'status': 'Success', 'InvoiceNo': editid})
            else:
                general_billing = General_Billing_Table_Detials(
                    Billing_Date=BillingData.get('InvoiceDate'),
                    Doctor_Id=doctor,
                    Patient_Id=patient,
                    Register_Id=register,
                    Visit_Id=visit,
                    Billing_Type=NetAmount_CDmethod.get('Method'),
                    Select_Discount=NetAmount_CDmethod.get('Method'),
                    Discount_Type=NetAmount_CDmethod.get('Method'),
                    Discount_Value=NetAmount_CDmethod.get('Amount') if NetAmount_CDmethod.get('Amount') != '' else 0.00,
                    Discount_Amount=initialState.get('totalDiscount'),
                    Total_Items=int(initialState.get('totalItems')),
                    Total_Qty=int(initialState.get('totalUnits')),
                    Total_Amount=initialState.get('totalTaxable'),
                    Total_GSTAmount=initialState.get('totalGstamount'),
                    Net_Amount=initialState.get('totalNetAmount'),
                    Net_Paid_Amount=initialState.get('totalAmountt'),
                    Round_Off=initialState.get('Roundoff'),
                    Paid_Amount=initialState.get('PaidAmount'),
                    Balance_Amount=initialState.get('BalanceAmount'),
                    Bill_Status=new_bill_status,
                    created_by=Created_by,
                    Location=locationget
                )
                general_billing.save()

                print('dvwebjvwhbvjwe')
                if service_type == 'Lab':
                    service_code = ''
                # Save each item in the General Billing Items Table Details
                for item in SelectDatalist:
                    service_cd = ''
                    if service_type == 'Lab':
                        if item.get('type') == "individual":
                            service_cd = item.get('Test_Code')
                        elif item.get('type') == "individual":
                            service_cd = item.get("group")
                    else:
                        service_cd = item.get('ServiceCode')
                    print('vsdvsdvsdv',service_cd)

                    def safe_to_decimal(value, default=0.00):
                        try:
                            return Decimal(value)
                        except (InvalidOperation, TypeError, ValueError):
                            return Decimal(default)
                        
                    general_billing_item = General_Billing_Items_Table_Detials(
                        Billing_Invoice_No=general_billing,
                        Service_Type=item.get('ServiceType'),
                        Service_Code=service_cd,
                        Service_Name=item.get('SelectItemName'),
                        Rate=safe_to_decimal(item.get('Amount')) ,
                        Charge=safe_to_decimal(item.get('Charges')),
                        Quantity=int(item.get('Quantity',1)),
                        Amount=safe_to_decimal(item.get('Amount')),
                        Discount_Type=item.get('DiscountType'),
                        Discount_Value=safe_to_decimal(item.get('Discount') if item.get('Discount') != "" else 0.00),
                        # Discount_Amount=to_decimal(item.get('DiscountAmount')),
                        Taxable_Amount=safe_to_decimal(item.get('Amount')),
                        # Tax_Percentage= item.get('GST'),
                        Tax_Amount=safe_to_decimal(item.get('GST') if item.get('GST') != "" else 0.00),
                        Total_Amount=safe_to_decimal(item.get('NetAmount')), 
                        Item_Status=new_bill_status,
                    )
                    general_billing_item.save()
                    
                # Save multiple payment details
                print('ucjcjvjhcj')
                for payment in billAmount:
                
                    multiple_payment = Multiple_Payment_Table_Detials(
                        Invoice_No_Paid=general_billing.Billing_Invoice_No,
                        Payment_Type=payment.get('Billpay_method'),
                        Cart_Type=payment.get('CardType'),
                        Card_No=payment.get('CardNo'),
                        TransactionId=payment.get('TransactionId'),
                        upiid=payment.get('upiid'),
                        Cheque_No=payment.get('ChequeNo'),
                        Bank_Name=payment.get('BankName'),
                        Amount=safe_to_decimal(payment.get('paidamount')),
                        Transaction_Amount = safe_to_decimal(payment.get('transactionFee')),
                        AdditionalAmount = safe_to_decimal(payment.get('Additionalamount')),
                    )
                    multiple_payment.save()
                    # if payment.get('Billpay_method') == 'Advance':
                    #     advance_record = advancemaintaintable.objects.get(
                    #     id=advanceid
                    # )
                    # # Calculate new remaining amount
                    #     advance_record.Remaining_amount = remainingadvanceamount
                    # # Update the record
                    #     advance_record.paidamount = to_decimal(initialState.get('totalTaxable'))
                    #     advance_record.save()

                    if service_type == 'Lab':
                        print('yvkjhgjh', request_id, SelectedPatient_list.get('RegisterId'))
                        try:
                            patient_ins = Patient_Appointment_Registration_Detials.objects.get(Registration_Id=SelectedPatient_list.get('RegisterId'))
                            print('11111', patient_ins)
                            # Use .filter() instead of .get() to avoid exceptions if no record is found
                            lab_qeue_ins = Lab_Request_Details.objects.filter(Request_Id=request_id, OP_Register_Id__Registration_Id=patient_ins.pk).first()
                            
                            if lab_qeue_ins:
                                print('svwevwevwe', lab_qeue_ins)
                                lab_qeue_ins.Billing_Status = 'Completed'
                                lab_qeue_ins.Billing_Invoice_No = general_billing
                                lab_qeue_ins.save()
                            else:
                                print("No matching Lab_Request_Details found.")
                        except Patient_Appointment_Registration_Detials.DoesNotExist:
                            print("Patient not found.")
                        except Exception as e:
                            print(f"An error occurred: {e}")

                # if SelectedPatient_list.get('QueueList_ID'):
                #     try:
                #         billing_queue_list_instance = OP_Billing_QueueList_Detials.objects.get(BillingQueueList_ID=SelectedPatient_list.get('QueueList_ID'))
                #         billing_queue_list_instance.Status = new_bill_status
                #         billing_queue_list_instance.save()
                #     except ObjectDoesNotExist:
                #         return JsonResponse({'error': 'Billing Queue List not found'})
                #     except MultipleObjectsReturned:
                #         return JsonResponse({'error': 'Multiple Billing Queue List instances found'})


                billing_receipt_table = GeneralBillingReceipt(
                    Invoice_NO=general_billing,
                    PatientID=patient.PatientId,
                    PhoneNumber=patient.PhoneNo,
                    Patient_Name=f"{patient.FirstName} {patient.MiddleName or ''} {patient.SurName}".strip(),
                    TotalAmount= safe_to_decimal(initialState.get('totalNetAmount')),
                    TotalPaidAmount=safe_to_decimal(initialState.get('PaidAmount')),
                    BalanceAmount=safe_to_decimal(initialState.get('BalanceAmount')),
                    Billing_Date=BillingData.get('InvoiceDate'),
                    PaidAmount=safe_to_decimal(initialState.get('PaidAmount')),
                    Billedby=Created_by,
                )
                billing_receipt_table.save()
                invoicenoforbill=general_billing.Billing_Invoice_No
                return JsonResponse({'status': 'Success','InvoiceNo':invoicenoforbill})
            
        except Exception as e:
            print(str(e))
            return JsonResponse({'error': str(e)}, status=500)


    elif request.method == "GET":
        try:
            # Retrieve query parameters
            SearchbyDate = request.GET.get('SearchbyDate')
            SearchbyFirstName = request.GET.get('SearchbyFirstName')
            SearchbyPhoneNumber = request.GET.get('SearchbyPhoneNumber')
            SearchTimeOrderby = request.GET.get('SearchTimeOrderby')
            status_filter = request.GET.get('SearchStatus')

            print('status_filter:', status_filter)
            
            # Build dynamic filter query
            search_query = Q()
            
            if SearchbyFirstName:
                search_query &= Q(Register_Id__PatientId__FirstName__icontains=SearchbyFirstName)
            if SearchbyPhoneNumber:
                search_query &= Q(Register_Id__PatientId__PhoneNo__icontains=SearchbyPhoneNumber)
            if SearchbyDate:
                search_query &= Q(Billing_Date__icontains=SearchbyDate)
            if status_filter:
                search_query &= Q(Bill_Status=status_filter)


            general_billing_data = General_Billing_Table_Detials.objects.filter(search_query)

                        # Apply ordering dynamically
            if SearchTimeOrderby:
                if SearchTimeOrderby.lower() == 'order':
                    general_billing_data = general_billing_data.order_by('Billing_Date')  # Ascending
                elif SearchTimeOrderby.lower() == 'disorder':
                    general_billing_data = general_billing_data.order_by('-Billing_Date')  # Descending

            response_data = []

            for row in general_billing_data:
                # Construct the patient's full name
                full_name = f"{row.Patient_Id.FirstName} {row.Patient_Id.MiddleName or ''} {row.Patient_Id.SurName}".strip()

                # Prepare the general billing details
                billing_details = {
                    'id': row.Billing_Invoice_No,
                    'Type': 'OPEdit',
                    'Billing_Date': row.Billing_Date,
                    'Doctor_Id': row.Doctor_Id.Doctor_ID,
                    'Doctor_Name': row.Doctor_Id.ShortName,
                    'PatientId': row.Patient_Id.PatientId,
                    'Patient_Name': full_name,
                    'PhoneNo': row.Patient_Id.PhoneNo,
                    'Register_Id': row.Register_Id.Registration_Id,
                    'Gender': row.Register_Id.PatientId.Gender,
                    'City': row.Register_Id.PatientId.City,
                    'State': row.Register_Id.PatientId.State,
                    'Pincode': row.Register_Id.PatientId.Pincode,
                    'AgeGender': f'{row.Register_Id.PatientId.Age}/{row.Register_Id.PatientId.Gender}',
                    'Address':f'{row.Register_Id.PatientId.DoorNo}, {row.Register_Id.PatientId.Street}, {row.Register_Id.PatientId.Area}, {row.Register_Id.PatientId.City}, {row.Register_Id.PatientId.State}, {row.Register_Id.PatientId.Country}, {row.Register_Id.PatientId.Pincode}',
                    'PatientCategory': row.Register_Id.PatientCategory,
                    'PatientCategoryName': (
                        row.Register_Id.InsuranceName.Insurance_Name
                        if row.Register_Id.PatientCategory == 'Insurance'
                        else getattr(row.Register_Id.ClientName, 'Client_Name', None)
                    ),
                    'Visit_Id': row.Visit_Id.VisitId,
                    'Billing_Type': row.Billing_Type,
                    'TotalItems': row.Total_Items,
                    'TotalQty': row.Total_Qty,
                    'RoundOff': row.Round_Off,
                    'TotalAmount': row.Total_Amount,
                    'Net_Amount': row.Net_Amount,
                    'PaidAmount': row.Paid_Amount,
                    'PaidNetAmount': row.Net_Paid_Amount,
                    'BalanceAmount': row.Balance_Amount,
                    'Bill_Status': row.Bill_Status,
                    'Billing_Items': [],
                    'Payment_Details': [],
                }

                # Fetch related billing items
                billing_items = General_Billing_Items_Table_Detials.objects.filter(Billing_Invoice_No=row.Billing_Invoice_No)
                for item in billing_items:
                    item_details = {
                        'Service_Type': item.Service_Type,
                        # 'Service_Code': item.Service_Code,
                        'Service_Name': item.Service_Name,
                        'Rate': item.Rate,
                        'Charge': item.Charge,
                        'Quantity': item.Quantity,
                        'Amount': item.Amount,
                        'Discount_Type': item.Discount_Type,
                        'Discount_Value': item.Discount_Value,
                        'Discount_Amount': item.Discount_Amount,
                        'Taxable_Amount': item.Taxable_Amount,
                        # 'Tax_Percentage': item.Tax_Percentage,
                        'Tax_Amount': item.Tax_Amount,
                        'Total_Amount': item.Total_Amount,
                    }
                    billing_details['Billing_Items'].append(item_details)

                # Fetch related payment details
                payment_details = Multiple_Payment_Table_Detials.objects.filter(Invoice_No_Paid=row.Billing_Invoice_No)
                for payment in payment_details:
                    payment_info = {
                        'Payment_Type': payment.Payment_Type,
                        'Card_Type': payment.Cart_Type,
                        'Card_No': payment.Card_No,
                        'TransactionId': payment.TransactionId,
                        'upiid': payment.upiid,
                        'Cheque_No': payment.Cheque_No,
                        'Bank_Name': payment.Bank_Name,
                        'Amount': payment.Amount,
                        'Transaction_Amount': payment.Transaction_Amount,
                        'AdditionalAmount': payment.AdditionalAmount,
                    }
                    billing_details['Payment_Details'].append(payment_info)

                # Add the billing details to the response data
                response_data.append(billing_details)

            return JsonResponse(response_data, safe=False)

        except Exception as e:
            print({'error': str(e)})
            return JsonResponse({'error': str(e)})

            

    return JsonResponse({'status': 'failure', 'message': 'Invalid request method'})



@csrf_exempt
@require_http_methods(["GET"])
def Filter_Patient_data_For_Billing(request):
    try:
        first_name = request.GET.get("FirstName", None)
        phone_no = request.GET.get("PhoneNo", None)
        patient_id = request.GET.get("PatientId", None)

        filter_Conditions=Q()

        if first_name:
            filter_Conditions &= Q(FirstName__icontains=first_name)
        if phone_no:
            filter_Conditions &= Q(PhoneNo__icontains=phone_no)
        if patient_id:
            filter_Conditions &= Q(PatientId__icontains=patient_id)

        patients = Patient_Detials.objects.filter(filter_Conditions,DuplicateId=False)
        print('patients :', patients)

        remaining_amount = 0
        record_id = None
        if patient_id:
            advance_record = advancemaintaintable.objects.filter(Patient_Id=patient_id).first()
            
            # Check if advance record exists
            if advance_record:
                # Retrieve the ID of the record
                record_id = advance_record.id

                # Calculate total advance amount and total paid amount
                total_advance_amount = advance_record.fullAmount
                total_paid_amount = advance_record.paidamount

                # Calculate remaining amount
                full_amount = total_advance_amount
                if full_amount > total_paid_amount:
                    remaining_amount = full_amount - total_paid_amount
            

        patient_data = [
            {
                'PatientId': patient.PatientId,
                'PhoneNo': patient.PhoneNo,
                'FirstName': patient.FirstName,
                'Gender':patient.Gender,
                'DoorNo':patient.DoorNo,
                'Age':patient.Age,
                'Street':patient.Street,
                'Area':patient.Area,
                'City':patient.City,
                'State':patient.State,
                'Country':patient.Country,
                'Pincode':patient.Pincode,
                'Advance_Amount':remaining_amount,
                'advanceid':record_id

            } for patient in patients
        ]

       
        return JsonResponse(patient_data, safe=False)

    
    except Exception as e:
        print({f'error:{str(e)}'})
        return JsonResponse({'error':'An internal server error occurred'},status=500)


 
# @csrf_exempt
# def get_merged_service_data(request):
#     services = Service_Master_Details.objects.exclude(Department='IP').values(
#         'Service_Id', 'Service_Name', 'Department', 'IsGst', 'GstValue', 'Status', 'created_by', 'created_at', 'updated_at'
#     )
#     charges = Service_Procedure_Charges.objects.select_related(
#         'Service_ratecard', 'Procedure_ratecard', 'Location'
#     ).all().values(
#         'MasterType', 'Service_ratecard__Service_Id', 'Service_ratecard__Service_Name', 'Procedure_ratecard__Procedure_Name', 'Location__Location_Name',
#         'General_Prev_fee', 'General_fee', 'Special_Prev_fee', 'Special_fee'
#     )
#     merged_data = []

#     service_dict = {service['Service_Id']: service for service in services}
    
#     for charge in charges:
#         if charge['MasterType'] == 'Service':
#             service_id = charge['Service_ratecard__Service_Id']
#             service_info = service_dict.get(service_id, {})
#             merged_data.append({
#                 'Type': 'Service',
#                 'Service_Id': service_id,
#                 'Service_Name': charge['Service_ratecard__Service_Name'],
#                 'GstValue': service_info.get('GstValue', 'N/A'),
#                 'Location': charge['Location__Location_Name'],
#                 'General_Prev_fee': charge['General_Prev_fee'],
#                 'General_fee': charge['General_fee'],
#                 'Special_Prev_fee': charge['Special_Prev_fee'],
#                 'Special_fee': charge['Special_fee']
#             })
#         elif charge['MasterType'] == 'Procedure':
#             merged_data.append({
#                 'Type': 'Procedure',
#                 'Procedure_Name': charge['Procedure_ratecard__Procedure_Name'],
#                 'Location': charge['Location__Location_Name'],
#                 'General_Prev_fee': charge['General_Prev_fee'],
#                 'General_fee': charge['General_fee'],
#                 'Special_Prev_fee': charge['Special_Prev_fee'],
#                 'Special_fee': charge['Special_fee']
#             })
    
#     return JsonResponse(merged_data,safe=False)





@csrf_exempt
def get_merged_service_data(request):
    try:
        selectedOption = request.GET.get('selectedOption')
        location = request.GET.get('location')
        PatientCategory = request.GET.get('PatientCategory')
        PatientCategoryType = request.GET.get('PatientCategoryType', None)
        ServiceType = request.GET.get('ServiceType', 'Interventional')
        merged_data = []
        
        if selectedOption == 'OPDServices':
            ser_pro_inss = Service_Master_Details.objects.filter(Status=True).exclude(Department='IP')
        else:
            ser_pro_inss = Procedure_Master_Details.objects.filter(Status=True, Type=ServiceType)
        
        for inss in ser_pro_inss:
            data = {
                'Service_Id': inss.pk,
                'Service_Name': inss.Service_Name if selectedOption == 'OPDServices' else inss.Procedure_Name,
                'GstValue': inss.GstValue if inss.IsGst == 'Yes' else "Nill"
            }

            # Filter conditions
            filter_conditions = Q()
            if selectedOption == 'OPDServices':
                filter_conditions &= Q(Service_ratecard__pk=inss.pk, Location__pk=location)
            elif selectedOption == 'OPDProcedures':
                filter_conditions &= Q(Procedure_ratecard__pk=inss.pk, Location__pk=location)

            try:
                inss_ser_pro = Service_Procedure_Charges.objects.get(filter_conditions)
                charges_gen_spe = Service_Procedure_Rate_Charges.objects.get(Service_Procedure_ratecard=inss_ser_pro)

                if PatientCategory == 'General':
                    data['charge'] = charges_gen_spe.General_fee
                elif PatientCategory == 'Special':
                    data['charge'] = charges_gen_spe.Special_fee
                elif PatientCategory == 'Insurance' and PatientCategoryType:
                    ins_ins = Service_Procedure_InsuranceFee.objects.get(Service_Procedure_ratecard=inss_ser_pro, insurance__pk=PatientCategoryType)
                    data['charge'] = ins_ins.fee
                elif PatientCategory == 'Client' and PatientCategoryType:
                    cli_ins = Service_Procedure_ClientFee.objects.get(Service_Procedure_ratecard=inss_ser_pro, client__pk=PatientCategoryType)
                    data['charge'] = cli_ins.fee

            except Service_Procedure_Charges.DoesNotExist:
                data['charge'] = ""
            except Service_Procedure_Rate_Charges.DoesNotExist:
                data['charge'] = ""
            except (Service_Procedure_InsuranceFee.DoesNotExist, Service_Procedure_ClientFee.DoesNotExist):
                data['charge'] = ""

            merged_data.append(data)
        
        return JsonResponse(merged_data, safe=False)

    except Exception as e:
        print(f'error: {str(e)}')
        return JsonResponse({'error': 'An internal server error occurred'}, status=500)

        
    
    

@csrf_exempt
def get_latest_appointment_for_patient(request):
    try:
        patient_id = request.GET.get('PatientId')
        latest_appointment = Patient_Appointment_Registration_Detials.objects.filter(PatientId=patient_id).order_by('-Registration_Id').first()

        if latest_appointment:
            appointment_data = {
                'Registration_Id': latest_appointment.Registration_Id,
                'VisitId': latest_appointment.VisitId,
            }

            return JsonResponse(appointment_data, safe=False)
        else:
            return JsonResponse({'error': 'No appointments found for this patient.'}, status=404)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)








#  For  Pharmacy Billing Op




def get_prescription(request):
    try:
        # Retrieve PatientID and VisitID from the request
        PatientID = request.GET.get('PatientID')
        VisitID = request.GET.get('VisitID')

        # Validate PatientID and VisitID
        if not PatientID or not VisitID:
            return JsonResponse({"error": "PatientID and VisitID parameters are required"}, status=400)

        print('PatientID:', PatientID, 'VisitID:', VisitID)

        # Fetch patient details to get the Patient Name
        try:
            patient = Patient_Detials.objects.get(PatientId=PatientID)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Patient not found"}, status=404)

        PatientName = f"{patient.FirstName} {patient.MiddleName} {patient.SurName}"

        # Fetch registration details
        try:
            registration = Patient_Appointment_Registration_Detials.objects.get(
                PatientId_id=PatientID, VisitId=VisitID
            )
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Registration not found for the given PatientID and VisitID"})

        print("Registration ID for Filtering:", registration.Registration_Id)

        # Query the prescriptions related to the Registration ID
        prescriptions = OPD_Prescription_Details.objects.filter(
            Registration_Id=registration
        )
        print("Prescriptions Queryset:", prescriptions)

        # Prepare the list of prescriptions
        prescription_list = []
        for prescription in prescriptions:
            try:
                # Fetch location details
                location = Location_Detials.objects.get(Location_Id=registration.Location_id)
                location_name = location.Location_Name
            except ObjectDoesNotExist:
                location_name = "N/A"
                
            products = Stock_Maintance_Table_Detials.objects.filter(Product_Detials__ItemName=prescription.ItemId.ItemName)
            if products.exists():
                for product in products:
                    doctor = prescription.Registration_Id.PrimaryDoctor
                    prescription_dict = {
                        'PrescriptionID': prescription.Prescription_Id,
                        'PatientID': PatientID,
                        'VisitID': registration.VisitId,
                        'AppointmentDate': registration.created_at.date().isoformat(),
                        'DoctorId': doctor.Doctor_ID if doctor else "N/A",
                        'DoctorName': f"{doctor.First_Name} {doctor.Last_Name}" if doctor else "N/A",
                        'GenericName': prescription.ItemId.GenericName.GenericName if prescription.ItemId else "N/A",
                        'ItemName': prescription.ItemId.ItemName if prescription.ItemId else "N/A",
                        'Dose': prescription.Dosage,
                        'Route': prescription.Route,
                        'Frequency': prescription.Frequency,
                        'Duration': f"{prescription.DurationNumber} {prescription.DurationUnit}",
                        'Qty': prescription.Qty,
                        'Instruction': prescription.Instruction,
                        'Status': registration.Status,
                        'LoggedBy': prescription.created_by,
                        'Location': location_name,
                        'CreatedAt': prescription.created_at.date().isoformat(),
                        'Patient_Name': PatientName,
                        'MRP' : int(product.Sellable_price),
                        'BatchNo' : product.Batch_No,
                        'Exp_Date' : product.Expiry_Date,

                    }
                    prescription_list.append(prescription_dict)
                    print('Product:', product.Batch_No)
            else:
                print("No products found for the given ItemName")

            

        return JsonResponse(prescription_list, safe=False)

    except Exception as e:
        print('Error:', str(e))
        return JsonResponse({"error": "Internal Server Error: " + str(e)}, status=500)

    
def op_pharmacy_queue_list_prescrib(request):
    try:        
        # Filter drug requests based on location if applicable
        drug_requests = OPD_Prescription_Details.objects.filter(Status = '1')
        
        datafetch = []
        processed_patients = set()  # Set to store processed patient IDs
        record_id = 1
        print('1111111')
        for drug_request in drug_requests:
            registration_id = drug_request.Registration_Id
            if not registration_id:
                continue

            # Check if registration_id is valid and proceed only if it exists
            try:
                print('1111111')
                # room_detail = Patient_Admission_Room_Detials.objects.filter(IP_Registration_Id_id=registration_id).first()
                # if not room_detail:
                #     continue
                
                # room_status = Room_Master_Detials.objects.filter(Room_Id=room_detail.RoomId.Room_Id, Booking_Status='Occupied').first()
                # if not room_status:
                #     continue
                
                patient_data = Patient_Appointment_Registration_Detials.objects.filter(Registration_Id=registration_id.Registration_Id).first()
                print('55555555',patient_data)
                if not patient_data:
                    continue
                
                personal_data = Patient_Detials.objects.filter(PatientId=patient_data.PatientId.PatientId).first()
                print('2222222',personal_data)
                if not personal_data or personal_data.PatientId in processed_patients:
                    continue  # Skip if patient already processed

                processed_patients.add(personal_data.PatientId)  # Add to processed list
                
                # Handle possible None values in name fields
                patient_name = f"{personal_data.FirstName or ''} {personal_data.MiddleName or ''} {personal_data.SurName or ''}".strip()

                datafetch.append({
                    'id': record_id,
                    'VisitID' : registration_id.VisitId,
                    'Booking_Id': registration_id.Registration_Id,  # Ensure this is a serializable ID
                    'PatientName': patient_name,
                    'PatientId': personal_data.PatientId,  # Assuming this is a serializable ID
                    'PatientPhoneNo': personal_data.PhoneNo,
                    'DoctorName': str(drug_request.Registration_Id.PrimaryDoctor.ShortName)  # Convert to string if necessary
                })

                record_id += 1

            except ObjectDoesNotExist as e:
                print(f"Error fetching data for registration_id {registration_id}: {str(e)}")
                continue

        return JsonResponse(datafetch, safe=False)

    except Exception as e:
        return JsonResponse({"Error": str(e)}, status=500)







    
def get_prescriptionqueue(request):
    try:
        # Fetch all prescriptions with related data
        prescriptions = Workbench_Prescription.objects.select_related(
            'Doctor_Id'  # Related doctor details
        ).all()

        # Serialize the prescriptions queryset to JSON
        serialized_prescriptions = serialize('json', prescriptions, use_natural_primary_keys=True)
        
        # Convert serialized data to Python dict
        serialized_data = json.loads(serialized_prescriptions)

        # Dictionary to hold unique patient details
        patient_data = {}
        
        id = 1
        # Enhance the serialized data with additional details
        for item in serialized_data:
            fields = item['fields']
            registration_id = fields.get('Registration_Id')
            doctor_id = fields.get('Doctor_Id')
            
            # Get PatientId using Registration_Id
            appointment = Patient_Appointment_Registration_Detials.objects.filter(id=registration_id).first()
            if appointment:
                patient_id = appointment.PatientId.PatientId
            else:
                patient_id = None
            
            if patient_id:
                if registration_id not in patient_data:
                    patient = Patient_Detials.objects.filter(PatientId=patient_id).first()
                    if patient:
                        # Fetch doctor details
                        doctor = Doctor_Personal_Form_Detials.objects.filter(Doctor_ID=doctor_id).first()
                        doctor_name = f"{doctor.First_Name} {doctor.Last_Name}" if doctor else ''
                        
                        patient_data[registration_id] = {
                            'Patient_Name': f"{patient.FirstName} {patient.MiddleName} {patient.SurName}",
                            'PatientPhoneNo': patient.PhoneNo,
                            'PatientEmail': patient.Email,
                            'PatientCity': patient.City,
                            'PatientState': patient.State,
                            'PatientCountry': patient.Country,
                            'VisitID': appointment.VisitId if appointment else '',
                            'DoctorName': doctor_name,
                            'id': id,
                            'PatientID': patient.PatientId 
                        }
            id += 1    
        # Convert patient data dictionary to list
        enhanced_data = list(patient_data.values())
        
        # Return the enhanced serialized data
        return JsonResponse(enhanced_data, safe=False)

    except Exception as e:
        print('error:', str(e))
        return JsonResponse({"error": "Internal Server Error: " + str(e)}, status=500)
    
    
    
@csrf_exempt
def get_personal_info(request):
    try:
        

        patientdata = Patient_Detials.objects.all()
        serialized_prescriptions = serialize('json', patientdata, use_natural_primary_keys=True)
        
        # Convert serialized data to Python dict
        serialized_data = json.loads(serialized_prescriptions)

        cleaned_data = [
            {
                **item['fields'],
                'PatientId': item['pk'] 
            }
            for item in serialized_data
        ]

        return JsonResponse(cleaned_data, safe=False)


    except Exception as e:
        print(e)
        return JsonResponse({'error': 'Internal Server Error: ' + str(e)},
                            status=500)
    

@csrf_exempt
def get_quick_list(request):
    try:
        # Get location id from query parameters
        location_id = request.GET.get('location')
        
        location = Location_Detials.objects.filter(Location_Id=location_id).first()

        if not location:
            return JsonResponse({'error': 'Location not found'}, status=404)

        stock_query = pharmacy_stock_location_information.objects.filter(Location=location.Location_Name)

        serialized_stock = serialize('json', stock_query, use_natural_primary_keys=True)
        
        serialized_data = json.loads(serialized_stock)
        
        cleaned_data = [
            {
                **item['fields']
            }
            for item in serialized_data
        ]

        return JsonResponse(cleaned_data, safe=False)

        
    except Exception as e:
        print(e)
        return JsonResponse({'error': 'Internal Server Error: ' + str(e)})
    
    
@csrf_exempt
def get_name(request):
    try:
        item_name = request.GET.get('ItemName')  
        batch_no = request.GET.get('BatchNo') 
        location = request.GET.get('location')  
        
        location = Location_Detials.objects.get(Location_Id=location)
        print('location :',location)
        if not location:
            return JsonResponse({'error': f'Location {location} not found'}, status=404)
        
        stock_query = pharmacy_stock_location_information.objects.filter(Location=location.Location_Name,Item_Name=item_name,Batch_No=batch_no)
       
        
        serialized_stock = serialize('json', stock_query, use_natural_primary_keys=True)
        # cleaned_data = [
        #     {
        #         **item['fields']
        #     }
        #     for item in serialized_stock
        # ]
        serialized_data = json.loads(serialized_stock)

        return JsonResponse(serialized_data, safe=False)
    
    except Exception as e:
        print(e)
        return JsonResponse({'error': 'Internal Server Error: ' + str(e)}, status=500)
    



# def get_prescription_forIP(request):
#     try:
#         # Retrieve PatientID from request
#         PatientID = request.GET.get('PatientID')
#         VisitID = request.GET.get('VisitID')

#         # Check if PatientID and VisitID are provided
#         if not PatientID:
#             return JsonResponse({"error": "PatientID parameter is required"}, status=400)
#         if not VisitID:
#             return JsonResponse({"error": "VisitID parameter is required"}, status=400)

#         # Fetch patient details to get the Patient Name
#         patient = Patient_Detials.objects.get(PatientId=PatientID)
#         PatientName = f"{patient.FirstName} {patient.MiddleName} {patient.SurName}"

#         # Query the prescriptions related to the VisitID (Registration_Id_id)
#         prescriptions = ip_drug_request_table.objects.filter(Booking_Id=VisitID)

#         # Prepare the list of prescriptions in the specified format
#         prescription_list = []
#         for prescription in prescriptions:
#             prescription_dict = {
#                 'PrescriptionID': prescription.Drug_Request_Id,
#                 'PatientID': PatientID,
#                 'VisitID': VisitID,  # Mapping VisitID as Registration_Id
#                 'Booking_Id': prescription.Booking_Id,
#                 # 'AppointmentDate': prescription.CreatedAt.date().isoformat(),  # Date of prescription creation
#                 'DoctorName': prescription.DoctorName,
#                 'GenericName': prescription.GenericName,
#                 'ItemName': prescription.MedicineName,
#                 'Dose': prescription.Dosage,
#                 'Route': prescription.Route,
#                 'Frequency': prescription.Duration,  # Assuming Frequency is in Duration
#                 'Duration': prescription.DurationType,
#                 'Qty': prescription.RequestQuantity,
#                 'Instruction': prescription.RequestType,  # Assuming RequestType includes instructions
#                 'Status': prescription.Status,
#                 'LoggedBy': prescription.CreatedBy,
#                 # 'CreatedAt': prescription.CreatedAt.date().isoformat(),
#                 'Patient_Name': PatientName
#             }
#             prescription_list.append(prescription_dict)

#         return JsonResponse(prescription_list, safe=False)

#     except Patient_Detials.DoesNotExist:
#         return JsonResponse({"error": "Patient not found"}, status=404)
#     except Exception as e:
#         print('error:', str(e))
#         return JsonResponse({"error": "Internal Server Error: " + str(e)}, status=500)



# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.db import connection

# @csrf_exempt
# def Post_Ip_PharmacyBilling_table(request):
#     if request.method == 'POST':
#         try:
#             # Extract prescription barcode from the form
#             prescription_barcode = request.POST.get('Priscription_Barcode', None)
            
#             # Extract medicines data
#             Billing_itemtable = []
#             index = 0
#             while True:
#                 item_id = request.POST.get(f'ItemId_{index}', None)
#                 quantity = request.POST.get(f'Billing_Quantity_{index}', None)
#                 if item_id is None and quantity is None:
#                     break
#                 Billing_itemtable.append({
#                     'ItemId': item_id,
#                     'Billing_Quantity': quantity
#                 })
#                 index += 1

#             # Database operations
#             with connection.cursor() as cursor:
#                 if prescription_barcode:
#                     # Update the status of the prescription barcode
#                     update_query_ip = """
#                         UPDATE Ip_Drug_Request_Table
#                         SET Status = 'Completed'
#                         WHERE Priscription_Barcode = %s
#                     """
#                     cursor.execute(update_query_ip, [prescription_barcode])

#                     # Update quantities for each medicine item
#                     for item in Billing_itemtable:
#                         item_id = item.get('ItemId')
#                         quantity = item.get('Billing_Quantity')
#                         if item_id and quantity is not None:
#                             update_query_item = """
#                                 UPDATE Ip_Drug_Request_Table
#                                 SET RecivedQuantity = %s
#                                 WHERE Priscription_Barcode = %s AND MedicineCode = %s
#                             """
#                             cursor.execute(update_query_item, [quantity, prescription_barcode, item_id])

#                     response_data = {'message': 'Data updated successfully'}
#                     return JsonResponse(response_data)
#                 else:
#                     return JsonResponse({'error': 'Prescription barcode is missing'}, status=400)

#         except Exception as e:
#             print(f"An error occurred: {str(e)}")
#             return JsonResponse({'error': 'An internal server error occurred'}, status=500)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=405)



@csrf_exempt
def OP_Billing_Report(request):
    if request.method == 'GET':
        try:
            # Retrieve query parameters
            # SearchbyDate = request.GET.get('SearchbyDate')
            SearchbyFirstName = request.GET.get('SearchbyFirstName')
            SearchbySpeciality = request.GET.get('SearchbySpeciality')
            SearchbyDoctor = request.GET.get('SearchbyDoctor')
            DateType = request.GET.get('DateType')
            CurrentDate=request.GET.get('CurrentDate')  
            FromDate = request.GET.get('FromDate')  
            ToDate = request.GET.get('ToDate')
            SearchTimeOrderby = request.GET.get('SearchTimeOrderby')
            status_filter = request.GET.get('SearchStatus')

            print('status_filter:', status_filter)
            print('Date:', CurrentDate)
            
            # Build dynamic filter query
            search_query = Q()
            
            if SearchbyFirstName:
                search_query &= Q(created_by__icontains=SearchbyFirstName)
            if SearchbySpeciality:
                search_query &= Q(Register_Id__Specialization__Speciality_Id__icontains=SearchbySpeciality)
            if SearchbyDoctor:
                search_query &= Q(Doctor_Id__Doctor_ID__icontains=SearchbyDoctor)
            # if SearchbyDate:
            #     search_query &= Q(Billing_Date__icontains=SearchbyDate)
            if status_filter:
                search_query &= Q(Bill_Status=status_filter)

            
            if DateType == "Current":
                if CurrentDate:
                    search_query &= Q(Billing_Date=CurrentDate)
            elif DateType == "Customize":
                if FromDate and ToDate:
                    search_query &= Q(Billing_Date__range=[FromDate, ToDate])
                elif FromDate:
                    search_query &= Q(Billing_Date__gte=FromDate)
                elif ToDate:
                    search_query &= Q(Billing_Date__lte=ToDate)

            general_billing_data = General_Billing_Table_Detials.objects.filter(search_query)

            # Apply ordering dynamically
            if SearchTimeOrderby:
                if SearchTimeOrderby.lower() == 'order':
                    general_billing_data = general_billing_data.order_by('Billing_Date')  # Ascending
                elif SearchTimeOrderby.lower() == 'disorder':
                    general_billing_data = general_billing_data.order_by('-Billing_Date')  # Descending

            response_data = []
            # Get the total sum of all Paid_Amount after applying the filter
            total_paid_amount = general_billing_data.aggregate(total_paid=Sum('Net_Paid_Amount'))['total_paid'] or 0


            for row in general_billing_data:
                # Construct the patient's full name
                full_name = f"{row.Patient_Id.FirstName} {row.Patient_Id.MiddleName or ''} {row.Patient_Id.SurName}".strip()

                # Prepare the general billing details
                billing_details = {
                    'id': row.Billing_Invoice_No,
                    'Type': 'OPEdit',
                    'Billing_Date': row.Billing_Date,
                    'Doctor_Id': row.Doctor_Id.Doctor_ID,
                    'Doctor_Name': row.Doctor_Id.ShortName,
                    'PatientId': row.Patient_Id.PatientId,
                    'Patient_Name': full_name,
                    'PhoneNo': row.Patient_Id.PhoneNo,
                    'Register_Id': row.Register_Id.Registration_Id,
                    'Gender': row.Register_Id.PatientId.Gender,
                    'City': row.Register_Id.PatientId.City,
                    'State': row.Register_Id.PatientId.State,
                    'Pincode': row.Register_Id.PatientId.Pincode,
                    'AgeGender': f'{row.Register_Id.PatientId.Age}/{row.Register_Id.PatientId.Gender}',
                    'Address':f'{row.Register_Id.PatientId.DoorNo}, {row.Register_Id.PatientId.Street}, {row.Register_Id.PatientId.Area}, {row.Register_Id.PatientId.City}, {row.Register_Id.PatientId.State}, {row.Register_Id.PatientId.Country}, {row.Register_Id.PatientId.Pincode}',
                    'PatientCategory': row.Register_Id.PatientCategory,
                    'PatientCategoryName': (
                        row.Register_Id.InsuranceName.Insurance_Name
                        if row.Register_Id.PatientCategory == 'Insurance'
                        else getattr(row.Register_Id.ClientName, 'Client_Name', None)
                    ),
                    'Visit_Id': row.Visit_Id.VisitId,
                    'Billing_Type': row.Billing_Type,
                    'TotalItems': row.Total_Items,
                    'TotalQty': row.Total_Qty,
                    'RoundOff': row.Round_Off,
                    'TotalAmount': row.Total_Amount,
                    'Net_Amount': row.Net_Amount,
                    'PaidAmount': row.Paid_Amount,
                    'PaidNetAmount': row.Net_Paid_Amount,
                    'BalanceAmount': row.Balance_Amount,
                    'Bill_Status': row.Bill_Status,
                    'TotalPaidAmount':total_paid_amount,
                    'Billing_Items': [],
                    'Payment_Details': [],
                }
                # Fetch related payment details
                payment_details = Multiple_Payment_Table_Detials.objects.filter(Invoice_No_Paid=row.Billing_Invoice_No)
                for payment in payment_details:
                    payment_info = {
                        'Payment_Type': payment.Payment_Type,
                        'Card_Type': payment.Cart_Type,
                        'Card_No': payment.Card_No,
                        'TransactionId': payment.TransactionId,
                        'upiid': payment.upiid,
                        'Cheque_No': payment.Cheque_No,
                        'Bank_Name': payment.Bank_Name,
                        'Amount': payment.Amount,
                        'Transaction_Amount': payment.Transaction_Amount,
                        'AdditionalAmount': payment.AdditionalAmount,
                    }
                    billing_details['Payment_Details'].append(payment_info)

                # Add the billing details to the response data
                response_data.append(billing_details)
                response = {
                    "total_paid_amount": total_paid_amount,
                    "billing_data": response_data
                }

            return JsonResponse(response, safe=False)

        except Exception as e:
            print({'error': str(e)})
            return JsonResponse({'error': str(e)})
        
@csrf_exempt
@require_http_methods(["POST", "OPTIONS", "GET"])
def RadiologyBilling_Link(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
           
            # Extract data from the request
            billAmount = data.get('billAmount', [])
            SelectedPatient_list = data.get('SelectedPatient_list', {})
            NetAmount_CDmethod = data.get('NetAmount_CDmethod', {})
            SelectDatalist = data.get('SelectDatalist', [])
            BillingData = data.get('BillingData', {})
            initialState = data.get('initialState', {})
            Created_by = data.get('Created_by', '')
            Location = data.get('Location', '')
            request_id = data.get('Request_Id','')
            service_type = data.get('ServiceProcedureForm','')
            editid = data.get('EditId','')

            RegisterType = SelectedPatient_list.get(data.get('RegisterType'))


            # selectedOption = data.get('selectedOption', '')
            # remainingadvanceamount=data.get('remainingadvanceamount')
            # advanceid=data.get('advanceid')
            # Fetch related foreign key objects
            print('billAmount',billAmount)
            print('SelectedPatient_list',SelectedPatient_list)
            print('NetAmount_CDmethod',NetAmount_CDmethod)
            print('SelectDatalist',SelectDatalist)
            print('BillingData',BillingData)
            print('initialState',initialState)
            print('service_type',service_type)
            print('request_id',request_id)

            print('1111111')
            # Validate essential data
            if not billAmount:
                return JsonResponse({'error': 'billAmount is empty or missing'}, status=400)
            if not SelectDatalist:
                return JsonResponse({'error': 'SelectDatalist is empty or missing'}, status=400)

            try:
                doctor = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=BillingData.get('DoctorId'))
              
                patient = Patient_Detials.objects.get(PatientId=SelectedPatient_list.get('PatientId'))

                register = None
                opregister = None  
                ipregister = None
                if RegisterType == "OP" or RegisterType == 'RADIOLOGY':
                      opregister = Patient_Appointment_Registration_Detials.objects.filter(pk=SelectedPatient_list.get('RegisterId')).first()
                elif RegisterType == "IP":
                      ipregister = Patient_IP_Registration_Detials.objects.filter(Registration_Id=SelectedPatient_list.get('RegisterId')).first()

               # register = Patient_Appointment_Registration_Detials.objects.get(Registration_Id=SelectedPatient_list.get('RegisterId'))
                
                # visit = Patient_Visit_Detials.objects.get(
                #     PatientId=SelectedPatient_list.get('PatientId'),
                #     VisitId=SelectedPatient_list.get('VisitId')
                # )
                print('lajhdsjsks')
                locationget=Location_Detials.objects.get(Location_Id=Location)
            except ObjectDoesNotExist as e:
                return JsonResponse({'error': f'{str(e).split(":")[1].strip()} not found'})
            except MultipleObjectsReturned:
                return JsonResponse({'error': 'Multiple instances found'})
            print('jdjdjkdkdkd')
            # Convert to Decimal with error handling
            def safe_to_decimal(value, default=0.00):
                try:
                    return Decimal(value)
                except (InvalidOperation, TypeError, ValueError):
                    return Decimal(default)
            print('ueoejcjdjd')
            new_bill_status= 'Paid' if safe_to_decimal(initialState.get('BalanceAmount')) == 0 else 'Due'
            # Begin an atomic transaction
            
            # Create and save the General Billing entry
            print('hello')
            if editid:
                # Edit existing billing entry
                general_billing = Radiology_Billing_Table_Detials.objects.get(Billing_Invoice_No=editid)
                general_billing.Billing_Date = BillingData.get('InvoiceDate')
                general_billing.Doctor_Id = doctor
                general_billing.Patient_Id = patient
                general_billing.OP_Register_Id = register

              #  general_billing.Visit_Id = visit
                general_billing.Billing_Type = NetAmount_CDmethod.get('Method')
                general_billing.Select_Discount = NetAmount_CDmethod.get('Method')
                general_billing.Discount_Type = NetAmount_CDmethod.get('Method')
                general_billing.Discount_Value = safe_to_decimal(NetAmount_CDmethod.get('Amount'))
                general_billing.Discount_Amount = safe_to_decimal(initialState.get('totalDiscount'))
                general_billing.Total_Items = int(initialState.get('totalItems'))
                general_billing.Total_Qty = int(initialState.get('totalUnits'))
                general_billing.Total_Amount = safe_to_decimal(initialState.get('totalTaxable'))
                general_billing.Total_GSTAmount = safe_to_decimal(initialState.get('totalGstamount'))
                general_billing.Net_Amount = safe_to_decimal(initialState.get('totalNetAmount'))
                general_billing.Net_Paid_Amount=safe_to_decimal(initialState.get('totalAmountt'))
                general_billing.Round_Off = safe_to_decimal(initialState.get('Roundoff'))
                general_billing.Paid_Amount = safe_to_decimal(initialState.get('PaidAmount'))
                general_billing.Balance_Amount = safe_to_decimal(initialState.get('BalanceAmount'))
                general_billing.Bill_Status = new_bill_status
                general_billing.save()

                # Delete existing billing items and re-add them
                Radiology_Billing_Items_Table_Detials.objects.filter(Billing_Invoice_No=editid).delete()
                for item in SelectDatalist:
                    print('item:', item)
                    service_cd = item.get('ServiceCode', '') if service_type != 'Lab' else (
                        item.get('Test_Code') if item.get('type') == "individual" else item.get("group")
                    )
                    general_billing_item_instance = Radiology_Billing_Items_Table_Detials(
                        Billing_Invoice_No=general_billing,
                        Service_Type=item.get('ServiceType'),
                        Service_Code=item.get('ServiceCode'),
                        Service_Name=item.get('SelectItemName'),
                        Rate=safe_to_decimal(item.get('Amount')),
                        Charge=safe_to_decimal(item.get('Charges')),
                        Quantity=int(item.get('Quantity', 1)),
                        Amount=safe_to_decimal(item.get('Amount')),
                        Discount_Type=item.get('DiscountType'),
                        Discount_Value=safe_to_decimal(item.get('Discount', 0.00)),
                        Taxable_Amount=safe_to_decimal(item.get('Amount')),
                        Tax_Amount=safe_to_decimal(item.get('GST', 0.00)),
                        Total_Amount=safe_to_decimal(item.get('NetAmount')),
                        Item_Status=new_bill_status,
                    )
                    general_billing_item_instance.save()

                # Delete existing payment details and re-add them
                Multiple_Payment_Radiology_Table_Detials.objects.filter(Invoice_No_Paid=editid).delete()
                for payment in billAmount:
                    print('payment:', payment)
                    multiple_payment_instance = Multiple_Payment_Radiology_Table_Detials(
                        Invoice_No_Paid=editid,
                        Payment_Type=payment.get('Billpay_method'),
                        Cart_Type=payment.get('CardType'),
                        Card_No=payment.get('CardNo'),
                        TransactionId=payment.get('TransactionId'),
                        upiid=payment.get('upiid'),
                        Cheque_No=payment.get('ChequeNo'),
                        Bank_Name=payment.get('BankName'),
                        Amount=safe_to_decimal(payment.get('paidamount')),
                        Transaction_Amount=safe_to_decimal(payment.get('transactionFee')),
                        AdditionalAmount=safe_to_decimal(payment.get('Additionalamount')),
                    )
                    multiple_payment_instance.save()

                # Handle lab queue status update if applicable
                if service_type == 'Lab':
                    lab_queue_instance = Lab_Request_Details.objects.get(
                        Request_Id=request_id, OP_Register_Id__Registration_Id=SelectedPatient_list.get('RegisterId')
                    )
                    lab_queue_instance.Billing_Status = 'Completed'
                    lab_queue_instance.Billing_Invoice_No = general_billing
                    lab_queue_instance.save()

                return JsonResponse({'status': 'Success', 'InvoiceNo': editid})
            else:
                general_billing = Radiology_Billing_Table_Detials(
                    Billing_Date=BillingData.get('InvoiceDate'),
                    Doctor_Id=doctor,
                    Patient_Id=patient,
                    OP_Register_Id=opregister,
                    IP_Register_Id = ipregister,

                    # IP_Register_Id = register,
                    # Visit_Id=visit,
                    Billing_Type=NetAmount_CDmethod.get('Method'),
                    Select_Discount=NetAmount_CDmethod.get('Method'),
                    Discount_Type=NetAmount_CDmethod.get('Method'),
                    Discount_Value=NetAmount_CDmethod.get('Amount') if NetAmount_CDmethod.get('Amount') != '' else 0.00,
                    Discount_Amount=initialState.get('totalDiscount'),
                    Total_Items=int(initialState.get('totalItems')),
                    Total_Qty=int(initialState.get('totalUnits')),
                    Total_Amount=initialState.get('totalTaxable'),
                    Total_GSTAmount=initialState.get('totalGstamount'),
                    Net_Amount=initialState.get('totalNetAmount'),
                    Net_Paid_Amount=initialState.get('totalAmountt'),
                    Round_Off=initialState.get('Roundoff'),
                    Paid_Amount=initialState.get('PaidAmount'),
                    Balance_Amount=initialState.get('BalanceAmount'),
                    Bill_Status=new_bill_status,
                    created_by=Created_by,
                    Location=locationget
                )
                general_billing.save()

                print('dvwebjvwhbvjwe')

                if service_type == 'Lab':
                    service_code = ''
                # Save each item in the General Billing Items Table Details
                for item in SelectDatalist:
                    service_cd = ''
                    if service_type == 'Lab':
                        if item.get('type') == "individual":
                            service_cd = item.get('Test_Code')
                        elif item.get('type') == "individual":
                            service_cd = item.get("group")
                    else:
                        service_cd = item.get('ServiceCode')
                    print('vsdvsdvsdv',service_cd)

                    def safe_to_decimal(value, default=0.00):
                        try:
                            return Decimal(value)
                        except (InvalidOperation, TypeError, ValueError):
                            return Decimal(default)
                        
                    general_billing_item = Radiology_Billing_Items_Table_Detials(
                        Billing_Invoice_No=general_billing,
                        Service_Type=item.get('ServiceType'),
                        Service_Code=service_cd,
                        Service_Name=item.get('SelectItemName'),
                        Rate=safe_to_decimal(item.get('Amount')) ,
                        Charge=safe_to_decimal(item.get('Charges')),
                        Quantity=int(item.get('Quantity',1)),
                        Amount=safe_to_decimal(item.get('Amount')),
                        Discount_Type=item.get('DiscountType'),
                        Discount_Value=safe_to_decimal(item.get('Discount') if item.get('Discount') != "" else 0.00),
                        # Discount_Amount=to_decimal(item.get('DiscountAmount')),
                        Taxable_Amount=safe_to_decimal(item.get('Amount')),
                        # Tax_Percentage= item.get('GST'),
                        Tax_Amount=safe_to_decimal(item.get('GST') if item.get('GST') != "" else 0.00),
                        Total_Amount=safe_to_decimal(item.get('NetAmount')), 
                        Item_Status=new_bill_status,
                    )
                    general_billing_item.save()
                    
                # Save multiple payment details
                print('ucjcjvjhcj')
                for payment in billAmount:
                
                    multiple_payment = Multiple_Payment_Radiology_Table_Detials(
                        Invoice_No_Paid=general_billing.Billing_Invoice_No,
                        Payment_Type=payment.get('Billpay_method'),
                        Cart_Type=payment.get('CardType'),
                        Card_No=payment.get('CardNo'),
                        TransactionId=payment.get('TransactionId'),
                        upiid=payment.get('upiid'),
                        Cheque_No=payment.get('ChequeNo'),
                        Bank_Name=payment.get('BankName'),
                        Amount=safe_to_decimal(payment.get('paidamount')),
                        Transaction_Amount = safe_to_decimal(payment.get('transactionFee')),
                        AdditionalAmount = safe_to_decimal(payment.get('Additionalamount')),
                    )
                    multiple_payment.save()
                    # if payment.get('Billpay_method') == 'Advance':
                    #     advance_record = advancemaintaintable.objects.get(
                    #     id=advanceid
                    # )
                    # # Calculate new remaining amount
                    #     advance_record.Remaining_amount = remainingadvanceamount
                    # # Update the record
                    #     advance_record.paidamount = to_decimal(initialState.get('totalTaxable'))
                    #     advance_record.save()

                    if service_type == 'Lab':
                        print('yvkjhgjh', request_id, SelectedPatient_list.get('RegisterId'))
                        try:
                            patient_ins = Patient_Appointment_Registration_Detials.objects.get(Registration_Id=SelectedPatient_list.get('RegisterId'))
                            print('11111', patient_ins)
                            # Use .filter() instead of .get() to avoid exceptions if no record is found
                            lab_qeue_ins = Lab_Request_Details.objects.filter(Request_Id=request_id, OP_Register_Id__Registration_Id=patient_ins.pk).first()
                            
                            if lab_qeue_ins:
                                print('svwevwevwe', lab_qeue_ins)
                                lab_qeue_ins.Billing_Status = 'Completed'
                                lab_qeue_ins.Billing_Invoice_No = general_billing
                                lab_qeue_ins.save()
                            else:
                                print("No matching Lab_Request_Details found.")
                        except Patient_Appointment_Registration_Detials.DoesNotExist:
                            print("Patient not found.")
                        except Exception as e:
                            print(f"An error occurred: {e}")

                # if SelectedPatient_list.get('QueueList_ID'):
                #     try:
                #         billing_queue_list_instance = OP_Billing_QueueList_Detials.objects.get(BillingQueueList_ID=SelectedPatient_list.get('QueueList_ID'))
                #         billing_queue_list_instance.Status = new_bill_status
                #         billing_queue_list_instance.save()
                #     except ObjectDoesNotExist:
                #         return JsonResponse({'error': 'Billing Queue List not found'})
                #     except MultipleObjectsReturned:
                #         return JsonResponse({'error': 'Multiple Billing Queue List instances found'})


                # billing_receipt_table = GeneralBillingReceipt(
                #     Invoice_NO=general_billing,
                #     PatientID=patient.PatientId,
                #     PhoneNumber=patient.PhoneNo,
                #     Patient_Name=f"{patient.FirstName} {patient.MiddleName or ''} {patient.SurName}".strip(),
                #     TotalAmount= safe_to_decimal(initialState.get('totalNetAmount')),
                #     TotalPaidAmount=safe_to_decimal(initialState.get('PaidAmount')),
                #     BalanceAmount=safe_to_decimal(initialState.get('BalanceAmount')),
                #     Billing_Date=BillingData.get('InvoiceDate'),
                #     PaidAmount=safe_to_decimal(initialState.get('PaidAmount')),
                #     Billedby=Created_by,
                # )
                # billing_receipt_table.save()
                invoicenoforbill=general_billing.Billing_Invoice_No
                
                
                
                
                
                
                
                
                
                
                
                return JsonResponse({'status': 'Success','InvoiceNo':invoicenoforbill})
            
        except Exception as e:
            print(str(e))
            return JsonResponse({'error': str(e)}, status=500)


    elif request.method == "GET":
        try:
            # Retrieve query parameters
            SearchbyDate = request.GET.get('SearchbyDate')
            SearchbyFirstName = request.GET.get('SearchbyFirstName')
            SearchbyPhoneNumber = request.GET.get('SearchbyPhoneNumber')
            SearchTimeOrderby = request.GET.get('SearchTimeOrderby')
            status_filter = request.GET.get('SearchStatus')

            print('status_filter:', status_filter)
            
            # Build dynamic filter query
            search_query = Q()
            
            if SearchbyFirstName:
                search_query &= Q(Register_Id__PatientId__FirstName__icontains=SearchbyFirstName)
            if SearchbyPhoneNumber:
                search_query &= Q(Register_Id__PatientId__PhoneNo__icontains=SearchbyPhoneNumber)
            if SearchbyDate:
                search_query &= Q(Billing_Date__icontains=SearchbyDate)
            if status_filter:
                search_query &= Q(Bill_Status=status_filter)


            general_billing_data = Radiology_Billing_Table_Detials.objects.filter(search_query)

                        # Apply ordering dynamically
            if SearchTimeOrderby:
                if SearchTimeOrderby.lower() == 'order':
                    general_billing_data = general_billing_data.order_by('Billing_Date')  # Ascending
                elif SearchTimeOrderby.lower() == 'disorder':
                    general_billing_data = general_billing_data.order_by('-Billing_Date')  # Descending

            response_data = []

            for row in general_billing_data:
                # Construct the patient's full name
                full_name = f"{row.Patient_Id.FirstName} {row.Patient_Id.MiddleName or ''} {row.Patient_Id.SurName}".strip()

                # Prepare the general billing details
                billing_details = {
                    'id': row.Billing_Invoice_No,
                    'Type': 'OPEdit',
                    'Billing_Date': row.Billing_Date,
                    'Doctor_Id': row.Doctor_Id.Doctor_ID,
                    'Doctor_Name': row.Doctor_Id.ShortName,
                    'PatientId': row.Patient_Id.PatientId,
                    'Patient_Name': full_name,
                    'PhoneNo': row.Patient_Id.PhoneNo,
                    'Register_Id': row.Register_Id.Registration_Id,
                    'Gender': row.Register_Id.PatientId.Gender,
                    'City': row.Register_Id.PatientId.City,
                    'State': row.Register_Id.PatientId.State,
                    'Pincode': row.Register_Id.PatientId.Pincode,
                    'AgeGender': f'{row.Register_Id.PatientId.Age}/{row.Register_Id.PatientId.Gender}',
                    'Address':f'{row.Register_Id.PatientId.DoorNo}, {row.Register_Id.PatientId.Street}, {row.Register_Id.PatientId.Area}, {row.Register_Id.PatientId.City}, {row.Register_Id.PatientId.State}, {row.Register_Id.PatientId.Country}, {row.Register_Id.PatientId.Pincode}',
                    'PatientCategory': row.Register_Id.PatientCategory,
                    'PatientCategoryName': (
                        row.Register_Id.InsuranceName.Insurance_Name
                        if row.Register_Id.PatientCategory == 'Insurance'
                        else getattr(row.Register_Id.ClientName, 'Client_Name', None)
                    ),
                    'Visit_Id': row.Visit_Id.VisitId,
                    'Billing_Type': row.Billing_Type,
                    'TotalItems': row.Total_Items,
                    'TotalQty': row.Total_Qty,
                    'RoundOff': row.Round_Off,
                    'TotalAmount': row.Total_Amount,
                    'Net_Amount': row.Net_Amount,
                    'PaidAmount': row.Paid_Amount,
                    'PaidNetAmount': row.Net_Paid_Amount,
                    'BalanceAmount': row.Balance_Amount,
                    'Bill_Status': row.Bill_Status,
                    'Billing_Items': [],
                    'Payment_Details': [],
                }

                # Fetch related billing items
                billing_items = Radiology_Billing_Items_Table_Detials.objects.filter(Billing_Invoice_No=row.Billing_Invoice_No)
                for item in billing_items:
                    item_details = {
                        'Service_Type': item.Service_Type,
                        # 'Service_Code': item.Service_Code,
                        'Service_Name': item.Service_Name,
                        'Rate': item.Rate,
                        'Charge': item.Charge,
                        'Quantity': item.Quantity,
                        'Amount': item.Amount,
                        'Discount_Type': item.Discount_Type,
                        'Discount_Value': item.Discount_Value,
                        'Discount_Amount': item.Discount_Amount,
                        'Taxable_Amount': item.Taxable_Amount,
                        # 'Tax_Percentage': item.Tax_Percentage,
                        'Tax_Amount': item.Tax_Amount,
                        'Total_Amount': item.Total_Amount,
                    }
                    billing_details['Billing_Items'].append(item_details)

                # Fetch related payment details
                payment_details = Multiple_Payment_Radiology_Table_Detials.objects.filter(Invoice_No_Paid=row.Billing_Invoice_No)
                for payment in payment_details:
                    payment_info = {
                        'Payment_Type': payment.Payment_Type,
                        'Card_Type': payment.Cart_Type,
                        'Card_No': payment.Card_No,
                        'TransactionId': payment.TransactionId,
                        'upiid': payment.upiid,
                        'Cheque_No': payment.Cheque_No,
                        'Bank_Name': payment.Bank_Name,
                        'Amount': payment.Amount,
                        'Transaction_Amount': payment.Transaction_Amount,
                        'AdditionalAmount': payment.AdditionalAmount,
                    }
                    billing_details['Payment_Details'].append(payment_info)

                # Add the billing details to the response data
                response_data.append(billing_details)

            return JsonResponse(response_data, safe=False)

        except Exception as e:
            print({'error': str(e)})
            return JsonResponse({'error': str(e)})

            

    return JsonResponse({'status': 'failure', 'message': 'Invalid request method'})





@csrf_exempt
@require_http_methods(["GET"])
def Get_Radiology_Billing_Details(request):


    
    try:
        location = request.GET.get('location')
        Status = request.GET.get('Status','Pending')
        searchBy = request.GET.get('searchBy')
        
        print('222222',location,Status,searchBy)
         
        if Status == 'Unpaid':

            try:
                            query = request.GET.get('query', '')
                            # status = request.GET.get('status', '')

                            print(Status,'status')
                            print(query,'query')

                            queryset = Radiology_Request_Details.objects.all()

                            # print(queryset,'queryset')

                            # Filter based on query parameter
                            if query:
                                queryset = queryset.filter(
                                    Q(OP_Register_Id__PatientId__FirstName__icontains=query) |
                                    Q(OP_Register_Id__PatientId__MiddleName__icontains=query) |
                                    Q(OP_Register_Id__PatientId__SurName__icontains=query) |
                                    Q(OP_Register_Id__PatientId__PatientId__icontains=query) |
                                    Q(OP_Register_Id__PatientId__PhoneNo__icontains=query) |
                                    Q(IP_Register_Id__PatientId__FirstName__icontains=query) |
                                    Q(IP_Register_Id__PatientId__MiddleName__icontains=query) |
                                    Q(IP_Register_Id__PatientId__SurName__icontains=query) |
                                    Q(IP_Register_Id__PatientId__PatientId__icontains=query) |
                                    Q(IP_Register_Id__PatientId__PhoneNo__icontains=query) |
                                    Q(Casuality_Register_Id__PatientId__FirstName__icontains=query) |
                                    Q(Casuality_Register_Id__PatientId__MiddleName__icontains=query) |
                                    Q(Casuality_Register_Id__PatientId__SurName__icontains=query) |
                                    Q(Casuality_Register_Id__PatientId__PatientId__icontains=query) |
                                    Q(Casuality_Register_Id__PatientId__PhoneNo__icontains=query) |
                                    Q(Diagnosis_Register_Id__PatientId__FirstName__icontains=query) |
                                    Q(Diagnosis_Register_Id__PatientId__MiddleName__icontains=query) |
                                    Q(Diagnosis_Register_Id__PatientId__SurName__icontains=query) |
                                    Q(Diagnosis_Register_Id__PatientId__PatientId__icontains=query) |
                                    Q(Diagnosis_Register_Id__PatientId__PhoneNo__icontains=query)
                                )

                            # Filter by status if provided
                            if Status:
                                queryset = queryset.filter(Q(Status__icontains=Status))

                            # print(queryset,'queryset')

                            response_data = []
                            seen_registration_ids = set()  # Set to track unique registration IDs
                            index = 1  # Initialize index

                            for radiology_request in queryset:
                                registration_id = None
                                registration_details = None

                                # Determine which registration ID and details to use based on RegisterType
                                if radiology_request.RegisterType == 'OP' or radiology_request.RegisterType == 'RADIOLOGY'  and radiology_request.OP_Register_Id:
                                    registration_id = radiology_request.OP_Register_Id.pk
                                    registration_details = radiology_request.OP_Register_Id
                                elif radiology_request.RegisterType == 'IP' and radiology_request.IP_Register_Id:
                                    registration_id = radiology_request.IP_Register_Id.Registration_Id
                                    registration_details = radiology_request.IP_Register_Id
                                elif radiology_request.RegisterType == 'Casuality' and radiology_request.Casuality_Register_Id:
                                    registration_id = radiology_request.Casuality_Register_Id.Registration_Id
                                    registration_details = radiology_request.Casuality_Register_Id
                                elif radiology_request.RegisterType == "ExternalRadiology" and radiology_request.Diagnosis_Register_Id:
                                    registration_id = radiology_request.Diagnosis_Register_Id.pk  # Added to ensure registration_id is set
                                    registration_details = radiology_request.Diagnosis_Register_Id
                                

                                # Skip if the registration_id is not set or if already processed
                                if not registration_id or registration_id in seen_registration_ids:
                                    continue

                                # Add registration ID to the set to avoid duplicates
                                seen_registration_ids.add(registration_id)

                                # Extract patient and doctor details, handling None gracefully
                                patient = registration_details.PatientId
                                doctor = registration_details.PrimaryDoctor if registration_details.PrimaryDoctor else None

                                patient_id = patient.PatientId if patient else None
                                patient_age = patient.Age if patient else None
                                patient_gender = patient.Gender if patient else None
                                patient_name = f"{patient.FirstName or ''} {patient.MiddleName or ''} {patient.SurName or ''}".strip() if patient else None
                                phone_number = patient.PhoneNo if patient else None
                                doctor_id = doctor.Doctor_ID if doctor else None
                                doctor_shortname = doctor.ShortName if doctor else None
                                doctor_name = f"{doctor.Tittle.Title_Name}. {doctor.First_Name}{doctor.Middle_Name}{doctor.Last_Name}" if doctor else None

                                if radiology_request.RegisterType == 'OP' or radiology_request.RegisterType == 'RADIOLOGY':

                                    visitId = registration_details.VisitId
                                else :
                                    visitId = None

                                # Add the collected data to the response
                                response_data.append({
                                    'id': index,
                                    'PatientId': patient_id,
                                    'VisitId': visitId,
                                    'RegistrationId': registration_id,
                                    'Patient_Name': patient_name,
                                    'PhoneNo': phone_number,
                                    'DoctorId': doctor_id,
                                    'DoctorShortName': doctor_shortname,
                                    'Doctor_ShortName': doctor_name,
                                    'RegisterType': radiology_request.RegisterType,
                                    # 'age': patient_age,
                                    # 'gender': patient_gender,
                                    'Status': radiology_request.Status,
                                    'AgeGender': f'{patient_age}/{patient_gender}',
                                    'VisitPurpose' : 'RADIOLOGY',
                                    'VisitType' : radiology_request.RegisterType
                                })

                                # Increment index
                                index += 1

                            # Return the collected data as a JSON response
                            return JsonResponse(response_data, safe=False)

            except Exception as e:
                print("Exception:", e)
                return JsonResponse({'error': 'An internal server error occurred'}, status=500)

        elif Status == 'Paid':
              
            try:
                            query = request.GET.get('query', '')
                            # status = request.GET.get('status', '')

                            print(Status,'status')
                            print(query,'query')

                            queryset = Radiology_Request_Details.objects.all()

                            # print(queryset,'queryset')

                            # Filter based on query parameter
                            if query:
                                queryset = queryset.filter(
                                    Q(OP_Register_Id__PatientId__FirstName__icontains=query) |
                                    Q(OP_Register_Id__PatientId__MiddleName__icontains=query) |
                                    Q(OP_Register_Id__PatientId__SurName__icontains=query) |
                                    Q(OP_Register_Id__PatientId__PatientId__icontains=query) |
                                    Q(OP_Register_Id__PatientId__PhoneNo__icontains=query) |
                                    Q(IP_Register_Id__PatientId__FirstName__icontains=query) |
                                    Q(IP_Register_Id__PatientId__MiddleName__icontains=query) |
                                    Q(IP_Register_Id__PatientId__SurName__icontains=query) |
                                    Q(IP_Register_Id__PatientId__PatientId__icontains=query) |
                                    Q(IP_Register_Id__PatientId__PhoneNo__icontains=query) |
                                    Q(Casuality_Register_Id__PatientId__FirstName__icontains=query) |
                                    Q(Casuality_Register_Id__PatientId__MiddleName__icontains=query) |
                                    Q(Casuality_Register_Id__PatientId__SurName__icontains=query) |
                                    Q(Casuality_Register_Id__PatientId__PatientId__icontains=query) |
                                    Q(Casuality_Register_Id__PatientId__PhoneNo__icontains=query) |
                                    Q(Diagnosis_Register_Id__PatientId__FirstName__icontains=query) |
                                    Q(Diagnosis_Register_Id__PatientId__MiddleName__icontains=query) |
                                    Q(Diagnosis_Register_Id__PatientId__SurName__icontains=query) |
                                    Q(Diagnosis_Register_Id__PatientId__PatientId__icontains=query) |
                                    Q(Diagnosis_Register_Id__PatientId__PhoneNo__icontains=query)
                                )

                            # Filter by status if provided
                            if Status:
                                queryset = queryset.filter(Q(Status__icontains=Status))

                            # print(queryset,'queryset')

                            response_data = []
                            seen_registration_ids = set()  # Set to track unique registration IDs
                            index = 1  # Initialize index

                            for radiology_request in queryset:
                                registration_id = None
                                registration_details = None

                                # Determine which registration ID and details to use based on RegisterType
                                if radiology_request.RegisterType == 'OP' or radiology_request.RegisterType == 'RADIOLOGY'  and radiology_request.OP_Register_Id:
                                    registration_id = radiology_request.OP_Register_Id.pk
                                    registration_details = radiology_request.OP_Register_Id
                                elif radiology_request.RegisterType == 'IP' and radiology_request.IP_Register_Id:
                                    registration_id = radiology_request.IP_Register_Id.Registration_Id
                                    registration_details = radiology_request.IP_Register_Id
                                elif radiology_request.RegisterType == 'Casuality' and radiology_request.Casuality_Register_Id:
                                    registration_id = radiology_request.Casuality_Register_Id.Registration_Id
                                    registration_details = radiology_request.Casuality_Register_Id
                                elif radiology_request.RegisterType == "ExternalRadiology" and radiology_request.Diagnosis_Register_Id:
                                    registration_id = radiology_request.Diagnosis_Register_Id.pk  # Added to ensure registration_id is set
                                    registration_details = radiology_request.Diagnosis_Register_Id
                                

                                # Skip if the registration_id is not set or if already processed
                                if not registration_id or registration_id in seen_registration_ids:
                                    continue

                                # Add registration ID to the set to avoid duplicates
                                seen_registration_ids.add(registration_id)

                                # Extract patient and doctor details, handling None gracefully
                                patient = registration_details.PatientId
                                doctor = registration_details.PrimaryDoctor if registration_details.PrimaryDoctor else None

                                patient_id = patient.PatientId if patient else None
                                patient_age = patient.Age if patient else None
                                patient_gender = patient.Gender if patient else None
                                patient_name = f"{patient.FirstName or ''} {patient.MiddleName or ''} {patient.SurName or ''}".strip() if patient else None
                                phone_number = patient.PhoneNo if patient else None
                                doctor_id = doctor.Doctor_ID if doctor else None
                                doctor_shortname = doctor.ShortName if doctor else None
                                doctor_name = f"{doctor.Tittle.Title_Name}. {doctor.First_Name}{doctor.Middle_Name}{doctor.Last_Name}" if doctor else None

                                if radiology_request.RegisterType == 'OP' or radiology_request.RegisterType == 'RADIOLOGY':

                                    visitId = registration_details.VisitId
                                else :
                                    visitId = None

                                # Add the collected data to the response
                                response_data.append({
                                    'id': index,
                                    'PatientId': patient_id,
                                    'VisitId': visitId,
                                    'RegistrationId': registration_id,
                                    'Patient_Name': patient_name,
                                    'PhoneNo': phone_number,
                                    'DoctorId': doctor_id,
                                    'DoctorShortName': doctor_shortname,
                                    'Doctor_ShortName': doctor_name,
                                    'RegisterType': radiology_request.RegisterType,
                                    # 'age': patient_age,
                                    # 'gender': patient_gender,
                                    'Status': radiology_request.Status,
                                    'AgeGender': f'{patient_age}/{patient_gender}',
                                    'VisitPurpose' : 'RADIOLOGY',
                                    'VisitType' : radiology_request.RegisterType
                                })

                                # Increment index
                                index += 1

                            # Return the collected data as a JSON response
                            return JsonResponse(response_data, safe=False)

            except Exception as e:
                print("Exception:", e)
                return JsonResponse({'error': 'An internal server error occurred'}, status=500)


       
       

           
  


    except Exception  as e:
        print({'error':str(e)})
        return JsonResponse ({'error':str(e)})