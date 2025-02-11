from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Count
from django.http import JsonResponse
from .models import *
from Masters.models import *
from Frontoffice.models import Patient_Admission_Room_Detials,Patient_Admission_Detials
from django.shortcuts import get_object_or_404
from django.db.models import  Q
from .serializers import *

# building----------------
@csrf_exempt   
@require_http_methods(["POST","OPTIONS","GET"])
def Building_Master_Detials_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data,'dataaa')
            # Extract and validate data
            BuildingId = data.get('BuildingId','')
            BuildingName = data.get('BuildingName','')
            Location = data.get('Location','')
            Statusedit = data.get('Statusedit',False)
            created_by = data.get('created_by','')
            if Location:
                Location_instance = Location_Detials.objects.get(Location_Id = Location)
           
            if BuildingId:
                if Statusedit:
                    Building_instance = Building_Master_Detials.objects.get(pk=BuildingId)
                    # Check if any Room_Master_Detials records have Booking_Status not equal to "Available"
                    non_available_status_exists = Room_Master_Detials.objects.filter(
                        Building_Name=Building_instance
                    ).exclude(Booking_Status='Available').exists()

                    if non_available_status_exists:
                        # Raise a ValidationError if any Booking_Status is not "Available"
                        return JsonResponse ({'warn':"Cannot change the status because some Booking_Status in Room_Master_Detials is not 'Available'."})
                    else:
                        # Toggle the status
                        Building_instance.Status = not Building_instance.Status

                        # If all Booking_Status are 'Available', proceed with the status update
                        Block_Master_Detials.objects.filter(Building_Name=Building_instance).update(Status=Building_instance.Status)
                        Floor_Master_Detials.objects.filter(Building_Name=Building_instance).update(Status=Building_instance.Status)
                        WardType_Master_Detials.objects.filter(Building_Name=Building_instance).update(Status=Building_instance.Status)
                        RoomType_Master_Detials.objects.filter(Building_Name=Building_instance).update(Status=Building_instance.Status)
                        Room_Master_Detials.objects.filter(Building_Name=Building_instance).update(Status=Building_instance.Status)
                        # Save the changes to the database
                        Building_instance.save()

                 
        
                    
                else:
                    if Building_Master_Detials.objects.filter(Building_Name=BuildingName, Location_Name=Location_instance ).exclude(pk = BuildingId).exists():
                        return JsonResponse({'warn': f"The Building Detials are already present in the name of {BuildingName} and {Location_instance.Location_Name} "})
                    else:
                        Building_instance = Building_Master_Detials.objects.get(pk=BuildingId)
                        # Create a new LocationName instance
                        Building_instance.Building_Name=BuildingName
                        Building_instance.Location_Name=Location_instance
                    
                        Building_instance.save()

                return JsonResponse({'success': 'Building Detials Updated successfully'})
            else:
                if Building_Master_Detials.objects.filter(Building_Name=BuildingName, Location_Name=Location_instance ).exists():
                    return JsonResponse({'warn': f"The Building Detials are already present in the name of {BuildingName} and {Location_instance.Location_Name} "})
                else:
                    Building_instance = Building_Master_Detials(
                        Building_Name=BuildingName,
                        Location_Name=Location_instance,
                        created_by=created_by
                    )
                Building_instance.save()
                return JsonResponse({'success': 'Building Detials added successfully'})
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
        
    elif request.method == 'GET':
        try:
            # Fetch all records from the LocationName model
            Building_Master = Building_Master_Detials.objects.all()
            
            # Construct a list of dictionaries containing location data
            Building_Master_data = []
            for Build in Building_Master:
                Build_dict = {
                    'id': Build.Building_Id,
                    'BuildingName': Build.Building_Name,
                    'Location_Name': Build.Location_Name.Location_Name,
                    'Location_Id': Build.Location_Name.Location_Id,
                    'Status': 'Active' if Build.Status else 'Inactive',
                    'created_by': Build.created_by,
                    
                }
                Building_Master_data.append(Build_dict)

            return JsonResponse(Building_Master_data, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)



def get_building_Data_by_location(request):
    try:
        Location=request.GET.get('Location')
        if not Location:
            return JsonResponse({'error':'Location are required'})
        
        loc_ins= Location_Detials.objects.get(Location_Id=Location)
        # Fetch all records from the LocationName model
        if not Building_Master_Detials.objects.filter(Status=True,Location_Name=loc_ins).exists():
            return JsonResponse({'error':'Data not found'})
        
        Building_Master = Building_Master_Detials.objects.filter(Status=True,Location_Name=loc_ins)
        print(Building_Master)
        # Construct a list of dictionaries containing location data
        Building_Master_data = []
        for Build in Building_Master:
            Build_dict = {
                'id': Build.Building_Id,
                'BuildingName': Build.Building_Name,
                
            }
            Building_Master_data.append(Build_dict)

        return JsonResponse(Building_Master_data, safe=False)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'An internal server error occurred'}, status=500)


# block-----------

@csrf_exempt   
@require_http_methods(["POST","OPTIONS","GET"])
def Block_Master_Detials_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data,'dataaa')
            # Extract and validate data
            BlockId = data.get('BlockId','')
            BlockName = data.get('BlockName','')
            BuildingName = data.get('BuildingName','')
            Location = data.get('Location','')
            Statusedit = data.get('Statusedit',False)
            created_by = data.get('created_by','')
            if Location:
                Location_instance = Location_Detials.objects.get(Location_Id = Location)
            if BuildingName:
                Building_instance = Building_Master_Detials.objects.get(Building_Id = BuildingName)
                
           
            if BlockId:
                if Statusedit:
                    Block_instance = Block_Master_Detials.objects.get(pk=BlockId)
    
                    # Check if any Room_Master_Detials records have Booking_Status not equal to "Available"
                    non_available_status_exists = Room_Master_Detials.objects.filter(
                        Block_Name=Block_instance
                    ).exclude(Booking_Status='Available').exists()

                    if non_available_status_exists:
                        # Return a warning message if any Booking_Status is not "Available"
                        return JsonResponse({'warn': "Cannot change the status because some Booking_Status in Room_Master_Detials is not 'Available'."})
                    
                    # Check if all parent statuses are True
                    parent_statuses = []
                    
                    if not Block_instance.Building_Name.Status:
                        parent_statuses.append("Building Status")
                    
                    if parent_statuses:
                        # If any parent status is False, return a warning message
                        return JsonResponse({'warn': f"Cannot change the block status because the following parent statuses are not Active: {', '.join(parent_statuses)}."})
                    
                    # Toggle the status
                    Block_instance.Status = not Block_instance.Status
                    
                    # If all Booking_Status are 'Available', proceed with the status update
                    Floor_Master_Detials.objects.filter(Block_Name=Block_instance).update(Status=Block_instance.Status)
                    WardType_Master_Detials.objects.filter(Block_Name=Block_instance).update(Status=Block_instance.Status)
                    RoomType_Master_Detials.objects.filter(Block_Name=Block_instance).update(Status=Block_instance.Status)
                    Room_Master_Detials.objects.filter(Block_Name=Block_instance).update(Status=Block_instance.Status)
                    
                    # Save the changes to the database
                    Block_instance.save()
                    
                    return JsonResponse({'success': "Block status updated successfully."})
                    
        
                else:
                    if Block_Master_Detials.objects.filter(Block_Name=BlockName, Location_Name=Location_instance,Building_Name = Building_instance ).exclude(pk = BlockId).exists():
                        return JsonResponse({'warn': f"The Block Detials are already present in the name of {BlockName} and {Location_instance.Location_Name} and {Building_instance.Building_Name}"})
                    else:
                        Block_instance = Block_Master_Detials.objects.get(pk=BlockId)
                        # Create a new LocationName instance
                        Block_instance.Block_Name=BlockName
                        Block_instance.Location_Name=Location_instance
                        Block_instance.Building_Name = Building_instance
                    
                        Block_instance.save()

                return JsonResponse({'success': 'Block Detials Updated successfully'})
            else:
                if Block_Master_Detials.objects.filter(Block_Name=BlockName, Location_Name=Location_instance,Building_Name = Building_instance ).exists():
                    return JsonResponse({'warn': f"The Block Detials are already present in the name of {BlockName} and {Location_instance.Location_Name} and {Building_instance.Building_Name}"})
                else:
                    Block_instance = Block_Master_Detials(
                        Block_Name=BlockName,
                        Building_Name = Building_instance,
                        Location_Name=Location_instance,
                        created_by=created_by
                    )
                Block_instance.save()
                return JsonResponse({'success': 'Block Detials added successfully'})
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
        
    elif request.method == 'GET':
        try:
            # Fetch all records from the LocationName model
            Block_Master = Block_Master_Detials.objects.all()
            
            # Construct a list of dictionaries containing location data
            Block_Master_data = []
            for Block in Block_Master:
                Block_dict = {
                    'id': Block.Block_Id,
                    'BlockName': Block.Block_Name,
                    'BuildingId': Block.Building_Name.Building_Id,
                    'BuildingName': Block.Building_Name.Building_Name,
                    'Location_Name': Block.Location_Name.Location_Name,
                    'Location_Id': Block.Location_Name.Location_Id,
                    'Status': 'Active' if Block.Status else 'Inactive',
                    'created_by': Block.created_by,
                    
                }
                Block_Master_data.append(Block_dict)

            return JsonResponse(Block_Master_data, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)



def get_block_Data_by_Building(request):
    try:
       
        Building=request.GET.get('Building')
        if not Building:
            return JsonResponse({'error':'Building are required'},status=400)
        
        Building_ins= Building_Master_Detials.objects.get(Building_Id=Building)
        
        if not Block_Master_Detials.objects.filter(Status=True,Building_Name=Building_ins,Location_Name__pk=Building_ins.Location_Name.pk).exists():
            return JsonResponse({'error':'Data Not Found'},status=400)
        # Fetch all records from the LocationName model
        Block_Master = Block_Master_Detials.objects.filter(Status=True,Building_Name=Building_ins,Location_Name__pk=Building_ins.Location_Name.pk)
 
        # Construct a list of dictionaries containing location data
        Block_Master_data = []
        for Block in Block_Master:
            Block_dict = {
                'id': Block.Block_Id,
                'BlockName': Block.Block_Name,
                
            }
            Block_Master_data.append(Block_dict)

        return JsonResponse(Block_Master_data, safe=False)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'An internal server error occurred'}, status=500)



# floor------------
@csrf_exempt   
@require_http_methods(["POST","OPTIONS","GET"])
def Floor_Master_Detials_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data,'dataaa')
            # Extract and validate data
            FloorId = data.get('FloorId','')
            FloorName = data.get('FloorName','')
            BlockName = data.get('BlockName','')
            BuildingName = data.get('BuildingName','')
            Location = data.get('Location','')
            Statusedit = data.get('Statusedit',False)
            created_by = data.get('created_by','')
            
            Location_instance=None
            Building_instance=None
            Block_instance=None
            
            if Location:
                Location_instance = Location_Detials.objects.get(Location_Id = Location)
            if BuildingName:
                Building_instance = Building_Master_Detials.objects.get(Building_Id = BuildingName)
                
            if BlockName:
                Block_instance = Block_Master_Detials.objects.get(Block_Id = BlockName)
                
        
            if FloorId:
                if Statusedit:
                    Floor_instance = Floor_Master_Detials.objects.get(pk=FloorId)
    
                    # Check if any Room_Master_Detials records have Booking_Status not equal to "Available"
                    non_available_status_exists = Room_Master_Detials.objects.filter(
                        Floor_Name=Floor_instance
                    ).exclude(Booking_Status='Available').exists()

                    if non_available_status_exists:
                        # Return a warning message if any Booking_Status is not "Available"
                        return JsonResponse({'warn': "Cannot change the status because some Booking_Status in Room_Master_Detials is not 'Available'."})
                    
                    # Check if all parent statuses are True
                    parent_statuses = []
                    
                    if not Floor_instance.Building_Name.Status:
                        parent_statuses.append("Building Status")
                    
                    if not Floor_instance.Block_Name.Status:
                        parent_statuses.append("Block Status")
                    
                    if parent_statuses:
                        # If any parent status is False, return a warning message
                        return JsonResponse({'warn': f"Cannot change the floor status because the following parent statuses are not Active: {', '.join(parent_statuses)}."})
                    
                    # Toggle the status
                    Floor_instance.Status = not Floor_instance.Status
                    
                    # If all Booking_Status are 'Available', proceed with the status update
                    WardType_Master_Detials.objects.filter(Floor_Name=Floor_instance).update(Status=Floor_instance.Status)
                    RoomType_Master_Detials.objects.filter(Floor_Name=Floor_instance).update(Status=Floor_instance.Status)
                    Room_Master_Detials.objects.filter(Floor_Name=Floor_instance).update(Status=Floor_instance.Status)
                    
                    # Save the changes to the database
                    Floor_instance.save()
                    
                    return JsonResponse({'success': "Floor status updated successfully."})
                    
                   
        
                    # Toggle the status
                    
                    
                    # Save the changes to the database
                    
                else:
                    if Floor_Master_Detials.objects.filter(Floor_Name=FloorName, Location_Name=Location_instance,Building_Name = Building_instance ,Block_Name=Block_instance).exclude(pk= FloorId).exists():
                        return JsonResponse({'warn': f"The Block Detials are already present in the name of {FloorName} and {Location_instance.Location_Name} and {Building_instance.Building_Name} and {Block_instance.Block_Name}"})
                    else:
                        Floor_instance = Floor_Master_Detials.objects.get(pk=FloorId)
                        # Create a new LocationName instance
                        Floor_instance.Floor_Name=FloorName
                        Floor_instance.Block_Name=Block_instance
                        Floor_instance.Location_Name=Location_instance
                        Floor_instance.Building_Name = Building_instance
                    
                        Floor_instance.save()

                return JsonResponse({'success': 'Floor Detials Updated successfully'})
            else:
                if Floor_Master_Detials.objects.filter(Floor_Name=FloorName, Location_Name=Location_instance,Building_Name = Building_instance ,Block_Name=Block_instance).exists():
                    return JsonResponse({'warn': f"The Block Detials are already present in the name of {FloorName} and {Location_instance.Location_Name} and {Building_instance.Building_Name} and {Block_instance.Block_Name}"})
                else:
                    Floor_instance = Floor_Master_Detials(
                        Floor_Name=FloorName,
                        Block_Name=Block_instance,
                        Building_Name = Building_instance,
                        Location_Name=Location_instance,
                        created_by=created_by
                    )
                Floor_instance.save()
                return JsonResponse({'success': 'Floor Detials added successfully'})
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
        
    elif request.method == 'GET':
        try:
            # Fetch all records from the LocationName model
            Floor_Master = Floor_Master_Detials.objects.all()
            
            # Construct a list of dictionaries containing location data
            Floor_Master_data = []
            for Floor in Floor_Master:
                Floor_dict = {
                    'id': Floor.Floor_Id,
                    'FloorName': Floor.Floor_Name,
                    'BlockId': Floor.Block_Name.Block_Id,
                    'BlockName': Floor.Block_Name.Block_Name,
                    'BuildingId': Floor.Building_Name.Building_Id,
                    'BuildingName': Floor.Building_Name.Building_Name,
                    'Location_Name': Floor.Location_Name.Location_Name,
                    'Location_Id': Floor.Location_Name.Location_Id,
                    'Status': 'Active' if Floor.Status else 'Inactive',
                    'created_by': Floor.created_by,
                    
                }
                Floor_Master_data.append(Floor_dict)

            return JsonResponse(Floor_Master_data, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)



