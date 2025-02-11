


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import *
from django.db.models import Sum, Q
from .serializers import *
import pandas as pd

@csrf_exempt  
@require_http_methods(["POST","OPTIONS","GET"])
def Title_Master_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
           
            # Extract and validate data
            TitleId = data.get('TitleId')
            Title = data.get('Title')
            Statusedit = data.get('statusEdit',False)
            created_by = data.get('created_by','')
     
           
           
            if TitleId:
                if Statusedit:
                   Title_instance = Title_Detials.objects.get(Title_Id=TitleId)
                   Title_instance.Status= not Title_instance.Status
                   Title_instance.save()
                else:  
                    if Title_Detials.objects.filter(Title_Name=Title).exists():
                       return JsonResponse({'warn': f"The Title already present in the name of {Title} "})
                    else:
               
                        Title_instance = Title_Detials.objects.get(Title_Id=TitleId)
                        Title_instance.Title_Name=Title
                        Title_instance.save()
 
                return JsonResponse({'success': 'Title Updated successfully'})
            else:
                if Title_Detials.objects.filter(Title_Name=Title).exists():
                    return JsonResponse({'warn': f"The Title_Name  are already present in the name of {Title} "})
                else:
                    Religion_instance = Title_Detials(
                        Title_Name=Title,
                        created_by=created_by
                    )
                Religion_instance.save()
                return JsonResponse({'success': 'Religion added successfully'})
       
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
       
    elif request.method == 'GET':
        try:
            # Fetch all records from the LocationName model
            Titles = Title_Detials.objects.all()
           
            # Construct a list of dictionaries containing location data
            Titles_Master_data = []
            for Title in Titles:
                Title_dict = {
                    'id': Title.Title_Id,
                    'Title': Title.Title_Name,
                    'status': 'Active' if Title.Status else 'Inactive',
                    'created_by': Title.created_by,
                   
                }
                Titles_Master_data.append(Title_dict)
 
            return JsonResponse(Titles_Master_data, safe=False)
 
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'})
 
 
 
# ------------------------flaggg

@csrf_exempt   
@require_http_methods(["POST", "OPTIONS", "GET"])
def Flagg_color_Detials_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Extract and validate data
            FlaggId = data.get('FlaggId', '')
            FlaggName = data.get('FlaggName', '')
            FlaggColor = data.get('FlaggColor', '')
            Statusedit = data.get('Statusedit', False)
            created_by = data.get('created_by', '')
      
            if FlaggId:
                if Statusedit:
                    try:
                        Flagg_instance = Flaggcolor_Detials.objects.get(Flagg_Id=FlaggId)
                        Flagg_instance.Status = not Flagg_instance.Status
                        Flagg_instance.save()
                        return JsonResponse({'success': 'Flagg status updated successfully'})
                    except Flaggcolor_Detials.DoesNotExist:
                        return JsonResponse({'error': f"No entry found with FlaggId '{FlaggId}'."}, status=404)
                
              
                 # Update the existing Flaggcolor_Detials object if FlaggId is provided
                try:
                    Flagg_instance = Flaggcolor_Detials.objects.get(Flagg_Id=FlaggId)
                except Flaggcolor_Detials.DoesNotExist:
                    return JsonResponse({'error': f"No entry found with FlaggId '{FlaggId}'."}, status=404)
                    
                # Check if the new FlaggName exists with a different FlaggColor or vice versa
                if Flaggcolor_Detials.objects.filter(
                    (Q(Flagg_Name=FlaggName) & ~Q(Flagg_Color=FlaggColor)) | 
                    (Q(Flagg_Color=FlaggColor) & ~Q(Flagg_Name=FlaggName))
                ).exclude(Flagg_Id=FlaggId).exists():
                    return JsonResponse({'warn': f"A Flagg Name '{FlaggName}' already exists for a different Flagg Color."})
                   
                # Update the Flagg Name and/or Flagg Color
                Flagg_instance.Flagg_Name = FlaggName
                Flagg_instance.Flagg_Color = FlaggColor
                Flagg_instance.save()

                return JsonResponse({'success': 'Flagg updated successfully'})
            else:
                if Flaggcolor_Detials.objects.filter(Q(Flagg_Name=FlaggName) & ~Q(Flagg_Color=FlaggColor)).exists():
                    return JsonResponse({'warn': f"A Flagg Name '{FlaggName}' already exists for the Flagg Color '{FlaggColor}'."})
                    
                # Create a new entry if it does not exist
                Flagg_instance = Flaggcolor_Detials(
                    Flagg_Name=FlaggName,
                    Flagg_Color=FlaggColor,
                    created_by=created_by
                )
                Flagg_instance.save()
                return JsonResponse({'success': 'Flagg added successfully'})

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
        
    elif request.method == 'GET':
        try:
            # Fetch all records from the LocationName model
            Flagg_instance = Flaggcolor_Detials.objects.all()
            
            # Construct a list of dictionaries containing location data
            Flagg_instance_data = []
            for flagg in Flagg_instance:
                flagg_dict = {
                    'id': flagg.Flagg_Id,
                    'FlaggName': flagg.Flagg_Name,
                    'FlaggColor': flagg.Flagg_Color,
                    'Status': 'Active' if flagg.Status else "Inactive",
                    'created_by': flagg.created_by,
                }
                Flagg_instance_data.append(flagg_dict)

            return JsonResponse(Flagg_instance_data, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)



#--------------------------------------------Location insert,get,update----------------------------------------






@csrf_exempt
@require_http_methods(["POST", "OPTIONS", "GET"])
def Location_Detials_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Extract and validate data
            locationId = data.get('locationId','')
            locationName = data.get('locationName','')
            bedCount = data.get('bedCount','')
            Statusedit = data.get('Statusedit',False)
            created_by = data.get('created_by', '')
      
            if locationId:
                if Statusedit:
                    Location_instance = Location_Detials.objects.get(pk=locationId)
                    Location_instance.Status = not Location_instance.Status
                    Location_instance.save()
                else:
                    if Location_Detials.objects.filter(Location_Name=locationName).exists():
                        return JsonResponse({'error': 'Location with the same name already exists'})
                    else:
                        
                        # Update existing location
                        Location_instance = Location_Detials.objects.get(pk=locationId)
                        Location_instance.Location_Name = locationName
                        Location_instance.Bed_Count = bedCount

                        Location_instance.save()

                return JsonResponse({'success': 'Location_Name Updated successfully'})
            else:
                # Insert new location
                total_bed_count = Location_Detials.objects.filter(Location_Name='ALL').aggregate(total=Sum('Bed_Count'))['total']
                total_bed_count = total_bed_count if total_bed_count else 500

                created_bed_count = Location_Detials.objects.filter(~Q(Location_Name='ALL')).aggregate(total=Sum('Bed_Count'))['total']
                created_bed_count = created_bed_count if created_bed_count else 0

                created_bed_count_sum = created_bed_count + int(bedCount)

                if total_bed_count >= created_bed_count_sum:
                    if Location_Detials.objects.filter(Location_Name=locationName).exists():
                        return JsonResponse({'error': 'Location with the same name already exists'})

                   

                    Location_instance = Location_Detials(
                        Location_Name=locationName,
                        Bed_Count=bedCount,
                        created_by=created_by
                    )
                    Location_instance.save()

                    return JsonResponse({'success': 'Location added successfully'})
                else:
                    return JsonResponse({'warn': f'Your Registered Bed Count is {total_bed_count}, so please stay below or equal to that'})

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
        
    elif request.method == 'GET':
        try:
            # Fetch all records from the Location_Detials model
            locations = Location_Detials.objects.all()
            
            # Construct a list of dictionaries containing location data
            location_data = [
                {
                    'id': location.Location_Id,
                    'locationName': location.Location_Name,
                    'bedCount': location.Bed_Count,
                    'Status': 'Active' if location.Status else 'Inactive',
                    'created_by': location.created_by
                } for location in locations
            ]

            return JsonResponse(location_data, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)









