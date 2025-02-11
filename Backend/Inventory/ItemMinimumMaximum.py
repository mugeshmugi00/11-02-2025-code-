import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import  Q
from .models import (
    Product_Master_All_Category_Details,
    Location_Items_Minimum_Maximum_Detailes    
)
from Masters.models import (
    Location_Detials,
    NurseStationMaster,    
    Inventory_Location_Master_Detials

)
from django.db.models import Func




# @csrf_exempt
# @require_http_methods(["GET"])
# def Product_Get_For_MinimumMaximum(request):
#     if request.method == 'GET':
#             try:
#                 ProductCategory = request.GET.get('ProductCategory')
#                 SubCategory = request.GET.get('SubCategory','')
#                 ItemCode = request.GET.get('ItemCode','')
#                 ItemName = request.GET.get('ItemName','')
#                 GenericName = request.GET.get('GenericName','')
#                 CompanyName = request.GET.get('CompanyName','')
#                 HSNCode = request.GET.get('HSNCode','')
#                 Singledata = bool(request.GET.get('Singledata',False))
#                 ForFilter = bool(request.GET.get('ForFilter',False))
#                 filter_conditions = Q()
                
#                 if ProductCategory:
#                     filter_conditions &= Q(ProductCategory__pk =ProductCategory)
#                 if SubCategory:
#                     filter_conditions &= Q(SubCategory__pk =SubCategory)
#                 if ItemCode:
#                     filter_conditions &= Q(pk__icontains=ItemCode)
#                 if ItemName:
#                     filter_conditions &= Q(ItemName__icontains=ItemName)
#                 if GenericName:
#                     filter_conditions &= Q(GenericName__pk=GenericName)
#                 if CompanyName:
#                     filter_conditions &= Q(CompanyName__pk=CompanyName)
#                 if HSNCode:
#                     filter_conditions &= Q(HSNCode__icontains=HSNCode)

                
#                 if ForFilter :
#                     pass
#                 elif ItemCode and Singledata:
#                     pass
            
#                 else:
#                     Product_Instance = Product_Master_All_Category_Details.objects.filter(filter_conditions,Status=True)
#                     product_instance_data =[]
#                     index =1
#                     for ins in Product_Instance:
#                         ins_data={
#                             "id":index,
#                             "Item_Code":ins.pk,
#                             "Item_Name":ins.ItemName,
#                             "Product_Category_pk":ins.ProductCategory.pk if ins.ProductCategory else '',
#                             "Product_Category":ins.ProductCategory.ProductCategory_Name if ins.ProductCategory else '',
#                             "Sub_Category_pk":ins.SubCategory.pk if ins.SubCategory else '',
#                             "Sub_Category":ins.SubCategory.SubCategoryName if ins.SubCategory else '',
#                             "Generic_Name_pk":ins.GenericName.pk if ins.GenericName else '',
#                             "Generic_Name":ins.GenericName.GenericName if ins.GenericName else '',
#                             "Manufacturer_pk":ins.CompanyName.pk if ins.CompanyName else '',
#                             "Manufacturer_Name":ins.CompanyName.CompanyName if ins.CompanyName else '',
#                             "HSN_Code":ins.HSNCode,
#                             "Product_Type_pk":ins.ProductType.pk if ins.ProductType else '',
#                             "Product_Type":ins.ProductType.ProductType_Name if ins.ProductType else '',
#                             "Product_Group_pk":ins.ProductGroup.pk if ins.ProductGroup else '',
#                             "Product_Group":ins.ProductGroup.ProductGroup_Name if ins.ProductGroup else '',
#                             "Strength":ins.Strength,
#                             "Strength_Type":ins.StrengthType,
#                             "Volume":ins.Volume,
#                             "Volume_Type_pk":ins.VolumeType.pk if ins.VolumeType else '',
#                             "Volume_Type":f"{ins.VolumeType.Unit_Name} ({ins.VolumeType.Unit_Symbol})" if ins.VolumeType else '',
#                             "Pack_Type_pk":ins.PackType.pk if ins.PackType else '',
#                             "Pack_Type":ins.PackType.PackType_Name if ins.PackType else '',
#                             "Pack_Quantity":ins.PackQty,
#                             "Minimum_Quantity":ins.MinimumQty,
#                             "Maximum_Quantity":ins.MaximumQty,
#                             "Re_order_Level":ins.ReorderLevel,
                            
#                         }
#                         product_instance_data.append(ins_data)
#                         index += 1
#                     return JsonResponse(product_instance_data, safe=False)
                    
#             except Exception as e:
#                 print(f"An error occurred: {str(e)}")
#                 return JsonResponse({'error': 'An internal server error occurred'}, status=500)



