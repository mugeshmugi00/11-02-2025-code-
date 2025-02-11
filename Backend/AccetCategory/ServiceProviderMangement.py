from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json
import traceback
   
    
@csrf_exempt  
@require_http_methods(['GET'])
def ServiceProviderManagement_GET(request):
    try:
        providers = Asset_ServiceProviderManagement.objects.all()
        provider_list = []
        
        for provider in providers:
            try:
                # Get all categories for this provider
                categories_data = []
                for category in provider.asset_categories.all():
                    categories_data.append({
                        'id': category.id,
                        'name': category.name
                    })

                # Get subcategories data
                subcategories_data = []
                for subcat in provider.subcategories.all():
                    subcategories_data.append({
                        'id': subcat.id,
                        'name': subcat.name
                    })

                provider_data = {
                    'id': provider.id,
                    'name': provider.name,
                    'contact_info': provider.contact_info,
                    'email': provider.email,
                    'asset_categories': categories_data, 
                    'subcategories': subcategories_data,
                    'status': provider.status,
                    'cost_effective': provider.cost_effective,
                    'service_quality': provider.service_quality,
                    'hourly_rate': str(provider.hourly_rate) if provider.hourly_rate else "0.00",
                    'average_response_time': provider.average_response_time,
                    'years_of_experience': provider.years_of_experience,
                    'ranking': provider.ranking,
                    'rating': str(provider.rating) if provider.rating else "0.00"
                }
                provider_list.append(provider_data)
            except Exception as provider_error:
                print(f"Error processing provider {provider.id}: {str(provider_error)}")
                print(traceback.format_exc())
                continue
        
        return JsonResponse(provider_list, safe=False, status=200)
    
    except Exception as e:
        print("Error in ServiceProviderManagement_GET:")
        print(str(e))
        print(traceback.format_exc())
        return JsonResponse({
            'error': 'Internal server error',
            'details': str(e)
        }, status=500)


@csrf_exempt  
@require_http_methods(['POST'])
def ServiceProviderManagement_POST(request):
    try:
        data = json.loads(request.body)
        
        # Create provider first
        provider = Asset_ServiceProviderManagement.objects.create(
            name=data.get('name', ''),
            contact_info=data.get('contact_info', ''),
            email=data.get('email', ''),
            status=data.get('status', 'active'),
            cost_effective=data.get('cost_effective', True),
            service_quality=data.get('service_quality', 'fair'),
            hourly_rate=data.get('hourly_rate', 0.0),
            average_response_time=data.get('average_response_time', '1 day'),
            years_of_experience=data.get('years_of_experience', 0),
            ranking=data.get('ranking', 0),
            rating=data.get('rating', 0.0)
        )
        
        # Handle categories
        category_ids = data.get('asset_categories', [])
        if category_ids:
            categories = AssetCategory.objects.filter(id__in=category_ids)
            provider.asset_categories.set(categories)
        
        # Handle subcategories
        subcategory_ids = data.get('subcategories', [])
        if subcategory_ids:
            subcategories = AssetSubCategory.objects.filter(id__in=subcategory_ids)
            provider.subcategories.set(subcategories)
        
        return JsonResponse({
            'message': 'Service provider created successfully',
            'id': provider.id
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        print("Error in ServiceProviderManagement_POST:")
        print(str(e))
        print(traceback.format_exc())
        return JsonResponse({'error': str(e)}, status=500)
    
    
@csrf_exempt
@require_http_methods(['PUT'])
def ServiceProviderManagement_PUT(request, ServiceProviderManagement_id):
    try:
        data = json.loads(request.body)
        provider = Asset_ServiceProviderManagement.objects.get(id=ServiceProviderManagement_id)

        # Update basic fields
        fields_to_update = [
            'name', 'contact_info', 'email', 'status', 'cost_effective',
            'service_quality', 'hourly_rate', 'average_response_time',
            'years_of_experience', 'ranking', 'rating'
        ]
        
        for field in fields_to_update:
            if field in data:
                setattr(provider, field, data[field])

        provider.save()

        # Update categories
        if 'asset_categories' in data:
            category_ids = data['asset_categories']
            categories = AssetCategory.objects.filter(id__in=category_ids)
            provider.asset_categories.set(categories)

        # Update subcategories
        if 'subcategories' in data:
            subcategory_ids = data['subcategories']
            subcategories = AssetSubCategory.objects.filter(id__in=subcategory_ids)
            provider.subcategories.set(subcategories)

        return JsonResponse({
            'message': 'Service provider updated successfully',
            'id': provider.id
        }, status=200)

    except Asset_ServiceProviderManagement.DoesNotExist:
        return JsonResponse({'error': 'Service provider not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        print("Error in ServiceProviderManagement_PUT:")
        print(str(e))
        print(traceback.format_exc())
        return JsonResponse({'error': str(e)}, status=500)