#--------------------------------------------Department insert,get,update----------------------------------------




@csrf_exempt   
@require_http_methods(["POST","OPTIONS","GET"])
def Department_Detials_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Extract and validate data
            DepartmentId = data.get('DepartmentId','')
            DepartmentName = data.get('DepartmentName','')
            Statusedit = data.get('Statusedit',False)
            created_by = data.get('created_by','')
      
            
           
            if DepartmentId:
                if Statusedit:
                    Department_instance = Department_Detials.objects.get(pk=DepartmentId)
                    # Create a new LocationName instance
                    Department_instance.Status= not Department_instance.Status
                    Department_instance.save()
                else:
                    if Department_Detials.objects.filter(Department_Name=DepartmentName).exists():
                        return JsonResponse({'warn': f"The DepartmentName  are already present in the name of {DepartmentName} "})
                    else:
                        Department_instance = Department_Detials.objects.get(pk=DepartmentId)
                        # Create a new LocationName instance
                        Department_instance.Department_Name=DepartmentName
                        Department_instance.save()

                return JsonResponse({'success': 'DepartmentName Updated successfully'})
            else:
                if Department_Detials.objects.filter(Department_Name=DepartmentName).exists():
                    return JsonResponse({'warn': f"The DepartmentName  are already present in the name of {DepartmentName} "})
                else:
                    Department_instance = Department_Detials(
                        Department_Name=DepartmentName,
                        created_by=created_by
                    )
                Department_instance.save()
                return JsonResponse({'success': 'Department added successfully'})
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
        
    elif request.method == 'GET':
        try:
            # Fetch all records from the LocationName model
            Department_Master = Department_Detials.objects.all()
            
            # Construct a list of dictionaries containing location data
            Department_Master_data = []
            for Department in Department_Master:
                Department_dict = {
                    'id': Department.Department_Id,
                    'DepartmentName': Department.Department_Name,
                    'Status': 'Active' if Department.Status else 'Inactive',
                    'created_by': Department.created_by,
                    
                }
                Department_Master_data.append(Department_dict)

            return JsonResponse(Department_Master_data, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)




#-------------------------------------------- Designation insert,get,update----------------------------------------



@csrf_exempt   
@require_http_methods(["POST","OPTIONS","GET"])
def Designation_Detials_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            # Extract and validate data
            DesignationId = data.get('DesignationId','')
            # Department = data.get('Department','')
            Designation = data.get('Designation','')
            Statusedit = data.get('Statusedit',False)
            created_by = data.get('created_by','')
            # if Department:
            #     Department_instance = Department_Detials.objects.get(Department_Id=Department)
           
            if DesignationId:
                if Statusedit:
                    Designation_instance = Designation_Detials.objects.get(pk=DesignationId)
                    Designation_instance.Status= not Designation_instance.Status
                    Designation_instance.save()
                else:
                    if Designation_Detials.objects.filter(Designation_Name=Designation).exists():
                        return JsonResponse({'warn': f"The Designation {Designation} already exists."})
                    else:
                        Designation_instance = Designation_Detials.objects.get(pk=DesignationId)
                        # Create a new LocationName instance
                        
                        Designation_instance.Designation_Name=Designation
                        # Designation_instance.Department_Name=Department_instance
                        Designation_instance.save()

                return JsonResponse({'success': ' Updated successfully'})
            else:
                if Designation_Detials.objects.filter(Designation_Name=Designation).exists():
                    return JsonResponse({'warn': f"The  Designation {Designation} already exists."})
                else:
                    Designation_instance = Designation_Detials(
                        
                        Designation_Name=Designation,
                        # Department_Name=Department_instance,
                        created_by=created_by
                    )
                Designation_instance.save()
                return JsonResponse({'success': ' added successfully'})
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
        
    elif request.method == 'GET':
        try:
            # Fetch all records from the LocationName model
            Designations = Designation_Detials.objects.all()
            
            # Construct a list of dictionaries containing location data
            Designation_Master_data = []
            for Designation in Designations:
                Designation_dict = {
                    'id': Designation.Designation_Id,
                    'Designation': Designation.Designation_Name,
                    # 'DepartmentId': Designation.Department_Name.Department_Id,
                    # 'Department': Designation.Department_Name.Department_Name,
                    'Status':'Active' if Designation.Status else 'Inactive' ,
                    'created_by': Designation.created_by,
                    
                }
                Designation_Master_data.append(Designation_dict)

            return JsonResponse(Designation_Master_data, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)


