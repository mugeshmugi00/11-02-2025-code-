from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import *
import json
from datetime import datetime, date
import traceback
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist



@csrf_exempt
@require_http_methods(['POST'])
def Asset_Reg_post(request):
    try:
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'})
        
        category_id = int(data.pop('category', 0)) if data.get('category') else None
        subcategory_ids = [int(id) for id in data.pop('asset_subcategory', []) if id]
        supplier_ids = [int(id) for id in data.pop('supplier', []) if id]

        asset = AssetReg_Data(**data)

        if category_id:
            asset.category = get_object_or_404(AssetCategory, id=category_id)

        asset.save()

        asset.asset_subcategory.set(AssetSubCategory.objects.filter(id__in=subcategory_ids))
        asset.supplier.set(Supplier.objects.filter(id__in=supplier_ids))

        return JsonResponse({'id': asset.id, 'message': 'Asset created successfully'})
    
    except Exception as e:
        return JsonResponse({'error': str(e)})

@csrf_exempt
@require_http_methods(['GET'])
def Asset_Reg_Get(request):   
    assets = AssetReg_Data.objects.all().prefetch_related(
        'asset_subcategory', 
        'supplier'
    ).select_related('category')
    
    data = []
    for asset in assets:
        asset_data = {
            'id': asset.id,
            'Asset_id': asset.id,  
            'Asset_name': asset.name,  
            'name': asset.name,
            'category': asset.category.id if asset.category else None,
            'category_name': asset.category.name if asset.category else None, 
            'asset_subcategory': list(asset.asset_subcategory.values_list('id', flat=True)),
            'subcategory_name': [sub.name for sub in asset.asset_subcategory.all()], 
            'supplier': list(asset.supplier.values_list('id', flat=True)),
            'supplier_name': ', '.join([sup.name for sup in asset.supplier.all()]), 
            'Company_Brand': asset.Company_Brand,
            'current_location': asset.current_location,
            'room_no': asset.room_no,
            'condition': asset.condition,
            'status': asset.status,
            'purchase_date': asset.purchase_date.strftime('%Y-%m-%d') if asset.purchase_date else None,
            'purchase_price': str(asset.purchase_price) if asset.purchase_price else None,
            'market_value': str(asset.market_value) if asset.market_value else None,
            'total_working_life': asset.total_working_life,
            'expected_working_life': asset.expected_working_life,
            'valuation_method': asset.valuation_method,
            'is_new_asset': asset.is_new_asset,
            'depreciation_method': asset.depreciation_method,
            'depreciation_rate': str(asset.depreciation_rate) if asset.depreciation_rate else None,
            'salvage_value': str(asset.salvage_value) if asset.salvage_value else None,
            'appreciation_rate': str(asset.appreciation_rate) if asset.appreciation_rate else None,
            # Add calculated fields
            'life_completed': calculate_life_completed(asset.purchase_date) if asset.purchase_date else None,
            'life_remain': calculate_life_remaining(
                asset.purchase_date, 
                asset.total_working_life
            ) if asset.purchase_date and asset.total_working_life else None,
            'current_value': calculate_current_value(asset),
        }
        data.append(asset_data)
    return JsonResponse(data, safe=False)

def calculate_life_completed(purchase_date):
    if not purchase_date:
        return None
    today = datetime.now().date()
    days = (today - purchase_date).days
    return round(days / 365, 2)

def calculate_life_remaining(purchase_date, total_life):
    if not purchase_date or not total_life:
        return None
    life_completed = calculate_life_completed(purchase_date)
    return max(0, round(total_life - life_completed, 2))

def calculate_current_value(asset):
    if not asset.purchase_price:
        return None
        
    if asset.valuation_method == 'DEPRECIATION':
        life_completed = calculate_life_completed(asset.purchase_date)
        if not life_completed or not asset.depreciation_rate:
            return asset.purchase_price
            
        if asset.depreciation_method == 'STRAIGHT_LINE':
            depreciation = (float(asset.purchase_price) - float(asset.salvage_value or 0)) * (life_completed / float(asset.total_working_life))
            return max(float(asset.salvage_value or 0), float(asset.purchase_price) - depreciation)
            
        elif asset.depreciation_method == 'DECLINING_BALANCE':
            current_value = float(asset.purchase_price)
            rate = float(asset.depreciation_rate) / 100
            for _ in range(int(life_completed)):
                current_value = current_value * (1 - rate)
            return max(float(asset.salvage_value or 0), current_value)
            
    elif asset.valuation_method == 'APPRECIATION':
        life_completed = calculate_life_completed(asset.purchase_date)
        if not life_completed or not asset.appreciation_rate:
            return asset.purchase_price
            
        rate = float(asset.appreciation_rate) / 100
        return float(asset.purchase_price) * (1 + rate) ** life_completed
        
    return float(asset.purchase_price)


