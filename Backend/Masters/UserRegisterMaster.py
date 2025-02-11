                 
import json
import random
import string
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from .models import *
from django.contrib.auth.models import User
from HR_Management.models import *


def Get_User_Detialsby_id(request):
    if request.method == 'GET':
        try:
            UserId = request.GET.get('UserId')
            if UserId:
                UserRegister = UserRegister_Master_Details.objects.get(User_Id=UserId)

                # Retrieve locations associated with the user
                locations = list(UserRegister.Locations.all().values('Location_Id', 'Location_Name'))
                doctor_professional=None
                
                if UserRegister.EmployeeType =='DOCTOR':
                    doctor_professional = Doctor_ProfessForm_Detials.objects.get(Doctor_ID=UserRegister.Doctor_Id.Doctor_ID)
                
                UserRegister_dict = {
                    'id': UserRegister.User_Id,
                    'EmployeeType':UserRegister.EmployeeType,
                    'EmployeeId': UserRegister.Employee_Id.Employee_ID if UserRegister.EmployeeType =='EMPLOYEE' else '',
                    'DoctorId': UserRegister.Doctor_Id.Doctor_ID if UserRegister.EmployeeType =='DOCTOR' else '',
                    'UserName': UserRegister.auth_user_id.username,
                    'Title': UserRegister.Employee_Id.Tittle.Title_Name if UserRegister.EmployeeType =='EMPLOYEE' else UserRegister.Doctor_Id.Tittle,
                    'firstName': UserRegister.Employee_Id.First_Name if UserRegister.EmployeeType =='EMPLOYEE' else UserRegister.Doctor_Id.First_Name,
                    'middleName':  UserRegister.Employee_Id.Middle_Name if UserRegister.EmployeeType =='EMPLOYEE' else UserRegister.Doctor_Id.Middle_Name,
                    'lastName': UserRegister.Employee_Id.Last_Name if UserRegister.EmployeeType =='EMPLOYEE' else UserRegister.Doctor_Id.Last_Name,
                    'Email': UserRegister.Employee_Id.E_mail if UserRegister.EmployeeType =='EMPLOYEE' else UserRegister.Doctor_Id.E_mail,
                    'roleName': UserRegister.role.Role_Name, 
                    'PhoneNo': UserRegister.Employee_Id.Contact_Number if UserRegister.EmployeeType =='EMPLOYEE' else UserRegister.Doctor_Id.Contact_Number,
                    'Gender': UserRegister.Employee_Id.Gender if UserRegister.EmployeeType =='EMPLOYEE' else UserRegister.Doctor_Id.Gender,
                    'Qualification': 'EMP' if UserRegister.EmployeeType == 'EMPLOYEE' else (doctor_professional.Qualification if doctor_professional else ''),
                    'Status': UserRegister.Status,
                    'created_by': UserRegister.created_by,
                    'Access': UserRegister.Access,
                    'SubAccess': UserRegister.SubAccess,
                    'Locations': locations  # Assign the list of locations
                }

                return JsonResponse(UserRegister_dict)

        except UserRegister_Master_Details.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)




# @csrf_exempt
# def UserRegister_Detials_link(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             print(data)  # For debugging purposes
            
#             UserId = data.get('UserId', '')
#             EmployeeType = data.get('EmployeeType', '')
#             employeeid = data.get('EmployeeId', '')
#             doctorid = data.get('DoctorId', '')
#             username = data.get('UserName', '')
#             password = data.get('Password', '')
#             roleName = data.get('roleName', '')
#             location_names = data.get('Location', '')  # Assuming location names are passed as a string

#             Access = data.get('ParentData', '')
#             SubAccess = data.get('ChildData', '')
#             created_by = data.get('created_by', '')

#             if UserId:  # If UserId is provided, update existing user
#                 user_instance = UserRegister_Master_Details.objects.get(User_Id=UserId)
#                 user_instance.Access = Access
#                 user_instance.SubAccess = SubAccess
#                 user_instance.created_by = created_by
#                 user_instance.save()

