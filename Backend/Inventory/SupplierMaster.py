# import json
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_http_methods
# from django.db.models import  Q
# from django.db import transaction
# from .models import *
# from io import BytesIO
# from PIL import Image
# import base64
# from PyPDF2 import PdfReader, PdfWriter
# import magic




# def validate_and_process_file(file):    
        
#         def get_file_type(file):
#             if file.startswith('data:application/pdf;base64'):
#                 return 'application/pdf'
#             elif file.startswith('data:image/jpeg;base64') or file.startswith('data:image/jpg;base64'):
#                 return 'image/jpeg'
#             elif file.startswith('data:image/png;base64'):
#                 return 'image/png'
#             else:
#                 return 'unknown'

#         def compress_image(image, min_quality=10, step=5):
#             output = BytesIO()
#             quality = 95
#             compressed_data = None
#             while quality >= min_quality:
#                 output.seek(0)
#                 image.save(output, format='JPEG', quality=quality)
#                 compressed_data = output.getvalue()
#                 quality -= step
#             output.seek(0)
#             compressed_size = len(compressed_data)
#             return compressed_data, compressed_size

#         def compress_pdf(file):
#             output = BytesIO()
#             reader = PdfReader(file)
#             writer = PdfWriter()
#             for page_num in range(len(reader.pages)):
#                 writer.add_page(reader.pages[page_num])
#             writer.write(output)
#             compressed_data = output.getvalue()
#             compressed_size = len(compressed_data)
#             return compressed_data, compressed_size

#         if file:
#             file_data = file.split(',')[1]
#             file_content = base64.b64decode(file_data)
#             file_size = len(file_content)
            
#             max_size_mb = 5

#             if file_size > max_size_mb * 1024 * 1024:
#                 print('maximum mb')
#                 return JsonResponse({'warn': f'File size exceeds the maximum allowed size ({max_size_mb}MB)'})

#             file_type = get_file_type(file)
            
#             if file_type == 'image/jpeg' or file_type == 'image/png':
#                 try:
#                     image = Image.open(BytesIO(file_content))
#                     if image.mode in ('RGBA', 'P'):
#                         image = image.convert('RGB')
#                     compressed_image_data, compressed_size = compress_image(image)
#                     return compressed_image_data
#                 except Exception as e:
#                     return JsonResponse({'error': f'Error processing image: {str(e)}'})

#             elif file_type == 'application/pdf':
#                 try:
#                     compressed_pdf_data, compressed_size = compress_pdf(BytesIO(file_content))

#                     return compressed_pdf_data
#                 except Exception as e:
#                     return JsonResponse({'error': f'Error processing PDF: {str(e)}'})

#             else:
#                 return JsonResponse({'warn': 'Unsupported file format'})

#         return None


# @csrf_exempt
# @require_http_methods(["POST", "OPTIONS", "GET"])
# def Supplier_Master_Link(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             FileAttachment = data.get('FileAttachment', None)
#             FileAttachment_prossed = validate_and_process_file(FileAttachment) if FileAttachment else None
#             SupplierId = data.get('SupplierId', None)
#             StatusEdit = data.get('StatusEdit',False)
#             SupplierName = data.get('SupplierName', '')
#             SupplierType = data.get('SupplierType', '')
#             ContactPerson = data.get('ContactPerson', '')
#             ContactNumber = data.get('ContactNumber', '')
#             EmailAddress = data.get('EmailAddress', '')
#             Address = data.get('Address', '')
#             RegistrationNumber = data.get('RegistrationNumber', '')
#             GSTNumber = data.get('GSTNumber', '')
#             PANNumber = data.get('PANNumber', '')
#             PaymentTerms = data.get('PaymentTerms', '')
#             CreditLimit = data.get('CreditLimit', '')
#             LeadTime = data.get('LeadTime', '')
#             Notes = data.get('Notes', '')
#             PaymentMode = data.get('PaymentMode', '')
#             BankName = data.get('BankName', '')
#             AccountNumber = data.get('AccountNumber', '')
#             IFSCCode = data.get('IFSCCode', '')
#             BankBranch = data.get('BankBranch', '')
#             created_by = data.get('created_by', '')
            
#             with transaction.atomic():
#                 if SupplierId :
#                     print('--',SupplierId)
                    
#                     supplier_ins =Supplier_Master_Details.objects.get(pk = SupplierId)
#                     print('--')
#                     if StatusEdit:
#                         supplier_ins.Status = not supplier_ins.Status
#                         supplier_ins.save()
#                         return JsonResponse ({'success': 'Supplier Master Updated successfully'})
                        
