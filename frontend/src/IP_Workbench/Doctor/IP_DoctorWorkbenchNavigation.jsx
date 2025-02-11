import React, { useState, useEffect, lazy, Suspense } from "react";
import "../../DoctorWorkBench/Navigation.css";
// import "../Navigation.css";
import ToggleOnIcon from "@mui/icons-material/ToggleOn";
import ToggleOffIcon from "@mui/icons-material/ToggleOff";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import "../../DoctorWorkBench/TreatmentComponent.css";
import axios from "axios";
import bgImg2 from "../../Assets/bgImg2.jpg";

const LabTest = lazy(() => import("./LabTest.jsx"));
const RadiologyTest = lazy(() => import("./RadiologyTest.jsx"));

const IP_Vitals = lazy(() => import("./IP_Vitals.jsx"));

const IP_SurgicalHistory = lazy(() => import("./IP_SurgicalHistory.jsx"));
const IP_Assesment = lazy(() => import("./IP_Assesment.jsx"));
const IP_InputOutputChart = lazy(() => import("./IP_InputOutputChart.jsx"));
const IP_ProgressNotes = lazy(() => import("./IP_ProgressNotes.jsx"));
const IP_DocMlc = lazy(() => import("./IP_DocMlc.jsx"));
const IP_Doc_DAMA = lazy(() => import("./IP_Doc_DAMA.jsx"));
const IP_Doc_PreoperativeChecklist = lazy(() =>
  import("./IP_Doc_PreoperativeChecklist.jsx")
);
const IP_DoctorPrescribtion = lazy(() => import("./Ip_DoctorPrescribtion.jsx"));
const NewProcedure = lazy(() => import("./NewProcedure.js"));

