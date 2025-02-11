import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import *
from PIL import Image
from io import BytesIO
import base64
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.http import JsonResponse
import json
from django.db.models import Max
from django.http import JsonResponse
from django.db.models import Max
import re
from django.http import JsonResponse
import csv
import openpyxl
import pandas as pd
from django.forms.models import model_to_dict
from django.db import transaction
from django.db import connection
from django.db.models import F
from django.db.models import Case, When, Value, IntegerField
from django.db.models import OuterRef, Subquery
from .serializers import *


def Common_Function_For_Genarate_Next_Code_For_6Digit(max_code):
    numeric_part = max_code[-6:]
    prefix = max_code[:-6]
    next_number = int(numeric_part) + 1
    new_code = f"{prefix}{next_number:06d}"

    return new_code


def get_NextAntibiotic_Code(max_anti_biotic_group_code, max_anti_biotic_code):
    numeric_part_group = max_anti_biotic_group_code[-3:]
    prefix_group = max_anti_biotic_group_code[:-3]

    numeric_part_code = max_anti_biotic_code[-3:]
    prefix_code = max_anti_biotic_code[:-3]

    next_number_group = int(numeric_part_group) + 1
    next_number_code = int(numeric_part_code) + 1

    new_anti_biotic_group_code = f"{prefix_group}{next_number_group:03d}"
    new_anti_biotic_code = f"{prefix_code}{next_number_code:03d}"

    return new_anti_biotic_group_code, new_anti_biotic_code


def Genarate_Next_Code_4digit(max_code):
    numeric_part = max_code[-4:]
    prefix = max_code[:-4]
    next_number = int(numeric_part) + 1
    new_code = f"{prefix}{next_number:04d}"

    return new_code


def Get_All_Other_Masters_PrimaryCodes(request):
    if request.method == "GET":
        try:
            # Get the 'Type' parameter from the request
            Type = request.GET.get("Type")
            print("Type :", Type)
            if Type == "LabDepartment":
                # Fetch all department codes with the specified prefix pattern
                max_code = Lab_Department_Detials.objects.all().aggregate(
                    Max("Department_Code")
                )["Department_Code__max"]
                print("max_code :", max_code)
                if max_code:
                    new_department_code = (
                        Common_Function_For_Genarate_Next_Code_For_6Digit(max_code)
                    )
                else:
                    new_department_code = "LDC000001"

                return JsonResponse(
                    {"success": True, "department_code": new_department_code},
                    status=200,
                )
            elif Type == "LabSubDepartment":
                # Fetch all department codes with the specified prefix pattern
                max_code = SubLab_Department_Detials.objects.all().aggregate(
                    Max("SubDepartment_Code")
                )["SubDepartment_Code__max"]
                print("max_code :", max_code)
                if max_code:
                    new_sub_department_code = (
                        Common_Function_For_Genarate_Next_Code_For_6Digit(max_code)
                    )
                else:
                    new_sub_department_code = "LSDC000001"

                return JsonResponse(
                    {"success": True, "Subdepartment_code": new_sub_department_code},
                    status=200,
                )
            elif Type == "UnitMaster":
                # Fetch all department codes with the specified prefix pattern
                max_code = Unit_Masters.objects.all().aggregate(Max("Unit_Code"))[
                    "Unit_Code__max"
                ]
                print("max_code :", max_code)
                if max_code:
                    new_Unit_Code = Common_Function_For_Genarate_Next_Code_For_6Digit(
                        max_code
                    )
                else:
                    new_Unit_Code = "LUC000001"

                return JsonResponse(
                    {"success": True, "unitCode": new_Unit_Code},
                    status=200,
                )
            elif Type == "ContainerMaster":
                # Fetch all department codes with the specified prefix pattern
                max_code = Container_Masters.objects.all().aggregate(
                    Max("Container_Code")
                )["Container_Code__max"]
                print("max_code :", max_code)
                if max_code:
                    new_Container_Code = (
                        Common_Function_For_Genarate_Next_Code_For_6Digit(max_code)
                    )
                else:
                    new_Container_Code = "LCC000001"

                return JsonResponse(
                    {"success": True, "container_code": new_Container_Code},
                    status=200,
                )
            elif Type == "SpecimenMaster":
                # Fetch all department codes with the specified prefix pattern
                max_code = Specimen_Masters.objects.all().aggregate(
                    Max("Specimen_Code")
                )["Specimen_Code__max"]
                print("max_code :", max_code)
                if max_code:
                    new_Specimen_Code = (
                        Common_Function_For_Genarate_Next_Code_For_6Digit(max_code)
                    )
                else:
                    new_Specimen_Code = "LSC000001"

                return JsonResponse(
                    {"success": True, "Specimen_Code": new_Specimen_Code},
                    status=200,
                )
            elif Type == "MethodsMaster":
                # Fetch all department codes with the specified prefix pattern
                max_code = Methods_Masters.objects.all().aggregate(Max("Method_Code"))[
                    "Method_Code__max"
                ]
                print("max_code :", max_code)
                if max_code:
                    new_Method_Code = Common_Function_For_Genarate_Next_Code_For_6Digit(
                        max_code
                    )
                else:
                    new_Method_Code = "LMC000001"

                return JsonResponse(
                    {"success": True, "method_code": new_Method_Code},
                    status=200,
                )
            elif Type == "AntibioticMaster":
                # Fetch the maximum values for anti_biotic_group_code and anti_biotic_code
                max_anti_biotic_group_code = AntibioticMaster.objects.all().aggregate(
                    Max("anti_biotic_group_code")
                )["anti_biotic_group_code__max"]
                max_anti_biotic_code = AntibioticMaster.objects.all().aggregate(
                    Max("anti_biotic_code")
                )["anti_biotic_code__max"]

                print("max_anti_biotic_group_code:", max_anti_biotic_group_code)
                print("max_anti_biotic_code:", max_anti_biotic_code)

                if max_anti_biotic_group_code and max_anti_biotic_code:
                    new_anti_biotic_group_code, new_anti_biotic_code = (
                        get_NextAntibiotic_Code(
                            max_anti_biotic_group_code, max_anti_biotic_code
                        )
                    )
                else:
                    new_anti_biotic_group_code = "AG001"
                    new_anti_biotic_code = "A001"

                data = {
                    "anti_biotic_group_code": new_anti_biotic_group_code,
                    "anti_biotic_code": new_anti_biotic_code,
                }
                return JsonResponse(
                    {"success": True, "data": data},
                    status=200,
                )
            elif Type == "OrganismMaster":
                # Fetch all department codes with the specified prefix pattern
                max_code = Organism_Masters.objects.all().aggregate(
                    Max("Organism_Code")
                )["Organism_Code__max"]
                print("max_code :", max_code)
                if max_code:
                    new_Organism_Code = (
                        Common_Function_For_Genarate_Next_Code_For_6Digit(max_code)
                    )
                else:
                    new_Organism_Code = "LOC000001"

                return JsonResponse(
                    {"success": True, "Organism_Code": new_Organism_Code},
                    status=200,
                )
            elif Type == "LabRemarksData":
                # Fetch all department codes with the specified prefix pattern
                max_code = LabRemarksMaster.objects.all().aggregate(Max("LabRemarkID"))[
                    "LabRemarkID__max"
                ]
                print("max_code :", max_code)
                if max_code:
                    new_LabRemarkID = Common_Function_For_Genarate_Next_Code_For_6Digit(
                        max_code
                    )
                else:
                    new_LabRemarkID = "LRM000001"

                return JsonResponse(
                    {"success": True, "LabRemarkID": new_LabRemarkID},
                    status=200,
                )
            elif Type == "RemarksMaster":
                # Fetch all department codes with the specified prefix pattern
                max_code = Remarks_master.objects.all().aggregate(Max("Remark_Id"))[
                    "Remark_Id__max"
                ]
                print("max_code :", max_code)
                if max_code:
                    new_Remark_Id = Common_Function_For_Genarate_Next_Code_For_6Digit(
                        max_code
                    )
                else:
                    new_Remark_Id = "LRI000001"

                return JsonResponse(
                    {"success": True, "Remark_Id": new_Remark_Id},
                    status=200,
                )
            elif Type == "ReasonMaster":
                # Fetch all department codes with the specified prefix pattern
                max_code = Reason_master.objects.all().aggregate(Max("Reason_Id"))[
                    "Reason_Id__max"
                ]
                print("max_code :", max_code)
                if max_code:
                    new_Reason_Id = Common_Function_For_Genarate_Next_Code_For_6Digit(
                        max_code
                    )
                else:
                    new_Reason_Id = "LRC000001"

                return JsonResponse(
                    {"success": True, "Reason_Id": new_Reason_Id},
                    status=200,
                )
            elif Type == "QualificationMaster":
                # Fetch all department codes with the specified prefix pattern
                max_code = Qualification_master.objects.all().aggregate(
                    Max("Qualification_Id")
                )["Qualification_Id__max"]
                print("max_code :", max_code)
                if max_code:
                    new_Qualification_Id = (
                        Common_Function_For_Genarate_Next_Code_For_6Digit(max_code)
                    )
                else:
                    new_Qualification_Id = "LRC000001"

                return JsonResponse(
                    {"success": True, "Qualification_Id": new_Qualification_Id},
                    status=200,
                )
            elif Type == "TestMaster":
                # Fetch all department codes with the specified prefix pattern
                max_code = Test_Descriptions.objects.all().aggregate(Max("Test_Code"))[
                    "Test_Code__max"
                ]
                print("max_code :", max_code)
                if max_code:
                    new_Test_Code = Genarate_Next_Code_4digit(max_code)
                else:
                    new_Test_Code = "LTC0001"

                return JsonResponse(
                    {"success": True, "TestCode": new_Test_Code},
                    status=200,
                )
            elif Type == "ExternalLabMaster":
                max_code = External_Lab_Master.objects.all().aggregate(Max("LabCode"))[
                    "LabCode__max"
                ]
                print("max_code :", max_code)
                if max_code:
                    new_Lab_Code = Genarate_Next_Code_4digit(max_code)
                else:
                    new_Lab_Code = "LAB0001"

                return JsonResponse(
                    {"success": True, "Lab_Code": new_Lab_Code},
                    status=200,
                )
            elif Type == "ReferDoctorMaster":
                max_code = Refering_Doctor_Details.objects.all().aggregate(
                    Max("DoctorID")
                )["DoctorID__max"]
                print("max_code :", max_code)
                if max_code:
                    new_DoctorID = Genarate_Next_Code_4digit(max_code)
                else:
                    new_DoctorID = "RD0001"

                return JsonResponse(
                    {"success": True, "new_DoctorID": new_DoctorID},
                    status=200,
                )
            elif Type == "GroupMaster":
                # Fetch all department codes with the specified prefix pattern
                max_code = Group_Master.objects.all().aggregate(Max("Group_Code"))[
                    "Group_Code__max"
                ]
 
                if max_code:
                    new_Group_Code = Genarate_Next_Code_4digit(max_code)
                else:
                    new_Group_Code = "LGM0001"

                return JsonResponse(
                    {"success": True, "GroupCode": new_Group_Code},
                    status=200,
                )
            
            else:
                return JsonResponse({"message": "Type Required"})

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return JsonResponse(
                {"success": False, "message": "An internal error occurred."}, status=500
            )