#                     else:
#                         if Supplier_Master_Details.objects.filter(Supplier_Name = SupplierName).exclude(pk = SupplierId).exists():
#                             return JsonResponse({'warn': f"The Supplier Name are already present in the name of {SupplierName}. "})
#                         else:
#                             supplier_ins.Supplier_Name = SupplierName
#                             supplier_ins.Supplier_Type = SupplierType
#                             supplier_ins.Contact_Person = ContactPerson
#                             supplier_ins.Contact_Number = ContactNumber
#                             supplier_ins.Email_Address = EmailAddress
#                             supplier_ins.Address = Address
#                             supplier_ins.Registration_Number = RegistrationNumber
#                             supplier_ins.GST_Number = GSTNumber
#                             supplier_ins.PAN_Number = PANNumber
#                             supplier_ins.Payment_Terms = PaymentTerms
#                             supplier_ins.Credit_Limit = CreditLimit
#                             supplier_ins.DeliveryDuration = LeadTime
#                             supplier_ins.Notes = Notes
#                             supplier_ins.Payment_Mode = PaymentMode
#                             supplier_ins.File_Attachment = FileAttachment_prossed
#                             supplier_ins.save()
                        
                        
#                             if PaymentMode == 'Online':
#                                 if Supplier_Bank_Details.objects.filter(Supplier_Detials__pk = SupplierId).exists():
#                                     supplier_bank_ins = Supplier_Bank_Details.objects.get(Supplier_Detials__pk =SupplierId)
#                                     supplier_bank_ins.Bank_Name = BankName
#                                     supplier_bank_ins.Account_Number= AccountNumber
#                                     supplier_bank_ins.IFSCCode= IFSCCode
#                                     supplier_bank_ins.BankBranch=BankBranch
#                                     supplier_bank_ins.save()
                                    
#                                 else:
#                                     Supplier_Bank_Details.objects.create(
#                                     Supplier_Detials= supplier_ins,
#                                     Bank_Name= BankName,
#                                     Account_Number= AccountNumber,
#                                     IFSCCode= IFSCCode,
#                                     BankBranch=BankBranch,
#                                     )
#                             return JsonResponse ({'success': 'Supplier Master Updated successfully'})
                            
#                 else:
#                     if Supplier_Master_Details.objects.filter(Supplier_Name = SupplierName).exists():
#                             return JsonResponse({'warn': f"The Supplier Name are already present in the name of {SupplierName}. "})
#                     else:
#                         supplier_ins = Supplier_Master_Details.objects.create(
#                             Supplier_Name = SupplierName,
#                             Supplier_Type = SupplierType,
#                             Contact_Person = ContactPerson,
#                             Contact_Number = ContactNumber,
#                             Email_Address = EmailAddress,
#                             Address = Address,
#                             Registration_Number = RegistrationNumber,
#                             GST_Number = GSTNumber,
#                             PAN_Number = PANNumber,
#                             Payment_Terms = PaymentTerms,
#                             Credit_Limit = CreditLimit,
#                             DeliveryDuration = LeadTime,
#                             Notes = Notes,
#                             Payment_Mode = PaymentMode,
#                             File_Attachment = FileAttachment_prossed,
#                             created_by = created_by
#                             )
#                         if PaymentMode == 'Online':

#                             Supplier_Bank_Details.objects.create(
#                             Supplier_Detials= supplier_ins,
#                             Bank_Name= BankName,
#                             Account_Number= AccountNumber,
#                             IFSCCode= IFSCCode,
#                             BankBranch=BankBranch
#                             )
#                         return JsonResponse ({'success': 'Supplier Master Created successfully'})
                        
                    
               
                        
                    
#         except Exception as e:
#             print(f'An error occurred: {str(e)}')
#             return JsonResponse ({'error':'An internal server error occurred'},status=500)
#     elif request.method == 'GET':
        
#         filters = {
#         1: Medical_Consumable_ProductMaster_Details,
#         2: Medical_Non_Consumable_ProductMaster_Details,
#         3: Non_Medical_Consumable_ProductMaster_Details,
#         4: Non_Medical_Non_Consumable_ProductMaster_Details,
#         5: Surgical_Consumable_ProductMaster_Details,
#         6: Surgical_Non_Consumable_ProductMaster_Details,
#         7: Stationery_ProductMaster_Details,
#         8: Assets_Movable_ProductMaster_Details,
#         9: Assets_Non_Movable_ProductMaster_Details,
#         10: Lenin_ProductMaster_Details,
#         11: Kitchen_ProductMaster_Details,
#         12: Miscellaneous_ProductMaster_Details,
#     }
#         try:
            
#             SupplierId = request.GET.get('SupplierId')
#             SupplierName = request.GET.get('SupplierName')
#             SupplierType = request.GET.get('SupplierType')
#             ContactNumber = request.GET.get('ContactNumber')
#             FilterBy = request.GET.get('FilterBy','Supplier')
#             forfilter =bool(request.GET.get('forfilter',False))
#             ProductCategory = request.GET.get('ProductCategory','')
#             SubCategory = request.GET.get('SubCategory','')
#             ItemId = request.GET.get('ItemId','')
#             ItemName = request.GET.get('ItemName','')
#             GenericName = request.GET.get('GenericName','')
#             CompanyName = request.GET.get('CompanyName','')
#             HSNCode = request.GET.get('HSNCode','')
            
