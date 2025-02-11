import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";
import { useSelector, useDispatch } from "react-redux";
import {
  differenceInYears,
  differenceInMonths,
  differenceInDays,
  addMonths,
  addYears,
  format,
  startOfYear,
  subYears,
  isBefore,
} from "date-fns";
import { useNavigate } from "react-router-dom";
import CameraAltIcon from "@mui/icons-material/CameraAlt";
import male from "../Assets/maledoctor.jpg";
import female from "../Assets/femaledoctor.jpg";
import PhotoCameraBackIcon from "@mui/icons-material/PhotoCameraBack";
import "../IP_Workbench/Nurse/jeeva.css";
import ModelContainer from "../OtherComponent/ModelContainer/ModelContainer";
import VisibilityIcon from "@mui/icons-material/Visibility";
import CameraswitchIcon from "@mui/icons-material/Cameraswitch";
import Webcam from "react-webcam";
import Skilset from "./Skilset";
import "./EmployeeRegistration.css";
import { useLocation } from "react-router-dom";
import ReactGrid from "../OtherComponent/ReactGrid/ReactGrid";
import Button from "@mui/material/Button";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import AddBoxIcon from "@mui/icons-material/AddBox";

const EmployeeRegistration = () => {
  const userRecord = useSelector((state) => state.userRecord?.UserData);
  console.log(userRecord, "userRecord");
  const navigate = useNavigate();
  const EmployeeListId = useSelector(
    (state) => state.Frontoffice?.EmployeeListId
  );
  const location = useLocation();

  const UrlLink = useSelector((state) => state.userRecord?.UrlLink);
  const dispatchvalue = useDispatch();
  const dispatch = useDispatch();

  const webcamRef1 = useRef(null);
  const [showFile, setShowFile] = useState({ file1: false });
  const [isImageCaptured1, setIsImageCaptured1] = useState(false);
  const [facingMode, setFacingMode] = useState("user");
  const [deviceInfo, setDeviceInfo] = useState({
    device_type: null,
    os_type: null,
  });

  const [skills, setSkills] = useState([]);
  const [newSkills, setNewSkills] = useState([]);
  const [viewMode, setViewMode] = useState(false);
  const [newSkillName, setNewSkillName] = useState("");

  const videoConstraints = { facingMode: facingMode };

  useEffect(() => {
    console.log("Webcam ref:", webcamRef1.current);
  }, []);

  const [FilteredFormdataAddress, setFilteredFormdataAddress] = useState(null);


  const [TitleNameData, setTitleNameData] = useState([]);
  const [BloodGroupData, setBloodGroupData] = useState([]);

  const [Category, setCategory] = useState([]);
  const [Speciality, setSpeciality] = useState([]);
  const [Departments, setDepartments] = useState([]);
  const [DepartmentData, setDepartmentData] = useState([]);
  const [selectDepartment, setSelectDepartment] = useState(false);
  const [selectDepModal, setselectDepModal] = useState({
    SelectDepartment: "",
  });
  const [Designations, setDesignations] = useState([]);
  const [Locations, setLocations] = useState([]);

  const [Classifications, setClassifications] = useState([]);
  const [Roles, setRoles] = useState([]);


  const [isPhoneValid, setIsPhoneValid] = useState({
    phone: false,
    alternatePhone: false,
    FatherContact: false,
    MotherContact: false,
    SpouseContact: false,
    EmergencyContactNo1: false,
    EmergencyContactNo2: false,
    WorkStationPhoneNo: false,
  });
  const [isEmailValid, setIsEmailValid] = useState(false);

  const [EmployeeformData, setEmployeeformData] = useState({
    Title: "",
    FirstName: "",
    MiddleName: "",
    SurName: "",
    gender: "",
    dob: "",
    Age: "",
    bloodgroup: "",
    phone: "",
    alternatePhone: "",

    email: "",
    qualification: "",
    SkillSet: [],
    IdProofType: "",
    IdProofNo: "",

    maritalStatus: "",
    MarriagePlan: "",
    AnniversaryDate: "",
    FatherName: "",
    FatherContact: "",
    FatherWorking: "",
    FatherWorkPlace: "",


    MotherName: "",
    MotherContact: "",
    MotherWorking: "",
    MotherWorkPlace: "",

    SpouseName: "",
    SpouseContact: "",
    SpouseWorking: "",
    SpouseWorkPlace: "",
    Child: "",
    TotalNoChild: "",
    // address
    doorNo: "",
    Street: "",
    Area: "",
    City: "",
    District: "",
    State: "",
    Country: "",
    Pincode: "",
    PermanentAddressSame: "YES",
    // PERMANENT ADDRESS
    PermanentdoorNo: "",
    PermanentStreet: "",
    PermanentArea: "",
    PermanentCity: "",
    PermanentDistrict: "",
    PermanentState: "",
    PermanentCountry: "",
    PermanentPincode: "",
    Residence: "",
    EmergencyContactName1: "",
    EmergencyContactName2: "",
    EmergencyContactNo1: "",
    EmergencyContactNo2: "",
    ActiveStatus: "Yes",
    RequirementSource: "",
    Source: "",
    Photo: null,
    CapturedImage1: null,
    Signature: null,

    // Medical Information..................

    PsychiatricMedicines: "",
    PsychiatricMedicinesDetails: "",
    PreviousOperation: "",
    SurgeriesDetails: "",
    VaccinationStatus: "",
    VaccinationStatusDetails: "",
    MedicalFitnessCertificate: null,
    AnnualMedicalCheckup: null,

    // Employeement History..................

    PreviousWorkExperience: "No",
    PreviousPfnumber: "No",
    PreviousESInumber: "No",
    PFnumber: "",
    ESInumber: "",
    NoOfYears: "",
    WorkStationNameAddress: "",
    WorkStationPhoneNo: "",
    ReasonForLeft: "",
    ConfirmedBy: "",
    EmployeePaySlip: null,
    EmployeeOfferLetter: null,
    EmployeeReliveLetter: null,

    // Current Employment ..................

    DateOfJoining: "",
    Category: "",
    Classification: "",
    Role: "",
    Speciality: "",
    Department: "",
    DepartmentId: "",
    Designation: "",
    Locations: "",
    // EmployeeId: "",
    WorkEmail: "",
    ReportingManager: "",
    GovtLeave: "",
    CasualLeave: "",
    SickLeave: "",
    TotalLeave: "",
    ProbationPeriod: "",
    months: "",
    years: "",
    TrainingGivenBy: "",
    TrainingVerifiedBy: "",
    TrainingCompletedDate: "",
    IsPF_Applicable: false,

    // Financial Information --------------------

    Salary: 0,
    BasicSalary: 0,
    Allowance: "",
    PfForEmployee: 12,
    SecurityDeposite: 0,
    FinalAllowance: 0,

    AccountHolderName: "",
    AccountNumber: "",
    BankName: "",
    Branch: "",
    IfscCode: "",
    PanNumber: "",
    UploadCsvFile: null,

    // Document Checklist --------------------

    Resume: null,
    PanCard: null,
    AadharCard: null,
    BankPassbook: null,
    ExperienceCertificate: null,
    MedicalFitness: null,
    Offerletter: null,
  });

  const [MedicalInformation, setMedicalInformation] = useState({
    Fit: false,
    Epilepsy: false,
    Ashthma: false,
    Dm: false,
    Ht: false,
    Ihd: false,
  });
  console.log("EmployeeformData", EmployeeformData);
  console.log('EmployeeListId', EmployeeListId)

  const handleCloseModal = () => {
    setShowskil(false);
  };

  const HandleDepartmentSelect = () => {

    setSelectDepartment(true);
  };

  const SelectDataColumn = [
    {
      key: "id",
      name: "Department Id",
    },
    {
      key: "SelectedDepartment",
      name: "Selected Department",
    },
    {
      key: "Action",
      name: "Action",
      renderCell: (params) => {
        return (
          <>
            <Button
              className="cell_btn"
              onClick={() => handleDeleteDepartments(params.row)}
            >
              <DeleteIcon className="check_box_clrr_cancell" />
            </Button>
          </>
        );
      },
    },
  ];

  const handleDeleteDepartments = (departmentId) => {
    console.log("Department ID to delete:", departmentId);
    const updatedDepartments = Departments.filter(
      (dep) => dep.id !== departmentId.id
    );
    console.log("Updated Departments after deletion:", updatedDepartments);
    setDepartments(updatedDepartments);

    // Update the DoctorProfessForm state with the remaining departments
    setEmployeeformData((prev) => ({
      ...prev,
      Department: updatedDepartments
        .map((dep) => dep.SelectedDepartment)
        .join(", "),
      DepartmentId: updatedDepartments.map((dep) => dep.id).join(", "),
    }));
  };

  const handleinpchangeDepartment = (e) => {
    const { name, value } = e.target;
    const formattedValue = value;
    setselectDepModal((prev) => ({
      ...prev,
      [name]: formattedValue,
    }));
  };
  // Save the selected department
  const handleDepartmentSave = () => {
    const selectedDepartment = DepartmentData.find(
      (dep) => dep.id === parseInt(selectDepModal.SelectDepartment)
    );

    if (selectedDepartment) {
      const departmentExists = Departments.some(
        (dep) => dep.id === selectedDepartment.id
      );

      if (departmentExists) {
        // Dispatch a warning toast
        const tdata = {
          message: "The Department is already Selected",
          type: "warn",
        };
        dispatchvalue({ type: "toast", value: tdata });
      } else {
        const updatedDepartments = [
          ...Departments,
          {
            id: selectedDepartment.id,
            SelectedDepartment: selectedDepartment.DepartmentName,
          },
        ];

        setDepartments(updatedDepartments);

        // Update the DoctorProfessForm state with a comma-separated string
        setEmployeeformData((prev) => ({
          ...prev,
          Department: updatedDepartments
            .map((dep) => dep.SelectedDepartment)
            .join(", "),
          DepartmentId: updatedDepartments.map((dep) => dep.id).join(", "),
        }));
      }
    }

    setselectDepModal({ SelectDepartment: "" }); // Reset after saving
  };

  const addSkill = () => {
    const skillName = newSkillName.trim();

    if (!skillName) {
      alert("Please enter a skill name.");
      return;
    }

    const normalizedSkillName = skillName.toLowerCase();
    if (
      skills.some((skill) => skill.name.toLowerCase() === normalizedSkillName)
    ) {
      alert("This skill already exists.");
      return;
    }

    // Add the new skill to the skills list
    setSkills((prevSkills) => [...prevSkills, { name: skillName, level: "" }]);

    // Clear the input field
    setNewSkillName(""); // Reset the input field by updating state
  };

  const deleteSkill = (index) => {
    if (window.confirm("Are you sure you want to delete this skill?")) {
      const updatedSkills = skills.filter((_, i) => i !== index);
      setSkills(updatedSkills);
    }
  };

  const updateSkillLevel = (index, level) => {
    const updatedSkills = skills.map((skill, i) =>
      i === index ? { ...skill, level } : skill
    );
    setSkills(updatedSkills);
  };

  const saveSkills = () => {
    // Validation: Ensure at least one skill is added
    if (skills.length === 0) {
      dispatch({
        type: "toast",
        value: {
          message: "Please add at least one skill before submitting.",
          type: "warn",
        },
      });
      return;
    }

    // Validation: Check for incomplete skills
    const incompleteSkills = skills.filter((skill) => !skill.level);
    if (incompleteSkills.length > 0) {
      dispatch({
        type: "toast",
        value: {
          message: `Please select a proficiency level for the following skills: ${incompleteSkills
            .map((skill) => skill.name)
            .join(", ")}`,
          type: "warn",
        },
      });
      return;
    }

    // Prepare data for submission
    const Data = { skills };

    console.log(Data, "Data to Submit");

    setEmployeeformData((prevState) => ({
      ...prevState,
      SkillSet: skills, // Add the skills array to the EmployeeformData
    }));

    setShowskil(false);
  };

  const handleViewClick = () => {
    // Merge saved skills and newly added skills
    const allSkills = [...(EmployeeformData.SkillSet || []), ...newSkills];
    setSkills(allSkills); // Update the skills state with merged data
    setShowskil(true); // Open the skill modal
    setViewMode(true); // Set the view mode to "read-only"
  };

  useEffect(() => {
    axios
      .get(`${UrlLink}Masters/Title_Master_link`)
      .then((res) => setTitleNameData(res.data))
      .catch((err) => console.log(err));

    axios
      .get(`${UrlLink}Masters/BloodGroup_Master_link`)
      .then((res) => setBloodGroupData(res.data))
      .catch((err) => console.log(err));

    axios
      .get(`${UrlLink}Masters/Category_Detials_link`)
      .then((res) => setCategory(res.data))
      .catch((err) => console.log(err));

    axios
      .get(`${UrlLink}Masters/Speciality_Detials_link`)
      .then((res) => setSpeciality(res.data))
      .catch((err) => console.log(err));

    axios
      .get(`${UrlLink}Masters/Department_Detials_link`)
      .then((res) => setDepartmentData(res.data))
      .catch((err) => console.log(err));

    axios
      .get(`${UrlLink}Masters/Designation_Detials_link`)
      .then((res) => setDesignations(res.data))
      .catch((err) => console.log(err));

    axios
      .get(`${UrlLink}Masters/Classification_Detials_link`)
      .then((res) => setClassifications(res.data))
      .catch((err) => console.log(err));

    axios
      .get(`${UrlLink}Masters/UserControl_Role_link`)
      .then((res) => setRoles(res.data))
      .catch((err) => console.log(err));

    axios
      .get(`${UrlLink}Masters/Location_Detials_link`)
      .then((res) => setLocations(res.data))
      .catch((err) => console.log(err));
  }, [UrlLink]);

  useEffect(() => {
    axios
      .get(`${UrlLink}patientmanagement/detect_device`)
      .then((response) => setDeviceInfo(response.data))
      .catch((error) => console.error(error));
  }, [UrlLink]);

  const switchCamera = () => {
    setFacingMode((prevMode) => (prevMode === "user" ? "environment" : "user"));
  };

  const handleRecaptureImage1 = () => {
    setEmployeeformData((prev) => ({
      ...prev,
      Photo: null,
    }));
    setIsImageCaptured1(false);
  };

  const dataURItoBlob = (dataURI) => {
    const byteString = atob(dataURI.split(",")[1]);
    const mimeString = dataURI.split(",")[0].split(":")[1].split(";")[0];
    const ab = new ArrayBuffer(byteString.length);
    const ia = new Uint8Array(ab);
    for (let i = 0; i < byteString.length; i++) {
      ia[i] = byteString.charCodeAt(i);
    }
    return new Blob([ab], { type: mimeString });
  };

  //important................

  useEffect(() => {
    console.log("Webcam reference:", webcamRef1.current);
  }, [webcamRef1.current]);

  const handleCaptureImage1 = () => {
    if (webcamRef1.current && webcamRef1.current.getScreenshot) {
      const file = webcamRef1.current.getScreenshot();

      if (file && file.length > 0) {
        const formattedValue = dataURItoBlob(file);

        const allowedTypes = ["application/pdf", "image/jpeg", "image/png"];
        const maxSize = 5 * 1024 * 1024;

        if (
          !allowedTypes.includes(formattedValue.type) ||
          formattedValue.type === ""
        ) {
          const tdata = {
            message:
              "Invalid file type. Please upload a PDF, JPEG, or PNG file.",
            type: "warn",
          };
          dispatch({ type: "toast", value: tdata });
        } else if (formattedValue.size > maxSize) {
          const tdata = {
            message: "File size exceeds the limit of 5MB.",
            type: "warn",
          };
          dispatch({ type: "toast", value: tdata });
        } else {
          const reader = new FileReader();
          reader.onload = () => {
            setEmployeeformData((prev) => ({
              ...prev,
              Photo: reader.result,
            }));
            setIsImageCaptured1(true);
          };
          reader.readAsDataURL(formattedValue);
        }
      } else {
        const tdata = {
          message:
            "Unable to capture the image. Please make sure the webcam is working.",
          type: "warn",
        };
        dispatch({ type: "toast", value: tdata });
      }
    } else {
      console.error(
        "Webcam reference is null or getScreenshot is not available."
      );
    }
  };

  const handleInputChange = (e) => {
    const { name, value, checked, type } = e.target;
    let formattedValue = value;
    let GapFormatValue = value.trim();

    // Capitalize the first letter for specific fields
    if (["FirstName", "MiddleName", "SurName", "AliasName"].includes(name)) {
      formattedValue = `${value.charAt(0).toUpperCase()}${value.slice(1)}`;
    }

    if (name === "dob") {
      const selectedDate = new Date(value);
      const age = differenceInYears(new Date(), selectedDate);
      setEmployeeformData((prev) => ({
        ...prev,
        dob: value,
        Age: age >= 0 && age <= 100 ? age : "",
      }));
      return; // Exit after handling dob
    }

    if (name === "Age") {
      const intAge = parseInt(value, 10);
      if (!isNaN(intAge) && intAge >= 0 && intAge <= 100) {
        const dobDate = subYears(new Date(), intAge);
        setEmployeeformData((prev) => ({
          ...prev,
          Age: intAge,
          dob: format(dobDate, "yyyy-MM-dd"),
        }));
      } else {
        setEmployeeformData((prev) => ({
          ...prev,
          Age: value,
          dob: "",
        }));
      }
      return; // Exit after handling Age
    }

    if (name === "Title") {
      setEmployeeformData((prev) => ({
        ...prev,
        [name]: value, // Assign original dropdown value to Title
        gender: ["Miss", "Ms", "Mrs"].includes(value)
          ? "Female"
          : ["Mr", "Master"].includes(value)
            ? "Male"
            : ["TransGender", "Baby", "Dr"].includes(value)
              ? "Transgender"
              : prev.gender, // Retain existing gender if no match
      }));
      return; // Exit after handling Title
    }
    if (name === "maritalStatus") {
      setEmployeeformData((prev) => ({
        ...prev,
        [name]: value,
        SpouseName: ["Married", "Widowed"].includes(value) ? prev.SpouseName : "",
        AnniversaryDate: value === "Married" ? prev.AnniversaryDate : "",  // Only keep AnniversaryDate if married
      }));
      return;
    }
    if (
      name === "phone" ||
      name === "alternatePhone" ||
      name === "FatherContact" ||
      name === "MotherContact" ||
      name === "SpouseContact" ||
      name === "EmergencyContactNo1" ||
      name === "EmergencyContactNo2" ||
      name === "WorkStationPhoneNo"
    ) {
      if (GapFormatValue.length <= 10) {
        setEmployeeformData((prev) => ({
          ...prev,
          [name]: GapFormatValue,
        }));

        // Update validity for the specific field
        setIsPhoneValid((prev) => ({
          ...prev,
          [name]: GapFormatValue.length === 10,
        }));
      } else {
        setIsPhoneValid((prev) => ({
          ...prev,
          [name]: false,
        }));
      }
      return;
    }

    if (name === "email") {
      const isGmail = value.endsWith("@gmail.com");
      setEmployeeformData((prev) => ({
        ...prev,
        email: value,
      }));
      setIsEmailValid(isGmail); // Update email validity
      return; // Exit after handling email
    }

    if (name === "Salary") {
      if (value === "" || parseFloat(value) === 0) {
        // If CTC is empty or zero, reset BasicSalary and GrossSalary
        setEmployeeformData((prev) => ({
          ...prev,
          [name]: value, // Clear CTC
          BasicSalary: 0, // Clear BasicSalary
        }));
      } else {
        // Calculate Basic Salary (assuming 40% of CTC is Basic Salary)
        const ctcValue = parseFloat(value) * 100000;
        const basicSalary = ((ctcValue / 12) * 0.6).toFixed(2);
        setEmployeeformData((prev) => ({
          ...prev,
          [name]: value,
          BasicSalary: basicSalary,
        }));
      }
    }
    if (name === "Residence") {

      setEmployeeformData((prev) => ({
        ...prev,
        [name]: value,
      }));
    }
    if (name === "Pincode") {
      setEmployeeformData((prev) => ({
        ...prev,
        [name]: value,
      }));
    }

    if (name === "PermanentAddressSame" && value === "NO") {
      if (name === "PermanentdoorNo" || name === "PermanentStreet" || name === "PermanentArea" || name === "PermanentCity" || name === "PermanentCountry" || name === "PermanentPincode") {
        setEmployeeformData((prev) => ({
          ...prev,
          [name]: value,
        }));
      }



    } else if (name === "PermanentAddressSame" && value === "YES") {
      setEmployeeformData((prev) => ({
        ...prev,
        PermanentdoorNo: '',
        PermanentStreet: '',
        PermanentArea: '',
        PermanentCity: '',
        PermanentDistrict: '',
        PermanentState: '',
        PermanentCountry: '',
        PermanentPincode: '',
      }));
    }

    if (type === "checkbox") {
      setEmployeeformData((prev) => ({
        ...prev,
        [name]: checked, // Use `checked` to toggle true/false
      }));
      return;
    }

    if (name === "ProbationPeriod") {
      setEmployeeformData((prev) => ({
        ...prev,
        [name]: formattedValue,
      }));

      if (value === "No") {
        // Reset probation-related fields and disable PF
        setEmployeeformData((prev) => ({
          ...prev,
          IsPF_Applicable: false,
          TrainingCompletedDate: "",
          TrainingVerifiedBy: "",
          TrainingGivenBy: "",
          years: "",
          months: "",
        }));
      }
      return;
    }

    
    if (name === "PfForEmployee" && EmployeeformData.IsPF_Applicable) {
      setEmployeeformData((prev) => ({
        ...prev,
        [name]: value, // Update PfForEmployee only if IsPF_Applicable is checked
      }));
    } else if (name === "PfForEmployee" && !EmployeeformData.IsPF_Applicable) {
      setEmployeeformData((prev) => ({
        ...prev,
        [name]: "", 
      }));
    }
    

    // Handle all other fields normally
    setEmployeeformData((prev) => ({
      ...prev,
      [name]: formattedValue,
    }));




    setEmployeeformData((prev) => ({
      ...prev,
      [name]: formattedValue,
    }));
  };

  const handleMedicalInformationInputChange = (event) => {
    const { name, checked } = event.target;
    setMedicalInformation((prevData) => ({
      ...prevData,
      [name]: checked,
    }));
  };





  useEffect(() => {
    if (EmployeeformData.Pincode.length > 5 && !EmployeeListId?.Employee) {
      axios
        .get(`${UrlLink}Frontoffice/get_location_by_pincode?pincode=${EmployeeformData.Pincode}`)
        .then((response) => {
          const { country, state, city, district } = response.data;
          setEmployeeformData((prev) => ({
            ...prev,
            Country: country || '',
            State: state || '',
            City: city || '',
            District: district || '',
          }));
        })
        .catch((err) => {
          console.error('Error fetching pincode details:', err);
        });
    }
  }, [EmployeeformData.Pincode, EmployeeListId]);

  // Effect for permanent address Pincode when "PermanentAddressSame" is "NO"
  useEffect(() => {
    if (EmployeeformData.PermanentAddressSame === "NO" && EmployeeformData.PermanentPincode.length > 5 && !EmployeeListId?.Employee) {
      axios
        .get(`${UrlLink}Frontoffice/get_location_by_pincode?pincode=${EmployeeformData.PermanentPincode}`)
        .then((response) => {
          const data = response.data;

          const { country, state, city, district } = data;
          setEmployeeformData((prev) => ({
            ...prev,
            PermanentCountry: country || '',
            PermanentState: state || '',
            PermanentCity: city || '',
            PermanentDistrict: district || '',
          }));
        })
        .catch((err) => {
          console.error("Error fetching permanent pincode details:", err);
        });
    }
  }, [EmployeeformData.PermanentAddressSame, EmployeeformData.PermanentPincode, EmployeeListId]); // Dependencies for PermanentAddressSame and PermanentPincode


  const handleInputChange1 = (e) => {
    const { name, value } = e.target;

    // Update the form state for the changed field
    setEmployeeformData((prev) => ({
      ...prev,
      [name]: value, // Update the specific field (value will be dynamic)
    }));
  };

  // useEffect to handle the calculation of GrossSalary whenever relevant fields change
  useEffect(() => {
    const {
      Allowance,
      BasicSalary,
    } = EmployeeformData;

    // If Basic Salary is not set or is zero, skip further calculations
    const basicSalary = parseFloat(BasicSalary);
    if (isNaN(basicSalary) || basicSalary === 0) return;

    // Check if any allowance field is empty or 0 and treat them as 0
    const HRA = parseFloat(Allowance) || 0;


    // Calculate each allowance as a percentage of Basic Salary
    const HRA_value = (basicSalary * (HRA / 100)).toFixed(2);


    // Convert them to numbers (if the result is a valid number)
    const HRA_final = isNaN(parseFloat(HRA_value)) ? 0 : parseFloat(HRA_value);


    // Calculate the Gross Salary by summing all components
    const grossSalary =
      basicSalary +
      HRA_final;



    setEmployeeformData((prev) => ({
      ...prev,
      FinalAllowance: HRA_final,
    }));
  }, [
    EmployeeformData.Allowance,
    EmployeeformData.BasicSalary,
  ]); // Dependency array, only rerun when one of these fields changes

  const handleChangeGovtLeave = (e) => {
    const value = e.target.value;
    setEmployeeformData((prevData) => ({
      ...prevData,
      GovtLeave: value,
      TotalLeave: calculateTotalLeave(value, prevData.CasualLeave),
    }));
  };

  const handleChangeCasualLeave = (e) => {
    const value = e.target.value;
    setEmployeeformData((prevData) => ({
      ...prevData,
      CasualLeave: value,
      TotalLeave: calculateTotalLeave(prevData.GovtLeave, value),
    }));
  };
  const handleChangeSickLeave = (e) => {
    const value = e.target.value;
    setEmployeeformData((prevData) => ({
      ...prevData,
      SickLeave: value,
      TotalLeave: calculateTotalLeave(
        prevData.GovtLeave,
        prevData.CasualLeave,
        value
      ),
    }));
  };

  const calculateTotalLeave = (GovtLeave, CasualLeave, SickLeave) => {
    const GovtLeaveValue = parseInt(GovtLeave) || 0;
    const CasualLeaveValue = parseInt(CasualLeave) || 0;
    const SickLeaveValue = parseInt(SickLeave) || 0;
    return GovtLeaveValue + CasualLeaveValue + SickLeaveValue;
  };

  const Selectedfileview = (fileval) => {
    if (fileval) {
      let tdata = {
        Isopen: false,
        content: null,
        type: "image/jpg",
      };
      if (
        ["data:image/jpeg;base64", "data:image/jpg;base64"].includes(
          fileval?.split(",")[0]
        )
      ) {
        tdata = {
          Isopen: true,
          content: fileval,
          type: "image/jpeg",
        };
      } else if (fileval?.split(",")[0] === "data:image/png;base64") {
        tdata = {
          Isopen: true,
          content: fileval,
          type: "image/png",
        };
      } else if (fileval?.split(",")[0] === "data:application/pdf;base64") {
        tdata = {
          Isopen: true,
          content: fileval,
          type: "application/pdf",
        };
      }

      dispatch({ type: "modelcon", value: tdata });
    } else {
      const tdata = {
        message: "There is no file to view.",
        type: "warn",
      };
      dispatch({ type: "toast", value: tdata });
    }
  };

  const handleinpchangeDocumentsForm = (e) => {
    const { name, files } = e.target;

    // Ensure that files exist and are not empty
    if (files && files.length > 0) {
      const formattedValue = files[0];

      // Optional: Add validation for file type and size
      const allowedTypes = ["application/pdf", "image/jpeg", "image/png"]; // Example allowed types
      const maxSize = 5 * 1024 * 1024; // Example max size of 5MB
      if (
        !allowedTypes.includes(formattedValue.type) ||
        formattedValue.type === ""
      ) {
        // Dispatch a warning toast or handle file type validation
        const tdata = {
          message: "Invalid file type. Please upload a PDF, JPEG, or PNG file.",
          type: "warn",
        };
        dispatch({ type: "toast", value: tdata });
      } else if (formattedValue.size > maxSize) {
        // Dispatch a warning toast or handle file size validation
        const tdata = {
          message: "File size exceeds the limit of 5MB.",
          type: "warn",
        };
        dispatch({ type: "toast", value: tdata });
      } else {
        const reader = new FileReader();
        reader.onload = () => {
          setEmployeeformData((prev) => ({
            ...prev,
            [name]: reader.result,
          }));
        };
        reader.readAsDataURL(formattedValue);
      }
    } else {
      // Handle case where no file is selected
      const tdata = {
        message: "No file selected. Please choose a file to upload.",
        type: "warn",
      };
      dispatch({ type: "toast", value: tdata });
    }
  };

  const [showskil, setShowskil] = useState(false);

  const handleClear = () => {
    setEmployeeformData({});
    setMedicalInformation({});
  };

  useEffect(() => {
    const Employee = EmployeeListId?.Employee_Id;
    if (Employee) {
      axios
        .get(`${UrlLink}HR_Management/Get_Employee_Registered_Details`, {
          params: { Employee },
        })
        .then((res) => {
          const data = res.data;
          console.log(data);
          console.log(data.Department);
          console.log(data.departments);

          const department =
            (data.Department).split(",") || [];
          const departmentId = data.departments.split(",");
          console.log("id", departmentId);
          console.log("name", department);
          // Map each department ID to its corresponding department name
          const departmentData = departmentId.map((id, index) => ({
            id: id.trim(), // Trim to remove any leading/trailing whitespace
            SelectedDepartment: department[index]?.trim(), // Trim department name and ensure it's mapped correctly
          }));

          // Log the mapped department data for verification
          console.log("Mapped Department Data:", departmentData);

          // Set the mapped department data to the state
          setDepartments(departmentData);

          const EmployeeHistory = data.EmployeeHistory[0] || {};
          const EmployeeSkillset = data.EmployeeSkillset || [];
          const EmployeeMedicalInfo = data.EmployeeMedicalInfo[0] || {};
          const EmployeeCurrentDetails = data.EmployeeCurrentDetails[0] || {};
          const EmployeeFinancialHistory =
            data.EmployeeFinancialHistory[0] || {};
          const EmployeeDocumentChecklist =
            data.EmployeeDocumentChecklist[0] || {};

          console.log(EmployeeSkillset, "EmployeeSkillset");

          const medicalConditions =
            EmployeeMedicalInfo?.PreExisiting_Medical_Condition?.split(",") ||
            [];
          const mappedMedicalConditions = {
            Fit: medicalConditions.includes("Fit"),
            Epilepsy: medicalConditions.includes("Epilepsy"),
            Ashthma: medicalConditions.includes("Ashthma"),
            Dm: medicalConditions.includes("Dm"),
            Ht: medicalConditions.includes("Ht"),
            Ihd: medicalConditions.includes("Ihd"),
          };

          if (data) {
            console.log("data", data);
            setEmployeeformData((prev) => ({
              ...prev,
              Title: data.Title || "",
              FirstName: data.FirstName || "",
              MiddleName: data.MiddleName || "",
              SurName: data.LastName || "",
              gender: data.Gender || "",
              dob: data.DOB || "",
              Age: data.Age || "",
              bloodgroup: data.BloodGroup || "",
              phone: data.Phone || "",
              alternatePhone: data.Alternate_Number || "",
              email: data.Email || "",
              qualification: data.Qualification || "",
              SkillSet: EmployeeSkillset.map((skill) => ({
                name: skill.skill_name,
                level: skill.skill_level,
              })),
              IdProofType: data.IdProofType || "",
              IdProofNo: data.IdProofNo || "",
              maritalStatus: data.Marital_Status || "",
              AnniversaryDate: data.AnniversaryDate || "",
              Residence: data.Residence || "",
              MarriagePlan: data.MarriagePlan || "",
              FatherName: data.FatherName || "",
              FatherContact: data.FatherContact || "",
              FatherWorking: data.FatherWorking || "",
              FatherWorkPlace: data.FatherWorkPlace || "",
              MotherName: data.MotherName || "",
              MotherContact: data.MotherContact || "",
              MotherWorking: data.MotherWorking || "",
              MotherWorkPlace: data.MotherWorkPlace || "",
              SpouseName: data.Spouse_Name || "",
              SpouseContact: data.SpouseContact || "",
              SpouseWorking: data.SpouseWorking || "",
              SpouseWorkPlace: data.SpouseWorkPlace || "",
              Child: data.Child || "",
              TotalNoChild: data.TotalNoChild || "",
              doorNo: data.DoorNo || "",
              Street: data.Street || "",
              Area: data.Area || "",
              City: data.City || "",
              District: data.District || "",
              State: data.State || "",
              Country: data.Country || "",
              Pincode: data.Pincode || "",
              PermanentAddressSame: data.PermanentAddressSameAsAbove || '',
              PermanentdoorNo: data.PermanentDoorNo || '',
              PermanentStreet: data.PermanentStreet || '',
              PermanentArea: data.PermanentArea || '',
              PermanentCity: data.PermanentCity || '',
              PermanentDistrict: data.PermanentDistrict || '',
              PermanentState: data.PermanentState || '',
              PermanentCountry: data.PermanentCountry || '',
              PermanentPincode: data.PermanentPincode || '',
              Category: data?.Category || "",
              Speciality: data?.Speciality || "",
              Department: department || "",
              DepartmentId: data?.departments || '',
              Designation: data?.Designation || "",
              Classification: data?.Classification || "",
              Role: data?.Role || "",
              EmergencyContactName1: data.EmergencyContactName1 || "",
              EmergencyContactName2: data.EmergencyContactName2 || "",
              EmergencyContactNo1: data.EmergencyContactNo1 || "",
              EmergencyContactNo2: data.EmergencyContactNo2 || "",
              ActiveStatus: data.ActiveStatus || "",
              RequirementSource: data.RequirementSource || "",
              Source: data.Source || "",
              Photo: data.Photo || null,
              Signature: data.Signature || null,
              CaptureImage1: data.CaptureImage1 || null,

              PreviousWorkExperience:
                EmployeeHistory?.PreviousWorkExperience || "",
              PreviousPfnumber: EmployeeHistory?.PreviousWorkPFNumber || "",
              PreviousESInumber: EmployeeHistory?.PreviousWorkESINumber || "",
              PFnumber: EmployeeHistory?.PFNumber || "",
              ESInumber: EmployeeHistory?.ESINumber || "",
              NoOfYears: EmployeeHistory?.NoOfYears || "",
              WorkStationNameAddress:
                EmployeeHistory?.WorkStationNameAddress || "",
              ReasonForLeft: EmployeeHistory?.ReasonForLeft || "",
              WorkStationPhoneNo: EmployeeHistory?.WorkStationPhoneNo || "",
              EmployeePaySlip: EmployeeHistory?.EmployeePaySlip || null,
              EmployeeOfferLetter: EmployeeHistory?.EmployeeOfferLetter || null,
              EmployeeReliveLetter:
                EmployeeHistory?.EmployeeReliveLetter || null,
              ConfirmedBy: EmployeeHistory?.ConfirmedBy || "",

              // PreExisiting_Medical_Condition: EmployeeMedicalInfo?.PreExisiting_Medical_Condition || '',

              PsychiatricMedicines:
                EmployeeMedicalInfo?.PsychiatricMedicines || "",
              PsychiatricMedicinesDetails:
                EmployeeMedicalInfo?.PsychiatricMedicinesDetails || "",
              PreviousOperation: EmployeeMedicalInfo?.PreviousOperation || "",
              SurgeriesDetails: EmployeeMedicalInfo?.SurgeriesDetails || "",
              VaccinationStatus: EmployeeMedicalInfo?.VaccinationStatus || "",
              VaccinationStatusDetails:
                EmployeeMedicalInfo?.VaccinationStatusDetails || "",
              MedicalFitnessCertificate:
                EmployeeMedicalInfo?.MedicalFitnessCertificate || "",
              AnnualMedicalCheckup:
                EmployeeMedicalInfo?.AnnualMedicalCheckup || "",

              DateOfJoining: EmployeeCurrentDetails?.DateOfJoining || "",
              Locations:
                EmployeeCurrentDetails?.CurrentEmployeementLocations || "",
              ReportingManager: EmployeeCurrentDetails?.ReportingManager || "",
              GovtLeave: EmployeeCurrentDetails?.GovtLeave || "",
              CasualLeave: EmployeeCurrentDetails?.CasualLeave || "",
              SickLeave: EmployeeCurrentDetails?.SickLeave || "",
              TotalLeave: EmployeeCurrentDetails?.TotalLeave || "",
              WorkEmail: EmployeeCurrentDetails?.WorkEmail || "",
              ProbationPeriod: EmployeeCurrentDetails?.ProbationPeriod || "",
              months: EmployeeCurrentDetails?.Months || "",
              years: EmployeeCurrentDetails?.Years || "",
              TrainingGivenBy: EmployeeCurrentDetails?.TrainingGivenBy || "",
              TrainingVerifiedBy:
                EmployeeCurrentDetails?.TrainingVerifiedBy || "",
              TrainingCompletedDate:
                EmployeeCurrentDetails?.TrainingCompletedDate || "",
              IsPF_Applicable: EmployeeCurrentDetails?.IsPF_Applicable || "No",
              BasicSalary: EmployeeFinancialHistory?.BasicSalary || 0,
              Salary: EmployeeFinancialHistory?.Salary || "",
              Allowance: EmployeeFinancialHistory?.Allowance || "",
              PfForEmployee: EmployeeFinancialHistory?.PfForEmployee || "",
              SecurityDeposite: EmployeeFinancialHistory?.SecurityDeposite || "",
              AccountHolderName:
                EmployeeFinancialHistory?.AccountHolderName || "",
              AccountNumber: EmployeeFinancialHistory?.AccountNumber || "",
              BankName: EmployeeFinancialHistory?.BankName || "",
              Branch: EmployeeFinancialHistory?.Branch || "",
              IfscCode: EmployeeFinancialHistory?.IfscCode || "",
              PanNumber: EmployeeFinancialHistory?.PanNumber || "",
              UploadCsvFile: EmployeeFinancialHistory?.UploadCsvFile || null,
              FinalAllowance: EmployeeFinancialHistory?.FinalAllowance || "",
              Resume: EmployeeDocumentChecklist?.Resume || null,
              PanCard: EmployeeDocumentChecklist?.PanCard || null,
              AadharCard: EmployeeDocumentChecklist?.AadharCard || null,
              BankPassbook: EmployeeDocumentChecklist?.BankPassbook || null,
              ExperienceCertificate:
                EmployeeDocumentChecklist?.ExperienceCertificate || null,
              MedicalFitness: EmployeeDocumentChecklist?.MedicalFitness || null,
              Offerletter: EmployeeDocumentChecklist?.Offerletter || null,
            }));
            setMedicalInformation((prev) => ({
              ...prev,
              ...mappedMedicalConditions,
            }));
          }
        });
    }
  }, [UrlLink, EmployeeListId]);

  const handleSubmit = async () => {
    // Combine EmployeeformData and other necessary data
    const Data = {
      ...EmployeeformData,
      Createdby: userRecord?.username,
      Location: userRecord?.location,
      Employee_Id: EmployeeListId?.Employee_Id || "",
      PreExistingMedicalCondition: Object.keys(MedicalInformation)
        .filter((key) => MedicalInformation[key]) // Filter out keys with truthy values
        .join(","), // Join the keys with commas
    };

    console.log(Data, "Datakkkkkkkkkkkk");

    // List of required fields
    const requiredFields = [
      "FirstName",
      "Title",
      "dob",
      "Age",
      "gender",
      "phone",

      "Designation",
    ];

    const emptyFields = requiredFields.filter(
      (field) => !EmployeeformData[field]
    );

    if (emptyFields.length > 0) {
      alert(`The following fields are required: ${emptyFields.join(", ")}`);
      return;
    }

    try {
      // Send a POST request with the JSON payload
      const response = await axios.post(
        `${UrlLink}HR_Management/Employee_Registration_Details`,
        Data // Send plain JSON object
      );

      // Handle response
      const [type, message] = [
        Object.keys(response.data)[0],
        Object.values(response.data)[0],
      ];
      dispatch({ type: "toast", value: { message, type } });
      navigate("/Home/EmployeeRegistrationList");
      dispatchvalue({ type: "EmployeeListId", value: "" });
      dispatchvalue({ type: "HrFolder", value: "EmployeeRegistrationList" });
    } catch (error) {
      console.error("Error during submission:", error);
    }
  };

  return (
    <div className="Main_container_app">
      <h3>New Employee Register</h3>

      {/* PERSONAL DETAILS =============================/ */}
      <div className="DivCenter_container">Personal Details</div>
      <br />

      <div className="RegisFormcon">
        <div className="RegisForm_1">
          <label htmlFor="Title">
            Title <span>:</span>
          </label>
          <select
            id="Title"
            name="Title"
            value={EmployeeformData.Title}
            onChange={handleInputChange}
          >
            <option value="">Select</option>
            {TitleNameData.map((row, indx) => (
              <option key={indx} value={row.id}>
                {row.Title}
              </option>
            ))}
          </select>
        </div>
        <div className="RegisForm_1">
          <label>
            First Name <span>:</span>
          </label>
          <input
            type="text"
            name="FirstName"
            value={EmployeeformData.FirstName}
            onChange={handleInputChange}
          />
        </div>
        <div className="RegisForm_1">
          <label>
            Middle Name <span>:</span>
          </label>
          <input
            type="text"
            name="MiddleName"
            value={EmployeeformData.MiddleName}
            onChange={handleInputChange}
          />
        </div>
        <div className="RegisForm_1">
          <label>
            Sur Name <span>:</span>
          </label>
          <input
            type="text"
            name="SurName"
            value={EmployeeformData.SurName}
            onChange={handleInputChange}
          />
        </div>
        <div className="RegisForm_1">
          <label>
            Gender <span>:</span>
          </label>
          <select
            name="gender"
            value={EmployeeformData.gender}
            onChange={handleInputChange}
          >
            <option value="">Select</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Transgender">TransGender</option>
          </select>
        </div>

        <div className="RegisForm_1">
          <label>
            DOB <span>:</span>
          </label>
          <input
            type="date"
            name="dob"
            value={EmployeeformData.dob}
            onChange={handleInputChange}
          />
        </div>

        <div className="RegisForm_1">
          <label>
            Age <span>:</span>
          </label>
          <input
            type="number"
            name="Age"
            onKeyDown={(e) =>
              ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()
            }
            value={EmployeeformData.Age}
            onChange={handleInputChange}
          />
        </div>

        <div className="RegisForm_1">
          <label>
            Blood Group <span>:</span>
          </label>
          <select
            name="bloodgroup"
            id="bloodgroup"
            value={EmployeeformData.bloodgroup}
            onChange={handleInputChange}
          >
            <option value="">Select</option>
            {BloodGroupData.map((row, indx) => (
              <option key={indx} value={row.id}>
                {row.BloodGroup}
              </option>
            ))}
          </select>
        </div>

        <div class="RegisForm_1">
          <label>
            Phone <span>:</span>
          </label>
          <input
            type="number"
            name="phone"
            onKeyDown={(e) =>
              ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()
            }
            pattern="[0-9]*"
            className={isPhoneValid.phone ? "valid-label" : "invalid-label"}
            value={EmployeeformData.phone}
            onChange={handleInputChange}
            required
          />
        </div>

        <div class="RegisForm_1">
          <label>
            Alternate Phone<span>:</span>
          </label>
          <input
            type="number"
            onKeyDown={(e) =>
              ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()
            }
            name="alternatePhone"
            pattern="[0-9]*"
            value={EmployeeformData.alternatePhone}
            className={
              isPhoneValid.alternatePhone ? "valid-label" : "invalid-label"
            }
            onChange={handleInputChange}
            required
          />
        </div>

        <div className="RegisForm_1">
          <label>
            Email <span>:</span>
          </label>
          <input
            type="email"
            name="email"
            pattern="[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}"
            value={EmployeeformData.email}
            className={isEmailValid ? "valid-label" : "invalid-label"}
            onChange={handleInputChange}
          />
        </div>

        <div className="RegisForm_1">
          <label>
            Qualification <span>:</span>
          </label>
          <input
            type="text"
            name="qualification"
            value={EmployeeformData.qualification}
            onChange={handleInputChange}
            required
          />
        </div>
        <div className="RegisForm_1">
          <label>
            Skills Set <span>:</span>
          </label>
          <button
            className="fileviewbtn"
            value={EmployeeformData.SkillSet}
            onClick={() => {
              setSkills([]); // Clear current skills for adding new ones
              setShowskil(true);
              setViewMode(false); // Set the mode to Select (editable)
            }}
          >
            Select
          </button>
          <button
            className="RegisterForm_1_btns choose_file_update"
            onClick={handleViewClick} // Use the handleViewClick function to merge and show skills
          >
            <VisibilityIcon />
          </button>
        </div>

        {showskil && (
          <div className="modal-container" onClick={handleCloseModal}>
            <div className="pop_v_up" onClick={(e) => e.stopPropagation()}>
              <div className="table-container_v7">
                {/* View Table - Displays Saved Skills (Read-Only) */}
                {viewMode && (
                  <div>
                    <h2>View Saved Skills</h2>
                    <table className="styled-table">
                      <thead>
                        <tr>
                          <th>Skill</th>
                          <th>Level</th>
                        </tr>
                      </thead>
                      <tbody>
                        {skills.length > 0 ? (
                          skills.map((skill, index) => (
                            <tr key={index}>
                              <td>{skill.name}</td>
                              <td>{skill.level}</td>
                            </tr>
                          ))
                        ) : (
                          <tr>
                            <td colSpan="2">No skills added yet.</td>
                          </tr>
                        )}
                      </tbody>
                    </table>
                  </div>
                )}

                {/* Select Table - Allows Editing and Adding New Skills */}
                {!viewMode && (
                  <div>
                    <h2>Select Skills</h2>
                    <div className="skvinput">
                      <label htmlFor="new-skill">
                        Add Skill:&nbsp;&nbsp;&nbsp;
                      </label>
                      <input
                        type="text"
                        id="new-skill"
                        placeholder="Enter new skill"
                        value={newSkillName} // Bind value to the state
                        onChange={(e) => setNewSkillName(e.target.value)}
                      // onChange={(e) => updateSkillLevel(e.target.value)} // Update new skill state
                      />
                      <button type="button" onClick={addSkill}>
                        Add New
                      </button>
                    </div>

                    <table className="styled-table">
                      <thead>
                        <tr>
                          <th>Skill</th>
                          <th>Beginner</th>
                          <th>Intermediate</th>
                          <th>Expert</th>
                          <th>Action</th>
                        </tr>
                      </thead>
                      <tbody>
                        {skills.length > 0 ? (
                          skills.map((skill, index) => (
                            <tr key={index}>
                              <td>{skill.name}</td>
                              <td>
                                <input
                                  type="radio"
                                  name={`level-${index}`}
                                  value="Beginner"
                                  checked={skill.level === "Beginner"}
                                  onChange={() =>
                                    updateSkillLevel(index, "Beginner")
                                  }
                                />
                              </td>
                              <td>
                                <input
                                  type="radio"
                                  name={`level-${index}`}
                                  value="Intermediate"
                                  checked={skill.level === "Intermediate"}
                                  onChange={() =>
                                    updateSkillLevel(index, "Intermediate")
                                  }
                                />
                              </td>
                              <td>
                                <input
                                  type="radio"
                                  name={`level-${index}`}
                                  value="Expert"
                                  checked={skill.level === "Expert"}
                                  onChange={() =>
                                    updateSkillLevel(index, "Expert")
                                  }
                                />
                              </td>
                              <td>
                                <button
                                  type="button"
                                  onClick={() => deleteSkill(index)}
                                  style={{
                                    padding: "5px 10px",
                                    backgroundColor: "#f44336",
                                    color: "white",
                                    border: "none",
                                    borderRadius: "4px",
                                    cursor: "pointer",
                                  }}
                                >
                                  X
                                </button>
                              </td>
                            </tr>
                          ))
                        ) : (
                          <tr>
                            <td colSpan="5">No skills added yet.</td>
                          </tr>
                        )}
                      </tbody>
                    </table>

                    <button
                      onClick={saveSkills}
                      style={{
                        marginTop: "20px",
                        padding: "10px 20px",
                        backgroundColor: "#2196F3",
                        color: "white",
                        border: "none",
                        borderRadius: "4px",
                        cursor: "pointer",
                      }}
                    >
                      Submit
                    </button>
                  </div>
                )}

                {/* Close Button */}
                <button
                  onClick={() => setShowskil(false)}
                  style={{
                    marginTop: "20px",
                    padding: "10px 20px",
                    backgroundColor: "#2196F3",
                    color: "white",
                    border: "none",
                    borderRadius: "4px",
                    cursor: "pointer",
                  }}
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        )}

        <div class="RegisForm_1">
          <label>
            Id Proof Type <span>:</span>
          </label>
          <select
            name="IdProofType"
            value={EmployeeformData.IdProofType}
            onChange={handleInputChange}
            required
          >
            <option value="">Select</option>
            <option value="Aadhar">Aadhar</option>
            <option value="VoterId">Voter ID</option>
            <option value="SmartCard">SmartCard</option>
            <option value="PanCard">PanCard</option>
          </select>
        </div>

        {EmployeeformData.IdProofType && (
          <div className="RegisForm_1">
            <label>
              Id Proof No <span>:</span>
            </label>
            <input
              type="text"
              name="IdProofNo"
              value={EmployeeformData.IdProofNo}
              onChange={handleInputChange}
            />
          </div>
        )}

        <div class="RegisForm_1">
          <label>
            Marital Status <span>:</span>
          </label>
          <select
            name="maritalStatus"
            value={EmployeeformData.maritalStatus}
            onChange={handleInputChange}
            required
          >
            <option value="">Select</option>
            <option value="Single">Single</option>
            <option value="Married">Married</option>
            <option value="Divorced">Divorced</option>
            <option value="Widowed">Widowed</option>
          </select>
        </div>

        {["Married", "Widowed"].includes(EmployeeformData.maritalStatus) && (
          <>
            <div className="RegisForm_1">
              <label>
                Spouse Name <span>:</span>
              </label>
              <input
                type="text"
                name="SpouseName"
                value={EmployeeformData.SpouseName}
                onChange={handleInputChange}
              />
            </div>

            <div className="RegisForm_1">
              <label>
                Contact No <span>:</span>
              </label>
              <input
                type="number"
                name="SpouseContact"
                onKeyDown={(e) =>
                  ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()
                }
                value={EmployeeformData.SpouseContact}
                className={
                  isPhoneValid.SpouseContact ? "valid-label" : "invalid-label"
                }
                onChange={handleInputChange}
              />
            </div>

            <div className="RegisForm_1">
              <label>
                Working <span>:</span>
              </label>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  width: "150px",
                }}
              >
                <label style={{ width: "auto" }} htmlFor="SpouseWorking_yes">
                  <input
                    required
                    id="SpouseWorking_yes"
                    type="radio"
                    name="SpouseWorking"
                    value="Yes"
                    style={{ width: "15px" }}
                    checked={EmployeeformData.SpouseWorking === "Yes"}
                    onChange={handleInputChange}
                  />
                  Yes
                </label>
                <label style={{ width: "auto" }} htmlFor="SpouseWorking_no">
                  <input
                    required
                    id="SpouseWorking_no"
                    type="radio"
                    name="SpouseWorking"
                    value="No"
                    style={{ width: "15px" }}
                    checked={EmployeeformData.SpouseWorking === "No"}
                    onChange={handleInputChange}
                  />
                  No
                </label>
              </div>
            </div>

            {EmployeeformData.SpouseWorking === "Yes" && (
              <div className="RegisForm_1">
                <label>Spouse Working Place :</label>
                <input
                  type="text"
                  name="SpouseWorkPlace"
                  value={EmployeeformData.SpouseWorkPlace}
                  onChange={handleInputChange}
                />
              </div>
            )}

            <div className="RegisForm_1">
              <label>
                Child <span>:</span>
              </label>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  width: "150px",
                }}
              >
                <label style={{ width: "auto" }} htmlFor="Child_yes">
                  <input
                    required
                    id="Child_yes"
                    type="radio"
                    name="Child"
                    value="Yes"
                    style={{ width: "15px" }}
                    checked={EmployeeformData.Child === "Yes"}
                    onChange={handleInputChange}
                  />
                  Yes
                </label>
                <label style={{ width: "auto" }} htmlFor="Child_no">
                  <input
                    required
                    id="Child_no"
                    type="radio"
                    name="Child"
                    value="No"
                    style={{ width: "15px" }}
                    checked={EmployeeformData.Child === "No"}
                    onChange={handleInputChange}
                  />
                  No
                </label>
              </div>
            </div>

            {EmployeeformData.Child === "Yes" && (
              <div className="RegisForm_1">
                <label>
                  Total No Child <span>:</span>
                </label>
                <input
                  type="text"
                  name="TotalNoChild"
                  value={EmployeeformData.TotalNoChild}
                  onChange={handleInputChange}
                />
              </div>
            )}
          </>
        )}

        {["Married", "Widowed", "Divorced"].includes(EmployeeformData.maritalStatus) && (
          <>
            <div className="RegisForm_1">
              <label>
                Anniversary Date <span>:</span>
              </label>
              <input
                type="date"
                name="AnniversaryDate"
                value={EmployeeformData.AnniversaryDate}
                onChange={handleInputChange}
              />
            </div>
          </>
        )}


        {["Single", "Divorced"].includes(EmployeeformData.maritalStatus) && (
          <>
            {EmployeeformData.maritalStatus === "Single" && (
              <div className="RegisForm_1">
                <label>
                  MarriagePlan <span>:</span>
                </label>
                <input
                  type="text"
                  name="MarriagePlan"
                  value={EmployeeformData.MarriagePlan}
                  onChange={handleInputChange}
                />
              </div>
            )}

            <div className="RegisForm_1">
              <label>
                Father Name <span>:</span>
              </label>
              <input
                type="text"
                name="FatherName"
                value={EmployeeformData.FatherName}
                onChange={handleInputChange}
              />
            </div>

            <div className="RegisForm_1">
              <label>
                Contact No <span>:</span>
              </label>
              <input
                type="number"
                onKeyDown={(e) =>
                  ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()
                }
                name="FatherContact"
                value={EmployeeformData.FatherContact}
                className={
                  isPhoneValid.FatherContact ? "valid-label" : "invalid-label"
                }
                onChange={handleInputChange}
              />
            </div>

            <div className="RegisForm_1">
              <label>
                FatherWorking <span>:</span>
              </label>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  width: "150px",
                }}
              >
                <label style={{ width: "auto" }} htmlFor="FatherWorking_yes">
                  <input
                    required
                    id="FatherWorking_yes"
                    type="radio"
                    name="FatherWorking"
                    value="Yes"
                    style={{ width: "15px" }}
                    checked={EmployeeformData.FatherWorking === "Yes"}
                    onChange={handleInputChange}
                  />
                  Yes
                </label>
                <label style={{ width: "auto" }} htmlFor="FatherWorking_no">
                  <input
                    required
                    id="FatherWorking_no"
                    type="radio"
                    name="FatherWorking"
                    value="No"
                    style={{ width: "15px" }}
                    checked={EmployeeformData.FatherWorking === "No"}
                    onChange={handleInputChange}
                  />
                  No
                </label>
              </div>
            </div>

            {EmployeeformData.FatherWorking === "Yes" && (
              <div className="RegisForm_1">
                <label>
                  Father Working Place <span>:</span>
                </label>
                <input
                  type="text"
                  name="FatherWorkPlace"
                  value={EmployeeformData.FatherWorkPlace}
                  onChange={handleInputChange}
                />
              </div>
            )}

            <div className="RegisForm_1">
              <label>
                Mother Name <span>:</span>
              </label>
              <input
                type="text"
                name="MotherName"
                value={EmployeeformData.MotherName}
                onChange={handleInputChange}
              />
            </div>

            <div className="RegisForm_1">
              <label>
                Contact No <span>:</span>
              </label>
              <input
                type="number"
                onKeyDown={(e) =>
                  ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()
                }
                name="MotherContact"
                value={EmployeeformData.MotherContact}
                className={
                  isPhoneValid.MotherContact ? "valid-label" : "invalid-label"
                }
                onChange={handleInputChange}
              />
            </div>

            <div className="RegisForm_1">
              <label>
                Mother Working <span>:</span>
              </label>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  width: "150px",
                }}
              >
                <label style={{ width: "auto" }} htmlFor="MotherWorking_yes">
                  <input
                    required
                    id="MotherWorking_yes"
                    type="radio"
                    name="MotherWorking"
                    value="Yes"
                    style={{ width: "15px" }}
                    checked={EmployeeformData.MotherWorking === "Yes"}
                    onChange={handleInputChange}
                  />
                  Yes
                </label>
                <label style={{ width: "auto" }} htmlFor="MotherWorking_no">
                  <input
                    required
                    id="MotherWorking_no"
                    type="radio"
                    name="MotherWorking"
                    value="No"
                    style={{ width: "15px" }}
                    checked={EmployeeformData.MotherWorking === "No"}
                    onChange={handleInputChange}
                  />
                  No
                </label>
              </div>
            </div>

            {EmployeeformData.MotherWorking === "Yes" && (
              <div className="RegisForm_1">
                <label>
                  Working Place <span>:</span>
                </label>
                <input
                  type="text"
                  name="MotherWorkPlace"
                  value={EmployeeformData.MotherWorkPlace}
                  onChange={handleInputChange}
                />
              </div>
            )}

            {EmployeeformData.maritalStatus === "Divorced" && (
              <>
                <div className="RegisForm_1">
                  <label>
                    Child <span>:</span>
                  </label>
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      width: "150px",
                    }}
                  >
                    <label style={{ width: "auto" }} htmlFor="Child_yes">
                      <input
                        required
                        id="Child_yes"
                        type="radio"
                        name="Child"
                        value="Yes"
                        style={{ width: "15px" }}
                        checked={EmployeeformData.Child === "Yes"}
                        onChange={handleInputChange}
                      />
                      Yes
                    </label>
                    <label style={{ width: "auto" }} htmlFor="Child_no">
                      <input
                        required
                        id="Child_no"
                        type="radio"
                        name="Child"
                        value="No"
                        style={{ width: "15px" }}
                        checked={EmployeeformData.Child === "No"}
                        onChange={handleInputChange}
                      />
                      No
                    </label>
                  </div>
                </div>

                {EmployeeformData.Child === "Yes" && (
                  <div className="RegisForm_1">
                    <label>
                      Total No Child <span>:</span>
                    </label>
                    <input
                      type="text"
                      name="TotalNoChild"
                      value={EmployeeformData.TotalNoChild}
                      onChange={handleInputChange}
                    />
                  </div>
                )}
              </>
            )}
          </>
        )}


        <div className="RegisForm_1">
          <label>
            Emergency ContactName 1<span>:</span>
          </label>
          <input
            type="text"
            name="EmergencyContactName1"
            value={EmployeeformData.EmergencyContactName1}
            onChange={handleInputChange}
            required
          />
        </div>
        <div className="RegisForm_1">
          <label>
            Emergency ContactNo 1<span>:</span>
          </label>
          <input
            type="number"
            name="EmergencyContactNo1"
            value={EmployeeformData.EmergencyContactNo1}
            className={
              isPhoneValid.EmergencyContactNo1 ? "valid-label" : "invalid-label"
            }
            onKeyDown={(e) =>
              ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()
            }
            onChange={handleInputChange}
            required
          />
        </div>

        <div className="RegisForm_1">
          <label>
            Emergency ContactName 2<span>:</span>
          </label>
          <input
            type="text"
            name="EmergencyContactName2"
            value={EmployeeformData.EmergencyContactName2}
            onChange={handleInputChange}
            required
          />
        </div>
        <div className="RegisForm_1">
          <label>
            Emergency ContactNo 2 <span>:</span>
          </label>
          <input
            type="number"
            onKeyDown={(e) =>
              ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()
            }
            name="EmergencyContactNo2"
            value={EmployeeformData.EmergencyContactNo2}
            className={
              isPhoneValid.EmergencyContactNo2 ? "valid-label" : "invalid-label"
            }
            onChange={handleInputChange}
            required
          />
        </div>
        <div className="RegisForm_1">
          <label>
            Residence <span>:</span>
          </label>
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              width: "150px",
            }}
          >
            <label style={{ width: "auto" }} htmlFor="Residence_dayscholar">
              <input
                required
                id="Residence_dayscholar"
                type="radio"
                name="Residence"
                value="Day Scholar"
                style={{ width: "15px" }}
                checked={EmployeeformData.Residence === "Day Scholar"}
                onChange={handleInputChange}
              />
              Day Scholar
            </label>
            <label style={{ width: "auto" }} htmlFor="Residence_hostel">
              <input
                required
                id="Residence_hostel"
                type="radio"
                name="Residence"
                value="Hostel"
                style={{ width: "15px" }}
                checked={EmployeeformData.Residence === "Hostel"}
                onChange={handleInputChange}
              />
              Hostel
            </label>
          </div>
        </div>


        <div className="RegisForm_1">
          <label>
            Photo <span>:</span>
          </label>

          <div className="RegisterForm_2">
            {/* Button to show the webcam or captured image */}
            <button
              onClick={() => setShowFile({ file1: true })}
              className="RegisterForm_1_btns choose_file_update"
            >
              <CameraAltIcon />
            </button>

            {/* Webcam/captured image interface */}
            {showFile.file1 && (
              <div
                className="showcamera_takepic"
                onClick={() => setShowFile({ file1: false })}
              >
                <div
                  className="showcamera_1_takepic1"
                  onClick={(e) => e.stopPropagation()}
                >
                  {EmployeeformData.Photo ? (
                    <div>
                      <img
                        src={EmployeeformData.Photo}
                        alt="Captured"
                        className="captured-image11"
                      />
                      <div className="web_btn">
                        <button
                          onClick={handleRecaptureImage1}
                          className="btncon_add"
                        >
                          Update Image
                        </button>
                        <button
                          onClick={() => setShowFile({ file1: false })}
                          className="btncon_add"
                        >
                          Close
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div className="camera-container">
                      <div className="web_head">
                        <h3>Image</h3>
                      </div>
                      <div className="RotateButton_canva">
                        <Webcam
                          audio={false}
                          ref={webcamRef1}
                          screenshotFormat="image/jpeg"
                          mirrored={facingMode === "user"}
                          className="web_cam"
                          videoConstraints={videoConstraints}
                        />
                        {deviceInfo.device_type !== "mobile" && (
                          <button onClick={switchCamera}>
                            <CameraswitchIcon />
                          </button>
                        )}
                      </div>
                      <div className="web_btn">
                        <button
                          onClick={handleCaptureImage1}
                          className="btncon_add"
                        >
                          Capture
                        </button>
                        <button
                          onClick={() => setShowFile({ file1: false })}
                          className="btncon_add"
                        >
                          Close
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* File input and view controls */}
          <div style={{ display: "flex", alignItems: "center" }}>
            <input
              type="file"
              name="Photo"
              accept="image/jpeg, image/png, application/pdf"
              required
              id="Photo"
              autoComplete="off"
              onChange={handleinpchangeDocumentsForm}
              style={{ display: "none" }}
            />
            <div
              style={{
                width: "87px",
                display: "flex",
                justifyContent: "flex-start",
                gap: "10px",
              }}
            >
              <label
                htmlFor="Photo"
                className="RegisterForm_1_btns choose_file_update"
              >
                <PhotoCameraBackIcon />
              </label>
              <button
                className="RegisterForm_1_btns choose_file_update"
                onClick={() => {
                  Selectedfileview(EmployeeformData.Photo);
                }}
              >
                <VisibilityIcon />
              </button>
            </div>
          </div>
        </div>

        <div className="RegisForm_1">
          <label>
            Signature<span>:</span>
          </label>
          <div className="RegisterForm_2">
            <input
              type="file"
              name={"Signature"}
              accept="image/jpeg, image/png, application/pdf"
              required
              id={"Signature"}
              autoComplete="off"
              onChange={handleinpchangeDocumentsForm}
              //   readOnly={IsViewMode}
              style={{ display: "none" }}
            />
            <div
              style={{
                width: "120px",
                display: "flex",
                justifyContent: "flex-start",
                gap: "20px",
              }}
            >
              <label
                htmlFor={"Signature"}
                className="RegisterForm_1_btns choose_file_update"
              >
                <PhotoCameraBackIcon />
              </label>
              <button
                className="RegisterForm_1_btns choose_file_update"
                onClick={() => Selectedfileview(EmployeeformData.Signature)}
              >
                <VisibilityIcon />
              </button>
            </div>
          </div>
        </div>

        <div className="RegisForm_1">
          <label>
            {" "}
            RequirementSource <span>:</span>{" "}
          </label>

          <select
            name="RequirementSource"
            required
            value={EmployeeformData.RequirementSource}
            onChange={handleInputChange}
          >
            <option value="">Select</option>
            <option value="Advertisement">Advertisement</option>
            <option value="SocialMedia">Social Media</option>
            <option value="Refferal">Refferal</option>
            <option value="Walkin">Walk in</option>
          </select>
        </div>
        {EmployeeformData.RequirementSource &&
          EmployeeformData.RequirementSource !== "Select" && (
            <div className="RegisForm_1">
              <label>
                Source <span>:</span>
              </label>
              <input
                type="text"
                name="Source"
                value={EmployeeformData.Source}
                onChange={handleInputChange}
                placeholder={`details for ${EmployeeformData.RequirementSource}`}
              />
            </div>
          )}

        <div className="RegisForm_1">
          <label>
            Active Status <span>:</span>
          </label>
          <div
            style={{
              display: "flex",
              justifyContent: "flex-start",
              width: "120px",
              gap: "10px",
            }}
          >
            <label style={{ width: "auto" }} htmlFor="ActiveStatus_yes">
              <input
                required
                id="ActiveStatus_yes"
                type="radio"
                name="ActiveStatus"
                value="Yes"
                style={{ width: "15px" }}
                checked={EmployeeformData.ActiveStatus === "Yes"}
                onChange={handleInputChange}
              />
              Yes
            </label>
            <label style={{ width: "auto" }} htmlFor="ActiveStatus_no">
              <input
                required
                id="ActiveStatus_no"
                type="radio"
                name="ActiveStatus"
                value="No"
                style={{ width: "15px" }}
                checked={EmployeeformData.ActiveStatus === "No"}
                onChange={handleInputChange}
              />
              No
            </label>
          </div>
        </div>
      </div>
      {/* personal details End =========== */}
      <br />
      {/* {employee communication address} */}
      <div className="DivCenter_container">Communication Address</div>
      <br></br>
      <div className="RegisFormcon">

        <div className="RegisForm_1">
          <label>
            Pincode <span>:</span>
          </label>
          <input
            type="number"
            name="Pincode"
            pattern="\d{6,7}"  // Direct pattern for 6 to 7 digits
            autoComplete="off"
            onKeyDown={(e) => ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()}
            value={EmployeeformData.Pincode}
            onChange={handleInputChange}
          />
        </div>

        <div className="RegisForm_1">
          <label>
            Door No<span>:</span>
          </label>
          <input
            type="text"
            name="doorNo"
            value={EmployeeformData.doorNo}
            onChange={handleInputChange}
            required
          />
        </div>

        <div className="RegisForm_1">
          <label>
            Street<span>:</span>
          </label>
          <input
            type="text"
            name="Street"
            value={EmployeeformData.Street}
            onChange={handleInputChange}
            required
          />
        </div>

        <div className="RegisForm_1">
          <label>
            Area<span>:</span>
          </label>
          <input
            type="text"
            name="Area"
            value={EmployeeformData.Area}
            onChange={handleInputChange}
            required
          />
        </div>

        <div className="RegisForm_1">
          <label>
            City<span>:</span>
          </label>
          <input
            type="text"
            name="City"
            value={EmployeeformData.City}
            onChange={handleInputChange}
            required
          />
        </div>

        <div className="RegisForm_1">
          <label>
            District<span>:</span>
          </label>
          <input
            type="text"
            name="District"
            value={EmployeeformData.District}
            onChange={handleInputChange}
            required
          />
        </div>
        <div className="RegisForm_1">
          <label>
            State<span>:</span>
          </label>
          <input
            type="text"
            name="State"
            value={EmployeeformData.State}
            onChange={handleInputChange}
            required
          />
        </div>

        <div className="RegisForm_1">
          <label>
            Country<span>:</span>
          </label>
          <input
            type="text"
            name="Country"
            value={EmployeeformData.Country}
            onChange={handleInputChange}
            required
          />
        </div>
        <div className="RegisForm_1">
          <label>
            Permanent Address Same As Above <span>:</span>
          </label>
          <div
            style={{
              display: "flex",
              justifyContent: "flex-start",
              width: "120px",
              gap: "10px",
            }}
          >
            <label style={{ width: "auto" }} htmlFor="Residence_dayscholar">
              <input
                required
                type="radio"
                name="PermanentAddressSame"
                value="YES"
                style={{ width: "15px" }}
                checked={EmployeeformData.PermanentAddressSame === "YES"}
                onChange={handleInputChange}
              />
              Yes
            </label>
            <label style={{ width: "auto" }} htmlFor="Residence_hostel">
              <input
                type="radio"
                name="PermanentAddressSame"
                value="NO"
                style={{ width: "15px" }}
                checked={EmployeeformData.PermanentAddressSame === "NO"}
                onChange={handleInputChange}
              />
              No
            </label>
          </div>
        </div>



      </div>
      <br />

      {/* ==================employee permanent address */}
      {EmployeeformData.PermanentAddressSame === "NO" && (
        <>
          <div className="DivCenter_container">Permanent Address</div>
          <br />
          <div className="RegisFormcon">
            <div className="RegisForm_1">
              <label>
                Pincode <span>:</span>
              </label>
              <input
                type="number"
                name="PermanentPincode"
                pattern="\d{6,7}" // Direct pattern for 6 to 7 digits
                autoComplete="off"
                onKeyDown={(e) => ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()}
                value={EmployeeformData.PermanentPincode}
                onChange={handleInputChange}
              />
            </div>

            <div className="RegisForm_1">
              <label>
                Door No <span>:</span>
              </label>
              <input
                type="text"
                name="PermanentdoorNo"
                value={EmployeeformData.PermanentdoorNo}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="RegisForm_1">
              <label>
                Street <span>:</span>
              </label>
              <input
                type="text"
                name="PermanentStreet"
                value={EmployeeformData.PermanentStreet}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="RegisForm_1">
              <label>
                Area <span>:</span>
              </label>
              <input
                type="text"
                name="PermanentArea"
                value={EmployeeformData.PermanentArea}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="RegisForm_1">
              <label>
                City <span>:</span>
              </label>
              <input
                type="text"
                name="PermanentCity"
                value={EmployeeformData.PermanentCity}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="RegisForm_1">
              <label>
                District <span>:</span>
              </label>
              <input
                type="text"
                name="PermanentDistrict"
                value={EmployeeformData.PermanentDistrict}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="RegisForm_1">
              <label>
                State <span>:</span>
              </label>
              <input
                type="text"
                name="PermanentState"
                value={EmployeeformData.PermanentState}
                onChange={handleInputChange}
                required
              />
            </div>

            <div className="RegisForm_1">
              <label>
                Country <span>:</span>
              </label>
              <input
                type="text"
                name="PermanentCountry"
                value={EmployeeformData.PermanentCountry}
                onChange={handleInputChange}
                required
              />
            </div>
          </div>
          <br />
        </>
      )}


      {/* Employeement History  ========================== / */}

      <div className="DivCenter_container">Employeement History</div>
      <br />

      <div className="RegisFormcon">
        <div className="RegisForm_1">
          <label>
            Previous Work Experience <span>:</span>
          </label>
          <div
            style={{
              display: "flex",
              justifyContent: "flex-start",
              width: "120px",
              gap: "10px",
            }}
          >
            <label
              style={{ width: "auto" }}
              htmlFor="PreviousWorkExperience_yes"
            >
              <input
                required
                id="PreviousWorkExperience_yes"
                type="radio"
                name="PreviousWorkExperience"
                value="Yes"
                style={{ width: "15px" }}
                checked={EmployeeformData.PreviousWorkExperience === "Yes"}
                onChange={handleInputChange}
              />
              Yes
            </label>
            <label
              style={{ width: "auto" }}
              htmlFor="PreviousWorkExperience_no"
            >
              <input
                required
                id="PreviousWorkExperience_no"
                type="radio"
                name="PreviousWorkExperience"
                value="No"
                style={{ width: "15px" }}
                checked={EmployeeformData.PreviousWorkExperience === "No"}
                onChange={handleInputChange}
              />
              No
            </label>
          </div>
        </div>

        {EmployeeformData.PreviousWorkExperience === "Yes" && (
          <>
            <div className="RegisForm_1">
              <label>
                No.Of Years<span>:</span>
              </label>
              <input
                type="number"
                name="NoOfYears"
                onKeyDown={(e) =>
                  ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()
                }
                value={EmployeeformData.NoOfYears}
                onChange={handleInputChange}
              />
            </div>

            <div className="RegisForm_1">
              <label>
                WorkStation Name & Address<span>:</span>
              </label>
              <input
                type="text"
                name="WorkStationNameAddress"
                value={EmployeeformData.WorkStationNameAddress}
                // placeholder='WorkStationNameAddress'
                onChange={handleInputChange}
              />
            </div>

            <div className="RegisForm_1">
              <label>
                Reason For Left<span>:</span>
              </label>
              <select
                name="ReasonForLeft"
                value={EmployeeformData.ReasonForLeft}
                onChange={handleInputChange}
                required
              >
                <option value="">Select</option>
                <option value="Better Opportunity">Better Opportunity</option>
                <option value="Department/Hospital issue">
                  Department/Hospital issue
                </option>
                <option value="Salary Concern">Salary Concern</option>
                <option value="Personal Reason">Personal Reason</option>
                <option value="Relocation">Relocation</option>
                <option value="Health">Health</option>
                <option value="Further Studies">Further Studies</option>
                <option value="without Notice">without Notice</option>
              </select>
            </div>

            <div className="RegisForm_1">
              <label>
                Company Contact No <span>:</span>
              </label>
              <input
                type="number"
                name="WorkStationPhoneNo"
                value={EmployeeformData.WorkStationPhoneNo}
                className={
                  isPhoneValid.WorkStationPhoneNo
                    ? "valid-label"
                    : "invalid-label"
                }
                onChange={handleInputChange}
              />
            </div>


            <div className="RegisForm_1">
              <label>
                Pay Slip CSV <span>:</span>
              </label>
              <div className="RegisterForm_2">
                <input
                  type="file"
                  name={"EmployeePaySlip"}
                  accept="image/jpeg, image/png, application/pdf"
                  required
                  id={"EmployeePaySlip"}
                  autoComplete="off"
                  onChange={handleinpchangeDocumentsForm}
                  //   readOnly={IsViewMode}
                  style={{ display: "none" }}
                />
                <div
                  style={{
                    width: "87px",
                    display: "flex",
                    justifyContent: "flex-start",
                    gap: "10px",
                  }}
                >
                  <label
                    htmlFor={"EmployeePaySlip"}
                    className="RegisterForm_1_btns choose_file_update"
                  >
                    <PhotoCameraBackIcon />
                  </label>
                  <button
                    className="RegisterForm_1_btns choose_file_update"
                    onClick={() =>
                      Selectedfileview(EmployeeformData.EmployeePaySlip)
                    }
                  >
                    <VisibilityIcon />
                  </button>
                </div>
              </div>
            </div>



            <div className="RegisForm_1">
              <label>
                Offer Letter<span>:</span>
              </label>
              <div className="RegisterForm_2">
                <input
                  type="file"
                  name={"EmployeeOfferLetter"}
                  accept="image/jpeg, image/png, application/pdf"
                  required
                  id={"EmployeeOfferLetter"}
                  autoComplete="off"
                  onChange={handleinpchangeDocumentsForm}
                  style={{ display: "none" }}
                />
                <div
                  style={{
                    width: "87px",
                    display: "flex",
                    justifyContent: "flex-start",
                    gap: "10px",
                  }}
                >
                  <label
                    htmlFor={"EmployeeOfferLetter"}
                    className="RegisterForm_1_btns choose_file_update"
                  >
                    <PhotoCameraBackIcon />
                  </label>
                  <button
                    className="RegisterForm_1_btns choose_file_update"
                    onClick={() =>
                      Selectedfileview(EmployeeformData.EmployeeOfferLetter)
                    }
                  >
                    <VisibilityIcon />
                  </button>
                </div>
              </div>
            </div>


            <div className="RegisForm_1">
              <label>
                {" "}
                Relieve Letter <span>:</span>{" "}
              </label>
              <div className="RegisterForm_2">
                <input
                  type="file"
                  name={"EmployeeReliveLetter"}
                  accept="image/jpeg, image/png, application/pdf"
                  required
                  id={"EmployeeReliveLetter"}
                  autoComplete="off"
                  onChange={handleinpchangeDocumentsForm}
                  style={{ display: "none" }}
                />
                <div
                  style={{
                    width: "87px",
                    display: "flex",
                    justifyContent: "flex-start",
                    gap: "10px",
                  }}
                >
                  <label
                    htmlFor={"EmployeeReliveLetter"}
                    className="RegisterForm_1_btns choose_file_update"
                  >
                    <PhotoCameraBackIcon />
                  </label>
                  <button
                    className="RegisterForm_1_btns choose_file_update"
                    onClick={() =>
                      Selectedfileview(EmployeeformData.EmployeeReliveLetter)
                    }
                  >
                    <VisibilityIcon />
                  </button>
                </div>
              </div>
            </div>

            <div className="RegisForm_1">
              <label>
                Confirmed By<span>:</span>
              </label>
              <input
                type="text"
                name="ConfirmedBy"
                value={EmployeeformData.ConfirmedBy}
                onChange={handleInputChange}
              />
            </div>
            <div className="RegisForm_1">
              <label>
                Do you have PF Number <span>:</span>
              </label>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  width: "150px",
                }}
              >
                <label style={{ width: "auto" }} htmlFor="PreviousPfnumber_yes">
                  <input
                    required
                    id="PreviousPfnumber_yes"
                    type="radio"
                    name="PreviousPfnumber"
                    value="Yes"
                    style={{ width: "15px" }}
                    checked={EmployeeformData.PreviousPfnumber === "Yes"}
                    onChange={handleInputChange}
                  />
                  Yes
                </label>
                <label style={{ width: "auto" }} htmlFor="PreviousPfnumber_no">
                  <input
                    required
                    id="PreviousWorkExperience_no"
                    type="radio"
                    name="PreviousPfnumber"
                    value="No"
                    style={{ width: "15px" }}
                    checked={EmployeeformData.PreviousPfnumber === "No"}
                    onChange={handleInputChange}
                  />
                  No
                </label>
              </div>
            </div>
            {EmployeeformData.PreviousPfnumber === "Yes" && (
              <div className="RegisForm_1">
                <label>
                  PF Number<span>:</span>
                </label>
                <input
                  type="text"
                  name="PFnumber"
                  value={EmployeeformData.PFnumber}
                  // placeholder='WorkStationNameAddress'
                  onChange={handleInputChange}
                />
              </div>
            )}
            <div className="RegisForm_1">
              <label>
                Do you have ESI Number <span>:</span>
              </label>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  width: "150px",
                }}
              >
                <label
                  style={{ width: "auto" }}
                  htmlFor="PreviousESInumber_yes"
                >
                  <input
                    required
                    id="PreviousESInumber_yes"
                    type="radio"
                    name="PreviousESInumber"
                    value="Yes"
                    style={{ width: "15px" }}
                    checked={EmployeeformData.PreviousESInumber === "Yes"}
                    onChange={handleInputChange}
                  />
                  Yes
                </label>
                <label style={{ width: "auto" }} htmlFor="PreviousESInumber_no">
                  <input
                    required
                    id="PreviousESInumber_no"
                    type="radio"
                    name="PreviousESInumber"
                    value="No"
                    style={{ width: "15px" }}
                    checked={EmployeeformData.PreviousESInumber === "No"}
                    onChange={handleInputChange}
                  />
                  No
                </label>
              </div>
            </div>

            {EmployeeformData.PreviousESInumber === "Yes" && (
              <div className="RegisForm_1">
                <label>
                  ESI Number<span>:</span>
                </label>
                <input
                  type="text"
                  name="ESInumber"
                  value={EmployeeformData.ESInumber}
                  // placeholder='WorkStationNameAddress'
                  onChange={handleInputChange}
                />
              </div>
            )}
          </>
        )}
      </div>
      {/* employment End =================*/}
      <br />
      <br />

      {/* Medical History  ========================== / */}

      <div className="DivCenter_container">Medical Information </div>
      <br />

      <div className="RegisFormcon">
        <div className="div_ckkck_box alcho_tac_drg11">
          <div className="ffdff44">
            <div>
              <label className="checkbox-label_ooo alcho_tac_drg">
                {" "}
                Pre-Existing Medical Condition <span>: </span>
              </label>
            </div>

            <div className="flx_cjk_labl3">
              <label className="checkbox-label_ooo">
                <input
                  type="checkbox"
                  name="Fit"
                  className="checkbox-input ddsfe"
                  checked={MedicalInformation.Fit}
                  onChange={handleMedicalInformationInputChange}
                />
                Fit
              </label>

              <label className="checkbox-label_ooo">
                <input
                  type="checkbox"
                  name="Epilepsy"
                  className="checkbox-input ddsfe"
                  checked={MedicalInformation.Epilepsy}
                  onChange={handleMedicalInformationInputChange}
                />
                Epilepsy
              </label>

              <label className="checkbox-label_ooo">
                <input
                  type="checkbox"
                  name="Ashthma"
                  className="checkbox-input ddsfe"
                  checked={MedicalInformation.Ashthma}
                  onChange={handleMedicalInformationInputChange}
                />
                Ashthma
              </label>

              <label className="checkbox-label_ooo">
                <input
                  type="checkbox"
                  name="Dm"
                  className="checkbox-input ddsfe"
                  checked={MedicalInformation.Dm}
                  onChange={handleMedicalInformationInputChange}
                />
                DM
              </label>

              <label className="checkbox-label_ooo">
                <input
                  type="checkbox"
                  name="Ht"
                  className="checkbox-input ddsfe"
                  checked={MedicalInformation.Ht}
                  onChange={handleMedicalInformationInputChange}
                />
                HT
              </label>

              <label className="checkbox-label_ooo">
                <input
                  type="checkbox"
                  name="Ihd"
                  className="checkbox-input ddsfe"
                  checked={MedicalInformation.Ihd}
                  onChange={handleMedicalInformationInputChange}
                />
                IHD
              </label>
            </div>
          </div>
        </div>

        <div className="RegisForm_1">
          <label>
            Pychitric Medicines<span>:</span>
          </label>
          <div
            style={{
              display: "flex",
              justifyContent: "flex-start",
              width: "120px",
              gap: "10px",
            }}
          >
            <label style={{ width: "auto" }} htmlFor="PsychiatricMedicines_yes">
              <input
                required
                id="PsychiatricMedicines_yes"
                type="radio"
                name="PsychiatricMedicines"
                value="Yes"
                style={{ width: "15px" }}
                checked={EmployeeformData.PsychiatricMedicines === "Yes"}
                onChange={handleInputChange}
              />
              Yes
            </label>
            <label style={{ width: "auto" }} htmlFor="PsychiatricMedicines_no">
              <input
                required
                id="PsychiatricMedicines_no"
                type="radio"
                name="PsychiatricMedicines"
                value="No"
                style={{ width: "15px" }}
                checked={EmployeeformData.PsychiatricMedicines === "No"}
                onChange={handleInputChange}
              />
              No
            </label>
          </div>
        </div>
        {EmployeeformData.PsychiatricMedicines === "Yes" && (
          <div className="RegisForm_1">
            <label>
              Psychiatric Medicines Details<span>:</span>
            </label>
            <textarea
              name="PsychiatricMedicinesDetails"
              value={EmployeeformData.PsychiatricMedicinesDetails}
              onChange={handleInputChange}
            />
          </div>
        )}

        <div className="RegisForm_1">
          <label>
            Previous Operation/Surgeries<span>:</span>
          </label>
          <div
            style={{
              display: "flex",
              justifyContent: "flex-start",
              width: "120px",
              gap: "10px",
            }}
          >
            <label style={{ width: "auto" }} htmlFor="PreviousOperation_yes">
              <input
                required
                id="PreviousOperation_yes"
                type="radio"
                name="PreviousOperation"
                value="Yes"
                style={{ width: "15px" }}
                checked={EmployeeformData.PreviousOperation === "Yes"}
                onChange={handleInputChange}
              />
              Yes
            </label>
            <label style={{ width: "auto" }} htmlFor="PreviousOperation_no">
              <input
                required
                id="PreviousOperation_no"
                type="radio"
                name="PreviousOperation"
                value="No"
                style={{ width: "15px" }}
                checked={EmployeeformData.PreviousOperation === "No"}
                onChange={handleInputChange}
              />
              No
            </label>
          </div>
        </div>
        {EmployeeformData.PreviousOperation === "Yes" && (
          <div className="RegisForm_1">
            <label>
              Surgeries Details<span>:</span>
            </label>
            <textarea
              name="SurgeriesDetails"
              value={EmployeeformData.SurgeriesDetails}
              onChange={handleInputChange}
            />
          </div>
        )}

        <div className="RegisForm_1">
          <label>
            Vaccination Status<span>:</span>
          </label>
          <div
            style={{
              display: "flex",
              justifyContent: "flex-start",
              width: "120px",
              gap: "10px",
            }}
          >
            <label style={{ width: "auto" }} htmlFor="VaccinationStatus_yes">
              <input
                required
                id="VaccinationStatus_yes"
                type="radio"
                name="VaccinationStatus"
                value="Yes"
                style={{ width: "15px" }}
                checked={EmployeeformData.VaccinationStatus === "Yes"}
                onChange={handleInputChange}
              />
              Yes
            </label>
            <label style={{ width: "auto" }} htmlFor="VaccinationStatus_no">
              <input
                required
                id="VaccinationStatus_no"
                type="radio"
                name="VaccinationStatus"
                value="No"
                style={{ width: "15px" }}
                checked={EmployeeformData.VaccinationStatus === "No"}
                onChange={handleInputChange}
              />
              No
            </label>
          </div>
        </div>

        {EmployeeformData.VaccinationStatus === "Yes" && (
          <div className="RegisForm_1">
            <label>
              Vaccination Details<span>:</span>
            </label>
            <textarea
              name="VaccinationStatusDetails"
              value={EmployeeformData.VaccinationStatusDetails}
              onChange={handleInputChange}
            />
          </div>
        )}


        <div className="RegisForm_1">
          <label>
            {" "}
            Medical Fitness Certificate<span>:</span>{" "}
          </label>
          <div className="RegisterForm_2">
            <input
              type="file"
              name={"MedicalFitnessCertificate"}
              accept="image/jpeg, image/png, application/pdf"
              required
              id={"MedicalFitnessCertificate"}
              autoComplete="off"
              onChange={handleinpchangeDocumentsForm}
              //   readOnly={IsViewMode}
              style={{ display: "none" }}
            />
            <div
              style={{
                width: "120px",
                display: "flex",
                justifyContent: "flex-start",
                gap: "10px",
                gap: "20px",
              }}
            >
              <label
                htmlFor={"MedicalFitnessCertificate"}
                className="RegisterForm_1_btns choose_file_update"
              >
                <PhotoCameraBackIcon />
              </label>
              <button
                className="RegisterForm_1_btns choose_file_update"
                onClick={() =>
                  Selectedfileview(EmployeeformData.MedicalFitnessCertificate)
                }
              >
                <VisibilityIcon />
              </button>
            </div>
          </div>
        </div>


        <div className="RegisForm_1">
          <label>
            {" "}
            Annual Medical Checkup<span>:</span>{" "}
          </label>
          <div className="RegisterForm_2">
            <input
              type="file"
              name={"AnnualMedicalCheckup"}
              accept="image/jpeg, image/png, application/pdf"
              required
              id={"AnnualMedicalCheckup"}
              autoComplete="off"
              onChange={handleinpchangeDocumentsForm}
              //   readOnly={IsViewMode}
              style={{ display: "none" }}
            />
            <div
              style={{
                width: "120px",
                display: "flex",
                justifyContent: "flex-start",
                gap: "10px",
                gap: "20px",
              }}
            >
              <label
                htmlFor={"AnnualMedicalCheckup"}
                className="RegisterForm_1_btns choose_file_update"
              >
                <PhotoCameraBackIcon />
              </label>
              <button
                className="RegisterForm_1_btns choose_file_update"
                onClick={() =>
                  Selectedfileview(EmployeeformData.AnnualMedicalCheckup)
                }
              >
                <VisibilityIcon />
              </button>
            </div>
          </div>
        </div>
      </div>
      {/* medical End */}
      <br />
      <br />

      {/* Current Employment ========================== / */}

      <div className="DivCenter_container">Current Employment </div>
      <br />

      <div className="RegisFormcon">
        <div className="RegisForm_1">
          <label>
            Date of Joining<span>:</span>
          </label>
          <input
            type="date"
            name="DateOfJoining"
            value={EmployeeformData.DateOfJoining}
            onChange={handleInputChange}
          />
        </div>

        <div className="RegisForm_1">
          <label>
            Locations<span>:</span>
          </label>
          <select
            name="Locations"
            required
            value={EmployeeformData.Locations}
            onChange={handleInputChange}
          >
            <option value="">Select</option>
            {Locations.filter((p) => p.Status === "Active")?.map(
              (Loc, indx) => (
                <option key={indx} value={Loc.id}>
                  {Loc.locationName}
                </option>
              )
            )}
          </select>
        </div>

        <div className="RegisForm_1">
          <label>
            Classification<span>:</span>
          </label>
          <select
            name="Classification"
            required
            value={EmployeeformData.Classification}
            onChange={handleInputChange}
          >
            <option value="">Select</option>
            {Classifications.filter((p) => p.Status === "Active")?.map(
              (Loc, indx) => (
                <option key={indx} value={Loc.id}>
                  {Loc.Classification}
                </option>
              )
            )}
          </select>
        </div>

        <div className="RegisForm_1">
          <label>
            {" "}
            Category <span>:</span>{" "}
          </label>

          <select
            name="Category"
            required
            value={EmployeeformData.Category}
            onChange={handleInputChange}
          >
            <option value="">Select</option>
            {Category.filter((p) => p.Status === "Active").map((catg, indx) => (
              <option key={indx} value={catg.id}>
                {catg.CategoryName}
              </option>
            ))}
          </select>
        </div>

        <div className="RegisForm_1">
          <label>
            {" "}
            Speciality <span>:</span>{" "}
          </label>

          <select
            name="Speciality"
            required
            value={EmployeeformData.Speciality}
            onChange={handleInputChange}
          >
            <option value="">Select</option>
            {Speciality.filter((p) => p.Status === "Active").map(
              (spec, indx) => (
                <option key={indx} value={spec.id}>
                  {spec.SpecialityName}
                </option>
              )
            )}
          </select>
        </div>

        <div className="RegisForm_1">
          <label>
            {" "}
            Designation <span>:</span>{" "}
          </label>

          <select
            name="Designation"
            required
            value={EmployeeformData.Designation}
            onChange={handleInputChange}
          >
            <option value="">Select</option>
            {Designations.filter((p) => p.Status === "Active")?.map(
              (Des, indx) => (
                <option key={indx} value={Des.id}>
                  {Des.Designation}
                </option>
              )
            )}
          </select>
        </div>

        <div className="RegisForm_1">
          <label>Department<span>:</span></label>
          <input
            type="Text"
            name="Department"

            value={EmployeeformData.Department}
            onChange={handleInputChange}
            required

          />
          <span>
            <AddBoxIcon onClick={HandleDepartmentSelect} />
          </span>

        </div>

        <div className="RegisForm_1">
          <label>
            {" "}
            Role <span>:</span>{" "}
          </label>

          <select
            name="Role"
            required
            value={EmployeeformData.Role}
            onChange={handleInputChange}
          >
            <option value="">Select</option>
            {Roles.filter((p) => p.Status === "Active").map(
              (dept, indx) => (
                <option key={indx} value={dept.id}>
                  {dept.Role}
                </option>
              )
            )}
          </select>
        </div>


        <div className="RegisForm_1">
          <label>
            Reporting Manager<span>:</span>
          </label>
          <input
            type="text"
            name="ReportingManager"
            value={EmployeeformData.ReportingManager}
            onChange={handleInputChange}
          />
        </div>

        <div className="RegisForm_1">
          <label>
            Govt Leave (.yrs) <span>:</span>
          </label>
          <input
            type="number"
            name="GovtLeave"
            onKeyDown={(e) =>
              ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()
            }
            value={EmployeeformData.GovtLeave}
            onChange={handleChangeGovtLeave}
            required
          ></input>
        </div>
        <div className="RegisForm_1">
          <label>
            Casual Leave (.yrs) <span>:</span>
          </label>
          <input
            type="number"
            name="CasualLeave"
            onKeyDown={(e) =>
              ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()
            }
            value={EmployeeformData.CasualLeave}
            onChange={handleChangeCasualLeave}
            required
          ></input>
        </div>
        <div className="RegisForm_1">
          <label>
            Sick Leave (.yrs) <span>:</span>
          </label>
          <input
            type="number"
            name="SickLeave"
            onKeyDown={(e) =>
              ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()
            }
            value={EmployeeformData.SickLeave}
            onChange={handleChangeSickLeave}
            required
          ></input>
        </div>
        <div className="RegisForm_1">
          <label>
            Total Leave (.yrs) <span>:</span>
          </label>
          <input
            name="TotalLeave"
            value={EmployeeformData.TotalLeave}
            onKeyDown={(e) =>
              ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()
            }
            readOnly
            required
          ></input>
        </div>



        <div className="RegisForm_1">
          <label>
            Work Email<span>:</span>
          </label>
          <input
            type="text"
            name="WorkEmail"
            value={EmployeeformData.WorkEmail}
            onChange={handleInputChange}
          />
        </div>

        <div className="RegisForm_1">
          <label>
            Probation Period <span>:</span>
          </label>
          <div
            style={{
              display: "flex",
              justifyContent: "flex-start",
              width: "120px",
              gap: "10px",
            }}
          >
            <label style={{ width: "auto" }} htmlFor="ProbationPeriod_yes">
              <input
                required
                id="ProbationPeriod_yes"
                type="radio"
                name="ProbationPeriod"
                value="Yes"
                style={{ width: "15px" }}
                checked={EmployeeformData.ProbationPeriod === "Yes"}
                onChange={handleInputChange}
              />
              Yes
            </label>
            <label style={{ width: "auto" }} htmlFor="ProbationPeriod_no">
              <input
                required
                id="ProbationPeriod_no"
                type="radio"
                name="ProbationPeriod"
                value="No"
                style={{ width: "15px" }}
                checked={EmployeeformData.ProbationPeriod === "No"}
                onChange={handleInputChange}
              />
              No
            </label>
          </div>
        </div>
        {EmployeeformData.ProbationPeriod === "Yes" && (
          <>
            <div className="RegisForm_1">
              <select
                name="months"
                value={EmployeeformData.months}
                onChange={handleInputChange}
                // onClick={handleTypeChange}
                required
              >
                <option value="0">0</option>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
                <option value="6">6</option>
                <option value="7">7</option>
                <option value="8">8</option>
                <option value="9">9</option>
                <option value="10">10</option>
                <option value="11">11</option>
              </select>
              <label>Months</label>
              <select
                name="years"
                value={EmployeeformData.years}
                onChange={handleInputChange}
                // onClick={handleyearChange}
                required
              >
                <option value="0">0</option>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
                <option value="6">6</option>
                <option value="7">7</option>
                <option value="8">8</option>
                <option value="9">9</option>
                <option value="10">10</option>
                <option value="11">11</option>
              </select>
              <label>Years</label>
            </div>

            <div className="RegisForm_1">
              <label>
                Training Given By<span>:</span>
              </label>
              <input
                type="text"
                name="TrainingGivenBy"
                value={EmployeeformData.TrainingGivenBy}
                onChange={handleInputChange}
              />
            </div>

            <div className="RegisForm_1">
              <label>
                Training Verified By<span>:</span>
              </label>
              <input
                type="text"
                name="TrainingVerifiedBy"
                value={EmployeeformData.TrainingVerifiedBy}
                onChange={handleInputChange}
              />
            </div>

            <div className="RegisForm_1">
              <label>
                Training Completion Date<span>:</span>
              </label>
              <input
                type="date"
                name="TrainingCompletedDate"
                value={EmployeeformData.TrainingCompletedDate}
                onChange={handleInputChange}
              />
            </div>
            <div className="RegisForm_1">
              <label>PF Applicable After Probation<span>:</span></label>
              <input
                type="checkbox"
                name="IsPF_Applicable"
                className="checkbox-input ddsfe"
                checked={!!EmployeeformData.IsPF_Applicable} // Ensures it’s always boolean
                onChange={handleInputChange}
              />
            </div>

          </>
        )}
      </div>
      {/* Current Employee End */}
      <br />
      <br />

      {/* Financial Information ========== */}

      <div className="DivCenter_container">Financial Information</div>
      <br />
      <div className="RegisFormcon">

        <div className="RegisForm_1">
          <label>Salary(%)<span>:</span></label>
          <input
            type="number"
            name="Salary"
            onKeyDown={(e) =>
              ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()
            }
            value={EmployeeformData.Salary}
            onChange={handleInputChange}
          />
        </div>

        <div className="RegisForm_1">
          <label>Basic Salary<span>:</span></label>
          <input
            type="number"
            name="BasicSalary"
            onKeyDown={(e) =>
              ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()
            }
            value={EmployeeformData.BasicSalary}
            disabled
          />
        </div>
        <div className="RegisForm_1">
          <label>
            Allowance(%)<span>:</span>
          </label>
          <input
            type="number"
            name="Allowance"
            value={EmployeeformData.Allowance || ""}
            onChange={handleInputChange1}
            onKeyDown={(e) =>
              ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()
            }
          />
        </div>
        <div className="RegisForm_1">
          <label>
            Security Deposite (%)<span>:</span>
          </label>
          <input
            type="number"
            onKeyDown={(e) =>
              ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()
            }
            name="SecurityDeposite"
            value={EmployeeformData.SecurityDeposite}
            onChange={handleInputChange}
          />
        </div>

        {EmployeeformData.IsPF_Applicable && (
          <div className="RegisForm_1">
            <label>
              PF for Employee (%)<span>:</span>
            </label>
            <input
              type="number"
              onKeyDown={(e) =>
                ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()
              }
              name="PfForEmployee"
              value={EmployeeformData.PfForEmployee}
              onChange={handleInputChange}
              disabled
             
            />
          </div>
        )}






        <div className="RegisForm_1">
          <label>
            Account Holder Name<span>:</span>
          </label>
          <input
            type="text"
            name="AccountHolderName"
            value={EmployeeformData.AccountHolderName}
            onChange={handleInputChange}
            required
          />
        </div>
        <div className="RegisForm_1">
          <label>
            Account Number<span>:</span>
          </label>
          <input
            type="number"
            name="AccountNumber"
            onKeyDown={(e) =>
              ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()
            }
            value={EmployeeformData.AccountNumber}
            onChange={handleInputChange}
            required
          />
        </div>

        <div className="RegisForm_1">
          <label>
            Bank Name<span>:</span>
          </label>
          <input
            type="text"
            name="BankName"
            value={EmployeeformData.BankName}
            onChange={handleInputChange}
            required
          />
        </div>

        <div className="RegisForm_1">
          <label>
            Branch<span>:</span>
          </label>
          <input
            type="text"
            name="Branch"
            value={EmployeeformData.Branch}
            onChange={handleInputChange}
            required
          />
        </div>

        <div className="RegisForm_1">
          <label>
            IFSC Code <span>:</span>
          </label>
          <input
            type="text"
            name="IfscCode"
            value={EmployeeformData.IfscCode}
            onChange={handleInputChange}
            required
          />
        </div>
        <div className="RegisForm_1">
          <label>
            Pan Number <span>:</span>
          </label>
          <input
            type="text"
            name="PanNumber"
            value={EmployeeformData.PanNumber}
            onChange={handleInputChange}
            required
          />
        </div>


      </div>

      <br />
      <br />



      <div className="DivCenter_container">Document Checklist</div>
      <br />
      <div className="RegisFormcon">
        <div className="RegisForm_1">
          <label>
            Resume<span>:</span>
          </label>

          <div className="RegisterForm_2">
            <input
              type="file"
              name={"Resume"}
              accept="image/jpeg, image/png, application/pdf"
              required
              id={"Resume"}
              autoComplete="off"
              onChange={handleinpchangeDocumentsForm}
              style={{ display: "none" }}
            />
            <div
              style={{
                width: "120px",
                display: "flex",
                justifyContent: "flex-start",
                gap: "20px",
              }}
            >
              <label
                htmlFor={"Resume"}
                className="RegisterForm_1_btns choose_file_update"
              >
                <PhotoCameraBackIcon />
              </label>
              <button
                className="RegisterForm_1_btns choose_file_update"
                onClick={() => Selectedfileview(EmployeeformData.Resume)}
              >
                <VisibilityIcon />
              </button>
            </div>
          </div>
        </div>
        <div className="RegisForm_1">
          <label>
            Govt Id (PAN)<span>:</span>
          </label>
          <div className="RegisterForm_2">
            <input
              type="file"
              name={"PanCard"}
              accept="image/jpeg, image/png, application/pdf"
              required
              id={"PanCard"}
              autoComplete="off"
              onChange={handleinpchangeDocumentsForm}
              //   readOnly={IsViewMode}
              style={{ display: "none" }}
            />
            <div
              style={{
                width: "120px",
                display: "flex",
                justifyContent: "flex-start",
                gap: "20px",
              }}
            >
              <label
                htmlFor={"PanCard"}
                className="RegisterForm_1_btns choose_file_update"
              >
                <PhotoCameraBackIcon />
              </label>
              <button
                className="RegisterForm_1_btns choose_file_update"
                onClick={() => Selectedfileview(EmployeeformData.PanCard)}
              >
                <VisibilityIcon />
              </button>
            </div>
          </div>
        </div>

        <div className="RegisForm_1">
          <label>
            Aadhar Card<span>:</span>
          </label>
          <div className="RegisterForm_2">
            <input
              type="file"
              name={"AadharCard"}
              accept="image/jpeg, image/png, application/pdf"
              required
              id={"AadharCard"}
              autoComplete="off"
              onChange={handleinpchangeDocumentsForm}
              //   readOnly={IsViewMode}
              style={{ display: "none" }}
            />
            <div
              style={{
                width: "120px",
                display: "flex",
                justifyContent: "flex-start",
                gap: "20px",
              }}
            >
              <label
                htmlFor={"AadharCard"}
                className="RegisterForm_1_btns choose_file_update"
              >
                <PhotoCameraBackIcon />
              </label>
              <button
                className="RegisterForm_1_btns choose_file_update"
                onClick={() => Selectedfileview(EmployeeformData.AadharCard)}
              >
                <VisibilityIcon />
              </button>
            </div>
          </div>
        </div>

        <div className="RegisForm_1">
          <label>
            Bank Passbook <span>:</span>
          </label>
          <div className="RegisterForm_2">
            <input
              type="file"
              name={"BankPassbook"}
              accept="image/jpeg, image/png, application/pdf"
              required
              id={"BankPassbook"}
              autoComplete="off"
              onChange={handleinpchangeDocumentsForm}
              //   readOnly={IsViewMode}
              style={{ display: "none" }}
            />
            <div
              style={{
                width: "120px",
                display: "flex",
                justifyContent: "flex-start",
                gap: "20px",
              }}
            >
              <label
                htmlFor={"BankPassbook"}
                className="RegisterForm_1_btns choose_file_update"
              >
                <PhotoCameraBackIcon />
              </label>
              <button
                className="RegisterForm_1_btns choose_file_update"
                onClick={() => Selectedfileview(EmployeeformData.BankPassbook)}
              >
                <VisibilityIcon />
              </button>
            </div>
          </div>
        </div>

        <div className="RegisForm_1">
          <label>
            Experience Certificate<span>:</span>
          </label>
          <div className="RegisterForm_2">
            <input
              type="file"
              name={"ExperienceCertificate"}
              accept="image/jpeg, image/png, application/pdf"
              required
              id={"ExperienceCertificate"}
              autoComplete="off"
              onChange={handleinpchangeDocumentsForm}
              //   readOnly={IsViewMode}
              style={{ display: "none" }}
            />
            <div
              style={{
                width: "120px",
                display: "flex",
                justifyContent: "flex-start",
                gap: "20px",
              }}
            >
              <label
                htmlFor={"ExperienceCertificate"}
                className="RegisterForm_1_btns choose_file_update"
              >
                <PhotoCameraBackIcon />
              </label>
              <button
                className="RegisterForm_1_btns choose_file_update"
                onClick={() =>
                  Selectedfileview(EmployeeformData.ExperienceCertificate)
                }
              >
                <VisibilityIcon />
              </button>
            </div>
          </div>
        </div>
        <div className="RegisForm_1">
          <label>
            Medical Fitness<span>:</span>
          </label>
          <div className="RegisterForm_2">
            <input
              type="file"
              name={"MedicalFitness"}
              accept="image/jpeg, image/png, application/pdf"
              required
              id={"MedicalFitness"}
              autoComplete="off"
              onChange={handleinpchangeDocumentsForm}
              //   readOnly={IsViewMode}
              style={{ display: "none" }}
            />
            <div
              style={{
                width: "120px",
                display: "flex",
                justifyContent: "flex-start",
                gap: "20px",
              }}
            >
              <label
                htmlFor={"MedicalFitness"}
                className="RegisterForm_1_btns choose_file_update"
              >
                <PhotoCameraBackIcon />
              </label>
              <button
                className="RegisterForm_1_btns choose_file_update"
                onClick={() =>
                  Selectedfileview(EmployeeformData.MedicalFitness)
                }
              >
                <VisibilityIcon />
              </button>
            </div>
          </div>
        </div>

        <div className="RegisForm_1">
          <label>
            Offer Letter<span>:</span>
          </label>
          <div className="RegisterForm_2">
            <input
              type="file"
              name={"Offerletter"}
              accept="image/jpeg, image/png, application/pdf"
              required
              id={"Offerletter"}
              autoComplete="off"
              onChange={handleinpchangeDocumentsForm}
              //   readOnly={IsViewMode}
              style={{ display: "none" }}
            />
            <div
              style={{
                width: "120px",
                display: "flex",
                justifyContent: "flex-start",
                gap: "20px",
              }}
            >
              <label
                htmlFor={"Offerletter"}
                className="RegisterForm_1_btns choose_file_update"
              >
                <PhotoCameraBackIcon />
              </label>
              <button
                className="RegisterForm_1_btns choose_file_update"
                onClick={() => Selectedfileview(EmployeeformData.Offerletter)}
              >
                <VisibilityIcon />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Document Checklist End */}
      <br />
      <br />

      <ToastContainer />
      {selectDepartment && (
        <div className="loader" onClick={() => setSelectDepartment(false)}>
          <div
            className="loader_register_roomshow"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="DivCenter_container">Select Department Details</div>
            <div className="RegisFormcon_1">
              <div className="RegisForm_1">
                <label htmlFor="selectDepModal.SelectDepartment">
                  Select Department <span>:</span>
                </label>
                <select
                  name="SelectDepartment"
                  required
                  id={selectDepModal.SelectDepartment}
                  value={selectDepModal.SelectDepartment}
                  onChange={handleinpchangeDepartment}
                >
                  <option value="">Select</option>
                  {DepartmentData.filter((p) => p.Status === "Active").map(
                    (p, index) => (
                      <option key={index} value={p.id}>
                        {p.DepartmentName}
                      </option>
                    )
                  )}
                </select>
                <div className="Main_container_Btn">
                  <button onClick={handleDepartmentSave}>Save</button>
                </div>
              </div>
            </div>
            <ReactGrid columns={SelectDataColumn} RowData={Departments} />
          </div>
        </div>
      )}
      <ModelContainer />

      <div className="Main_container_Btn">
        <button onClick={handleSubmit}>
          {EmployeeListId?.Employee_Id ? "Update" : "Save"}
        </button>
      </div>
    </div>
  );
};

export default EmployeeRegistration;
