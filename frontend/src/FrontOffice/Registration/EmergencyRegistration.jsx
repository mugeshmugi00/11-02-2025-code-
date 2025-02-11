import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import axios from "axios";
import ToastAlert from "../../OtherComponent/ToastContainer/ToastAlert";
import { useNavigate } from "react-router-dom";
import { IoBedOutline } from "react-icons/io5";
import "../../App.css";
import IP_NurseMlc from "../../IP_Workbench/Nurse/IP_NurseMlc";
import RoomDetialsSelect from "./RoomDetialsSelect";
import Button from "@mui/material/Button";
import ReactGrid from "../../OtherComponent/ReactGrid/ReactGrid";

const EmergencyRegistration = () => {
  const UrlLink = useSelector((state) => state.userRecord?.UrlLink);
  const userRecord = useSelector((state) => state.userRecord?.UserData);
  const toast = useSelector((state) => state.userRecord?.toast);
  const dispatchvalue = useDispatch();
  const UserData = useSelector((state) => state.userRecord?.UserData);
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false); // State for modal visibility
  const Registeredit = useSelector((state) => state.Frontoffice?.Registeredit);
  const [errors, setErrors] = useState({});
  const [PatientRegisterDetails, setPatientRegisterDetails] = useState({});
  const AppointmentRegisType = "Emergency";
  console.log(PatientRegisterDetails, "PatientRegisterDetails");
  const [FilteredFormdataIpRoomDetials, setFilteredFormdataIpRoomDetials] =
    useState(null);

  const RegisterRoomShow = useSelector(
    (state) => state.Frontoffice?.RegisterRoomShow
  );
  const SelectRoomRegister = useSelector(
    (state) => state.Frontoffice?.SelectRoomRegister
  );
  const [PatientData, setPatientData] = useState([]);
  const [IsGetData, setIsGetData] = useState(false);

  const [EmgRegister, setEmgRegister] = useState({
    FirstName: "",
    PhoneNumber: "",
    Gender: "",
    IdentificationMark1: "",
    IdentificationMark2: "",
    IsConscious: "No",
    Instructions: "",
    IsMLC: "No",

    Building: null,
    Block: null,
    Floor: null,
    WardType: null,
    RoomNo: null,
    BedNo: null,
    RoomId: null,
  });

  const [RoomdeditalsShow, setRoomdeditalsShow] = useState({
    Building: "",
    Block: "",
    Floor: "",
    WardType: "",
    RoomNo: "",
    BedNo: "",
    RoomId: "",
  });

  const formatLabel = (label) => {
    if (/[a-z]/.test(label) && /[A-Z]/.test(label) && !/\d/.test(label)) {
      return label
        .replace(/([a-z])([A-Z])/g, "$1 $2")
        .replace(/^./, (str) => str.toUpperCase());
    } else {
      return label;
    }
  };

  const handleClear = () => {
    setEmgRegister({
      FirstName: "",
      Gender: "",
      PhoneNumber: "",
      IdentificationMark1: "",
      IdentificationMark2: "",
      IsConscious: "",
      Instructions: "",
      IsMLC: "",

      Building: null,
      Block: null,
      Floor: null,
      WardType: null,
      // RoomType: null,
      RoomNo: null,
      BedNo: null,
      RoomId: null,
    });

    setRoomdeditalsShow((prev) => ({
      ...prev,
      Building: "",
      Block: "",
      Floor: "",
      WardType: "",
      // RoomType: '',
      RoomNo: "",
      BedNo: "",
      RoomId: "",
    }));
  };

  const HandleOnchange = async (e) => {
    const { name, value, pattern } = e.target;

    const formattedValue = [
      "FirstName",
      "MiddleName",
      "SurName",
      "AliasName",
      "Occupation",
      "NextToKinName",
      "FamilyHeadName",
      "Street",
      "Area",
      "City",
      "District",
      "State",
      "Country",
    ].includes(name)
      ? `${value.charAt(0).toUpperCase()}${value.slice(1)}`
      : value;

    setRoomdeditalsShow((prev) => ({
      ...prev,
      [name]: formattedValue,
    }));
    const validateField = (value, pattern) => {
      if (!value) {
        return "Required";
      }
      if (pattern && !new RegExp(pattern).test(value)) {
        return "Invalid";
      } else {
        return "Valid";
      }
    };

    const error = validateField(value, pattern);
    console.log(error, "error");

    setErrors((prevErrors) => ({
      ...prevErrors,
      [name]: error,
    }));
  };

  useEffect(() => {
    let roomdata = Object.keys(EmgRegister).filter((p) =>
      [
        "Building",
        "Block",
        "Floor",
        "WardType",
        // 'RoomType',
        "RoomNo",
        "BedNo",
      ].includes(p)
    );
    setFilteredFormdataIpRoomDetials(roomdata);
  }, [EmgRegister]);

  useEffect(() => {
    if (Object.keys(SelectRoomRegister).length !== 0) {
      setEmgRegister((prev) => ({
        ...prev,
        Building: SelectRoomRegister.BuildingId,
        Block: SelectRoomRegister.BlockId,
        Floor: SelectRoomRegister.FloorId,
        WardType: SelectRoomRegister.WardId,
        // RoomType: SelectRoomRegister.RoomId,
        RoomNo: SelectRoomRegister.RoomNo,
        BedNo: SelectRoomRegister.BedNo,
        RoomId: SelectRoomRegister.id,
      }));
      setRoomdeditalsShow({
        Building: SelectRoomRegister.BuildingName,
        Block: SelectRoomRegister.BlockName,
        Floor: SelectRoomRegister.FloorName,
        WardType: SelectRoomRegister.WardName,
        // RoomType: SelectRoomRegister.RoomName,
        RoomNo: SelectRoomRegister.RoomNo,
        BedNo: SelectRoomRegister.BedNo,
        RoomId: SelectRoomRegister.RoomId,
      });
    }
  }, [SelectRoomRegister]);

  useEffect(() => {
    axios
      .get(`${UrlLink}Frontoffice/get_Emergency_patient_list`, {
        params: { status: "EmgPatientSaved" },
      })
      .then((res) => {
        const data = res.data;
        if (Array.isArray(data)) {
          setPatientData(data);
        } else {
          setPatientData([]);
        }
      })
      .catch((err) => {
        console.log(err);
      });
  }, [UrlLink, IsGetData]);

  //   useEffect(() => {
  //     axios.get(`${UrlLink}Frontoffice/get_Emergency_patient_list`,{params:{SavedStatus: 'EmgPatientSaved' }})
  //     .then((res) => {
  //         const data = res.data;
  //         if (Array.isArray(data)) {
  //             setPatientData(data);
  //         } else {
  //             setPatientData([]);
  //         }
  //     })
  //     .catch((err) => {
  //         console.log(err);
  //     });
  // }, [UrlLink,IsGetData]);

  const PatientRegisterColumns = [
    { key: "id", name: "ID" },
    { key: "PatientId", name: "Patient Id" },
    { key: "FullName", name: "Patient Name" },
    { key: "PhoneNo", name: "PhoneNo" },
    { key: "Gender", name: "Gender" },
    // { key: "Email", name: "Email" },
    {
      key: "Action",
      name: "Action",
      renderCell: (params) => {
        console.log(params.row, "params.row");

        return (
          <>
            <Button
              className="cell_btn"
              onClick={() => handleNavigateEmergency(params.row)} // Pass row data to handleNavigateEmg
            >
              Emg
            </Button>
            <Button
                className="cell_btn"
                onClick={() => handleNavigateOT(params.row)} // Pass row data to handleNavigateIP
              >
                OT
              </Button>
          </>
        );
      },
    },
  ];

  const handleSubmit = () => {
    // setLoading(true);
    // scrollToElement("RegisFormcon_11");

    // Define explicitly required fields
    const requiredFields = ["Gender"];

    let missingFields = [];

    // Identify missing fields from the explicitly required list
    requiredFields.forEach((field) => {
      if (!EmgRegister[field]) {
        missingFields.push(formatLabel(field)); // Assuming formatLabel formats field names for display
      }
    });

    console.log("missingFields", missingFields);

    // If any required fields are missing, show a warning
    if (missingFields.length > 0) {
      setLoading(false);
      const tdata = {
        message: `Please fill out the required fields: ${missingFields.join(
          ", "
        )}`,
        type: "warn",
      };
      dispatchvalue({ type: "toast", value: tdata });
    } else {
      const exist = Object.keys(errors).filter((p) => errors[p] === "Invalid");
      if (exist.length > 0) {
        setLoading(false);
        const tdata = {
          message: `please fill the field required pattern  :  ${exist.join(
            ","
          )}`,
          type: "warn",
        };
        dispatchvalue({ type: "toast", value: tdata });
      } else {
        const submitdata = {
          ...EmgRegister,
          Created_by: UserData?.username,
          Location: UserData?.location,
        };
        console.log("submitdata", submitdata);

        axios
          .post(
            `${UrlLink}Frontoffice/Emergency_Patient_Registration`,
            submitdata
          )
          .then((res) => {
            setLoading(false);

            console.log(res.data);
            const resData = res.data;
            console.log(resData, "resData");

            let typp = Object.keys(resData)[0];
            let mess = Object.values(resData)[0];
            const tdata = {
              message: mess,
              type: typp,
            };
            // dispatchvalue({ type: "Registeredit", value: {} });
            dispatchvalue({ type: "toast", value: tdata });
            handleClear();
            setIsGetData((prev) => !prev);

            setPatientRegisterDetails(resData.data[0]);

            dispatchvalue({ type: "PatientDetails", value: {} });
            dispatchvalue({ type: "Registeredit", value: {} });

            // dispatchvalue({ type: "HrFolder", value:"PatientManagement"});

            // navigate("/Home/FrontOfficeFolder");

            // console.log(dispatchvalue({ type: "HrFolder", value: "PatientManagement" }))
          })
          .catch((err) => {
            setLoading(false);
            console.log(err);
          });
      }
    }
  };

  // const handleNavigateEmergency = () => {
  //   dispatchvalue({ type: "HrFolder", value: "EmergencyPatientRoomRegistration" });
  //   dispatchvalue({ type: "PatientDetails", value: PatientRegisterDetails });
  //   navigate("/Home/FrontOfficeFolder");
  // }

  // const handleNavigateEmergency = async (row) => {
  //   try {
  //     const response = await axios.get(`${UrlLink}Frontoffice/Fetch_Register_Patients_Details`, {
  //       params: { PatientId: row.PatientId }, // Send PatientId as a query parameter
  //     });
  //     const patientData = response.data;
  //     console.log(patientData, "Fetched Patient Data for Emergency");
  //     dispatchvalue({ type: "HrFolder", value: "EmergencyPatientRoomRegistration" });
  //     dispatchvalue({ type: "PatientDetails", value: patientData });
  //     navigate("/Home/FrontOfficeFolder");
  //   } catch (error) {
  //     console.error("Error fetching patient data for Emergency:", error);
  //   }
  // };

  const handleNavigateEmergency = async (row) => {
    try {
      const response = await axios.get(
        `${UrlLink}Frontoffice/get_Emergency_Registration_edit_details`,
        {
          params: { RegistrationId: row.RegistrationId }, // Send PatientId as a query parameter
        }
      );
      const patientData = response.data;
      console.log(response.data, "response.data");

      console.log(patientData, "Fetched Patient Data for Emg");
      
      dispatchvalue({
        type: "HrFolder",
        value: "EmergencyPatientRoomRegistration",
      });

      dispatchvalue({ type: "PatientDetails", value: {...patientData,Department:'EMERGENCY'} });
      navigate("/Home/FrontOfficeFolder");
    } catch (error) {
      console.error("Error fetching patient data for OP:", error);
    }
  };


  const handleNavigateOT = async (params) => {  

    console.log(params,'otttttttttt');
    try {
      // const response = await axios.get(${UrlLink}Frontoffice/get_Emergency_Registration_edit_details, {
      //   params: { RegistrationId: row.RegistrationId }, // Send PatientId as a query parameter
      // });
      // const patientData = response.data;
      // console.log(response.data,'response.data');
      
      // console.log(patientData, "Fetched Patient Data for Emg");
      // dispatchvalue({ type: "HrFolder", value: "EmergencyPatientRoomRegistration" });
      // dispatchvalue({ type: "PatientDetails", value: patientData });
      navigate("/New_theater_booking", { state: { params }  });
    } catch (error) {
      console.error("Error fetching patient data for OP:", error);
    }
  };
  const adjustHeight = (e) => {
    e.target.style.height = "auto"; // Reset height to calculate scrollHeight
    e.target.style.height = `${e.target.scrollHeight}px`; // Set height to scrollHeight
  };


  return (
    <>
      <div className="Main_container_app">
        <h3>Emergency Registration</h3>
        <br />
        <div className="RegisFormcon" id="RegisFormcon_11">
          {Object.keys(EmgRegister)
            .filter(
              (p) =>
                ![
                  "Building",
                  "Block",
                  "Floor",
                  "WardType",
                  "RoomNo",
                  "BedNo",
                  "RoomId",
                  "IdentificationMark1",
                  "IdentificationMark2",
                  "Instructions",
                ].includes(p)
            )
            .map((field, indx) => (
              <div className="RegisForm_1" key={indx}>
                <label>
                  {formatLabel(field)} <span>:</span>
                </label>
                {field === "Gender" ? (
                  <select
                    name={field}
                    required
                    value={EmgRegister[field]}
                    onChange={(e) =>
                      setEmgRegister((prev) => ({
                        ...prev,
                        [field]: e.target.value,
                      }))
                    }
                  >
                    <option value="">Select</option>
                    {["Male", "Female", "TransGender"].map((row, indx) => (
                      <option key={indx} value={row}>
                        {row}
                      </option>
                    ))}
                  </select>
                ) : field === "IsMLC" || field === "IsConscious" ? (
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "flex-start",
                      width: "120px",
                      gap: "10px",
                    }}
                  >
                    <label style={{ width: "auto" }} htmlFor={`${field}_yes`}>
                      <input
                        required
                        id={`${field}_yes`}
                        type="radio"
                        name={`radio_${field}`}
                        value="Yes"
                        style={{ width: "15px" }}
                        checked={EmgRegister[field] === "Yes"}
                        onChange={(e) => {
                          setEmgRegister((prevState) => ({
                            ...prevState,
                            [field]: "Yes",
                          }));
                          if (field === "IsMLC") {
                            setShowModal(true);
                          }
                        }}
                      />
                      Yes
                    </label>

                    <label style={{ width: "auto" }} htmlFor={`${field}_no`}>
                      <input
                        required
                        id={`${field}_no`}
                        type="radio"
                        name={`radio_${field}`}
                        value="No"
                        style={{ width: "15px" }}
                        checked={EmgRegister[field] === "No"}
                        onChange={(e) => {
                          setEmgRegister((prevState) => ({
                            ...prevState,
                            [field]: "No",
                          }));
                          if (field === "IsMLC") {
                            setShowModal(false);
                          }
                        }}
                      />
                      No
                    </label>
                  </div>
                ) : (
                  <input
                    name={field}
                    required
                    type={field === "PhoneNumber" ? "number" : "text"}
                    onKeyDown={(e) =>
                      field === "PhoneNumber" &&
                      ["e", "E", "+", "-"].includes(e.key) &&
                      e.preventDefault()
                    }
                    value={EmgRegister[field]}
                    onChange={(e) => {
                      const { value } = e.target;
                      if (field === "PhoneNumber" && value.length > 10) return;
                      setEmgRegister((prev) => ({ ...prev, [field]: value }));
                    }}
                  />
                )}
              </div>
            ))}




