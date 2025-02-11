import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import *
from django.db.models import Sum, Max, Q

import random
import string
from django.db import transaction
from decimal import Decimal
from .Login import authenticate_request

from docx import Document
import base64
# import magic  # Make sure you have the pyathon-magic library installed
import filetype
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter
#--------------------------------------------Radiology insert,get,update----------------------------------------







@csrf_exempt
@require_http_methods(["POST", "GET", "OPTIONS"])
def Radiology_Names_link(request):
    api_key = request.headers.get('Apikey')
    api_password = request.headers.get('Apipassword')
    sessionid = request.headers.get('Sessionid')
    if authenticate_request(sessionid, api_key, api_password):
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                print("Received data:", data)

                RadiologyId = data.get('RadiologyId', '')
                RadiologyName = data.get('RadiologyName', '').strip().upper()
                created_by = data.get('created_by', '')
                Location = data.get('Location', '')
                Statusedit = data.get('Statusedit', False)

                if RadiologyId:
                    try:
                        Radiology_instance = RadiologyNames_Details.objects.get(pk=RadiologyId)
                    except RadiologyNames_Details.DoesNotExist:
                        return JsonResponse({'warn': 'Radiology ID not found'})
                    if RadiologyNames_Details.objects.filter(Radiology_Name=RadiologyName).exists():
                        return JsonResponse({'warn': f"The RadiologyName '{RadiologyName}' is already present "})

                    if Statusedit:
                        Radiology_instance.Status = not Radiology_instance.Status
                    else:
                        Radiology_instance.Radiology_Name = RadiologyName
                    Radiology_instance.save()

                    # Clear existing BookingFees_Details for this Radiology instance
                  
                    return JsonResponse({'success': 'RadiologyName updated successfully'})
                else:
                    if not Location:
                        return JsonResponse({'warn': 'Location is required'})

                    try:
                        Location_instance = Location_Detials.objects.get(Location_Id=Location)
                    except Location_Detials.DoesNotExist:
                        return JsonResponse({'warn': 'Invalid location'})

                    if RadiologyNames_Details.objects.filter(Radiology_Name=RadiologyName, Location_Name=Location_instance).exists():
                        return JsonResponse({'warn': f"The RadiologyName '{RadiologyName}' is already present "})

                    Radiology_instance = RadiologyNames_Details(
                        Radiology_Name=RadiologyName,
                        Location_Name=Location_instance,
                        created_by=created_by,
                    )
                    Radiology_instance.save()

                    return JsonResponse({'success': 'RadiologyName added successfully'})

            except Exception as e:
                print(f"An error occurred: {str(e)}")
                return JsonResponse({'error': 'An internal server error occurred'}, status=500)

        elif request.method == 'GET':
            try:
                Radiology_Master = RadiologyNames_Details.objects.all()
                Radiology_Master_data = []
                for Radiology in Radiology_Master:


                    Radiology_Master_data.append({
                        'id': Radiology.Radiology_Id,
                        'RadiologyName': Radiology.Radiology_Name,
                        'created_by': Radiology.created_by,
                        'Location_Name': Radiology.Location_Name.Location_Name if Radiology.Location_Name else 'Unknown',
                        'Location_Id': Radiology.Location_Name.pk if Radiology.Location_Name else 'Unknown',
                        'Status': 'Active' if Radiology.Status else 'Inactive',
                    })

                return JsonResponse(Radiology_Master_data, safe=False)
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                return JsonResponse({'error': 'An internal server error occurred'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=200)
        

   
#------------------Sub_TestName------------------------
  
@csrf_exempt
@require_http_methods(["POST", "OPTIONS", "GET"])
def Radiology_details_link(request):
    api_key = request.headers.get('Apikey')
    api_password = request.headers.get('Apipassword')
    sessionid = request.headers.get('Sessionid')
    if authenticate_request(sessionid, api_key, api_password):
        def validate_and_process_file(file):
          
            def get_file_type(file):
                if file.startswith('data:application/pdf;base64'):
                    return 'application/pdf'
                elif file.startswith('data:image/jpeg;base64') or file.startswith('data:image/jpg;base64'):
                    return 'image/jpeg'
                elif file.startswith('data:image/png;base64'):
                    return 'image/png'
                elif file.startswith('data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64'):
                    return 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'  # .docx
                elif file.startswith('data:application/msword;base64'):
                    return 'application/msword'  # .doc
                else:
                    return 'unknown'

            def compress_image(image, min_quality=10, step=5):
                output = BytesIO()
                quality = 95
                while quality >= min_quality:
                    output.seek(0)
                    image.save(output, format='JPEG', quality=quality)
                    compressed_data = output.getvalue()
                    quality -= step
                return compressed_data, len(compressed_data)

            def compress_pdf(file):
                output = BytesIO()
                reader = PdfReader(file)
                writer = PdfWriter()
                for page_num in range(len(reader.pages)):
                    writer.add_page(reader.pages[page_num])
                writer.write(output)
                return output.getvalue(), len(output.getvalue())

            def process_word_file(file):
                # Open the Word file and return some information (or process it as needed)
                document = Document(file)
                # For demonstration, we return the number of paragraphs as an example of processing
                num_paragraphs = len(document.paragraphs)
                return num_paragraphs

            if file:
                try:
                    file_data = file.split(',')[1]
                    file_content = base64.b64decode(file_data)
                    file_size = len(file_content)

                    max_size_mb = 5
                    if file_size > max_size_mb * 1024 * 1024:
                        return JsonResponse({'warn': f'File size exceeds the maximum allowed size ({max_size_mb}MB)'}, status=400)

                    file_type = get_file_type(file)

                    if file_type in ['image/jpeg', 'image/png']:
                        image = image.open(BytesIO(file_content))
                        if image.mode in ('RGBA', 'P'):
                            image = image.convert('RGB')
                        compressed_image_data, _ = compress_image(image)
                        return compressed_image_data

                    elif file_type == 'application/pdf':
                        compressed_pdf_data, _ = compress_pdf(BytesIO(file_content))
                        return compressed_pdf_data

                    elif file_type in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword']:
                        # Process Word files
                        word_content = process_word_file(BytesIO(file_content))
                        return JsonResponse({'word_content': word_content}, status=200)

                    else:
                        return JsonResponse({'warn': 'Unsupported file format'}, status=400)

                except Exception as e:
                    return JsonResponse({'error': f'Error processing file: {str(e)}'}, status=500)

            return None

  
        if request.method == 'POST':
            try:
                data = request.POST
                print("TestName ersdsPOST data123:", data)

                # Extract data from POST request
                TestNameId = data.get('TestNameId', '')
                TestCode = data.get('TestCode', '')
                RadiologyName = data.get('RadiologyName', '')
                TestName = data.get('TestName', '')
                Amount = data.get('Amount', '')
                Amount = float(Amount) if Amount else 0.0
                BookingFees = data.get('BookingFees', '')
                BookingFees = float(BookingFees) if BookingFees else 0.0
                Prev_Amount = data.get('Prev_Amount', '')
                Prev_Amount = float(Prev_Amount) if Prev_Amount else 0.0
                Prev_BookingFees = data.get('Prev_BookingFees', '')
                Prev_BookingFees = float(Prev_BookingFees) if Prev_BookingFees else 0.0
                created_by = data.get('created_by', '')
                Status = data.get('Status', '')


                # Ensure RadiologyName is provided and is valid
                if not RadiologyName:
                    return JsonResponse({'error': 'RadiologyName is missing'}, status=400)

                try:
                    RadiologyName = int(RadiologyName)
                    rad_instance = RadiologyNames_Details.objects.get(Radiology_Id=RadiologyName)
                    radiology_name = rad_instance.Radiology_Name
                except RadiologyNames_Details.DoesNotExist:
                    return JsonResponse({'warn': 'Radiology name does not exist'})
                except ValueError:
                    return JsonResponse({'warn': 'Invalid RadiologyName provided'})

                print("Radiology instance:", rad_instance)

                # Process file if available
                processed_files = {
                    'ChooseFile': validate_and_process_file(data.get('ChooseFile')) if data.get('ChooseFile') else None,
                }

                if TestCode:
                    # Update existing TestName_Details instance
                    with transaction.atomic():
                        try:
                            test_instance = TestName_Details.objects.get(Test_Code=TestCode)
                        except TestName_Details.DoesNotExist:
                            return JsonResponse({'warn': 'TestName not found'})

                    
                        test_instance.Radiology_Id = rad_instance
                        test_instance.Test_Name = TestName
                        test_instance.Prev_Amount = test_instance.Amount
                        test_instance.Amount = Amount
                        test_instance.Prev_BookingFees = test_instance.BookingFees
                        test_instance.BookingFees = BookingFees
                        test_instance.Report_file = processed_files['ChooseFile']
                        test_instance.Status = Status
                        test_instance.save()
                         
                        # Handle SubTestName if Types is 'Yes'
                    return JsonResponse({'success': 'TestName Updated successfully'})   
                else:
                    # Create new TestName_Details instance
                    with transaction.atomic():
                        duplicate_test = TestName_Details.objects.filter(
                            Radiology_Id=rad_instance,
                            Test_Name=TestName
                        ).exists()

                        if duplicate_test:
                            return JsonResponse({'warn': 'Test name already exists for this radiology department'})
                        inst_test_name_instance = TestName_Details.objects.create(
                            Radiology_Id=rad_instance,
                            Test_Name=TestName,
                            Prev_Amount=Prev_Amount,
                            Amount=Amount,
                            Prev_BookingFees=Prev_BookingFees,
                            BookingFees=BookingFees,
                            Report_file=processed_files['ChooseFile'],
                            Status=Status,
                            created_by=created_by,
                        )

                        
                return JsonResponse({'success': 'TestName added successfully'})

            except Exception as e:
                print(f"An error occurred: {str(e)}")
                return JsonResponse({'error': 'An internal server error occurred'}, status=500)

                                
                        
                    
        elif request.method == 'GET':
            try:

                def get_file_image(filedata):
                    try:
                        kind = filetype.guess(filedata)

                        # List of supported MIME types
                        supported_mime_types = [
                            'application/pdf',
                            'image/jpeg',
                            'image/png',
                            'application/msword',  # For .doc files
                            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'  # For .docx files
                        ]

                        contenttype1 = 'application/pdf'
                        if kind:
                            if kind.mime in supported_mime_types:
                                contenttype1 = kind.mime
                        
                        # Return base64 encoded data with MIME type
                        return f'data:{contenttype1};base64,{base64.b64encode(filedata).decode("utf-8")}'
                    
                    except Exception as e:
                        print(f"Error processing file: {e}")
                        return None

                TestNames = TestName_Details.objects.all()
                TestName_data = []
                
                
                for idss, TestName in enumerate(TestNames, start=1):
                    TestName_dict = {
                        'id': idss,
                        'RadiologyId': TestName.Radiology_Id.pk,
                        'RadiologyName': TestName.Radiology_Id.Radiology_Name,
                        'locationid': TestName.Radiology_Id.Location_Name.pk,
                        'TestName': TestName.Test_Name,
                        'TestCode': TestName.Test_Code,
                        'Prev_Amount': TestName.Prev_Amount,
                        'Curr_Amount': TestName.Amount,
                        'Prev_BookingFees':TestName.Prev_BookingFees,
                        'Curr_BookingFees':TestName.BookingFees,
                        'ChooseFile': get_file_image(TestName.Report_file) if TestName.Report_file else None,
                        'Status': TestName.Status,
                        'created_by': TestName.created_by,
                        
                    }
                    
                     
                    TestName_data.append(TestName_dict)
                
                return JsonResponse(TestName_data, safe=False)
            
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                return JsonResponse({'error': 'An internal server error occurred'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=200)
        

















@csrf_exempt
@require_http_methods(["GET", "OPTIONS"])
def Radiology_Department_TestNames(request):
    try:

        Radiologyid = request.GET.get('id', '')
        print("Radiologyid",Radiologyid)

        # Check if Radiology ID is provided
        if not Radiologyid:
            return JsonResponse({'warn': 'Radiology department ID is required'})

        # Fetch the test names related to the selected radiology department
        test_names = TestName_Details.objects.filter(Radiology_Id_id=Radiologyid, Status="Active")

        # Prepare the response data
        testname_data = []
        for test in test_names:
            testname_data.append({
                'id': test.Test_Code,  # Test_Code as ID
                'TestName': test.Test_Name,  # Test_Name
                'Amount': test.Amount,
            })
            

        # Return the data in JSON format
        return JsonResponse(testname_data, safe=False)
      
    except Exception as e:
        # Handle any exception and return an error response
        print("Exception:", e)
        return JsonResponse({'error': 'An internal server error occurred'}, status=500)



@csrf_exempt
@require_http_methods(["OPTIONS", "GET"])        
def Radiology_details_link_view(request):
    api_key = request.headers.get('Apikey')
    api_password = request.headers.get('Apipassword')
    sessionid = request.headers.get('Sessionid')
    if authenticate_request(sessionid, api_key, api_password):
        try:
            Radiology_Master = RadiologyNames_Details.objects.all()
            
            
            Test_data = []
            index=0
            for rad in Radiology_Master:
                    
                rad_dic={
                    'id':index+1,
                    'RadiologyId':rad.Radiology_Id,
                    'RadiologyName': rad.Radiology_Name,
                    'LocationId': rad.Location_Name.pk,
                    'TestNames':[]
                }
                TestNames = TestName_Details.objects.filter(Radiology_Id=rad,Status='Active')
                testindx=0
                
                for test in TestNames:
                    test_dict={
                        'id':testindx+1,
                        'TestName': test.Test_Name,
                        'TestCode': test.Test_Code,
                        'Prev_Amount': test.Prev_Amount,
                        'Curr_Amount': test.Amount,
                    }
                           
                    rad_dic['TestNames'].append(test_dict)
                    testindx = testindx + 1
                    
                    
                    
                Test_data.append(rad_dic)
                index = index+ 1
            return JsonResponse(Test_data, safe=False)
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=200)

