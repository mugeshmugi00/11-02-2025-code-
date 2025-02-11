from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from Masters.models import *
import pandas as pd
from Inventory.models import *
from django.db.models import Func, Value



# -----------------------------------------------------------------------------------



@csrf_exempt   
@require_http_methods(["POST","OPTIONS","GET"])
def Rack_Detials_link(request):
    if request.method == 'POST':
         try:
            data=json.loads(request.body)
            # print("data",data)

            RackID=data.get("RackID",'')
            RackName=data.get('RackName')
            Location=data.get('Location')
            StoreLocation=data.get('StoreLocation')
            created_by=data.get('created_by')
            Statusedit=data.get('Statusedit',False)
            
            if Location:
                Location_instance = Location_Detials.objects.get(Location_Id = Location)
            if StoreLocation:
                Inventory_Location = Inventory_Location_Master_Detials.objects.get(Store_Id = StoreLocation)
            
            if RackID:
                if Statusedit:
                    Rack_instance = Rack_Master_Detials.objects.get(pk=RackID)
                    Rack_instance.Status = not Rack_instance.Status
                    Rack_instance.save()
                    
                    return JsonResponse({'success': 'Rack Detials Updated successfully'})
                    

                else:
                    if not RackName  or not Location or not StoreLocation:
                        return JsonResponse({'warn': 'RackName , Location and StoreLocation are mandatory fields'})
                
                    if Rack_Master_Detials.objects.filter(Rack_Name=RackName).exclude(pk=RackID).exists():

                        return JsonResponse ({'warn':f"The Rack Detials are already present in the name of {RackName}"})


                    else:
                        Rack_instance=Rack_Master_Detials.objects.get(pk=RackID)
                        Rack_instance.Rack_Name=RackName
                        Rack_instance.Store_Location_Name=Inventory_Location
                        Rack_instance.Location_Name=Location_instance
                        Rack_instance.save()

                        return JsonResponse({'success': 'Rack Detials Updated successfully'})
            
            else:
                if not RackName  or not Location or not StoreLocation:
                    return JsonResponse({'warn': 'RackName , Location and StoreLocation are mandatory fields'})

                if Rack_Master_Detials.objects.filter(Rack_Name=RackName, Location_Name=Location_instance,Store_Location_Name=Inventory_Location).exists():
                    return JsonResponse({'warn': f"The Rack Detials are already present in the name of {RackName},{Inventory_Location.Store_Name} and {Location_instance.Location_Name} "})
                else:
                    Rack_instance=Rack_Master_Detials(
                        Rack_Name=RackName,
                        Location_Name=Location_instance,
                        Store_Location_Name=Inventory_Location,
                        created_by=created_by
                    )
                    Rack_instance.save()
                    return JsonResponse ({'success': 'Rack Detials added successfully'})


         except Exception as e :
             print(f"An error occurred: {str(e)}")
             return JsonResponse ({'error':'An internal server error occurred'},status=500)

    elif request.method == 'GET':
        try:
            SearchLocation=request.GET.get('SearchLocation')
            StoreLocation=request.GET.get('StoreLocation')

            Rack_Master=Rack_Master_Detials.objects.all()

            if SearchLocation:
                Rack_Master=Rack_Master.filter(Location_Name__Location_Id=SearchLocation)
            
            if StoreLocation:
                Rack_Master=Rack_Master.filter(Store_Location_Name__Store_Id=StoreLocation)

            Rack_Master_Array = []

            for row in Rack_Master :
                Rack_Master_dic={
                    "id":row.Rack_Id,
                    "RackName":row.Rack_Name,
                    "Location":row.Location_Name.Location_Name,
                    'Location_Id': row.Location_Name.Location_Id,                    
                    "Store_Location":row.Store_Location_Name.Store_Name,
                    'Store_Location_Id': row.Store_Location_Name.Store_Id,
                    "Status":row.Status,
                }
                
                Rack_Master_Array.append(Rack_Master_dic)
            
            return JsonResponse (Rack_Master_Array,safe=False)

        except Exception as e :
            print(f'An error occurred: {str(e)}')
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)    


# -----------------------------------------------------------------------------------


@csrf_exempt
@require_http_methods(["POST","OPTIONS","GET"])
def Shelf_Detials_link(request):
    if request.method=='POST':
        try:
            data = json.loads(request.body)
            # print("data",data)
            ShelfID=data.get('ShelfID','')
            RackName=data.get('RackName')
            ShelfName=data.get('ShelfName')
            created_by=data.get('created_by')
            Location=data.get('Location')
            Statusedit=data.get('Statusedit',False)
            StoreLocation=data.get('StoreLocation')

            print(ShelfID,Statusedit,'===')


            
            if RackName :
                RackDetials_Instance=Rack_Master_Detials.objects.get(pk=RackName)

            if ShelfID:
                if Statusedit:
                    Shelf_instance=Shelf_Master_Detials.objects.get(pk=ShelfID)
                    Shelf_instance.Status=not Shelf_instance.Status
                    Shelf_instance.save()

                    return JsonResponse({'success': 'Shelf Detials Updated successfully'})
                
                else:
                  
                  if not RackName or not ShelfName or not StoreLocation or not Location:
                        return JsonResponse({'warn': 'RackName, ShelfName, StoreLocation and Location are mandatory fields'})
                  if Shelf_Master_Detials.objects.filter(Shelf_Name=ShelfName).exclude(pk=ShelfID).exists():
                        return JsonResponse ({'warn':f"The Shelf Detials are already present in the name of {RackName} and {ShelfName} "})
                  else:
                      Shelf_instance=Shelf_Master_Detials.objects.get(pk=ShelfID)
                      Shelf_instance.Shelf_Name=ShelfName
                      Shelf_instance.Rack_Name=RackDetials_Instance
                      Shelf_instance.save()
                  
                      return JsonResponse({'success': 'Shelf Detials Updated successfully'})


                
            else:
                if not RackName or not ShelfName or not StoreLocation or not Location:
                    return JsonResponse({'warn': 'RackName, ShelfName, StoreLocation and Location are mandatory fields'})

                if Shelf_Master_Detials.objects.filter(Shelf_Name=ShelfName,Rack_Name__Rack_Id=RackName,Rack_Name__Location_Name__Location_Id=Location,Rack_Name__Store_Location_Name__Store_Id=StoreLocation).exists():
                    return JsonResponse({'warn': f"The Shelf Detials are already present in the name of {ShelfName} and {RackName} "})
                else:
                    Shelf_instance=Shelf_Master_Detials(
                        Shelf_Name=ShelfName,
                        Rack_Name=RackDetials_Instance,
                        created_by=created_by

                    )
                    Shelf_instance.save()
                    
                    return JsonResponse ({'success':'Shelf Detials Added Successfully'})


        except Exception as e:
            print(f'An error occurred:{str(e)}')
            return JsonResponse ({'error':'An internal server error Occurred'},status=500)
    elif request.method == "GET":
        try:
            SearchLocation=request.GET.get('SearchLocation')
            StoreLocation=request.GET.get('StoreLocation')
            RackName=request.GET.get('RackName')


            Shelf_Master=Shelf_Master_Detials.objects.all()

            if SearchLocation:
                Shelf_Master=Shelf_Master.filter(Rack_Name__Location_Name__Location_Id=SearchLocation)
            
            if StoreLocation:
                Shelf_Master=Shelf_Master.filter(Rack_Name__Store_Location_Name__Store_Id=StoreLocation)
            
            if RackName:
                Shelf_Master=Shelf_Master.filter(Rack_Name__Rack_Id=RackName)

            shelf_Master_Array =[]

            for row in Shelf_Master:
                Shelf_dict={
                    'id':row.Shelf_Id,
                    'Shelf_Name':row.Shelf_Name,
                    'Rack_Name':row.Rack_Name.Rack_Name,
                    'Rack_Id':row.Rack_Name.Rack_Id,
                    'Location_Name':row.Rack_Name.Location_Name.Location_Name,
                    'Location_Id':row.Rack_Name.Location_Name.Location_Id,                    
                    'Store_Location':row.Rack_Name.Store_Location_Name.Store_Name,
                    'Store_Location_Id':row.Rack_Name.Store_Location_Name.Store_Id,
                    "Status":row.Status,
                }
                shelf_Master_Array.append(Shelf_dict)
            
            return JsonResponse (shelf_Master_Array,safe=False)
        
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse ({'error': 'An internal server error occurred'}, status=500)



