from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import *

@csrf_exempt
@require_http_methods(["POST","OPTIONS","GET"])
def bioWaste(request):
    if request.method=='POST':
        try:
            data = json.loads(request.body)
            Waste=data.get("data")
            
            red=Waste[0]
            green=Waste[1]
            yellow=Waste[2]
            blue=Waste[3]

            
            data=bioWaste.object.create()

            print(red)
            return JsonResponse({'success':"yes, success"})
        except Exception as err:
            return JsonResponse({'Error':f"{str(err)}"})
    