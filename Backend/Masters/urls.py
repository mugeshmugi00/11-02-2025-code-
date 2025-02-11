from django.urls import path
from .RoomMasters import *
from .ClinicMasters import *
from .ReferalRouteMaster import *
from .DoctorMaster import *
from .BasicMaster import *
from .UserRegisterMaster import *
from .InsuranceClientMaster import *
from .Login import *
from .ServiceProcedureMaster import *
from .RadiologyMaster import *
from .LabMaster import *
from .InstrumentMaster import *
from .doctorworkbench import *
from .RackMaster import*
from .DutyRouster import*
from .SurgeryMaster import *
# from .Frequencymaster import *
from .apprenewal import *
from .Frequencymaster import *
from .RatecardMaster import *
from .Feedback import *
from .OtherLabMasters import *
from .DoctorDahboard import *
from .ServiceMaster import *
from .OTMaster import *


urlpatterns=[
    path('Hospital_Detials_link',Hospital_Detials_link,name='Hospital_Detials_link'),
    path('Clinic_Detials_link', Clinic_Detials_link, name='Clinic_Detials_link'),
    path('get_clinic_detials_by_loc_id', get_clinic_detials_by_loc_id, name='get_clinic_detials_by_loc_id'),
    path('Location_Detials_link',Location_Detials_link, name='Location_Detials_link'),
    path('Department_Detials_link',Department_Detials_link, name='Department_Detials_link'),
    path('Designation_Detials_link',Designation_Detials_link, name='Designation_Detials_link'),
    path('Category_Detials_link',Category_Detials_link, name='Category_Detials_link'),
    path('Speciality_Detials_link',Speciality_Detials_link, name='Speciality_Detials_link'),
    path('Classification_Detials_link',Classification_Detials_link, name='Classification_Detials_link'),
    path('UserRegister_Detials_link',UserRegister_Detials_link, name='UserRegister_Detials_link'),
    path('update_status_User_Detials_link',update_status_User_Detials_link, name='update_status_User_Detials_link'),
    path('Get_User_Detialsby_id',Get_User_Detialsby_id, name='Get_User_Detialsby_id'),
    path('UserControl_Role_link',UserControl_Role_link, name='UserControl_Role_link'),
    path('Flagg_color_Detials_link',Flagg_color_Detials_link, name='Flagg_color_Detials_link'),
    path('Relegion_Master_link',Relegion_Master_link, name='Relegion_Master_link'),
    path('ConsentName_Detials_link',ConsentName_Detials_link, name='ConsentName_Detials_link'),
    path('Doctors_Speciality_Detials_link',Doctors_Speciality_Detials_link, name='Doctors_Speciality_Detials_link'),
    path('Title_Master_link',Title_Master_link, name='Title_Master_link'),
     path('Ward_Detials_link',Ward_Detials_link, name='Ward_Detials_link'),
 
    path('Cast_Master_link',Cast_Master_link, name='Cast_Master_link'),
    path('TriageCategory_Master_link',TriageCategory_Master_link, name='TriageCategory_Master_link'),
    path('BloodGroup_Master_link',BloodGroup_Master_link, name='BloodGroup_Master_link'),
    path('OtTheaterMaster_Detials_link',OtTheaterMaster_Detials_link, name='OtTheaterMaster_Detials_link'),

    path('get_Location_data_for_login', get_Location_data_for_login, name='get_Location_data_for_login'),
    path('login_logic', login_logic, name='login_logic'),
    path('location_Change', location_Change, name='location_Change'),
    path('Building_Master_Detials_link', Building_Master_Detials_link, name='Building_Master_Detials_link'),
    path('get_building_Data_by_location', get_building_Data_by_location, name='get_building_Data_by_location'),
    path('Block_Master_Detials_link', Block_Master_Detials_link, name='Block_Master_Detials_link'),
    path('get_block_Data_by_Building', get_block_Data_by_Building, name='get_block_Data_by_Building'),
    path('Floor_Master_Detials_link', Floor_Master_Detials_link, name='Floor_Master_Detials_link'),
    path('get_Floor_Data_by_Building_block_loc', get_Floor_Data_by_Building_block_loc, name='get_Floor_Data_by_Building_block_loc'),
    path('Ward_Master_Detials_link', Ward_Master_Detials_link, name='Ward_Master_Detials_link'),
    path('get_Ward_Data_by_Building_block_Floor_loc', get_Ward_Data_by_Building_block_Floor_loc, name='get_Ward_Data_by_Building_block_Floor_loc'),
    path('Room_Master_Detials_link', Room_Master_Detials_link, name='Room_Master_Detials_link'),
    path('get_RoomType_Data_by_Building_block_Floor_ward_loc', get_RoomType_Data_by_Building_block_Floor_ward_loc, name='get_RoomType_Data_by_Building_block_Floor_ward_loc'),
    path('Room_Master_Master_Detials_link', Room_Master_Master_Detials_link, name='Room_Master_Master_Detials_link'),
    path('get_RoomNo_Data_by_Building_block_Floor_ward_Room_loc', get_RoomNo_Data_by_Building_block_Floor_ward_Room_loc, name='get_RoomNo_Data_by_Building_block_Floor_ward_Room_loc'),
    path('get_BedNo_Data_by_Building_block_Floor_ward_RoomNo_loc', get_BedNo_Data_by_Building_block_Floor_ward_RoomNo_loc, name='get_BedNo_Data_by_Building_block_Floor_ward_RoomNo_loc'),
    path('get_room_count_data_total', get_room_count_data_total, name='get_room_count_data_total'),
    path('get_Room_Master_Data', get_Room_Master_Data, name='get_Room_Master_Data'),
    path('get_Room_Master_Data_for_registration', get_Room_Master_Data_for_registration, name='get_Room_Master_Data_for_registration'),
    path('get_filter_Data_for_registration', get_filter_Data_for_registration, name='get_filter_Data_for_registration'),
    
    
    
    path('Route_Master_Detials_link', Route_Master_Detials_link, name='Route_Master_Detials_link'),
    path('Doctor_Detials_link', Doctor_Detials_link, name='Doctor_Detials_link'),
    path('get_Doctor_Detials_link', get_Doctor_Detials_link, name='get_Doctor_Detials_link'),
    path('update_status_Doctor_Detials_link', update_status_Doctor_Detials_link, name='update_status_Doctor_Detials_link'),
    path('get_Doctor_Ratecard_link', get_Doctor_Ratecard_link, name='get_Doctor_Ratecard_link'),
    path('doctor_Ratecard_details_view_by_doctor_id', doctor_Ratecard_details_view_by_doctor_id, name='doctor_Ratecard_details_view_by_doctor_id'),
    path('doctor_Ratecard_details_update', doctor_Ratecard_details_update, name='doctor_Ratecard_details_update'),
    path('get_User_Doctor_Detials', get_User_Doctor_Detials, name='get_User_Doctor_Detials'),
    path('get_referral_doctor_Name_Detials', get_referral_doctor_Name_Detials, name='get_referral_doctor_Name_Detials'),
    path('get_Doctor_by_Speciality_Detials', get_Doctor_by_Speciality_Detials, name='get_Doctor_by_Speciality_Detials'),
    path('get_route_details', get_route_details, name= 'get_route_details'),
    path('get_All_doctor_Name_Detials', get_All_doctor_Name_Detials, name='get_All_doctor_Name_Detials'),
    path('Insurance_Client_Master_Detials_link', Insurance_Client_Master_Detials_link, name='Insurance_Client_Master_Detials_link'),
    path('update_status_Insurance_Client_Detials_link', update_status_Insurance_Client_Detials_link, name='update_status_Insurance_Client_Detials_link'),
    path('get_insurance_client_name', get_insurance_client_name, name='get_insurance_client_name'),
    path('get_insurance_data_registration', get_insurance_data_registration, name='get_insurance_data_registration'),
    path('get_client_data_registration', get_client_data_registration, name='get_client_data_registration'),
    path('get_donation_data_registration', get_donation_data_registration, name='get_donation_data_registration'),
    path('Service_Procedure_Master_Detials_link', Service_Procedure_Master_Detials_link, name='Service_Procedure_Master_Detials_link'),
    path('update_status_Service_Procedure_Detials_link', update_status_Service_Procedure_Detials_link, name='update_status_Service_Procedure_Detials_link'),
    path('Service_Procedure_Ratecard_details_view_by_id', Service_Procedure_Ratecard_details_view_by_id, name='Service_Procedure_Ratecard_details_view_by_id'),
    path('Service_Procedure_Ratecard_details_update', Service_Procedure_Ratecard_details_update, name='Service_Procedure_Ratecard_details_update'),
    path('get_service_procedure_for_ip', get_service_procedure_for_ip, name='get_service_procedure_for_ip'),
  
  
  
    path('doctor_calender_details_view_by_doctor_id', doctor_calender_details_view_by_doctor_id, name='doctor_calender_details_view_by_doctor_id'),
    path('doctor_calender_details_view_by_day', doctor_calender_details_view_by_day, name='doctor_calender_details_view_by_day'),
    path('doctor_calender_details_view_by_doctorId_locationId', doctor_calender_details_view_by_doctorId_locationId, name='doctor_calender_details_view_by_doctorId_locationId'),
    path('calender_modal_display_data_by_day', calender_modal_display_data_by_day, name='calender_modal_display_data_by_day'),
    path('calender_modal_display_edit_by_day', calender_modal_display_edit_by_day, name='calender_modal_display_edit_by_day'),
    path('calender_modal_display_edit_by_mutiple_day', calender_modal_display_edit_by_mutiple_day, name='calender_modal_display_edit_by_mutiple_day'),
    path('Appointment_Request_List_Links', Appointment_Request_List_Links, name='Appointment_Request_List_Links'),
    path('Appointment_Request_List_Delete_Links', Appointment_Request_List_Delete_Links, name='Appointment_Request_List_Delete_Links'),

    
    
    path('Radiology_Names_link',Radiology_Names_link,name='Radiology_Names_link'),
    path('Radiology_details_link',Radiology_details_link,name='Radiology_details_link'),
    path('Radiology_details_link_view',Radiology_details_link_view,name='Radiology_details_link_view'),
    path('inhouse_doctor_details',inhouse_doctor_details,name="inhouse_doctor_details"),
    
    path('Lab_Test_Name_link',Lab_Test_Name_link,name="Lab_Test_Name_link"),
    path('Test_Names_link',Test_Names_link,name="Test_Names_link"),
    path('Favourite_TestNames_Details',Favourite_TestNames_Details,name="Favourite_TestNames_Details"),
    path('Favourites_Names_link',Favourites_Names_link,name="Favourites_Names_link"),
    path('Test_Names_link_LabTest',Test_Names_link_LabTest,name='Test_Names_link_LabTest'),
    
    path('Instrument_Name_link',Instrument_Name_link,name="Instrument_Name_link"),
    path('Instruiment_Names_link',Instruiment_Names_link,name="Instruiment_Names_link"),
    path('Instrument_Tray_Names_link',Instrument_Tray_Names_link,name="Instrument_Tray_Names_link"),
    path('OpDoctor_Details_link',OpDoctor_Details_link,name="OpDoctor_Details_link"),
    path('OpPatients_Details_link',OpPatients_Details_link,name="OpPatients_Details_link"),
    path('StatusUpdate_Details_Patient',StatusUpdate_Details_Patient,name="StatusUpdate_Details_Patient"),
    path('StatusUpdate_Details_Patient_Reshedule',StatusUpdate_Details_Patient_Reshedule,name="StatusUpdate_Details_Patient_Reshedule"),
    path('StatusUpdate_Details_Patient_Cancel',StatusUpdate_Details_Patient_Cancel,name="StatusUpdate_Details_Patient_Cancel"),
    path('Status_Duration_link',Status_Duration_link,name="Status_Duration_link"),
    path('Status_Patient_Details_link',Status_Patient_Details_link,name="Status_Patient_Details_link"),
    path('Separated_Patient_Details_link',Separated_Patient_Details_link,name="Separated_Patient_Details_link"),
    path('VisitPurpose_Patient_Details_link',VisitPurpose_Patient_Details_link,name="VisitPurpose_Patient_Details_link"),
    path('inhouse_doctor_details',inhouse_doctor_details,name="inhouse_doctor_details"),
    
    
     path('Rack_Detials_link', Rack_Detials_link, name='Rack_Detials_link'),
    path('Shelf_Detials_link',Shelf_Detials_link,name="Shelf_Detials_link"),
    path('Tray_Detials_link',Tray_Detials_link,name="Tray_Detials_link"),
    # path('ProductCategory_Master_link',ProductCategory_Master_link,name='ProductCategory_Master_link'),
    path('Medical_Stock_InsetLink',Medical_Stock_InsetLink,name='Medical_Stock_InsetLink'),
    path('ProductType_Master_lik',ProductType_Master_lik,name='ProductType_Master_lik'),
    
    
    path('Duty_rouster_master_link',Duty_rouster_master_link,name='Duty_rouster_master_link'),
    # path('insert_frequency_masters', insert_frequency_masters, name='insert_frequency_masters'),
    
    

    path('Surgery_Names_link',Surgery_Names_link,name='Surgery_Names_link'),
    path('Surgeryname_Speciality_link',Surgeryname_Speciality_link,name='Surgeryname_Speciality_link'),
    path('Surgeryname_Speciality_Doctor_link',Surgeryname_Speciality_Doctor_link,name='Surgeryname_Speciality_Doctor_link'),
    
    path('get_All_DoctorNames',get_All_DoctorNames,name='get_All_DoctorNames'),
    path('get_All_DoctorNames_with_specialitySpecific',get_All_DoctorNames_with_specialitySpecific,name='get_All_DoctorNames_with_specialitySpecific'),
    
    path('get_data',get_data,name='get_data'),
    path('update_session',update_session,name='update_session'),
    path('send_otp',send_otp,name='send_otp'),
    path('save_new_password',save_new_password,name='save_new_password'),
    path('getemail_for_user',getemail_for_user,name='getemail_for_user'),
    path('subscribeapp',subscribeapp,name='subscribeapp'),
    path('marquerun',marquerun,name='marquerun'),
    
    
    path('get_DoctorSchedule_details',get_DoctorSchedule_details,name='get_DoctorSchedule_details'),

    path('External_LabDetails_Link',External_LabDetails_Link,name='External_LabDetails_Link'),
    path('Active_LabDetails_Link',Active_LabDetails_Link,name='Active_LabDetails_Link'),
    path('Radiology_Department_TestNames',Radiology_Department_TestNames,name='Radiology_Department_TestNames'),
    # path('Radiology_TestName_SubTestNames',Radiology_TestName_SubTestNames,name='Radiology_TestName_SubTestNames'),

    path('Inventory_Master_Detials_link',Inventory_Master_Detials_link,name='Inventory_Master_Detials_link'),

    path('Difine_Tray_For_Products',Difine_Tray_For_Products,name='Difine_Tray_For_Products'),
    path('Tray_Management_List_For_Products',Tray_Management_List_For_Products,name='Tray_Management_List_For_Products'),

    path('Pack_Type_link',Pack_Type_link,name='Pack_Type_link'),
    path('GenericName_Master_Link',GenericName_Master_Link,name='GenericName_Master_Link'),
    path('CompanyName_Master_Link',CompanyName_Master_Link,name='CompanyName_Master_Link'),
    
     path('SubCategory_Master_link',SubCategory_Master_link,name='SubCategory_Master_link'),
    path('Product_Group_Link',Product_Group_Link,name='Product_Group_Link'),
    
    path('Medical_Stock_InsetLink',Medical_Stock_InsetLink,name='Medical_Stock_InsetLink'),
    path('ProductType_Master_lik',ProductType_Master_lik,name='ProductType_Master_lik'),
    
    
    
    path('insert_frequency_masters',insert_frequency_masters,name='insert_frequency_masters'),
    path('get_corporate_data_registration', get_corporate_data_registration, name='get_corporate_data_registration'),
    
    path('ICDCode_Master_InsetLink',ICDCode_Master_InsetLink,name='ICDCode_Master_InsetLink'),
    path('ICDCode_Master_DoctorGetLink',ICDCode_Master_DoctorGetLink,name='ICDCode_Master_DoctorGetLink'),
    path('GradeName_Master_link', GradeName_Master_link, name='GradeName_Master_link'),
    path('Active_GradeNames_link', Active_GradeNames_link, name='Active_GradeNames_link'),
    path('Active_Rooms_link', Active_Rooms_link, name='Active_Rooms_link'),
    path('TherapyType_Master_link',TherapyType_Master_link, name='TherapyType_Master_link'),
    path('TherapyTypes_Active_link',TherapyTypes_Active_link,name='TherapyTypes_Active_link'),
    
    
    path('Insurance_client_master_details',Insurance_client_master_details,name='Insurance_client_master_details'),
    path('Overall_services_link',Overall_services_link,name='Overall_services_link'),
    path('UpdateRatecardDetails',UpdateRatecardDetails,name='UpdateRatecardDetails'),
    path('Get_RoomDetails_Ratecard',Get_RoomDetails_Ratecard,name='Get_RoomDetails_Ratecard'),

    path('insert_into_feedback', insert_into_feedback, name= 'insert_into_feedback'),
    path('get_feedback_data_for_chart', get_feedback_data_for_chart, name = 'get_feedback_data_for_chart'),
    path('get_all_feedback_data', get_all_feedback_data, name='get_all_feedback_data'),
    path('insert_insto_alert_table', insert_insto_alert_table, name='insert_insto_alert_table'),


    path('Flagg_color_Detials_by_specialtype',Flagg_color_Detials_by_specialtype, name='Flagg_color_Detials_by_specialtype'),


# Lab Masters
    path('Get_All_Other_Masters_PrimaryCodes',Get_All_Other_Masters_PrimaryCodes,name='Get_All_Other_Masters_PrimaryCodes'),
    path('All_Other_Lab_Masters_POST_AND_GET',All_Other_Lab_Masters_POST_AND_GET,name='All_Other_Lab_Masters_POST_AND_GET'),
    path('Update_All_Masters_Status_update',Update_All_Masters_Status_update,name='Update_All_Masters_Status_update'),
    path('All_CSV_Files_Upload',All_CSV_Files_Upload,name='All_CSV_Files_Upload'),
    path('Update_Formula_And_ResultValue',Update_Formula_And_ResultValue,name='Update_Formula_And_ResultValue'),

    path('get_patient_stats_ddashboard',get_patient_stats_ddashboard,name='get_patient_stats_ddashboard'),
    path('get_total_appointment',get_total_appointment,name='get_total_appointment'),
    
    
    path('Administration_Details_link',Administration_Details_link,name='Administration_Details_link'),
    
    
    path('NurseStationData',NurseStationData,name='NurseStationData'),
    path('get_Ward_Data_by_Floor_loc',get_Ward_Data_by_Floor_loc,name='get_Ward_Data_by_Floor_loc'),

    path('Insert_service_category_master', Insert_service_category_master, name= 'Insert_service_category_master'),

    
    # bharathi
    path('GenericName_by_Product_SubProduct', GenericName_by_Product_SubProduct, name='GenericName_by_Product_SubProduct'),
    path('CompanyName_by_Product_SubProduct', CompanyName_by_Product_SubProduct, name='CompanyName_by_Product_SubProduct'),
    path('Product_Group_by_Product_SubProduct', Product_Group_by_Product_SubProduct, name='Product_Group_by_Product_SubProduct'),
    path('PackType_by_Product_SubProduct', PackType_by_Product_SubProduct, name='PackType_by_Product_SubProduct'),
    path('ProductType_by_Product_SubProduct', ProductType_by_Product_SubProduct, name='ProductType_by_Product_SubProduct'),


    path('Services_List', Services_List, name= 'Services_List'),
    path('service_map_details', service_map_details, name= 'service_map_details'),
    path('packege_master_details', packege_master_details, name= 'packege_master_details'),
    path('services_Group_list_details', services_Group_list_details, name= 'services_Group_list_details'),
    path('services_Subcategory_details_by_category', services_Subcategory_details_by_category, name= 'services_Subcategory_details_by_category'), 
    path('services_Subcategory_details_by_Patient_category', services_Subcategory_details_by_Patient_category, name= 'services_Subcategory_details_by_Patient_category'),
    path('Services_Group_details', Services_Group_details, name= 'Services_Group_details'),
    path('service_map_delete', service_map_delete, name= 'service_map_delete'),

    path('get_Building_data', get_Building_data, name= 'get_Building_data'),
    path('get_floor_data_by_Block', get_floor_data_by_Block, name= 'get_floor_data_by_Block'),
    path('get_Ward_details_by_floor', get_Ward_details_by_floor, name= 'get_Ward_details_by_floor'),
    path('get_patient_appointment_details', get_patient_appointment_details, name= 'get_patient_appointment_details'),
    # path('get_bed_details_by_ward', get_bed_details_by_ward, name= 'get_bed_details_by_ward'),

    path('service_added_details', service_added_details, name= 'service_added_details'),
    
    #OT
   path('Theatrename_all', Theatrename_all, name= 'Theatrename_all'),
    path('Doctorname_for_OTBooking', Doctorname_for_OTBooking, name= 'Doctorname_for_OTBooking'),
    path('Surgeon_list', Surgeon_list, name= 'Surgeon_list'), 
    path('Surgeon_list_for_calendar', Surgeon_list_for_calendar, name= 'Surgeon_list_for_calendar'), 
    
    path('Assistant_Surgeon_list', Assistant_Surgeon_list, name= 'Assistant_Surgeon_list'),
    path('Anaesthesiologist_list', Anaesthesiologist_list, name= 'Anaesthesiologist_list'),
    path('Scrub_Nurse_list', Scrub_Nurse_list, name= 'Scrub_Nurse_list'),
    path('Circulating_Nurse_list', Circulating_Nurse_list, name= 'Circulating_Nurse_list'),
    path('Technician_list', Technician_list, name= 'Technician_list'),
    path('Helper_list', Helper_list, name= 'Helper_list'),
    path('Theatre_booking_request_details', Theatre_booking_request_details, name= 'Theatre_booking_request_details'),
    path('OTQueuelist_details', OTQueuelist_details, name= 'OTQueuelist_details'),
    path('Theatre_booking_request_detail_by_Patient', Theatre_booking_request_detail_by_Patient, name= 'Theatre_booking_request_detail_by_Patient'),
    path('Theatre_booking_request_Outside_details', Theatre_booking_request_Outside_details, name= 'Theatre_booking_request_Outside_details'),
    path('Surgical_Team_details', Surgical_Team_details, name= 'Surgical_Team_details'),
    path('get_item_details_for_consumables',get_item_details_for_consumables, name= 'get_item_details_for_consumables'),
    path('get_store_name_for_OT',get_store_name_for_OT, name= 'get_store_name_for_OT'),
    path('get_Theatre_name_for_OT_Calendar',get_Theatre_name_for_OT_Calendar,name = 'get_Theatre_name_for_OT_Calendar'),
    path('get_ot_availability',get_ot_availability,name='get_ot_availability'),
    path('Consumable_details',Consumable_details,name='Consumable_details'),
    path('Consignment_details',Consignment_details,name='Consignment_details'),
    path('OTCompletepatient_details',OTCompletepatient_details,name='OTCompletepatient_details'),
    path('Equipment_details',Equipment_details,name = 'Equipment_details'),
    path('OTConfirmedpatient_details',OTConfirmedpatient_details,name='OTConfirmedpatient_details'),
    path('OTCalendar_Booking_Status',OTCalendar_Booking_Status,name='OTCalendar_Booking_Status'),
    path('get_Ward_details_by_floor_for_ot',get_Ward_details_by_floor_for_ot,name ='get_Ward_details_by_floor_for_ot'),
    path('get_ot_doctor_availability',get_ot_doctor_availability,name="get_ot_doctor_availability"),
   # path('Theatre_booking_request_detail_by_status',Theatre_booking_request_detail_by_status,name='Theatre_booking_request_detail_by_status'),
    path('OT_Billing_details',OT_Billing_details,name='OT_Billing_details'),
    path('Services_List_by_servicecategory',Services_List_by_servicecategory,name='Services_List_by_servicecategory'),
    
   

]