# -----------------------------------------------------------------------------------


@csrf_exempt
@require_http_methods(["POST", "OPTIONS", "GET"])
def Tray_Detials_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)

            TrayID = data.get("TrayID", '')
            RackName = data.get("RackName")
            ShelfName = data.get("ShelfName")
            TrayName = data.get("TrayName")
            Location = data.get('Location')
            StoreLocation = data.get('StoreLocation')
            created_by = data.get('created_by')
            Statusedit=data.get('Statusedit',False)

            if ShelfName:
                Shelf_instance = Shelf_Master_Detials.objects.get(pk=ShelfName)


            if TrayID:
                if Statusedit:
                    Tray_instance=Tray_Master_Details.objects.get(pk=TrayID)
                    Tray_instance.Status=  not Tray_instance.Status
                    Tray_instance.save()
                    
                    return JsonResponse({'success': 'Tray Detials Updated successfully'})

                else:
                    if not RackName or not ShelfName or not TrayName or not Location or not StoreLocation:
                        return JsonResponse({'warn': 'RackName, ShelfName, TrayName, StoreLocation and Location are mandatory fields'})
                    if Tray_Master_Details.objects.filter(Tray_Name=TrayName).exclude(pk=TrayID).exists():
                        return JsonResponse ({'warn':f"The Tray Detials are already present in the name of {TrayName} "})
                    else:
                        Tray_instance=Tray_Master_Details.objects.get(pk=TrayID)
                        Tray_instance.Tray_Name=TrayName
                        Tray_instance.Shelf_Name=Shelf_instance                   
                        Tray_instance.created_by=created_by
                        Tray_instance.save()

                    return JsonResponse({'success': 'Tray Detials Updated successfully'})
            
            else:       
                if not RackName or not ShelfName or not TrayName or not Location:
                    return JsonResponse({'warn': 'RackName, ShelfName, TrayName, and Location are mandatory fields'})
                if Tray_Master_Details.objects.filter(Tray_Name=TrayName).exists():
                        return JsonResponse ({'warn':f"The Tray Detials are already present in the name of {TrayName} "})
                
                if Tray_Master_Details.objects.filter(
                    Tray_Name=TrayName,
                    Shelf_Name__Shelf_Id=ShelfName,
                    Shelf_Name__Rack_Name__Rack_Id=RackName,
                    Shelf_Name__Rack_Name__Location_Name__Location_Id=Location
                ).exists():
                    return JsonResponse({
                        'warn': f"The Tray Detials are already present in the name of {ShelfName},{RackName} and {TrayName}"
                    })

                Tray_instance = Tray_Master_Details(
                    Tray_Name=TrayName,
                    Shelf_Name=Shelf_instance,
                    created_by=created_by
                )
                Tray_instance.save()

                return JsonResponse({'success': 'Tray details saved successfully'})

        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

    elif request.method == "GET":
        try:
            SearchLocation=request.GET.get('SearchLocation')
            StoreLocation=request.GET.get('StoreLocation')
            RackName=request.GET.get('RackName')
            ShelfName=request.GET.get('ShelfName')
            Statuschek=request.GET.get('Statuschek')
            BookingStatus=request.GET.get('BookingStatus')


            # print('ShelfName',ShelfName)

            Tray_Master=Tray_Master_Details.objects.all()

            if SearchLocation:
                Tray_Master=Tray_Master.filter(Shelf_Name__Rack_Name__Location_Name__Location_Id=SearchLocation)
            
            if StoreLocation:
                Tray_Master=Tray_Master.filter(Shelf_Name__Rack_Name__Store_Location_Name__Store_Id=StoreLocation)
            
            if RackName:
                Tray_Master=Tray_Master.filter(Shelf_Name__Rack_Name__Rack_Id=RackName)
            
            if ShelfName:
                Tray_Master=Tray_Master.filter(Shelf_Name__Shelf_Id=ShelfName)
            
            if Statuschek:
                Tray_Master=Tray_Master.filter(Status=True)
            
            if BookingStatus:
                Tray_Master=Tray_Master.filter(Booking_Status=BookingStatus)


            Tray_Master_Array =[]

            for row in Tray_Master:
                Tray_dict={
                    'id':row.Tray_Id,
                    'Tray_Name':row.Tray_Name,
                    'Shelf_Id':row.Shelf_Name.Shelf_Id,
                    'Shelf_Name':row.Shelf_Name.Shelf_Name,
                    'Rack_Name':row.Shelf_Name.Rack_Name.Rack_Name,
                    'Rack_Id':row.Shelf_Name.Rack_Name.Rack_Id,
                    'Store_Location':row.Shelf_Name.Rack_Name.Store_Location_Name.Store_Name,
                    'Store_Location_Id':row.Shelf_Name.Rack_Name.Store_Location_Name.Store_Id,
                    'Location_Name':row.Shelf_Name.Rack_Name.Location_Name.Location_Name,
                    'Location_Id':row.Shelf_Name.Rack_Name.Location_Name.Location_Id,
                    "Status":row.Status,
                    'BookingStatus':row.Booking_Status
                }
                Tray_Master_Array.append(Tray_dict)
            
            return JsonResponse (Tray_Master_Array,safe=False)
        
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse ({'error': 'An internal server error occurred'}, status=500)


# ==============================TrayManagement===============================


