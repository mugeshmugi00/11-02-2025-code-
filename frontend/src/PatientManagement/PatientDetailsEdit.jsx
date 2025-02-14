import React, { useEffect, useState } from "react";
import axios from "axios";
import { useSelector, useDispatch } from "react-redux";
import { ToastContainer, toast } from "react-toastify";
import { format } from "date-fns";
import PersonSearchIcon from "@mui/icons-material/PersonSearch";
import { useNavigate } from "react-router-dom";
import {
  differenceInYears,
  differenceInMonths,
  differenceInDays,
  startOfYear,
  subYears,
  isBefore,
  addMonths,
  addYears,
} from "date-fns";

import ToastAlert from "../OtherComponent/ToastContainer/ToastAlert";
import ReactGrid from "../OtherComponent/ReactGrid/ReactGrid";
import { Button } from "@mui/material";
// import EditIcon from "@mui/icons-material/Edit";

const PatientDetailsEdit = () => {
  const dispatchvalue = useDispatch();
  const dispatch = useDispatch();
  
  const PatientListId = useSelector(
    (state) => state.Frontoffice?.PatientListId
  );
  const navigate = useNavigate();

  // console.log(PatientListId,'111111111111');

  const UrlLink = useSelector((state) => state.userRecord?.UrlLink);
  const userRecord = useSelector((state) => state.userRecord?.UserData);
  // console.log(userRecord,'userRecord');
  const [BloodGroupData, setBloodGroupData] = useState([]);
  const [ReligionData, setReligionData] = useState([]);
  const [errors, setErrors] = useState({});
  const [FlaggData, setFlaggData] = useState([]);
  const [InsuranceData, setInsuranceData] = useState([]);
  const [ClientData, setClientData] = useState([]);
  const [DonationData, setDonationData] = useState([]);
  const [EmployeeData, setEmployeeData] = useState([]);
  // console.log(FlaggData,'FlaggDataaaaaaaaaaa');
  const [TitleNameData, setTitleNameData] = useState([]);

  const [DoctorIdData, setDoctorIdData] = useState([]);
  const [isUpdating, setIsUpdating] = useState(false);
  const [FilterbyPatientNo, setFilterbyPatientNo] = useState([]);
  const [RegPatientId, setRegPatientId] = useState(null);
  const [postdata, setPostData] = useState(null);

  const [searchQuery, setSearchQuery] = useState("");
  const [patientList, setPatientList] = useState([]);
  const [filteredPatients, setFilteredPatients] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [FamilyData, setFamilyData] = useState([]);

  const [selectedRows, setSelectedRows] = useState([]);
  const [FamilymembersData, setFamilymembersData] = useState([]);

  const [FilteredFormdata, setFilteredFormdata] = useState(null);
  const [FilteredFormdataAddress, setFilteredFormdataAddress] = useState(null);
  const [
    FilteredFormdataPermanentAddress,
    setFilteredFormdataPermanentAddress,
  ] = useState(null);

  const [PatientEdit, setPatientEdit] = useState({
    PatientId: "",
    ABHA: "",
    Title: "",
    FirstName: "",
    MiddleName: "",
    SurName: "",
    DOB: "",
    Age: "",
    Gender: "",
    PhoneNo: "",
    Email: "",
    MaritalStatus: "",
    SpouseName: "",
    FatherName: "",
    AliasName: "",
    BloodGroup: "",
    Occupation: "",
    Religion: "",
    Nationality: "",
    UniqueIdType: "",
    UniqueIdNo: "",
    PatientType: "",

    // PatientCategory: "",
    // InsuranceName: "",
    // InsuranceType: "",
    // ClientName: "",
    // ClientType: "Self",
    // ClientEmployeeId: "",
    // ClientEmployeeDesignation: "",
    // ClientEmployeeRelation: "",
    // EmployeeId: "",
    // EmployeeRelation: "",
    // DoctorId: "",
    // DoctorRelation: "",
    // DonationType: "",

    Flagging: "",

    Pincode: "",
    DoorNo: "",
    Street: "",
    Area: "",
    City: "",
    District: "",
    State: "",
    Country: "",

    PermanentAddressSameAsAbove: "Yes",

    // PERMANENT ADDRESS
    PermanentPincode: "",
    PermanentdoorNo: "",
    PermanentStreet: "",
    PermanentArea: "",
    PermanentCity: "",
    PermanentDistrict: "",
    PermanentState: "",
    PermanentCountry: "",
    Photo: null,
  });

  const relationships = [
    "Spouse",
    "Father",
    "Mother",
    "Brother",
    "Sister",
    "Father-in-law",
    "Mother-in-law",
    "Grandfather",
    "Grandmother",
    "Son",
    "Daughter",
    "Grandson",
    "Granddaughter",
    "Son-in-law",
    "Daughter-in-law",
    "Uncle",
    "Aunt",
    "Nephew",
    "Niece",
    "Cousin",
    "Step-father",
    "Step-mother",
    "Step-son",
    "Step-daughter",
  ];

  useEffect(() => {
    console.log(PatientListId, "PatientListId after navigation");
  }, [PatientListId]);

  useEffect(() => {
    const PatientId = PatientListId?.PatientId;

    if (PatientId) {
      axios
        .get(`${UrlLink}Frontoffice/Patient_Master_List`, {
          params: { PatientId },
        })
        .then((res) => {
          const data = res.data; // Assume the response data contains the patient details
          console.log(data, "dataaaa");

          const OP = data?.OP_details?.[0];
          console.log(OP, "aaaaaaaaaa");
          const IP = data?.IP_details?.[0];
          console.log(IP, "bbbbbbbbb");
          const Casuality = data?.Casuality_details?.[0];
          console.log(Casuality, "ccccccccc");
          const Diagnosis = data?.Diagnosis_details?.[0];
          console.log(Diagnosis, "dddddddd");
          const Laboratory = data?.Laboratory_details?.[0];
          console.log(Laboratory, "eeeeeeeee");

          if (data) {
            setPatientEdit((prev) => ({
              ...prev, // Spread previous state

              PatientId: data.PatientId || "", // Update PatientId
              PhoneNo: data.PhoneNo || "", // Update PhoneNo
              Title: data.Title || "",
              FirstName: data.FirstName || "",
              MiddleName: data.MiddleName || "",
              SurName: data.SurName || "",
              Gender: data.Gender || "",
              MaritalStatus: data.MaritalStatus || "",
              SpouseName: data.SpouseName || "",
              FatherName: data.FatherName || "",
              AliasName: data.AliasName || "",
              DOB: data.DOB || "",
              Age: data.Age || "",
              Email: data.Email || "",
              BloodGroup: data.BloodGroup || "",
              Occupation: data.Occupation || "",
              Religion: data.Religion || "",
              Nationality: data.Nationality || "",
              UniqueIdType: data.UniqueIdType || "",
              UniqueIdNo: data.UniqueIdNo || "",
              DoorNo: data.DoorNo || "",
              Street: data.Street || "",
              Area: data.Area || "",
              City: data.City || "",
              District: data.District || "",
              State: data.State || "",
              Country: data.Country || "",
              Pincode: data.Pincode || "",
              PatientType: data.PatientType || "",
              Flagging: data.Flagging || "",
              ABHA: data.ABHA || "",
              PermanentAddressSameAsAbove:
                data.PermanentAddressSameAsAbove || "",
              PermanentPincode: data.PermanentPincode || "",
              PermanentdoorNo: data.PermanentdoorNo || "",
              PermanentStreet: data.PermanentStreet || "",
              PermanentArea: data.PermanentArea || "",
              PermanentCity: data.PermanentCity || "",
              PermanentDistrict: data.PermanentDistrict || "",
              PermanentState: data.PermanentState || "",
              PermanentCountry: data.PermanentCountry || "",
              Photo: data.Photo || "",

              // PatientType: OP?.PatientType || IP?.PatientType || Casuality?.PatientType || Diagnosis?.PatientType || Laboratory?.PatientType|| "",
              // PatientCategory: OP?.PatientCategory || IP?.PatientCategory || Casuality?.PatientCategory || Diagnosis?.PatientCategory || Laboratory?.PatientCategory ||  "",
              // InsuranceName: OP?.InsuranceName || IP?.InsuranceName || Casuality?.InsuranceName || Diagnosis?.InsuranceName || Laboratory?.InsuranceName ||  "",
              // InsuranceType: OP?.InsuranceType || IP?.InsuranceType || Casuality?.InsuranceType || Diagnosis?.InsuranceType || Laboratory?.InsuranceType ||  "",
              // ClientName: OP?.ClientName || IP?.ClientName || Casuality?.ClientName || Diagnosis?.ClientName || Laboratory?.ClientName ||  "",
              // ClientType: OP?.ClientType || IP?.ClientType || Casuality?.ClientType || Diagnosis?.ClientType || Laboratory?.ClientType ||  "",
              // ClientEmployeeId: OP?.ClientEmployeeId || IP?.ClientEmployeeId || Casuality?.ClientEmployeeId || Diagnosis?.ClientEmployeeId || Laboratory?.ClientEmployeeId ||  "",
              // ClientEmployeeDesignation: OP?.ClientEmployeeDesignation || IP?.ClientEmployeeDesignation || Casuality?.ClientEmployeeDesignation || Diagnosis?.ClientEmployeeDesignation || Laboratory?.ClientEmployeeDesignation ||  "",
              // ClientEmployeeRelation: OP?.ClientEmployeeRelation || IP?.ClientEmployeeRelation || Casuality?.ClientEmployeeRelation || Diagnosis?.ClientEmployeeRelation || Laboratory?.ClientEmployeeRelation ||  "",
              // EmployeeId: OP?.EmployeeId || IP?.EmployeeId || Casuality?.EmployeeId || Diagnosis?.EmployeeId || Laboratory?.EmployeeId ||  "",
              // EmployeeRelation: OP?.EmployeeRelation || IP?.EmployeeRelation || Casuality?.EmployeeRelation || Diagnosis?.EmployeeRelation || Laboratory?.EmployeeRelation ||  "",
              // DoctorId: OP?.DoctorId || IP?.DoctorId || Casuality?.DoctorId || Diagnosis?.DoctorId || Laboratory?.DoctorId ||  "",
              // DoctorRelation: OP?.DoctorRelation || IP?.DoctorRelation || Casuality?.DoctorRelation || Diagnosis?.DoctorRelation || Laboratory?.DoctorRelation ||  "",
              // DonationType: OP?.DonationType || IP?.DonationType || Casuality?.DonationType || Diagnosis?.DonationType || Laboratory?.DonationType ||  "",
              // Flagging:OP?.Flagging || IP?.Flagging || Casuality?.Flagging || Diagnosis?.Flagging || Laboratory?.Flagging || "",
            }));
          }
        })
        .catch((err) => {
          console.error("Error fetching patient data:", err);
        });
    }
  }, [PatientListId, UrlLink]);

  useEffect(() => {
    let PersonalData = Object.keys(PatientEdit).filter((p) =>
      [
        "PatientId",
        "ABHA",
        "Title",
        "FirstName",
        "MiddleName",
        "SurName",
        "DOB",
        "Age",
        "Gender",
        "PhoneNo",
        "Email",
        "MaritalStatus",
        "SpouseName",
        "AliasName",
        "FatherName",
        "BloodGroup",
        "Occupation",
        "Religion",
        "Nationality",
        "UniqueIdType",
        "UniqueIdNo",
        "PatientType",
        "Flagging",
      ].includes(p)
    );
    setFilteredFormdata(PersonalData);

    let Addressdata = Object.keys(PatientEdit).filter((p) =>
      [
        "Pincode",
        "DoorNo",
        "Street",
        "Area",
        "City",
        "District",
        "State",
        "Country",
        "PermanentAddressSameAsAbove",
      ].includes(p)
    );
    setFilteredFormdataAddress(Addressdata);

    let PermanentAddressdata = Object.keys(PatientEdit).filter((p) =>
      [
        "PermanentdoorNo",
        "PermanentStreet",
        "PermanentArea",
        "PermanentCity",
        "PermanentDistrict",
        "PermanentState",
        "PermanentCountry",
        "PermanentPincode",
      ].includes(p)
    );
    setFilteredFormdataPermanentAddress(PermanentAddressdata);
  }, [PatientEdit]);

  // -------------------------------------------------------------------------

  

  // --------------------------------------------------------------------------
  useEffect(() => {
    axios
      .get(`${UrlLink}Frontoffice/get_DoctorId_by_PatientCategory`)
      .then((res) => {
        const data = res.data;
        if (Array.isArray(data)) {
          setDoctorIdData(data);
        } else {
          setDoctorIdData([]);
        }
      })
      .catch((err) => {
        console.log(err);
      });
  }, [UrlLink]);

  useEffect(() => {
    axios
      .get(`${UrlLink}Frontoffice/get_Employee_by_PatientCategory`)
      .then((res) => {
        const data = res.data;
        if (Array.isArray(data)) {
          setEmployeeData(data);
        } else {
          setEmployeeData([]);
        }
      })
      .catch((err) => {
        console.log(err);
      });
  }, [UrlLink]);

  useEffect(() => {
    axios
      .get(`${UrlLink}Masters/get_client_data_registration`)
      .then((res) => {
        const data = res.data;
        if (Array.isArray(data)) {
          setClientData(data);
        } else {
          setClientData([]);
        }
      })
      .catch((err) => {
        console.log(err);
      });
  }, [UrlLink]);

  useEffect(() => {
    axios
      .get(`${UrlLink}Masters/get_donation_data_registration`)
      .then((res) => {
        const data = res.data;
        if (Array.isArray(data)) {
          setDonationData(data);
        } else {
          setDonationData([]);
        }
      })
      .catch((err) => {
        console.log(err);
      });
  }, [UrlLink]);

  useEffect(() => {
    axios
      .get(`${UrlLink}Masters/get_insurance_data_registration`)
      .then((res) => {
        const data = res.data;
        if (Array.isArray(data)) {
          setInsuranceData(data);
        } else {
          setInsuranceData([]);
        }
      })
      .catch((err) => {
        console.log(err);
      });
  }, [UrlLink]);

  useEffect(() => {
    axios
      .get(`${UrlLink}Masters/BloodGroup_Master_link`)
      .then((res) => {
        const data = res.data;
        if (Array.isArray(data)) {
          setBloodGroupData(data);
        } else {
          setBloodGroupData([]);
        }
      })
      .catch((err) => {
        console.log(err);
      });
  }, [UrlLink]);

  useEffect(() => {
    axios
      .get(`${UrlLink}Masters/Flagg_color_Detials_by_specialtype`)
      .then((res) => {
        const data = res.data;
        if (Array.isArray(data)) {
          setFlaggData(data);
        } else {
          setFlaggData([]);
        }
      })
      .catch((err) => {
        console.log(err);
      });
  }, [UrlLink]);

  useEffect(() => {
    axios
      .get(`${UrlLink}Masters/Relegion_Master_link`)
      .then((res) => {
        const data = res.data;
        if (Array.isArray(data)) {
          setReligionData(data);
        } else {
          setReligionData([]);
        }
      })
      .catch((err) => {
        console.log(err);
      });
  }, [UrlLink]);

  useEffect(() => {
    axios
      .get(`${UrlLink}Masters/Title_Master_link`)
      .then((res) => {
        const data = res.data;
        if (Array.isArray(data)) {
          setTitleNameData(data);
        } else {
          setTitleNameData([]);
        }
      })
      .catch((err) => {
        console.log(err);
      });
  }, [UrlLink]);

  const handleInputChange = (e) => {
    const { name, value, pattern } = e.target;

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

    // Field validation
    setErrors((prevErrors) => ({
      ...prevErrors,
      [name]: error,
    }));

    let formattedValue = value;

    const formatABHA = (value) =>
      value
        .replace(/\D/g, "")
        .replace(/(\d{2})(\d{4})?(\d{4})?(\d{4})?/, (match, p1, p2, p3, p4) =>
          [p1, p2, p3, p4].filter(Boolean).join("-")
        );

    if (name === "ABHA") {
      const formattedABHA = formatABHA(value);
      setPatientEdit((prev) => ({
        ...prev,
        [name]: formattedABHA,
      }));
      return;
    }

    const capitalizeFirstLetter = (value) =>
      value.charAt(0).toUpperCase() + value.slice(1);

    // Capitalize first letter for specific fields
    if (
      [
        "FirstName",
        "MiddleName",
        "SurName",
        "AliasName",
        "Occupation",
        "FatherName",
        "SpouseName",
        "DoorNo",
        "Street",
        "Area",
        "City",
        "District",
        "State",
        "Country",
        "PermanentdoorNo",
        "PermanentStreet",
        "PermanentArea",
        "PermanentCity",
        "PermanentDistrict",
        "PermanentState",
        "PermanentCountry",
      ].includes(name)
    ) {
      formattedValue = capitalizeFirstLetter(value);
    }

    // Check character length for certain fields
    if (
      [
        "FirstName",
        "MiddleName",
        "AliasName",
        "SurName",
        "Occupation",
      ].includes(name) &&
      value.length > 30
    ) {
      dispatchvalue({
        type: "toast",
        value: {
          message: `${name} should not exceed 30 characters.`,
          type: "warn",
        },
      });
      return; // Exit early
    }

    // Handle PhoneNo
    if (name === "PhoneNo") {
      if (formattedValue.includes("|")) {
        const [patientId, firstName, phoneNo] = formattedValue.split(" | ");
        if (phoneNo?.trim().length <= 10) {
          setPatientEdit((prev) => ({
            ...prev,
            [name]: phoneNo.trim(),
            PatientId: patientId.trim(),
            FirstName: firstName.trim(),
          }));
        }
      } else if (formattedValue.length <= 10) {
        setPatientEdit((prev) => ({
          ...prev,
          [name]: formattedValue,
        }));
      }
    }

    // Handle FirstName with pipe logic
    else if (name === "FirstName") {
      if (formattedValue.includes("|")) {
        const [patientId, firstName, phoneNo] = formattedValue.split(" | ");
        setPatientEdit((prev) => ({
          ...prev,
          [name]: firstName.trim(),
          PatientId: patientId.trim(),
          PhoneNo: phoneNo.trim(),
        }));
      } else {
        setPatientEdit((prev) => ({
          ...prev,
          [name]: formattedValue,
        }));
      }
    }

    // Handle Title changes for gender
    else if (name === "Title") {
      setPatientEdit((prev) => ({
        ...prev,
        [name]: formattedValue,
        Gender: ["Miss", "Ms", "Mrs"].includes(value)
          ? "Female"
          : ["Mr", "Master"].includes(value)
          ? "Male"
          : ["TransGender", "Baby", "Dr"].includes(value)
          ? "Transgender"
          : prev.Gender, // fallback to existing value
      }));
    }

    // Handle DOB validation and Age calculation
    // else if (name === "DOB") {
    //     const currentDate = new Date();
    //     const minAllowedDate = subYears(currentDate, 100);
    //     const selectedDate = new Date(value);

    //     if (isBefore(minAllowedDate, selectedDate) && isBefore(selectedDate, currentDate)) {
    //         const age = differenceInYears(currentDate, selectedDate);
    //         setPatientEdit((prev) => ({
    //             ...prev,
    //             [name]: formattedValue,
    //             Age: age,
    //         }));
    //     } else {
    //         setPatientEdit((prev) => ({
    //             ...prev,
    //             [name]: formattedValue,
    //             Age: "",
    //         }));
    //     }
    // }

    if (name === "DOB") {
      const currentdate = new Date();
      const minAllowedDate = subYears(currentdate, 100);
      const selectedDate = new Date(value);

      if (
        isBefore(minAllowedDate, selectedDate) &&
        isBefore(selectedDate, currentdate)
      ) {
        const years = differenceInYears(currentdate, selectedDate);
        const months = differenceInMonths(currentdate, selectedDate) % 12;
        const days = differenceInDays(
          currentdate,
          addMonths(addYears(selectedDate, years), months)
        );
        const formattedAge = `${years} Y, ${months} M, ${days} D`;

        setPatientEdit((prevFormData) => ({
          ...prevFormData,
          [name]: value,
          Age: formattedAge,
        }));
      } else {
        setPatientEdit((prevFormData) => ({
          ...prevFormData,
          [name]: value,
          Age: "",
        }));
      }
    }

    // Handle Age change and calculate DOB
    else if (name === "Age") {
      if (
        formattedValue &&
        !isNaN(formattedValue) &&
        formattedValue.length <= 3
      ) {
        const currentDate = new Date();
        const targetYear = subYears(currentDate, formattedValue);
        const dob = startOfYear(targetYear);
        const formattedDOB = format(dob, "yyyy-MM-dd");

        setPatientEdit((prev) => ({
          ...prev,
          [name]: formattedValue,
          DOB: formattedDOB,
        }));
      } else {
        setPatientEdit((prev) => ({
          ...prev,
          [name]: formattedValue,
          DOB: "",
        }));
      }
    }

    // Handle Unique ID validation
    else if (name === "UniqueIdNo") {
      setPatientEdit((prev) => ({
        ...prev,
        [name]: formattedValue,
      }));

      axios
        .get(
          `${UrlLink}Frontoffice/get_unique_id_no_validation?UniqueIdNo=${formattedValue}`
        )
        .then((response) => {
          if (response.data?.error) {
            dispatchvalue({
              type: "toast",
              value: { message: response.data.error, type: "warn" },
            });
          }
        })
        .catch((err) => console.error(err));
    }

    // Default update for other fields
    else {
      setPatientEdit((prev) => ({
        ...prev,
        [name]: formattedValue,
      }));
    }

    if (name === "MaritalStatus") {
      setPatientEdit((prev) => ({
        ...prev,
        [name]: formattedValue,
        SpouseName: formattedValue === "Married" ? prev.SpouseName : "",
        FatherName: formattedValue === "Single" ? prev.FatherName : "",
      }));
      return; // Exit early to avoid the default set
    }

    if (name === "Pincode") {
      setPatientEdit((prev) => ({
        ...prev,
        [name]: formattedValue,
      }));
    }

    // Address handling
    if (
      [
        "DoorNo",
        "Street",
        "Area",
        "City",
        "District",
        "State",
        "Country",
        "Pincode",
      ].includes(name)
    ) {
      setPatientEdit((prev) => ({
        ...prev,
        [name]: formattedValue,
      }));
    }

    // Permanent address handling based on condition
    if (PatientEdit.PermanentAddressSameAsAbove === "NO") {
      if (name === "PermanentPincode") {
        setPatientEdit((prev) => ({
          ...prev,
          [name]: formattedValue,
        }));
      }
      if (
        [
          "PermanentdoorNo",
          "PermanentStreet",
          "PermanentArea",
          "PermanentCity",
          "PermanentDistrict",
          "PermanentState",
          "PermanentCountry",
          "PermanentPincode",
        ].includes(name)
      ) {
        setPatientEdit((prev) => ({
          ...prev,
          [name]: formattedValue,
        }));
      }
    } else {
      setPatientEdit((prev) => ({
        ...prev,
        [name]: formattedValue,
      }));
    }

    // if (name === "PatientCategory") {
    //     setPatientEdit((prev) => ({
    //         ...prev,
    //         [name]:formattedValue,
    //         InsuranceName: formattedValue === "Insurance" ? prev.InsuranceName : "",

    //     }))
    // }
  };

  useEffect(() => {
    if (PatientEdit.Pincode.length > 5) {
      axios
        .get(
          `${UrlLink}Frontoffice/get_location_by_pincode?pincode=${PatientEdit.Pincode}`
        )
        .then((response) => {
          const data = response.data;
          console.log("Pincode response:", data);
          const { country, state, city, district } = data;
          setPatientEdit((prev) => ({
            ...prev,
            Country: country || "",
            State: state || "",
            City: city || "",
            District: district || "",
          }));
        })
        .catch((err) => {
          console.error("Error fetching pincode details:", err);
        });
    }
  }, [PatientEdit.Pincode]); // Dependency on Pincode

  // Effect for permanent address Pincode when "PermanentAddressSame" is "NO"
  useEffect(() => {
    console.log("123");
    if (
      PatientEdit.PermanentAddressSameAsAbove === "No" &&
      PatientEdit.PermanentPincode.length > 5
    ) {
      console.log("900000");
      axios
        .get(
          `${UrlLink}Frontoffice/get_location_by_pincode?pincode=${PatientEdit.PermanentPincode}`
        )
        .then((response) => {
          const data = response.data;
          console.log("Permanent Pincode response:", data);
          const { country, state, city, district } = data;
          setPatientEdit((prev) => ({
            ...prev,
            PermanentCountry: country || "",
            PermanentState: state || "",
            PermanentCity: city || "",
            PermanentDistrict: district || "",
          }));
        })
        .catch((err) => {
          console.error("Error fetching permanent pincode details:", err);
        });
    }
  }, [PatientEdit.PermanentAddressSameAsAbove, PatientEdit.PermanentPincode]); // Dependencies for PermanentAddressSame and PermanentPincode

  const formatLabel = (label) => {
    if (/[a-z]/.test(label) && /[A-Z]/.test(label) && !/\d/.test(label)) {
      return label
        .replace(/([a-z])([A-Z])/g, "$1 $2")
        .replace(/^./, (str) => str.toUpperCase());
    }
    return label;
  };

  // const handlePhotoUpload = (e) => {
  //   const file = e.target.files[0];
  //   if (file) {
  //     const reader = new FileReader();
  //     reader.onloadend = () => {
  //       handleInputChange({
  //         target: { name: "ProfilePhoto", value: reader.result },
  //       });
  //     };
  //     reader.readAsDataURL(file);
  //   }
  // };

  
  // handleSearchChange



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
          console.log("File Loaded:", reader.result); 
          setPatientEdit((prev) => ({
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


  const handleClear = () => {
    setPatientEdit({
      PatientId: "",
      PhoneNo: "",
      Title: "",
      FirstName: "",
      MiddleName: "",
      SurName: "",
      Gender: "",
      MaritalStatus: "",
      SpouseName: "",
      FatherName: "",
      AliasName: "",
      DOB: "",
      Age: "",
      Email: "",
      BloodGroup: "",
      Occupation: "",
      Religion: "",
      Nationality: "",
      UniqueIdType: "",
      UniqueIdNo: "",

      PatientType: "",
      PatientCategory: "",
      InsuranceName: "",
      InsuranceType: "",
      ClientName: "",
      ClientType: "Self",
      ClientEmployeeId: "",
      ClientEmployeeDesignation: "",
      ClientEmployeeRelation: "",
      EmployeeId: "",
      EmployeeRelation: "",
      DoctorId: "",
      DoctorRelation: "",
      DonationType: "",

      DoorNo: "",
      Street: "",
      Area: "",
      City: "",
      District: "",
      State: "",
      Country: "",
      Pincode: "",
      ABHA: "",
      Photo: "",
    });
  };

  const handleSubmit = () => {
    const data = {
      ...PatientEdit,
      created_by: userRecord?.username || "",
    };

    console.log(data, "data");

    axios
      .post(`${UrlLink}Frontoffice/Patient_BasicDetails_Update`, data)
      .then((res) => {
        const resData = res.data;
        console.log(resData, "resData");

        const message = Object.values(resData)[0];
        const type = Object.keys(resData)[0];
        const tdata = {
          message: message,
          type: type,
        };
        console.log(tdata, "tdata");

        dispatchvalue({ type: "toast", value: tdata });
        handleClear();
        
        navigate("/Home/FrontOfficeFolder");
        dispatchvalue({ type: "HrFolder", value: "PatientManagement" });
        dispatchvalue({ type: "setPreviousFolder", value: null });
        dispatchvalue({ type: "showMenu", value: true });
      })
      .catch((err) => console.log(err));
  };

  const handleClose = () => {
    navigate("/Home/PatientList");
  };
  // ---------------------------------------------------------------------------------------------------
  // --------------------------------------------------------------------------------------------------

  const HandlesearchFamily = async () => {
    if (!searchQuery) {
        setError("Please enter a phone number.");
        return;
    }

    try {
        setIsLoading(true);

        const response = await axios.get(`${UrlLink}Frontoffice/search_patients_by_phone/`, {
          params: { phone: searchQuery } 
      });

        const patientData = response.data || [];
        const matchingPatients = Array.isArray(patientData) ? patientData : [];

        const transformedData = matchingPatients.map((member) => ({
            id: member.PatientId,
            name: (`${member.FirstName} ${member.MiddleName || ""} ${member.SurName || ""}`).trim(),
            mobileNumber: member.PhoneNo,
            status: member.Status || "Unknown",
        }));

        setFamilyData(transformedData);
        setError(transformedData.length === 0 ? 'No matching patients found' : '');
    } catch (err) {
        setError('Failed to fetch family member data');
        console.error('Search error:', err);
        setFamilyData([]); 
    } finally {
        setIsLoading(false);
    }
};


const handleAddFamily = async () => {
  try {
      if (!primaryPatientId) {
          setError("Primary patient ID is missing.");
          return;
      }

      if (selectedRows.length === 0) {
          setError("Please select family members to add.");
          return;
      }

      const selectedPatients = FamilyData.filter(patient =>
          selectedRows.includes(patient.id)
      );

      // Update state
      setFamilymembersData(prev => {
          const newMembers = selectedPatients.filter(
              newPatient => !prev.some(existingPatient =>
                  existingPatient.id === newPatient.id
              )
          );
          return [...prev, ...newMembers];
      });

      // Clear selections
      setSelectedRows([]);
      setError("");

      try {
          const response = await axios.post(`${UrlLink}Frontoffice/add_family_members/`, {
              primary_patient_id: primaryPatientId,  
              family_member_ids: selectedRows
          }, {
              headers: { "Content-Type": "application/json" }
          });

          console.log("Family members added:", response.data);
      } catch (saveErr) {
          console.error("Warning: Failed to save to backend:", saveErr);
          setError("Failed to save family members.");
      }

  } catch (err) {
      setError("Failed to add family members.");
      console.error("Add family error:", err);
  }
};


const handleCheckboxChange = (id) => {
  setSelectedRows(prev =>
      prev.includes(id) 
          ? prev.filter(item => item !== id)
          : [...prev, id]
  );
};

  useEffect(() => {
    const fetchPatients = async () => {
      try {
        setIsLoading(true);
        const response = await axios.get(
          `${UrlLink}Frontoffice/search_patients_by_phone`
        );
        setPatientList(response.data || []);
      } catch (err) {
        setError("Failed to fetch patient list");
        console.error("Error fetching patients:", err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchPatients();
  }, [UrlLink]);

  const handleChange = (e) => {
    const value = e.target.value;
    setSearchQuery(value.trim());

    if (value.match(/^\d{10}$/)) {
        setFilteredPatients(patientList.filter(patient => patient.PhoneNo === value));
    } else {
        const nameParts = value.split(" ");
        const filtered = patientList.filter(patient =>
            nameParts.some(part =>
                patient.FirstName.toLowerCase().includes(part.toLowerCase()) ||
                patient.MiddleName?.toLowerCase().includes(part.toLowerCase()) ||
                patient.SurName?.toLowerCase().includes(part.toLowerCase())
            )
        );
        setFilteredPatients(filtered);
    }
};



const [primaryPatientId, setPrimaryPatientId] = useState(null);

useEffect(() => {
    if (FamilyData.length > 0) {
        setPrimaryPatientId(FamilyData[0].id); 
    }
}, [FamilyData]);

const handle_familyUpdate_Submit = async () => {
  if (selectedRows.length === 0) {
      setError("Please select family members to update");
      return;
  }

  try {
      const primaryPatientId = localStorage.getItem("primary_patient_id"); // Ensure this is set

      if (!primaryPatientId) {
          setError("Primary patient ID is missing.");
          return;
      }

      await axios.put(`${UrlLink}Frontoffice/update_family_members/${primaryPatientId}/`, {
          family_member_ids: selectedRows
      }, {
          headers: { "Content-Type": "application/json" }
      });

      setFamilymembersData(FamilyData.filter(patient => selectedRows.includes(patient.id)));
      setSelectedRows([]);
      setError('');

  } catch (err) {
      console.error("Warning: Failed to update backend:", err);
      setError("Failed to update family members");
  }
};


  const getRowStyle = (row) => ({
    backgroundColor: selectedRows.includes(row.id) ? "#e6f3ff" : "transparent",
    color: selectedRows.includes(row.id) ? "blue" : "blue",
    padding: "10px",
    cursor: "pointer",
  });

  const FamilyColumns = [
    { key: "id", name: "ID" },
    { key: "name", name: "Name" },
    { key: "mobileNumber", name: "Mobile Number" },
    {
      key: "status",
      name: "Status",
      renderCell: (params) => (
        <Button disabled={isUpdating} className="cell_btn">
          {params.row.status === "active" ? "ACTIVE" : "INACTIVE"}
        </Button>
      ),
    },
    {
      key: "checklist",
      name: "Select",
      renderCell: (params) => (
        <input
          type="checkbox"
          checked={selectedRows.includes(params.row.id)}
          onChange={() => handleCheckboxChange(params.row.id)}
        />
      ),
    },
  ];

  const FamilymembersColumns = [
    { key: "id", name: "ID" },
    { key: "name", name: "Name" },
    { key: "mobileNumber", name: "Mobile Number" },
  ];
// -------------------------------------------------------------------------------------------------------
// --------------------------------------------------------------------------------------------------------
  return (
    <>
      <div className="RegisFormcon_1">
        <div className="common_center_tag">
          <span>Patient Details Update</span>
        </div>
        {/* -----------------------------------------photo-------------------------------------- */}
        <div className="efuiefh_jn8">
          <div className="ProfilePhotoContainer"
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              marginBottom: "20px",
            }}
          >
            <img
              src={PatientEdit.Photo}
              alt="Profile"
              style={{
                width: "120px",
                height: "120px",
                borderRadius: "90px",
                objectFit: "cover",
                border: "2px solid #ccc",
              }}
            />
            <label
              htmlFor="Photo"
              style={{
                marginTop: "5px",
                padding: "2px 9px",
                backgroundColor: "var(--selectbackgroundcolor)",
                color: "black",
                borderRadius: "4px",
                cursor: "pointer",
                fontSize: "13px",
                display: "inline-block",
              }}
            >
              Choose File
            </label>
            <input
              type="file"
              // accept="image/*"
              accept="image/jpeg, image/png, application/pdf"
              name = "Photo"
              autoComplete="off"
              id="Photo"
              onChange={handleinpchangeDocumentsForm}
              style={{display: "none"}}
            />
          </div>


          {/* ------------------------------------------------------------------------------------------- */}
          <div
            style={{ display: "flex", flexDirection: "column", gap: "10px" }}
          >
            <div className="RegisFormcon">
              {FilteredFormdata &&
                FilteredFormdata.filter(
                  (p) => !["CreatedBy", "Location"].includes(p)
                ).map(
                  (field, indx) =>
                    (field !== "SpouseName" ||
                      ["Married", "Widowed"].includes(
                        PatientEdit.MaritalStatus
                      )) &&
                    (field !== "FatherName" ||
                      ["Single", "Divorced"].includes(
                        PatientEdit.MaritalStatus
                      )) &&
                    (field !== "AliasName" ||
                      ["Mrs"].includes(PatientEdit.Title)) && (
                      <div className="RegisForm_1" key={indx}>
                        <label>
                          {formatLabel(field)}
                          <span>:</span>{" "}
                        </label>
                        {field === "Flagging" ||
                        field === "PatientType" ||
                        field === "Gender" ||
                        field === "UniqueIdType" ||
                        field === "Nationality" ||
                        field === "MaritalStatus" ||
                        field === "BloodGroup" ||
                        field === "Religion" ||
                        field === "Title" ? (
                          <select
                            name={field}
                            value={PatientEdit[field]}
                            onChange={handleInputChange}
                          >
                            <option value="">Select</option>
                            {field === "Gender" &&
                              ["Male", "Female", "TransGender"].map(
                                (option, indx) => (
                                  <option value={option} key={indx}>
                                    {option}
                                  </option>
                                )
                              )}
                            {field === "MaritalStatus" &&
                              ["Single", "Married", "Divorced", "Widowed"].map(
                                (option, indx) => (
                                  <option value={option} key={indx}>
                                    {option}
                                  </option>
                                )
                              )}

                            {field === "Nationality" &&
                              ["Indian", "International"].map(
                                (option, indx) => (
                                  <option value={option} key={indx}>
                                    {option}
                                  </option>
                                )
                              )}

                            {field === "PatientType" &&
                              ["General", "VIP", "Govt"].map((option, indx) => (
                                <option value={option} key={indx}>
                                  {option}
                                </option>
                              ))}

                            {field === "Flagging" &&
                              FlaggData?.filter(
                                (p) => p.Status === "Active"
                              ).map((row, indx) => (
                                <option
                                  key={indx}
                                  value={row.id}
                                  style={{ backgroundColor: row.FlaggColor }}
                                >
                                  {" "}
                                  {row.FlaggName}
                                </option>
                              ))}

                            {field === "UniqueIdType" && (
                              <>
                                {PatientEdit.Nationality === "Indian" &&
                                  ["Aadhar", "VoterId", "SmartCard"].map(
                                    (row, indx) => (
                                      <option key={indx} value={row}>
                                        {row}
                                      </option>
                                    )
                                  )}
                                {PatientEdit.Nationality === "International" &&
                                  ["DrivingLicence", "Passport"].map(
                                    (row, indx) => (
                                      <option key={indx} value={row}>
                                        {row}
                                      </option>
                                    )
                                  )}
                              </>
                            )}
                            {field === "Title" &&
                              TitleNameData?.map((row, indx) => (
                                <option key={indx} value={row.id}>
                                  {row.Title}
                                </option>
                              ))}
                            {field === "BloodGroup" &&
                              BloodGroupData?.map((option, indx) => (
                                <option value={option.id} key={indx}>
                                  {option.BloodGroup}
                                </option>
                              ))}
                            {field === "Religion" &&
                              ReligionData?.map((option, indx) => (
                                <option key={indx} value={option.id}>
                                  {option.religion}
                                </option>
                              ))}
                          </select>
                        ) : field === "PermanentAddressSameAsAbove" ? (
                          <div
                            style={{
                              display: "flex",
                              justifyContent: "space-between",
                              width: "150px",
                            }}
                          >
                            <label
                              style={{ width: "auto" }}
                              htmlFor={`${field}_Yes`}
                            >
                              <input
                                required
                                id={`${field}_Yes`}
                                type="radio"
                                name={field}
                                value="Yes"
                                style={{ width: "15px" }}
                                checked={
                                  PatientEdit[field] === "Yes" ||
                                  PatientEdit[field] === undefined
                                }
                                onChange={(e) =>
                                  handleInputChange({
                                    target: { name: field, value: "Yes" },
                                  })
                                }
                              />
                              Yes
                            </label>
                            <label
                              style={{ width: "auto" }}
                              htmlFor={`${field}_No`}
                            >
                              <input
                                required
                                id={`${field}_No`}
                                type="radio"
                                name={field}
                                value="No"
                                style={{ width: "15px" }}
                                checked={PatientEdit[field] === "No"}
                                onChange={(e) =>
                                  handleInputChange({
                                    target: { name: field, value: "No" },
                                  })
                                }
                              />
                              No
                            </label>
                          </div>
                        ) : (
                          <input
                            type={field === "DOB" ? "date" : "text"}
                            name={field}
                            autoComplete="off"
                            value={PatientEdit[field]}
                            onChange={handleInputChange}
                            readOnly={field === "PatientId"}
                            pattern={
                              field === "Email"
                                ? "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[cC][oO][mM]$"
                                : field === "PhoneNo"
                                ? "\\d{10}"
                                : ["UniqueIdNo"].includes(field)
                                ? "[A-Za-z0-9]+"
                                : field === "Age"
                                ? "\\d{1,3}"
                                : field === "DOB"
                                ? ""
                                : "[A-Za-z]+"
                            }
                          />
                        )}
                      </div>
                    )
                )}
            </div>
          </div>
        </div>

        {/* ----------------- Address --------------- */}

        <br />

        <div className="DivCenter_container">Address</div>
        <br />

        <div className="RegisFormcon" id="RegisFormcon_11">
          {FilteredFormdataAddress &&
            FilteredFormdataAddress.map((field, index) => (
              <div className="RegisForm_1" key={index}>
                {field === "PermanentAddressSameAsAbove" ? (
                  <>
                    <label htmlFor={`${field}_${index}`}>
                      {field === "PermanentAddressSameAsAbove"
                        ? "Permanent Address Same As Above ?"
                        : formatLabel(field)}
                      <span>:</span>
                    </label>
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
                          name={field}
                          value="Yes"
                          style={{ width: "15px" }}
                          checked={PatientEdit[field] === "Yes"}
                          onChange={(e) =>
                            setPatientEdit((prevState) => ({
                              ...prevState,
                              [field]: "Yes",
                            }))
                          }
                        />
                        Yes
                      </label>
                      <label style={{ width: "auto" }} htmlFor={`${field}_no`}>
                        <input
                          required
                          id={`${field}_no`}
                          type="radio"
                          name={field}
                          value="No"
                          style={{ width: "15px" }}
                          checked={PatientEdit[field] === "No"}
                          onChange={(e) =>
                            setPatientEdit((prevState) => ({
                              ...prevState,
                              [field]: "No",
                            }))
                          }
                        />
                        No
                      </label>
                    </div>
                  </>
                ) : (
                  <>
                    <label htmlFor={`${field}_${index}`}>
                      {formatLabel(field)}
                      <span>:</span>
                    </label>
                    <input
                      id={`${field}_${index}`}
                      autoComplete="off"
                      type={field === "Pincode" ? "number" : "text"}
                      name={field}
                      pattern={
                        field === "Pincode"
                          ? "\\d{6,7}"
                          : ["DoorNo"].includes(field)
                          ? "[A-Za-z0-9]+"
                          : "[A-Za-z]+"
                      }
                      className={
                        errors[field] === "Invalid"
                          ? "invalid"
                          : errors[field] === "Valid"
                          ? "valid"
                          : ""
                      }
                      value={PatientEdit[field]}
                      onChange={handleInputChange}
                    />
                  </>
                )}
              </div>
            ))}

          {PatientEdit.PermanentAddressSameAsAbove === "No" ? (
            <>
              <div className="DivCenter_container">Permanent Address</div>
              {FilteredFormdataPermanentAddress &&
                FilteredFormdataPermanentAddress.map((field, index) => (
                  <div className="RegisForm_1" key={index}>
                    <label htmlFor={`${field}_${index}`}>
                      {field === "PermanentPincode"
                        ? "Pincode"
                        : field === "PermanentdoorNo"
                        ? "Door No"
                        : field === "PermanentStreet"
                        ? "Street"
                        : field === "PermanentArea"
                        ? "Area"
                        : field === "PermanentCity"
                        ? "City"
                        : field === "PermanentDistrict"
                        ? "District"
                        : field === "PermanentState"
                        ? "State"
                        : field === "PermanentCountry"
                        ? "Country"
                        : formatLabel(field)}
                      <span>:</span>
                    </label>
                    <input
                      id={`${field}_${index}`}
                      autoComplete="off"
                      type={field === "PermanentPincode" ? "number" : "text"}
                      name={field}
                      pattern={
                        field === "PermanentPincode"
                          ? "\\d{6,7}" // Pattern for 6-7 digit numbers
                          : field === "PermanentdoorNo"
                          ? "[A-Za-z0-9]+" // Alphanumeric pattern
                          : "[A-Za-z]+" // Alphabetic pattern
                      }
                      className={
                        errors[field] === "Invalid"
                          ? "invalid"
                          : errors[field] === "Valid"
                          ? "valid"
                          : ""
                      }
                      value={PatientEdit[field]} // Ensure controlled input
                      onChange={handleInputChange}
                    />
                  </div>
                ))}
            </>
          ) : null}
        </div>

        <div className="Main_container_Btn">
          <button onClick={handleSubmit}>Update</button>
          <button onClick={handleClose}>Close</button>
        </div>
        {/* ---------------------------------FamilymembersColumns----------------------------------------- */}
        <br />

        <div className="RegisFormcon_1 jjxjx_">
          <ReactGrid
            columns={FamilymembersColumns}
            RowData={FamilymembersData}
          />
        </div>

        <div className="Main_container_Btn">
          <button onClick={handle_familyUpdate_Submit}>Update</button>
        </div>

        {/* --------------------------------------------------------------- */}
        <br />
        <div className="DivCenter_container">Family Member</div>
        <br />
        <div className="Main_container_app">
          <div className="RegisFormcon_1">
            <div className="RegisForm_1">
              <label>
                {" "}
                Search Here <span>:</span>{" "}
              </label>
              <input
                list="patients" // Link input to the datalist
                type="text"
                placeholder="Enter Patient Phone Number"
                value={searchQuery}
                onChange={handleChange} // Update the search query
                onKeyDown={(e) => e.key === "Enter" && HandlesearchFamily()} // Trigger search on Enter
              />
              <datalist id="patients">
                {FilterbyPatientNo.map((row, indx) => (
                  <option
                    key={indx}
                    value={`${row.PatientId} | ${row.PhoneNo} | ${
                      row.FirstName
                    } ${row.MiddleName || ""} ${row.SurName || ""}`}
                  >
                    {`${row.PatientId} | ${row.PhoneNo} | ${row.FirstName} ${
                      row.MiddleName || ""
                    } ${row.SurName || ""}`}
                  </option>
                ))}
              </datalist>

              <span>
                <PersonSearchIcon onClick={HandlesearchFamily} />{" "}
                {/* Call the search function on icon click */}
              </span>
            </div>
          </div>
          <ReactGrid
            columns={FamilyColumns}
            RowData={FamilyData}
            getRowStyle={getRowStyle} // Add this line
          />
          {/* <ReactGrid columns={FamilyColumns} RowData={FamilyData} /> */}
          <div className="Main_container_Btn">
            <button
              onClick={handleAddFamily}
              disabled={selectedRows.length === 0}
              style={{ width: "100px" }}
            >
              Add Family
            </button>
          </div>
        </div>
        <br />

        {/* ----------------------------------------------------------------- */}
        <ToastAlert Message={toast.message} Type={toast.type} />

        {/* <ToastContainer /> */}
      </div>
    </>
  );
};

export default PatientDetailsEdit;
