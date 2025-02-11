import React, { useState, useEffect, lazy, Suspense } from "react";
import "./Navigation.css";
import ToggleOnIcon from "@mui/icons-material/ToggleOn";
import ToggleOffIcon from "@mui/icons-material/ToggleOff";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import bgImg2 from "../Assets/bgImg2.jpg";
import "./TreatmentComponent.css";
import "../DoctorWorkBench/TreatmentComponent.css";
import axios from "axios";

const Vitals = lazy(() => import("./vitals.jsx"));
const Allergy = lazy(() => import("./Allergy.jsx"));
const Neurology = lazy(() => import("./Neurology.jsx"));
const IFCard = lazy(() => import("./IFCard.jsx"));
const Gynecology = lazy(() => import("./Gynecology.jsx"));
const OP_Sheet = lazy(() => import("./OP_Sheet.jsx"));
const PastHistory = lazy(() => import("./PastHistory.js"));
const Prescription = lazy(() => import("./Prescription.js"));
const NewProcedure = lazy(() => import("./NewProcedure.js"));
const GeneralEvaluation = lazy(() => import("./GeneralEvaluation.jsx"));
const LabTest = lazy(() => import("./LabTest.jsx"));
const RadiologyTest = lazy(() => import("./RadiologyTest.jsx"));
const Opthalmology = lazy(() => import("./Opthalmology.jsx"));
const AncCard = lazy(() => import("./ANCCard.jsx"));

// const ReferaDoctor = lazy(() => import('./ReferaDoctor.jsx'));
// const FollowUp = lazy(() => import('./FollowUp.jsx'));
// const OtRequest = lazy(() => import('./OtRequest.jsx'));
// const OpIpconnect = lazy(() => import('./OpIpconnect.jsx'))

