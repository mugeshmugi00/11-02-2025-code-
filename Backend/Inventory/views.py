import json
from django.http import JsonResponse, HttpResponse
from .models import UnitOfMeasurement,Product_field_Details,Product_Category_Product_Details,ProductMaster_Drug_Segment_Details
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import *


@csrf_exempt
def get_unit_of_measurements(request):
    if request.method == 'GET':
        # Fetch all unit records from the database
        units = UnitOfMeasurement.objects.filter(Status = True)

        # Prepare data as a list of dictionaries
        units_data = []
        for unit in units:
            units_data.append({
                'id': unit.pk,
                'Unit_Name': unit.Unit_Name,
                'Unit_Symbol': unit.Unit_Symbol,
                'Unit_Type': unit.Unit_Type,
                'Base_Unit': unit.Base_Unit,
                'Conversion_Factor': float(unit.Conversion_Factor),  # Convert to string for JSON compatibility
                'Difference_Description': unit.Difference_Description,
            })

        # Return the data as JSON
        return JsonResponse(units_data, safe=False)
    else:
        return HttpResponse("Only GET method is allowed", status=405)
    
    



@csrf_exempt
def get_Product_fields_for_productcategory(request):
    if request.method == 'GET':
        gettype = request.GET.get('type','category')
        Category = request.GET.get('Category','')
        # Fetch all unit records from the database
        fileds = Product_field_Details.objects.filter(Status = True).order_by('field_Order')
        
        if gettype =='category' :
            fileds_data = []
            for filed in fileds:
                fileds_data.append({
                    'id': filed.pk,
                    'field_Name': filed.field_Name,
                    'checked': True if filed.pk in [1,2,3,4,12,13,18,21,22,23] else False
                })
            return JsonResponse(fileds_data, safe=False)
            
        else:
            fileds_data=[]
            
            if Category :
                Product_instance =Product_Category_Product_Details.objects.get(pk = int(Category))
                product_field_pks = Product_instance.Product_fields.values_list('pk', flat=True)
                for filed in fileds:
                    if filed.pk in product_field_pks:
                        fields_name =filed.field_Name.strip().replace(' ',"_")
                        
                        if fields_name =='Volume':
                            fileds_data.append(fields_name)
                            fileds_data.append(f"{fields_name}_Type")
                            
                        elif fields_name =='Strength':
                            fileds_data.append(fields_name)
                            fileds_data.append(f"{fields_name}_Type")

                        elif fields_name =='Is_Reusable':
                            fileds_data.append(fields_name)
                            fileds_data.append("Re_Usable_Times")
                        elif fields_name =='Is_Sellable':
                            fileds_data.append(fields_name)
                            fileds_data.append('Least_Sellable_Unit')
                        
                            
                        elif fields_name =='Is_Perishable':
                            fileds_data.append(fields_name) 
                            fileds_data.append("Perishable_Duration") 
                            fileds_data.append("Perishable_Duration_Type") 
                        else :
                            fileds_data.append(fields_name)
            else:
                
                for filed in fileds:
                    if filed.pk <=4:
                        fields_name =filed.field_Name.replace(' ',"_")
                        fileds_data.append(fields_name)
                 
            # Return the data as JSON
            return JsonResponse(fileds_data, safe=False)
    else:
        return HttpResponse("Only GET method is allowed", status=405)
    



@csrf_exempt
def get_Drug_segments(request):
    if request.method == 'GET':
        # Fetch all unit records from the database
        segments = ProductMaster_Drug_Segment_Details.objects.filter(Status = True)

        # Prepare data as a list of dictionaries
        segments_data = []
        for seg in segments:
            segments_data.append({
                'id': seg.pk,
                'Segment': seg.Segment,
                'Description': seg.Description,
                'checked':False
            })

        # Return the data as JSON
        return JsonResponse(segments_data, safe=False)
    else:
        return HttpResponse("Only GET method is allowed", status=405)
    
    
# bharathi