#                 # Update locations
#                 if location_names:
#                     location_names_list = location_names.split(',')
#                     locations = Location_Detials.objects.filter(Location_Name__in=location_names_list)
#                     user_instance.Locations.set(locations)
                
#                 return JsonResponse({'success': 'User details updated successfully'})

#             else:  # If UserId is not provided, create a new user
#                 if User.objects.filter(Username=username).exists():
#                     return JsonResponse({'warn': f"The Username: {username} is already present"})
#                 else:
#                     # Generate random password if not provided
#                     if not password:
#                         length = random.randint(8, 10)
#                         all_characters = string.ascii_letters + string.digits + '!@#$'
#                         password_auto = ''.join(random.choice(all_characters) for _ in range(length))
#                         # Hash the password
#                         hashed_password = make_password(password_auto)
#                     else:
#                         hashed_password = make_password(password)

#                     print(password_auto, 'password_auto')  
#                     print(hashed_password, 'hashed_password')  
#                     print(username, 'username')  

#                     new_user = User.objects.create(username=username, password=hashed_password)

#                     # Retrieve locations based on location_names
#                     if location_names:
#                         location_names_list = location_names.split(',')
#                         locations = Location_Detials.objects.filter(Location_Name__in=location_names_list)
#                     else:
#                         locations = []

#                     Doctor_instance = None
#                     Employee_instance = None

#                     # Find instance of doctor and employee
#                     if doctorid:
#                         Doctor_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=doctorid)
#                     if employeeid:
#                         Employee_instance = Employee_Personal_Form_Detials.objects.get(Employee_ID=employeeid)
                    
#                     # Create user instance
#                     user_instance = UserRegister_Master_Details(
#                         EmployeeType=EmployeeType,
#                         Doctor_Id=Doctor_instance,
#                         Employee_Id=Employee_instance,
#                         auth_user_id=new_user,
#                         Password=hashed_password,
#                         role=Role_Master.objects.get(Role_Name=roleName),  # Correct role assignment
#                         Access=Access,
#                         SubAccess=SubAccess,
#                         created_by=created_by
#                     )
#                     user_instance.save()

#                     # Assign locations to the user using the set() method of the ManyToManyField
#                     user_instance.Locations.set(locations)

#                     return JsonResponse({'success': f'User registered successfully. Password: {password_auto}' if not password else 'User registered successfully'})

#         except Exception as e:
#             print(f"An error occurred: {str(e)}")
#             return JsonResponse({'error': 'An internal server error occurred'}, status=500)

#     elif request.method == 'GET':
#         try:
#             user_register_data = UserRegister_Master_Details.objects.exclude(created_by='system')

#             user_register_list = []
#             for user in user_register_data:
#                 doctor_professional = None
#                 if user.EmployeeType == 'DOCTOR':
#                     doctor_professional = Doctor_ProfessForm_Detials.objects.get(Doctor_ID=user.Doctor_Id.Doctor_ID)
                
#                 user_dict = {
#                     'id': user.User_Id,
#                     'EmployeeType': user.EmployeeType,
#                     'EmployeeId': user.Employee_Id.Employee_ID if user.EmployeeType == 'EMPLOYEE' else '',
#                     'DoctorId': user.Doctor_Id.Doctor_ID if user.EmployeeType == 'DOCTOR' else '',
#                     'UserName': user.auth_user_id.username,
#                     'Name': f'{user.Employee_Id.Tittle}.{user.Employee_Id.First_Name} {user.Employee_Id.Middle_Name} {user.Employee_Id.Last_Name}'if user.EmployeeType == 'EMPLOYEE' else  f'{user.Doctor_Id.Tittle}.{user.Doctor_Id.First_Name} {user.Doctor_Id.Middle_Name} {user.Doctor_Id.Last_Name}' ,
#                     'Email': user.Employee_Id.E_mail if user.EmployeeType == 'EMPLOYEE' else user.Doctor_Id.E_mail,
#                     'roleName': user.role.Role_Name, 
#                     'PhoneNo': user.Employee_Id.Contact_Number if user.EmployeeType == 'EMPLOYEE' else user.Doctor_Id.Contact_Number,
#                     'Gender': user.Employee_Id.Gender if user.EmployeeType == 'EMPLOYEE' else user.Doctor_Id.Gender,
#                     'Qualification': 'EMP' if user.EmployeeType == 'EMPLOYEE' else (doctor_professional.Qualification if doctor_professional else ''),
#                     'Locations': [location.Location_Name for location in user.Locations.all()],
#                     'Status': 'Active' if user.Status else 'Inactive',
#                     'created_by': user.created_by
#                 }
#                 user_register_list.append(user_dict)

