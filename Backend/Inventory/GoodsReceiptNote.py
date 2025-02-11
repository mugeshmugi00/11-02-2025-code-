import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import  Q,Sum, Value
from django.db.models.functions import Coalesce

from decimal import Decimal, InvalidOperation
from django.db import transaction
from io import BytesIO
from PIL import Image
import base64
from PyPDF2 import PdfReader, PdfWriter
# import magic
import filetype
from .models import (Purchase_Order_Details,GRN_Table_Detials,GRN_Product_Item_Detials,Supplier_Master_Details,
Product_Master_All_Category_Details,Purchase_Order_Item_Details,Supplier_Product_Amount_Details,
Supplier_pay_detials,Supplier_Pay_By_Date,Old_Grn_stock_detials,Stock_Maintance_Table_Detials,Product_Master_All_Category_Details)
from Masters.models import Inventory_Location_Master_Detials,Inventory_Page_Access_Detailes,NurseStationMaster
from datetime import datetime



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

def get_file_image(filedata):
    kind = filetype.guess(filedata)
                
    contenttype1 = 'application/pdf'
    if kind and kind.mime == 'image/jpeg':
        contenttype1 = 'image/jpeg'
    elif kind and kind.mime == 'image/png':
        contenttype1 = 'image/png'

    # Return base64 encoded data with MIME type
    return f'data:{contenttype1};base64,{base64.b64encode(filedata).decode("utf-8")}'
                    
def get_or_none(model, pk):
    try:
        return model.objects.get(pk=pk)
    except model.DoesNotExist:
        return None

def to_decimal(value):
    try:
        return Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        return 0
    