def get_Floor_Data_by_Building_block_loc(request):
    try:
        Block=request.GET.get('Block')
        if not Block:
            return JsonResponse({'error':'Block are required'})
        
        Block_ins= Block_Master_Detials.objects.get(Block_Id=Block)
        if not Floor_Master_Detials.objects.filter(Status=True,Building_Name=Block_ins.Building_Name,Block_Name=Block_ins,Location_Name=Block_ins.Location_Name).exists():
            return JsonResponse({'error':'Data not found'})
        # Fetch all records from the LocationName model
        Floor_Master = Floor_Master_Detials.objects.filter(Status=True,Building_Name=Block_ins.Building_Name,Block_Name=Block_ins,Location_Name=Block_ins.Location_Name)
 
        # Construct a list of dictionaries containing location data
        Floor_Master_data = []
        for Floor in Floor_Master:
            Floor_dict = {
                'id': Floor.Floor_Id,
                'FloorName': Floor.Floor_Name, 
            }
            Floor_Master_data.append(Floor_dict)

        return JsonResponse(Floor_Master_data, safe=False)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'An internal server error occurred'}, status=500)


# ward name
@csrf_exempt   
@require_http_methods(["POST","OPTIONS","GET"])
def Ward_Master_Detials_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data,'dataaa')
            # Extract and validate data
            WardId = data.get('WardId','')
            WardName = data.get('WardName','')
            FloorName = data.get('FloorName','')
            BlockName = data.get('BlockName','')
            BuildingName = data.get('BuildingName','')
            Location = data.get('Location','')
            Statusedit = data.get('Statusedit',False)
            created_by = data.get('created_by','')
            
            Location_instance=None
            Building_instance=None
            Block_instance=None
            Floor_instance=None
            
            if Location:
                Location_instance = Location_Detials.objects.get(Location_Id = Location)
            
            if BuildingName:
                Building_instance = Building_Master_Detials.objects.get(Building_Id = BuildingName)
                
            if BlockName:
                Block_instance = Block_Master_Detials.objects.get(Block_Id = BlockName)
                
            if FloorName:
                Floor_instance = Floor_Master_Detials.objects.get(Floor_Id = FloorName)
                
        
            if WardId:
                if Statusedit:
                    ward_instance = WardType_Master_Detials.objects.get(pk=WardId)
    
                    # Check if any Room_Master_Detials records have Booking_Status not equal to "Available"
                    non_available_status_exists = Room_Master_Detials.objects.filter(
                        Ward_Name=ward_instance
                    ).exclude(Booking_Status='Available').exists()

                    if non_available_status_exists:
                        # Return a warning message if any Booking_Status is not "Available"
                        return JsonResponse({'warn': "Cannot change the status because some Booking_Status in Room_Master_Detials is not 'Available'."})
                    
                    # Check if all parent statuses are True
                    parent_statuses = []
                    
                    if not ward_instance.Building_Name.Status:
                        parent_statuses.append("Building Status")
                    
                    if not ward_instance.Block_Name.Status:
                        parent_statuses.append("Block Status")
                    
                    if not ward_instance.Floor_Name.Status:
                        parent_statuses.append("Floor Status")
                    
                    if parent_statuses:
                        # If any parent status is False, return a warning message
                        return JsonResponse({'warn': f"Cannot change the ward status because the following parent statuses are not Active: {', '.join(parent_statuses)}."})
                    
                    # If all conditions are met, toggle the ward status
                    ward_instance.Status = not ward_instance.Status
                    
                    # Update related RoomType and Room statuses
                    RoomType_Master_Detials.objects.filter(Ward_Name=ward_instance).update(Status=ward_instance.Status)
                    Room_Master_Detials.objects.filter(Ward_Name=ward_instance).update(Status=ward_instance.Status)
                    
                    # Save the changes to the database
                    ward_instance.save()
                    
                    return JsonResponse({'success': "Ward status updated successfully."})
                    
        
                   
                else:
                    if WardType_Master_Detials.objects.filter(Ward_Name=WardName, Location_Name=Location_instance,Building_Name = Building_instance ,Block_Name=Block_instance,Floor_Name=Floor_instance).exclude(pk=WardId).exists():
                        return JsonResponse({'warn': f"The Ward Detials are already present in the name of {WardName} and {Location_instance.Location_Name} and {Building_instance.Building_Name} and {Block_instance.Block_Name} and {Floor_instance.Floor_Name}"})
                    else:
                        print("opopopoo")
                        ward_instance = WardType_Master_Detials.objects.get(pk=WardId)
                        print("ward_instance",ward_instance)
                        # Create a new LocationName instance
                        ward_instance.Ward_Name=WardName
                        ward_instance.Floor_Name=Floor_instance
                        ward_instance.Block_Name=Block_instance
                        ward_instance.Building_Name = Building_instance
                        ward_instance.Location_Name=Location_instance
                        ward_instance.save()
                        print("8080809")
    
                return JsonResponse({'success': 'Ward Detials Updated successfully'})
            else:
                if WardType_Master_Detials.objects.filter(Ward_Name=WardName, Location_Name=Location_instance,Building_Name = Building_instance ,Block_Name=Block_instance,Floor_Name=Floor_instance).exists():
                        return JsonResponse({'warn': f"The Ward Detials are already present in the name of {WardName} and {Location_instance.Location_Name} and {Building_instance.Building_Name} and {Block_instance.Block_Name} and {Floor_instance.Floor_Name}"})
                else:
                    print("ward")
                    ward_instance = WardType_Master_Detials(
                        Ward_Name=WardName,
                        Floor_Name=Floor_instance,
                        Block_Name=Block_instance,
                        Building_Name = Building_instance,
                        Location_Name=Location_instance,
                        created_by=created_by
                    )

                    ward_instance.save()

                    return JsonResponse({'success': 'Ward Detials added successfully'})
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
        
    elif request.method == 'GET':
        try:
            Floor_Master = WardType_Master_Detials.objects.all()
            
            Floor_Master_data = []
            for Floor in Floor_Master:
                Floor_dict = {
                    'id': Floor.Ward_Id,
                    'WardName': Floor.Ward_Name,
                    'FloorId': Floor.Floor_Name.Floor_Id,
                    'FloorName': Floor.Floor_Name.Floor_Name,
                    'BlockId': Floor.Block_Name.Block_Id,
                    'BlockName': Floor.Block_Name.Block_Name,
                    'BuildingId': Floor.Building_Name.Building_Id,
                    'BuildingName': Floor.Building_Name.Building_Name,
                    'Location_Name': Floor.Location_Name.Location_Name,
                    'Location_Id': Floor.Location_Name.Location_Id,
                    'Status': 'Active' if Floor.Status else 'Inactive',
                    'created_by': Floor.created_by,
                }

                Floor_Master_data.append(Floor_dict)
            return JsonResponse(Floor_Master_data, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)




def get_Ward_Data_by_Building_block_Floor_loc(request):
    try:
        Floor = request.GET.get('Floor')
        RegisterType = request.GET.get('RegisterType')
        
        if not Floor:
            return JsonResponse({'error': 'Floor is required'}, status=400)
        
        # Get the Floor instance
        try:
            Floor_ins = Floor_Master_Detials.objects.get(Floor_Id=Floor)
        except Floor_Master_Detials.DoesNotExist:
            return JsonResponse({'error': 'Floor not found'}, status=404)
        
        # Base query for WardType_Master_Details
        ward_query = WardType_Master_Detials.objects.filter(
            Status=True,
            Building_Name=Floor_ins.Building_Name,
            Block_Name=Floor_ins.Block_Name,
            Floor_Name=Floor_ins,
            Location_Name=Floor_ins.Location_Name
        )
        
        # Apply additional filtering based on RegisterType
        if RegisterType == 'IP':
            ward_query = ward_query.exclude(Ward_Name__in=['CASUALITY', 'OT'])
        elif RegisterType == 'Casuality':
            ward_query = ward_query.filter(Ward_Name='Casuality')
        
        # If no Ward records found
        if not ward_query.exists():
            return JsonResponse({'error': 'No Ward data found'}, status=404)
        
        # Construct response data
        Ward_Master_data = [{'id': Ward.Ward_Id, 'WardName': Ward.Ward_Name} for Ward in ward_query]

        return JsonResponse(Ward_Master_data, safe=False)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'An internal server error occurred'}, status=500)

