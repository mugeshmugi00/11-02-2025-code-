from django.urls import path
from .InsurancePatientEntry import (Signal_PatientEntry_Get_Details,Post_Insurance_Patient_Detailes,
Update_StatusFor_Insurance_Patient_Detailes,Get_StatusCount, Insurance_Patient_Details,Insurance_Details_get)

from .ClientPatientEntry import(Signal_ClientPatientEntry_Get_Details,Get_StatusCount_Client,Post_Client_Patient_Detailes,Update_StatusFor_Client_Patient_Detailes,Client_Details_get)

urlpatterns = [
    path('Signal_PatientEntry_Get_Details',Signal_PatientEntry_Get_Details,name='Signal_PatientEntry_Get_Details'),    
    path('Get_StatusCount',Get_StatusCount,name='Get_StatusCount'),
    path('Post_Insurance_Patient_Detailes',Post_Insurance_Patient_Detailes,name='Post_Insurance_Patient_Detailes'),
    path('Update_StatusFor_Insurance_Patient_Detailes',Update_StatusFor_Insurance_Patient_Detailes,name='Update_StatusFor_Insurance_Patient_Detailes'),

    path('Signal_ClientPatientEntry_Get_Details', Signal_ClientPatientEntry_Get_Details, name='Signal_ClientPatientEntry_Get_Details'),
    path('Get_StatusCount_Client', Get_StatusCount_Client, name='Get_StatusCount_Client'),
    path('Post_Client_Patient_Detailes', Post_Client_Patient_Detailes, name='Post_Client_Patient_Detailes'),
    path('Update_StatusFor_Client_Patient_Detailes', Update_StatusFor_Client_Patient_Detailes, name='Update_StatusFor_Client_Patient_Detailes'),
    path('Insurance_Patient_Details', Insurance_Patient_Details, name='Insurance_Patient_Details'),
    path('Insurance_Details_get', Insurance_Details_get, name='Insurance_Details_get'),
    path('Client_Details_get', Client_Details_get, name='Client_Details_get')

]