#             def get_file_image(filedata):
#                         mime = magic.Magic()
#                         contenttype = mime.from_buffer(filedata).split(',')[0]
#                         # print('contenttype :',contenttype)
#                         contenttype1 = 'application/pdf'
#                         if contenttype == 'application/pdf':
#                             contenttype1 = 'application/pdf'
#                         elif contenttype == 'JPEG image data':
#                             contenttype1 = 'image/jpeg'
#                         elif contenttype == 'PNG image data':
#                             contenttype1 = 'image/png'
                    
                        
#                         return f"data:{contenttype1};base64,{base64.b64encode(filedata).decode('utf-8')}"
                    
#             if FilterBy == 'Supplier':      
#                 if not forfilter and SupplierId:
#                     Supplier_Master_instance=Supplier_Master_Details.objects.get(pk=SupplierId)
#                     dic={
#                             'id':Supplier_Master_instance.Supplier_Id,
#                             'SupplierName':Supplier_Master_instance.Supplier_Name,
#                             'SupplierType':Supplier_Master_instance.Supplier_Type,
#                             'ContactPerson':Supplier_Master_instance.Contact_Person,
#                             'ContactNumber':Supplier_Master_instance.Contact_Number,
#                             'EmailAddress':Supplier_Master_instance.Email_Address,
#                             'Address':Supplier_Master_instance.Address,
#                             'RegistrationNumber':Supplier_Master_instance.Registration_Number,
#                             'GSTNumber':Supplier_Master_instance.GST_Number,
#                             'PANNumber':Supplier_Master_instance.PAN_Number,
#                             'PaymentTerms':Supplier_Master_instance.Payment_Terms,
#                             'CreditLimit':Supplier_Master_instance.Credit_Limit,
#                             'LeadTime':Supplier_Master_instance.DeliveryDuration,
#                             'Status':'Active'if  Supplier_Master_instance.Status else 'Inactive',
#                             'Notes':Supplier_Master_instance.Notes,
#                             'PaymentMode':Supplier_Master_instance.Payment_Mode,
                            
#                         }

#                     return JsonResponse(dic,safe=False)
#                 else:
#                     filter_conditions = Q()
#                     if SupplierId:
#                         filter_conditions &= Q(pk__icontains = SupplierId)
#                     if SupplierName:
#                         filter_conditions &= Q(Supplier_Name__icontains =SupplierName)
#                     if SupplierType:
#                         filter_conditions &= Q(Supplier_Type__icontains =SupplierType)
#                     if ContactNumber:
#                         filter_conditions &= Q(Contact_Number__icontains =ContactNumber)
                    
#                     Supplier_Master_instance=Supplier_Master_Details.objects.filter(filter_conditions)

#                     Supplier_Array=[]

                    
#                     index = 1
#                     for row in Supplier_Master_instance:
#                         dic={
#                             'id':index,
#                             'SupplierId':row.pk,
#                             'SupplierName':row.Supplier_Name,
#                             'SupplierType':row.Supplier_Type,
#                             'ContactPerson':row.Contact_Person,
#                             'ContactNumber':row.Contact_Number,
#                             'EmailAddress':row.Email_Address,
#                             'Address':row.Address,
#                             'RegistrationNumber':row.Registration_Number,
#                             'GSTNumber':row.GST_Number,
#                             'PANNumber':row.PAN_Number,
#                             'PaymentTerms':row.Payment_Terms,
#                             'CreditLimit':row.Credit_Limit,
#                             'LeadTime':row.DeliveryDuration,
#                             'Status':'Active'if  row.Status else 'Inactive',
#                             'Notes':row.Notes,
#                             'PaymentMode':row.Payment_Mode,
#                             'FileAttachment':get_file_image(row.File_Attachment) if row.File_Attachment else None,
#                         }
                        
                    

#                         if row.Payment_Mode =='Online':

#                             Supplier_Bank_instance=Supplier_Bank_Details.objects.filter(Supplier_Detials__pk=row.Supplier_Id)
#                             bank_Array=[]
#                             if Supplier_Bank_instance:
                                
#                                 for Bank in Supplier_Bank_instance:
#                                     bankdic={
#                                         'id':Bank.pk,
#                                         'BankName':Bank.Bank_Name,
#                                         'AccountNumber':Bank.Account_Number,
#                                         'IFSCCode':Bank.IFSCCode,
#                                         'BankBranch':Bank.BankBranch,
#                                     }
#                                     bank_Array.append(bankdic)
                                
#                                 dic['Bank_Details']=bank_Array
#                             else:
#                                 dic['Bank_Details']=[]
#                         else:
#                             dic['Bank_Details']=[]


#                         Supplier_Array.append(dic)
#                         index += 1



#                     return JsonResponse (Supplier_Array,safe=False)
#             else:
#                 if not ProductCategory:
#                     return JsonResponse({'error': 'ProductCategory is required'}, status=400)
                
#                 selected_model = filters[int(ProductCategory)]
#                 model_fields = [field.name for field in selected_model._meta.get_fields()]
                
#                 filter_conditions = Q()
                