@csrf_exempt
@require_http_methods(["GET"])
def Product_Get_For_MinimumMaximum(request):
    if request.method == 'GET':
            try:
                ProductCategory = request.GET.get('ProductCategory')
                SubCategory = request.GET.get('SubCategory','')
                ItemCode = request.GET.get('ItemCode','')
                ItemName = request.GET.get('ItemName','')

               
                filter_conditions = Q()
                
                if ProductCategory:
                    filter_conditions &= Q(ProductCategory__pk =ProductCategory)
                if SubCategory:
                    filter_conditions &= Q(SubCategory__pk =SubCategory)
                if ItemCode:
                    filter_conditions &= Q(pk__icontains=ItemCode)
                if ItemName:
                    filter_conditions &= Q(ItemName__icontains=ItemName)            
                else:
                    Product_Instance = Product_Master_All_Category_Details.objects.filter(filter_conditions,Status=True)
                    product_instance_data =[]
                    index =1
                    for ins in Product_Instance:
                        ins_data={
                            "id":index,
                            "Item_Code":ins.pk,
                            "Item_Name":ins.ItemName,
                            "Product_Category_pk":ins.ProductCategory.pk if ins.ProductCategory else '',
                            "Product_Category":ins.ProductCategory.ProductCategory_Name if ins.ProductCategory else '',
                            "Sub_Category_pk":ins.SubCategory.pk if ins.SubCategory else '',
                            "Sub_Category":ins.SubCategory.SubCategoryName if ins.SubCategory else '',
                            "Minimum_Quantity":ins.MinimumQty,
                            "Maximum_Quantity":ins.MaximumQty,
                            "Re_order_Level":ins.ReorderLevel,
                            
                        }
                        product_instance_data.append(ins_data)
                        index += 1
                    return JsonResponse(product_instance_data, safe=False)
                    
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                return JsonResponse({'error': 'An internal server error occurred'}, status=500)






@csrf_exempt
@require_http_methods(["GET"])
def Single_Item_All_Location_Minimum_Maximum_Qty(request):
    if request.method == 'GET':
        try:
            ItemCode = request.GET.get('ItemCode')

            print('ItemCode:', ItemCode)

            Location_Detials_ins = Location_Detials.objects.all()

            Main_Dec = {}

            for row in Location_Detials_ins:
                Main_Dec[row.Location_Name] = {
                    'StoreLocation': {},
                    'NurseStation': {}
                }

                store_locations = Inventory_Location_Master_Detials.objects.filter(Status=True, Location_Name=row.pk)
                for row2 in store_locations:
                    print('row2.Store_Name:', row2.Store_Name)
                    
                    Main_Dec[row.Location_Name]['StoreLocation'][row2.Store_Name] = {}

                    Item1 = Location_Items_Minimum_Maximum_Detailes.objects.filter(Product_Detailes=ItemCode, Store_location=row2, Status=True).first()
                    
                    if Item1:
                        Item1_dec = {
                            'id': Item1.pk,
                            'MinimumQuantity': Item1.MinimumQty,
                            'MaximumQuantity': Item1.MaximumQty,
                            'ReorderLevel': Item1.ReorderLevel,
                        }
                        Main_Dec[row.Location_Name]['StoreLocation'][row2.Store_Name] = Item1_dec
                    else:
                        Main_Dec[row.Location_Name]['StoreLocation'][row2.Store_Name] = {}

            
                ward_locations = NurseStationMaster.objects.filter(Status=True, Location_Name=row.pk)
                for row3 in ward_locations:
                    print('row3.Ward_Name:', row3.NurseStationName)

                    Main_Dec[row.Location_Name]['NurseStation'][row3.NurseStationName] = {}

                    Item2 = Location_Items_Minimum_Maximum_Detailes.objects.filter(Product_Detailes=ItemCode, NurseStation_location=row3, Status=True).first()
                    
                    if Item2:
                        Item2_dec = {
                            'id': Item2.pk,
                            'MinimumQuantity': Item2.MinimumQty,
                            'MaximumQuantity': Item2.MaximumQty,
                            'ReorderLevel': Item2.ReorderLevel,
                        }
                        Main_Dec[row.Location_Name]['NurseStation'][row3.NurseStationName] = Item2_dec
                    else:
                        Main_Dec[row.Location_Name]['NurseStation'][row3.NurseStationName] = {}

            print('Main_Dec:', Main_Dec)
            return JsonResponse(Main_Dec, safe=False)
        
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)



@csrf_exempt
@require_http_methods(["POST","OPTIONS","GET"])
def Post_Change_Minimum_Maximum_Qty(request):
    if request.method == 'POST':
        try:
            data=json.loads(request.body)

            print('data-----?',data)

            if data:
                column=data.get('column')
                findId=data.get('id')
                MinimumQuantity=data.get('MinimumQuantity')
                MaximumQuantity=data.get('MaximumQuantity')
                ReorderLevel=data.get('ReorderLevel')

                if findId:
                    Location_Items_Minimum_Maximum_Ins=Location_Items_Minimum_Maximum_Detailes.objects.get(pk=findId)

                    if column == 'MinimumQuantity' and MinimumQuantity:
                        Location_Items_Minimum_Maximum_Ins.MinimumQty = MinimumQuantity
                    elif column == 'MaximumQuantity' and MaximumQuantity:
                        Location_Items_Minimum_Maximum_Ins.MaximumQty= MaximumQuantity
                    elif column == 'ReorderLevel' and ReorderLevel:
                        Location_Items_Minimum_Maximum_Ins.ReorderLevel=ReorderLevel

                    Location_Items_Minimum_Maximum_Ins.save()

                return JsonResponse ({'success': 'Quantity Changed successfully'}, status=200)  
        except Exception as e:
            print(f'An error occurred:{str(e)}')
            return JsonResponse({'error':'An internal server error occurred'},status=500)