@csrf_exempt
@require_http_methods(['PUT'])
def Asset_Reg_put(request,asset_id):
    try:
        data = json.loads(request.body)
        # asset_id = data.get('id')
        asset = AssetReg_Data.objects.get(id=asset_id)

        
        category_id = data.pop('category', None)
        subcategory_ids = data.pop('asset_subcategory', [])
        supplier_ids = data.pop('supplier', [])
        
        if not isinstance(subcategory_ids, list):
            subcategory_ids = [subcategory_ids] if subcategory_ids else []
        if not isinstance(supplier_ids, list):
            supplier_ids = [supplier_ids] if supplier_ids else []
        
        for field, value in data.items():
            setattr(asset, field, value)
        
        if category_id:
            asset.category = AssetCategory.objects.get(id=category_id)
        else:
            asset.category = None
        
        asset.save()
        
        asset.asset_subcategory.set(AssetSubCategory.objects.filter(id__in=subcategory_ids))
        asset.supplier.set(Supplier.objects.filter(id__in=supplier_ids))
        
        return JsonResponse({'message': 'Asset updated successfully'})
    
    except AssetReg_Data.DoesNotExist:
        return JsonResponse({'error': 'Asset not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    

# --------------------------------------------AssetList---------------------------------------------------------


# @csrf_exempt
# @require_http_methods(['POST'])
# def assetList_POST(request):
#     try:
#         data = json.loads(request.body.decode('utf-8'))
#         asset = AssetList.objects.create(
#             name=data.get('name'),
#             category_id=data.get('category_id'),
#             subcategory_id=data.get('subcategory_id'),
#             supplier=data.get('supplier'),
#             status=data.get('status'),
#             condition=data.get('condition'),
#             valuation_method=data.get('valuation_method')
#         )
#         return JsonResponse({'message': 'Asset created successfully', 'id': asset.id}, status=201)
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_http_methods(['GET'])
def assetList_Get(request):
    try:
        print("Query Parameters:", request.GET)

        # Extract query parameters safely
        name = request.GET.get('name', '').strip()
        category_id = request.GET.get('category_id', '').strip()
        subcategory_id = request.GET.get('subcategory_id', '').strip()
        supplier = request.GET.get('supplier', '').strip()
        status = request.GET.get('status', '').strip()
        condition = request.GET.get('condition', '').strip()
        valuation_method = request.GET.get('valuation_method', '').strip()

        # Query the database
        assets = AssetReg_Data.objects.all()

        # Apply filters dynamically
        if category_id.isdigit():  
            assets = assets.filter(category_id=int(category_id))

        if subcategory_id.isdigit():
            assets = assets.filter(asset_subcategory__id=int(subcategory_id))

        if supplier:
            assets = assets.filter(supplier__name__icontains=supplier)  

        if name:
            assets = assets.filter(name__icontains=name)

        if status:
            assets = assets.filter(status=status)

        if condition:
            assets = assets.filter(condition=condition)

        if valuation_method:
            assets = assets.filter(valuation_method=valuation_method)

        asset_data = []
        for asset in assets:
            asset_data.append({
                'id': asset.id,
                'name': asset.name,
                'category': {
                    'id': asset.category.id if asset.category else None,
                    'name': asset.category.name if asset.category else None
                },
                'subcategory': [{
                    'id': sub.id,
                    'name': sub.name
                } for sub in asset.asset_subcategory.all()],
                'supplier': list(asset.supplier.values_list('name', flat=True)),
                'status': asset.status,
                'condition': asset.condition,
                'valuation_method': asset.valuation_method,
            })

        return JsonResponse(asset_data, safe=False)

    except Exception as e:
        print("Error:", str(e))  
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(['PUT'])
def assetList_PUT(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        asset_id = data.get('id')

        if not asset_id:
            return JsonResponse({'error': 'Asset ID is required for updating'}, status=400)

        asset = AssetList.objects.filter(id=asset_id).first()
        if not asset:
            return JsonResponse({'error': 'Asset not found'}, status=404)

        asset.name = data.get('name', asset.name)
        asset.category_id = data.get('category_id', asset.category_id)
        asset.subcategory_id = data.get('subcategory_id', asset.subcategory_id)
        asset.supplier = data.get('supplier', asset.supplier)
        asset.status = data.get('status', asset.status)
        asset.condition = data.get('condition', asset.condition)
        asset.valuation_method = data.get('valuation_method', asset.valuation_method)
        asset.save()

        return JsonResponse({'message': 'Asset updated successfully', 'id': asset.id}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