#                 if 'SubCategory' in model_fields and SubCategory:
#                     filter_conditions &= Q(SubCategory__pk =SubCategory)
#                 if 'ItemId' in model_fields and ItemId:
#                     filter_conditions &= Q(ItemId__icontains=ItemId)
#                 if 'ItemName' in model_fields and ItemName:
#                     filter_conditions &= Q(ItemName__icontains=ItemName)
#                 if 'GenericName' in model_fields and GenericName:
#                     filter_conditions &= Q(GenericName__icontains=GenericName)
#                 if 'CompanyName' in model_fields and CompanyName:
#                     filter_conditions &= Q(CompanyName__icontains=CompanyName)
#                 if 'HSNCode' in model_fields and HSNCode:
#                     filter_conditions &= Q(HSNCode__icontains=HSNCode)

#                 product_instance = selected_model.objects.filter(filter_conditions)
#                 content_type = ContentType.objects.get_for_model(selected_model)
#                 print('content_type',content_type)
#                 productlist=[]
#                 for ins in product_instance:
#                     print('Product_Item',ins.pk)
                    
#                     # Get the supplier product details where the product matches the content type and the item exists in Product_Item
#                     Supplier_Product_instance = Supplier_Product_Details.objects.filter(
#                         Product_Content_Type=content_type, Product_Object_Id=ins.pk
#                     )
#                     print('Supplier_Product_instance',Supplier_Product_instance)
#                     # If there is no supplier product for this item, skip to the next one
#                     if not Supplier_Product_instance.exists():
#                         continue
                    
#                     # Loop through the supplier products if they exist
#                     for sup_ins in Supplier_Product_instance:
#                         # Get the latest Supplier_Product_Amount_Details for this supplier product
#                         sup_pro_amount_ins = Supplier_Product_Amount_Details.objects.filter(
#                             Supplier_detials=sup_ins
#                         ).order_by('-Created_at').first()

#                         # Prepare the product data
#                         product_data = {
#                             'ItemId': ins.pk,
#                             'SubCategory': ins.SubCategory.pk if ins.SubCategory else None,
#                             'ItemName': ins.ItemName,
#                             'GenericName': ins.GenericName if 'GenericName' in model_fields else '',
#                             'CompanyName': ins.CompanyName if 'CompanyName' in model_fields else '',
#                             'HSNCode': ins.HSNCode if 'HSNCode' in model_fields else '',
#                             'DrugCharacter': ins.DrugCharacter if 'DrugCharacter' in model_fields and ins.DrugCharacter else '',
#                             'DrugType': ins.DrugType.pk if 'DrugType' in model_fields and ins.DrugType else None,
#                             'DrugGroup': ins.DrugGroup.pk if 'DrugGroup' in model_fields and ins.DrugGroup else None,
#                             'MeasurementType': ins.MeasurementType if 'MeasurementType' in model_fields else '',
#                             'Quantity': ins.Quantity if 'Quantity' in model_fields else '',
#                             'UOM': ins.UOM.pk if 'UOM' in model_fields else '',
#                             'Size': ins.Size if 'Size' in model_fields else '',
#                             'PackType': ins.PackType.pk if 'PackType' in model_fields and ins.PackType else None,
#                             'PackQty': ins.PackQty if 'PackQty' in model_fields else '',
                            
#                         }

#                         # Filter the product data and enrich with supplier pricing
#                         datafiltered = {
#                             'id': len(productlist)+1,
#                             # 'Supplier_product_id':sup_ins.pk,
#                             'ProductCategory': ProductCategory,
#                             'MRP': sup_pro_amount_ins.MRP if sup_pro_amount_ins else "",
#                             'PurchaseRateBeforeGST': sup_pro_amount_ins.PurchaseRateBeforeGST if sup_pro_amount_ins else "",
#                             'GST': sup_pro_amount_ins.GST if sup_pro_amount_ins else "",
#                             'PurchaseRateAfterGST': sup_pro_amount_ins.PurchaseRateAfterGST if sup_pro_amount_ins else "",
#                             'ProductStatus': 'Active' if ins.Status else 'Inactive',
#                             'SupplierProductStatus': 'Active' if sup_ins.Status else 'Inactive',
#                         }

#                         # Add additional fields dynamically based on the model's fields
#                         for key, value in product_data.items():
#                             if key in model_fields:
#                                 datafiltered[key] = value

#                                 # Add extra display names where appropriate
#                                 if key == 'SubCategory':
#                                     datafiltered['SubCategoryName'] = ins.SubCategory.SubCategoryName if ins.SubCategory else None
#                                 if key == 'DrugType':
#                                     datafiltered['DrugTypeName'] = ins.DrugType.DrugType_Name if ins.DrugType else None
#                                 if key == 'DrugGroup':
#                                     datafiltered['DrugGroupName'] = ins.DrugGroup.DrugGroup_Name if ins.DrugGroup else None
#                                 if key == 'PackType':
#                                     datafiltered['PackTypeName'] = ins.PackType.ProductType_Name if ins.PackType else None

#                         # Append the filtered data to the product list
#                         productlist.append(datafiltered)