#--------------------------------------------Classification-----------------------------------------
@csrf_exempt   
@require_http_methods(["POST","OPTIONS","GET"])
def Classification_Detials_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            # Extract and validate data
            ClassificationId = data.get('ClassificationId','')
            Classification = data.get('Classification','')
            Statusedit = data.get('Statusedit',False)
            created_by = data.get('created_by','')
            # if Department:
            #     Department_instance = Department_Detials.objects.get(Department_Id=Department)
           
            if ClassificationId:
                if Statusedit:
                    Classification_instance = Classification_Detials.objects.get(pk=ClassificationId)
                    Classification_instance.Status= not Classification_instance.Status
                    Classification_instance.save()
                else:
                    if Classification_Detials.objects.filter(Classification_Name=Classification).exists():
                        return JsonResponse({'warn': f"The Classification {Classification} already exists."})
                    else:
                        Classification_instance = Classification_Detials.objects.get(pk=ClassificationId)
                        # Create a new LocationName instance
                        
                        Classification_instance.Classification_Name=Classification
                        # Designation_instance.Department_Name=Department_instance
                        Classification_instance.save()

                return JsonResponse({'success': ' Updated successfully'})
            else:
                if Classification_Detials.objects.filter(Classification_Name=Classification).exists():
                    return JsonResponse({'warn': f"The  Classification {Classification} already exists."})
                else:
                    Classification_instance = Classification_Detials(
                        
                        Classification_Name=Classification,
                        created_by=created_by
                    )
                Classification_instance.save()
                return JsonResponse({'success': ' added successfully'})
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
        
    elif request.method == 'GET':
        try:
            # Fetch all records from the LocationName model
            Classifications = Classification_Detials.objects.all()
            
            # Construct a list of dictionaries containing location data
            Classification_Master_data = []
            for Classification in Classifications:
                Classification_dict = {
                    'id': Classification.Classification_Id,
                    'Classification': Classification.Classification_Name,
                    'Status':'Active' if Classification.Status else 'Inactive' ,
                    'created_by': Classification.created_by,
                    
                }
                Classification_Master_data.append(Classification_dict)

            return JsonResponse(Classification_Master_data, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

#-------------------------------------------- ConsentName insert,get,update----------------------------------------



@csrf_exempt   
@require_http_methods(["POST", "OPTIONS", "GET"])
def ConsentName_Detials_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            
            Department = data.get('Department', '')
            ConsentFormsName = data.get('ConsentFormsName', '')
            Statusedit = data.get('Statusedit', False)
            ConsentId = data.get('ConsentId', None)  # Assuming ConsentId is sent from the client side
            created_by = data.get('created_by', '')

            if Department:
                Department_instance = Department_Detials.objects.get(Department_Id=Department)
            else:
                return JsonResponse({'error': 'Department is required'}, status=400)

            if ConsentId:
                Consent_instance = ConsentName_Detials.objects.get(pk=ConsentId)

                if Statusedit:
                    # Toggle the status of the Consent
                    Consent_instance.Status = not Consent_instance.Status
                    Consent_instance.save()
                    return JsonResponse({'success': 'Status updated successfully'})
                else:
                    if ConsentName_Detials.objects.filter(
                            ConsentName=ConsentFormsName, 
                            DepartmentName=Department_instance
                        ).exclude(pk=ConsentId).exists():
                        return JsonResponse({'warn': f"The ConsentFormsName '{ConsentFormsName}' already exists in this department."})
                    else:
                        # Update the existing consent details
                        Consent_instance.DepartmentName = Department_instance
                        Consent_instance.ConsentName = ConsentFormsName
                        Consent_instance.save()
                        return JsonResponse({'success': 'Consent updated successfully'})
            else:
                if ConsentName_Detials.objects.filter(
                        ConsentName=ConsentFormsName, 
                        DepartmentName=Department_instance
                    ).exists():
                    return JsonResponse({'warn': f"The ConsentFormsName '{ConsentFormsName}' already exists in this department."})
                else:
                    # Create a new Consent
                    Consent_instance = ConsentName_Detials(
                        DepartmentName=Department_instance,
                        ConsentName=ConsentFormsName,
                        created_by=created_by
                    )
                    Consent_instance.save()
                    return JsonResponse({'success': 'Consent added successfully'})
        
        except Department_Detials.DoesNotExist:
            return JsonResponse({'error': 'Department not found'}, status=404)
        except ConsentName_Detials.DoesNotExist:
            return JsonResponse({'error': 'Consent not found'}, status=404)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

    elif request.method == 'GET':
        try:
            # Fetch all records from the ConsentName_Detials model
            ConsentNames = ConsentName_Detials.objects.all()
            
            # Construct a list of dictionaries containing consent data
            Consent_Master_data = []
            for Consent in ConsentNames:
                Consent_dict = {
                    'id': Consent.ConsentName_Id,
                    'DepartmentId': Consent.DepartmentName.Department_Id,
                    'Department': Consent.DepartmentName.Department_Name,
                    'ConsentFormsName': Consent.ConsentName,
                    'Status': 'Active' if Consent.Status else 'Inactive',
                    'created_by': Consent.created_by,
                }
                Consent_Master_data.append(Consent_dict)

            return JsonResponse(Consent_Master_data, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)


#-------------------------------------------- Category insert,get,update----------------------------------------


@csrf_exempt   
@require_http_methods(["POST","OPTIONS","GET"])
def Category_Detials_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
            
            # Extract and validate data
            CategoryId = data.get('CategoryId','')
            CategoryName = data.get('Category','')
            
            Statusedit = data.get('Statusedit',False)
            created_by = data.get('created_by','')
            
            
           
            if CategoryId:
                if Statusedit:
                    Category_instance = Category_Detials.objects.get(pk=CategoryId)

                    Category_instance.Status=not Category_instance.Status
                    Category_instance.save()
                else:
                    if Category_Detials.objects.filter(Category_Name=CategoryName).exists():
                        return JsonResponse({'warn': f"The CategoryName {CategoryName} already exists."})
                    else:
                        Category_instance = Category_Detials.objects.get(pk=CategoryId)
                        # Create a new Category instance
                        
                        
                        Category_instance.Category_Name=CategoryName
                        Category_instance.save()

                return JsonResponse({'success': 'Category Updated successfully'})
            else:
                if Category_Detials.objects.filter(Category_Name=CategoryName).exists():
                    return JsonResponse({'warn': f"The CategoryName {CategoryName} already exists."})
                else:
                    Category_instance = Category_Detials(
                        
                        
                        Category_Name=CategoryName,
                        created_by=created_by
                    )
                Category_instance.save()
                return JsonResponse({'success': 'Category added successfully'})
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
        
    elif request.method == 'GET':
        try:
            # Fetch all records from the Category model
            Categories = Category_Detials.objects.all()
            
            # Construct a list of dictionaries containing Category data
            Category_Master_data = []
            for Category in Categories:
                Category_dict = {
                    'id': Category.Category_Id,
                    'CategoryName': Category.Category_Name,
                    'Status':'Active' if Category.Status else 'Inactive',
                    'created_by': Category.created_by,
                    
                }
                Category_Master_data.append(Category_dict)

            return JsonResponse(Category_Master_data, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)






# ---------------------------------Speciality---------------

@csrf_exempt  
@require_http_methods(["POST","OPTIONS","GET"])
def Speciality_Detials_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data)
           
            # Extract and validate data
            SpecialityId = data.get('SpecialityId','')
            SpecialityName = data.get('SpecialityName','')
            Category = data.get('Category','')
            Statusedit = data.get('Statusedit',False)
            created_by = data.get('created_by','')
            if Category:
                Category_instance = Category_Detials.objects.get(pk = Category)
           
            if SpecialityId:
                if Statusedit:
                    Speciality_instance = Speciality_Detials.objects.get(pk=SpecialityId)
 
                    Speciality_instance.Status= not Speciality_instance.Status
                    Speciality_instance.save()
                else:
                    if Speciality_Detials.objects.filter(Speciality_Name=SpecialityName,Category_Name=Category_instance).exists():
                        return JsonResponse({'warn': f"The SpecialityName {SpecialityName} with Category {Category_instance.Category_Name} already exists."})
                    else:
                        Speciality_instance = Speciality_Detials.objects.get(pk=SpecialityId)
                        # Create a new Category instance
                       
                        Speciality_instance.Category_Name=Category_instance
                        Speciality_instance.Speciality_Name=SpecialityName
                        Speciality_instance.save()
 
                return JsonResponse({'success': 'Speciality Updated successfully'})
            else:
                if Speciality_Detials.objects.filter(Speciality_Name=SpecialityName,Category_Name=Category_instance).exists():
                    return JsonResponse({'warn': f"The SpecialityName {SpecialityName} with Category {Category_instance.Category_Name} already exists."})
                else:
                    Speciality_instance = Speciality_Detials(
                       
                        Category_Name=Category_instance,
                        Speciality_Name=SpecialityName,
                        created_by=created_by
                    )
                Speciality_instance.save()
                return JsonResponse({'success': 'Speciality Detials added successfully'})
       
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
       
    elif request.method == 'GET':
        try:
 
            id = request.GET.get('id')
           
 
 
            if id:
                Speciality_Master_data = []
               
                Speciality_ins = Speciality_Detials.objects.get(Speciality_Id=id)
               
                Speciality_dict = {
                        'id': Speciality_ins.Speciality_Id,
                        'Speciality_Id': Speciality_ins.Speciality_Id,
                        'CategoryId': Speciality_ins.Category_Name.Category_Id,
                        'CategoryName': Speciality_ins.Category_Name.Category_Name,
                        'SpecialityName': Speciality_ins.Speciality_Name,
                        'Status': 'Active' if Speciality_ins.Status else 'Inactive',
                        'created_by': Speciality_ins.created_by,
                       
                    }
                Speciality_Master_data.append(Speciality_dict)
 
                return JsonResponse(Speciality_Master_data, safe=False)
 
            # Fetch all records from the Category model
            Specialities = Speciality_Detials.objects.all()
           
 
           
            # Construct a list of dictionaries containing Category data
            Speciality_Master_data = []
            for Speciality in Specialities:
                Speciality_dict = {
                    'id': Speciality.Speciality_Id,
                    'Speciality_Id': Speciality.Speciality_Id,
                    'CategoryId': Speciality.Category_Name.Category_Id,
                    'CategoryName': Speciality.Category_Name.Category_Name,
                    'SpecialityName': Speciality.Speciality_Name,
                    'Status': 'Active' if Speciality.Status else 'Inactive',
                    'created_by': Speciality.created_by,
                   
                }
                Speciality_Master_data.append(Speciality_dict)
 
            return JsonResponse(Speciality_Master_data, safe=False)
 
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
 
 
 
 



