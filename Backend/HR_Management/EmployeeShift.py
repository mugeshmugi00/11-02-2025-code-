import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import *
from django.db.models import Sum, Q

import pandas as pd
from .serializers import *


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import ShiftDetails_Master  # Replace with your actual model
from .serializers import ShiftDetailsSerializer  # Replace with your actual serializer

@csrf_exempt
@require_http_methods(["POST", "OPTIONS", "GET"])
def Shift_Details_link(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            bulkAssign = data.get("bulkAssign")
            def check_existing_duty(employee_id, start_date, end_date):
                return ShiftDetails_Master.objects.filter(Employee=employee_id,Shiftstartdate__lte=end_date, Shiftenddate__gte=start_date).exists()
            if bulkAssign is True:
                Employees = data.get("selectedEmployees")
                print('Employees :',Employees)
                errors = []
                for i in Employees:
                    if check_existing_duty(i["Employee_Id"], data.get("Shiftstartdate"), data.get("Shiftenddate")):
                        error_msg = f"Employee {i['Employee_Id']} already has a duty assigned during this period."
                        errors.append({i["Employee_Id"]: error_msg})
                        continue
                    i["Shiftstartdate"] = data.get("Shiftstartdate")
                    i["Shiftenddate"] = data.get("Shiftenddate")
                    i["Shift_Id"] = data.get("Shift_Id")
                    i["Create_by"] = data.get("Create_by")
                    i["Location_Name"] = data.get("Location_Name")
                    i["Department"] = data.get("openRow")
                    i["Status"] = data.get("Status1")
                    i["Employee"] = i.get("Employee_Id")
                    serializer = ShiftDetailsSerializer(data=i)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        errors.append({i["Employee_Id"]: serializer.errors})
                if errors:
                    print('errors :',errors)
                    return JsonResponse({"errors": errors})
                return JsonResponse({"success": "All shifts added successfully"}, status=200)

            else:
                employee_id = data.get("Employee")
                duplicate = check_existing_duty(employee_id, data.get("Shiftstartdate"), data.get("Shiftenddate"))
                if duplicate:
                    return JsonResponse({"error": f"Employee {employee_id} already has a duty assigned during this period."},)
                serializer = ShiftDetailsSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(
                        {"success": "Shift added successfully"})
                return JsonResponse({"error": serializer.errors})
        except Exception as e:
            return JsonResponse({"error": "An unexpected error occurred"})

    elif request.method == "GET":
        try:
            # Fetch all records from the LocationName model
            ShiftsData = ShiftDetails_Master.objects.all()

            # Construct a list of dictionaries containing location data
            Shift_Master_data = []
            for Shift in ShiftsData:
                Shift_dict = {
                    "id": Shift.pk,
                    "Employee": Shift.Employee.Employee_ID if Shift.Employee else None,
                    "ShiftName": Shift.ShiftName.ShiftName if Shift.ShiftName else None,
                    "Intime": Shift.Intime,
                    "Outtime": Shift.Outtime,
                    "Shiftstartdate": Shift.Shiftstartdate,
                    "Shiftenddate": Shift.Shiftenddate,
                    "Status": "Active" if Shift.Status else "Inactive",
                    "Create_by": Shift.Create_by,
                }
                Shift_Master_data.append(Shift_dict)

            return JsonResponse(Shift_Master_data, safe=False)

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return JsonResponse({"error": "An internal server error occurred"})