# room name master
@csrf_exempt   
@require_http_methods(["POST","OPTIONS","GET"])
def Room_Master_Detials_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data,'dataaa')
            # Extract and validate data
            RoomId = data.get('RoomId','')
            # RoomName = data.get('RoomName')
            WardName = data.get('WardName','')
            FloorName = data.get('FloorName','')
            BlockName = data.get('BlockName','')
            BuildingName = data.get('BuildingName','')
            RoomCharge = float(data.get('RoomCharge','0'))
            doctorcharges = float(data.get('DoctorCharges','0'))
            nursecharges = float(data.get('NurseCharges','0'))
            GST_val = data.get('GST','Nill')
            Location = data.get('Location','')
            Statusedit = data.get('Statusedit',False)
            created_by = data.get('created_by','')
            
            Location_instance=None
            Building_instance=None
            Block_instance=None
            Floor_instance=None
            Ward_instance=None
            
            if Location:
                Location_instance = Location_Detials.objects.get(Location_Id = Location)
            
            if BuildingName:
                Building_instance = Building_Master_Detials.objects.get(Building_Id = BuildingName)
                
            if BlockName:
                Block_instance = Block_Master_Detials.objects.get(Block_Id = BlockName)
                
            if FloorName:
                Floor_instance = Floor_Master_Detials.objects.get(Floor_Id = FloorName)
                
            if WardName:
                Ward_instance = WardType_Master_Detials.objects.get(Ward_Id = WardName)
                
            Total_Current_Charge=0
            if GST_val !='Nill':
                Total_Current_Charge=  RoomCharge + ((RoomCharge * int(GST_val)) / 100) 
            else:
                Total_Current_Charge=RoomCharge
                
            if RoomId:
                if Statusedit:
                   
                    Room_instance = RoomType_Master_Detials.objects.get(pk=RoomId)
                    
                    # Check if any Room_Master_Detials records have Booking_Status not equal to "Available"
                    non_available_status_exists = Room_Master_Detials.objects.filter(
                        Room_Name=Room_instance
                    ).exclude(Booking_Status='Available').exists()

                    if non_available_status_exists:
                        # Return a warning message if any Booking_Status is not "Available"
                        return JsonResponse({'warn': "Cannot change the status because some Booking_Status in Room_Master_Detials is not 'Available'."})
                    
                    # Check if all parent statuses are True
                    parent_statuses = []
                    
                    if not Room_instance.Building_Name.Status:
                        parent_statuses.append("Building Status")
                    
                    if not Room_instance.Block_Name.Status:
                        parent_statuses.append("Block Status")
                    
                    if not Room_instance.Floor_Name.Status:
                        parent_statuses.append("Floor Status")
                    
                    if not Room_instance.Ward_Name.Status:
                        parent_statuses.append("Ward Status")
                    
                    if parent_statuses:
                        # If any parent status is False, return a warning message
                        return JsonResponse({'warn': f"Cannot change the room status because the following parent statuses are not Active: {', '.join(parent_statuses)}."})
                    
                    # If all conditions are met, toggle the room status
                    Room_instance.Status = not Room_instance.Status
                    
                    # Update related Room_Master_Detials statuses
                    Room_Master_Detials.objects.filter(Room_Name=Room_instance).update(Status=Room_instance.Status)
                    
                    # Save the changes to the database
                    Room_instance.save()
                    
                    return JsonResponse({'success': "Room status updated successfully."})
        
                else:
                    if RoomType_Master_Detials.objects.filter(Location_Name=Location_instance,Building_Name = Building_instance ,Block_Name=Block_instance,Floor_Name=Floor_instance,Ward_Name=Ward_instance,Current_Charge=RoomCharge).exclude(pk = RoomId).exists():
                        return JsonResponse({'warn': f"The Room Detials are already present in the name of {WardName} and {Location_instance.Location_Name} and {Building_instance.Building_Name} and {Block_instance.Block_Name} and {Floor_instance.Floor_Name}"})
                    else:
                        RoomType_instance = RoomType_Master_Detials.objects.get(pk=RoomId)
                        # RoomType_instance.Room_Name = RoomName
                        RoomType_instance.Ward_Name=Ward_instance
                        RoomType_instance.Floor_Name=Floor_instance
                        RoomType_instance.Block_Name=Block_instance
                        RoomType_instance.Building_Name = Building_instance
                        RoomType_instance.Location_Name=Location_instance
                        RoomType_instance.Prev_Charge = RoomType_instance.Current_Charge
                        RoomType_instance.Current_Charge = RoomCharge if RoomCharge else 0
                        RoomType_instance.Doctorcharges = doctorcharges if doctorcharges else 0
                        RoomType_instance.Nursecharges = nursecharges if nursecharges else 0
                        RoomType_instance.GST_Charge = GST_val
                        RoomType_instance.Total_Prev_Charge = RoomType_instance.Total_Current_Charge
                        RoomType_instance.Total_Current_Charge = Total_Current_Charge
                        
                        RoomType_instance.save()
                        

                return JsonResponse({'success': 'Room Detials Updated successfully'})
            else:
                if RoomType_Master_Detials.objects.filter(Location_Name=Location_instance,Building_Name = Building_instance ,Block_Name=Block_instance,Floor_Name=Floor_instance,Ward_Name=Ward_instance).exists():
                        return JsonResponse({'warn': f"The Room Detials are already present in the name of {WardName} and {Location_instance.Location_Name} and {Building_instance.Building_Name} and {Block_instance.Block_Name} and {Floor_instance.Floor_Name}"})
                else:
                    RoomType_instance = RoomType_Master_Detials(
                        Ward_Name=Ward_instance,
                        Floor_Name=Floor_instance,
                        Block_Name=Block_instance,
                        Building_Name = Building_instance,
                        Location_Name=Location_instance,
                        # Room_Name=RoomName,
                        Current_Charge=RoomCharge if RoomCharge else 0,
                        Doctorcharges=doctorcharges if doctorcharges else 0,
                        Nursecharges=nursecharges if nursecharges else 0,
                        GST_Charge=GST_val,
                        Total_Current_Charge=Total_Current_Charge,
                        created_by=created_by
                    )
                    RoomType_instance.save()
                    return JsonResponse({'success': 'Room Detials added successfully'})
        
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
        
    elif request.method == 'GET':
        try:
            # Fetch all records from the LocationName model
            RoomType_Master = RoomType_Master_Detials.objects.all()
            
            # Construct a list of dictionaries containing location data
            RoomType_Master_data = []
            for Roomtype in RoomType_Master:
                Roomtype_dict = {
                    'id': Roomtype.Room_Id,
                    # 'RoomName': Roomtype.Room_Name,
                    'Prev_Charge': Roomtype.Prev_Charge,
                    'Current_Charge': Roomtype.Current_Charge,
                    'GST_val': Roomtype.GST_Charge,
                    'Total_Prev_Charge': Roomtype.Total_Prev_Charge,
                    'Total_Current_Charge': Roomtype.Total_Current_Charge,
                    'WardId': Roomtype.Ward_Name.Ward_Id,
                    'WardName': Roomtype.Ward_Name.Ward_Name,
                    'FloorId': Roomtype.Floor_Name.Floor_Id,
                    'FloorName': Roomtype.Floor_Name.Floor_Name,
                    'BlockId': Roomtype.Block_Name.Block_Id,
                    'BlockName': Roomtype.Block_Name.Block_Name,
                    'BuildingId': Roomtype.Building_Name.Building_Id,
                    'BuildingName': Roomtype.Building_Name.Building_Name,
                    'Location_Name': Roomtype.Location_Name.Location_Name,
                    'Doctor_Charge': Roomtype.Doctorcharges,
                    'Nurse_Charge': Roomtype.Nursecharges,
                    'Location_Id': Roomtype.Location_Name.Location_Id,
                    'Status': 'Active' if Roomtype.Status else 'Inactive',
                    'created_by': Roomtype.created_by,
                    
                }
                RoomType_Master_data.append(Roomtype_dict)

            return JsonResponse(RoomType_Master_data, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)



def get_RoomType_Data_by_Building_block_Floor_ward_loc(request):
    try:
        Ward=request.GET.get('Ward')
        RegisterType=request.GET.get('RegisterType')
        print('Waaarrrrddddddddd',Ward)
        if not Ward:
            return JsonResponse({'error':'Ward are required'})
        

        Ward_ins= WardType_Master_Detials.objects.get(Ward_Id=Ward)
        print('Waaarrrrd111111',Ward)
        if not RoomType_Master_Detials.objects.filter(Status=True,Building_Name=Ward_ins.Building_Name,Block_Name=Ward_ins.Block_Name,Floor_Name=Ward_ins.Floor_Name,Ward_Name=Ward_ins,Location_Name=Ward_ins.Location_Name).exists():
            return JsonResponse({'error':'Data not found'})
        
        # Fetch all records from the LocationName model
        RoomType_Master = RoomType_Master_Detials.objects.filter(
            Status=True,
            Building_Name=Ward_ins.Building_Name,
            Block_Name=Ward_ins.Block_Name,
            Floor_Name=Ward_ins.Floor_Name,
            Ward_Name=Ward_ins,
            Location_Name=Ward_ins.Location_Name
            )
        
 
        # Construct a list of dictionaries containing location data
        RoomType_Master_data = []
        for RoomType in RoomType_Master:
            Floor_dict = {
                'id': RoomType.Room_Id,
                'id1': RoomType.Ward_Name.Ward_Id,
                # 'RoomName': RoomType.Room_Name, 
                'BedCharge': RoomType.Current_Charge, 
                'GST': RoomType.GST_Charge, 
                'TotalCharge': RoomType.Total_Current_Charge, 
            }
            RoomType_Master_data.append(Floor_dict)

        return JsonResponse(RoomType_Master_data, safe=False)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'An internal server error occurred'}, status=500)



# room master master


@csrf_exempt   
@require_http_methods(["POST","OPTIONS","GET"])
def Room_Master_Master_Detials_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data, 'dataaa')

            # Extract and validate data
            RoomMasterId = data.get('RoomMasterId', '')
            RoomNo = data.get('RoomNo')
            BedNo = data.get('BedNo')
            WardName = data.get('WardName', '')
            FloorName = data.get('FloorName', '')
            BlockName = data.get('BlockName', '')
            BuildingName = data.get('BuildingName', '')
            Location = data.get('Location', '')
            Statusedit = data.get('Statusedit', False)
            created_by = data.get('created_by', '')

            # Fetch related instances
            Location_instance = Location_Detials.objects.get(Location_Id=Location) if Location else None
            Building_instance = Building_Master_Detials.objects.get(Building_Id=BuildingName) if BuildingName else None
            Block_instance = Block_Master_Detials.objects.get(Block_Id=BlockName) if BlockName else None
            Floor_instance = Floor_Master_Detials.objects.get(Floor_Id=FloorName) if FloorName else None
            Ward_instance = RoomType_Master_Detials.objects.get(Ward_Name__Ward_Id=WardName) if WardName else None

            if RoomMasterId:
                if Statusedit:
                    Room_master_instance = Room_Master_Detials.objects.get(pk=RoomMasterId)

                    # Ensure Booking_Status is 'Available'
                    if Room_master_instance.Booking_Status != 'Available':
                        return JsonResponse({'warn': "Cannot change the status because the Booking_Status is not 'Available'."})

                    # Validate parent statuses
                    parent_statuses = []
                    if not Room_master_instance.Building_Name.Status:
                        parent_statuses.append("Building Status")
                    if not Room_master_instance.Block_Name.Status:
                        parent_statuses.append("Block Status")
                    if not Room_master_instance.Floor_Name.Status:
                        parent_statuses.append("Floor Status")
                    if not Room_master_instance.Ward_Name.Status:
                        parent_statuses.append("Ward Status")

                    if parent_statuses:
                        return JsonResponse({'warn': f"Cannot change the room status because the following parent statuses are not Active: {', '.join(parent_statuses)}."})

                    # Toggle the status
                    Room_master_instance.Status = not Room_master_instance.Status
                    Room_master_instance.save()

                    return JsonResponse({'success': "Room status updated successfully."})
                else:
                    # Validate uniqueness of Room Master Details
                    if Room_Master_Detials.objects.filter(
                        Room_No=RoomNo,
                        Bed_No=BedNo,
                        Location_Name=Location_instance,
                        Building_Name=Building_instance,
                        Block_Name=Block_instance,
                        Floor_Name=Floor_instance
                    ).exclude(pk=RoomMasterId).exists():
                        return JsonResponse({'warn': f"The Room Master Detials are already present in the name of {RoomNo} and {BedNo}."})
                    else:
                        # Update the Room Master details
                        Room_master_instance = Room_Master_Detials.objects.get(pk=RoomMasterId)
                        Room_master_instance.Room_No = RoomNo
                        Room_master_instance.Bed_No = BedNo
                        Room_master_instance.Ward_Name = Ward_instance
                        Room_master_instance.Floor_Name = Floor_instance
                        Room_master_instance.Block_Name = Block_instance
                        Room_master_instance.Building_Name = Building_instance
                        Room_master_instance.Location_Name = Location_instance
                        Room_master_instance.save()

                return JsonResponse({'success': 'Room Master Detials Updated successfully'})
            else:
                # Validate uniqueness of Room Master Details
                if Room_Master_Detials.objects.filter(
                    Room_No=RoomNo,
                    Bed_No=BedNo,
                    Location_Name=Location_instance,
                    Building_Name=Building_instance,
                    Block_Name=Block_instance,
                    Floor_Name=Floor_instance
                ).exists():
                    return JsonResponse({'warn': f"The Room Master Detials are already present in the name of {RoomNo} and {BedNo}."})
                else:
                    # Create a new Room Master instance
                    Room_master_instance = Room_Master_Detials(
                        Room_No=RoomNo,
                        Bed_No=BedNo,
                        Ward_Name=Ward_instance,
                        Floor_Name=Floor_instance,
                        Block_Name=Block_instance,
                        Building_Name=Building_instance,
                        Location_Name=Location_instance,
                        created_by=created_by
                    )
                    Room_master_instance.save()
                    return JsonResponse({'success': 'Room Master Detials added successfully'})

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
        
        
    elif request.method == 'GET':
        try:
            # Fetch all records from the LocationName model
            Room_master_instance = Room_Master_Detials.objects.all().order_by(
                'Location_Name__Location_Name',
                'Building_Name__Building_Name',
                'Block_Name__Block_Name',
                'Floor_Name__Floor_Name',
                'Ward_Name__Ward_Name',
                # '-Room_Name__Room_Name',
                'Room_No',
                'Bed_No',
                )
            
            # Construct a list of dictionaries containing location data
            Room_Master_data = []
            for Roommaster in Room_master_instance:
                RoomMaster_dict = {
                    'id': Roommaster.Room_Id,
                    'RoomNo': Roommaster.Room_No,
                    'BedNo': Roommaster.Bed_No,
                    'RoomId': Roommaster.Room_Id,
                    # 'RoomName': Roommaster.Room_Name.Room_Name,
                    'BedCharge': Roommaster.Ward_Name.Current_Charge,
                    'GST': Roommaster.Ward_Name.GST_Charge,
                    'TotalCharge': Roommaster.Ward_Name.Total_Current_Charge,
                    'WardId': Roommaster.Ward_Name.Ward_Name.Ward_Id,
                    'WardName': Roommaster.Ward_Name.Ward_Name.Ward_Name,
                    'FloorId': Roommaster.Floor_Name.Floor_Id,
                    'FloorName': Roommaster.Floor_Name.Floor_Name,
                    'BlockId': Roommaster.Block_Name.Block_Id,
                    'BlockName': Roommaster.Block_Name.Block_Name,
                    'BuildingId': Roommaster.Building_Name.Building_Id,
                    'BuildingName': Roommaster.Building_Name.Building_Name,
                    'LocationName': Roommaster.Location_Name.Location_Name,
                    'LocationId': Roommaster.Location_Name.Location_Id,
                    'Status': 'Active' if Roommaster.Status else 'Inactive',
                    'created_by': Roommaster.created_by,
                    
                }
                Room_Master_data.append(RoomMaster_dict)

            return JsonResponse(Room_Master_data, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)





