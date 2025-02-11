import axios from "axios";
import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import Button from "@mui/material/Button";
import EditIcon from "@mui/icons-material/Edit";
// import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import ReactGrid from "../../OtherComponent/ReactGrid/ReactGrid";
import ToastAlert from "../../OtherComponent/ToastContainer/ToastAlert";
import { useNavigate } from "react-router-dom";
import LoupeIcon from "@mui/icons-material/Loupe";
import AddCircleIcon from '@mui/icons-material/AddCircle';
import { Tooltip } from 'react-tooltip';

const RegistrationList = () => {
  const UrlLink = useSelector((state) => state.userRecord?.UrlLink);
  // const userRecord = useSelector((state) => state.userRecord?.UserData);
  const toast = useSelector((state) => state.userRecord?.toast);
  const pagewidth = useSelector((state) => state.userRecord?.pagewidth);
  const dispatchvalue = useDispatch();
  const navigate = useNavigate();
  const [PatientRegisterData, setPatientRegisterData] = useState([]);
  const [PatientIPRegisterData, setPatientIPRegisterData] = useState([]);
  const [PatientCasualityRegisterData, setPatientCasualityRegisterData] = useState([]);
  const [PatientEmergencyRegisterData, setPatientEmergencyRegisterData] = useState([]);
  const [PatientDiagnosisRegisterData, setPatientDiagnosisRegisterData] =useState([]);
  const [PatientLaboratoryRegisterData, setPatientLaboratoryRegisterData] =useState([]);
  const UserData = useSelector(state => state.userRecord?.UserData)


  const [dateOption, setDateOption] = useState('current');
  const [fromDate, setFromDate] = useState('');
  const [toDate, setToDate] = useState('');
  const [ParticularDate, setParticularDate] = useState('');
  const [CurrentDate, setCurrentDate] = useState(new Date().toISOString().split('T')[0]);

  useEffect(() => {
      if (dateOption === 'current') {
          setCurrentDate(new Date().toISOString().split('T')[0]); // Auto-set today
      }
  }, [dateOption]);
  console.log(PatientRegisterData,'PatientRegisterData');
  console.log(PatientEmergencyRegisterData,'PatientEmergencyRegisterData');
  
  
  const [searchOPParams, setsearchOPParams] = useState({ query: '', status: 'Registered', DoctorId: UserData?.Doctor });
  
  const [searchIPParams, setsearchIPParams] = useState({
      query: '',
      status: 'Admitted',
      type: 'IP',
      DoctorId: UserData?.Doctor,
      // SelectedWard : SelectedWard
  });

  const [searchCasualityParams, setsearchCasualityParams] = useState({
    query: "",
    status: 'Admitted',
    DoctorId: UserData?.Doctor,
  });

  const [searchEmergencyParams, setsearchEmergencyParams] = useState({
    query: "",
    status: 'Admitted',
    DoctorId: UserData?.Doctor,
  });
  const [searchDiagnosisParams, setsearchDiagnosisParams] = useState({
    query: "",
    status: "",
  });
  const [searchLaboratoryParams, setsearchLaboratoryParams] = useState({
    query: "",
    status: "",
  });


  useEffect(() => {
    const params = {};
    
    if (searchOPParams.query.trim()) {
        params.query = searchOPParams.query;  // ✅ Use searchOPParams.query
    } else {
        params.limit = 10; // Default limit if no search query
    }

    if (searchOPParams.status) {
        params.status = searchOPParams.status;
    }

    if (searchOPParams.DoctorId) {
        params.DoctorId = searchOPParams.DoctorId;
    }

    if (dateOption === 'custom') {
        if (fromDate && toDate) {
            params.fromDate = fromDate;
            params.toDate = toDate;
        } else {
          setPatientRegisterData([]); // Clear the data if both dates are not provided
            return;
        }
    } else if (dateOption === 'current') {
        params.CurrentDate = CurrentDate;
        
        
        
    } else if (dateOption === 'particular') {
        if (ParticularDate) {
            params.ParticularDate = ParticularDate;
            
        } else {
          setPatientRegisterData([]); // Clear data if no particular date is selected
            return;
        }
    }
    

    axios
      .get(`${UrlLink}Frontoffice/get_patient_appointment_details_withoutcancelled`, {params})
      .then((res) => {
        const ress = res.data;
        if (Array.isArray(ress)) {
          setPatientRegisterData(ress);
        } else {
          setPatientRegisterData([]);
        }
      })
      .catch((err) => {
        console.log(err);
      });
  }, [UrlLink, searchOPParams,UserData,dateOption, fromDate, toDate, ParticularDate,CurrentDate]);



  useEffect(() => {
    axios
      .get(`${UrlLink}Frontoffice/get_ip_Patient_registration_details_for_workbench`, {
        params: searchIPParams,
      })
      .then((res) => {
        console.log("API Response:", res.data);
        const ress = res.data;
        if (Array.isArray(ress)) {
          setPatientIPRegisterData(ress);
          console.log(ress);
        } else {
          setPatientIPRegisterData([]);
        }
      })
      .catch((err) => {
        console.log(err);
      });
  }, [UrlLink, searchIPParams]);

  useEffect(() => {
    axios
      .get(`${UrlLink}Frontoffice/get_patient_casuality_details`, {
        params: searchCasualityParams,
      })
      .then((res) => {
        console.log("Casualityyyy", res.data);
        const ress = res.data;
        if (Array.isArray(ress)) {
          setPatientCasualityRegisterData(ress);
          console.log(ress);
        } else {
          setPatientCasualityRegisterData([]);
        }
      })
      .catch((err) => {
        console.log(err);
      });
  }, [UrlLink, searchCasualityParams]);
  
  useEffect(() => {
    axios
      .get(`${UrlLink}Frontoffice/get_Emergency_patient_details_for_Quelist`, {
        params: searchEmergencyParams,
      })
      .then((res) => {
        console.log("Emergencyyyyyyy", res.data);
        const ress = res.data;
        console.log("Emergencyyyyyyy", ress);

        if (Array.isArray(ress)) {
          setPatientEmergencyRegisterData(ress);
          console.log(ress);
        } else {
          setPatientEmergencyRegisterData([]);
        }
      })
      .catch((err) => {
        console.log(err);
      });
  }, [UrlLink, searchEmergencyParams]);

  useEffect(() => {
    axios
      .get(`${UrlLink}Frontoffice/get_patient_diagnosis_details`, {
        params: searchDiagnosisParams,
      })
      .then((res) => {
        console.log("API Response:", res.data);
        const ress = res.data;
        if (Array.isArray(ress)) {
          setPatientDiagnosisRegisterData(ress);
          console.log(ress);
        } else {
          setPatientDiagnosisRegisterData([]);
        }
      })
      .catch((err) => {
        console.log(err);
      });
  }, [UrlLink, searchDiagnosisParams]);

  useEffect(() => {
    axios
      .get(`${UrlLink}Frontoffice/get_patient_laboratory_details`, {
        params: searchLaboratoryParams,
      })
      .then((res) => {
        console.log("API Response:", res.data);
        const ress = res.data;
        if (Array.isArray(ress)) {
          setPatientLaboratoryRegisterData(ress);
          console.log(ress);
        } else {
          setPatientLaboratoryRegisterData([]);
        }
      })
      .catch((err) => {
        console.log(err);
      });
  }, [UrlLink, searchLaboratoryParams]);

  const PatientOPRegisterColumns = [
    {
      key: "id",
      name: "ID",
      frozen: pagewidth > 500 ? true : false,
    },
    {
      key: "PatientId",
      name: "Patient Id",
      frozen: pagewidth > 500 ? true : false,
    },
    {
      key: "PatientName",
      name: "Patient Name",
      width: 150,
      frozen: pagewidth > 500 ? true : false,
    },
    {
      key: "PhoneNo",
      name: "PhoneNo",
      frozen: pagewidth > 500 ? true : false,
    },
    {
      key: "AppointmentId",
      name: "Appointment Id",
    },
    {
      key: "VisitId",
      name: "Visit Id",
    },
    {
      key: "Complaint",
      name: "Complaint",
    },
    {
      key: "isMLC",
      name: "isMLC",
      frozen: pagewidth > 500 ? true : false,
    },
    {
      key: "Flagging",
      name: "Flagging",
    },
    {
      key: "isRefferal",
      name: "isRefferal",
    },
    {
      key: "Status",
      name: "Status",
    },
    {
      key: "Specilization",
      name: "Specilization",
    },
    {
      key: "DoctorName",
      name: "Doctor Name",
    },
    {
      key: "Action",
      name: "Action",
      renderCell: (params) => (
        <>
          <Button
            className="cell_btn"
            onClick={() => handleeditOPPatientRegister(params.row)}
          >
            <EditIcon className="check_box_clrr_cancell" />
          </Button>
        </>
      ),
    },
  ];

  const PatientIPRegisterColumns = [
    {
      key: "id",
      name: "ID",
      frozen: pagewidth > 500 ? true : false,
    },
    {
      key: "PatientId",
      name: "Patient Id",
      frozen: pagewidth > 500 ? true : false,
    },
    {
      key: "PatientName",
      name: "Patient Name",
      width: 150,
      frozen: pagewidth > 500 ? true : false,
    },
    {
      key: "PhoneNo",
      name: "PhoneNo",
      frozen: pagewidth > 500 ? true : false,
    },
    // {
    //   key: "AppointmentId",
    //   name: "Appointment Id",
    // },
    {
      key: "Complaint",
      name: "Complaint",
    },
    {
      key: "isMLC",
      name: "isMLC",
      frozen: pagewidth > 500 ? true : false,
    },
    {
      key: "Flagging",
      name: "Flagging",
    },
    {
      key: "isRefferal",
      name: "isRefferal",
    },
    {
      key: "Status",
      name: "Status",
    },
    {
      key: "Specilization",
      name: "Specilization",
    },
    {
      key: "DoctorName",
      name: "Doctor Name",
    },
    {
      key: "Action",
      name: "Action",
      renderCell: (params) => (
        <>
          <Button
            className="cell_btn"
            onClick={() => handleeditIPPatientRegister(params.row)}
          >
            <EditIcon className="check_box_clrr_cancell" />
          </Button>
        </>
      ),
    },
  ];

  const PatientCasualityRegisterColumns = [
    {
      key: "id",
      name: "ID",
      frozen: pagewidth > 500 ? true : false,
    },
    {
      key: "PatientId",
      name: "Patient Id",
      frozen: pagewidth > 500 ? true : false,
    },
    {
      key: "PatientName",
      name: "Patient Name",
      width: 150,
      frozen: pagewidth > 500 ? true : false,
    },
    {
      key: "PhoneNo",
      name: "PhoneNo",
      frozen: pagewidth > 500 ? true : false,
    },
    {
      key: "VisitId",
      name: "Visit Id",
    },
    {
      key: "Complaint",
      name: "Complaint",
    },
    {
      key: "isMLC",
      name: "isMLC",
      frozen: pagewidth > 500 ? true : false,
    },
    {
      key: "Flagging",
      name: "Flagging",
    },
    {
      key: "isRefferal",
      name: "isRefferal",
    },
    {
      key: "Status",
      name: "Status",
    },
    {
      key: "Specilization",
      name: "Specilization",
    },
    {
      key: "DoctorName",
      name: "Doctor Name",
    },
    {
      key: "Action",
      name: "Action",
      renderCell: (params) => (
        <>
          <Button
            className="cell_btn"
            onClick={() => handleeditCasualityPatientRegister(params.row)}
          >
            <EditIcon className="check_box_clrr_cancell" />
          </Button>
        </>
      ),
    },
  ];


  const PatientEmergencyRegisterColumns = [
    {
      key: "id",
      name: "ID",
      frozen: pagewidth > 500 ? true : false,
    },
    {
      key: "PatientId",
      name: "Patient Id",
      frozen: pagewidth > 500 ? true : false,
    },
    {
      key: "PatientName",
      name: "Patient Name",
      width: 150,
      frozen: pagewidth > 500 ? true : false,
    },
    {
      key: "PhoneNo",
      name: "PhoneNo",
      frozen: pagewidth > 500 ? true : false,
    },
    {
      key: "VisitId",
      name: "Visit Id",
    },
    {
      key: "Complaint",
      name: "Complaint",
    },
    {
      key: "isMLC",
      name: "isMLC",
      frozen: pagewidth > 500 ? true : false,
    },
    {
      key: "Flagging",
      name: "Flagging",
    },
    {
      key: "isRefferal",
      name: "isRefferal",
    },
    {
      key: "Status",
      name: "Status",
    },
    {
      key: "Specilization",
      name: "Specilization",
    },
    {
      key: "DoctorName",
      name: "Doctor Name",
    },
    {
      key: "Action",
      name: "Action",
      renderCell: (params) => (
        <>
          <Button
            className="cell_btn"
            onClick={() => handleeditEmergencyPatientRegister(params.row)}
          >
            <EditIcon className="check_box_clrr_cancell" />
          </Button>
        </>
      ),
    },
  ];

  const PatientDiagnosisRegisterColumns = [
    {
      key: "id",
      name: "ID",
      frozen: pagewidth > 500 ? true : false,
    },
    {
      key: "PatientId",
      name: "Patient Id",
      frozen: pagewidth > 500 ? true : false,
    },
    {
      key: "PatientName",
      name: "Patient Name",
      width: 150,
      frozen: pagewidth > 500 ? true : false,
    },
    {
      key: "PhoneNo",
      name: "PhoneNo",
      frozen: pagewidth > 500 ? true : false,
    },
    {
      key: "VisitId",
      name: "Visit Id",
    },
    {
      key: "Complaint",
      name: "Complaint",
    },
    {
      key: "isMLC",
      name: "isMLC",
      frozen: pagewidth > 500 ? true : false,
    },
    {
      key: "Flagging",
      name: "Flagging",
    },
    {
      key: "isRefferal",
      name: "isRefferal",
    },
    {
      key: "Status",
      name: "Status",
    },
    {
      key: "Action",
      name: "Action",
      renderCell: (params) => (
        <>
          <Button
            className="cell_btn"
            onClick={() => handleeditDiagnosisPatientRegister(params.row)}
          >
            <EditIcon className="check_box_clrr_cancell" />
          </Button>
        </>
      ),
    },
  ];

  const PatientLaboratoryRegisterColumns = [
    {
      key: "id",
      name: "ID",
      frozen: pagewidth > 500 ? true : false,
    },
    {
      key: "PatientId",
      name: "Patient Id",
      frozen: pagewidth > 500 ? true : false,
    },
    {
      key: "PatientName",
      name: "Patient Name",
      width: 150,
      frozen: pagewidth > 500 ? true : false,
    },
    {
      key: "PhoneNo",
      name: "PhoneNo",
      frozen: pagewidth > 500 ? true : false,
    },
    {
      key: "Complaint",
      name: "Complaint",
    },
    {
      key: "isMLC",
      name: "isMLC",
      frozen: pagewidth > 500 ? true : false,
    },
    {
      key: "Flagging",
      name: "Flagging",
    },
    {
      key: "isRefferal",
      name: "isRefferal",
    },
    {
      key: "Status",
      name: "Status",
    },
    {
      key: "Action",
      name: "Action",
      renderCell: (params) => (
        <>
          <Button
            className="cell_btn"
            onClick={() => handleeditLaboratoryPatientRegister(params.row)}
          >
            <EditIcon className="check_box_clrr_cancell" />
          </Button>
        </>
      ),
    },
  ];

  const handleDateOptionChange = (e) => {
        setDateOption(e.target.value);
    
        // Reset date states when changing the selection
        if (e.target.value === 'current') {
            setFromDate('');
            setToDate('');
            setParticularDate('');
        } else if (e.target.value === 'custom') {
            setParticularDate('');
            setCurrentDate('');
        } else if (e.target.value === 'particular') {
            setFromDate('');
            setToDate('');
            setCurrentDate('');
        }
    };
    
    const handleCurrentDateChange = (e) => {
        setCurrentDate(e.target.value);
    };


    const handleFromDateChange = (e) => {
        setFromDate(e.target.value);
    };
    
    const handleToDateChange = (e) => {
        setToDate(e.target.value);
    };
    
    const handleParticularDateChange = (e) => {
        setParticularDate(e.target.value);
    };
    

  const handlenewPatientRegister = () => {
    dispatchvalue({ type: "Registeredit", value: {} });
    dispatchvalue({ type: "HrFolder", value:"OPVisitEntry"});
    navigate("/Home/FrontOfficeFolder");
    dispatchvalue({ type: "setPreviousFolder", value: null });
    dispatchvalue({ type: "showMenu", value: true });
  };
  const handlenewIPPatientRegister = () => {
    dispatchvalue({ type: "Registeredit", value: {} });
    dispatchvalue({ type: "HrFolder", value:"IPRegistration"});
    navigate("/Home/FrontOfficeFolder");
    dispatchvalue({ type: "setPreviousFolder", value: null });
    dispatchvalue({ type: "showMenu", value: true });
  };

  const handleNewEmergencyPatientRegister = () => {
    dispatchvalue({ type: "Registeredit", value: {} });
    dispatchvalue({ type: "HrFolder", value:"PatientRegistration"});
    navigate("/Home/FrontOfficeFolder");
    dispatchvalue({ type: "setPreviousFolder", value: null });
    dispatchvalue({ type: "showMenu", value: true });
  };


  const handleeditOPPatientRegister = (params) => {
    // Destructure the id and PatientId from the params object
    const { PatientId, VisitId, ...rest } = params;

    // Log the entire params object for debugging purposes
    console.log("paraaaammmmmsss", params);

    // Dispatch an action to update the Redux store with the selected PatientId
    dispatchvalue({
      type: "Registeredit",
      value: {...params,Department:'OP'},
      // value: { PatientId: PatientId, VisitId: VisitId, Type: "OP", ...rest },
    });

    dispatchvalue({ type: "HrFolder", value:"OPVisitEntry"});
    navigate("/Home/FrontOfficeFolder");
    dispatchvalue({ type: "setPreviousFolder", value: null });
    dispatchvalue({ type: "showMenu", value: true });

    // Navigate to the registration page for editing the patient's details
    // navigate("/Home/Registration");
  };

  
  const handleeditIPPatientRegister = (params) => {
    // Destructure the id and PatientId from the params object
    const { PatientId, ...rest } = params;

    // Log the entire params object for debugging purposes
    console.log("Ipppppppppp", params);

    // Dispatch an action to update the Redux store with the selected PatientId
    dispatchvalue({
      type: "Registeredit",
      value: {...params,Department:'IP'},
      // value: { PatientId: PatientId, Type: "IP", ...rest },
    });

    dispatchvalue({ type: "HrFolder", value:"IPRegistration"});
    navigate("/Home/FrontOfficeFolder");
    dispatchvalue({ type: "setPreviousFolder", value: null });
    dispatchvalue({ type: "showMenu", value: true });

    
  };


  const handleeditEmergencyPatientRegister = (params) => {
    // Destructure the id and PatientId from the params object
    const { PatientId, ...rest } = params;

    // Log the entire params object for debugging purposes
    console.log("Emergenccccccccy", params);

    // Dispatch an action to update the Redux store with the selected PatientId
    dispatchvalue({
      type: "Registeredit",
      value: params,
      // value: { PatientId: PatientId, Type: "IP", ...rest },
    });

    dispatchvalue({ type: "HrFolder", value:"EmergencyPatientRoomRegistration"});
    navigate("/Home/FrontOfficeFolder");
    dispatchvalue({ type: "setPreviousFolder", value: null });
    dispatchvalue({ type: "showMenu", value: true });

    
  };

  const handleeditCasualityPatientRegister = (params) => {
    const { PatientId, ...rest } = params;

    console.log("Casualityyyyyyy", params);

    dispatchvalue({
      type: "Registeredit",
      value: { PatientId: PatientId, Type: "Casuality", ...rest },
    });

    navigate("/Home/Registration");
  };



  

 

  const handleeditDiagnosisPatientRegister = (params) => {
    const { PatientId, ...rest } = params;

    console.log("Diagnosissssssss", params);

    dispatchvalue({
      type: "Registeredit",
      value: { PatientId: PatientId, Type: "Diagnosis", ...rest },
    });

    navigate("/Home/Registration");
  };

  const handleeditLaboratoryPatientRegister = (params) => {
    // Destructure the id and PatientId from the params object
    const { PatientId, ...rest } = params;

    console.log("laboratoryyyyyyyy", params);

    dispatchvalue({
      type: "Registeredit",
      value: { PatientId: PatientId, Type: "Laboratory", ...rest },
    });

    navigate("/Home/Registration");
  };

  const handleSearchChange = (table, e) => {
    if (table === "OP") {
      setsearchOPParams({ ...searchOPParams, query: e.target.value });
    } else if (table === "IP") {
      setsearchIPParams({ ...searchIPParams, query: e.target.value });
    } else if (table === "Casuality") {
      setsearchCasualityParams({
        ...searchCasualityParams,
        query: e.target.value,
      });
    } else if (table === "Emergency") {
      setsearchEmergencyParams({
        ...searchEmergencyParams,
        query: e.target.value,
      });
    }  else if (table === "Diagnosis") {
      setsearchDiagnosisParams({
        ...searchDiagnosisParams,
        query: e.target.value,
      });
    } else if (table === "Laboratory") {
      setsearchLaboratoryParams({
        ...searchLaboratoryParams,
        query: e.target.value,
      });
    }
  };

  const handleStatusChange = (table, e) => {
    console.log("Status selected:", e.target.value);
    if (table === "OP") {
      setsearchOPParams({ ...searchOPParams, status: e.target.value });
    } else if (table === "IP") {
      setsearchIPParams({ ...searchIPParams, status: e.target.value });
    } else if (table === "Casuality") {
      setsearchCasualityParams({ ...searchCasualityParams,status: e.target.value});
    } else if (table === "Emergency") {
      setsearchCasualityParams({...searchCasualityParams,status: e.target.value});
    } 
    else if (table === "Diagnosis") {
      setsearchDiagnosisParams({...searchDiagnosisParams,status: e.target.value
      });
    } else if (table === "Laboratory") {
      setsearchLaboratoryParams({...searchLaboratoryParams,status: e.target.value,
      });
    }
  };

  const [selectedType, setSelectedType] = useState("OP");

  const handleSelectChange = (event) => {
    setSelectedType(event.target.value);
  };

  return (
    <>
      <div className="Main_container_app">
        <h3>Patient Register List</h3>

        <div className="RegisterTypecon  navchange">
          <div className="RegisterType">
            {["OP", "IP", "EMERGENCY", "DIAGNOSIS", "LABORATORY"].map(
              (p, ind) => (
                <div className="registertypeval" key={ind + "key"}>
                  <input
                    type="radio"
                    id={p}
                    name="appointment_type"
                    checked={selectedType === p}
                    // checked={InsuranceClientForm === p}
                    onChange={handleSelectChange}
                    value={p}
                  />
                  <label htmlFor={p}>{p}</label>
                </div>
              )
            )}
          </div>
        </div>

        <div className="content " style={{ width: "100%" }}>
          {selectedType === "OP" && (
            <div className="op-content">
              <div className="DivCenter_container">OP Patient Details </div>
              <div className="search_div_bar">
               
                <button
                    className="RegisterForm_1_btns choose_file_update"
                    onClick={handlenewPatientRegister}
                    data-tooltip-id="add-patient-tooltip"
                >
                    <AddCircleIcon />
                </button>
                <Tooltip id="add-patient-tooltip" place="top" content="New Patient Register" />

                <div className=" search_div_bar_inp_1">
                  <label htmlFor="">
                    Search by
                    <span>:</span>
                  </label>
                  <input
                    type="text"
                    value={searchOPParams.query}
                    placeholder="Patient ID or Name or PhoneNo "
                    onChange={(e) => handleSearchChange("OP", e)}
                  />
                </div>
                
                <div className=" RegisForm_1">
                  <label htmlFor="">
                    Status
                    <span>:</span>
                  </label>
                  <select
                    id=""
                    name="status"
                    value={searchOPParams.status}
                    onChange={(e) => handleStatusChange("OP", e)}
                  >
                    <option value="">Select</option>
                    <option value="Registered">Registered</option>
                    <option value="Completed">Completed</option>
                  </select>
                </div>

                <div className="RegisForm_1">
                    <label> Date <span>:</span> </label>
                    <select 
                        value={dateOption} 
                        onChange={handleDateOptionChange}
                    >
                        <option value="current">Current Date</option>
                        <option value="custom">Custom Date</option>
                        <option value="particular">Particular Date</option>
                    </select>

                    {dateOption === 'current' && (
                        <div className="RegisForm_1">
                            <input
                            type="date"
                            value={CurrentDate}
                            onChange={handleCurrentDateChange}
                            />
                        </div>
                    )}

                    {dateOption === 'custom' && (
                        <div className="RegisForm_1">
                        <label> From  <span>:</span> </label>

                        <input
                            type="date"
                            placeholder="From Date"
                            value={fromDate}
                            onChange={handleFromDateChange}
                        />
                        <label> To  <span>:</span> </label>

                        <input
                            type="date"
                            placeholder="To Date"
                            value={toDate}
                            onChange={handleToDateChange}
                        />
                        </div>
                    )}

                    {/* Particular Date Input */}
                    <br/>
                    {dateOption === 'particular' && (
                        <div className="RegisForm_1">
                            <label> Select Date <span>:</span> </label>
                            <input type="date" value={ParticularDate} onChange={handleParticularDateChange} />
                        </div>
                    )}
                </div>

                {/* <button
                  className="search_div_bar_btn_1"
                  onClick={handlenewPatientRegister}
                  title="New Patient Register"
                >
                  <LoupeIcon />
                </button> */}

              </div>
              <ReactGrid
                columns={PatientOPRegisterColumns}
                RowData={PatientRegisterData}
              />
            </div>
          )}

          {selectedType === "IP" && (
            <div className="ip-content">
              <div className="DivCenter_container">IP Patient Details </div>
              <div className="search_div_bar">
                  <button
                      className="RegisterForm_1_btns choose_file_update"
                      onClick={handlenewIPPatientRegister}
                      data-tooltip-id="add-patient-tooltip"
                  >
                      <AddCircleIcon />
                  </button>
                

                  <Tooltip id="add-patient-tooltip" place="top" content="New Patient Register" />

                
                <div className=" search_div_bar_inp_1">
                  <label htmlFor="">
                    Search by
                    <span>:</span>
                  </label>
                  <input
                    type="text"
                    value={searchIPParams.query}
                    placeholder="Patient ID or Name or PhoneNo "
                    onChange={(e) => handleSearchChange("IP", e)}
                  />
                </div>
                <div className=" RegisForm_1">
                  <label htmlFor="">
                    Status
                    <span>:</span>
                  </label>
                  <select
                    id=""
                    name="status"
                    value={searchIPParams.status}
                    onChange={(e) => handleStatusChange("IP", e)}
                  >
                    <option value="">Select</option>
                    <option value="Admitted">Admitted</option>
                    <option value="Completed">Completed</option>
                  </select>
                </div>

                {/* <button
                  className="search_div_bar_btn_1"
                  onClick={handlenewIPPatientRegister}
                  title="New Patient Register"
                >
                  <LoupeIcon />
                </button> */}
              </div>
              <ReactGrid
                columns={PatientIPRegisterColumns}
                RowData={PatientIPRegisterData}
              />
            </div>
          )}

          {/* {selectedType === "CASUALITY" && (
            <div className="casuality-content">
              <div className="DivCenter_container">
                Casuality Patient Details{" "}
              </div>
              <div className="search_div_bar">
                <div className=" search_div_bar_inp_1">
                  <label htmlFor="">
                    Search by
                    <span>:</span>
                  </label>
                  <input
                    type="text"
                    value={searchCasualityParams.query}
                    placeholder="Patient ID or Name or PhoneNo "
                    onChange={(e) => handleSearchChange("Casuality", e)}
                  />
                </div>
                <div className=" RegisForm_1">
                  <label htmlFor="">
                    Status
                    <span>:</span>
                  </label>
                  <select
                    id=""
                    name="status"
                    value={searchCasualityParams.status}
                    onChange={(e) => handleStatusChange("Casuality", e)}
                  >
                    <option value="">Select</option>
                    <option value="Pending">Pending</option>
                    <option value="Completed">Completed</option>
                  </select>
                </div>
                <button
                  className="search_div_bar_btn_1"
                  onClick={handlenewPatientRegister}
                  title="New Patient Register"
                >
                  <LoupeIcon />
                </button>
              </div>
              <ReactGrid
                columns={PatientCasualityRegisterColumns}
                RowData={PatientCasualityRegisterData}
              />
            </div>
          )} */}

          {selectedType === "EMERGENCY" && (
            <div className="casuality-content">
              <div className="DivCenter_container">
                Emergency Patient Details{" "}
              </div>
              <div className="search_div_bar">

                <button
                    className="RegisterForm_1_btns choose_file_update"
                    onClick={handleNewEmergencyPatientRegister}
                    data-tooltip-id="add-patient-tooltip"
                >
                    <AddCircleIcon />
                </button>
              

                <Tooltip id="add-patient-tooltip" place="top" content="New Patient Register" />

                <div className=" search_div_bar_inp_1">
                  <label htmlFor="">
                    Search by
                    <span>:</span>
                  </label>
                  <input
                    type="text"
                    value={searchEmergencyParams.query}
                    placeholder="Patient ID or Name or PhoneNo "
                    onChange={(e) => handleSearchChange("Emergency", e)}
                  />
                </div>
                <div className=" RegisForm_1">
                  <label htmlFor="">
                    Status
                    <span>:</span>
                  </label>
                  <select
                    id=""
                    name="status"
                    value={searchEmergencyParams.status}
                    onChange={(e) => handleStatusChange("Emergency", e)}
                  >
                    <option value="">Select</option>
                    <option value="Admitted">Admitted</option>
                    <option value="Completed">Completed</option>
                  </select>
                </div>
                
                {/* <button
                  className="search_div_bar_btn_1"
                  onClick={handleNewEmergencyPatientRegister}
                  title="New Patient Register"
                >
                  <LoupeIcon />
                </button> */}
              </div>
              <ReactGrid
                columns={PatientEmergencyRegisterColumns}
                RowData={PatientEmergencyRegisterData}
              />
            </div>
          )}

          {selectedType === "DIAGNOSIS" && (
            <div className="diagnosis-content">
              <div className="DivCenter_container">
                Diagnosis Patient Details{" "}
              </div>
              <div className="search_div_bar">

                <button
                    className="RegisterForm_1_btns choose_file_update"
                    onClick={handlenewPatientRegister}
                    data-tooltip-id="add-patient-tooltip"
                >
                    <AddCircleIcon />
                </button>
                
                <Tooltip id="add-patient-tooltip" place="top" content="New Patient Register" />

                <div className=" search_div_bar_inp_1">
                  <label htmlFor="">
                    Search by
                    <span>:</span>
                  </label>
                  <input
                    type="text"
                    value={searchDiagnosisParams.query}
                    placeholder="Patient ID or Name or PhoneNo "
                    onChange={(e) => handleSearchChange("Diagnosis", e)}
                  />
                </div>
                <div className=" RegisForm_1">
                  <label htmlFor="">
                    Status
                    <span>:</span>
                  </label>
                  <select
                    id=""
                    name="status"
                    value={searchDiagnosisParams.status}
                    onChange={(e) => handleStatusChange("Diagnosis", e)}
                  >
                    <option value="">Select</option>
                    <option value="Pending">Pending</option>
                    <option value="Completed">Completed</option>
                  </select>
                </div>

                {/* <button
                  className="search_div_bar_btn_1"
                  onClick={handlenewPatientRegister}
                  title="New Patient Register"
                >
                  <LoupeIcon />
                </button> */}
              </div>
              <ReactGrid
                columns={PatientDiagnosisRegisterColumns}
                RowData={PatientDiagnosisRegisterData}
              />
            </div>
          )}
          {selectedType === "LABORATORY" && (
            <div className="laboratory-content">
              <div className="DivCenter_container">
                Laboratory Patient Details{" "}
              </div>
              <div className="search_div_bar">

                <button
                    className="RegisterForm_1_btns choose_file_update"
                    onClick={handlenewPatientRegister}
                    data-tooltip-id="add-patient-tooltip"
                >
                    <AddCircleIcon />
                </button>
              
                <Tooltip id="add-patient-tooltip" place="top" content="New Patient Register" />

                <div className=" search_div_bar_inp_1">
                  <label htmlFor="">
                    Search by
                    <span>:</span>
                  </label>
                  <input
                    type="text"
                    value={searchLaboratoryParams.query}
                    placeholder="Patient ID or Name or PhoneNo "
                    onChange={(e) => handleSearchChange("Laboratory", e)}
                  />
                </div>

                <div className=" RegisForm_1">
                  <label htmlFor="">
                    Status
                    <span>:</span>
                  </label>
                  <select
                    id=""
                    name="status"
                    value={searchLaboratoryParams.status}
                    onChange={(e) => handleStatusChange("Laboratory", e)}
                  >
                    <option value="">Select</option>
                    <option value="Pending">Pending</option>
                    <option value="Completed">Completed</option>
                  </select>
                </div>

                {/* <button
                  className="search_div_bar_btn_1"
                  onClick={handlenewPatientRegister}
                  title="New Patient Register"
                >
                  <LoupeIcon />
                </button> */}
              </div>
              <ReactGrid
                columns={PatientLaboratoryRegisterColumns}
                RowData={PatientLaboratoryRegisterData}
              />
            </div>
          )}
        </div>
      </div>
      <ToastAlert Message={toast.message} Type={toast.type} />
    </>
  );
};
export default RegistrationList;
