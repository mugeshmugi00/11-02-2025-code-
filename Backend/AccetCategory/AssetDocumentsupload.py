from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse

from django.views.decorators.csrf import csrf_exempt
from .models import *
import json
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
from django.db import transaction
import filetype
import base64
import traceback

import base64
from django.core.files.uploadedfile import InMemoryUploadedFile


@transaction.atomic
def validate_and_process_file(file):
    if isinstance(file, InMemoryUploadedFile):
        file_content = file.read()  
        return file_content  

    if isinstance(file, str):
        try:
            file_data = file.split(',')[1] if ',' in file else file
            return base64.b64decode(file_data)
        except Exception as e:
            return JsonResponse({'error': f'Invalid base64 data: {str(e)}'})

    return None


@csrf_exempt
@require_http_methods(['POST'])
def assetdocumentsuploadpost(request):
    try:
        asset_id = request.POST.get('asset')  
        document_type = request.POST.get('document_type')
        description = request.POST.get('description', '')
        category = request.POST.get('category')
        subcategory = request.POST.get('subcategory')
        file = request.FILES.get('file')

        print("Received asset_id:", asset_id)
        print("Received category:", category)
        print("Received subcategory:", subcategory)
        
        if not file:
            return JsonResponse({'error': 'No file provided'})

        file_content = file.read()

        asset = AssetReg_Data.objects.filter(id=asset_id).first()
        if not asset:
            asset = AssetReg_Data.objects.filter(asset_code=asset_id).first()
            
        if not asset:
            return JsonResponse({'error': f'Asset not found with ID/code: {asset_id}'})

        category_instance = AssetCategory.objects.get(id=category)
        subcategory_instance = AssetSubCategory.objects.get(id=subcategory)

        document = AssetDocuments_Uplode(
            asset_name=asset,
            document_type=document_type,
            file=file_content,  
            description=description,
            category=category_instance,
            asset_subcategory=subcategory_instance
        )
        document.save()

        return JsonResponse({
            'message': 'Document uploaded successfully',
            'document_id': document.id
        })

    except AssetCategory.DoesNotExist:
        return JsonResponse({'error': f'Category not found with ID: {category}'})
    except AssetSubCategory.DoesNotExist:
        return JsonResponse({'error': f'Subcategory not found with ID: {subcategory}'})
    except Exception as e:
        error_message = f"Error: {str(e)}\nTraceback: {traceback.format_exc()}"
        print(error_message)
        return JsonResponse({'error': str(e)})

@csrf_exempt
@require_http_methods(['GET'])
def assetdocumentsuploadget(request):
    
    try:
        asset_code = request.GET.get('asset_code')
        print(f"Received request for asset_code: {asset_code}")
        
        asset = AssetReg_Data.objects.filter(id=asset_code).first()
        print(f"Found asset: {asset}")
        
        if not asset_code:
            return JsonResponse({'error': 'Asset code is required'})

       
        
        if not asset:
            return JsonResponse({'error': f'Asset not found with code: {asset_code}'})
        
        documents = AssetDocuments_Uplode.objects.filter(asset_name=asset)
        print(f"Found {documents.count()} documents")
        
        doc_list = []
        for doc in documents:
            try:
                doc_data = {
                    'id': doc.id,
                    'asset_name': doc.asset_name.name,
                    'asset_code': doc.asset_name.asset_code,
                    'document_type': doc.document_type,
                    'description': doc.description,
                    'file_url': f'/media/documents/{doc.id}' if doc.file else None
                }
                doc_list.append(doc_data)
            except Exception as e:
                print(f"Error processing document {doc.id}: {str(e)}")
                continue
        
        print(f"Returning {len(doc_list)} documents")
        return JsonResponse(doc_list, safe=False)
    
    except AssetReg_Data.DoesNotExist:
        error_msg = f"Asset not found with code: {asset_code}"
        print(error_msg)
        return JsonResponse({'error': error_msg})
    except Exception as e:
        error_msg = f"Error in assetdocumentsuploadget: {str(e)}"
        print(error_msg)
        import traceback
        print(traceback.format_exc())
        return JsonResponse({'error': error_msg})
    
# -----------------------------------------------------------------------------------
@csrf_exempt
@require_http_methods(['GET'])
def get_asset_sub(request):
    try:
        category_id = request.GET.get('category_id')
        if not category_id:
            return JsonResponse({'error': 'category_id parameter is required'})
        
        subcategories = AssetSubCategory.objects.filter(category_id=category_id).values('id', 'name', 'category_id')
        return JsonResponse(list(subcategories), safe=False)
    
    except Exception as e:
        return JsonResponse({'error': str(e)})
    
@csrf_exempt
@require_http_methods(['GET'])
def get_assets(request):
    try:
        subcategory_id = request.GET.get('subcategory_id')
        if not subcategory_id:
            return JsonResponse({'error': 'subcategory_id parameter is required'})
        
        assets = AssetReg_Data.objects.filter(subcategory_id=subcategory_id).values('id', 'name', 'subcategory_id')
        return JsonResponse(list(assets), safe=False)
    
    except Exception as e:
        return JsonResponse({'error': str(e)})