const IP_DoctorWorkbenchNavigation = () => {
  const IP_DoctorWorkbenchNavigation = useSelector(
    (state) => state.Frontoffice?.IP_DoctorWorkbenchNavigation
  );

  console.log(IP_DoctorWorkbenchNavigation);
  const UrlLink = useSelector((state) => state.userRecord?.UrlLink);
  const AllergyDetails = useSelector(state => state.Frontoffice?.AllergyDetails);

  const dispatchvalue = useDispatch();
  const navigate = useNavigate();
  const [ActiveTab, setActiveTab] = useState("IP_Vitals");
  const [isToggled, setIsToggled] = useState(false);
  const [AdmissionDetails, setAdmissionDetails] = useState([]);
  const [CurrentPreviousRoom, setCurrentPreviousRoom] = useState(null);
  const [Assesment, setAssesment] = useState([]);
  const [AllergyData, setAllergyData] = useState([]);
  const [ShowAllergyData, setShowAllergyData] = useState(false);
  const [showTooltip, setShowTooltip] = useState(false);

  const [openModal, setOpenModal] = useState(false);

  const isSidebarOpen = useSelector((state) => state.userRecord?.isSidebarOpen);

  const handleEditClick = () => {
    setOpenModal(true);
  };


  const toggle = () => setIsToggled(!isToggled);

  const handleTabChange = (tab) => {
    setActiveTab(tab);
    closeToggle();
  };

  const closeToggle = () => {
    setIsToggled(false);
  };

  useEffect(() => {
    console.log(IP_DoctorWorkbenchNavigation);
    if (Object.keys(IP_DoctorWorkbenchNavigation).length === 0) {
      navigate("/Home/IP_WorkbenchQuelist");
    }
    // else if (Object.keys(Casuality_DoctorWorkbenchNavigation).length === 0) {
    //   navigate('/Home/CasualityDocQuelist')
    // }
  }, [IP_DoctorWorkbenchNavigation]);

useEffect(() => {
  if (AllergyData.length > 0) {
      dispatchvalue({ type: "AllergyDetails", value: AllergyData });
      console.log({ type: "AllergyDetails", value: AllergyData }, 'Dispatching AllergyDetails');
  }
}, [AllergyData]); // This will run whenever gridData changes


  useEffect(() => {
    const RegistrationId = IP_DoctorWorkbenchNavigation?.RegistrationId;
    axios
      .get(`${UrlLink}Frontoffice/get_AdmissionDetails`, {
        params: {
          RegistrationId: RegistrationId,
        },
      })
      .then((res) => {
        setAdmissionDetails(res.data);
        console.log(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  }, [UrlLink, IP_DoctorWorkbenchNavigation]);





  useEffect(() => {
    axios
      .get(
        `${UrlLink}Frontoffice/get_ip_roomdetials_for_bedtransfer_details?RegistrationId=${IP_DoctorWorkbenchNavigation?.RegistrationId}`
      )
      .then((res) => {
        const ress = res.data;
        setCurrentPreviousRoom(ress);
        console.log(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  }, [UrlLink, IP_DoctorWorkbenchNavigation]);



  useEffect(() => {
    const RegistrationId = IP_DoctorWorkbenchNavigation?.RegistrationId;
    const departmentType = IP_DoctorWorkbenchNavigation?.RequestType;

    if (RegistrationId) {
      axios
        .get(`${UrlLink}Ip_Workbench/IP_Assesment_details_Link`, {
          params: {
            RegistrationId: RegistrationId,
            DepartmentType: departmentType,
          },
        })
        .then((res) => {
          const ress = res.data;
          console.log(res);
          setAssesment(ress);
        })
        .catch((err) => {
          console.log(err);
        });
    }
  }, [UrlLink, IP_DoctorWorkbenchNavigation]);

  useEffect(() => {
    const RegistrationId = IP_DoctorWorkbenchNavigation?.RegistrationId;
    const departmentType = IP_DoctorWorkbenchNavigation?.RequestType;

    if (RegistrationId) {
      axios
        .get(`${UrlLink}Ip_Workbench/IP_Allergy_Details_Link`, {
          params: {
            RegistrationId: RegistrationId,
            DepartmentType: departmentType,
          },
        })
        .then((res) => {
          setAllergyData(res.data);
          console.log(res.data);
          setShowAllergyData(true);
        })
        .catch((err) => {
          console.log(err);
        });
    }
  }, [UrlLink, IP_DoctorWorkbenchNavigation, ShowAllergyData]);




  // useEffect(() => {
  //   if (Object.keys(IP_DoctorWorkbenchNavigation).length === 0 && Object.keys(Casuality_DoctorWorkbenchNavigation).length === 0) {
  //     navigate('/Home/IP_WorkbenchQuelist');
  //   } else if (Object.keys(Casuality_DoctorWorkbenchNavigation).length === 0) {
  //     navigate('/Home/CasualityDocQuelist');
  //   }
  // }, [IP_DoctorWorkbenchNavigation, Casuality_DoctorWorkbenchNavigation]);

  return (
    <>
      <div className="Main_container_app">
        <div className="new-patient-registration-form">
          <div className="dctr_info_up_head">
            <div className="RegisFormcon ">
              <div className="dctr_info_up_head22">
                <img
                  src={bgImg2}
                  // src={IP_DoctorWorkbenchNavigation?.PatientProfile}
                  alt="Default Patient Photo"
                />

                <label>Profile</label>
              </div>
            </div>

            <div className="RegisFormcon_1">
              <div className="RegisForm_1 ">
                <label htmlFor="PatientID">
                  Patient ID <span>:</span>
                </label>
                <span className="dctr_wrbvh_pice" htmlFor="PatientID">
                  {IP_DoctorWorkbenchNavigation?.PatientId}
                </span>
              </div>
              <div className="RegisForm_1 ">
                <label htmlFor="PatientName">
                  Patient Name <span>:</span>{" "}
                </label>
                <span className="dctr_wrbvh_pice" htmlFor="PatientName">
                  {IP_DoctorWorkbenchNavigation?.PatientName}
                </span>
              </div>

              <div className="RegisForm_1 ">
                <label htmlFor="AgeGender">
                  Age / Gender <span>:</span>{" "}
                </label>
                <span className="dctr_wrbvh_pice" htmlFor="Age">
                  {IP_DoctorWorkbenchNavigation?.Age} /{" "}
                  {IP_DoctorWorkbenchNavigation?.Gender}
                </span>
              </div>


             
              <div className="RegisForm_1 ">
                <label htmlFor="Gender">
                  Blood Group <span>:</span>{" "}
                </label>
                <span className="dctr_wrbvh_pice" htmlFor="Gender">
                  {IP_DoctorWorkbenchNavigation?.BloodGroup}
                </span>
              </div>

              <div className="RegisForm_1 ">
                <label htmlFor="RegistrationIdBedNo">
                  IP No / Bed No<span>:</span>{" "}
                </label>
                <span className="dctr_wrbvh_pice" htmlFor="RegistrationIdBedNo">
                  {IP_DoctorWorkbenchNavigation?.RegistrationId} /
                  { IP_DoctorWorkbenchNavigation?.BedNo}
                </span>
              </div>

              <div className="RegisForm_1 ">
                <label htmlFor="DoctorName">
                  Doctor Name <span>:</span>{" "}
                </label>
                <span className="dctr_wrbvh_pice" htmlFor="DoctorName">
                  {IP_DoctorWorkbenchNavigation?.DoctorName}
                </span>
              </div>

              
              {AdmissionDetails.length > 0 && (
                <div className="RegisForm_1 ">
                  <label htmlFor="AdmissionPurpose">
                    POA<span>:</span>{" "}
                  </label>
                  <span className="dctr_wrbvh_pice" htmlFor="AdmissionPurpose">
                    {AdmissionDetails?.[0]?.AdmissionPurpose}
                  </span>
                </div>
              )}


              <div className="RegisForm_1 ">
                <label htmlFor="AdmitDate">
                  DOA<span>:</span>{" "}
                </label>
                <span className="dctr_wrbvh_pice" htmlFor="AdmitDate">
                  {CurrentPreviousRoom?.ip_register_data?.[0]?.AdmitDate}
                </span>
              </div>

              <div className="RegisForm_1">
                <label htmlFor="PatientCategory">
                  Patient Category <span>:</span>
                </label>
                <span className="dctr_wrbvh_pice" htmlFor="PatientCategory">
                  {IP_DoctorWorkbenchNavigation?.PatientCategory}
                </span>
              </div>


              {["Insurance", "Client"].includes(IP_DoctorWorkbenchNavigation?.PatientCategory && IP_DoctorWorkbenchNavigation?.PatientCategoryName) && (
                <div className="RegisForm_1">
                  <label htmlFor="InsuranceNameClientName">
                    {IP_DoctorWorkbenchNavigation?.PatientCategory === "Insurance"
                      ? "Insurance Name"
                      : "Client Name"}
                    <span>:</span>
                  </label>
                  <span className="dctr_wrbvh_pice" htmlFor="InsuranceNameClientName">
                    {IP_DoctorWorkbenchNavigation?.PatientCategoryName}
                  </span>
                </div>
              )}


              <div className="RegisForm_1 ">
                <label htmlFor="IsMLC">
                  MLC<span>:</span>
                </label>
                <span className="dctr_wrbvh_pice" htmlFor="IsMLC">
                  {IP_DoctorWorkbenchNavigation?.IsMLC}
                </span>
              </div>


              {Assesment.length > 0 && (
                <div className="RegisForm_1 ">
                  <label htmlFor="FinalDiagnosis">
                    FinalDiagnosis<span>:</span>
                  </label>
                  <span className="dctr_wrbvh_pice" htmlFor="FinalDiagnosis">
                    {Assesment?.[0]?.FinalDiagnosis}
                  </span>
                </div>
              )}

              <div className="RegisFormcon_j">
                {/* Only render Allergy button and modal if there is allergy data */}
                {AllergyDetails?.length > 0 && (
                  <div className="jhidusch_90">
                    <button onClick={handleEditClick}>Allergy</button>

                    {/* Conditional rendering for the modal */}
                    {openModal && (
                      <div
                        className={
                          isSidebarOpen
                            ? "sideopen_showcamera_profile_chirayu"
                            : "showcamera_profile_chirayu"
                        }
                        onClick={() => {
                          setOpenModal(false);
                        }}
                      >
                        <div
                          className="neww_chirayu"
                          onClick={(e) => e.stopPropagation()} // Prevent modal close when clicking inside
                        >
                          <button
                            className="modal-close-btnSS"
                            onClick={() => setOpenModal(false)}
                          >
                            &times; {/* Close button */}
                          </button>

                          <div className="judscy_uj11">
                            <div className="wwdsdlm_o">
                              {AllergyDetails.map(
                                (allergy) => allergy.Allergent
                              ).join(", ")}
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>

              <div className="RegisFormcon_j">
                <div className="jjxss_07">
                  {/* <h4>
                    Flagging<span>:</span>
                  </h4> */}
                  <h4
                    style={{
                      width: "30px",
                      height: "20px",
                      backgroundColor:
                        IP_DoctorWorkbenchNavigation?.FlaggingColour || "green",
                      position: "relative",
                      cursor: "pointer",
                    }}
                    onMouseEnter={() => setShowTooltip(true)}
                    onMouseLeave={() => setShowTooltip(false)}
                  >
                    {/* Tooltip div */}
                    {showTooltip && (
                      <div
                        style={{
                          position: "absolute",
                          top: "-25px",
                          left: "0",
                          backgroundColor: "rgba(0, 0, 0, 0.75)",
                          color: "#fff",
                          padding: "5px 10px",
                          borderRadius: "4px",
                          fontSize: "12px",
                          whiteSpace: "nowrap",
                        }}
                      >
                        {IP_DoctorWorkbenchNavigation?.Flagging ||
                          "No flagging data"}
                      </div>
                    )}
                  </h4>
                </div>
              </div>








            </div>
          </div>

          <div className="new-patient-registration-form">
            <div className="new-navigation">
              <h2>
                <button
                  style={{ color: ActiveTab === "IP_Vitals" ? "white" : "" }}
                  onClick={() => handleTabChange("IP_Vitals")}
                >
                  Vitals
                </button>
                |
                {/* <button style={{ color: ActiveTab === "IP_MedicalHistory" ? 'white' : '' }} onClick={() => handleTabChange("IP_MedicalHistory")}>
                MedicalHistory
                </button>
                | */}
                <button
                  style={{
                    color: ActiveTab === "IP_SurgicalHistory" ? "white" : "",
                  }}
                  onClick={() => handleTabChange("IP_SurgicalHistory")}
                >
                  Surgical History
                </button>
                |
                <button
                  style={{ color: ActiveTab === "IP_Assesment" ? "white" : "" }}
                  onClick={() => handleTabChange("IP_Assesment")}
                >
                  Assesment
                </button>
                {/* |
                <button
                  style={{
                    color: ActiveTab === "IP_InputOutputChart" ? "white" : "",
                  }}
                  onClick={() => handleTabChange("IP_InputOutputChart")}
                >
                  Input Output Chart
                </button> */}
                |
                <button
                  style={{
                    color: ActiveTab === "IP_ProgressNotes" ? "white" : "",
                  }}
                  onClick={() => handleTabChange("IP_ProgressNotes")}
                >
                  ProgressNotes
                </button>
                |
                <button
                  style={{ color: ActiveTab === "IP_DocMlc" ? "white" : "" }}
                  onClick={() => handleTabChange("IP_DocMlc")}
                >
                  MLC
                </button>
                |
                <button
                  style={{ color: ActiveTab === "IP_Doc_DAMA" ? "white" : "" }}
                  onClick={() => handleTabChange("IP_Doc_DAMA")}
                >
                  DAMA
                </button>
                |
                <button
                  style={{
                    color:
                      ActiveTab === "IP_Doc_PreoperativeChecklist"
                        ? "white"
                        : "",
                  }}
                  onClick={() =>
                    handleTabChange("IP_Doc_PreoperativeChecklist")
                  }
                >
                  PreoperativeChecklist
                </button>
                |
                <div className="Lab_dropdown">
                  <button
                    style={{
                      color:
                        ActiveTab === "Lab_Test" ||
                          ActiveTab === "Radiology_Test"
                          ? "white"
                          : "",
                    }}
                    className="Lab_button"
                  >
                    Diagnostics
                  </button>
                  <div className="Lab_dropdown_content">
                    <button
                      style={{ color: ActiveTab === "Lab_Test" ? "white" : "" }}
                      onClick={() => handleTabChange("Lab_Test")}
                    >
                      Lab
                    </button>
                    <button
                      style={{
                        color: ActiveTab === "Radiology_Test" ? "white" : "",
                      }}
                      onClick={() => handleTabChange("Radiology_Test")}
                    >
                      Radiology
                    </button>
                  </div>
                </div>
                |
                <button
                  style={{
                    color: ActiveTab === "IP_DoctorPrescribtion" ? "white" : "",
                  }}
                  onClick={() => handleTabChange("IP_DoctorPrescribtion")}
                >
                  Prescription
                </button>
                |
                <button
                  style={{
                    color: ActiveTab === "NewProcedure" ? "white" : "",
                  }}
                  onClick={() => handleTabChange("NewProcedure")}
                >
                  Therapy
                </button>
              </h2>
            </div>

            <div className="new-kit ">
              <button className="new-tog" onClick={toggle}>
                {isToggled ? <ToggleOffIcon /> : <ToggleOnIcon />}
              </button>

              <div>
                {isToggled && (
                  <div className="new-navigation-toggle">
                    <h2>
                      <button
                        style={{
                          color: ActiveTab === "IP_Vitals" ? "white" : "",
                        }}
                        onClick={() => handleTabChange("IP_Vitals")}
                      >
                        Vitals
                      </button>
                      |
                      {/* <button style={{ color: ActiveTab === "IP_MedicalHistory" ? 'white' : '' }} onClick={() => handleTabChange("IP_MedicalHistory")}>
                      MedicalHistory
                      </button>
                      | */}
                      <button
                        style={{
                          color:
                            ActiveTab === "IP_SurgicalHistory" ? "white" : "",
                        }}
                        onClick={() => handleTabChange("IP_SurgicalHistory")}
                      >
                        Surgical History
                      </button>
                      |
                      <button
                        style={{
                          color: ActiveTab === "IP_Assesment" ? "white" : "",
                        }}
                        onClick={() => handleTabChange("IP_Assesment")}
                      >
                        Assesment
                      </button>
                      |
                      <button
                        style={{
                          color:
                            ActiveTab === "IP_InputOutputChart" ? "white" : "",
                        }}
                        onClick={() => handleTabChange("IP_InputOutputChart")}
                      >
                        Input Output Chart
                      </button>
                      |
                      <button
                        style={{
                          color:
                            ActiveTab === "IP_ProgressNotes" ? "white" : "",
                        }}
                        onClick={() => handleTabChange("IP_ProgressNotes")}
                      >
                        ProgressNotes
                      </button>
                      |
                      <button
                        style={{
                          color: ActiveTab === "IP_DocMlc" ? "white" : "",
                        }}
                        onClick={() => handleTabChange("IP_DocMlc")}
                      >
                        MLC
                      </button>
                      |
                      <button
                        style={{
                          color: ActiveTab === "IP_Doc_DAMA" ? "white" : "",
                        }}
                        onClick={() => handleTabChange("IP_Doc_DAMA")}
                      >
                        DAMA
                      </button>
                      |
                      <button
                        style={{
                          color:
                            ActiveTab === "IP_Doc_PreoperativeChecklist"
                              ? "white"
                              : "",
                        }}
                        onClick={() =>
                          handleTabChange("IP_Doc_PreoperativeChecklist")
                        }
                      >
                        PreoperativeChecklist
                      </button>
                      |
                      <div className="Lab_dropdown">
                        <button
                          style={{
                            color:
                              ActiveTab === "Lab_Test" ||
                                ActiveTab === "Radiology_Test"
                                ? "white"
                                : "",
                          }}
                          className="Lab_button"
                        >
                          Diagnostics
                        </button>
                        <div className="Lab_dropdown_content">
                          <button
                            style={{
                              color: ActiveTab === "Lab_Test" ? "white" : "",
                            }}
                            onClick={() => handleTabChange("Lab_Test")}
                          >
                            Lab
                          </button>
                          <button
                            style={{
                              color:
                                ActiveTab === "Radiology_Test" ? "white" : "",
                            }}
                            onClick={() => handleTabChange("Radiology_Test")}
                          >
                            Radiology
                          </button>
                        </div>
                      </div>
                      |
                      <button
                        style={{
                          color:
                            ActiveTab === "IP_DoctorPrescribtion"
                              ? "white"
                              : "",
                        }}
                        onClick={() => handleTabChange("IP_DoctorPrescribtion")}
                      >
                        Prescription
                      </button>
                      |
                      <button
                        style={{
                          color: ActiveTab === "NewProcedure" ? "white" : "",
                        }}
                        onClick={() => handleTabChange("NewProcedure")}
                      >
                        Therapy
                      </button>
                    </h2>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
        <Suspense fallback={<div>Loading...</div>}>
          {ActiveTab === "IP_Vitals" && <IP_Vitals />}

          {/* {ActiveTab === "IPD_Handover" && <IPD_Handover />}  */}
          {/* {ActiveTab === "IP_MedicalHistory" && <IP_MedicalHistory />}  */}
          {ActiveTab === "IP_SurgicalHistory" && <IP_SurgicalHistory />}
          {ActiveTab === "IP_Assesment" && <IP_Assesment />}
          {ActiveTab === "IP_InputOutputChart" && <IP_InputOutputChart />}
          {ActiveTab === "IP_ProgressNotes" && <IP_ProgressNotes />}
          {ActiveTab === "IP_DocMlc" && <IP_DocMlc />}
          {ActiveTab === "IP_Doc_DAMA" && <IP_Doc_DAMA />}
          {ActiveTab === "IP_Doc_PreoperativeChecklist" && (
            <IP_Doc_PreoperativeChecklist />
          )}
          {ActiveTab === "Lab_Test" && <LabTest />}
          {ActiveTab === "Radiology_Test" && <RadiologyTest />}
          {ActiveTab === "IP_DoctorPrescribtion" && <IP_DoctorPrescribtion />}
          {ActiveTab === "NewProcedure" && <NewProcedure />}
        </Suspense>
      </div>
    </>
  );
};

export default IP_DoctorWorkbenchNavigation;