@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def Difine_Tray_For_Products(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            print(data,'kkkkk')
            Tray_ID = data.get('TrayName')
            ItemCode = data.get('ItemCode')
            created_by = data.get('created_by')            
            StoreLocation = data.get('StoreLocation')

            ItemConfirmed = data.get('ItemConfirmed')
            TrayManagementId=data.get('TrayManagementId')

            if not Tray_ID:
                return JsonResponse({'warn': 'TrayName is a mandatory field'}, status=400)
            else:                
                Tray_Master_instance = Tray_Master_Details.objects.get(pk=Tray_ID)

            if not ItemCode:
                return JsonResponse({'warn': 'ItemCode and ItemName are mandatory fields'}, status=400)
            else:
                Product_Master_instance=Product_Master_All_Category_Details.objects.get(pk=ItemCode)
            
            if ItemCode and Tray_ID :
                existing_tray_management = Tray_management_Details.objects.filter(
                        Product_Detials__pk=ItemCode,
                        Tray_Name__Shelf_Name__Rack_Name__Store_Location_Name__Store_Id=StoreLocation
                    ).select_related('Tray_Name').first()

            if TrayManagementId and Tray_ID and ItemCode :
                    
                    print( TrayManagementId , Tray_ID , ItemCode ,'wertyui')

                    Delete_Tray_management_instance = Tray_management_Details.objects.get(pk=TrayManagementId)

                    DelTray_Master_instance = Tray_Master_Details.objects.get(pk=Delete_Tray_management_instance.Tray_Name.Tray_Id)
                    
                    DelMedical_Product_instance = Product_Master_All_Category_Details.objects.get(pk=Delete_Tray_management_instance.Product_Detials.pk)

                    Prev_Tray_management_instance = Prev_Tray_management_Details(
                    Prev_Tray_Name=DelTray_Master_instance,
                    Prev_Product_Detials=DelMedical_Product_instance,
                    Create_by=Delete_Tray_management_instance.Create_by,
                    )

                    Prev_Tray_management_instance.save()

                    Delete_Tray_management_instance.delete()

                    Tray_Master_instance.Booking_Status = 'Available'
                    Tray_Master_instance.save()

                    return JsonResponse({'success': 'Item removed from tray and tray is now available'}, status=200)

            elif ItemConfirmed :

                Update_Tray_Master_Id=existing_tray_management.Tray_Management_Id

                Edit_Tray_management_instance = Tray_management_Details.objects.get(pk=Update_Tray_Master_Id)

                EditTray_Master_instance = Tray_Master_Details.objects.get(pk=Edit_Tray_management_instance.Tray_Name.Tray_Id)
                EditMedical_Product_instance = Product_Master_All_Category_Details.objects.get(pk=Edit_Tray_management_instance.Product_Detials.pk)

                Prev_Tray_management_instance = Prev_Tray_management_Details(
                    Prev_Tray_Name=EditTray_Master_instance,
                    Prev_Product_Detials=EditMedical_Product_instance,
                    Create_by=Edit_Tray_management_instance.Create_by,
                )

                Prev_Tray_management_instance.save()

                Edit_Tray_management_instance.delete()

                EditTray_Master_instance.Booking_Status = 'Available'
                EditTray_Master_instance.save()

                Tray_management_Details.objects.create(
                    Tray_Name=Tray_Master_instance,
                    Product_Detials=Product_Master_instance,
                    Create_by=created_by,
                )

                Tray_Master_instance.Booking_Status = 'Occupied'
                Tray_Master_instance.save()

                return JsonResponse({'success': 'Updated successfully'})
            
            
            else:
                if existing_tray_management:
                        Update_Tray_Master_instance = existing_tray_management.Tray_Name
                        store_location = Update_Tray_Master_instance.Shelf_Name.Rack_Name.Store_Location_Name.Store_Name                
                        return JsonResponse({
                            'Update': f'This Item already exists in the following tray. Do you want to change the item combination and free the tray?'
                                    f'Store Location: {store_location}, '
                                    f'Rack Name: {Update_Tray_Master_instance.Shelf_Name.Rack_Name.Rack_Name}, '
                                    f'Shelf Name: {Update_Tray_Master_instance.Shelf_Name.Shelf_Name}, '
                                    f'Tray Name: {Update_Tray_Master_instance.Tray_Name}'
                        })

                Tray_management_Details.objects.create(
                    Tray_Name=Tray_Master_instance,
                    Product_Detials=Product_Master_instance,
                    Create_by=created_by,
                )

                Tray_Master_instance.Booking_Status = 'Occupied'
                Tray_Master_instance.save()

                return JsonResponse({'success': 'Tray management details created successfully'}, status=201)

        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)
     

# --------------------------------------------------------------------------------------------------


@csrf_exempt
@require_http_methods(["GET"])
def Tray_Management_List_For_Products(request):
    if request.method == "GET":
        try:
            SearchLocation = request.GET.get('SearchLocation')
            StoreLocation = request.GET.get('StoreLocation')
            tray_status = request.GET.get('TrayStatus')
            rack_name = request.GET.get('RackName')
            shelf_name = request.GET.get('ShelfName')
            tray_name = request.GET.get('TrayName')
            ItemCode = request.GET.get('ItemCode')
            ProductCategory = request.GET.get('ProductCategory')
            SubCategory = request.GET.get('SubCategory')


            result_data = []

            Tray_Master_instance = Tray_Master_Details.objects.all()

            if SearchLocation:
                Tray_Master_instance = Tray_Master_instance.filter(
                    Shelf_Name__Rack_Name__Location_Name__Location_Id=SearchLocation
                )
            
            if StoreLocation:
                Tray_Master_instance = Tray_Master_instance.filter(
                    Shelf_Name__Rack_Name__Store_Location_Name__Store_Id=StoreLocation
                )

            if tray_status in ['Available', 'Occupied']:
                Tray_Master_instance = Tray_Master_instance.filter(
                    Booking_Status=tray_status, Status=True
                )
            if tray_status == 'InActive':
                Tray_Master_instance = Tray_Master_instance.filter(Status=False)
            
            if rack_name:
                Tray_Master_instance = Tray_Master_instance.filter(
                    Shelf_Name__Rack_Name__Rack_Id=rack_name
                )
            
            if shelf_name:
                Tray_Master_instance = Tray_Master_instance.filter(
                    Shelf_Name__Shelf_Id=shelf_name
                )
            
            if tray_name:
                Tray_Master_instance = Tray_Master_instance.filter(
                    Tray_Id=tray_name
                )
            
            if ItemCode:
                tray_management_instance = Tray_management_Details.objects.get(Product_Detials__pk=ItemCode)
                Tray_Master_instance = Tray_Master_instance.filter(Tray_Id=tray_management_instance.Tray_Name.Tray_Id)

            
            
            for row in Tray_Master_instance:
                dic = {
                    'id': row.Tray_Id,
                    'Tray_Name': row.Tray_Name,
                    'Shelf_Id': row.Shelf_Name.Shelf_Id,
                    'Shelf_Name': row.Shelf_Name.Shelf_Name,
                    'Rack_Id': row.Shelf_Name.Rack_Name.Rack_Id,
                    'Rack_Name': row.Shelf_Name.Rack_Name.Rack_Name,                    
                    'Store_Location_Id': row.Shelf_Name.Rack_Name.Store_Location_Name.Store_Id,
                    'Store_Location_Name': row.Shelf_Name.Rack_Name.Store_Location_Name.Store_Name,
                    'Location_Id': row.Shelf_Name.Rack_Name.Location_Name.Location_Id,
                    'Location_Name': row.Shelf_Name.Rack_Name.Location_Name.Location_Name,
                    'Status': row.Status,
                    'Booking_Status': row.Booking_Status,
                }
                if row.Booking_Status == 'Occupied':
                    Tray_management_instance = Tray_management_Details.objects.get(Tray_Name__Tray_Id=row.Tray_Id)
                    dic['Item_Code'] = Tray_management_instance.Product_Detials.pk
                    dic['Item_Name'] = Tray_management_instance.Product_Detials.ItemName
                    dic['Tray_Management_Id'] = Tray_management_instance.Tray_Management_Id
                else:
                    dic['Item_Code'] = ''
                    dic['Item_Name'] = ''

                result_data.append(dic)

            return JsonResponse(result_data, safe=False)
            
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse({'error': str(e)}, safe=False, status=500)









# ------------------------------------------------------------------------------
# ---------------------------------ProductCatgory-------------------------------