def get_RoomNo_Data_by_Building_block_Floor_ward_Room_loc(request):
    try:
        Room = request.GET.get('Room')
        Room_ins =None
        if not Room:
            return JsonResponse({'error':'Room are required'})
        
        Room_ins = RoomType_Master_Detials.objects.get(Room_Id=Room)
        
        if not Room_Master_Detials.objects.filter(
            Status=True,
            Building_Name=Room_ins.Building_Name,
            Block_Name=Room_ins.Block_Name,
            Floor_Name=Room_ins.Floor_Name,
            Ward_Name=Room_ins.Ward_Name,
            Location_Name=Room_ins.Location_Name,
            Room_Name=Room_ins
        ).exists():
            return JsonResponse({'error':'Data not found'})
        
        
        # Fetch all records from the Room_Master_Detials model
        RoomType_Master = Room_Master_Detials.objects.filter(
            Status=True,
            Building_Name=Room_ins.Building_Name,
            Block_Name=Room_ins.Block_Name,
            Floor_Name=Room_ins.Floor_Name,
            Ward_Name=Room_ins.Ward_Name,
            Location_Name=Room_ins.Location_Name,
            Room_Name=Room_ins
        ).values('Room_No').distinct()  # Ensure distinct room numbers

        # Construct a list of dictionaries containing location data
        RoomType_Master_data = []
        index = 0
        for room in RoomType_Master:
            room_dict = {
                'id': index + 1,
                'RoomNo': room['Room_No'], 
            }
            RoomType_Master_data.append(room_dict)
            index += 1

        return JsonResponse(RoomType_Master_data, safe=False)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'An internal server error occurred'}, status=500)





def get_BedNo_Data_by_Building_block_Floor_ward_RoomNo_loc(request):
    try:
        Room = request.GET.get('Room')
        RoomNo = request.GET.get('RoomNo')
        
        Room_ins =None
        if not Room and not RoomNo:
            return JsonResponse({'error':'Room are required'})
        
        Room_ins = RoomType_Master_Detials.objects.get(Room_Id=Room)
        
        if not Room_Master_Detials.objects.filter(
            Status=True,
            Building_Name=Room_ins.Building_Name,
            Block_Name=Room_ins.Block_Name,
            Floor_Name=Room_ins.Floor_Name,
            Ward_Name=Room_ins.Ward_Name,
            Location_Name=Room_ins.Location_Name,
            Room_Name=Room_ins,
            Room_No=RoomNo
        ).exists():
            return JsonResponse({'error':'Data not found'})
        
        
        # Fetch all records from the Room_Master_Detials model
        RoomType_Master = Room_Master_Detials.objects.filter(
            Status=True,
            Building_Name=Room_ins.Building_Name,
            Block_Name=Room_ins.Block_Name,
            Floor_Name=Room_ins.Floor_Name,
            Ward_Name=Room_ins.Ward_Name,
            Location_Name=Room_ins.Location_Name,
            Room_Name=Room_ins,
            Room_No=RoomNo,
        ).exclude(Booking_Status = 'Occupied') 
        print('RoomType_Master',RoomType_Master)
       
        RoomType_Master_data = []
        index = 0
        for room in RoomType_Master:
            room_dict = {
                'id': index + 1,
                'BedNo': room.Bed_No, 
                'RoomId':room.Room_Id
            }
            RoomType_Master_data.append(room_dict)
            index += 1

        return JsonResponse(RoomType_Master_data, safe=False)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'An internal server error occurred'}, status=500)



def get_Room_Master_Data(request):
    try:
        Location = request.GET.get('location')
        status = request.GET.get('status')
        wardtype = request.GET.get('wardtype')
        print('111111111',Location,status,wardtype)
        if not Location or not status:
            return JsonResponse({'error': 'Location and status parameter is missing'}, status=400)
        
        Room_master_instances=None
        if status=='Total':
            Room_master_instances = Room_Master_Detials.objects.filter(Location_Name__pk=Location).order_by('Booking_Status','-Status')
            if wardtype :
                ward, room = wardtype.split(" - ")
                Room_master_instances = Room_Master_Detials.objects.filter(Location_Name__pk=Location,Ward_Name__Ward_Name__Ward_Name=ward).order_by('Booking_Status','-Status')
            
        elif status=='InActive':
            Room_master_instances = Room_Master_Detials.objects.filter(Location_Name__pk=Location,Status=False)
            if wardtype :
                ward, room = wardtype.split(" - ")
                Room_master_instances = Room_Master_Detials.objects.filter(Location_Name__pk=Location,Ward_Name__Ward_Name__Ward_Name=ward,Status=False)
            
        else:
            Room_master_instances = Room_Master_Detials.objects.filter(Location_Name__pk=Location,Status=True,Booking_Status=status)
            if wardtype :
                ward, room = wardtype.split(" - ")
                print( ward, room)
                Room_master_instances = Room_Master_Detials.objects.filter(Location_Name__pk=Location,Ward_Name__Ward_Name__Ward_Name=ward,Status=True,Booking_Status=status)
            
            
        Room_Master_data = []
        if Room_master_instances:
            for Roommaster in Room_master_instances:
                admission_details = None
                if  Roommaster.Booking_Status in  ['Booked','Occupied','Requested'] :
                  admission_details = Patient_Admission_Room_Detials.objects.filter(
                        RoomId__pk=Roommaster.pk
                    ).filter(
                        Q(IP_Registration_Id__Booking_Status=Roommaster.Booking_Status) if Patient_Admission_Room_Detials.objects.filter(RoomId=Roommaster).values_list('RegisterType', flat=True).order_by('-created_by').first() == 'IP' 
                        else Q(Casuality_Registration_Id__Booking_Status=Roommaster.Booking_Status)
                    ).order_by('-created_by').first()
                    
                patient_data = {}
                if admission_details:
                    if admission_details.IP_Registration_Id:
                        dat = admission_details.IP_Registration_Id
                        # Dynamically determine the correct field to filter by based on the registration type
                        if admission_details.RegisterType == 'IP':
                            admiss_Det = get_object_or_404(Patient_Admission_Detials, IP_Registration_Id=dat)
                       
                        patient_data['IsCasualityPatient'] = admiss_Det.IsCasualityPatient
                        patient_data['Casuality_Registration_Id'] = admiss_Det.Casuality_Registration_Id
                        patient_data['AdmissionPurpose'] = admiss_Det.AdmissionPurpose
                        patient_data['Admitdate'] = admission_details.Admitted_Date
                        patient_data['PatientID'] = dat.PatientId.PatientId if dat.PatientId else None
                        patient_data['Age'] = dat.PatientId.Age if dat.PatientId else None
                        patient_data['PhoneNo'] = dat.PatientId.PhoneNo if dat.PatientId else None
                        patient_data['attenders'] = admiss_Det.NextToKinName
                        patient_data['attenderPhoneNo'] = admiss_Det.RelativePhoneNo
                        patient_data['PatientName'] = f"{dat.PatientId.Title.Title_Name}.{dat.PatientId.FirstName} {dat.PatientId.MiddleName} {dat.PatientId.SurName}" if dat.PatientId else None
                    

                RoomMaster_dict = {
                    'id': Roommaster.Room_Id,
                    'RoomNo': Roommaster.Room_No,
                    'BedNo': Roommaster.Bed_No,
                    'RoomId': Roommaster.Ward_Name.Room_Id,
                    'BedCharge': Roommaster.Ward_Name.Current_Charge,
                    'GST': Roommaster.Ward_Name.GST_Charge,
                    'TotalCharge': Roommaster.Ward_Name.Total_Current_Charge,
                    'WardId': Roommaster.Ward_Name.Ward_Name.Ward_Id,
                    'WardName': Roommaster.Ward_Name.Ward_Name.Ward_Name,
                    'FloorId': Roommaster.Floor_Name.Floor_Id,
                    'FloorName': Roommaster.Floor_Name.Floor_Name,
                    'BlockId': Roommaster.Block_Name.Block_Id,
                    'BlockName': Roommaster.Block_Name.Block_Name,
                    'BuildingId': Roommaster.Building_Name.Building_Id,
                    'BuildingName': Roommaster.Building_Name.Building_Name,
                    'LocationName': Roommaster.Location_Name.Location_Name,
                    'LocationId': Roommaster.Location_Name.Location_Id,
                    'Status': 'Active' if Roommaster.Status else 'Inactive',
                    'BookingStatus': Roommaster.Booking_Status,
                    'created_by': Roommaster.created_by,
                }

                RoomMaster_dict.update(patient_data)
                Room_Master_data.append(RoomMaster_dict)

        return JsonResponse(Room_Master_data, safe=False)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'An internal server error occurred'}, status=500)



@csrf_exempt
def get_room_count_data_total(request):
    try:
        if request.method == 'GET':
            location = request.GET.get('Location')
            
            if not location:
                return JsonResponse({'error': 'Location is required'}, status=400)
            
            # Default statuses
            default_statuses = ['Available', 'Requested', 'Booked', 'Occupied', 'Maintenance']
            
            # Initialize a dictionary to hold the total counts and room data
            formatted_data = {
                'totalcount': {
                    'Total': 0,
                    'InActive': 0,
                    **{status: 0 for status in default_statuses}
                },
                'totaldata': []
            }
            
            # Query to get distinct Ward_Type and Room_name
            distinct_ward_rooms = Room_Master_Detials.objects.filter(Location_Name__pk=location).values('Ward_Name__Ward_Name').distinct()
            index = 1
            print('dissssss', distinct_ward_rooms)
            for ward_room in distinct_ward_rooms:
                # Corrected field reference
                room_name = f"{ward_room['Ward_Name__Ward_Name']}"
                
                # Total count for the room
                total_count = Room_Master_Detials.objects.filter(
                    Location_Name__pk=location,
                    Ward_Name__Ward_Name=ward_room['Ward_Name__Ward_Name']
                ).count()
                total_inactive_count = Room_Master_Detials.objects.filter(
                    Location_Name__pk=location,
                    Ward_Name__Ward_Name=ward_room['Ward_Name__Ward_Name'],
                    Status=False
                ).count()

                # Initialize room data with default statuses
                room_data = {
                    "id": index,
                    "roomname": room_name,
                    "Total": total_count,
                    'InActive': total_inactive_count,
                    **{status: 0 for status in default_statuses}  # Initialize default statuses
                }

                # Count occurrences of each status for the room
                for status in default_statuses:
                    count_status = Room_Master_Detials.objects.filter(
                        Location_Name__pk=location,
                        Ward_Name__Ward_Name=ward_room['Ward_Name__Ward_Name'],
                        Booking_Status=status,
                        Status=True
                    ).count()
                    room_data[status] = count_status
                    
                    # Update the total counts for the entire location
                    formatted_data['totalcount'][status] += count_status

                # Append the total count for the room to the overall total count
                formatted_data['totalcount']['Total'] += total_count
                formatted_data['totalcount']['InActive'] += total_inactive_count

                # Append formatted room data to the list
                formatted_data['totaldata'].append(room_data)
                index += 1

            return JsonResponse(formatted_data, safe=False)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'An internal server error occurred'}, status=500)




# def get_Room_Master_Data_for_registration(request):
#     try:
#         Location = request.GET.get('location')
#         RegisterType = request.GET.get('RegisterType')
#         Building = request.GET.get('Building')
#         Block = request.GET.get('Block',"")
#         Floor = request.GET.get('Floor',"")
#         Ward = request.GET.get('Ward',"")
#         # Room = request.GET.get('Room',"")
#         print('111111111111',Block, RegisterType)
        
#         filter_kwargs = {
#             'Location_Name__pk': Location,
#             'Status': True,
#             'Booking_Status': 'Available',
#         }

#         # Add the non-empty fields to the filter kwargs
#         if Building:
#             filter_kwargs['Building_Name__pk'] = Building
#         if Block:
#             filter_kwargs['Block_Name__pk'] = Block
#         if Floor:
#             filter_kwargs['Floor_Name__pk'] = Floor
#         if Ward:
#             filter_kwargs['Ward_Name__pk'] = Ward
#         print('22222222')