#             return JsonResponse(user_register_list, safe=False)
#         except Exception as e:
#             print(f"An error occurred: {str(e)}")
#             return JsonResponse({'error': 'An internal server error occurred'}, status=500)

#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=400)





# @csrf_exempt
# def UserRegister_Detials_link(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             print(data)  # For debugging purposes
            
#             UserId = data.get('UserId', '')
#             EmployeeType = data.get('EmployeeType', '')
#             employeeid = data.get('EmployeeId', '')
#             doctorid = data.get('DoctorId', '')
#             username = data.get('UserName', '')
#             password = data.get('Password', '')
#             roleName = data.get('roleName', '')
#             location_names = data.get('Location', '')  # Assuming location names are passed as a string

#             Access = data.get('ParentData', '')
#             SubAccess = data.get('ChildData', '')
#             created_by = data.get('created_by', '')

#             if UserId:  # If UserId is provided, update existing user
#                 user_instance = UserRegister_Master_Details.objects.get(User_Id=UserId)
#                 user_instance.Access = Access
#                 user_instance.SubAccess = SubAccess
#                 user_instance.created_by = created_by
#                 user_instance.save()

#                 # Update locations
#                 if location_names:
#                     location_names_list = location_names.split(',')
#                     locations = Location_Detials.objects.filter(Location_Name__in=location_names_list)
#                     user_instance.Locations.set(locations)
                
#                 return JsonResponse({'success': 'User details updated successfully'})

#             else:  # If UserId is not provided, create a new user
#                 if User.objects.filter(username=username).exists():
#                     return JsonResponse({'warn': f"The Username: {username} is already present"})
#                 else:
                    

                    

#                     # Retrieve locations based on location_names
#                     if location_names:
#                         location_names_list = location_names.split(',')
#                         locations = Location_Detials.objects.filter(Location_Name__in=location_names_list)
#                     else:
#                         locations = []

#                     Doctor_instance = None
#                     Employee_instance = None

#                     # Find instance of doctor and employee
#                     if doctorid:
#                         Doctor_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=doctorid)
#                     if employeeid:
#                         Employee_instance = Employee_Personal_Form_Detials.objects.get(Employee_ID=employeeid)
                    
#                     # Create user instance
                    
#                     user_auth_user = User.objects.create_user(
#                         username=username,
#                         password=password,
#                         first_name=Doctor_instance.First_Name if Doctor_instance else Employee_instance.First_Name,
#                         last_name=Doctor_instance.Last_Name if Doctor_instance else Employee_instance.Last_Name,
#                         email= Doctor_instance.E_mail if Doctor_instance else Employee_instance.E_mail,
#                         is_staff=True
#                     )
#                     user_instance = UserRegister_Master_Details(
#                         auth_user_id = user_auth_user,
#                         EmployeeType=EmployeeType,
#                         Doctor_Id=Doctor_instance,
#                         Employee_Id=Employee_instance,
#                         role=Role_Master.objects.get(Role_Name=roleName),  # Correct role assignment
#                         Access=Access,
#                         SubAccess=SubAccess,
#                         created_by=created_by
#                     )
#                     user_instance.save()

#                     # Assign locations to the user using the set() method of the ManyToManyField
#                     user_instance.Locations.set(locations)

