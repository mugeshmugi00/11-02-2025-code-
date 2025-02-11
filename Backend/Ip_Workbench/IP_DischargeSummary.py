from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from .models import *
from django.utils.timezone import now





@csrf_exempt
@require_http_methods(['POST', 'GET'])
def IP_DischargeSummary_Details_Link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data, 'Received Data')

            RegistrationId = data.get("RegistrationId")
            FinalDiagnosis = data.get("finalDiagnosis", '')
            PresentingComplaints = data.get("presentingComplaints", '')
            PastMedicalHistory = data.get("PastMedicalHistory", '')
            AllergyHistory = data.get("AllergyHistory", '')
            Vitals = data.get("vitals", '')
            DischargeNotes = data.get("dischargeNotes", '')
            Referdoctor = data.get("Referdoctor", '')
            ConditionOnDischarge = data.get("ConditionOnDischarge", '')
            PrescriptionSummary = data.get("PrescriptionSummary", '')
            NoOfDays = data.get("NoOfDays", '')
            TimeInterval = data.get("TimeInterval", '')
            Date = data.get("Date", '')
            DietAdvice = data.get("DietAdvice", '')
            Emergency = data.get("Emergency", '')
            AdviceOnDischarge = data.get("AdviceOnDischarge", '')
            DoctorSchedule = data.get("doctorSchedule", '')
            DepartmentType = data.get("DepartmentType")
            createdby = data.get("Createdby")

            registration_ins_ip = None
            registration_ins_casuality = None

            print(f"Received RegistrationId: {RegistrationId}")  # Debugging line

            if RegistrationId:
                # Attempt to find registration in IP or Casualty tables
                try:
                    registration_ins_ip = Patient_IP_Registration_Detials.objects.get(pk=RegistrationId)
                    print("Found in IP Registration")
                except Patient_IP_Registration_Detials.DoesNotExist:
                    print("Not found in IP Registration, trying Casuality Registration")
                    try:
                        registration_ins_casuality = Patient_Casuality_Registration_Detials.objects.get(pk=RegistrationId)
                        print("Found in Casuality Registration")
                    except Patient_Casuality_Registration_Detials.DoesNotExist:
                        return JsonResponse({'error': 'No registration found for the given RegistrationId'})

                # Update existing discharge summary if it exists
                try:
                    DischargeSummary = IP_DischargeSummary.objects.get(Ip_Registration_Id=RegistrationId)
                    DischargeSummary.DepartmentType = DepartmentType
                    DischargeSummary.FinalDiagnosis = FinalDiagnosis
                    DischargeSummary.PresentingComplaints = PresentingComplaints
                    DischargeSummary.PastMedicalHistory = PastMedicalHistory
                    DischargeSummary.AllergyHistory = AllergyHistory
                    DischargeSummary.Vitals = Vitals
                    DischargeSummary.DischargeNotes = DischargeNotes
                    DischargeSummary.Referdoctor = Referdoctor
                    DischargeSummary.ConditionOnDischarge = ConditionOnDischarge
                    DischargeSummary.PrescriptionSummary = PrescriptionSummary
                    DischargeSummary.NoOfDays = NoOfDays
                    DischargeSummary.TimeInterval = TimeInterval
                    DischargeSummary.Date = Date
                    DischargeSummary.DietAdvice = DietAdvice
                    DischargeSummary.Emergency = Emergency
                    DischargeSummary.AdviceOnDischarge = AdviceOnDischarge
                    DischargeSummary.DoctorSchedule = DoctorSchedule
                    DischargeSummary.Created_by = createdby
                    DischargeSummary.save()
                except IP_DischargeSummary.DoesNotExist:
                    # Create a new discharge summary if it doesn't exist
                    Discharge_instance = IP_DischargeSummary(
                        Ip_Registration_Id=registration_ins_ip,
                        Casuality_Registration_Id=registration_ins_casuality,
                        DepartmentType=DepartmentType,
                        FinalDiagnosis=FinalDiagnosis,
                        PresentingComplaints=PresentingComplaints,
                        PastMedicalHistory=PastMedicalHistory,
                        AllergyHistory=AllergyHistory,
                        Vitals=Vitals,
                        DischargeNotes=DischargeNotes,
                        Referdoctor=Referdoctor,
                        ConditionOnDischarge=ConditionOnDischarge,
                        PrescriptionSummary=PrescriptionSummary,
                        NoOfDays=NoOfDays,
                        TimeInterval=TimeInterval,
                        Date=Date,
                        DietAdvice=DietAdvice,
                        Emergency=Emergency,
                        AdviceOnDischarge=AdviceOnDischarge,
                        DoctorSchedule=DoctorSchedule,
                        Created_by=createdby,
                    )
                    Discharge_instance.save()

            else:
                return JsonResponse({'error': 'RegistrationId is required'})

            return JsonResponse({'success': 'Discharge summary details saved successfully'})

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

    elif request.method == 'GET':
        try:
            Ip_Registration_Id = request.GET.get('RegistrationId')
            DepartmentType = request.GET.get('DepartmentType')

            if not Ip_Registration_Id and not DepartmentType:
                return JsonResponse({'error': 'Both Ip_Registration_Id and DepartmentType are required'})

            if DepartmentType == 'IP':
                Discharge_Details = IP_DischargeSummary.objects.filter(Ip_Registration_Id__pk=Ip_Registration_Id, DepartmentType=DepartmentType)
            else:
                Discharge_Details = IP_DischargeSummary.objects.filter(Casuality_Registration_Id__pk=Ip_Registration_Id, DepartmentType=DepartmentType)

            # Serialize data
            Discharge_Details_data = []
            for idx, Discharge in enumerate(Discharge_Details, start=1):
                ip_registration = Discharge.Ip_Registration_Id
                casuality_registration = Discharge.Casuality_Registration_Id
                
               
                Discharge_dict = {
                    'id': idx,
                    # 'RegistrationId': Discharge.Ip_Registration_Id.pk if Discharge.Ip_Registration_Id else Discharge.Casuality_Registration_Id.pk,
                    # 'VisitId': Discharge.Ip_Registration_Id.VisitId if Discharge.Ip_Registration_Id else Discharge.Casuality_Registration_Id.VisitId,
                    # 'PrimaryDoctorId': Discharge.Ip_Registration_Id.PrimaryDoctor.Doctor_ID if Discharge.Ip_Registration_Id else Discharge.Casuality_Registration_Id.PrimaryDoctor.Doctor_ID,
                    # 'PrimaryDoctorName': Discharge.Ip_Registration_Id.PrimaryDoctor.ShortName if Discharge.Ip_Registration_Id else Discharge.Casuality_Registration_Id.PrimaryDoctor.ShortName,
                    'RegistrationId': ip_registration.pk if ip_registration else casuality_registration.pk if casuality_registration else None,
                    'PrimaryDoctorId': (
                        ip_registration.PrimaryDoctor.Doctor_ID if ip_registration and ip_registration.PrimaryDoctor 
                        else casuality_registration.PrimaryDoctor.Doctor_ID if casuality_registration and casuality_registration.PrimaryDoctor 
                        else None
                    ),
                    'PrimaryDoctorName': (
                        ip_registration.PrimaryDoctor.ShortName if ip_registration and ip_registration.PrimaryDoctor 
                        else casuality_registration.PrimaryDoctor.ShortName if casuality_registration and casuality_registration.PrimaryDoctor 
                        else None
                    ),
                   
                    'FinalDiagnosis': Discharge.FinalDiagnosis,
                    'PresentingComplaints': Discharge.PresentingComplaints,
                    'PastMedicalHistory': Discharge.PastMedicalHistory,
                    'AllergyHistory': Discharge.AllergyHistory,
                    'Vitals': Discharge.Vitals,
                    'DischargeNotes': Discharge.DischargeNotes,
                    'Referdoctor': Discharge.Referdoctor,
                    'ConditionOnDischarge': Discharge.ConditionOnDischarge,
                    'PrescriptionSummary': Discharge.PrescriptionSummary,
                    'NoOfDays': Discharge.NoOfDays,
                    'TimeInterval': Discharge.TimeInterval,
                    'Date': Discharge.Date,
                    'DietAdvice': Discharge.DietAdvice,
                    'Emergency': Discharge.Emergency,
                    'AdviceOnDischarge': Discharge.AdviceOnDischarge,
                    'DoctorSchedule': Discharge.DoctorSchedule,
                    'DepartmentType': Discharge.DepartmentType,
                    'CurrDate': Discharge.created_at.strftime('%d-%m-%y'),
                    'CurrTime': Discharge.created_at.strftime('%H:%M:%S'),
                    'Createdby': Discharge.Created_by,
                }
                Discharge_Details_data.append(Discharge_dict)

            return JsonResponse(Discharge_Details_data, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

