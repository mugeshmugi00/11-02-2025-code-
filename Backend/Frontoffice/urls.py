from django.urls import path
from .EmgRegister import *
from .Registration import *
from .AppointmentRequestList import *
from .GeneralBilling import *
from .IP_Billing import *
from .ReceptionReports import *
from .FODashboard import *

urlpatterns=[
    path('Emergency_Registration_Details', Emergency_Registration_Details, name='Emergency_Registration_Details'),
    path('get_Emergency_patient_list', get_Emergency_patient_list, name='get_Emergency_patient_list'),
    path('Patient_Registration', Patient_Registration, name='Patient_Registration'),
    path('Register_Patients_Details', Register_Patients_Details, name='Register_Patients_Details'),
    path('Fetch_Register_Patients_Details', Fetch_Register_Patients_Details, name='Fetch_Register_Patients_Details'),
    path('Patient_OP_Registration', Patient_OP_Registration, name='Patient_OP_Registration'),
    path('get_OP_patient_details', get_OP_patient_details, name='get_OP_patient_details'),
    path('IP_Patient_Registration_Details_Link', IP_Patient_Registration_Details_Link, name='IP_Patient_Registration_Details_Link'),
    path('get_Employee_by_PatientCategory', get_Employee_by_PatientCategory, name='get_Employee_by_PatientCategory'),
    path('get_DoctorId_by_PatientCategory', get_DoctorId_by_PatientCategory, name='get_DoctorId_by_PatientCategory'),
    path('get_Patient_Details_by_patientId', get_Patient_Details_by_patientId, name='get_Patient_Details_by_patientId'),
    path('Filter_Patient_by_Multiple_Criteria', Filter_Patient_by_Multiple_Criteria, name='get_DoctorId_by_PFilter_Patient_by_Multiple_CriteriaatientCategory'),
    path('get_patient_appointment_details', get_patient_appointment_details, name='get_patient_appointment_details'),
    path('get_patient_unique_id', get_patient_unique_id, name='get_patient_unique_id'),
    path('get_patient_ip_registration_details', get_patient_ip_registration_details, name='get_patient_ip_registration_details'),
    path('get_ip_registration_before_handover_details', get_ip_registration_before_handover_details, name='get_ip_registration_before_handover_details'),
    path('get_ip_roomdetials_before_handover_details', get_ip_roomdetials_before_handover_details, name='get_ip_roomdetials_before_handover_details'),
    path('post_ip_roomdetials_before_handover_details', post_ip_roomdetials_before_handover_details, name='post_ip_roomdetials_before_handover_details'),
    path('post_ip_handover_details', post_ip_handover_details, name='post_ip_handover_details'),
    path('post_ip_submit_handover_or_cancel_details', post_ip_submit_handover_or_cancel_details, name='post_ip_submit_handover_or_cancel_details'),
    path('get_ip_roomdetials_for_bedtransfer_details', get_ip_roomdetials_for_bedtransfer_details, name='get_ip_roomdetials_for_bedtransfer_details'),
    path('insert_op_ip_convertion', insert_op_ip_convertion, name='insert_op_ip_convertion'),
    path('post_ip_bed_transfer_details', post_ip_bed_transfer_details, name='post_ip_bed_transfer_details'),
    path('bed_transfer_approve_cancel_details', bed_transfer_approve_cancel_details, name='bed_transfer_approve_cancel_details'),
    path('service_procedure_request', service_procedure_request, name='service_procedure_request'),
    path('get_ip_billing_datasss', get_ip_billing_datasss, name='get_ip_billing_datasss'),
    
    path('Patients_Management_Filter', Patients_Management_Filter, name='Patients_Management_Filter'),
    path('Patient_Master_List', Patient_Master_List, name='Patient_Master_List'),
    path('Patient_BasicDetails_Update', Patient_BasicDetails_Update, name='Patient_BasicDetails_Update'),
    path('Patients_Counts', Patients_Counts, name='Patients_Counts'),
    path('get_AdmissionDetails', get_AdmissionDetails, name='get_AdmissionDetails'),
    
    
    path('get_patient_casuality_details', get_patient_casuality_details, name='get_patient_casuality_details'),
    path('get_patient_diagnosis_details', get_patient_diagnosis_details, name='get_patient_diagnosis_details'),
    path('get_patient_laboratory_details', get_patient_laboratory_details, name='get_patient_laboratory_details'),
    # path('get_Registration_edit_details', get_Registration_edit_details, name='get_Registration_edit_details'),
    path('get_patient_visit_details', get_patient_visit_details, name='get_patient_visit_details'),



    path('Appointment_Request_List_Link', Appointment_Request_List_Link, name='Appointment_Request_List_link'),
    path('Appointment_Request_Cancel', Appointment_Request_Cancel, name='Appointment_Request_Cancel'),
    path('Appointment_Reschedule_List', Appointment_Reschedule_List, name='Appointment_Reschedule_List'),
    path('get_all_appointments', get_all_appointments, name='get_all_appointments'),
    path('Appointment_Request_List_Delete_Links', Appointment_Request_List_Delete_Links, name='Appointment_Request_List_Delete_Links'),
    path('appointment_request_count_today', appointment_request_count_today, name='appointment_request_count_today'),
    path('calender_modal_display_data_by_day', calender_modal_display_data_by_day, name='calender_modal_display_data_by_day'),
    path('get_available_doctor_by_speciality', get_available_doctor_by_speciality, name='get_available_doctor_by_speciality'),
    path('doctor_available_calender_by_day', doctor_available_calender_by_day, name='doctor_available_calender_by_day'),
    path('daily_appointment_counts_all_doctors', daily_appointment_counts_all_doctors, name='daily_appointment_counts_all_doctors'),
   
       
    path('Get_OP_Billing_Details', Get_OP_Billing_Details, name='Get_OP_Billing_Details'),
    path('Get_OP_Billing_Details_SingleId', Get_OP_Billing_Details_SingleId, name='Get_OP_Billing_Details_SingleId'),

    path('GeneralBilling_Link', GeneralBilling_Link, name='GeneralBilling_Link'),
    path('get_merged_service_data', get_merged_service_data, name='get_merged_service_data'),
    path('get_latest_appointment_for_patient', get_latest_appointment_for_patient, name='get_latest_appointment_for_patient'),
    path('Filter_Patient_data_For_Billing', Filter_Patient_data_For_Billing, name='Filter_Patient_data_For_Billing'),


    path('get_patient_appointment_details_specifydoctor',get_patient_appointment_details_specifydoctor,name='get_patient_appointment_details_specifydoctor'),
    path('Register_Request_Cancel',Register_Request_Cancel,name='Register_Request_Cancel'),
    path('get_patient_appointment_details_withoutcancelled',get_patient_appointment_details_withoutcancelled,name='get_patient_appointment_details_withoutcancelled'),
    path('Registration_Reshedule_Details',Registration_Reshedule_Details,name='Registration_Reshedule_Details'),
    
    path('get_OP_patient_Filter_SpecialityWise',get_OP_patient_Filter_SpecialityWise,name='get_OP_patient_Filter_SpecialityWise'),
    path('get_ip_Patient_registration_details_for_workbench',get_ip_Patient_registration_details_for_workbench,name='get_ip_Patient_registration_details_for_workbench'),
    
    
    path('get_unique_id_no_validation',get_unique_id_no_validation,name='get_unique_id_no_validation'),


    path('Get_IP_Billing_Details', Get_IP_Billing_Details, name='Get_IP_Billing_Details'),
    path('Get_IP_Billing_Details_SingleId', Get_IP_Billing_Details_SingleId, name='Get_IP_Billing_Details_SingleId'),
    path('IP_Billing_Service_List', IP_Billing_Service_List, name='IP_Billing_Service_List'),
    path('IPBilling_Link', IPBilling_Link, name='IPBilling_Link'),
    path('get_merged_service_data_bill', get_merged_service_data_bill, name='get_merged_service_data_bill'),
    path('get_client_insurance_details', get_client_insurance_details, name='get_client_insurance_details'),
    path('get_countries', get_countries, name='get_countries'),
    path('get_states', get_states, name='get_states'),
    path('get_location_by_pincode', get_location_by_pincode, name='get_location_by_pincode'),
    path('get_location_by_params', get_location_by_params, name='get_location_by_params'),
    path('Patient_details_register', Patient_details_register, name='Patient_details_register'),
    path('Filter_Patients_using_Multiple_Criteria', Filter_Patients_using_Multiple_Criteria, name='Filter_Patients_using_Multiple_Criteria'),

 #  For  Pharmacy Billing Op
    path(
        "get_prescription",
        get_prescription,
        name="get_prescription",
    ),
    path(
        "get_prescriptionqueue",
        get_prescriptionqueue,
        name="get_prescriptionqueue",
    ),
    
    path(
        "get_personal_info",
        get_personal_info,
        name="get_personal_info",
    ),
    
     path(
        "get_name",
        get_name,
        name="get_name",
    ),

    
     path(
        "get_quick_list",
        get_quick_list,
        name="get_quick_list",
    ),
     
       #  opbilling
    path(
        "advance_billing_link",
        advance_billing_link,
        name="advance_billing_link",
    ),
     
    path('op_pharmacy_queue_list_prescrib', op_pharmacy_queue_list_prescrib, name='op_pharmacy_queue_list_prescrib'),
    
    path('Get_OP_Doctor_For_appointment',Get_OP_Doctor_For_appointment,name='Get_OP_Doctor_For_appointment'),
    # path('daily_appointment_counts_per_doctor', daily_appointment_counts_per_doctor, name='daily_appointment_counts_per_doctor'),
    path('daily_appointment_patient_list', daily_appointment_patient_list, name='daily_appointment_patient_list'),

    path('get_available_tokenno_by_speciality',get_available_tokenno_by_speciality,name='get_available_tokenno_by_speciality'),


   # bharathi
    path('Patient_management_details', Patient_management_details, name='Patient_management_details'),
    path('patient_details_management_get_link', patient_details_management_get_link, name='patient_details_management_get_link'),
    path('Patient_Datewise_Annotedimage_details', Patient_Datewise_Annotedimage_details, name='Patient_Datewise_Annotedimage_details'),
    path('patient_appointment_details_link', patient_appointment_details_link, name='patient_appointment_details_link'),
    path('Patient_Datewise_Casesheet_details', Patient_Datewise_Casesheet_details, name='Patient_Datewise_Casesheet_details'),
    
    path('get_Patient_Registration_Summary_Details', get_Patient_Registration_Summary_Details, name='get_Patient_Registration_Summary_Details'),
    path('get_referal_doctor_report_details', get_referal_doctor_report_details, name='get_referal_doctor_report_details'),
    path('get_referal_patient_report_details', get_referal_patient_report_details, name='get_referal_patient_report_details'),
    path('get_referal_doctor_by_dept', get_referal_doctor_by_dept, name='get_referal_doctor_by_dept'),
    path('get_total_patient_report_details', get_total_patient_report_details, name='get_total_patient_report_details'),

    path('get_patient_stats', get_patient_stats, name='get_patient_stats'),
    #path('get_age_distribution_for_male', get_age_distribution_for_male, name='get_age_distribution_for_male'),
    #path('get_age_distribution_for_female', get_age_distribution_for_female, name='get_age_distribution_for_female'),
    path('get_age_distribution', get_age_distribution, name='get_age_distribution'),
    path('op_doctor_wise', op_doctor_wise, name='op_doctor_wise'),
    path('ip_doctor_wise', ip_doctor_wise, name='ip_doctor_wise'),
    
    

    path('IP_AdvanceAmount_collection', IP_AdvanceAmount_collection, name='IP_AdvanceAmount_collection'),
    
    path('get_IP_Registration_edit_details', get_IP_Registration_edit_details, name='get_IP_Registration_edit_details'),
    path('Emergency_Patient_Registration', Emergency_Patient_Registration, name='Emergency_Patient_Registration'),
    path('Emergency_Patient_With_Room_Registration_Details_Link', Emergency_Patient_With_Room_Registration_Details_Link, name='Emergency_Patient_With_Room_Registration_Details_Link'),
    path('get_Emergency_patient_details_for_Quelist', get_Emergency_patient_details_for_Quelist, name='get_Emergency_patient_details_for_Quelist'),
    path('get_Emergency_Registration_edit_details', get_Emergency_Registration_edit_details, name='get_Emergency_Registration_edit_details'),
 
    path('get_appointment_check', get_appointment_check, name='get_appointment_check'),
    
    path('get_IP_Patient_Details_by_patientId', get_IP_Patient_Details_by_patientId, name='get_IP_Patient_Details_by_patientId'),
    path('Filter_IP_Patient_by_Multiple_Criteria', Filter_IP_Patient_by_Multiple_Criteria, name='Filter_IP_Patient_by_Multiple_Criteria'),
    path('get_overall_advance_details', get_overall_advance_details, name='get_overall_advance_details'),
    path('get_registered_patient_details', get_registered_patient_details, name='get_registered_patient_details'),
    path('get_Insurance_amount', get_Insurance_amount, name='get_Insurance_amount'),
    path('risk_management_list', risk_management_list, name='risk_management_list'),

    path('OP_Billing_Report', OP_Billing_Report, name='OP_Billing_Report'),
    path('IP_Billing_Report', IP_Billing_Report, name='IP_Billing_Report'),

    # ABHA
    path('abha_register',abha_register,name='abha_register'),
    path('abha_OTP_register',abha_OTP_register,name='abha_OTP_register'),
    path('verifyOtpSubmit',verifyOtpSubmit,name='verifyOtpSubmit'),
    path('ABHA_Mobile_OTP',ABHA_Mobile_OTP,name='ABHA_Mobile_OTP'),
    path('ABHA_Address_Suggestion_API',ABHA_Address_Suggestion_API,name='ABHA_Address_Suggestion_API'),
    path('ABHA_card',ABHA_card,name='ABHA_card'),
    path('ABHA_card_get',ABHA_card_get,name='ABHA_card_get'),
    path('Get_Patient_by_PhoneNo_Using_AbhaRegister',Get_Patient_by_PhoneNo_Using_AbhaRegister,name='Get_Patient_by_PhoneNo_Using_AbhaRegister'),


    path('get_inhouse_doctor_list',get_inhouse_doctor_list,name='get_inhouse_doctor_list'),
    path('get_inhouse_doctor_related_patient_list',get_inhouse_doctor_related_patient_list,name='get_inhouse_doctor_related_patient_list'),
    # inhouse reports backend urls
 
path('get_inhouse_doctor_list',get_inhouse_doctor_list,name='get_inhouse_doctor_list'),
    path('get_inhouse_doctor_related_patient_list',get_inhouse_doctor_related_patient_list,name='get_inhouse_doctor_related_patient_list'),
   
    ]