</div>
<br />

          <div className="RegisFormcon extend_textarea_new">
            {/* Render the separated fields */}
            <div className="RegisForm_1 extend_textarea_new">
              <label>
                Identification Mark 1 <span>:</span>
              </label>
              <textarea
                name="IdentificationMark1"
                value={EmgRegister["IdentificationMark1"]}
                onChange={(e) =>{
                  setEmgRegister((prev) => ({
                    ...prev,
                    IdentificationMark1: e.target.value,
                  }));
                  adjustHeight(e); 

                }
                  
                }

                style={{
                  overflow: "hidden", 
                  resize: "none", 
                  minHeight: "60px", 
                }}

              />
            </div>
          </div>


<div className="RegisFormcon extend_textarea_new">
          <div className="RegisForm_1 extend_textarea_new">
            <label>
              Identification Mark 2 <span>:</span>
            </label>
            <textarea
              name="IdentificationMark2"
              value={EmgRegister["IdentificationMark2"]}
              onChange={(e) =>{
                setEmgRegister((prev) => ({
                  ...prev,
                  IdentificationMark2: e.target.value,
                }));
                adjustHeight(e); 


              }
              
              }

              style={{
                overflow: "hidden", 
                resize: "none", 
                minHeight: "60px", 
              }}

            />
          </div>

          </div>

          
