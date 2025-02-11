from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from Masters.models import NurseStationMaster,Inventory_Location_Master_Detials,Location_Detials,Inventory_Page_Access_Detailes
from .models import (
    Product_Category_Product_Details,Product_Master_All_Category_Details,
    
    Indent_raise_details_table,Indent_raise_items_details_table,
    Indent_issue_details_table,Indent_issue_items_details_table,
    Indent_receive_details_table,Indent_receive_items_details_table,
    Stock_Maintance_Table_Detials,
    SerialNumber_Stock_Maintance_Table_Detials)
from django.db.models import  Q
import json
from django.db import transaction
from .GoodsReceiptNote import get_or_none,to_integer
from django.utils import timezone
from datetime import datetime



def get_ward_store_detials_by_loc(request):
    try:
        Location = request.GET.get('Location')
        IsFromWardStore =request.GET.get('IsFromWardStore','true') == 'true'
        
        
        print('llll---',Location,IsFromWardStore)

        if not Location:
            return JsonResponse({'error': 'Location is required'}, status=400)
        
        response_data = []
        if IsFromWardStore:
            # Base query for WardType_Master_Details
            dataa_ins = NurseStationMaster.objects.filter(
                Status=True,
                Location_Name__pk =Location
            )
            for ins in dataa_ins:
                dict_dat={
                    'id':ins.pk,
                    'NurseStation':ins.NurseStationName,
                    'BuildingName':ins.Building_Name.Building_Name,
                    'BlockName':ins.Block_Name.Block_Name,
                    'FloorName':ins.Floor_Name.Floor_Name,
                  
                }
                response_data.append(dict_dat)
        else:
            dataa_ins = Inventory_Location_Master_Detials.objects.filter(
                Status =True,
                Location_Name__pk = Location
            )
            for ins in dataa_ins:
                dict_dat={
                    'id':ins.pk,
                    'StoreName':ins.Store_Name,
                    'BuildingName':ins.Building_Name.Building_Name,
                    'BlockName':ins.Block_Name.Block_Name,
                    'FloorName':ins.Floor_Name.Floor_Name,
                  
                }
                response_data.append(dict_dat)
        
        
        
        return JsonResponse(response_data, safe=False)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'An internal server error occurred'}, status=500)



