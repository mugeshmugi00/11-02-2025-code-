const initstate = {
    Registeredit: {},
    RegisterRoomShow: { type: '', val: false },
    SelectRoomRegister: {},
    RegistereditIP: {},
    RegistereditCasuality: {},
    RegistereditDiagnosis: {},
    RegistereditLaboratory: {},
    SpecialityWise_DoctorWorkbenchNavigation: {},
    DoctorWorkbenchNavigation: {},
    IP_DoctorWorkbenchNavigation: {},
    Casuality_DoctorWorkbenchNavigation: {},
    LabWorkbenchNavigation: {},
    OPBillingData: {},
    IPBillingData: {},
    RadiologyWorkbenchNavigation: {},
    PatientListId: {},
    EmployeeListId: {},
    TraineeEditData:{},
    EmployeePaySlipData: {},
    TestMasterEditData: {},
    LabEditData: {},
    ReferDoctorEditData: {},
    GroupMasterEditData: {},
    TestMasterEditData: {},
    LabEditData: {},
    ReferDoctorEditData: {},
    GroupMasterEditData: {},
    ResultEntryNavigationdata: {},
    SampleCollectionqueueData: {},
    PrintBarcode: {},
    PatientDetails:{},
    AllergyDetails:[],
    
};

const Frontoffice = (state = initstate, action) => {
    switch (action.type) {
        case 'Registeredit':
            return { ...state, Registeredit: action.value }
        case 'PatientDetails':
            return { ...state, PatientDetails: action.value }
        case 'AllergyDetails':
            return { ...state, AllergyDetails: action.value }
        case 'RegisterRoomShow':
            return { ...state, RegisterRoomShow: action.value }
        case 'SelectRoomRegister':
            return { ...state, SelectRoomRegister: action.value }
        case 'RegistereditIP':
            return { ...state, RegistereditIP: action.value }
        case 'RegistereditCasuality':
            return { ...state, RegistereditCasuality: action.value }
        case 'RegistereditDiagnosis':
            return { ...state, RegistereditDiagnosis: action.value }
        case 'RegistereditLaboratory':
            return { ...state, RegistereditLaboratory: action.value }


        case 'DoctorWorkbenchNavigation':
            return { ...state, DoctorWorkbenchNavigation: action.value }

        case 'SpecialityWise_DoctorWorkbenchNavigation':
            return { ...state, SpecialityWise_DoctorWorkbenchNavigation: action.value }

        case 'IP_DoctorWorkbenchNavigation':
            return { ...state, IP_DoctorWorkbenchNavigation: action.value }
        case 'Casuality_DoctorWorkbenchNavigation':
            return { ...state, Casuality_DoctorWorkbenchNavigation: action.value }

        case 'LabWorkbenchNavigation':
            return { ...state, LabWorkbenchNavigation: action.value }
        case 'RadiologyWorkbenchNavigation':
            return { ...state, RadiologyWorkbenchNavigation: action.value }
        case 'OPBillingData':
            return { ...state, OPBillingData: action.value }
        case 'IPBillingData':
            return { ...state, IPBillingData: action.value }

        case 'PatientListId':
            return { ...state, PatientListId: action.value }

        case 'TraineeEditData':
            return { ...state, TraineeEditData: action.value }

        case 'EmployeeListId':
            return { ...state, EmployeeListId: action.value }
        case "ResultEntryNavigationdata":
            return { ...state, ResultEntryNavigationdata: action.value };
        case "SampleCollectionqueueData":
            return { ...state, SampleCollectionqueueData: action.value };
        case "PrintBarcode":
            return { ...state, PrintBarcode: action.value };

        case "EmployeePaySlipData":
            return { ...state, EmployeePaySlipData: action.value };
        case "TestMasterEditData":
            return { ...state, TestMasterEditData: action.value };
        case "LabEditData":
            return { ...state, LabEditData: action.value };
        case "ReferDoctorEditData":
            return { ...state, ReferDoctorEditData: action.value };

        case "GroupMasterEditData":
            return { ...state, GroupMasterEditData: action.value };
        

        default:
            return state;
    }
}

export default Frontoffice;











