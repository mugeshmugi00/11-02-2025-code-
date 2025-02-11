import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import  Q
from django.db import transaction
from .models import *
from io import BytesIO
from PIL import Image
import base64
from PyPDF2 import PdfReader, PdfWriter
# import magic
import filetype



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

        def compress_image(image, min_quality=10, step=5):
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
            file_data = file.split(',')[1]
            file_content = base64.b64decode(file_data)
            file_size = len(file_content)
            
            max_size_mb = 5

            if file_size > max_size_mb * 1024 * 1024:
                print('maximum mb')
                return JsonResponse({'warn': f'File size exceeds the maximum allowed size ({max_size_mb}MB)'})

            file_type = get_file_type(file)
            
            if file_type == 'image/jpeg' or file_type == 'image/png':
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


@csrf_exempt
@require_http_methods(["POST", "OPTIONS", "GET"])
def Supplier_Master_Link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            FileAttachment = data.get('FileAttachment', None)
            FileAttachment_prossed = validate_and_process_file(FileAttachment) if FileAttachment else None
            SupplierId = data.get('SupplierId', None)
            StatusEdit = data.get('StatusEdit',False)
            SupplierName = data.get('SupplierName', '')
            SupplierType = data.get('SupplierType', '')
            ContactPerson = data.get('ContactPerson', '')
            ContactNumber = data.get('ContactNumber', '')
            EmailAddress = data.get('EmailAddress', '')
            Address = data.get('Address', '')
            RegistrationNumber = data.get('RegistrationNumber', '')
            GSTNumber = data.get('GSTNumber', '')
            PANNumber = data.get('PANNumber', '')
            PaymentTerms = data.get('PaymentTerms', '')
            CreditLimitstr = data.get('CreditLimit', '')
            CreditLimit = int(CreditLimitstr) if CreditLimitstr !='' else 0
            LeadTime = data.get('LeadTime', '')
            Notes = data.get('Notes', '')
            BankName = data.get('BankName', '')
            AccountNumber = data.get('AccountNumber', '')
            IFSCCode = data.get('IFSCCode', '')
            BankBranch = data.get('BankBranch', '')
            created_by = data.get('created_by', '')
            DruglicenseNostr = data.get('DruglicenseNo','')
            DruglicenseNo = DruglicenseNostr if DruglicenseNostr !='' else None
            
            with transaction.atomic():
                if SupplierId :
                    print('--',SupplierId)
                    
                    supplier_ins =Supplier_Master_Details.objects.get(pk = SupplierId)
                    print('--')
                    if StatusEdit:
                        supplier_ins.Status = not supplier_ins.Status
                        supplier_ins.save()
                        return JsonResponse ({'success': 'Supplier Master Updated successfully'})
                        
                    else:
                        if Supplier_Master_Details.objects.filter(Supplier_Name = SupplierName).exclude(pk = SupplierId).exists():
                            return JsonResponse({'warn': f"The Supplier Name are already present in the name of {SupplierName}. "})
                        else:
                            supplier_ins.Supplier_Name = SupplierName
                            supplier_ins.Supplier_Type = SupplierType
                            supplier_ins.Contact_Person = ContactPerson
                            supplier_ins.Contact_Number = ContactNumber
                            supplier_ins.Email_Address = EmailAddress
                            supplier_ins.Address = Address
                            supplier_ins.Registration_Number = RegistrationNumber
                            supplier_ins.GST_Number = GSTNumber
                            supplier_ins.PAN_Number = PANNumber
                            supplier_ins.Druglicense_Number = DruglicenseNo
                            supplier_ins.Payment_Terms = PaymentTerms
                            supplier_ins.Credit_Limit = CreditLimit
                            supplier_ins.DeliveryDuration = LeadTime
                            supplier_ins.Notes = Notes
                            supplier_ins.File_Attachment = FileAttachment_prossed
                            supplier_ins.save()
                        
                        
                            
                            if Supplier_Bank_Details.objects.filter(Supplier_Detials__pk = SupplierId).exists():
                                supplier_bank_ins = Supplier_Bank_Details.objects.get(Supplier_Detials__pk =SupplierId)
                                supplier_bank_ins.Bank_Name = BankName
                                supplier_bank_ins.Account_Number= AccountNumber
                                supplier_bank_ins.IFSCCode= IFSCCode
                                supplier_bank_ins.BankBranch=BankBranch
                                supplier_bank_ins.save()
                                    
                            else:
                                Supplier_Bank_Details.objects.create(
                                Supplier_Detials= supplier_ins,
                                Bank_Name= BankName,
                                Account_Number= AccountNumber,
                                IFSCCode= IFSCCode,
                                BankBranch=BankBranch,
                                )
                        return JsonResponse ({'success': 'Supplier Master Updated successfully'})
                            
                else:
                    if Supplier_Master_Details.objects.filter(Supplier_Name = SupplierName).exists():
                            return JsonResponse({'warn': f"The Supplier Name are already present in the name of {SupplierName}. "})
                    else:
                        supplier_ins = Supplier_Master_Details.objects.create(
                            Supplier_Name = SupplierName,
                            Supplier_Type = SupplierType,
                            Contact_Person = ContactPerson,
                            Contact_Number = ContactNumber,
                            Email_Address = EmailAddress,
                            Address = Address,
                            Registration_Number = RegistrationNumber,
                            GST_Number = GSTNumber,
                            PAN_Number = PANNumber,
                            Druglicense_Number = DruglicenseNo,
                            Payment_Terms = PaymentTerms,
                            Credit_Limit = CreditLimit,
                            DeliveryDuration = LeadTime,
                            Notes = Notes,
                            File_Attachment = FileAttachment_prossed,
                            created_by = created_by
                            )
                        

                        Supplier_Bank_Details.objects.create(
                            Supplier_Detials= supplier_ins,
                            Bank_Name= BankName,
                            Account_Number= AccountNumber,
                            IFSCCode= IFSCCode,
                            BankBranch=BankBranch
                        )
                        return JsonResponse ({'success': 'Supplier Master Created successfully'})
                        
                    
               
                        
                    
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse ({'error':'An internal server error occurred'},status=500)
    elif request.method == 'GET':
        
       
        try:
            
            SupplierId = request.GET.get('SupplierId')
            SupplierName = request.GET.get('SupplierName')
            SupplierType = request.GET.get('SupplierType')
            ContactNumber = request.GET.get('ContactNumber')
            FilterBy = request.GET.get('FilterBy','Supplier')
            forfilter =bool(request.GET.get('forfilter',False))
            ProductCategory = request.GET.get('ProductCategory','')
            SubCategory = request.GET.get('SubCategory','')
            ItemCode = request.GET.get('ItemCode','')
            ItemName = request.GET.get('ItemName','')
            GenericName = request.GET.get('GenericName','')
            CompanyName = request.GET.get('CompanyName','')
            HSNCode = request.GET.get('HSNCode','')
            
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
                    
            if FilterBy == 'Supplier':      
                if not forfilter and SupplierId:
                    Supplier_Master_instance=Supplier_Master_Details.objects.get(pk=SupplierId)
                    dic={
                            'id':Supplier_Master_instance.Supplier_Id,
                            'SupplierName':Supplier_Master_instance.Supplier_Name,
                            'SupplierType':Supplier_Master_instance.Supplier_Type,
                            'ContactPerson':Supplier_Master_instance.Contact_Person,
                            'ContactNumber':Supplier_Master_instance.Contact_Number,
                            'EmailAddress':Supplier_Master_instance.Email_Address,
                            'Address':Supplier_Master_instance.Address,
                            'RegistrationNumber':Supplier_Master_instance.Registration_Number,
                            'GSTNumber':Supplier_Master_instance.GST_Number,
                            'PANNumber':Supplier_Master_instance.PAN_Number,
                            'PaymentTerms':Supplier_Master_instance.Payment_Terms,
                            'CreditLimit':Supplier_Master_instance.Credit_Limit,
                            'LeadTime':Supplier_Master_instance.DeliveryDuration,
                            'Status':'Active'if  Supplier_Master_instance.Status else 'Inactive',
                            'Notes':Supplier_Master_instance.Notes                         
                        }

                    return JsonResponse(dic,safe=False)
                else:
                    filter_conditions = Q()
                    if SupplierId:
                        filter_conditions &= Q(pk__icontains = SupplierId)
                    if SupplierName:
                        filter_conditions &= Q(Supplier_Name__icontains =SupplierName)
                    if SupplierType:
                        filter_conditions &= Q(Supplier_Type__icontains =SupplierType)
                    if ContactNumber:
                        filter_conditions &= Q(Contact_Number__icontains =ContactNumber)
                    
                    Supplier_Master_instance=Supplier_Master_Details.objects.filter(filter_conditions)

                    Supplier_Array=[]

                    
                    index = 1
                    for row in Supplier_Master_instance:
                        dic={
                            'id':index,
                            'SupplierId':row.pk,
                            'SupplierName':row.Supplier_Name,
                            'SupplierType':row.Supplier_Type,
                            'ContactPerson':row.Contact_Person,
                            'ContactNumber':row.Contact_Number,
                            'EmailAddress':row.Email_Address,
                            'Address':row.Address,
                            'RegistrationNumber':row.Registration_Number,
                            'GSTNumber':row.GST_Number,
                            'PANNumber':row.PAN_Number,
                            'DruglicenseNo':row.Druglicense_Number,
                            'PaymentTerms':row.Payment_Terms,
                            'CreditLimit':row.Credit_Limit,
                            'LeadTime':row.DeliveryDuration,
                            'Status':'Active'if  row.Status else 'Inactive',
                            'Notes':row.Notes,
                            'FileAttachment':get_file_image(row.File_Attachment) if row.File_Attachment else None,
                        }
                        
                    

                        

                        Supplier_Bank_instance=Supplier_Bank_Details.objects.filter(Supplier_Detials__pk=row.Supplier_Id)
                        bank_Array=[]
                        if Supplier_Bank_instance:
                                
                            for Bank in Supplier_Bank_instance:
                                bankdic={
                                    'id':Bank.pk,
                                    'BankName':Bank.Bank_Name,
                                    'AccountNumber':Bank.Account_Number,
                                    'IFSCCode':Bank.IFSCCode,
                                    'BankBranch':Bank.BankBranch,
                                }
                                bank_Array.append(bankdic)
                                
                            dic['Bank_Details']=bank_Array
                        else:
                            dic['Bank_Details']=[]
                       


                        Supplier_Array.append(dic)
                        index += 1



                    return JsonResponse (Supplier_Array,safe=False)
            else:
                
                filter_conditions = Q()
                
                if ProductCategory:
                    filter_conditions &= Q(ProductCategory__pk =ProductCategory)
                if SubCategory:
                    filter_conditions &= Q(SubCategory__pk =SubCategory)
                if ItemCode:
                    filter_conditions &= Q(pk__icontains=ItemCode)
                if ItemName:
                    filter_conditions &= Q(ItemName__icontains=ItemName)
                if GenericName:
                    filter_conditions &= Q(GenericName__pk=GenericName)
                if CompanyName:
                    filter_conditions &= Q(CompanyName__pk=CompanyName)
                if HSNCode:
                    filter_conditions &= Q(HSNCode__icontains=HSNCode)
                    
                Product_Instance = Product_Master_All_Category_Details.objects.filter(filter_conditions)
                productList=[]
                if Product_Instance.exists():
                    for ins in Product_Instance:
                        data={
                            "id":len(productList)+1,
                            "ItemCode":ins.pk,
                            "ItemName":ins.ItemName,
                            "ProductCategory":ins.ProductCategory.ProductCategory_Name if ins.ProductCategory else '',
                            "SubCategory":ins.SubCategory.SubCategoryName if ins.SubCategory else '',
                        }
                        productList.append(data)
                return JsonResponse (productList,safe=False)
                
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse ({'error':'An internal server error occurred'},status=500)
    else:
        return JsonResponse ({'error':'method not allowed'},status=400)




