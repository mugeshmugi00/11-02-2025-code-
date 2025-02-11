from django.urls import path

# from .views import *
from .DrugAdministration import *
from Frontoffice.GeneralBilling import get_prescription

urlpatterns = [
    # path('insert_Drug_Administration_datas', insert_Drug_Administration_datas, name='insert_Drug_Administration_datas'),
    # path('getgenericname', getgenericname, name='getgenericname'),
    # path('getitemname_bygenericname', getitemname_bygenericname, name='getitemname_bygenericname'),
    # path('getDose_By_Itemname', getDose_By_Itemname, name='getDose_By_Itemname'),
    # path('get_prescription_master_code',get_prescription_master_code,name='get_prescription_master_code'),
    # path('get_for_doc_drugs_nurse_request', get_for_doc_drugs_nurse_request, name='get_for_doc_drugs_nurse_request'),
    # path('insert_nurse_request_drugs', insert_nurse_request_drugs, name='insert_nurse_request_drugs'),
    # path('get_completed_prescribed_medicine', get_completed_prescribed_medicine, name='get_completed_prescribed_medicine'),
    # path('inhouse_pharmacy_queue_list_prescrib', inhouse_pharmacy_queue_list_prescrib, name='inhouse_pharmacy_queue_list_prescrib'),
    # path('get_completed_prescribed_medicine', get_completed_prescribed_medicine, name='get_completed_prescribed_medicine'),
    # path('insert_nurse_received_drugs', insert_nurse_received_drugs, name='insert_nurse_received_drugs'),
    # path('get_Drug_Administration_datas', get_Drug_Administration_datas, name='get_Drug_Administration_datas'),
    # path('insert_Drug_Administration_nurse_frequencywise_datas', insert_Drug_Administration_nurse_frequencywise_datas, name='insert_Drug_Administration_nurse_frequencywise_datas'),
    
    
    
    
    path('doctor_drug_prescription_link', doctor_drug_prescription_link, name='doctor_drug_prescription_link'),
    path('Nurse_drug_prescription_link', Nurse_drug_prescription_link, name='Nurse_drug_prescription_link'),
    path('Nurse_drug_prescription_Add_link', Nurse_drug_prescription_Add_link, name='Nurse_drug_prescription_Add_link'),
    path('Nurse_drug_prescription_update_link', Nurse_drug_prescription_update_link, name='Nurse_drug_prescription_update_link'),
    path('Pharmacy_drug_quelist_link', Pharmacy_drug_quelist_link, name='Pharmacy_drug_quelist_link'),
    path('get_for_ip_durgs_doctor_show', get_for_ip_durgs_doctor_show, name='get_for_ip_durgs_doctor_show'),
    path('inhouse_pharmacy_queue_list_prescrib', inhouse_pharmacy_queue_list_prescrib, name='inhouse_pharmacy_queue_list_prescrib'),
    path('get_prescription_forIP', get_prescription_forIP, name='get_prescription_forIP'),
    path('get_last_prescription_forIP', get_last_prescription_forIP, name='get_last_prescription_forIP'),
    path('IP_Pharmacy_Billing_link', IP_Pharmacy_Billing_link, name='IP_Pharmacy_Billing_link'),
    path('OP_Pharmacy_Billing_link', OP_Pharmacy_Billing_link, name='OP_Pharmacy_Billing_link'),
    path('OP_Pharmacy_Walkin_Billing_link', OP_Pharmacy_Walkin_Billing_link, name='OP_Pharmacy_Walkin_Billing_link'),
    path('get_OP_Pharmacy_Billing_datas', get_OP_Pharmacy_Billing_datas, name='get_OP_Pharmacy_Billing_datas'),
    path('Nurse_drug_prescription_Completed', Nurse_drug_prescription_Completed, name='Nurse_drug_prescription_Completed'),
    path('Nurse_drug_prescription_Recieved', Nurse_drug_prescription_Recieved, name='Nurse_drug_prescription_Recieved'),
    path('get_Drug_Administration_datas', get_Drug_Administration_datas, name='get_Drug_Administration_datas'),
    path('insert_Drug_Administration_nurse_frequencywise_datas', insert_Drug_Administration_nurse_frequencywise_datas, name='insert_Drug_Administration_nurse_frequencywise_datas'),
    path('get_for_ip_drugs_doctor_show', get_for_ip_drugs_doctor_show, name='get_for_ip_drugs_doctor_show'),
    
    
    
    path('get_prescription', get_prescription, name='get_prescription'),
    
    
    
]