#         # if Room:
#         #     filter_kwargs['Room_Name__pk'] = Room
#         if RegisterType == 'Casuality':
#             filter_kwargs['Ward_Name__Ward_Name'] = 'CASUALITY'
#         Room_master_instances = None
#         print('kaawwwggg',filter_kwargs)
#         if RegisterType == 'IP':
#             Room_master_instances = Room_Master_Detials.objects.filter(**filter_kwargs).exclude(Ward_Name__Ward_Name__Ward_Name__in=['CASUALITY', 'OT'])
#         elif RegisterType == 'Emergency':
#             Room_master_instances = Room_Master_Detials.objects.filter(**filter_kwargs).exclude(Ward_Name__Ward_Name__Ward_Name__in=['GENERAL', 'OT','ICU'])
 
#         else:
#             Room_master_instances = Room_Master_Detials.objects.filter(**filter_kwargs)
            
#         print('22222222')
#         Room_Master_data = []
        
#         if Room_master_instances:
#             for Roommaster in Room_master_instances:
                

#                 RoomMaster_dict = {
#                     'id': Roommaster.Room_Id,
#                     'RoomNo': Roommaster.Room_No,
#                     'BedNo': Roommaster.Bed_No,
#                     'RoomId': Roommaster.Ward_Name.Room_Id,
#                     'BedCharge': Roommaster.Ward_Name.Current_Charge,
#                     'GST': Roommaster.Ward_Name.GST_Charge,
#                     'TotalCharge': Roommaster.Ward_Name.Total_Current_Charge,
#                     'WardId': Roommaster.Ward_Name.Ward_Name.Ward_Id,
#                     'WardName': Roommaster.Ward_Name.Ward_Name.Ward_Name,
#                     'FloorId': Roommaster.Floor_Name.Floor_Id,
#                     'FloorName': Roommaster.Floor_Name.Floor_Name,
#                     'BlockId': Roommaster.Block_Name.Block_Id,
#                     'BlockName': Roommaster.Block_Name.Block_Name,
#                     'BuildingId': Roommaster.Building_Name.Building_Id,
#                     'BuildingName': Roommaster.Building_Name.Building_Name,
#                     'LocationName': Roommaster.Location_Name.Location_Name,
#                     'LocationId': Roommaster.Location_Name.Location_Id,
#                     'Status': 'Active' if Roommaster.Status else 'Inactive',
#                     'BookingStatus': Roommaster.Booking_Status,
#                     'created_by': Roommaster.created_by,
#                 }

              
#                 Room_Master_data.append(RoomMaster_dict)

#         return JsonResponse(Room_Master_data, safe=False)

#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         return JsonResponse({'error': 'An internal server error occurred'}, status=500)

def get_Room_Master_Data_for_registration(request):
    try:
        # Extract query parameters
        Location = request.GET.get('location')
        RegisterType = request.GET.get('RegisterType')
        Building = request.GET.get('Building')
        Block = request.GET.get('Block')
        Floor = request.GET.get('Floor')
        Ward = request.GET.get('Ward')

        print('Filter inputs:', Block, RegisterType)

        # Base filter conditions
        filter_kwargs = Q(Status=True, Booking_Status='Available')

        if Location:
            filter_kwargs &= Q(Location_Name__Location_Id=Location)
        print(filter_kwargs,'filter_kwargs11111')
        
        if Building:
            filter_kwargs &= Q(Building_Name__Building_Id=Building)
        print(filter_kwargs,'filter_kwargs222222')
        
        if Block:
            filter_kwargs &= Q(Block_Name__Block_Id=Block)
        print(filter_kwargs,'filter_kwargs33333')
        
        if Floor:
            filter_kwargs &= Q(Floor_Name__Floor_Id=Floor)
        print(filter_kwargs,'filter_kwargs44444')
        
        if Ward:
            filter_kwargs &= Q(Ward_Name__Ward_Name__Ward_Id=Ward)
        
        print(filter_kwargs,'filter_kwargs5555555')


        # Special filtering based on RegisterType
        # if RegisterType == 'Emergency':
        #     filter_kwargs &= Q(Ward_Name__Ward_Name='CASUALITY')
        if RegisterType == 'Emergency':
            casualty_ward_ids = WardType_Master_Detials.objects.filter(Ward_Name__in=['CASUALITY']).values_list('Ward_Id', flat=True)
            filter_kwargs &= Q(Ward_Name__Ward_Name__in=casualty_ward_ids)

        if RegisterType == 'IP':
            exclude_ward_ids = WardType_Master_Detials.objects.exclude(Ward_Name__in=['CASUALITY', 'OT']).values_list('Ward_Id', flat=True)
            filter_kwargs &= Q(Ward_Name__Ward_Name__in=exclude_ward_ids)
        
        print('Final filter:', filter_kwargs)

        # Fetch filtered room data
        Room_master_instances = Room_Master_Detials.objects.filter(filter_kwargs)
        
        print('Room_master_instances----??',Room_master_instances)
        # Convert queryset to JSON response
        Room_Master_data = [
            {
                'id': room.Room_Id,
                'RoomNo': room.Room_No,
                'BedNo': room.Bed_No,
                'RoomId': room.Ward_Name.Room_Id,
                'BedCharge': room.Ward_Name.Current_Charge,
                'GST': room.Ward_Name.GST_Charge,
                'TotalCharge': room.Ward_Name.Total_Current_Charge,
                'WardId': room.Ward_Name.Ward_Name.Ward_Id,
                'WardName': room.Ward_Name.Ward_Name.Ward_Name,
                'FloorId': room.Floor_Name.Floor_Id,
                'FloorName': room.Floor_Name.Floor_Name,
                'BlockId': room.Block_Name.Block_Id,
                'BlockName': room.Block_Name.Block_Name,
                'BuildingId': room.Building_Name.Building_Id,
                'BuildingName': room.Building_Name.Building_Name,
                'LocationName': room.Location_Name.Location_Name,
                'LocationId': room.Location_Name.Location_Id,
                'Status': 'Active' if room.Status else 'Inactive',
                'BookingStatus': room.Booking_Status,
                'created_by': room.created_by,
            }
            for room in Room_master_instances
        ]
        
        print(Room_Master_data,'Room_Master_data')
        return JsonResponse(Room_Master_data, safe=False)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'An internal server error occurred'}, status=500)



# def get_filter_Data_for_registration(request):
#     try:
#         Location = request.GET.get('location')
#         RegisterType = request.GET.get('RegisterType')
        
#         data={
#             'Building':[],
#             'Block':[],
#             'Floor':[],
#             'Ward':[],
#             # 'Room':[],
#         }
#         for buil in Building_Master_Detials.objects.filter(Location_Name__pk = Location ,Status=True):
#             data['Building'].append({'id':buil.pk,'Name':buil.Building_Name})
#         for block in Block_Master_Detials.objects.filter(Location_Name__pk = Location ,Status=True):
#             data['Block'].append({'id':block.pk,'Name':block.Block_Name})
#         for floor in Floor_Master_Detials.objects.filter(Location_Name__pk = Location ,Status=True):
#             data['Floor'].append({'id':floor.pk,'Name':floor.Floor_Name})
        
#         if RegisterType=='IP':
#             for ward in WardType_Master_Detials.objects.filter(Location_Name__pk = Location ,Status=True).exclude(Ward_Name__in=['CASUALITY', 'OT']):
#                 data['Ward'].append({'id':ward.pk,'Name':ward.Ward_Name})
#             # for room in RoomType_Master_Detials.objects.filter(Location_Name__pk = Location ,Status=True).exclude(Ward_Name__Ward_Name__in=['CASUALITY', 'OT']):
#                 # data['Room'].append({'id':room.pk,'Name':room.Room_Name})
#         else:
#             for ward in WardType_Master_Detials.objects.filter(Location_Name__pk = Location ,Status=True,Ward_Name='CASUALITY'):
#                 data['Ward'].append({'id':ward.pk,'Name':ward.Ward_Name})
#             # for room in RoomType_Master_Detials.objects.filter(Location_Name__pk = Location ,Status=True,Ward_Name__Ward_Name='CASUALITY'):
#             #     data['Room'].append({'id':room.pk,'Name':room.Room_Name})

      
#         return JsonResponse(data)

#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         return JsonResponse({'error': 'An internal server error occurred'}, status=500)



def get_filter_Data_for_registration(request):
    try:
        Location = request.GET.get('location')
        RegisterType = request.GET.get('RegisterType')
        Building=request.GET.get('Building')
        Block=request.GET.get('Block')
        Floor=request.GET.get('Floor')
        Ward=request.GET.get('Ward')


        print('8877-0099---1111',RegisterType,Building,Block,Floor,Ward)

        data={
            'Building':[],
            'Block':[],
            'Floor':[],
            'Ward':[],
        }
        for buil in Building_Master_Detials.objects.filter(Location_Name__pk = Location ,Status=True):
            data['Building'].append({'id':buil.pk,'Name':buil.Building_Name})
        if Building:
            for block in Block_Master_Detials.objects.filter(Location_Name__pk = Location ,Building_Name__Building_Id =Building, Status=True):
                data['Block'].append({'id':block.pk,'Name':block.Block_Name})
        if Block:
            for floor in Floor_Master_Detials.objects.filter(Location_Name__pk = Location ,Block_Name__Block_Id=Block,Status=True):
                data['Floor'].append({'id':floor.pk,'Name':floor.Floor_Name})
        
        if RegisterType=='IP':
            if Floor:
                for ward in WardType_Master_Detials.objects.filter(Location_Name__pk = Location ,Floor_Name__Floor_Id = Floor, Status=True).exclude(Ward_Name__in=['CASUALITY', 'OT']):
                    data['Ward'].append({'id':ward.pk,'Name':ward.Ward_Name})
            # for room in RoomType_Master_Detials.objects.filter(Location_Name__pk = Location ,Status=True).exclude(Ward_Name__Ward_Name__in=['CASUALITY', 'OT']):
                # data['Room'].append({'id':room.pk,'Name':room.Room_Name})
        else:
            if Floor:
                for ward in WardType_Master_Detials.objects.filter(Location_Name__pk = Location ,Floor_Name__Floor_Id = Floor,Status=True,Ward_Name='CASUALITY'):
                    data['Ward'].append({'id':ward.pk,'Name':ward.Ward_Name})
            # for room in RoomType_Master_Detials.objects.filter(Location_Name__pk = Location ,Status=True,Ward_Name__Ward_Name='CASUALITY'):
            #     data['Room'].append({'id':room.pk,'Name':room.Room_Name})

        print(data,'dataaaaaaaaaaaaa')
        return JsonResponse(data)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'An internal server error occurred'}, status=500)




# -----------------------------------Invvvvv-------------------------------------



# ward name
# @csrf_exempt   
# @require_http_methods(["POST","OPTIONS","GET"])
# def Inventory_Master_Detials_link(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
            
#             # Extract and validate data
#             StoreId = data.get('StoreId', '')
#             StoreName = data.get('StoreName', '')
#             StoreType = data.get('StoreType', '')
#             FloorName = data.get('FloorName', '')
#             BlockName = data.get('BlockName', '')
#             BuildingName = data.get('BuildingName', '')
#             Location = data.get('Location', '')
#             Statusedit = data.get('Statusedit', False)
#             created_by = data.get('created_by', '')
#             approvalConditions = data.get('approvalConditions', [])

#             # Print to check received conditions
#             print('approvalConditions', approvalConditions)

#             # Fetch related instances
#             Location_instance = Location_Detials.objects.get(Location_Id=Location) if Location else None
#             Building_instance = Building_Master_Detials.objects.get(Building_Id=BuildingName) if BuildingName else None
#             Block_instance = Block_Master_Detials.objects.get(Block_Id=BlockName) if BlockName else None
#             Floor_instance = Floor_Master_Detials.objects.get(Floor_Id=FloorName) if FloorName else None

#             # Update Store Details
#             if StoreId:
#                 Inventory_Location_instance = Inventory_Location_Master_Detials.objects.get(pk=StoreId)

#                 if Statusedit:
#                     # Toggle Status
#                     Inventory_Location_instance.Status = not Inventory_Location_instance.Status
#                     Inventory_Location_instance.save()
#                     return JsonResponse({'success': "Store Name status updated successfully."})

#                 else:
#                     if Inventory_Location_Master_Detials.objects.filter(Store_Name=StoreName).exclude(pk=StoreId).exists():
#                         return JsonResponse({'warn': f"The Store Name Detials are already present in the name of {StoreName}."})
                    
#                     if StoreType == 'CENTRALSTORE' and Inventory_Location_Master_Detials.objects.filter(Store_Type=StoreType).exclude(pk=StoreId).exists():
#                         return JsonResponse({'warn': f"A Central Store already exists. Cannot add another Central Store with the name '{StoreName}'."})
                    
#                     # Update store details
#                     Inventory_Location_instance.Store_Name = StoreName
#                     Inventory_Location_instance.Store_Type = StoreType
#                     Inventory_Location_instance.Floor_Name = Floor_instance
#                     Inventory_Location_instance.Block_Name = Block_instance
#                     Inventory_Location_instance.Building_Name = Building_instance
#                     Inventory_Location_instance.Location_Name = Location_instance
#                     Inventory_Location_instance.save()

#                     # Handle approval conditions
#                     Inventory_Page_Access_Detailes.objects.filter(Access_StoreId=Inventory_Location_instance).delete()  # Clear existing access

#                     for condition in approvalConditions:
                                    
