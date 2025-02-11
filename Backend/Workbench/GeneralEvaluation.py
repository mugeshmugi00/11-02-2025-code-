from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import *
import json
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
# import magic
import filetype
import base64
from django.db.models import Q
from Masters.models import *


def Generate_Next_Code_3digit(max_code):
    numeric_part = max_code[-3:]
    prefix = max_code[:-3]
    next_number = int(numeric_part) + 1
    new_code = f"{prefix}{next_number:03d}"

    return new_code



@csrf_exempt
@require_http_methods(["POST", "OPTIONS", "GET"])
def Workbench_GeneralEvaluation_Details(request):

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

        def compress_image(image, min_quality=50, step=5):
            output = BytesIO()
            quality = 95
            compressed_data = None
            while quality >= min_quality:
                output.seek(0)
                image.save(output, format='JPEG', quality=quality)
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
            file_data = file.split(',')[1] if ',' in file else file
            file_content = base64.b64decode(file_data)
            file_size = len(file_content)
            max_size_mb = 5

            if file_size > max_size_mb * 1024 * 1024:
                return JsonResponse({'warn': f'File size exceeds the maximum allowed size ({max_size_mb}MB)'})

            file_type = get_file_type(file)

            if file_type in ['image/jpeg', 'image/png']:
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
            data = request.POST
            
            cheifComplaint = data.get('cheifComplaint','')
            KeyComplaint = data.get('KeyComplaint','')
            History = data.get('History','')
            Examine = data.get('Examine','')
            Diagnosis = data.get('Diagnosis','')

            SearchICDCode = data.get('SearchICDCode','')
            SearchDescription = data.get('SearchDescription','')
            SearchDiagnosis = data.get('SearchDiagnosis','')

            ChooseDocument = data.get('ChooseDocument', None)

            currentAnnotation = data.get('currentAnnotation', None)

            
            DiseaseDetails = data.get('DiseaseDetails',None)
            diseasedata = json.loads(DiseaseDetails)
            print(diseasedata)
             
           
            created_by = data.get('Createdby', '')
            Type = data.get('Type', '')
            registration_id = data.get('RegistrationId', '')

            processedChooseDocument = validate_and_process_file(ChooseDocument) if ChooseDocument  else None

            processedcurrentAnnotation = validate_and_process_file(currentAnnotation) if currentAnnotation  else None

            if not registration_id:
                return JsonResponse({'error': 'RegistrationId is required'}, status=400)

            try:
                registration_ins = Patient_Appointment_Registration_Detials.objects.get(pk=registration_id)
            except Patient_Appointment_Registration_Detials.DoesNotExist:
                return JsonResponse({'error': 'Patient not found'}, status=404)

            GeneralEvaluation_instance = Workbench_GeneralEvaluation(
                Registration_Id=registration_ins,
                CheifComplaint=cheifComplaint,
                KeyComplaint=KeyComplaint,
                History=History,
                Examine=Examine,
                Diagnosis=Diagnosis,
                ICDCode=SearchICDCode,
                ICDCode_Description=SearchDescription,
                ICDCode_Diagnosis=SearchDiagnosis,
                DiseaseDetails = diseasedata,
                ChooseDocument=processedChooseDocument,
                AnnotationDocument=processedcurrentAnnotation,
                created_by=created_by,
                Type=Type,
            )
            GeneralEvaluation_instance.save()
            return JsonResponse({'success': 'GeneralEvaluation Details added successfully'})
       
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
            
   
    elif request.method == 'GET':
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
            
            registration_id = request.GET.get('RegistrationId')
            if not registration_id:
                return JsonResponse({'warn': 'RegistrationId is required'}, status=400)
            
            try:
                registration_ins = Patient_Appointment_Registration_Detials.objects.get(pk=registration_id)
            except Patient_Appointment_Registration_Detials.DoesNotExist:
                return JsonResponse({'error': 'Patient not found'}, status=404)

            # Fetch all records from the Location_Detials model
            GeneralEvaluation = Workbench_GeneralEvaluation.objects.filter(Registration_Id=registration_ins)
            
            # Construct a list of dictionaries containing location data
            GeneralEvaluation_data = [
                {
                    'id': GeneralEvaluation.Id,
                    'RegistrationId': GeneralEvaluation.Registration_Id.pk,
                    'VisitId': GeneralEvaluation.Registration_Id.VisitId,
                    'PrimaryDoctorId': GeneralEvaluation.Registration_Id.PrimaryDoctor.Doctor_ID,
                    'PrimaryDoctorName': GeneralEvaluation.Registration_Id.PrimaryDoctor.ShortName,
                    'KeyComplaint': GeneralEvaluation.KeyComplaint,
                    'cheifComplaint': GeneralEvaluation.CheifComplaint,
                    'History': GeneralEvaluation.History,
                    'Examine': GeneralEvaluation.Examine,
                    'Diagnosis': GeneralEvaluation.Diagnosis,
                    'SearchICDCode':GeneralEvaluation.ICDCode,
                    'SearchDescription':GeneralEvaluation.ICDCode_Description,
                    'SearchDiagnosis':GeneralEvaluation.ICDCode_Diagnosis,
                    'ChooseDocument': get_file_image(GeneralEvaluation.ChooseDocument) if GeneralEvaluation.ChooseDocument else None,
                    'currentAnnotation': get_file_image(GeneralEvaluation.AnnotationDocument) if GeneralEvaluation.AnnotationDocument else None,
                    'DiseaseDetails': GeneralEvaluation.DiseaseDetails,
                    'created_by': GeneralEvaluation.created_by,
                    'Type': GeneralEvaluation.Type,
                    'Date' : GeneralEvaluation.created_at.strftime('%Y-%m-%d'),  # Format date
                    'Time' : GeneralEvaluation.created_at.strftime('%H:%M:%S') , # Format time
                } for GeneralEvaluation in GeneralEvaluation
            ] 
            # print(GeneralEvaluation_data,'GeneralEvaluation_data')
            for idx, GeneralEva in enumerate(GeneralEvaluation_data, start=1):
                      GeneralEva["sno"] = idx
            return JsonResponse(GeneralEvaluation_data, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def Get_Keycomplaint(request):
    try:
        data = request.GET.get('KeyComplaint')
        querys =Q()
        if data:
            querys &= Q(KeyComplaint__icontains = data)
        responsedata =[]
        keycomplaints = Workbench_GeneralEvaluation.objects.filter(querys).values('KeyComplaint').distinct()[:10]
        print(keycomplaints,'keycomplaints')
        for key in keycomplaints:

            keval= key.get('KeyComplaint')
            complaints = Workbench_GeneralEvaluation.objects.filter(KeyComplaint = keval).order_by('-created_at').first()
            print(complaints,'complaints')
            data={
                    'id': len(responsedata) +1,
                    'PrimaryDoctorId': complaints.Registration_Id.PrimaryDoctor.Doctor_ID,
                    'PrimaryDoctorName': complaints.Registration_Id.PrimaryDoctor.ShortName,
                    'KeyComplaint': complaints.KeyComplaint,
                    'cheifComplaint': complaints.CheifComplaint,
                    'History': complaints.History,
                    'Examine': complaints.Examine,
                    'Diagnosis': complaints.Diagnosis,
                    'SearchICDCode':complaints.ICDCode,
                    'SearchDescription':complaints.ICDCode_Description,
                    'SearchDiagnosis':complaints.ICDCode_Diagnosis,

                }
            responsedata.append(data)
        return JsonResponse(responsedata, safe=False)
    except Exception as e:
        # Log the error and return a 500 Internal Server Error
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'An internal server error occurred'}, status=500)