@csrf_exempt
@require_http_methods(["POST","OPTIONS","GET"])
def ProductCategory_Master_link (request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            ProductCategoryId=data.get('ProductCategoryId')
        
        except Exception as e:
             print(f'An error occurred: {str(e)}')
             return JsonResponse ({'error':'An internal server error occurred'},status=500)


        
    elif request.method == 'GET':
        try:
            Medical_ProductCategory_instance=ProductCategory_Details.objects.all()

            Category_Array=[]

            for row in Medical_ProductCategory_instance:
                Category_dic={
                    'id':row.ProductCategory_Id,
                    'ProductCategoryName':row.ProductCategory_Name,
                    'Status':row.Status
                }
                Category_Array.append(Category_dic)

            return JsonResponse (Category_Array,safe=False)

        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse ({'error':'An internal server error occurred'},status=500)


@csrf_exempt
@require_http_methods(["POST","OPTIONS","GET"])
def SubCategory_Master_link (request):
    if request.method == 'POST':
        try:
            data=json.loads(request.body)
            print('data',data)

            SubCategoryId=data.get('SubCategoryId','')
            ProductCategoryId=data.get('ProductCategoryId')
            SubCategoryName=data.get('SubCategoryName')
            
            if SubCategoryName:
                Uppercase_name = SubCategoryName.upper()
                normalized_name = SubCategoryName.replace(" ", "").lower()
            else:
                
                Uppercase_name = None
                normalized_name = None
            
            created_by=data.get('created_by')
            Statusedit=data.get('Statusedit')

            if SubCategoryId:
                if Statusedit:
                    SubCategory_Instance=SubCategory_Detailes.objects.get(pk=SubCategoryId)
                    SubCategory_Instance.Status=not SubCategory_Instance.Status
                    SubCategory_Instance.save()

                    return JsonResponse ({'success': 'SubCategory Updated successfully'})
                else:
                    if not ProductCategoryId:
                        return JsonResponse({'warn': 'Product Category Name are mandatory fields'})
                    if not SubCategoryName:
                        return JsonResponse({'warn': 'SubCategory Name are mandatory fields'})
                    if ProductCategoryId:
                        ProductCat_instance=Product_Category_Product_Details.objects.get(pk=ProductCategoryId)
                    existing_Sub_category = SubCategory_Detailes.objects.annotate(
                        normalized_name=Func(
                            'SubCategoryName',
                            function='LOWER',
                            template="REPLACE(%(expressions)s, ' ', '')"
                        )
                    ).filter(ProductCategoryId=ProductCat_instance,normalized_name = normalized_name).exclude(pk=SubCategoryId)
                    if existing_Sub_category.exists():
                        return JsonResponse ({'Warn':f"The Product Category are already present in the name of {Uppercase_name}"})
                    
                    SubCategory_Instance=SubCategory_Detailes.objects.get(pk=SubCategoryId)
                    SubCategory_Instance.ProductCategoryId=ProductCat_instance
                    SubCategory_Instance.SubCategoryName=Uppercase_name
                    SubCategory_Instance.save()

                    return JsonResponse ({'success': 'SubCategory Updated successfully'})


                    



            else:
                if not ProductCategoryId:
                    return JsonResponse({'warn': 'Product Category Name are mandatory fields'})
                if not SubCategoryName:
                    return JsonResponse({'warn': 'SubCategory Name are mandatory fields'})
                if ProductCategoryId:
                    ProductCat_instance=Product_Category_Product_Details.objects.get(pk=ProductCategoryId)
                existing_Sub_category = SubCategory_Detailes.objects.annotate(
                    normalized_name=Func(
                        'SubCategoryName',
                        function='LOWER',
                        template="REPLACE(%(expressions)s, ' ', '')"
                    )
                ).filter(ProductCategoryId=ProductCat_instance,normalized_name = normalized_name)
                if existing_Sub_category.exists():
                    return JsonResponse ({'warn':f"The Product Category are already present in the name of {Uppercase_name}"})
                
                else:
                    SubCategory_Instance=SubCategory_Detailes(
                        ProductCategoryId=ProductCat_instance,
                        SubCategoryName=Uppercase_name,
                        Created_by=created_by
                    )
                    SubCategory_Instance.save()

                    return JsonResponse ({'success': 'SubCategory saved successfully'})

        except Exception as e:
            print(f'An error occurred :{str(e)}')
            return JsonResponse (f'error:{str(e)}')

    elif request.method == 'GET':
        try:
            ProductCategory =request.GET.get('ProductCategory',None)

            SubCategory_instance=SubCategory_Detailes.objects.all().order_by('ProductCategoryId')

            if ProductCategory:                          
                SubCategory_instance=SubCategory_instance.filter(ProductCategoryId__pk = int(ProductCategory),Status=True)
                
            SubCategoryArray=[]

            for row in SubCategory_instance:
                Cat_dic={
                    'id':row.SubCategory_Id,
                    'ProductCategoryId':row.ProductCategoryId.pk,
                    'ProductCategory_Name':row.ProductCategoryId.ProductCategory_Name,
                    'SubCategoryName':row.SubCategoryName,
                    'Status':row.Status,
                }
                SubCategoryArray.append(Cat_dic)

            return JsonResponse(SubCategoryArray,safe=False)
        
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse ({'error': 'An internal server error occurred'},status=500)


@csrf_exempt
@require_http_methods(["POST","OPTIONS","GET"])
def Product_Group_Link (request):
    if request.method == 'POST':
        try:
            data=json.loads(request.body)

            print("ProductGroupName",data)

            ProductGroupID=data.get('ProductGroupID')
            ProductCategoryId=data.get('ProductCategoryName', None)
            SubProductCategoryId=data.get('SubProductCategoryName', None)
            ProductGroupName=data.get('ProductGroupName')
            created_by=data.get('created_by')
            Statusedit=data.get('Statusedit')

            if ProductGroupID:
                if Statusedit:
                    Product_Group_Master_instance=Product_Group_Master_Details.objects.get(pk=ProductGroupID)
                    Product_Group_Master_instance.Status=not Product_Group_Master_instance.Status
                    Product_Group_Master_instance.save()

                    return JsonResponse ({'success': 'Drug Group Updated successfully'})
                else:
                    if not ProductGroupName:
                        return JsonResponse({'warn': 'Drug Group Name are mandatory fields'})
                    if Product_Group_Master_Details.objects.filter(ProductGroup_Name=ProductGroupName).exclude(pk=ProductGroupID).exists():
                        return JsonResponse({'warn':f"The Product Category are already present in the name of {ProductGroupName}" })
                    if not ProductCategoryId:
                        return({'warn': 'ProductCategory not found'})
                    if not SubProductCategoryId:
                        return JsonResponse({'warn': "SubCategory not found"})
                    try:
                        ProductCategory_instance = Product_Category_Product_Details.objects.get(pk=ProductCategoryId)
                        print("ProductCategory_instance",ProductCategory_instance)
                    
                    except Product_Category_Product_Details.DoesNotExist:
                        return JsonResponse({'warn':  "Productid not found"})
                    
                    try:
                        Sub_ProductCategory_instance = SubCategory_Detailes.objects.get(pk=SubProductCategoryId)
                        print("Sub_ProductCategory_instance",Sub_ProductCategory_instance)
                    except Sub_ProductCategory_instance.DoesNotExist:
                        return JsonResponse({'warn': 'SubProduct Category not found'})
                        
                    else:
                        Product_Group_Master_instance=Product_Group_Master_Details.objects.get(pk=ProductGroupID)
                        Product_Group_Master_instance.ProductCategory=ProductCategory_instance
                        Product_Group_Master_instance.SubProductCategory=Sub_ProductCategory_instance
                        Product_Group_Master_instance.ProductGroup_Name=ProductGroupName
                        Product_Group_Master_instance.save()
                        
                        return JsonResponse ({'success': 'Drug Group Updated successfully'})
                        

            else:
                if not ProductGroupName:
                    return JsonResponse ({'warn':'Drug Group Name are mandatory fields'})
                if Product_Group_Master_Details.objects.filter(ProductGroup_Name=ProductGroupName).exists():
                    return JsonResponse ({'warn': f"The Drug Group Name are already present in the name of {ProductGroupName}"})
                if not ProductCategoryId:
                    return({'warn': 'ProductCategory not found'})
                if not SubProductCategoryId:
                    return JsonResponse({'warn': "SubCategory not found"})
                try:
                    ProductCategory_instance = Product_Category_Product_Details.objects.get(pk=ProductCategoryId)
                    print("ProductCategory_instance",ProductCategory_instance)
                
                except Product_Category_Product_Details.DoesNotExist:
                    return JsonResponse({'warn':  "Productid not found"})
                
                try:
                    Sub_ProductCategory_instance = SubCategory_Detailes.objects.get(pk=SubProductCategoryId)
                    print("Sub_ProductCategory_instance",Sub_ProductCategory_instance)
                except Sub_ProductCategory_instance.DoesNotExist:
                    return JsonResponse({'warn': 'SubProduct Category not found'})
                else:
                    Product_Group_instance=Product_Group_Master_Details(
                        ProductCategory=ProductCategory_instance,
                        SubProductCategory=Sub_ProductCategory_instance,
                        ProductGroup_Name=ProductGroupName,
                        Create_by=created_by
                    )
                    Product_Group_instance.save()

                    return JsonResponse ({'success': 'Drug Group Name saved successfully'})
        
        except Exception as e:
            print(f'An error occurred:{str(e)}')
            return JsonResponse ({'error':'An internal server error occurred'},status=500)
    elif request.method == 'GET':
        try:
            Product_Group_Master_instance=Product_Group_Master_Details.objects.all()

            Product_Group=[]

            for row in Product_Group_Master_instance:
                Drug_dic={
                    'id':row.ProductGroup_Id,
                    'ProductGroupName':row.ProductGroup_Name,
                    'ProductCategoryName':row.ProductCategory.ProductCategory_Name if row.ProductCategory else None,
                    'ProductCategory':row.ProductCategory.pk if row.ProductCategory else None,
                    'SubProductCategoryName':row.SubProductCategory.SubCategoryName if row.SubProductCategory else None,
                    'SubProductCategory':row.SubProductCategory.pk if row.SubProductCategory else None,
                    'Status':row.Status
                }
                Product_Group.append(Drug_dic)

            return JsonResponse (Product_Group,safe=False)
        except Exception as e:
            print(f'An error occurred:{str(e)}')
            return JsonResponse ({'error':'An internal server error occurred'},status=500)


@csrf_exempt
@require_http_methods(["POST","OPTIONS","GET"])
def Pack_Type_link (request):
    if request.method == 'POST':
        try:
            data=json.loads(request.body)

            print("data",data)

            PackTypeID=data.get('PackTypeID')
            PackTypeName=data.get('PackTypeName')
            ProductCategoryId=data.get('ProductCategoryName', None)
            SubProductCategoryId=data.get('SubProductCategoryName', None)
            created_by=data.get('created_by')
            Statusedit=data.get('Statusedit')

            if PackTypeID:
                if Statusedit:
                    Pack_Type_Master_instance=Pack_Type_Master_Details.objects.get(pk=PackTypeID)
                    Pack_Type_Master_instance.Status=not Pack_Type_Master_instance.Status
                    Pack_Type_Master_instance.save()

                    return JsonResponse ({'success': 'Pack Type Updated successfully'})
                else:
                    if not PackTypeName:
                        return JsonResponse({'warn': 'Pack Type Name are mandatory fields'})
                    if Pack_Type_Master_Details.objects.filter(PackType_Name=PackTypeName).exclude(pk=PackTypeID).exists():
                        return JsonResponse({'warn':f"The Pack Type are already present in the name of {PackTypeName}" })
                    if not ProductCategoryId:
                        return({'warn': 'ProductCategory not found'})
                    if not SubProductCategoryId:
                        return JsonResponse({'warn': "SubCategory not found"})
                    try:
                        ProductCategory_instance = Product_Category_Product_Details.objects.get(pk=ProductCategoryId)
                        print("ProductCategory_instance",ProductCategory_instance)
                    
                    except Product_Category_Product_Details.DoesNotExist:
                        return JsonResponse({'warn':  "Productid not found"})
                    
                    try:
                        Sub_ProductCategory_instance = SubCategory_Detailes.objects.get(pk=SubProductCategoryId)
                        print("Sub_ProductCategory_instance",Sub_ProductCategory_instance)
                    except Sub_ProductCategory_instance.DoesNotExist:
                        return JsonResponse({'warn': 'SubProduct Category not found'})
                        
                    else:
                        Pack_Type_Master_instance=Pack_Type_Master_Details.objects.get(pk=PackTypeID)
                        Pack_Type_Master_instance.ProductCategory=ProductCategory_instance
                        Pack_Type_Master_instance.SubProductCategory=Sub_ProductCategory_instance
                        Pack_Type_Master_instance.PackType_Name=PackTypeName
                        Pack_Type_Master_instance.save()
                        
                        return JsonResponse ({'success': 'Pack Type Updated successfully'})
                        

            else:
                if not PackTypeName:
                    return JsonResponse ({'warn':'Pack Type Name are mandatory fields'})
                if Pack_Type_Master_Details.objects.filter(PackType_Name=PackTypeName).exists():
                    return JsonResponse ({'warn': f"The Pack Type Name are already present in the name of {PackTypeName}"})
                if not ProductCategoryId:
                    return({'warn': 'ProductCategory not found'})
                if not SubProductCategoryId:
                    return JsonResponse({'warn': "SubCategory not found"})
                try:
                    ProductCategory_instance = Product_Category_Product_Details.objects.get(pk=ProductCategoryId)
                    print("ProductCategory_instance",ProductCategory_instance)
                
                except Product_Category_Product_Details.DoesNotExist:
                    return JsonResponse({'warn':  "Productid not found"})
                
                try:
                    Sub_ProductCategory_instance = SubCategory_Detailes.objects.get(pk=SubProductCategoryId)
                    print("Sub_ProductCategory_instance",Sub_ProductCategory_instance)
                except Sub_ProductCategory_instance.DoesNotExist:
                    return JsonResponse({'warn': 'SubProduct Category not found'})
                else:
                    Pack_Type_instance=Pack_Type_Master_Details(
                        ProductCategory=ProductCategory_instance,
                        SubProductCategory=Sub_ProductCategory_instance,
                        PackType_Name=PackTypeName,
                        Create_by=created_by
                    )
                    Pack_Type_instance.save()

                    return JsonResponse ({'success': 'Pack Type Name saved successfully'})
        
        except Exception as e:
            print(f'An error occurred:{str(e)}')
            return JsonResponse ({'error':'An internal server error occurred'},status=500)
    elif request.method == 'GET':
        try:
            Pack_Type_Master_instance=Pack_Type_Master_Details.objects.all()

            Pack_Type_array=[]
            
            for row in Pack_Type_Master_instance:
                Drug_dic={
                    'id':row.pk,
                    'PackTypeName':row.PackType_Name,
                    'ProductCategoryName':row.ProductCategory.ProductCategory_Name if row.ProductCategory else None,
                    'ProductCategory':row.ProductCategory.pk if row.ProductCategory else None,
                    'SubProductCategoryName':row.SubProductCategory.SubCategoryName if row.SubProductCategory else None,
                    'SubProductCategory':row.SubProductCategory.pk if row.SubProductCategory else None,                   
                    'Status':row.Status
                }
                Pack_Type_array.append(Drug_dic)
            return JsonResponse (Pack_Type_array,safe=False)
        except Exception as e:
            print(f'An error occurred:{str(e)}')
            return JsonResponse ({'error':'An internal server error occurred'},status=500)


@csrf_exempt
@require_http_methods(["POST","OPTIONS","GET"])
def GenericName_Master_Link (request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # print("gent",data)

            GenericNameID=data.get('GenericNameID')
            GenericName=data.get('GenericName')
            ProductCategoryId=data.get('ProductCategoryName', None)
            SubProductCategoryId=data.get('SubProductCategoryName', None)
            created_by=data.get('created_by')
            Statusedit=data.get('Statusedit')

            
            if GenericNameID:
                if Statusedit:
                    GenericName_Instance=GenericName_Master_Details.objects.get(pk=GenericNameID)
                    GenericName_Instance.Status = not GenericName_Instance.Status
                    GenericName_Instance.save()
                    
                    return JsonResponse ({'success': 'Generic Name Updated successfully'})

                else:

                    if not GenericName:
                        return JsonResponse ({'warn':'Generic Name are mandatory fields'})
                    if GenericName_Master_Details.objects.filter(GenericName=GenericName).exclude(pk=GenericNameID).exists():
                        return JsonResponse ({'warn': f"The Generic Name are already present in the name of {GenericName}"})
                    if not ProductCategoryId:
                        return({'warn': 'ProductCategory not found'})
                    if not SubProductCategoryId:
                        return JsonResponse({'warn': "SubCategory not found"})
                    try:
                        ProductCategory_instance = Product_Category_Product_Details.objects.get(pk=ProductCategoryId)
                        print("ProductCategory_instance",ProductCategory_instance)
                    
                    except Product_Category_Product_Details.DoesNotExist:
                        return JsonResponse({'warn':  "Productid not found"})
                    
                    try:
                        Sub_ProductCategory_instance = SubCategory_Detailes.objects.get(pk=SubProductCategoryId)
                        print("Sub_ProductCategory_instance",Sub_ProductCategory_instance)
                    except Sub_ProductCategory_instance.DoesNotExist:
                        return JsonResponse({'warn': 'SubProduct Category not found'})
                                           
                    GenericName_Instance=GenericName_Master_Details.objects.get(pk=GenericNameID)
                    GenericName_Instance.ProductCategory=ProductCategory_instance
                    GenericName_Instance.SubProductCategory=Sub_ProductCategory_instance
                    GenericName_Instance.GenericName=GenericName
                    GenericName_Instance.Updated_by=created_by
                    GenericName_Instance.save()

                    return JsonResponse ({'success': 'Generic Name Updated successfully'})





            else:
                if not GenericName:
                    return JsonResponse ({'warn':'Generic Name are mandatory fields'})
                if GenericName_Master_Details.objects.filter(GenericName=GenericName).exists():
                        return JsonResponse ({'warn': f"The Generic Name are already present in the name of {GenericName}"})
                if not ProductCategoryId:
                    return({'warn': 'ProductCategory not found'})
                if not SubProductCategoryId:
                    return JsonResponse({'warn': "SubCategory not found"})
                try:
                    ProductCategory_instance = Product_Category_Product_Details.objects.get(pk=ProductCategoryId)
                    print("ProductCategory_instance",ProductCategory_instance)
                
                except Product_Category_Product_Details.DoesNotExist:
                    return JsonResponse({'warn':  "Productid not found"})
                
                try:
                    Sub_ProductCategory_instance = SubCategory_Detailes.objects.get(pk=SubProductCategoryId)
                    print("Sub_ProductCategory_instance",Sub_ProductCategory_instance)
                except Sub_ProductCategory_instance.DoesNotExist:
                    return JsonResponse({'warn': 'SubProduct Category not found'})                
                else:
                    GenericName_Ins=GenericName_Master_Details(
                        ProductCategory=ProductCategory_instance,
                        SubProductCategory=Sub_ProductCategory_instance,
                        GenericName=GenericName,
                        Create_by=created_by
                    )
                    GenericName_Ins.save()
            
                    return JsonResponse ({'success': 'Generic Name saved successfully'})
        
        except Exception as e :
            print(f'An error occurred:{str(e)}')
            return JsonResponse ({'error':'An internal server error occurred'},status=500)

    elif request.method == "GET":
        try:

            GenericName_Instance=GenericName_Master_Details.objects.all()

            GenericName_Array=[]

            for row in GenericName_Instance :
                Gen_dic={
                    'id':row.pk,
                    'GenericName':row.GenericName,
                    'ProductCategoryName':row.ProductCategory.ProductCategory_Name if row.ProductCategory else None,
                    'ProductCategory':row.ProductCategory.pk if row.ProductCategory else None,
                    'SubProductCategoryName':row.SubProductCategory.SubCategoryName if row.SubProductCategory else None,
                    'SubProductCategory':row.SubProductCategory.pk if row.SubProductCategory else None,
                    'Status':row.Status,
                }
                GenericName_Array.append(Gen_dic)
            
            return JsonResponse(GenericName_Array,safe=False)

        except Exception as e:
            print(f'An error occurred:{str(e)}')
            return JsonResponse ({'error':'An internal server error occurred'},status=500)




@csrf_exempt
@require_http_methods(["POST","OPTIONS","GET"])
def CompanyName_Master_Link (request):
    if request.method == "POST":
        try:
            data =json.loads(request.body)

            CompanyNameId=data.get('CompanyNameId')
            CompanyName=data.get('CompanyName','')
            ProductCategoryId=data.get('ProductCategoryName', None)
            SubProductCategoryId=data.get('SubProductCategoryName', None)
            created_by=data.get('created_by')
            Statusedit=data.get('Statusedit')

            if CompanyNameId:
                if Statusedit:
                    CompanyName_Instance=CompanyName_mfg_Master_Details.objects.get(pk=CompanyNameId)
                    CompanyName_Instance.Status = not CompanyName_Instance.Status
                    CompanyName_Instance.save()

                    return JsonResponse ({'success': 'Company Name Updated successfully'})
                
                else:
                    if not CompanyName:
                        return JsonResponse ({'warn':'Company Name are mandatory fields'})
                    if CompanyName_mfg_Master_Details.objects.filter(CompanyName=CompanyName).exclude(pk=CompanyNameId).exists():
                        return JsonResponse ({'warn': f"The Company Name are already present in the name of {CompanyName}"})
                    if not ProductCategoryId:
                        return({'warn': 'ProductCategory not found'})
                    if not SubProductCategoryId:
                        return JsonResponse({'warn': "SubCategory not found"})
                    try:
                        ProductCategory_instance = Product_Category_Product_Details.objects.get(pk=ProductCategoryId)
                        print("ProductCategory_instance",ProductCategory_instance)
                    
                    except Product_Category_Product_Details.DoesNotExist:
                        return JsonResponse({'warn':  "Productid not found"})
                    
                    try:
                        Sub_ProductCategory_instance = SubCategory_Detailes.objects.get(pk=SubProductCategoryId)
                        print("Sub_ProductCategory_instance",Sub_ProductCategory_instance)
                    except Sub_ProductCategory_instance.DoesNotExist:
                        return JsonResponse({'warn': 'SubProduct Category not found'})
                                            
                    else:
                        CompanyName_Instance=CompanyName_mfg_Master_Details.objects.get(pk=CompanyNameId)
                        CompanyName_Instance.ProductCategory=ProductCategory_instance
                        CompanyName_Instance.SubProductCategory=Sub_ProductCategory_instance
                        CompanyName_Instance.CompanyName = CompanyName
                        CompanyName_Instance.Updated_by = created_by
                        CompanyName_Instance.save()

                        return JsonResponse ({'success': 'Company Name Updated successfully'})


            else:
                if not CompanyName:
                    return JsonResponse ({'warn':'Company Name are mandatory fields'})
                if CompanyName_mfg_Master_Details.objects.filter(CompanyName=CompanyName).exists():
                        return JsonResponse ({'warn': f"The Company Name are already present in the name of {CompanyName}"})
                if not ProductCategoryId:
                    return({'warn': 'ProductCategory not found'})
                if not SubProductCategoryId:
                    return JsonResponse({'warn': "SubCategory not found"})
                try:
                    ProductCategory_instance = Product_Category_Product_Details.objects.get(pk=ProductCategoryId)
                    print("ProductCategory_instance",ProductCategory_instance)
                
                except Product_Category_Product_Details.DoesNotExist:
                    return JsonResponse({'warn':  "Productid not found"})
                
                try:
                    Sub_ProductCategory_instance = SubCategory_Detailes.objects.get(pk=SubProductCategoryId)
                    print("Sub_ProductCategory_instance",Sub_ProductCategory_instance)
                except Sub_ProductCategory_instance.DoesNotExist:
                    return JsonResponse({'warn': 'SubProduct Category not found'})
                else:
                    CompanyName_instance=CompanyName_mfg_Master_Details(
                        ProductCategory=ProductCategory_instance,
                        SubProductCategory=Sub_ProductCategory_instance,
                        CompanyName=CompanyName,
                        Create_by=created_by,
                    )

                    CompanyName_instance.save()
                
                    return JsonResponse ({'success': 'Company Name saved successfully'})
            
            
        except Exception as e:
            print(f'An error Accurred:{str(e)}')
            return  JsonResponse ({'error':'An internal server error occurred'},status=500)

    elif request.method == "GET":
        try:
            CompanyName_Instance=CompanyName_mfg_Master_Details.objects.all()

            CompanyName_Array=[]

            for row in CompanyName_Instance:
                dic={
                    'id':row.pk,
                    'CompanyName':row.CompanyName,
                    'ProductCategoryName':row.ProductCategory.ProductCategory_Name if row.ProductCategory else None,
                    'ProductCategory':row.ProductCategory.pk if row.ProductCategory else None,
                    'SubProductCategoryName':row.SubProductCategory.SubCategoryName if row.SubProductCategory else None,
                    'SubProductCategory':row.SubProductCategory.pk if row.SubProductCategory else None,
                    'Status':row.Status
                }
                CompanyName_Array.append(dic)

            return JsonResponse (CompanyName_Array,safe=False)
        
        except Exception as e :
            print(f'An error occurred:{str(e)}')
            return JsonResponse ({'error':'An internal server error occurred'},status=500)




@csrf_exempt
@require_http_methods(["POST", "OPTIONS", "GET"])
def Medical_Stock_InsetLink(request):
    if request.method == "POST":
        try:
            Getfile = request.FILES.get('file')
            print('file', Getfile)

            if Getfile.name.endswith('.csv'):
                df = pd.read_csv(Getfile)
            else:
                return JsonResponse({
                    'error': 'Unsupported file format. Please upload a CSV or Excel file'
                })

            csv_data = df.to_dict(orient='records')

            Medical_Stock_FileUpload.objects.all().delete()

            for row in csv_data:
                for key in row:
                    if pd.isna(row[key]):
                        if isinstance(row[key], str):
                            row[key] = 'None'
                        elif isinstance(row[key], (int, float)):
                            row[key] = None
        
                Medical_Stock_FileUpload.objects.create(
                    Product_Id=row.get('Product_Id', 'None'),
                    Product_Name=row.get('Product_Name', 'None'),
                    Generic_Name=row.get('Generic_Name', 'None'),
                    Available_Qantity=row.get('Available_Qantity', 0),
                    Item_Type = row.get('Item_Type'),
                    Dosage = row.get('Dosage')
                )

            return JsonResponse({'message': 'File uploaded and data inserted successfully'})

        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

    elif request.method == "GET":
        try:
            medical_stock_data = Medical_Stock_FileUpload.objects.all()
            data = [
                {
                    'id': item.Product_Id,
                    'Product_Name': item.Product_Name,
                    'Generic_Name': item.Generic_Name,
                    'Item_Type':item.Item_Type,
                    'Dosage':item.Dosage,
                    'Available_Qantity': item.Available_Qantity,
                }
                for item in medical_stock_data
            ]
            return JsonResponse(data, safe=False)

        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

# ----------------------------------------------------------

@csrf_exempt
@require_http_methods(["POST","OPTIONS","GET"])
def ProductType_Master_lik(request):
    if request.method=='POST':
        try:
            data=json.loads(request.body)
            print('000',data)
            ProductTypeID=data.get('ProductTypeID','')
            ProductTypeName=data.get('ProductTypeName','')
            ProductCategoryId=data.get('ProductCategoryName', None)
            SubProductCategoryId=data.get('SubProductCategoryName', None)
            created_by=data.get('created_by')
            Statusedit=data.get('Statusedit')

            if ProductTypeID:
                if Statusedit:
                    ProductType_instance=ProductType_Master_Details.objects.get(pk=ProductTypeID)
                    ProductType_instance.Status= not ProductType_instance.Status
                    ProductType_instance.save()
                    return JsonResponse ({'success': 'ProductType Updated successfully'})
                else:
                    if not ProductTypeName:
                        return JsonResponse({'warn': 'ProductType Name are mandatory fields'})
                    if ProductType_Master_Details.objects.filter(ProductType_Name=ProductTypeName).exclude(pk=ProductTypeID).exists():
                        return JsonResponse ({'Warn':f"The ProductType are already present in the name of {ProductTypeName}"})
                    if not ProductCategoryId:
                        return({'warn': 'ProductCategory not found'})
                    if not SubProductCategoryId:
                        return JsonResponse({'warn': "SubCategory not found"})
                    try:
                        ProductCategory_instance = Product_Category_Product_Details.objects.get(pk=ProductCategoryId)
                        print("ProductCategory_instance",ProductCategory_instance)
                    
                    except Product_Category_Product_Details.DoesNotExist:
                        return JsonResponse({'warn':  "Productid not found"})
                    
                    try:
                        Sub_ProductCategory_instance = SubCategory_Detailes.objects.get(pk=SubProductCategoryId)
                        print("Sub_ProductCategory_instance",Sub_ProductCategory_instance)
                    except Sub_ProductCategory_instance.DoesNotExist:
                        return JsonResponse({'warn': 'SubProduct Category not found'})
                        
                    ProductType_instance=ProductType_Master_Details.objects.get(pk=ProductTypeID)
                    ProductType_instance.ProductCategory=ProductCategory_instance
                    ProductType_instance.SubProductCategory=Sub_ProductCategory_instance
                    ProductType_instance.ProductType_Name=ProductTypeName
                    ProductType_instance.save()

                    return JsonResponse ({'success': 'ProductType Updated successfully'})

            else:
                if not ProductTypeName:
                    return JsonResponse ({'warn': 'ProductType Name are mandatory fields'})
                if ProductType_Master_Details.objects.filter(ProductType_Name=ProductTypeName).exists():
                    return JsonResponse({'warn': f"The ProductType Name are already present in the name of {ProductTypeName}"})
                if not ProductCategoryId:
                    return({'warn': 'ProductCategory not found'})
                if not SubProductCategoryId:
                    return JsonResponse({'warn': "SubCategory not found"})
                try:
                    ProductCategory_instance = Product_Category_Product_Details.objects.get(pk=ProductCategoryId)
                    print("ProductCategory_instance",ProductCategory_instance)
                
                except Product_Category_Product_Details.DoesNotExist:
                    return JsonResponse({'warn':  "Productid not found"})
                
                try:
                    Sub_ProductCategory_instance = SubCategory_Detailes.objects.get(pk=SubProductCategoryId)
                    print("Sub_ProductCategory_instance",Sub_ProductCategory_instance)
                except Sub_ProductCategory_instance.DoesNotExist:
                    return JsonResponse({'warn': 'SubProduct Category not found'})
                else:
                    ProductType_instance=ProductType_Master_Details(
                    ProductCategory=ProductCategory_instance,
                    SubProductCategory=Sub_ProductCategory_instance,
                    ProductType_Name= ProductTypeName,
                    Create_by=created_by
                    )
                    ProductType_instance.save()
                    
                    return JsonResponse({'success': 'ProductType saved successfully'})
                    

        except Exception as e:
            print(f'An error occurred:{str(e)}')
            return JsonResponse(f'An error occurred:{str(e)}')
    
    elif request.method =='GET':
        try:
            ProductType_instance=ProductType_Master_Details.objects.all()

            ProductType_Array=[]

            for row in ProductType_instance:
                ProductType_dic={
                    'id':row.ProductType_Id,
                    'ProductTypeName':row.ProductType_Name,
                    'ProductCategoryName':row.ProductCategory.ProductCategory_Name if row.ProductCategory else None,
                    'ProductCategory':row.ProductCategory.pk if row.ProductCategory else None,
                    'SubProductCategoryName':row.SubProductCategory.SubCategoryName if row.SubProductCategory else None,
                    'SubProductCategory':row.SubProductCategory.pk if row.SubProductCategory else None,
                    'Status':row.Status
                }
                ProductType_Array.append(ProductType_dic)

            return JsonResponse(ProductType_Array,safe=False)
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse ({'error':'An internal server error occurred'},status=500)




# -------------------------------------------




# bharathi



@csrf_exempt
@require_http_methods(["GET"])
def GenericName_by_Product_SubProduct(request):
    if request.method == 'GET':
        try:
            # Extract query parameters
            ProductCategoryid = request.GET.get('ProductCategory')
            SubProductCategoryid = request.GET.get('SubProductCategory')

  

            # Validate input
            if not ProductCategoryid or not SubProductCategoryid:
                return JsonResponse({'warn': 'ProductCategory AND SubProductCategory not found.'})

            # Query database
            GenericName_Instance = GenericName_Master_Details.objects.filter(
                ProductCategory=ProductCategoryid,
                SubProductCategory=SubProductCategoryid
            )
            

            # Prepare response data
            GenericName_Array = []
            for row in GenericName_Instance:
                Gen_dic = {
                    'id': row.pk,
                    'GenericName': row.GenericName,
                    'ProductCategoryName': row.ProductCategory.ProductCategory_Name if row.ProductCategory else None,
                    'ProductCategory': row.ProductCategory.pk if row.ProductCategory else None,
                    'SubProductCategoryName': row.SubProductCategory.SubCategoryName if row.SubProductCategory else None,
                    'SubProductCategory': row.SubProductCategory.pk if row.SubProductCategory else None,
                    'Status': row.Status,
                }
                GenericName_Array.append(Gen_dic)

            # Return response
            return JsonResponse(GenericName_Array, safe=False)

        except Exception as e:
            # Log the exception for debugging
            print("Error:", str(e))
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)




@csrf_exempt
@require_http_methods(["GET"])
def CompanyName_by_Product_SubProduct(request):
    if request.method == 'GET':
        try:
            ProductCategoryid = request.GET.get('ProductCategory')
            SubProductCategoryid = request.GET.get('SubProductCategory')
            if not ProductCategoryid or not SubProductCategoryid:
                return JsonResponse({'warn': 'ProductCategory AND SubProductCategory not found.'})

            CompanyName_instance = CompanyName_mfg_Master_Details.objects.filter(
                ProductCategory=ProductCategoryid,
                SubProductCategory=SubProductCategoryid
            )
            

            CompanyName_Array = []
            for row in CompanyName_instance:
                Company_dict = {
                    'id':row.pk,
                    'CompanyName': row.CompanyName,
                    'ProductCategoryName': row.ProductCategory.ProductCategory_Name if row.ProductCategory else None,
                    'ProductCategory': row.ProductCategory.pk if row.ProductCategory else None,
                    'SubProductCategoryName': row.SubProductCategory.SubCategoryName if row.SubProductCategory else None,
                    'SubProductCategory': row.SubProductCategory.pk if row.SubProductCategory else None,
                    'Status': row.Status,
                }
                CompanyName_Array.append(Company_dict)
            return JsonResponse(CompanyName_Array, safe=False)


        
        except Exception as e:
            return JsonResponse({'warn': 'An internal server error occurred.'}, status=500)

    
    return JsonResponse({'error': 'Method not allowed'}, status=405)



@csrf_exempt
@require_http_methods(["GET"])
def Product_Group_by_Product_SubProduct(request):
    if request.method == 'GET':
        try:
            ProductCategoryid = request.GET.get('ProductCategory')
            SubProductCategoryid = request.GET.get('SubProductCategory')
            if not ProductCategoryid or not SubProductCategoryid:
                return JsonResponse({'warn': 'ProductCategory and SubProductCategory not found'})
            ProductGroup_instance = Product_Group_Master_Details.objects.filter(
                ProductCategory=ProductCategoryid,
                SubProductCategory=SubProductCategoryid

            )
            print("ProductGroup_instance",ProductGroup_instance)
            ProductGroupName_Array = []
            for row in ProductGroup_instance:
                group_dict = {
                    'id':row.pk,
                    'ProductGroupName':row.ProductGroup_Name,
                    'ProductCategoryName': row.ProductCategory.ProductCategory_Name if row.ProductCategory else None,
                    'ProductCategory': row.ProductCategory.pk if row.ProductCategory else None,
                    'SubProductCategoryName': row.SubProductCategory.SubCategoryName if row.SubProductCategory else None,
                    'SubProductCategory': row.SubProductCategory.pk if row.SubProductCategory else None,
                    'Status': row.Status,
                }
                ProductGroupName_Array.append(group_dict)
            return JsonResponse(ProductGroupName_Array, safe=False)
        except Exception as e:
            return JsonResponse({'warn':'An internal server error occurred'}, status=500)
            
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
@require_http_methods(["GET"])
def PackType_by_Product_SubProduct(request):
    if request.method == 'GET':
        try:
            ProductCategoryid = request.GET.get('ProductCategory')
            SubProductCategoryid = request.GET.get('SubProductCategory')
            if not ProductCategoryid or not SubProductCategoryid:
                return JsonResponse({'warn': 'ProductCategory and SubProductCategory not found'})
            PackType_instance = Pack_Type_Master_Details.objects.filter(
                ProductCategory=ProductCategoryid,
                SubProductCategory=SubProductCategoryid

            )
            print("PackType_instance",PackType_instance)
            PackType_Array = []
            for row in PackType_instance:
                group_dict = {
                    'id':row.pk,
                    'PackTypeName':row.PackType_Name,
                    'ProductCategoryName': row.ProductCategory.ProductCategory_Name if row.ProductCategory else None,
                    'ProductCategory': row.ProductCategory.pk if row.ProductCategory else None,
                    'SubProductCategoryName': row.SubProductCategory.SubCategoryName if row.SubProductCategory else None,
                    'SubProductCategory': row.SubProductCategory.pk if row.SubProductCategory else None,
                    'Status': row.Status,
                }
                PackType_Array.append(group_dict)
            return JsonResponse(PackType_Array, safe=False)
        except Exception as e:
            return JsonResponse({'warn':'An internal server error occurred'}, status=500)
            
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)