#                 # Return the product list as a JSON response
#                 return JsonResponse(productlist, safe=False)

#         except Exception as e:
#             print(f'An error occurred: {str(e)}')
#             return JsonResponse ({'error':'An internal server error occurred'},status=500)
#     else:
#         return JsonResponse ({'error':'method not allowed'},status=400)




# @csrf_exempt
# @require_http_methods(["GET"])
# def Supplier_product_list_link(request):
#     try:
#         SupplierId = request.GET.get('SupplierId')
#         if not SupplierId:
#             return JsonResponse({'error': 'SupplierId is required'}, status=400)

#         # Define filters for product types
#         filters = {
#             Medical_Consumable_ProductMaster_Details: 'Medical Consumable',
#             Medical_Non_Consumable_ProductMaster_Details: 'Medical Non Consumable',
#             Non_Medical_Consumable_ProductMaster_Details: 'Non Medical Consumable',
#             Non_Medical_Non_Consumable_ProductMaster_Details: 'Non Medical Non Consumable',
#             Surgical_Consumable_ProductMaster_Details: 'Surgical Consumable',
#             Surgical_Non_Consumable_ProductMaster_Details: 'Surgical Non Consumable',
#             Stationery_ProductMaster_Details: 'Stationery',
#             Assets_Movable_ProductMaster_Details: 'Assets Movable',
#             Assets_Non_Movable_ProductMaster_Details: 'Assets Non Movable',
#             Lenin_ProductMaster_Details: 'Lenin',
#             Kitchen_ProductMaster_Details: 'Kitchen',
#             Miscellaneous_ProductMaster_Details: 'Miscellaneous',
#         }

#         item = {}
#         for key, pvalue in filters.items():
#             content_type = ContentType.objects.get_for_model(key)
            
#             # Filter Supplier_Product_Details based on supplier and product content type
#             Supplier_Product_instance = Supplier_Product_Details.objects.filter(
#                 Supplier_Name__pk=SupplierId, Product_Content_Type=content_type
#             )

#             model_fields = [field.name for field in key._meta.get_fields()]
#             productlist = []

#             for ins in Supplier_Product_instance:
#                 product_item = ins.Product_Item  # Access GenericForeignKey Product_Item
#                 sup_pro_amount_ins = Supplier_Product_Amount_Details.objects.filter(Supplier_detials= ins).order_by('-Created_at').first()
#                 data = {
#                     'id': len(productlist) + 1,
#                     'SupplierPoductId': ins.pk,
#                     'ProductCategory': product_item.SubCategory.ProductCategoryId.pk,
#                     'SubCategoryId': product_item.SubCategory.pk,
#                     'SubCategory': product_item.SubCategory.SubCategoryName,
#                     'ItemId': product_item.pk,
#                     'ItemName': product_item.ItemName,   
#                     'CompanyName': product_item.CompanyName if 'CompanyName' in model_fields and product_item.CompanyName   else '',
#                     'GenericName': product_item.GenericName if 'GenericName' in model_fields  and product_item.GenericName  else '',
#                     'HSNCode': product_item.HSNCode if 'HSNCode' in model_fields  and product_item.HSNCode else '',
#                     'Quantity': product_item.Quantity if 'Quantity' in model_fields  and product_item.Quantity else '',
#                     'UOM': product_item.UOM.Unit_Name if 'UOM' in model_fields  and product_item.UOM else '',
#                     'Size': product_item.Size if 'Size' in model_fields and product_item.Size  else '',
#                     'DrugCharacter': product_item.DrugCharacter if 'DrugCharacter' in model_fields and product_item.DrugCharacter else '',
#                     'DrugType': product_item.DrugType.DrugType_Name if 'DrugType' in model_fields and product_item.DrugType else '',
#                     'DrugGroup': product_item.DrugGroup.DrugGroup_Name if 'DrugGroup' in model_fields and product_item.DrugGroup else '',
#                     'PackType': product_item.PackType.ProductType_Name if 'PackType' in model_fields and product_item.PackType else '',
#                     'PackQty': product_item.PackQty if 'PackQty' in model_fields and product_item.PackQty else '',
#                     'MRP': sup_pro_amount_ins.MRP if sup_pro_amount_ins else "",
#                     'PurchaseRateBeforeGST': sup_pro_amount_ins.PurchaseRateBeforeGST if sup_pro_amount_ins else "",
#                     'GST': sup_pro_amount_ins.GST if sup_pro_amount_ins else "",
#                     'PurchaseRateAfterGST': sup_pro_amount_ins.PurchaseRateAfterGST if sup_pro_amount_ins else "",
#                     'Status': 'Active' if ins.Status else 'Inactive',
#                 }

#                 filtereddata = {}
#                 for key, value in data.items():
#                     if key in ['id', 'SupplierPoductId', 
#                                'PurchaseRateBeforeGST', 'GST', 
#                                'PurchaseRateAfterGST', 'MRP', 'Status',
#                                'ProductCategory','SubCategoryId']:
#                         filtereddata[key] = value
#                     elif key in model_fields:
#                         filtereddata[key] = value
                      