def Get_DiseaseName(request):
    try:
        diseasename = request.GET.get('Diseasename','')
        print(diseasename)
        diseasedata = Disease_Master.objects.all()
        disease_list = []

        if diseasename:

            disease_ins = Disease_Master.objects.filter(DiseaseName=diseasename)
            print(disease_ins)
            for datas in disease_ins:
                disease_dict = {
                    'DiseaseCode': datas.DiseaseCode,
                    'DiseaseName': datas.DiseaseName,
                    'IsChronicle': datas.IsChronicle,
                    'IsCommunicable' : datas.IsCommunicable

                }
                disease_list.append(disease_dict)
            return JsonResponse(disease_list, safe=False)

        for datas in diseasedata:

            disease_dict = {
                   'DiseaseCode': datas.DiseaseCode,
                   'DiseaseName': datas.DiseaseName,
                   'IsChronicle': datas.IsChronicle,
                   'IsCommunicable' : datas.IsCommunicable

            }
            disease_list.append(disease_dict)
   
        return JsonResponse(disease_list, safe=False)
    except Exception as e:
        # Log the error and return a 500 Internal Server Error
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'An internal server error occurred'}, status=500)   

def Get_PrimaryCodes():

        try:
            max_code = Disease_Master.objects.all().aggregate(
                    Max("DiseaseCode")
                )["DiseaseCode__max"]

            if max_code:
                new_department_code = (
                    Generate_Next_Code_3digit(max_code)
                )
            else:
                new_department_code = "DMC001"
        
            return new_department_code 
      
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return JsonResponse(
                {"success": False, "message": "An internal error occurred."}, status=500
            )

@csrf_exempt
@require_http_methods(["POST", "OPTIONS", "GET"])
def Disease_master_details(request):

    if request.method == 'POST':

        data = json.loads(request.body)
        DiseaseCode = Get_PrimaryCodes()
        disease =  data.get('DiseaseName','')
        Ischronicle = data.get('IsChronicle','')
        IsCommunicable = data.get('IsCommunicable','')
        CreatedBy = data.get('CreatedBy','host')

        existing_name = Disease_Master.objects.filter(DiseaseName=disease).first()

        if existing_name:
            return JsonResponse('The name already present',safe=False)
        
        Disease_ins = Disease_Master(
            DiseaseCode = DiseaseCode,
            DiseaseName = disease,
            IsCommunicable = IsCommunicable,
            IsChronicle = Ischronicle,
            CreatedBy = CreatedBy
        )

        Disease_ins.save()

        return JsonResponse('success',safe=False)

    
# @csrf_exempt
# def G