@csrf_exempt
@require_http_methods(["POST", "OPTIONS","GET"])
def Supplier_product_Mapping_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Extract required fields
            SupplierId = data.get('SupplierId')
            ItemId = data.get('ItemCode')
            PurchaseRateBeforeGST = data.get('PurchaseRateBeforeGST')
            product_GST = data.get('GST')
            PurchaseRateAfterGST = data.get('PurchaseRateAfterGST')
            product_MRP = data.get('MRP')
            edit = data.get('edit', False)
            pk = data.get('pk', None)
            statusedit = data.get('statusedit', False)
            created_by = data.get('created_by','')


            print('kkkkk',edit,pk)
            # Validation for required fields
            if edit :
                if not pk:
                    return JsonResponse({'warn': 'Product Category is a mandatory field'}, status=400)
            else:
                
                if not SupplierId:
                    return JsonResponse({'warn': 'SupplierId is a mandatory field'}, status=400)
                if not ItemId:
                    return JsonResponse({'warn': 'ItemId is a mandatory field'}, status=400)

 
            if edit and pk:
                try:
                    supplier_product_ins = Supplier_Product_Details.objects.get(pk=pk)
                    
                    if statusedit:
                        supplier_product_ins.Status = not supplier_product_ins.Status
                        supplier_product_ins.save()
                        return JsonResponse({'success': f'Product status updated for the Supplier of {supplier_product_ins.Supplier_Detials.Supplier_Name}'}, status=200)
                    # Fetch the latest record based on supplier details
                    
                    print('SupplierId-----',SupplierId)
                    
                    sup_pro_amount_ins = Supplier_Product_Amount_Details.objects.filter(
                        Supplier_detials=supplier_product_ins
                    ).order_by('-Created_at').first()

                    if sup_pro_amount_ins:
                        print(sup_pro_amount_ins.Supplier_detials)
                    else:
                        print("No matching Supplier_Product_Amount_Details found.")

                    # Flag to check if any field value has changed
                    is_changed = False

                    # Check if the values differ from the latest record

                    print('vvvvv----1111','pk---',pk,product_GST,'--name:',sup_pro_amount_ins.Supplier_detials.Supplier_Detials.Supplier_Name,sup_pro_amount_ins.GST,sup_pro_amount_ins.GST != product_GST)

                    if sup_pro_amount_ins:
                        if (sup_pro_amount_ins.PurchaseRateBeforeGST != PurchaseRateBeforeGST or
                            sup_pro_amount_ins.GST != product_GST or
                            sup_pro_amount_ins.PurchaseRateAfterGST != PurchaseRateAfterGST or
                            sup_pro_amount_ins.MRP != product_MRP):
                            is_changed = True
                    else:
                        # If no previous record exists, consider it a change (new data)
                        is_changed = True

                    # If any field has changed, create a new entry
                    if is_changed:
                        Supplier_Product_Amount_Details.objects.create(
                            Supplier_detials=supplier_product_ins,
                            PurchaseRateBeforeGST=PurchaseRateBeforeGST,
                            GST=product_GST,
                            PurchaseRateAfterGST=PurchaseRateAfterGST,
                            MRP=product_MRP,
                            EditType='Master',
                            created_by=created_by
                        )
                    
                    
                    return JsonResponse({'success': 'Product details updated successfully'}, status=200)

                except Supplier_Product_Details.DoesNotExist:
                    return JsonResponse({'error': 'Product details not found'}, status=404)
           
           

           
            supplier_ins = Supplier_Master_Details.objects.get(pk=SupplierId)
            product_ins = Product_Master_All_Category_Details.objects.get(pk = ItemId)
            # Create new supplier product mapping
           
            if Supplier_Product_Details.objects.filter(
                    Supplier_Detials=supplier_ins,
                    Product_Detials=product_ins,
                ).exists():
                return JsonResponse({'warn': f'Product details already exist for {supplier_ins.Supplier_Name}'}, status=200)

            supp_prod_inss = Supplier_Product_Details.objects.create(
                Supplier_Detials=supplier_ins,
                Product_Detials=product_ins,
                created_by=created_by
            )
            Supplier_Product_Amount_Details.objects.create(
                Supplier_detials=supp_prod_inss,
                PurchaseRateBeforeGST=PurchaseRateBeforeGST,
                GST=product_GST,
                PurchaseRateAfterGST=PurchaseRateAfterGST,
                MRP=product_MRP,
                EditType='Master',
                created_by=created_by
            )
            
            return JsonResponse({'success': f'Product details added successfully for {supplier_ins.Supplier_Name}'}, status=201)

        except Supplier_Master_Details.DoesNotExist:
            return JsonResponse({'error': 'Supplier not found'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
    elif request.method =='GET':
        try:
            SupplierId = request.GET.get('SupplierId')
            ItemCode = request.GET.get('ItemCode')
            ItemName = request.GET.get('ItemName')
            mappedProducts = request.GET.get('mappedProducts', 'false').lower() == 'true'
            forquickgrn = request.GET.get('forquickgrn', 'false').lower() == 'true'
            
            if not SupplierId:
                return JsonResponse({'error': 'SupplierId is required'}, status=400)
            
            productlist = []
            
            if not mappedProducts:
                print('11111111111')
                if not forquickgrn:
                    print('22222222')

                    Supplier_Product_instance = Supplier_Product_Details.objects.filter(Supplier_Detials__pk=SupplierId)
                else:
                    print('33333333')

                    
                    filtercondition=Q()
                    if ItemCode:
                        filtercondition &= Q(Product_Detials__pk__icontains=ItemCode)
                    if ItemName:
                        filtercondition &= Q(Product_Detials__ItemName__icontains = ItemName)
                    Supplier_Product_instance = Supplier_Product_Details.objects.filter(Supplier_Detials__pk=SupplierId,Status =True).filter(filtercondition)[:10]
                    
                if Supplier_Product_instance.exists():
                    print('4444444')


                    print('mmmm',forquickgrn,SupplierId)

                    for ins in Supplier_Product_instance:
                        product_item = ins.Product_Detials  # Access GenericForeignKey Product_Item
                        sup_pro_amount_ins = Supplier_Product_Amount_Details.objects.filter(Supplier_detials=ins).order_by('-Created_at').first()
                        product_field_names = Product_Category_Product_Details.objects.get(pk = product_item.SubCategory.ProductCategoryId.pk).Product_fields.values_list('field_Name',flat=True)
                        
                        print(ins.pk,'sup_pro_amount_ins---supId',sup_pro_amount_ins.Supplier_detials.Supplier_Detials.Supplier_Id)
                        data = {
                            'id': len(productlist) + 1,
                            'SupplierPoductId': ins.pk,
                            'ItemCode': product_item.pk,
                            'ItemName': product_item.ItemName,
                            'ProductCategory': product_item.SubCategory.ProductCategoryId.ProductCategory_Name,
                            'SubCategory': product_item.SubCategory.SubCategoryName,
                            'ManufacturerName': product_item.CompanyName.CompanyName if product_item.CompanyName else '',
                            'GenericName': product_item.GenericName.GenericName if product_item.GenericName else '',
                            'HSNCode': product_item.HSNCode if product_item.HSNCode else '',
                            'PackType': product_item.PackType.PackType_Name if product_item.PackType else '',
                            'PackQuantity': product_item.PackQty if product_item.PackQty else '',
                            'LeastSellableUnit': product_item.LeastSellableUnit if product_item.LeastSellableUnit else '',
                            'MRP' if not forquickgrn else "PreviousMRP": sup_pro_amount_ins.MRP if sup_pro_amount_ins else '',
                            'PurchaseRateBeforeGST'if not forquickgrn else 'PreviousPurchaseRateBeforeGST': sup_pro_amount_ins.PurchaseRateBeforeGST if sup_pro_amount_ins else '',
                            'GST' if not forquickgrn else 'PreviousGST': sup_pro_amount_ins.GST if sup_pro_amount_ins else '',
                            'PurchaseRateAfterGST' if not forquickgrn else 'PreviousPurchaseRateAfterGST': sup_pro_amount_ins.PurchaseRateAfterGST if sup_pro_amount_ins else '',
                            'Status': 'Active' if ins.Status else 'Inactive',
                            'Is_Manufacture_Date_Available': product_item.Is_Manufacture_Date_Available ,
                            'Is_Expiry_Date_Available': product_item.Is_Expiry_Date_Available ,
                        }
                        filtereddata={}
                        print('nnnn','vvvvvvvvv')
                        for fields,value in data.items():
                            cleaned_product_field_names = [field.replace(' ', '') for field in product_field_names]
                            if fields in [
                                'id','SupplierPoductId','MRP','PurchaseRateBeforeGST','GST','PurchaseRateAfterGST',
                                'PreviousMRP','PreviousPurchaseRateBeforeGST','PreviousGST',
                                'PreviousPurchaseRateAfterGST','Status','Is_Manufacture_Date_Available',
                                'Is_Expiry_Date_Available']:
                                filtereddata[fields]=value 
                            
                            elif fields=='LeastSellableUnit' :
                                if 'IsSellable' in cleaned_product_field_names:
                                    filtereddata[fields]=value
                                else:
                                    filtereddata[fields]='Not Sellable'
                            else:
                                if fields in cleaned_product_field_names:
                                    filtereddata[fields]=value
                            

                        productlist.append(filtereddata)


                return JsonResponse(productlist, safe=False)
            else:
                print('5555555')

                Supplier_Product_mapped_ins = Supplier_Product_Details.objects.filter(Supplier_Detials__pk=SupplierId).values_list('Product_Detials__pk', flat=True)
                filtercondition = Q()
                
                if ItemCode:
                    filtercondition &= Q(pk__icontains=ItemCode)
                if ItemName:
                    filtercondition &= Q(ItemName__icontains=ItemName)
                    
                product_ins = Product_Master_All_Category_Details.objects.filter(Status=True).filter(filtercondition).exclude(pk__in=Supplier_Product_mapped_ins)[:10]
                
                for ins in product_ins:
                    sup_pro_amount_ins = Supplier_Product_Amount_Details.objects.filter(Supplier_detials__Supplier_Detials__pk=SupplierId,Supplier_detials__Product_Detials__pk=ins.pk).order_by('-Created_at').first()
                    product_field_names = Product_Category_Product_Details.objects.get(pk = ins.SubCategory.ProductCategoryId.pk).Product_fields.values_list('field_Name',flat=True)
                    print('nnnnn','kkkkkkkkkkk')
                    data = {
                        'id': ins.pk,
                        'ItemName': ins.ItemName,
                        'ProductCategory': ins.SubCategory.ProductCategoryId.ProductCategory_Name,
                        'SubCategory': ins.SubCategory.SubCategoryName,
                        'CompanyName': ins.CompanyName.CompanyName if ins.CompanyName else '',
                        'GenericName': ins.GenericName.GenericName if ins.GenericName else '',
                        'HSNCode': ins.HSNCode if ins.HSNCode else '',
                        'PackType': ins.PackType.PackType_Name if ins.PackType else 'Nill',
                        'PackQuantity': ins.PackQty if ins.PackQty else 'Nill',
                        'MRP': sup_pro_amount_ins.MRP if sup_pro_amount_ins else '',
                        'PurchaseRateBeforeGST': sup_pro_amount_ins.PurchaseRateBeforeGST if sup_pro_amount_ins else '',
                        'GST': sup_pro_amount_ins.GST if sup_pro_amount_ins else '',
                        'PurchaseRateAfterGST': sup_pro_amount_ins.PurchaseRateAfterGST if sup_pro_amount_ins else '',
                    }
                    filtereddata={}
                    for fields,value in data.items():
                        if fields in ['id','MRP','PurchaseRateBeforeGST','GST','PurchaseRateAfterGST']:
                            filtereddata[fields]=value 
                        else:
                            cleaned_product_field_names = [field.replace(' ', '') for field in product_field_names]
                            if fields in cleaned_product_field_names:
                                filtereddata[fields]=value
                        

                    productlist.append(filtereddata)
                
                return JsonResponse(productlist, safe=False)
        
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
    
    else:
        return JsonResponse({'error': f'An error occurred: Request method not allowed'}, status=500)

    


@csrf_exempt
@require_http_methods(["GET"])
def Supplier_Data_Get(request):
    if request.method == "GET":
        try:
            ForQuickGrn = request.GET.get('ForQuickGrn', 'false').lower() == 'true'
            SupplierCode = request.GET.get('SupplierCode')
            SupplierName = request.GET.get('SupplierName')
            if not ForQuickGrn:
                if SupplierCode:
                    Supplier_Master_instance=Supplier_Master_Details.objects.get(pk=SupplierCode)
                    dic={
                            'id':Supplier_Master_instance.Supplier_Id,
                            'SupplierName':Supplier_Master_instance.Supplier_Name,
                            'SupplierType':Supplier_Master_instance.Supplier_Type,
                            'ContactPerson':Supplier_Master_instance.Contact_Person,
                            'ContactNumber':Supplier_Master_instance.Contact_Number,
                            'EmailAddress':Supplier_Master_instance.Email_Address,
                            'Address':Supplier_Master_instance.Address,
                            'RegistrationNumber':Supplier_Master_instance.Registration_Number,
                            'GSTNumber':Supplier_Master_instance.GST_Number,
                            'PANNumber':Supplier_Master_instance.PAN_Number,
                            'PaymentTerms':Supplier_Master_instance.Payment_Terms,
                            'CreditLimit':Supplier_Master_instance.Credit_Limit,
                            'LeadTime':Supplier_Master_instance.DeliveryDuration,
                            'Status':'Active'if  Supplier_Master_instance.Status else 'Inactive',
                            'Notes':Supplier_Master_instance.Notes,
                            # 'PaymentMode':Supplier_Master_instance.Payment_Mode,
                            
                        }

                    return JsonResponse(dic,safe=False)
            
            else:
                filterQuery=Q()
                if SupplierCode:
                    filterQuery &= Q(pk__icontains = SupplierCode)
                if SupplierName:
                    filterQuery &= Q(Supplier_Name__icontains = SupplierName)

                Supplier_Master_instance=Supplier_Master_Details.objects.filter(Status=True).filter(filterQuery)[:10]

                Supplier_Array=[]

                for row in Supplier_Master_instance:
                    dic={
                        'id':row.pk,
                        'SupplierName':row.Supplier_Name,
                        'ContactNo':row.Contact_Number,
                    }
                    Supplier_Array.append(dic)
                
                return JsonResponse (Supplier_Array,safe=False)
            
            
            
        except Exception  as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse ({'error':'An internal server error occurred'},status=500) 




@csrf_exempt
@require_http_methods(["GET"])
def Product_wise_supplier_getdata(request):
    if request.method == "GET":
        try:
            ItemCode = request.GET.get('ItemCode', '')

            if ItemCode :
                
                # Get the supplier product details related to the ItemId
                Supplier_Product_instance = Supplier_Product_Details.objects.filter(
                    Product_Detials__pk=ItemCode
                ).order_by('Supplier_Detials__pk')

                # Dictionary to store final result
                list_supplier = {
                    'data': [],
                    'Suppliers':[]
                }

                # Prepare a set of suppliers
                
                for sup_ins in Supplier_Product_instance:
                    list_supplier['Suppliers'].append({
                        "id":sup_ins.Supplier_Detials.pk,
                        "Name":sup_ins.Supplier_Detials.Supplier_Name
                    })
                
                # List of Amount types to loop over
                amount_types = ["PurchaseRateBeforeGST", "GST", "PurchaseRateAfterGST", "MRP"]
                amount_type_labels = {
                    "PurchaseRateBeforeGST": "PurchaseRateBeforeGST",
                    "GST": "GST",
                    "PurchaseRateAfterGST": "PurchaseRateAfterGST",
                    "MRP": "MRP"
                }
                
                # Loop through each amount type and create rows for each supplier
                for amount_type in amount_types:
                    dic = {
                        'id': len(list_supplier['data']) + 1,
                        'AmountType': amount_type_labels[amount_type],
                    }

                    

                    # Populate supplier-specific values
                    for sup_ins in Supplier_Product_instance:
                        supp_pro_amount_ins = Supplier_Product_Amount_Details.objects.filter(
                            Supplier_detials=sup_ins,
                            Supplier_detials__Product_Detials__pk=ItemCode
                        )
                        for s_amount in supp_pro_amount_ins:
                            supplier_key = f"{str(sup_ins.Supplier_Detials.pk)}"
                            dic[supplier_key] = getattr(s_amount, amount_type, "-")

                    list_supplier['data'].append(dic)

                return JsonResponse(list_supplier, safe=False)
            else:
                return JsonResponse({'error': 'Both ProductId and ProductCategory are required'}, status=400)

        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def PO_Supplier_Data_Get(request):
    if request.method == "GET":
        try:
            SupplierTwo=request.GET.get('SupplierTwo')
            SupplierId = request.GET.get('SupplierId')
            
            if SupplierId:
                Supplier_Master_instance=Supplier_Master_Details.objects.get(pk=SupplierId)
                dic={
                        'id':Supplier_Master_instance.Supplier_Id,
                        'SupplierName':Supplier_Master_instance.Supplier_Name,
                        'SupplierType':Supplier_Master_instance.Supplier_Type,
                        'ContactPerson':Supplier_Master_instance.Contact_Person,
                        'ContactNumber':Supplier_Master_instance.Contact_Number,
                        'EmailAddress':Supplier_Master_instance.Email_Address,
                        'Address':Supplier_Master_instance.Address,
                        'RegistrationNumber':Supplier_Master_instance.Registration_Number,
                        'GSTNumber':Supplier_Master_instance.GST_Number,
                        'PANNumber':Supplier_Master_instance.PAN_Number,
                        'PaymentTerms':Supplier_Master_instance.Payment_Terms,
                        'CreditLimit':Supplier_Master_instance.Credit_Limit,
                        'LeadTime':Supplier_Master_instance.DeliveryDuration,
                        'Status':'Active'if  Supplier_Master_instance.Status else 'Inactive',
                        'Notes':Supplier_Master_instance.Notes,
                        
                    }

                return JsonResponse(dic,safe=False)
            
            elif SupplierTwo:
                

                Supplier_Master_instance=Supplier_Master_Details.objects.filter(Status=True)

                Supplier_Array=[]

                for row in Supplier_Master_instance:
                    dic={
                        'id':row.pk,
                        'SupplierName':row.Supplier_Name,
                    }
                    Supplier_Array.append(dic)
                
                return JsonResponse (Supplier_Array,safe=False)
            
            
            
        except Exception  as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse ({'error':'An internal server error occurred'},status=500) 




# -------------------change 10.10.24


@csrf_exempt
@require_http_methods(["GET"])
def PO_SupplierWise_product_Get(request):
    if request.method == "GET":
        try:
            SupplierId = request.GET.get('SupplierId')
            POitems = request.GET.get('POitems')
            SupplierTwo = request.GET.get('SupplierTwo')

            Item_Array=[]
            # Convert POitems to a list of integers if it's not empty
            if POitems:
                POitems_list = [int(item) for item in POitems.split(',')]
            else:
                POitems_list = []

            if SupplierId:
                Supplier_Product_Inst = Supplier_Product_Details.objects.filter(Supplier_Detials__Supplier_Id=SupplierId, Status=True)
            else:
                return JsonResponse({'error': 'Supplier not found'}, status=404)

            if not Supplier_Product_Inst:
                return JsonResponse(Item_Array, safe=False)

            if SupplierTwo:
                for row in Supplier_Product_Inst:
                    item_Dec = {
                        'ItemCode': row.Product_Detials.pk,
                        'ItemName': row.Product_Detials.ItemName,
                        'ProductCategory': row.Product_Detials.ProductCategory.ProductCategory_Name,
                        'SubCategory': row.Product_Detials.SubCategory.SubCategoryName,
                    }
                    Item_Array.append(item_Dec)

            else:
                for row in Supplier_Product_Inst:
                    if not POitems_list or row.Product_Detials.pk not in POitems_list:
                        Get_Rate_Inst = Supplier_Product_Amount_Details.objects.filter(Supplier_detials=row,Supplier_detials__Product_Detials=row.Product_Detials).order_by('-Created_at').first()
                        item_Dec = {
                            'ItemCode': row.Product_Detials.pk,
                            'ItemName': row.Product_Detials.ItemName,
                            'ProductCategory': row.Product_Detials.ProductCategory.ProductCategory_Name,
                            'SubCategory': row.Product_Detials.SubCategory.SubCategoryName,
                        }

                        if row.Product_Detials.GenericName:
                            item_Dec['GenericName'] = row.Product_Detials.GenericName.GenericName
                        if row.Product_Detials.CompanyName:
                            item_Dec['ManufacturerName'] = row.Product_Detials.CompanyName.CompanyName
                        if row.Product_Detials.HSNCode:
                            item_Dec['HSNCode'] = row.Product_Detials.HSNCode
                        if row.Product_Detials.Strength:
                            item_Dec['Strength'] = row.Product_Detials.Strength
                        if row.Product_Detials.StrengthType:
                            item_Dec['StrengthType'] = row.Product_Detials.StrengthType
                        if row.Product_Detials.Volume:
                            item_Dec['Volume'] = row.Product_Detials.Volume
                        if row.Product_Detials.VolumeType:
                            item_Dec['VolumeType'] = row.Product_Detials.VolumeType.Unit_Name
                        if row.Product_Detials.PackType:
                            item_Dec['PackType'] = row.Product_Detials.PackType.PackType_Name
                        if row.Product_Detials.PackQty:
                            item_Dec['PackQty'] = row.Product_Detials.PackQty

                        if row.Product_Detials.Is_Manufacture_Date_Available:
                            item_Dec['Is_Manufacture_Date_Available'] = row.Product_Detials.Is_Manufacture_Date_Available
                        if row.Product_Detials.Is_Expiry_Date_Available:
                            item_Dec['Is_Expiry_Date_Available'] = row.Product_Detials.Is_Expiry_Date_Available

                        # Safely check and assign 'IsSellable'
                        if row.Product_Detials.IsSellable is not None:
                            item_Dec['IsSellable'] = 'Yes' if row.Product_Detials.IsSellable else 'No' 
                            if item_Dec['IsSellable'] == 'Yes':                         
                                item_Dec['LeastSellableUnit'] = row.Product_Detials.LeastSellableUnit

                        item_Dec['MRP'] = Get_Rate_Inst.MRP
                        item_Dec['PurchaseRateBeforeGST'] = Get_Rate_Inst.PurchaseRateBeforeGST
                        item_Dec['GST'] = Get_Rate_Inst.GST
                        item_Dec['PurchaseRateAfterGST'] = Get_Rate_Inst.PurchaseRateAfterGST

                        Item_Array.append(item_Dec)

            return JsonResponse(Item_Array, safe=False)
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