@csrf_exempt
@require_http_methods(["GET", "OPTIONS"])
def Sub_Product_Category_Details_by_Product(request):
    if request.method == 'GET':
        try:
            Product = request.GET.get('ProductCategory')
            
            if not Product:
                return JsonResponse({'warn': 'Product Category not found'})
            SubProductCategory_Details = SubCategory_Detailes.objects.filter(ProductCategoryId=Product)
            print("SubProductCategory_Details",SubProductCategory_Details)

            Sub_ProductData = []
            for sub in SubProductCategory_Details:
                sub_dict = {
                    'id':sub.pk,
                    'SubCategoryName':sub.SubCategoryName,
                    'ProductCategoryId':sub.ProductCategoryId.pk,
                    'ProductCategory_Name':sub.ProductCategoryId.ProductCategory_Name,
                    'Status':'Active' if sub.Status else 'Inactive',

                }
                Sub_ProductData.append(sub_dict)
            return JsonResponse(Sub_ProductData, safe=False)


        except Exception as e:
            print(f"Error occurred: {e}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
    
    return JsonResponse({'error': 'Method not Allowed'}, status=405)


@csrf_exempt
@require_http_methods(["GET", "OPTIONS"])
def Items_by_ProductCategory_Details(request):
    if request.method == 'GET':
        try:
            Product = request.GET.get('ProductCategory')
            if not Product:
                return JsonResponse({'warn': 'Product Category not found'})
            
            Product_Items = Product_Master_All_Category_Details.objects.filter(ProductCategory=Product)
            print("Product_Items",Product_Items)
            Product_ItemData = []
            for item in Product_Items:
                item_dict = {
                    'id':item.pk,
                    'ItemName':item.ItemName,                    
                    'Status':item.Status,
                }
                Product_ItemData.append(item_dict)
            return JsonResponse(Product_ItemData, safe=False)


        except Exception as e:
            return JsonResponse({'warn': 'An internal server error occurred'}, status=500)
    
    return JsonResponse({'error': 'Method not Allowed'}, status=405)

@csrf_exempt
@require_http_methods(["GET"])
def Item_wise_supplier_getdata(request):
    if request.method == 'GET':
        try:
            ItemCode = request.GET.get('ItemCode', '')
            print("ItemCode", ItemCode)
            if not ItemCode:
                return JsonResponse({'warn': 'ItemCode not found'})
            
            # Get the supplier product details related to the ItemCode
            Supplier_Product_instance = Supplier_Product_Details.objects.filter(
                Product_Detials__pk=ItemCode
            ).order_by('Supplier_Detials__pk')

            # Dictionary to store final result
            list_supplier = {
                'data': [],
                'Suppliers': []
            }

            # Prepare a set of suppliers
            for sup_ins in Supplier_Product_instance:
                list_supplier['Suppliers'].append({
                    "id": sup_ins.Supplier_Detials.pk,
                    "Name": sup_ins.Supplier_Detials.Supplier_Name,
                })

            # List of amount types to loop over
            amount_types = ["PurchaseRateBeforeGST", "GST", "PurchaseRateAfterGST", "MRP"]
            amount_type_labels = {
                "PurchaseRateBeforeGST": "Purchase Rate Before GST",
                "GST": "GST",
                "PurchaseRateAfterGST": "Purchase Rate After GST",
                "MRP": "MRP",
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

            # Add DeliveryDuration as a separate row
            delivery_duration_dic = {
                'id': len(list_supplier['data']) + 1,
                'AmountType': "DeliveryDuration",
            }
            for sup_ins in Supplier_Product_instance:
                delivery_duration_dic[f"{str(sup_ins.Supplier_Detials.pk)}"] = sup_ins.Supplier_Detials.DeliveryDuration if sup_ins.Supplier_Detials.DeliveryDuration else 0

            list_supplier['data'].append(delivery_duration_dic)

            return JsonResponse(list_supplier, safe=False)
        except Exception as e:
            print("Error:", str(e))  # Log the error for debugging
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
@require_http_methods(["GET"])
def SupplierId_Supplier_Data_Get(request):
    if request.method == "GET":
        try:
            SupplierId = request.GET.get('SupplierId')
  
            if not SupplierId:
                return JsonResponse({'warn': "Supplier not found"})
            if SupplierId:
                Supplier_Master_instance=Supplier_Master_Details.objects.get(pk=SupplierId)
                dic={
                    'id':Supplier_Master_instance.Supplier_Id,
                    'SupplierName':Supplier_Master_instance.Supplier_Name,
                    'ContactPerson':Supplier_Master_instance.Contact_Person,
                    'ContactNumber':Supplier_Master_instance.Contact_Number,
                    'EmailAddress':Supplier_Master_instance.Email_Address,
                    'LeadTime':Supplier_Master_instance.DeliveryDuration,
                }
                return JsonResponse(dic,safe=False)


        except Exception as e:
            return JsonResponse({'warn':'An internal server error occurred'}, status=500)

    
    return JsonResponse({'warn': 'Invalid Method'}, status=405)

# PO_SupplierWise_Item_Get

@csrf_exempt
@require_http_methods(["GET"])
def PO_SupplierWise_Item_Get(request):
    try:
        # Extract parameters
        SupplierId = request.GET.get('SupplierId')
        POitems = request.GET.get('POitems')

        # Debugging logs
        print("SupplierId:", SupplierId)
        print("POitems:", POitems)
        Item_Array = []

        # Validate parameters
        if not SupplierId or not POitems:
            return JsonResponse({'warn': 'Both SupplierId and item are required'}, status=400)

        # Fetch supplier product details
        Supplier_Product_Inst = Supplier_Product_Details.objects.filter(
            Supplier_Detials__Supplier_Id=SupplierId,
            Product_Detials__pk=POitems,
            Status=True
        )

        if not Supplier_Product_Inst.exists():
            return JsonResponse(Item_Array, safe=False)

        # Process each product detail
        for row in Supplier_Product_Inst:
            item_Dec = {
                'itemCode': row.Product_Detials.pk,
                'itemName': row.Product_Detials.ItemName,
                'ProductCategory': row.Product_Detials.ProductCategory.ProductCategory_Name if row.Product_Detials.ProductCategory else None,
                'SubCategory': row.Product_Detials.SubCategory.SubCategoryName if row.Product_Detials.SubCategory else None,
            }

            # Fetch rate details
            Get_Rate_Inst = Supplier_Product_Amount_Details.objects.filter(
                Supplier_detials=row,
                Supplier_detials__Product_Detials=row.Product_Detials
            ).order_by('-Created_at').first()

            # Optional fields
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
            if row.Product_Detials.Is_Manufacture_Date_Available is not None:
                item_Dec['Is_Manufacture_Date_Available'] = row.Product_Detials.Is_Manufacture_Date_Available
            if row.Product_Detials.Is_Expiry_Date_Available is not None:
                item_Dec['Is_Expiry_Date_Available'] = row.Product_Detials.Is_Expiry_Date_Available

            # Safely check and assign 'IsSellable'
            if row.Product_Detials.IsSellable is not None:
                item_Dec['IsSellable'] = 'Yes' if row.Product_Detials.IsSellable else 'No'
                if row.Product_Detials.IsSellable:
                    item_Dec['LeastSellableUnit'] = row.Product_Detials.LeastSellableUnit

            # Add rate details
            if Get_Rate_Inst:
                item_Dec['MRP'] = Get_Rate_Inst.MRP
                item_Dec['PurchaseRateBeforeGST'] = Get_Rate_Inst.PurchaseRateBeforeGST
                item_Dec['GST'] = Get_Rate_Inst.GST
                item_Dec['PurchaseRateAfterGST'] = Get_Rate_Inst.PurchaseRateAfterGST

            Item_Array.append(item_Dec)

        return JsonResponse(Item_Array, safe=False)

    except Exception as e:
        print("Error:", str(e))  # Detailed logging for debugging
        return JsonResponse({'warn': 'An internal server error occurred'}, status=500)