#                         if condition['id'] == 'PurchaseOrder' :
#                             get_IS_PurchaseOrder = condition['exists']
#                             get_IS_PurchaseOrder_Approve =  condition['additionalOptions'][0]['checked']

                        
#                         if condition['id'] == 'GoodsReceivedNote' :
#                             get_IS_GRN = condition['exists']
#                             get_IS_GRN_Approve = condition['additionalOptions'][0]['checked']

#                         if condition['id'] == 'QuickGoodsReceivedNote' :
#                             get_IS_Quick_GRN = condition['exists']
#                             get_IS_Quick_GRN_Approve = condition['additionalOptions'][0]['checked']

#                         if condition['id'] == 'PurchaseReturn' :
#                             get_IS_Purchase_Return = condition['exists']
#                             get_IS_Purchase_Return_Approve =  condition['additionalOptions'][0]['checked']

#                         if condition['id'] == 'Indent' :
#                             get_IS_Indent = condition['exists']
#                             get_IS_Indent_Raise_Approve = condition['additionalOptions'][0]['checked']
#                             get_IS_Indent_Issue_Approve = condition['additionalOptions'][1]['checked']
#                             get_IS_Indent_Receive_Approve = condition['additionalOptions'][2]['checked']
#                             get_IS_Indent_Return_Approve = condition['additionalOptions'][3]['checked']
                            


#                     Inventory_Page_Access_Detailes.objects.create(
#                         Access_StoreId=Inventory_Location_instance,
#                         IS_PurchaseOrder=get_IS_PurchaseOrder,
#                         IS_PurchaseOrder_Approve=get_IS_PurchaseOrder_Approve,
#                         IS_GRN=get_IS_GRN,
#                         IS_GRN_Approve=get_IS_GRN_Approve,
#                         IS_Quick_GRN=get_IS_Quick_GRN,
#                         IS_Quick_GRN_Approve=get_IS_Quick_GRN_Approve,
#                         IS_Purchase_Return=get_IS_Purchase_Return,
#                         IS_Purchase_Return_Approve=get_IS_Purchase_Return_Approve,
#                         IS_Indent=get_IS_Indent,
#                         IS_Indent_Raise_Approve=get_IS_Indent_Raise_Approve,
#                         IS_Indent_Issue_Approve=get_IS_Indent_Issue_Approve,
#                         IS_Indent_Receive_Approve=get_IS_Indent_Receive_Approve,
#                         IS_Indent_Return_Approve=get_IS_Indent_Return_Approve,
#                         updated_by=created_by
#                     )

#                     return JsonResponse({'success': 'Store Name and Approval Conditions updated successfully.'})

#             else:
#                 # Add new store
#                 if Inventory_Location_Master_Detials.objects.filter(Store_Name=StoreName).exists():
#                     return JsonResponse({'warn': f"The Store Name Detials are already present in the name of {StoreName}."})

#                 if StoreType == 'CENTRALSTORE' and Inventory_Location_Master_Detials.objects.filter(Store_Type=StoreType).exists():
#                     return JsonResponse({'warn': f"A Central Store already exists. Cannot add another Central Store with the name '{StoreName}'."})
                
#                 Inventory_Location_instance = Inventory_Location_Master_Detials(
#                     Store_Name=StoreName,
#                     Store_Type=StoreType,
#                     Floor_Name=Floor_instance,
#                     Block_Name=Block_instance,
#                     Building_Name=Building_instance,
#                     Location_Name=Location_instance,
#                     created_by=created_by
#                 )
#                 Inventory_Location_instance.save()

#                 for condition in approvalConditions:
                                    
#                         if condition['id'] == 'PurchaseOrder' :
#                             get_IS_PurchaseOrder = condition['exists']
#                             get_IS_PurchaseOrder_Approve =  condition['additionalOptions'][0]['checked']

                        
#                         if condition['id'] == 'GoodsReceivedNote' :
#                             get_IS_GRN = condition['exists']
#                             get_IS_GRN_Approve = condition['additionalOptions'][0]['checked']

#                         if condition['id'] == 'QuickGoodsReceivedNote' :
#                             get_IS_Quick_GRN = condition['exists']
#                             get_IS_Quick_GRN_Approve = condition['additionalOptions'][0]['checked']

#                         if condition['id'] == 'PurchaseReturn' :
#                             get_IS_Purchase_Return = condition['exists']
#                             get_IS_Purchase_Return_Approve =  condition['additionalOptions'][0]['checked']

#                         if condition['id'] == 'Indent' :
#                             get_IS_Indent = condition['exists']
#                             get_IS_Indent_Raise_Approve = condition['additionalOptions'][0]['checked']
#                             get_IS_Indent_Issue_Approve = condition['additionalOptions'][1]['checked']
#                             get_IS_Indent_Receive_Approve = condition['additionalOptions'][2]['checked']
#                             get_IS_Indent_Return_Approve = condition['additionalOptions'][3]['checked']


#                 Inventory_Page_Access_Detailes.objects.create(
#                         Access_StoreId=Inventory_Location_instance,
#                         IS_PurchaseOrder=get_IS_PurchaseOrder,
#                         IS_PurchaseOrder_Approve=get_IS_PurchaseOrder_Approve,
#                         IS_GRN=get_IS_GRN,
#                         IS_GRN_Approve=get_IS_GRN_Approve,
#                         IS_Quick_GRN=get_IS_Quick_GRN,
#                         IS_Quick_GRN_Approve=get_IS_Quick_GRN_Approve,
#                         IS_Purchase_Return=get_IS_Purchase_Return,
#                         IS_Purchase_Return_Approve=get_IS_Purchase_Return_Approve,
#                         IS_Indent=get_IS_Indent,
#                         IS_Indent_Raise_Approve=get_IS_Indent_Raise_Approve,
#                         IS_Indent_Issue_Approve=get_IS_Indent_Issue_Approve,
#                         IS_Indent_Receive_Approve=get_IS_Indent_Receive_Approve,
#                         IS_Indent_Return_Approve=get_IS_Indent_Return_Approve,
#                         created_by=created_by
#                     )              

#                 return JsonResponse({'success': 'Store Name and Approval Conditions added successfully.'})

#         except Exception as e:
#             print(f"An error occurred: {str(e)}")
#             return JsonResponse({'error': 'An internal server error occurred'}, status=500)  
    
#     elif request.method == 'GET':
#         try:
#             SearchLocation = request.GET.get('SearchLocation')
#             forquickgrn = bool(request.GET.get('forquickgrn', False))

#             Inventory_Location_Master = Inventory_Location_Master_Detials.objects.all()
#             if SearchLocation:
#                 Inventory_Location_Master = Inventory_Location_Master.filter(Location_Name__Location_Id=SearchLocation, Status=True)

#             INLO_Master_data = []
#             for Floor in Inventory_Location_Master:
#                 Floor_dict = {
#                     'id': Floor.Store_Id,
#                     'StoreName': Floor.Store_Name,
#                     'StoreType': Floor.Store_Type,
#                     'FloorId': Floor.Floor_Name.Floor_Id if Floor.Floor_Name else None,
#                     'FloorName': Floor.Floor_Name.Floor_Name if Floor.Floor_Name else None,
#                     'BlockId': Floor.Block_Name.Block_Id if Floor.Block_Name else None,
#                     'BlockName': Floor.Block_Name.Block_Name if Floor.Block_Name else None,
#                     'BuildingId': Floor.Building_Name.Building_Id if Floor.Building_Name else None,
#                     'BuildingName': Floor.Building_Name.Building_Name if Floor.Building_Name else None,
#                     'Location_Name': Floor.Location_Name.Location_Name if Floor.Location_Name else None,
#                     'Location_Id': Floor.Location_Name.Location_Id if Floor.Location_Name else None,
#                     'Status': 'Active' if Floor.Status else 'Inactive',
#                     'created_by': Floor.created_by
#                 }

#                 # Fetch approval conditions for the current store
#                 approval_conditions = Inventory_Page_Access_Detailes.objects.filter(Access_StoreId=Floor.Store_Id).first()

#                 # Define default approval conditions structure
#                 approvalConditions = [
#                     {
#                         'id': 'PurchaseOrder',
#                         'label': 'Purchase Order',
#                         'exists': approval_conditions.IS_PurchaseOrder if approval_conditions else False,
#                         'additionalOptions': [
#                             {'id': 'PurchaseOrderApprove', 'label': 'Purchase Order Approve', 'checked': approval_conditions.IS_PurchaseOrder_Approve if approval_conditions else False}
#                         ]
#                     },
#                     {
#                         'id': 'GoodsReceivedNote',
#                         'label': 'Goods Received Note',
#                         'exists': approval_conditions.IS_GRN if approval_conditions else False,
#                         'additionalOptions': [
#                             {'id': 'GoodsReceivedNoteApprove', 'label': 'Goods Received Note Approve', 'checked': approval_conditions.IS_GRN_Approve if approval_conditions else False}
#                         ]
#                     },
#                     {
#                         'id': 'QuickGoodsReceivedNote',
#                         'label': 'Quick Goods Received Note',
#                         'exists': approval_conditions.IS_Quick_GRN if approval_conditions else False,
#                         'additionalOptions': [
#                             {'id': 'QuickGoodsReceivedNoteApprove', 'label': 'Quick Goods Received Note Approve', 'checked': approval_conditions.IS_Quick_GRN_Approve if approval_conditions else False}
#                         ]
#                     },
#                     {
#                         'id': 'PurchaseReturn',
#                         'label': 'Purchase Return',
#                         'exists': approval_conditions.IS_Purchase_Return if approval_conditions else False,
#                         'additionalOptions': [
#                             {'id': 'PurchaseReturnApprove', 'label': 'Purchase Return Approve', 'checked': approval_conditions.IS_Purchase_Return_Approve if approval_conditions else False}
#                         ]
#                     },
#                     {
#                         'id': 'Indent',
#                         'label': 'Indent',
#                         'exists': approval_conditions.IS_Indent if approval_conditions else False,
#                         'additionalOptions': [
#                             {'id': 'raiseApprove', 'label': 'Raise Approve', 'checked': approval_conditions.IS_Indent_Raise_Approve if approval_conditions else False},
#                             {'id': 'issueApprove', 'label': 'Issue Approve', 'checked': approval_conditions.IS_Indent_Issue_Approve if approval_conditions else False},
#                             {'id': 'receiveApprove', 'label': 'Receive Approve', 'checked': approval_conditions.IS_Indent_Receive_Approve if approval_conditions else False},
#                             {'id': 'returnApprove', 'label': 'Return Approve', 'checked': approval_conditions.IS_Indent_Return_Approve if approval_conditions else False},
#                         ]
#                     },
#                 ]

#                 Floor_dict['approvalConditions'] = approvalConditions

#                 getSingledata = []

#                 conditions = {
#                     'IS_PurchaseOrder': 'PurchaseOrder',
#                     'IS_PurchaseOrder_Approve': 'PurchaseOrderApprove',
#                     'IS_GRN': 'GoodsReceivedNote',
#                     'IS_GRN_Approve': 'GoodsReceivedNoteApprove',
#                     'IS_Quick_GRN': 'QuickGoodsReceivedNote',
#                     'IS_Quick_GRN_Approve': 'QuickGoodsReceivedNoteApprove',
#                     'IS_Purchase_Return': 'PurchaseReturn',
#                     'IS_Purchase_Return_Approve': 'PurchaseReturnApprove',
#                     'IS_Indent': 'Indent',
#                     'IS_Indent_Raise_Approve': 'IndentRaiseApprove',
#                     'IS_Indent_Issue_Approve': 'IndentIssueApprove',
#                     'IS_Indent_Receive_Approve': 'IndentReceiveApprove',
#                     'IS_Indent_Return_Approve': 'IndentReturnApprove',

#                 }


#                 if approval_conditions:
#                     for condition, label in conditions.items():
#                         if getattr(approval_conditions, condition, False):
#                             getSingledata.append(label)
                
#                 Floor_dict['getSingledata'] =getSingledata
                
#                 INLO_Master_data.append(Floor_dict)

#             return JsonResponse(INLO_Master_data, safe=False)

#         except Exception as e:
#             print(f"An error occurred: {str(e)}")
#             return JsonResponse({'error': 'An internal server error occurred'}, status=500)