#                 productlist.append(filtereddata)

#             item[pvalue] = productlist

#         return JsonResponse(item, safe=False)

#     except Exception as e:
#         print(f'An error occurred: {str(e)}')
#         return JsonResponse({'error': 'An internal server error occurred'}, status=500)



# @csrf_exempt
# @require_http_methods(["POST", "OPTIONS"])
# def Supplier_product_Mapping_link(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)

#             # Extract required fields
#             ProductCategory = data.get('ProductCategory')
#             SupplierId = data.get('SupplierId')
#             ItemId = data.get('ItemId')
#             PurchaseRateBeforeGST = data.get('PurchaseRateBeforeGST')
#             product_GST = data.get('GST')
#             PurchaseRateAfterGST = data.get('PurchaseRateAfterGST')
#             product_MRP = data.get('MRP')
#             edit = data.get('edit', False)
#             pk = data.get('pk', None)
#             statusedit = data.get('statusedit', False)
#             created_by = data.get('created_by')

#             # Validation for required fields
#             if edit :
#                 if not pk:
#                     return JsonResponse({'warn': 'Product Category is a mandatory field'}, status=400)
#             else:
#                 if not ProductCategory:
#                     return JsonResponse({'warn': 'Product Category is a mandatory field'}, status=400)
#                 if not SupplierId:
#                     return JsonResponse({'warn': 'SupplierId is a mandatory field'}, status=400)
#                 if not ItemId:
#                     return JsonResponse({'warn': 'ItemId is a mandatory field'}, status=400)

           

#             # Define model filters
#             filters = {
#                 1: Medical_Consumable_ProductMaster_Details,
#                 2: Medical_Non_Consumable_ProductMaster_Details,
#                 3: Non_Medical_Consumable_ProductMaster_Details,
#                 4: Non_Medical_Non_Consumable_ProductMaster_Details,
#                 5: Surgical_Consumable_ProductMaster_Details,
#                 6: Surgical_Non_Consumable_ProductMaster_Details,
#                 7: Stationery_ProductMaster_Details,
#                 8: Assets_Movable_ProductMaster_Details,
#                 9: Assets_Non_Movable_ProductMaster_Details,
#                 10: Lenin_ProductMaster_Details,
#                 11: Kitchen_ProductMaster_Details,
#                 12: Miscellaneous_ProductMaster_Details,
#             }

            
#             if edit and pk:
#                 try:
#                     supplier_product_ins = Supplier_Product_Details.objects.get(pk=pk)
                    
#                     if statusedit:
#                         supplier_product_ins.Status = not supplier_product_ins.Status
#                         supplier_product_ins.save()
#                         return JsonResponse({'success': f'Product status updated for {supplier_product_ins.Supplier_Name.Supplier_Name}'}, status=200)
#                     # Fetch the latest record based on supplier details
#                     sup_pro_amount_ins = Supplier_Product_Amount_Details.objects.filter(
#                         Supplier_detials=supplier_product_ins
#                     ).order_by('-Created_at').first()

#                     # Flag to check if any field value has changed
#                     is_changed = False

#                     # Check if the values differ from the latest record
#                     if sup_pro_amount_ins:
#                         if (sup_pro_amount_ins.PurchaseRateBeforeGST != PurchaseRateBeforeGST or
#                             sup_pro_amount_ins.GST != product_GST or
#                             sup_pro_amount_ins.PurchaseRateAfterGST != PurchaseRateAfterGST or
#                             sup_pro_amount_ins.MRP != product_MRP):
#                             is_changed = True
#                     else:
#                         # If no previous record exists, consider it a change (new data)
#                         is_changed = True

#                     # If any field has changed, create a new entry
#                     if is_changed:
#                         Supplier_Product_Amount_Details.objects.create(
#                             Supplier_detials=supplier_product_ins,
#                             PurchaseRateBeforeGST=PurchaseRateBeforeGST,
#                             GST=product_GST,
#                             PurchaseRateAfterGST=PurchaseRateAfterGST,
#                             MRP=product_MRP,
#                             EditType='Master',
#                             created_by=created_by
#                         )
                    
                    
#                     return JsonResponse({'success': 'Product details updated successfully'}, status=200)

#                 except Supplier_Product_Details.DoesNotExist:
#                     return JsonResponse({'error': 'Product details not found'}, status=404)
           
#             # Retrieve the appropriate model for the product category
#             selected_model = filters.get(ProductCategory)
#             if not selected_model:
#                 return JsonResponse({'warn': 'Invalid Product Category'}, status=400)

#             content_type = ContentType.objects.get_for_model(selected_model)
#             supplier_ins = Supplier_Master_Details.objects.get(pk=SupplierId)

#             # Create new supplier product mapping
#             if Supplier_Product_Details.objects.filter(
#                     Supplier_Name=supplier_ins,
#                     Product_Content_Type=content_type,
#                     Product_Object_Id=ItemId,
#                 ).exists():
#                 return JsonResponse({'warn': f'Product details already exist for {supplier_ins.Supplier_Name}'}, status=200)

