import React, { useState, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux';
import ToastAlert from '../../OtherComponent/ToastContainer/ToastAlert';
import axios from "axios";
import { useNavigate } from 'react-router-dom';

const UserRegisterMaster = () => {
  const UrlLink = useSelector(state => state.userRecord?.UrlLink);
  const userRecord = useSelector(state => state.userRecord?.UserData);
  const toast = useSelector(state => state.userRecord?.toast);
  const UserListId = useSelector(state => state.userRecord?.UserListId);
  const Usercreatedocdata = useSelector(state => state.userRecord?.Usercreatedocdata);
  const UsercreateEmpdata = useSelector(state => state.userRecord?.UsercreateEmpdata);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  console.log('UsercreateEmpdata---999', UsercreateEmpdata);


  const [UserRegister, setUserRegister] = useState({
    UserId: '',
    EmployeeType: '',
    DoctorId: '',
    EmployeeId: '',
    Title: '',
    firstName: '',
    middleName: '',
    lastName: '',
    Email: '',
    PhoneNo: '',
    Gender: '',
    Qualification: '',
    UserName: '',
    Password: '',
    roleName: '',
  });

  const [UserRegistershow, setUserRegistershow] = useState([])
  const [RoleNameData, setRoleNameData] = useState([]);

  useEffect(() => {
    axios.get(`${UrlLink}Masters/UserControl_Role_link`)
      .then((res) => {
        const ress = res.data;
        setRoleNameData(ress);
      })
      .catch((err) => {
        console.log(err);
      });
  }, [UrlLink]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setUserRegister((prevState) => ({
      ...prevState,
      [name]: value
    }));
  };








  const [checkedItems, setCheckedItems] = useState([
    // {
    //   key: '1',
    //   value: 'A',
    //   label: 'ClinicMetrics',
    //   check: false,
    //   children: []
    // },
    {
      key: '1',
      value: 'A',
      label: 'FrontOffice',
      check: false,
      children: [
        { key: '1-1', value: 'A1-1', label: 'Dashboard', check: false },
        { key: '1-2', value: 'A1-2', label: 'AppoinmentRequestList', check: false },
        { key: '1-3', value: 'A1-3', label: 'NewBasicRegistation', check: false },
        { key: '1-4', value: 'A1-4', label: 'OPVisitEntry', check: false },
        { key: '1-5', value: 'A1-5', label: 'IPRegistration', check: false },
        // { key: '1-6', value: 'A1-6', label: 'OPDQueueList', check: false },
        { key: '1-7', value: 'A1-7', label: 'PatientRegisterList', check: false },
        { key: '1-8', value: 'A1-8', label: 'GeneralBilling', check: false },
        { key: '1-9', value: 'A1-9', label: 'OPDQueueList', check: false },
        // { key: '1-10', value: 'A1-10', label: 'DoctorScheduleCalendar', check: false },
        { key: '1-11', value: 'A1-11', label: 'PatientManagement', check: false },
        { key: '1-12', value: 'A1-12', label: 'IPRequestList', check: false },
        { key: '1-13', value: 'A1-13', label: 'DoctorScheduleCalendar', check: false },
        { key: '1-14', value: 'A1-14', label: 'PatientReports', check: false },
        // { key: '1-15', value: 'A1-15', label: 'NewBasicRegistation', check: false },
        // { key: '1-16', value: 'A1-16', label: '', check: false },
        // { key: '1-17', value: 'A1-17', label: '', check: false },
        { key: '1-18', value: 'A1-18', label: 'SelfRegistration', check: false },
        // { key: '1-19', value: 'A1-19', label: '', check: false },
        { key: '1-20', value: 'A1-20', label: 'PatientRegistration', check: false },
        // { key: '1-21', value: 'A1-21', label: '', check: false },
        // { key: '1-22', value: 'A1-22', label: '', check: false },
      ]
    },
    {
      key: '2',
      value: 'B',
      label: 'OPD_Reception',
      check: false,
      children: [
        { key: '2-1', value: 'B2-1', label: 'OP_patients', check: false },
        // { key: '2-2', value: 'B2-2', label: '', check: false },
        // { key: '2-3', value: 'B2-3', label: '', check: false }
      ]
    },
    {
      key: '3',
      value: 'C',
      label: 'Nurse',
      check: false,
      children: [
        { key: '3-1', value: 'C3-1', label: 'PatientQuelist', check: false },
        { key: '3-2', value: 'C3-2', label: 'BirthRegisterList', check: false },
        { key: '3-3', value: 'C3-3', label: 'DeathRegisterList', check: false },
        { key: '3-4', value: 'C3-4', label: 'OpNurse_WorkbenchNavigation', check: false },
        { key: '3-5', value: 'C3-5', label: 'IP_NurseWorkbenchNavigation', check: false },
      ]
    },
    {
      key: '4',
      value: 'D',
      label: 'Doctor',
      check: false,
      children: [
        { key: '4-1', value: 'D4-1', label: 'Doctordashboard', check: false },
        { key: '4-2', value: 'D4-2', label: 'PatientQuelist', check: false },
        { key: '4-3', value: 'D4-3', label: 'SpecialityWiseDoctorPatientList', check: false },
        // { key: '3-2', value: 'C3-2', label: 'PatientQueueList', check: false }
      ]
    },

    {
      key: '5',
      value: 'E',
      label: 'WardManagement',
      check: false,
      children: [
        { key: '5-1', value: 'E5-1', label: 'Warddashboard', check: false },
        { key: '5-2', value: 'E5-2', label: 'IPHandOverList', check: false },
        { key: '5-3', value: 'E5-3', label: 'RoomMangement', check: false },
        { key: '5-4', value: 'E5-4', label: 'IPQueList', check: false },
      ]
    },


        {
      key: '6',
      value: 'F',
      label: 'NurseStation',
      check: false,
      children: [
        { key: '6-1', value: 'F6-1', label: 'InventoryNurseStation', check: false },
        { key: '6-2', value: 'F6-2', label: 'PatientQueList', check: false },
        { key: '6-3', value: 'F6-3', label: 'BreakageMaintenance', check: false },
        // { key: '6-4', value: 'F6-4', label: '', check: false },
        // { key: '6-5', value: 'F6-5', label: '', check: false },
        // { key: '6-6', value: 'F6-6', label: '', check: false },

      ]
    },
    

    {
      key: '7',
      value: 'G',
      label: 'OTManagement',
      check: false,
      children: [
        { key: '7-1', value: 'G7-1', label: 'OtMaster', check: false },
        { key: '7-2', value: 'G7-2', label: 'NewOTBook', check: false },
        { key: '7-3', value: 'G7-3', label: 'OT_Queue_List', check: false },
        { key: '7-4', value: 'G7-4', label: 'SurgicalTeam', check: false },
        { key: '7-5', value: 'G7-5', label: 'Doctor_OueueList', check: false },
        { key: '7-6', value: 'G7-6', label: 'OT_Doctor', check: false },
        { key: '7-7', value: 'G7-7', label: 'OT_Anaesthesia', check: false },
        { key: '7-8', value: 'G7-8', label: 'OT_Nurse', check: false },
        { key: '7-9', value: 'G7-9', label: 'OtCharges', check: false },
        { key: '7-10', value: 'G7-10', label: 'OTReports', check: false },
        { key: '7-11', value: 'G7-11', label: 'OTCompletelist', check: false },

      ]
    },
    
    
    
    
    {
      key: '8',
      value: 'H',
      label: 'Pharmacy',
      check: false,
      children: [
        { key: '8-1', value: 'H8-1', label: 'OPPharmachyBillingList', check: false },
        { key: '8-2', value: 'H8-2', label: 'IPPharmacyBillingList', check: false },
        { key: '8-3', value: 'H8-3', label: 'PharmacyWalkinQue', check: false },
        
      ]
    },
    {
      key: '9',
      value: 'I',
      label: 'Cashier',
      check: false,
      children: [
        { key: '9-1', value: 'I9-1', label: 'CashierDashboard', check: false },
        { key: '9-2', value: 'I9-2', label: 'GeneralBillingList', check: false },
        { key: '9-3', value: 'I9-3', label: 'GeneralBillingEditList', check: false },
        { key: '9-4', value: 'I9-4', label: 'IPBillingList', check: false },
        { key: '9-5', value: 'I9-5', label: 'IPBillingEditList', check: false },
        { key: '9-6', value: 'I9-6', label: 'IP_BillingDischargeQueslist', check: false },
        { key: '9-7', value: 'I9-7', label: 'LabQueuelist', check: false },
        { key: '9-8', value: 'I9-8', label: 'AdvanceCollection', check: false },
        { key: '9-9', value: 'I9-9', label: 'RiskManagementList', check: false },

      ]
    },

    {
      key: '10',
      value: 'J',
      label: 'Insurance',
      check: false,
      children: [
        { key: '10-1', value: 'J10-1', label: 'InsuranceDashboard', check: false },
        { key: '10-2', value: 'J10-2', label: 'ClientDashboard', check: false },

      ]
    },


    // {
    //   key: '11',
    //   value: 'K',
    //   label: 'CRMdashboard',
    //   check: false,
    //   children: [
    //     { key: '11-1', value: 'k11-1', label: 'Opfollowup', check: false },
    //     { key: '11-2', value: 'k11-2', label: 'IPfollowup', check: false },
    //     { key: '11-3', value: 'k11-3', label: 'Discharge', check: false },
    //     { key: '11-4', value: 'k11-4', label: 'Therapy', check: false },
    //     { key: '11-5', value: 'k11-5', label: 'Labque', check: false },
    //     { key: '11-6', value: 'k11-6', label: 'Radiologyque', check: false },

    //   ]
    // },

    
    {
      key: '12',
      value: 'L',
      label: 'Lab',
      check: false,
      children: [
        { key: '12-1', value: 'L12-1', label: 'SampleCollectionQueue'        , check: false },
        { key: '12-2', value: 'L12-2', label: 'ResultEntryQueueList'         , check: false },
      //   { key: '12-3', value: 'L12-3', label: 'NewNavigationMasters', check: false },
      //   { key: '12-4', value: 'L12-4', label: 'ExternalLabMaster', check: false },
      //   { key: '12-5', value: 'L12-5', label: 'ReferDoctor', check: false },
      //   { key: '12-6', value: 'L12-6', label: 'RatecardLims', check: false },
      //   { key: '12-7', value: 'L12-7', label: 'GroupMaster', check: false },
      //   { key: '12-8', value: 'L12-8', label: 'IP_LabDischargeQueslist', check: false },
      ]
    },

    {
      key: '13',
      value: 'M',
      label: 'Radiology',
      check: false,
      children: [
        { key: '13-1', value: 'M13-1', label: 'RadiologyQuelist'             , check: false },
        { key: '13-2', value: 'M13-2', label: 'Mritechnician'                , check: false },
        { key: '13-3', value: 'M13-3', label: 'Cttechnician'                 , check: false },
        { key: '13-4', value: 'M13-4', label: 'XRayTechnician'               , check: false },
        { key: '13-5', value: 'M13-5', label: 'IP_RadiologyDischargeQueslist', check: false },

      ]
    },

    {
      key: '14',
      value: 'N',
      label: 'Therapy',
      check: false,
      children: [
        { key: '14-1', value: 'N14-1', label: 'RadiologyQuelist'            , check: false },
        
      ]
    },

    {
      key: '15',
      value: 'O',
      label: 'Master',
      check: false,
      children: [
        { key: '15-1', value: 'O15-1', label: 'HospitalClinicMaster'        , check: false },
        // { key: '15-2', value: 'O15-2', label: 'DutyRousterMaster'        , check: false },
        { key: '15-3' , value: 'O15-3' , label: 'ConsentFormsMaster'        , check: false },
        { key: '15-4' , value: 'O15-4' , label: 'RoomMaster'                , check: false },
        { key: '15-5' , value: 'O15-5' , label: 'Referal_Route'             , check: false },
        { key: '15-6' , value: 'O15-6' , label: 'DoctorList'                , check: false },
        { key: '15-7' , value: 'O15-7' , label: 'Basic_Master'              , check: false },
        { key: '15-8' , value: 'O15-8' , label: 'OtMaster'                  , check: false },
        { key: '15-9' , value: 'O15-9' , label: 'AnaesthesiaMaster'         , check: false },
        { key: '15-10', value: 'O15-10', label: 'UserRegisterList'          , check: false },
        { key: '15-11', value: 'O15-11', label: 'InsClientDonationList'     , check: false },
        { key: '15-12', value: 'O15-12', label: 'ServiceProcedureMasterList', check: false },
        { key: '15-13', value: 'O15-13', label: 'Servicecategory'           , check: false },
        { key: '15-14', value: 'O15-14', label: 'ServiceSubCategory'        , check: false },
        { key: '15-15', value: 'O15-15', label: 'Radiology_Master'          , check: false },
        { key: '15-16', value: 'O15-16', label: 'Lab_Master'                , check: false },
        { key: '15-17', value: 'O15-17', label: 'Surgery_Master'            , check: false },
        { key: '15-18', value: 'O15-18', label: 'FrequencyMaster'           , check: false },
        { key: '15-19', value: 'O15-19', label: 'apprenewal'                , check: false },
        { key: '15-20', value: 'O15-20', label: 'LocationMaster'            , check: false },
        { key: '15-21', value: 'O15-21', label: 'TherapyMaster'             , check: false },
        { key: '15-22', value: 'O15-22', label: 'RatecardMaster'            , check: false },
        { key: '15-23', value: 'O15-23', label: 'ICDCodeMaster'             , check: false },
        { key: '15-24', value: 'O15-24', label: 'NurseStationMaser'         , check: false },
        { key: '15-25', value: 'O15-25', label: 'PackageMaster'             , check: false },

      ]
    },

    {
      key: '16',
      value: 'P',
      label: 'Inventory',
      check: false,
      children: [
        { key: '16-1' , value: 'P16-1' , label: 'InventoryLocation'        , check: false },
        { key: '16-2' , value: 'P16-2' , label: 'Medicine_rack_Master'     , check: false },
        { key: '16-3' , value: 'P16-3' , label: 'TrayManagementList'       , check: false },
        { key: '16-4' , value: 'P16-4' , label: 'Productcategory'          , check: false },
        { key: '16-5' , value: 'P16-5' , label: 'InventorySubMasters'      , check: false },
        { key: '16-6' , value: 'P16-6' , label: 'ProductMasterList'        , check: false },
        { key: '16-7' , value: 'P16-7' , label: 'SupplierMasterList'       , check: false },
        { key: '16-8' , value: 'P16-8' , label: 'PurchaseOrderList'        , check: false },
        { key: '16-9' , value: 'P16-9' , label: 'ItemwisePurchaseOrder'    , check: false },
        { key: '16-10', value: 'P16-10', label: 'GoodsReceiptNoteList'     , check: false },
        { key: '16-11', value: 'P16-11', label: 'QuickGoodsRecieptNote'    , check: false },
        { key: '16-12', value: 'P16-12', label: 'PurchaseReturnList'       , check: false },
        { key: '16-13', value: 'P16-13', label: 'OldGrnQueList'            , check: false },
        { key: '16-14', value: 'P16-14', label: 'IndentRaiseList'          , check: false },
        { key: '16-15', value: 'P16-15', label: 'IndentIssueList'          , check: false },
        { key: '16-16', value: 'P16-16', label: 'IndentRecieveList'        , check: false },
        { key: '16-17', value: 'P16-17', label: 'SerialNoQuelist'          , check: false },
        { key: '16-18', value: 'P16-18', label: 'SerialNoReport'           , check: false },
        { key: '16-19', value: 'P16-19', label: 'ItemMinimumMaximum'       , check: false },
        { key: '16-20', value: 'P16-20', label: 'SupplierPayList'          , check: false },
        { key: '16-21', value: 'P16-21', label: 'SupplierPaidList'         , check: false },
        { key: '16-22', value: 'P16-22', label: 'StockList'                , check: false },
        { key: '16-23', value: 'P16-23', label: 'MedicalStockInsertmaster' , check: false }
 
      ]
    },






   
    {
      key: '17',
      value: 'Q',
      label: 'AssetDashboard',
      check: false,
      children: [
        { key: '17-1' , value: 'Q17-1' , label: 'AssetCategories'            , check: false },
        { key: '17-2' , value: 'Q17-2' , label: 'AssetSubCategoryManagement' , check: false },
        { key: '17-3' , value: 'Q17-3' , label: 'Suppliers'                  , check: false },
        { key: '17-4' , value: 'Q17-4' , label: 'ServiceProviderMangement'   , check: false },
        { key: '17-5' , value: 'Q17-5' , label: 'ChecklistMasterEntry'       , check: false },
        { key: '17-6' , value: 'Q17-6' , label: 'ChecklistManagement'        , check: false },
        { key: '17-7' , value: 'Q17-7' , label: 'AssetManagement'            , check: false },
        { key: '17-8' , value: 'Q17-8' , label: 'AssetDocumentsupload'       , check: false },
        { key: '17-9' , value: 'Q17-9' , label: 'AssetRelationship'          , check: false },
        { key: '17-10', value: 'Q17-10', label: 'AssetAMC'                   , check: false },
      ]
    },
    {
      key: '18',
      value: 'R',
      label: 'Lenin',
      check: false,
      children: [
        { key: '18-1', value: 'R18-1', label: 'LeninMaster'                  , check: false },
        { key: '18-2', value: 'R18-2', label: 'Lenin_DeptWise_MinMax'        , check: false },
        { key: '18-3', value: 'R18-3', label: 'Lenin_Stock'                  , check: false }
      ]
    },

   

    {
      key: '19',
      value: 'S',
      label: 'Finance',
      check: false,
      children: [
        { key: '19-1', value: 'S19-1', label: 'FinanceMasterList'            , check: false },
        { key: '19-2', value: 'S19-2', label: 'VouchersList'                 , check: false },
        { key: '19-3', value: 'S19-3', label: 'DayBook'                      , check: false },
        { key: '19-4', value: 'S19-4', label: 'CashBook'                     , check: false },
        { key: '19-5', value: 'S19-5', label: 'TrialBalance'                 , check: false },
        { key: '19-6', value: 'S19-6', label: 'ProfitandLoss'                , check: false },
        { key: '19-7', value: 'S19-7', label: 'BalanceSheet'                 , check: false },

      ]
    },



    {
      key: '20',
      value: 'T',
      label: 'HR',
      check: false,
      children: [
        { key: '20-1' , value: 'T20-1' , label: 'EmployeeRegistrationList'   , check: false },
        { key: '20-2' , value: 'T20-2' , label: 'DutyRosterMasterList'       , check: false },
        { key: '20-3' , value: 'T20-3' , label: 'ShiftManagement'            , check: false },
        { key: '20-4' , value: 'T20-4' , label: 'LeaveMangement'             , check: false },
        { key: '20-5' , value: 'T20-5' , label: 'AdvanceManagementNavigation', check: false },
        { key: '20-6' , value: 'T20-6' , label: 'Attendance'                 , check: false },
        { key: '20-7' , value: 'T20-7' , label: 'PayRoll'                    , check: false },
        { key: '20-8' , value: 'T20-8' , label: 'EmployeeReport'             , check: false },
        { key: '20-9' , value: 'T20-9' , label: 'JobRequirements'            , check: false },
        { key: '20-10', value: 'T20-10', label: 'EmployeeSourceWiseList'     , check: false },
        { key: '20-11', value: 'T20-11', label: 'Performance'                , check: false },
        { key: '20-12', value: 'T20-12', label: 'ComplaintAction'            , check: false },
        { key: '20-13', value: 'T20-13', label: 'Circular'                   , check: false },
        // { key: '20-14', value: 'T20-14', label: 'HrDashboard', check: false },

      ]
    },

    {
      key: '21',
      value: 'U',
      label: 'EmployeeRequest',
      check: false,
      children: [
        { key: '21-1', value: 'U21-1', label: 'LeaveManagement'              , check: false },
        { key: '21-2', value: 'U21-2', label: 'AdvanceNavigation'            , check: false },
        { key: '21-3', value: 'U21-3', label: 'ShiftManagement'              , check: false },
        { key: '21-4', value: 'U21-4', label: 'PaySlip'                      , check: false },
        { key: '21-5', value: 'U21-5', label: 'Complaint'                    , check: false },


      ]
    },


    {
      key: '22',
      value: 'V',
      label: 'MIS',
      check: false,
      children: [
        { key: '22-1', value: 'V22-1', label: ''                             , check: false },
        { key: '22-2', value: 'V22-2', label: ''                             , check: false },
        { key: '22-3', value: 'V22-3', label: ''                             , check: false },
        { key: '22-4', value: 'V22-4', label: ''                             , check: false },
        { key: '22-5', value: 'V22-5', label: ''                             , check: false },
        { key: '22-6', value: 'V22-6', label: ''                             , check: false },

      ]
    },
    {
      key: '23',
      value: 'W',
      label: 'MRD',
      check: false,
      children: [
        { key: '23-1', value: 'W23-1', label: ''                             , check: false },
        { key: '23-2', value: 'W23-2', label: ''                             , check: false },
        { key: '23-3', value: 'W23-3', label: ''                             , check: false },
        { key: '23-4', value: 'W23-4', label: ''                             , check: false },
        { key: '23-5', value: 'W23-5', label: ''                             , check: false },
        { key: '23-6', value: 'W23-6', label: ''                             , check: false },

      ]
    },
    {
      key: '24',
      value: 'X',
      label: 'CSSDManage',
      check: false,
      children: [
        { key: '24-1', value: 'X24-1', label: 'TrayMaster'                   , check: false },
        { key: '24-1', value: 'X24-1', label: 'TrayCreation'                 , check: false },

      ]
    },
    {
      key: '25',
      value: 'Y',
      label: 'WasteManagement',
      check: false,
      children: [
        { key: '25-1', value: 'Y25-1', label: 'WasteManagement'              , check: false },
        { key: '25-2', value: 'Y25-2', label: 'HandOver'                     , check: false },
        { key: '25-3', value: 'Y25-3', label: ''                             , check: false },
        { key: '25-4', value: 'Y25-4', label: ''                             , check: false },
        { key: '25-5', value: 'Y25-5', label: ''                             , check: false },
        { key: '25-6', value: 'Y25-6', label: ''                             , check: false },

      ]
    },
    {
      key: '26',
      value: 'Z',
      label: 'Marketing',
      check: false,
      children: [
        { key: '26-1', value: 'Z26-1', label: ''                             , check: false },
        { key: '26-2', value: 'Z26-2', label: ''                             , check: false },
        { key: '26-3', value: 'Z26-3', label: ''                             , check: false },
        { key: '26-4', value: 'Z26-4', label: ''                             , check: false },
        { key: '26-5', value: 'Z26-5', label: ''                             , check: false },
        { key: '26-6', value: 'Z26-6', label: ''                             , check: false },
        { key: '26-7', value: 'Z26-7', label: ''                             , check: false },

      ]
    },
    {
      key: '27',
      value: 'AA',
      label: 'QualityIndicators',
      check: false,
      children: [
        { key: '27-1', value: 'AA27-1', label: ''                            , check: false },
        { key: '27-2', value: 'AA27-2', label: ''                            , check: false },
        { key: '27-3', value: 'AA27-3', label: ''                            , check: false },
        { key: '27-4', value: 'AA27-4', label: ''                            , check: false },
        { key: '27-5', value: 'AA27-5', label: ''                            , check: false },
        { key: '27-6', value: 'AA27-6', label: ''                            , check: false },

      ]
    },
    {
      key: '28',
      value: 'AB',
      label: 'Casuality',
      check: false,
      children: [
        { key: '28-1', value: 'AB28-1', label: ''                           , check: false },
        { key: '28-2', value: 'AB28-2', label: ''                           , check: false },
        { key: '28-3', value: 'AB28-3', label: ''                           , check: false },
        { key: '28-4', value: 'AB28-4', label: ''                           , check: false },
        { key: '28-5', value: 'AB28-5', label: ''                           , check: false },

      ]
    },
    {
      key: '29',
      value: 'AC',
      label: 'BloodBank',
      check: false,
      children: [
        { key: '29-1', value: 'Ac29-1', label: ''                           , check: false },
        { key: '29-2', value: 'Ac29-2', label: ''                           , check: false },
        { key: '29-3', value: 'Ac29-3', label: ''                           , check: false },
        { key: '29-4', value: 'Ac29-4', label: ''                           , check: false },
        { key: '29-5', value: 'Ac29-5', label: ''                           , check: false },

      ]
    },
    {
      key: '30',
      value: 'AD',
      label: 'CRMdashboard',
      check: false,
      children: [
        { key: '30-1', value: 'AD30-1', label: 'Opfollowup'                 , check: false },
        { key: '30-2', value: 'AD30-2', label: 'IPfollowup'                 , check: false },
        { key: '30-3', value: 'AD30-3', label: 'Discharge'                  , check: false },
        { key: '30-4', value: 'AD30-4', label: 'Therapy'                    , check: false },
        { key: '30-5', value: 'AD30-5', label: 'Labque'                     , check: false },
        { key: '30-6', value: 'AD30-6', label: 'Radiologyque'               , check: false },

      ]
    },
    
  ]);
  const [Locations, setLocations] = useState([])
  const [LocationData, setLocationData] = useState([])
  const [ParentData, setParentData] = useState([])
  const [ChildData, setChildData] = useState([]);


  useEffect(() => {
    axios.get(`${UrlLink}Masters/Location_Detials_link`)
      .then((res) => {
        const ress = res.data
        console.log(ress);
        setLocations(ress)
      })
      .catch((err) => {
        console.log(err);
      })
  }, [UrlLink])


  useEffect(() => {
    if (UserListId && UserListId.UserId) {
      axios.get(`${UrlLink}Masters/Get_User_Detialsby_id?UserId=${UserListId.UserId}`)
        .then((res) => {
          const resss = res.data;
          console.log(resss, 'ressssssssssssssss');

          setUserRegister({
            UserId: resss?.id || '',
            EmployeeType: resss?.EmployeeType || '',
            DoctorId: resss?.DoctorId || '',
            EmployeeId: resss?.EmployeeId || '',
            Title: resss?.Title || '',
            firstName: resss?.firstName || '',
            middleName: resss?.middleName || '',
            lastName: resss?.lastName || '',
            Email: resss?.Email || '',
            PhoneNo: resss?.PhoneNo || '',
            Gender: resss?.Gender || '',
            Qualification: resss?.Qualification || '',
            UserName: resss.UserName || '',
            roleName: resss?.roleName || '',
          });
          const ParentData = resss?.Access?.split(',') || [];
          const ChildData = resss?.SubAccess?.split(',') || [];



          const locData = resss?.Locations || [];
          if (locData.length === 1 && locData[0].Location_Name === 'All') {
            setLocationData([...Locations])
          } else {
            const locationNames = locData.map(loc => loc.Location_Name);
            setLocationData([...locationNames]);
          }


          setCheckedItems((prev) => {
            return prev.map((item) => {
              if (item.children && item.children.length > 0) {
                const updatedChildren = item.children.map((child) => {
                  if (ChildData.includes(child.value)) {
                    return { ...child, check: true };
                  }
                  return child;
                });

                const someval = updatedChildren.some((child) => child.check) || ParentData.includes(item.value);
                console.log(item, '---', someval);
                return { ...item, check: someval, children: updatedChildren };
              } else {
                if (ParentData.includes(item.value)) {
                  return { ...item, check: true };
                }
              }
              return item;
            });
          });
          setChildData(ChildData);
          setParentData(ParentData);
        })
        .catch((err) => {
          console.log(err);
        });
    } else if (Usercreatedocdata && Usercreatedocdata?.DoctorId) {
      axios.get(`${UrlLink}Masters/get_User_Doctor_Detials?DoctorId=${Usercreatedocdata.DoctorId}`)
        .then(res => {
          const resData = res.data;
          console.log(resData, 'resDataDocccccccccc');
          console.log(Usercreatedocdata, 'Usercreatedocdata');

          setUserRegister((prev) => ({
            ...prev,
            DoctorId: resData?.id,
            EmployeeId: '',
            EmployeeType: Usercreatedocdata?.Type,
            Title: resData?.Title,
            firstName: resData?.firstName,
            middleName: resData?.middleName,
            lastName: resData?.lastName,
            Email: resData?.Email,
            PhoneNo: resData?.PhoneNo,
            Gender: resData?.Gender,
            Qualification: resData?.Qualification,

          }))
        })
        .catch(err => {
          console.log(err);
        })


    } else if (UsercreateEmpdata && UsercreateEmpdata?.EmployeeId) {
      axios.get(`${UrlLink}HR_Management/get_User_Employee_Details?EmployeeId=${UsercreateEmpdata.EmployeeId}`)
        .then(res => {
          const resData = res.data;
          console.log(resData, 'resData');
          console.log(UsercreateEmpdata, 'UsercreateEmpdata');

          setUserRegister((prev) => ({
            ...prev,
            EmployeeId: resData?.Employee_Id,
            DoctorId: '',
            EmployeeType: UsercreateEmpdata?.Type,
            Title: resData?.Title,
            firstName: resData?.FirstName,
            middleName: resData?.MiddleName,
            lastName: resData?.lastName,
            Email: resData?.Email,
            PhoneNo: resData?.Phone,
            Gender: resData?.Gender,
            Qualification: resData?.Qualification,

          }))
        })
        .catch(err => {
          console.log(err);
        })
    }
    else {
      navigate('/Home/UserRegisterList');
    }
  }, [UserListId, UrlLink, navigate, Locations, Usercreatedocdata, UsercreateEmpdata]);




  const handlelocationChange = (lname) => {

    setLocationData((prev) => {
      if (!prev.includes(lname)) {
        return [...prev, lname];
      } else {
        return [...prev.filter((value) => value !== lname)]
      }

    });

  }


  const handleParentChange = (index) => {
    setCheckedItems((prev) => {
      const updated = [...prev];
      updated[index].check = !updated[index].check;
      if (updated[index].children.length > 0) {
        updated[index].children.forEach((child) => {
          if (updated[index].check) {
            child.check = true;
            setChildData((prev) => [...prev, child.value]);
          } else {
            child.check = false;
            setChildData((prev) => prev.filter((value) => value !== child.value));
          }
        });
      }
      if (updated[index].check) {
        setParentData((prev) => [...prev, updated[index].value]);
      } else {
        setParentData((prev) => prev.filter((value) => value !== updated[index].value));
      }
      return updated;
    });
  };

  const handleChildChange = (parentIndex, childIndex) => {
    setCheckedItems((prev) => {
      const updated = [...prev];
      updated[parentIndex].children[childIndex].check = !updated[parentIndex].children[childIndex].check;
      if (updated[parentIndex].children[childIndex].check) {
        setChildData((prev) => [...prev, updated[parentIndex].children[childIndex].value]);
      } else {
        setChildData((prev) => prev.filter((value) => value !== updated[parentIndex].children[childIndex].value));
      }
      if (updated[parentIndex].children.some((child) => child.check)) {
        updated[parentIndex].check = true;
        setParentData((prev) => {
          if (!prev.includes(updated[parentIndex].value)) {
            return [...prev, updated[parentIndex].value];
          }
          return prev;
        });
      } else {
        updated[parentIndex].check = false;
        setParentData((prev) => prev.filter((value) => value !== updated[parentIndex].value));
      }
      return updated;
    });
  };


  const formatLabel = (label) => {
    if (/[a-z]/.test(label) && /[A-Z]/.test(label) && !/\d/.test(label)) {
      return label
        .replace(/([a-z])([A-Z])/g, "$1 $2")
        .replace(/^./, (str) => str.toUpperCase());
    } else {
      return label;
    }
  };

  const handleUserRegistersubmit = () => {

    if (Object.keys(UserRegister).filter(p => UserRegister.EmployeeType === 'DOCTOR' ? !['UserId', 'EmployeeId'].includes(p) : !['UserId', 'DoctorId'].includes(p)).filter(value => !UserRegister[value]).length !== 0 || (ChildData.length === 0 || ParentData.length === 0) || LocationData.length === 0) {
      dispatch({ type: 'toast', value: { message: 'Please provide all required fields.', type: 'warn' } });

      console.log('gggggg', Object.keys(UserRegister).filter(p => p !== 'UserId').filter(p => UserRegister.EmployeeType === 'DOCTOR' ? !['UserId', 'EmployeeId'].includes(p) : !['UserId', 'DoctorId'].includes(p)).filter(value => !UserRegister[value]));

    } else {
      let locadata = LocationData.join(',')

      const data = {
        ...UserRegister,
        created_by: userRecord?.username || '',
        ChildData: ChildData.join(','),
        ParentData: ParentData.join(','),
        Location: locadata,

      };
      axios.post(`${UrlLink}Masters/UserRegister_Detials_link`, data)
        .then((res) => {
          const resData = res.data;
          const mess = Object.values(resData)[0];
          const typp = Object.keys(resData)[0];
          const tdata = { message: mess, type: typp };
          dispatch({ type: 'toast', value: tdata });
          setUserRegister({
            UserId: '', EmployeeType: '', DoctorId: '',
            EmployeeId: '', UserName: '', firstName: '', middleName: '', lastName: '', Title: '', Email: '',
            Password: '', confirmPassword: '', roleName: '', PhoneNo: '', Gender: '',
            Qualification: ''
          });
          navigate('/Home/UserRegisterList')
        })
        .catch((err) => {
          console.log(err);
        });
    }
  };



  useEffect(() => {
    let data = Object.keys(UserRegister).filter(p => !['UserId', 'DoctorId', 'EmployeeId'].includes(p))

    if (UserRegister.EmployeeType === 'DOCTOR') {
      const categoryIndex = data.indexOf('EmployeeType');
      data.splice(categoryIndex + 1, 0, 'DoctorId');
    }
    if (UserRegister.EmployeeType === 'EMPLOYEE') {
      const categoryIndex = data.indexOf('EmployeeType');
      data.splice(categoryIndex + 1, 0, 'EmployeeId');
    }
    setUserRegistershow(data)
  }, [UserRegister])



  return (
    <>
      <div className="Main_container_app">
        <h3>User Register</h3>
        <div className="common_center_tag">
          <span>User Register</span>
        </div>
        <div className="RegisFormcon_1">
          {UserRegistershow.map((field, index) => (
            <div className="RegisForm_1" key={index}>
              <label htmlFor={`${field}_${index}_${field}`}>
                {formatLabel(field)}
                <span>:</span>
              </label>
              {field === 'roleName' ? (
                <select
                  name={field}
                  id={`${field}_${index}_${field}`}
                  value={UserRegister[field] || ''}
                  onChange={handleInputChange}
                >
                  <option value="">select</option>
                  {RoleNameData.filter(p => p.Status === 'Active').map((p, indx) => (
                    <option value={p.Role} key={indx}>{p.Role}</option>
                  ))}
                </select>
              ) : (
                <input
                  // readOnly
                  id={`${field}_${index}_${field}`}
                  autoComplete='off'
                  readOnly={!['UserName', 'Password'].includes(field)}
                  pattern={
                    field === 'Email' ? "[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,}$" :
                      field === 'PhoneNo' ? "\\d{10}" :
                        field === 'Password' ? "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$" :
                          null
                  }
                  type={
                    field === 'Email' ? 'Email' :
                      field === 'PhoneNo' ? 'tel' :
                        // field === 'Password' ? 'password' :
                        'text'
                  }
                  title={
                    field === 'Email' ? "Format: example@example.com" :
                      field === 'PhoneNo' ? "Format: 10 digits only" :
                        field === 'Password' ? "Must contain 8 characters, one uppercase, one lowercase, one number and one special character" :
                          ''
                  }
                  name={field}
                  value={UserRegister[field] || ''}
                  onChange={handleInputChange}
                />
              )}
            </div>
          ))}
        </div>
        <div className="DivCenter_container">
          <h2>Location Access</h2>
        </div>
        <div className="displayuseraccess">
          {
            Locations.map((p, indx) => (
              <div className="displayuseraccess_child">
                <input
                  type="checkbox"
                  id={`${indx}_${p?.locationName}`}
                  checked={LocationData.includes(p?.locationName)}
                  onChange={() => handlelocationChange(p?.locationName)}
                />
                <label htmlFor={`${indx}_${p?.locationName}`} className='par_acc_lab'>{p?.locationName}</label>
              </div>
            ))
          }
        </div>
       
        <div>
          <h2 style={{ textAlign: "center", margin: "10px 0", color: "gray", 
            fontSize: "clamp(12px, 1.5vw, 24px)", }}>Access</h2>
          <div className="DivCenter_container">
            <div className="displayuseraccess">
              {checkedItems.map((item, indx) => (
                <div key={indx} className="displayuseraccess_child" style={{ marginBottom: "5px", }} >
                  <div style={{ display: "flex", alignItems: "center", marginBottom: "5px", }} >
                    <input
                      type="checkbox"
                      id={item.key}
                      checked={item.check}
                      onChange={() => handleParentChange(indx)}
                    />
                    <label
                      htmlFor={item.key}
                      className="par_acc_lab"
                      style={{ marginLeft: "10px" }}
                    >
                      {item.label}
                    </label>
                  </div>

                  {item.check && (
                    <div style={{ display: "flex", flexWrap: "wrap", }} >
                      {item.children.map((child, ind1) => (
                        <div key={ind1} style={{ display: "flex", flex: "calc(33.33% - 25px)", }} >
                          <input
                            type="checkbox"
                            id={child.key}
                            checked={child.check}
                            onChange={() => handleChildChange(indx, ind1)}
                          />
                          <label
                            htmlFor={child.key}
                            className="chi_acc_lab"
                            style={{ marginLeft: "10px" }}
                          >
                            {child.label}
                          </label>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="Main_container_Btn">
          <button onClick={handleUserRegistersubmit}>{UserRegister?.UserId ? 'Update' : 'Submit'}</button>
        </div>
      </div>
      <ToastAlert Message={toast.message} Type={toast.type} />
    </>
  );
};

export default UserRegisterMaster;






















