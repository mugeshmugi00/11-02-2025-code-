
from django.urls import path


from .Vitals import *
from .views import *
from .ReferDoctor import *
from .Request import *
from .RadiologyVitals import *
from .LabRequests import *

urlpatterns=[
   
    path('Vitals_Form_Details_Link',Vitals_Form_Details_Link,name='Vitals_Form_Details_Link'),
    path('get_workbenchquelist_doctor',get_workbenchquelist_doctor,name='get_workbenchquelist_doctor'),
    path('ReferDoctor_Details_link',ReferDoctor_Details_link,name='ReferDoctor_Details_link'),
    path('Lab_Request_Detailslink',Lab_Request_Detailslink,name='Lab_Request_Detailslink'),
    path('Radiology_Request_Detailslink',Radiology_Request_Detailslink,name='Radiology_Request_Detailslink'),
    path('Lab_Queuelist_link',Lab_Queuelist_link,name='Lab_Queuelist_link'),
    path('Lab_Request_TestDetails',Lab_Request_TestDetails,name='Lab_Request_TestDetails'),
    path('Lab_SelectedTest_Detailslink',Lab_SelectedTest_Detailslink,name='Lab_SelectedTest_Detailslink'),
    path('Radiology_Queuelist_link',Radiology_Queuelist_link,name='Radiology_Queuelist_link'),
    path('Lab_ViewStatus_link',Lab_ViewStatus_link,name='Lab_ViewStatus_link'),
    
    # labcompleted
    path('Lab_completed_quelist',Lab_completed_quelist,name='Lab_completed_quelist'),
    path('Lab_Complete_TestDetails',Lab_Complete_TestDetails,name='Lab_Complete_TestDetails'),
    path('Lab_PaidDetails_link',Lab_PaidDetails_link,name='Lab_PaidDetails_link'),
    path('lab_report_details_view', lab_report_details_view, name='lab_report_details_view'),


    path('OtRequest_Details',OtRequest_Details,name='OtRequest_Details'),
    path('OtRequest_Names_link',OtRequest_Names_link,name='OtRequest_Names_link'),

    # path('Radiology_Complete_Details_Link',Radiology_Complete_Details_Link,name='Radiology_Complete_Details_Link'),
        # bharathi
    path('RadiologyVitals_Form_Details_Link',RadiologyVitals_Form_Details_Link,name='RadiologyVitals_Form_Details_Link'),
    path('Radiology_Medical_History_Details',Radiology_Medical_History_Details,name='Radiology_Medical_History_Details'),
    path('Radiology_MedicalSection_Details_Link',Radiology_MedicalSection_Details_Link,name='Radiology_MedicalSection_Details_Link'),
    
    path('get_lab_request_details',get_lab_request_details,name='get_lab_request_details'),
    # path('lab_rep_details_view',lab_rep_details_view,name='lab_rep_details_view')
    path('POST_Lab_Data',POST_Lab_Data,name='POST_Lab_Data'),
    # path('lab_rep_details_view',lab_rep_details_view,name='lab_rep_details_view')
    path('Radiology_TestAmount_Entry',Radiology_TestAmount_Entry,name='Radiology_TestAmount_Entry'),
    path('ReportData',ReportData,name='ReportData')
]