#                     return JsonResponse({'success': f'User registered successfully. Password: {password_auto}' if not password else 'User registered successfully'})

#         except Exception as e:
#             print(f"An error occurred: {str(e)}")
#             return JsonResponse({'error': 'An internal server error occurred'}, status=500)

#     elif request.method == 'GET':
#         try:
#             user_register_data = User.objects.exclude(username='host')

#             user_register_list = []
#             for user in user_register_data:
#                 print(user)
#                 print(user.pk)
#                 user_register_ins = UserRegister_Master_Details.objects.filter(auth_user_id__username = user.username).first()
#                 print('0000')
#                 if not user_register_ins:
#                     return JsonResponse({'error': 'user doesn`t exist.'}, status=400)
#                 doctor_professional = None
#                 if user_register_ins.EmployeeType == 'DOCTOR':
#                     doctor_professional = Doctor_ProfessForm_Detials.objects.get(Doctor_ID=user_register_ins.Doctor_Id.Doctor_ID)
#                 print('1233')
#                 user_dict = {
#                     'id': user.pk,
#                     'EmployeeType': user_register_ins.EmployeeType,
#                     'EmployeeId': user_register_ins.Employee_Id.Employee_ID if user_register_ins.EmployeeType == 'EMPLOYEE' else '',
#                     'DoctorId': user_register_ins.Doctor_Id.Doctor_ID if user_register_ins.EmployeeType == 'DOCTOR' else '',
#                     'UserName': user.username,
#                     'Name': f'{user_register_ins.Employee_Id.Tittle}.{user_register_ins.Employee_Id.First_Name} {user_register_ins.Employee_Id.Middle_Name} {user_register_ins.Employee_Id.Last_Name}'if user_register_ins.EmployeeType == 'EMPLOYEE' else  f'{user_register_ins.Doctor_Id.Tittle}.{user_register_ins.Doctor_Id.First_Name} {user_register_ins.Doctor_Id.Middle_Name} {user_register_ins.Doctor_Id.Last_Name}' ,
#                     'Email': user.email,
#                     'roleName': user_register_ins.role.Role_Name, 
#                     'PhoneNo': user_register_ins.Employee_Id.Contact_Number if user_register_ins.EmployeeType == 'EMPLOYEE' else user_register_ins.Doctor_Id.Contact_Number,
#                     'Gender': user_register_ins.Employee_Id.Gender if user_register_ins.EmployeeType == 'EMPLOYEE' else user_register_ins.Doctor_Id.Gender,
#                     'Qualification': 'EMP' if user_register_ins.EmployeeType == 'EMPLOYEE' else (doctor_professional.Qualification if doctor_professional else ''),
#                     'Locations': [location.Location_Name for location in user_register_ins.Locations.all()],
#                     'Status': 'Active' if user.is_active else 'Inactive',
#                     'created_by': user_register_ins.created_by
#                 }
#                 user_register_list.append(user_dict)

#             return JsonResponse(user_register_list, safe=False)
#         except Exception as e:
#             print(f"An error occurred: {str(e)}")
#             return JsonResponse({'error': 'An internal server error occurred'}, status=500)

#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=400)



# @csrf_exempt
# def UserRegister_Detials_link(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             print(data,'aaaaaaaaaaaaaaaaaaaa')  # For debugging purposes
           
#             UserId = data.get('UserId', '')
#             EmployeeType = data.get('EmployeeType', '')
#             employeeid = data.get('EmployeeId', '')
#             doctorid = data.get('DoctorId', '')
#             username = data.get('UserName', '')
#             password = data.get('Password', '')
#             roleName = data.get('roleName', '')
#             location_names = data.get('Location', '')  # Assuming location names are passed as a string
 
#             Access = data.get('ParentData', '')
#             SubAccess = data.get('ChildData', '')
#             created_by = data.get('created_by', '')
 