@csrf_exempt  
@require_http_methods(["POST","OPTIONS","GET"])
def Inventory_Master_Detials_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
           
            # Extract and validate data
            StoreId = data.get('StoreId', '')
            StoreName = data.get('StoreName', '')
            StoreType = data.get('StoreType', '')
            FloorName = data.get('FloorName', '')
            BlockName = data.get('BlockName', '')
            BuildingName = data.get('BuildingName', '')
            IsPointOfSale=data.get('IsPointOfSale','')
            Location = data.get('Location', '')
            Statusedit = data.get('Statusedit', False)
            created_by = data.get('created_by', '')
            approvalConditions = data.get('approvalConditions', [])
 
            SelectedDepartmentIDs=data.get('SelectedDepartmentIDs')
 
            # Print to check received conditions
            print('SelectedDepartmentIDs', SelectedDepartmentIDs)
 
            # Fetch related instances
            Location_instance = Location_Detials.objects.get(Location_Id=Location) if Location else None
            Building_instance = Building_Master_Detials.objects.get(Building_Id=BuildingName) if BuildingName else None
            Block_instance = Block_Master_Detials.objects.get(Block_Id=BlockName) if BlockName else None
            Floor_instance = Floor_Master_Detials.objects.get(Floor_Id=FloorName) if FloorName else None
 
            # Update Store Details
            if StoreId:
                Inventory_Location_instance = Inventory_Location_Master_Detials.objects.get(pk=StoreId)
 
                if Statusedit:
                    # Toggle Status
                    Inventory_Location_instance.Status = not Inventory_Location_instance.Status
                    Inventory_Location_instance.save()
                    return JsonResponse({'success': "Store Name status updated successfully."})
 
                else:
                    if Inventory_Location_Master_Detials.objects.filter(Store_Name=StoreName).exclude(pk=StoreId).exists():
                        return JsonResponse({'warn': f"The Store Name Detials are already present in the name of {StoreName}."})
                   
                    if StoreType == 'CENTRALSTORE' and Inventory_Location_Master_Detials.objects.filter(Store_Type=StoreType).exclude(pk=StoreId).exists():
                        return JsonResponse({'warn': f"A Central Store already exists. Cannot add another Central Store with the name '{StoreName}'."})
                   
                    # Update store details
                    Inventory_Location_instance.Store_Name = StoreName
                    Inventory_Location_instance.Store_Type = StoreType
                    Inventory_Location_instance.Floor_Name = Floor_instance
                    Inventory_Location_instance.Block_Name = Block_instance
                    Inventory_Location_instance.Building_Name = Building_instance
                    Inventory_Location_instance.Location_Name = Location_instance                    
                    Inventory_Location_instance.IsPointOfSale = IsPointOfSale
 
                    if SelectedDepartmentIDs:
                        Inventory_Location_instance.Departments.set(SelectedDepartmentIDs)
                    else:
                        Inventory_Location_instance.Departments.clear()
 
                    Inventory_Location_instance.save()
 
                    # Handle approval conditions
                    Inventory_Page_Access_Detailes.objects.filter(Access_StoreId=Inventory_Location_instance).delete()  # Clear existing access
 
                    for condition in approvalConditions:
                                   
                        if condition['id'] == 'PurchaseOrder' :
                            get_IS_PurchaseOrder = condition['exists']
                            get_IS_PurchaseOrder_Approve =  condition['additionalOptions'][0]['checked']
 
                       
                        if condition['id'] == 'GoodsReceivedNote' :
                            get_IS_GRN = condition['exists']
                            get_IS_GRN_Approve = condition['additionalOptions'][0]['checked']
 
                        if condition['id'] == 'QuickGoodsReceivedNote' :
                            get_IS_Quick_GRN = condition['exists']
                            get_IS_Quick_GRN_Approve = condition['additionalOptions'][0]['checked']
 
                        if condition['id'] == 'PurchaseReturn' :
                            get_IS_Purchase_Return = condition['exists']
                            get_IS_Purchase_Return_Approve =  condition['additionalOptions'][0]['checked']
 
                        if condition['id'] == 'Indent' :
                            get_IS_Indent = condition['exists']
                            get_IS_Indent_Raise_Approve = condition['additionalOptions'][0]['checked']
                            get_IS_Indent_Issue_Approve = condition['additionalOptions'][1]['checked']
                            get_IS_Indent_Receive_Approve = condition['additionalOptions'][2]['checked']
                            get_IS_Indent_Return_Approve = condition['additionalOptions'][3]['checked']
                           
 
 
                    Inventory_Page_Access_Detailes.objects.create(
                        Access_StoreId=Inventory_Location_instance,
                        IS_PurchaseOrder=get_IS_PurchaseOrder,
                        IS_PurchaseOrder_Approve=get_IS_PurchaseOrder_Approve,
                        IS_GRN=get_IS_GRN,
                        IS_GRN_Approve=get_IS_GRN_Approve,
                        IS_Quick_GRN=get_IS_Quick_GRN,
                        IS_Quick_GRN_Approve=get_IS_Quick_GRN_Approve,
                        IS_Purchase_Return=get_IS_Purchase_Return,
                        IS_Purchase_Return_Approve=get_IS_Purchase_Return_Approve,
                        IS_Indent=get_IS_Indent,
                        IS_Indent_Raise_Approve=get_IS_Indent_Raise_Approve,
                        IS_Indent_Issue_Approve=get_IS_Indent_Issue_Approve,
                        IS_Indent_Receive_Approve=get_IS_Indent_Receive_Approve,
                        IS_Indent_Return_Approve=get_IS_Indent_Return_Approve,
                        updated_by=created_by
                    )
 
                    return JsonResponse({'success': 'Store Name and Approval Conditions updated successfully.'})
 
            else:
                # Add new store
                if Inventory_Location_Master_Detials.objects.filter(Store_Name=StoreName).exists():
                    return JsonResponse({'warn': f"The Store Name Detials are already present in the name of {StoreName}."})
 
                if StoreType == 'CENTRALSTORE' and Inventory_Location_Master_Detials.objects.filter(Store_Type=StoreType).exists():
                    return JsonResponse({'warn': f"A Central Store already exists. Cannot add another Central Store with the name '{StoreName}'."})
               
                Inventory_Location_instance = Inventory_Location_Master_Detials(
                    Store_Name=StoreName,
                    Store_Type=StoreType,
                    Floor_Name=Floor_instance,
                    Block_Name=Block_instance,
                    Building_Name=Building_instance,
                    Location_Name=Location_instance,
                    IsPointOfSale=IsPointOfSale,
                    created_by=created_by
                )
                Inventory_Location_instance.save()  # Save first to generate Store_Id
 
                # Assign departments after saving
                if SelectedDepartmentIDs:
                    Inventory_Location_instance.Departments.set(SelectedDepartmentIDs)  # Now Store_Id exists
 
                # Optionally save again (not required, but safe)
                Inventory_Location_instance.save()
 
                for condition in approvalConditions:
                                   
                        if condition['id'] == 'PurchaseOrder' :
                            get_IS_PurchaseOrder = condition['exists']
                            get_IS_PurchaseOrder_Approve =  condition['additionalOptions'][0]['checked']
 
                       
                        if condition['id'] == 'GoodsReceivedNote' :
                            get_IS_GRN = condition['exists']
                            get_IS_GRN_Approve = condition['additionalOptions'][0]['checked']
 
                        if condition['id'] == 'QuickGoodsReceivedNote' :
                            get_IS_Quick_GRN = condition['exists']
                            get_IS_Quick_GRN_Approve = condition['additionalOptions'][0]['checked']
 
                        if condition['id'] == 'PurchaseReturn' :
                            get_IS_Purchase_Return = condition['exists']
                            get_IS_Purchase_Return_Approve =  condition['additionalOptions'][0]['checked']
 
                        if condition['id'] == 'Indent' :
                            get_IS_Indent = condition['exists']
                            get_IS_Indent_Raise_Approve = condition['additionalOptions'][0]['checked']
                            get_IS_Indent_Issue_Approve = condition['additionalOptions'][1]['checked']
                            get_IS_Indent_Receive_Approve = condition['additionalOptions'][2]['checked']
                            get_IS_Indent_Return_Approve = condition['additionalOptions'][3]['checked']
 
 
                Inventory_Page_Access_Detailes.objects.create(
                        Access_StoreId=Inventory_Location_instance,
                        IS_PurchaseOrder=get_IS_PurchaseOrder,
                        IS_PurchaseOrder_Approve=get_IS_PurchaseOrder_Approve,
                        IS_GRN=get_IS_GRN,
                        IS_GRN_Approve=get_IS_GRN_Approve,
                        IS_Quick_GRN=get_IS_Quick_GRN,
                        IS_Quick_GRN_Approve=get_IS_Quick_GRN_Approve,
                        IS_Purchase_Return=get_IS_Purchase_Return,
                        IS_Purchase_Return_Approve=get_IS_Purchase_Return_Approve,
                        IS_Indent=get_IS_Indent,
                        IS_Indent_Raise_Approve=get_IS_Indent_Raise_Approve,
                        IS_Indent_Issue_Approve=get_IS_Indent_Issue_Approve,
                        IS_Indent_Receive_Approve=get_IS_Indent_Receive_Approve,
                        IS_Indent_Return_Approve=get_IS_Indent_Return_Approve,
                        created_by=created_by
                    )              
 
                return JsonResponse({'success': 'Store Name and Approval Conditions added successfully.'})
 
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)  
   
    elif request.method == 'GET':
        try:
            SearchLocation = request.GET.get('SearchLocation')
            forquickgrn = bool(request.GET.get('forquickgrn', False))
 
            Inventory_Location_Master = Inventory_Location_Master_Detials.objects.all()
            if SearchLocation:
                Inventory_Location_Master = Inventory_Location_Master.filter(Location_Name__Location_Id=SearchLocation, Status=True)
 
            INLO_Master_data = []
            for Floor in Inventory_Location_Master:
                Floor_dict = {
                    'id': Floor.Store_Id,
                    'StoreName': Floor.Store_Name,
                    'StoreType': Floor.Store_Type,
                    'FloorId': Floor.Floor_Name.Floor_Id if Floor.Floor_Name else None,
                    'FloorName': Floor.Floor_Name.Floor_Name if Floor.Floor_Name else None,
                    'BlockId': Floor.Block_Name.Block_Id if Floor.Block_Name else None,
                    'BlockName': Floor.Block_Name.Block_Name if Floor.Block_Name else None,
                    'BuildingId': Floor.Building_Name.Building_Id if Floor.Building_Name else None,
                    'BuildingName': Floor.Building_Name.Building_Name if Floor.Building_Name else None,
                    'Location_Name': Floor.Location_Name.Location_Name if Floor.Location_Name else None,
                    'Location_Id': Floor.Location_Name.Location_Id if Floor.Location_Name else None,
                    'IsPointOfSale': 'Yes' if Floor.IsPointOfSale else 'No',
                    'Status': 'Active' if Floor.Status else 'Inactive',
                    'created_by': Floor.created_by,
                    'Departmentslist': [
                            dept.Department_Name
                            for dept in Floor.Departments.all()
                        ],
                    'Departments': [
                            dept.Department_Id
                            for dept in Floor.Departments.all()
                        ]
                }
 
               
               
                # Fetch approval conditions for the current store              
                approval_conditions = Inventory_Page_Access_Detailes.objects.filter(Access_StoreId=Floor.Store_Id).first()
 
                # Define default approval conditions structure
                approvalConditions = [
                    {
                        'id': 'PurchaseOrder',
                        'label': 'Purchase Order',
                        'exists': approval_conditions.IS_PurchaseOrder if approval_conditions else False,
                        'additionalOptions': [
                            {'id': 'PurchaseOrderApprove', 'label': 'Purchase Order Approve', 'checked': approval_conditions.IS_PurchaseOrder_Approve if approval_conditions else False}
                        ]
                    },
                    {
                        'id': 'GoodsReceivedNote',
                        'label': 'Goods Received Note',
                        'exists': approval_conditions.IS_GRN if approval_conditions else False,
                        'additionalOptions': [
                            {'id': 'GoodsReceivedNoteApprove', 'label': 'Goods Received Note Approve', 'checked': approval_conditions.IS_GRN_Approve if approval_conditions else False}
                        ]
                    },
                    {
                        'id': 'QuickGoodsReceivedNote',
                        'label': 'Quick Goods Received Note',
                        'exists': approval_conditions.IS_Quick_GRN if approval_conditions else False,
                        'additionalOptions': [
                            {'id': 'QuickGoodsReceivedNoteApprove', 'label': 'Quick Goods Received Note Approve', 'checked': approval_conditions.IS_Quick_GRN_Approve if approval_conditions else False}
                        ]
                    },
                    {
                        'id': 'PurchaseReturn',
                        'label': 'Purchase Return',
                        'exists': approval_conditions.IS_Purchase_Return if approval_conditions else False,
                        'additionalOptions': [
                            {'id': 'PurchaseReturnApprove', 'label': 'Purchase Return Approve', 'checked': approval_conditions.IS_Purchase_Return_Approve if approval_conditions else False}
                        ]
                    },
                    {
                        'id': 'Indent',
                        'label': 'Indent',
                        'exists': approval_conditions.IS_Indent if approval_conditions else False,
                        'additionalOptions': [
                            {'id': 'raiseApprove', 'label': 'Raise Approve', 'checked': approval_conditions.IS_Indent_Raise_Approve if approval_conditions else False},
                            {'id': 'issueApprove', 'label': 'Issue Approve', 'checked': approval_conditions.IS_Indent_Issue_Approve if approval_conditions else False},
                            {'id': 'receiveApprove', 'label': 'Receive Approve', 'checked': approval_conditions.IS_Indent_Receive_Approve if approval_conditions else False},
                            {'id': 'returnApprove', 'label': 'Return Approve', 'checked': approval_conditions.IS_Indent_Return_Approve if approval_conditions else False},
                        ]
                    },
                ]
 
                Floor_dict['approvalConditions'] = approvalConditions
 
                getSingledata = []
 
                conditions = {
                    'IS_PurchaseOrder': 'PurchaseOrder',
                    'IS_PurchaseOrder_Approve': 'PurchaseOrderApprove',
                    'IS_GRN': 'GoodsReceivedNote',
                    'IS_GRN_Approve': 'GoodsReceivedNoteApprove',
                    'IS_Quick_GRN': 'QuickGoodsReceivedNote',
                    'IS_Quick_GRN_Approve': 'QuickGoodsReceivedNoteApprove',
                    'IS_Purchase_Return': 'PurchaseReturn',
                    'IS_Purchase_Return_Approve': 'PurchaseReturnApprove',
                    'IS_Indent': 'Indent',
                    'IS_Indent_Raise_Approve': 'IndentRaiseApprove',
                    'IS_Indent_Issue_Approve': 'IndentIssueApprove',
                    'IS_Indent_Receive_Approve': 'IndentReceiveApprove',
                    'IS_Indent_Return_Approve': 'IndentReturnApprove',
 
                }
 
 
                if approval_conditions:
                    for condition, label in conditions.items():
                        if getattr(approval_conditions, condition, False):
                            getSingledata.append(label)
               
                Floor_dict['getSingledata'] =getSingledata
               
                INLO_Master_data.append(Floor_dict)
 
            return JsonResponse(INLO_Master_data, safe=False)
 
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

 
# Administration name
@csrf_exempt
@require_http_methods(["POST","OPTIONS","GET"])
def Administration_Details_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("administrationdata", data)
            AdministartionNameId = data.get('AdministartionNameId', '')
            AdministartionName = data.get('AdministartionName','')
            BlockName = data.get('BlockName','')
            FloorName = data.get('FloorName','')
            BuildingName = data.get('BuildingName','')
            Location = data.get('Location','')
            created_by = data.get('created_by','')
            Statusedit = data.get('Statusedit',False)
 
            Location_instance=None
            Building_instance=None
            Block_instance=None
            Floor_instance=None
 
            if Location:
                Location_instance = Location_Detials.objects.get(Location_Id = Location)
           
            if BuildingName:
                Building_instance = Building_Master_Detials.objects.get(Building_Id = BuildingName)
               
            if BlockName:
                Block_instance = Block_Master_Detials.objects.get(Block_Id = BlockName)
               
            if FloorName:
                Floor_instance = Floor_Master_Detials.objects.get(Floor_Id = FloorName)
               
            if AdministartionNameId:
                if Statusedit:
                    administration_instance = Administration_Master_Details.objects.get(Administration_Id=AdministartionNameId)
                    administration_instance.Status = not administration_instance.Status
                    administration_instance.save()
                    return JsonResponse({'success': "Administration status updated successfully."})
                else:
 
                    if Administration_Master_Details.objects.filter(Administration_Name=AdministartionName, Location_Name=Location_instance, Building_Name = Building_instance,Block_Name=Block_instance, Floor_Name=Floor_instance).exclude(pk=AdministartionNameId).exists():
                        return JsonResponse({'warn': f"The Administration Details are already present  in the name of {AdministartionName} and {Location_instance.Location_Name} and {Building_instance.Building_Name} and {Block_instance.Block_Name} and {Floor_instance.Floor_Name}"})
                    else:
                        administration_instance = Administration_Master_Details.objects.get(pk=AdministartionNameId)
                        administration_instance.Administration_Name = AdministartionName
                        administration_instance.Floor_Name = Floor_instance
                        administration_instance.Block_Name = Block_instance
                        administration_instance.Building_Name = Building_instance
                        administration_instance.Location_Name=Location_instance
                        administration_instance.save()
                    return JsonResponse({'success': 'Administration  Detials Updated successfully'})
 
            else:
                if Administration_Master_Details.objects.filter(Administration_Name=AdministartionName, Location_Name=Location_instance, Building_Name = Building_instance ,Block_Name=Block_instance,Floor_Name=Floor_instance).exists():
                    return JsonResponse({'warn': f"The Administration Detials are already present in the name of {AdministartionName} and {Location_instance.Location_Name} and {Building_instance.Building_Name} and {Block_instance.Block_Name} and {Floor_instance.Floor_Name}"})
                else:
                    administration_instance = Administration_Master_Details(
                        Administration_Name=AdministartionName,
                        Building_Name=Building_instance,
                        Block_Name=Block_instance,
                        Floor_Name=Floor_instance,
                        Location_Name=Location_instance,
                        created_by=created_by,
 
 
 
                    )
                    administration_instance.save()
                    return JsonResponse({'success': 'Administration Detials added successfully'})
 
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
 
    elif request.method == 'GET':
        try:
            Administration_Master = Administration_Master_Details.objects.all()
            print("Administration_Master",Administration_Master)
            Administration_Master_Data = []
            for administration in Administration_Master:
                administration_dict = {
                    'id': administration.Administration_Id,
                    'AdministrationName':administration.Administration_Name,
                    'FloorId': administration.Floor_Name.Floor_Id,
                    'FloorName': administration.Floor_Name.Floor_Name,
                    'BlockId': administration.Block_Name.Block_Id,
                    'BlockName': administration.Block_Name.Block_Name,
                    'BuildingId': administration.Building_Name.Building_Id,
                    'BuildingName': administration.Building_Name.Building_Name,
                    'Location_Name': administration.Location_Name.Location_Name,
                    'Location_Id': administration.Location_Name.Location_Id,
                    'Status': 'Active' if administration.Status else 'Inactive',
                    'created_by': administration.created_by,
                }
                Administration_Master_Data.append(administration_dict)
            return JsonResponse(Administration_Master_Data, safe=False)
 
       
        except Exception as e:
            return JsonResponse({'error' : 'An internal server error occurred'}, status=500)
 
