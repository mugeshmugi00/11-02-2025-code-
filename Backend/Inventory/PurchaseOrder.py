from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import transaction
import json
from Masters.models import * 
from Inventory.models import *
from django.db.models import Q
import pandas as pd
from io import BytesIO
from PIL import Image
import base64
from PyPDF2 import PdfReader, PdfWriter
# import magic
from decimal import Decimal, ROUND_HALF_UP





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


# ----------------------------------------------------------


@csrf_exempt
@require_http_methods(["POST","OPTIONS","GET"])
def PurchaseOrder_Link(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # print('dataaaaaa',data)

            SupplierId=data.get('SupplierId')
            OrderDate=data.get('OrderDate')
            DeliveryDate=data.get('DeliveryExpectedDate')
            BillingLocation=data.get('BillingLocation')
            ShippingLocation=data.get('ShippingLocation')
            TotalOrderValue=data.get('TotalOrderValue')
            Create_by=data.get('Create_by')
            POItemArrays=data.get('POItemArrays')
            PurchaseOrderNumber=data.get('PurchaseOrderNumber')

            EditStatus=data.get('EditStatus')


            if SupplierId:
                Supplier_Instance=Supplier_Master_Details.objects.get(pk=SupplierId)
            if BillingLocation:
                BillingLocation_instance=Location_Detials.objects.get(pk=BillingLocation)
                BillingLocation_Address_instance=Clinic_Detials.objects.get(Location__Location_Id=BillingLocation)
            if ShippingLocation:
                ShippingLocation_instance=Location_Detials.objects.get(pk=ShippingLocation)
                ShippingLocation_Address_instance=Clinic_Detials.objects.get(Location__Location_Id=ShippingLocation)

            if EditStatus:
                PO_Edit_instance=Purchase_Order_Details.objects.get(pk=PurchaseOrderNumber)
                PO_Edit_instance.PO_Status=EditStatus
                PO_Edit_instance.save()

                Purchase_Order_Items = Purchase_Order_Item_Details.objects.filter(PurchaseOrder=PO_Edit_instance)
    
                for item in Purchase_Order_Items:
                    item.Item_Status = EditStatus
                    item.save() 

                return JsonResponse ({'success': 'Purchase Order Approved successfully'})      


            elif PurchaseOrderNumber:
                print('Edit---PurchaseOrderNumber',PurchaseOrderNumber)
                PO_Edit_instance=Purchase_Order_Details.objects.get(pk=PurchaseOrderNumber)
                PO_Edit_instance.Supplier_Id=Supplier_Instance
                PO_Edit_instance.Order_Date=OrderDate
                PO_Edit_instance.Delivery_Expected_Date=DeliveryDate
                PO_Edit_instance.Billing_Location=BillingLocation_instance
                PO_Edit_instance.Billing_Address=BillingLocation_Address_instance
                PO_Edit_instance.Shipping_Location=ShippingLocation_instance
                PO_Edit_instance.Shipping_Address=ShippingLocation_Address_instance
                PO_Edit_instance.Total_Order_Value=TotalOrderValue
                PO_Edit_instance.Create_by=Create_by
                PO_Edit_instance.save()

                Purchase_Order_Item_Details.objects.filter(PurchaseOrder__PurchaseOrder_Number=PurchaseOrderNumber).delete()
                
                for row in POItemArrays:
                    ItemCode=int(row.get('ItemCode'))
                    Supplier_Product_instance=Supplier_Product_Details.objects.get(Supplier_Detials=Supplier_Instance,Product_Detials__pk=ItemCode)

                    Purchase_Order_Item_Details.objects.create(
                        PurchaseOrder=PO_Edit_instance,
                        PO_Item_Detailes=Supplier_Product_instance,
                        PO_Order_Qty=row.get('PurchaseQty'),
                        TotalAmount=row.get('TotalAmount'),
                        Balance_Qty=row.get('PurchaseQty'),
                        Create_by=Create_by,
                    )

                return JsonResponse ({'success': 'Purchase Order Detials Update successfully'})      

            else:
                
                print(OrderDate,DeliveryDate,'------')

                Purchase_Order_istance=Purchase_Order_Details.objects.create(
                    Supplier_Id=Supplier_Instance,
                    Order_Date=OrderDate,
                    Delivery_Expected_Date=DeliveryDate,
                    Billing_Location=BillingLocation_instance,
                    Billing_Address=BillingLocation_Address_instance,
                    Shipping_Location=ShippingLocation_instance,
                    Shipping_Address=ShippingLocation_Address_instance,
                    Total_Order_Value=TotalOrderValue,
                    Create_by=Create_by,
                    )
                
                for row in POItemArrays:
                    ItemCode=int(row.get('ItemCode'))
                    print('111',ItemCode)
                    Supplier_Product_instance=Supplier_Product_Details.objects.get(Supplier_Detials=Supplier_Instance,Product_Detials__pk=ItemCode)
                    print('222',Supplier_Product_instance)

                    Purchase_Order_Item_Details.objects.create(
                        PurchaseOrder=Purchase_Order_istance,
                        PO_Item_Detailes=Supplier_Product_instance,
                        PO_Order_Qty=row.get('PurchaseQty'),
                        TotalAmount=row.get('TotalAmount'),
                        Balance_Qty=row.get('PurchaseQty'),
                        Create_by=Create_by,
                    )


                return JsonResponse ({'success': 'Purchase Order Detials added successfully'})      
        
        except Exception as e:
            print(f'An error occurred:{str(e)}')
            return JsonResponse (f'An error occurred:{str(e)}')




# ------------------------PO report


# -------------------change 10.10.24


@csrf_exempt
@require_http_methods(["GET"])
def PurchaseOrder_Report_Details(request):
    if request.method == 'GET':
        try:
            StatusCheck = request.GET.get('StatusCheck')
            DateType = request.GET.get('DateType')
            CurrentDate = request.GET.get('CurrentDate')
            FromDate = request.GET.get('FromDate')
            ToDate = request.GET.get('ToDate')
            SupplierId = request.GET.get('SupplierId')
            BillingLocation = request.GET.get('BillingLocation')
            ShippingLocation = request.GET.get('ShippingLocation')

            

            Purchase_Order_instance = Purchase_Order_Details.objects.all()

            
            if StatusCheck:
                Purchase_Order_instance = Purchase_Order_instance.filter(PO_Status=StatusCheck)
            
            if SupplierId:
                Purchase_Order_instance = Purchase_Order_instance.filter(Supplier_Id=SupplierId)
            
            if BillingLocation:                
                    Purchase_Order_instance = Purchase_Order_instance.filter(Billing_Location__Location_Id=BillingLocation)
            
            if ShippingLocation:                
                    Purchase_Order_instance = Purchase_Order_instance.filter(Shipping_Location__Location_Id=ShippingLocation)
            
            if DateType == 'CurrentDate' and CurrentDate:                
                    Purchase_Order_instance = Purchase_Order_instance.filter(Order_Date=CurrentDate)
            
            if DateType == 'Customize' and FromDate and ToDate:
                Purchase_Order_instance = Purchase_Order_instance.filter(
                    Q(Order_Date__range=[FromDate, ToDate]) | Q(Order_Date__range=[FromDate, ToDate])
            )

            PO_Array = []

            for row in Purchase_Order_instance:
                PO_dic = {
                    'id': row.PurchaseOrder_Number,
                    'SupplierId': row.Supplier_Id.pk,
                    'SupplierName': row.Supplier_Id.Supplier_Name,
                    'SupplierMailId': row.Supplier_Id.Email_Address,
                    'SupplierContactNumber': row.Supplier_Id.Contact_Number,
                    'SupplierContactPerson': row.Supplier_Id.Contact_Person,
                    'OrderDate': row.Order_Date,
                    'DeliveryExpectedDate': row.Delivery_Expected_Date,
                    'BillingLocation': row.Billing_Location.Location_Id,
                    'Use_BillingLocation': row.Billing_Location.Location_Name,
                    'ShippingLocation': row.Shipping_Location.Location_Id,
                    'Use_ShippingLocation': row.Shipping_Location.Location_Name,
                    'TotalOrderValue': row.Total_Order_Value,
                    'PO_Status': row.PO_Status,

                }
                print('PO_dic',PO_dic)
                Item_instance = Purchase_Order_Item_Details.objects.filter(PurchaseOrder__PurchaseOrder_Number=row.PurchaseOrder_Number)
                
                Item_Array = []
                for item in Item_instance:
                    # print('1232',item)
                    Get_Rate_Inst = Supplier_Product_Amount_Details.objects.filter(Supplier_detials__Supplier_Detials__pk=row.Supplier_Id.Supplier_Id, Supplier_detials__Product_Detials=item.PO_Item_Detailes.Product_Detials.pk).order_by('-Created_at').first()

                    item_dic = {
                        'id': item.PO_Item_Number,
                        'ItemCode': item.PO_Item_Detailes.Product_Detials.pk,
                        'ItemName': item.PO_Item_Detailes.Product_Detials.ItemName,
                        'ProductCategory': item.PO_Item_Detailes.Product_Detials.ProductCategory.ProductCategory_Name,
                        'SubCategory': item.PO_Item_Detailes.Product_Detials.SubCategory.SubCategoryName,
                        
                    }
                    
                    if item.PO_Item_Detailes.Product_Detials.GenericName :                     
                        item_dic['GenericName'] = item.PO_Item_Detailes.Product_Detials.GenericName.GenericName
                    if item.PO_Item_Detailes.Product_Detials.CompanyName :
                        item_dic['ManufacturerName'] = item.PO_Item_Detailes.Product_Detials.CompanyName.CompanyName
                    if item.PO_Item_Detailes.Product_Detials.HSNCode :
                        item_dic['HSNCode'] = item.PO_Item_Detailes.Product_Detials.HSNCode
                    if item.PO_Item_Detailes.Product_Detials.Strength :
                        item_dic['Strength'] = item.PO_Item_Detailes.Product_Detials.Strength
                    if item.PO_Item_Detailes.Product_Detials.StrengthType :
                        item_dic['StrengthType'] = item.PO_Item_Detailes.Product_Detials.StrengthType
                    if item.PO_Item_Detailes.Product_Detials.Volume :
                        item_dic['Volume'] = item.PO_Item_Detailes.Product_Detials.Volume
                    if item.PO_Item_Detailes.Product_Detials.VolumeType :
                        item_dic['VolumeType'] = item.PO_Item_Detailes.Product_Detials.VolumeType.Unit_Name                   
                    if item.PO_Item_Detailes.Product_Detials.PackType :
                        item_dic['PackType'] = item.PO_Item_Detailes.Product_Detials.PackType.PackType_Name
                    if item.PO_Item_Detailes.Product_Detials.PackQty :
                        item_dic['PackQty']= item.PO_Item_Detailes.Product_Detials.PackQty
                    if item.PO_Item_Detailes.Product_Detials.Is_Manufacture_Date_Available :
                        item_dic['Is_Manufacture_Date_Available']= item.PO_Item_Detailes.Product_Detials.Is_Manufacture_Date_Available
                    if item.PO_Item_Detailes.Product_Detials.Is_Expiry_Date_Available :
                        item_dic['Is_Expiry_Date_Available']= item.PO_Item_Detailes.Product_Detials.Is_Expiry_Date_Available
                    
                    
                    if item.Item_Status == 'Waiting For GRN' and item.PO_Item_Detailes.Product_Detials.IsSellable is not None : 
                         item_dic['IsSellable']='Yes' if item.PO_Item_Detailes.Product_Detials.IsSellable else 'No'
                         if item_dic['IsSellable'] == 'Yes':                         
                            item_dic['LeastSellableUnit']=item.PO_Item_Detailes.Product_Detials.LeastSellableUnit

                    
                    item_dic['MRP']= Get_Rate_Inst.MRP
                    item_dic['PurchaseRateBeforeGST']= Get_Rate_Inst.PurchaseRateBeforeGST
                    item_dic['GST']=  Get_Rate_Inst.GST
                    item_dic['PurchaseRateAfterGST']=Get_Rate_Inst.PurchaseRateAfterGST
                    
                        
                    item_dic['PurchaseQty']= item.PO_Order_Qty
                    item_dic['TotalAmount'] = item.TotalAmount
                    item_dic['Item_Status']= item.Item_Status
                    item_dic['Reason']= item.Reason                              
                    item_dic['Received_Qty']=item.Received_Qty
                    item_dic['Balance_Qty']=item.Balance_Qty
                    
                    
                    Item_Array.append(item_dic)

                PO_dic['Item_Details'] = Item_Array
                PO_Array.append(PO_dic)

            PO_Array.reverse()

            return JsonResponse(PO_Array, safe=False)
        
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
        



# ===================PurchseReturn Code======================================






def safe_decimal(value):
    try:
        return Decimal(value)
    except (TypeError, ValueError):
        return Decimal(0)

@csrf_exempt
@require_http_methods(["GET"])
def GRN_Details_GET_For_PurchseReturn(request):
    if request.method == 'GET':
        try:
            Suppliercode = request.GET.get('SupplierCode')
            StoreLocation=request.GET.get('StoreLocation')

            GRNInvoiceNo=request.GET.get('GRNInvoiceNo')
            Reason=request.GET.get('Reason')
            
            
            if Suppliercode and StoreLocation :
                GRN_Table_Detials_Ins=GRN_Table_Detials.objects.filter(Supplier_Detials=Suppliercode,Store_location=StoreLocation)
                GRN_Array=[]
                for row in GRN_Table_Detials_Ins :
                    Grn_dec={
                        'GRNNumber':row.pk,
                        'GrnDate':row.GrnDate.strftime('%Y-%m-%d') if row.GrnDate else None,
                        'SupplierBillNumber':row.Supplier_Bill_Number,
                        'SupplierBillDate':row.Supplier_Bill_Date.strftime('%Y-%m-%d') if row.Supplier_Bill_Date else None,
                    }

                    GRN_Array.append(Grn_dec)
              
                return JsonResponse (GRN_Array,safe=False)
            elif GRNInvoiceNo :
                print('Reason',Reason)
                GRN_Table_Detials_ins=GRN_Table_Detials.objects.get(pk=GRNInvoiceNo)
                GRN_Product_Item_Ins=GRN_Product_Item_Detials.objects.filter(Grn_Detials=GRNInvoiceNo)
                
                
                Item_Array=[]
                
                for row in GRN_Product_Item_Ins:
                    Item_dec = {}

                    Stock_Maintance_Ins=Stock_Maintance_Table_Detials.objects.get(Product_Detials=row.Product_Detials,Batch_No=row.Batch_No,Store_location=GRN_Table_Detials_ins.Store_location)

                    if row.Product_Detials.pk:
                        Item_dec['ItemCode'] = row.Product_Detials.pk
                    if row.Product_Detials.ItemName:
                        Item_dec['ItemName'] = row.Product_Detials.ItemName
                    # if row.Product_Detials.ProductCategory:
                    #     Item_dec['ProductCategory'] = row.Product_Detials.ProductCategory.ProductCategory_Name
                    # if row.Product_Detials.SubCategory:
                    #     Item_dec['SubCategory'] = row.Product_Detials.SubCategory.SubCategoryName
                    if row.Product_Detials.GenericName:
                        Item_dec['GenericName'] = row.Product_Detials.GenericName.GenericName
                    if row.Product_Detials.CompanyName:
                        Item_dec['CompanyName'] = row.Product_Detials.CompanyName.CompanyName
                    if row.Product_Detials.HSNCode:
                        Item_dec['HSNCode'] = row.Product_Detials.HSNCode
                    if row.Product_Detials.ProductType:
                        Item_dec['ProductType'] = row.Product_Detials.ProductType.ProductType_Name
                    # if row.Product_Detials.ProductGroup:
                    #     Item_dec['ProductGroup'] = row.Product_Detials.ProductGroup.ProductGroup_Name
                    if row.Product_Detials.Strength and row.Product_Detials.StrengthType:
                        Item_dec['Strength'] = f'{row.Product_Detials.Strength} {row.Product_Detials.StrengthType}'
                    if row.Product_Detials.Volume and row.Product_Detials.VolumeType:
                        Item_dec['Volume'] = f'{row.Product_Detials.Volume} {row.Product_Detials.VolumeType.Unit_Name}'
                    if row.Product_Detials.PackType:
                        Item_dec['PackType'] = row.Product_Detials.PackType.PackType_Name
                    if row.Product_Detials.PackQty:
                        Item_dec['PackQuantity'] = row.Product_Detials.PackQty
                    if row.Batch_No:
                        Item_dec['BatchNo'] = row.Batch_No
                    if row.Manufacture_Date:
                        Item_dec['ManufactureDate'] = row.Manufacture_Date
                    if row.Expiry_Date:
                        Item_dec['ExpiryDate'] = row.Expiry_Date
                    # if row.Purchase_MRP:
                    #     Item_dec['PurchaseMRP'] = row.Purchase_MRP
                    # if row.Purchase_rate_taxable:
                    #     Item_dec['PurchaseRateTaxable'] = row.Purchase_rate_taxable
                    # if row.Tax_Percentage:
                    #     Item_dec['TaxPercentage'] = row.Tax_Percentage
                    if row.Purchase_rate_with_tax:
                        Item_dec['PurchaseRateWithTax'] = row.Purchase_rate_with_tax
                    # if Stock_Maintance_Ins:
                    #     Item_dec['ExpiryStatus'] = Stock_Maintance_Ins.Expiry_Status
                    if row.Total_Received_Quantity:
                        Item_dec['PurchaseQuantity'] = row.Total_Received_Quantity
                    # if row.Total_Pack_Quantity:
                    #     Item_dec['TotalPackQuantity'] = row.Total_Pack_Quantity                    
                    # if row.Total_Pack_Taxable_Amount:
                    #     Item_dec['TotalTaxableAmount'] = row.Total_Pack_Taxable_Amount
                    # if row.Total_Pack_Tax_Amount:
                    #     Item_dec['TotalTaxAmount'] = row.Total_Pack_Tax_Amount
                    if row.Total_Pack_Amount_with_tax:
                        Item_dec['TotalAmount'] = row.Total_Pack_Amount_with_tax
                    if Stock_Maintance_Ins:
                        Item_dec['AvailableQuantity'] = Stock_Maintance_Ins.AvailableQuantity

                    if row.Discount_Amount:
                        Item_dec['Discount'] = 'Item Wise Discount'
                        Item_dec['DiscountMethod'] = row.Discount_Method
                        Item_dec['DiscountType'] = row.Discount_Type
                        Item_dec['DiscountValue'] = row.Discount_Amount

                  
                        if row.Discount_Method == 'BeforeTax':
                            if row.Discount_Type == 'Cash':
                                taxable_amount = row.Purchase_rate_taxable - (row.Discount_Amount / row.Total_Received_Quantity)
                                ResultAmount1 = taxable_amount + (taxable_amount * safe_decimal(row.Tax_Percentage) / 100)
                                Item_dec['SingleProductPurchaseAmount'] = ResultAmount1.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                                print('D11111',Item_dec['SingleProductPurchaseAmount'])

                            elif row.Discount_Type == 'Percentage':
                                discounted_rate = row.Purchase_rate_taxable * (1 - row.Discount_Amount / 100)
                                ResultAmount2 = discounted_rate + (discounted_rate * safe_decimal(row.Tax_Percentage) / 100)
                                Item_dec['SingleProductPurchaseAmount'] = ResultAmount2.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                                print('D22222',Item_dec['SingleProductPurchaseAmount'])


                        elif row.Discount_Method == 'AfterTax':
                            if row.Discount_Type == 'Cash':
                                amount_with_tax = row.Purchase_rate_with_tax 
                                ResultAmount3 = max(0, amount_with_tax - row.Discount_Amount / row.Total_Received_Quantity)
                                Item_dec['SingleProductPurchaseAmount']=ResultAmount3.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                                print('D33333',Item_dec['SingleProductPurchaseAmount'])


                            elif row.Discount_Type == 'Percentage':
                                amount_with_tax = row.Purchase_rate_with_tax
                                ResultAmount4 = amount_with_tax * (1 - row.Discount_Amount / 100)
                                Item_dec['SingleProductPurchaseAmount'] = ResultAmount4.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                                print('D44444',Item_dec['SingleProductPurchaseAmount'])
                                

                    elif GRN_Table_Detials_ins.Discount_Amount :
                        Item_dec['Discount'] = 'Overall Discount'
                        Item_dec['DiscountMethod'] = GRN_Table_Detials_ins.Total_Discount_Method
                        Item_dec['DiscountType'] = GRN_Table_Detials_ins.Total_Discount_Type
                        Item_dec['DiscountValue'] = GRN_Table_Detials_ins.Discount_Amount

                        findlength=GRN_Product_Item_Detials.objects.filter(Grn_Detials=GRNInvoiceNo,Discount_Amount=0).count()

                        if GRN_Table_Detials_ins.Total_Discount_Method =='BeforeTax':
                            if GRN_Table_Detials_ins.Total_Discount_Type == 'Cash' :
                                ItemDiscound1 = GRN_Table_Detials_ins.Discount_Amount / findlength
                                taxable_amount = row.Purchase_rate_taxable - (ItemDiscound1 / row.Total_Received_Quantity)
                                ResultAmount1 = taxable_amount + (taxable_amount * safe_decimal(row.Tax_Percentage) / 100)
                                
                                Item_dec['DiscountValue'] = ItemDiscound1
                                Item_dec['SingleProductPurchaseAmount'] = ResultAmount1.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                                print('D55555',Item_dec['SingleProductPurchaseAmount'])


                            elif GRN_Table_Detials_ins.Total_Discount_Type == 'Percentage' :
                                discounted_rate = row.Purchase_rate_taxable * (1 - GRN_Table_Detials_ins.Discount_Amount / 100)
                                ResultAmount2 = discounted_rate + (discounted_rate * safe_decimal(row.Tax_Percentage) / 100)
                                
                                Item_dec['DiscountValue'] = GRN_Table_Detials_ins.Discount_Amount
                                Item_dec['SingleProductPurchaseAmount'] = ResultAmount2.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                                print('D66666',Item_dec['SingleProductPurchaseAmount'])
                                
                                
                        elif GRN_Table_Detials_ins.Total_Discount_Method =='AfterTax':
                            if GRN_Table_Detials_ins.Total_Discount_Type == 'Cash' :
                                ItemDiscound3 = GRN_Table_Detials_ins.Discount_Amount / findlength
                                amount_with_tax = row.Purchase_rate_with_tax 
                                ResultAmount3 = max(0, amount_with_tax - ItemDiscound3 / row.Total_Received_Quantity)
                                
                                Item_dec['DiscountValue'] = ItemDiscound3
                                Item_dec['SingleProductPurchaseAmount']=ResultAmount3.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                                print('D77777',Item_dec['SingleProductPurchaseAmount'])

                            
                            elif GRN_Table_Detials_ins.Total_Discount_Type == 'Percentage' :
                                amount_with_tax = row.Purchase_rate_with_tax
                                ResultAmount4 = amount_with_tax * (1 - GRN_Table_Detials_ins.Discount_Amount / 100)
                                
                                Item_dec['DiscountValue'] = GRN_Table_Detials_ins.Discount_Amount
                                Item_dec['SingleProductPurchaseAmount'] = ResultAmount4.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

                                print('D88888',Item_dec['SingleProductPurchaseAmount'])

                    else:
                        Item_dec['SingleProductPurchaseAmount'] = row.Purchase_rate_with_tax

                    
                    Item_Array.append(Item_dec)

                if Reason == 'ExpiredReturn':

                    Item_Array = [item for item in Item_Array if item.get('ExpiryStatus') != 'Not-Expired']


                return JsonResponse (Item_Array,safe=False)

        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse({'error':f'An error occurred: {str(e)}'},status=500)




@csrf_exempt
@require_http_methods(["POST","OPTIONS","GET"])
def PurcchaseReturn_Link(request):
    if request.method == "POST":
        try:

            data = json.loads(request.body)


            SupplierDetailes=data.get('SupplierDetailes')
            ReturnItemList=data.get('ReturnItemList')
            Create_by=data.get('Create_by')

            print('data',data)

            ReturnDate=SupplierDetailes.get('ReturnDate')
            SupplierCode=SupplierDetailes.get('SupplierCode')
            StoreLocation=SupplierDetailes.get('StoreLocation')
            ReturnTotalItem=SupplierDetailes.get('ReturnTotalItem')
            ReturnTotalQuantity=SupplierDetailes.get('ReturnTotalQuantity')
            ReturnTotalAmount=SupplierDetailes.get('ReturnTotalAmount')

            PurchaseReturnNumber=SupplierDetailes.get('PurchaseReturnNumber')
       
            print('PurchaseReturnNumber',PurchaseReturnNumber)

            if SupplierCode:
                Supplier_Master_Inst=Supplier_Master_Details.objects.get(pk=SupplierCode)
            if StoreLocation:
                Inventory_Location_Ins=Inventory_Location_Master_Detials.objects.get(pk=StoreLocation)
            if PurchaseReturnNumber :
                Purchase_Return_Ins=Purchase_Return_Details_Table.objects.get(pk=PurchaseReturnNumber)

                Purchase_Return_Ins.Supplier_Detials=Supplier_Master_Inst
                Purchase_Return_Ins.Store_location=Inventory_Location_Ins
                Purchase_Return_Ins.Return_Total_Item=ReturnTotalItem
                Purchase_Return_Ins.Return_Total_Quantity=ReturnTotalQuantity
                Purchase_Return_Ins.Return_Total_Amount=ReturnTotalAmount

                Purchase_Return_Ins.save()

                Purchase_Return_Items_Details_Table.objects.filter(Purchase_Return_Details__pk=PurchaseReturnNumber).delete()

                for row in ReturnItemList:
                
                    GRN_Table_Detials_ins=GRN_Table_Detials.objects.get(pk=row.get('GRNInvoiceNo'))
                    GRN_Product_ins=GRN_Product_Item_Detials.objects.filter(Grn_Detials=GRN_Table_Detials_ins,Product_Detials=row.get('ItemCode'),Batch_No=row.get('BatchNo')).first()
                    Stock_Maintance_ins=Stock_Maintance_Table_Detials.objects.filter(Product_Detials=row.get('ItemCode'),Batch_No=row.get('BatchNo'),Store_location=Inventory_Location_Ins).first()

                    Purchase_Return_Items_Details_Table.objects.create(
                        Purchase_Return_Details=Purchase_Return_Ins,
                        GRN_Detials=GRN_Table_Detials_ins,
                        GRN_Item_Detials=GRN_Product_ins,
                        Stock_Detials=Stock_Maintance_ins,
                        Reason=row.get('Reason'),
                        Single_Product_Purchase_Amount=row.get('PurchaseAmount'),
                        Available_Pack_Quantity=row.get('AvailablePackQuantity'),
                        Return_Quantity=row.get('ReturnQuantity'),
                        Return_Pack_Quantity=row.get('ReturnPackQuantity'),
                        Return_Quantity_Amount=row.get('ReturnQuantityAmount'),
                        Remarks=row.get('Remarks'),
                        Created_by=Create_by
                    ) 

                return JsonResponse ({'success': 'Purchase Return Detials Update successfully'})      
        

            

            else:
                PO_Return_Ins=Purchase_Return_Details_Table.objects.create(
                Purchase_Return_Date=ReturnDate,
                Supplier_Detials=Supplier_Master_Inst,
                Store_location=Inventory_Location_Ins,
                Return_Total_Item=ReturnTotalItem,
                Return_Total_Quantity=ReturnTotalQuantity,
                Return_Total_Amount=ReturnTotalAmount,
                Created_by=Create_by
                )

                for row in ReturnItemList:
                
                    GRN_Table_Detials_ins=GRN_Table_Detials.objects.get(pk=row.get('GRNInvoiceNo'))
                    GRN_Product_ins=GRN_Product_Item_Detials.objects.filter(Grn_Detials=GRN_Table_Detials_ins,Product_Detials=row.get('ItemCode'),Batch_No=row.get('BatchNo')).first()
                    Stock_Maintance_ins=Stock_Maintance_Table_Detials.objects.filter(Product_Detials=row.get('ItemCode'),Batch_No=row.get('BatchNo')).first()

                    Purchase_Return_Items_Details_Table.objects.create(
                        Purchase_Return_Details=PO_Return_Ins,
                        GRN_Detials=GRN_Table_Detials_ins,
                        GRN_Item_Detials=GRN_Product_ins,
                        Stock_Detials=Stock_Maintance_ins,
                        Reason=row.get('Reason'),
                        Single_Product_Purchase_Amount=row.get('PurchaseAmount'),
                        Available_Pack_Quantity=row.get('AvailablePackQuantity'),
                        Return_Quantity=row.get('ReturnQuantity'),
                        Return_Pack_Quantity=row.get('ReturnPackQuantity'),
                        Return_Quantity_Amount=row.get('ReturnQuantityAmount'),
                        Remarks=row.get('Remarks'),
                        Created_by=Create_by
                    ) 

                return JsonResponse ({'success': 'Purchase Return Detials added successfully'})      
        
        except Exception as e :
            print(f'An error occurred:{str(e)}')
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)