#             if UserId:  # If UserId is provided, update existing user
#                 user_instance = UserRegister_Master_Details.objects.get(User_Id=UserId)
#                 user_instance.Access = Access
#                 user_instance.SubAccess = SubAccess
#                 user_instance.created_by = created_by
#                 user_instance.save()
 
#                 # Update locations
#                 if location_names:
#                     location_names_list = location_names.split(',')
#                     locations = Location_Detials.objects.filter(Location_Name__in=location_names_list)
#                     user_instance.Locations.set(locations)
               
#                 return JsonResponse({'success': 'User details updated successfully'})
 
#             else:  # If UserId is not provided, create a new user
#                 if User.objects.filter(username=username).exists():
#                     return JsonResponse({'warn': f"The Username: {username} is already present"})
#                 else:
                   
 
                   
 
#                     # Retrieve locations based on location_names
#                     if location_names:
#                         location_names_list = location_names.split(',')
#                         locations = Location_Detials.objects.filter(Location_Name__in=location_names_list)
#                     else:
#                         locations = []
 
#                     Doctor_instance = None
#                     Employee_instance = None
 
#                     # Find instance of doctor and employee
#                     if doctorid:
#                         Doctor_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=doctorid)
#                     if employeeid:
#                         try:
#                             Employee_instance = Employee_Personal_Form_Detials.objects.get(pk=employeeid)
#                         except Employee_Personal_Form_Detials.DoesNotExist:
#                             return JsonResponse({'error': 'Employee not found'}, status=404)
 
#                     # Create user instance
                   
#                     user_auth_user = User.objects.create_user(
#                         username=username,
#                         password=password,
#                         first_name=Doctor_instance.First_Name if Doctor_instance else Employee_instance.First_Name,
#                         last_name=Doctor_instance.Last_Name if Doctor_instance else Employee_instance.Last_Name,
#                         email= Doctor_instance.E_mail if Doctor_instance else Employee_instance.E_mail,
#                         is_staff=True
#                     )
#                     user_instance = UserRegister_Master_Details(
#                         auth_user_id = user_auth_user,
#                         EmployeeType=EmployeeType,
#                         Doctor_Id=Doctor_instance,
#                         Employee_Id=Employee_instance,
#                         role=Role_Master.objects.get(Role_Name=roleName),  # Correct role assignment
#                         Access=Access,
#                         SubAccess=SubAccess,
#                         created_by=created_by
#                     )
#                     user_instance.save()
 
#                     # Assign locations to the user using the set() method of the ManyToManyField
#                     user_instance.Locations.set(locations)
 
#                     return JsonResponse({'success': f'User registered successfully. Password: ' if not password else 'User registered successfully'})
 
#         except Exception as e:
#             print(f"An error occurred: {str(e)}")
#             return JsonResponse({'error': 'An internal server error occurred'}, status=500)
 
#     elif request.method == 'GET':
#         try:
#             # Retrieve all users except the 'host' user
#             user_register_data = User.objects.exclude(username='host')
 
#             print(user_register_data, 'user_register_data')
#             user_register_list = []
 
#             # Loop through all the users
#             for user in user_register_data:
#                 print(user.username)
#                 print(user.pk)
 
#                 # Try to fetch UserRegister_Master_Details for each user, if it exists
#                 # user_register_ins = UserRegister_Master_Details.objects.filter(auth_user_id__username=user.username).first()
#                 user_register_ins = UserRegister_Master_Details.objects.select_related(

#                     'auth_user_id', 'Doctor_Id', 'Employee_Id', 'role'

#                 ).prefetch_related('Locations').filter(auth_user_id__username=user.username).first()

 
#                 print('0000')
#                 print('user_register_ins:', user_register_ins)
 
#                 # If no registration details exist for the user, you can choose to either skip the user or handle it differently
#                 if not user_register_ins:
#                     user_register_ins = None  # Explicitly set to None if the record doesn't exist
 
#                 # Initialize professional details as None
#                 doctor_professional = None
#                 Employee_professional = None
 