@csrf_exempt
@require_http_methods(["GET"])
def ProductType_by_Product_SubProduct(request):
    if request.method == 'GET':
        try:
            ProductCategoryid = request.GET.get('ProductCategory')
            SubProductCategoryid = request.GET.get('SubProductCategory')
            if not ProductCategoryid or not SubProductCategoryid:
                return JsonResponse({'warn': 'ProductCategory and SubProductCategory not found'})
            ProductType_instance = ProductType_Master_Details.objects.filter(
                ProductCategory=ProductCategoryid,
                SubProductCategory=SubProductCategoryid

            )
            print("ProductType_instance",ProductType_instance)
            ProductType_Array = []
            for row in ProductType_instance:
                group_dict = {
                    'id':row.pk,
                    'ProductTypeName':row.ProductType_Name,
                    'ProductCategoryName': row.ProductCategory.ProductCategory_Name if row.ProductCategory else None,
                    'ProductCategory': row.ProductCategory.pk if row.ProductCategory else None,
                    'SubProductCategoryName': row.SubProductCategory.SubCategoryName if row.SubProductCategory else None,
                    'SubProductCategory': row.SubProductCategory.pk if row.SubProductCategory else None,
                    'Status': row.Status,
                }
                ProductType_Array.append(group_dict)
            return JsonResponse(ProductType_Array, safe=False)
        except Exception as e:
            return JsonResponse({'warn':'An internal server error occurred'}, status=500)
            
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)