def to_integer(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None

def process_grn_items(grn_table_instance, items, created_by,approval_status):
   
    for item in items:
        item_instance=None
        foc_item_instance=None
        if item.get('ItemCode'):
            item_instance = get_or_none(Product_Master_All_Category_Details, item.get('ItemCode'))
        if item.get('FOCItemCode'):
            foc_item_instance = get_or_none(Product_Master_All_Category_Details, item.get('FOCItemCode'))
        item_status = item.get('Status')
        if item_status == 'Recieved':
            item_status = approval_status
            
        item_data = {
            'Product_Detials': item_instance,
            'Is_Foc_Product': item.get('IsFOCProduct',False),
            'Foc_Product_Detials': foc_item_instance,
            'Tax_Type': item.get('TaxType'),
            'Purchase_rate_taxable': to_decimal(item.get('PurchaseRateTaxable')),
            'Tax_Percentage': to_decimal(item.get('TaxPercentage')),
            'Purchase_rate_with_tax': to_decimal(item.get('PurchaseRateWithTax')),
            'Purchase_MRP': to_decimal(item.get('MRP')),
            'Received_Quantity': to_integer(item.get('ReceivedQty')),
            'FOC_Quantity': to_integer(item.get('FOCQuantity')),
            'Total_Received_Quantity': to_integer(item.get('TotalReceivedQty')),
            'Total_Pack_Quantity': to_integer(item.get('TotalPackQuantity')),
            'Is_MRP_as_sellable_price': item.get('IsMRPAsSellablePrice',False),
            'Sellable_price': to_decimal(item.get('SellablePrice')),
            'Sellable_qty_price': to_decimal(item.get('SellableQtyPrice')),
            'Total_Pack_Taxable_Amount': to_decimal(item.get('TotalPackTaxableAmount')),
            'Total_Pack_Tax_Amount': to_decimal(item.get('TotalTaxAmount')),
            'Total_Pack_Amount_with_tax': to_decimal(item.get('TotalPackAmount')),
            'Batch_No': item.get('BatchNo'),
            'Is_Manufacture_Date_Available': item.get('IsManufactureDateAvailable',False),
            'Manufacture_Date': item.get('ManufactureDate') if item.get('ManufactureDate') else None,
            'Is_Expiry_Date_Available': item.get('IsExpiryDateAvailable',False),
            'Expiry_Date': item.get('ExpiryDate') if item.get('ExpiryDate') else None,
            'Discount_Method': item.get('DiscountMethod'),
            'Discount_Type': item.get('DiscountType'),
            'Discount_Amount': to_decimal(item.get('Discount')),
            'Final_Total_Pack_Taxable_Amount': to_decimal(item.get('FinalTotalPackTaxableAmount')),
            'Final_Total_Pack_Tax_Amount': to_decimal(item.get('FinalTotalTaxAmount')),
            'Final_Total_Pack_Amount_with_tax': to_decimal(item.get('FinalTotalPackAmount')),
            'Status': item_status,
            'Created_by': created_by
        }

        item_pk = item.get('pk')
        
        # if item_pk:
        #     grn_item_instance = get_or_none(GRN_Product_Item_Detials, item_pk)
        #     if grn_item_instance:
        #         for key, value in item_data.items():
        #             if key =='Created_by':
        #                 setattr(grn_table_instance, 'Updated_by', value)
        #             setattr(grn_item_instance, key, value)
        #         grn_item_instance.save()
        # else:
           
        GRN_Product_Item_Detials.objects.create(Grn_Detials=grn_table_instance, **item_data)
        

@csrf_exempt
@require_http_methods(["POST", "OPTIONS", "GET"])
def Goods_Reciept_Note_Details_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            supplier_instance=None
            store_location_instance=None
            approval_status = 'Recieved'
            
            if data.get('SupplierCode'):
                supplier_instance = get_or_none(Supplier_Master_Details, data.get('SupplierCode'))
            if data.get('StoreLocation'):
                store_location_instance = get_or_none(Inventory_Location_Master_Detials, data.get('StoreLocation'))
                if store_location_instance:
                    inv_page_access = Inventory_Page_Access_Detailes.objects.get(Access_StoreId = store_location_instance)
                    # if inv_page_access:
                    #     if data.get('IsQuickGRN', False):
                    #         if inv_page_access.IS_Quick_GRN:
                    #             approval_status ='Recieved' if inv_page_access.IS_Quick_GRN_Approve else 'Approved'
            # Prepare data for GRN table
            with transaction.atomic():
                grn_data = {
                    'IsQuickGRN': data.get('IsQuickGRN', False),
                    'IsOldGRN': data.get('IsOldGRN', False),
                    'GrnDate': data.get('GRNDate', ''),
                    'Supplier_Detials': supplier_instance,
                    'Supplier_Bill_Number': data.get('SupplierBillNumber', ''),
                    'Supplier_Bill_Date': data.get('SupplierBillDate', ''),
                    'Supplier_Bill_Due_Date': data.get('SupplierBillDueDate', ''),
                    'Supplier_Bill_Amount': to_decimal(data.get('SupplierBillAmount')),
                    'Store_location': store_location_instance,
                    'Received_person': data.get('ReceivingPersonName', ''),
                    'Is_Foc_Available': data.get('IsFOCAvailable', False),
                    'Foc_Method': data.get('FOCMethod', ''),
                    'File_Attachment': validate_and_process_file(data.get('FileAttachment')) if data.get('FileAttachment') else None,
                    'Taxable_Amount': to_decimal(data.get('TotalTaxableAmount')),
                    'Tax_Amount': to_decimal(data.get('TotalTaxAmount')),
                    'Total_Amount': to_decimal(data.get('TotalAmount')),
                    'Total_Discount_Method': data.get('TotalDiscountMethod', ''),
                    'Total_Discount_Type': data.get('TotalDiscountType', ''),
                    'Discount_Amount': to_decimal(data.get('TotalDiscount')),
                    'Final_Taxable_Amount': to_decimal(data.get('FinalTotalTaxableAmount')),
                    'Final_Tax_Amount': to_decimal(data.get('FinalTotalTaxAmount')),
                    'Final_Total_Amount': to_decimal(data.get('FinalTotalAmount')),
                    'Round_off_Amount': to_decimal(data.get('RoundOffAmount')),
                    'Net_Amount': to_decimal(data.get('NetAmount')),
                    'Created_by': data.get('Created_by', ''),
                    'Status': approval_status
                }

                pk = data.get('pk')
                if pk:
                    grn_table_instance = get_or_none(GRN_Table_Detials, pk)
                    if grn_table_instance:
                        for key, value in grn_data.items():
                            if key =='Created_by':
                                setattr(grn_table_instance, 'Updated_by', value)
                            setattr(grn_table_instance, key, value)
                        grn_table_instance.save()

                        items_to_delete = GRN_Product_Item_Detials.objects.filter(Grn_Detials=grn_table_instance)
                        if items_to_delete.exists():
                            items_to_delete.delete()
                        else:
                            print("No matching records found in GRN_Product_Item_Detials.")
                else:
                    grn_table_instance = GRN_Table_Detials.objects.create(**grn_data)

                # Process GRN items
                if data.get('GrnItemList'):
                    process_grn_items(grn_table_instance, data['GrnItemList'], data.get('Created_by', ''),approval_status)

                return JsonResponse({'success': 'GRN details saved successfully'}, status=200)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

    elif request.method == 'GET':
        try:
            GRNType = request.GET.get('GRNType')
            DateType=request.GET.get('DateType')
            StatusCheck=request.GET.get('StatusCheck')  
            CurrentDate=request.GET.get('CurrentDate')  
            GrnFromDate = request.GET.get('FromDate')  
            GrnToDate = request.GET.get('ToDate')
            SupplierId = request.GET.get('SupplierId')
            SupplierName = request.GET.get('SupplierName')
            GRNLocation = request.GET.get('GRNLocation')


            # print('00001-----',GRNType,StatusCheck,DateType,CurrentDate,GrnFromDate,GrnToDate,SupplierId,SupplierName,DeliveredLocation)

            
            query = Q()

            if GRNType:
                if GRNType == 'QuickGRN':  
                    GRNType_Condition = Q(IsQuickGRN=True) & Q(IsOldGRN=False)        
                elif GRNType == 'OldGRN':
                    GRNType_Condition = Q(IsOldGRN=True)  & Q(IsQuickGRN=True)
                elif GRNType == 'GRN':
                    GRNType_Condition = Q(IsOldGRN=False) & Q(IsQuickGRN=False)
                else:
                    GRNType_Condition = Q()  

                query &= GRNType_Condition
            

            if DateType == "Current":
                if CurrentDate:
                    query &= Q(GrnDate=CurrentDate)
            elif DateType == "Customize":
                if GrnFromDate and GrnToDate:
                    query &= Q(GrnDate__range=[GrnFromDate, GrnToDate])
                elif GrnFromDate:
                    query &= Q(GrnDate__gte=GrnFromDate)
                elif GrnToDate:
                    query &= Q(GrnDate__lte=GrnToDate)

            
            if StatusCheck:
                query &= Q(Status=StatusCheck)
            if SupplierId:
                query &= Q(Supplier_Detials__pk=SupplierId)
            if SupplierName:
                query &= Q(Supplier_Detials__Supplier_Name__icontains=SupplierName)
            if GRNLocation:
                query &= Q(Store_location__Location_Name__Location_Id=GRNLocation)

            # Fetch GRN table details
            grn_table_instance = GRN_Table_Detials.objects.filter(query)

            grn_table_data = []

            for grn in grn_table_instance :
                dic={
                    'id':len(grn_table_data) + 1,
                    'pk':grn.pk,
                    'IsQuickGRN':grn.IsQuickGRN,
                    'IsOldGRN':grn.IsOldGRN,
                    'GrnDate':grn.GrnDate,
                    'Purchase_order_Detials':grn.Purchase_order_Detials.pk if grn.Purchase_order_Detials else None,
                    'SupplierCode':grn.Supplier_Detials.pk,
                    'SupplierName':grn.Supplier_Detials.Supplier_Name,
                    'ContactPerson':grn.Supplier_Detials.Contact_Person,
                    'ContactNumber':grn.Supplier_Detials.Contact_Number,
                    'EmailAddress':grn.Supplier_Detials.Email_Address,
                    'Supplier_Bill_Number':grn.Supplier_Bill_Number,
                    'Supplier_Bill_Date':grn.Supplier_Bill_Date,
                    'Supplier_Bill_Due_Date':grn.Supplier_Bill_Due_Date,
                    'Supplier_Bill_Amount':grn.Supplier_Bill_Amount,
                    'Use_BillingLocation':grn.Store_location.Location_Name.Location_Name,
                    'Store_location_pk':grn.Store_location.pk,
                    'Store_location':grn.Store_location.Store_Name,
                    'Received_person':grn.Received_person,
                    'Is_Foc_Available':grn.Is_Foc_Available,
                    'Foc_Method':grn.Foc_Method,
                    'FileAttachment':get_file_image(grn.File_Attachment) if grn.File_Attachment else None,
                    'Taxable_Amount':grn.Taxable_Amount,
                    'Tax_Amount':grn.Tax_Amount,
                    'Total_Amount':grn.Total_Amount,
                    'Total_Discount_Method':grn.Total_Discount_Method,
                    'Total_Discount_Type':grn.Total_Discount_Type,
                    'Discount_Amount':grn.Discount_Amount,
                    'Final_Taxable_Amount':grn.Final_Taxable_Amount,
                    'Final_Tax_Amount':grn.Final_Tax_Amount,
                    'Final_Total_Amount':grn.Final_Total_Amount,
                    'Round_off_Amount':grn.Round_off_Amount,
                    'Net_Amount':grn.Net_Amount,
                    'Status':grn.Status,
                    'GRN_Items':[]
                }
                
                for items in GRN_Product_Item_Detials.objects.filter(Grn_Detials = grn.pk):
                    item_dic = {
                        'id' :len(dic['GRN_Items']) +1,
                        'pk':items.pk,
                        'ItemCode':items.Product_Detials.pk,
                        'ItemName':items.Product_Detials.ItemName,
                        'IsFOCProduct':items.Is_Foc_Product,
                        'FOCItemCode':items.Foc_Product_Detials.pk if items.Foc_Product_Detials else '',
                        'FOCItemName':items.Foc_Product_Detials.ItemName if items.Foc_Product_Detials else '',
                        'TaxType':items.Tax_Type,
                        'PurchaseRateTaxable':items.Purchase_rate_taxable,
                        'TaxPercentage':items.Tax_Percentage,
                        'PurchaseRateWithTax':items.Purchase_rate_with_tax,
                        'MRP':items.Purchase_MRP,
                        'ReceivedQty':items.Received_Quantity,
                        'FOCQuantity':items.FOC_Quantity if items.FOC_Quantity else "",
                        'TotalReceivedQty':items.Total_Received_Quantity,
                        'TotalPackQuantity':items.Total_Pack_Quantity,
                        'IsMRPAsSellablePrice':items.Is_MRP_as_sellable_price,
                        'SellablePrice':items.Sellable_price,
                        'SellableQtyPrice':items.Sellable_qty_price,
                        'TotalPackTaxableAmount':items.Total_Pack_Taxable_Amount,
                        'TotalTaxAmount':items.Total_Pack_Tax_Amount,
                        'TotalPackAmount':items.Total_Pack_Amount_with_tax,
                        'BatchNo':items.Batch_No,
                        'IsManufactureDateAvailable':items.Is_Manufacture_Date_Available,
                        'ManufactureDate':items.Manufacture_Date,
                        'IsExpiryDateAvailable':items.Is_Expiry_Date_Available,
                        'ExpiryDate':items.Expiry_Date,
                        'DiscountMethod':items.Discount_Method,
                        'DiscountType':items.Discount_Type,
                        'Discount':items.Discount_Amount,
                        'FinalTotalPackTaxableAmount':items.Final_Total_Pack_Taxable_Amount,
                        'FinalTotalTaxAmount':items.Final_Total_Pack_Tax_Amount,
                        'FinalTotalPackAmount':items.Final_Total_Pack_Amount_with_tax,
                        'Status':items.Status,
                    }
                    dic['GRN_Items'].append(item_dic)
                grn_table_data.append(dic)

            return JsonResponse (grn_table_data,safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

    return JsonResponse({'error': f'An error occurred: Request method not allowed'}, status=405)



@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def Goods_Reciept_Note_Details_Approve_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            InvoiceNo = data.get('InvoiceNo')
            Approved_by = data.get('Approved_by', '')
            
            if InvoiceNo:
                try:
                    grn_table_ins = GRN_Table_Detials.objects.get(pk=InvoiceNo)
                except GRN_Table_Detials.DoesNotExist:
                    return JsonResponse({'error': 'Invoice not found'}, status=404)
                
                grn_table_ins.Status = 'Approved'
                grn_table_ins.Approved_by = Approved_by
                grn_table_ins.save()

                 # Fetch related GRN_Product_Item_Detials instances
                product_items = GRN_Product_Item_Detials.objects.filter(Grn_Detials=grn_table_ins, Status='Recieved')

                # Iterate and update each item to trigger the post_save signal
                for item in product_items:
                    item.Status = 'Approved'
                    item.Approved_by = Approved_by
                    item.save()  
                
                return JsonResponse({'success': 'GRN approved successfully'}, status=200)
            
            return JsonResponse({'error': 'InvoiceNo is required'}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)







# -------------------------VV GRN post-------------------------------------------------------------


def parse_date(date_str):
    try:
        # Try to parse the date to ensure it is in the correct format
        return datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None
    except ValueError:
        # Return None if the format is invalid
        return None

def safe_decimal(value, default=0):
    try:
        return Decimal(value) if value else Decimal(default)
    except (InvalidOperation, TypeError):
        return Decimal(default)

def safe_int(value, default=0):
    try:
        return int(value) if value else default
    except ValueError:
        return default


# ---------------------------------------------------



@csrf_exempt
@require_http_methods(["POST", "OPTIONS", "GET"])
def PO_Goods_Reciept_Note_Details_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Extracting data from the request
            GRNState = data.get('GRNState')
            POItemArrays = data.get('POItemArrays')
            SupplierBillfile = data.get('SupplierBillfile')
            GRNItemlist = data.get('GRNItemlist')
            Amountstate = data.get('Amountstate')
            Created_by = data.get('Created_by')

            # Extracting GRN specific data
            GRNNumber = GRNState.get('GRNNumber')
            GRNDate = GRNState.get('GRNDate')
            PONumber = GRNState.get('PONumber')
            SupplierCode = GRNState.get('SupplierCode')
            SupplierBillNumber = GRNState.get('SupplierBillNumber')
            SupplierBillDate = GRNState.get('SupplierBillDate')
            SupplierBillDueDate = GRNState.get('SupplierBillDueDate')
            SupplierBillAmount = GRNState.get('SupplierBillAmount')
            StorageLocation = GRNState.get('StorageLocation')
            ReceivingPersonName = GRNState.get('ReceivingPersonName')
            IsFOCAvailable = GRNState.get('IsFOCAvailable')
            FOCMethod = GRNState.get('FOCMethod')

            # Extracting amount details
            TotalTaxableAmount = Amountstate.get('TotalTaxableAmount')
            TotalTaxAmount = Amountstate.get('TotalTaxAmount')
            TotalAmount = Amountstate.get('TotalAmount')
            TotalDiscountMethod = Amountstate.get('TotalDiscountMethod')
            TotalDiscountType = Amountstate.get('TotalDiscountType')
            TotalDiscount = Amountstate.get('TotalDiscount')
            FinalTotalTaxableAmount = Amountstate.get('FinalTotalTaxableAmount')
            FinalTotalTaxAmount = Amountstate.get('FinalTotalTaxAmount')
            FinalTotalAmount = Amountstate.get('FinalTotalAmount')
            RoundOff = Amountstate.get('RoundOff')
            NetAmount = Amountstate.get('NetAmount')

            # Fetching related instances
            Purchase_Order_inst = Purchase_Order_Details.objects.get(pk=PONumber) if PONumber else None
            supplier_instance = get_or_none(Supplier_Master_Details, SupplierCode) if SupplierCode else None
            store_location_instance = get_or_none(Inventory_Location_Master_Detials, StorageLocation) if StorageLocation else None

            # Determine approval status
            approval_status = 'Recieved'
            if store_location_instance:
                inv_page_access = Inventory_Page_Access_Detailes.objects.get(Access_StoreId=store_location_instance)
                # if inv_page_access.IS_GRN:
                #     approval_status = 'Recieved' if inv_page_access.IS_GRN_Approve else 'Approved'

            with transaction.atomic():
                # Check if GRN exists, update if it does, else create new
                if GRNNumber:
                    # Update existing GRN entry
                    GRN_Table_Ins = GRN_Table_Detials.objects.get(pk=GRNNumber)
                    GRN_Table_Ins.GrnDate = GRNDate
                    GRN_Table_Ins.Purchase_order_Detials = Purchase_Order_inst
                    GRN_Table_Ins.Supplier_Detials = supplier_instance
                    GRN_Table_Ins.Supplier_Bill_Number = SupplierBillNumber
                    GRN_Table_Ins.Supplier_Bill_Date = SupplierBillDate
                    GRN_Table_Ins.Supplier_Bill_Due_Date = SupplierBillDueDate
                    GRN_Table_Ins.Supplier_Bill_Amount = SupplierBillAmount
                    GRN_Table_Ins.Store_location = store_location_instance
                    GRN_Table_Ins.Received_person = ReceivingPersonName
                    GRN_Table_Ins.Is_Foc_Available = IsFOCAvailable
                    GRN_Table_Ins.Foc_Method = FOCMethod
                    GRN_Table_Ins.File_Attachment = validate_and_process_file(SupplierBillfile) if SupplierBillfile else GRN_Table_Ins.File_Attachment
                    GRN_Table_Ins.Taxable_Amount = safe_decimal(TotalTaxableAmount)
                    GRN_Table_Ins.Tax_Amount = safe_decimal(TotalTaxAmount)
                    GRN_Table_Ins.Total_Amount = safe_decimal(TotalAmount)
                    GRN_Table_Ins.Total_Discount_Method = TotalDiscountMethod
                    GRN_Table_Ins.Total_Discount_Type = TotalDiscountType
                    GRN_Table_Ins.Discount_Amount = safe_decimal(TotalDiscount)
                    GRN_Table_Ins.Final_Taxable_Amount = safe_decimal(FinalTotalTaxableAmount)
                    GRN_Table_Ins.Final_Tax_Amount = safe_decimal(FinalTotalTaxAmount)
                    GRN_Table_Ins.Final_Total_Amount = safe_decimal(FinalTotalAmount)
                    GRN_Table_Ins.Round_off_Amount = safe_decimal(RoundOff)
                    GRN_Table_Ins.Net_Amount = safe_decimal(NetAmount)
                    GRN_Table_Ins.Status = approval_status
                    GRN_Table_Ins.Created_by = Created_by
                    GRN_Table_Ins.save()

                else:
                    # Create new GRN entry
                    GRN_Inst = GRN_Table_Detials.objects.create(
                        GrnDate=GRNDate,
                        Purchase_order_Detials=Purchase_Order_inst,
                        Supplier_Detials=supplier_instance,
                        Supplier_Bill_Number=SupplierBillNumber,
                        Supplier_Bill_Date=SupplierBillDate,
                        Supplier_Bill_Due_Date=SupplierBillDueDate,
                        Supplier_Bill_Amount=SupplierBillAmount,
                        Store_location=store_location_instance,
                        Received_person=ReceivingPersonName,
                        Is_Foc_Available=IsFOCAvailable,
                        Foc_Method=FOCMethod,
                        File_Attachment=validate_and_process_file(SupplierBillfile) if SupplierBillfile else None,
                        Taxable_Amount=safe_decimal(TotalTaxableAmount),
                        Tax_Amount=safe_decimal(TotalTaxAmount),
                        Total_Amount=safe_decimal(TotalAmount),
                        Total_Discount_Method=TotalDiscountMethod,
                        Total_Discount_Type=TotalDiscountType,
                        Discount_Amount=safe_decimal(TotalDiscount),
                        Final_Taxable_Amount=safe_decimal(FinalTotalTaxableAmount),
                        Final_Tax_Amount=safe_decimal(FinalTotalTaxAmount),
                        Final_Total_Amount=safe_decimal(FinalTotalAmount),
                        Round_off_Amount=safe_decimal(RoundOff),
                        Net_Amount=safe_decimal(NetAmount),
                        Status=approval_status,
                        Created_by=Created_by
                    )
                GRN_Product_Item_Detials.objects.filter(Grn_Detials=GRN_Table_Ins if GRNNumber else GRN_Inst).delete()
                # Fetch existing GRN product items
                
                # existing_grn_items = GRN_Product_Item_Detials.objects.filter(Grn_Detials=GRN_Table_Ins if GRNNumber else GRN_Inst)
                # existing_item_ids = {item.Product_Detials for item in existing_grn_items}

                # Track updated item IDs to identify which items to delete
                updated_item_ids = set()

                 # Updating/creating GRN items
                for item in GRNItemlist:
                    item_instance = get_or_none(Product_Master_All_Category_Details, item.get('ItemCode'))
                    foc_item_instance = get_or_none(Product_Master_All_Category_Details, item.get('FOCItemCode')) if item.get('FOCItemCode') else None

                    Total_Quantity = safe_int(item.get('ReceivedQty')) + safe_int(item.get('FOCQty', 0))
                    
                    GRN_Product_Item_Detials.objects.update_or_create(
                        Grn_Detials=GRN_Table_Ins if GRNNumber else GRN_Inst,
                        Product_Detials=item_instance,
                        defaults={
                            'Not_In_PO_Product': item.get('NotInPurchaseOrder'),
                            'Is_Foc_Product': item.get('IsFOCProduct'),
                            'Foc_Product_Detials': foc_item_instance,
                            'Tax_Type': item.get('TaxType'),
                            'Purchase_rate_taxable': safe_decimal(item.get('PurchaseRateTaxable')),
                            'Tax_Percentage': safe_decimal(item.get('TaxPercentage')),
                            'Purchase_rate_with_tax': safe_decimal(item.get('PurchaseRateWithTax')),
                            'Purchase_MRP': safe_decimal(item.get('GRNMRP')),
                            'Received_Quantity': safe_int(item.get('ReceivedQty')),
                            'FOC_Quantity': safe_int(item.get('FOCQty') or 0),
                            'Extra_PO_Quantity': safe_int(item.get('ExtraQty') or 0),
                            'Total_Received_Quantity': safe_int(Total_Quantity),
                            'Total_Pack_Quantity': safe_int(item.get('TotalPackQty')),
                            'Is_MRP_as_sellable_price': safe_decimal(item.get('IsMRPAsSellablePrice')),
                            'Sellable_price': safe_decimal(item.get('SellablePrice')),
                            'Sellable_qty_price': safe_decimal(item.get('SellableQtyPrice')),
                            'Total_Pack_Taxable_Amount': safe_decimal(item.get('TotalPackTaxableAmount')),
                            'Total_Pack_Tax_Amount': safe_decimal(item.get('TotalTaxAmount')),
                            'Total_Pack_Amount_with_tax': safe_decimal(item.get('TotalPackAmount')),
                            'Batch_No': item.get('BatchNo'),
                            'Is_Manufacture_Date_Available': item.get('IsManufactureDateAvailable'),
                            'Manufacture_Date': parse_date(item.get('ManufactureDate')),
                            'Is_Expiry_Date_Available': item.get('IsExpiryDateAvailable'),
                            'Expiry_Date': parse_date(item.get('ExpiryDate')),
                            'Discount_Method': item.get('DiscountMethod'),
                            'Discount_Type': item.get('DiscountType'),
                            'Discount_Amount': safe_decimal(item.get('Discount')),
                            'Final_Total_Pack_Taxable_Amount': safe_decimal(item.get('FinalTotalPackTaxableAmount')),
                            'Final_Total_Pack_Tax_Amount': safe_decimal(item.get('FinalTotalTaxAmount')),
                            'Final_Total_Pack_Amount_with_tax': safe_decimal(item.get('FinalTotalPackAmount')),
                            'Status': approval_status,
                            'Created_by': Created_by,
                        }
                    )

                    # Keep track of updated items
                    updated_item_ids.add(item_instance.id)

                # Remove GRN items not in the updated list
                # items_to_remove = existing_item_ids - updated_item_ids
                # GRN_Product_Item_Detials.objects.filter(Grn_Detials=GRN_Table_Ins if GRNNumber else GRN_Inst, Product_Detials__in=items_to_remove).delete()

                
                for POitem in POItemArrays:
                        Purchase_Order_Item_instance = Purchase_Order_Item_Details.objects.get(pk=POitem['id'])
                        
                        received_qty = int(POitem['Received_Qty'])
                        order_qty = int(Purchase_Order_Item_instance.PO_Order_Qty)
                        item_status = POitem['Item_Status']
                        reason = POitem['Reason']

                        # print('------',received_qty,order_qty,item_status,reason)

                        if received_qty == 0 and item_status == "Waiting For GRN":
                            Purchase_Order_Item_instance.Item_Status = 'Waiting For GRN'
                            Purchase_Order_Item_instance.Reason = reason
                            Purchase_Order_Item_instance.save()

                        elif received_qty == 0 and item_status != "Waiting For GRN":
                            Purchase_Order_Item_instance.Item_Status = 'Canceled'
                            Purchase_Order_Item_instance.Reason = reason
                            Purchase_Order_Item_instance.save()

                        elif order_qty == received_qty or order_qty < received_qty:
                            Purchase_Order_Item_instance.Received_Qty = received_qty
                            Purchase_Order_Item_instance.Balance_Qty = 0
                            Purchase_Order_Item_instance.Item_Status = 'GRN Completed'
                            Purchase_Order_Item_instance.Reason = 'GRN Completed'
                            Purchase_Order_Item_instance.save()

                        elif order_qty > received_qty > 0 and item_status == "Waiting For GRN":
                            Purchase_Order_Item_instance.Received_Qty = received_qty
                            Purchase_Order_Item_instance.Balance_Qty = order_qty - received_qty
                            Purchase_Order_Item_instance.Item_Status = 'Waiting For GRN'
                            Purchase_Order_Item_instance.Reason = reason
                            Purchase_Order_Item_instance.save()

                        elif order_qty > received_qty > 0 and item_status != "Waiting For GRN":
                            Purchase_Order_Item_instance.Received_Qty = received_qty
                            Purchase_Order_Item_instance.Balance_Qty = order_qty - received_qty
                            Purchase_Order_Item_instance.Item_Status = 'GRN Completed'
                            Purchase_Order_Item_instance.Reason = reason
                            Purchase_Order_Item_instance.save()

                        if Purchase_Order_Item_Details.objects.filter(PurchaseOrder=Purchase_Order_inst, Item_Status='Waiting For GRN').exists():
                            Purchase_Order_inst.PO_Status ='Waiting For GRN'
                        else:
                            Purchase_Order_inst.PO_Status ='GRN Compleated'
                        
                        Purchase_Order_inst.save() 

            

            return JsonResponse({'success': 'GRN details processed successfully'}, status=200)

        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)



# --------------------------------GRN Edit get---------------------

@csrf_exempt
@require_http_methods(["GET"])
def PO_Goods_Reciept_Note_GET_Details_link(request):
    if request.method == "GET":
        try:
            GRN_Number=request.GET.get('GRN_Number')
            
            print('GRN_Number',GRN_Number)


            if GRN_Number:
                grn_table_instance = GRN_Table_Detials.objects.get(pk=GRN_Number)

                Purchase_order_Num =grn_table_instance.Purchase_order_Detials.pk if grn_table_instance.Purchase_order_Detials else None
            
                dic={
                    'id':grn_table_instance.pk,
                    'GrnDate':grn_table_instance.GrnDate,
                    'Purchase_order_Detials':Purchase_order_Num,
                    'SupplierCode':grn_table_instance.Supplier_Detials.pk,
                    'SupplierName':grn_table_instance.Supplier_Detials.Supplier_Name,
                    'ContactPerson':grn_table_instance.Supplier_Detials.Contact_Person,
                    'ContactNumber':grn_table_instance.Supplier_Detials.Contact_Number,
                    'EmailAddress':grn_table_instance.Supplier_Detials.Email_Address,
                    'Supplier_Bill_Number':grn_table_instance.Supplier_Bill_Number,
                    'Supplier_Bill_Date':grn_table_instance.Supplier_Bill_Date,
                    'Supplier_Bill_Due_Date':grn_table_instance.Supplier_Bill_Due_Date,
                    'Supplier_Bill_Amount':grn_table_instance.Supplier_Bill_Amount,                    
                    'GRNLocation':grn_table_instance.Store_location.Location_Name.pk,
                    'Store_location_pk':grn_table_instance.Store_location.pk,
                    'Received_person':grn_table_instance.Received_person,
                    'Is_Foc_Available':grn_table_instance.Is_Foc_Available,
                    'Foc_Method':grn_table_instance.Foc_Method,
                    'FileAttachment':get_file_image(grn_table_instance.File_Attachment) if grn_table_instance.File_Attachment else None,
                    'Taxable_Amount':grn_table_instance.Taxable_Amount,
                    'Tax_Amount':grn_table_instance.Tax_Amount,
                    'Total_Amount':grn_table_instance.Total_Amount,
                    'Total_Discount_Method':grn_table_instance.Total_Discount_Method,
                    'Total_Discount_Type':grn_table_instance.Total_Discount_Type,
                    'Discount_Amount':grn_table_instance.Discount_Amount,
                    'Final_Taxable_Amount':grn_table_instance.Final_Taxable_Amount,
                    'Final_Tax_Amount':grn_table_instance.Final_Tax_Amount,
                    'Final_Total_Amount':grn_table_instance.Final_Total_Amount,
                    'Round_off_Amount':grn_table_instance.Round_off_Amount,
                    'Net_Amount':grn_table_instance.Net_Amount,
                    'GRN_Items':[],
                    'PO_Items':[],
                }
                
                for items in GRN_Product_Item_Detials.objects.filter(Grn_Detials = grn_table_instance.pk):
                    
                    item_dic = {
                        'id':items.pk,
                        'NotInPurchaseOrder':items.Not_In_PO_Product,
                        'ItemCode':items.Product_Detials.pk,
                        'ItemName':items.Product_Detials.ItemName,
                        'IsFOCProduct':items.Is_Foc_Product,
                        'FOCItemCode':items.Foc_Product_Detials.pk if items.Foc_Product_Detials else '',
                        'FOCItemName':items.Foc_Product_Detials.ItemName if items.Foc_Product_Detials else '',
                        'GRNMRP':items.Purchase_MRP,
                        'PurchaseRateTaxable':items.Purchase_rate_taxable,
                        'TaxType':items.Tax_Type,
                        'TaxPercentage':items.Tax_Percentage,
                        'PurchaseRateWithTax':items.Purchase_rate_with_tax,
                        'OrderQty':'',
                        'ReceivedQty':items.Received_Quantity,
                        'PendingQty':'',
                        'ExtraQty':items.Extra_PO_Quantity,
                        'IsFOCQtyAvailable':True if items.FOC_Quantity else False,
                        'FOCQty':items.FOC_Quantity if items.FOC_Quantity else "",
                        'TotalPackQty':items.Total_Pack_Quantity,
                        'IsMRPAsSellablePrice':items.Is_MRP_as_sellable_price,
                        'SellablePrice':items.Sellable_price,
                        'SellableQtyPrice':items.Sellable_qty_price,
                        'TotalPackTaxableAmount':items.Total_Pack_Taxable_Amount,
                        'TotalTaxAmount':items.Total_Pack_Tax_Amount,
                        'TotalPackAmount':items.Total_Pack_Amount_with_tax,
                        'BatchNo':items.Batch_No,
                        'IsManufactureDateAvailable':items.Is_Manufacture_Date_Available,
                        'ManufactureDate':items.Manufacture_Date,
                        'IsExpiryDateAvailable':items.Is_Expiry_Date_Available,
                        'ExpiryDate':items.Expiry_Date,
                        'DiscountMethod':items.Discount_Method,
                        'DiscountType':items.Discount_Type,
                        'Discount':items.Discount_Amount,
                        'FinalTotalPackTaxableAmount':items.Final_Total_Pack_Taxable_Amount,
                        'FinalTotalTaxAmount':items.Final_Total_Pack_Tax_Amount,
                        'FinalTotalPackAmount':items.Final_Total_Pack_Amount_with_tax,
                    }

                    if Purchase_Order_Item_Details.objects.filter(PurchaseOrder__pk = Purchase_order_Num,PO_Item_Detailes__Product_Detials=items.Product_Detials).exists() :
                        PO_Item_ins=Purchase_Order_Item_Details.objects.get(PurchaseOrder__pk = Purchase_order_Num,PO_Item_Detailes__Product_Detials=items.Product_Detials)

                        item_dic['OrderQty']=PO_Item_ins.PO_Order_Qty
                        item_dic['PendingQty']=PO_Item_ins.Balance_Qty

                    
                    dic['GRN_Items'].append(item_dic)


                for POitems in Purchase_Order_Item_Details.objects.filter(PurchaseOrder = Purchase_order_Num):
                    # print('POitems-------',POitems)
                    Get_Rate_Inst = Supplier_Product_Amount_Details.objects.filter(Supplier_detials__Supplier_Detials__pk=grn_table_instance.Supplier_Detials.pk, Supplier_detials__Product_Detials=POitems.PO_Item_Detailes.Product_Detials.pk).order_by('-Created_at').first()


                    PO_item_dic = {
                        'id': POitems.PO_Item_Number,
                        'ItemCode': POitems.PO_Item_Detailes.Product_Detials.pk,
                        'ItemName': POitems.PO_Item_Detailes.Product_Detials.ItemName,
                        'ProductCategory': POitems.PO_Item_Detailes.Product_Detials.ProductCategory.ProductCategory_Name,
                        'SubCategory': POitems.PO_Item_Detailes.Product_Detials.SubCategory.SubCategoryName,
                        }
                    if POitems.PO_Item_Detailes.Product_Detials.GenericName :                     
                        PO_item_dic['GenericName'] = POitems.PO_Item_Detailes.Product_Detials.GenericName.GenericName
                    if POitems.PO_Item_Detailes.Product_Detials.CompanyName :
                        PO_item_dic['ManufacturerName'] = POitems.PO_Item_Detailes.Product_Detials.CompanyName.CompanyName
                    if POitems.PO_Item_Detailes.Product_Detials.HSNCode :
                        PO_item_dic['HSNCode'] = POitems.PO_Item_Detailes.Product_Detials.HSNCode
                    if POitems.PO_Item_Detailes.Product_Detials.Strength :
                        PO_item_dic['Strength'] = POitems.PO_Item_Detailes.Product_Detials.Strength
                    if POitems.PO_Item_Detailes.Product_Detials.StrengthType :
                        PO_item_dic['StrengthType'] = POitems.PO_Item_Detailes.Product_Detials.StrengthType
                    if POitems.PO_Item_Detailes.Product_Detials.Volume :
                        PO_item_dic['Volume'] = POitems.PO_Item_Detailes.Product_Detials.Volume
                    if POitems.PO_Item_Detailes.Product_Detials.VolumeType :
                        PO_item_dic['VolumeType'] = POitems.PO_Item_Detailes.Product_Detials.VolumeType.Unit_Name                   
                    if POitems.PO_Item_Detailes.Product_Detials.PackType :
                        PO_item_dic['PackType'] = POitems.PO_Item_Detailes.Product_Detials.PackType.PackType_Name
                    if POitems.PO_Item_Detailes.Product_Detials.PackQty :
                        PO_item_dic['PackQty']= POitems.PO_Item_Detailes.Product_Detials.PackQty
                    
                    if POitems.PO_Item_Detailes.Product_Detials.Is_Manufacture_Date_Available :
                        PO_item_dic['Is_Manufacture_Date_Available']= POitems.PO_Item_Detailes.Product_Detials.Is_Manufacture_Date_Available
                    if POitems.PO_Item_Detailes.Product_Detials.Is_Expiry_Date_Available :
                        PO_item_dic['Is_Expiry_Date_Available']= POitems.PO_Item_Detailes.Product_Detials.Is_Expiry_Date_Available
                    
                    if POitems.PO_Item_Detailes.Product_Detials.IsSellable is not None : 
                         PO_item_dic['IsSellable']='Yes' if POitems.PO_Item_Detailes.Product_Detials.IsSellable else 'No'
                         if PO_item_dic['IsSellable'] == 'Yes':                         
                            PO_item_dic['LeastSellableUnit']=POitems.PO_Item_Detailes.Product_Detials.LeastSellableUnit

                    
                    PO_item_dic['MRP']= Get_Rate_Inst.MRP
                    PO_item_dic['PurchaseRateBeforeGST']= Get_Rate_Inst.PurchaseRateBeforeGST
                    PO_item_dic['GST']=  Get_Rate_Inst.GST
                    PO_item_dic['PurchaseRateAfterGST']=Get_Rate_Inst.PurchaseRateAfterGST
                    
                        
                    PO_item_dic['PurchaseQty']= POitems.PO_Order_Qty
                    PO_item_dic['TotalAmount'] = POitems.TotalAmount
                    PO_item_dic['Item_Status']= POitems.Item_Status
                    PO_item_dic['Reason']= POitems.Reason                              
                    PO_item_dic['Received_Qty']=POitems.Received_Qty
                    PO_item_dic['Balance_Qty']=POitems.Balance_Qty

                    dic['PO_Items'].append(PO_item_dic)


            return JsonResponse (dic,safe=False)


        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)