@csrf_exempt  
@require_http_methods(["POST", "OPTIONS", "GET"])
def Doctors_Speciality_Detials_link(request):
    if request.method == 'GET':
        try:
            # Fetch the 'Doctor' designation
            Catg_instance = Category_Detials.objects.get(Category_Name='DOCTOR')
           
            # Fetch all specialties associated with the 'Doctor' designation
            Specialities = Speciality_Detials.objects.filter(Category_Name=Catg_instance)
   
            # Construct a list of dictionaries containing the data
            Speciality_Master_data = []
            for Speciality in Specialities:
                Speciality_dict = {
                    'id': Speciality.Speciality_Id,
                    'DesignationId': Speciality.Category_Name.Category_Id,
                    'DesignationName': Speciality.Category_Name.Category_Name,
                    'SpecialityName': Speciality.Speciality_Name,
                    'Status': 'Active' if Speciality.Status else 'Inactive',
                    'created_by': Speciality.created_by,
                }
                Speciality_Master_data.append(Speciality_dict)
 
            return JsonResponse(Speciality_Master_data, safe=False)
 
        except Designation_Detials.DoesNotExist:
            return JsonResponse({'error': 'Doctor designation not found'}, status=404)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)




@csrf_exempt   
@require_http_methods(["POST","OPTIONS","GET"])
def UserControl_Role_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Extract and validate data
            RoleId = data.get('RoleId','')
            Role = data.get('Role','')
            Statusedit = data.get('Statusedit',False)
            created_by = data.get('created_by','')
      
            
           
            if RoleId:
                if Statusedit:
                    Role_instance = Role_Master.objects.get(Role_Id=RoleId)

                    Role_instance.Status= not Role_instance.Status
                    Role_instance.save()
                else:
                    if Role_Master.objects.filter(Role_Name=Role).exists():
                        return JsonResponse({'warn': f"The Role Name  are already present in the name of {Role} "})
                    else:
                        Role_instance = Role_Master.objects.get(Role_Id=RoleId)
                        # Create a new LocationName instance
                        Role_instance.Role_Name=Role
                        Role_instance.save()

                return JsonResponse({'success': 'Role Updated successfully'})
            else:
                if Role_Master.objects.filter(Role_Name=Role).exists():
                     return JsonResponse({'warn': f"The Role Name  are already present in the name of {Role} "})
                else:
                    Role_instance = Role_Master(
                        Role_Name=Role,
                        created_by=created_by
                    )
                Role_instance.save()
                return JsonResponse({'success': 'Role added successfully'})
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
        
    elif request.method == 'GET':
        try:
            # Fetch all records from the LocationName model
            Roles = Role_Master.objects.exclude(created_by='system')
            
            # Construct a list of dictionaries containing location data
            Role_Master_data = []
            for role in Roles:
                Role_dict = {
                    'id': role.Role_Id,
                    'Role': role.Role_Name,
                    'Status': 'Active' if role.Status else "Inactive",
                    'created_by': role.created_by,
                    
                }
                Role_Master_data.append(Role_dict)

            return JsonResponse(Role_Master_data, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)