#             supp_prod_inss = Supplier_Product_Details.objects.create(
#                 Supplier_Name=supplier_ins,
#                 Product_Content_Type=content_type,
#                 Product_Object_Id=ItemId,
#                 created_by=created_by
#             )
#             Supplier_Product_Amount_Details.objects.create(
#                 Supplier_detials=supp_prod_inss,
#                 PurchaseRateBeforeGST=PurchaseRateBeforeGST,
#                 GST=product_GST,
#                 PurchaseRateAfterGST=PurchaseRateAfterGST,
#                 MRP=product_MRP,
#                 EditType='Master',
#                 created_by=created_by
#             )
            
#             return JsonResponse({'success': f'Product details added successfully for {supplier_ins.Supplier_Name}'}, status=201)

#         except Supplier_Master_Details.DoesNotExist:
#             return JsonResponse({'error': 'Supplier not found'}, status=404)

#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON format'}, status=400)

#         except Exception as e:
#             print(f'An error occurred: {str(e)}')
#             return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
        


# @csrf_exempt
# @require_http_methods(["GET"])
# def Supplier_Product_Category_link(request):
#     if request.method == "GET":
#         try:
#             SupplierId = request.GET.get('SupplierId')
#             ProductCategory=request.GET.get('ProductCategory','')
#             SubCategory=request.GET.get('SubCategory','')


#             if not SupplierId:
#                 return JsonResponse({'error': 'SupplierId is required'}, status=400)

#             category = []

#             Sub_category = []

#             Item_Array=[]

#             filters = {
#                 1: Medical_Consumable_ProductMaster_Details,
#                 2: Medical_Non_Consumable_ProductMaster_Details,
#                 3: Non_Medical_Consumable_ProductMaster_Details,
#                 4: Non_Medical_Non_Consumable_ProductMaster_Details,
#                 5: Surgical_Consumable_ProductMaster_Details,
#                 6: Surgical_Non_Consumable_ProductMaster_Details,
#                 7: Stationery_ProductMaster_Details,
#                 8: Assets_Movable_ProductMaster_Details,
#                 9: Assets_Non_Movable_ProductMaster_Details,
#                 10: Lenin_ProductMaster_Details,
#                 11: Kitchen_ProductMaster_Details,
#                 12: Miscellaneous_ProductMaster_Details,
#             }
            
#             if SupplierId and ProductCategory and SubCategory:
                
#                 selected_model = filters.get(int(ProductCategory))
#                 content_type = ContentType.objects.get_for_model(selected_model)

#                 products = Supplier_Product_Details.objects.filter(
#                     Supplier_Name__pk=SupplierId,
#                     Product_Content_Type=content_type,
#                     Status=True
#                     )
                
                
#                 model_fields = [field.name for field in selected_model._meta.get_fields()]
                
                
#                 for ins in products:
#                     product_item = ins.Product_Item  # Access GenericForeignKey Product_Item

#                     sup_pro_amount_ins = Supplier_Product_Amount_Details.objects.filter(
#                             Supplier_detials=ins
#                         ).order_by('-Created_at').first()
                    
#                     data = {
#                         'id': product_item.pk,
#                         'ItemName': product_item.ItemName,   
#                         'CompanyName': product_item.CompanyName if 'CompanyName' in model_fields and product_item.CompanyName   else '',
#                         'GenericName': product_item.GenericName if 'GenericName' in model_fields  and product_item.GenericName  else '',
#                         'HSNCode': product_item.HSNCode if 'HSNCode' in model_fields  and product_item.HSNCode else '',
#                         'Quantity': product_item.Quantity if 'Quantity' in model_fields  and product_item.Quantity else '',
#                         'UOM': product_item.UOM.Unit_Name if 'UOM' in model_fields  and product_item.UOM else '',
#                         'Size': product_item.Size if 'Size' in model_fields and product_item.Size  else '',
#                         'DrugType': product_item.DrugType.DrugType_Name if 'DrugType' in model_fields and product_item.DrugType else '',
#                         'DrugGroup': product_item.DrugGroup.DrugGroup_Name if 'DrugGroup' in model_fields and product_item.DrugGroup else '',
#                         'PackType': product_item.PackType.ProductType_Name if 'PackType' in model_fields and product_item.PackType else '',
#                         'PackQty': product_item.PackQty if 'PackQty' in model_fields and product_item.PackQty else '',
#                         'MRP': sup_pro_amount_ins.MRP,
#                         'PurchaseRateBeforeGST': sup_pro_amount_ins.PurchaseRateBeforeGST,
#                         'GST': sup_pro_amount_ins.GST,
#                         'PurchaseRateAfterGST': sup_pro_amount_ins.PurchaseRateAfterGST,
                       
#                     }
                    

#                     filtereddata = {}
#                     for key, value in data.items():
#                         if key in ['id', 'SupplierPoductId', 
#                                 'PurchaseRateBeforeGST', 'GST', 
#                                 'PurchaseRateAfterGST', 'MRP', 'Status',
#                                 'ProductCategory','SubCategoryId']:
#                             filtereddata[key] = value
#                         elif key in model_fields:
#                             filtereddata[key] = value