@csrf_exempt
@require_http_methods(["POST", "OPTIONS","GET"])
def Old_Goods_Reciept_Note_stock_supplier_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            InvoiceNo = data.get('pk')
            supplierdata = data.get('supplierdata', [])
            stockdata = data.get('stockdata', [])
            Created_by = data.get('Created_by', '')
            print(data)
            
            if not InvoiceNo:
                return JsonResponse({'error': 'InvoiceNo is required'}, status=400)

            try:
                # Fetch the GRN and Supplier payment details
                grn_table_ins = GRN_Table_Detials.objects.get(pk=InvoiceNo)
                supp_pay_ins = Supplier_pay_detials.objects.get(Grn_Detials__pk=InvoiceNo)
                if not grn_table_ins.OldGRN_Updated:
                    grn_table_ins.OldGRN_Updated = True
                    grn_table_ins.save()
                    
                GRN_Invoice_Amount = grn_table_ins.Net_Amount
                GRN_Paid_Amount = 0  # Initialize paid amount
                GRN_Balance_Amount = GRN_Invoice_Amount  # Start with full balance

                with transaction.atomic():  # Ensure atomic operations for DB changes
                    # Process supplier payment data
                    for supp in supplierdata:
                        PaymentDate = supp.get('PaymentDate')
                        PaymentAmount = supp.get('PaymentAmount', 0)
                        PaymentMethod = supp.get('PaymentMethod')
                        PaymentDetials = supp.get('PaymentDetials')
                        PaymentBy = supp.get('PaymentBy')

                        if not PaymentAmount:
                            return JsonResponse({'error': 'PaymentAmount is required'}, status=400)

                        Supplier_Pay_By_Date.objects.create(
                            Supplier_pay_detials=supp_pay_ins,
                            GRN_Invoice_Amount=GRN_Invoice_Amount,
                            GRN_Paid_Amount=GRN_Paid_Amount,
                            GRN_Balance_Amount=GRN_Balance_Amount,
                            Paid_Amount=PaymentAmount,
                            Balance_Amount=GRN_Balance_Amount - PaymentAmount,
                            Bill_Paid_Date=PaymentDate,
                            Payment_Method=PaymentMethod,
                            Payment_Detials=PaymentDetials,
                            NewPayment=False,
                            Created_by=PaymentBy,
                        )
                        GRN_Paid_Amount += PaymentAmount
                        GRN_Balance_Amount -= PaymentAmount

                    # Process stock data
                    for item in stockdata:
                        item_pk = item.get('pk')
                        IsFromWardStore = item.get('IsFromWardStore')
                        StoreLocation = item.get('StoreLocation')
                        TotalPackQuantity = item.get('TotalPackQuantity', 0)

                        Grn_Detials_item_ins = get_or_none(GRN_Product_Item_Detials, item_pk)
                        if not Grn_Detials_item_ins:
                            return JsonResponse({'error': f'Stock item {item_pk} not found'}, status=404)

                        Store_location_ins = None
                        Ward_Store_location_ins = None

                        if IsFromWardStore:
                            Ward_Store_location_ins = get_or_none(NurseStationMaster, StoreLocation)
                        else:
                            Store_location_ins = get_or_none(Inventory_Location_Master_Detials, StoreLocation)

                        Old_Grn_stock_detials.objects.create(
                            Grn_Detials=Grn_Detials_item_ins,
                            IsNurseStation=IsFromWardStore,
                            Store_location=Store_location_ins,
                            NurseStation_location=Ward_Store_location_ins,
                            TotalPackQuantity=TotalPackQuantity,
                            Created_by=Created_by,
                            
                        )

                return JsonResponse({'success': 'GRN and related data processed successfully'}, status=200)

            except GRN_Table_Detials.DoesNotExist:
                return JsonResponse({'error': 'Invoice not found'}, status=404)
            except Supplier_pay_detials.DoesNotExist:
                return JsonResponse({'error': 'Supplier payment details not found for this invoice'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
    elif request.method == 'GET':
        try:
            
            SupplierCode = request.GET.get('SupplierCode')
            SupplierName = request.GET.get('SupplierName')
            InvoiceNo = request.GET.get('InvoiceNo')
            DateType = request.GET.get('DateType')
            CurrentDate = request.GET.get('CurrentDate')
            FromDate = request.GET.get('FromDate')
            ToDate = request.GET.get('ToDate')
            BillingLocation = request.GET.get('BillingLocation')
            Status = request.GET.get('Status')
            
            query = Q()
            
            if DateType == "Current":
                # Filter by CurrentDate (expecting 'YYYY-MM-DD' format)
                if CurrentDate:
                    query &= Q(GrnDate=CurrentDate)
            elif DateType == "Customize":
                # Filter by date range (FromDate and ToDate)
                if FromDate and ToDate:
                    query &= Q(GrnDate__range=[FromDate, ToDate])
                elif FromDate:
                    query &= Q(GrnDate__gte=FromDate)
                elif ToDate:
                    query &= Q(GrnDate__lte=ToDate)
            if SupplierCode:
                query &= Q(Supplier_Detials__pk__icontains=SupplierCode)
            if SupplierName:
                query &= Q(Supplier_Detials__Supplier_Name__icontains=SupplierName)
                
            if BillingLocation:
                query &= Q(Store_location__Location_Name__pk=BillingLocation)
         
            if Status:
                if Status == 'Pending':
                    query &=Q(OldGRN_Updated = False)   
                else:
                    query &=Q(OldGRN_Updated = True) 
                    
            grn_table_instance = GRN_Table_Detials.objects.filter(Status ='Approved',IsQuickGRN=True,IsOldGRN = True).filter(query)
            grn_table_data=[]
            for grn in grn_table_instance:
                dic={
                    'id':len(grn_table_data) + 1,
                    'pk':grn.pk,
                    'IsQuickGRN':grn.IsQuickGRN,
                    'IsOldGRN':grn.IsOldGRN,
                    'OldGRN_Updated':grn.OldGRN_Updated,
                    'GrnDate':grn.GrnDate,
                    'Purchase_order_Detials':grn.Purchase_order_Detials.pk if grn.Purchase_order_Detials else None,
                    'SupplierCode':grn.Supplier_Detials.pk,
                    'SupplierName':grn.Supplier_Detials.Supplier_Name,
                    'ContactPerson':grn.Supplier_Detials.Contact_Person,
                    'ContactNumber':grn.Supplier_Detials.Contact_Number,
                    'EmailAddress':grn.Supplier_Detials.Email_Address,
                    'Supplier_Bill_Number':grn.Supplier_Bill_Number,
                    'Supplier_Bill_Date':grn.Supplier_Bill_Date,
                    'Supplier_Bill_Due_Date':grn.Supplier_Bill_Due_Date,
                    'Supplier_Bill_Amount':grn.Supplier_Bill_Amount,
                    'Store_location_pk':grn.Store_location.pk,
                    'Store_location':grn.Store_location.Store_Name,
                    'Received_person':grn.Received_person,
                    'Is_Foc_Available':grn.Is_Foc_Available,
                    'Foc_Method':grn.Foc_Method,
                    'FileAttachment':get_file_image(grn.File_Attachment) if grn.File_Attachment else None,
                    'Taxable_Amount':grn.Taxable_Amount,
                    'Tax_Amount':grn.Tax_Amount,
                    'Total_Amount':grn.Total_Amount,
                    'Total_Discount_Method':grn.Total_Discount_Method,
                    'Total_Discount_Type':grn.Total_Discount_Type,
                    'Discount_Amount':grn.Discount_Amount,
                    'Final_Taxable_Amount':grn.Final_Taxable_Amount,
                    'Final_Tax_Amount':grn.Final_Tax_Amount,
                    'Final_Total_Amount':grn.Final_Total_Amount,
                    'Round_off_Amount':grn.Round_off_Amount,
                    'Net_Amount':grn.Net_Amount,
                    'Status':grn.Status,
                    'Supplier_Payment':[],
                    'GRN_Items':[]
                }
                #  for supplier payment
                supplier_payments_ins = Supplier_Pay_By_Date.objects.filter(Supplier_pay_detials__Grn_Detials__pk = grn.pk,NewPayment =False)
                print(supplier_payments_ins)
                if supplier_payments_ins.exists():
                    for indx,ins in enumerate(supplier_payments_ins):
                        supp_data = {
                            "id": indx + 1,
                            "SupplierCode": ins.Supplier_pay_detials.Grn_Detials.Supplier_Detials.pk,
                            "SupplierName": ins.Supplier_pay_detials.Grn_Detials.Supplier_Detials.Supplier_Name,
                            "GRN_Invoice_No": ins.Supplier_pay_detials.Grn_Detials.pk,
                            "GRN_Invoice_Date": ins.Supplier_pay_detials.Grn_Detials.Created_at.strftime('%Y-%m-%d'),
                            "Supplier_Bill_Date": ins.Supplier_pay_detials.Grn_Detials.Supplier_Bill_Date,
                            "GRN_Due_Date": ins.Supplier_pay_detials.Grn_Detials.Supplier_Bill_Due_Date,
                            "GRN_Invoice_Amount": ins.GRN_Invoice_Amount,
                            "GRN_Paid_Amount": ins.GRN_Paid_Amount,
                            "GRN_Balance_Amount": ins.GRN_Balance_Amount,
                            "Paid_Amount": ins.Paid_Amount,
                            "Balance_Amount": ins.Balance_Amount,
                            "Bill_Paid_Date": ins.Bill_Paid_Date,
                            "Payment_Method": ins.Payment_Method,
                            "Payment_Detials": ins.Payment_Detials,
                            "Payment_By": ins.Created_by,
                        }
                        dic['Supplier_Payment'].append(supp_data)
                # for grn items
                for items in GRN_Product_Item_Detials.objects.filter(Grn_Detials = grn.pk):
                    if not grn.OldGRN_Updated:
                        item_dic={
                            'id' :len(dic['GRN_Items']) +1,
                            'pk':items.pk,
                            'ItemCode':items.Product_Detials.pk,
                            'ItemName':items.Product_Detials.ItemName,
                            'ProductCategory':items.Product_Detials.ProductCategory.ProductCategory_Name,
                            'SubCategory':items.Product_Detials.SubCategory.SubCategoryName,
                            'PackType':items.Product_Detials.PackType.PackType_Name if items.Product_Detials.PackType else "",
                            'PackQuantity':items.Product_Detials.PackQty,
                            'TotalReceivedQty':items.Total_Received_Quantity,
                            'TotalPackQuantity':items.Total_Pack_Quantity,
                            'BatchNo':items.Batch_No,
                            'Location' :'Nill',
                            'IsNurseStation' :'Nill',
                            'Store_location':'Nill',
                            'Store_Stock' : 0
                        }
                    else:
                        
                        item_dic={
                            'id' :len(dic['GRN_Items']) +1,
                            'pk':items.pk,
                            'ItemCode':items.Product_Detials.pk,
                            'ItemName':items.Product_Detials.ItemName,
                            'ProductCategory':items.Product_Detials.ProductCategory.ProductCategory_Name,
                            'SubCategory':items.Product_Detials.SubCategory.SubCategoryName,
                            'PackType':items.Product_Detials.PackType.PackType_Name if items.Product_Detials.PackType else "",
                            'PackQuantity':items.Product_Detials.PackQty,
                            'TotalReceivedQty':items.Total_Received_Quantity,
                            'TotalPackQuantity':items.Total_Pack_Quantity,
                            'BatchNo':items.Batch_No,
                        }
                        updateddata = Old_Grn_stock_detials.objects.filter(Grn_Detials__pk = items.pk)
                        if updateddata.exists():
                            
                            item_dic['IsNurseStation'] = updateddata[0].IsNurseStation
                            if updateddata[0].IsNurseStation:  
                                item_dic['Location'] = updateddata[0].NurseStation_location.Location_Name.Location_Name
                                item_dic['Store_location'] = updateddata[0].NurseStation_location.NurseStationName
                                item_dic['Store_Stock'] = updateddata[0].TotalPackQuantity
                            else:
                                item_dic['Location'] = updateddata[0].Store_location.Location_Name.Location_Name
                                item_dic['Store_location'] = updateddata[0].Store_location.Store_Name
                                item_dic['Store_Stock'] = updateddata[0].TotalPackQuantity
                        else:
                            item_dic['Location'] = 'Nill'
                            item_dic['IsNurseStation'] = 'Nill'
                            item_dic['Store_location'] = 'Nill'
                            item_dic['Store_Stock'] = 0
                            
                   
                    dic['GRN_Items'].append(item_dic)
                    
                   
                    
                grn_table_data.append(dic)
            return JsonResponse (grn_table_data,safe=False)
         
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
        
    else:
        return JsonResponse({'error': 'Request method not allowed'}, status=405)
 
@csrf_exempt
@require_http_methods(["GET"])
def get_overall_stock_list_details(request):
    if request.method == "GET":
        try:
            # Get parameters from request
            FilterType = request.GET.get('FilterType')
            ItemCode = request.GET.get('ItemCode')
            ItemName = request.GET.get('ItemName')
            ProductCategory = request.GET.get('ProductCategory')
            SubCategory = request.GET.get('SubCategory')
            Location = request.GET.get('Location')
            IsWardStore = request.GET.get('StoreType','').lower()  
            Store_location = request.GET.get('StoreName')
 
            # Product filter conditions
            product_filter_conditions = Q()
            if ItemCode:
                product_filter_conditions &= Q(pk__icontains=ItemCode)
            if ItemName:
                product_filter_conditions &= Q(ItemName__icontains=ItemName)
            if ProductCategory:
                product_filter_conditions &= Q(ProductCategory__pk=ProductCategory)
            if SubCategory:
                product_filter_conditions &= Q(SubCategory__pk=SubCategory)
            inv_loc_filter_condition =Q(Status=True)
            NurseStation_loc_filter_condition =Q(Status=True)
            if FilterType != 'OverAll':
             
                if Location:
                    inv_loc_filter_condition &= Q(Location_Name__pk__iexact = Location)
                    NurseStation_loc_filter_condition &= Q(Location_Name__pk__iexact = Location)
                   
                    if IsWardStore == 'NurseStation':
                        if Store_location:
                            NurseStation_loc_filter_condition &= Q(pk = Store_location)
                    elif IsWardStore == "inventory":
                        if Store_location:
                         
                            inv_loc_filter_condition &= Q(pk = Store_location)
               
           
 
            # Query the products and locations
            Product_details_ins = Product_Master_All_Category_Details.objects.filter(product_filter_conditions)
            Inv_Location_details_ins = Inventory_Location_Master_Detials.objects.filter(inv_loc_filter_condition)
            NurseStation_loc_Location_details_ins = NurseStationMaster.objects.filter(NurseStation_loc_filter_condition)

            print('7777------',FilterType)

            stock_data_list = []
 
            # Iterate over product details
            for Product in Product_details_ins:
                if FilterType == 'OverAll':

                    pro_dic = {
                        "id":len(stock_data_list) +1,
                        "ItemCode": Product.pk,
                        "ItemName": Product.ItemName,
                        "ProductCategory": Product.ProductCategory.ProductCategory_Name if Product.ProductCategory else None,
                        "SubCategory": Product.SubCategory.SubCategoryName if Product.SubCategory else None,
                    }
 
                # Inventory stores
                for inv in Inv_Location_details_ins:
                    stock_list_ins = Stock_Maintance_Table_Detials.objects.filter(
                        Product_Detials__pk=Product.pk,
                        IsNurseStation=False,
                        Store_location=inv.pk
                    ).aggregate(
                        total_quantity=Coalesce(Sum('Total_Quantity'), Value(0)),
                        grn_recieve_quantity=Coalesce(Sum('Grn_Recieve_Quantity'), Value(0)),
                        indent_send_quantity=Coalesce(Sum('Indent_Send_Quantity'), Value(0)),
                        indent_recieve_quantity=Coalesce(Sum('Indent_Recieve_Quantity'), Value(0)),
                        indent_return_quantity=Coalesce(Sum('Indent_Return_Quantity'), Value(0)),
                        grn_return_quantity=Coalesce(Sum('Grn_Return_Quantity'), Value(0)),
                        scrab_quantity=Coalesce(Sum('Scrab_Quantity'), Value(0)),
                        sold_quantity=Coalesce(Sum('Sold_Quantity'), Value(0)),
                        available_quantity=Coalesce(Sum('AvailableQuantity'), Value(0))
                    )
                    if  FilterType != 'OverAll':
                        inv_dic = {
                            "ItemCode": Product.pk,
                            "ItemName": Product.ItemName,
                            "ProductCategory": Product.ProductCategory.ProductCategory_Name if Product.ProductCategory else None,
                            "SubCategory": Product.SubCategory.SubCategoryName if Product.SubCategory else None,
                            'LocationId': inv.Location_Name.pk,
                            'Location': inv.Location_Name.Location_Name,
                            'StoreType': 'Inventory Store',
                            'StoreId': inv.pk,
                            'StoreName': inv.Store_Name,
                            'Total_Quantity': stock_list_ins.get('total_quantity',0) if stock_list_ins else 0,
                            'Grn_Recieve_Quantity': stock_list_ins.get('grn_recieve_quantity',0) if stock_list_ins else 0,
                            'Indent_Send_Quantity': stock_list_ins.get('indent_send_quantity',0) if stock_list_ins else 0,
                            'Indent_Recieve_Quantity': stock_list_ins.get('indent_recieve_quantity',0) if stock_list_ins else 0,
                            'Indent_Return_Quantity': stock_list_ins.get('indent_return_quantity',0) if stock_list_ins else 0,
                            'Grn_Return_Quantity': stock_list_ins.get('grn_return_quantity',0) if stock_list_ins else 0,
                            'Scrab_Quantity': stock_list_ins.get('scrab_quantity',0) if stock_list_ins else 0,
                            'Sold_Quantity': stock_list_ins.get('sold_quantity',0) if stock_list_ins else 0,
                            'AvailableQuantity': stock_list_ins.get('available_quantity',0) if stock_list_ins else 0,
                        }
                        if IsWardStore != 'NurseStation':
                            stock_data_list.append(inv_dic)
                    else:
                        location_dat = inv.Location_Name
                       
                        pro_dic[f'{location_dat.pk}_inv_{inv.pk}_Total_Quantity'] = stock_list_ins.get('total_quantity',0) if stock_list_ins else 0
                        pro_dic[f'{location_dat.pk}_inv_{inv.pk}_Grn_Recieve_Quantity'] = stock_list_ins.get('grn_recieve_quantity',0) if stock_list_ins else 0
                        pro_dic[f'{location_dat.pk}_inv_{inv.pk}_Indent_Send_Quantity'] = stock_list_ins.get('indent_send_quantity',0) if stock_list_ins else 0
                        pro_dic[f'{location_dat.pk}_inv_{inv.pk}_Indent_Recieve_Quantity'] = stock_list_ins.get('indent_recieve_quantity',0) if stock_list_ins else 0
                        pro_dic[f'{location_dat.pk}_inv_{inv.pk}_Indent_Return_Quantity'] = stock_list_ins.get('indent_return_quantity',0) if stock_list_ins else 0
                        pro_dic[f'{location_dat.pk}_inv_{inv.pk}_Grn_Return_Quantity'] = stock_list_ins.get('grn_return_quantity',0) if stock_list_ins else 0
                        pro_dic[f'{location_dat.pk}_inv_{inv.pk}_Scrab_Quantity'] = stock_list_ins.get('scrab_quantity',0) if stock_list_ins else 0
                        pro_dic[f'{location_dat.pk}_inv_{inv.pk}_Sold_Quantity'] = stock_list_ins.get('sold_quantity',0) if stock_list_ins else 0
                        pro_dic[f'{location_dat.pk}_inv_{inv.pk}_AvailableQuantity'] = stock_list_ins.get('available_quantity',0) if stock_list_ins else 0
 
                # Ward stores


                for Nurse in NurseStation_loc_Location_details_ins:
                    stock_list_ins = Stock_Maintance_Table_Detials.objects.filter(
                        Product_Detials__pk=Product.pk,
                        IsNurseStation=True,
                        NurseStation_location=Nurse.pk
                    ).aggregate(
                        total_quantity=Coalesce(Sum('Total_Quantity'), Value(0)),
                        grn_recieve_quantity=Coalesce(Sum('Grn_Recieve_Quantity'), Value(0)),
                        indent_send_quantity=Coalesce(Sum('Indent_Send_Quantity'), Value(0)),
                        indent_recieve_quantity=Coalesce(Sum('Indent_Recieve_Quantity'), Value(0)),
                        indent_return_quantity=Coalesce(Sum('Indent_Return_Quantity'), Value(0)),
                        grn_return_quantity=Coalesce(Sum('Grn_Return_Quantity'), Value(0)),
                        scrab_quantity=Coalesce(Sum('Scrab_Quantity'), Value(0)),
                        sold_quantity=Coalesce(Sum('Sold_Quantity'), Value(0)),
                        available_quantity=Coalesce(Sum('AvailableQuantity'), Value(0))
                    )
                    if  FilterType != 'OverAll':
                        ward_dic = {
                            "ItemCode": Product.pk,
                            "ItemName": Product.ItemName,
                            "ProductCategory": Product.ProductCategory.ProductCategory_Name if Product.ProductCategory else None,
                            "SubCategory": Product.SubCategory.SubCategoryName if Product.SubCategory else None,
                            'LocationId': Nurse.Location_Name.pk,
                            'Location': Nurse.Location_Name.Location_Name,
                            'StoreType': 'Nurse Station Store',
                            'StoreId': Nurse.pk,
                            'StoreName': Nurse.NurseStationName,
                            'Total_Quantity': stock_list_ins.get('total_quantity',0) if stock_list_ins else 0,
                            'Grn_Recieve_Quantity': stock_list_ins.get('grn_recieve_quantity',0) if stock_list_ins else 0,
                            'Indent_Send_Quantity': stock_list_ins.get('indent_send_quantity',0) if stock_list_ins else 0,
                            'Indent_Recieve_Quantity': stock_list_ins.get('indent_recieve_quantity',0) if stock_list_ins else 0,
                            'Indent_Return_Quantity': stock_list_ins.get('indent_return_quantity',0) if stock_list_ins else 0,
                            'Grn_Return_Quantity': stock_list_ins.get('grn_return_quantity',0) if stock_list_ins else 0,
                            'Scrab_Quantity': stock_list_ins.get('scrab_quantity',0) if stock_list_ins else 0,
                            'Sold_Quantity': stock_list_ins.get('sold_quantity',0) if stock_list_ins else 0,
                            'AvailableQuantity': stock_list_ins.get('available_quantity',0) if stock_list_ins else 0,
                        }
                        if IsWardStore != 'inventory':
                            stock_data_list.append(ward_dic)
                    else:
                        location_dat = Nurse.Location_Name  # Should be ward.Location_Name here
                       
                        pro_dic[f'{location_dat.pk}_Nurse_{Nurse.pk}_Total_Quantity'] = stock_list_ins.get('total_quantity',0) if stock_list_ins else 0
                        pro_dic[f'{location_dat.pk}_Nurse_{Nurse.pk}_Grn_Recieve_Quantity'] = stock_list_ins.get('grn_recieve_quantity',0) if stock_list_ins else 0
                        pro_dic[f'{location_dat.pk}_Nurse_{Nurse.pk}_Indent_Send_Quantity'] = stock_list_ins.get('indent_send_quantity',0) if stock_list_ins else 0
                        pro_dic[f'{location_dat.pk}_Nurse_{Nurse.pk}_Indent_Recieve_Quantity'] = stock_list_ins.get('indent_recieve_quantity',0) if stock_list_ins else 0
                        pro_dic[f'{location_dat.pk}_Nurse_{Nurse.pk}_Indent_Return_Quantity'] = stock_list_ins.get('indent_return_quantity',0) if stock_list_ins else 0
                        pro_dic[f'{location_dat.pk}_Nurse_{Nurse.pk}_Grn_Return_Quantity'] = stock_list_ins.get('grn_return_quantity',0) if stock_list_ins else 0
                        pro_dic[f'{location_dat.pk}_Nurse_{Nurse.pk}_Scrab_Quantity'] = stock_list_ins.get('scrab_quantity',0) if stock_list_ins else 0
                        pro_dic[f'{location_dat.pk}_Nurse_{Nurse.pk}_Sold_Quantity'] = stock_list_ins.get('sold_quantity',0) if stock_list_ins else 0
                        pro_dic[f'{location_dat.pk}_Nurse_{Nurse.pk}_AvailableQuantity'] = stock_list_ins.get('available_quantity',0) if stock_list_ins else 0
               
               
               
                if  FilterType == 'OverAll':
                    stock_data_list.append(pro_dic)
 
            return JsonResponse(stock_data_list, safe=False)
 
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
 
    else:
        return JsonResponse({'error': 'Request method not allowed'}, status=405)
 
@csrf_exempt
@require_http_methods(["GET"])
def get_overall_stock_list_By_batchwise_details(request):
    if request.method == "GET":
        try:
            ItemCode = request.GET.get('ItemCode')
            StoreType = request.GET.get('StoreType')
            StoreName = request.GET.get('StoreName')
            filter_query=Q()
            if ItemCode :
                filter_query &= Q(Product_Detials__pk =ItemCode)
            if StoreType =='NurseStation':
                filter_query &= Q(NurseStation_location__pk =StoreName)
            elif StoreType =='inv':
                filter_query &= Q(Store_location__pk =StoreName)
            StockData = []
           
            stock_data_ins = Stock_Maintance_Table_Detials.objects.filter(filter_query)
            for indx,ins  in enumerate(stock_data_ins):
                stock_dic = {
                    "id": indx +1,
                    "pk": ins.pk,
                    "ItemCode": ins.Product_Detials.pk,
                    "ItemName": ins.Product_Detials.ItemName,
                    "ProductCategory": ins.Product_Detials.ProductCategory.ProductCategory_Name if ins.Product_Detials.ProductCategory else None,
                    "SubCategory": ins.Product_Detials.SubCategory.SubCategoryName if ins.Product_Detials.SubCategory else None,
                    'Location': ins.NurseStation_location.Location_Name.Location_Name if ins.IsNurseStation else ins.Store_location.Location_Name.Location_Name,
                    'LocationId': ins.NurseStation_location.Location_Name.pk if ins.IsNurseStation else ins.Store_location.Location_Name.pk,
                    'StoreType': 'Nurse Station' if ins.IsNurseStation else "Inventory Store",
                    'StoreId': ins.NurseStation_location.pk if ins.IsNurseStation else ins.Store_location.pk,
                    'StoreName': ins.NurseStation_location.NurseStationName if ins.IsNurseStation else ins.Store_location.Store_Name,
                    'Batch_No': ins.Batch_No,
                    'Total_Quantity': ins.Total_Quantity if ins else 0,
                    'Grn_Recieve_Quantity': ins.Grn_Recieve_Quantity if ins else 0,
                    'Indent_Send_Quantity': ins.Indent_Send_Quantity if ins else 0,
                    'Indent_Recieve_Quantity': ins.Indent_Recieve_Quantity if ins else 0,
                    'Indent_Return_Quantity': ins.Indent_Return_Quantity if ins else 0,
                    'Grn_Return_Quantity': ins.Grn_Return_Quantity if ins else 0,
                    'Scrab_Quantity': ins.Scrab_Quantity if ins else 0,
                    'Sold_Quantity': ins.Sold_Quantity if ins else 0,
                    'AvailableQuantity': ins.AvailableQuantity if ins else 0,
                    'Expiry_Date':ins.Expiry_Date if ins.Is_Expiry_Date_Available else 'Not Available',
                    'Expiry_Status':ins.Expiry_Status
                }
                StockData.append(stock_dic)
            return JsonResponse(StockData, safe=False)
           
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
    else:
        return JsonResponse({'error': 'Request method not allowed'}, status=405)



@csrf_exempt
@require_http_methods(["GET"])
def get_overall_stock_list_table_column_details(request):
    if request.method == "GET":
        try:
            table_struc = {}
            Inv_Location_details_ins = Inventory_Location_Master_Detials.objects.filter(Status=True)
            NurseStation_Location_details_ins = NurseStationMaster.objects.filter(Status=True)
            for inv in Inv_Location_details_ins:
                location_dat = inv.Location_Name
                location_key = f"{location_dat.pk}_{location_dat.Location_Name}"
 
                if location_key not in table_struc:
                    table_struc[location_key] = {'inv': [], 'Nurse': []}
               
                inv_store_entry = f"{inv.pk}_{inv.Store_Name}"
 
                # Add only if it doesn't already exist
                if inv_store_entry not in table_struc[location_key]['inv']:
                    table_struc[location_key]['inv'].append(inv_store_entry)
            for Nurse in NurseStation_Location_details_ins:
                location_dat = Nurse.Location_Name
                location_key = f"{location_dat.pk}_{location_dat.Location_Name}"
 
                if location_key not in table_struc:
                    table_struc[location_key] = {'inv': [], 'Nurse': []}
               
                Nurse_store_entry = f"{Nurse.pk}_{Nurse.NurseStationName}"
 
                # Add only if it doesn't already exist
                if Nurse_store_entry not in table_struc[location_key]['Nurse']:
                    table_struc[location_key]['Nurse'].append(Nurse_store_entry)
            return JsonResponse(table_struc, safe=False)
           
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
    else:
        return JsonResponse({'error': 'Request method not allowed'}, status=405)
 
 
 
 
