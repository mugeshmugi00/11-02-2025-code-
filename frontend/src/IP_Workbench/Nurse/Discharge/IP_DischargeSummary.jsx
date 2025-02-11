import React, { useState, useEffect, useRef, useCallback } from "react";
import { useDispatch, useSelector } from "react-redux";
import axios from "axios";
import "./IP_DischargeSummary.css";
import SignatureCanvas from "react-signature-canvas";
import { useReactToPrint } from "react-to-print";

import ReactGrid from "../../../OtherComponent/ReactGrid/ReactGrid";
import ToastAlert from "../../../OtherComponent/ToastContainer/ToastAlert";

const PrintContent = React.forwardRef((props, ref) => {
  return (
    <div ref={ref} id="reactprintcontent">
      {props.children}
    </div>
  );
});

const IP_DischargeSummary = () => {
  const printRef = useRef();
  const [pages, setPages] = useState([]);
  const [totalPages, setTotalPages] = useState(0);
  const dispatch = useDispatch();

  const userRecord = useSelector((state) => state.userRecord?.UserData);

  const UrlLink = useSelector((state) => state.userRecord?.UrlLink);
  const IP_DoctorWorkbenchNavigation = useSelector(
    (state) => state.Frontoffice?.IP_DoctorWorkbenchNavigation
  );

  console.log(IP_DoctorWorkbenchNavigation, "IP_DoctorWorkbenchNavigation");

  // const RadiologyWorkbenchNavigation = useSelector(state => state.Frontoffice?.RadiologyWorkbenchNavigation);
  const RadiologyWorkbenchNavigation = useSelector(
    (state) => state.Frontoffice?.RadiologyWorkbenchNavigation
  );

  console.log(RadiologyWorkbenchNavigation, "RadiologyWorkbenchNavigation");

  const pagewidth = useSelector((state) => state.userRecord?.pagewidth);

  const [AssesmentData, setAssesmentData] = useState([]);
  const [AllergyData, setAllergyData] = useState([]);
  const [HospitalClinicDetails, setHospitalClinicDetails] = useState([]);
  const [Prescription, setPrescription] = useState([]);

  const [InchargeDetailsData, setInchargeDetailsData] = useState([]);

  console.log(InchargeDetailsData, "InchargeDetailsData");

  const [PrescriptionData, setPrescriptionData] = useState([]);
  console.log(PrescriptionData, "PrescriptionData");

  const [DamaData, setDamaData] = useState([]);
  const [DoctorData, setDoctorData] = useState([]);
  const [RadiologyData, setRadiologyData] = useState([]);
  const [LabData, setLabData] = useState([]);
  const [DischargeSummarySavedData, setDischargeSummarySavedData] = useState(
    []
  );

  console.log(DischargeSummarySavedData, "DischargeSummarySavedData");

  const [currentDate, setCurrentDate] = useState("");

  const [finalDiagnosis, setFinalDiagnosis] = useState("");
  const [presentingComplaints, setPresentingComplaints] = useState("");
  const [PastMedicalHistory, setPastMedicalHistory] = useState("");
  const [AllergyHistory, setAllergyHistory] = useState("");
  const [vitals, setVitals] = useState("");
  const [Radiology, setRadiology] = useState("");
  const [dischargeNotes, setDischargeNotes] = useState("");
  const [Referdoctor, setReferdoctor] = useState("");
  const [ConditionOnDischarge, setConditionOnDischarge] = useState("");
  const [PrescriptionSummary, setPrescriptionSummary] = useState("");
  const [Followup, setFollowup] = useState({
    Followupid: "",
    NoOfDays: "",
    TimeInterval: "days",
    Date: "",
  });
  const [DietAdvice, setDietAdvice] = useState("");
  const [Emergency, setEmergency] = useState("");
  const [AdviceOnDischarge, setAdviceOnDischarge] = useState("");
  const [doctorSchedule, setDoctorSchedule] = useState("");
  const [HospitalDetails, setHospitalDetails] = useState("");
  const [treatmentGiven, setTreatmentGiven] = useState("");
  const [Lab, setLab] = useState("");
  const [showDetails, setShowDetails] = useState(false);
  const [ShowPrintBtn, setShowPrintBtn] = useState(false);
  const componentRef = useRef();
  const [isPrintButtonVisible, setIsPrintButtonVisible] = useState(true);

  const Finddays = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
  ];

  const handleFollowupInputChange = (event) => {
    const { name, value } = event.target;

    if (name === "NoOfDays") {
      const numberOfDays = parseInt(value, 10);
      const timeInterval = Followup.TimeInterval;

      let totalDaysToAdd = 0;

      if (timeInterval === "days") {
        totalDaysToAdd = numberOfDays || 0;
      } else if (timeInterval === "weeks") {
        totalDaysToAdd = (numberOfDays || 0) * 7;
      } else if (timeInterval === "months") {
        const currentDate = new Date();
        const newDate = new Date(
          currentDate.setMonth(currentDate.getMonth() + (numberOfDays || 0))
        );
        const formattedDate = newDate.toISOString().split("T")[0];

        setFollowup((prevData) => ({
          ...prevData,
          NoOfDays: value,
          Date: formattedDate,
          TimeInterval: timeInterval, // Ensure the interval is stored
        }));
        return;
      }

      const newDate = new Date();
      newDate.setDate(newDate.getDate() + totalDaysToAdd);
      const formattedDate = newDate.toISOString().split("T")[0];

      setFollowup((prevData) => ({
        ...prevData,
        NoOfDays: value,
        Date: formattedDate,
        TimeInterval: timeInterval, // Ensure the interval is stored
      }));
    } else if (name === "TimeInterval") {
      const currentNoOfDays = parseInt(Followup.NoOfDays, 10) || 0;
      let totalDaysToAdd = 0;

      if (value === "days") {
        totalDaysToAdd = currentNoOfDays;
      } else if (value === "weeks") {
        totalDaysToAdd = currentNoOfDays * 7;
      } else if (value === "months") {
        const currentDate = new Date();
        const newDate = new Date(
          currentDate.setMonth(currentDate.getMonth() + currentNoOfDays)
        );
        const formattedDate = newDate.toISOString().split("T")[0];

        setFollowup((prevData) => ({
          ...prevData,
          TimeInterval: value,
          Date: formattedDate,
        }));
        return;
      }

      const newDate = new Date();
      newDate.setDate(newDate.getDate() + totalDaysToAdd);
      const formattedDate = newDate.toISOString().split("T")[0];

      setFollowup((prevData) => ({
        ...prevData,
        TimeInterval: value,
        Date: formattedDate,
      }));
    } else if (name === "Date") {
      const selectedDate = new Date(value);
      const currentDate = new Date();
      const timeDiff = selectedDate - currentDate;

      if (timeDiff >= 0) {
        const monthsDiff =
          (selectedDate.getFullYear() - currentDate.getFullYear()) * 12 +
          (selectedDate.getMonth() - currentDate.getMonth());
        const daysDiff = Math.ceil(timeDiff / (1000 * 60 * 60 * 24));
        let timeInterval = "days";

        if (monthsDiff > 0) {
          timeInterval = "months";
          setFollowup((prevData) => ({
            ...prevData,
            NoOfDays: monthsDiff.toString(),
            Date: value,
            TimeInterval: timeInterval,
          }));
        } else if (daysDiff >= 7) {
          timeInterval = "weeks";
          setFollowup((prevData) => ({
            ...prevData,
            NoOfDays: Math.ceil(daysDiff / 7).toString(),
            Date: value,
            TimeInterval: timeInterval,
          }));
        } else {
          timeInterval = "days";
          setFollowup((prevData) => ({
            ...prevData,
            NoOfDays: daysDiff.toString(),
            Date: value,
            TimeInterval: timeInterval,
          }));
        }
      } else {
        setFollowup((prevData) => ({
          ...prevData,
          NoOfDays: "",
          Date: value,
          TimeInterval: "", // Reset TimeInterval if the date is in the past
        }));
      }
    } else {
      setFollowup((prevData) => ({
        ...prevData,
        [name]: value,
      }));
    }
  };

  useEffect(() => {
    // Get the current date
    const today = new Date();

    // Format the date (e.g., 'MM/DD/YYYY' or 'DD/MM/YYYY')
    const formattedDate = `${
      today.getMonth() + 1
    }/${today.getDate()}/${today.getFullYear()}`;

    // Set the formatted date to state
    setCurrentDate(formattedDate);
  }, []);

  const [PatientDischargeData, setPatientDischargeData] = useState([]);
  console.log(PatientDischargeData, "PatientDischargeData");
  const [expanded, setExpanded] = useState(false);

  const handleAccordionClick = () => {
    setExpanded(!expanded); // Toggle the expanded state when accordion is clicked
  };

  const signatureRef = useRef(null);

  const clearSignature = () => {
    signatureRef.current.clear();
  };

  const saveSignature = () => {
    console.log("Signature saved");
  };

  const fetchDischargeSummary = useCallback(() => {
    const RegistrationId = IP_DoctorWorkbenchNavigation?.RegistrationId;
    const departmentType = IP_DoctorWorkbenchNavigation?.RequestType;
    const doctorId = IP_DoctorWorkbenchNavigation?.DoctorId;
    const PatientID = IP_DoctorWorkbenchNavigation?.PatientId;
    const VisitID = IP_DoctorWorkbenchNavigation?.RegistrationId;

    if (RegistrationId) {
      // Check if data exists for the given RegistrationId
      axios
        .get(`${UrlLink}Ip_Workbench/IP_DischargeSummary_Details_Link`, {
          params: {
            RegistrationId,
            DepartmentType: departmentType,
          },
        })
        .then((res) => {
          if (res.data && res.data.length > 0) {
            // If data exists, set the state with backend data
            const dischargeDetails = res.data[0]; // Assuming you want the first result
            setDischargeSummarySavedData(dischargeDetails);
            console.log("Discharge Details from backend:", dischargeDetails);
            setShowPrintBtn(true);
            setFinalDiagnosis(dischargeDetails.FinalDiagnosis);
            setPresentingComplaints(dischargeDetails.PresentingComplaints);
            setPastMedicalHistory(dischargeDetails.PastMedicalHistory);
            setVitals(dischargeDetails.Vitals);
            setTreatmentGiven(dischargeDetails.DischargeNotes);
            setAllergyHistory(dischargeDetails.AllergyHistory);
            setDischargeNotes(dischargeDetails.DischargeNotes);
            setReferdoctor(dischargeDetails.Referdoctor);
            setConditionOnDischarge(dischargeDetails.ConditionOnDischarge);
            setDietAdvice(dischargeDetails.DietAdvice);
            setEmergency(dischargeDetails.Emergency);
            setAdviceOnDischarge(dischargeDetails.AdviceOnDischarge);
            setDoctorSchedule(dischargeDetails.DoctorSchedule);
            // setPrescriptionSummary(dischargeDetails.PrescriptionSummary);
            setFollowup((prevFollowup) => ({
              ...prevFollowup,
              NoOfDays: dischargeDetails.NoOfDays,
              TimeInterval: dischargeDetails.TimeInterval,
              Date: dischargeDetails.Date,
            }));
          } else {
            // If no data exists, fetch assessment details
            // fetchAssessmentDetails(RegistrationId, departmentType);
            // fetchAllergyDetails(RegistrationId, departmentType);
            // fetchProgressNotesDetails(RegistrationId, departmentType);
            // fetchDamaDetails(RegistrationId, departmentType);
            // fetchInchargeAndReferDocDetails(RegistrationId, departmentType);
            // fetchDoctorSchedule(Doctor);

            fetchAdditionalData(
              RegistrationId,
              departmentType,
              doctorId,
              PatientID,
              VisitID
            );
          }
        })
        .catch((err) => {
          console.log("Error fetching discharge details:", err);
        });
    }
  }, [UrlLink, IP_DoctorWorkbenchNavigation]);

  const fetchAdditionalData = (
    RegistrationId,
    departmentType,
    doctorId,
    PatientID,
    VisitID
  ) => {
    fetchAssessmentDetails(RegistrationId, departmentType);
    fetchAllergyDetails(RegistrationId, departmentType);
    fetchProgressNotesDetails(RegistrationId, departmentType);
    fetchDamaDetails(RegistrationId, departmentType);
    fetchInchargeAndReferDocDetails(RegistrationId, departmentType);
    fetchDoctorSchedule(doctorId);
    fetchPrescriptionData(PatientID, VisitID);
  };

  const fetchAssessmentDetails = (RegistrationId, departmentType) => {
    axios
      .get(`${UrlLink}Ip_Workbench/IP_Assesment_details_Link`, {
        params: {
          RegistrationId,
          DepartmentType: departmentType,
        },
      })
      .then((res) => {
        const ress = res.data;
        console.log("Assessment Data:", ress);
        setAssesmentData(ress);
      })
      .catch((err) => {
        console.log("Error fetching assessment details:", err);
      });
  };

  const fetchAllergyDetails = (RegistrationId, departmentType) => {
    axios
      .get(`${UrlLink}Ip_Workbench/IP_Allergy_Details_Link`, {
        params: {
          RegistrationId,
          DepartmentType: departmentType,
        },
      })
      .then((res) => {
        const ress = res.data;
        console.log("Assessment Data:", ress);
        setAllergyData(ress);
      })
      .catch((err) => {
        console.log("Error fetching assessment details:", err);
      });
  };

  const fetchProgressNotesDetails = (RegistrationId, departmentType) => {
    axios
      .get(`${UrlLink}Ip_Workbench/IP_ProgressNotes_Details_Link`, {
        params: {
          RegistrationId,
          DepartmentType: departmentType,
        },
      })
      .then((res) => {
        console.log(res.data, "Prescription");
        setPrescriptionData(res.data);
      })
      .catch((err) => {
        console.log("Error fetching prescription details:", err);
      });
  };

  const fetchDamaDetails = (RegistrationId, departmentType) => {
    axios
      .get(`${UrlLink}Ip_Workbench/IP_Dama_Details_Link`, {
        params: {
          RegistrationId,
          DepartmentType: departmentType,
          Type: "Nurse",
        },
      })
      .then((res) => {
        setDamaData(res.data);
      })
      .catch((err) => {
        console.log("Error fetching DAMA details:", err);
      });
  };

  const fetchInchargeAndReferDocDetails = (RegistrationId, departmentType) => {
    axios
      .get(`${UrlLink}Ip_Workbench/IP_InchargeAndRefer_Details_Link`, {
        params: {
          RegistrationId,
          DepartmentType: departmentType,
          Type: "Refer",
        },
      })
      .then((res) => {
        setInchargeDetailsData(res.data || []);
      })
      .catch((err) => {
        console.log("Error fetching Refer a doctor details:", err);
      });
  };

  const fetchDoctorSchedule = (doctorId) => {
    if (!doctorId) return;

    axios
      .get(`${UrlLink}Masters/get_DoctorSchedule_details`, {
        params: { DoctorId: doctorId },
      })
      .then((response) => {
        const schedule = response.data.DoctorScheduleForm.Schedule || [];
        console.log(schedule, "Doctor details");

        // Update raw data
        setDoctorData(schedule);

        // Format and update schedule for display
        const formattedSchedule = schedule
          .filter((item) => item.working === "yes") // Filter for working days
          .map(
            (item) =>
              `${item.days}: ${item.starting_time} to ${item.ending_time}`
          ) // Format schedule
          .join("\n"); // Join for display

        setDoctorSchedule(formattedSchedule);
      })
      .catch((error) => {
        console.error("Error fetching doctor schedule:", error);
      });
  };

  const fetchPrescriptionData = (PatientID, VisitID) => {
    axios
      .get(`${UrlLink}DrugAdminstrations/get_prescription_forIP_Discharge`, {
        params: {
          PatientID,
          VisitID,
        },
      })
      .then((res) => {
        console.log("Prescription Data:", res.data);
        if (Array.isArray(res.data) && res.data.length > 0) {
          setPrescription(res.data); // Assuming `setPrescription` is defined elsewhere
        }
      })
      .catch((err) => {
        console.error("Error fetching prescription data:", err);
      });
  };

  useEffect(() => {
    axios
      .get(
        `${UrlLink}DrugAdminstrations/get_prescription_forIP_Discharge?PatientID=${IP_DoctorWorkbenchNavigation?.PatientId}&VisitID=${IP_DoctorWorkbenchNavigation.RegistrationId}`
      )
      .then((res) => {
        console.log("111111111", res.data);

        setPrescription(res.data);
      })
      .catch((err) => {
        console.error(err);
      });
  }, [UrlLink, IP_DoctorWorkbenchNavigation]);

  useEffect(() => {
    axios
      .get(`${UrlLink}Masters/Clinic_Detials_link`)
      .then((res) => {
        setHospitalClinicDetails(res.data);
      })
      .catch((err) => {
        console.error(err);
      });
  }, [UrlLink, IP_DoctorWorkbenchNavigation]);

  const handleDiagnosisChange = (event) => {
    setFinalDiagnosis(event.target.value);
    adjustHeight(event);
  };

  useEffect(() => {
    if (AssesmentData.length > 0) {
      const latestFinalDiagnosis =
        AssesmentData[AssesmentData.length - 1].FinalDiagnosis;
      setFinalDiagnosis(latestFinalDiagnosis);

      const latestAssessment = AssesmentData[AssesmentData.length - 1];

      console.log(latestAssessment, "latestAssessment");

      // Set presenting complaints
      const presentingComplaintsData =
        `PresentingComplaints : ${latestAssessment.PresentingComplaints}  ,  ` +
        `DetailsPresentingComplaints : ${latestAssessment.DetailsPresentingComplaints}`;
      // ` ${latestAssessment.HistoryOf}`
      console.log("presentingComplaintsData", presentingComplaintsData);

      setPresentingComplaints(presentingComplaintsData);

      const medicalHistoryArray =
        latestAssessment.MedicalHistoryCheckbox.split(",");
      const surgicalHistoryArray =
        latestAssessment.SurgicalHistoryCheckbox.split(",");
      const socialHistoryArray =
        latestAssessment.SocialHistoryCheckbox.split(",");
      const familyHistoryArray =
        latestAssessment.FamilyHistoryCheckbox.split(",");

      const pastmedicalhistory = `
      Medical History: ${medicalHistoryArray.join(", ")}
      Surgical History: ${surgicalHistoryArray.join(", ")}
      Social History: ${socialHistoryArray.join(", ")}
      Family History: ${familyHistoryArray.join(", ")}
      `;

      // Set the state
      setPastMedicalHistory(pastmedicalhistory);

      // Log the value
      console.log(pastmedicalhistory, "PastMedicalHistory");

      // Set vitals
      const vitalsData =
        `Temperature: ${latestAssessment.Temperature}  ` +
        `PulseRate: ${latestAssessment.PulseRate}  ` +
        `SPO2: ${latestAssessment.SPO2}  ` +
        `HeartRate: ${latestAssessment.HeartRate}  ` +
        `RR: ${latestAssessment.RR}  ` +
        `BP: ${latestAssessment.BP}  ` +
        `Height: ${latestAssessment.Height}  ` +
        `Weight: ${latestAssessment.Weight}  ` +
        `BMI: ${latestAssessment.BMI}  ` +
        `WC: ${latestAssessment.WC}  ` +
        `HC: ${latestAssessment.HC}  ` +
        `BSL: ${latestAssessment.BSL}` +
        `Cvs: ${latestAssessment.Cvs}` +
        `Pupil: ${latestAssessment.Pupil}` +
        `Ul Rt: ${latestAssessment.UlRt}, Ul Lt: ${latestAssessment.UlLt}, ` +
        `Ll Rt: ${latestAssessment.LlRt}, Ll Lt: ${latestAssessment.LlLt}, ` +
        `Rt: ${latestAssessment.Rt}, Lt: ${latestAssessment.Lt} ` +
        `Rs: ${latestAssessment.Rs} ` +
        `Pa: ${latestAssessment.Pa} ` +
        `Cns: ${latestAssessment.Cns}`;
      setVitals(vitalsData);

      // Set treatment given
      setTreatmentGiven(latestAssessment.TreatmentGiven);
    }
  }, [AssesmentData]);

  useEffect(() => {
    if (AllergyData.length > 0) {
      // Format each allergy item with Allergent and AllergyType
      const formattedAllergyList = AllergyData.map(
        (item) =>
          `Allergent: ${item.Allergent} AllergyType: ${item.AllergyType}`
      );

      setAllergyHistory(formattedAllergyList.join("\n"));
    } else {
      setAllergyHistory("No allergies recorded.");
    }
  }, [AllergyData]);

  useEffect(() => {
    if (InchargeDetailsData.length > 0) {
      const referDoctorList = InchargeDetailsData.map(
        (item) => `${item.DoctorName} (${item.Speciality})`
      ).join("\n\n");
      setReferdoctor(referDoctorList);
    }
  }, [InchargeDetailsData]);

  useEffect(() => {
    let combinedNotes = "";

    // Get the last element from DamaData if available
    if (DamaData.length > 0) {
      const lastDama = DamaData[DamaData.length - 1];
      const damaNotes = `Reasons for DAMA: ${lastDama.Reasons}\n\n`;
      combinedNotes += `${damaNotes}`;
    }

    // Get the last element from PrescriptionData if available
    if (PrescriptionData.length > 0) {
      const lastPrescription = PrescriptionData[PrescriptionData.length - 1];
      const notes = `
      ProgressNotes: ${lastPrescription.ProgressNotes}
      TreatmentNotes: ${lastPrescription.TreatmentNotes}`;
      combinedNotes += notes;
    }

    setDischargeNotes(combinedNotes);
  }, [PrescriptionData, DamaData]);

  useEffect(() => {
    if (HospitalClinicDetails.length > 0) {
      const HospitalNo = HospitalClinicDetails.map((item) => item.PhoneNo);
      setHospitalDetails(HospitalNo);
    }
  }, [HospitalClinicDetails]);

  // useEffect(() => {
  //   if (Prescription.length > 0) {
  //     const summary = Prescription.map((item) => ({
  //       DrugName: item.GenericName,
  //       Strength: item.Strength,
  //       Frequency: item.Frequency,
  //       Route: item.Route,
  //       MealRelation: item.FrequencyMethod,
  //       Duration: item.Duration,
  //     }));
  //     setPrescriptionSummary(summary);
  //   }
  // }, [Prescription]);

  useEffect(() => {
    if (Prescription && Prescription.length > 0) {
      const summary =
        Array.isArray(Prescription) &&
        Prescription?.map((item) => ({
          DrugName: item.GenericName,
          Strength: item.Strength,
          Frequency: item.Frequency,
          Route: item.Route,
          MealRelation: item.FrequencyMethod, // Assuming 'FrequencyMethod' is MealRelation
          Duration: item.Duration,
        }));
      setPrescriptionSummary(summary); // This will hold the summary details
    }
  }, [Prescription]);

  useEffect(() => {
    if (RadiologyData.length > 0) {
      const allRadiologyDetails =
        Array.isArray(RadiologyData) &&
        RadiologyData.map((entry, index) => {
          return (
            `Date: ${entry.ReportDate || "N/A"}  ` +
            `Test Name: ${entry.TestName || "N/A"}  ` +
            `SubTest Name: ${entry.SubTestName || "N/A"}  ` +
            `Report: ${entry.Report || "No report available"}  \n`
          );
        }).join(""); // Combine all records into one string

      setRadiology(allRadiologyDetails); // Update state with the formatted details
    }
  }, [RadiologyData]);

  useEffect(() => {
    if (LabData.length > 0) {
      const LabReportDetails =
        Array.isArray(LabData) &&
        LabData.map((entry) => {
          return (
            `Date: ${entry.report_date || "N/A"}  ` +
            `Test Name: ${entry.test_name || "N/A"}  ` +
            `Value: ${entry.value || "N/A"}  \n`
          );
        }).join("");
      setLab(LabReportDetails);
    }
  }, [LabData]);

  const LabColumns = [
    {
      key: "id",
      name: "S.No",
      frozen: true,
    },

    {
      key: "test_name",
      name: "test_name",
      frozen: true,
    },

    {
      key: "value",
      name: "value",
    },

    {
      key: "report_date",
      name: "report_date",
    },
    {
      key: "report_time",
      name: "report_time",
    },
  ];

  const prepareTableData = () => {
    const tableData = {};
    const uniqueDates = new Set();

    LabData.forEach((item) => {
      const { report_date, test_name, value } = item;

      // Add the date to the uniqueDates set
      uniqueDates.add(report_date);

      // Initialize the row for test_name if it doesn't exist
      if (!tableData[test_name]) {
        tableData[test_name] = {};
      }

      // Assign the value for the test_name and report_date
      tableData[test_name][report_date] = value || "N/A"; // Set 'N/A' if value is empty
    });

    return { tableData, uniqueDates: Array.from(uniqueDates) };
  };

  // Prepare tableData and uniqueDates
  const { tableData, uniqueDates } = prepareTableData();

  useEffect(() => {
    axios
      .get(`${UrlLink}Ip_Workbench/IP_DischargeRequest_Details_Link`, {
        params: {
          RegistrationId: IP_DoctorWorkbenchNavigation?.RegistrationId,
        },
      })
      .then((res) => {
        const ress = res.data;
        console.log(ress, "resssss");
        setPatientDischargeData(ress);
      })
      .catch((err) => {
        console.log(err);
      });
  }, [UrlLink]);

  useEffect(() => {
    if (IP_DoctorWorkbenchNavigation?.pk) {
      // Ensure pk exists
      const params = {
        Register_Id: IP_DoctorWorkbenchNavigation.pk,
        RegisterType: "IP",
      };

      axios
        .get(`${UrlLink}OP/Radiology_Complete_Details_Link`, { params })
        .then((res) => {
          const ress = res.data;
          console.log("Response Data:", ress);
          setRadiologyData(ress); // Update state with the response
        })
        .catch((err) => {
          console.error("Error fetching data:", err);
        });
    }
  }, [UrlLink, IP_DoctorWorkbenchNavigation?.pk]); // Add pk to the dependency array

  useEffect(() => {
    // Define the params object to include RegistrationId
    const params = {
      Register_Id: IP_DoctorWorkbenchNavigation?.RegistrationId,
      RegisterType: "IP",
    };

    axios
      .get(`${UrlLink}OP/lab_report_details_view`, { params })
      .then((res) => {
        console.log("Response Lab Report:", res.data);

        // Extract report date
        const rawReportDate = res.data.lab_report_entry.report_date;
        const rawReportTime = res.data.lab_report_entry.report_time;
        const dateObject = new Date(rawReportDate);
        const formattedDate = dateObject.toISOString().split("T")[0]; // "YYYY-MM-DD"

        // Combine individual tests and favorite tests
        const combinedTests = [
          ...res.data.individual_tests.map((test, idx) => ({
            id: idx + 1, // Add index for S.No
            test_name: test.test_name,
            value: test.value || "N/A",
            report_date: formattedDate,
            report_time: rawReportTime,
          })),
          ...res.data.favourite_tests.map((fav, idx) => ({
            id: res.data.individual_tests.length + idx + 1, // Continue the S.No after individual tests
            test_name: fav.test_name,
            value: fav.value || "N/A",
            report_date: formattedDate,
            report_time: rawReportTime,
          })),
        ];

        // Update state with combined tests
        setLabData(combinedTests);

        console.log("Combined Tests:", combinedTests);
      })
      .catch((err) => {
        console.error("Error fetching lab report details:", err);
      });
  }, [UrlLink, IP_DoctorWorkbenchNavigation?.RegistrationId]);

  const handlePrint2 = useReactToPrint({
    content: () => componentRef.current,
    pageStyle: `
  //   @page {
  //     size: auto;
    
  
  //     @bottom-center {
  //       content: 'Page ' counter(page) ' of ' counter(pages);
  //       text-align: center;
  //       font-size: 10.5px;
  //       font-family: Arial, sans-serif;
  //       font-style: italic;
  //    margin-bottom: 100px !important;
    
  //     }
  //   }
  // `,
    onAfterPrint: async () => {
      // Additional action after printing, if needed
    },
  });

  const Submitalldata = () => {
    setIsPrintButtonVisible(false);
    setTimeout(() => {
      handlePrint2();
      setIsPrintButtonVisible(true); // Resetting print button visibility
    }, 800);


  };

  const handleClear = () => {
    setFinalDiagnosis("");
    setPresentingComplaints("");
    setPastMedicalHistory("");
    setAllergyHistory("");
    setVitals("");
    setRadiology("");
    setDischargeNotes("");
    setReferdoctor("");
    setConditionOnDischarge("");
    // setPrescriptionSummary('');
    // setFollowup('');
    setFollowup({
      NoOfDays: "",
      TimeInterval: "",
      Date: "",
    });
    setDietAdvice("");
    setEmergency("");
    setAdviceOnDischarge("");
    setDoctorSchedule("");
  };

  const handleDischargeSummarySubmit = () => {
    const RegistrationId = IP_DoctorWorkbenchNavigation?.RegistrationId;
    const DepartmentType = IP_DoctorWorkbenchNavigation?.RequestType;

    if (!RegistrationId) {
      dispatch({
        type: "toast",
        value: { message: "Registration ID is missing", type: "error" },
      });
      return;
    }

    console.log(IP_DoctorWorkbenchNavigation?.RegistrationId);

    const senddata = {
      finalDiagnosis,
      presentingComplaints,
      PastMedicalHistory,
      AllergyHistory,
      vitals,
      Radiology,
      dischargeNotes,
      Referdoctor,
      ConditionOnDischarge,
      PrescriptionSummary,
      ...Followup,
      DietAdvice,
      Emergency,
      AdviceOnDischarge,
      doctorSchedule,
      RegistrationId,
      DepartmentType,
      Createdby: userRecord?.username,
    };

    // Remove newline characters
    const cleanedData = Object.fromEntries(
      Object.entries(senddata).map(([key, value]) => [
        key,
        typeof value === "string" ? value.replace(/\n/g, " ") : value,
      ])
    );

    console.log("Cleaned data:", cleanedData);

    axios
      .post(
        `${UrlLink}Ip_Workbench/IP_DischargeSummary_Details_Link`,
        cleanedData
      )
      .then((res) => {
        const [type, message] = [
          Object.keys(res.data)[0],
          Object.values(res.data)[0],
        ];
        dispatch({ type: "toast", value: { message, type } });
        handleClear();
        fetchDischargeSummary();
      })
      .catch((err) => console.log(err));
  };

  useEffect(() => {
    fetchDischargeSummary();
  }, [fetchDischargeSummary]);

  const adjustHeight = (e) => {
    e.target.style.height = "auto"; // Reset height to calculate scrollHeight
    e.target.style.height = `${e.target.scrollHeight}px`; // Set height to scrollHeight
  };


  return (
    <>
      {isPrintButtonVisible ? (
        <>
          {/* <div className="Main_container_app"> */}
          {/* Patient Details */}

          <br />

          {/* Final Diagnosis */}

          <div className="Otdoctor_intra_Con">
            <div className="text_adjust_mt_Ot wedje_98i">
              <label htmlFor="finalDiagnosis">
                FINAL DIAGNOSIS<span>:</span>{" "}
              </label>
              <textarea
                name="finalDiagnosis"
                id="finalDiagnosis"
                value={finalDiagnosis}
                onChange={handleDiagnosisChange}
                    style={{
          overflow: "hidden", 
          resize: "none", 
          minHeight: "60px", 
        }}
        />
            </div>

            <div className="text_adjust_mt_Ot wedje_98i">
                <label> PRESENTING HISTORY <span>:</span> </label>

              <textarea
                name="presentingComplaints"
                id="presentingComplaints"
                value={presentingComplaints}
                onChange={(e) =>{ setPresentingComplaints(e.target.value);
                          adjustHeight(e); 
                          }}

               style={{
          overflow: "hidden", 
          resize: "none", 
          minHeight: "60px", 
        }}
         />
            </div>

          </div>

        

          <br />
          <div className="Otdoctor_intra_Con">
            <div className="text_adjust_mt_Ot wedje_98i">
              <label htmlFor="PastMedicalHistory">
                PAST MEDICAL HISTORY<span>:</span>{" "}
              </label>
              <textarea
                name="PastMedicalHistory"
                id="PastMedicalHistory"
                value={PastMedicalHistory}
                onChange={(e) => {setPastMedicalHistory(e.target.value);
                          adjustHeight(e); 
}}
  style={{
          overflow: "hidden", 
          resize: "none", 
          minHeight: "60px", 
        }}
              />
            </div>
          </div>
          <br />
          <div className="Otdoctor_intra_Con">
            <div className="text_adjust_mt_Ot wedje_98i">
              <label htmlFor="AllergyHistory">
                DRUG ALLERGIES<span>:</span>{" "}
              </label>
              <textarea
                name="AllergyHistory"
                id="AllergyHistory"
                value={AllergyHistory}
                onChange={(e) => {setAllergyHistory(e.target.value);
                          adjustHeight(e); 
}}
                style={{
          overflow: "hidden", 
          resize: "none", 
          minHeight: "60px", 
        }}
          />
            </div>
          </div>

          {/* On Admission Examination */}

          <div className="RegisFormcon_1">
            <div className="Otdoctor_intra_Con_2_New0">
              <div className="common_center_tag">
                <span> ON EXAMINATION</span>
              </div>

 <textarea
        name="OnAdmissionExamination"
        id="OnAdmissionExamination"
        value={vitals}
        onChange={(e) => {
          setVitals(e.target.value);
          adjustHeight(e); 
        }}
        style={{
          overflow: "hidden", 
          resize: "none", 
          minHeight: "60px", 
        }}
      />
            </div>
          </div>


          <div className="RegisFormcon_1">
            <div className="Otdoctor_intra_Con_2_New0">
              <div className="common_center_tag">
                <span> Radiology Details</span>
              </div>

              <textarea
                name="RadiologyDetails"
                id="RadiologyDetails"
                value={Radiology}
                onChange={(e) => {setRadiology(e.target.value);
                          adjustHeight(e); 
}}
                 style={{
          overflow: "hidden", 
          resize: "none", 
          minHeight: "60px", 
        }} />
            </div>
          </div>

          {/* Lab Details */}

          {/* <div className="RegisFormcon_1">

            <div className="Otdoctor_intra_Con_2_New0">
              <div className="common_center_tag">
                <span>Lab Details</span>
              </div>
              
              <textarea
                name="LabDetails"
                id="LabDetails"
                value={Lab}
                onChange={(e) => setLab(e.target.value)}
                rows={10} // Optional: Adjust rows for better display
                style={{ width: '100%' }} // Optional: Full width textarea
              />
              

            </div> 


          </div> */}

          {/* <div className="RegisFormcon_1">
            <div className="Otdoctor_intra_Con_2_New0">
                <div className="common_center_tag">
                    <span>Lab Details</span>
                </div>
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                    <thead>
                        <tr>
                            <th>Test Name</th>
                            <th>Value</th>
                            <th>Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        {LabData.map((entry, index) => (
                            <tr key={index}>
                                <td>{entry.test_name || 'N/A'}</td>
                                <td>{entry.value || 'N/A'}</td>
                                <td>{entry.report_date || 'N/A'}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div> */}

          <div className="RegisFormcon_1">
            <div className="Otdoctor_intra_Con_2_New0">
              <div className="common_center_tag">
                <span>Lab Details</span>
              </div>
              {LabData.length >= 0 && (
                <ReactGrid columns={LabColumns} RowData={LabData} />
              )}
            </div>
          </div>

          {/* <div className="RegisFormcon_1">
            <div className="Otdoctor_intra_Con_2_New0">
                <div className="common_center_tag">
                    <span>Lab Details</span>
                </div>
                <table style={{ width: '100%', borderCollapse: 'collapse', border: '1px solid black' }}>
        <thead>
            <tr>
                <th style={{ border: '1px solid black', padding: '8px' }}>Test Name</th>
                {uniqueDates.map((date, index) => (
                    <th key={index} style={{ border: '1px solid black', padding: '8px' }}>{date}</th>
                ))}
            </tr>
        </thead>
        <tbody>
            {Object.keys(tableData).map((testName, index) => (
                <tr key={index}>
                    <td style={{ border: '1px solid black', padding: '8px' }}>{testName}</td>
                    {uniqueDates.map((date, idx) => (
                        <td key={idx} style={{ border: '1px solid black', padding: '8px' }}>
                            {tableData[testName][date] || 'N/A'}
                        </td>
                    ))}
                </tr>
            ))}
        </tbody>
    </table>

            </div>
        </div> */}

          {/* <div className="RegisFormcon_1">
            <div className="Otdoctor_intra_Con_2_New0">
                <div className="common_center_tag">
                    <span>Lab Details</span>
                </div>
                <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                    <thead>
                        <tr>
                            <th>Test Name</th>
                            {uniqueDates.map(date => (
                                <th key={date}>{date}</th>
                            ))}
                        </tr>
                    </thead>
                    <tbody>
                        {Object.entries(tableData).map(([test_name, dates]) => (
                            <tr key={test_name}>
                                <td>{test_name}</td>
                                {uniqueDates.map(date => (
                                    <td key={date} style={{ border: '1px solid #ccc', padding: '8px', textAlign: 'center' }}>
                                        {dates[date] !== undefined ? dates[date] : '-'}
                                    </td>
                                ))}
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div> */}

          {/* Treatment Given */}

          {/* <div className='Otdoctor_intra_Con'>
            <div className='text_adjust_mt_Ot wedje_98i'>
              <label htmlFor='treatmentGiven'>
                TREATMENT GIVEN <span>:</span>{' '}
              </label>
              <textarea
                name='treatmentGiven'
                id='treatmentGiven'
                value={treatmentGiven}
                onChange={e => setTreatmentGiven(e.target.value)}
              />
            </div>
          </div> */}

          {/* Prescription - Progress Notes */}
          {/* Course in Ward */}

          <div className="RegisFormcon_1">
            <div className="Otdoctor_intra_Con_2_New0">
              <div className="common_center_tag">
                <span> COURSE IN THE HOSPITAL</span>
              </div>

              <textarea
                name="notes"
                id="notes"
                value={dischargeNotes}
                onChange={(e) => {setDischargeNotes(e.target.value);
                          adjustHeight(e); 
}}
                   style={{
          overflow: "hidden", 
          resize: "none", 
          minHeight: "60px", 
        }}
        />
            </div>
          </div>
          <br />

          {/* refer a doctor / cross consultant  */}

          <div className="Otdoctor_intra_Con">
            <div className="text_adjust_mt_Ot wedje_98i">
              <label htmlFor="Referdoctor">
                CROSS CONSULTATION <span>:</span>{" "}
              </label>
              <textarea
                name="Referdoctor"
                id="Referdoctor"
                value={Referdoctor}
                onChange={(e) =>{ setReferdoctor(e.target.value);
                          adjustHeight(e); 
}}
                  style={{
          overflow: "hidden", 
          resize: "none", 
          minHeight: "60px", 
        }}
         />
            </div>
          </div>

          {/* Condition on Discharge */}
          <div className="Otdoctor_intra_Con">
            <div className="text_adjust_mt_Ot wedje_98i">
              <label htmlFor="ConditionDischarge">
                CONDITION AT DISCHARGE <span>:</span>{" "}
              </label>

              <textarea
                name="ConditionDischarge"
                id="ConditionDischarge"
                value={ConditionOnDischarge}
                onChange={(e) =>{ setConditionOnDischarge(e.target.value);
                          adjustHeight(e); 
}}
                style={{
          overflow: "hidden", 
          resize: "none", 
          minHeight: "60px", 
        }}
          />
            </div>
          </div>
          <div className="Otdoctor_intra_Con">
            <div className="text_adjust_mt_Ot wedje_98i">
              <label htmlFor="PrescriptionSummary">
                DISCHARGE MEDICATIONS<span>:</span>
              </label>

              <div className="Selected-table-container">
              <table className="selected-medicine-table2">
                <thead>
                  <tr>
                    <th>Drug Name</th>
                    <th>Strength</th>
                    <th colSpan="3">Frequency</th>
                    <th>Route</th>
                    <th>Relationship with Meal</th>
                    <th>Duration</th>
                  </tr>
                  <tr>
                    <th></th>
                    <th></th>
                    <th>M</th>
                    <th>A</th>
                    <th>N</th>
                    <th></th>
                    <th></th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  {PrescriptionSummary.length > 0 ? (
                    PrescriptionSummary.map((item, index) => {
                      const frequencyParts = item.Frequency.split("-"); // Assuming format "1-0-1" (M-A-N)
                      return (
                        <tr key={index}>
                          <td>{item.DrugName}</td>
                          <td>{item.Strength}</td>
                          <td>{frequencyParts[0]}</td>
                          <td>{frequencyParts[1]}</td>
                          <td>{frequencyParts[2]}</td>
                          <td>{item.Route}</td>
                          <td>{item.MealRelation}</td>
                          <td>{item.Duration}</td>
                        </tr>
                      );
                    })
                  ) : (
                    <tr>
                      <td colSpan="8" style={{ textAlign: "center" }}>
                        No prescription data available.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
              </div>


              

            </div>
          </div>

          {/* Follow Up  */}

          {/* <div className='Otdoctor_intra_Con'>
            <div className='text_adjust_mt_Ot wedje_98i'>
              <label htmlFor='Followup'>
                Follow Up<span>:</span>{' '}
              </label>

              <textarea name='Followup' id='Followup' />
            </div>
          </div> */}
          
          {/* <div className='Otdoctor_intra_Con'>
            <div className='Otdoctor_intra_Con_2_input'>
              <label htmlFor='followupDate'>
                Followup Date <span>:</span>
              </label>
              <input type='date' id='followupDate' name='followupDate' />
            </div>
          </div>
          <br /> */}
          <br />

          <div className="RegisFormcon">
            <div className="RegisForm_1">
              <label>
                After <span>:</span>
              </label>
              <input
                name="NoOfDays"
                id="NoOfDays"
                type="number"
                value={Followup.NoOfDays}
                className="dura_with2"
                onKeyDown={(e) =>
                  ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()
                }
                onChange={handleFollowupInputChange}
              />
              <select
                name="TimeInterval"
                id="TimeInterval"
                value={Followup.TimeInterval} // Add this to your state
                onChange={handleFollowupInputChange}
              >
                <option value="days">Days</option>
                <option value="weeks">Weeks</option>
                <option value="months">Months</option>
              </select>
            </div>

            <div className="RegisForm_1">
              <label>
                Date <span>:</span>
              </label>
              <input
                name="Date"
                type="date"
                value={Followup.Date}
                onChange={handleFollowupInputChange}
              />
            </div>

            <div className="RegisForm_1">
              <span
                style={{
                  color: ["Sunday", "Saturday"].includes(
                    Finddays[new Date(Followup.Date).getDay()]
                  )
                    ? "red"
                    : "",
                }}
              >
                {Finddays[new Date(Followup.Date).getDay()]}
              </span>
            </div>
          </div>
 <br />
          {/* Advise on Discharge  */}

          <div className="Otdoctor_intra_Con">
            <div className="text_adjust_mt_Ot wedje_98i">
              <label htmlFor="DietAdvice">
                DIET ADVICE<span>:</span>{" "}
              </label>

              <textarea
                name="DietAdvice"
                id="DietAdvice"
                value={DietAdvice}
                onChange={(e) =>{ setDietAdvice(e.target.value);
                          adjustHeight(e); 
}}
                 style={{
          overflow: "hidden", 
          resize: "none", 
          minHeight: "60px", 
        }}
         />
            </div>
          </div>
          <div className="Otdoctor_intra_Con">
            <div className="text_adjust_mt_Ot wedje_98i">
              <label htmlFor="DietAdvice">
                PLEASE COME TO EMERGENCY IF YOU HAVE<span>:</span>{" "}
              </label>

              <textarea
                name="Emergency"
                id="Emergency"
                value={Emergency}
                onChange={(e) =>{ setEmergency(e.target.value);
                          adjustHeight(e); 
}}
            
                style={{
          overflow: "hidden", 
          resize: "none", 
          minHeight: "60px", 
        }}
             />
            </div>
          </div>

          <div className="Otdoctor_intra_Con">
            <div className="text_adjust_mt_Ot wedje_98i">
              <label htmlFor="AdviseonDischarge">
                ADVICE ON DISCHARGE<span>:</span>{" "}
              </label>

              <textarea
                name="AdviseonDischarge"
                id="AdviseonDischarge"
                value={AdviceOnDischarge}
                onChange={(e) =>{ setAdviceOnDischarge(e.target.value);
                  adjustHeight(e); }}
              
                  style={{
          overflow: "hidden", 
          resize: "none", 
          minHeight: "60px", 
        }}/>
            </div>
          </div>

          {/* Dcotors Schedule  */}

          <div className="Otdoctor_intra_Con">
            <div className="text_adjust_mt_Ot wedje_98i">
              <label htmlFor="doctorSchedule ">
                DOCTOR SCHEDULE <span>:</span>{" "}
              </label>

              <textarea
                name="doctorSchedule"
                id="doctorSchedule"
                value={doctorSchedule} // Use doctorSchedule here
                onChange={(e) =>{ setDoctorSchedule(e.target.value);
                  adjustHeight(e); }} // Optional: If you want users to edit
                style={{
          overflow: "hidden", 
          resize: "none", 
          minHeight: "60px", 
        }}
         />
            </div>
          </div>

          {/* Advise on Discharge  */}

          {/* <div className='Otdoctor_intra_Con'>
            <div className='text_adjust_mt_Ot wedje_98i'>
              <label htmlFor='OtherClinic'>
                Other Clinic OPD Contact<span>:</span>{' '}
              </label>

              <textarea name='OtherClinic' id='OtherClinic' />
            </div>
          </div>
          <br /> */}

          <div className="RegisForm_1 signature-align">
            <div className="">
              <div>
                <SignatureCanvas
                  ref={signatureRef}
                  penColor="black"
                  canvasProps={{
                    width: 190,
                    height: 100,
                    className: "sigCanvas2",
                  }}
                />
              </div>
              <h5
                style={{
                  display: "flex",
                  justifyContent: "center",
                  marginTop: "5px",
                }}
              >
                Signature
              </h5>

              <div className="Register_btn_con">
                <button
                  className="RegisterForm_1_btns"
                  onClick={clearSignature}
                >
                  Clear
                </button>
                <button className="RegisterForm_1_btns" onClick={saveSignature}>
                  Save
                </button>
              </div>
            </div>
          </div>
          <br />
          <br />

          {isPrintButtonVisible && (
            <div className="Main_container_Btn">
              <button onClick={handleDischargeSummarySubmit}>
                {ShowPrintBtn ? "Update" : "Submit"}
              </button>

              <button onClick={Submitalldata}>Print</button>
            </div>
          )}

          {/* 
      <div className="Main_container_Btn">
          <button onClick={handlePrint2}>Print</button>
      </div> */}
          {/* </div> */}
        </>
      ) : (
        <>
          {/* Patient Details */}

          {/* {pages.map((pageContent, pageIndex) => ( */}

          <PrintContent
            ref={componentRef}
            // key={pageIndex}
            style={{
              // marginTop: "50px",
              display: "flex",
              justifyContent: "center",
            }}
          >
            
            <div className="Print_ot_all_div edewdedw_89j" id="reactprintcontent">
              <div className="print_dischrge_sum" ref={printRef}>
                <table style={{ width: "100%", borderCollapse: "collapse" }}>
                  <thead>
                    <div>
                      <div className="paymt-fr-mnth-slp">
                        <div className="logo-pay-slp">
                          <img alt="" />
                        </div>

                        <div>
                          <h2>{/* {clinicName} ({location}) */}</h2>
                        </div>
                      </div>
                    </div>

                    <div className="patient_basic_details_print">
                      <div className="align_label_print_head">
                        <div className="align_label_print">
                          <label htmlFor="PatientName">
                            Patient Name <span>:</span>{" "}
                          </label>
                          <h5 htmlFor="PatientName">
                            {IP_DoctorWorkbenchNavigation?.PatientName}
                          </h5>
                        </div>

                        <div className="align_label_print">
                          <label htmlFor="Age">
                            Age <span>:</span>{" "}
                          </label>
                          <h5 htmlFor="Age">
                            {IP_DoctorWorkbenchNavigation?.Age}
                          </h5>
                        </div>

                        <div className="align_label_print">
                          <label htmlFor="Age">
                            Gender <span>:</span>{" "}
                          </label>
                          <h5 htmlFor="Gender">
                            {IP_DoctorWorkbenchNavigation?.Gender}
                          </h5>
                        </div>

                        <div className="align_label_print">
                          <label htmlFor="BedNo">
                            Bed No <span>:</span>{" "}
                          </label>
                          <h5 htmlFor="BedNo">
                            {IP_DoctorWorkbenchNavigation?.BedNo}
                          </h5>
                        </div>

                        <div className="align_label_print">
                          <label htmlFor="Age">
                            PhoneNo <span>:</span>{" "}
                          </label>
                          <h5 htmlFor="PhoneNo">
                            {IP_DoctorWorkbenchNavigation?.PhoneNo}
                          </h5>
                        </div>

                        <div className="align_label_print">
                          <label htmlFor="Address">
                            Address <span>:</span>{" "}
                          </label>
                          <h5 htmlFor="Address">
                            {IP_DoctorWorkbenchNavigation?.Address}
                          </h5>
                        </div>
                      </div>

                      <div className="align_label_print_head">
                        <div className="align_label_print">
                          <label htmlFor="RegistrationId">
                            In Patient No <span>:</span>{" "}
                          </label>
                          <h5 htmlFor="RegistrationId">
                            {IP_DoctorWorkbenchNavigation?.RegistrationId}
                          </h5>
                        </div>

                        <div className="align_label_print">
                          <label htmlFor="CurrDate">
                            Admit Date <span>:</span>{" "}
                          </label>
                          <h5 htmlFor="CurrDate">
                            {IP_DoctorWorkbenchNavigation?.CurrDate}
                          </h5>
                        </div>

                        <div className="align_label_print">
                          <label htmlFor="CurrTime">
                            Time <span>:</span>{" "}
                          </label>
                          <h5 htmlFor="CurrTime">
                            {IP_DoctorWorkbenchNavigation?.CurrTime}
                          </h5>
                        </div>

                        <div className="align_label_print">
                          <label htmlFor="CurrDate">
                            Discharge date <span>:</span>{" "}
                          </label>
                          <h5 htmlFor="CurrDate">{currentDate}</h5>
                        </div>

                        <div className="align_label_print">
                          <label htmlFor="DoctorName">
                            Primary Dr Name <span>:</span>{" "}
                          </label>
                          <h5 htmlFor="DoctorName">
                            {IP_DoctorWorkbenchNavigation?.DoctorName}
                          </h5>
                        </div>
                      </div>
                    </div>
                  </thead>

                  <tbody>
                    <tr className="">
                      <td className="text_adjust_ppd8">
                        <label htmlFor="finalDiagnosis">FINAL DIAGNOSIS</label>
                        <p>{DischargeSummarySavedData.FinalDiagnosis}</p>
                      </td>

                      <td className="text_adjust_ppd8">
                        <label> PRESENTING HISTORY</label>

                        <p>{DischargeSummarySavedData.PresentingComplaints}</p>
                      </td>
                      <td className="text_adjust_ppd8">
                        <label> PAST MEDICAL HISTORY</label>

                        <p>{DischargeSummarySavedData.PastMedicalHistory}</p>
                      </td>
                      <td className="text_adjust_ppd8">
                        <label> DRUG ALLERGIES </label>

                        <p>{DischargeSummarySavedData.AllergyHistory}</p>
                      </td>

                      <td className="text_adjust_ppd8">
                        <label> ON EXAMINATION</label>

                        <p>{DischargeSummarySavedData.Vitals}</p>
                      </td>

                      {/* <td className='text_adjust_ppd8'>
                        <label htmlFor='finalDiagnosis'>Treatment Given</label>
                        <p
                         
                          >{treatmentGiven}
                        </p>
                      </td> */}

                      <td className="text_adjust_ppd8">
                        <label> COURSE IN WARD</label>

                        <p>{DischargeSummarySavedData.DischargeNotes}</p>
                      </td>

                      <td className="text_adjust_ppd8">
                        <label> CROSS CONSULTATION </label>

                        <p>{DischargeSummarySavedData.Referdoctor}</p>
                      </td>

                      <td className="text_adjust_ppd8">
                        <label htmlFor="ConditionDischarge">
                          CONDITION AT DISCHARGE
                        </label>

                        <p>{DischargeSummarySavedData.ConditionOnDischarge}</p>
                      </td>
                      <td className="text_adjust_ppd8">
                        <label htmlFor="ConditionDischarge">
                          DISCHARGE MEDICATIONS
                        </label>

                        <div className="prin_nnrmll_table prin_nnrmll_table_new_add">
                        <table>
                          <thead>
                            <tr>
                              <th>Drug Name</th>
                              <th>Strength</th>
                              <th colSpan="3">Frequency</th>
                              <th>Route</th>
                              <th>Relationship with Meal</th>
                              <th>Duration</th>
                            </tr>
                            <tr>
                              <th></th>
                              <th></th>
                              <th>M</th>
                              <th>A</th>
                              <th>N</th>
                              <th></th>
                              <th></th>
                              <th></th>
                            </tr>
                          </thead>
                          <tbody>
                            {PrescriptionSummary.length > 0 ? (
                              PrescriptionSummary.map((item, index) => {
                                const frequencyParts =
                                  item.Frequency.split("-"); // Assuming format "1-0-1" (M-A-N)
                                return (
                                  <tr key={index}>
                                    <td>{item.DrugName}</td>
                                    <td>{item.Strength}</td>
                                    <td>{frequencyParts[0]}</td>
                                    <td>{frequencyParts[1]}</td>
                                    <td>{frequencyParts[2]}</td>
                                    <td>{item.Route}</td>
                                    <td>{item.MealRelation}</td>
                                    <td>{item.Duration}</td>
                                  </tr>
                                );
                              })
                            ) : (
                              <tr>
                                <td colSpan="8" style={{ textAlign: "center" }}>
                                  No prescription data available.
                                </td>
                              </tr>
                            )}
                          </tbody>
                        </table>
                        </div>


                        
                      </td>

                      <td className="text_adjust_ppd8">
                        <label htmlFor="ConditionDischarge">DIET ADVICE</label>
                        <p>{DischargeSummarySavedData.DietAdvice}</p>
                      </td>

                      <td className="text_adjust_ppd8">
                        <label htmlFor="Appointment">
                          FOR APPOINTMENTS / EMERGENCY CALL
                        </label>
                        <h6>IN CASE OF EMERGENCY CALL :{HospitalDetails}</h6>
                        <h6>FOR APPOINTMENTS CALL :{HospitalDetails}</h6>
                      </td>

                      <td className="text_adjust_ppd8">
                        <label htmlFor="ConditionDischarge">
                          PLEASE COME TO EMERGENCY IF YOU HAVE
                        </label>
                        <p>{DischargeSummarySavedData.Emergency}</p>
                      </td>

                      <td className="text_adjust_ppd8">
                        <label htmlFor="followupDate">FOLLOW UP</label>
                        <p>
                          To Review {DischargeSummarySavedData.Referdoctor}{" "}
                          after {DischargeSummarySavedData.NoOfDays}{" "}
                          {DischargeSummarySavedData.TimeInterval}
                        </p>
                      </td>

                      <td className="text_adjust_ppd8">
                        <label htmlFor="AdviseonDischarge"></label>

                        <p name="AdviseonDischarge" id="AdviseonDischarge"></p>
                      </td>
                      <td className="text_adjust_ppd8">
                        <label htmlFor="finalDiagnosis">DOCTOR SCHEDULE</label>

                        <p>{DischargeSummarySavedData.DoctorSchedule} </p>
                      </td>

                      {/* <td className='text_adjust_ppd8'>
                        <label htmlFor='OtherClinic'>
                          Other Clinic OPD Contact
                        </label>

                        <p name='OtherClinic' id='OtherClinic' />
                      </td> */}
                    </tr>
                  </tbody>

                  <tfoot className="print_footerr">
                    {/* <tr className='signature-align'>
                      <td className='signature-align-plo'>
                        <div>
                          <SignatureCanvas
                            ref={signatureRef}
                            penColor='black'
                            canvasProps={{
                              width: 130,
                              height: 80,
                              className: 'sigCanvas2'
                            }}
                          />
                        </div>

                        
                        <h5
                          style={{
                            display: 'flex',
                            justifyContent: 'center',
                            marginTop: '5px'
                          }}
                        >
                          Signature
                        </h5>

                       
                      </td>
                    </tr> */}

                    <tr className="ehydyedyu">
                      <td
                        className="hdhsj_kkw"
                        colSpan="3"
                        style={{
                          borderTop: "2px solid #000",
                          paddingTop: "10px",
                          textAlign: "center",
                        }}
                      >
                        <div
                          style={{ height: "1px solid black", width: "100%" }}
                        ></div>
                        <p>Lab Address: 456 Lab St., City, State, Zip</p>
                        <p>Total Tests: deded</p>
                      </td>
                    </tr>
                  </tfoot>
                </table>
              </div>
            </div>

          </PrintContent>
        </>
      )}
    </>
  );
};

export default IP_DischargeSummary;
