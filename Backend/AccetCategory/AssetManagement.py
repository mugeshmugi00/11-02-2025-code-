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
        subcategory_id = data.pop('asset_subcategory', None)
        supplier_ids = [int(id) for id in data.pop('supplier', []) if id]

        # Generate asset_code
        name_part = data.get('name', '')[:2].upper()  
        location_part = ''.join(word[0].upper() for word in data.get('current_location', '').split())
        date_part = data.get('purchase_date', '').replace('-', '')[2:]  

        base_code = f"{name_part}/{location_part}/{date_part}"

        existing_codes = set(AssetReg_Data.objects.values_list('asset_code', flat=True))

        count = 1
        unique_code = base_code

        while unique_code in existing_codes:
            unique_code = f"{base_code}/{str(count).zfill(2)}"
            count += 1

        data.pop("asset_code", None)  # Remove asset_code if present

        asset = AssetReg_Data(**data, asset_code=unique_code)


        if category_id:
            asset.category = get_object_or_404(AssetCategory, id=category_id)
            
        asset = AssetReg_Data(**data)
        if subcategory_id:
            asset.asset_subcategory = get_object_or_404(AssetSubCategory, id=subcategory_id)
        asset.save()

        # asset.save()
        # subcategory_id = data.pop('asset_subcategory', None)
        # if subcategory_id:
        #     asset.asset_subcategory = get_object_or_404(AssetSubCategory, id=subcategory_id)

        # if subcategory_ids:
        #     asset.asset_subcategory.set(AssetSubCategory.objects.filter(id__in=subcategory_ids))

        asset.supplier.set(Supplier.objects.filter(id__in=supplier_ids))

        return JsonResponse({'id': asset.id, 'asset_code': asset.asset_code, 'message': 'Asset created successfully'})
    
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
            'asset_code': asset.asset_code, 
            'name': asset.name,
            'category': asset.category.id if asset.category else None,
            'category_name': asset.category.name if asset.category else None, 
            'asset_subcategory': asset.asset_subcategory.id if asset.asset_subcategory else None,
            'subcategory_name': asset.asset_subcategory.name if asset.asset_subcategory else None,
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


from datetime import datetime


@csrf_exempt
@require_http_methods(['PUT'])
def Asset_Reg_put(request, asset_id):
    try:
        data = json.loads(request.body)

        asset = AssetReg_Data.objects.get(id=asset_id)

        category_id = data.pop('category', None)
        supplier_ids = data.pop('supplier', [])
        
        subcategory_id = data.pop('asset_subcategory', None)
        if subcategory_id:
            asset.asset_subcategory = get_object_or_404(AssetSubCategory, id=subcategory_id)
        else:
            asset.asset_subcategory = None

        # Ensure IDs are lists
        subcategory_id = subcategory_id if isinstance(subcategory_id, list) else [subcategory_id]
        supplier_ids = supplier_ids if isinstance(supplier_ids, list) else [supplier_ids]

        # Parse purchase_date
        purchase_date_str = data.get('purchase_date')
        if purchase_date_str:
            possible_formats = ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S.%fZ"]
            purchase_date = None

            for fmt in possible_formats:
                try:
                    purchase_date = datetime.strptime(purchase_date_str, fmt).date()
                    break
                except ValueError:
                    continue

            if purchase_date is None:
                return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD or ISO 8601 format.'}, status=400)

            asset.purchase_date = purchase_date
            # Remove purchase_date from data to prevent overwriting in the loop below
            if 'purchase_date' in data:
                del data['purchase_date']

        # Update fields dynamically (excluding purchase_date if it was processed)
        for field, value in data.items():
            setattr(asset, field, value)

        # Update category
        asset.category = AssetCategory.objects.get(id=category_id) if category_id else None

        # Only update asset_code if relevant fields changed
        if (
            asset.name != data.get('name', asset.name) or
            asset.current_location != data.get('current_location', asset.current_location) or
            (purchase_date_str and asset.purchase_date != purchase_date)
        ):
            if asset.name and asset.current_location and asset.purchase_date:
                base_code = f"{asset.name[:2].upper()}/{''.join([w[0].upper() for w in asset.current_location.split()])}/{asset.purchase_date.strftime('%y%m%d')}"
                existing_codes = set(AssetReg_Data.objects.values_list('asset_code', flat=True))

                count = 1
                unique_code = base_code

                while unique_code in existing_codes:
                    unique_code = f"{base_code}/{str(count).zfill(2)}"
                    count += 1

                asset.asset_code = unique_code

        asset.save()

        # Update Many-to-Many relationships
        asset.asset_subcategory.set(AssetSubCategory.objects.filter(id__in=subcategory_id))
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
                'asset_code': asset.asset_code, 

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
def assetList_PUT(request, asset_id):  
    try:
        data = json.loads(request.body.decode('utf-8'))

        try:
            asset = AssetReg_Data.objects.get(id=asset_id)  
        except AssetReg_Data.DoesNotExist:
            return JsonResponse({'error': 'Asset not found'}, status=404)

        if 'name' in data:
            asset.name = data['name']
        if 'asset_code' in data:
            asset.asset_code = data['asset_code']
        if 'category_id' in data:
            asset.category_id = data['category_id']
        if 'subcategory_id' in data:
            asset.asset_subcategory.clear()
            if data['subcategory_id']:
                asset.asset_subcategory.add(data['subcategory_id'])
        if 'supplier' in data:
            asset.supplier.clear()
            if isinstance(data['supplier'], list):
                for supplier_name in data['supplier']:
                    supplier, _ = Supplier.objects.get_or_create(name=supplier_name)
                    asset.supplier.add(supplier)
        if 'status' in data:
            asset.status = data['status']
        if 'condition' in data:
            asset.condition = data['condition']
        if 'valuation_method' in data:
            asset.valuation_method = data['valuation_method']

        asset.save()

        return JsonResponse({
            'message': 'Asset updated successfully',
            'asset': {
                'id': asset.id,
                'name': asset.name,
                'asset_code': asset.asset_code,
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
            }
        })
    except Exception as e:
        print(f"Error updating asset: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