const DoctorWorkbenchNavigation = () => {
  const DoctorWorkbenchNavigation = useSelector(
    (state) => state.Frontoffice?.DoctorWorkbenchNavigation
  );
  const SpecialityWise_DoctorWorkbenchNavigation = useSelector(
    (state) => state.Frontoffice?.SpecialityWise_DoctorWorkbenchNavigation
  );

  const AllergyDetails = useSelector(
    (state) => state.Frontoffice?.AllergyDetails
  );

  console.log(AllergyDetails, "AllergyDetails");
  console.log(
    SpecialityWise_DoctorWorkbenchNavigation,
    "SpecialityWise_DoctorWorkbenchNavigation"
  );
  console.log(DoctorWorkbenchNavigation, "DoctorWorkbenchNavigation");

  const UserData = useSelector((state) => state.userRecord?.UserData);
  console.log(UserData, "UserData");

  const UrlLink = useSelector((state) => state.userRecord?.UrlLink);

  const dispatchvalue = useDispatch();
  const navigate = useNavigate();
  const [ActiveTab, setActiveTab] = useState("Vitals");
  const [isToggled, setIsToggled] = useState(false);

  const toggle = () => setIsToggled(!isToggled);

  const handleTabChange = (tab) => {
    setActiveTab(tab);
    closeToggle();
  };

  const closeToggle = () => {
    setIsToggled(false);
  };

  useEffect(() => {
    console.log(AllergyDetails, "Redux AllergyDetails");
  }, [AllergyDetails]);

  const [SpecialityData, setSpecialityData] = useState([]);
  console.log(SpecialityData, "SpecialityData");

  useEffect(() => {
    axios
      .get(`${UrlLink}Masters/Speciality_Detials_link`)
      .then((res) => {
        const ress = res.data;
        setSpecialityData(ress);
      })
      .catch((err) => {
        console.log(err);
      });
  }, [UrlLink]);

  const [AllergyData, setAllergyData] = useState([]);
  console.log(AllergyData, "AllergyData");

  useEffect(() => {
    let registerid = null;
    if (Object.keys(DoctorWorkbenchNavigation).length > 0) {
      registerid = DoctorWorkbenchNavigation?.pk;
    }
    if (Object.keys(SpecialityWise_DoctorWorkbenchNavigation).length > 0) {
      registerid = SpecialityWise_DoctorWorkbenchNavigation?.pk;
    }

    console.log(registerid, "registerididijfijfijfjijfkueygcuidojgcjb");

    axios
      .get(`${UrlLink}Workbench/Allergy_Details_Link`, {
        params: {
          RegistrationId: registerid,
        },
      })
      .then((res) => {
        setAllergyData(res.data);
      })
      .catch((err) => {
        console.log(err);
      });
  }, [UrlLink, DoctorWorkbenchNavigation]);

  useEffect(() => {
    if (AllergyData.length > 0) {
      dispatchvalue({ type: "AllergyDetails", value: AllergyData });
      console.log(
        { type: "AllergyDetails", value: AllergyData },
        "Dispatching AllergyDetails"
      );
    }
  }, [AllergyData]); // This will run whenever gridData changes

  const [condition, setCondition] = useState(false);

  // useEffect(()=> {
  //   console.log('1111111111');
  //   const SpecData = SpecialityData?.find((p)=> p?.Speciality_Id === DoctorWorkbenchNavigation?.Specialization)

  //   console.log(SpecData,'SpecData');

  //   const Speciality = UserData?.Specialization && DoctorWorkbenchNavigation?.Specialization === SpecData?.Speciality_Id
  //   console.log('222222222222',Speciality);

  //   if (Speciality) {
  //     const PatientSpeciality = DoctorWorkbenchNavigation?.Specialization === SpecData?.Speciality_Id
  //     console.log(PatientSpeciality,'PatientSpeciality');

  //     if (SpecData?.SpecialityName === 'NEUROLOGY'){
  //       setCondition(true)
  //       console.log('NEUROLOGY',condition);

  //     }
  //     else if (SpecData?.SpecialityName === 'CARDIOLOGY') {

  //       setCondition(true)
  //       console.log('CARDIOLOGY',condition);

  //     }
  //     else if (SpecData?.SpecialityName === 'GYNECOLOGY') {

  //       setCondition(true)
  //       console.log('GYNECOLOGY',condition);

  //     }
  //     else if (SpecData?.SpecialityName === 'OPTHALMOLOGY') {
  //       console.log('OPTHALMOLOGY',condition);

  //       setCondition(true)
  //     }
  //     else if (SpecData?.SpecialityName === 'ONCOLOGY') {
  //       console.log('ONCOLOGY',condition);

  //       setCondition(true)
  //     }

  //   }
  // },[UserData,DoctorWorkbenchNavigation,SpecialityData])

  // useEffect(() => {
  //   console.log('1111111111');

  //   // Find the relevant specialization data
  //   const SpecData = SpecialityData?.find(
  //     (p) => p?.Speciality_Id === DoctorWorkbenchNavigation?.Specialization
  //   );

  //   console.log(SpecData, 'SpecData');

  //   if (!SpecData) {
  //     console.error('SpecData not found');
  //     return;
  //   }

  //   // Check if the user's specialization matches
  //   const Speciality =
  //     UserData?.Specialization &&
  //     DoctorWorkbenchNavigation?.Specialization === SpecData?.Speciality_Id;

  //   console.log('222222222222', Speciality);

  //   if (Speciality) {
  //     const validSpecialities = [
  //       'NEUROLOGY',
  //       'CARDIOLOGY',
  //       'GYNECOLOGY',
  //       'OPTHALMOLOGY',
  //       'ONCOLOGY',
  //     ];

  //     // Check if the specialization is valid
  //     if (validSpecialities.includes(SpecData?.SpecialityName)) {
  //       setCondition(true);
  //       console.log(SpecData?.SpecialityName, 'Speciality set to true');
  //       console.log(condition,'condition');

  //     } else {
  //       setCondition(false);
  //     }
  //   }
  // }, [UserData, DoctorWorkbenchNavigation, SpecialityData]);

  // useEffect(() => {
  //   console.log('1111111111');

  //   if (!SpecialityData || !DoctorWorkbenchNavigation?.Specialization) {
  //     console.error("Missing SpecialityData or DoctorWorkbenchNavigation.Specialization");
  //     return;
  //   }

  //   const SpecData = SpecialityData.find(
  //     (p) => p?.Speciality_Id === DoctorWorkbenchNavigation?.Specialization
  //   );

  //   console.log(SpecData, 'SpecData');

  //   if (!SpecData) {
  //     console.error("No matching SpecData found");
  //     return;
  //   }

  //   const Speciality =
  //     UserData?.Specialization &&
  //     DoctorWorkbenchNavigation?.Specialization === SpecData?.Speciality_Id;

  //   console.log('222222222222', Speciality);

  //   if (Speciality) {
  //     const validSpecialities = [
  //       'NEUROLOGY',
  //       'CARDIOLOGY',
  //       'GYNECOLOGY',
  //       'OPTHALMOLOGY',
  //       'ONCOLOGY',
  //     ];

  //     if (validSpecialities.includes(SpecData?.SpecialityName)) {
  //       setCondition(true);
  //       console.log(condition,'validSpecialities');

  //     } else {
  //       setCondition(false);
  //     }
  //   }
  // }, [UserData, DoctorWorkbenchNavigation, SpecialityData]);

  const [specialityName, setSpecialityName] = useState(null);
  const [DocWiseSpeciality, setDocWiseSpeciality] = useState(null);
  const [isHost, setIsHost] = useState(false);
  console.log(specialityName, "specialityName");
  console.log(DocWiseSpeciality, "DocWiseSpeciality");

  // useEffect(() => {
  //   console.log("1111111111");
  //   const SpecData = SpecialityData?.find(
  //     (p) => p?.Speciality_Id === DoctorWorkbenchNavigation?.Specialization
  //   );

  //   console.log(SpecData, "SpecData");

  //   const Speciality =
  //     UserData?.Specialization &&
  //     DoctorWorkbenchNavigation?.Specialization === SpecData?.Speciality_Id;

  //   console.log("222222222222", Speciality);

  //   if (Speciality) {
  //     setSpecialityName(SpecData?.SpecialityName); // Set the SpecialityName dynamically
  //   } else {
  //     setSpecialityName(null); // Reset if no match
  //   }
  // }, [UserData, DoctorWorkbenchNavigation, SpecialityData]);

  // useEffect(() => {
  //   console.log("1111111111");

  //   if (UserData?.username === 'host' || UserData?.username === 'admin') {
  //     setIsHost(true); // Set isHost to true if the user is 'host'

  //     SpecialityWise_DoctorWorkbenchNavigation

  //     const DocSpecWise = SpecialityData?.find(
  //       (p) => p?.Speciality_Id === SpecialityWise_DoctorWorkbenchNavigation?.Specialization
  //     );

  //     console.log(DocSpecWise,'DocSpecWise');

  //     if(DocSpecWise){
  //       setDocWiseSpeciality(DocSpecWise?.SpecialityName)
  //     } else {
  //       setDocWiseSpeciality(null)
  //     }

  //   } else {
  //     setIsHost(false); // Reset isHost if not 'host'

  //     const SpecData = SpecialityData?.find(
  //       (p) => p?.Speciality_Id === DoctorWorkbenchNavigation?.Specialization
  //     );

  //     console.log(SpecData, "SpecData");

  //     const Speciality =
  //       UserData?.Specialization &&
  //       DoctorWorkbenchNavigation?.Specialization === SpecData?.Speciality_Id;

  //     console.log("222222222222", Speciality);

  //     if (Speciality) {
  //       setSpecialityName(SpecData?.SpecialityName); // Set the SpecialityName dynamically
  //     } else {
  //       setSpecialityName(null); // Reset if no match
  //     }
  //   }
  // }, [UserData, DoctorWorkbenchNavigation, SpecialityData,SpecialityWise_DoctorWorkbenchNavigation,DocWiseSpeciality]);

  // useEffect(() => {
  //   console.log("1111111111");

  //   if (UserData?.username === 'host' || UserData?.username === 'admin') {
  //     setIsHost(true); // Set isHost to true if the user is 'host'

  //     if (DoctorWorkbenchNavigation?.Specialization) {
  //       const SpecData = SpecialityData?.find(
  //         (p) => p?.Speciality_Id === DoctorWorkbenchNavigation?.Specialization
  //       );
  //     console.log(SpecData,'SpecData');

  //     }

  //     if (SpecialityWise_DoctorWorkbenchNavigation?.Specialization) {
  //       const DocSpecWise = SpecialityData?.find(
  //         (p) => p?.Speciality_Id === SpecialityWise_DoctorWorkbenchNavigation?.Specialization
  //       );
  //       console.log(DocSpecWise, 'DocSpecWise');

  //     }

  //     console.log(DocSpecWise?.SpecialityName, 'DocSpecWise?.SpecialityName');

  //     console.log(SpecData?.SpecialityName,'SpecData?.SpecialityName');

  //     setSpecialityName(null);
  //     setDocWiseSpeciality(null);

  //     // if (SpecData) {
  //     //   setSpecialityName(SpecData?.SpecialityName);
  //     // } else {
  //     //   setSpecialityName(null); // Reset if no match
  //     // }

  //     if (SpecData) {
  //       setSpecialityName(SpecData?.SpecialityName);
  //       console.log('kkkkkkkkkk');

  //     } else if (DocSpecWise) {

  //       setDocWiseSpeciality(DocSpecWise?.SpecialityName);
  //       console.log('lllllllllllllll');

  //     } else {
  //       // If neither are found, reset both
  //       setSpecialityName(null);
  //       setDocWiseSpeciality(null);
  //     }

  //     // if (DocSpecWise) {
  //     //   setDocWiseSpeciality(DocSpecWise?.SpecialityName);
  //     // } else {
  //     //   setDocWiseSpeciality(null);
  //     // }

  //   } else {
  //     setIsHost(false); // Reset isHost if not 'host'

  //     const SpecData = SpecialityData?.find(
  //       (p) => p?.Speciality_Id === DoctorWorkbenchNavigation?.Specialization
  //     );

  //     console.log(SpecData, "SpecData");

  //     const Speciality =
  //       UserData?.Specialization &&
  //       DoctorWorkbenchNavigation?.Specialization === SpecData?.Speciality_Id;

  //     console.log("222222222222", Speciality);

  //     setSpecialityName(null);

  //     if (Speciality) {
  //       setSpecialityName(SpecData?.SpecialityName); // Set the SpecialityName dynamically
  //     } else {
  //       setSpecialityName(null); // Reset if no match
  //     }

  //   }
  // }, [
  //   UserData,
  //   DoctorWorkbenchNavigation,
  //   SpecialityData,
  //   SpecialityWise_DoctorWorkbenchNavigation,

  // ]);

  //------------------------------19-12-2024

  useEffect(() => {
    console.log("1111111111");

    let SpecData = null;
    let DocSpecWise = null;

    if (UserData?.username === "host" || UserData?.username === "admin") {
      setIsHost(true); // Set isHost to true if the user is 'host'

      // Get SpecData based on DoctorWorkbenchNavigation
      if (DoctorWorkbenchNavigation?.Specialization) {
        SpecData = SpecialityData?.find(
          (p) => p?.Speciality_Id === DoctorWorkbenchNavigation?.Specialization
        );
        console.log(SpecData, "SpecData");
        console.log(SpecData?.Speciality_Id, "SpecData?.Speciality_Id");
        console.log(
          DoctorWorkbenchNavigation?.Specialization,
          "DoctorWorkbenchNavigation?.Specialization"
        );

        if (SpecData) {
          setSpecialityName(SpecData?.SpecialityName);
          console.log("matching patient", SpecData?.SpecialityName);
          setDocWiseSpeciality(null);
        } else {
          setSpecialityName(null);
        }
      }

      // Get DocSpecWise based on SpecialityWise_DoctorWorkbenchNavigation
      if (SpecialityWise_DoctorWorkbenchNavigation?.Specialization) {
        DocSpecWise = SpecialityData?.find(
          (p) =>
            p?.Speciality_Id ===
            SpecialityWise_DoctorWorkbenchNavigation?.Specialization
        );
        console.log(DocSpecWise, "DocSpecWise");
        console.log(DocSpecWise?.Speciality_Id, "DocSpecWise?.Speciality_Id");
        console.log(
          SpecialityWise_DoctorWorkbenchNavigation?.Specialization,
          "SpecialityWise_DoctorWorkbenchNavigation?.Specialization"
        );

        if (DocSpecWise) {
          setDocWiseSpeciality(DocSpecWise?.SpecialityName);
          console.log("matching speciality", DocSpecWise?.SpecialityName);
          setSpecialityName(null);
        } else {
          setDocWiseSpeciality(null);
        }
      }
    } else {
      setIsHost(false); // Reset isHost if not 'host'

      // Get SpecData based on DoctorWorkbenchNavigation
      if (DoctorWorkbenchNavigation?.Specialization) {
        const SpecData = SpecialityData?.find(
          (p) => p?.Speciality_Id === DoctorWorkbenchNavigation?.Specialization
        );
        console.log(SpecData, "SpecData");
        console.log(SpecData?.Speciality_Id, "SpecData?.Speciality_Id");
        console.log(UserData?.Specialization, "UserData?.Specialization");
        console.log(
          DoctorWorkbenchNavigation?.Specialization,
          "DoctorWorkbenchNavigation?.Specialization"
        );

        const PatientSpeciality =
          UserData?.Specialization &&
          DoctorWorkbenchNavigation?.Specialization === SpecData?.Speciality_Id;
        console.log("PatientSpeciality", PatientSpeciality);

        setSpecialityName(null);
        if (PatientSpeciality) {
          console.log("pppppppp");

          setSpecialityName(SpecData?.SpecialityName);
          console.log("matching totalpatient");

          setDocWiseSpeciality(null);
        } else {
          setSpecialityName(null); // Reset if no match
        }
      }

      if (SpecialityWise_DoctorWorkbenchNavigation?.Specialization) {
        DocSpecWise = SpecialityData?.find(
          (p) =>
            p?.Speciality_Id ===
            SpecialityWise_DoctorWorkbenchNavigation?.Specialization
        );
        console.log(DocSpecWise, "DocSpecWise");
        console.log(DocSpecWise?.Speciality_Id, "DocSpecWise?.Speciality_Id");
        console.log(UserData?.Specialization, "UserData?.Specialization");
        console.log(
          SpecialityWise_DoctorWorkbenchNavigation?.Specialization,
          "SpecialityWise_DoctorWorkbenchNavigation?.Specialization"
        );

        const DocPatientSpeciality =
          UserData?.Specialization &&
          SpecialityWise_DoctorWorkbenchNavigation?.Specialization ===
            DocSpecWise?.Speciality_Id;

        console.log("DocPatientSpeciality", DocPatientSpeciality);
        console.log("DocSpecWise?.SpecialityName", DocSpecWise?.SpecialityName);

        setDocWiseSpeciality(null);

        if (DocPatientSpeciality) {
          console.log("4444444444444");

          setDocWiseSpeciality(DocSpecWise?.SpecialityName);
          console.log("matching specialitywise ");

          setSpecialityName(null);
        } else {
          setDocWiseSpeciality(null); // Reset if no match
        }
      }

      // const PatientSpeciality = UserData?.Specialization && DoctorWorkbenchNavigation?.Specialization === SpecData?.Speciality_Id;

      // console.log("SpecData?.SpecialityName", SpecData?.SpecialityName);

      // setSpecialityName(null);
      // setDocWiseSpeciality(null);

      // if (PatientSpeciality) {
      //   setSpecialityName(SpecData?.SpecialityName);
      // } else if (DocPatientSpeciality) {
      //   setDocWiseSpeciality(DocSpecWise?.SpecialityName);
      // }
    }
  }, [
    UserData,
    DoctorWorkbenchNavigation,
    SpecialityData,
    SpecialityWise_DoctorWorkbenchNavigation,
  ]);

  // useEffect(() => {
  //   console.log("Effect triggered");

  //   const findSpeciality = (navigationKey) => {
  //     return SpecialityData?.find((p) => p?.Speciality_Id === navigationKey);
  //   };

  //   console.log(findSpeciality,'findSpeciality');

  //   let SpecData = findSpeciality(DoctorWorkbenchNavigation?.Specialization);
  //   let DocSpecWise = findSpeciality(SpecialityWise_DoctorWorkbenchNavigation?.Specialization);

  //   if (UserData?.username === "host" || UserData?.username === "admin") {
  //     setIsHost(true);

  //     setSpecialityName(SpecData?.SpecialityName || null);
  //     setDocWiseSpeciality(DocSpecWise?.SpecialityName || null);

  //   } else {
  //     setIsHost(false);

  //     const PatientSpeciality =
  //       UserData?.Specialization &&
  //       DoctorWorkbenchNavigation?.Specialization === SpecData?.Speciality_Id;
  //     const DocPatientSpeciality =
  //       UserData?.Specialization &&
  //       SpecialityWise_DoctorWorkbenchNavigation?.Specialization === DocSpecWise?.Speciality_Id;

  //     setSpecialityName(PatientSpeciality ? SpecData?.SpecialityName : null);
  //     setDocWiseSpeciality(DocPatientSpeciality ? DocSpecWise?.SpecialityName : null);
  //   }
  // }, [
  //   UserData,
  //   DoctorWorkbenchNavigation,
  //   SpecialityData,
  //   SpecialityWise_DoctorWorkbenchNavigation,
  // ]);

  return (
    <>
      <div className="Main_container_app">
        <div className="new-patient-registration-form">
          <div className="dctr_info_up_head">
            <div className="RegisFormcon ">
              <div className="dctr_info_up_head22">
                <img src={bgImg2} alt="Default Patient Photo" />

                <label>Profile</label>
              </div>
            </div>

            <div className="RegisFormcon_1">
              <div className="RegisForm_1 ">
                <label htmlFor="PatientID">
                  Patient ID <span>:</span>
                </label>
                <span className="dctr_wrbvh_pice" htmlFor="PatientID">
                  {SpecialityWise_DoctorWorkbenchNavigation?.PatientId ||
                    DoctorWorkbenchNavigation?.PatientId}
                </span>
              </div>
              <div className="RegisForm_1 ">
                <label htmlFor="PatientName">
                  Patient Name <span>:</span>{" "}
                </label>
                <span className="dctr_wrbvh_pice" htmlFor="PatientName">
                  {SpecialityWise_DoctorWorkbenchNavigation?.PatientName ||
                    DoctorWorkbenchNavigation?.PatientName}
                </span>
              </div>

              <div className="RegisForm_1 ">
                <label htmlFor="OpNo">
                  OP No <span>:</span>{" "}
                </label>
                <span className="dctr_wrbvh_pice" htmlFor="PatientName">
                  {SpecialityWise_DoctorWorkbenchNavigation?.RegistrationId ||
                    DoctorWorkbenchNavigation?.RegistrationId}
                </span>
              </div>
              <div className="RegisForm_1 ">
                <label htmlFor="PrimaryDoctor">
                  Primary Doctor <span>:</span>{" "}
                </label>
                <span className="dctr_wrbvh_pice" htmlFor="PatientName">
                  {SpecialityWise_DoctorWorkbenchNavigation?.DoctorName ||
                    DoctorWorkbenchNavigation?.DoctorName}
                </span>
              </div>

              <div className="RegisForm_1">
                <label htmlFor="AgeGender">
                  Age / Gender<span>:</span>{" "}
                </label>
                <span className="dctr_wrbvh_pice" id="AgeGender">
                  {SpecialityWise_DoctorWorkbenchNavigation?.Age ||
                    DoctorWorkbenchNavigation?.Age}{" "}
                  /{" "}
                  {SpecialityWise_DoctorWorkbenchNavigation?.Gender ||
                    DoctorWorkbenchNavigation?.Gender}
                </span>
              </div>
              <div className="RegisForm_1">
                <label htmlFor="PatientCategory">
                  Patient Category<span>:</span>{" "}
                </label>
                <span className="dctr_wrbvh_pice" id="PatientCategory">
                  {SpecialityWise_DoctorWorkbenchNavigation?.PatientCategory ||
                    DoctorWorkbenchNavigation?.PatientCategory}
                </span>
              </div>
              <div className="RegisForm_1 ">
                <label htmlFor="BloodGroup">
                  Blood Group <span>:</span>{" "}
                </label>
                <span className="dctr_wrbvh_pice" htmlFor="BloodGroup">
                  {SpecialityWise_DoctorWorkbenchNavigation?.BloodGroup ||
                    DoctorWorkbenchNavigation?.BloodGroup}
                </span>
              </div>
              <div className="RegisForm_1 ">
                <label htmlFor="Allergy">
                  Allergy <span>:</span>{" "}
                </label>
                <span className="dctr_wrbvh_pice" htmlFor="Gender">
                  {/* Check if AllergyDetails is an array and map through it */}
                  {Array.isArray(AllergyDetails) && AllergyDetails.length > 0
                    ? AllergyDetails.map((allergy) => allergy.Allergent).join(
                        ", "
                      )
                    : "No allergy details available"}
                </span>
              </div>
            </div>
          </div>

          <div className="new-patient-registration-form">
            <div className="new-navigation">
              <h2>
                <button
                  style={{ color: ActiveTab === "Vitals" ? "white" : "" }}
                  onClick={() => handleTabChange("Vitals")}
                >
                  Vitals
                </button>
                |
                <button
                  style={{ color: ActiveTab === "PastHistory" ? "white" : "" }}
                  onClick={() => handleTabChange("PastHistory")}
                >
                  Past History
                </button>
                |
                <button
                  style={{ color: ActiveTab === "Allergy" ? "white" : "" }}
                  onClick={() => handleTabChange("Allergy")}
                >
                  Allergy
                </button>
                |
                <button
                  style={{
                    color: ActiveTab === "GeneralEvaluation" ? "white" : "",
                  }}
                  onClick={() => handleTabChange("GeneralEvaluation")}
                >
                  GeneralEvaluation
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
                  style={{ color: ActiveTab === "Prescription" ? "white" : "" }}
                  onClick={() => handleTabChange("Prescription")}
                >
                  Prescription
                </button>
                
                {/* <>
                {isHost && (
                  <>
                    <button
                      style={{ color: ActiveTab === "Neurology" ? "white" : "" }}
                      onClick={() => handleTabChange("Neurology")}
                    >
                      Neurology Form
                    </button>
                    |
                    <button
                      style={{ color: ActiveTab === "OP_Sheet" ? "white" : "" }}
                      onClick={() => handleTabChange("OP_Sheet")}
                    >
                      Neuro Surgery
                    </button>
                    |
                    <button
                      style={{ color: ActiveTab === "Opthalmology" ? "white" : "" }}
                      onClick={() => handleTabChange("Opthalmology")}
                    >
                      Opthalmology
                    </button>
                    |
                    <button
                      style={{ color: ActiveTab === "IFCard" ? "white" : "" }}
                      onClick={() => handleTabChange("IFCard")}
                    >
                      IFCard
                    </button>
                    |
                    <button
                      style={{ color: ActiveTab === "Gynecology" ? "white" : "" }}
                      onClick={() => handleTabChange("Gynecology")}
                    >
                      Gynecology
                    </button>
                    |
                    <button
                      style={{ color: ActiveTab === "AncCard" ? "white" : "" }}
                      onClick={() => handleTabChange("AncCard")}
                    >
                      ANCCard
                    </button>
                    |
                  </>
                )}
                </> */}
                {!isHost && 
                  (specialityName === "OPTHALMOLOGY" ||
                    DocWiseSpeciality === "OPTHALMOLOGY") && (
                    <>
                    |
                      <button
                        style={{
                          color: ActiveTab === "Opthalmology" ? "white" : "",
                        }}
                        onClick={() => handleTabChange("Opthalmology")}
                      >
                        Opthalmology
                      </button>
                      |
                    </>
                  )}
                {!isHost &&
                  (specialityName === "NEUROLOGY" ||
                    DocWiseSpeciality === "NEUROLOGY") && (
                    <>
                      <button
                        style={{
                          color: ActiveTab === "Neurology" ? "white" : "",
                        }}
                        onClick={() => handleTabChange("Neurology")}
                      >
                        Neurology Form
                      </button>
                      |
                      <button
                        style={{
                          color: ActiveTab === "OP_Sheet" ? "white" : "",
                        }}
                        onClick={() => handleTabChange("OP_Sheet")}
                      >
                        Neuro Surgery
                      </button>
                      |
                    </>
                  )}
                {!isHost &&
                  (specialityName === "GYNECOLOGY" ||
                    DocWiseSpeciality === "GYNECOLOGY") && (
                    <>
                      <button
                        style={{ color: ActiveTab === "IFCard" ? "white" : "" }}
                        onClick={() => handleTabChange("IFCard")}
                      >
                        IFCard
                      </button>
                      |
                      <button
                        style={{
                          color: ActiveTab === "Gynecology" ? "white" : "",
                        }}
                        onClick={() => handleTabChange("Gynecology")}
                      >
                        Gynecology
                      </button>
                      |
                      <button
                        style={{
                          color: ActiveTab === "AncCard" ? "white" : "",
                        }}
                        onClick={() => handleTabChange("AncCard")}
                      >
                        ANCCard
                      </button>
                      |
                    </>
                  )}
               
                {isHost && specialityName !== "GENERAL MEDICINE" && (
                  <>
                    <div className="Lab_dropdown">
                      |
                      <button
                        style={{
                          color:
                            ActiveTab === "Neurology" ||
                            ActiveTab === "Gynecology" ||
                            ActiveTab === "AncCard" ||
                            ActiveTab === "Opthalmology" ||
                            ActiveTab === "IFCard"
                              ? "white"
                              : "",
                        }}
                        className="Lab_button"
                      >
                        Forms
                      </button>
                      <div className="Lab_dropdown_content">
                        <>
                          {/* Neurology */}
                          {isHost &&
                            (DocWiseSpeciality === "NEUROLOGY" ||
                              specialityName === "NEUROLOGY") && (
                              <>
                                <button
                                  style={{
                                    color:
                                      ActiveTab === "Neurology" ? "white" : "",
                                  }}
                                  onClick={() => handleTabChange("Neurology")}
                                >
                                  Neurology Form
                                </button>

                                <button
                                  style={{
                                    color:
                                      ActiveTab === "OP_Sheet" ? "white" : "",
                                  }}
                                  onClick={() => handleTabChange("OP_Sheet")}
                                >
                                  Neuro Surgery
                                </button>
                              </>
                            )}

                          {/* Opthalmology */}
                          {isHost &&
                            (DocWiseSpeciality === "OPTHALMOLOGY" ||
                              specialityName === "OPTHALMOLOGY") && (
                              <>
                                <button
                                  style={{
                                    color:
                                      ActiveTab === "Opthalmology"
                                        ? "white"
                                        : "",
                                  }}
                                  onClick={() =>
                                    handleTabChange("Opthalmology")
                                  }
                                >
                                  Opthalmology
                                </button>
                              </>
                            )}

                          {/* Gynecology */}
                          {isHost &&
                            (DocWiseSpeciality === "GYNECOLOGY" ||
                              specialityName === "GYNECOLOGY") && (
                              <>
                                <button
                                  style={{
                                    color:
                                      ActiveTab === "IFCard" ? "white" : "",
                                  }}
                                  onClick={() => handleTabChange("IFCard")}
                                >
                                  IFCard
                                </button>

                                <button
                                  style={{
                                    color:
                                      ActiveTab === "Gynecology" ? "white" : "",
                                  }}
                                  onClick={() => handleTabChange("Gynecology")}
                                >
                                  Gynecology
                                </button>

                                <button
                                  style={{
                                    color:
                                      ActiveTab === "AncCard" ? "white" : "",
                                  }}
                                  onClick={() => handleTabChange("AncCard")}
                                >
                                  ANCCard
                                </button>
                              </>
                            )}
                        </>
                      </div>
                    </div>
                  </>
                )}
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
                        style={{ color: ActiveTab === "Vitals" ? "white" : "" }}
                        onClick={() => handleTabChange("Vitals")}
                      >
                        Vitals
                      </button>
                      |
                      <button
                        style={{
                          color: ActiveTab === "PastHistory" ? "white" : "",
                        }}
                        onClick={() => handleTabChange("PastHistory")}
                      >
                        Past History
                      </button>
                      |
                      <button
                        style={{
                          color: ActiveTab === "Allergy" ? "white" : "",
                        }}
                        onClick={() => handleTabChange("Allergy")}
                      >
                        Allergy
                      </button>
                      |
                      <button
                        style={{
                          color:
                            ActiveTab === "GeneralEvaluation" ? "white" : "",
                        }}
                        onClick={() => handleTabChange("GeneralEvaluation")}
                      >
                        GeneralEvaluation
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
                          color: ActiveTab === "Prescription" ? "white" : "",
                        }}
                        onClick={() => handleTabChange("Prescription")}
                      >
                        Prescription
                      </button>
                      |
                      {/* <>
                      {isHost && (
                        <>
                          <button
                            style={{ color: ActiveTab === "Neurology" ? "white" : "" }}
                            onClick={() => handleTabChange("Neurology")}
                          >
                            Neurology Form
                          </button>
                          |
                          <button
                            style={{ color: ActiveTab === "OP_Sheet" ? "white" : "" }}
                            onClick={() => handleTabChange("OP_Sheet")}
                          >
                            Neuro Surgery
                          </button>
                          |
                          <button
                            style={{ color: ActiveTab === "Opthalmology" ? "white" : "" }}
                            onClick={() => handleTabChange("Opthalmology")}
                          >
                            Opthalmology
                          </button>
                          |
                          <button
                            style={{ color: ActiveTab === "IFCard" ? "white" : "" }}
                            onClick={() => handleTabChange("IFCard")}
                          >
                            IFCard
                          </button>
                          |
                          <button
                            style={{ color: ActiveTab === "Gynecology" ? "white" : "" }}
                            onClick={() => handleTabChange("Gynecology")}
                          >
                            Gynecology
                          </button>
                          |
                          <button
                            style={{ color: ActiveTab === "AncCard" ? "white" : "" }}
                            onClick={() => handleTabChange("AncCard")}
                          >
                            ANCCard
                          </button>
                          |
                        </>
                      )}
                      </> */}
                      {!isHost && specialityName === "OPTHALMOLOGY" && (
                        <>
                          <button
                            style={{
                              color:
                                ActiveTab === "Opthalmology" ? "white" : "",
                            }}
                            onClick={() => handleTabChange("Opthalmology")}
                          >
                            Opthalmology
                          </button>
                          |
                        </>
                      )}
                      {!isHost && specialityName === "NEUROLOGY" && (
                        <>
                          <button
                            style={{
                              color: ActiveTab === "Neurology" ? "white" : "",
                            }}
                            onClick={() => handleTabChange("Neurology")}
                          >
                            Neurology Form
                          </button>
                          |
                          <button
                            style={{
                              color: ActiveTab === "OP_Sheet" ? "white" : "",
                            }}
                            onClick={() => handleTabChange("OP_Sheet")}
                          >
                            Neuro Surgery
                          </button>
                          |
                        </>
                      )}
                      {!isHost && specialityName === "GYNECOLOGY" && (
                        <>
                          <button
                            style={{
                              color: ActiveTab === "IFCard" ? "white" : "",
                            }}
                            onClick={() => handleTabChange("IFCard")}
                          >
                            IFCard
                          </button>
                          |
                          <button
                            style={{
                              color: ActiveTab === "Gynecology" ? "white" : "",
                            }}
                            onClick={() => handleTabChange("Gynecology")}
                          >
                            Gynecology
                          </button>
                          |
                          <button
                            style={{
                              color: ActiveTab === "AncCard" ? "white" : "",
                            }}
                            onClick={() => handleTabChange("AncCard")}
                          >
                            ANCCard
                          </button>
                          |
                        </>
                      )}
                      <div className="Lab_dropdown">
                        |
                        <button
                          style={{
                            color:
                              ActiveTab === "Neurology" ||
                              ActiveTab === "Gynecology" ||
                              ActiveTab === "AncCard" ||
                              ActiveTab === "Opthalmology" ||
                              ActiveTab === "IFCard"
                                ? "white"
                                : "",
                          }}
                          className="Lab_button"
                        >
                          Forms
                        </button>
                        <div className="Lab_dropdown_content">
                          <>
                            {/* Neurology */}
                            {isHost &&
                              (DocWiseSpeciality === "NEUROLOGY" ||
                                specialityName === "NEUROLOGY") && (
                                <>
                                  <button
                                    style={{
                                      color:
                                        ActiveTab === "Neurology"
                                          ? "white"
                                          : "",
                                    }}
                                    onClick={() => handleTabChange("Neurology")}
                                  >
                                    Neurology Form
                                  </button>

                                  <button
                                    style={{
                                      color:
                                        ActiveTab === "OP_Sheet" ? "white" : "",
                                    }}
                                    onClick={() => handleTabChange("OP_Sheet")}
                                  >
                                    Neuro Surgery
                                  </button>
                                </>
                              )}

                            {/* Opthalmology */}
                            {isHost &&
                              (DocWiseSpeciality === "OPTHALMOLOGY" ||
                                specialityName === "OPTHALMOLOGY") && (
                                <>
                                  <button
                                    style={{
                                      color:
                                        ActiveTab === "Opthalmology"
                                          ? "white"
                                          : "",
                                    }}
                                    onClick={() =>
                                      handleTabChange("Opthalmology")
                                    }
                                  >
                                    Opthalmology
                                  </button>
                                </>
                              )}

                            {/* Gynecology */}
                            {isHost &&
                              (DocWiseSpeciality === "GYNECOLOGY" ||
                                specialityName === "GYNECOLOGY") && (
                                <>
                                  <button
                                    style={{
                                      color:
                                        ActiveTab === "IFCard" ? "white" : "",
                                    }}
                                    onClick={() => handleTabChange("IFCard")}
                                  >
                                    IFCard
                                  </button>

                                  <button
                                    style={{
                                      color:
                                        ActiveTab === "Gynecology"
                                          ? "white"
                                          : "",
                                    }}
                                    onClick={() =>
                                      handleTabChange("Gynecology")
                                    }
                                  >
                                    Gynecology
                                  </button>

                                  <button
                                    style={{
                                      color:
                                        ActiveTab === "AncCard" ? "white" : "",
                                    }}
                                    onClick={() => handleTabChange("AncCard")}
                                  >
                                    ANCCard
                                  </button>
                                </>
                              )}
                          </>
                        </div>
                      </div>
                    </h2>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
        <Suspense fallback={<div>Loading...</div>}>
          {ActiveTab === "Vitals" && <Vitals />}
          {ActiveTab === "Allergy" && <Allergy />}
          {ActiveTab === "PastHistory" && <PastHistory />}
          {/* {ActiveTab === "Treatment" && <Treatment />} */}
          {ActiveTab === "Prescription" && <Prescription />}
          {ActiveTab === "NewProcedure" && <NewProcedure />}

          {ActiveTab === "Neurology" && <Neurology />}
          {ActiveTab === "IFCard" && <IFCard />}
          {ActiveTab === "Gynecology" && <Gynecology />}
          {ActiveTab === "AncCard" && <AncCard />}
          {ActiveTab === "OP_Sheet" && <OP_Sheet />}

          {ActiveTab === "GeneralEvaluation" && <GeneralEvaluation />}
          {ActiveTab === "Opthalmology" && <Opthalmology />}
          {ActiveTab === "Lab_Test" && <LabTest />}
          {ActiveTab === "Radiology_Test" && <RadiologyTest />}

          {/* {ActiveTab === "Refer_Doctor" && <ReferaDoctor />}
          {ActiveTab === "FollowUp" && <FollowUp />}
          {ActiveTab === "OtRequest" && <OtRequest />}
          {ActiveTab === "OP_IP_Connect" && <OpIpconnect />} */}
        </Suspense>
      </div>
    </>
  );
};

export default DoctorWorkbenchNavigation;