@csrf_exempt
@require_http_methods(["GET"])
def get_item_detials_for_indent(request):
    if request.method == "GET":
        try:
            ItemCode = request.GET.get('ItemCode')
            ItemName = request.GET.get('ItemName')
            filtercondition=Q()
            if ItemCode:
                filtercondition &= Q(pk__icontains=ItemCode)
            if ItemName:
                filtercondition &= Q(ItemName__icontains=ItemName)
                
            product_ins = Product_Master_All_Category_Details.objects.filter(Status=True).filter(filtercondition)[:10]
            productlist=[]
            for ins in product_ins:
               
                product_field_names = Product_Category_Product_Details.objects.get(pk = ins.SubCategory.ProductCategoryId.pk).Product_fields.values_list('field_Name',flat=True)
             
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
@require_http_methods(["POST", "OPTIONS", "GET"])
def post_indent_raise_details(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print('data',data)
            pk = data.get('pk')
            RequestFromLocation = data.get('RequestFromLocation', None)
            RequestFromNurseStation = data.get('RequestFromNurseStation', False)
            RequestFromStore = data.get('RequestFromStore', None)
            RequestToLocation = data.get('RequestToLocation', None)
            RequestToNurseStation = data.get('RequestToNurseStation', False)
            RequestToStore = data.get('RequestToStore', None)
            RequestDate = data.get('RequestDate', None)
            Reason = data.get('Reason', '')
            Created_by = data.get('Created_by', '')
            IndentItemsList = data.get('IndentItemsList', [])
            approval_status = 'Raised'
            # Initialize variables for storing instances
            RequestFromLocation_ins = None
            RequestFromStore_Nurse_ins = None
            RequestFromStore_ins = None
            
            RequestToLocation_ins = None
            RequestToStore_Nurse_ins = None
            RequestToStore_ins = None


            # Get instances if present
            if RequestFromLocation:
                RequestFromLocation_ins = get_or_none(Location_Detials, RequestFromLocation)
                if RequestFromLocation_ins:
                    inv_page_access = Inventory_Page_Access_Detailes.objects.get(Access_StoreId__pk = RequestFromLocation_ins.pk)
                    if inv_page_access:
                        if inv_page_access.IS_Indent:
                            if inv_page_access.IS_Indent_Raise_Approve:
                                approval_status ='Raised' if inv_page_access.IS_Indent_Raise_Approve else 'Approved'
           
            if RequestFromStore:
                if RequestFromNurseStation:
                    RequestFromStore_Nurse_ins = get_or_none(NurseStationMaster, RequestFromStore)
                else:
                    RequestFromStore_ins = get_or_none(Inventory_Location_Master_Detials, RequestFromStore)
            
            if RequestToLocation:
                RequestToLocation_ins = get_or_none(Location_Detials, RequestToLocation)
           
            if RequestToStore:
                if RequestToNurseStation:
                    RequestToStore_Nurse_ins = get_or_none(NurseStationMaster, RequestToStore)
                else:
                    RequestToStore_ins = get_or_none(Inventory_Location_Master_Detials, RequestToStore)
            
            with transaction.atomic():
                # Update case
                # Get current date and time
                current_date_time = datetime.now()

                # Format as 'yyyy-MM-dd hh:mm am/pm'
                formatted_date_time = current_date_time.strftime('%Y-%m-%d %H:%M')

                indent_data={
                    'Raise_From_Location':RequestFromLocation_ins,
                    'Raise_From_NurseStation_Store':RequestFromNurseStation,
                    'Raise_From_Store_Location':RequestFromStore_ins,
                    'Raise_From_NurseStation_Location':RequestFromStore_Nurse_ins,
                    'Raise_To_Location':RequestToLocation_ins,
                    'Raise_To_NurseStation_Store':RequestToNurseStation,
                    'Raise_To_Store_Location':RequestToStore_ins,
                    'Raise_To_NurseStation_Location':RequestToStore_Nurse_ins,
                    'Raise_Date':formatted_date_time,
                    'Raise_Reason':Reason,
                    'Raise_by':Created_by,
                    'Raise_Status': approval_status
                }


                if approval_status == 'Approved':
                    indent_data['Raise_Approved_by'] = Created_by
                    indent_data['Raise_ApprovedDate'] = formatted_date_time
                if pk:
                    indent_ins = get_or_none(Indent_raise_details_table,pk)
                    if indent_ins:
                        for key, value in indent_data.items():
                            if key =='Created_by':
                                setattr(indent_ins, 'Raise_Updated_by', value)
                            setattr(indent_ins, key, value)
                        indent_ins.save()
                   
                else:
                    indent_ins = Indent_raise_details_table.objects.create(**indent_data)
               
                # Handle indent items
                print('IndentItemsList',IndentItemsList)
                for ins in IndentItemsList:
                    item_pk = ins.get('pk')
                    Item_code_ins = get_or_none(Product_Master_All_Category_Details,ins.get('ItemCode'))
        
                    indent_items_data={
                        'Indent_Detials':indent_ins,
                        'Product_Detials':Item_code_ins,
                        'Raise_Quantity':ins.get('RaisedQuantity'),
                        'Reason':ins.get('Reason',''),
                        'Remarks':ins.get('Remarks',''),
                        'Raise_Status':approval_status,
                    }
                    
                    
                    # Update item case
                    if item_pk:
                        indent_item_ins = Indent_raise_items_details_table.objects.get(pk=item_pk)
                        if indent_item_ins:
                            for key, value in indent_items_data.items():
                                setattr(indent_item_ins, key, value)
                        indent_item_ins.save()
                    # Create item case
                    else:
                        Indent_raise_items_details_table.objects.create(**indent_items_data)
                        
            return JsonResponse({'success': 'Data saved successfully'}, status=200)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
        

    elif request.method == 'GET':

        Invoice_No = request.GET.get('Invoice_No')
        RaisedFromLocation = request.GET.get('RaisedFromLocation')
        RaisedFromNurseStation = request.GET.get('RaisedFromNurseStation','true').lower() == 'true'
        RaisedFromStore = request.GET.get('RaisedFromStore')
        RaisedToLocation = request.GET.get('RaisedToLocation')
        RaisedToNurseStation = request.GET.get('RaisedToNurseStation','true').lower() == 'true'
        RaisedToStore = request.GET.get('RaisedToStore')
        DateType = request.GET.get('DateType')
        CurrentDate = request.GET.get('CurrentDate')
        FromDate = request.GET.get('FromDate')
        ToDate = request.GET.get('ToDate')
        Status = request.GET.get('Status')
        print(RaisedFromNurseStation)
        print(RaisedToNurseStation)
        query=Q()
        
        if RaisedFromLocation :
            query &= Q(Raise_From_Location__pk = RaisedFromLocation)
            query &= Q(Raise_From_NurseStation_Store = RaisedFromNurseStation)
            
            if RaisedFromStore:
                if RaisedFromNurseStation:
                    query &= Q(Raise_From_NurseStation_Location__pk = RaisedFromStore)
                else:
                    query &= Q(Raise_From_Store_Location__pk = RaisedFromStore)
                
        if RaisedToLocation :
            query &= Q(Raise_To_Location__pk = RaisedToLocation)
            query &= Q(Raise_To_NurseStation_Store__pk = RaisedToNurseStation)
            
            if RaisedToStore:
                if RaisedToNurseStation:
                    query &= Q(Raise_To_NurseStation_Location__pk = RaisedToStore)
                else:
                    query &= Q(Raise_To_Store_Location__pk = RaisedToStore)
                
            
        if Invoice_No:
            query &= Q(pk__iexact = Invoice_No)
        
        if DateType == 'Current':
            if CurrentDate:
                # Parse the date from the frontend and apply the filter
                current_date_obj = datetime.strptime(CurrentDate, '%Y-%m-%d').date()
                query &= Q(Raise_Date=current_date_obj)

        if DateType == 'Customize':
            if FromDate and ToDate:
                # Parse the 'FromDate' and 'ToDate' from the frontend
                from_date_obj = datetime.strptime(FromDate, '%Y-%m-%d').date()
                to_date_obj = datetime.strptime(ToDate, '%Y-%m-%d').date()
                query &= Q(Raise_Date__range=(from_date_obj, to_date_obj))
        
        if Status:
            query &= Q(Raise_Status = Status)
        
        indent_table_ins = Indent_raise_details_table.objects.filter(query)
        
        responsedata=[]
        for index,ins in enumerate(indent_table_ins):
            dic={
                'id':index+1,
                'pk':ins.pk,
                'RaisedFromLocation_pk':ins.Raise_From_Location.pk if ins.Raise_From_Location else None,
                'RaisedFromLocation':ins.Raise_From_Location.Location_Name if ins.Raise_From_Location else None,
                'RaisedFromNurseStation':ins.Raise_From_NurseStation_Store,
                'RaisedFromNurseStation_pk':ins.Raise_From_NurseStation_Location.pk if ins.Raise_From_NurseStation_Store and ins.Raise_From_NurseStation_Location else '',
                'RaisedFromStoreNurseStation':ins.Raise_From_NurseStation_Location.NurseStationName if ins.Raise_From_NurseStation_Store and ins.Raise_From_NurseStation_Location else "",
                'RaisedFromStore_pk':ins.Raise_From_Store_Location.pk if not ins.Raise_From_NurseStation_Store and ins.Raise_From_Store_Location else '',
                'RaisedFromStore':ins.Raise_From_Store_Location.Store_Name if not ins.Raise_From_NurseStation_Store and ins.Raise_From_Store_Location else '',
                
                'RaisedToLocation_pk':ins.Raise_To_Location.pk if ins.Raise_To_Location else None,
                'RaisedToLocation':ins.Raise_To_Location.Location_Name if ins.Raise_To_Location else None,
                'RequestToNurseStation':ins.Raise_To_NurseStation_Store,
                'RaisedToStoreNurseStation_pk':ins.Raise_To_NurseStation_Location.pk if ins.Raise_To_NurseStation_Store and ins.Raise_To_NurseStation_Location else '',
                'RaisedToStoreNurseStation':ins.Raise_To_NurseStation_Location.NurseStationName if ins.Raise_To_NurseStation_Store and ins.Raise_To_NurseStation_Location else '',
                'RaisedToStore_pk':ins.Raise_To_Store_Location.pk if not ins.Raise_To_NurseStation_Store and ins.Raise_To_Store_Location else '',
                'RaisedToStore':ins.Raise_To_Store_Location.Store_Name if not ins.Raise_To_NurseStation_Store and ins.Raise_To_Store_Location else '',
             
                'RaisedDate':ins.Raise_Date.strftime('%Y-%m-%d') if ins.Raise_Date else None,
                'RaisedApprovedDate':ins.Raise_ApprovedDate.strftime('%Y-%m-%d') if ins.Raise_ApprovedDate else None,
                'Raised_by':ins.Raise_by,
                'RaisedApproved_by':ins.Raise_Approved_by,
                'RaisedReason':ins.Raise_Reason,
                
               
                'Raise_Status':ins.Raise_Status,
                'Issue_Status':ins.Issue_Status,
              
                'Item_Detials':[]
            }
            
            

            Items_filter_query = Q(Indent_Detials__pk=ins.pk)

            
            indent_item_data_ins = Indent_raise_items_details_table.objects.filter(Items_filter_query)
            for it_index,it_ins in enumerate(indent_item_data_ins):
                item_dic={
                    'id':it_index +1,
                    'pk':it_ins.pk,
                    "ItemCode": it_ins.Product_Detials.pk,
                    "ItemName": it_ins.Product_Detials.ItemName,
                    "ProductCategory":it_ins.Product_Detials.SubCategory.ProductCategoryId.ProductCategory_Name,
                    "SubCategory": it_ins.Product_Detials.SubCategory.SubCategoryName,
                    'PackType': it_ins.Product_Detials.PackType.PackType_Name if it_ins.Product_Detials.PackType else 'Nill',
                    'PackQuantity': it_ins.Product_Detials.PackQty if it_ins.Product_Detials.PackQty else 'Nill',
                    'RaisedQuantity':it_ins.Raise_Quantity,
                    'IssuedQuantity':it_ins.Issue_Quantity,
                    'IssueQuantity':it_ins.Issue_Quantity,
                    'PendingQuantity':it_ins.Pending_Quantity,
                    'RaisedReason':it_ins.Reason,
                    'RaisedRemarks':it_ins.Remarks,
                    'Raise_Status':it_ins.Raise_Status,
                    'Issue_Status':it_ins.Issue_Status,
                    'Status':it_ins.Issue_Status

                }
                dic['Item_Detials'].append(item_dic)
            responsedata.append(dic)
        return JsonResponse (responsedata,safe=False)   
    
    
    else:
        return JsonResponse({'error': f'An error occurred: Request method not allowed'}, status=405)
    





@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def Indent_Raise_Details_Approve_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            InvoiceNo = data.get('InvoiceNo')
            Status = data.get('Status','Approved')
            Approved_by = data.get('Approved_by', '')
            
            if InvoiceNo:
                try:
                    indent_table_ins = Indent_raise_details_table.objects.get(pk=InvoiceNo)
                except :
                    return JsonResponse({'error': 'Invoice not found'}, status=404)
                
                indent_table_ins.Raise_Status = Status
                indent_table_ins.Raise_Approved_by = Approved_by
                indent_table_ins.save()

                 # Fetch related GRN_Product_Item_Detials instances
                product_items = Indent_raise_items_details_table.objects.filter(Indent_Detials=indent_table_ins, Raise_Status='Raised')

                # Iterate and update each item to trigger the post_save signal
                for item in product_items:
                    item.Raise_Status = Status
                    item.save()  
                
                return JsonResponse({'success': 'Indent Raise approved successfully'}, status=200)
            
            return JsonResponse({'error': 'InvoiceNo is required'}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_item_detials_for_batch_indent_issue(request):
    if request.method == "GET":
        try:
            ItemCode = request.GET.get('ItemCode')
            Location = request.GET.get('Location')
            Isward = request.GET.get('Isward','').lower()
            StoreName = request.GET.get('StoreName')
            ExpiredProducts = request.GET.get('ExpiredProducts','false').lower()
            filter_query =Q()
            if ItemCode:
                filter_query &= Q(Product_Detials__pk__iexact = ItemCode)
            if Location:
                filter_query &= Q(Store_location__Location_Name__pk__iexact = Location) | Q(NurseStation_location__Location_Name__pk__iexact = Location)
            if Isward:
                if StoreName:
                    if Isward =='true':
                        filter_query &= Q( NurseStation_location__pk__iexact = StoreName,IsNurseStation = True )
                    else: 
                        filter_query &= Q( Store_location__pk__iexact = StoreName,IsNurseStation = False )
            if ExpiredProducts ==  'true':
                filter_query &= ~Q(Expiry_Status='Not-Expired')
            if not ItemCode:
                return JsonResponse({'error': 'ItemCode Is required'}, status=400)
                
            product_ins = Stock_Maintance_Table_Detials.objects.filter(filter_query)
            productlist=[]
            for ins in product_ins:
                data = {
                    'pk': ins.pk,
                    'ItemCode': ins.Product_Detials.pk,
                    'ItemName': ins.Product_Detials.ItemName,
                    'SerialNoAvailable': ins.Product_Detials.Is_Serial_No_Available_for_each_quantity,
                    'BatchNo': ins.Batch_No,
                    'AvailableQuantity': ins.AvailableQuantity,
                    'IsSellable':ins.Product_Detials.IsSellable,
                    'LeastSellableUnit':ins.Product_Detials.LeastSellableUnit,
                    'Sellable_price':ins.Sellable_price,
                    'Sellable_qty_price':ins.Sellable_qty_price,
                }
                productlist.append(data)
            return JsonResponse(productlist, safe=False)
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
    else:
        return JsonResponse({'error': f'An error occurred: Request method not allowed'}, status=500)

 
@csrf_exempt
@require_http_methods(["GET"])
def get_serialno_detials_for_batch_indent_issue(request):
    if request.method == "GET":
        try:
            ItemCode = request.GET.get('ItemCode')
            Location = request.GET.get('Location')
            Isward = request.GET.get('Isward','').lower()
            StoreName = request.GET.get('StoreName')
            BatchNo = request.GET.get('BatchNo')
            
            filter_query =Q(Item_Status ='Available')
            if ItemCode:
                filter_query &= Q(Stock_Table__Product_Detials__pk__iexact = ItemCode)
            if BatchNo:
                filter_query &= Q(Stock_Table__Batch_No = BatchNo)
            if Location:
                filter_query &= Q(Stock_Table__Store_location__Location_Name__pk__iexact = Location) | Q(Stock_Table__NurseStation_location__Location_Name__pk__iexact = Location)
            if Isward:
                if StoreName:
                    if Isward =='true':
                        filter_query &= Q( Stock_Table__NurseStation_location__pk__iexact = StoreName,IsNurseStation = True )
                    else: 
                        filter_query &= Q( Stock_Table__Store_location__pk__iexact = StoreName,IsNurseStation = False )
            
            if not ItemCode:
                return JsonResponse({'error': 'ItemCode Is required'}, status=400)
                
            serialNo_ins = SerialNumber_Stock_Maintance_Table_Detials.objects.filter(filter_query)
            serialNo_ins_list=[]
            for ins_indx,ins in enumerate(serialNo_ins):
                data = {
                    'pk': ins.pk,
                    'Serial_Number': ins.Serial_Number,
                    "Status": False,
                    'Item_Status': ins.Item_Status,
                }
                serialNo_ins_list.append(data)
            return JsonResponse(serialNo_ins_list, safe=False)
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
    else:
        return JsonResponse({'error': f'An error occurred: Request method not allowed'}, status=500)


@csrf_exempt
@require_http_methods(["POST", 'GET', 'OPTIONS'])
def post_indent_issue_details(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            
            # Extract main data fields from request
            IndentRaiseInvoice = data.get("IndentRaiseInvoice", None)
            IndentIssueInvoice = data.get("IndentIssueInvoice", None)
            IssueFromLocation = data.get("IssueFromLocation")
            IssueFromNurseStation = data.get("IssueFromNurseStation")
            IssueFromStore = data.get("IssueFromStore")
            IssueToLocation = data.get("IssueToLocation")
            IssueToNurseStation = data.get("IssueToNurseStation")
            IssueToStore = data.get("IssueToStore")
            IssueReason = data.get("IssueReason", '')
            print("IssueReason",IssueReason)
            createdBy = data.get("createdBy", '')
            ItemsData = data.get("ItemsData", [])

            # Initialize instances for locations and stores
            IssueFromLocation_ins = IssueFromNurseStation_ins = IssueFromInvStore_ins = None
            IssueToLocation_ins = IssueToNurseStation_ins = IssueToInvStore_ins = None
            approval_status = 'Issued'
            IndentRaiseInvoice_ins = None

            # Get indent raise instance
            if IndentRaiseInvoice:
                IndentRaiseInvoice_ins = get_or_none(Indent_raise_details_table, IndentRaiseInvoice)
            
            # Handle issue location instances for IssueFrom
            if IssueFromLocation:
                IssueFromLocation_ins = get_or_none(Location_Detials, IssueFromLocation)
                if IssueFromLocation_ins:
                    inv_page_access = Inventory_Page_Access_Detailes.objects.filter(Access_StoreId__pk=IssueFromLocation_ins.pk).first()
                    if inv_page_access and inv_page_access.IS_Indent:
                        approval_status = 'Issued' if inv_page_access.IS_Indent_Issue_Approve else 'Approved'
            
            # Handle ward and inventory store instances for IssueFrom
            if IssueFromStore:
                if IssueFromNurseStation:
                    IssueFromNurseStation_ins = get_or_none(NurseStationMaster, IssueFromStore)
                else:
                    IssueFromInvStore_ins = get_or_none(Inventory_Location_Master_Detials, IssueFromStore)
            
            # Handle issue location instances for IssueTo
            if IssueToLocation:
                IssueToLocation_ins = get_or_none(Location_Detials, IssueToLocation)
            
            # Handle ward and inventory store instances for IssueTo
            if IssueToStore:
                if IssueToNurseStation:
                    IssueToNurseStation_ins = get_or_none(NurseStationMaster, IssueToStore)
                else:
                    IssueToInvStore_ins = get_or_none(Inventory_Location_Master_Detials, IssueToStore)
            
            # Current datetime for issuing
            current_date_time = datetime.now()
            formatted_date_time = current_date_time.strftime('%Y-%m-%d %H:%M')

            # Begin transaction for atomic database operations
            with transaction.atomic():
                # Update or create All_Indent_Details record
                indent_data = {
                    'pk': IndentIssueInvoice,
                    'Indent_Type': 'raise' if IndentRaiseInvoice else "issue",
                    'Indent_raise': IndentRaiseInvoice_ins,
                    'Issue_From_Location': IssueFromLocation_ins,
                    'Issue_From_NurseStation_Store': IssueFromNurseStation,
                    'Issue_From_Store_Location': IssueFromInvStore_ins,
                    'Issue_From_NurseStation_Location': IssueFromNurseStation_ins,
                    'Issue_To_Location': IssueToLocation_ins,
                    'Issue_To_NurseStation_Store': IssueToNurseStation,
                    'Issue_To_Store_Location': IssueToInvStore_ins,
                    'Issue_To_NurseStation_Location': IssueToNurseStation_ins,
                    'Issue_Date': formatted_date_time,
                    'Issue_Reason': IssueReason,
                    'Issue_Status': approval_status,
                }
                
                # Set issue/updated by fields
                if indent_data['pk']:
                    indent_data['Issue_Updated_by'] = createdBy
                else:
                    indent_data['Issue_by'] = createdBy
                
                # Set approval fields if status is approved
                if approval_status == 'Approved':
                    indent_data.update({
                        'Issue_Approved_by': createdBy,
                        'Issue_ApprovedDate': formatted_date_time,
                    })

                # Save or update indent issue instance
                if indent_data['pk']:
                    indent_issue_ins = get_or_none(Indent_issue_details_table, indent_data['pk'])
                    if indent_issue_ins:
                        for key, value in indent_data.items():
                            setattr(indent_issue_ins, key, value)
                        indent_issue_ins.save()
                else:
                    indent_issue_ins = Indent_issue_details_table.objects.create(**indent_data)

                issue_messages = []
                for it_ins in ItemsData:
                    try:
                        item_code = it_ins.get('ItemCode')
                        IssueQuantity = int(it_ins.get('IssueQuantity'))
                        BatchNo = it_ins.get('BatchNo')
                        Serial_Number = it_ins.get('SerialNo', [])

                        product_ins = Product_Master_All_Category_Details.objects.get(pk=item_code)

                        stock_Ins = Stock_Maintance_Table_Detials.objects.get(
                            Product_Detials=product_ins,
                            Batch_No=BatchNo,
                            IsNurseStation=IssueFromNurseStation,
                            Store_location=IssueFromInvStore_ins,
                            NurseStation_location=IssueFromNurseStation_ins
                        )
                        
                        # Check stock availability
                        if stock_Ins.AvailableQuantity < IssueQuantity:
                            issue_messages.append(f"Insufficient stock for {product_ins.ItemName} (ItemCode: {item_code}). Available: {stock_Ins.AvailableQuantity}, Requested: {IssueQuantity}.")
                        print('1111')
                        print('1111', len(Serial_Number))
                        # Check serial number availability
                        if len(Serial_Number):
                            print('1222')
                            Serial_no_ins = []
                            for serial in Serial_Number:
                                serial_ins = SerialNumber_Stock_Maintance_Table_Detials.objects.get(
                                    pk=serial['pk'],
                                    Stock_Table=stock_Ins,
                                    Store_location=IssueFromInvStore_ins,
                                    NurseStation_location=IssueFromNurseStation_ins,
                                    Item_Status='Available'
                                )
                                print('12',serial_ins)
                                if serial_ins:
                                    Serial_no_ins.append({
                                        'serial_no':serial['pk'],
                                        'message': f" the serial no {serial['pk']} in the selected location "
                                    })
                            print('222',Serial_no_ins)
                            if len(Serial_no_ins) < IssueQuantity:
                                issue_messages.append(f"Insufficient serials for {product_ins.ItemName} (ItemCode: {item_code}). Available serials: {len(Serial_no_ins)}, Requested: {IssueQuantity}.")
                    
                    except Exception as e:
                        return JsonResponse({
                            'ItemCode': item_code,
                            'Issue': f"An error occurred: {str(e)}"
                        },status=400)
                
                if issue_messages:
                    return JsonResponse({
                        'warn': issue_messages
                    },status=400)
                
                print('ItemsData',ItemsData)

                for it_ins in ItemsData:
                    print('it_ins')
                    try:
                        Raisedpk = it_ins.get('Raisedpk')
                        Issuedpk = it_ins.get('Issuedpk')
                        item_code = it_ins.get('ItemCode')
                        IssueQuantity = int(it_ins.get('IssueQuantity'))
                        BatchNo = it_ins.get('BatchNo')
                        Reason = it_ins.get('Reason', '')
                        Remarks = it_ins.get('Remarks', '')
                        Serial_Number = it_ins.get('SerialNo', [])
                        Status = it_ins.get('Status', '')
                        if Status != 'Cancelled':
                            Status = approval_status
                        
                        # Fetch product and stock details
                        product_ins = Product_Master_All_Category_Details.objects.get(pk=item_code)
                        try:
                            stock_Ins = Stock_Maintance_Table_Detials.objects.get(
                                Product_Detials=product_ins,
                                Batch_No=BatchNo,
                                IsNurseStation=IssueFromNurseStation,
                                Store_location=IssueFromInvStore_ins,
                                NurseStation_location=IssueFromNurseStation_ins
                            )
                        except Exception as e :
                            return JsonResponse(f"Error fetching stock for ItemCode {item_code}, BatchNo {BatchNo}: {str(e)}",status=400)
                        print('///1')
                        Serial_no_ins = set()
                        for serial in Serial_Number:
                            serial_ins = SerialNumber_Stock_Maintance_Table_Detials.objects.filter(
                                pk=serial['pk'],
                                Stock_Table=stock_Ins,
                                Store_location=IssueFromInvStore_ins,
                                NurseStation_location=IssueFromNurseStation_ins
                            ).first()
                            print('///2')

                            if serial_ins:
                                Serial_no_ins.add(serial_ins)
                            print('///3')
                        print('///4',Serial_no_ins)
                        
                        # Prepare data for indent items
                        indent_items_data = {
                            'pk': Issuedpk,
                            'Indent_Raise_Item': get_or_none(Indent_raise_items_details_table, Raisedpk),
                            'Indent_Detials': indent_issue_ins,
                            'Product_Detials': product_ins,
                            'stock_Detials': stock_Ins,
                            'Issue_Quantity': 0 if  Status == 'Cancelled' else IssueQuantity,
                            'Issue_Status': Status,
                            'Reason': Reason,
                            'Remarks': Remarks,
                        }

                        # Save or update indent item instance
                        if indent_items_data['pk']:
                            print("indent_items_data['pk']",indent_items_data['pk'])
                            indent_issue_item_ins = get_or_none(Indent_issue_items_details_table, indent_items_data['pk'])
                            print('indent_issue_item_ins',indent_issue_item_ins)
                            if indent_issue_item_ins:
                                for key, value in indent_items_data.items():
                                    setattr(indent_issue_item_ins, key, value)
                                indent_issue_item_ins.save()
                        else:
                            indent_issue_item_ins = Indent_issue_items_details_table.objects.create(**indent_items_data)
                        
                        
                        
                        print('///6')
                        # Assign serial numbers to the many-to-many field
                        if Serial_no_ins:
                            indent_issue_item_ins.serialNo.set(Serial_no_ins)
                        print('///7')
                        
                        
                        if indent_issue_item_ins.Issue_Status == 'Approved':
                            print('///8')
                            stock = indent_issue_item_ins.stock_Detials
                            issue_quantity = indent_issue_item_ins.Issue_Quantity

                            # Update stock details
                            stock.AvailableQuantity -= issue_quantity
                            stock.Indent_Send_Quantity += issue_quantity
                            stock.Total_Moved_Quantity += issue_quantity
                            stock.save(update_fields=['AvailableQuantity', 'Indent_Send_Quantity', 'Total_Moved_Quantity'])
                            if indent_issue_item_ins.serialNo.exists():
                                # Update serial numbers for the issue item
                                serial_numbers_to_update = list(
                                    indent_issue_item_ins.serialNo.filter(
                                        Store_location=indent_issue_ins.Issue_From_Store_Location,
                                        NurseStation_location=indent_issue_ins.Issue_From_NurseStation_Location,
                                        Item_Status='Available'
                                    ).values_list('id', flat=True)[:issue_quantity]
                                )
                                # Update serial numbers in stock maintenance table
                                SerialNumber_Stock_Maintance_Table_Detials.objects.filter(
                                    pk__in=serial_numbers_to_update
                                ).update(Item_Status='Indent Movement')

                        if indent_issue_item_ins.Issue_Status == 'Cancelled':
                             # Update serial numbers for the issue item
                            if indent_issue_item_ins.serialNo.exists(): 
                                serial_numbers_to_update = list(
                                    indent_issue_item_ins.serialNo.filter(
                                        Store_location=indent_issue_ins.Issue_From_Store_Location,
                                        NurseStation_location=indent_issue_ins.Issue_From_NurseStation_Location,
                                        
                                    ).values_list('id', flat=True)[:indent_issue_item_ins.Issue_Quantity]
                                )
                                # Update serial numbers in stock maintenance table
                                SerialNumber_Stock_Maintance_Table_Detials.objects.filter(
                                    pk__in=serial_numbers_to_update
                                ).update(Item_Status='Available')

                        print('///9')
                        if indent_issue_item_ins.Indent_Raise_Item:
                            print('///10')
                            if indent_issue_item_ins.Issue_Status != 'Cancelled':
                                print('///11')
                                indent_raise_ins_indent = indent_issue_item_ins.Indent_Raise_Item
                                indent_raise_ins_indent.Issue_Quantity += indent_issue_item_ins.Issue_Quantity
                                indent_raise_ins_indent.Pending_Quantity = indent_raise_ins_indent.Pending_Quantity - indent_issue_item_ins.Issue_Quantity if indent_raise_ins_indent.Raise_Quantity > indent_raise_ins_indent.Issue_Quantity else 0
                                if indent_raise_ins_indent.Pending_Quantity == 0:
                                    indent_raise_ins_indent.Issue_Status = 'Completed'
                                elif indent_issue_item_ins.Issue_Quantity != 0:
                                    indent_raise_ins_indent.Issue_Status = 'Completed'
                                print('///12')
                            else:
                                print('///13')
                                indent_raise_ins_indent = indent_issue_item_ins.Indent_Raise_Item
                                indent_raise_ins_indent.Issue_Quantity = 0
                                indent_raise_ins_indent.Pending_Quantity = indent_raise_ins_indent.Raise_Quantity
                                indent_raise_ins_indent.Issue_Status = 'Cancelled'
                                print('///14')
                            indent_raise_ins_indent.save()
                        
                    except Exception as e:
                        return JsonResponse({
                            'ItemCode': item_code,
                            'Issue': f"An error occurred: {str(e)}"
                        },status=400)

                if indent_issue_ins.Indent_raise:
                    print('///15')
                    indent_issue_item_ins_12 = list(
                        Indent_issue_items_details_table.objects.exclude(
                            Issue_Status='Cancelled'
                        ).filter(
                            Indent_Raise_Item__Indent_Detials=indent_issue_ins.Indent_raise
                        ).values_list('Indent_Raise_Item', flat=True)
                    )
                    print('///15---',indent_issue_item_ins_12)
                    if indent_issue_item_ins_12:
                        print('///16')
                        indent_raise_update_ins = Indent_raise_items_details_table.objects.exclude(pk__in=indent_issue_item_ins_12)
                        for ins_ins in indent_raise_update_ins:
                            ins_ins.Issue_Status = 'Cancelled'
                            ins_ins.save()
                    print('///17')
                    indent_raise_items = Indent_raise_items_details_table.objects.filter(
                        Indent_Detials=indent_issue_ins.Indent_raise,
                        Raise_Status='Approved'
                    )
                    all_Cancelled = all(item.Issue_Status == 'Cancelled' for item in indent_raise_items)
                    print('///18')
                    if all_Cancelled:
                        indent_issue_ins.Indent_raise.Issue_Status = 'Cancelled'
                        indent_issue_ins.Issue_Status = 'Cancelled'
                    else:
                        indent_issue_ins.Indent_raise.Issue_Status = 'Completed'
                    print('///19')
                    indent_issue_ins.save()
                    indent_issue_ins.Indent_raise.save()

                # If no issues, save instances and return success
                return JsonResponse({
                    'status': 'Success',
                    'message': 'Indent issue details recorded successfully.'
                }, status=200)
 
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

    elif request.method == 'GET':
        try:
            # Extracting query parameters
            Indent_Type = request.GET.get('Indent_Type','raise').strip().lower()
            Raise_Invoice_No = request.GET.get('Raise_Invoice_No')
            Issue_Invoice_No = request.GET.get('Issue_Invoice_No')
            DateType = request.GET.get('DateType')
            CurrentDate = request.GET.get('CurrentDate')
            FromDate = request.GET.get('FromDate')
            ToDate = request.GET.get('ToDate')
            Status = request.GET.get('Status','waiting').strip()
            
            
            # Initialize query
            query = Q()
            indent_table = None

            # Choose table and apply filters based on Indent_Type and Status
            if Indent_Type == "raise" :
                # Filter `Indent_raise_details_table` for status 'Approved'
                indent_table = Indent_raise_details_table
                query &= Q(Raise_Status="Approved",Issue_Status = Status)
           
            else:
                # Filter `Indent_issue_details_table` for Indent_Type == 'direct' and status 'Pending'
                indent_table = Indent_issue_details_table
                query &= Q(Issue_Status=Status)

           

            # Add additional filters based on other parameters if provided
            if Indent_Type == 'issue':
                if Raise_Invoice_No:
                    query &= Q(pk__iexact=Raise_Invoice_No)
            else:
                if Raise_Invoice_No:
                    query &= Q(Indent_raise__pk__iexact=Raise_Invoice_No)
                if Issue_Invoice_No:
                    query &= Q(pk__iexact=Issue_Invoice_No)

            # Date filtering
            if DateType == 'Current' and CurrentDate:
                query &= Q(date=CurrentDate)
            elif DateType == 'Customize' and FromDate and ToDate:
                query &= Q(date__range=[FromDate, ToDate])
            print(indent_table)
            print(query)
            # Execute query on chosen table
            Indent_table_results = None
            if indent_table:
                Indent_table_results = indent_table.objects.filter(query)
                print('----',Indent_table_results)
            # Display results for debugging
            
            indent_inssue_datas=[]
            if Indent_table_results:
                for indx, ins in enumerate(Indent_table_results):
                    dic={
                        'id':indx+1,
                        'Item_Detials':[]
                    }
                    
                    if Indent_Type == "raise":
                        
                        dic['Raised_pk'] = ins.pk
                        dic['RaisedFromLocation_pk'] = ins.Raise_From_Location.pk if ins.Raise_From_Location else None
                        dic['RaisedFromLocation'] = ins.Raise_From_Location.Location_Name if ins.Raise_From_Location else None
                        dic['RaisedFromNurseStation'] = ins.Raise_From_NurseStation_Store
                        dic['RaisedFromNurseStation_pk'] = ins.Raise_From_NurseStation_Location.pk if ins.Raise_From_NurseStation_Store and ins.Raise_From_NurseStation_Location else ''
                        dic['RaisedFromNurseStationWard'] = ins.Raise_From_NurseStation_Location.NurseStationName if ins.Raise_From_NurseStation_Store and ins.Raise_From_NurseStation_Location else ""
                        dic['RaisedFromStore_pk'] = ins.Raise_From_Store_Location.pk if not ins.Raise_From_NurseStation_Store and ins.Raise_From_Store_Location else ''
                        dic['RaisedFromStore'] = ins.Raise_From_Store_Location.Store_Name if not ins.Raise_From_NurseStation_Store and ins.Raise_From_Store_Location else ''
                        dic['RaisedToLocation_pk'] = ins.Raise_To_Location.pk if ins.Raise_To_Location else None
                        dic['RaisedToLocation'] = ins.Raise_To_Location.Location_Name if ins.Raise_To_Location else None
                        dic['RaisedToNurseStation'] = ins.Raise_To_NurseStation_Store
                        dic['RaisedToNurseStation_pk'] = ins.Raise_To_NurseStation_Location.pk if ins.Raise_To_NurseStation_Store and ins.Raise_To_NurseStation_Location else ''
                        dic['RaisedToNurseStationWard'] = ins.Raise_To_NurseStation_Location.NurseStationName if ins.Raise_To_NurseStation_Store and ins.Raise_To_NurseStation_Location else ''
                        dic['RaisedToStore_pk'] = ins.Raise_To_Store_Location.pk if not ins.Raise_To_NurseStation_Store and ins.Raise_To_Store_Location else ''
                        dic['RaisedToStore'] = ins.Raise_To_Store_Location.Store_Name if not ins.Raise_To_NurseStation_Store and ins.Raise_To_Store_Location else ''
                        dic['RaisedDate'] = ins.Raise_Date.strftime('%Y-%m-%d') if ins.Raise_Date else None
                        dic['RaisedApprovedDate'] = ins.Raise_ApprovedDate.strftime('%Y-%m-%d %I:%M %p') if ins.Raise_ApprovedDate else None
                        dic['Raised_by'] = ins.Raise_by
                        dic['RaisedApproved_by'] = ins.Raise_Approved_by
                        dic['RaisedReason'] = ins.Raise_Reason
                        dic['Raise_Status'] = ins.Raise_Status
                        dic['Issue_Status'] = ins.Issue_Status
                        
                        indent_item_data_ins = Indent_raise_items_details_table.objects.filter(Indent_Detials__pk=ins.pk,Raise_Status='Approved')
                        
                        for it_index,it_ins in enumerate(indent_item_data_ins):
                            item_dic={
                                'id':it_index +1,
                                'pk':it_ins.pk,
                                "ItemCode": it_ins.Product_Detials.pk,
                                "ItemName": it_ins.Product_Detials.ItemName,
                                "ProductCategory":it_ins.Product_Detials.SubCategory.ProductCategoryId.ProductCategory_Name,
                                "SubCategory": it_ins.Product_Detials.SubCategory.SubCategoryName,
                                'PackType': it_ins.Product_Detials.PackType.PackType_Name if it_ins.Product_Detials.PackType else 'Nill',
                                'PackQuantity': it_ins.Product_Detials.PackQty if it_ins.Product_Detials.PackQty else 'Nill',
                                'RaisedQuantity':it_ins.Raise_Quantity,
                                'IssuedQuantity':it_ins.Issue_Quantity,
                                'PendingQuantity':it_ins.Pending_Quantity,
                                'RaisedReason':it_ins.Reason,
                                'RaisedRemarks':it_ins.Remarks,
                                'Raise_Status':it_ins.Raise_Status,
                                'Issue_Status':it_ins.Issue_Status
                            }
                            dic['Item_Detials'].append(item_dic)
                    
                    else:
                        
                        dic['Indent_Type'] = 'By Raise' if ins.Indent_Type =='raise' else 'Direct Issue'
                        dic['Issued_pk'] = ins.pk

                        if ins.Indent_Type =='raise':
                            Indent_raise_insss = ins.Indent_raise
                            dic['Raised_pk'] = Indent_raise_insss.pk if Indent_raise_insss else None
                            dic['RaisedFromLocation_pk'] = Indent_raise_insss.Raise_From_Location.pk if Indent_raise_insss and Indent_raise_insss.Raise_From_Location else None
                            dic['RaisedFromLocation'] = Indent_raise_insss.Raise_From_Location.Location_Name if Indent_raise_insss and Indent_raise_insss.Raise_From_Location else None
                            dic['RaisedFromNurseStation'] = Indent_raise_insss.Raise_From_NurseStation_Store
                            dic['RaisedFromNurseStation_pk'] = Indent_raise_insss.Raise_From_NurseStation_Location.pk if Indent_raise_insss and Indent_raise_insss.Raise_From_NurseStation_Store and Indent_raise_insss.Raise_From_NurseStation_Location else ''
                            dic['RaisedFromNurseStationWard'] = Indent_raise_insss.Raise_From_NurseStation_Location.NurseStationName if Indent_raise_insss and Indent_raise_insss.Raise_From_NurseStation_Store and Indent_raise_insss.Raise_From_NurseStation_Location else ""
                            dic['RaisedFromStore_pk'] = Indent_raise_insss.Raise_From_Store_Location.pk if Indent_raise_insss and not Indent_raise_insss.Raise_From_NurseStation_Store and Indent_raise_insss.Raise_From_Store_Location else ''
                            dic['RaisedFromStore'] = Indent_raise_insss.Raise_From_Store_Location.Store_Name if Indent_raise_insss and not Indent_raise_insss.Raise_From_NurseStation_Store and Indent_raise_insss.Raise_From_Store_Location else ''
                           
                            dic['RaisedToLocation_pk'] = Indent_raise_insss.Raise_To_Location.pk if Indent_raise_insss and Indent_raise_insss.Raise_To_Location else None
                            dic['RaisedToLocation'] = Indent_raise_insss.Raise_To_Location.Location_Name if Indent_raise_insss and Indent_raise_insss.Raise_To_Location else None
                            dic['RaisedToNurseStation'] = Indent_raise_insss.Raise_To_NurseStation_Store
                            dic['RaisedToNurseStation_pk'] = Indent_raise_insss.Raise_To_NurseStation_Location.pk if Indent_raise_insss and Indent_raise_insss.Raise_To_NurseStation_Store and Indent_raise_insss.Raise_To_NurseStation_Location else ''
                            dic['RaisedToNurseStationWard'] = Indent_raise_insss.Raise_To_NurseStation_Location.NurseStationName if Indent_raise_insss and Indent_raise_insss.Raise_To_NurseStation_Store and Indent_raise_insss.Raise_To_NurseStation_Location else ''
                            dic['RaisedToStore_pk'] = Indent_raise_insss.Raise_To_Store_Location.pk if Indent_raise_insss and not Indent_raise_insss.Raise_To_NurseStation_Store and Indent_raise_insss.Raise_To_Store_Location else ''
                            dic['RaisedToStore'] = Indent_raise_insss.Raise_To_Store_Location.Store_Name if Indent_raise_insss and not Indent_raise_insss.Raise_To_NurseStation_Store and Indent_raise_insss.Raise_To_Store_Location else ''
                            
                            dic['RaisedDate'] = Indent_raise_insss.Raise_Date.strftime('%Y-%m-%d') if Indent_raise_insss and Indent_raise_insss.Raise_Date else None
                            dic['RaisedApprovedDate'] = Indent_raise_insss.Raise_ApprovedDate.strftime('%Y-%m-%d') if Indent_raise_insss and Indent_raise_insss.Raise_ApprovedDate else None
                            dic['Raised_by'] = Indent_raise_insss.Raise_by
                            dic['RaisedApproved_by'] = Indent_raise_insss.Raise_Approved_by
                            dic['RaisedReason'] = Indent_raise_insss.Raise_Reason
                            dic['Raise_Status'] = Indent_raise_insss.Raise_Status
                            dic['Issue_Status'] = Indent_raise_insss.Issue_Status
                        
                        dic['IssuedFromLocation_pk'] = ins.Issue_From_Location.pk if ins.Issue_From_Location else None
                        dic['IssuedFromLocation'] = ins.Issue_From_Location.Location_Name if ins.Issue_From_Location else None
                        dic['IssuedFromNurseStation'] = ins.Issue_From_NurseStation_Store
                        dic['IssuedFromNurseStation_pk'] = ins.Issue_From_NurseStation_Location.pk if ins.Issue_From_NurseStation_Store and ins.Issue_From_NurseStation_Location else ''
                        dic['IssuedFromNurseStationWard'] = ins.Issue_From_NurseStation_Location.NurseStationName if ins.Issue_From_NurseStation_Store and ins.Issue_From_NurseStation_Location else ""
                        dic['IssuedFromStore_pk'] = ins.Issue_From_Store_Location.pk if not ins.Issue_From_NurseStation_Store and ins.Issue_From_Store_Location else ''
                        dic['IssuedFromStore'] = ins.Issue_From_Store_Location.Store_Name if not ins.Issue_From_NurseStation_Store and ins.Issue_From_Store_Location else ''
                        
                        dic['IssuedToLocation_pk'] = ins.Issue_To_Location.pk if ins.Issue_To_Location else None
                        dic['IssuedToLocation'] = ins.Issue_To_Location.Location_Name if ins.Issue_To_Location else None
                        dic['IssuedToNurseStation'] = ins.Issue_To_NurseStation_Store
                        dic['IssuedToNurseStation_pk'] = ins.Issue_To_NurseStation_Location.pk if ins.Issue_To_NurseStation_Store and ins.Issue_To_NurseStation_Location else ''
                        dic['IssuedToNurseStationWard'] = ins.Issue_To_NurseStation_Location.NurseStationName if ins.Issue_To_NurseStation_Store and ins.Issue_To_NurseStation_Location else ''
                        dic['IssuedToStore_pk'] = ins.Issue_To_Store_Location.pk if not ins.Issue_To_NurseStation_Store and ins.Issue_To_Store_Location else ''
                        dic['IssuedToStore'] = ins.Issue_To_Store_Location.Store_Name if not ins.Issue_To_NurseStation_Store and ins.Issue_To_Store_Location else ''
                        
                        
                        dic['IssuedDate'] = ins.Issue_Date.strftime('%Y-%m-%d') if ins.Issue_Date else None
                        dic['IssuedApprovedDate'] = ins.Issue_ApprovedDate.strftime('%Y-%m-%d') if ins.Issue_ApprovedDate else None
                        dic['Issued_by'] = ins.Issue_by
                        dic['IssuedApproved_by'] = ins.Issue_Approved_by
                        dic['IssuedReason'] = ins.Issue_Reason
                        dic['Status'] = ins.Issue_Status
                        
                        indent_item_data_ins = Indent_issue_items_details_table.objects.filter(Indent_Detials__pk=ins.pk)
                        for it_index,it_ins in enumerate(indent_item_data_ins):
                            item_dic={
                                'id':it_index +1,
                                'Raisedpk':it_ins.Indent_Raise_Item.pk if it_ins.Indent_Raise_Item else None,
                                'Issuedpk':it_ins.pk,
                                "ItemCode": it_ins.Product_Detials.pk,
                                "ItemName": it_ins.Product_Detials.ItemName,
                                "ProductCategory":it_ins.Product_Detials.SubCategory.ProductCategoryId.ProductCategory_Name,
                                "SubCategory": it_ins.Product_Detials.SubCategory.SubCategoryName,
                                'PackType': it_ins.Product_Detials.PackType.PackType_Name if it_ins.Product_Detials.PackType else 'Nill',
                                'PackQuantity': it_ins.Product_Detials.PackQty if it_ins.Product_Detials.PackQty else 'Nill',
                                'Reason':it_ins.Reason,
                                'BatchNo':it_ins.stock_Detials.Batch_No,
                                'AvailableQuantity':it_ins.stock_Detials.AvailableQuantity,
                                'IssuedQuantity':it_ins.Issue_Quantity,
                                'IssueQuantity':it_ins.Issue_Quantity,
                                'Remarks':it_ins.Remarks,
                                'Issue_Status':it_ins.Issue_Status,
                                'Status':it_ins.Issue_Status,
                                'SerialNoAvailable':it_ins.stock_Detials.Is_Serial_No_Available_for_each_quantity
                            }
                            if item_dic['SerialNoAvailable'] and it_ins.serialNo.exists():

                                print('123333')
                                item_dic['SerialNo'] = []
                                for serial in it_ins.serialNo.all():
                                    print('serial',serial)
                                    print('serial',serial.pk)
                                   
                                    print('121212')
                                    dattt= {
                                        'pk': serial.pk,
                                        'Serial_Number': serial.Serial_Number,
                                        "Status": True,
                                        'Item_Status': serial.Item_Status,
                                    }
                                    item_dic['SerialNo'].append(dattt)
                                    print('0000')
                                serial_status = all(item.get('Item_Status') == 'Available' for item in item_dic['SerialNo'])
                                if not serial_status:
                                    item_dic['SerialNo'] = []
                                    item_dic['SerialNo_status'] = False
                                else:
                                    item_dic['SerialNo_status'] = True
                                
                            if it_ins.Indent_Raise_Item:
                                item_dic['RaisedQuantity'] = it_ins.Indent_Raise_Item.Raise_Quantity
                                item_dic['PendingQuantity'] = it_ins.Indent_Raise_Item.Pending_Quantity
                            dic['Item_Detials'].append(item_dic)
                    indent_inssue_datas.append(dic)
                    
            return JsonResponse(indent_inssue_datas, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)   




@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def Indent_Issue_Details_Approve_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            indent_type = data.get('IndentType')
            invoice_no = data.get('InvoiceNo')
            status = data.get('Status')
            approved_by = data.get('Approved_by', '')

            if not invoice_no:
                return JsonResponse({'error': 'InvoiceNo is required'}, status=400)
            current_date_time = datetime.now()
            formatted_date_time = current_date_time.strftime('%Y-%m-%d %H:%M')

            with transaction.atomic():
                if indent_type == 'raise':
                    # Process for Indent Raise
                    try:
                        indent_instance = Indent_raise_details_table.objects.get(pk=invoice_no)
                    except Indent_raise_details_table.DoesNotExist:
                        return JsonResponse({'error': 'Indent raise entry not found'}, status=404)

                    

                    # Update related items
                    related_items = Indent_raise_items_details_table.objects.filter(
                        Indent_Detials=indent_instance,
                        Raise_Status='Approved'
                    )
                    for item in related_items:
                        item.Issue_Status = status
                        item.save()

                    
                    indent_instance.Issue_Status = status
                    indent_instance.Raise_ApprovedDate = formatted_date_time
                    indent_instance.Raise_Approved_by = approved_by
                    indent_instance.save()
                    
                    return JsonResponse({'success': f'Indent Raise {status} successfully'}, status=200)

                elif indent_type == 'issue':
                    # Process for Indent Issue
                    try:
                        indent_instance = Indent_issue_details_table.objects.get(pk=invoice_no)
                    except Indent_issue_details_table.DoesNotExist:
                        return JsonResponse({'error': 'Indent issue entry not found'}, status=404)

                    

                    # Update related items
                    related_items = Indent_issue_items_details_table.objects.filter(
                        Indent_Detials=indent_instance,
                        Issue_Status='Issued'
                    )
                    issue_messages =[]
                    for item in related_items:
                        try:
                            product_ins = item.Product_Detials
                            IssueQuantity = item.Issue_Quantity
                            stock_Ins = item.stock_Detials
                            serial_no =  item.serialNo
                            issue_parent_ins = item.Indent_Detials
                            if stock_Ins.AvailableQuantity < IssueQuantity:
                                issue_messages.append(f"Insufficient stock for {product_ins.ItemName} (ItemCode: {product_ins.pk}). Available: {stock_Ins.AvailableQuantity}, Requested: {IssueQuantity}.")

                            if serial_no.exists():
                                Serial_no_ins = serial_no.filter(Item_Status='Available')

                                if len(Serial_no_ins) < IssueQuantity:
                                    issue_messages.append(f"Insufficient serials for {product_ins.ItemName} (ItemCode: {product_ins.pk}). Available serials: {len(Serial_no_ins)}, Requested: {IssueQuantity}.")
                        
                        except Exception as e:
                            print(f"An error occurred: {str(e)}")
                            return JsonResponse({'error': 'An internal server error occurred'}, status=500)   
                    if issue_messages:
                        return JsonResponse({
                            'warn': issue_messages
                        })
                    for item in related_items:
                        item.Issue_Status = status
                        item.save()
                    # Check if status is approved and update stock and serial numbers
                        if item.Issue_Status == 'Approved':
                            stock = item.stock_Detials
                            issue_quantity = item.Issue_Quantity

                            # Update stock details
                            stock.AvailableQuantity -= issue_quantity
                            stock.Indent_Send_Quantity += issue_quantity
                            stock.Total_Moved_Quantity += issue_quantity
                            stock.save(update_fields=['AvailableQuantity', 'Indent_Send_Quantity', 'Total_Moved_Quantity'])

                            # Update serial numbers for the issue item

                            serial_numbers_to_update = list(
                                item.serialNo.filter(
                                    Store_location=indent_instance.Issue_From_Store_Location,
                                    NurseStation_location=indent_instance.Issue_From_NurseStation_Location,
                                    Item_Status='Available'
                                ).values_list('id', flat=True)[:issue_quantity]
                            )
                            # Update serial numbers in stock maintenance table

                            
                            SerialNumber_Stock_Maintance_Table_Detials.objects.filter(
                                id__in=serial_numbers_to_update
                            ).update(Item_Status='Indent Movement')
                    
                    indent_instance.Issue_Status = status
                    indent_instance.Issue_ApprovedDate = formatted_date_time
                    indent_instance.Issue_Approved_by = approved_by
                    indent_instance.save()
                    
                    return JsonResponse({'success': f'Indent Issue {status} successfully'}, status=200)

                else:
                    return JsonResponse({'error': 'Invalid IndentType provided'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)



@csrf_exempt
@require_http_methods(["GET","POST","OPTIONS"])
def Post_Indent_Receive_Details_link(request):
    if request.method == 'POST':
        try:

            data = json.loads(request.body)
            Received_pk = data.get('Received_pk')
            Issued_pk = data.get('Issued_pk')
            ReceivedReason = data.get('ReceivedReason')
            Items_Data = data.get('Items_Data')
            createdBy = data.get('createdBy')

            # print('data???????',data)

            approval_status = 'Received'
            Received_pk_ins = get_or_none(Indent_receive_details_table, Received_pk) if Received_pk else None
            Issued_pk_ins = get_or_none(Indent_issue_details_table, Issued_pk) if Issued_pk else None
            
            print('Received_pk_ins',Received_pk_ins)

            print('Issued_pk_ins',Issued_pk_ins)


    
            with transaction.atomic():
                current_date_time = datetime.now()
                formatted_date_time = current_date_time.strftime('%Y-%m-%d')

                indent_data = {
                    'pk': Received_pk_ins.pk if Received_pk_ins else None,
                    'Indent_issue': Issued_pk_ins,
                    'Receive_Date': formatted_date_time,
                    'Receive_Reason': ReceivedReason,
                    'Receive_Status': approval_status,
                }

                if indent_data['pk']:
                    indent_data['Receive_Updated_by'] = createdBy
                else:
                    indent_data['Receive_by'] = createdBy

                if approval_status == 'Approved':
                    indent_data.update({
                        'Receive_Approved_by': createdBy,
                        'Receive_ApprovedDate': formatted_date_time,
                    })


                if indent_data['pk']:
                    indent_receive_ins = get_or_none(Indent_receive_details_table, indent_data['pk'])
                    if indent_receive_ins:
                        for key, value in indent_data.items():
                            setattr(indent_receive_ins, key, value)
                        indent_receive_ins.save()
                else:
                    indent_receive_ins = Indent_receive_details_table.objects.create(**indent_data)
        
                print('Items_Data---==',Items_Data)

                for it_ins in Items_Data:
                    it_ins_Receivedpk = it_ins.get('Receivedpk')
                    it_ins_Issuedpk = it_ins.get('Issuedpk')
                    
                    print(it_ins_Receivedpk,type(it_ins_Receivedpk),'-----it_ins_Receivedpk')
                    print(it_ins_Issuedpk,type(it_ins_Issuedpk),'-----it_ins_Issuedpk')

                    ReceivedQuantity = it_ins.get('ReceivedQuantity')
                    DamagedQuantity = it_ins.get('DamagedQuantity')
                    PendingQuantity = it_ins.get('PendingQuantity')
                    ReceivedSerialNo = it_ins.get('ReceivedSerialNo', [])
                    DamagedSerialNo = it_ins.get('DamagedSerialNo', [])
                    PendingSerialNo = it_ins.get('PendingSerialNo', [])
                    Reason = it_ins.get('Reason', '')
                    Remarks = it_ins.get('Remarks', '')
                    Status = it_ins.get('Status', 'Received')
                  
                    if Status != 'Cancelled':
                        Status = approval_status

                    it_ins_Receivedpk_ins = get_or_none(Indent_receive_items_details_table, it_ins_Receivedpk)
                    it_ins_Issuedpk_ins = get_or_none(Indent_issue_items_details_table, it_ins_Issuedpk)

                    ReceivedSerialNo_ins = set()
                    DamagedSerialNo_ins = set()
                    PendingSerialNo_ins = set()

                    # Handling Serial Numbers
                    for serial in ReceivedSerialNo + DamagedSerialNo + PendingSerialNo:
                        serial_ins = get_or_none(SerialNumber_Stock_Maintance_Table_Detials, serial['pk'])
                        if serial_ins:
                            if serial in ReceivedSerialNo:
                                ReceivedSerialNo_ins.add(serial_ins)
                            if serial in DamagedSerialNo:
                                DamagedSerialNo_ins.add(serial_ins)
                            if serial in PendingSerialNo:
                                PendingSerialNo_ins.add(serial_ins)

                    # print('hhhhh',it_ins_Receivedpk_ins.pk,'oooo')
                    indent_items_data = {
                        'pk': it_ins_Receivedpk_ins.pk if it_ins_Receivedpk_ins else None,
                        'Indent_Detials': indent_receive_ins,
                        'Indent_issue_Item': it_ins_Issuedpk_ins,
                        'Received_Quantity': ReceivedQuantity,
                        'Damaged_Quantity': DamagedQuantity,
                        'Pending_Quantity': PendingQuantity,
                        'Reason': Reason,
                        'Remarks': Remarks,
                        'Status': Status,
                    }

                    if indent_items_data['pk']:
                        indent_receive_item_ins = get_or_none(Indent_receive_items_details_table, indent_items_data['pk'])
                        if indent_receive_item_ins:
                            for key, value in indent_items_data.items():
                                setattr(indent_receive_item_ins, key, value)
                            indent_receive_item_ins.save()
                    else:
                        indent_receive_item_ins = Indent_receive_items_details_table.objects.create(**indent_items_data)

                    indent_receive_item_ins.Received_serialNo.set(ReceivedSerialNo_ins)
                    indent_receive_item_ins.Damaged_serialNo.set(DamagedSerialNo_ins)
                    indent_receive_item_ins.Pending_serialNo.set(PendingSerialNo_ins)
                
                Indent_issue_Ins=Indent_issue_details_table.objects.get(pk=Issued_pk_ins.pk)
                Indent_issue_Ins.Receive_Status='Completed'
                Indent_issue_Ins.save()
                
                return JsonResponse({
                    'status': 'success',
                    'message': 'Indent receive details recorded successfully.'
                }, status=200)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

    elif request.method =='GET':
        try:
            Indent_Type = request.GET.get('Indent_Type','issue')
            # print("Indent_Type",Indent_Type)
            Issue_Invoice_No = request.GET.get('Issue_Invoice_No')
            # print("Issue_Invoice_No",Issue_Invoice_No)
            Receive_Invoice_No = request.GET.get('Receive_Invoice_No')
            # print("Receive_Invoice_No",Receive_Invoice_No)
            DateType = request.GET.get('DateType')
            # print("DateType",DateType)
            CurrentDate = request.GET.get('CurrentDate')
            # print("CurrentDate",CurrentDate)
            FromDate = request.GET.get('FromDate')
            ToDate = request.GET.get('ToDate')
            Status = request.GET.get('Status','waiting').strip()
            # print("Status",Status)

            query = Q()
            indent_table = None
            indent_items_table = None

            if Indent_Type =='issue':
                indent_table = Indent_issue_details_table
                indent_items_table = Indent_issue_items_details_table
                query &= Q(Issue_Status = 'Approved',Receive_Status = Status)
            else:
                indent_table = Indent_receive_details_table
                indent_items_table = Indent_receive_items_details_table
                query &= Q(Receive_Status = Status)
            
            if Indent_Type == 'issue':
                if Issue_Invoice_No:
                    query &= Q(pk__iexact=Issue_Invoice_No)
            else:
                if Issue_Invoice_No:
                    query &= Q(Indent_raise__pk__iexact=Issue_Invoice_No)
                if Receive_Invoice_No:
                    query &= Q(pk__iexact=Receive_Invoice_No)

            if DateType == 'Current' and CurrentDate:
                if Indent_Type =='issue':
                    query &= Q(Issue_Date=CurrentDate)
                query &= Q(Receive_Date=CurrentDate)
            elif DateType == 'Customize' and FromDate and ToDate:
                if Indent_Type == 'issue':
                    query &= Q(Issue_Date__range=[FromDate, ToDate])
                query &= Q(Receive_Date__range=[FromDate, ToDate])

            # Execute query on chosen table
            Indent_table_results = None
            if indent_table:
                Indent_table_results = indent_table.objects.filter(query)
            
            print('Indent_table_results???',Indent_table_results)

            indent_inssue_datas=[]

            print('Indent_Type',Indent_Type)

            if Indent_table_results:
                for indx, ins in enumerate(Indent_table_results):
                    print("ins",ins)
                    dic ={
                        'id':indx + 1, 
                        'Item_Detials':[]
                    }

                    if Indent_Type == 'issue':
                        print('111111')

                        print(ins.Indent_raise)


                        print('22222222')

                        if ins.Indent_raise:
                            Indent_raise_insss = ins.Indent_raise
                            dic['issue_Indent_Type'] = ins.Indent_Type
                            dic['Raised_pk'] = Indent_raise_insss.pk if Indent_raise_insss else None
                            dic['RaisedFromLocation_pk'] = Indent_raise_insss.Raise_From_Location.pk if Indent_raise_insss and Indent_raise_insss.Raise_From_Location else None
                            dic['RaisedFromLocation'] = Indent_raise_insss.Raise_From_Location.Location_Name if Indent_raise_insss and Indent_raise_insss.Raise_From_Location else None
                            dic['RaisedFromNurseStation'] = Indent_raise_insss.Raise_From_NurseStation_Store if Indent_raise_insss and Indent_raise_insss.Raise_From_NurseStation_Store is not None else None
                            dic['RaisedFromNurseStation_pk'] = Indent_raise_insss.Raise_From_NurseStation_Location.pk if Indent_raise_insss and Indent_raise_insss.Raise_From_NurseStation_Store and Indent_raise_insss.Raise_From_NurseStation_Location else ''
                            dic['RaisedFromNurseStationWard'] = Indent_raise_insss.Raise_From_NurseStation_Location.NurseStationName if Indent_raise_insss and Indent_raise_insss.Raise_From_NurseStation_Store and Indent_raise_insss.Raise_From_NurseStation_Location else ""
                            dic['RaisedFromStore_pk'] = Indent_raise_insss.Raise_From_Store_Location.pk if Indent_raise_insss and not Indent_raise_insss.Raise_From_NurseStation_Store and Indent_raise_insss.Raise_From_Store_Location else ''
                            dic['RaisedFromStore'] = Indent_raise_insss.Raise_From_Store_Location.Store_Name if Indent_raise_insss and not Indent_raise_insss.Raise_From_NurseStation_Store and Indent_raise_insss.Raise_From_Store_Location else ''
                            
                            dic['RaisedToLocation_pk'] = Indent_raise_insss.Raise_To_Location.pk if Indent_raise_insss and Indent_raise_insss.Raise_To_Location else None
                            dic['RaisedToLocation'] = Indent_raise_insss.Raise_To_Location.Location_Name if Indent_raise_insss and Indent_raise_insss.Raise_To_Location else None
                            dic['RaisedToNurseStation'] = Indent_raise_insss.Raise_To_NurseStation_Store
                            dic['RaisedToNurseStation_pk'] = Indent_raise_insss.Raise_To_NurseStation_Location.pk if Indent_raise_insss and Indent_raise_insss.Raise_To_NurseStation_Store and Indent_raise_insss.Raise_To_NurseStation_Location else ''
                            dic['RaisedToNurseStationWard'] = Indent_raise_insss.Raise_To_NurseStation_Location.NurseStationName if Indent_raise_insss and Indent_raise_insss.Raise_To_NurseStation_Store and Indent_raise_insss.Raise_To_NurseStation_Location else ''
                            dic['RaisedToStore_pk'] = Indent_raise_insss.Raise_To_Store_Location.pk if Indent_raise_insss and not Indent_raise_insss.Raise_To_NurseStation_Store and Indent_raise_insss.Raise_To_Store_Location else ''
                            dic['RaisedToStore'] = Indent_raise_insss.Raise_To_Store_Location.Store_Name if Indent_raise_insss and not Indent_raise_insss.Raise_To_NurseStation_Store and Indent_raise_insss.Raise_To_Store_Location else ''
                            dic['RaisedDate'] = Indent_raise_insss.Raise_Date.strftime('%Y-%m-%d') if Indent_raise_insss and Indent_raise_insss.Raise_Date else None
                            dic['RaisedApprovedDate'] = Indent_raise_insss.Raise_ApprovedDate.strftime('%Y-%m-%d') if Indent_raise_insss and Indent_raise_insss.Raise_ApprovedDate else None
                            dic['Raised_by'] = Indent_raise_insss.Raise_by if Indent_raise_insss else None
                            dic['RaisedApproved_by'] = Indent_raise_insss.Raise_Approved_by if Indent_raise_insss else None
                            dic['RaisedReason'] = Indent_raise_insss.Raise_Reason if Indent_raise_insss else None
                            dic['raise_Raise_Status'] = Indent_raise_insss.Raise_Status if Indent_raise_insss else None
                            dic['raise_Issue_Status'] = Indent_raise_insss.Issue_Status if Indent_raise_insss else None

                        dic['Issued_pk'] = ins.pk
                        dic['IssuedFromLocation_pk'] = ins.Issue_From_Location.pk if ins.Issue_From_Location else None
                        dic['IssuedFromLocation'] = ins.Issue_From_Location.Location_Name if ins.Issue_From_Location else None
                        dic['IssuedFromNurseStation'] = ins.Issue_From_NurseStation_Store
                        dic['IssuedFromNurseStation_pk'] = ins.Issue_From_Store_Location.pk if ins.Issue_From_NurseStation_Store and ins.Issue_From_Store_Location else ''
                        dic['IssuedFromNurseStationWard'] = ins.Issue_From_Store_Location.NurseStationName if ins.Issue_From_NurseStation_Store and ins.Issue_From_Store_Location else ""
                        dic['IssuedFromStore_pk'] = ins.Issue_From_Store_Location.pk if not ins.Issue_From_NurseStation_Store and ins.Issue_From_Store_Location else ''
                        dic['IssuedFromStore'] = ins.Issue_From_Store_Location.Store_Name if not ins.Issue_From_NurseStation_Store and ins.Issue_From_Store_Location else ''
                        
                        dic['IssuedToLocation_pk'] = ins.Issue_To_Location.pk if ins.Issue_To_Location else None
                        dic['IssuedToLocation'] = ins.Issue_To_Location.Location_Name if ins.Issue_To_Location else None
                        dic['IssuedToNurseStation'] = ins.Issue_To_NurseStation_Store
                        dic['IssuedToNurseStation_pk'] = ins.Issue_To_NurseStation_Location.pk if ins.Issue_To_NurseStation_Store and ins.Issue_To_NurseStation_Location else ''
                        dic['IssuedToNurseStationWard'] = ins.Issue_To_NurseStation_Location.NurseStationName if ins.Issue_To_NurseStation_Store and ins.Issue_To_NurseStation_Location else ''
                        dic['IssuedToStore_pk'] = ins.Issue_To_Store_Location.pk if not ins.Issue_To_NurseStation_Store and ins.Issue_To_Store_Location else ''
                        dic['IssuedToStore'] = ins.Issue_To_Store_Location.Store_Name if not ins.Issue_To_NurseStation_Store and ins.Issue_To_Store_Location else ''
                        
                        dic['IssuedDate'] = ins.Issue_Date.strftime('%Y-%m-%d') if ins.Issue_Date else None
                        dic['IssuedApprovedDate'] = ins.Issue_ApprovedDate.strftime('%Y-%m-%d') if ins.Issue_ApprovedDate else None
                        dic['Issued_by'] = ins.Issue_by
                        dic['IssuedApproved_by'] = ins.Issue_Approved_by
                        dic['IssuedReason'] = ins.Issue_Reason
                        dic['issue_Issue_Status'] = ins.Issue_Status
                        dic['issue_Receive_Status'] = ins.Receive_Status
                    else:
                        print("elsepart")
                        Indent_issue_inssss = ins.Indent_issue
                        print("Indent_issue_inssss",Indent_issue_inssss)
                        Indent_raise_insss = Indent_issue_inssss.Indent_raise
                        if Indent_raise_insss:
                            dic['Raised_pk'] = Indent_raise_insss.pk if Indent_raise_insss else None
                            dic['RaisedFromLocation_pk'] = Indent_raise_insss.Raise_From_Location.pk if Indent_raise_insss and Indent_raise_insss.Raise_From_Location else None
                            dic['RaisedFromLocation'] = Indent_raise_insss.Raise_From_Location.Location_Name if Indent_raise_insss and Indent_raise_insss.Raise_From_Location else None
                            dic['RaisedFromNurseStation'] = Indent_raise_insss.Raise_From_NurseStation_Store
                            dic['RaisedFromNurseStation_pk'] = Indent_raise_insss.Raise_From_NurseStation_Location.pk if Indent_raise_insss and Indent_raise_insss.Raise_From_NurseStation_Store and Indent_raise_insss.Raise_From_NurseStation_Location else ''
                            dic['RaisedFromNurseStationWard'] = Indent_raise_insss.Raise_From_NurseStation_Location.NurseStationName if Indent_raise_insss and Indent_raise_insss.Raise_From_NurseStation_Store and Indent_raise_insss.Raise_From_NurseStation_Location else ""
                            dic['RaisedFromStore_pk'] = Indent_raise_insss.Raise_From_Store_Location.pk if Indent_raise_insss and not Indent_raise_insss.Raise_From_NurseStation_Store and Indent_raise_insss.Raise_From_Store_Location else ''
                            dic['RaisedFromStore'] = Indent_raise_insss.Raise_From_Store_Location.Store_Name if Indent_raise_insss and not Indent_raise_insss.Raise_From_NurseStation_Store and Indent_raise_insss.Raise_From_Store_Location else ''
                            dic['RaisedToLocation_pk'] = Indent_raise_insss.Raise_To_Location.pk if Indent_raise_insss and Indent_raise_insss.Raise_To_Location else None
                            dic['RaisedToLocation'] = Indent_raise_insss.Raise_To_Location.Location_Name if Indent_raise_insss and Indent_raise_insss.Raise_To_Location else None
                            dic['RaisedToNurseStation'] = Indent_raise_insss.Raise_To_NurseStation_Store 
                            dic['RaisedToNurseStation_pk'] = Indent_raise_insss.Raise_To_NurseStation_Location.pk if Indent_raise_insss and Indent_raise_insss.Raise_To_NurseStation_Store and Indent_raise_insss.Raise_To_NurseStation_Location else ''
                            dic['RaisedToNurseStationWard'] = Indent_raise_insss.Raise_To_NurseStation_Location.NurseStationName if Indent_raise_insss and Indent_raise_insss.Raise_To_NurseStation_Store and Indent_raise_insss.Raise_To_NurseStation_Location else ''
                            dic['RaisedToStore_pk'] = Indent_raise_insss.Raise_To_Store_Location.pk if Indent_raise_insss and not Indent_raise_insss.Raise_To_NurseStation_Store and Indent_raise_insss.Raise_To_Store_Location else ''
                            dic['RaisedToStore'] = Indent_raise_insss.Raise_To_Store_Location.Store_Name if Indent_raise_insss and not Indent_raise_insss.Raise_To_NurseStation_Store and Indent_raise_insss.Raise_To_Store_Location else ''
                            dic['RaisedDate'] = Indent_raise_insss.Raise_Date.strftime('%Y-%m-%d') if Indent_raise_insss and Indent_raise_insss.Raise_Date else None
                            dic['RaisedApprovedDate'] = Indent_raise_insss.Raise_ApprovedDate.strftime('%Y-%m-%d') if Indent_raise_insss and Indent_raise_insss.Raise_ApprovedDate else None
                            dic['Raised_by'] = Indent_raise_insss.Raise_by if Indent_raise_insss else None
                            dic['RaisedApproved_by'] = Indent_raise_insss.Raise_Approved_by if Indent_raise_insss else None
                            dic['RaisedReason'] = Indent_raise_insss.Raise_Reason if Indent_raise_insss else None
                            dic['raise_Raise_Status'] = Indent_raise_insss.Raise_Status if Indent_raise_insss else None
                            dic['raise_Issue_Status'] = Indent_raise_insss.Issue_Status if Indent_raise_insss else None

                        dic['issue_Indent_Type'] = Indent_issue_inssss.Indent_Type


                        


                        dic['Issued_pk'] = Indent_issue_inssss.pk
                        dic['IssuedFromLocation_pk'] = Indent_issue_inssss.Issue_From_Location.pk if Indent_issue_inssss.Issue_From_Location else None
                        dic['IssuedFromLocation'] = Indent_issue_inssss.Issue_From_Location.Location_Name if Indent_issue_inssss.Issue_From_Location else None
                        dic['IssuedFromNurseStation'] = Indent_issue_inssss.Issue_From_NurseStation_Store
                        dic['IssuedFromNurseStation_pk'] = Indent_issue_inssss.Issue_From_NurseStation_Location.pk if Indent_issue_inssss.Issue_From_NurseStation_Store and Indent_issue_inssss.Issue_From_NurseStation_Location else ''
                        dic['IssuedFromNurseStationWard'] = Indent_issue_inssss.Issue_From_NurseStation_Location.NurseStationName if Indent_issue_inssss.Issue_From_NurseStation_Store and Indent_issue_inssss.Issue_From_NurseStation_Location else ""
                        dic['IssuedFromStore_pk'] = Indent_issue_inssss.Issue_From_Store_Location.pk if not Indent_issue_inssss.Issue_From_NurseStation_Store and Indent_issue_inssss.Issue_From_Store_Location else ''
                        dic['IssuedFromStore'] = Indent_issue_inssss.Issue_From_Store_Location.Store_Name if not Indent_issue_inssss.Issue_From_NurseStation_Store and Indent_issue_inssss.Issue_From_Store_Location else ''
                        
                        dic['IssuedToLocation_pk'] = Indent_issue_inssss.Issue_To_Location.pk if Indent_issue_inssss.Issue_To_Location else None
                        dic['IssuedToLocation'] = Indent_issue_inssss.Issue_To_Location.Location_Name if Indent_issue_inssss.Issue_To_Location else None
                        dic['IssuedToNurseStation'] = Indent_issue_inssss.Issue_To_NurseStation_Store
                        dic['IssuedToNurseStation_pk'] = Indent_issue_inssss.Issue_To_NurseStation_Location.pk if Indent_issue_inssss.Issue_To_NurseStation_Store and Indent_issue_inssss.Issue_To_NurseStation_Location else ''
                        dic['IssuedToNurseStationWard'] = Indent_issue_inssss.Issue_To_NurseStation_Location.NurseStationName if Indent_issue_inssss.Issue_To_NurseStation_Store and Indent_issue_inssss.Issue_To_NurseStation_Location else ''
                        dic['IssuedToStore_pk'] = Indent_issue_inssss.Issue_To_Store_Location.pk if not Indent_issue_inssss.Issue_To_NurseStation_Store and Indent_issue_inssss.Issue_To_Store_Location else ''
                        dic['IssuedToStore'] = Indent_issue_inssss.Issue_To_Store_Location.Store_Name if not Indent_issue_inssss.Issue_To_NurseStation_Store and Indent_issue_inssss.Issue_To_Store_Location else ''
                        
                        dic['IssuedDate'] = Indent_issue_inssss.Issue_Date.strftime('%Y-%m-%d') if Indent_issue_inssss.Issue_Date else None
                        dic['IssuedApprovedDate'] = Indent_issue_inssss.Issue_ApprovedDate.strftime('%Y-%m-%d') if Indent_issue_inssss.Issue_ApprovedDate else None
                        dic['Issued_by'] = Indent_issue_inssss.Issue_by
                        dic['IssuedApproved_by'] = Indent_issue_inssss.Issue_Approved_by
                        dic['IssuedReason'] = Indent_issue_inssss.Issue_Reason
                        dic['issue_Issue_Status'] = Indent_issue_inssss.Issue_Status
                        dic['issue_Receive_Status'] = Indent_issue_inssss.Receive_Status
                        
                        dic['Received_pk'] = ins.pk
                        dic['ReceiveDate'] = ins.Receive_Date.strftime('%Y-%m-%d %I:%M %p') if ins.Receive_Date else None
                        dic['ReceiveApprovedDate'] = ins.Receive_ApprovedDate.strftime('%Y-%m-%d %I:%M %p') if ins.Receive_ApprovedDate else None
                        dic['Receive_by'] = ins.Receive_by
                        dic['ReceiveApproved_by'] = ins.Receive_Approved_by
                        dic['ReceiveReason'] = ins.Receive_Reason
                        dic['Receive_Receive_Status'] = ins.Receive_Status
                    items_query =Q()
                    if Indent_Type=='issue' :
                        items_query &=Q(Indent_Detials = dic['Issued_pk'],Issue_Status='Approved')
                    else:
                        items_query &=Q(Indent_Detials = dic['Received_pk'])

                    indent_items_table_insss = indent_items_table.objects.filter(Indent_Detials = dic['Issued_pk'] if Indent_Type=='issue' else dic['Received_pk'])
                    print("indent_items_table_insss",indent_items_table_insss)
                    for it_index,it_ins in enumerate(indent_items_table_insss):
                        if Indent_Type == 'issue':
                            print("sundari")

                            item_dic={
                                'id':len(dic['Item_Detials']) +1,
                                'Raisedpk':it_ins.Indent_Raise_Item.pk if it_ins.Indent_Raise_Item else None,
                                'Issuedpk':it_ins.pk,
                                'Receivedpk':None,
                                "ItemCode": it_ins.Product_Detials.pk,
                                "ItemName": it_ins.Product_Detials.ItemName,
                                "ProductCategory":it_ins.Product_Detials.SubCategory.ProductCategoryId.ProductCategory_Name,
                                "SubCategory": it_ins.Product_Detials.SubCategory.SubCategoryName,
                                'PackType': it_ins.Product_Detials.PackType.PackType_Name if it_ins.Product_Detials.PackType else 'Nill',
                                'PackQuantity': it_ins.Product_Detials.PackQty if it_ins.Product_Detials.PackQty else 'Nill',
                                'Reason':it_ins.Reason,
                                'BatchNo':it_ins.stock_Detials.Batch_No,
                                'RaisedQuantity':it_ins.Indent_Raise_Item.Raise_Quantity if it_ins.Indent_Raise_Item else None,
                                'IssueQuantity':it_ins.Issue_Quantity,
                                'ReceivedQuantity':it_ins.Issue_Quantity,
                                'DamagedQuantity':it_ins.Issue_Quantity if it_ins.Reason == 'DamagedProducts' else 0 ,
                                'Remarks':it_ins.Remarks,
                                'Issue_Status':it_ins.Issue_Status,
                                'Receive_Status':it_ins.Receive_Status,
                                'SerialNoAvailable':it_ins.stock_Detials.Is_Serial_No_Available_for_each_quantity
                            }
                            if item_dic['SerialNoAvailable'] and it_ins.serialNo.exists():
                                item_dic['SerialNo'] = []
                                for serial in it_ins.serialNo.all():
                                    dattt= {
                                        'pk': serial.pk,
                                        'Serial_Number': serial.Serial_Number,
                                        "Status": True,
                                        'Item_Status': serial.Item_Status,
                                        'Product_Status': 'good',
                                    }
                                    item_dic['SerialNo'].append(dattt)
                            dic['Item_Detials'].append(item_dic)
                        else:
                            issue_items_ins = it_ins.Indent_issue_Item
                            item_dic={
                                "id":len(dic['Item_Detials']) +1,
                                'Raisedpk':issue_items_ins.Indent_Raise_Item.pk if issue_items_ins.Indent_Raise_Item else None,
                                'Issuedpk':issue_items_ins.pk,
                                'Receivedpk':it_ins.pk,
                                "ItemCode": issue_items_ins.Product_Detials.pk,
                                "ItemName": issue_items_ins.Product_Detials.ItemName,
                                "ProductCategory":issue_items_ins.Product_Detials.SubCategory.ProductCategoryId.ProductCategory_Name,
                                "SubCategory": issue_items_ins.Product_Detials.SubCategory.SubCategoryName,
                                'PackType': issue_items_ins.Product_Detials.PackType.PackType_Name if issue_items_ins.Product_Detials.PackType else 'Nill',
                                'PackQuantity': issue_items_ins.Product_Detials.PackQty if issue_items_ins.Product_Detials.PackQty else 'Nill',
                                'Reason':issue_items_ins.Reason,
                                'BatchNo':issue_items_ins.stock_Detials.Batch_No,
                                'SerialNoAvailable':issue_items_ins.stock_Detials.Is_Serial_No_Available_for_each_quantity,
                                'RaisedQuantity':issue_items_ins.Indent_Raise_Item.Raise_Quantity if issue_items_ins.Indent_Raise_Item else None,
                                'IssueQuantity':issue_items_ins.Issue_Quantity,
                                'ReceivedQuantity':it_ins.Received_Quantity,
                                'Receive_Status':issue_items_ins.Receive_Status,
                                'DamagedQuantity':it_ins.Damaged_Quantity,
                                'PendingQuantity':it_ins.Pending_Quantity,
                                'SerialNo':[],
                                'ReceivedSerialNo':[],
                                'DamagedSerialNo':[],
                                'PendingSerialNo':[],
                            }
                            # Check if SerialNo is available and then append related serial numbers
                            if item_dic['SerialNoAvailable']:
                                # Process Received Serial Numbers
                                if it_ins.Received_serialNo.exists():
                                    for serial in it_ins.Received_serialNo.all():
                                        dattt = {
                                            'pk': serial.pk,
                                            'Serial_Number': serial.Serial_Number,
                                            "Status": True,
                                            'Item_Status': serial.Item_Status,
                                            'Product_Status': 'good',
                                        }
                                        item_dic['ReceivedSerialNo'].append(dattt)
                                        item_dic['SerialNo'].append(dattt)

                                # Process Damaged Serial Numbers
                                if it_ins.Damaged_serialNo.exists():
                                    for serial in it_ins.Damaged_serialNo.all():
                                        dattt = {
                                            'pk': serial.pk,
                                            'Serial_Number': serial.Serial_Number,
                                            "Status": True,
                                            'Item_Status': serial.Item_Status,
                                            'Product_Status': 'damaged',
                                        }
                                        item_dic['DamagedSerialNo'].append(dattt)
                                        # Check if the serial.pk already exists in SerialNo, replace if found
                                        serial_exists = False
                                        for idx, existing_serial in enumerate(item_dic['SerialNo']):
                                            if existing_serial['pk'] == serial.pk:
                                                item_dic['SerialNo'][idx] = dattt  # Replace the existing entry
                                                serial_exists = True
                                                break

                                        # If the serial does not exist in SerialNo, append it
                                        if not serial_exists:
                                            item_dic['SerialNo'].append(dattt)

                                        for idx, existing_serial in enumerate(item_dic['ReceivedSerialNo']):
                                            if existing_serial['pk'] == serial.pk:
                                                item_dic['ReceivedSerialNo'][idx] = dattt  # Replace the existing entry
                                                serial_exists = True
                                                break

                                # Process Pending Serial Numbers
                                if it_ins.Pending_serialNo.exists():
                                    for serial in it_ins.Pending_serialNo.all():
                                        dattt = {
                                            'pk': serial.pk,
                                            'Serial_Number': serial.Serial_Number,
                                            "Status": False,
                                            'Item_Status': serial.Item_Status,
                                            'Product_Status': 'good',
                                        }
                                        item_dic['PendingSerialNo'].append(dattt)
                                        item_dic['SerialNo'].append(dattt)
                                
                            dic['Item_Detials'].append(item_dic)    
                    
                    indent_inssue_datas.append(dic)
                    # print("indent_inssue_datas",indent_inssue_datas)
            return JsonResponse(indent_inssue_datas, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
    
    else:
        return JsonResponse({'error': f'An error occurred: Request method not allowed'}, status=405)



@csrf_exempt
@require_http_methods(["POST","OPTIONS"])
def Indent_Receive_Details_Approve_link(request):
    if request.method == 'POST':
        try:

            data = json.loads(request.body)
            indent_type = data.get('IndentType')
            invoice_no = data.get('InvoiceNo')
            status = data.get('Status')
            approved_by = data.get('Approved_by')
            CancelReceivepk = data.get('CancelReceivepk')


            print('data-----2222',data,invoice_no,CancelReceivepk)

            current_date_time = datetime.now()
            formatted_date_time = current_date_time.strftime('%Y-%m-%d %H:%M')

            with transaction.atomic():
                if (indent_type == 'issue' and status == 'Cancelled') or \
                   (indent_type == 'Receive' and status == 'Cancelled' and CancelReceivepk):
                    try:
                        indent_instance = Indent_issue_details_table.objects.get(pk=invoice_no)
                    except Indent_issue_details_table.DoesNotExist:
                        return JsonResponse({'error': 'Indent raise entry not found'}, status=404)

                    related_items = Indent_issue_items_details_table.objects.filter(
                        Indent_Detials=indent_instance,
                        Issue_Status='Approved'
                    )
                    for item in related_items:
                        item.Receive_Status = status
                        issue_quantity = item.Issue_Quantity

                        Stock_instance=Stock_Maintance_Table_Detials.objects.get(pk=item.stock_Detials.pk)
                        
                        Stock_instance.AvailableQuantity += issue_quantity
                        Stock_instance.Indent_Send_Quantity -= issue_quantity
                        Stock_instance.Total_Moved_Quantity -= issue_quantity
                        Stock_instance.save()
                        item.save()
                        
                        if item.serialNo.exists():
                            serial_no_ids = list(item.serialNo.values_list('id', flat=True))  
                            print("Serial Numbers to Update:", serial_no_ids)
                            SerialNumber_Stock_Maintance_Table_Detials.objects.filter(
                                id__in=serial_no_ids
                            ).update(Item_Status='Available')
                    
                    
                    indent_instance.Receive_Status = status
                    indent_instance.Issue_ApprovedDate = formatted_date_time
                    indent_instance.Issue_Approved_by = approved_by
                    indent_instance.save()

                    if indent_type =='Receive' and status == 'Cancelled' and CancelReceivepk :
                        print('hiiii---1111')

                        Indent_receive_Ins=Indent_receive_details_table.objects.get(pk=CancelReceivepk)
                        Indent_receive_Ins.Receive_Status=status
                        Indent_receive_Ins.save()

                        Indent_receive_items_details_table.objects.filter(
                           Indent_Detials=Indent_receive_Ins
                        ).update(Status=status)

                        
                
                elif indent_type == 'Receive':
                    if status == 'Approved':

                        print('ooooo',status)
                        try:
                            indent_instance = Indent_receive_details_table.objects.get(pk=invoice_no)
                        except Indent_receive_details_table.DoesNotExist:
                            return JsonResponse({'error': 'Indent raise entry not found'}, status=404)

                        related_items = Indent_receive_items_details_table.objects.filter(
                            Indent_Detials=indent_instance
                        )

                        for item in related_items:
                            print(item.Indent_issue_Item.stock_Detials.pk,'kkkk??????')
                            
                            StockIns=item.Indent_issue_Item.stock_Detials
                            Indent_issue_ins=indent_instance.Indent_issue

                            print('vvvvv',StockIns)

                            if StockIns:
                                Product_Master_Ins=Product_Master_All_Category_Details.objects.get(pk=StockIns.Product_Detials.pk)
                            
                            Stock_Maintance_Ins=''
                            try:
                                Stock_Maintance_Ins=Stock_Maintance_Table_Detials.objects.get(
                                Product_Detials=Product_Master_Ins,
                                Batch_No=StockIns.Batch_No,
                                IsNurseStation=Indent_issue_ins.Issue_To_NurseStation_Store,
                                Store_location=Indent_issue_ins.Issue_To_Store_Location,
                                NurseStation_location=Indent_issue_ins.Issue_To_NurseStation_Location
                                )
                            except:
                                print('Data Not Matching')

                            if Stock_Maintance_Ins:

                                print('Stock_Maintance_Ins save update')

                                Stock_Maintance_Ins.Total_Quantity+=item.Received_Quantity
                                Stock_Maintance_Ins.Indent_Recieve_Quantity+=item.Received_Quantity
                                Stock_Maintance_Ins.AvailableQuantity+=item.Received_Quantity

                                Stock_Maintance_Ins.save()

                                if StockIns.Is_Serial_No_Available_for_each_quantity :
                                    if item.Indent_issue_Item.serialNo.exists():
                                        serial_no_ids = list(item.Indent_issue_Item.serialNo.values_list('id', flat=True))  
                                        print("Serial Numbers to Update:", serial_no_ids)
                                        SerialNumber_Stock_Maintance_Table_Detials.objects.filter(
                                            id__in=serial_no_ids
                                        ).update(Item_Status='Available',
                                                IsNurseStation=Indent_issue_ins.Issue_To_NurseStation_Store,
                                                Store_location=Indent_issue_ins.Issue_To_Store_Location,
                                                NurseStation_location=Indent_issue_ins.Issue_To_NurseStation_Location)
                                        
                            else:
                                Stock_Maintance_Table_Detials.objects.create(
                                    Product_Detials=Product_Master_Ins,
                                    Batch_No=StockIns.Batch_No,
                                    Is_MRP_as_sellable_price=StockIns.Is_MRP_as_sellable_price,
                                    Sellable_price=StockIns.Sellable_price,
                                    Sellable_qty_price=StockIns.Sellable_qty_price,
                                    Is_Manufacture_Date_Available=StockIns.Is_Manufacture_Date_Available,
                                    Manufacture_Date=StockIns.Manufacture_Date,
                                    Is_Expiry_Date_Available=StockIns.Is_Expiry_Date_Available,
                                    Expiry_Date=StockIns.Expiry_Date,
                                    Total_Quantity=item.Received_Quantity,
                                    Indent_Recieve_Quantity=item.Received_Quantity,
                                    AvailableQuantity=item.Received_Quantity,
                                    IsNurseStation=Indent_issue_ins.Issue_To_NurseStation_Store,
                                    Store_location=Indent_issue_ins.Issue_To_Store_Location,
                                    NurseStation_location=Indent_issue_ins.Issue_To_NurseStation_Location,
                                    Expiry_Status=StockIns.Expiry_Status,
                                    Is_Serial_No_Available_for_each_quantity=StockIns.Is_Serial_No_Available_for_each_quantity,
                                    Is_Serial_No_Status=StockIns.Is_Serial_No_Status,
                                    Serial_No_Type=StockIns.Serial_No_Type,
                                    Created_by=approved_by
                                    )
                            
                                if StockIns.Is_Serial_No_Available_for_each_quantity :
                                    if item.Indent_issue_Item.serialNo.exists():
                                        serial_no_ids = list(item.Indent_issue_Item.serialNo.values_list('id', flat=True))  
                                        print("Serial Numbers to Update:", serial_no_ids)
                                        SerialNumber_Stock_Maintance_Table_Detials.objects.filter(
                                            id__in=serial_no_ids
                                        ).update(Item_Status='Available',
                                                IsNurseStation=Indent_issue_ins.Issue_To_NurseStation_Store,
                                                Store_location=Indent_issue_ins.Issue_To_Store_Location,
                                                NurseStation_location=Indent_issue_ins.Issue_To_NurseStation_Location)
                                


                            item.Status=status
                            item.save()


                        indent_instance.Receive_Status=status
                        indent_instance.save()

            return JsonResponse({'success': f'Indent Raise {status} successfully'}, status=200)

        
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)