#                 if user_register_ins:
#                     # If there is a registration entry, get doctor or employee professional details
#                     if user_register_ins.EmployeeType == 'DOCTOR' and user_register_ins.Doctor_Id:
#                         doctor_professional = Doctor_ProfessForm_Detials.objects.get(Doctor_ID=user_register_ins.Doctor_Id.Doctor_ID)
#                         print('doctor_professional:', doctor_professional)
#                     elif user_register_ins.EmployeeType == 'EMPLOYEE' and user_register_ins.pk:
#                         Employee_professional = Employee_Personal_Form_Detials.objects.get(pk=user_register_ins.Employee_Id.pk)
#                         print('Employee professional details:', Employee_professional)
 
#                 # Construct the user dict with available information
#                 user_dict = {
#                     'id': user.pk,
#                     'EmployeeType': user_register_ins.EmployeeType if user_register_ins else 'N/A',
#                     'EmployeeId': user_register_ins.Employee_Id.pk if user_register_ins and user_register_ins.EmployeeType == 'EMPLOYEE' else '',
#                     'DoctorId': user_register_ins.Doctor_Id.Doctor_ID if user_register_ins and user_register_ins.EmployeeType == 'DOCTOR' else '',
#                     'UserName': user.username,
#                     'Name': f'{user_register_ins.Employee_Id.Tittle.Title_Name}.{user_register_ins.Employee_Id.First_Name} {user_register_ins.Employee_Id.Middle_Name} {user_register_ins.Employee_Id.Last_Name}' if user_register_ins and user_register_ins.EmployeeType == 'EMPLOYEE' else
#                             f'{user_register_ins.Doctor_Id.Tittle.Title_Name}.{user_register_ins.Doctor_Id.First_Name} {user_register_ins.Doctor_Id.Middle_Name} {user_register_ins.Doctor_Id.Last_Name}' if user_register_ins and user_register_ins.EmployeeType == 'DOCTOR' else 'N/A',
#                     'Email': user.email,
#                     'roleName': user_register_ins.role.Role_Name if user_register_ins else 'N/A',
#                     'PhoneNo': user_register_ins.Employee_Id.Contact_Number if user_register_ins and user_register_ins.EmployeeType == 'EMPLOYEE' else user_register_ins.Doctor_Id.Contact_Number if user_register_ins else 'N/A',
#                     'Gender': user_register_ins.Employee_Id.Gender if user_register_ins and user_register_ins.EmployeeType == 'EMPLOYEE' else user_register_ins.Doctor_Id.Gender if user_register_ins else 'N/A',
#                     'Qualification': user_register_ins.Employee_Id.Qualification if user_register_ins and user_register_ins.EmployeeType == 'EMPLOYEE' else
#                                     (doctor_professional.Qualification if doctor_professional else '') if user_register_ins and user_register_ins.EmployeeType == 'DOCTOR' else 'N/A',
#                     'Locations': [location.Location_Name for location in user_register_ins.Locations.all()] if user_register_ins else [],
#                     'Status': 'Active' if user.is_active else 'Inactive',
#                     'created_by': user_register_ins.created_by if user_register_ins else 'N/A'
#                 }
 
#                 # Append the user dict to the list
#                 user_register_list.append(user_dict)
 
#             return JsonResponse(user_register_list, safe=False)
 
#         except Exception as e:
#             print(f"An error occurred: {str(e)}")
#             return JsonResponse({'error': 'An internal server error occurred'}, status=500)
 
