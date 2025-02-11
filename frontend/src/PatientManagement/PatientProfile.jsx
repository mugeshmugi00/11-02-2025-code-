import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch, } from "react-redux";

import SearchIcon from '@mui/icons-material/Search';
import CancelIcon from '@mui/icons-material/Cancel';
import VisibilityIcon from '@mui/icons-material/Visibility';
import { useNavigate } from 'react-router-dom';
import axios from "axios";
import './Patient.css';
import ReactGrid from "../OtherComponent/ReactGrid/ReactGrid";

import ModelContainer from '../OtherComponent/ModelContainer/ModelContainer';

const PatientProfile = () => {

  const UrlLink = useSelector((state) => state.userRecord?.UrlLink);
  const navigate = useNavigate();

  const dispatchvalue = useDispatch();
  const [profilePhoto, setProfilePhoto] = useState(null);
  const [annotatedimage, setAnnotatedimage] = useState(null);
  const [selectedrow, setselectedrow] = useState(false);
  const [selectedrowcase, setselectedrowcase] = useState(false);

  const [generalEvaluationData, setGeneralEvaluationData] = useState([]);


  const [vitalDetailsData, setVitalDetailsData] = useState([]);

  const [prescriptionList, setPrescriptionList] = useState([]);

  const [labDetails, setLabDetails] = useState([]);

  const [radiologyTestname, setRadiologyTestname] = useState([]);


  const [adviceList, setAdviceList] = useState([]);

  const [nextReviewDate, setNextReviewDate] = useState([]);

  const [referdoctor, setReferdoctor] = useState([]);



  const handleClose = () => {
    navigate('/Home/PatientList');
  }
  const [showif, setShowif] = useState(false);
  const [showans, setShowans] = useState(false);
  const PatientListId = useSelector((state) => state.Frontoffice?.PatientListId);
  const [casedata, setCasedata] = useState([]);
  const [patientdetails, setpatientdetails] = useState([]);
  const [allpatientdetails, setAllpatientdetails] = useState([]);
  const [selectedrowappointment, setSelectedrowappointment] = useState(false);
  const [allappointment, setAllappointment] = useState([]);
  const [dates, setDates] = useState({
    currDate: '',
    FromDate: '',
    ToDate: ''
  });

  const [date, setDate] = useState('');
 

  useEffect(() => {
    if (!PatientListId || Object.keys(PatientListId).length === 0) {
      navigate('/Home/PatientList');
    }
  }, [PatientListId, navigate]);


  useEffect(() => {
    if (PatientListId?.PatientId) {
      axios
        .get(`${UrlLink}/Frontoffice/patient_details_management_get_link?PatientId=${PatientListId?.PatientId}`)
        .then((res) => {
          const ress = res.data;
          setpatientdetails(ress);

          // Set profile photo if available
          if (ress?.PatientProfile) {
            setProfilePhoto(ress.PatientProfile);
          } else {
            setProfilePhoto(null);
          }
        })
        .catch((error) => {
          console.error("Error fetching patient details:", error);
        });
    }
  }, [PatientListId, UrlLink]);

  useEffect(() => {
    if (PatientListId?.PatientId) {
      axios
        .get(`${UrlLink}/Frontoffice/Patient_management_details?PatientId=${PatientListId?.PatientId}`)
        .then((res) => {
          const ress = res.data;
          if (ress) {
            setAllpatientdetails(ress);
          }
          else {
            setAllpatientdetails([]);
          }


        })
        .catch((error) => {
          console.error("Error fetching patient details:", error);
        });
    }
  }, [PatientListId, UrlLink]);

  const handleViewinamge = (record) => {

    setselectedrow(true);
    setselectedrowcase(false);

    if (record?.PatientId && record?.Date) {
      const requestUrl = `${UrlLink}/Frontoffice/Patient_Datewise_Annotedimage_details?PatientId=${record.PatientId}&Date=${record.Date}`;

      axios
        .get(requestUrl)
        .then((res) => {
          const responseData = res.data;


          if (responseData && responseData.length > 0) {

            setAnnotatedimage(responseData[0]?.currentAnnotation);
          } else {
            setAnnotatedimage(null);
          }
        })
        .catch((error) => {
          console.error("Error fetching patient annotated details:", error.message || error);
        });
    } else {
      const tdata = {
        message: 'There is no Annoteded Image to view.',
        type: 'warn',
      };
      dispatchvalue({ type: 'toast', value: tdata });
    }
  };



  const handleShowCaseSheet = (record) => {

    setselectedrow(false);
    setselectedrowcase(true);

    if (record?.PatientId && record?.Date) {
      const requestUrl = `${UrlLink}/Frontoffice/Patient_Datewise_Casesheet_details?PatientId=${record.PatientId}&Date=${record.Date}`;

      axios
        .get(requestUrl)
        .then((res) => {
          const responseData = res.data;

          // Separate data into individual arrays
          setGeneralEvaluationData(responseData.general_evaluation_data || []);
          setVitalDetailsData(responseData.vital_details_data || []);
          setPrescriptionList(responseData.prescription_list || []);
          setLabDetails(responseData.Lab_details || []);
          setRadiologyTestname(responseData.Radiology_Testname || []);
          setAdviceList(responseData.advice || []);
          setNextReviewDate(responseData.next_reviewdate || []);
          setReferdoctor(responseData.referdoctor || []);
        })
        .catch((error) => {
          console.error("Error fetching patient annotated details:", error.message || error);
        });
    } else {
      const tdata = {
        message: "There is no Case Sheet to view.",
        type: "warn",
      };
      dispatchvalue({ type: "toast", value: tdata });
    }
  };
  const handleCloseCaseSheet = () => {
    // Resetting selected row case to false
    setselectedrowcase(false);

    // Clearing all state variables (arrays) that hold data related to the case
    setGeneralEvaluationData([]);
    setVitalDetailsData([]);
    setPrescriptionList([]);
    setLabDetails([]);
    setRadiologyTestname([]);
    setAdviceList([]);
    setNextReviewDate([]);
    setReferdoctor([]);
  };



  const handleDateOnChange = (event, name) => {
    if (name === 'currDate') {
      // Clear the 'FromDate' and 'ToDate' when 'currDate' is updated
      setDates((prevDates) => ({
        ...prevDates,
        currDate: event.target.value,
        FromDate: '',  // Clear FromDate
        ToDate: ''     // Clear ToDate
      }));
    } else if (name === 'FromDate') {
      // Clear 'ToDate' when 'FromDate' is updated
      setDates((prevDates) => ({
        ...prevDates,
        FromDate: event.target.value,
        ToDate: ''    // Clear ToDate
      }));
    } else if (name === 'ToDate') {
      // Clear 'FromDate' and 'currDate' when 'ToDate' is updated
      setDates((prevDates) => ({
        ...prevDates,
        ToDate: event.target.value,
        // Clear FromDate
        currDate: ''   // Clear currDate
      }));
    }
  };




  const handleCloseimage = () => {
    setselectedrow(false);
  };
  const handleCloseAppointments = () => {
    setSelectedrowappointment(false);
    setDates({
      currDate: "",
      FromDate: "",
      ToDate: "",
    });
  }

  const handleAppointments = () => {
    if (PatientListId?.PatientId) {
      axios
        .get(`${UrlLink}/Frontoffice/patient_appointment_details_link?PatientId=${PatientListId?.PatientId}`)
        .then((res) => {
          const ress = res.data;
          if (ress) {
            setSelectedrowappointment(true);
            setAllappointment(ress);
          } else {
            setSelectedrowappointment(false);
            setAllappointment([]);
          }
        })
        .catch((error) => {
          console.error("Error fetching patient appointment details:", error);
        });
    }

  }



  const handleInvoice = () => {

  }

  const handleConsentForms = () => {

  }

  const handleTheropyRecords = () => {

  }

  const handleDiagnostics = () => {

  }

  const handleImages = () => {

  }

  const AppointColumn = [
    {
      key: "id",
      name: "S.No",
      frozen: true,
    },
    {
      key: "Visitid",
      name: "VisitId",
      frozen: true,
    },
    {
      key: "VisitPurpose",
      name: "VisitPurpose",
      width: 150,
      frozen: true,
    },

    {
      key: "Date",
      name: "RegisteredDate",
      width: 150,
      frozen: true,
    },
    {
      key: "PrimaryDoctorName",
      name: "DoctorName",
      width: 160,

    },
    {
      key: "Status",
      name: "Status",

    },
    {
      key: "Location",
      name: "Location",

    },

  ]

  const handleSearchSingleDate = (event, name) => {
    const newDates = { ...dates, [name]: event.target.value };
    setDates(newDates);

    if (newDates.currDate) {
      // Filter appointments based on currDate
      const filteredData = allappointment.filter(appointment =>
        appointment.Date === newDates.currDate
      );
      setDate((prev) => ({
        ...prev, // Spread the previous state to retain other fields, if any
        FromDate: '',
        ToDate: ''
      }));

      setAllappointment(filteredData);
    } else {
      // Show a warning toast if no date is selected
      const tdata = {
        message: 'Choose a Date.',
        type: 'warn',
      };
      dispatchvalue({ type: 'toast', value: tdata });

      // Reset to original appointments
      setDates((prev) => ({ ...prev, currDate: "" }));
      setAllappointment(allappointment);
    }
  };

  const handleSearchCustomDate = (event, name) => {
    const newDates = { ...dates, [name]: event.target.value }; // Update dates dynamically
    setDates(newDates);
  
    const { FromDate, ToDate } = newDates;
  
    if (FromDate && ToDate) {
      // Parse and handle date reversal
      const startDate = new Date(Math.min(new Date(FromDate), new Date(ToDate)));
      const endDate = new Date(Math.max(new Date(FromDate), new Date(ToDate)));
  
      // Filter appointments within the date range
      const filteredData = allappointment.filter((appointment) => {
        const appointmentDate = new Date(appointment.Date); // Ensure proper parsing
        return appointmentDate >= startDate && appointmentDate <= endDate;
      });
  

      setAllappointment(filteredData);
    } else {
      // Warning for missing dates
      if (!FromDate || !ToDate) {
        const tdata = {
          message: "Please select both From Date and To Date.",
          type: "warn",
        };
        dispatchvalue({ type: "toast", value: tdata });
      }
  
      // Reset to the original appointments list
      setAllappointment(allappointment);
    }
  };
  
  const handleDateChange = (event) => {
    setDate(event.target.value); // Update 'date' directly
  };


  const handleSearchDate = () => {
    if (date) {
      // Fetch filtered data if a date is provided
      axios
        .get(
          `${UrlLink}/Frontoffice/Patient_management_details?PatientId=${PatientListId?.PatientId}&date=${date}`
        )
        .then((res) => {
          const response = res.data;
          if (response) {
            setAllpatientdetails(response); // Set filtered data
          } else {
            const tdata = {
              message: "No Patient Details in the Date",
              type: "warn",
            };
            dispatchvalue({ type: "toast", value: tdata });
          }
        })
        .catch((error) => {
          console.error("Error fetching patient details:", error);
        });
    } else {

      axios
        .get(
          `${UrlLink}/Frontoffice/Patient_management_details?PatientId=${PatientListId?.PatientId}`
        )
        .then((res) => {
          const previousData = res.data;
          if (previousData) {
            setAllpatientdetails(previousData); // Show previous data
          } else {
            setAllpatientdetails([]); // Clear if no data available
          }
        })
        .catch((error) => {
          console.error("Error fetching previous patient details:", error);
        });
    }
  };

  const handleCloseCancel = () => {
    setDate('');
    axios
    .get(
      `${UrlLink}/Frontoffice/Patient_management_details?PatientId=${PatientListId?.PatientId}`
    )
    .then((res) => {
      const previousData = res.data;
      if (previousData) {
        setAllpatientdetails(previousData); // Show previous data
      } else {
        setAllpatientdetails([]); // Clear if no data available
      }
    })
    .catch((error) => {
      console.error("Error fetching previous patient details:", error);
    });
  }
  useEffect(() => { setCasedata(['1', '20/10/24', 'CH321', 'NewComer']) }, [])

  return (
    <div className='ProfileContainer'>
      {/* Left Profile Section */}
      <div className="LeftContainer">

        <div className='imagebox'>
          {
            profilePhoto ? (
              <img src={profilePhoto} alt="Profile Photo" className="profile-photo" />
            ) : (
              <div className="no-photo">No Profile Photo Available</div>
            )}
        </div>
        <h3> {patientdetails?.PatientName || <span>No Patient Name Available</span>}</h3>

        <p>
          Email: <strong>{patientdetails?.Email || "No Email"}</strong>
        </p>

        <p>
          Phone Number: <strong>{patientdetails?.PhoneNo || "No PhoneNo"}</strong>
        </p>

        <button >Case Sheets </button>
        <button className='but' onClick={handleAppointments}>Appointments</button>
        <button className='but' onClick={handleInvoice}>Invoice(billing)</button>
        <button className='but' onClick={handleConsentForms}>Consent Forms</button>
        <button className='but' onClick={handleTheropyRecords}>Theropy Records</button>
        <button className='but' onClick={handleDiagnostics}>Diagnostics</button>
        <button className='but' onClick={handleImages}>Images</button>
        <div className='butt'>
          <button onClick={() => setShowif(true)}>IF </button>
          <button onClick={() => setShowans(true)}>ANS </button>

        </div>

      </div>

      {/* Right Content Section */}
      <div className="RightContainer">


        <div className='medicalheader'>
          <h2>Medical Record</h2>
          <div className="RegisForm_1">
            <label>Date<span>:</span></label>
            <input
              type="date"
              name="date"
              value={date} // Controlled input from string state
              onChange={handleDateChange}

            />

            <button onClick={handleSearchDate}><SearchIcon /></button>
            <button onClick={handleCloseCancel  }><CancelIcon /></button>


          </div>
        </div>

        {/* Records List */}
        <div>
          {allpatientdetails.length > 0 ? (
            allpatientdetails.map((record, index) => (
              <div
                key={index}
                className="recordcard"
                onClick={() => handleShowCaseSheet(record)} // Only trigger this for the parent div
              >

                <div style={styles.actionButtons}>
                  <button
                    className="viewbutton"
                    onClick={(event) => {
                      event.stopPropagation(); // Prevent the click from propagating to the parent div
                      handleViewinamge(record);
                    }}
                  >
                    <VisibilityIcon />
                  </button>
                </div>
                <p><strong>Date:</strong> {record.date}</p>
                <p><strong>Complaint:</strong> {record.CheifComplaint || "NoChiefComplaint"}</p>
                <p><strong>Diagnosis:</strong> {record.Diagnosis || "NoDiagnosis"}</p>
                <p><strong>Examine:</strong> {record.Examine || "NoExamine"}</p>
                <p><strong>History:</strong> {record.History || "NoHistory"}</p>

                {/* Vitals Section */}
                <p>
                  <strong>Vitals:</strong>
                  {record.Temperature ? `Temperature: ${record.Temperature}°C, ` : "Temperature: N/A, "}
                  {record.Pulse_Rate && `Pulse Rate: ${record.Pulse_Rate} bpm, `}
                  {record.SPO2 && `SPO2: ${record.SPO2}%, `}
                  {record.Heart_Rate && `Heart Rate: ${record.Heart_Rate} bpm, `}
                  {record.SBP && `SBP: ${record.SBP} mmHg, `}
                  {record.DBP && `DBP: ${record.DBP} mmHg, `}
                  {record.Height && `Height: ${record.Height} cm, `}
                  {record.Weight && `Weight: ${record.Weight} kg, `}
                  {record.BMI && `BMI: ${record.BMI}, `}
                  {record.WC && `WC: ${record.WC} cm, `}
                  {record.HC && `HC: ${record.HC} cm`}
                </p>

                {/* Prescriptions Section */}
                <p>
                  <strong>Prescriptions:</strong>
                  {(record.Prescriptions && record.Prescriptions.length > 0
                    ? record.Prescriptions.join(', ')
                    : null) || "No prescriptions"}
                </p>
              </div>
            ))
          ) : (
            <div className="no-records">
              No medical records available.
            </div>
          )}
        </div>




      </div>

      {selectedrow && (
        <div className="loader" onClick={() => setselectedrow(false)}>
          <div className="loader_register_roomshow" onClick={(e) => e.stopPropagation()}>

            {annotatedimage ? (
              <div>
                <div className="common_center_tag">
                  <span>Image</span>
                </div>
                <br />
                <div className="Main_container_app">
                  <img src={annotatedimage} alt="Annotated" />
                </div>
                <br></br>
                <div className="Main_container_Btn">
                  <button onClick={handleCloseimage}>
                    Close
                  </button>
                </div>
              </div>
            ) : (
              <div className="no-photo"
                style={{
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                  height: "100%", // Adjust this as needed based on the container size
                  textAlign: "center",
                }}>
                No  Annotated Image Available
                <br></br>
                <div className="Main_container_Btn">
                  <button onClick={handleCloseimage}>
                    Close
                  </button>
                </div>
              </div>
            )}

          </div>
        </div>
      )}


      {selectedrowappointment && (
        <div className="loader" onClick={() => setSelectedrowappointment(false)}>
          <div className="loader_register_roomshow" onClick={(e) => e.stopPropagation()}>

            {allappointment.length > 0 ? (  // Fixed the typo from 'lenth' to 'length'
              <div>
                <div className="common_center_tag">
                  <span>Appointment Details</span>
                </div>
                <div className="RegisForm_1">
                  <label>
                    Choose Date <span>:</span>
                  </label>
                  <input
                    type="date"
                    name="currDate"
                    value={dates.currDate}
                    onChange={(event) => handleDateOnChange(event, 'currDate')} // Pass the name dynamically
                  />
                  <button onClick={handleSearchSingleDate}><SearchIcon /></button>

                </div>
                <br>
                </br>
                <div className="RegisForm_1">
                  <label>
                    Custom Date
                  </label>
                  <br></br>
                  <br>
                  </br>
                  <label>
                    From Date <span>:</span>
                  </label>
                  <input
                    type="date"
                    name="FromDate"

                    value={dates.FromDate}
                    onChange={(event) => handleDateOnChange(event, 'FromDate')} // Pass the name dynamically
                  />
                  <label>
                    To Date <span>:</span>
                  </label>
                  <input
                    type="date"
                    name="ToDate"
                    min={dates.FromDate}
                    value={dates.ToDate}
                    onChange={(event) => handleDateOnChange(event, 'ToDate')} // Pass the name dynamically
                  />
                  <button onClick={handleSearchCustomDate}><SearchIcon /></button>
                </div>

                <br />

                <div className="Main_container_app">
                  <ReactGrid columns={AppointColumn} RowData={allappointment} />
                </div>
                <br />
                <div className="Main_container_Btn">
                  <button onClick={handleCloseAppointments}>
                    Close
                  </button>
                </div>
              </div>
            ) : (
              <div className="no-photo">
                No Appointment Details Available
              </div>
            )}

          </div>
        </div>
      )}





      {selectedrowcase && (
        <div className="modal-container" onClick={handleCloseCaseSheet}>
          <div className="recordpopup" onClick={(e) => e.stopPropagation()}>
            <h2>Recordcard  Details</h2>

            <div>
              <h3 style={{ textAlign: "center" }}>Patient Visit Details</h3>
              <h4 style={{ textAlign: "center" }}>Case Sheet</h4>

              {generalEvaluationData?.length > 0 ? (
                <div>
                  {generalEvaluationData.map((item, index) => (
                    <p key={index}>
                      {"Mr. " + patientdetails?.PatientName + " (PatientId: " + item.PatientId +
                        ") Age " + item.Age + " Years, " + item.gender +
                        ", was presented with " + item.KeyComplaint +
                        " with the following history of " + item.History}
                    </p>
                  ))}
                </div>
              ) : (
                <span>No patient details not filled  General Evaluation ...</span>
              )}

              <hr />
            </div>


            <div>
              <h4 style={{ textAlign: "center" }}>ReferDoctor Details</h4>
              <div>
                {Array.isArray(referdoctor) && referdoctor.length > 0 ? (
                  <div className="for">
                    <div className="Selected-table-container">
                      <table className="selected-medicine-table2">
                        <thead>
                          <tr>
                            <th id="slectbill_ins">PrimaryDoctor Name</th>
                            <th id="slectbill_ins">ReferDoctor Speciality</th>
                            <th id="slectbill_ins">ReferDoctor Name</th>
                            <th id="slectbill_ins">ReferDoctor Type</th>
                          </tr>
                        </thead>
                        <tbody>
                          {referdoctor.map((refer, index) => (
                            <tr key={refer.id || index}>
                              <td>{refer.PrimaryDoctorId ? `${refer.PrimaryDoctorId.Tittle} ${refer.PrimaryDoctorId.ShortName}` : "No PrimaryDoctor"}</td>
                              <td>{refer.ReferDoctorSpeciality || "No ReferDoctor Speciality"}</td>
                              <td>{refer.ReferDoctorId ? `${refer.ReferDoctorId.Tittle} ${refer.ReferDoctorId.ShortName}` : "No ReferDoctor"}</td>
                              <td>{refer.ReferDoctorType || "No ReferDoctor Type"}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                ) : (
                  <div className="DivCenter_container">
                    No refer doctor details were recorded during the current visit.
                  </div>
                )}
              </div>
            </div>


            <div>
              <h4 style={{ textAlign: "center" }}>Vitals</h4>
              {Array.isArray(vitalDetailsData) && vitalDetailsData.length > 0 ? ( // Check if vitalDetailsData is an array and has items
                <div className="for">
                  <div className="Selected-table-container">
                    <table className="selected-medicine-table2">
                      <thead>
                        <tr>
                          <th id="slectbill_ins">Temperature</th>
                          <th id="slectbill_ins">SBP</th>
                          <th id="slectbill_ins">DBP</th>
                          <th id="slectbill_ins">Pulse Rate</th>
                          <th id="slectbill_ins">Height</th>
                          <th id="slectbill_ins">Weight</th>
                          <th id="slectbill_ins">BMI</th>
                          <th id="slectbill_ins">SPO2</th>
                          <th id="slectbill_ins">WC</th>
                          <th id="slectbill_ins">HC</th>
                          <th id="slectbill_ins">Date</th>
                          <th id="slectbill_ins">Time</th>
                        </tr>
                      </thead>
                      <tbody>
                        {vitalDetailsData.map((item, index) => (
                          <tr key={item.id || index}>
                            <td>{item.Temperature || "No Temperature"}</td>
                            <td>{item.SBP || "No SBP"}</td>
                            <td>{item.DBP || "No DBP"}</td>
                            <td>{item.PulseRate || "No Pulse Rate"}</td>
                            <td>{item.Height || "No Height"}</td>
                            <td>{item.Weight || "No Weight"}</td>
                            <td>{item.BMI || "No BMI"}</td>
                            <td>{item.SPO2 || "No SPO2"}</td>
                            <td>{item.WC || "No WC"}</td>
                            <td>{item.HC || "No HC"}</td>
                            <td>{item.Date || "No Date"}</td>
                            <td>{item.Time || "No Time"}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              ) : (
                <div className="DivCenter_container">
                  No vitals were recorded during the current visit.
                </div>
              )}
            </div>


            <div>
              <h4 style={{ textAlign: "center" }}>Treatment</h4>
              <h4>Prescription</h4>
              {Array.isArray(prescriptionList) && prescriptionList.length > 0 ? ( // Check if prescriptionList is an array and has items
                <div className="for">
                  <div className="Selected-table-container">
                    <table className="selected-medicine-table2">
                      <thead>
                        <tr>
                          <th id="slectbill_ins">Item Name</th>
                          <th id="slectbill_ins">Item Type</th>
                          <th id="slectbill_ins">Dosage</th>
                          <th id="slectbill_ins">Route</th>
                          <th id="slectbill_ins">Frequency Type</th>
                          <th id="slectbill_ins">Frequency</th>
                          <th id="slectbill_ins">Duration</th>
                          <th id="slectbill_ins">Qty</th>
                          <th id="slectbill_ins">Instruction</th>
                        </tr>
                      </thead>
                      <tbody>
                        {prescriptionList.map((item, index) => (
                          <tr key={item.Id || index}>
                            <td>{item.ItemName || "No Item Name"}</td>
                            <td>{item.ItemType || "No Item Type"}</td>
                            <td>{item.Dosage || "No Dosage"}</td>
                            <td>{item.Route || "No Route"}</td>
                            <td>{item.FrequencyType || "No Frequency Type"}</td>
                            <td>{item.Frequency || item.Frequencys || "No Frequency"}</td>
                            <td>{`${item.DurationNumber || "No Duration"} ${item.DurationUnit || ""}`}</td>
                            <td>{item.Qty || "None"}</td>
                            <td>{item.Instruction || "No Instruction"}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              ) : (
                <div className="DivCenter_container">
                  No medication was issued during the current visit.
                </div>
              )}
            </div>

            <div>
              <h4>Lab</h4>
              <h4 style={{ textAlign: "center" }}>Investigations Ordered</h4>
              <div>

                {Array.isArray(labDetails) && labDetails.length > 0 ? (
                  // Check if labDetails is an array and contains items
                  <div className="for">
                    <div className="Selected-table-container">
                      <table className="selected-medicine-table2">
                        <thead>
                          <tr>
                            <th id="slectbill_ins">Test Name</th>
                          </tr>
                        </thead>
                        <tbody>
                          {labDetails.map((item, index) => (
                            <tr key={item.id || index}>
                              <td>{item.TestName || "No Test Name"}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                ) : (
                  <div className="DivCenter_container">
                    No lab investigations were recorded during the current visit.
                  </div>
                )}
              </div>
            </div>

            <div>
              <h4>Radiology</h4>
              <h4 style={{ textAlign: "center" }}>Investigations Ordered</h4>
              <div>

                {Array.isArray(radiologyTestname) && radiologyTestname.length > 0 ? (
                  // Check if radiologyTestname is an array and contains items
                  <div className="for">
                    <div className="Selected-table-container">
                      <table className="selected-medicine-table2">
                        <thead>
                          <tr>
                            <th>Radiology Department</th>
                            <th id="slectbill_ins">Test Name</th>
                          </tr>
                        </thead>
                        <tbody>
                          {radiologyTestname.map((item, index) => (
                            <tr key={item.id || index}>
                              <td>{item.RadiologyName || "No Radiology Name"}</td>
                              <td>{item.TestName || "No Test Name"}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                ) : (
                  <div className="DivCenter_container">
                    No radiology tests were recorded during the current visit.
                  </div>
                )}
              </div>
            </div>

            <div>
              <h4 style={{ textAlign: "center" }}>Advice</h4>
              <div>
                {Array.isArray(adviceList) && adviceList.length > 0 ? (
                  <div className="for">
                    <div className="Selected-table-container">
                      <table className="selected-medicine-table2">
                        <tbody>
                          {adviceList.map((item, index) => (
                            <tr key={item.id || index}>
                              <td>{item.Advice && item.Advice.trim() !== "" ? item.Advice : "No advice available."}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                ) : (
                  <div className="DivCenter_container">
                    No advice was recorded during the current visit.
                  </div>
                )}
              </div>
            </div>


            <div>
              <h4 style={{ textAlign: "center" }}>Next Review Date</h4>
              <div>
                {Array.isArray(nextReviewDate) && nextReviewDate.length > 0 ? (
                  <div className="for">
                    <div className="Selected-table-container">
                      <table className="selected-medicine-table2">
                        <thead>
                          <tr>
                            <th id="slectbill_ins">No. of Days</th>
                            <th id="slectbill_ins">Time Interval</th>
                            <th id="slectbill_ins">Date</th>
                          </tr>
                        </thead>
                        <tbody>
                          {nextReviewDate.map((item, index) => (
                            <tr key={item.id || index}>
                              <td>{item.NoOfDays || "No data"}</td>
                              <td>{item.TimeInterval || "No data"}</td>
                              <td>{item.Date || "No data"}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                ) : (
                  <div className="DivCenter_container">
                    No next review details were recorded during the current visit.
                  </div>
                )}
              </div>
            </div>
            <br>
            </br>

            <div className="Main_container_Btn">
              <button onClick={handleCloseCaseSheet}>
                Close
              </button>
            </div>

















          </div>
        </div>


      )}



      <ModelContainer />
    </div>

  );
};

// Inline styles
const styles = {
  actionButtons: {
    display: "flex",
    justifyContent: "flex-end",
    marginTop: "10px",
  },

};
export default PatientProfile;