@csrf_exempt
def NurseStationData(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            ward_ids = data.get('SelectedWardIDs', [])
            
            # Dictionary to group wards by nurse station
            station_assignments = {}
            
            for ward_id in ward_ids:
                if ward_id != "ALL":
                    existing_detail = NurseStationMasterDetails.objects.filter(Wardid=ward_id).first()
                    if existing_detail:
                        existing_station = NurseStationMaster.objects.get(NurseStationid=existing_detail.NurseStationid.NurseStationid)
                        station_name = existing_station.NurseStationName
                        ward_name = existing_detail.Wardid.Ward_Name
                        
                        # Group the wards by their nurse station
                        if station_name not in station_assignments:
                            station_assignments[station_name] = []
                        station_assignments[station_name].append(ward_name)
            
            if station_assignments:
                # Create a response with all the assigned wards grouped by nurse station
                messages = []
                for station_name, wards in station_assignments.items():
                    ward_list = ', '.join(wards)  # Join ward names by comma
                    messages.append(f"Selected {ward_list} are already assigned to Nurse Station -'{station_name}'")
                
                return JsonResponse(
                    {
                        "message": '\n'.join(messages),  # Join messages for each station with newline
                        "type": "warn",
                        "response": ""
                    }
                )


            fields_to_convert = ['Location_Name', 'Building_Name', 'Block_Name', 'Floor_Name']
            keys_to_remove = ['SelectedWardIDs', 'WardNames']
            for field in fields_to_convert:
                if field in data and data[field]:
                    data[field] = int(data[field])
            for key in keys_to_remove:
                if key in data:
                    del data[key]

            print('data :',data)
            nurse_station_serializer = NurseStationSerializer(data=data,context={'request': request})
            if nurse_station_serializer.is_valid():
                try:
                    nurse_station = nurse_station_serializer.save()
                except Exception as e:
                    print('error1:', e)
                    return JsonResponse({"message": "Error saving Nurse Station.", "error": str(e)}, status=500)
            else:
                return JsonResponse(nurse_station_serializer.errors, status=400)
            nurse_station_details_list = []
            for ward_id in ward_ids:
                if ward_id != "ALL":
                    detail_data = {
                        'NurseStationid': nurse_station.NurseStationid,
                        'Wardid': ward_id,
                        'created_by': data.get('created_by'),
                    }
                    details_serializer = NurseStationDetailsSerializer(data=detail_data)
                    if details_serializer.is_valid():
                        try:
                            detail = details_serializer.save()
                            nurse_station_details_list.append(detail)
                        except Exception as e:
                            return JsonResponse(
                                {"message": "Error saving Nurse Station Detail.", "error": str(e)}, status=500
                            )
                    else:
                        return JsonResponse(details_serializer.errors, status=400)

            return JsonResponse(
                {
                    "message": "Nurse Station and Wards inserted successfully.",
                    "type": "success",
                    "nurse_station": nurse_station_serializer.data,
                    "nurse_station_details": [detail.NurseStationDetailsid for detail in nurse_station_details_list],
                },
                status=201
            )

        elif request.method == 'GET':
            nurse_stations = NurseStationMaster.objects.all()
            nurse_stations_serialized = NurseStationSerializer(nurse_stations, many=True,context={'request': request})

            # Attach wards to each Nurse Station
            for idex,station in enumerate(nurse_stations_serialized.data,start=1):
                station_details = NurseStationMasterDetails.objects.filter(NurseStationid=station["NurseStationid"])
                details_serialized = NurseStationDetailsSerializer(station_details, many=True)
                station["Wards"] = details_serialized.data
                station['id'] = idex
                if station.get('Status') == True:
                    station["Status_Name"] = "Active"
                else:
                    station["Status_Name"] = "InActive"

            return JsonResponse(nurse_stations_serialized.data, safe=False)

        else:
            return JsonResponse({"message": "Invalid HTTP method."}, status=405)

    except Exception as e:
        print('error:', e)
        return JsonResponse({'message': 'An error occurred.', 'error': str(e)}, status=500)



def get_Ward_Data_by_Floor_loc(request):
    try:
        Floor = request.GET.get('FloorName')
        
        if not Floor:
            return JsonResponse({'error': 'Floor is required'}, status=400)
        
        # Get the Floor instance
        try:
            Floor_ins = Floor_Master_Detials.objects.get(Floor_Id=Floor)
        except Floor_Master_Detials.DoesNotExist:
            return JsonResponse({'error': 'Floor not found'}, status=404)
        
        # Base query for WardType_Master_Details
        ward_query = WardType_Master_Detials.objects.filter(
            Status=True,
            Building_Name=Floor_ins.Building_Name,
            Block_Name=Floor_ins.Block_Name,
            Floor_Name=Floor_ins,
            Location_Name=Floor_ins.Location_Name
        )
                
        # If no Ward records found
        if not ward_query.exists():
            return JsonResponse({'error': 'No Ward data found'}, status=404)
        
        # Construct response data
        Ward_Master_data = [{'id': Ward.Ward_Id, 'WardName': Ward.Ward_Name} for Ward in ward_query]
        
        Ward_Master_data.insert(0,{'id': 'ALL', 'WardName': 'ALL' })

        return JsonResponse(Ward_Master_data, safe=False)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'An internal server error occurred'}, status=500)
    


    

@csrf_exempt
def get_Building_data(request):
 
    try:
      if request.method == 'GET':
 
        building_ins = Building_Master_Detials.objects.all()
        building_data_list = []
        for datas in building_ins:
            data_dict = {
                'id': datas.Building_Id,
                'BuildingName': datas.Building_Name
            }
            building_data_list.append(data_dict)
 
 
 
        return JsonResponse(building_data_list,safe = False)
 
 
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'An internal server error occurred'},status=500)
   
@csrf_exempt
def get_floor_data_by_Block(request):
 
    try:
      if request.method == 'GET':
 
        Block = request.GET.get('Block')
 
        Floor_ins = Floor_Master_Detials.objects.filter(Block_Name_id=Block)
        floor_data_list = []
        for datas in Floor_ins:
            data_dict = {
                'id': datas.Floor_Id,
                'FloorName': datas.Floor_Name
            }
            floor_data_list.append(data_dict)
 
 
 
        return JsonResponse(floor_data_list,safe = False)
 
 
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'An internal server error occurred'},status=500)
 
@csrf_exempt
def get_Ward_details_by_floor(request):
 
    try:
      if request.method == 'GET':
 
        Floor = request.GET.get('Floor')
 
        Ward_ins = WardType_Master_Detials.objects.filter(Floor_Name_id=Floor)
       
       
        bed_details = []
        for datas in Ward_ins:
           
            rooms = Room_Master_Detials.objects.filter(Ward_Name_id=datas.Ward_Id)
            unique_rooms = {}
 
            for room in rooms:
                    room_no = room.Room_No
                    if room_no not in unique_rooms:
                        unique_rooms[room_no] = {
                            "RoomNo": room_no,
                            "Beds": []
                        }
                    unique_rooms[room_no]["Beds"].append({
                        "BedId": room.Room_Id,
                        "BedNo": room.Bed_No,
                        "status":room.Booking_Status
                    })
 
            ward_data = {
                    'WardId': datas.Ward_Id,
                    'WardName': datas.Ward_Name,
                    "Rooms": list(unique_rooms.values())
                }
            bed_details.append(ward_data)
           
       
 
 
 
        return JsonResponse(bed_details,safe = False)
 
 
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return JsonResponse({'error': 'An internal server error occurred'},status=500)
 