# ------------------------------------------------------

@csrf_exempt
@require_http_methods(["GET"])
def PurchaseReturn_Report_Link (request):
    if request.method == "GET":
        try:
            StatusCheck = request.GET.get('StatusCheck')
            DateType=request.GET.get('DateType')
            CurrentDate=request.GET.get('CurrentDate')
            FromDate=request.GET.get('FromDate')
            ToDate=request.GET.get('ToDate')
            SupplierId=request.GET.get('SupplierId')
            SupplierName=request.GET.get('SupplierName')
            Location=request.GET.get('Location')

            print('Location',Location)

            Item_Array=[]

            query =Q()

            if StatusCheck :
                query &= Q(Status = StatusCheck)

            if DateType :
                if DateType == 'CurrentDate':
                    if CurrentDate:
                        query &= Q(Purchase_Return_Date = CurrentDate)
                elif DateType == 'Customize':
                    if FromDate and ToDate:
                        query &= Q(Purchase_Return_Date__range=[FromDate,ToDate])
                    elif FromDate:
                        query &= Q(Purchase_Return_Date__gte=FromDate)
                    elif ToDate:
                        query &= Q(Purchase_Return_Date__lte=ToDate)
            
            if SupplierId :
                query &= Q(Supplier_Detials=SupplierId)
            if Location :
                query &= Q(Store_location__Location_Name__Location_Id=Location)
            
            # print('query',query)

            Purchase_Return_Ins=Purchase_Return_Details_Table.objects.filter(query)

            for row in Purchase_Return_Ins :
                Main_Dec={
                    'id':row.pk,
                    'ReturnDate':row.Purchase_Return_Date,
                    'SupplierCode' :row.Supplier_Detials.pk,
                    'SupplierName' :row.Supplier_Detials.Supplier_Name,
                    'SupplierMailId' :row.Supplier_Detials.Email_Address,
                    'SupplierContactNumber' :row.Supplier_Detials.Contact_Number,
                    'SupplierContactPerson' :row.Supplier_Detials.Contact_Person,
                    'StoreLocation_id' :row.Store_location.Store_Id,
                    'StoreLocation' :row.Store_location.Store_Name,
                    'Location_id' :row.Store_location.Location_Name.pk,
                    'Location' :row.Store_location.Location_Name.Location_Name,
                    'ReturnTotalItem':row.Return_Total_Item,
                    'ReturnTotalQuantity':row.Return_Total_Quantity,
                    'ReturnTotalAmount':row.Return_Total_Amount,
                    'Status':row.Status,
                    'Items':[]     
                }

                Items_Ins=Purchase_Return_Items_Details_Table.objects.filter(Purchase_Return_Details=row)

                for item in Items_Ins:
                    Item_dec={
                        'id':item.pk,
                        'GRNInvoiceNo':item.GRN_Detials.pk,
                        'GRNDate':item.GRN_Detials.GrnDate,
                        'SupplierBillNo':item.GRN_Detials.Supplier_Bill_Number,
                        'SupplierBillDate':item.GRN_Detials.Supplier_Bill_Date,
                        'Reason':item.Reason,
                        'ItemCode':item.GRN_Item_Detials.Product_Detials.pk,
                        'ItemName':item.GRN_Item_Detials.Product_Detials.ItemName,
                    }

                    if item.GRN_Item_Detials.Product_Detials.GenericName:
                        Item_dec['GenericName']=item.GRN_Item_Detials.Product_Detials.GenericName.GenericName
                    if item.GRN_Item_Detials.Product_Detials.CompanyName:   
                        Item_dec['CompanyName']=item.GRN_Item_Detials.Product_Detials.CompanyName.CompanyName
                    if item.GRN_Item_Detials.Product_Detials.HSNCode:   
                        Item_dec['HSNCode']=item.GRN_Item_Detials.Product_Detials.HSNCode
                    if item.GRN_Item_Detials.Product_Detials.ProductType:
                        Item_dec['ProductType']=item.GRN_Item_Detials.Product_Detials.ProductType.ProductType_Name
                    if item.GRN_Item_Detials.Product_Detials.Strength and item.GRN_Item_Detials.Product_Detials.StrengthType:
                        Item_dec['Strength'] = f'{item.GRN_Item_Detials.Product_Detials.Strength} {item.GRN_Item_Detials.Product_Detials.StrengthType}'
                    if item.GRN_Item_Detials.Product_Detials.Volume and item.GRN_Item_Detials.Product_Detials.VolumeType:
                        Item_dec['Volume'] = f'{item.GRN_Item_Detials.Product_Detials.Volume} {item.GRN_Item_Detials.Product_Detials.VolumeType.Unit_Name}'
                    if item.GRN_Item_Detials.Product_Detials.PackType:
                        Item_dec['PackType'] = item.GRN_Item_Detials.Product_Detials.PackType.PackType_Name
                    if item.GRN_Item_Detials.Product_Detials.PackQty:
                        Item_dec['PackQuantity'] = item.GRN_Item_Detials.Product_Detials.PackQty
                    if item.GRN_Item_Detials.Batch_No:
                        Item_dec['BatchNo'] = item.GRN_Item_Detials.Batch_No
                    if item.GRN_Item_Detials.Manufacture_Date:
                        Item_dec['ManufactureDate'] = item.GRN_Item_Detials.Manufacture_Date
                    if item.GRN_Item_Detials.Expiry_Date:
                        Item_dec['ExpiryDate'] = item.GRN_Item_Detials.Expiry_Date  
                    if item.GRN_Item_Detials.Purchase_rate_with_tax:
                        Item_dec['PurchaseRateWithTax'] = item.GRN_Item_Detials.Purchase_rate_with_tax   
                    if item.GRN_Item_Detials.Total_Received_Quantity:
                        Item_dec['PurchaseQuantity'] = item.GRN_Item_Detials.Total_Received_Quantity
                    if item.GRN_Item_Detials.Total_Pack_Amount_with_tax:
                        Item_dec['TotalAmount'] = item.GRN_Item_Detials.Total_Pack_Amount_with_tax
                    if item.Stock_Detials:
                        Item_dec['AvailablePackQuantity'] = item.Stock_Detials.AvailableQuantity
                    
                    if item.GRN_Item_Detials.Discount_Amount:
                        Item_dec['Discount'] = 'Item Wise Discount'
                        Item_dec['DiscountMethod'] = item.GRN_Item_Detials.Discount_Method
                        Item_dec['DiscountType'] = item.GRN_Item_Detials.Discount_Type
                        Item_dec['DiscountValue'] = item.GRN_Item_Detials.Discount_Amount
                    if item.GRN_Detials.Discount_Amount:
                        Item_dec['Discount'] = 'Overall Discount'
                        Item_dec['DiscountMethod'] = item.GRN_Detials.Total_Discount_Method
                        Item_dec['DiscountType'] = item.GRN_Detials.Total_Discount_Type
                        Item_dec['DiscountValue'] = item.GRN_Detials.Discount_Amount
                    if item.Single_Product_Purchase_Amount :
                        Item_dec['PurchaseAmount']=item.Single_Product_Purchase_Amount
                    if item.Return_Quantity:
                        Item_dec['ReturnQuantity']=item.Return_Quantity
                    if item.Return_Pack_Quantity:
                        Item_dec['ReturnPackQuantity']=item.Return_Pack_Quantity
                    if item.Return_Quantity_Amount :
                        Item_dec['ReturnQuantityAmount']=item.Return_Quantity_Amount
                    if item.Remarks:
                        Item_dec['Remarks']=item.Remarks
                    
                    Main_Dec['Items'].append(Item_dec)
                Item_Array.append(Main_Dec)


            return JsonResponse(Item_Array,safe=False)
        
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse({'error':f'An error occurred: {str(e)}'},status=500)



