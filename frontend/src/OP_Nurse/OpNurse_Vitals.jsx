import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
// import { format } from "date-fns";
import ReactGrid from "../OtherComponent/ReactGrid/ReactGrid";
import axios from "axios";
import ToastAlert from "../OtherComponent/ToastContainer/ToastAlert";
import { IconButton } from "@mui/material";
import VisibilityIcon from "@mui/icons-material/Visibility";
import Button from "@mui/material/Button";
import AddIcon from "@mui/icons-material/Add";
import ToggleButton from "@mui/material/ToggleButton";
import ToggleButtonGroup from "@mui/material/ToggleButtonGroup";

const OpNurse_Vitals = () => {
  const dispatch = useDispatch();
  const UrlLink = useSelector((state) => state.userRecord?.UrlLink);
  const toast = useSelector((state) => state.userRecord?.toast);
  const DoctorWorkbenchNavigation = useSelector(
    (state) => state.Frontoffice?.DoctorWorkbenchNavigation
  );
  console.log(DoctorWorkbenchNavigation, "DoctorWorkbenchNavigation");

  const userRecord = useSelector((state) => state.userRecord?.UserData);

  const formatLabel = (label) => {
    if (/[a-z]/.test(label) && /[A-Z]/.test(label) && !/\d/.test(label)) {
      return label
        .replace(/([a-z])([A-Z])/g, "$1 $2")
        .replace(/^./, (str) => str.toUpperCase());
    } else {
      return label;
    }
  };

  const [VitalFormData, setVitalFormData] = useState({
    Temperature: "",
    PulseRate: "",
    SPO2: "",
    HeartRate: "",
    RespiratoryRate: "",
    SBP: "",
    DBP: "",
    Height: "",
    Weight: "",
    BMI: "",
    WC: "",
    HC: "",
    BSL: "",
    // Date: "",

    // Painscore: '',
    // SupplementalOxygen: '',
    // LevelOfConsiousness: '',
    // CapillaryRefillTime: '',

    // ETCO2: "",
    // BreathSounds: "",
    // Date: "",
    // Time: "",
  });

  const [type, setType] = useState("Vital");

  const [gridData, setGridData] = useState([]);
  const [IsGetData, setIsGetData] = useState(false);

  const [IsViewMode, setIsViewMode] = useState(false);
  const [isNewsScoreOpen, setIsNewsScoreOpen] = useState(false); // New state

  const [openModal2, setOpenModal2] = useState(false);

  const [openModalNewScore, setOpenModalNewScore] = useState(false);

  const openModal = () => {
    setOpenModal2(true);
  };

  const colorStyles = {
    normal: "green",
    minlow: "yellow",
    maxlow: "yellow",
    minmedium: "orange",
    maxmedium: "orange",
    minhigh: "red",
    maxhigh: "red",
  };

  const getColorByStatus = (status) => {
    switch (status) {
      case 3:
        return "red";
      case 2:
        return "orange";
      case 1:
        return "yellow";
      case 0:
        return "green";
      default:
        return ""; // Default color for undefined or other values
    }
  };

  const getColorStyle = (status) => {
    return colorStyles[status] || ""; // Default color if no match
  };

  const renderColorBox = (status) => {
    // Ensure `status` is defined and is a string
    if (typeof status !== "string" || status.length === 0) {
      return null; // Or render a default/fallback element
    }

    return (
      <div
        style={{
          width: "40px", // Slightly larger for better visibility
          height: "40px", // Slightly larger for better visibility
          backgroundColor: getColorStyle(status),
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          marginRight: "15px", // Increased spacing
          borderRadius: "8px", // Rounded corners
          boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)", // Subtle shadow for depth
          border: "1px solid rgba(0, 0, 0, 0.2)", // Light border for contrast
          fontSize: "12px", // Adjust font size for the box
          fontWeight: "bold", // Bold text
          color: "#fff", // Text color for better contrast
        }}
      >
        {status.charAt(0).toUpperCase()}{" "}
        {/* Display first letter of the range */}
      </div>
    );
  };

  useEffect(() => {
    if (VitalFormData.Weight && VitalFormData.Height) {
      const parsedWeight = parseFloat(VitalFormData.Weight);
      const parsedHeight = parseFloat(VitalFormData.Height) / 100; // Convert cm to m
      const calculatedBMI = (
        parsedWeight /
        (parsedHeight * parsedHeight)
      ).toFixed(2);

      setVitalFormData((prev) => ({
        ...prev,
        BMI: calculatedBMI,
      }));
    }
  }, [VitalFormData.Weight, VitalFormData.Height]);

  // Handle setting the form data when viewing
  const handleView = (data) => {
    setVitalFormData({
      Temperature: data.Temperature || "",
      PulseRate: data.PulseRate || "",
      SPO2: data.SPO2 || "",
      HeartRate: data.HeartRate || "",
      RespiratoryRate: data.RespiratoryRate || "",
      SBP: data.SBP || "",
      DBP: data.DBP || "",
      Height: data.Height || "",
      Weight: data.Weight || "",
      BMI: data.BMI || "",
      WC: data.WC || "",
      HC: data.HC || "",
      BSL: data.BSL || "",

      //Painscore: data.Painscore || '',
      //SupplementalOxygen: data.SupplementalOxygen || '',
      //LevelOfConsiousness: data.LevelOfConsiousness || '',
      //CapillaryRefillTime: data.CapillaryRefillTime || '',

      // ETCO2: data.EtCO2 || '',
      // BreathSounds: data.BreathSounds || '',
      // Date: data.Date || '',
      // Time: data.Time || '',
      // Createdby: data.Createdby || '',
    });
    setIsViewMode(true);
    setOpenModal2(true);
  };

  // Handle clearing the form and resetting the view mode
  const handleClear = () => {
    setVitalFormData({
      Temperature: "",
      PulseRate: "",
      SPO2: "",
      HeartRate: "",
      RespiratoryRate: "",
      SBP: "",
      DBP: "",
      Height: "",
      Weight: "",
      BMI: "",
      WC: "",
      HC: "",
      BSL: "",
      // Date: "",
    });
    setIsViewMode(false);
  };

  useEffect(() => {
    const RegistrationId = DoctorWorkbenchNavigation?.pk;

    if (RegistrationId) {
      axios
        .get(`${UrlLink}OP/Vitals_Form_Details_Link`, {
          params: {
            RegistrationId: RegistrationId,
          },
        })
        .then((res) => {
          const data = res.data;
          if (data && Array.isArray(data.vital_details)) {
            setGridData(data.vital_details);
          } else {
            console.error("vital_details is not an array:", data);
          }
        })
        .catch((err) => {
          console.error("Error fetching data:", err);
        });
    }
  }, [UrlLink, DoctorWorkbenchNavigation, IsGetData]);
  const HandleOnChange = (event) => {
    const { name, value } = event.target; // Get the input field's name and value

    // Update the VitalFormData object
    setVitalFormData((prev) => ({
      ...prev, // Keep all previous values
      [name]: value, // Update the value for the input that was changed
    }));
  };

  const handleChange = (event) => {
    setType(event.target.value);
  };

  const columns = [
    {
      key: "temperature_status",
      name: "Temperature Status",
      renderCell: (params) => (
        <div
          style={{
            backgroundColor: getColorByStatus(params.row.temperature_status),
            width: "100%",
            height: "100%",
            textAlign: "center",
            color: "#fff",
            fontWeight: "bold",
            borderRadius: "4px",
            padding: "5px",
          }}
        >
          {params.row.temperature_status}
        </div>
      ),
    },
    {
      key: "spo2_status",
      name: "SPO2 Status",
      renderCell: (params) => (
        <div
          style={{
            backgroundColor: getColorByStatus(params.row.spo2_status),
            width: "100%",
            height: "100%",
            textAlign: "center",
            color: "#fff",
            fontWeight: "bold",
            borderRadius: "4px",
            padding: "5px",
          }}
        >
          {params.row.spo2_status}
        </div>
      ),
    },
    {
      key: "heartrate_status",
      name: "Heart Rate Status",
      renderCell: (params) => (
        <div
          style={{
            backgroundColor: getColorByStatus(params.row.heartrate_status),
            width: "100%",
            height: "100%",
            textAlign: "center",
            color: "#fff",
            fontWeight: "bold",
            borderRadius: "4px",
            padding: "5px",
          }}
        >
          {params.row.heartrate_status}
        </div>
      ),
    },
    {
      key: "RespiratoryStatus",
      name: "Respiratory Status",
      renderCell: (params) => (
        <div
          style={{
            backgroundColor: getColorByStatus(params.row.RespiratoryStatus),
            width: "100%",
            height: "100%",
            textAlign: "center",
            color: "#fff",
            fontWeight: "bold",
            borderRadius: "4px",
            padding: "5px",
          }}
        >
          {params.row.RespiratoryStatus}
        </div>
      ),
    },
    {
      key: "sbp_status",
      name: "SBP Status",
      renderCell: (params) => (
        <div
          style={{
            backgroundColor: getColorByStatus(params.row.sbp_status),
            width: "100%",
            height: "100%",
            textAlign: "center",
            color: "#fff",
            fontWeight: "bold",
            borderRadius: "4px",
            padding: "5px",
          }}
        >
          {params.row.sbp_status}
        </div>
      ),
    },
  ];

  const calculateTotalScore = (row) => {
    const fields = [
      "RespiratoryStatus",

      "heartrate_status",
      "temperature_status",
      "spo2_status",
      "sbp_status",
    ];

    return fields.reduce((total, field) => {
      const value = row[field];
      return total + (value !== null ? value : 0); // Ensure we handle null values
    }, 0);
  };

  const calculateAge = (dob) => {
    const dobDate = new Date(dob);
    const today = new Date();
    let age = today.getFullYear() - dobDate.getFullYear();
    const monthDifference = today.getMonth() - dobDate.getMonth();
    if (
      monthDifference < 0 ||
      (monthDifference === 0 && today.getDate() < dobDate.getDate())
    ) {
      age--;
    }
    return age;
  };

  const dob = DoctorWorkbenchNavigation?.DOB; // Ensure this matches the structure of your state
  const age = dob ? calculateAge(dob) : null;

  const getScoreCategory = (score, age) => {
    if (age >= 16) {
      // Score categories for age 16 and above
      if (score >= 0 && score <= 4) {
        return "Low";
      } else if (score >= 5 && score <= 6) {
        return "Medium";
      } else if (score >= 7 && score <= 21) {
        return "High";
      } else {
        return "Unknown";
      }
    } else {
      // Score categories for age below 16
      if (score >= 0 && score <= 2) {
        return "Low";
      } else if (score >= 3 && score <= 5) {
        return "Medium";
      } else if (score >= 6 && score <= 12) {
        return "High";
      } else {
        return "Unknown";
      }
    }
  };

  // Example usage in render or function
  const totalScore =
    gridData.length > 0
      ? calculateTotalScore(gridData[gridData.length - 1])
      : 0;
  // const scoreCategory = getScoreCategory(totalScore);
  const scoreCategory =
    age !== null ? getScoreCategory(totalScore, age) : "Unknown";
  console.log(totalScore, "totalScore");

  const handleVitalFormSubmit = () => {
    const senddata = {
      ...VitalFormData,
      RegistrationId: DoctorWorkbenchNavigation?.pk,
      Createdby: userRecord?.username,
      Type: "Doctor",
    };

    axios
      .post(`${UrlLink}OP/Vitals_Form_Details_Link`, senddata)
      .then((res) => {
        const [type, message] = [
          Object.keys(res.data)[0],
          Object.values(res.data)[0],
        ];
        dispatch({ type: "toast", value: { message, type } });

        // Fetch the updated data or update gridData optimistically
        setGridData((prevGridData) => [
          ...prevGridData,
          {
            ...VitalFormData,
            Date: new Date().toISOString().split("T")[0], // Adding current date
          },
        ]);

        setIsGetData((prev) => !prev); // Trigger data re-fetch if needed
        handleClear(); // Reset form
        setOpenModal2(false);
      })
      .catch((err) => console.log(err));
  };

  return (
    <>
      <div className="RegisFormcon_1">
        <div
          style={{
            width: "100%",
            display: "flex",
            textAlign: "end",
            justifyContent: "flex-end",
          }}
        ></div>

        <div className="vitals-container">
          {type === "Vital" && (
            <div>
              <div>
                <div className="past_present_pl efef_iuwd">
                  <h5>All Vitals</h5>
                  <div className="cwsu_6yw">
                  <Button
                    className="cell_btn"
                    style={{
                      backgroundColor: "skyblue",
                      width: "110px",
                      fontSize: "13px",
                    }}
                    onClick={openModal}
                  >
                    <div
                      style={{
                        width: "100%",
                        display: "flex",
                        cursor: "pointer",
                        alignItems: "center",
                        fontSize:'11px',
                        gap: "3px",
                        justifyContent: "center",
                      }}
                    >
                      <AddIcon style={{ fontSize: "17px" }} />
                      Add Vitals
                    </div>
                  </Button>

                  <Button
                    style={{
                      backgroundColor: "skyblue",
                      width: "110px",
                      fontSize:'11px',
                      color:'black',
                    }}
                    className="togglebutton_container"
                    onClick={() => setOpenModalNewScore(true)} // Open the grid
                  >
                    NewsScore
                  </Button>
                  </div>

                  {/* Data Grid */}
                  {openModalNewScore && gridData.length > 0 && (
                    <div
                      className="sideopen_showcamera_profile"
                      onClick={() => setOpenModalNewScore(false)}
                    >
                      <div
                        className="newwProfiles newwPopupforreason"
                        onClick={(e) => e.stopPropagation()}
                      >
                        <>
                          <div
                            style={{
                              display: "flex",
                              alignItems: "center",

                              justifyContent: "center",
                            }}
                          >
                            {renderColorBox("minhigh")}Min High
                            {renderColorBox("minmedium")}Min Medium
                            {renderColorBox("minlow")}Min Low
                            {renderColorBox("normal")}Normal
                            {renderColorBox("maxlow")}Max Low
                            {renderColorBox("maxmedium")}Max Medium
                            {renderColorBox("maxhigh")}Max High
                          </div>

                          <ReactGrid
                            columns={columns} // Ensure these are properly defined
                            RowData={gridData} // Pass the grid data here
                          />
                          <br />
                          <div className="Main_container_Btn">
                            <button
                              onClick={() => setOpenModalNewScore(false)} // Close the grid
                            >
                              Close
                            </button>
                          </div>
                        </>
                      </div>
                    </div>
                  )}
                </div>

                <div className="Selected-table-container">
                  <table className="selected-medicine-table2">
                    <thead>
                      <tr>
                        <th>Vital Name</th>
                        {gridData.map((entry, index) => (
                          <th key={index}>{entry.Date}</th>
                        ))}
                      </tr>
                    </thead>
                    <tbody>
                      {[
                        "Temperature",
                        "PulseRate",
                        "SPO2",
                        "HeartRate",
                        "RespiratoryRate",
                        "SBP",
                        "DBP",
                        "Height",
                        "Weight",
                        "BMI",
                        "WC",
                        "HC",
                        "BSL",
                      ].map((vital, index) => (
                        <tr key={index}>
                          <td>{vital}</td>
                          {gridData.map((entry, i) => (
                            <td key={i}>{entry[vital] || ""}</td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Toast Alert */}
        <ToastAlert Message={toast.message} Type={toast.type} />
      </div>

      {/* Modal for Adding Vitals */}
      {openModal2 && (
        <div
          className="sideopen_showcamera_profile"
          onClick={() => setOpenModal2(false)}
        >
          <div
            className="newwProfiles newwPopupforreason"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="RegisFormcon_1">
              <div
                style={{ width: "100%", display: "grid", placeItems: "center" }}
              >
                <ToggleButtonGroup
                  value={type}
                  exclusive
                  onChange={handleChange}
                  aria-label="Platform"
                >
                  <ToggleButton
                    value="Vital"
                    style={{
                      height: "30px",
                      width: "100px",
                      backgroundColor:
                        type === "Vital"
                          ? "var(--selectbackgroundcolor)"
                          : "inherit",
                    }}
                    className="togglebutton_container"
                  >
                    Vital
                  </ToggleButton>
                </ToggleButtonGroup>
              </div>

              {/* Form for Adding/Editing Vitals */}
              {type === "Vital"
                ? Object.keys(VitalFormData).map((p, index) => (
                    <div className="RegisForm_1 regis_2_for_smll9" key={p}>
                      <label htmlFor={`${p}_${index}`}>
                        {formatLabel(p)} <span>:</span>
                      </label>
                      {p === "SupplementalOxygen" ||
                      p === "LevelOfConsiousness" ? (
                        <select
                          id={`${p}_${index}`}
                          name={p}
                          value={VitalFormData[p]}
                          onChange={HandleOnChange}
                          readOnly={IsViewMode}
                          disabled={IsViewMode}
                        >
                          {p === "SupplementalOxygen" ? (
                            <>
                              <option value="">Select</option>
                              <option value="Yes">Yes</option>
                              <option value="No">No</option>
                            </>
                          ) : (
                            <>
                              <option value="">Select</option>
                              <option value="Alert">Alert</option>
                              <option value="Responsive to Voice">
                                V - Responsive to Voice
                              </option>
                              <option value="Responsive to Pain">
                                P - Responsive to Pain
                              </option>
                              <option value="Unresponsive">
                                U - Unresponsive
                              </option>
                            </>
                          )}
                        </select>
                      ) : (
                        <input
                          id={`${p}_${index}`}
                          autoComplete="off"
                          type={
                            p === "Date"
                              ? "date"
                              : p === "Time"
                              ? "time"
                              : "text"
                          }
                          name={p}
                          value={VitalFormData[p]}
                          readOnly={IsViewMode}
                          onChange={HandleOnChange}
                        />
                      )}
                    </div>
                  ))
                : null}

              <div className="Main_container_Btn">
                {IsViewMode && <button onClick={handleClear}>Clear</button>}
                {!IsViewMode && type === "Vital" && (
                  <button onClick={handleVitalFormSubmit}>Submit</button>
                )}
              </div>

              {type === "Vital" && (
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    textAlign: "center",
                    marginTop: "10px",
                    width: "100%",
                  }}
                >
                  <h2>
                    Vitals Score: {totalScore} ({scoreCategory})
                  </h2>
                </div>
              )}
            </div>

            <br />

            <div className="Main_container_Btn">
              <button onClick={() => setOpenModal2(false)}>Close</button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default OpNurse_Vitals;