@csrf_exempt   
@require_http_methods(["POST","OPTIONS","GET"])
def Relegion_Master_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Extract and validate data
            RelegionId = data.get('religionId')
            Relegion = data.get('religion')
            Statusedit = data.get('statusEdit',False)
            created_by = data.get('created_by','')
      
            
           
            if RelegionId:
                if Statusedit:
                   Relegion_instance = Religion_Detials.objects.get(Religion_Id=RelegionId)
                   Relegion_instance.Status= not Relegion_instance.Status
                   Relegion_instance.save()
                else:   
                    if Religion_Detials.objects.filter(Religion_Name=Relegion).exists():
                       return JsonResponse({'warn': f"The Relegion already present in the name of {Relegion} "})
                    else:
                
                        Relegion_instance = Religion_Detials.objects.get(Religion_Id=RelegionId)
                        Relegion_instance.Religion_Name=Relegion
                        Relegion_instance.save()

                return JsonResponse({'success': 'Relegion Updated successfully'})
            else:
                if Religion_Detials.objects.filter(Religion_Name=Relegion).exists():
                    return JsonResponse({'warn': f"The Religion_Name  are already present in the name of {Relegion} "})
                else:
                    Religion_instance = Religion_Detials(
                        Religion_Name=Relegion,
                        created_by=created_by
                    )
                Religion_instance.save()
                return JsonResponse({'success': 'Religion added successfully'})
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
        
    elif request.method == 'GET':
        try:
            # Fetch all records from the LocationName model
            Religions = Religion_Detials.objects.all()
            
            # Construct a list of dictionaries containing location data
            Religions_Master_data = []
            for Religion in Religions:
                Religion_dict = {
                    'id': Religion.Religion_Id,
                    'religion': Religion.Religion_Name,
                    'status': 'Active' if Religion.Status else 'Inactive',
                    'created_by': Religion.created_by,
                    
                }
                Religions_Master_data.append(Religion_dict)

            return JsonResponse(Religions_Master_data, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'})


@csrf_exempt   
@require_http_methods(["POST","OPTIONS","GET"])
def Cast_Master_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Extract and validate data
            CastId = data.get('CastId')
            Cast = data.get('Cast')
            Statusedit = data.get('statusEdit',False)
            created_by = data.get('created_by','')
      
            
           
            if CastId:
                if Statusedit:
                   Cast_instance = Cast_Detials.objects.get(Cast_Id=CastId)
                   Cast_instance.Status= not Cast_instance.Status
                   Cast_instance.save()
                else:   
                    if Cast_Detials.objects.filter(Cast_Name=Cast).exists():
                       return JsonResponse({'warn': f"The Cast already present in the name of {Cast} "})
                    else:
                
                        Cast_instance = Cast_Detials.objects.get(Cast_Id=CastId)
                        Cast_instance.Cast_Name=Cast
                        Cast_instance.save()

                return JsonResponse({'success': 'Cast Updated successfully'})
            else:
                if Cast_Detials.objects.filter(Cast_Name=Cast).exists():
                    return JsonResponse({'warn': f"The Cast_Name  are already present in the name of {Cast} "})
                else:
                    Religion_instance = Cast_Detials(
                        Cast_Name=Cast,
                        created_by=created_by
                    )
                Religion_instance.save()
                return JsonResponse({'success': 'Religion added successfully'})
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
        
    elif request.method == 'GET':
        try:
            # Fetch all records from the LocationName model
            Casts = Cast_Detials.objects.all()
            
            # Construct a list of dictionaries containing location data
            Casts_Master_data = []
            for Cast in Casts:
                Cast_dict = {
                    'id': Cast.Cast_Id,
                    'Cast': Cast.Cast_Name,
                    'status': 'Active' if Cast.Status else 'Inactive',
                    'created_by': Cast.created_by,
                    
                }
                Casts_Master_data.append(Cast_dict)

            return JsonResponse(Casts_Master_data, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'})






@csrf_exempt   
@require_http_methods(["POST","OPTIONS","GET"])
def TriageCategory_Master_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            Triage_Id = data.get('Triage_Id')
            Description = data.get('Description')
            Statusedit = data.get('statusEdit', False)
            
            if Triage_Id:
                Triage_instance = TriageCategory_Detials.objects.get(Triage_Id=Triage_Id)
                
                if Statusedit:
                    Triage_instance.Status = not Triage_instance.Status
                    Triage_instance.save()
                    return JsonResponse({'success': 'Status updated successfully'})
                
                # Update Description only if Description is provided
                if Description:
                    if TriageCategory_Detials.objects.filter(Description=Description).exclude(Triage_Id=Triage_Id).exists():
                        return JsonResponse({'warn': f"The Description '{Description}' already exists."})
                    Triage_instance.Description = Description
                    Triage_instance.save()
                    return JsonResponse({'success': 'Description updated successfully'})
                else:
                    return JsonResponse({'error': 'Description is required for updating'}, status=400)

            else:
                # Handle case where no Triage_Id is provided, assuming it's a new entry
                # Additional logic for new entry if needed here...
                return JsonResponse({'error': 'Triage_Id required'}, status=400)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

    elif request.method == 'GET':
        try:
            TriageCategory = TriageCategory_Detials.objects.all()
            Triage_Master_data = [
                {
                    'id': Triage.Triage_Id,
                    'Description': Triage.Description,
                    'Category': Triage.Category,
                    'Colour': Triage.Colour,
                    'status': 'Active' if Triage.Status else 'Inactive',
                    'created_by': Triage.created_by,
                }
                for Triage in TriageCategory
            ]
            return JsonResponse(Triage_Master_data, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'})



@csrf_exempt   
@require_http_methods(["POST","OPTIONS","GET"])
def BloodGroup_Master_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Extract and validate data
            BloodGroupId = data.get('BloodGroupId')
            BloodGroup = data.get('BloodGroup')
            Statusedit = data.get('statusEdit',False)
            created_by = data.get('created_by','')
      
            
           
            if BloodGroupId:
                if Statusedit:
                   BloodGroup_instance = BloodGroup_Detials.objects.get(BloodGroup_Id=BloodGroupId)
                   BloodGroup_instance.Status= not BloodGroup_instance.Status
                   BloodGroup_instance.save()
                else:   
                    if BloodGroup_Detials.objects.filter(BloodGroup_Name=BloodGroup).exists():
                       return JsonResponse({'warn': f"The BloodGroup already present in the name of {BloodGroup} "})
                    else:
                
                        BloodGroup_instance = BloodGroup_Detials.objects.get(BloodGroup_Id=BloodGroupId)
                        BloodGroup_instance.BloodGroup_Name=BloodGroup
                        BloodGroup_instance.save()

                return JsonResponse({'success': 'BloodGroup Updated successfully'})
            else:
                if BloodGroup_Detials.objects.filter(BloodGroup_Name=BloodGroup).exists():
                    return JsonResponse({'warn': f"The BloodGroup_Name  are already present in the name of {BloodGroup} "})
                else:
                    Religion_instance = BloodGroup_Detials(
                        BloodGroup_Name=BloodGroup,
                        created_by=created_by
                    )
                Religion_instance.save()
                return JsonResponse({'success': 'Religion added successfully'})
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
        
    elif request.method == 'GET':
        try:
            # Fetch all records from the LocationName model
            BloodGroups = BloodGroup_Detials.objects.all()
            
            # Construct a list of dictionaries containing location data
            BloodGroups_Master_data = []
            for BloodGroup in BloodGroups:
                BloodGroup_dict = {
                    'id': BloodGroup.BloodGroup_Id,
                    'BloodGroup': BloodGroup.BloodGroup_Name,
                    'status': 'Active' if BloodGroup.Status else 'Inactive',
                    'created_by': BloodGroup.created_by,
                    
                }
                BloodGroups_Master_data.append(BloodGroup_dict)

            return JsonResponse(BloodGroups_Master_data, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'})


@csrf_exempt
@require_http_methods(["POST", "OPTIONS", "GET"])
def ICDCode_Master_InsetLink(request):
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

            ICDCode_Masterdata_FileUpload.objects.all().delete()

            for row in csv_data:
                for key in row:
                    if pd.isna(row[key]):
                        if isinstance(row[key], str):
                            row[key] = 'None'
                        elif isinstance(row[key], (int, float)):
                            row[key] = None
        
                ICDCode_Masterdata_FileUpload.objects.create(
                    ICDCode=row.get('ICDCode', 'None'),
                    ICDCode_Description=row.get('ICDCode_Description', 'None'),
                    Diagnosis=row.get('Diagnosis', 'None'),
                )

            return JsonResponse({'success': 'File uploaded and data inserted successfully'})

        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

    elif request.method == "GET":
        try:

            Searchbyname=request.GET.get('Searchbyname')
            Searchbyvalue=request.GET.get('Searchbyvalue')

            query = Q()

            if Searchbyname == 'SearchICDCode':
                query &= Q(ICDCode__icontains=Searchbyvalue)
            if Searchbyname == 'SearchDescription':
                query &= Q(ICDCode_Description__icontains=Searchbyvalue)
            if Searchbyname == 'SearchDiagnosis':
                query &= Q(Diagnosis__icontains=Searchbyvalue)

            ICDCode_Masterdata = ICDCode_Masterdata_FileUpload.objects.filter(query)
            
            data = [
                {
                    'id': index + 1, 
                    'ICDCode': item.ICDCode,
                    'ICDCode_Description': item.ICDCode_Description,
                    'Diagnosis': item.Diagnosis,
                    'CreatedAt': item.CreatedAt.strftime('%d-%m-%Y'),
                }
                for index, item in enumerate(ICDCode_Masterdata)
            ]
            return JsonResponse(data, safe=False)

        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)





@csrf_exempt
@require_http_methods(["POST", "OPTIONS", "GET"])
def ICDCode_Master_DoctorGetLink(request):
    if request.method == "GET":
        try:

            SearchICDCode=request.GET.get('SearchICDCode')
            SearchDescription=request.GET.get('SearchDescription')
            SearchDiagnosis=request.GET.get('SearchDiagnosis')


            query = Q()

            if SearchICDCode :
                query &= Q(ICDCode__icontains=SearchICDCode)
            if SearchDescription:
                query &= Q(ICDCode_Description__icontains=SearchDescription)
            if SearchDiagnosis:
                query &= Q(Diagnosis__icontains=SearchDiagnosis)
            
            ICDCode_Masterdata = ICDCode_Masterdata_FileUpload.objects.filter(query)[:20]
           

            data = [
                {
                    'id': index + 1, 
                    'ICDCode': item.ICDCode,
                    'ICDCode_Description': item.ICDCode_Description,
                    'Diagnosis': item.Diagnosis,
                    'CreatedAt': item.CreatedAt.strftime('%d-%m-%Y'),
                }
                for index, item in enumerate(ICDCode_Masterdata)
            ]
            return JsonResponse(data, safe=False)

        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)


@csrf_exempt
@require_http_methods(["POST", "OPTIONS", "GET"])
def GradeName_Master_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("datagradename", data)

            # Extract and validate data
            GradeNameId = data.get('GradeNameId')
            GradeName = data.get('GradeName')
            Roomid = data.get('Roomid', None)
            Statusedit = data.get('statusEdit', False)
            created_by = data.get('created_by', '')

            # If GradeNameId is provided
            if GradeNameId:
                if Statusedit:
                    print("Statusedit", Statusedit)
                    GradeName_instance = GradeName_Detials.objects.get(GradeName_Id=GradeNameId)
                    GradeName_instance.Status = not GradeName_instance.Status
                    GradeName_instance.save()
                    return JsonResponse({'success': 'GradeName status updated successfully'})

                else:
                    if GradeName_Detials.objects.filter(GradeName_Name=GradeName, RoomName=Roomid).exists():
                        return JsonResponse({'warn': f"The GradeName is already present in the room {Roomid} with the name {GradeName}"})
                    else:
                        if Roomid:
                            try:
                                Room_Instance = RoomType_Master_Detials.objects.get(pk=Roomid)
                                print('Room_Instance:', Room_Instance)
                            except RoomType_Master_Detials.DoesNotExist:
                                return JsonResponse({'warn': "Room not found."})

                        GradeName_instance = GradeName_Detials.objects.get(GradeName_Id=GradeNameId)
                        GradeName_instance.GradeName_Name = GradeName
                        GradeName_instance.RoomName = Room_Instance if Room_Instance else None
                        GradeName_instance.save()

                        return JsonResponse({'success': 'GradeName Updated successfully'})

            else:
                # If no GradeNameId is provided, create a new GradeName
                if GradeName_Detials.objects.filter(GradeName_Name=GradeName, RoomName=Roomid).exists():
                    return JsonResponse({'warn': f"The GradeName is already present in the room {Roomid} with the name {GradeName}"})
                else:
                    if Roomid:
                        try:
                            Room_Instance = RoomType_Master_Detials.objects.get(pk=Roomid)
                            print('Room_Instance:', Room_Instance)
                        except RoomType_Master_Detials.DoesNotExist:
                            return JsonResponse({'warn': "Room not found."})

                    GradeName_instance = GradeName_Detials(
                        GradeName_Name=GradeName,
                        RoomName=Room_Instance if Room_Instance else None,
                        created_by=created_by
                    )
                    GradeName_instance.save()
                    return JsonResponse({'success': 'GradeName added successfully'})

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

    elif request.method == 'GET':
        try:
            # Fetch all records from the GradeName_Detials model
            GradeNames = GradeName_Detials.objects.all()

            # Construct a list of dictionaries containing GradeName data
            GradeNames_Master_data = []
            for GradeName in GradeNames:
                GradeName_dict = {
                    'id': GradeName.GradeName_Id,
                    'GradeName': GradeName.GradeName_Name,
                    'Roomid': GradeName.RoomName.pk if GradeName.RoomName else None,
                    'Roomtype': GradeName.RoomName.Room_Name if GradeName.RoomName else None,
                    'status': 'Active' if GradeName.Status else 'Inactive',
                    'created_by': GradeName.created_by,
                }
                GradeNames_Master_data.append(GradeName_dict)

            return JsonResponse(GradeNames_Master_data, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'})




@csrf_exempt   
@require_http_methods(["OPTIONS","GET"])
def Active_GradeNames_link(request):
    if request.method == 'GET':
        try:
            # Fetch all records from the LocationName model
            GradeNames = GradeName_Detials.objects.filter(Status=1)
            if not GradeNames.exists():
                return JsonResponse([], safe=False)
            
            # Construct a list of dictionaries containing location data
            GradeNames_Master_data = []
            for GradeName in GradeNames:
                GradeName_dict = {
                    'id': GradeName.GradeName_Id,
                    'GradeName': GradeName.GradeName_Name,
                    
                }
                GradeNames_Master_data.append(GradeName_dict)

            return JsonResponse(GradeNames_Master_data, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'})






@csrf_exempt   
@require_http_methods(["OPTIONS","GET"])
def Active_Rooms_link(request):
    if request.method == 'GET':
        try:
            # Fetch all records from the LocationName model
            RoomNames = RoomType_Master_Detials.objects.filter(Status=1)
            if not RoomNames.exists():
                return JsonResponse([], safe=False)
            
            # Construct a list of dictionaries containing location data
            RoomNames_Master_data = []
            for RoomName in RoomNames:
                RoomName_dict = {
                    'id': RoomName.Room_Id,
                    'RoomName': RoomName.Room_Name,
                    'Amount': RoomName.Current_Charge
                    
                }
                RoomNames_Master_data.append(RoomName_dict)

            return JsonResponse(RoomNames_Master_data, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'})



 
@csrf_exempt
@require_http_methods(["POST", "OPTIONS", "GET"])
def TherapyType_Master_link(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON request
            data = json.loads(request.body)
            print(":TherapyData", data)
 
            # Extract and sanitize data
            TherapyId = data.get('TherapyId')
            Description = data.get('Description', '')
            IsRequireMedication = data.get('IsRequireMedication', False)
            TherapyType = data.get('TherapyType')  # This should refer to SpecialityId
            SubprocedureName = data.get('SubprocedureName', '')
            IpAmount = data.get('IpAmount', 0)
            OpAmount = data.get('OpAmount', 0)
            IsGst = data.get('IsGst', False)
            GSTvalue = data.get('GSTvalue', 0)
            TherapyName = data.get('TherapyName', '')
            Statusedit = data.get('Statusedit', False)
            created_by = data.get('created_by', '')
 
            # Convert amounts to float, default to 0.0 if invalid or empty
            try:
                IpAmount = float(IpAmount) if IpAmount not in (None, '') else 0.0
            except ValueError:
                return JsonResponse({'error': 'Invalid value for IpAmount'}, status=400)
 
            try:
                OpAmount = float(OpAmount) if OpAmount not in (None, '') else 0.0
            except ValueError:
                return JsonResponse({'error': 'Invalid value for OpAmount'}, status=400)
 
            try:
                GSTvalue = float(GSTvalue) if GSTvalue not in (None, '') else 0.0
            except ValueError:
                return JsonResponse({'error': 'Invalid value for GSTvalue'}, status=400)
 
            # Handle Update/Status Toggle
            if TherapyId:
                print('TherapyId:', TherapyId)
                try:
                    TherapyType_instance = TherapyType_Detials.objects.get(TherapyType_Id=TherapyId)
                except TherapyType_Detials.DoesNotExist:
                    return JsonResponse({'warn': 'TherapyType not found.'})
 
                if Statusedit:
                    print('Statusedit:', Statusedit)
                    TherapyType_instance.Status = not TherapyType_instance.Status
                    TherapyType_instance.save()
                    return JsonResponse({'success': 'TherapyType status updated successfully'})
                else:
                    if TherapyType_Detials.objects.filter(
                        Therapy_Name=TherapyName
                    ).exclude(TherapyType_Id=TherapyId).exists():
                        return JsonResponse({'warn': f"The TherapyType '{TherapyName}' already exists."})
 
                    # Store the old values before updating
                    OldIpAmount = TherapyType_instance.IpAmount
                    OldOpAmount = TherapyType_instance.OpAmount
 
                    # Update the old amounts with previous values
                    TherapyType_instance.OldIpAmount = OldIpAmount
                    TherapyType_instance.OldOpAmount = OldOpAmount
 
                    # Check if TherapyType (SpecialityId) exists
                    if TherapyType:
                        try:
                            Speciality_instance = Speciality_Detials.objects.get(Speciality_Id=TherapyType)
                            TherapyType_instance.TherapyType = Speciality_instance
                        except Speciality_Detials.DoesNotExist:
                            return JsonResponse({'warn': 'Speciality not found.'})
 
                    # Update the new fields
                    TherapyType_instance.TherapyType_Name = Speciality_instance  # This is now set to the Speciality instance
                    TherapyType_instance.Description = Description
                    TherapyType_instance.IsMedications = IsRequireMedication
                    TherapyType_instance.Therapy_Name = TherapyName
                    TherapyType_instance.Sub_Therapy_Name = SubprocedureName
                    TherapyType_instance.IpAmount = IpAmount
                    TherapyType_instance.OpAmount = OpAmount
                    TherapyType_instance.IsGst = IsGst
                    TherapyType_instance.GSTvalue = GSTvalue
 
                    # Save the updated instance
                    TherapyType_instance.save()
                    return JsonResponse({'success': 'TherapyType updated successfully'})
 
 
            # Handle Creation
            else:
                if TherapyType:
                    try:
                        Speciality_instance = Speciality_Detials.objects.get(Speciality_Id=TherapyType)
                    except Speciality_Detials.DoesNotExist:
                        return JsonResponse({'warn': 'Speciality not found.'})
                else:
                    return JsonResponse({'warn': 'TherapyType (SpecialityId) is required to create a TherapyType.'}, status=400)
 
                # Create the new TherapyType instance
                TherapyType_instance = TherapyType_Detials.objects.create(
                    TherapyType_Name=Speciality_instance,  # Correctly assigning the Speciality instance
                    Therapy_Name=TherapyName,
                    Sub_Therapy_Name=SubprocedureName,
                    Description=Description,
                    IsMedications=IsRequireMedication,
                    IpAmount=IpAmount,
                    OpAmount=OpAmount,
                    IsGst=IsGst,
                    GSTvalue=GSTvalue,
                    created_by=created_by
                )
                TherapyType_instance.save()
                return JsonResponse({'success': 'TherapyType added successfully'})
 
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
 
    elif request.method == 'GET':
        try:
            TherapyTypes = TherapyType_Detials.objects.all()
            TherapyTypes_Master_data = []
            for therapy in TherapyTypes:
                # Extract the related Speciality instance
                speciality = therapy.TherapyType_Name  # Assuming TherapyType_Name is the FK to Speciality_Detials
               
                # Build the response dictionary
                therapy_dict = {
                    'id': therapy.TherapyType_Id,
                    # 'TherapyType': str(therapy.TherapyType_Name),  # You may want to extract a specific field for the name
                    'TherapyName': therapy.Therapy_Name,
                    'Description': therapy.Description,
                    'IsRequireMedication': therapy.IsMedications,
                    'SubprocedureName': therapy.Sub_Therapy_Name,
                    'IpAmount': therapy.IpAmount,
                    'OpAmount': therapy.OpAmount,
                    'IsGst': therapy.IsGst,
                    'GSTvalue': therapy.GSTvalue,
                    'created_by': therapy.created_by,
                    'OldIpAmount': therapy.OldIpAmount,
                    'OldOpAmount': therapy.OldOpAmount,
                    'status': 'Active' if therapy.Status else 'Inactive',
                    # Extract relevant fields from the related Speciality model
                    'SpecialityId': speciality.Speciality_Id,  # Assuming this is the field you need
                    'SpecialityName': speciality.Speciality_Name,  # Assuming this is the field you need
                }
                TherapyTypes_Master_data.append(therapy_dict)
           
            # Return the serialized data
            return JsonResponse(TherapyTypes_Master_data, safe=False)
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
 
 
@csrf_exempt  
@require_http_methods(["OPTIONS","GET"])
def TherapyTypes_Active_link(request):
    if request.method == 'GET':
        try:
            # Fetch all records from the LocationName model
            TherapyTypes = TherapyType_Detials.objects.all()
            if not TherapyTypes.exists():
                return JsonResponse([], safe=False)
           
            # Construct a list of dictionaries containing location data
            TherapyTypes_Master_data = []
            for therapy in TherapyTypes:
                speciality = therapy.TherapyType_Name
                Therapy_dict = {
                    'id':therapy.TherapyType_Id,
                    'TherapyName':therapy.Therapy_Name,
                    'SubTherapyName':therapy.Sub_Therapy_Name,
                    'Speciality_Id' :speciality.Speciality_Id,
                    'Speciality_Name': speciality.Speciality_Name
                }
                TherapyTypes_Master_data.append(Therapy_dict)
 
            return JsonResponse(TherapyTypes_Master_data, safe=False)
 
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'})

 
@csrf_exempt  
@require_http_methods(["POST","OPTIONS","GET"])
def Ward_Detials_link(request):
   if request.method == 'GET':
        try:
            # Fetch all records from the LocationName model
            Ward_Master = WardType_Master_Detials.objects.all()
           
            # Construct a list of dictionaries containing location data
            Ward_Master_data = []
            for Ward in Ward_Master:
                Ward_dict = {
                    'id': Ward.Ward_Id,
                    'WardName': Ward.Ward_Name,
                    'Status': 'Active' if Ward.Status else 'Inactive',
                    'created_by': Ward.created_by,
                   
                }
                Ward_Master_data.append(Ward_dict)
 
            return JsonResponse(Ward_Master_data, safe=False)
 
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
 
 
 

@csrf_exempt  
@require_http_methods(["POST","OPTIONS","GET"])
def OtTheaterMaster_Detials_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
 
            print(f"Received data: {data}")
           
            # Extract and validate data
            OtId = data.get('OtId')
            Location = data.get('Location')
            TheatreName = data.get('TheatreName')
            ShortName = data.get('ShortName')
            FloorName = data.get('FloorName')
            Building = data.get('Building')
            Block = data.get('Block')
           
            speciality = data.get('Speciality')
            SpecialityName = data.get('SpecialityName')
            TheatreType = data.get('TheatreType')
            Rent = data.get('Rent')
            Emergency = data.get('Emergency',False)
            Details = data.get('Details')
            Remarks = data.get('Remarks')
            Statusedit = data.get('StatusEdit',False)
            created_by = data.get('created_by','')
     
            try:
                location_instance = Location_Detials.objects.get(pk=Location)
                floor_instance = Floor_Master_Detials.objects.get(pk=FloorName)
                Buiding_ins = Building_Master_Detials.objects.get(pk=Building)
                Block_ins = Block_Master_Detials.objects.get(pk=Block)
               
               
            except (Location_Detials.DoesNotExist, Floor_Master_Detials.DoesNotExist,Building_Master_Detials.DoesNotExist,Block_Master_Detials.DoesNotExist,WardType_Master_Detials.DoesNotExist):
                return JsonResponse({'error': 'Invalid Location or FloorName'})
 
           
           
           
            if OtId:
                if Statusedit:
                   
                    OtTheater_instance = OtTheaterMaster_Detials.objects.get(Ot_Id=OtId)
                    OtTheater_instance.Status = not OtTheater_instance.Status
                    OtTheater_instance.save()
                     
                   
                else:  
                   
                        OtTheater_instance = OtTheaterMaster_Detials.objects.get(Ot_Id=OtId)
                        print(OtTheater_instance)
                        OtTheater_instance.Location=location_instance
                        OtTheater_instance.TheatreName=TheatreName
                        OtTheater_instance.ShortName=ShortName
                        OtTheater_instance.FloorName=floor_instance
                        OtTheater_instance.Building = Buiding_ins
                        OtTheater_instance.Block = Block_ins
                   
                        OtTheater_instance.Speciality=speciality
                        OtTheater_instance.TheatreType = TheatreType
                        OtTheater_instance.Rent = Rent
                        OtTheater_instance.Emergency=Emergency
                        OtTheater_instance.Details=Details
                        OtTheater_instance.Remarks=Remarks
                        OtTheater_instance.save()
                        print('Premkumar')
 
                return JsonResponse({'success': 'OtTheater Updated successfully'})
            else:
               
                if OtTheaterMaster_Detials.objects.filter(TheatreName=TheatreName).exists():
                    return JsonResponse({'warn': f"The TheatreName  are already present in the name of {TheatreName} "})
                else:
                   
                    OtTheater_instance = OtTheaterMaster_Detials(
                        Location=location_instance,
                        TheatreName=TheatreName,
                        ShortName=ShortName,
                        FloorName=floor_instance,
                        Building = Buiding_ins,
                        Block = Block_ins,
                         
                        Speciality = speciality,
                        TheatreType = TheatreType,
                        Rent = Rent,
                        Emergency=Emergency,
                        Details=Details,
                        Remarks=Remarks,
                        created_by=created_by
                    )
                OtTheater_instance.save()
               
            return JsonResponse({'success': 'OtTheater added successfully'})
       
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
       
    elif request.method == 'GET':
        try:
            # Fetch all records from the LocationName model
            OtTheaters = OtTheaterMaster_Detials.objects.all()
           
            # Construct a list of dictionaries containing location data
            OtTheaters_Master_data = []
            for OtTheater in OtTheaters:
                OtTheater_dict = {
                    'id': OtTheater.pk,
                    'LocationId': OtTheater.Location.Location_Id,
                    'Location': OtTheater.Location.Location_Name,
                    'TheatreName': OtTheater.TheatreName,
                    'ShortName': OtTheater.ShortName,
                    'FloorId': OtTheater.FloorName.Floor_Id,
                    'FloorName': OtTheater.FloorName.Floor_Name,
                    'BuidingId':OtTheater.Building.Building_Id,
                    'BuildingName':OtTheater.Building.Building_Name,
                    'BlockId':OtTheater.Block.Block_Id,
                    'BlockName':OtTheater.Block.Block_Name,
                   
                    'SpecialityName':OtTheater.Speciality,
                    'TheatreType':OtTheater.TheatreType,
                    'Rent':OtTheater.Rent,
                    'Emergency': OtTheater.Emergency,
                    'Details': OtTheater.Details,
                    'Remarks': OtTheater.Remarks,
                    'Status': 'Active' if OtTheater.Status else 'Inactive',
                    'created_by': OtTheater.created_by,
                   
                }
                OtTheaters_Master_data.append(OtTheater_dict)
 
                for idx, theatre in enumerate(OtTheaters_Master_data, start=1):
                        theatre["sno"] = idx
 
            return JsonResponse(OtTheaters_Master_data, safe=False)
 
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'})

@csrf_exempt
def Flagg_color_Detials_by_specialtype(request):
     try:
            # Fetch all records from the LocationName model
            Flagg_instance = Flaggcolor_Detials.objects.all()
            specialtypelist = ['GENERAL','VIP','GOVT','INSURANCE','MLC','CLIENT','CORPORATE','DONATION','EMPLOYEE','EMPLOYEERELATION','DOCTOR','DOCTORRELATION']
           
            # Construct a list of dictionaries containing location data
            Flagg_instance_data = []
            for flagg in Flagg_instance:
                flagg_dict = {
                    'id': flagg.Flagg_Id,
                    'FlaggName' : flagg.Flagg_Name ,
                    'FlaggColor': flagg.Flagg_Color,
                    'Status': 'Active' if flagg.Status else "Inactive",
                    'created_by': flagg.created_by,
                }
 
                if flagg.Flagg_Name not  in specialtypelist:
 
                 
                    Flagg_instance_data.append(flagg_dict)
                #print(Flagg_instance_data)
 
            return JsonResponse(Flagg_instance_data, safe=False)
 
     except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
    
 
# service masters
 
@csrf_exempt
@require_http_methods(['POST', 'GET', 'OPTIONS'])
def Insert_service_category_master(request):
    if request.method == 'POST':
 
        try:
 
            data = json.loads(request.body)
 
            print(data, 'data')
            Serviceid = data.get('Serviceid')
 
            if Serviceid:
                try:
                    instance = Service_Category_Masters.objects.get(Serviceid = Serviceid)
                    serializers = ServiceCategoryMasterSerializer(instance, data = data, partial=True)
                    if serializers.is_valid():
                        serializers.save()
                        return JsonResponse({'success': 'Updated Sucessfully'})
                    else:
                        return JsonResponse(serializers.errors)
                except Lab_Department_Detials.DoesNotExist:
                    return JsonResponse({"error":"Service Not Found"})
            else:
                serializers = ServiceCategoryMasterSerializer(data=data)
                print('serializers :', serializers)
                if serializers.is_valid():
                    serializers.save()
                    return JsonResponse({"success": " Saved successfully."})
                else:
                    print('error :', serializers.errors)
                    return JsonResponse(serializers.errors)
 
        except Exception as e:
            print('error', e)
            return JsonResponse({"Error": e})
 
    elif request.method == 'GET':
 
        try:
            # Get all records from Service_Category_Masters
            subdepartments = Service_Category_Masters.objects.all()
           
            # Serialize the data
            serializers = ServiceCategoryMasterSerializer(subdepartments, many=True)
           
            # Add custom 'id' field
            for index, i in enumerate(serializers.data, start=1):
                i["id"] = index
           
            # Return serialized data as JSON
            return JsonResponse(serializers.data, safe=False)
       
        except Exception as e:
            # Catch any exceptions, convert to string, and return as a JSON response
            return JsonResponse({'error': str(e)})
 
 