@csrf_exempt
def All_Other_Lab_Masters_POST_AND_GET(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print('data :',data)
            
            if isinstance(data, dict):
                Type = data.get("Type")
            elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                Type = data[0].get("Type")
            else:
                Type = None
            print('Type :',Type)
            
            ResponseMsg = data.get("ResponseMsg")
            
            if Type == "MainDepartment":
                is_edit = data.get('isEdit')
                department_code = data.get('Department_Code')

                if is_edit:
                    try:
                        instance = Lab_Department_Detials.objects.get(Department_Code=department_code)
                        print('instance :', instance)
                        serializers = MainDepartmentSerializer(instance, data=data, partial=True)  # partial=True allows partial updates
                        print('serializers :', serializers)
                        if serializers.is_valid():
                            serializers.save()
                            return JsonResponse({"success": f"{ResponseMsg} Successfully"})
                        else:
                            print('error :', serializers.errors)
                            return JsonResponse(serializers.errors)
                    except Lab_Department_Detials.DoesNotExist:
                        return JsonResponse({"error": "Department not found."})
                else:
                    serializers = MainDepartmentSerializer(data=data)
                    print('serializers :', serializers)
                    if serializers.is_valid():
                        serializers.save()
                        return JsonResponse({"success": f"{ResponseMsg} successfully."})
                    else:
                        print('error :', serializers.errors)
                        return JsonResponse(serializers.errors)
            elif Type == "SubMainDepartment":
                is_edit = data.get('isEdit')
                SubDepartment_Code = data.get('SubDepartment_Code')

                if is_edit:
                    try:
                        # Fetch the existing instance
                        instance = SubLab_Department_Detials.objects.get(SubDepartment_Code=SubDepartment_Code)
                        serializer = SubLabDepartmentSerializer(instance, data=data, partial=True)
                        if serializer.is_valid():
                            serializer.save()
                            return JsonResponse({"success": f"{ResponseMsg} Successfully"})
                        else:
                            print(serializer.errors)
                            return JsonResponse(serializer.errors)
                    except SubLab_Department_Detials.DoesNotExist:
                        return JsonResponse({"error": "Sub Department not found."})
                else:
                    # Handle create case
                    serializer = SubLabDepartmentSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse({"success": f"{ResponseMsg} successfully."})
                    else:
                        return JsonResponse(serializer.errors)
            elif Type == "ContainerMaster":
                is_edit = data.get('isEdit')
                Container_Code = data.get('Container_Code')

                if is_edit:
                    try:
                        instance = Container_Masters.objects.get(Container_Code=Container_Code)
                        print('instance :', instance)
                        serializers = ContainerMastersSerializer(instance, data=data, partial=True)  # partial=True allows partial updates
                        print('serializers :', serializers)
                        if serializers.is_valid():
                            serializers.save()
                            return JsonResponse({"success": f"{ResponseMsg} Successfully"})
                        else:
                            print('error :', serializers.errors)
                            return JsonResponse(serializers.errors)
                    except Container_Masters.DoesNotExist:
                        return JsonResponse({"error": "Department not found."})
                else:
                    serializers = ContainerMastersSerializer(data=data)
                    print('serializers :', serializers)
                    if serializers.is_valid():
                        serializers.save()
                        return JsonResponse({"success": f"{ResponseMsg} successfully."})
                    else:
                        print('error :', serializers.errors)
                        return JsonResponse(serializers.errors)
            elif Type == "UnitMaster":
                is_edit = data.get('isEdit')
                Unit_Code = data.get('Unit_Code')

                if is_edit:
                    try:
                        instance = Unit_Masters.objects.get(Unit_Code=Unit_Code)
                        serilizer = UnitMasterSerilizer(instance,data=data,partial=True)
                        if serilizer.is_valid():
                            serilizer.save()
                            return JsonResponse({"success":f"{ResponseMsg} Successfully"})
                        else:
                            return JsonResponse(serializer.errors)
                    except Unit_Masters.DoesNotExist:
                        return JsonResponse({"warn":"Unit Not Found"})
                else:
                    serilizer = UnitMasterSerilizer(data=data)
                    if serilizer.is_valid():
                        serilizer.save()
                        return JsonResponse({"success":f"{ResponseMsg} Successfully"})
                    else:
                        return JsonResponse(serilizer.errors)             
            elif Type == "SpecimenMaster":
                is_edit = data.get('isEdit')
                Specimen_Code = data.get('Specimen_Code')

                if is_edit:
                    try:
                        instance = Specimen_Masters.objects.get(Specimen_Code=Specimen_Code)
                        print('instance :', instance)
                        serializers = SpecimenMasterSerializer(instance, data=data, partial=True)  # partial=True allows partial updates
                        print('serializers :', serializers)
                        if serializers.is_valid():
                            serializers.save()
                            return JsonResponse({"success": f"{ResponseMsg} Successfully"})
                        else:
                            print('error :', serializers.errors)
                            return JsonResponse(serializers.errors)
                    except Container_Masters.DoesNotExist:
                        return JsonResponse({"error": "Specimen not found."})
                else:
                    serializers = SpecimenMasterSerializer(data=data)
                    print('serializers :', serializers)
                    if serializers.is_valid():
                        serializers.save()
                        return JsonResponse({"success": f"{ResponseMsg} successfully."})
                    else:
                        print('error :', serializers.errors)
                        return JsonResponse(serializers.errors)
            elif Type == "MethodsMaster":
                is_edit = data.get('isEdit')
                Method_Code = data.get('Method_Code')

                if is_edit:
                    try:
                        instance = Methods_Masters.objects.get(Method_Code=Method_Code)
                        serilizer = MethodMasterSerializer(instance,data=data,partial=True)
                        if serilizer.is_valid():
                            serilizer.save()
                            return JsonResponse({"success": f"{ResponseMsg} Successfully"})
                        else:
                            return JsonResponse(serilizer.errors)
                    except Methods_Masters.DoesNotExist:
                        return JsonResponse({"warn":"Method Not Found"})
                else:
                    serializer = MethodMasterSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse({"success": f"{ResponseMsg} Successfullly"})
                    else:
                        return JsonResponse(serializer.errors)                 
            elif Type == "AntibioticMaster":
                is_edit = data.get('isEdit')
                anti_biotic_group_code = data.get('anti_biotic_group_code')
                anti_biotic_code = data.get("anti_biotic_code")
                print('is_edit :',is_edit)
                if is_edit:
                    try:
                        instance = AntibioticMaster.objects.get(anti_biotic_code=anti_biotic_code,anti_biotic_group_code=anti_biotic_group_code)
                        serializer = AntibioticMasterSerializer(instance,data=data,partial=True)
                        if serializer.is_valid():
                            serializer.save()
                            return JsonResponse({"success": f"{ResponseMsg} Successfully"})
                        else:
                            print('wrro :',serializer.errors)
                            return JsonResponse(serializer.errors)
                    except AntibioticMaster.DoesNotExist:
                        return JsonResponse({"warn": "Antiobiotic Not Found"})
                else:
                    last_anti_biotic_id = AntibioticMaster.objects.aggregate(
                    Max("anti_biotic_id")
                    )["anti_biotic_id__max"]
                    next_anti_biotic_id = 1 if last_anti_biotic_id is None else int(last_anti_biotic_id) + 1

                    data["anti_biotic_id"] = next_anti_biotic_id
                    
                    instance = AntibioticMasterSerializer(data=data)
                    if instance.is_valid():
                        instance.save()
                        return JsonResponse({"success": f"{ResponseMsg} Successfully"})
                    else:
                        print('error :',instance.errors)
                        return JsonResponse(instance.errors)

            elif Type == "OrganismMaster":
                is_edit = data.get('isEdit')
                Organism_Code = data.get('Organism_Code')
                
                if is_edit:
                    try:
                        exist_instance = Organism_Masters.objects.get(Organism_Code=Organism_Code)
                        serializer = OrganismMasterSerializer(exist_instance,data=data,partial=True)
                        if serializer.is_valid():
                            serializer.save()
                            return JsonResponse({"success": f"{ResponseMsg} Successfully"})
                        else:
                            return JsonResponse({"warn":serializer.errors})   
                    except Organism_Masters.DoesNotExist:
                        return JsonResponse({"warn": "Organism Not Found"})
                else:
                    new_instance = OrganismMasterSerializer(data=data)
                    if new_instance.is_valid():
                        new_instance.save()
                        return JsonResponse({"success": f"{ResponseMsg} Successfully"}) 
                    else:
                        return JsonResponse({"warn": new_instance.errors})            
                
            elif Type == "LabRemarksData":
                # Get department data from the request
                LabRemarks = data.get("LabRemarks")
                LabRemarkID = data.get("LabRemarkID")
                createdby = data.get("createdby")
                Department = data.get("Department")

                if not LabRemarks or not LabRemarkID:
                    return JsonResponse(
                        {
                            "success": False,
                            "message": "Organism name and code are required.",
                        },
                        status=400,
                    )

                # Check if a department with the same code exists
                existing_Remark = LabRemarksMaster.objects.filter(
                    LabRemarkID=LabRemarkID
                ).first()
                if existing_Remark:
                    # Update existing record
                    existing_Remark.LabRemarks = LabRemarks
                    existing_Remark.Department = Department
                    existing_Remark.save()
                    message = "LabRemarks updated successfully."
                else:
                    # Create new record
                    LabRemarksMaster.objects.create(
                        LabRemarkID=LabRemarkID,
                        Department=Department,
                        LabRemarks=LabRemarks,
                        created_by=createdby,
                    )
                    message = "New LabRemarks created successfully."

                return JsonResponse({"success": True, "message": message}, status=200)
            elif Type == "RemarksMaster":
                is_edit = data.get('isEdit')
                Remark_Id = data.get('Remark_Id')
                
                
                if is_edit:
                    try:
                        exist_instance = Remarks_master.objects.get(Remark_Id=Remark_Id)
                        serializer = RemarksMasterSerializer(exist_instance,data=data,partial=True)
                        if serializer.is_valid():
                            serializer.save()
                            return JsonResponse({"success": f"{ResponseMsg} Successfully"})
                        else:
                            return JsonResponse({"warn":serializer.errors})   
                    except Remarks_master.DoesNotExist:
                        return JsonResponse({"warn": "Remark Not Found"})
                else:
                    new_instance = RemarksMasterSerializer(data=data)
                    if new_instance.is_valid():
                        new_instance.save()
                        return JsonResponse({"success": f"{ResponseMsg} Successfully"}) 
                    else:
                        return JsonResponse({"warn": new_instance.errors}) 
            elif Type == "ReasonMaster":
                # Get department data from the request
                ReasonId = data.get("ReasonID")
                Reason = data.get("Reason")
                createdby = data.get("createdby")

                if not ReasonId or not Reason:
                    return JsonResponse(
                        {
                            "success": False,
                            "message": "Reason and Id are required.",
                        },
                        status=400,
                    )

                # Check if a department with the same code exists
                existing_Reason = Reason_master.objects.filter(
                    Reason_Id=ReasonId
                ).first()

                if existing_Reason:
                    # Update existing record
                    existing_Reason.Reason = Reason
                    existing_Reason.save()
                    message = "Reason updated successfully."
                else:
                    # Create new record
                    Reason_master.objects.create(
                        Reason_Id=ReasonId,
                        Reason=Reason,
                        created_by=createdby,
                    )
                    message = "New Reason created successfully."

                return JsonResponse({"success": True, "message": message}, status=200)
            elif Type == "QualificationMaster":
                # Get department data from the request
                QualificationId = data.get("QualificationID")
                Qualification = data.get("Qualification")
                createdby = data.get("createdby")

                if not QualificationId or not Qualification:
                    return JsonResponse(
                        {
                            "success": False,
                            "message": "Qualification and Id are required.",
                        },
                        status=400,
                    )

                # Check if a department with the same code exists
                existing_Qualification = Qualification_master.objects.filter(
                    Qualification_Id=QualificationId
                ).first()

                existing_Qualification_name = Qualification_master.objects.filter(
                    Qualification=Qualification
                ).first()

                if existing_Qualification:

                    if existing_Qualification_name:
                        print(f"The {Qualification} name already exists.")
                        message = f"The {Qualification} name already exists."
                        success = False
                    else:

                        # Update existing record
                        existing_Qualification.Qualification = Qualification
                        existing_Qualification.save()
                        message = "Qualification updated successfully."
                        success = True

                elif existing_Qualification_name:

                    message = f"The {Qualification} name already exists."
                    success = False
                else:
                    # Create new record
                    Qualification_master.objects.create(
                        Qualification_Id=QualificationId,
                        Qualification=Qualification,
                        created_by=createdby,
                    )
                    message = "New Qualification created successfully."
                    success = True

                return JsonResponse({"success": success, "message": message})
            elif Type == "ExternalLabMaster":
                labName = data.get("labName")
                address = data.get("address")
                email = data.get("email")
                registerNo = data.get("registerNo")
                phoneNumber = data.get("phoneNumber")
                pincode = data.get("pincode")
                referenceCode = data.get("referenceCode")
                source = data.get("source")
                location = data.get("location")
                created_by = data.get("createdby")
                IsEditMode = data.get("IsEditMode")
                labcode = data.get("labCode")  # Assuming labcode is passed
                Status = "Active"
                # Check if labcode is provided

                if not labcode:
                    return JsonResponse(
                        {"success": False, "message": "Lab Code Required"}
                    )
                print('IsEditMode :',IsEditMode)
                if IsEditMode:
                    External_Client_Master_ins = External_Lab_Master.objects.get(
                        LabCode=labcode
                    )
                    External_Client_Master_ins.LabName = labName
                    External_Client_Master_ins.RegisterNo = registerNo
                    External_Client_Master_ins.Address = address
                    External_Client_Master_ins.Email = email
                    External_Client_Master_ins.PhoneNo = phoneNumber
                    External_Client_Master_ins.Pincode = pincode
                    External_Client_Master_ins.ReferenceCode = referenceCode
                    External_Client_Master_ins.Location = location
                    External_Client_Master_ins.SourceType = source
                    External_Client_Master_ins.save()
                    message = {
                        "success": True,
                        "message": "Lab Details Updated successfully",
                    }

                else:
                    if External_Lab_Master.objects.filter(LabCode=labcode).exists():
                        External_Client_Master_ins = External_Lab_Master.objects.get(
                            LabCode=labcode
                        )
                        External_Client_Master_ins.LabName = labName
                        External_Client_Master_ins.RegisterNo = registerNo
                        External_Client_Master_ins.Address = address
                        External_Client_Master_ins.Email = email
                        External_Client_Master_ins.PhoneNo = phoneNumber
                        External_Client_Master_ins.Pincode = pincode
                        External_Client_Master_ins.ReferenceCode = referenceCode
                        External_Client_Master_ins.Location = location
                        External_Client_Master_ins.SourceType = source
                        External_Client_Master_ins.save()
                        message = {
                            "success": True,
                            "message": "Lab Details Updated successfully",
                        }
                    else:
                        External_Client_Master_ins = External_Lab_Master(
                            LabCode=labcode,
                            LabName=labName,
                            RegisterNo=registerNo,
                            Address=address,
                            Email=email,
                            PhoneNo=phoneNumber,
                            Pincode=pincode,
                            ReferenceCode=referenceCode,
                            Location=location,
                            SourceType=source,
                            created_by=created_by,
                            Status=Status,
                        )

                        column_name = f"{labcode}"  # Generate a unique column name
                        with connection.cursor() as cursor:
                            # Add the new column with default value 0.000 after the 'Basic' column
                            cursor.execute(
                                f"""
        ALTER TABLE Testmaster_Cost_List
        ADD COLUMN {column_name} DECIMAL(10,3) DEFAULT 0.000
        AFTER Basic;
        """
                            )

                        External_Client_Master_ins.save()
                        message = {
                            "success": True,
                            "message": "New Lab Created successfully",
                        }

                return JsonResponse(message)
            elif Type == "ReferDoctorMaster":
                DoctorName = data.get("doctorname")
                Title = data.get("title")
                Qualification1 = data.get("Qualification")
                DoctorType = data.get("doctortype")
                PhoneNo = data.get("phone")
                Commission_per = data.get("commission")
                PaymentType = data.get("PaymentType")
                Address = data.get("address1")
                Address2 = data.get("address2")
                Status = "Active"
                created_by = data.get("createdby")
                BankName = data.get("Bankname")
                HolderName = data.get("HolderName")
                AccountNo = data.get("AccNumber")
                DoctorID = data.get("DoctorID")
                IsEditMode = data.get("isEdit")

                if not DoctorID:
                    return JsonResponse(
                        {"success": False, "message": "DoctorID Required"}
                    )

                Qualification2 = Qualification_master.objects.filter(
                    Qualification_Id=Qualification1
                ).first()

                print("DoctorID :", DoctorID)
                if IsEditMode == True:
                    ReferDoctorMaster_ins = Refering_Doctor_Details.objects.get(
                        DoctorID=DoctorID
                    )
                    print("ReferDoctorMaster_ins :", ReferDoctorMaster_ins)
                    ReferDoctorMaster_ins.Title = Title
                    ReferDoctorMaster_ins.DoctorName = DoctorName
                    ReferDoctorMaster_ins.Qualification = Qualification2
                    ReferDoctorMaster_ins.DoctorType = DoctorType
                    ReferDoctorMaster_ins.PhoneNo = PhoneNo
                    ReferDoctorMaster_ins.Commission_per = Commission_per
                    ReferDoctorMaster_ins.PaymentType = PaymentType
                    ReferDoctorMaster_ins.BankName = BankName
                    ReferDoctorMaster_ins.HolderName = HolderName
                    ReferDoctorMaster_ins.AccountNo = AccountNo
                    ReferDoctorMaster_ins.Address = Address
                    ReferDoctorMaster_ins.Address2 = Address2
                    ReferDoctorMaster_ins.save()
                    message = {
                        "success": True,
                        "message": "Refer Doctor Updated successfully",
                    }

                else:
                    if Refering_Doctor_Details.objects.filter(
                        DoctorID=DoctorID
                    ).exists():
                        ReferDoctorMaster_ins = Refering_Doctor_Details.objects.get(
                            DoctorID=DoctorID
                        )
                        ReferDoctorMaster_ins.Title = Title
                        ReferDoctorMaster_ins.DoctorName = DoctorName
                        ReferDoctorMaster_ins.Qualification = Qualification2
                        ReferDoctorMaster_ins.DoctorType = DoctorType
                        ReferDoctorMaster_ins.PhoneNo = PhoneNo
                        ReferDoctorMaster_ins.Commission_per = Commission_per
                        ReferDoctorMaster_ins.PaymentType = PaymentType
                        ReferDoctorMaster_ins.BankName = BankName
                        ReferDoctorMaster_ins.HolderName = HolderName
                        ReferDoctorMaster_ins.AccountNo = AccountNo
                        ReferDoctorMaster_ins.Address = Address
                        ReferDoctorMaster_ins.Address2 = Address2
                        ReferDoctorMaster_ins.save()
                        message = {
                            "success": True,
                            "message": "Refer Doctor Updated successfully",
                        }
                    else:
                        ReferDoctorMaster_ins = Refering_Doctor_Details(
                            DoctorID=DoctorID,
                            Title=Title,
                            DoctorName=DoctorName,
                            Qualification=Qualification2,
                            DoctorType=DoctorType,
                            PhoneNo=PhoneNo,
                            Commission_per=Commission_per,
                            PaymentType=PaymentType,
                            BankName=BankName,
                            HolderName=HolderName,
                            AccountNo=AccountNo,
                            Address=Address,
                            Address2=Address2,
                            Status=Status,
                            created_by=created_by,
                        )

                        ReferDoctorMaster_ins.save()
                        message = {
                            "success": True,
                            "message": "Doctor Registered successfully",
                        }

                return JsonResponse(message)
            elif Type == "TestMaster":
                # Get department data from the request
                testName = data.get("testName")
                testCode = data.get("testCode")

                department = data.get("department")
                departmentcode = data.get("departmentcode")
                department1 = Lab_Department_Detials.objects.filter(
                    Department_Code=departmentcode
                ).first()

                subdepartment = data.get("subdepartment")
                subdepartmentcode = data.get("subdepartmentcode")
                subdepartment1 = SubLab_Department_Detials.objects.filter(
                    SubDepartment_Code=subdepartmentcode
                ).first()

                header = data.get("header")
                displayText = data.get("displayText")
                billingName = data.get("billingName")
                container = data.get("container")
                containercode = data.get("containercode")
                container1 = Container_Masters.objects.filter(
                    Container_Code=containercode
                ).first()

                specimen = data.get("specimen")
                specimencode = data.get("specimencode")
                specimen1 = Specimen_Masters.objects.filter(
                    Specimen_Code=specimencode
                ).first()
                method = data.get("method")
                methodcode = data.get("methodcode")
                method1 = Methods_Masters.objects.filter(Method_Code=methodcode).first()

                gender = data.get("gender")
                inputType = data.get("inputType")
                decimalPlaces = data.get("decimalPlaces")
                decimalPlaces1 = decimalPlaces if decimalPlaces != "" else 0
                inputPatternType = data.get("inputPatternType")
                testCategory = data.get("testCategory")
                logicalCategory = data.get("logicalCategory")
                capturedUnit = data.get("capturedUnit")
                capturedUnit1 = capturedUnit if capturedUnit != "" else None
                uom = data.get("uom")
                uomcode = data.get("uomcode")

                uom1 = Unit_Masters.objects.filter(Unit_Code=uomcode).first()

                reportType = data.get("reportType")
                testInstruction = data.get("testInstruction")
                loincCode = data.get("loincCode")
                allowDiscount = data.get("allowDiscount")
                orderable = data.get("orderable")
                showGraph = data.get("showGraph")
                stat = data.get("stat")
                nonReportable = data.get("nonReportable")
                calculatedTest = data.get("calculatedTest")
                isOutsourced = data.get("isOutsourced")
                minimumtime = data.get("minimumtime")
                Emergencytime = data.get("Emergencytime")
                timeperiod = data.get("timeperiod")
                formula = data.get("formula")
                paraone = data.get("paraone")
                paratwo = data.get("paratwo")
                Culturetest = data.get("Culturetest")
                Checkout = data.get("Checkout")
                isNABHL = data.get("isNABHL")
                isCAP = data.get("isCAP")
                is_Machine_Interfaced = data.get("is_Machine_Interfaced")
                Reagentlevel = data.get("Reagentlevel")
                AssayCode = data.get("AssayCode")
                IsSubTest = data.get("IsSubTest")
                SubTestCodes = data.get("SubTestCodes")
                Captured_Unit_UOM = data.get("Captured_Unit_UOM")
                created_by = data.get("created_by")

                # Check if a department with the same code exists
                existing_Test_Descriptions = Test_Descriptions.objects.filter(
                    Test_Code=testCode
                ).first()

                if existing_Test_Descriptions:
                    existing_Test_Descriptions.Test_Name = (testName,)
                    existing_Test_Descriptions.department = (department,)
                    existing_Test_Descriptions.sub_department = (subdepartment,)
                    existing_Test_Descriptions.Header = (header,)
                    existing_Test_Descriptions.Billing_Name = (billingName,)
                    existing_Test_Descriptions.DisplayText = (displayText,)
                    existing_Test_Descriptions.Container_Name = (container,)
                    existing_Test_Descriptions.Specimen_Name = (specimen,)
                    existing_Test_Descriptions.Method_Name = (method,)
                    existing_Test_Descriptions.Gender = (gender,)
                    existing_Test_Descriptions.Input_Type = (inputType,)
                    existing_Test_Descriptions.Decimal_Palces = (decimalPlaces1,)
                    existing_Test_Descriptions.Input_Pattern_Type = (inputPatternType,)
                    existing_Test_Descriptions.Test_Category = (testCategory,)
                    existing_Test_Descriptions.Logical_Category = (logicalCategory,)
                    existing_Test_Descriptions.Captured_Unit = (capturedUnit1,)
                    existing_Test_Descriptions.Captured_Unit_UOM = (Captured_Unit_UOM,)
                    existing_Test_Descriptions.UOM = (uom,)
                    existing_Test_Descriptions.Report_Type = (reportType,)
                    existing_Test_Descriptions.Test_InstdisplayTextructions = (
                        testInstruction,
                    )
                    existing_Test_Descriptions.Loinc_Code = (loincCode,)
                    existing_Test_Descriptions.Allow_Discount = (allowDiscount,)
                    existing_Test_Descriptions.Oderable = (orderable,)
                    existing_Test_Descriptions.Show_Graph = (showGraph,)
                    existing_Test_Descriptions.STAT = (stat,)
                    existing_Test_Descriptions.Non_Reportable = (nonReportable,)
                    existing_Test_Descriptions.Calculated_Test = (calculatedTest,)
                    existing_Test_Descriptions.Outsourced = (isOutsourced,)
                    existing_Test_Descriptions.Processing_Time = (minimumtime,)
                    existing_Test_Descriptions.Emergency_Processing_Time = (
                        Emergencytime,
                    )
                    existing_Test_Descriptions.Period_Type = (timeperiod,)
                    existing_Test_Descriptions.Formula = (formula,)
                    existing_Test_Descriptions.Routine = (paraone,)
                    existing_Test_Descriptions.TimeGap = (paratwo,)
                    existing_Test_Descriptions.Autocheck = (Checkout,)
                    existing_Test_Descriptions.Culturetest = (Culturetest,)
                    existing_Test_Descriptions.Is_NABHL = (isNABHL,)
                    existing_Test_Descriptions.Is_CAP = (isCAP,)
                    existing_Test_Descriptions.Is_Machine_Interfaced = (
                        is_Machine_Interfaced,
                    )
                    existing_Test_Descriptions.Machine_Name = (None,)
                    existing_Test_Descriptions.Assay_Code = (AssayCode,)
                    existing_Test_Descriptions.IsSubTest = (IsSubTest,)
                    existing_Test_Descriptions.SubTestCodes = (SubTestCodes,)
                    existing_Test_Descriptions.created_by = (created_by,)
                    existing_Test_Descriptions.save()
                    message = "Test updated successfully."
                else:

                    with transaction.atomic():
                        # Insert into Test_Descriptions
                        test_description = Test_Descriptions.objects.create(
                            Test_Code=testCode,
                            Test_Name=testName,
                            department=department1,
                            sub_department=subdepartment1,
                            Header=header,
                            Billing_Name=billingName,
                            DisplayText=displayText,
                            Container_Name=container1,
                            Specimen_Name=specimen1,
                            Method_Name=method1,
                            Gender=gender,
                            Input_Type=inputType,
                            Decimal_Palces=decimalPlaces1,
                            Input_Pattern_Type=inputPatternType,
                            Test_Category=testCategory,
                            Logical_Category=logicalCategory,
                            Captured_Unit=capturedUnit1,
                            Captured_Unit_UOM=Captured_Unit_UOM,
                            UOM=uom1,
                            Report_Type=reportType,
                            Test_Instructions=testInstruction,
                            Loinc_Code=loincCode,
                            Allow_Discount=allowDiscount,
                            Oderable=orderable,
                            Show_Graph=showGraph,
                            STAT=stat,
                            Non_Reportable=nonReportable,
                            Calculated_Test=calculatedTest,
                            Outsourced=isOutsourced,
                            Processing_Time=minimumtime,
                            Emergency_Processing_Time=Emergencytime,
                            Period_Type=timeperiod,
                            Formula=formula,
                            Routine=paraone,
                            TimeGap=paratwo,
                            Autocheck=Checkout,
                            Culturetest=Culturetest,
                            Is_NABHL=isNABHL,
                            Is_CAP=isCAP,
                            Is_Machine_Interfaced=is_Machine_Interfaced,
                            Machine_Name=None,
                            Assay_Code=AssayCode,
                            Status="Active",
                            IsSubTest=IsSubTest,
                            SubTestCodes=SubTestCodes,
                            ResultValues=None,
                            created_by=created_by,
                        )

                        # Prepare default data for other tables
                        test_name = test_description.Test_Name
                        test_code = test_description.Test_Code

                        test_description_instance = Test_Descriptions.objects.get(
                            Test_Code=test_code
                        )

                        Testmaster_Remarks_Test_Id = (
                            Testmaster_Remarks.objects.aggregate(Max("Test_Id"))[
                                "Test_Id__max"
                            ]
                        )
                        next_Testmaster_Remarks_Test_Id = (
                            1
                            if Testmaster_Remarks_Test_Id is None
                            else int(Testmaster_Remarks_Test_Id) + 1
                        )

                        # Insert into Testmaster_Remarks
                        Testmaster_Remarks.objects.create(
                            Test_Id=next_Testmaster_Remarks_Test_Id,
                            Test_Code=test_description_instance,
                            # Test_Name=test_name,
                            Validation=None,
                            Remark_Type=None,
                            Remark=None,
                            created_by=created_by,
                        )

                        Testmaster_Reference_Range_Test_Id = (
                            Testmaster_Reference_Range.objects.aggregate(
                                Max("Test_Id")
                            )["Test_Id__max"]
                        )
                        next_Testmaster_Reference_Range_Test_Id = (
                            1
                            if Testmaster_Reference_Range_Test_Id is None
                            else int(Testmaster_Reference_Range_Test_Id) + 1
                        )

                        # Insert into Testmaster_Reference_Range
                        Testmaster_Reference_Range.objects.create(
                            Test_Id=next_Testmaster_Reference_Range_Test_Id,
                            Test_Code=test_description_instance,
                            # Test_Name=test_name,
                            Analizer_Type=None,
                            validation=None,
                            Method_Type=None,
                            Gender="Both",
                            Range_Lower_Limit=None,
                            Range_Higher_Limit=None,
                            Reference_Range_Text=None,
                            created_by=created_by,
                        )

                        Testmaster_Cost_List_Test_Id = (
                            Testmaster_Cost_List.objects.aggregate(Max("Test_Id"))[
                                "Test_Id__max"
                            ]
                        )
                        next_Testmaster_Cost_List_Test_Id = (
                            1
                            if Testmaster_Cost_List_Test_Id is None
                            else int(Testmaster_Cost_List_Test_Id) + 1
                        )

                        # Insert into Cost_List_Table
                        Testmaster_Cost_List.objects.create(
                            Test_Id=next_Testmaster_Cost_List_Test_Id,
                            Test_Code=test_description_instance,
                            # Test_Name=test_name,
                            Basic=0,
                            created_by=created_by,
                        )

                        Testmaster_Rule_Based_Test_Id = (
                            Testmaster_Rule_Based.objects.aggregate(Max("Test_Id"))[
                                "Test_Id__max"
                            ]
                        )
                        next_Testmaster_Rule_Based_Test_Id = (
                            1
                            if Testmaster_Rule_Based_Test_Id is None
                            else int(Testmaster_Rule_Based_Test_Id) + 1
                        )

                        Testmaster_Rule_Based.objects.create(
                            Test_Id=next_Testmaster_Rule_Based_Test_Id,
                            Test_Code=test_description_instance,
                            # Test_Name=test_name,
                            Validation_type=None,
                            Gender=None,
                            Rule_Type=None,
                            Remark=None,
                            created_by=created_by,
                        )

                        Testmaster_Interpretation_table_Test_Id = (
                            Testmaster_Interpretation_table.objects.aggregate(
                                Max("Test_Id")
                            )["Test_Id__max"]
                        )
                        next_Testmaster_Interpretation_table_Test_Id = (
                            1
                            if Testmaster_Interpretation_table_Test_Id is None
                            else int(Testmaster_Interpretation_table_Test_Id) + 1
                        )

                        Testmaster_Interpretation_table.objects.create(
                            Test_Id=next_Testmaster_Interpretation_table_Test_Id,
                            Test_Code=test_description_instance,
                            # Test_Name=test_name,
                            Header_interpretation=None,
                            Comments=None,
                            created_by=created_by,
                        )

                        Testmaster_Reflex_Test_Test_Id = (
                            Testmaster_Reflex_Test.objects.aggregate(Max("Test_Id"))[
                                "Test_Id__max"
                            ]
                        )
                        next_Testmaster_Reflex_Test_Test_Id = (
                            1
                            if Testmaster_Reflex_Test_Test_Id is None
                            else int(Testmaster_Reflex_Test_Test_Id) + 1
                        )

                        Testmaster_Reflex_Test.objects.create(
                            Test_Id=next_Testmaster_Reflex_Test_Test_Id,
                            Test_Code=test_description_instance,
                            # Test_Name=test_name,
                            Reflex_Test=None,
                            Reflex_Code=None,
                            created_by=created_by,
                        )

                        Testmaster_Age_Setup_Master = (
                            Age_Setup_Master.objects.aggregate(Max("Test_Id"))[
                                "Test_Id__max"
                            ]
                        )
                        next_Testmaster_Age_Setup_Master = (
                            1
                            if Testmaster_Age_Setup_Master is None
                            else int(Testmaster_Age_Setup_Master) + 1
                        )

                        # Insert into Age_Setup_Master
                        Age_Setup_Master.objects.create(
                            Test_Id=next_Testmaster_Age_Setup_Master,
                            Test_Code=test_description_instance,
                            # Test_Name=test_name,
                            Gender="Both",
                            FromAge=None,
                            FromAgeType=None,
                            Toage=None,
                            ToAgeType=None,
                            From_Value=None,
                            To_Value=None,
                            PanicLow=None,
                            PanicHigh=None,
                            NormalValue=None,
                            Reference_Range=None,
                            created_by=created_by,
                        )

                    message = "New Test created successfully."

                return JsonResponse({"success": True, "message": message}, status=200)
            elif Type == "DepartmentOrderMaster":

                with connection.cursor() as cursor:
                    cursor.execute("TRUNCATE TABLE DepartmentOrderMaster")
                for order in data:
                    DepartmentOrderMaster_S_No = DepartmentOrderMaster.objects.aggregate(
                    Max("S_No")
                    )["S_No__max"]
                    print('DepartmentOrderMaster_S_No :',DepartmentOrderMaster_S_No)
                    next_DepartmentOrderMaster_S_No = (
                        1
                        if DepartmentOrderMaster_S_No is None
                        else int(DepartmentOrderMaster_S_No) + 1
                    )
                    print('next_DepartmentOrderMaster_S_No :',next_DepartmentOrderMaster_S_No)
                    # Get or create SubLab_Department_Detials
                    subdepartment_code = order.get("SubDepartment_Code")
                    CreatedBy = order.get("created_by")
                    DepartmentOrderID = order.get("OrderID")

                    subdepartment = SubLab_Department_Detials.objects.filter(
                        SubDepartment_Code=subdepartment_code
                    ).first()

                    # Insert into DepartmentOrderMaster
                    DepartmentOrderMaster.objects.create(
                        S_No=next_DepartmentOrderMaster_S_No,
                        SubDepartment_Code=subdepartment,  # Foreign key relationship
                        OrderID=DepartmentOrderID,
                        created_by=CreatedBy,
                    )
                    

                    message = {"success": True, "message": "Saved Successfully"}
                return JsonResponse(message)
            elif Type == "RateCardMasterUpdate":
                # Get department data from the request
                TestCode = data.get("TestCode")
                TestName = data.get("TestName")
                Basic = data.get("Basic")
                updateamount = data.get("updateamount")
                columnname = data.get("franchaisename")  # columnname is dynamic

                if not TestCode or not columnname or not updateamount:
                    return JsonResponse(
                        {
                            "success": False,
                            "message": "TestCode, Franchise Name, and Update Amount are required.",
                        },
                        status=400,
                    )

                # Check if a department with the same code exists
                print('TestCode :',TestCode)
                if "LTC" in TestCode:
                    existing_data = Testmaster_Cost_List.objects.filter(Test_Code_id=TestCode).first()
                    wherecolumn = "Test_Code_id"
                elif "LGM" in TestCode:
                    existing_data = Testmaster_Cost_List.objects.filter(Group_Code_id=TestCode).first()
                    wherecolumn = "Group_Code_id"
                if not existing_data:
                    return JsonResponse(
                        {
                            "success": False,
                            "message": f"TestCode {TestCode} not found.",
                        },
                        status=404,
                    )

                with connection.cursor() as cursor:
                    cursor.execute("SHOW COLUMNS FROM Testmaster_Cost_List")
                    columns = cursor.fetchall()
                    column_names = [column[0] for column in columns]
                    print('column_names :',column_names)
                    # Check if the column exists
                    if columnname not in column_names:
                        return JsonResponse(
                                {
                                    "success": False,
                                    "message": f"Invalid field name: {columnname}.",
                                })
                        
                with connection.cursor() as cursor:
                    # Prepare the SQL query dynamically with the column name and value
                    query = f"""
                        UPDATE Testmaster_Cost_List
                        SET {columnname} = %s
                        WHERE {wherecolumn} = %s
                    """
                    cursor.execute(query, [updateamount, TestCode])

                message = "Amount updated successfully."
                success = True

                return JsonResponse(
                    {"success": success, "message": message},
                    status=200 if success else 400,
                )
            elif Type == "GroupMaster":
                
                Test_datas = data.get("selectedtest",[])
                groupCode = data.get('groupCode')
                groupName = data.get("groupName")
                displayName = data.get("displayName")
                billingCode = data.get("billingCode")
                billingName = data.get("billingName")
                gender = data.get("gender")
                reportType = data.get("reportType")
                SubDepartment_Code = data.get("SubDepartment_Code")
                testCategory = data.get("testCategory")
                logicalCategory = data.get("logicalCategory")
                authorizedUser = data.get("authorizedUser")
                lonicCode = data.get("lonicCode")
                groupCost = data.get('groupCost')
                created_by = data.get("created_by")
                isEditMode = data.get('isEditMode')
                
                
                
                existing_Group = Group_Master.objects.filter(
                    Group_Code=groupCode
                ).first()
                
                DepartmentDetails = SubLab_Department_Detials.objects.filter(
                        SubDepartment_Code=SubDepartment_Code
                    ).first()

                    
                if existing_Group:
                    # Update existing record
                    existing_Group.Group_Name = groupName
                    existing_Group.Display_Name = displayName
                    existing_Group.Billing_Code = billingCode
                    existing_Group.Billing_Name = billingName
                    existing_Group.Gender = gender
                    existing_Group.Report_Type = reportType                    
                    existing_Group.Department = DepartmentDetails                    
                    existing_Group.Test_Category = testCategory  
                    existing_Group.Logical_Category = logicalCategory                    
                    existing_Group.AutoAuthorized_User = authorizedUser
                    existing_Group.Lonic_Code = lonicCode            
                    existing_Group.created_by = created_by
                    
                    existing_Group.save()
                   
                else:
                    # Create new record
                    Group_Master.objects.create(
                    Group_Code = groupCode,
                    Group_Name = groupName,
                    Display_Name = displayName,
                    Billing_Code = billingCode,
                    Billing_Name = billingName,
                    Gender = gender,
                    Report_Type = reportType,               
                    Department = DepartmentDetails,                    
                    Test_Category = testCategory,  
                    Logical_Category = logicalCategory,                    
                    AutoAuthorized_User = authorizedUser,
                    Lonic_Code = lonicCode,     
                    Status = "Active",
                    created_by = created_by,
                    )

                
                
                if isEditMode is True:
                    with connection.cursor() as cursor:
                        query = "DELETE FROM Group_Master_TestList WHERE Group_Code_id = %s"
                        cursor.execute(query, (groupCode,))
                        connection.commit()  
                    message = {"success": True, "message": "updated Successfully"}
                else:
                    message = {"success": True, "message": "Saved Successfully"}

                    
                for Test in Test_datas:
                    group_code = Test.get("group_code")
                    Test_Code = Test.get("Test_Code")
                    
                    
                    Group_Master_TestList_S_No = Group_Master_TestList.objects.aggregate(
                    Max("Group_Master_TestList_Id")
                    )["Group_Master_TestList_Id__max"]
                    next_Group_Master_TestList_S_No = (
                        1
                        if Group_Master_TestList_S_No is None
                        else int(Group_Master_TestList_S_No) + 1
                    )
                    # Get or create SubLab_Department_Detials


                    GroupDetails = Group_Master.objects.filter(
                        Group_Code=group_code
                    ).first()

                    TestDetails = Test_Descriptions.objects.filter(
                        Test_Code=Test_Code
                    ).first()
                    
                    # Insert into DepartmentOrderMaster
                    Group_Master_TestList.objects.create(
                        Group_Master_TestList_Id=next_Group_Master_TestList_S_No,
                        Group_Code=GroupDetails,  # Foreign key relationship
                        Test_Code=TestDetails,
                        created_by=created_by,
                    )
                    

                    
                

                print('groupCode :',groupCode)
                existing_data1 = Testmaster_Cost_List.objects.filter(Group_Code=groupCode).first()
                print('existing_data1 :',existing_data1)
                
                Testmaster_Cost_List_Test_Id = (
                            Testmaster_Cost_List.objects.aggregate(Max("Test_Id"))[
                                "Test_Id__max"
                            ]
                        )
                next_Testmaster_Cost_List_Test_Id = (
                            1
                            if Testmaster_Cost_List_Test_Id is None
                            else int(Testmaster_Cost_List_Test_Id) + 1
                        )

                Group_Master_instance = Group_Master.objects.filter(
                        Group_Code=group_code
                    ).first()

                    
                if existing_data1:
                    existing_data1.Basic = groupCost
                    existing_data1.save()
                else:
                    Testmaster_Cost_List.objects.create(
                        Test_Id = next_Testmaster_Cost_List_Test_Id,
                        Basic = groupCost,
                        Group_Code = Group_Master_instance,
                        created_by = created_by
                    )
             

                return JsonResponse(message,safe=False)
            elif Type == "AgeSetupMaster":
                # Get department data from the request
                ageType = data.get("ageType")
                fromAge = data.get("fromAge")
                fromageType = data.get("ageType")
                toAge = data.get('toAge')
                toAgeType = data.get('toAgeType')
                fromvalue = data.get('fromvalue')
                tovalue = data.get('tovalue')
                gender = data.get('gender')
                panicHigh = data.get('panicHigh')
                panicLow = data.get('panicLow')
                testcode = data.get('testcode')
                testname = data.get('testname')
                Editmode = data.get('isEditMode1')
                print('Editmode :',Editmode)
                referencerange = data.get('referencerange')
                if referencerange != "":
                    NormalValue = "Yes"
                else:
                    NormalValue = "No"
                
                created_by = data.get('created_by')

                if Editmode is True:
                    # Check if a department with the same code exists
                    print('testcode :',testcode)
                    existing_AgeSetupdata = Age_Setup_Master.objects.filter(
                        Test_Code=testcode
                    ).first()
                    print('existing_AgeSetupdata :',existing_AgeSetupdata)
                    if existing_AgeSetupdata:
                        # Update existing record
                        existing_AgeSetupdata.Gender = gender
                        existing_AgeSetupdata.FromAge = fromAge
                        existing_AgeSetupdata.FromAgeType = fromageType
                        existing_AgeSetupdata.Toage = toAge
                        existing_AgeSetupdata.ToAgeType = toAgeType
                        existing_AgeSetupdata.From_Value = fromvalue
                        existing_AgeSetupdata.To_Value = tovalue
                        existing_AgeSetupdata.PanicLow = panicLow
                        existing_AgeSetupdata.PanicHigh = panicHigh
                        existing_AgeSetupdata.NormalValue = NormalValue
                        existing_AgeSetupdata.Reference_Range = referencerange
                        existing_AgeSetupdata.save()
                        message = "Data updated successfully."
                else:
                    # Create new record
                    
                    test_instance  = Test_Descriptions.objects.filter(Test_Code=test_code).first()
                    
                    Age_Setup_Master.objects.create(
                        Test_Code = test_instance,
                        Gender = gender,
                        FromAge = fromAge,
                        FromAgeType = fromageType,
                        Toage = toAge,
                        ToAgeType = toAgeType,
                        From_Value = fromvalue,
                        To_Value = tovalue,
                        PanicLow = panicLow,
                        PanicHigh = panicHigh,
                        NormalValue = NormalValue,
                        Reference_Range = referencerange,
                        created_by = created_by
                    )
                    message = "New Reason created successfully."

                return JsonResponse({"success": True, "message": message}, status=200)
            elif Type == "Update_Testmaster_Interpretation_table":
              
                comments = data.get('comments')
                testname = data.get('testname')
                header = data.get('header')
                Test_Code = data.get('Test_Code')
                print('Test_Code :',Test_Code)

                existing_Update_TestmasterInterpretationtable = Testmaster_Interpretation_table.objects.filter(
                        Test_Code=Test_Code
                    ).first()
                if existing_Update_TestmasterInterpretationtable:
                        # Update existing record
                        existing_Update_TestmasterInterpretationtable.Comments = comments
                        existing_Update_TestmasterInterpretationtable.Header_interpretation = header
                        existing_Update_TestmasterInterpretationtable.save()
                        message = {"success": True, "message": "Data Updated Sucessfully"}
                else:
                    message = {"success": False, "message": f"No Exist Data for This Test {testname}"}
                return JsonResponse(message,safe=False)
            
            
            else:
                return JsonResponse({"message": "Type Required"})


           

        except json.JSONDecodeError as e:
            print(e)
            return JsonResponse({"error": "Invalid JSON format."})
        except Exception as e:
            print('Unexpected error:', str(e))
            return JsonResponse({"error": str(e)})

    elif request.method == "GET":
        Type = request.GET.get("Type")
        if Type == "LabDepartment":
            departments = Lab_Department_Detials.objects.all()
            serializer = MainDepartmentSerializer(departments, many=True)
            for index,i in enumerate(serializer.data,start=1):
                i['id'] = index
            return JsonResponse(serializer.data, safe=False)
        elif Type == "LabSubDepartment":
            subdepartments = SubLab_Department_Detials.objects.all()
            serializers = SubLabDepartmentSerializer(subdepartments, many=True)
            for index,i in enumerate(serializers.data,start=1):
                i["id"] = index
            return JsonResponse(serializers.data, safe=False)       
        elif Type == "UnitMaster":
            UnitsData = Unit_Masters.objects.all()
            UnitsData_list = UnitMasterSerilizer(UnitsData,many=True)
            for index, i in enumerate(UnitsData_list.data, start=1):
                i["id"] = index
            return JsonResponse(UnitsData_list.data, safe=False)
        elif Type == "ContainerMaster":
            ContainerMasterData = Container_Masters.objects.all()
            serializer = ContainerMastersSerializer(ContainerMasterData, many=True)
            for index, i in enumerate(serializer.data, start=1):
                i["id"] = index
            return JsonResponse(serializer.data, safe=False)     
        elif Type == "SpecimenMaster":
            SpecimenMasterData = Specimen_Masters.objects.all()
            SpecimenMasterData_list = SpecimenMasterSerializer(SpecimenMasterData,many=True)
            for index, i in enumerate(SpecimenMasterData_list.data, start=1):
                i["id"] = index
            return JsonResponse(SpecimenMasterData_list.data, safe=False)
        elif Type == "MethodsMaster":
            MethodsMasterData = Methods_Masters.objects.all()
            MethodsMasterData_list = MethodMasterSerializer(MethodsMasterData,many=True)
            for index, i in enumerate(MethodsMasterData_list.data, start=1):
                i["id"] = index
            return JsonResponse(MethodsMasterData_list.data, safe=False)
        elif Type == "AntibioticMaster":
            AntibioticMasterData = AntibioticMaster.objects.all()
            AntibioticMasterData_list = AntibioticMasterSerializer(AntibioticMasterData,many=True)
            for index, i in enumerate(AntibioticMasterData_list.data, start=1):
                i["id"] = index
            return JsonResponse(AntibioticMasterData_list.data, safe=False)
        elif Type == "OrganismMaster":
            OrganismMasterData = Organism_Masters.objects.all()
            OrganismMasterData_list = OrganismMasterSerializer(OrganismMasterData,many=True)
            for index, i in enumerate(OrganismMasterData_list.data, start=1):
                i["id"] = index
            return JsonResponse(OrganismMasterData_list.data, safe=False)
        elif Type == "LabRemarksData":
            LabRemarksMasterData = LabRemarksMaster.objects.all()
            LabRemarksMasterData_list = list(LabRemarksMasterData.values())
            for Remarks in LabRemarksMasterData_list:
                departmentCode = Remarks["Department"]
                main_department = SubLab_Department_Detials.objects.filter(
                    SubDepartment_Code=departmentCode
                ).first()
                if main_department:
                    Remarks["Department_Name"] = main_department.SubDepartment_Name
                else:
                    Remarks["Department_Name"] = None
            for index, i in enumerate(LabRemarksMasterData_list, start=1):
                i["id"] = index

            return JsonResponse(LabRemarksMasterData_list, safe=False)
        elif Type == "RemarksMaster":
            RemarksMasterData = Remarks_master.objects.all()
            RemarksMasterData_list = RemarksMasterSerializer(RemarksMasterData,many=True)
            for index, i in enumerate(RemarksMasterData_list.data, start=1):
                i["id"] = index
            return JsonResponse(RemarksMasterData_list.data, safe=False)
        elif Type == "ReasonMaster":
            ReasonMasterData = Reason_master.objects.all()
            ReasonMasterData_list = list(ReasonMasterData.values())
            for index, i in enumerate(ReasonMasterData_list, start=1):
                i["id"] = index
            return JsonResponse(ReasonMasterData_list, safe=False)
        elif Type == "QualificationMaster":
            QualificationMasterData = Qualification_master.objects.all()
            QualificationMasterData_list = list(QualificationMasterData.values())
            for index, i in enumerate(QualificationMasterData_list, start=1):
                i["id"] = index
            return JsonResponse(QualificationMasterData_list, safe=False)
        elif Type == "ExternalLabMaster":
            Labcode = request.GET.get("Labcode")
            if Labcode:
                External_Lab_MasterData = External_Lab_Master.objects.filter(
                    LabCode=Labcode
                )
            else:
                External_Lab_MasterData = External_Lab_Master.objects.all()

            External_Lab_MasterData_list = list(External_Lab_MasterData.values())
            for index, i in enumerate(External_Lab_MasterData_list, start=1):
                i["id"] = index
            return JsonResponse(External_Lab_MasterData_list, safe=False)
        elif Type == "ReferDoctorMaster":

            ReferingDoctorDetails = Refering_Doctor_Details.objects.all()
            ReferingDoctorDetails_list = list(ReferingDoctorDetails.values())
            for ReferingDoctor in ReferingDoctorDetails_list:

                Qualification_id = ReferingDoctor["Qualification_id"]
                Qualification_details = Qualification_master.objects.filter(
                    Qualification_Id=Qualification_id
                ).first()
                if Qualification_details:
                    ReferingDoctor["Qualification_name"] = (
                        Qualification_details.Qualification
                    )
                else:
                    ReferingDoctor["Qualification_name"] = None

            for index, ReferingDoctor in enumerate(ReferingDoctorDetails_list, start=1):
                ReferingDoctor["id"] = index

            return JsonResponse(ReferingDoctorDetails_list, safe=False)
        elif Type == "TestMaster":
            print('Type :',Type)
            # First, get the SubDepartment_Code and corresponding OrderID from DepartmentOrderMaster
            sub_departments = SubLab_Department_Detials.objects.annotate(
                order_id=Subquery(
                    DepartmentOrderMaster.objects.filter(
                        SubDepartment_Code=OuterRef("SubDepartment_Code")
                    ).values("OrderID")[:1]
                )
            ).order_by(
                Case(
                    When(order_id__isnull=False, then=Value(0)),
                    default=Value(1),
                    output_field=IntegerField(),
                ),
                "order_id",  # This sorts OrderID in ascending order
                "SubDepartment_Name",  # This sorts sub_department_name in ascending order
            )

            # Now, remove duplicates by keeping only the first instance of each SubDepartment_Code
            seen_sub_departments = set()
            unique_sub_departments = []

            for sub_department in sub_departments:
                if sub_department.SubDepartment_Code not in seen_sub_departments:
                    unique_sub_departments.append(sub_department)
                    seen_sub_departments.add(sub_department.SubDepartment_Code)

            # Process the unique sub_departments
            data = []
            newsn = 1

            for sub_department in unique_sub_departments:
                # Department Details
                sub_department_id = sub_department.SubDepartment_Code
                sub_department_name = sub_department.SubDepartment_Name
                status = sub_department.Status
                sub_department_code = sub_department.SubDepartment_Code

                # Department and their Tests
                tests = Test_Descriptions.objects.filter(sub_department=sub_department)
                test_count = tests.count()
                test_data = [model_to_dict(row) for row in tests]

                for index, i in enumerate(test_data, start=1):
                    i["id"] = index

                data.append(
                    {
                        "sub_department_name": sub_department_name,
                        "tests": test_data,
                        "Testcount": test_count,
                        "sub_department_id": sub_department_id,
                        "DepartmentOrderID": sub_department.order_id,  # Use annotated order_id
                        "id": newsn,
                        "Status": status,
                        "sub_department_code": sub_department_code,
                    }
                )

                newsn += 1

            # Return the data in JSON format
            return JsonResponse({"data": data}, status=200)
        elif Type == "DepartmentOrderMaster":
            DepartmentOrderMaster_data = DepartmentOrderMaster.objects.all()
            DepartmentOrderMaster_list = list(DepartmentOrderMaster_data.values())
            for index, i in enumerate(DepartmentOrderMaster_list, start=1):
                SubDepartment_Code_id = i["SubDepartment_Code_id"]
                Subdepartment_instance = SubLab_Department_Detials.objects.filter(SubDepartment_Code=SubDepartment_Code_id).first()
                i["SubDepartment_Name"] = Subdepartment_instance.SubDepartment_Name
                i["id"] = index
                i["SubDepartment_Code"] = SubDepartment_Code_id
                i["Type"] = "DepartmentOrderMaster"
            return JsonResponse(DepartmentOrderMaster_list, safe=False) 
        elif Type == "Get_AllTests":
            gender = request.GET.get('gender')
            SubDepartment_Code = request.GET.get("SubDepartment_Code")
            
            # Base QuerySet
            Test_data = Test_Descriptions.objects.filter(Status="Active")
            
            # Apply filtering based on conditions
            if gender and SubDepartment_Code:
                # Filter by both gender and SubDepartment_Code
                Test_data = Test_data.filter(
                    sub_department_id=SubDepartment_Code
                ).filter(
                    Gender__in=[gender, "Both"]
                    )
            elif gender:
                # Filter by gender only
                Test_data = Test_data.filter(Gender__in=[gender, "Both"])
            elif SubDepartment_Code:
                # Filter by SubDepartment_Code only
                Test_data = Test_data.filter(sub_department_id=SubDepartment_Code)
            
            # Convert QuerySet to list of dictionaries
            Test_data_list = list(Test_data.values())
            
            # Add an incremental "id" field to the response
            for index, i in enumerate(Test_data_list, start=1):
                i["id"] = index

            # Return JSON response
            return JsonResponse(Test_data_list, safe=False)
        elif Type == "FormulaMaster":

            All_Test_data = Test_Descriptions.objects.all()
            Test_data_list_1 = list(All_Test_data.values())
            print("Test_data_list_1 :", Test_data_list_1)
            All_Test_data_list = {
                i.get("Test_Code"): i.get("Test_Name") for i in Test_data_list_1
            }
            print("All_Test_data_list :", All_Test_data_list)

            Test_data = Test_Descriptions.objects.filter(Calculated_Test="Yes").all()
            Test_data_list = list(Test_data.values())
            print("Test_data_list :", Test_data_list)
            for index, i in enumerate(Test_data_list, start=1):
                print("i :", i)
                formula = i.get("Formula")

                print("formula :", formula)
                displayformula = formula

                for code, name in All_Test_data_list.items():
                    displayformula = displayformula.replace(code, name)
                print("displayformula :", displayformula)
                i["displayformula"] = displayformula
                i["id"] = index

            return JsonResponse(Test_data_list, safe=False)
        elif Type == "RateCardMaster":
            with connection.cursor() as cursor:
                cursor.execute("SHOW COLUMNS FROM Testmaster_Cost_List")
                columns = cursor.fetchall()
            column_names = [column[0] for column in columns]
            excluded_columns = [
                "updated_at",
                "created_at",
                "test_id",
                "test_name",
                "test_code",
                "created_by",
                "Test_Code_id",
                "Group_Code_id"
            ]
            filtered_columns = [
                {"columname": column}
                for column in column_names
                if column.lower()
                not in [excluded.lower() for excluded in excluded_columns]
            ]
            for i in filtered_columns:
                columname = i.get("columname")
                if columname != "Basic":
                    lab_name = External_Lab_Master.objects.filter(
                        LabCode=columname
                    ).first()
                    if lab_name:
                        i["displayNames"] = lab_name.LabName
                    else:
                        i["displayNames"] = None
                else:
                    i["displayNames"] = columname

            return JsonResponse(filtered_columns, safe=False)
        elif Type == "RateCardMasterList":
            columnsname = request.GET.get("ratecard")
            if not columnsname:
                return JsonResponse({"success": False, "message": "Column name not provided"})

            with connection.cursor() as cursor:
                cursor.execute("SHOW COLUMNS FROM Testmaster_Cost_List")
                columns = cursor.fetchall()

            valid_columns_from_db = [column[0] for column in columns]
            if columnsname not in valid_columns_from_db:
                return JsonResponse({"success": False, "message": f"Invalid column name: {columnsname}"})

            query = f"SELECT * FROM Testmaster_Cost_List WHERE {columnsname} IS NOT NULL"
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()

                filtered_data = []
                for index, row in enumerate(rows, start=1):
                    row_dict = dict(zip([col[0] for col in cursor.description], row))
                    testcode = row_dict.get("Test_Code_id")
                    group_code = row_dict.get("Group_Code_id")

                    if testcode is not None:
                        test_description_instance = Test_Descriptions.objects.filter(Test_Code=testcode).first()
                        row_dict["Name"] = test_description_instance.Test_Name if test_description_instance else None
                        row_dict["Type"] = "Individual"
                        row_dict["rowColor"] = "black"
                        row_dict['Code'] = testcode
                    elif group_code is not None:
                        group_instance = Group_Master.objects.filter(Group_Code=group_code).first()
                        row_dict["Name"] = group_instance.Group_Name if group_instance else None
                        row_dict["rowColor"] = "green"
                        row_dict["Type"] = "Group"
                        row_dict['Code'] = group_code
                                                
                    row_dict["id"] = index
                    row_dict["Schemecost"] = float(row_dict.get(columnsname))
                    filtered_data.append(row_dict)

            return JsonResponse(filtered_data, safe=False)

        elif Type == "GroupMaster":
            # First, get the SubDepartment_Code and corresponding OrderID from DepartmentOrderMaster
            GroupMasterdata = Group_Master.objects.all()
            print('GroupMasterdata :',GroupMasterdata)
            GroupMasterdata_list = list(GroupMasterdata.values())
            print('GroupMasterdata_list :',GroupMasterdata_list)
            for index , i in enumerate(GroupMasterdata_list,start=1):
                Department_id = i.get("Department_id")
                GroupCode = i.get("Group_Code")
                
                
                Subdepartmentinstance = SubLab_Department_Detials.objects.filter(SubDepartment_Code=Department_id).first()
                Testmaster_Cost_List_instance = Testmaster_Cost_List.objects.filter(Group_Code=GroupCode).first()

                i["Sub_DepartmentName"] = Subdepartmentinstance.SubDepartment_Name
                i["id"] = index
                i["Amount"] = Testmaster_Cost_List_instance.Basic
                
                Group_TestList = Group_Master_TestList.objects.filter(Group_Code=GroupCode)
                Group_TestList_data = list(Group_TestList.values())
                
                for index,j in enumerate(Group_TestList_data,start=1):
                    GroupCode_in_List = j.get("Group_Code_id")
                    TestCode_GML = j.get("Test_Code_id")
                    print('GroupCode_in_List :',GroupCode_in_List)
                    Testdetails = Test_Descriptions.objects.filter(Test_Code=TestCode_GML).first()
                    
                    j["id"] = index
                    j["Test_Code"] = TestCode_GML
                    j["group_code"] = GroupCode_in_List
                    j["test_name"] = Testdetails.Test_Name
                    j["department"] = Testdetails.department.Department_Name
                    j["sub_department"] = Testdetails.sub_department.SubDepartment_Name
                    j["Header"] = Testdetails.Header
                    j["Billing_Name"] = Testdetails.Billing_Name
                    
                    if GroupCode_in_List == GroupCode:
                        i["GroupList"] = Group_TestList_data
                
            return JsonResponse(GroupMasterdata_list,safe=False)
        elif Type == "Get_AllTests_For_AgeSetup":
            test_data = Test_Descriptions.objects.filter(Status="Active")
    
            response_data = []
            id_counter = 1
            # Iterate over each Test_Description
            for index,test in enumerate(test_data,start=1):
                # Fetch related Age_Setup_Master data based on Test_Code
                age_setup_data = Age_Setup_Master.objects.filter(Test_Code=test.Test_Code)
                
                # Prepare the dictionary for each Test_Description
                test_dict = {}
        
                # Add all fields from the Test_Descriptions model
                for field in test._meta.get_fields():
                    if field.is_relation:
                        # Skip ForeignKeys or related fields (if you don't want to include them)
                        continue
                    field_name = field.name
                    field_value = getattr(test, field_name)
                    test_dict[field_name] = field_value
                
                # Add Age_Setup_Master fields to the test_dict
                for index,age in enumerate(age_setup_data,start=1):
                    for field in age._meta.get_fields():
                        # Skip ForeignKeys or related fields to avoid redundant data
                        if field.is_relation:
                            continue
                        field_name = field.name
                        test_dict[field_name] = getattr(age, field.name)
                
                test_dict["id"] = id_counter
        
                # Increment the ID counter for the next entry
                id_counter += 1
                response_data.append(test_dict)

            # Return the combined data as a JSON response
            return JsonResponse(response_data, safe=False)
     
        elif Type == "Get_AllTests_For_Reflex":
            test_data = Test_Descriptions.objects.filter(Status="Active")
    
            response_data = []
            id_counter = 1
            # Iterate over each Test_Description
            for index,test in enumerate(test_data,start=1):
                # Fetch related Age_Setup_Master data based on Test_Code
                age_setup_data = Testmaster_Reflex_Test.objects.filter(Test_Code=test.Test_Code)
                
                # Prepare the dictionary for each Test_Description
                test_dict = {}
        
                # Add all fields from the Test_Descriptions model
                for field in test._meta.get_fields():
                    if field.is_relation:
                        # Skip ForeignKeys or related fields (if you don't want to include them)
                        continue
                    field_name = field.name
                    field_value = getattr(test, field_name)
                    test_dict[field_name] = field_value
                
                # Add Age_Setup_Master fields to the test_dict
                for index,age in enumerate(age_setup_data,start=1):
                    for field in age._meta.get_fields():
                        # Skip ForeignKeys or related fields to avoid redundant data
                        if field.is_relation:
                            continue
                        field_name = field.name
                        test_dict[field_name] = getattr(age, field.name)
                
                test_dict["id"] = id_counter
        
                # Increment the ID counter for the next entry
                id_counter += 1
                response_data.append(test_dict)

            # Return the combined data as a JSON response
            return JsonResponse(response_data, safe=False)
        elif Type == "Get_AllTests_For_Interpretation":
            test_data = Test_Descriptions.objects.filter(Status="Active")
    
            response_data = []
            id_counter = 1
            # Iterate over each Test_Description
            for index,test in enumerate(test_data,start=1):
                # Fetch related Age_Setup_Master data based on Test_Code
                age_setup_data = Testmaster_Interpretation_table.objects.filter(Test_Code=test.Test_Code)
                
                # Prepare the dictionary for each Test_Description
                test_dict = {}
        
                # Add all fields from the Test_Descriptions model
                for field in test._meta.get_fields():
                    if field.is_relation:
                        # Skip ForeignKeys or related fields (if you don't want to include them)
                        continue
                    field_name = field.name
                    field_value = getattr(test, field_name)
                    test_dict[field_name] = field_value
                
                # Add Age_Setup_Master fields to the test_dict
                for index,age in enumerate(age_setup_data,start=1):
                    for field in age._meta.get_fields():
                        # Skip ForeignKeys or related fields to avoid redundant data
                        if field.is_relation:
                            continue
                        field_name = field.name
                        test_dict[field_name] = getattr(age, field.name)
                
                test_dict["id"] = id_counter
        
                # Increment the ID counter for the next entry
                id_counter += 1
                response_data.append(test_dict)

            # Return the combined data as a JSON response
            return JsonResponse(response_data, safe=False)
        
        
        
        else:
            return JsonResponse({"message": "Type Required"})



  

@csrf_exempt
def Update_All_Masters_Status_update(request):
    # Get parameters from GET request
    Type = request.GET.get("Type")

    if Type == "MainDepartment":
        # Get the department code and the new status
        department_code = request.GET.get("Code")
        newstatus = request.GET.get("newstatus")

        if department_code and newstatus:
            try:
                # Fetch the department using the department code
                department = Lab_Department_Detials.objects.get(
                    Department_Code=department_code
                )

                # Update the status of the department
                department.Status = newstatus
                department.save()

                # Return a success response
                return JsonResponse(
                    {"success": f"{newstatus} successfully"},
                    status=200,
                )
            except Lab_Department_Detials.DoesNotExist:
                # Handle case where the department code doesn't exist
                return JsonResponse(
                    {"warn": "Department not found"})
        else:
            return JsonResponse(
                {
                    "warn": "Department code and new status are required"
                }
            )
    elif Type == "SubMainDepartment":
        # Get the department code and the new status
        subdepartment_code = request.GET.get("subdepartment_code")
        newstatus = request.GET.get("newstatus")

        if subdepartment_code and newstatus:
            try:
                # Fetch the department using the department code
                sub_department = SubLab_Department_Detials.objects.get(
                    SubDepartment_Code=subdepartment_code
                )

                # Update the status of the department
                sub_department.Status = newstatus
                sub_department.save()

                # Return a success response
                return JsonResponse(
                    {"success": True, "message": f"{newstatus} successfully"},
                    status=200,
                )
            except SubLab_Department_Detials.DoesNotExist:
                # Handle case where the department code doesn't exist
                return JsonResponse(
                    {"success": False, "message": "Sub Department not found"},
                    status=404,
                )
        else:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Sub Department code and new status are required",
                },
                status=400,
            )
    elif Type == "ExternalLabMaster":
        # Get the department code and the new status
        Labcode = request.GET.get("Labcode")
        newstatus = request.GET.get("newstatus")

        if Labcode and newstatus:
            try:
                # Fetch the department using the department code
                External_LabMaster = External_Lab_Master.objects.get(LabCode=Labcode)

                # Update the status of the department
                External_LabMaster.Status = newstatus
                External_LabMaster.save()

                # Return a success response
                return JsonResponse(
                    {"success": True, "message": f"{newstatus} successfully"},
                    status=200,
                )
            except External_Lab_Master.DoesNotExist:
                # Handle case where the department code doesn't exist
                return JsonResponse(
                    {"success": False, "message": "External LabMaster not found"},
                    status=404,
                )
        else:
            return JsonResponse(
                {"success": False, "message": "Lab code and new status are required"},
                status=400,
            )
    elif Type == "ReferDoctorMaster":
        # Get the department code and the new status
        DoctorID = request.GET.get("DoctorID")
        newstatus = request.GET.get("newstatus")

        if DoctorID and newstatus:
            try:
                # Fetch the department using the department code
                Refering_DoctorDetails = Refering_Doctor_Details.objects.get(
                    DoctorID=DoctorID
                )

                # Update the status of the department
                Refering_DoctorDetails.Status = newstatus
                Refering_DoctorDetails.save()

                # Return a success response
                return JsonResponse(
                    {"success": True, "message": f"{newstatus} successfully"},
                    status=200,
                )
            except Refering_Doctor_Details.DoesNotExist:
                # Handle case where the department code doesn't exist
                return JsonResponse(
                    {"success": False, "message": "External LabMaster not found"},
                    status=404,
                )
        else:
            return JsonResponse(
                {"success": False, "message": "Lab code and new status are required"},
                status=400,
            )
    elif Type == "TestMaster":
        # Get the department code and the new status
        Test_Code = request.GET.get("Test_Code")
        newstatus = request.GET.get("newstatus")

        if Test_Code and newstatus:
            try:
                # Fetch the department using the department code
                TestDescriptions = Test_Descriptions.objects.get(
                    Test_Code=Test_Code
                )

                # Update the status of the department
                TestDescriptions.Status = newstatus
                TestDescriptions.save()

                # Return a success response
                return JsonResponse(
                    {"success": True, "message": f"{newstatus} successfully"},
                    status=200,
                )
            except Test_Descriptions.DoesNotExist:
                # Handle case where the department code doesn't exist
                return JsonResponse(
                    {"success": False, "message": "External LabMaster not found"},
                    status=404,
                )
        else:
            return JsonResponse(
                {"success": False, "message": "Lab code and new status are required"},
                status=400,
            )
    elif Type == "FormulaMaster":
        # Get the department code and the new status
        Test_Code = request.GET.get("Test_Code")

        if Test_Code:
            try:
                # Fetch the department using the department code
                TestDescriptions = Test_Descriptions.objects.get(Test_Code=Test_Code)

                # Update the status of the department
                TestDescriptions.Calculated_Test = "No"
                TestDescriptions.Formula = None
                TestDescriptions.save()

                # Return a success response
                return JsonResponse(
                    {"success": True, "message": "Formula Removed successfully"},
                    status=200,
                )
            except Test_Descriptions.DoesNotExist:
                # Handle case where the department code doesn't exist
                return JsonResponse(
                    {"success": False, "message": "Test Not found"},
                    status=404,
                )
        else:
            return JsonResponse(
                {"success": False, "message": "TestCode  required"},
                status=400,
            )
    elif Type == "GroupMaster":
        # Get the department code and the new status
        Group_Code = request.GET.get("Group_Code")
        newstatus = request.GET.get("newstatus")

        if Group_Code and newstatus:
            try:
                # Fetch the department using the department code
                GroupMaster = Group_Master.objects.get(
                    Group_Code=Group_Code
                )

                # Update the status of the department
                GroupMaster.Status = newstatus
                GroupMaster.save()

                # Return a success response
                return JsonResponse(
                    {"success": True, "message": f"{newstatus} successfully"},
                    status=200,
                )
            except Group_Master.DoesNotExist:
                # Handle case where the department code doesn't exist
                return JsonResponse(
                    {"success": False, "message": "Group not found"}
                )
        else:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Group code and new status are required",
                }
            )
    
    
    else:
        return JsonResponse({"message": "Type Required"})