#     else:
#         return JsonResponse({'error': 'Invalid request method'})
 
 
@csrf_exempt
def UserRegister_Detials_link(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(data,'aaaaaaaaaaaaaaaaaaaa')  # For debugging purposes
           
            UserId = data.get('UserId', '')
            EmployeeType = data.get('EmployeeType', '')
            employeeid = data.get('EmployeeId', '')
            doctorid = data.get('DoctorId', '')
            username = data.get('UserName', '')
            password = data.get('Password', '')
            roleName = data.get('roleName', '')
            location_names = data.get('Location', '')  # Assuming location names are passed as a string
 
            Access = data.get('ParentData', '')
            SubAccess = data.get('ChildData', '')
            created_by = data.get('created_by', '')
 
            if UserId:  # If UserId is provided, update existing user
                user_instance = UserRegister_Master_Details.objects.get(User_Id=UserId)
                user_instance.Access = Access
                user_instance.SubAccess = SubAccess
                user_instance.created_by = created_by
                user_instance.save()
 
                # Update locations
                if location_names:
                    location_names_list = location_names.split(',')
                    locations = Location_Detials.objects.filter(Location_Name__in=location_names_list)
                    user_instance.Locations.set(locations)
               
                return JsonResponse({'success': 'User details updated successfully'})
 
            else:  # If UserId is not provided, create a new user
                if User.objects.filter(username=username).exists():
                    return JsonResponse({'warn': f"The Username: {username} is already present"})
                else:
                   
 
                   
 
                    # Retrieve locations based on location_names
                    if location_names:
                        location_names_list = location_names.split(',')
                        locations = Location_Detials.objects.filter(Location_Name__in=location_names_list)
                    else:
                        locations = []
 
                    Doctor_instance = None
                    Employee_instance = None
 
                    # Find instance of doctor and employee
                    if doctorid:
                        Doctor_instance = Doctor_Personal_Form_Detials.objects.get(Doctor_ID=doctorid)
                    if employeeid:
                        try:
                            Employee_instance = Employee_Personal_Form_Detials.objects.get(pk=employeeid)
                        except Employee_Personal_Form_Detials.DoesNotExist:
                            return JsonResponse({'error': 'Employee not found'}, status=404)
 
                    # Create user instance
                   
                    user_auth_user = User.objects.create_user(
                        username=username,
                        password=password,
                        first_name=Doctor_instance.First_Name if Doctor_instance else Employee_instance.First_Name,
                        last_name=Doctor_instance.Last_Name if Doctor_instance else Employee_instance.Last_Name,
                        email= Doctor_instance.E_mail if Doctor_instance else Employee_instance.E_mail,
                        is_staff=True
                    )
                    user_instance = UserRegister_Master_Details(
                        auth_user_id = user_auth_user,
                        EmployeeType=EmployeeType,
                        Doctor_Id=Doctor_instance,
                        Employee_Id=Employee_instance,
                        role=Role_Master.objects.get(Role_Name=roleName),  # Correct role assignment
                        Access=Access,
                        SubAccess=SubAccess,
                        created_by=created_by
                    )
                    user_instance.save()
 
                    # Assign locations to the user using the set() method of the ManyToManyField
                    user_instance.Locations.set(locations)
 
                    return JsonResponse({'success': f'User registered successfully. Password: ' if not password else 'User registered successfully'})
 
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
 
    elif request.method == 'GET':
        try:
            # Retrieve all users except the 'host' user
            user_register_data = User.objects.exclude(username='host')
 
            print(user_register_data, 'user_register_data')
            
            RNo = 1
            user_register_list = []
            
            # Loop through all the users
            for user in user_register_data:
                print(user.username)
                print(user.pk)
 
                # Try to fetch UserRegister_Master_Details for each user, if it exists
                # user_register_ins = UserRegister_Master_Details.objects.filter(auth_user_id__username=user.username).first()
                user_register_ins = UserRegister_Master_Details.objects.select_related(

                    'auth_user_id', 'Doctor_Id', 'Employee_Id', 'role'

                ).prefetch_related('Locations').filter(auth_user_id__username=user.username).first()

 
                print('0000')
                print('user_register_ins:', user_register_ins)
 
                # If no registration details exist for the user, you can choose to either skip the user or handle it differently
                if not user_register_ins:
                    user_register_ins = None  # Explicitly set to None if the record doesn't exist
 
                # Initialize professional details as None
                doctor_professional = None
                Employee_professional = None
 
                if user_register_ins:
                    # If there is a registration entry, get doctor or employee professional details
                    if user_register_ins.EmployeeType == 'DOCTOR' and user_register_ins.Doctor_Id:
                        doctor_professional = Doctor_ProfessForm_Detials.objects.get(Doctor_ID=user_register_ins.Doctor_Id.Doctor_ID)
                        print('doctor_professional:', doctor_professional)
                    elif user_register_ins.EmployeeType == 'EMPLOYEE' and user_register_ins.pk:
                        Employee_professional = Employee_Personal_Form_Detials.objects.get(pk=user_register_ins.Employee_Id.pk)
                        print('Employee professional details:', Employee_professional)
 
                # Construct the user dict with available information
                
                user_dict = {
                    'id': RNo,
                    'Userid': user.pk,
                    'EmployeeType': user_register_ins.EmployeeType if user_register_ins else 'N/A',
                    'EmployeeId': user_register_ins.Employee_Id.pk if user_register_ins and user_register_ins.EmployeeType == 'EMPLOYEE' else '',
                    'DoctorId': user_register_ins.Doctor_Id.Doctor_ID if user_register_ins and user_register_ins.EmployeeType == 'DOCTOR' else '',
                    'UserName': user.username,
                    'Name': f'{user_register_ins.Employee_Id.Tittle.Title_Name if user_register_ins.Employee_Id.Tittle else ''}.{user_register_ins.Employee_Id.First_Name} {user_register_ins.Employee_Id.Middle_Name} {user_register_ins.Employee_Id.Last_Name}' if user_register_ins and user_register_ins.EmployeeType == 'EMPLOYEE' else
                            f'{user_register_ins.Doctor_Id.Tittle.Title_Name if user_register_ins.Doctor_Id.Tittle else ''}.{user_register_ins.Doctor_Id.First_Name} {user_register_ins.Doctor_Id.Middle_Name} {user_register_ins.Doctor_Id.Last_Name}' if user_register_ins and user_register_ins.EmployeeType == 'DOCTOR' else '',
                    'Email': user.email,
                    'roleName': user_register_ins.role.Role_Name if user_register_ins else 'N/A',
                    'PhoneNo': user_register_ins.Employee_Id.Contact_Number if user_register_ins and user_register_ins.EmployeeType == 'EMPLOYEE' else user_register_ins.Doctor_Id.Contact_Number if user_register_ins else 'N/A',
                    'Gender': user_register_ins.Employee_Id.Gender if user_register_ins and user_register_ins.EmployeeType == 'EMPLOYEE' else user_register_ins.Doctor_Id.Gender if user_register_ins else 'N/A',
                    'Qualification': user_register_ins.Employee_Id.Qualification if user_register_ins and user_register_ins.EmployeeType == 'EMPLOYEE' else
                                    (doctor_professional.Qualification if doctor_professional else '') if user_register_ins and user_register_ins.EmployeeType == 'DOCTOR' else 'N/A',
                    'Locations': [location.Location_Name for location in user_register_ins.Locations.all()] if user_register_ins else [],
                    'Status': 'Active' if user.is_active else 'Inactive',
                    'created_by': user_register_ins.created_by if user_register_ins else 'N/A'
                }
                
 
                # Append the user dict to the list
                user_register_list.append(user_dict)
                RNo += 1
 
            return JsonResponse(user_register_list, safe=False)
 
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An internal server error occurred'}, status=500)
 
    else:
        return JsonResponse({'error': 'Invalid request method'})
 




@csrf_exempt
def update_status_User_Detials_link(request):
    try:
        data = json.loads(request.body)

        UserId = data.get('UserId','')
        # Retrieve data from Doctor_Personal_Form_Detials
        user_data_ins = UserRegister_Master_Details.objects.get(User_Id = UserId)
        user_data_ins.Status = not user_data_ins.Status
        user_data_ins.save()

        # Return JSON response
        return JsonResponse({'success': 'User Status Updated successfully'})
    
    except Exception as e:
        # Handle exceptions and return error response
        return JsonResponse({'error': str(e)})


