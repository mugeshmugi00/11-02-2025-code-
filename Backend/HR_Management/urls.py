from django.urls import path
from .DutyMaster import *
from .EmployeeShift import *
from .EmployeeRequest import *
from .EmployeeRegistration import *
from .DutyManagement import *
from .TraineeRegistration import *


urlpatterns=[
   
    path('Employee_Registration_Details',Employee_Registration_Details,name='Employee_Registration_Details'),
    path('get_User_Employee_Details',get_User_Employee_Details,name='get_User_Employee_Details'),
    path('DutyRosterMasters', DutyRosterMasters, name='DutyRosterMasters'),
    path('Shift_Details_link', Shift_Details_link, name='Shift_Details_link'),
    path('Get_Employee_Registered_Details', Get_Employee_Registered_Details, name='Get_Employee_Registered_Details'),
    path('filter_Sourcewise_Employee_Details', filter_Sourcewise_Employee_Details, name='filter_Sourcewise_Employee_Details'),

    path('Employee_Details',Employee_Details, name='Employee_Details'),
    path('Employee_Leave_Details', Employee_Leave_Details, name='Employee_Leave_Details'),
    path('Insert_Leave_Register', Insert_Leave_Register, name='Insert_Leave_Register'),
    path('Employee_Leave_Status_Link', Employee_Leave_Status_Link, name='Employee_Leave_Status_Link'),
    path('Employee_Permission_Status_Link', Employee_Permission_Status_Link, name='Employee_Permission_Status_Link'),
    path('Employee_FullLeave_Status_Link', Employee_FullLeave_Status_Link, name='Employee_FullLeave_Status_Link'),
    path('Employee_FullPermission_Status_Link', Employee_FullPermission_Status_Link, name='Employee_FullPermission_Status_Link'),
    path('Insert_AdvanceRequest_Register', Insert_AdvanceRequest_Register, name='Insert_AdvanceRequest_Register'),
    path('Employee_PrevAdvance_Details', Employee_PrevAdvance_Details, name='Employee_PrevAdvance_Details'),
    path('Req_Recent_Advance_Register_Recent', Req_Recent_Advance_Register_Recent, name='Req_Recent_Advance_Register_Recent'),
    path('Employee_Designation_Details', Employee_Designation_Details, name='Employee_Designation_Details'),
    path('Employee_Advance_RequestList_link', Employee_Advance_RequestList_link, name='Employee_Advance_RequestList_link'),
    path('Prev_Amount_Details', Prev_Amount_Details, name='Prev_Amount_Details'),
    path('update_Advance_Approval', update_Advance_Approval, name='update_Advance_Approval'),
    path('Advance_Amount_Details', Advance_Amount_Details, name='Advance_Amount_Details'),
    path('AdvanceComplete_Amount_Details', AdvanceComplete_Amount_Details, name='AdvanceComplete_Amount_Details'),
    path('All_Employee_Leave_Status_Link', All_Employee_Leave_Status_Link, name='All_Employee_Leave_Status_Link'),
    path('All_Permission_details_link', All_Permission_details_link, name='All_Permission_details_link'),
    path('Employee_Consume_Permission_Link', Employee_Consume_Permission_Link, name='Employee_Consume_Permission_Link'),
    path('Employee_Previous_Leave_Details', Employee_Previous_Leave_Details, name='Employee_Previous_Leave_Details'),
    path('update_Advance_Leave', update_Advance_Leave, name='update_Advance_Leave'),
    path('Employee_Permission_Details', Employee_Permission_Details, name='Employee_Permission_Details'),
    path('All_Consumed_Leave', All_Consumed_Leave, name='All_Consumed_Leave'),
    path('All_Consume_Permission_details', All_Consume_Permission_details, name='All_Consume_Permission_details'),
    
    # DutyManagement
    path('Employee_DutyManagement_Details', Employee_DutyManagement_Details, name='Employee_DutyManagement_Details'),
    path('Employee_ShiftDetails_Link', Employee_ShiftDetails_Link, name='Employee_ShiftDetails_Link'),
    path('update_Shift_Detail_Link', update_Shift_Detail_Link, name='update_Shift_Detail_Link'),
    path('Employee_Complete_ShiftDetails_Link', Employee_Complete_ShiftDetails_Link, name='Employee_Complete_ShiftDetails_Link'),
    path('Shift_Details_Report', Shift_Details_Report, name='Shift_Details_Report'),
    
    # Attendence
    path('insert_attendance_report', insert_attendance_report, name='insert_attendance_report'),
      path('attendance_report', attendance_report, name='attendance_report'),
    path('holiday', holiday, name='holiday'),
    path('Attendance_Master_InsetLink', Attendance_Master_InsetLink, name='Attendance_Master_InsetLink'),
    path('Employee_Shift_Details_Link', Employee_Shift_Details_Link, name='Employee_Shift_Details_Link'),
    path('Employee_Report_Details_link', Employee_Report_Details_link, name='Employee_Report_Details_link'),

    path('Employee_Monthly_Report', Employee_Monthly_Report, name='Employee_Monthly_Report'),

    path('insert_EmployeePaySlips', insert_EmployeePaySlips, name='insert_EmployeePaySlips'),
  

    path('getforemployeepayrolllist', getforemployeepayrolllist, name='getforemployeepayrolllist'),
    path('EmployeePayslipDownload', EmployeePayslipDownload, name='EmployeePayslipDownload'),


    path('Employee_Monthly_Report', Employee_Monthly_Report, name='Employee_Monthly_Report'),
   


    path('Employee_Monthly_Report', Employee_Monthly_Report, name='Employee_Monthly_Report'),
    path('getemployeelistforappraisal', getemployeelistforappraisal, name='getemployeelistforappraisal'),
    path('employee_performanceamount', employee_performanceamount, name='employee_performanceamount'),
    path('insert_employee_performance', insert_employee_performance, name='insert_employee_performance'),
    path('employee_allowance', employee_allowance, name='employee_allowance'),
    path('get_employeeperformance', get_employeeperformance, name='get_employeeperformance'),
    path('Add_Complaint', Add_Complaint, name='Add_Complaint'),
    path('Complaint_Details', Complaint_Details, name='Complaint_Details'),
    path('All_Complaint_list', All_Complaint_list, name='All_Complaint_list'),
    path('insert_ComplaintActions', insert_ComplaintActions, name='insert_ComplaintActions'),
    path('Employee_Details_by_Designation', Employee_Details_by_Designation, name='Employee_Details_by_Designation'),
    path('Add_Circular', Add_Circular, name='Add_Circular'),
    path('get_circular_Details', get_circular_Details, name='get_circular_Details'),

    path('Employee_AttendnanceManagement_Details', Employee_AttendnanceManagement_Details, name='Employee_AttendnanceManagement_Details'),

    path('get_username_details', get_username_details, name='get_username_details'),
    path("DutyAssign_IndEmployee",DutyAssign_IndEmployee,name="DutyAssign_IndEmployee"),
    path('Trainee_Registration_Details', Trainee_Registration_Details, name='Trainee_Registration_Details'),

]