@csrf_exempt
@require_http_methods(["POST","OPTIONS","GET"])
def PurchaseReturn_StatusUpdate(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            EditStatus=data.get('EditStatus')
            PRreturnid=data.get('PRreturnid')

            print('data',EditStatus,PRreturnid)

            if not EditStatus or not PRreturnid:
                return JsonResponse({'error': 'EditStatus and PRreturnid are required fields.'}, status=400)
            

            Purchase_Return_Ins=Purchase_Return_Details_Table.objects.get(pk=PRreturnid)
            Purchase_Return_Ins.Status=EditStatus
            Purchase_Return_Ins.save()  

            Purchase_Return_Items_Ins=Purchase_Return_Items_Details_Table.objects.filter(Purchase_Return_Details=Purchase_Return_Ins)  

            for item in Purchase_Return_Items_Ins :
                
                item.Status = EditStatus
                item.save()

                if EditStatus == 'Approved':
                    # print('12345',item.GRN_Item_Detials.Product_Detials.ItemName,'-----',item.GRN_Item_Detials.Batch_No,item.Stock_Detials.pk)
                    Stock_Maintance_Table_ins = Stock_Maintance_Table_Detials.objects.get(pk=item.Stock_Detials.pk)
                    # print('67890',Stock_Maintance_Table_ins.AvailableQuantity,'-----',item.Return_Pack_Quantity)                    
                    Stock_Maintance_Table_ins.AvailableQuantity=Stock_Maintance_Table_ins.AvailableQuantity - item.Return_Pack_Quantity
                    # print('final',Stock_Maintance_Table_ins.AvailableQuantity)
                    Stock_Maintance_Table_ins.save()

            return JsonResponse ({'success': 'Purchase Return Status Update successfully'})      

        except Exception as e :
            print(f'An error occurred:{str(e)}')
            return JsonResponse (f'An error occurred:{str(e)}')



 
@csrf_exempt
@require_http_methods(["POST", "OPTIONS", "GET"])
def PurchaseOrder_Itemwise_Link(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            POItemsArrays = data.get('POItemArrays', [])
            Create_by = data.get('Create_by')
 
            if not POItemsArrays:
                return JsonResponse({'error': 'No purchase order items provided'})
 
            for row in POItemsArrays:
                SupplierId = row.get('SupplierId')
                OrderDate = row.get('OrderDate')
                DeliveryDate = row.get('DeliveryExpectedDate')
                BillingLocation = row.get('BillingLocation')
                ShippingLocation = row.get('ShippingLocation')
                TotalOrderValue = row.get('TotalOrderValue')
                Items = row.get('items', [])
 
                if not SupplierId or not Items:
                    return JsonResponse({'error': f'Missing required fields for supplier {SupplierId}'})
 
                try:
                    Supplier_Instance = Supplier_Master_Details.objects.get(pk=SupplierId)
                    BillingLocation_instance = Location_Detials.objects.get(pk=BillingLocation)
                    BillingLocation_Address_instance=Clinic_Detials.objects.get(Location__Location_Id=BillingLocation)
                    ShippingLocation_instance = Location_Detials.objects.get(pk=ShippingLocation)
                    ShippingLocation_Address_instance=Clinic_Detials.objects.get(Location__Location_Id=ShippingLocation)
                except Supplier_Master_Details.DoesNotExist:
                    return JsonResponse({'warn': f'Supplier {SupplierId} not found'})
                except Location_Detials.DoesNotExist:
                    return JsonResponse({'warn': f'Billing or shipping location not found'})
 
                Purchase_Order_instance = Purchase_Order_Details.objects.create(
                    Supplier_Id=Supplier_Instance,
                    Order_Date=OrderDate,
                    Delivery_Expected_Date=DeliveryDate,
                    Billing_Location=BillingLocation_instance,
                    Billing_Address=BillingLocation_Address_instance,
                    Shipping_Location=ShippingLocation_instance,
                    Shipping_Address=ShippingLocation_Address_instance,
                    Total_Order_Value=TotalOrderValue,
                    Create_by=Create_by,
                )
 
                try:
                    item_objects = []
                    for item in Items:
                        ItemCode = int(item.get('itemCode', 0))
                        Supplier_Product_instance = Supplier_Product_Details.objects.get(
                            Supplier_Detials=Supplier_Instance, Product_Detials__pk=ItemCode
                        )
                        item_objects.append(
                            Purchase_Order_Item_Details(
                                PurchaseOrder=Purchase_Order_instance,
                                PO_Item_Detailes=Supplier_Product_instance,
                                PO_Order_Qty=item.get('PurchaseQty', 0),
                                TotalAmount=item.get('TotalAmount', 0),
                                Balance_Qty=item.get('PurchaseQty', 0),
                                Create_by=Create_by,
                            )
                        )
 
                    # Use bulk_create for efficiency
                    Purchase_Order_Item_Details.objects.bulk_create(item_objects)
 
                except Supplier_Product_Details.DoesNotExist:
                    return JsonResponse({'warn': f'Item {ItemCode} not found for supplier {SupplierId}'})
 
            return JsonResponse({'success': 'Purchase Order Details added successfully'})
 
 
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
 
 