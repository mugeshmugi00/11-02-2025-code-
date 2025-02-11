from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
import json
from .models import *
from datetime import date
from django.db.models import Sum

@csrf_exempt
@require_http_methods(["POST","OPTIONS","GET"])
def bioWst(request):
    if request.method=='POST':
        try:
            data = json.loads(request.body)
            Waste=data.get("data")
            date=data.get("date")
            print(date)
            for clr in Waste:
                print(Waste[clr])

                if clr=="Red":
                    desc="Contaminated Waste - Recyclable"
                elif clr=="Blue":
                    desc="Glass Waste"
                elif clr=="Yellow":
                    desc="Infectious & Pathological Waste"

                
                data=wasteManagement.objects.create( wasteCategory='Bio Waste',wasteColor=clr, bagCount=Waste[clr]['BagCount'],weight=Waste[clr]['Weight'],date=date,description=desc)
                data.save()
                wstdata=WasteCount.objects.get(wasteCategory='Bio Waste',wasteColor=clr)
                wstdata.weight=wstdata.weight+int(Waste[clr]['Weight'])
                wstdata.totalWst=wstdata.totalWst+int(Waste[clr]['Weight'])
                wstdata.save()
                
                print("data Saved...")

            data=wasteManagement.objects.all()
            # print(data)
            

            return JsonResponse({'success':"yes, success"})
        except Exception as err:
            print(err)
            return JsonResponse({'Error':f"{str(err)}"})
    

@csrf_exempt
@require_http_methods(["POST","OPTIONS","GET"])
def genrelWst(request):
    if request.method=='POST':
        try:
            data = json.loads(request.body)
            Waste=data.get("data")
            date=data.get("date")
            print(date,Waste)


            
            data=wasteManagement.objects.create( wasteCategory='Genrel Waste',wasteColor='Green', bagCount=Waste['BagCount'],weight=Waste['Weight'],date=date,description="General Non-Infectious Waste")
            data.save()
            wstdata=WasteCount.objects.get(wasteCategory='Genrel Waste',wasteColor="Green")
            wstdata.weight=wstdata.weight+int(Waste['Weight'])
            wstdata.totalWst=wstdata.totalWst+int(Waste['Weight'])
            wstdata.save()
            print("data Saved...")

            data=wasteManagement.objects.all()
            print(data)
            

            return JsonResponse({'success':"yes, success"})
        except Exception as err:
            return JsonResponse({'Error':f"{str(err)}"})
        


@csrf_exempt
@require_http_methods(["POST","OPTIONS","GET"])
def eWst(request):
    if request.method=='POST':
        try:
            data = json.loads(request.body)
            Waste=data.get("data")
            date=data.get("date")
            print(date,Waste)


            
            data=wasteManagement.objects.create( wasteCategory='E Waste',wasteColor='Black',bagCount=Waste['BagCount'],weight=Waste['Weight'],date=date,description="discarded electronic devices or equipment")
            data.save()
            wstdata=WasteCount.objects.get(wasteCategory='E Waste',wasteColor="Black")
            wstdata.weight=wstdata.weight+int(Waste['Weight'])
            wstdata.totalWst=wstdata.totalWst+int(Waste['Weight'])
            wstdata.save()
            print("data Saved...")

            data=wasteManagement.objects.all()
            print(data)
            

            return JsonResponse({'success':"yes, success"})
        except Exception as err:
            print(err)
            return JsonResponse({'Error':f"{str(err)}"})
        

@csrf_exempt
@require_http_methods(["POST","OPTIONS","GET"])
def wastelist(request):
        try:
            data=list(wasteManagement.objects.all().values())
            return JsonResponse(data,safe=False)
        
        except Exception as err:
            print(err)
            return JsonResponse({'Error':f"{str(err)}"})
        

@csrf_exempt
@require_http_methods(["POST","OPTIONS","GET"])
def totalWaste(request):
        try:
             # data=WasteCount.objects.create(wasteCategory="Bio Waste",wasteColor="Red",weight=0,totalWst=0)
            # data=WasteCount.objects.create(wasteCategory="Bio Waste",wasteColor="Yellow",weight=0,totalWst=0)
            # data=WasteCount.objects.create(wasteCategory="Bio Waste",wasteColor="Blue",weight=0,totalWst=0)
            # data=WasteCount.objects.create(wasteCategory="Genrel Waste",wasteColor="Green",weight=0,totalWst=0)
            # data=WasteCount.objects.create(wasteCategory="E Waste",wasteColor="Black",weight=0,totalWst=0)
            # data.save()
 
            data=list(WasteCount.objects.all().values())
            # print(data[2]['wasteColor'])
            total_weight = WasteCount.objects.aggregate(total_weight=Sum('weight'))
            print(total_weight['total_weight'])


            wstDetails={
               "red":data[0]['weight'],
               "yellow":data[1]['weight'],
               "blue":data[2]['weight'],
               "green":data[3]['weight'],
               "black":data[4]['weight'],
               " total":total_weight['total_weight'],
            }



            return JsonResponse(wstDetails,safe=False)
        
        except Exception as err:
            print(err)
            return JsonResponse({'Error':f"{str(err)}"})



@csrf_exempt
@require_http_methods(["POST","OPTIONS","GET"])
def handle(request):
    if request.method=='POST':
        try:
            data = json.loads(request.body)
            Waste=data.get("data")
            print(Waste)


            if Waste:
                data=handOver.objects.create( wasteCategory=Waste['Category'],wasteColor=Waste['Color'],weight=Waste['Weight'],
                                             collecter=Waste['Collector'],collecterCnt=Waste['CollectorContact'],incharge=Waste['Incharge'])
                data.save()
                wstdata=WasteCount.objects.get(wasteCategory=Waste['Category'],wasteColor=Waste['Color'])
                wstdata.weight=wstdata.weight-int(Waste['Weight'])
                wstdata.totalWst=wstdata.totalWst-int(Waste['Weight'])
                wstdata.save()
                print("data Saved...")

                return JsonResponse({'success':"yes, success"})
            else:
                return JsonResponse({'Error':"Some Values Missing..."})

            # data=handOver.objects.all()
            # print(data)
            

            
        except Exception as err:
            print(err)
            return JsonResponse({'Error':f"{str(err)}"})
        


@csrf_exempt
@require_http_methods(["POST","OPTIONS","GET"])
def handoverlist(request):
        try:
            data=list(handOver.objects.all().values())
            return JsonResponse(data,safe=False)
        
        except Exception as err:
            print(err)
            return JsonResponse({'Error':f"{str(err)}"})