@csrf_exempt
def All_CSV_Files_Upload(request):
    Type = request.POST.get("Type")

    if Type == "AntibioticMaster_CSV":
        file = request.FILES.get("file")
        created_by = request.POST.get("created_by")
        print("file:", file)

        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        elif file.name.endswith(".xlsx"):
            df = pd.read_excel(file, engine="openpyxl")
        else:
            return JsonResponse(
                {
                    "error": "'Unsupported file format. Please upload a CSV or Excel file'"
                }
            )

        csv_data = df.to_dict(orient="records")

        # Get the last used anti_biotic_id before processing rows
        last_anti_biotic_id = AntibioticMaster.objects.aggregate(Max("anti_biotic_id"))[
            "anti_biotic_id__max"
        ]
        next_anti_biotic_id = (
            1 if last_anti_biotic_id is None else int(last_anti_biotic_id) + 1
        )

        print("Starting with next_anti_biotic_id:", next_anti_biotic_id)

        for row in csv_data:
            # Handle missing values in the row
            for key in row:
                if pd.isna(row[key]):
                    if isinstance(row[key], str):
                        row[key] = "None"
                    elif isinstance(row[key], (int, float)):
                        row[key] = None

            print("row:", row)

            # Assign the next available anti_biotic_id and increment it for the next record
            row["anti_biotic_id"] = next_anti_biotic_id
            next_anti_biotic_id += 1  # Increment for the next row

            try:
                # Create the AntibioticMaster record
                AntibioticMaster.objects.create(
                    anti_biotic_id=row["anti_biotic_id"],
                    anti_biotic_group_code=row["anti_biotic_group_code"],
                    anti_biotic_code=row["anti_biotic_code"],
                    anti_biotic=row["anti_biotic_des"],
                    created_by=created_by,
                )
            except Exception as e:
                return JsonResponse({"message": f"Error inserting row: {e}"})
        return JsonResponse({"message": "Upload Successfully"}, status=200)
    elif Type == "TestMaster_CSV":
        file = request.FILES.get("file")
        created_by = request.POST.get("created_by")
        print("file:", file)

        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        elif file.name.endswith(".xlsx"):
            df = pd.read_excel(file, engine="openpyxl")
        else:
            return JsonResponse(
                {
                    "error": "'Unsupported file format. Please upload a CSV or Excel file'"
                }
            )

        csv_data = df.to_dict(orient="records")

        def get_or_create_foreign_key(model, filters, defaults, return_existing_code=False):
            """
            Helper function to get or create a foreign key instance.
            Args:
                model: Django model to query.
                filters: Dictionary of fields to filter.
                defaults: Dictionary of fields for creating an object if not found.
                return_existing_code: Whether to return the existing instance's code if found.
            Returns:
                Instance of the model or existing code if specified.
            """
            print('model :', model)
            print('filters :', filters)
            print('defaults :', defaults)
            filter_conditions = {}
            for key, value in filters.items():
                if value:  # Only add to filter_conditions if value is not empty
                    filter_conditions[key] = value

            print('filter_conditions :', filter_conditions)
            instance = model.objects.filter(**filter_conditions).first()
            print('instance :', instance)
            if instance is not None and any(getattr(instance, field, None) for field in ['Department_Name', 'SubDepartment_Name', 'Container_Name','Method_Name','Specimen_Name','Unit_Name']):  # Replace with your relevant fields
                if hasattr(instance, 'Department_Code'):
                    return instance.Department_Code
                elif hasattr(instance, 'SubDepartment_Code'):
                    return instance.SubDepartment_Code
                elif hasattr(instance, 'Container_Code'):
                    return instance.Container_Code
                elif hasattr(instance, 'Specimen_Code'):
                    return instance.Specimen_Code
                elif hasattr(instance, 'Method_Code'):
                    return instance.Method_Code
                elif hasattr(instance, 'Unit_Code'):
                    return instance.Unit_Code
                print('Existing instance :', instance)
                return instance  # Return instance if no code attribute found

            else:
                print('hai')
                # Create a new instance
                instance = model.objects.create(**{**filters, **defaults})
                print('new instance :', instance)
                if hasattr(instance, 'Department_Code'):
                    return instance.Department_Code
                elif hasattr(instance, 'SubDepartment_Code'):
                    return instance.SubDepartment_Code
                elif hasattr(instance, 'Container_Code'):
                    return instance.Container_Code
                elif hasattr(instance, 'Specimen_Code'):
                    return instance.Specimen_Code
                elif hasattr(instance, 'Method_Code'):
                    return instance.Method_Code
                elif hasattr(instance, 'Unit_Code'):
                    return instance.Unit_Code

                return instance


        for row in csv_data:
            # Handle missing values in the row
            for key in row:
                if pd.isna(row[key]):
                    if isinstance(row[key], str):
                        row[key] = "None"
                    elif isinstance(row[key], (int, float)):
                        row[key] = None

            max_code = Lab_Department_Detials.objects.all().aggregate(Max("Department_Code"))["Department_Code__max"]
            new_department_code = Common_Function_For_Genarate_Next_Code_For_6Digit(max_code) if max_code else "LDC000001"

            # Get or create Department
            department = None
            if row["Department"] != '' and row["Department"] is not None:
                department = get_or_create_foreign_key(
                    Lab_Department_Detials,
                    filters={"Department_Name": row["Department"]},
                    defaults={"Department_Code": new_department_code, "Status": "Active", "created_by": created_by},
                    return_existing_code=True
                )
            print('department :', department)

            # Generate SubDepartment Code
            max_code1 = SubLab_Department_Detials.objects.all().aggregate(Max("SubDepartment_Code"))["SubDepartment_Code__max"]
            new_sub_department_code = Common_Function_For_Genarate_Next_Code_For_6Digit(max_code1) if max_code1 else "LSDC000001"

            # Get or create SubDepartment
            sub_department = None
            if row["Sub_Department"] != '' and row["Sub_Department"] is not None:
                # We need to get the actual department instance
                department_instance = Lab_Department_Detials.objects.get(Department_Code=department)  # Assuming department contains a code

                sub_department = get_or_create_foreign_key(
                    SubLab_Department_Detials,
                    filters={"SubDepartment_Name": row["Sub_Department"], "department": department_instance},
                    defaults={"SubDepartment_Code": new_sub_department_code, "Status": "Active", "created_by": created_by},
                    return_existing_code=True
                )
                sub_department_instance = SubLab_Department_Detials.objects.get(SubDepartment_Code=sub_department)  # Assuming department contains a code
            # Generate Container Code
            max_code = Container_Masters.objects.all().aggregate(Max("Container_Code"))["Container_Code__max"]
            new_Container_Code = Common_Function_For_Genarate_Next_Code_For_6Digit(max_code) if max_code else "LCC000001"

            # Get or create Container
            container_instance = None
            if row["Container_Name"] != '' and row["Container_Name"] is not None:
                container = get_or_create_foreign_key(
                    Container_Masters,
                    filters={"Container_Name": row["Container_Name"]},
                    defaults={"Container_Code": new_Container_Code,"created_by": created_by},
                    return_existing_code=True
                )
                container_instance = Container_Masters.objects.get(Container_Code=container)  # Assuming department contains a code
            # Generate Specimen Code
            max_code = Specimen_Masters.objects.all().aggregate(Max("Specimen_Code"))["Specimen_Code__max"]
            new_Specimen_Code = Common_Function_For_Genarate_Next_Code_For_6Digit(max_code) if max_code else "LSC000001"

            # Get or create Specimen
            specimen_instance = None
            if row["Specimen_Name"] != '' and row["Specimen_Name"] is not None:
                specimen = get_or_create_foreign_key(
                    Specimen_Masters,
                    filters={"Specimen_Name": row["Specimen_Name"]},
                    defaults={"Specimen_Code": new_Specimen_Code,"created_by": created_by},
                    return_existing_code=True
                )
                specimen_instance = Specimen_Masters.objects.get(Specimen_Code=specimen)  # Assuming department contains a code
            # Generate Method Code
            max_code = Methods_Masters.objects.all().aggregate(Max("Method_Code"))["Method_Code__max"]
            new_Method_Code = Common_Function_For_Genarate_Next_Code_For_6Digit(max_code) if max_code else "LMC000001"

            # Get or create Method
            method_instance = None
            if row["Method_Name"] != '' and row["Method_Name"] is not None:
                method = get_or_create_foreign_key(
                    Methods_Masters,
                    filters={"Method_Name": row["Method_Name"]},
                    defaults={"Method_Code": new_Method_Code,"created_by": created_by},
                    return_existing_code=True
                )
                method_instance = Methods_Masters.objects.get(Method_Code=method)
            # Generate Unit Code
            max_code = Unit_Masters.objects.all().aggregate(Max("Unit_Code"))["Unit_Code__max"]
            new_unit_code = Common_Function_For_Genarate_Next_Code_For_6Digit(max_code) if max_code else "LUC000001"

            # Get or create Unit
            uom_instance = None
            if row["UOM"] != '' and row["UOM"] is not None:
                uom = get_or_create_foreign_key(
                    Unit_Masters,
                    filters={"Unit_Name": row["UOM"]},
                    defaults={"Unit_Code": new_unit_code, "created_by": created_by},
                    return_existing_code=True
                )
            
                uom_instance = Unit_Masters.objects.get(Unit_Code=uom)
                
                
            Test_Name = row["Test_Name"]
            Header = row["Header"]
            Display_Text = row["Display_Text"]
            Billing_Name = row["Billing_Name"]
            Gender = row["Gender"] if row['Gender'] is not None else "Both"
            Input_Type = row["Input_Type"]
            Decimal_Palces = row["Decimal_Palces"]
            Input_Pattern_Type = row["Input_Pattern_Type"]
            Test_Category = row["Test_Category"]
            Logical_Category = row["Logical_Category"]
            Captured_Unit = None
            Captured_Unit_Uom = None
            Report_Type = row["Report_Type"]
            Test_Instructions = row["Test_Instructions"]
            Loinc_Code = row["Loinc_Code"]
            Allow_Discount = row["Allow_Discount"]
            Oderable = row["Oderable"]
            Show_Graph = row["Show_Graph"]
            STAT = row["STAT"]
            Non_Reportable = row["Non_Reportable"]
            Calculated_Test = "No"
            Outsourced = row["Outsourced"]
            Processing_Time = row["Processing_Time"]
            Emergency_Processing_Time = row["Emergency_Processing_Time"]
            Period_Type = row["Period_Type"]
            Formula = None
            Routine = row["Parameter_One"]
            TimeGap = row["Parameter_Two"]
            Autocheck = row["Autocheck"]
            Culturetest = row["Culturetest"]
            Is_NABHL = row["Is_NABHL"] 
            Is_CAP = row["Is_CAP"]    
            Is_Machine_Interfaced = row["Is_Machine_Interfaced"]
            Machine_Name = row["Machine_Name"]
            Assay_Code = row["Assay_Code"]
            IsSubTest = 'No'
            SubTestCodes = None
            
            with transaction.atomic():
                # Create the AntibioticMaster record
                
                max_code = Test_Descriptions.objects.all().aggregate(Max("Test_Code"))[
                    "Test_Code__max"
                ]
                new_Test_Code = Genarate_Next_Code_4digit(max_code) if max_code else "LTC0001"
                
                if Test_Name is not None and Test_Name != '':
                    test_description = Test_Descriptions.objects.create(
                                Test_Code=new_Test_Code,
                                Test_Name=Test_Name,
                                department=department_instance,
                                sub_department=sub_department_instance,
                                Header=Test_Name,
                                Billing_Name=Test_Name,
                                DisplayText=Test_Name,
                                Container_Name=container_instance,
                                Specimen_Name=specimen_instance,
                                Method_Name=method_instance,
                                Gender=Gender,
                                Input_Type=Input_Type,
                                Decimal_Palces=Decimal_Palces,
                                Input_Pattern_Type=Input_Pattern_Type,
                                Test_Category=Test_Category,
                                Logical_Category=Logical_Category,
                                Captured_Unit=Captured_Unit,
                                Captured_Unit_UOM=Captured_Unit_Uom,
                                UOM=uom_instance,
                                Report_Type=Report_Type,
                                Test_Instructions=Test_Instructions,
                                Loinc_Code=Loinc_Code,
                                Allow_Discount=Allow_Discount,
                                Oderable=Oderable,
                                Show_Graph=Show_Graph,
                                STAT=STAT,
                                Non_Reportable=Non_Reportable,
                                Calculated_Test=Calculated_Test,
                                Outsourced=Outsourced,
                                Processing_Time=Processing_Time,
                                Emergency_Processing_Time=Emergency_Processing_Time,
                                Period_Type=Period_Type,
                                Formula=Formula,
                                Routine=Routine,
                                TimeGap=TimeGap,
                                Autocheck= Autocheck,
                                Culturetest=Culturetest,
                                Is_NABHL=Is_NABHL,
                                Is_CAP=Is_CAP,
                                Is_Machine_Interfaced=Is_Machine_Interfaced,
                                Machine_Name= Machine_Name,
                                Assay_Code=Assay_Code,
                                Status="Active",
                                IsSubTest=IsSubTest,
                                SubTestCodes=SubTestCodes,
                                ResultValues=None,
                                created_by=created_by,
                            )
                
                    test_name = test_description.Test_Name
                    test_code = test_description.Test_Code

                    print('test_name :',test_name)
                
                    test_description_instance = Test_Descriptions.objects.get(
                                Test_Code=test_code
                            )

                    Testmaster_Remarks_Test_Id = (
                                Testmaster_Remarks.objects.aggregate(Max("Test_Id"))[
                                    "Test_Id__max"
                                ]
                            )
                    next_Testmaster_Remarks_Test_Id = (
                                1
                                if Testmaster_Remarks_Test_Id is None
                                else int(Testmaster_Remarks_Test_Id) + 1
                            )

                            # Insert into Testmaster_Remarks
                    Testmaster_Remarks.objects.create(
                                Test_Id=next_Testmaster_Remarks_Test_Id,
                                Test_Code=test_description_instance,
                                # Test_Name=test_name,
                                Validation=None,
                                Remark_Type=None,
                                Remark=None,
                                created_by=created_by,
                            )

                    Testmaster_Reference_Range_Test_Id = (
                                Testmaster_Reference_Range.objects.aggregate(
                                    Max("Test_Id")
                                )["Test_Id__max"]
                            )
                    next_Testmaster_Reference_Range_Test_Id = (
                                1
                                if Testmaster_Reference_Range_Test_Id is None
                                else int(Testmaster_Reference_Range_Test_Id) + 1
                            )

                            # Insert into Testmaster_Reference_Range
                    Testmaster_Reference_Range.objects.create(
                                Test_Id=next_Testmaster_Reference_Range_Test_Id,
                                Test_Code=test_description_instance,
                                # Test_Name=test_name,
                                Analizer_Type=None,
                                validation=None,
                                Method_Type=None,
                                Gender="Both",
                                Range_Lower_Limit=None,
                                Range_Higher_Limit=None,
                                Reference_Range_Text=None,
                                created_by=created_by,
                            )

                    Testmaster_Cost_List_Test_Id = (
                                Testmaster_Cost_List.objects.aggregate(Max("Test_Id"))[
                                    "Test_Id__max"
                                ]
                            )
                    next_Testmaster_Cost_List_Test_Id = (
                                1
                                if Testmaster_Cost_List_Test_Id is None
                                else int(Testmaster_Cost_List_Test_Id) + 1
                            )

                            # Insert into Cost_List_Table
                    Testmaster_Cost_List.objects.create(
                                Test_Id=next_Testmaster_Cost_List_Test_Id,
                                Test_Code=test_description_instance,
                                # Test_Name=test_name,
                                Basic=0,
                                created_by=created_by,
                            )

                    Testmaster_Rule_Based_Test_Id = (
                                Testmaster_Rule_Based.objects.aggregate(Max("Test_Id"))[
                                    "Test_Id__max"
                                ]
                            )
                    next_Testmaster_Rule_Based_Test_Id = (
                                1
                                if Testmaster_Rule_Based_Test_Id is None
                                else int(Testmaster_Rule_Based_Test_Id) + 1
                            )

                    Testmaster_Rule_Based.objects.create(
                                Test_Id=next_Testmaster_Rule_Based_Test_Id,
                                Test_Code=test_description_instance,
                                # Test_Name=test_name,
                                Validation_type=None,
                                Gender=None,
                                Rule_Type=None,
                                Remark=None,
                                created_by=created_by,
                            )

                    Testmaster_Interpretation_table_Test_Id = (
                                Testmaster_Interpretation_table.objects.aggregate(
                                    Max("Test_Id")
                                )["Test_Id__max"]
                            )
                    next_Testmaster_Interpretation_table_Test_Id = (
                                1
                                if Testmaster_Interpretation_table_Test_Id is None
                                else int(Testmaster_Interpretation_table_Test_Id) + 1
                            )

                    Testmaster_Interpretation_table.objects.create(
                                Test_Id=next_Testmaster_Interpretation_table_Test_Id,
                                Test_Code=test_description_instance,
                                # Test_Name=test_name,
                                Header_interpretation=None,
                                Comments=None,
                                created_by=created_by,
                            )

                    Testmaster_Reflex_Test_Test_Id = (
                                Testmaster_Reflex_Test.objects.aggregate(Max("Test_Id"))[
                                    "Test_Id__max"
                                ]
                            )
                    next_Testmaster_Reflex_Test_Test_Id = (
                                1
                                if Testmaster_Reflex_Test_Test_Id is None
                                else int(Testmaster_Reflex_Test_Test_Id) + 1
                            )

                    Testmaster_Reflex_Test.objects.create(
                                Test_Id=next_Testmaster_Reflex_Test_Test_Id,
                                Test_Code=test_description_instance,
                                # Test_Name=test_name,
                                Reflex_Test=None,
                                Reflex_Code=None,
                                created_by=created_by,
                            )

                    Testmaster_Age_Setup_Master = (
                                Age_Setup_Master.objects.aggregate(Max("Test_Id"))[
                                    "Test_Id__max"
                                ]
                            )
                    next_Testmaster_Age_Setup_Master = (
                                1
                                if Testmaster_Age_Setup_Master is None
                                else int(Testmaster_Age_Setup_Master) + 1
                            )

                            # Insert into Age_Setup_Master
                    Age_Setup_Master.objects.create(
                                Test_Id=next_Testmaster_Age_Setup_Master,
                                Test_Code=test_description_instance,
                                # Test_Name=test_name,
                                Gender="Both",
                                FromAge=None,
                                FromAgeType=None,
                                Toage=None,
                                ToAgeType=None,
                                From_Value=None,
                                To_Value=None,
                                PanicLow=None,
                                PanicHigh=None,
                                NormalValue=None,
                                Reference_Range=None,
                                created_by=created_by,
                            )

            


        return JsonResponse({'success': 'New TestMaster ExcelFile successfully'})
    
    else:
        return JsonResponse({"success":False,"message": "Invalid 'Type' parameter"})


@csrf_exempt
def Update_Formula_And_ResultValue(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if isinstance(data, dict):
            Type = data.get("Type")
        elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            Type = data[0].get("Type")
        else:
            Type = None

        if Type == "FormulaMaster":
            for i in data:
                testCode = i.get("testCode")
                formula = i.get("formula")
                Calculated_Test = "Yes"

                if testCode and formula:
                    try:
                        Test_data = Test_Descriptions.objects.get(Test_Code=testCode)
                        Test_data.Calculated_Test = Calculated_Test
                        Test_data.Formula = formula
                        Test_data.save()

                        return JsonResponse(
                            {"success": True, "message": "Formula Update Successfull"}
                        )
                    except Test_Descriptions.DoesNotExist:
                        return JsonResponse(
                            {"success": False, "message": "Test not found"}
                        )
                else:
                    return JsonResponse(
                        {
                            "success": False,
                            "message": "Test  and Formula are required",
                        }
                    )