#                     if not filtereddata.get('Size'):  # If Size is empty, remove it
#                         filtereddata.pop('Size', None)
#                     else:  # If Size is not empty, remove Quantity and UOM
#                         filtereddata.pop('Quantity', None)
#                         filtereddata.pop('UOM', None)

#                     Item_Array.append(filtereddata)

#                 return JsonResponse(Item_Array, safe=False)


#             if SupplierId and ProductCategory:
#                 selected_model = filters.get(int(ProductCategory))
#                 print(selected_model)
#                 content_type = ContentType.objects.get_for_model(selected_model)
               

#                 products = Supplier_Product_Details.objects.filter(
#                     Supplier_Name__pk=SupplierId,
#                     Product_Content_Type=content_type,
#                     Status=True
#                     )
                

#                 for product in products:
#                     product_item = product.Product_Item

#                     if (product_item and 
#                         hasattr(product_item, 'SubCategory') and 
#                         hasattr(product_item.SubCategory, 'SubCategory_Id') and
#                         hasattr(product_item.SubCategory, 'SubCategoryName')):

#                         Sub_category_id = product_item.SubCategory.SubCategory_Id
#                         Sub_category_name = product_item.SubCategory.SubCategoryName

#                         if Sub_category_id not in [cat['id'] for cat in Sub_category]:
#                             Sub_category.append({
#                                 'id': Sub_category_id,
#                                 'SubCategoryName': Sub_category_name,
                                
#                             })
#                         Sub_category.sort(key=lambda x: x['id'])
#                 return JsonResponse(Sub_category, safe=False)
            
#             else:
#                 products = Supplier_Product_Details.objects.filter(
#                     Supplier_Name__pk=SupplierId,
#                     Status=True)

#                 for product in products:
#                     product_item = product.Product_Item

#                     if (product_item and 
#                         hasattr(product_item, 'SubCategory') and 
#                         hasattr(product_item.SubCategory, 'ProductCategoryId') and
#                         hasattr(product_item.SubCategory.ProductCategoryId, 'pk') and
#                         hasattr(product_item.SubCategory.ProductCategoryId, 'ProductCategory_Name')):

#                         category_id = product_item.SubCategory.ProductCategoryId.pk
#                         category_name = product_item.SubCategory.ProductCategoryId.ProductCategory_Name

#                         if category_id not in [cat['id'] for cat in category]:
#                             category.append({
#                                 'id': category_id,
#                                 'ProductCategoryName': category_name
#                             })
#                         category.sort(key=lambda x: x['id'])
#                 return JsonResponse(category, safe=False)

#         except Exception as e:
#             print(f'An error occurred: {str(e)}')
#             return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)



# @csrf_exempt
# @require_http_methods(["GET"])
# def Supplier_Data_Get(request):
#     if request.method == "GET":
#         try:
#             SupplierTwo=request.GET.get('SupplierTwo')
#             SupplierId = request.GET.get('SupplierId')
            
#             if SupplierId:
#                 Supplier_Master_instance=Supplier_Master_Details.objects.get(pk=SupplierId)
#                 dic={
#                         'id':Supplier_Master_instance.Supplier_Id,
#                         'SupplierName':Supplier_Master_instance.Supplier_Name,
#                         'SupplierType':Supplier_Master_instance.Supplier_Type,
#                         'ContactPerson':Supplier_Master_instance.Contact_Person,
#                         'ContactNumber':Supplier_Master_instance.Contact_Number,
#                         'EmailAddress':Supplier_Master_instance.Email_Address,
#                         'Address':Supplier_Master_instance.Address,
#                         'RegistrationNumber':Supplier_Master_instance.Registration_Number,
#                         'GSTNumber':Supplier_Master_instance.GST_Number,
#                         'PANNumber':Supplier_Master_instance.PAN_Number,
#                         'PaymentTerms':Supplier_Master_instance.Payment_Terms,
#                         'CreditLimit':Supplier_Master_instance.Credit_Limit,
#                         'LeadTime':Supplier_Master_instance.DeliveryDuration,
#                         'Status':'Active'if  Supplier_Master_instance.Status else 'Inactive',
#                         'Notes':Supplier_Master_instance.Notes,
#                         'PaymentMode':Supplier_Master_instance.Payment_Mode,
                        
#                     }

#                 return JsonResponse(dic,safe=False)
            
#             elif SupplierTwo:
                

#                 Supplier_Master_instance=Supplier_Master_Details.objects.filter(Status=True)

#                 Supplier_Array=[]

#                 for row in Supplier_Master_instance:
#                     dic={
#                         'id':row.pk,
#                         'SupplierName':row.Supplier_Name,
#                     }
#                     Supplier_Array.append(dic)
                
#                 return JsonResponse (Supplier_Array,safe=False)
            
            
            
#         except Exception  as e:
#             print(f'An error occurred: {str(e)}')
#             return JsonResponse ({'error':'An internal server error occurred'},status=500) 