<div className="RegisFormcon extend_textarea_new">
          <div className="RegisForm_1 extend_textarea_new">
            <label>
              Instructions <span>:</span>
            </label>
            <textarea
              name="Instructions"
              value={EmgRegister["Instructions"]}
              onChange={(e) =>{
                setEmgRegister((prev) => ({
                  ...prev,
                  Instructions: e.target.value,
                }));
                adjustHeight(e); 

              }
              }

              style={{
                overflow: "hidden", 
                resize: "none", 
                minHeight: "60px", 
              }}
              
            />
          </div>
          </div>


        
            <div className="DivCenter_container">Room Details </div>
            <div className="DivCenter_container" style={{
              justifyContent:'center'
            }}>
              <IoBedOutline
                className="HotelIcon_registration"
                onClick={() => {
                  if (
                    Object.keys(Registeredit).length !== 0 &&
                    !Registeredit?.conversion
                  ) {
                    const tdata = {
                      message:
                        "Unable to select the room because it is already selected and cannot be updated.",
                      type: "warn",
                    };
                    dispatchvalue({ type: "toast", value: tdata });
                  } else {
                    dispatchvalue({
                      type: "RegisterRoomShow",
                      value: { type: AppointmentRegisType, val: true },
                    });
                  }
                }}
              />
            </div>

            <div className="RegisFormcon">
            {FilteredFormdataIpRoomDetials &&
              FilteredFormdataIpRoomDetials.map((field, index) => (
                <div className="RegisForm_1" key={index}>
                  <label htmlFor={field}>
                    {formatLabel(field)}
                    <span>:</span>
                  </label>

                  <input
                    type="text"
                    disabled
                    id={`${field}_${index}`}
                    name={field}
                    value={RoomdeditalsShow[field]}
                    onChange={HandleOnchange}
                  />
                </div>
              ))}
              </div>
         
    

        {showModal && (
          <div
            className="sideopen_showcamera_profile"
            onClick={() => setShowModal(false)}
          >
            <div
              className="newwProfiles newwPopupforreason"
              onClick={(e) => e.stopPropagation()}
            >
              <h4>MLC Details</h4>
              <IP_NurseMlc />
            </div>
          </div>
        )}

        <div className="Main_container_Btn">
          <button onClick={handleSubmit}>Submit</button>
          {/* <button onClick={handleNavigateEmergency}>Emergency</button> */}
        </div>
        {/* {RegData.length > 0 &&
            <ReactGrid columns={EmgRegisterColumns} RowData={RegData} />
        } */}

        <ToastAlert Message={toast.message} Type={toast.type} />
        <ReactGrid columns={PatientRegisterColumns} RowData={PatientData} />

        {RegisterRoomShow.val && <RoomDetialsSelect />}
      </div>
    </>
  );
};

export default EmergencyRegistration;
