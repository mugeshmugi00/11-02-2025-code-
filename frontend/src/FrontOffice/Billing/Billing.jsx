import React, { useEffect, useLayoutEffect, useRef, useState } from "react";
import debounce from "lodash.debounce";
import {
  differenceInYears,
  format,
  startOfYear,
  subYears,
  isBefore,
} from "date-fns";
// import Clinic_Logo from "../../Assets/logo.png";
import Chirayuulogo from "../../Assets/Chirayuulogo.png";

import axios from "axios";
import ToastAlert from "../../OtherComponent/ToastContainer/ToastAlert";
import PersonSearchIcon from "@mui/icons-material/PersonSearch";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { IoBedOutline } from "react-icons/io5";
import Button from "@mui/material/Button";
import { FaTrash } from "react-icons/fa";
import profile from "../../Assets/profileimg.jpeg";
import "../../App.css";
import { handleKeyDownText } from "../../OtherComponent/OtherFunctions";
import { handleKeyDownPhoneNo } from "../../OtherComponent/OtherFunctions";
// handleKeyDownTextRegistration
import { handleKeyDownTextRegistration } from "../../OtherComponent/OtherFunctions";
import ReactGrid from "../../OtherComponent/ReactGrid/ReactGrid";
import { useReactToPrint } from "react-to-print";
import { NumberToWords } from "../../OtherComponent/OtherFunctions";
import ShoppingCartIcon from "@mui/icons-material/ShoppingCart";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import EditNoteIcon from "@mui/icons-material/EditNote";

const QuickBilling = () => {
  const dispatchvalue = useDispatch();
  const navigate = useNavigate();

  const Registeredit = useSelector((state) => state.Frontoffice?.Registeredit);

  const UrlLink = useSelector((state) => state.userRecord?.UrlLink);
  const UserData = useSelector((state) => state.userRecord?.UserData);
  const IP_DoctorWorkbenchNavigation = useSelector(
    (state) => state.Frontoffice?.IP_DoctorWorkbenchNavigation
  );

  const toast = useSelector((state) => state.userRecord?.toast);
  const [errors, setErrors] = useState({});

  const OP_BillingData = useSelector(
    (state) => state.Frontoffice?.OPBillingData
  );
  console.log("Oppppppp", OP_BillingData);


  // useEffect(()=>{
  //   if(OP_BillingData !==)
  // },[UrlLink])

  const componentRef = useRef();
  const currentDate = new Date();
  const Formdate = format(currentDate, "yyyy-MM-dd");


  // For Lab 
  const [franchaisename, setFranchaisename] = useState("Basic");
  const [franchaise, setfranchaises] = useState([]);
  const [franchaisecolumnname, setfranchaisecolumnname] = useState("Basic")
  const [Department, setDepartment] = useState([])
  const [overallRateCard, setoverallRateCard] = useState([])
  const [testType, setTestType] = useState("Individual");

  const [formData, setFormData] = useState({
    SubDepartment_Code: "",
    SubDepartment_Name: "",
    testType: testType,
  });


  const handleInputChange1234 = (e) => {
    const { name, value } = e.target;
    let SubDepartment_Code;


    if (name === "SubDepartment_Name") {
      const selectedDepartment = Department?.find(
        (item) => item.SubDepartment_Name === value
      );
      SubDepartment_Code = selectedDepartment?.SubDepartment_Code;
    }
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
      SubDepartment_Code: SubDepartment_Code || prevData.SubDepartment_Code,
    }));
  };



  const handleRateCardLims = (e) => {
    setFranchaisename(e.target.value)
    const selectfranchaise = franchaise.find(
      (row) => row.displayNames === e.target.value
    );
    if (selectfranchaise) {
      setfranchaisecolumnname(selectfranchaise.columname);
    }
  };


  useEffect(() => {
    console.log(OP_BillingData?.ServiceProcedureForm);

    if (OP_BillingData?.ServiceProcedureForm === 'Lab') {
      axios
        .get(`${UrlLink}Masters/All_Other_Lab_Masters_POST_AND_GET?Type=RateCardMaster`)
        .then((response) => {
          console.log(response);
          setfranchaises(response.data);
        })
        .catch((error) => {
          console.log(error);
        });

      axios
        .get(`${UrlLink}Masters/All_Other_Lab_Masters_POST_AND_GET?Type=LabSubDepartment`)
        .then((response) => {
          console.log(response);
          setDepartment(response.data);
        })
        .catch((error) => {
          console.error("Error fetching SubDepartment data:", error);
        });

      // Fetch updated rate card amounts only when ratecard changes
      if (franchaisecolumnname !== "Basic") {
        axios
          .get(`${UrlLink}Masters/All_Other_Lab_Masters_POST_AND_GET?Type=RateCardMasterList&ratecard=${franchaisecolumnname}`)
          .then((response) => {
            const responseData = response.data;

            const updatedSelectDatalist = SelectDatalist.map((item) => {
              if (item.type === "individual") {
                const matchedTest = responseData.find((data) => data.Test_Code_id === item.Test_Code);
                return matchedTest
                  ? {
                    ...item, Amount: matchedTest.Schemecost, Charges: matchedTest.Schemecost,
                    NetAmount: matchedTest?.Schemecost,Quantity:1,
                  }
                  : item;
              } else if (item.type === "group") {
                const matchedGroup = responseData.find((data) => data.Group_Code_id === item.Group_Code);
                return matchedGroup
                  ? {
                    ...item, Amount: matchedGroup.Schemecost, Charges: matchedGroup.Schemecost,
                    NetAmount: matchedGroup?.Schemecost,Quantity:1,
                  }
                  : item;
              }
              return item;
            });

            console.log("Updated SelectDatalist:", updatedSelectDatalist);
            setSelectDatalist(updatedSelectDatalist); // Update state properly
          })
          .catch((error) => {
            console.error("Error fetching RateCardMasterList:", error);
          });
      } else {
        setSelectDatalist(OP_BillingData?.ItemDetails)
      }
    }
  }, [UrlLink, franchaisecolumnname]); // Include franchaisecolumnname in the dependency array




  const [ClinicDetials, setClinicDetials] = useState({
    ClinicLogo: null,
    ClinicName: "",
    ClinicGST: "",
    ClinicAddress: "",
    ClinicCity: "",
    ClinicState: "",
    ClinicCode: "",
    ClinicMobileNo: "",
    ClinicLandLineNo: "",
    ClinicMailID: "",
  });

  const [SelectedPatient_list, setSelectedPatient_list] = useState({
    PatientId: "",
    PatientName: "",
    PhoneNumber: "",
    PatientCategory: "General",
    PatientCategoryType: "",
    InsuranceName: "",
    Gender: "",
    City: "",
    State: "",
    PatientAddress: "",
    Pincode: "",
    VisitId: "",
  });

  const [RadiologyNames, setRadiologyNames] = useState([]);
  const [RadioNames, setRadioNames] = useState([]);
  const [PostInvoice, setPostInvoice] = useState(null);
  const [BillingData, setBillingData] = useState({
    InvoiceNo: "",
    InvoiceDate: Formdate,
    DoctorName: "",
    DoctorId: "",
  });
  const [SelectDatalist, setSelectDatalist] = useState([]);
  const [Reimbursable, setReimbursable] = useState(false);
  const [SelectDatalist1, setSelectDatalist1] = useState([]);
  const [initialState, setinitialState] = useState({
    totalItems: 0,
    totalTaxable: 0,
    totalAmount: 0,
    totalDiscount: 0,
    totalGstamount: 0,
    totalUnits: 0,
    totalNetAmount: 0,
    PaidAmount: 0,
    BalanceAmount: 0,
    Roundoff: 0,
    ReimbursableAmount: 0,
    totalAmountt: 0,
  });
  const [billAmount, setBillAmount] = useState([]);
  const [isPrintButtonVisible, setIsPrintButtonVisible] = useState(true);
  const [isPrintSummary, setisPrintSummary] = useState(false);
  const [Doctorsnames, setDoctorsnames] = useState([]);
  const [Patient_list, setPatient_list] = useState([]);
  const [selectedOption, setSelectedOption] = useState("IPDServices");
  const [Uptateitem, setUptateitem] = useState(false);
  const [SelectItemState, setSelectItemState] = useState({
    ServiceType: "",
    Servicecode: "",
    SelectItemName: "",
    Rate: "",
    Charges: "",
    Amount: "",
    DiscountType: "",
    Discount: "",
    GST: "",
    Total: "",
    GSTamount: "",
    Quantity: "",
    DiscountAmount: "",
  });
  const [NetAmount_CDmethod, setNetAmount_CDmethod] = useState({
    Method: "",
    Amount: "",
  });
  const [formAmount, setFormAmount] = useState({
    Billpay_method: "",
    CardType: "",
    CardNo: "",
    upiid: "",
    TransactionId: "",
    ChequeNo: "",
    BankName: "",
    paidamount: "",
    Additionalamount: "",
    transactionFee: "",
  });
  const [ServiceProcedure, setServiceProcedure] = useState({
    ServiceCategory: '',
    Categoryid: '',
    ServiceSubCategory: '',
    ServiceSubCatId: '',
    Subcategorypk: '',
    Rate: '',
    Quantity: "",
  });

  const [ServiceCategoryData, setServiceCategoryData] = useState([])
  const [ServiceSubCategoryData, setServiceSubCategoryData] = useState([])

  const [ServiceData, setServiceData] = useState([]);
  const [LabData, setLabData] = useState([]);

  const blockInvalidChar = (e) =>
    ["e", "E", "+", "-"].includes(e.key) && e.preventDefault();
  const [totalPaidAmount, settotalPaidAmount] = useState(0);
  const [isEdit, setIsEdit] = useState(null);

  const [FilterbyPatientId, setFilterbyPatientId] = useState([]);

  // const [patientsearchoption, setpatientsearchoption] = useState("PatientID");
  const [patientsearch, setpatientsearch] = useState({
    Search: "",
  });
  const [AppointmentRegisType, setAppointmentRegisType] = useState(Object.keys(OP_BillingData).length !== 0 ? "OP" : "IP");
  const [SmartCard, setSmartCard] = useState({
    SmartCardNo: "",
  });
  const [isClient, setisClient] = useState({
    isClient: "No",
    CoPaymentType: "Percentage",
    CoPaymentTypeinp: "",
    CoPaymentLogic: "PreAuth",
    CoPaymentdeducted: "PreAuth",
    PreAuthType: "Percentage",
    PreAuthTypeinp: "",
    PreAuthAmount: "",
    PreAuthApprovalNo: "",
    PolicyNo: "",
    PolicyStartDate: "",
    PolicyEndDate: "",
  });

  const [AdvanceAmount, setAdvanceAmount] = useState({
    isAdvance: 'No',
    AdvanceAmount: '',
  })
  const [AdvanceAmountGet, setAdvanceAmountGet] = useState([])
  const [AdvanceTotal, setAdvanceTotal] = useState([])
  const [RemainingCredit, setRemainingCredit] = useState([])
  console.log('Advancetotallll', AdvanceTotal);
  console.log('RemainingCredittt', RemainingCredit);

  const [register, setregister] = useState({
    isregister: "No",
    registerAmount: "",
  });
  const [ServiceProcedureForm, setServiceProcedureForm] =
    useState("Consultation");
  const [ServiceProcedureData, setServiceProcedureData] = useState([]);
  const [ServiceProcedureDataGet, setServiceProcedureDataGet] = useState([]);
  const [Consultation, setConsultation] = useState({
    PhysicianType: "",
    Physician: "",
    Service: "",
    Procedure: "",
    DrugName: "",
    LabTest: "",
    RadiologyDept: "",
    RadiologyTest: "",
    SubTestName: "",
    Rate: "",
    Quantity: "",
    Charges: "",
    Amount: "",
    DiscountType: "",
    Discount: "",
    GST: "",
    GSTamount: "",
    Total: "",
    DiscountAmount: "",
  });
  const [PhysicianData, setPhysicianData] = useState([]);
  const [SpecializationData, setSpecializationData] = useState([]);
  const [DoctorData, setDoctorData] = useState([]);
  const [DoctorRateData, setDoctorRateData] = useState([]);
  const [ReferralDoctorData, setReferralDoctorData] = useState([]);
  const [EmployeeData, setEmployeeData] = useState([]);
  const [DoctorIdData, setDoctorIdData] = useState([]);
  const [FlaggData, setFlaggData] = useState([]);
  const [ReligionData, setReligionData] = useState([]);
  const [AllDoctorData, setAllDoctorData] = useState([]);
  const [InsuranceData, setInsuranceData] = useState([]);
  const [ClientData, setClientData] = useState([]);
  const [DonationData, setDonationData] = useState([]);

  const [printoption, setprintoption] = useState("PrintDetailed");
  const [RegisterData, setRegisterData] = useState({
    PatientId: "",
    ABHA: "",
    PatientName: "",
    AgeGender: "",
    PhoneNo: "",
    PatientCategory: "",
    PatientCategoryName: "",
    Address: "",
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
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [
          specializationResponse,
          referralDoctorResponse,
          EmployeeResponse,
          DoctorResponse,
          FlaggData,
          ReligionData,
          AllDoctorData,
          Insurancedata,
          ClientData,
          DonationData,
        ] = await Promise.all([
          axios.get(`${UrlLink}Masters/Speciality_Detials_link`),
          axios.get(`${UrlLink}Masters/get_referral_doctor_Name_Detials`),
          axios.get(`${UrlLink}Frontoffice/get_Employee_by_PatientCategory`),
          axios.get(`${UrlLink}Frontoffice/get_DoctorId_by_PatientCategory`),
          axios.get(`${UrlLink}Masters/Flagg_color_Detials_link`),
          axios.get(`${UrlLink}Masters/Relegion_Master_link`),
          axios.get(`${UrlLink}Masters/get_All_doctor_Name_Detials`),
          axios.get(`${UrlLink}Masters/get_insurance_data_registration`),
          axios.get(`${UrlLink}Masters/get_client_data_registration`),
          axios.get(`${UrlLink}Masters/get_donation_data_registration`),
        ]);

        console.log("spppeeecccc", specializationResponse);

        setSpecializationData(
          Array.isArray(specializationResponse.data)
            ? specializationResponse.data
            : []
        );
        setReferralDoctorData(
          Array.isArray(referralDoctorResponse.data)
            ? referralDoctorResponse.data
            : []
        );
        setEmployeeData(
          Array.isArray(EmployeeResponse.data) ? EmployeeResponse.data : []
        );
        setDoctorIdData(
          Array.isArray(DoctorResponse.data) ? DoctorResponse.data : []
        );
        setFlaggData(Array.isArray(FlaggData.data) ? FlaggData.data : []);
        setReligionData(
          Array.isArray(ReligionData.data) ? ReligionData.data : []
        );
        setAllDoctorData(
          Array.isArray(AllDoctorData.data) ? AllDoctorData.data : []
        );
        setInsuranceData(
          Array.isArray(Insurancedata.data) ? Insurancedata.data : []
        );
        setClientData(Array.isArray(ClientData.data) ? ClientData.data : []);
        setDonationData(
          Array.isArray(DonationData.data) ? DonationData.data : []
        );
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [UrlLink]);

  useEffect(() => {
    if (Object.keys(Registeredit).length === 0) {
      const postdata = {
        PatientId: RegisterData.PatientId,
        PhoneNo: RegisterData.PhoneNo,
        FirstName: RegisterData.FirstName,
        DoctorId: RegisterData.DoctorName,
      };
      console.log("PosttttDDDD", postdata);

      axios
        .get(`${UrlLink}Frontoffice/Filter_Patient_by_Multiple_Criteria`, {
          params: postdata,
        })
        .then((res) => {
          const data = res.data;
          console.log("1222222", data);

          setFilterbyPatientId(data);
          // axios
          //   .get(`${UrlLink}Frontoffice/get_patient_visit_details`, {
          //     params: postdata,
          //   })
          //   .then((res) => {
          //     const visit = res.data?.VisitPurpose;
          //     console.log("Vissssss", res.data);

          //     setRegisterData((prev) => ({
          //       ...prev,
          //       VisitPurpose: visit,
          //     }));
          //   })
          //   .catch((err) => {
          //     console.log(err);
          //   });
        })
        .catch((err) => {
          console.log(err);
        });
    }
  }, [UrlLink, AppointmentRegisType]);


// Track previous totals
const prevTotalsRef = useRef({
  totalNetAmount: 0,
  totalUnits: 0,
  totalDiscount: 0,
  totalGstamount: 0,
  totalAmount: 0,
});

// Recalculate totals when SelectDatalist or NetAmount_CDmethod changes
useEffect(() => {
  let updatedTotals = {
    totalUnits: 0,
    totalAmount: 0,
    totalDiscount: 0,
    totalGstamount: 0,
    totalNetAmount: 0,
  };

  // Iterate through SelectDatalist and sum up values
  SelectDatalist.forEach((item) => {
    updatedTotals.totalUnits += +item.Quantity || 0;
    updatedTotals.totalAmount += parseFloat(item.Charges) || 0;
    updatedTotals.totalDiscount += parseFloat(item.Discount) || 0;
    updatedTotals.totalGstamount += parseFloat(item.GST) || 0;
    updatedTotals.totalNetAmount += parseFloat(item.NetAmount) || 0;
  });

  // Apply Discount Logic
  let additionalDiscount = 0;

  if (NetAmount_CDmethod.Amount !== "" && NetAmount_CDmethod.Method !== "") {
    if (NetAmount_CDmethod.Method === "Percentage") {
      additionalDiscount = (updatedTotals.totalAmount * NetAmount_CDmethod.Amount) / 100;
    } else if (NetAmount_CDmethod.Method === "Cash") {
      additionalDiscount = parseFloat(NetAmount_CDmethod.Amount) || 0;
    }
  }

  // Ensure the discount does not exceed the total amount
  let finalDiscount = Math.min(updatedTotals.totalAmount, updatedTotals.totalDiscount + additionalDiscount);

  // Adjust net amount after applying discount
  let totalTaxableAmount = updatedTotals.totalAmount - finalDiscount;

  // Corrected GST calculation based on the updated taxable amount
  let updatedGst = (totalTaxableAmount * (updatedTotals.totalGstamount / updatedTotals.totalAmount)) || 0;

  // Correct total net amount after discount and GST
  let finalNetAmount = totalTaxableAmount + updatedGst;

  // Preserve PaidAmount and calculate BalanceAmount correctly
  setinitialState((prevState) => ({
    ...prevState,
    totalItems: SelectDatalist.length,
    totalUnits: updatedTotals.totalUnits,
    totalDiscount: finalDiscount.toFixed(2),
    totalGstamount: updatedGst.toFixed(2),
    totalNetAmount: finalNetAmount.toFixed(2),
    totalAmount: finalNetAmount.toFixed(2),
    BalanceAmount: (finalNetAmount - prevState.PaidAmount).toFixed(2),
    Roundoff: (Math.round(finalNetAmount) - finalNetAmount).toFixed(2),
  }));

  // Update previous totals reference
  prevTotalsRef.current = { ...updatedTotals };
}, [SelectDatalist, NetAmount_CDmethod]);

console.log('SelectDatalist:', SelectDatalist);



  useEffect(() => {
    const totalPaidAmount = billAmount
      .filter((_, indx) => indx !== isEdit)
      .reduce((total, ele) => +total + +ele.paidamount, 0);
    settotalPaidAmount(totalPaidAmount);

    const totalPaidAddAmount = billAmount
      .filter((_, indx) => indx !== isEdit)
      .reduce(
        (total, ele) => +total + +ele.paidamount + (+ele.Additionalamount || 0),
        0
      );

    const totalAdditionalAmount = billAmount
      .filter((_, indx) => indx !== isEdit)
      .reduce((total, ele) => +total + +ele.Additionalamount, 0);

    const totalTransactionFee = billAmount
      .filter((_, indx) => indx !== isEdit)
      .reduce((total, ele) => +total + +ele.transactionFee || 0, 0); // Use `|| 0` to handle empty or undefined values.
    // Calculate the total transaction fee (as an absolute amount, not percentage)
    const totalTransactionAmount = billAmount
      .filter((_, indx) => indx !== isEdit)
      .reduce(
        (total, ele) =>
          total +
          ((+ele.paidamount + +ele.Additionalamount) *
            (+ele.transactionFee || 0)) /
          100, // Apply transaction fee proportionally
        0
      );

    const totalAmmm = totalPaidAddAmount + totalTransactionAmount;

    console.log("totalPaidAddAmount", totalPaidAddAmount);
    console.log("totalAdditionalAmount", totalAdditionalAmount);
    console.log("totalTransactionFee", totalTransactionFee);
    console.log("totalAmmm", totalAmmm);

    settotalPaidAmount(totalPaidAmount);
    setinitialState((prev) => ({
      ...prev,
      totalAmountt: totalAmmm.toFixed(2),
      BalanceAmount: (
        parseFloat(Math.round(prev.totalNetAmount)) -
        parseFloat(totalPaidAmount)
      ).toFixed(2),
      PaidAmount: totalPaidAmount.toFixed(2),
      Additionalamount: totalAdditionalAmount.toFixed(2),
      transactionfee: `${totalTransactionFee}%`,
    }));
  }, [billAmount, billAmount.length, isEdit]);

  const HandlesearchPatient = (value) => {

  };

  useEffect(() => {
    axios.get(`${UrlLink}Masters/services_Group_list_details`)
      .then((res) => {
        const ress = res.data
        console.log(ress, 'ddhdhdhdhdhdhdhdhdhdhdhdhdhdh');

        setServiceCategoryData(ress)
      })
      .catch((err) => {
        console.log(err);
      })
  }, [UrlLink]);

  const HandleSearchchange = (e) => {
    const { name, value } = e.target;
    const exist = FilterbyPatientId.find((f) => f.PatientId === value);
    if (!exist) {
      const tdata = {
        message: "Please enter a valid Patient Id",
        type: "warn",
      };
      dispatchvalue({ type: "toast", value: tdata });
    } else {
      axios
        .get(
          `${UrlLink}Frontoffice/get_Patient_Details_by_patientId?PatientId=${value}`
        )
        .then((res) => {
          const { PatientProfile, PatientId, ABHA, AliasName, PatientName, PhoneNo, Address, AgeGender, ...resss } = res.data;
          console.log("paaatttttttttt", res.data);

          setRegisterData((prev) => ({
            ...prev,
            PatientId: PatientId || "",
            ABHA: '64-9456-6541-8451',
            PatientName: PatientName || "",
            AgeGender: AgeGender || "",
            PhoneNo: PhoneNo || "",
            PatientCategory: 'General',
            Address: Address || "",
          }));
          setSmartCard((prev) => ({
            ...prev,
            SmartCardNo: PatientId || "",
          }));
          setpatientsearch((prev) => ({
            ...prev,
            [name]: value,
          }));
        })
        .catch((err) => console.log(err));
    }
  };


  const HandleClientCheck = (e) => {
    if (RegisterData.PatientId !== "" && RegisterData.InsuranceName !== "") {
      if (
        RegisterData.PatientCategory === "Insurance" ||
        RegisterData.PatientCategory === "Client"
      ) {
        setisClient((prevState) => ({
          ...prevState,
          isClient: prevState.isClient === "No" ? "Yes" : "No",
          CoPaymentType: "Percentage",
          CoPaymentTypeinp: "",
          CoPaymentLogic: "PreAuth",
          CoPaymentdeducted: "PreAuth",
          PreAuthType: "Percentage",
          PreAuthTypeinp: "",
          PreAuthAmount: "",
          PreAuthApprovalNo: "",
          PolicyNo: "",
          PolicyStartDate: "",
          PolicyEndDate: "",
        }));
      } else {
        const tdata = {
          message: "Please Select the Client/Insurance/TPA Patient Category",
          type: "warn",
        };
        dispatchvalue({ type: "toast", value: tdata });
        setisClient((prev) => ({
          ...prev,
          isClient: "No",
        }));
      }
    } else {
      const tdata = {
        message: "Please enter valid PatientId details.",
        type: "warn",
      };
      dispatchvalue({ type: "toast", value: tdata });
    }
  };
  const HandleOnClient = (e) => {
    const { name, value } = e.target;

    // Check if the input field is for CoPaymentTypeinp or PreAuthTypeinp
    if (name === "CoPaymentTypeinp" || name === "PreAuthTypeinp") {
      setisClient((prevState) => ({
        ...prevState,
        [name]: value, // Update the respective input field state
      }));
    } else {
      setisClient((prevState) => ({
        ...prevState,
        [name]: value, // Update other fields
      }));
    }
  };
  const handledispatch = () => {
    const tdata = {
      message: "Please enter search details.",
      type: "error",
    };
    dispatchvalue({ type: "toast", value: tdata });
  };

  const HandleOnchange = async (e) => {
    const { name, value, pattern } = e.target;

    const formattedValue = [
      "FirstName",
      "MiddleName",
      "SurName",
      "Occupation",
      "NextToKinName",
      "FamilyHeadName",
      "Street",
      "Area",
      "City",
      "State",
      "Country",
    ].includes(name)
      ? `${value.charAt(0).toUpperCase()}${value.slice(1)}`
      : value;

    // Check length for specific fields
    if (
      [
        "InsuranceName",
        "ClientName",
        "FirstName",
        "MiddleName",
        "SurName",
        "Occupation",
        "NextToKinName",
        "FamilyHeadName",
        "Street",
        "Area",
        "City",
        "State",
        "Country",
        "UniqueIdNo",
      ].includes(name) &&
      value.length > 30
    ) {
      const tdata = {
        message: `${name} should not exceed 30 characters.`,
        type: "warn", // Ensure 'warn' is a valid type for your toast system
      };
      dispatchvalue({ type: "toast", value: tdata });
      return; // Exit early to prevent state update
    }

    if (name === "PatientId") {
      setRegisterData((prev) => ({
        ...prev,
        IsConsciousness: "Yes",
        [name]: value,
        PhoneNo: "",
        Title: "",
        FirstName: "",
        MiddleName: "",
        SurName: "",
        Gender: "",
        DOB: "",
        Age: "",
        Email: "",
        BloodGroup: "",
        Occupation: "",
        Religion: "",
        Nationality: "",
        UniqueIdType: "",
        UniqueIdNo: "",
        CaseSheetNo: "",

        VisitPurpose: "",

        Complaint: "",
        PatientType: "General",
        PatientCategory: "General",

        DoorNo: "",
        Street: "",
        Area: "",
        City: "",
        State: "",
        Country: "",
        Pincode: "",
      }));
    } else if (name === "PhoneNo" || name === "RelativePhoneNo") {
      if (formattedValue.includes("|")) {
        const convert = formattedValue.split(" | ");
        console.log(convert);

        if (convert.length <= 10) {
          setRegisterData((prev) => ({
            ...prev,
            [name]: convert[2].trim(),
            PatientId: convert[0].trim(),
            FirstName: convert[1].trim(),
          }));
        }
      } else {
        if (formattedValue.length <= 10) {
          setRegisterData((prev) => ({
            ...prev,
            [name]: formattedValue,
          }));
        }
      }
    } else if (name === "FirstName") {
      if (formattedValue.includes("|")) {
        const convert = formattedValue.split(" | ");

        setRegisterData((prev) => ({
          ...prev,
          [name]: convert[1].trim(),
          PatientId: convert[0].trim(),
          PhoneNo: convert[2].trim(),
        }));
      } else {
        setRegisterData((prev) => ({
          ...prev,
          [name]: formattedValue,
        }));
      }
    } else if (name === "Title") {
      setRegisterData((prev) => ({
        ...prev,
        [name]: formattedValue,
        Gender: ["Miss", "Ms", "Mrs"].includes(value)
          ? "Female"
          : ["Mr", "Master", "Baby"].includes(value)
            ? "Male"
            : "TransGender",
      }));
    } else if (name === "DOB") {
      const currentdate = new Date();
      // Calculate the minimum allowed date (100 years before current date)
      const minAllowedDate = subYears(currentdate, 100);
      const selectedDate = new Date(value);

      if (
        isBefore(minAllowedDate, selectedDate) &&
        isBefore(selectedDate, currentdate)
      ) {
        const age = differenceInYears(currentdate, selectedDate);

        setRegisterData((prevFormData) => ({
          ...prevFormData,
          [name]: formattedValue,
          Age: age,
        }));
      } else {
        setRegisterData((prevFormData) => ({
          ...prevFormData,
          [name]: formattedValue,
          Age: "",
        }));
      }
    } else if (name === "Age") {
      if (formattedValue) {
        if (!isNaN(formattedValue) && formattedValue.length <= 3) {
          // Get the current date
          const currentDate = new Date();

          // Calculate the year to subtract
          const targetYear = subYears(currentDate, formattedValue);

          // Create a date for January 1st of the target year
          const dob = startOfYear(targetYear);

          // Format the DOB
          const formattedDOB = format(dob, "yyyy-MM-dd");
          setRegisterData((prev) => ({
            ...prev,
            [name]: formattedValue,
            DOB: format(formattedDOB, "yyyy-MM-dd"),
          }));
        }
      } else {
        setRegisterData((prev) => ({
          ...prev,
          [name]: formattedValue,
          DOB: "",
        }));
      }
    } else if (name === "ReferredBy") {
      try {
        const response = await axios.get(
          `${UrlLink}Masters/get_route_details?DoctorId=${value}`
        );
        const route = response.data;

        if (route) {
          setRegisterData((prevState) => ({
            ...prevState,
            [name]: formattedValue,
            RouteNo: route.RouteNo,
            RouteName: route.RouteName,
            TehsilName: route.TehsilName,
            VillageName: route.VillageName,
          }));
        } else {
          setRegisterData((prevState) => ({
            ...prevState,
            [name]: formattedValue,
            RouteNo: "",
            RouteName: "",
            TehsilName: "",
            VillageName: "",
          }));
        }
      } catch (error) {
        console.error("Error fetching route details:", error);
        setRegisterData((prevState) => ({
          ...prevState,
          [name]: formattedValue,
          RouteNo: "",
          RouteName: "",
          TehsilName: "",
          VillageName: "",
        }));
      }
    } else if (name === "Specialization") {
      setRegisterData((prev) => ({
        ...prev,
        [name]: formattedValue,
        DoctorName: "",
      }));
    } else if (name === "DoctorName") {
      setRegisterData((prev) => ({
        ...prev,
        [name]: formattedValue,
      }));

      // Filter for the selected doctor based on the doctor_id
      const doctor_list = DoctorData.find(
        (doc) => doc.doctor_id === formattedValue
      );

      // Check if the doctor was found
      if (doctor_list) {
        const doctor_schedule = doctor_list.schedule?.[0]; // Access the first schedule in the doctor's schedule list
        console.log("RequestedSchedule", doctor_schedule);

        if (doctor_schedule?.working === "yes") {
          const currentTime = new Date();

          // Single Shift
          if (doctor_schedule?.shift === "Single") {
            const startTime = doctor_schedule.starting_time;
            const endTime = doctor_schedule.ending_time;

            // Convert schedule times to Date objects
            const startTimeDate = new Date(`1970-01-01T${startTime}Z`);
            const endTimeDate = new Date(`1970-01-01T${endTime}Z`);

            // Check if the current time is within the available time
            if (currentTime >= startTimeDate && currentTime <= endTimeDate) {
              const tdata = {
                message: `The Doctor is currently Available`,
                type: "success",
              };
              dispatchvalue({ type: "toast", value: tdata });
            } else {
              const tdata = {
                message: `The Doctor is not Available at this time, Available from ${startTime} to ${endTime}`,
                type: "warn",
              };
              dispatchvalue({ type: "toast", value: tdata });
            }
          }

          // Double Shift
          else if (doctor_schedule?.shift === "Double") {
            const startTime_f = doctor_schedule.starting_time_f;
            const endTime_f = doctor_schedule.ending_time_f;
            const startTime_a = doctor_schedule.starting_time_a;
            const endTime_a = doctor_schedule.ending_time_a;

            // Convert schedule times to Date objects
            const startTimeDate_f = new Date(`1970-01-01T${startTime_f}Z`);
            const endTimeDate_f = new Date(`1970-01-01T${endTime_f}Z`);
            const startTimeDate_a = new Date(`1970-01-01T${startTime_a}Z`);
            const endTimeDate_a = new Date(`1970-01-01T${endTime_a}Z`);

            // Check if the current time falls within either shift (forenoon or afternoon)
            if (
              (currentTime >= startTimeDate_f &&
                currentTime <= endTimeDate_f) ||
              (currentTime >= startTimeDate_a && currentTime <= endTimeDate_a)
            ) {
              const tdata = {
                message: `The Doctor is currently Available`,
                type: "success",
              };
              dispatchvalue({ type: "toast", value: tdata });
            } else {
              const tdata = {
                message: `The Doctor is not Available at this time, Available in FN: ${startTime_f} to ${endTime_f} or AN: ${startTime_a} to ${endTime_a}`,
                type: "warn",
              };
              dispatchvalue({ type: "toast", value: tdata });
            }
          }
        }
      } else {
        const tdata = {
          message: "Doctor not found",
          type: "error",
        };
        dispatchvalue({ type: "toast", value: tdata });
      }
    } else if (name === "UniqueIdNo") {
      setRegisterData((prev) => ({
        ...prev,
        [name]: formattedValue,
      }));

      axios
        .get(
          `${UrlLink}Frontoffice/get_unique_id_no_validation?UniqueIdNo=${formattedValue}`
        )
        .then((reponse) => {
          let data = reponse.data;
          console.log("ressss", data);
          if (data && data.error) {
            // Show a toast if the unique ID already exists
            const tdata = {
              message: data.error,
              type: "warn", // Assuming you want to show a warning toast
            };
            dispatchvalue({ type: "toast", value: tdata });
          }
        })
        .catch((err) => {
          console.log(err);
        });
    } else if (name === "Pincode") {
      setRegisterData((prev) => ({
        ...prev,
        [name]: formattedValue,
      }));

      axios
        .get(
          `${UrlLink}Frontoffice/get_location_by_pincode?pincode=${formattedValue}`
        )
        .then((reponse) => {
          let data = reponse.data;
          console.log("ressss", data);
          if (formattedValue.length > 5) {
            const { country, state, city } = data;
            setRegisterData((prev) => ({
              ...prev,
              Country: country,
              State: state,
              City: city,
            }));
          }
        })
        .catch((err) => {
          console.log(err);
        });
    } else {
      setRegisterData((prev) => ({
        ...prev,
        [name]: formattedValue,
      }));
    }
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


  const HandleOnchangeService = (e) => {
    const { name, value } = e.target;
    if (name === 'ServiceCategory') {
      if (value.includes('-')) {
        const value1 = value.split('-')
        const value2 = value1[0];
        const value3 = value1[1];
        console.log('serrrrrr', value1, value2, value3);
        setServiceProcedure((prev) => ({
          ...prev,
          Categoryid: value2,
          [name]: value3,
        }))

        if (value2) {
          axios.get(`${UrlLink}Masters/services_Subcategory_details_by_category?ServiceCategory=${value2}`)
            .then((res) => {
              const ress = res.data
              console.log(ress, 'ddhdhdhdhdhdhdhdhdhdhdhdhdhdh');

              setServiceSubCategoryData(ress)
            })
            .catch((err) => {
              console.log(err);
            })
        }
      }
      else {
        setServiceProcedure((prev) => ({
          ...prev,
          [name]: value,
          Categoryid: '',
          ServiceSubCategory: '',
          ServiceSubCatId: '',
          Subcategorypk: '',
          Rate: '',
          Quantity: "",
        }))
      }
    } else if (name === 'ServiceSubCategory') {
      const value1 = value.split('-');
      if (value1.length === 3) {
        const subcategorypk = value1[0];
        const subCategoryid = value1[1];
        const subCategoryname = value1[2];
        setServiceProcedure((prev) => ({
          ...prev,
          ServiceSubCatId: subCategoryid,
          [name]: subCategoryname,
          Subcategorypk: subcategorypk,
        }));
      } else if (value1.length === 2) {
        const subcategorypk = value1[0];
        const subCategoryname = value1[1];
        setServiceProcedure((prev) => ({
          ...prev,
          Subcategorypk: subcategorypk,
          [name]: subCategoryname,
        }));
      } else if (value1.length === 4) {
        const subcategorypk = value1[0];
        const roomno = value1[1];
        const bedno = value1[2];
        const Wardname = value1[3];
        const subCategoryname = roomno + bedno + Wardname;
        setServiceProcedure((prev) => ({
          ...prev,
          Subcategorypk: subcategorypk,
          [name]: subCategoryname,
        }));
      } else {
        setServiceProcedure((prev) => ({
          ...prev,
          [name]: value,
        }));
      }
    }
    else {
      setServiceProcedure((prev) => ({
        ...prev,
        [name]: value,
        Categoryid: '',
        ServiceSubCatId: '',
        Subcategorypk: '',
      }));
    }
  }



  useEffect(() => {
    const postdata = {
      ServiceCategory: ServiceProcedure.Categoryid,
      ServicesubCategory: ServiceProcedure.Subcategorypk,
      Patientcategory: OP_BillingData.PatientCategory,
      PatientcategoryId: OP_BillingData.PatientCategoryId,
      patientid: OP_BillingData.PatientId,
    };

    console.log('possttt', postdata);

    axios
      .get(`${UrlLink}Masters/services_Subcategory_details_by_Patient_category`, {
        params: postdata, // Use params to send query parameters
      })
      .then((response) => {
        const res = response.data;
        console.log('ressssss', res);
        console.log('amttt', res?.[0]?.amt);
        setServiceProcedure((prev) => ({
          ...prev,
          Rate: res?.[0]?.amt,
          Quantity: 1,
        }))
      });
  }, [UrlLink, ServiceProcedure.Categoryid, ServiceProcedure.Subcategorypk]);


  const HandleSmartCard = () => { };


  const handleRegisterChange = (event, isInputChange = false) => {
    if (!isInputChange) {
      // Handle checkbox toggle
      if (patientsearch !== "" && RegisterData.PatientId !== "") {
        setregister((prev) => ({
          ...prev,
          isregister: prev.isregister === "No" ? "Yes" : "No",
        }));

        if (register.isregister === "No") {
          // Add registration row if it doesn't exist
          const alreadyExists = SelectDatalist.some(
            (item) => item.SelectItemName === "Registration"
          );

          if (!alreadyExists) {
            const listdata = {
              ServiceType: AppointmentRegisType,
              SelectItemName: "Registration",
              Rate: 300 || "",
              Quantity: 1 || "",
              Charges: 300 || "",
              Amount: 300 || "",
              DiscountType: "-",
              Discount: "-",
              GST_per: "-",
              GST: "-",
              NetAmount: 300 || "",
            };
            setSelectDatalist((prev) => [
              ...prev,
              { S_No: prev.length + 1, ...listdata },
            ]);
          }
        }
      } else {
        // Handle validation error
        const tdata = {
          message: "Please enter valid PatientId details.",
          type: "warn",
        };
        dispatchvalue({ type: "toast", value: tdata });
      }
    } else {
      // Handle input field change
      const { value } = event.target;
      setregister((prev) => ({
        ...prev,
        registerAmount: value,
      }));

      // Update the existing "Registration" row if present
      setSelectDatalist((prev) =>
        prev.map((item) =>
          item.SelectItemName === "Registration"
            ? {
              ...item,
              Rate: value || "0",
              Charges: value || "0",
              Amount: value || "0",
              NetAmount: value || "0",
            }
            : item
        )
      );
    }
  };

  const gridRef = useRef(null);

  const cleardata = () => {
    setRegisterData({
      PatientId: "",
      Title: "",
      FirstName: "",
      MiddleName: "",
      SurName: "",
      Gender: "",
      DOB: "",
      Age: "",
      Email: "",
      PhoneNo: "",
      BloodGroup: "",
      Occupation: "",
      Religion: "",
      Nationality: "",
      UniqueIdType: "",
      UniqueIdNo: "",
      CaseSheetNo: "",

      VisitPurpose: "",

      Complaint: "",
      PatientType: "General",
      PatientCategory: "General",

      DoorNo: "",
      Street: "",
      Area: "",
      City: "",
      State: "",
      Country: "",
      Pincode: "",
    });
    setpatientsearch({
      Search: "",
    });
    setisClient({
      isClient: "No",
      CoPaymentType: "Percentage",
      CoPaymentTypeinp: "",
      CoPaymentLogic: "PreAuth",
      CoPaymentdeducted: "PreAuth",
      PreAuthType: "Percentage",
      PreAuthTypeinp: "",
      PreAuthAmount: "",
      PreAuthApprovalNo: "",
      PolicyNo: "",
      PolicyStartDate: "",
      PolicyEndDate: "",
    });
    setSmartCard({
      SmartCardNo: "",
    });
    setConsultation({
      PhysicianType: "",
      Physician: "",
      Service: "",
      Procedure: "",
      DrugName: "",
      LabTest: "",
      RadiologyDept: "",
      RadiologyTest: "",
      SubTestName: "",
      Rate: "",
      Quantity: "",
      Charges: "",
      Amount: "",
      DiscountType: "",
      Discount: "",
      GST: "",
      GSTamount: "",
      Total: "",
      DiscountAmount: "",
    });
    setServiceProcedureForm("Consultation");
    setErrors({});
  };

  const clearservices = () => {
    setConsultation({
      PhysicianType: "",
      Physician: "",
      Service: "",
      Procedure: "",
      DrugName: "",
      LabTest: "",
      RadiologyDept: "",
      RadiologyTest: "",
      Rate: "",
      Quantity: "",
      Charges: "",
      Amount: "",
      DiscountType: "",
      Discount: "",
      GST: "",
      GSTamount: "",
      Total: "",
      DiscountAmount: "",
    });
  };

  const handleChangeBillingData = (e) => {
    const { name, value } = e.target;
    console.log("value", value);

    const finddata = Doctorsnames.find((ele) => ele.ShortName === value);

    if (finddata) {
      setBillingData((prev) => ({
        ...prev,
        [name]: value,
        DoctorId: finddata.Doctor_ID,
      }));
    } else {
      setBillingData((prev) => ({
        ...prev,
        [name]: value,
        DoctorId: "",
      }));
    }
  };

  useEffect(() => {
    if (patientsearch !== "" && ServiceProcedureForm !== "") {
      axios
        .get(`${UrlLink}Masters/Lab_Test_Name_link`)
        .then((response) => {
          const res = response?.data;
          console.log("ressssss", res);
          setLabData(res);
        })
        .catch((e) => {
          console.log(e);
        });
    }
  }, [UrlLink, ServiceProcedureForm, Consultation.LabTest]);

  // useEffect(() => {
  //   if (RegisterData.PatientId !== "" && ServiceProcedureForm !== "") {
  //     axios
  //       .get(`${UrlLink}Masters/Lab_Test_Name_link`)
  //       .then((response) => {
  //         const res = response?.data;
  //         console.log("ressssss", res);
  //         setLabData(res);
  //       })
  //       .catch((e) => {
  //         console.log(e);
  //       });
  //   }
  // }, [UrlLink]);

  useEffect(() => {
    setServiceData([]);
    if (RegisterData.PatientCategory !== "" && ServiceProcedureForm !== "") {
      if (["Insurance", "Client"].includes(RegisterData.PatientCategory)) {
        axios
          .get(`${UrlLink}Frontoffice/get_merged_service_data_bill`, {
            params: {
              PatientCategory: RegisterData.PatientCategory,
              ServiceProcedureForm,
              location: UserData?.location,
            },
          })
          .then((res) => {
            const data = res?.data;
            console.log("serrrrrrr", data);
            setServiceData(data || []);
          })
          .catch((err) => {
            console.log(err);
          });
      } else if (
        !["Insurance", "Client"].includes(RegisterData.PatientCategory) &&
        patientsearch.Search !== ""
      ) {
        axios
          .get(`${UrlLink}Frontoffice/get_merged_service_data_bill`, {
            params: {
              PatientCategory: RegisterData.PatientCategory,
              ServiceProcedureForm,
              location: UserData?.location,
            },
          })
          .then((res) => {
            const data = res?.data;
            console.log("serrrrrrr", data);
            setServiceData(data || []);
          })
          .catch((err) => {
            console.log(err);
          });
      }
    }
  }, [
    ServiceProcedureForm,
    UserData?.location,
    ServiceProcedureForm,
    Consultation.Procedure,
    Consultation.Service,
  ]);

  useEffect(() => {
    if (
      Consultation.Service !== "" &&
      ServiceProcedureForm === "GeneralBillingItem" &&
      ServiceData?.length !== 0
    ) {
      const finddata = ServiceData?.find(
        (ele) => ele.Service_Id === +Consultation?.Service
      );
      console.log('serviceeeeee', finddata);


      if (finddata && Object.keys(finddata).length !== 0) {
        setConsultation((prev) => ({
          ...prev,
          Amount: finddata.charge,
          GST: finddata?.GstValue === "Nill" ? 0 : finddata?.GstValue,
          Rate: finddata.charge,
        }));
      }
    } else if (
      Consultation.Procedure !== "" &&
      ServiceProcedureForm === "Procedure" &&
      ServiceData?.length !== 0
    ) {
      const finddata = ServiceData?.find(
        (ele) => ele.Service_Id === +Consultation.Procedure
      );

      if (finddata && Object.keys(finddata).length !== 0) {
        setConsultation((prev) => ({
          ...prev,
          Amount: finddata.charge,
          GST: finddata?.GstValue === "Nill" ? 0 : finddata?.GstValue,
          Rate: finddata.charge,
        }));
      }
    } else if (
      patientsearch.Search !== "" &&
      Consultation.PhysicianType !== "" &&
      Consultation.Physician !== "" &&
      ServiceProcedureForm === "Consultation" &&
      DoctorRateData?.length !== 0
    ) {
      console.log("gotttttttinnnn");

      console.log("DoctorRateData:", DoctorRateData);
      console.log("Ratecard Details:", DoctorRateData.Ratecarddetials);
      console.log(
        "RegisterData.PatientCategory:",
        RegisterData.PatientCategory
      );

      const finddata = DoctorRateData?.Ratecarddetials?.find(
        (ele) => ele?.RatecardType === RegisterData?.PatientCategory
      );
      console.log("finddataaaaaa", finddata);
      if (finddata && Object.keys(finddata).length !== 0) {
        setConsultation((prev) => ({
          ...prev,
          Amount: Number(finddata.consultation_curr_fee) || 0, // Ensure charge is a valid number
          GST:
            finddata?.GstValue === "Nill" ? 0 : Number(finddata?.GstValue) || 0, // Convert GST to a number
          Rate: Number(finddata?.consultation_curr_fee) || 0, // Convert Amount to a number
        }));
      }
    } else if (
      patientsearch.Search !== "" &&
      Consultation.LabTest !== "" &&
      ServiceProcedureForm === "Lab" &&
      LabData?.length !== 0
    ) {
      const finddata = LabData?.find(
        (ele) => ele?.TestCode === Consultation?.LabTest
      );
      console.log("finddataaa", finddata);

      if (finddata && Object.keys(finddata).length !== 0) {
        setConsultation((prev) => ({
          ...prev,
          Amount: Number(finddata.charge) || 0, // Ensure charge is a valid number
          GST:
            finddata?.GstValue === "Nill" ? 0 : Number(finddata?.GstValue) || 0, // Convert GST to a number
          Rate: Number(finddata?.Amount) || 0, // Convert Amount to a number
        }));
      }
    } else if (
      patientsearch.Search !== "" &&
      Consultation.RadiologyTest !== "" &&
      ServiceProcedureForm === "Radiology" &&
      RadioNames?.length !== 0
    ) {
      const finddata = RadioNames?.find(
        (ele) => ele?.id === Consultation?.RadiologyTest
      );
      console.log("finddataaa", finddata);

      if (finddata && Object.keys(finddata).length !== 0) {
        setConsultation((prev) => ({
          ...prev,
          Amount: Number(finddata.charge) || 0, // Ensure charge is a valid number
          GST:
            finddata?.GstValue === "Nill" ? 0 : Number(finddata?.GstValue) || 0, // Convert GST to a number
          Rate: Number(finddata?.Amount) || 0, // Convert Amount to a number
        }));
      }
    }
  }, [
    patientsearch.Search,
    Consultation.Service,
    Consultation.Procedure,
    Consultation.LabTest,
    DoctorRateData,
    Consultation.PhysicianType,
    Consultation.Physician,
    Consultation.RadiologyTest,
    ServiceProcedureData,
    ServiceProcedureForm,
  ]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;

    // Update the consultation state
    setConsultation((prev) => {
      // List of fields that need to reset others
      const resetFields = [
        "PhysicianType",
        "Physician",
        "Service",
        "Procedure",
        "DrugName",
        "LabTest",
        "RadiologyDept",
        "RadiologyTest",
      ];

      // If one of the reset fields changes, clear the remaining fields
      if (resetFields.includes(name)) {
        return {
          ...prev,
          [name]: value,
          Physician: name === "Physician" ? value : "",
          Service: name === "Service" ? value : "",
          Procedure: name === "Procedure" ? value : "",
          DrugName: name === "DrugName" ? value : "",
          LabTest: name === "LabTest" ? value : "",
          // RadiologyDept: name === "RadiologyDept" ? value : "",
          RadiologyTest: name === "RadiologyTest" ? value : "",
          SubTestName: name === "SubTestName" ? value : "",
          Rate: "",
          Quantity: "",
          Charges: "",
          Amount: "",
          DiscountType: "",
          Discount: "",
          GST: "",
          GSTamount: "",
          Total: "",
          DiscountAmount: "",
        };
      }

      return {
        ...prev,
        [name]: value,
      };
    });
    // // If PhysicianType changes, trigger the API call
    // if (name === "PhysicianType") {
    //   axios
    //     .get(`${UrlLink}Ip_Workbench/IP_InchargeAndRefer_Details_Link`, {
    //       params: {
    //         Type: value,
    //         RegistrationId: IP_DoctorWorkbenchNavigation?.RegistrationId,
    //       },
    //     })
    //     .then((response) => {
    //       const res = response.data;
    //       console.log("Physician data", res);
    //       setPhysicianData(res);
    //     })
    //     .catch((e) => {
    //       console.log(e);
    //     });
    // }

    // Handle Discount and GST calculation based on the Discount Type
    if (name === "Discount" && Consultation.DiscountType === "Cash") {
      if (+Consultation.Charges <= +value) {
        alert("Discount is larger than Total Amount");
      } else {
        const selectAmount =
          +Consultation.Rate * +Consultation.Quantity - +value;
        const gstAmount = (+selectAmount * +Consultation.GST) / 100;
        const totalAmount = +selectAmount + +gstAmount;

        setConsultation((prev) => ({
          ...prev,
          [name]: value,
          Amount: selectAmount.toFixed(2),
          Total: totalAmount.toFixed(2),
          DiscountAmount: value,
          GSTamount: gstAmount.toFixed(2) || "",
        }));
      }
    } else if (
      name === "Discount" &&
      Consultation.DiscountType === "Percentage"
    ) {
      if (+value >= 100) {
        alert("Discount percentage cannot be greater than 99");
      } else {
        const discountValue =
          (+Consultation.Rate * +Consultation.Quantity * +value) / 100;
        const selectAmount =
          +Consultation.Rate * +Consultation.Quantity - discountValue;
        const gstAmount = (+selectAmount * +Consultation.GST) / 100;
        const totalAmount = +selectAmount + +gstAmount;

        setConsultation((prev) => ({
          ...prev,
          [name]: value,
          Amount: selectAmount.toFixed(2),
          Total: totalAmount.toFixed(2),
          DiscountAmount: discountValue.toFixed(2),
          GSTamount: gstAmount.toFixed(2) || "",
        }));
      }
    }

    // When DiscountType changes, reset Discount and recalculate Amount and Total
    else if (name === "DiscountType") {
      const calculatedAmount = +Consultation.Rate * +Consultation.Quantity;
      const gstAmount = (+calculatedAmount * +Consultation.GST) / 100;
      const totalAmount = +calculatedAmount + +gstAmount;

      setConsultation((prev) => ({
        ...prev,
        [name]: value,
        Discount: "",
        DiscountAmount: "",
        Amount: calculatedAmount.toFixed(2),
        Total: totalAmount.toFixed(2),
        GSTamount: gstAmount.toFixed(2) || "",
      }));
    }

    // When Quantity changes, update Charges, Amount, GST, and Total
    else if (name === "Quantity") {
      const calculatedCharges = +Consultation.Rate * +value;
      const gstAmount = (+calculatedCharges * +Consultation.GST) / 100;
      const totalAmount = +calculatedCharges + +gstAmount;

      setConsultation((prev) => ({
        ...prev,
        [name]: value,
        Charges: calculatedCharges.toFixed(2),
        Amount: calculatedCharges.toFixed(2),
        Total: totalAmount.toFixed(2),
        GSTamount: gstAmount.toFixed(2) || "",
        DiscountType: "",
        Discount: "",
      }));
    }

    // When GST changes, update the calculation based on discount and GST
    else if (name === "GST") {
      // Calculate the charges after applying the discount (if any)
      let discountedAmount = +Consultation.Rate * +Consultation.Quantity;

      if (Consultation.DiscountType === "Cash" && Consultation.Discount) {
        discountedAmount = discountedAmount - +Consultation.Discount;
      } else if (
        Consultation.DiscountType === "Percentage" &&
        Consultation.Discount
      ) {
        const discountValue = (discountedAmount * +Consultation.Discount) / 100;
        discountedAmount = discountedAmount - discountValue;
      }

      // Calculate the GST based on the discounted amount
      const gstAmount = (+discountedAmount * +value) / 100;
      const totalAmount = +discountedAmount + +gstAmount;

      setConsultation((prev) => ({
        ...prev,
        [name]: value, // Set the new GST percentage
        GSTamount: gstAmount.toFixed(2), // Set the GST amount
        Total: totalAmount.toFixed(2), // Set the total amount including GST
      }));
    }

    // General field update for all other fields
    else {
      setConsultation((prev) => ({
        ...prev,
        [name]: value,
      }));
    }
  };

  const handleReimbursableChange = (event, index) => {
    const updatedList = SelectDatalist.map((item, i) =>
      i === index
        ? { ...item, isReimbursable: event.target.checked ? "Yes" : "No" }
        : item
    );

    // Check if any item in the updated list has isReimbursable as "Yes"
    const anyReimbursable = updatedList.some(
      (item) => item.isReimbursable === "Yes"
    );

    // Update states
    setSelectDatalist(updatedList); // Update state with the modified data
    setReimbursable(anyReimbursable); // Set true if any checkbox is "Yes", otherwise false

    console.log("Updated List:", updatedList);
    console.log("Is any item reimbursable?", anyReimbursable);
  };

  const handleInputChange1 = (e) => {
    const { name, value } = e.target;

    setSelectedOption("IPDServices");

    if (name === "PatientId") {
      const Getdata = Patient_list.find((ele) => ele.PatientId === value);

      if (Getdata) {
        setSelectedPatient_list((prev) => ({
          ...prev,
          PatientId: Getdata?.PatientId,
          PatientName: Getdata?.FirstName,
          PhoneNumber: Getdata?.PhoneNo,
          Gender: Getdata.Gender,
          City: Getdata.City,
          State: Getdata.State,
          PatientAddress: Getdata?.Area,
          Pincode: Getdata.Pincode,
        }));
      } else {
        setSelectedPatient_list((prev) => ({
          ...prev,
          [name]: value,
          PatientName: "",
          PhoneNumber: "",
          PatientCategory: "General",
          InsuranceName: "",
          Gender: "",
          City: "",
          State: "",
          PatientAddress: "",
          Pincode: "",
          VisitId: "",
        }));
      }
    }
    if (name === "PatientName") {
      const Getdata = Patient_list.find((ele) => ele.FirstName === value);

      if (Getdata) {
        setSelectedPatient_list((prev) => ({
          ...prev,
          PatientId: Getdata?.PatientId,
          PatientName: Getdata?.FirstName,
          PhoneNumber: Getdata?.PhoneNo,
          Gender: Getdata.Gender,
          City: Getdata.City,
          State: Getdata.State,
          PatientAddress: Getdata?.Area,
          Pincode: Getdata.Pincode,
        }));
      } else {
        setSelectedPatient_list((prev) => ({
          ...prev,
          [name]: value,
          PatientId: "",
          PhoneNumber: "",
          PatientCategory: "General",
          InsuranceName: "",
          Gender: "",
          City: "",
          State: "",
          PatientAddress: "",
          Pincode: "",
          VisitId: "",
        }));
      }
    } else if (name === "PhoneNumber") {
      const Getdata = Patient_list.find((ele) => ele.PhoneNo === value);

      if (Getdata) {
        setSelectedPatient_list((prev) => ({
          ...prev,
          PatientId: Getdata?.PatientId,
          PatientName: Getdata?.FirstName,
          PhoneNumber: Getdata?.PhoneNo,
          Gender: Getdata.Gender,
          City: Getdata.City,
          State: Getdata.State,
          PatientAddress: Getdata?.Area,
          Pincode: Getdata.Pincode,
        }));
      } else {
        setSelectedPatient_list((prev) => ({
          ...prev,
          [name]: value,
          PatientId: "",
          PatientName: "",
          PatientCategory: "General",
          InsuranceName: "",
          Gender: "",
          City: "",
          State: "",
          PatientAddress: "",
          Pincode: "",
          VisitId: "",
        }));
      }
    }
    if (name === "PatientCategory") {
      setSelectedPatient_list((prev) => ({
        ...prev,
        [name]: value,
      }));
    } else {
      setSelectedPatient_list((prev) => ({
        ...prev,
        [name]: value,
      }));
    }
  };

  const Additemstobillfun = () => {
    // Define required fields based on ServiceProcedureForm type
    const requiredfields = ['ServiceCategory', 'ServiceSubCategory'];
    const existing = requiredfields.filter((field) => !ServiceProcedure[field]);
    if (existing.length !== 0) {
      // Alert the user to fill in the missing required fields
      alert(`Please fill the required fields: ${existing.join(", ")}`);
    } else {
      // Check if the same ServiceType and the correct ItemName already exist in SelectDatalist
      const Checktest = SelectDatalist.some(
        (ele) =>
          ele.ServiceType === ServiceProcedure.ServiceCategory &&
          ele.SelectItemName === ServiceProcedure.ServiceSubCategory // Dynamically check the appropriate item name field
      );
      console.log("checkkkk", Checktest);
      if (Checktest) {
        alert(`${ServiceProcedure.ServiceSubCategory} already exists`);
      } else {
        // Create a new item with ServiceType and the available Consultation data
        const listdata = {
          ServiceType: ServiceProcedure.ServiceCategory,
          SelectItemName: ServiceProcedure.ServiceSubCategory,
          Quantity: parseFloat(ServiceProcedure.Quantity) || 1,
          Charges: parseFloat(ServiceProcedure.Rate) || 0,
          Amount: parseFloat(ServiceProcedure.Rate) || 0,
          NetAmount: parseFloat(ServiceProcedure.Rate * ServiceProcedure.Quantity) || 0,
          isReimbursable: "No",
        };

        console.log("Adding item:", listdata); // Log the data being added

        // Calculate the updated BalanceAmount based only on the newly added item
        const newBalanceAmount = parseFloat(listdata.NetAmount);

        // Update the SelectDatalist with the new item and recalculate the balance
        setSelectDatalist((prev) => [
          ...prev,
          { S_No: prev.length + 1, ...listdata },
        ]);

        setinitialState((prevState) => ({
          ...prevState,
          BalanceAmount: (
            parseFloat(prevState.BalanceAmount) + newBalanceAmount
          ).toFixed(2),
        }));

        // Reset the form after adding
        setServiceProcedure({
          ServiceCategory: '',
          Categoryid: '',
          ServiceSubCategory: '',
          ServiceSubCatId: '',
          Subcategorypk: '',
          Rate: '',
          Quantity: "",
        });
      }
    }
  };


// Delete billing item
const deletebillingitem = (row) => {
  const S_No = row.S_No;

  let Temp_delarr = SelectDatalist.filter((ele) => ele.S_No !== S_No);

  // Update state and trigger recalculation of totals
  setSelectDatalist(
    Temp_delarr.map((item, index) => ({ ...item, S_No: index+1}))
);
};  

  useEffect(() => {
    if (OP_BillingData.id && OP_BillingData.Type === 'OPEdit') {
      const Itemlist = OP_BillingData.Billing_Items
      const PaymentDetails = OP_BillingData.Payment_Details

      setpatientsearch((prev) => ({
        ...prev,
        Search: OP_BillingData?.PatientId,
      }));

      setSmartCard((prev) => ({
        ...prev,
        SmartCardNo: OP_BillingData.PatientId,
      }));

      setBillingData((prev) => ({
        ...prev,
        DoctorName: OP_BillingData.Doctor_Name || "",
        DoctorId: OP_BillingData.Doctor_Id || "",
      }));
      setRegisterData((prev) => ({
        ...prev,
        ABHA: '64-9456-6541-8451',
        PatientName: OP_BillingData.Patient_Name || "",
        AgeGender: OP_BillingData.AgeGender || "",
        PhoneNo: OP_BillingData.PhoneNo || "",
        PatientCategory: OP_BillingData.PatientCategory || "",
        PatientCategoryName: OP_BillingData.PatientCategoryName || "",
        Address: OP_BillingData.Address || "",
        PatientId: OP_BillingData.PatientId || "",
      }));
      setSelectedPatient_list((prev) => ({
        ...prev,
        PatientId: OP_BillingData.PatientId,
        PatientName: OP_BillingData.Patient_Name,
        PhoneNumber: OP_BillingData.PhoneNo,
        PatientCategory: OP_BillingData.PatientCategory,
        Gender: OP_BillingData.Gender,
        City: OP_BillingData.City,
        State: OP_BillingData.State,
        PatientAddress: OP_BillingData.Area,
        Pincode: OP_BillingData.Pincode,
        RegisterId: OP_BillingData.Register_Id,
        VisitId: OP_BillingData.Visit_Id,
      }))
      // setinitialState((prev)=>({
      //   ...prev,
      //   totalItems: OP_BillingData.totalItems,
      //   totalTaxable: 0,
      //   totalAmount: OP_BillingData.TotalAmount,
      //   totalDiscount: 0,
      //   totalGstamount: 0,
      //   totalUnits: OP_BillingData.TotalQty,
      //   totalNetAmount: OP_BillingData.Net_Amount,
      //   PaidAmount: OP_BillingData.PaidAmount,
      //   BalanceAmount: OP_BillingData.BalanceAmount,
      //   Roundoff: OP_BillingData.RoundOff,
      //   ReimbursableAmount: 0,
      //   totalAmountt: OP_BillingData,
      // }))

      const Items = Itemlist.map(
        (service, index) => {
          return {
            S_No: index + 1, // Add serial number based on index
            ServiceType: service.Service_Type,
            SelectItemName: service.Service_Name,
            Charges: parseFloat(service.Charge),
            Amount: parseFloat(service.Amount),
            DiscountType: "",
            Discount: "",
            GST_per: service.GST_per,
            GST: service.GST_Charge,
            Status: service.Status,
            NetAmount: parseFloat(service.Total_Amount),
            Quantity: parseFloat(service.Quantity),
            isReimbursable: "No",
          };
        }
      );
      setSelectDatalist(Items)
      const Payment = PaymentDetails.map((item, ind) => ({
        Billpay_method: item.Payment_Type,
        CardType: item.Card_Type,
        CardNo: item.Card_No,
        upiid: item.upiid,
        TransactionId: item.TransactionId,
        ChequeNo: item.Cheque_No,
        BankName: item.Bank_Name,
        paidamount: item.Amount,
        Additionalamount: item.AdditionalAmount,
        transactionFee: item.Transaction_Amount,
      }))
      setBillAmount(Payment)
    }
  }, [UrlLink, OP_BillingData])

  useEffect(() => {
    if (
      Object.keys(OP_BillingData).length !== 0 && OP_BillingData.id !== "" && OP_BillingData.id !== undefined
    ) {
      // First axios call to fetch IP Billing Service List
      axios
        .get(`${UrlLink}Frontoffice/Get_OP_Billing_Details_SingleId`, {
          params: {
            QueueList_ID: OP_BillingData?.id,
          },
        })
        .then((res) => {
          let GetIPBillingdata = res.data;
          let GetIPBillingdataService = res.data.Billing_data_list;

          console.log("GetIPBillingdata", GetIPBillingdata);
          console.log("GetIPBillingdataService", GetIPBillingdataService);

          if (Object.values(GetIPBillingdata).length > 5) {
            // Setting Doctor and Patient details
            setBillingData((prev) => ({
              ...prev,
              DoctorName: GetIPBillingdata.Doctor_ShortName || "",
              DoctorId: GetIPBillingdata.Doctor_ID || "",
            }));
            setpatientsearch((prev) => ({
              ...prev,
              Search: OP_BillingData?.PatientId,
            }));

            setSmartCard((prev) => ({
              ...prev,
              SmartCardNo: OP_BillingData.PatientId,
            }));

            setRegisterData((prev) => ({
              ...prev,
              ABHA: '64-9456-6541-8451',
              PatientName: OP_BillingData.Patient_Name || "",
              AgeGender: OP_BillingData.AgeGender || "",
              PhoneNo: OP_BillingData.PhoneNo || "",
              PatientCategory: OP_BillingData.PatientCategory || "",
              PatientCategoryName: OP_BillingData.PatientCategoryName || "",
              Address: OP_BillingData.Address || "",
              PatientId: OP_BillingData.PatientId || "",
            }));
            setAppointmentRegisType(OP_BillingData.VisitType);

            setSelectedPatient_list((prev) => ({
              ...prev,
              PatientId: GetIPBillingdata.PatientId,
              PatientName: GetIPBillingdata.Patient_Name,
              PhoneNumber: GetIPBillingdata.PhoneNo,
              PatientCategory: GetIPBillingdata.PatientCategory,
              Gender: GetIPBillingdata.Gender,
              City: GetIPBillingdata.City,
              State: GetIPBillingdata.State,
              PatientAddress: GetIPBillingdata.Area,
              Pincode: GetIPBillingdata.Pincode,
              RegisterId: GetIPBillingdata.Registration_Id,
              QueueList_ID: GetIPBillingdata.id,
              VisitId: GetIPBillingdata.VisitId,
            }));
            // Map over GetIPBillingdataService to get service data
            let mappedServiceData = GetIPBillingdataService.map(
              (service, index) => {
                return {
                  S_No: index + 1, // Add serial number based on index
                  ServiceType: service.Service_Type,
                  SelectItemName: service.Service_Name,
                  Charges: parseFloat(service.Charge),
                  Amount: parseFloat(service.Amount),
                  DiscountType: "",
                  Discount: "",
                  GST_per: service.GST_per,
                  GST: service.GST_Charge,
                  Status: service.Status,
                  NetAmount: parseFloat(service.NetAmount),
                  Quantity: parseFloat(service.Quantity) || 1,
                  isReimbursable: "No",
                };
              }
            );

            // Only add Adddata if the necessary fields are not empty
            let Adddata = {
              ServiceType: GetIPBillingdata.Billing_Type,
              SelectItemName: GetIPBillingdata.ServiceName,
              Rate: GetIPBillingdata.Service_Fee,
              Charges: GetIPBillingdata.Service_Fee,
              Amount: GetIPBillingdata.Service_Fee,
              DiscountType: "",
              Discount: "",
              GST_per: "",
              Total: GetIPBillingdata.Service_Fee,
              GST: "",
              Quantity: 1,
              Status: GetIPBillingdata.Status,
              DiscountAmount: "",
              isReimbursable: "No",
            };

            // Conditionally add Adddata only if ServiceName and Service_Fee are present
            if (
              Adddata.SelectItemName &&
              Adddata.ServiceType &&
              Adddata.Service_Fee
            ) {
              mappedServiceData = [Adddata, ...mappedServiceData];
            }

            // Set the updated service data to SelectDatalist
            setSelectDatalist(mappedServiceData);
            // Second axios call to fetch additional room billing data
          }
        })
        .catch((err) => {
          console.log(err);
        });

      if (OP_BillingData.ServiceProcedureForm === "Lab") {
        setServiceProcedureForm(OP_BillingData.ServiceProcedureForm)
        setSelectDatalist(OP_BillingData?.ItemDetails)
      }

    }
    // else {
    //   navigate("/Home/QuickBilling")
    // }
  }, [UrlLink, OP_BillingData]);

  useEffect(() => {
    // Aggregate data by ServiceType and calculate cumulative quantity, amount, and net amount
    const aggregatedData = SelectDatalist.reduce((acc, curr) => {
      const existing = acc.find((item) => item.ServiceType === curr.ServiceType);
      if (existing) {
        // If the ServiceType already exists, update the cumulative values
        existing.Quantity += curr.Quantity;
        existing.Amount += curr.Amount;
        existing.NetAmount += curr.NetAmount;
      } else {
        // If the ServiceType doesn't exist, create a new entry
        acc.push({
          ServiceType: curr.ServiceType,
          Quantity: curr.Quantity,
          Amount: curr.Amount,
          NetAmount: curr.NetAmount,
        });
      }
      return acc;
    }, []);
  
    console.log("Aggregated Data:", aggregatedData);
  
    // Set aggregated data to SelectDatalist1
    setSelectDatalist1(aggregatedData);
  }, [SelectDatalist]);
  

  const handleChange = (e) => {
    const { name, value } = e.target;
    const total_netamount = Math.round(initialState.totalNetAmount).toFixed(2);

    if (+totalPaidAmount !== +total_netamount) {
      if (name === "Billpay_method") {
        setFormAmount((prevState) => ({
          ...prevState,
          [name]: value,
        }));
      }
      else if (name === "CardNo") {
        if (value.length < 5) {
          setFormAmount((prevState) => ({
            ...prevState,
            [name]: value,
          }));
        }
      }
      else if (name === "TransactionId") {
        setFormAmount((prevState) => ({
          ...prevState,
          [name]: value.toUpperCase(),
        }));
      }
      else if (name === "paidamount") {
        if (billAmount.length > 0) {
          const amttt = parseFloat(total_netamount) - totalPaidAmount;
          if (+amttt >= +value) {
            setFormAmount((prevState) => ({
              ...prevState,
              [name]: value,
            }));
          } else {
            alert(`enter the Correct value blow the Net Amount ${amttt}`);
            setFormAmount((prevState) => ({
              ...prevState,
              [name]: "",
            }));
          }
        } else {
          if (+total_netamount >= +value) {
            setFormAmount((prevState) => ({
              ...prevState,
              [name]: value,
            }));
          } else {
            alert(
              `enter the Correct value blow the Net Amount ${total_netamount}`
            );
            setFormAmount((prevState) => ({
              ...prevState,
              [name]: "",
            }));
          }
        }
      } else {
        setFormAmount((prev) => ({
          ...prev,
          [name]: value,
        }));
      }
    } else {
      alert("No Balance Amount");
    }
  };

  const handleAdd = () => {
    let req = [];
    if (formAmount.Billpay_method === "Card") {
      req = ["Billpay_method", "CardType", "paidamount"];
    } else if (formAmount.Billpay_method === "Cheque") {
      req = ["Billpay_method", "ChequeNo", "BankName", "paidamount"];
    } else if (formAmount.Billpay_method === "OnlinePayment") {
      req = ["Billpay_method", "paidamount"];
    } else {
      req = ["Billpay_method", "paidamount"];
    }
    const missing = req.filter((row) => !formAmount[row]);
    if (missing.length === 0) {
      const exist = billAmount.find(
        (p) => p.Billpay_method === formAmount.Billpay_method
      );
      if (!exist) {
        setBillAmount((prev) => [...prev, formAmount]);
        setFormAmount({
          Billpay_method: "",
          CardType: "",
          CardNo: "",
          upiid: "",
          TransactionId: "",
          ChequeNo: "",
          BankName: "",
          paidamount: "",
          Additionalamount: "",
          transactionFee: "",
        });
      } else {
        alert("The Payment Method already exist");
      }
    } else {
      alert(`enter the required fields : ${missing.join(",")}`);
    }
  };

  const handleUpdate = () => {
    let req = [];
    if (formAmount.Billpay_method === "Card") {
      req = ["Billpay_method", "CardType", "paidamount"];
    } else if (formAmount.Billpay_method === "Cheque") {
      req = ["Billpay_method", "ChequeNo", "BankName", "paidamount"];
    } else if (formAmount.Billpay_method === "OnlinePayment") {
      req = ["Billpay_method", "paidamount"];
    } else {
      req = ["Billpay_method", "paidamount"];
    }
    const missing = req.filter((row) => !formAmount[row]);
    if (missing.length === 0) {
      const data = [...billAmount];
      data[isEdit] = formAmount;

      setBillAmount(data);
      setFormAmount({
        Billpay_method: "",
        CardType: "",
        CardNo: "",
        upiid: "",
        TransactionId: "",
        ChequeNo: "",
        BankName: "",
        paidamount: "",
        Additionalamount: "",
        transactionFee: "",
      });
      setIsEdit(null);
    } else {
      alert(`enter the required fields : ${missing.join(",")}`);
    }
  };

  const handleEdit = (index) => {
    console.log(index, "---");

    const item = billAmount[index];

    if (item.Billpay_method === "Advance") {
      let Remove = billAmount.filter((ele) => ele.Billpay_method !== "Advance");
      setBillAmount(Remove);
    } else {
      setIsEdit(index);
      const item = billAmount[index];
      setFormAmount({
        ...item,
      });
    }
  };

  // Automatically update ServiceProcedureForm when AppointmentRegisType changes
  useEffect(() => {
    if (AppointmentRegisType === "Laboratory") {
      setServiceProcedureForm("Lab");
    } else if (AppointmentRegisType === "Pharmacy") {
      setServiceProcedureForm("Pharmacy");
    } else if (AppointmentRegisType === "Radiology") {
      setServiceProcedureForm("Radiology");
    }
  }, [UrlLink, AppointmentRegisType]);

  // Automatically update ServiceProcedureForm when AppointmentRegisType changes
  useEffect(() => {
    if (
      RegisterData.PatientCategory === "Insurance" ||
      RegisterData.PatientCategory === "Client"
    ) {
      axios
        .get(
          `${UrlLink}Frontoffice/get_client_insurance_details?PatientId=${patientsearch.Search}`
        )
        .then((response) => {
          const res = response.data;
          console.log("ccccllliii", res);
          // Destructure the response data
          const {
            isClient,
            CoPaymentType,
            CoPaymentTypeinp,
            CoPaymentLogic,
            CoPaymentdeducted,
            PreAuthType,
            PreAuthTypeinp,
            PreAuthAmount,
            PreAuthApprovalNo,
            PolicyNo,
            PolicyStartDate,
            PolicyEndDate,
          } = res;

          // Update the state for isClient
          setisClient((prev) => ({
            ...prev,
            isClient: isClient,
            CoPaymentType,
            CoPaymentTypeinp,
            CoPaymentLogic,
            CoPaymentdeducted,
            PreAuthType,
            PreAuthTypeinp,
            PreAuthAmount,
            PreAuthApprovalNo,
            PolicyNo,
            PolicyStartDate,
            PolicyEndDate,
          }));
        })
        .catch((e) => {
          console.log(e);
        });
    } else {
      setisClient((prev) => ({
        ...prev,
        isClient: "No",
        CoPaymentType: "Percentage",
        CoPaymentTypeinp: "",
        CoPaymentLogic: "PreAuth",
        CoPaymentdeducted: "PreAuth",
        PreAuthType: "Percentage",
        PreAuthTypeinp: "",
        PreAuthAmount: "",
        PreAuthApprovalNo: "",
        PolicyNo: "",
        PolicyStartDate: "",
        PolicyEndDate: "",
      }));
    }
  }, [UrlLink, patientsearch.Search, RegisterData.PatientCategory]);



  const handlesubmitclient = () => {
    let requiredfields1 = [
      "CoPaymentTypeinp",
      "PreAuthTypeinp",
      "PreAuthAmount",
      "PreAuthApprovalNo",
      "PolicyNo",
      "PolicyStartDate",
      "PolicyEndDate",
    ];

    const existing = requiredfields1.filter((field) => !isClient[field]);
    if (existing.length !== 0) {
      alert(`Please fill the required fields ${existing.join(",")}`);
    } else {
      const postdata = {
        isClient: isClient.isClient, // isClient status
        CoPaymentType: isClient.CoPaymentType, // Ensure CoPaymentType is passed
        CoPaymentTypeinp: isClient.CoPaymentTypeinp,
        CoPaymentLogic: isClient.CoPaymentLogic,
        CoPaymentdeducted: isClient.CoPaymentdeducted,
        PreAuthType: isClient.PreAuthType, // Ensure PreAuthType is passed
        PreAuthTypeinp: isClient.PreAuthTypeinp,
        PreAuthAmount: isClient.PreAuthAmount,
        PreAuthApprovalNo: isClient.PreAuthApprovalNo,
        PolicyNo: isClient.PolicyNo,
        PolicyStartDate: isClient.PolicyStartDate,
        PolicyEndDate: isClient.PolicyEndDate,
        PatientId: patientsearch.Search, // Assuming patientsearch contains PatientId
        Created_by: UserData?.username,
        Location: UserData?.location,
      };

      console.log("cliiiiieeeee", postdata);
      axios
        .post(`${UrlLink}Frontoffice/get_client_insurance_details`, postdata)
        .then((response) => {
          console.log("submitdata", response.data);
          setisClient({
            CoPaymentType: "Percentage",
            CoPaymentTypeinp: "",
            CoPaymentLogic: "PreAuth",
            CoPaymentdeducted: "PreAuth",
            PreAuthType: "Percentage",
            PreAuthTypeinp: "",
            PreAuthAmount: "",
            PreAuthApprovalNo: "",
            PolicyNo: "",
            PolicyStartDate: "",
            PolicyEndDate: "",
          });

          let typp = Object.keys(response.data)[0]; // Get response type (success, error)
          let mess = Object.values(response.data)[0]; // Get response message
          const tdata = {
            message: mess,
            type: typp,
          };
          dispatchvalue({ type: "toast", value: tdata });
        })
        .catch((e) => {
          console.log(e);
        });
    }
  };

  useEffect(() => {
    // Schedule the event for 12:00 AM
    const scheduleMidnightEvent = () => {
      const now = new Date();
      const midnight = new Date(
        now.getFullYear(),
        now.getMonth(),
        now.getDate() + 1, // Schedule for the next day
        0, 0, 0, 0 // 12:00 AM
      );
      const timeUntilMidnight = midnight - now;

      // Schedule the first execution
      setTimeout(() => {
        handleSubmit(); // Call the function at midnight
        setInterval(handleSubmit, 24 * 60 * 60 * 1000); // Repeat every 24 hours
      }, timeUntilMidnight);
    };

    scheduleMidnightEvent();
  }, []);

  const handleSubmit = (
    isSummary = false,
    isReimb = false,
    isNon_Reimb = false
  ) => {
    let requiredfields1 = [
      "PatientId",
      "PatientName",
      "PhoneNo",
      "AgeGender",
    ];
    let missingFields = requiredfields1.filter((field) => !RegisterData[field]);
    let errorMessages = [];

    // Check for missing required fields
    if (missingFields.length > 0) {
      errorMessages.push(
        `Please fill the required fields: ${missingFields.join(", ")}`
      );
    }

    // Check if Item Details are empty
    if (SelectDatalist.length === 0) {
      errorMessages.push("Please fill the Item Details.");
    }

    // Check if Payment Details are missing
    if (billAmount.length === 0) {
      errorMessages.push("Please fill the Payment Details.");
    }
    if (OP_BillingData.PatientId !== "") {
      // Check if Doctor Name is missing
      if (!BillingData.DoctorName) {
        errorMessages.push("Please fill the DoctorName Details.");
      }
    }
    else {
      console.log('Doctor Name is not needed');

    }


    // If there are any errors, show them all in one alert
    if (errorMessages.length > 0) {
      alert(errorMessages.join("\n"));
      return; // Exit the function to avoid proceeding further
    }

    let senddata = {
      billAmount: billAmount,
      SelectedPatient_list: SelectedPatient_list,
      NetAmount_CDmethod: NetAmount_CDmethod,
      SelectDatalist: SelectDatalist,
      BillingData: BillingData,
      initialState: initialState,
      Created_by: UserData?.username,
      Location: UserData?.location,
      selectedOption: selectedOption,
      ServiceProcedureForm: ServiceProcedureForm,
      Request_Id: OP_BillingData?.Request_Id,
      EditId: OP_BillingData?.id ? OP_BillingData?.Type === 'OPEdit' ? OP_BillingData?.id : "" : "",
    };

    console.log("senddata", senddata);
    if (Object.keys(OP_BillingData).length !== 0) {
      axios.post(`${UrlLink}Frontoffice/GeneralBilling_Link`, senddata)
        .then((res) => {
          console.log('OPpppppPosttt', res.data);
          setPostInvoice(res.data.InvoiceNo);
          setIsPrintButtonVisible(false);
        })
        .catch((err) => {
          console.log(err);
        })
    }
  };

  const handlePrint2 = useReactToPrint({
    content: () => componentRef.current,

    onAfterPrint: async () => {
      navigate("/Home/CashierFolder");
      dispatchvalue({ type: "HrFolder", value: "GeneralBillingList" });
      dispatchvalue({ type: "setPreviousFolder", value: null });
      dispatchvalue({ type: "showMenu", value: true });
    },
  });

  const ForPrintSumData = () => {
    return (
      <div ref={componentRef}>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            minHeight: "100vh",
          }}
          id="reactprintcontent"
        >
          <table
            className="print-table33"
          // style={{ flexGrow: 1,  }}
          >
            {/* Header Section */}
            <thead
              className="print_header"
              style={{
                width: "100%",
                borderCollapse: "collapse",
                height: "150px",
              }}
            >
              <tr>
                <td colSpan="7" style={{ border: "none" }}>
                  <div className="New_billlling_invoice_head">
                    <div className="new_billing_logo_con">
                      <img src={Chirayuulogo} alt="Medical logo" />
                    </div>
                    <div className="new_billing_address_1">
                      <span>{ClinicDetials.ClinicName}</span>
                      <div>
                        <span>
                          {[ClinicDetials.ClinicAddress]
                            .filter((detail) => detail)
                            .join(", ")}
                        </span>
                        <span>
                          {[
                            ClinicDetials.ClinicCity,
                            ClinicDetials.ClinicState,
                            ClinicDetials.ClinicCode,
                          ]
                            .filter((detail) => detail)
                            .join(", ")}
                        </span>
                      </div>
                      <div>
                        {[
                          ClinicDetials.ClinicMobileNo,
                          ClinicDetials.ClinicLandLineNo,
                          ClinicDetials.ClinicMailID,
                        ]
                          .filter((detail) => detail)
                          .join(" , ")}
                      </div>
                    </div>
                  </div>
                </td>
              </tr>
              <tr>
                <td
                  colSpan="7"
                  style={{
                    textAlign: "center",
                    fontWeight: "600",
                    color: "black",
                    fontSize: "20px",
                  }}
                >
                  Billing Invoice
                </td>
              </tr>
              <tr>
                <td colSpan="7">
                  <div className="new_billing_address">
                    <div className="new_billing_address_2">
                      <div className="new_billing_div phrmy_newbilg wdwdwswdw">
                        <label>
                          Patient Name <span>:</span>
                        </label>
                        <h4>{SelectedPatient_list.PatientName}</h4>
                      </div>

                      <div className="new_billing_div phrmy_newbilg wdwdwswdw">
                        <label>
                          Patient ID <span>:</span>
                        </label>
                        <h4>{SelectedPatient_list.PatientId}</h4>
                      </div>
                      <div className="new_billing_div phrmy_newbilg wdwdwswdw">
                        <label>
                          Age / Gender <span>:</span>
                        </label>
                        <h4>{OP_BillingData.AgeGender}</h4>
                      </div>

                      {/* <div className="new_billing_div phrmy_newbilg wdwdwswdw">
                        <label>
                          Consultant <span>:</span>
                        </label>
                        <h4>{SelectedPatient_list.PatientId}</h4>
                      </div> */}
                      <div className="new_billing_div phrmy_newbilg wdwdwswdw">
                        <label>
                          D.O.A <span>:</span>
                        </label>
                        <h4>{OP_BillingData.Date}</h4>
                      </div>

                      {/* {SelectedPatient_list.PatientType === "BtoB" ? (
                        <div className="new_billing_div phrmy_newbilg">
                          <label>
                            GST Number <span>:</span>
                          </label>
                          <h4>{SelectedPatient_list.GSTnumber}</h4>
                        </div>
                      ) : (
                        <div className="new_billing_div phrmy_newbilg">
                          <label>
                            Gender <span>:</span>
                          </label>
                          <h4>{SelectedPatient_list.Gender}</h4>
                        </div>
                      )} */}

                    </div>

                    <div className="new_billing_address_2">
                      <div className="new_billing_div phrmy_newbilg mvfg_p7u">
                        <label>
                          OP NO <span>:</span>
                        </label>
                        <h4>{OP_BillingData.Registration_Id}</h4>
                      </div>
                      <div className="new_billing_div phrmy_newbilg mvfg_p7u">
                        <label>
                          Bill No <span>:</span>
                        </label>
                        <h4>{PostInvoice}</h4>
                      </div>
                      {/* <div className="new_billing_div phrmy_newbilg mvfg_p7u">
                        <label>
                          GST No <span>:</span>
                        </label>
                        <h4>{ClinicDetials.ClinicGST}</h4>
                      </div> */}
                      <div className="new_billing_div phrmy_newbilg mvfg_p7u">
                        <label>
                          Physician Name <span>:</span>
                        </label>
                        <h4>{`Dr.${BillingData.DoctorName}`}</h4>
                      </div>
                      <div className="new_billing_div phrmy_newbilg mvfg_p7u">
                        <label>
                          Patient Mobile No <span>:</span>
                        </label>
                        <h4>{SelectedPatient_list.PhoneNumber}</h4>
                      </div>

                      {/* <div className="new_billing_div phrmy_newbilg">
                        <label>
                          Date <span>:</span>
                        </label>
                        <h4>{BillingData.InvoiceDate}</h4>
                      </div> */}

                    </div>
                  </div>
                </td>



              </tr>

            </thead>
            <tbody>
              <br />
              <tr>
                <td colSpan="7" className="prin_nnrmll_table">
                  <table style={{ width: "100%", border: "none" }}>
                    <thead>
                      <tr style={{ borderTop: "1.5px solid black", borderBottom: "1.5px solid black" }}>
                        <th style={{ borderTop: "1px solid black" }}>Service Type / Name</th>
                        <th style={{ border: "none" }}>Unit / Graft</th>
                        <th style={{ border: "none" }}>Amount</th>
                        <th style={{ border: "none" }}>Net Amount</th>
                      </tr>
                    </thead>
                    <tbody style={{ borderBottom: "1.5px solid black", padding: "2px" }}>
                      {SelectDatalist1.map((row, index) => (
                        <React.Fragment key={index}>
                          {/* Render the Service Type in a single row */}
                          {index === 0 || SelectDatalist[index - 1].ServiceType !== row.ServiceType ? (
                            <tr style={{ borderTop: "1px solid grey", marginBottom: "10px" }}>
                              <td style={{ fontWeight: "bold", textAlign: "left", border: "none" }}>
                                {row.ServiceType}
                              </td>
                              <td colSpan="3" style={{ border: "none" }}></td>
                            </tr>
                          ) : null}

                          {/* Render the Service Name and details in the next row */}
                          <tr >
                            <td style={{ paddingLeft: "20px", border: "none" }}>{row.SelectItemName}</td>
                            <td style={{ border: "none" }}>{row.Quantity}</td>
                            <td style={{ border: "none" }}>{row.Amount}</td>
                            <td style={{ border: "none" }}>{row.NetAmount}</td>
                          </tr>
                        </React.Fragment>
                      ))}
                    </tbody>
                  </table>
                </td>
              </tr>
            </tbody>
            <div>
              <div colSpan="7">
                <div className="new_billing_invoice_detials">
                  <div className="invoice_detials_total_1">
                    <div className="total_con_bill">
                      <div className="bill_body_new_phar">
                        <label>
                          Amount In Words <span>:</span>
                        </label>
                        <span>
                          {NumberToWords(+initialState.totalNetAmount)}
                        </span>
                      </div>
                      <div className="bill_body_new_phar">
                        <label>
                          Billed By <span>:</span>
                        </label>
                        <span>{UserData?.username}</span>
                      </div>
                    </div>



                    <div>
                      <div className="bill_body_new_phar">
                        <label>
                          Gross Amount <span>:</span>
                        </label>
                        <span>{initialState.totalAmount}</span>
                      </div>
                      <div className="bill_body_new_phar">
                        <label>
                          Discount Amount <span>:</span>
                        </label>
                        <span>{initialState.totalDiscount}</span>
                      </div>
                      {/* <div className="bill_body_new_phar">
                        <label>
                          CGST <span>:</span>
                        </label>
                        <span>{initialState.totalGstamount / 2}</span>
                      </div> */}
                      <div className="bill_body_new_phar">
                        <label>
                          Net Amount <span>:</span>
                        </label>
                        <span>{initialState.totalNetAmount}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <tfoot className="print_footerr">
              <tr className="jjxcdsjjej_"></tr>

              <tr className="ehdhe_9ikw">
                <td className="shshxhxs_secfooter">
                  <div
                    style={{
                      display: "flex",
                      flexDirection: "column",
                      justifyContent: "center",
                      alignItems: "center",
                    }}
                  >
                    <p className="disclaimer23">
                      This page is created automatically without a signature.
                    </p>
                  </div>
                </td>
              </tr>
            </tfoot>
          </table>
        </div>








        <div className="Register_btn_con added_Register_btn_con">
          <button
            className="RegisterForm_1_btns jwedu6_99"
            onClick={handlePrint2}
          >
            Print
          </button>
          <button
            className="RegisterForm_1_btns jwedu6_99"
            onClick={handlePrint2}
          >
            Close
          </button>
        </div>
      </div>
    );
  };

  const ForPrintData = () => {
    return (
      <div ref={componentRef}>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            minHeight: "100vh",
          }}
          id="reactprintcontent"
        >
          <table
            className="print-table33"
          // style={{ flexGrow: 1, }}
          >
            <thead
              className="print_header"
              style={{
                width: "100%",
                borderCollapse: "collapse",
                height: "150px",
              }}
            >
              <tr>
                <td colSpan="7" style={{ border: "none" }}>
                  <div className="New_billlling_invoice_head">
                    <div className="new_billing_logo_con">
                      <img src={Chirayuulogo} alt="Medical logo" />
                    </div>
                    <div className="new_billing_address_1">
                      <span>{ClinicDetials.ClinicName}</span>
                      <div>
                        <span>
                          {[ClinicDetials.ClinicAddress]
                            .filter((detail) => detail)
                            .join(", ")}
                        </span>
                        <span>
                          {[
                            ClinicDetials.ClinicCity,
                            ClinicDetials.ClinicState,
                            ClinicDetials.ClinicCode,
                          ]
                            .filter((detail) => detail)
                            .join(", ")}
                        </span>
                      </div>
                      <div>
                        {[
                          ClinicDetials.ClinicMobileNo,
                          ClinicDetials.ClinicLandLineNo,
                          ClinicDetials.ClinicMailID,
                        ]
                          .filter((detail) => detail)
                          .join(" , ")}
                      </div>
                    </div>
                  </div>
                </td>
              </tr>
              <tr>
                <td
                  colSpan="7"
                  style={{
                    textAlign: "center",
                    fontWeight: "600",
                    color: "black",
                    fontSize: "20px",
                  }}
                >
                  Billing Invoice
                </td>
              </tr>
              <tr>
                <td colSpan="7">
                  <div className="new_billing_address">
                    <div className="new_billing_address_2">
                      <div className="new_billing_div phrmy_newbilg wdwdwswdw">
                        <label>
                          Patient Name <span>:</span>
                        </label>
                        <h4>{SelectedPatient_list.PatientName}</h4>
                      </div>

                      <div className="new_billing_div phrmy_newbilg wdwdwswdw">
                        <label>
                          Patient ID <span>:</span>
                        </label>
                        <h4>{SelectedPatient_list.PatientId}</h4>
                      </div>
                      <div className="new_billing_div phrmy_newbilg wdwdwswdw">
                        <label>
                          Age / Gender <span>:</span>
                        </label>
                        <h4>{OP_BillingData.AgeGender}</h4>
                      </div>

                      {/* <div className="new_billing_div phrmy_newbilg wdwdwswdw">
                        <label>
                          Consultant <span>:</span>
                        </label>
                        <h4>{SelectedPatient_list.PatientId}</h4>
                      </div> */}
                      <div className="new_billing_div phrmy_newbilg wdwdwswdw">
                        <label>
                          D.O.A <span>:</span>
                        </label>
                        <h4>{OP_BillingData.Date}</h4>
                      </div>

                      {/* {SelectedPatient_list.PatientType === "BtoB" ? (
                        <div className="new_billing_div phrmy_newbilg">
                          <label>
                            GST Number <span>:</span>
                          </label>
                          <h4>{SelectedPatient_list.GSTnumber}</h4>
                        </div>
                      ) : (
                        <div className="new_billing_div phrmy_newbilg">
                          <label>
                            Gender <span>:</span>
                          </label>
                          <h4>{SelectedPatient_list.Gender}</h4>
                        </div>
                      )} */}

                    </div>

                    <div className="new_billing_address_2">
                      <div className="new_billing_div phrmy_newbilg mvfg_p7u">
                        <label>
                          OP NO <span>:</span>
                        </label>
                        <h4>{SelectedPatient_list.RegisterId}</h4>
                      </div>
                      <div className="new_billing_div phrmy_newbilg mvfg_p7u">
                        <label>
                          Bill No <span>:</span>
                        </label>
                        <h4>{PostInvoice}</h4>
                      </div>
                      {/* <div className="new_billing_div phrmy_newbilg mvfg_p7u">
                        <label>
                          GST No <span>:</span>
                        </label>
                        <h4>{ClinicDetials.ClinicGST}</h4>
                      </div> */}
                      <div className="new_billing_div phrmy_newbilg mvfg_p7u">
                        <label>
                          Physician Name <span>:</span>
                        </label>
                        <h4>{`Dr.${BillingData.DoctorName}`}</h4>
                      </div>
                      <div className="new_billing_div phrmy_newbilg mvfg_p7u">
                        <label>
                          Patient Mobile No <span>:</span>
                        </label>
                        <h4>{SelectedPatient_list.PhoneNumber}</h4>
                      </div>

                      {/* <div className="new_billing_div phrmy_newbilg">
                        <label>
                          Date <span>:</span>
                        </label>
                        <h4>{BillingData.InvoiceDate}</h4>
                      </div> */}

                    </div>
                  </div>
                </td>



              </tr>

            </thead>

            <tbody>
              <br />
              <tr>
                <td colSpan="7" className="prin_nnrmll_table">
                  <table style={{ width: "100%", border: "none" }}>
                    <thead>
                      <tr style={{ borderTop: "1.5px solid black", borderBottom: "1.5px solid black" }}>
                        <th style={{ borderTop: "1px solid black" }}>Service Type / Name</th>
                        <th style={{ border: "none" }}>Unit / Graft</th>
                        <th style={{ border: "none" }}>Amount</th>
                        <th style={{ border: "none" }}>Net Amount</th>
                      </tr>
                    </thead>
                    <tbody style={{ borderBottom: "1.5px solid black", padding: "2px" }}>
                      {SelectDatalist.map((row, index) => (
                        <React.Fragment key={index}>
                          {/* Render the Service Type in a single row */}
                          {index === 0 || SelectDatalist[index - 1].ServiceType !== row.ServiceType ? (
                            <tr style={{ borderTop: "1px solid grey", marginBottom: "10px" }}>
                              <td style={{ fontWeight: "bold", textAlign: "left", border: "none" }}>
                                {row.ServiceType}
                              </td>
                              <td colSpan="3" style={{ border: "none" }}></td>
                            </tr>
                          ) : null}

                          {/* Render the Service Name and details in the next row */}
                          <tr >
                            <td style={{ paddingLeft: "20px", border: "none" }}>{row.SelectItemName}</td>
                            <td style={{ border: "none" }}>{row.Quantity}</td>
                            <td style={{ border: "none" }}>{row.Amount}</td>
                            <td style={{ border: "none" }}>{row.NetAmount}</td>
                          </tr>
                        </React.Fragment>
                      ))}
                    </tbody>
                  </table>
                </td>
              </tr>
            </tbody>
            <tr>
              <td colSpan="7">
                <div className="new_billing_invoice_detials">
                  <div className="invoice_detials_total_1">
                    <div className="total_con_bill">
                      <div className="bill_body_new_phar">
                        <label>
                          Amount In Words <span>:</span>
                        </label>
                        <span>
                          {NumberToWords(+initialState.totalNetAmount)}
                        </span>
                      </div>
                      <div className="bill_body_new_phar">
                        <label>
                          Billed By <span>:</span>
                        </label>
                        <span>{UserData?.username}</span>
                      </div>
                    </div>



                    <div>
                      <div className="bill_body_new_phar">
                        <label>
                          Gross Amount <span>:</span>
                        </label>
                        <span>{initialState.totalAmount}</span>
                      </div>
                      <div className="bill_body_new_phar">
                        <label>
                          Discount Amount <span>:</span>
                        </label>
                        <span>{initialState.totalDiscount}</span>
                      </div>
                      {/* <div className="bill_body_new_phar">
                        <label>
                          CGST <span>:</span>
                        </label>
                        <span>{initialState.totalGstamount / 2}</span>
                      </div> */}
                      <div className="bill_body_new_phar">
                        <label>
                          Net Amount <span>:</span>
                        </label>
                        <span>{initialState.totalNetAmount}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </td>
            </tr>


            <tfoot className="print_footerr">
              <tr className="jjxcdsjjej_"></tr>

              <tr className="ehdhe_9ikw">
                <td className="shshxhxs_secfooter">
                  <div
                    style={{
                      display: "flex",
                      flexDirection: "column",
                      justifyContent: "center",
                      alignItems: "center",
                    }}
                  >
                    <p className="disclaimer23">
                      This page is created automatically without a signature.
                    </p>
                  </div>
                </td>
              </tr>
            </tfoot>
          </table>
        </div>



        <div className="Register_btn_con added_Register_btn_con">
          <button
            className="RegisterForm_1_btns jwedu6_99"
            onClick={handlePrint2}
          >
            Print
          </button>
        </div>
      </div>
    );
  };

  const ForPrintReimbData = () => {
    return (
      <div ref={componentRef}>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            minHeight: "100vh",
          }}
          id="reactprintcontent"
        >
          <table
            className="print-table33"
          // style={{ flexGrow: 1, }}
          >
            <thead
              className="print_header"
              style={{
                width: "100%",
                borderCollapse: "collapse",
                height: "150px",
              }}
            >
              <tr>
                <td colSpan="7" style={{ border: "none" }}>
                  <div className="New_billlling_invoice_head">
                    <div className="new_billing_logo_con">
                      <img src={Chirayuulogo} alt="Medical logo" />
                    </div>
                    <div className="new_billing_address_1">
                      <span>{ClinicDetials.ClinicName}</span>
                      <div>
                        <span>
                          {[ClinicDetials.ClinicAddress]
                            .filter((detail) => detail)
                            .join(", ")}
                        </span>
                        <span>
                          {[
                            ClinicDetials.ClinicCity,
                            ClinicDetials.ClinicState,
                            ClinicDetials.ClinicCode,
                          ]
                            .filter((detail) => detail)
                            .join(", ")}
                        </span>
                      </div>
                      <div>
                        {[
                          ClinicDetials.ClinicMobileNo,
                          ClinicDetials.ClinicLandLineNo,
                          ClinicDetials.ClinicMailID,
                        ]
                          .filter((detail) => detail)
                          .join(" , ")}
                      </div>
                    </div>
                  </div>
                </td>
              </tr>
              <tr>
                <td
                  colSpan="7"
                  style={{
                    textAlign: "center",
                    fontWeight: "600",
                    color: "black",
                    fontSize: "20px",
                  }}
                >
                  Billing Invoice
                </td>
              </tr>
              <tr>
                <td colSpan="7">
                  <div className="new_billing_address">
                    <div className="new_billing_address_2">
                      <div className="new_billing_div phrmy_newbilg wdwdwswdw">
                        <label>
                          Patient Name <span>:</span>
                        </label>
                        <h4>{SelectedPatient_list.PatientName}</h4>
                      </div>

                      <div className="new_billing_div phrmy_newbilg wdwdwswdw">
                        <label>
                          Patient ID <span>:</span>
                        </label>
                        <h4>{SelectedPatient_list.PatientId}</h4>
                      </div>
                      <div className="new_billing_div phrmy_newbilg wdwdwswdw">
                        <label>
                          Age / Gender <span>:</span>
                        </label>
                        <h4>{OP_BillingData.AgeGender}</h4>
                      </div>

                      {/* <div className="new_billing_div phrmy_newbilg wdwdwswdw">
                        <label>
                          Consultant <span>:</span>
                        </label>
                        <h4>{SelectedPatient_list.PatientId}</h4>
                      </div> */}
                      <div className="new_billing_div phrmy_newbilg wdwdwswdw">
                        <label>
                          D.O.A <span>:</span>
                        </label>
                        <h4>{OP_BillingData.Date}</h4>
                      </div>

                      {/* {SelectedPatient_list.PatientType === "BtoB" ? (
                        <div className="new_billing_div phrmy_newbilg">
                          <label>
                            GST Number <span>:</span>
                          </label>
                          <h4>{SelectedPatient_list.GSTnumber}</h4>
                        </div>
                      ) : (
                        <div className="new_billing_div phrmy_newbilg">
                          <label>
                            Gender <span>:</span>
                          </label>
                          <h4>{SelectedPatient_list.Gender}</h4>
                        </div>
                      )} */}

                    </div>

                    <div className="new_billing_address_2">
                      <div className="new_billing_div phrmy_newbilg mvfg_p7u">
                        <label>
                          OP NO <span>:</span>
                        </label>
                        <h4>{OP_BillingData.Registration_Id}</h4>
                      </div>
                      <div className="new_billing_div phrmy_newbilg mvfg_p7u">
                        <label>
                          Bill No <span>:</span>
                        </label>
                        <h4>{PostInvoice}</h4>
                      </div>
                      {/* <div className="new_billing_div phrmy_newbilg mvfg_p7u">
                        <label>
                          GST No <span>:</span>
                        </label>
                        <h4>{ClinicDetials.ClinicGST}</h4>
                      </div> */}
                      <div className="new_billing_div phrmy_newbilg mvfg_p7u">
                        <label>
                          Physician Name <span>:</span>
                        </label>
                        <h4>{`Dr.${BillingData.DoctorName}`}</h4>
                      </div>
                      <div className="new_billing_div phrmy_newbilg mvfg_p7u">
                        <label>
                          Patient Mobile No <span>:</span>
                        </label>
                        <h4>{SelectedPatient_list.PhoneNumber}</h4>
                      </div>

                      {/* <div className="new_billing_div phrmy_newbilg">
                        <label>
                          Date <span>:</span>
                        </label>
                        <h4>{BillingData.InvoiceDate}</h4>
                      </div> */}

                    </div>
                  </div>
                </td>


              </tr>

            </thead>

            <tbody>

              <br />

              <tr>

                <td colSpan="7" className="prin_nnrmll_table">

                  <table style={{ width: "100%", border: "none" }}>

                    <thead>

                      <tr style={{ borderTop: "1.5px solid black", borderBottom: "1.5px solid black" }}>

                        <th style={{ borderTop: "1px solid black" }}>Service Type / Name</th>

                        <th style={{ border: "none" }}>Unit / Graft</th>

                        <th style={{ border: "none" }}>Amount</th>

                        <th style={{ border: "none" }}>Net Amount</th>

                      </tr>

                    </thead>



                    <tbody style={{ borderBottom: "1.5px solid black", padding: "2px" }}>

                      {SelectDatalist.filter((f) => f.isReimbursable === "Yes").map((row, index) => (

                        <React.Fragment key={index}>

                          {/* Render the Service Type in a single row */}

                          {index === 0 || SelectDatalist[index - 1].ServiceType !== row.ServiceType ? (

                            <tr style={{ borderTop: "1px solid grey", marginBottom: "10px" }}>

                              <td style={{ fontWeight: "bold", textAlign: "left", border: "none" }}>

                                {row.ServiceType}

                              </td>

                              <td colSpan="3" style={{ border: "none" }}></td>

                            </tr>

                          ) : null}



                          {/* Render the Service Name and details in the next row */}

                          <tr >

                            <td style={{ paddingLeft: "20px", border: "none" }}>{row.SelectItemName}</td>

                            <td style={{ border: "none" }}>{row.Quantity}</td>

                            <td style={{ border: "none" }}>{row.Amount}</td>

                            <td style={{ border: "none" }}>{row.NetAmount}</td>

                          </tr>

                        </React.Fragment>

                      ))}

                    </tbody>

                  </table>

                </td>

              </tr>

            </tbody>
            <tr>
              <td colSpan="7">
                <div className="new_billing_invoice_detials">
                  <div className="invoice_detials_total_1">
                    <div className="total_con_bill">
                      <div className="bill_body_new_phar">
                        <label>
                          Amount In Words <span>:</span>
                        </label>
                        <span>
                          {NumberToWords(+initialState.totalNetAmount)}
                        </span>
                      </div>
                      <div className="bill_body_new_phar">
                        <label>
                          Billed By <span>:</span>
                        </label>
                        <span>{UserData?.username}</span>
                      </div>
                    </div>



                    <div>
                      <div className="bill_body_new_phar">
                        <label>
                          Gross Amount <span>:</span>
                        </label>
                        <span>{initialState.totalAmount}</span>
                      </div>
                      <div className="bill_body_new_phar">
                        <label>
                          Discount Amount <span>:</span>
                        </label>
                        <span>{initialState.totalDiscount}</span>
                      </div>
                      {/* <div className="bill_body_new_phar">
                        <label>
                          CGST <span>:</span>
                        </label>
                        <span>{initialState.totalGstamount / 2}</span>
                      </div> */}
                      <div className="bill_body_new_phar">
                        <label>
                          Net Amount <span>:</span>
                        </label>
                        <span>{initialState.totalNetAmount}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </td>
            </tr>

            <tfoot className="print_footerr">
              <tr className="jjxcdsjjej_"></tr>

              <tr className="ehdhe_9ikw">
                <td className="shshxhxs_secfooter">
                  <div
                    style={{
                      display: "flex",
                      flexDirection: "column",
                      justifyContent: "center",
                      alignItems: "center",
                    }}
                  >
                    <p className="disclaimer23">
                      This page is created automatically without a signature.
                    </p>
                  </div>
                </td>
              </tr>
            </tfoot>
          </table>
        </div>



        <div className="Register_btn_con added_Register_btn_con">
          <button
            className="RegisterForm_1_btns jwedu6_99"
            onClick={handlePrint2}
          >
            Print
          </button>
        </div>
      </div>
    );
  };

  const ForPrintNon_ReimbData = () => {
    return (
      <div ref={componentRef}>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            minHeight: "100vh",
          }}
          id="reactprintcontent"
        >
          <table
            className="print-table33"
          // style={{ flexGrow: 1, }}
          >
            <thead
              className="print_header"
              style={{
                width: "100%",
                borderCollapse: "collapse",
                height: "150px",
              }}
            >
              <tr>
                <td colSpan="7" style={{ border: "none" }}>
                  <div className="New_billlling_invoice_head">
                    <div className="new_billing_logo_con">
                      <img src={Chirayuulogo} alt="Medical logo" />
                    </div>
                    <div className="new_billing_address_1">
                      <span>{ClinicDetials.ClinicName}</span>
                      <div>
                        <span>
                          {[ClinicDetials.ClinicAddress]
                            .filter((detail) => detail)
                            .join(", ")}
                        </span>
                        <span>
                          {[
                            ClinicDetials.ClinicCity,
                            ClinicDetials.ClinicState,
                            ClinicDetials.ClinicCode,
                          ]
                            .filter((detail) => detail)
                            .join(", ")}
                        </span>
                      </div>
                      <div>
                        {[
                          ClinicDetials.ClinicMobileNo,
                          ClinicDetials.ClinicLandLineNo,
                          ClinicDetials.ClinicMailID,
                        ]
                          .filter((detail) => detail)
                          .join(" , ")}
                      </div>
                    </div>
                  </div>
                </td>
              </tr>
              <tr>
                <td
                  colSpan="7"
                  style={{
                    textAlign: "center",
                    fontWeight: "600",
                    color: "black",
                    fontSize: "20px",
                  }}
                >
                  Billing Invoice
                </td>
              </tr>
              <tr>
                <td colSpan="7">
                  <div className="new_billing_address">
                    <div className="new_billing_address_2">
                      <div className="new_billing_div phrmy_newbilg wdwdwswdw">
                        <label>
                          Patient Name <span>:</span>
                        </label>
                        <h4>{SelectedPatient_list.PatientName}</h4>
                      </div>

                      <div className="new_billing_div phrmy_newbilg wdwdwswdw">
                        <label>
                          Patient ID <span>:</span>
                        </label>
                        <h4>{SelectedPatient_list.PatientId}</h4>
                      </div>
                      <div className="new_billing_div phrmy_newbilg wdwdwswdw">
                        <label>
                          Age / Gender <span>:</span>
                        </label>
                        <h4>{OP_BillingData.AgeGender}</h4>
                      </div>

                      {/* <div className="new_billing_div phrmy_newbilg wdwdwswdw">
                        <label>
                          Consultant <span>:</span>
                        </label>
                        <h4>{SelectedPatient_list.PatientId}</h4>
                      </div> */}
                      <div className="new_billing_div phrmy_newbilg wdwdwswdw">
                        <label>
                          D.O.A <span>:</span>
                        </label>
                        <h4>{OP_BillingData.Date}</h4>
                      </div>

                      {/* {SelectedPatient_list.PatientType === "BtoB" ? (
                        <div className="new_billing_div phrmy_newbilg">
                          <label>
                            GST Number <span>:</span>
                          </label>
                          <h4>{SelectedPatient_list.GSTnumber}</h4>
                        </div>
                      ) : (
                        <div className="new_billing_div phrmy_newbilg">
                          <label>
                            Gender <span>:</span>
                          </label>
                          <h4>{SelectedPatient_list.Gender}</h4>
                        </div>
                      )} */}

                    </div>

                    <div className="new_billing_address_2">
                      <div className="new_billing_div phrmy_newbilg mvfg_p7u">
                        <label>
                          OP NO <span>:</span>
                        </label>
                        <h4>{OP_BillingData.Registration_Id}</h4>
                      </div>
                      <div className="new_billing_div phrmy_newbilg mvfg_p7u">
                        <label>
                          Bill No <span>:</span>
                        </label>
                        <h4>{PostInvoice}</h4>
                      </div>
                      <div className="new_billing_div phrmy_newbilg mvfg_p7u">
                        <label>
                          GST No <span>:</span>
                        </label>
                        <h4>{ClinicDetials.ClinicGST}</h4>
                      </div>
                      <div className="new_billing_div phrmy_newbilg mvfg_p7u">
                        <label>
                          Physician Name <span>:</span>
                        </label>
                        <h4>{`Dr.${BillingData.DoctorName}`}</h4>
                      </div>
                      <div className="new_billing_div phrmy_newbilg mvfg_p7u">
                        <label>
                          Patient Mobile No <span>:</span>
                        </label>
                        <h4>{SelectedPatient_list.PhoneNumber}</h4>
                      </div>

                      {/* <div className="new_billing_div phrmy_newbilg">
                        <label>
                          Date <span>:</span>
                        </label>
                        <h4>{BillingData.InvoiceDate}</h4>
                      </div> */}

                    </div>
                  </div>
                </td>



              </tr>

            </thead>

            <tbody>

              <br />

              <tr>

                <td colSpan="7" className="prin_nnrmll_table">

                  <table style={{ width: "100%", border: "none" }}>

                    <thead>

                      <tr style={{ borderTop: "1.5px solid black", borderBottom: "1.5px solid black" }}>

                        <th style={{ borderTop: "1px solid black" }}>Service Type / Name</th>

                        <th style={{ border: "none" }}>Unit / Graft</th>

                        <th style={{ border: "none" }}>Amount</th>

                        <th style={{ border: "none" }}>Net Amount</th>

                      </tr>

                    </thead>



                    <tbody style={{ borderBottom: "1.5px solid black", padding: "2px" }}>

                      {SelectDatalist.filter((f) => f.isReimbursable === "No").map((row, index) => (

                        <React.Fragment key={index}>

                          {/* Render the Service Type in a single row */}

                          {index === 0 || SelectDatalist[index - 1].ServiceType !== row.ServiceType ? (

                            <tr style={{ borderTop: "1px solid grey", marginBottom: "10px" }}>

                              <td style={{ fontWeight: "bold", textAlign: "left", border: "none" }}>

                                {row.ServiceType}

                              </td>

                              <td colSpan="3" style={{ border: "none" }}></td>

                            </tr>

                          ) : null}



                          {/* Render the Service Name and details in the next row */}

                          <tr >

                            <td style={{ paddingLeft: "20px", border: "none" }}>{row.SelectItemName}</td>

                            <td style={{ border: "none" }}>{row.Quantity}</td>

                            <td style={{ border: "none" }}>{row.Amount}</td>

                            <td style={{ border: "none" }}>{row.NetAmount}</td>

                          </tr>

                        </React.Fragment>

                      ))}

                    </tbody>

                  </table>

                </td>

              </tr>

            </tbody>

            <tr>
              <td colSpan="7">
                <div className="new_billing_invoice_detials">
                  <div className="invoice_detials_total_1">
                    <div className="total_con_bill">
                      <div className="bill_body_new_phar">
                        <label>
                          Amount In Words <span>:</span>
                        </label>
                        <span>
                          {NumberToWords(+initialState.totalNetAmount)}
                        </span>
                      </div>
                      <div className="bill_body_new_phar">
                        <label>
                          Billed By <span>:</span>
                        </label>
                        <span>{UserData?.username}</span>
                      </div>
                    </div>



                    <div>
                      <div className="bill_body_new_phar">
                        <label>
                          Gross Amount <span>:</span>
                        </label>
                        <span>{initialState.totalAmount}</span>
                      </div>
                      <div className="bill_body_new_phar">
                        <label>
                          Discount Amount <span>:</span>
                        </label>
                        <span>{initialState.totalDiscount}</span>
                      </div>
                      {/* <div className="bill_body_new_phar">
                        <label>
                          CGST <span>:</span>
                        </label>
                        <span>{initialState.totalGstamount / 2}</span>
                      </div> */}
                      <div className="bill_body_new_phar">
                        <label>
                          Net Amount <span>:</span>
                        </label>
                        <span>{initialState.totalNetAmount}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </td>
            </tr>

            <tfoot className="print_footerr">
              <tr className="jjxcdsjjej_"></tr>

              <tr className="ehdhe_9ikw">
                <td className="shshxhxs_secfooter">
                  <div
                    style={{
                      display: "flex",
                      flexDirection: "column",
                      justifyContent: "center",
                      alignItems: "center",
                    }}
                  >
                    <p className="disclaimer23">
                      This page is created automatically without a signature.
                    </p>
                  </div>
                </td>
              </tr>
            </tfoot>
          </table>
        </div>


        <div className="Register_btn_con added_Register_btn_con">
          <button
            className="RegisterForm_1_btns jwedu6_99"
            onClick={handlePrint2}
          >
            Print
          </button>
        </div>
      </div>
    );
  };

  return (
    <>
      {isPrintButtonVisible ? (
        <>
          <div className="Main_container_app">
            <h3>Billing</h3>

            <div className="csdcedw_kl88">
              <div className="RegisBillSearchForm_1 RegisBillSearchForm_1_mmmm">
                <label>
                  Search <span>:</span>
                </label>
                <div className="Search_patient_icons">
                  <input
                    type="text"
                    onKeyDown={
                      patientsearch === "FirstName"
                        ? (e) => HandlesearchPatient(patientsearch.Search)
                        : null
                    }
                    list="Search_iddd"
                    autoComplete="off"
                    name="Search"
                    pattern={
                      patientsearch === "PhoneNumber" ? "\\d{10}" : "[A-Za-z]+"
                    }
                    className={
                      errors["Search"] === "Invalid"
                        ? "invalid"
                        : errors["Search"] === "Valid"
                          ? "valid"
                          : ""
                    }
                    value={patientsearch.Search}
                    onChange={HandleSearchchange}
                    disabled={
                      Object.values(OP_BillingData).length !== 0
                    }
                  />
                  <datalist id="Search_iddd">
                    {FilterbyPatientId.map((row, indx) => (
                      <option key={indx} value={row.PatientId}>
                        {`${row.PhoneNo} | ${row.FirstName} | ${row.UniqueIdNo}`}
                      </option>
                    ))}
                  </datalist>
                </div>
              </div>

              <div className="ewdwdwd_u7j" ref={gridRef}>
                <div className="RegisBillSmart_2">
                  <label>
                    Smart Card No <span>:</span>
                  </label>
                  <input
                    type="text"
                    value={SmartCard.SmartCardNo}
                    id="SmartCardNo"
                    readOnly
                  // onChange={handleSmartCard}
                  />
                  <button
                    style={{
                      backgroundColor: "#646653",
                      width: "50px",
                      height: "20px",
                      color: "white",
                      cursor: "pointerEvents",
                    }}
                    onClick={HandleSmartCard}
                  >
                    Go
                  </button>
                </div>

                <div className="RegisBillSmart_2">
                  <label>
                    <input
                      type="checkbox"
                      checked={register.isregister === "Yes"}
                      onChange={(e) => handleRegisterChange(e)}
                    />
                    Registration Amount
                  </label>
                </div>

                {register.isregister === "Yes" ? (
                  <div className="RegisBillForm_1">
                    <input
                      type="text"
                      name="registerAmount"
                      value={register.registerAmount}
                      onChange={(e) => handleRegisterChange(e, true)} // Pass an additional argument to indicate input field change
                    />
                  </div>
                ) : null}
              </div>
            </div>


            <br />

            <div className="RegisBillFormcon" ref={gridRef}>
              {RegisterData &&
                Object.keys(RegisterData).filter((p) => {
                  // If the PatientCategory is 'General', exclude 'PatientCategoryName'
                  if (OP_BillingData.PatientCategory === 'General' && p === 'PatientCategoryName') {
                    return false;
                  }
                  return true;
                }).map((field, index) => (
                  <div
                    className="RegisBillForm_1 RegisBillForm_1_M "
                    key={index}
                  >
                    <label htmlFor={`${field}_${index}`}>
                      {field === "AgeGender"
                        ? "Age/Gender"
                        : formatLabel(field)}
                      <span>:</span>
                    </label>
                    {[
                      "PatientId",
                      "ABHA",
                      "PatientName",
                      "AgeGender",
                      "PhoneNo",
                      "PatientCategory",
                      "PatientCategoryName",
                    ].includes(field) ? (
                      <input
                        id={`${field}_${index}`}
                        autoComplete="off"
                        type={field === "DOB" ? "date" : "text"}
                        name={field}
                        pattern={
                          field === "Email"
                            ? "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[cC][oO][mM]$"
                            : field === "PhoneNo"
                              ? "\\d{10}"
                              : ["CaseSheetNo", "UniqueIdNo"].includes(field)
                                ? "[A-Za-z0-9]+"
                                : field === "Age"
                                  ? "\\d{1,3}"
                                  : field === "DOB"
                                    ? ""
                                    : field === "Pincode"
                                      ? "\\d{6}"
                                      : "[A-Za-z]+"
                        }
                        className={
                          errors[field] === "Invalid"
                            ? "invalid"
                            : errors[field] === "Valid"
                              ? "valid"
                              : ""
                        }
                        required
                        value={RegisterData[field]}
                        onKeyDown={
                          [
                            "MiddleName",
                            "SurName",
                            "Occupation",
                            "NextToKinName",
                            "FamilyHeadName",
                            "Street",
                            "Area",
                            "City",
                            "State",
                            "Complaint",
                            "Country",
                          ].includes(field)
                            ? handleKeyDownTextRegistration
                            : field === "PhoneNo"
                              ? handleKeyDownPhoneNo
                              : null
                        }
                        onChange={HandleOnchange}
                      />
                    ) : (field === 'Address' && (
                      <textarea
                        name="Address"
                        value={RegisterData[field]}
                      />
                    ))}
                  </div>
                ))}
              {/* <div className="Register_btn_con added_Register_btn_con">
                <button
                  className="RegisterForm_1_btns added_RegisterForm_1_btns"
                  onClick={handlesubmitpatient}
                >
                  Submit
                </button>
              </div> */}
            </div>
            {/* <div className="Main_container_Btn">
          <button onClick={handlesubmit}>Save</button>
        </div> */}
            <div className="RegisBillFormcon">
              <div className="sjhdcys6">
                <label>
                  <input
                    type="checkbox"
                    checked={isClient.isClient === "Yes"}
                    onChange={HandleClientCheck}
                  />
                  Client/Insurance/TPA
                </label>
              </div>
            </div>
            {isClient.isClient === "Yes" ? (
              <>
                <div className="RegisBillFormcon">
                  {Object.keys(isClient)
                    .filter(
                      (f) =>
                        f !== "isClient" &&
                        f !== "CoPaymentTypeinp" &&
                        f !== "PreAuthTypeinp"
                    )
                    .map((field, ind) => (
                      <div className="RegisBillForm_1" key={ind}>
                        <label htmlFor={`${ind}_${field}`}>
                          {field === "CoPaymentdeducted"
                            ? "Co-Payment deducted"
                            : formatLabel(field)}
                          <span>:</span>
                        </label>
                        {[
                          "CoPaymentType",
                          "CoPaymentLogic",
                          "CoPaymentdeducted",
                          "PreAuthType",
                        ].includes(field) ? (
                          <div className="input-select-container">
                            <select
                              id={`${ind}_${field}`}
                              name={field}
                              value={isClient[field]}
                              onChange={HandleOnClient}
                            >
                              {["CoPaymentType", "PreAuthType"].includes(
                                field
                              ) &&
                                ["Percentage", "Value"].map((p, index) => (
                                  <option key={index} value={p}>
                                    {p}
                                  </option>
                                ))}
                              {field === "CoPaymentLogic" &&
                                ["PreAuth", "Final"].map((row, index) => (
                                  <option key={index} value={row}>
                                    {row}
                                  </option>
                                ))}
                              {field === "CoPaymentdeducted" &&
                                ["PreAuth", "Final"].map((row, index) => (
                                  <option key={index} value={row}>
                                    {row}
                                  </option>
                                ))}
                            </select>
                            {/* Input field next to select for CoPaymentType and PreAuthType */}
                            {field === "CoPaymentType" && (
                              <input
                                type="text"
                                name="CoPaymentTypeinp" // Unique name for input fields
                                value={isClient.CoPaymentTypeinp || ""} // Accessing the state for input field
                                onChange={HandleOnClient}
                                placeholder="Enter value"
                              />
                            )}
                            {field === "PreAuthType" && (
                              <input
                                type="text"
                                name="PreAuthTypeinp" // Unique name for input fields
                                value={isClient.PreAuthTypeinp || ""} // Accessing the state for input field
                                onChange={HandleOnClient}
                                placeholder="Enter value"
                              />
                            )}
                          </div>
                        ) : [
                          "PreAuthAmount",
                          "PreAuthApprovalNo",
                          "PolicyNo",
                        ].includes(field) ? (
                          <input
                            type="text"
                            name={field}
                            value={isClient[field]}
                            onChange={HandleOnClient}
                            placeholder={
                              field === "PreAuthAmount" ? "0.00" : ""
                            }
                          />
                        ) : (
                          <input
                            type="date"
                            name={field}
                            value={isClient[field]}
                            onChange={HandleOnClient}
                          />
                        )}
                      </div>
                    ))}
                </div>

                <div className="Bill_Btn">
                  <button onClick={handlesubmitclient}>Submit</button>
                </div>
              </>
            ) : null}



            <h3>Services</h3>

            <div className="RegisBillFormcon">
              <div className="Service_bill">
                {
                  Object.keys(ServiceProcedure).filter((p) => p !== 'ServiceSubCatId' && p !== 'Subcategorypk' && p !== 'Categoryid').map((field, indx) => (
                    <div className="RegisForm_1" key={indx}>
                      <label htmlFor={`${field}_${indx}`}>
                        {formatLabel(field)}
                        <span>:</span>
                      </label>
                      {
                        ['ServiceCategory', 'ServiceSubCategory', 'Rate', 'Quantity'].includes(field) && (
                          <input
                            type='text'
                            name={field} // Add the name attribute here
                            value={ServiceProcedure[field]}
                            list={`${field}_ServiceCategory`}
                            onChange={HandleOnchangeService}
                          // onKeyDown={(e) => ['e', 'E', '+', '-'].includes(e.key) && e.preventDefault()}
                          />

                        )
                      }
                      {
                        <datalist id={`${field}_ServiceCategory`}>
                          {field === 'ServiceCategory' && (
                            ServiceCategoryData?.map((row, indx) =>
                              <option key={indx} value={`${row.service_category_id}-${row.service_name}`}>
                                {row.service_name}
                              </option>
                            )
                          )}
                          {field === 'ServiceSubCategory' && (
                            Array.isArray(ServiceSubCategoryData) &&
                            ServiceSubCategoryData.map((row, indx) =>
                              <option key={indx} value={`${row.pk}-${row.service_subcategory}`}>
                                {row.service_subcategory}
                              </option>
                            )
                          )}
                        </datalist>
                      }

                    </div>

                  ))
                }

              </div>
              <div className="Register_btn_con added_Register_btn_con">

                <button
                  className="RegisterForm_1_btns added_RegisterForm_1_btns"
                  onClick={Additemstobillfun}
                >
                  Add
                </button>
              </div>
            </div>


            <div className="new-patient-registration-form">
              <div className="Selected-table-container444 DEWSDXWED">
                <table className="selected-medicine-table222 EDWEDE">
                  <thead>
                    <tr>
                      <th>S.No</th>
                      <th>Service Type</th>
                      <th>Service Name</th>
                      <th>Charge</th>
                      <th>Quantity</th>
                      <th>Amount </th>
                      <th>Discount Type</th>
                      <th>Discount</th>
                      <th>Net Amount</th>
                      <th>Status</th>
                      {/* <th>isReimbursable</th> */}
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {SelectDatalist.map((row, index) => {
                      return (
                        <tr key={index}>
                          <td>{row.S_No}</td>
                          <td>{row.ServiceType}</td>
                          <td>{row.SelectItemName}</td>
                          <td>{row.Charges || "-"}</td>
                          <td>{row.Quantity || "-"}</td>
                          <td>{row.Amount || "-"}</td>
                          <td>{row.DiscountType || "-"}</td>
                          <td>{row.Discount || "-"}</td>
                          <td>{row.NetAmount || "-"}</td>
                          <td>{row.Status || "-"}</td>
                          {/* <td>
                            <input
                              type="checkbox"
                              checked={row.isReimbursable === "Yes"}
                              onChange={(e) =>
                                handleReimbursableChange(e, index)
                              }
                            />
                          </td> */}
                          <td>
                            {/* <button
            className="delnamebtn"
            onClick={() => {
              Editbillingitem(row);
            }}
          >
            <EditIcon />
          </button> */}
                            <button
                              className="delnamebtn"
                              onClick={() => {
                                deletebillingitem(row);
                              }}
                            >
                              <DeleteIcon />
                            </button>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>

              <div className="">
                <br />

                <div className="summary-container addded_sumry_contre">
                  <div
                    className="RegisFormcon"
                    style={{ justifyContent: "center" }}
                  >
                    <div className="RegisBillSearchForm_1">
                      <label htmlFor="">
                        Total Discount<span>:</span>
                      </label>
                      <select
                        name="CDMethod"
                        value={NetAmount_CDmethod.Method}
                        onChange={(e) => {
                          setNetAmount_CDmethod((prev) => ({
                            ...prev,
                            Method: e.target.value,
                            Amount: "",
                          }));
                          setBillAmount([]);
                          setFormAmount({
                            Billpay_method: "",
                            CardType: "",
                            CardNo: "",
                            upiid: "",
                            TransactionId: "",
                            ChequeNo: "",
                            BankName: "",
                            paidamount: "",
                            Additionalamount: "",
                            transactionFee: "",
                          });
                        }}
                        disabled={SelectDatalist.length === 0}
                      >
                        <option value="">Select</option>
                        <option value="Cash">Cash</option>
                        <option value="Percentage">Percentage</option>
                      </select>
                    </div>
                    <div className="cah-d-wth RegisBillSearchForm_1">
                      <label htmlFor="">
                        Discount Value<span>:</span>
                      </label>
                      <input
                        type="number"
                        onKeyDown={blockInvalidChar}
                        name="CashDiscount"
                        value={NetAmount_CDmethod.Amount}
                        onChange={(e) => {
                          if (NetAmount_CDmethod.Method !== "") {
                            setNetAmount_CDmethod((prev) => ({
                              ...prev,
                              Amount: e.target.value,
                            }));
                            setBillAmount([]);
                            setFormAmount({
                              Billpay_method: "",
                              CardType: "",
                              CardNo: "",
                              upiid: "",
                              TransactionId: "",
                              ChequeNo: "",
                              BankName: "",
                              paidamount: "",
                              Additionalamount: "",
                              transactionFee: "",
                            });
                          } else {
                            alert("Please Choose an Discount Method");
                          }
                        }}
                      />
                    </div>
                  </div>
                </div>

                <div className="summary-container addded_sumry_contre">
                  <div className="WDWDWD_OO">
                    <div className="edcwjkediu87_mmmm">
                      <div>
                        <div
                          className="EWDWDWDWDCC_0"
                          style={{
                            justifyContent: "center",
                            marginTop: "5px",
                          }}
                        >
                          <div className="clm-itm-stl">
                            <label>
                              Payment Method <span>:</span>
                            </label>
                            <select
                              name="Billpay_method"
                              value={formAmount.Billpay_method}
                              onChange={handleChange}
                            >
                              <option value="">Select</option>
                              <option value="Cash">Cash</option>
                              <option value="Card">Card</option>
                              <option value="OnlinePayment">
                                Online Payment
                              </option>
                              <option value="Cheque">Cheque</option>
                            </select>
                          </div>
                          {formAmount.Billpay_method === "Card" && (
                            <>
                              <div className="clm-itm-stl">
                                <label>
                                  Card Type <span>:</span>
                                </label>
                                <select
                                  name="CardType"
                                  value={formAmount.CardType}
                                  onChange={handleChange}
                                >
                                  <option value="">Select</option>
                                  {["Debit", "Credit"].map((p, indx) => (
                                    <option key={indx} value={p}>
                                      {p}
                                    </option>
                                  ))}
                                </select>
                              </div>
                              <div className="clm-itm-stl">
                                <label>
                                  Card No <span>:</span>
                                </label>
                                <input
                                  type="number"
                                  onKeyDown={blockInvalidChar}
                                  name="CardNo"
                                  value={formAmount.CardNo}
                                  onChange={handleChange}
                                />
                              </div>
                              <div className="clm-itm-stl">
                                <label>
                                  Transaction Id <span>:</span>
                                </label>
                                <input
                                  type="text"
                                  onKeyDown={blockInvalidChar}
                                  name="TransactionId"
                                  value={formAmount.TransactionId}
                                  onChange={handleChange}
                                />
                              </div>
                            </>
                          )}
                          {formAmount.Billpay_method === "Cheque" && (
                            <>
                              <div className="clm-itm-stl">
                                <label>
                                  Cheque No <span>:</span>
                                </label>
                                <input
                                  type="number"
                                  onKeyDown={blockInvalidChar}
                                  name="ChequeNo"
                                  value={formAmount.ChequeNo}
                                  onChange={handleChange}
                                />
                              </div>
                              <div className="clm-itm-stl">
                                <label>
                                  Bank Name <span>:</span>
                                </label>
                                <input
                                  type="text"
                                  name="BankName"
                                  value={formAmount.BankName}
                                  onChange={handleChange}
                                />
                              </div>
                            </>
                          )}
                          {formAmount.Billpay_method === "Card" && (
                            <>
                              <div className="clm-itm-stl">
                                <label>
                                  Transaction Fee <span>:</span>
                                </label>
                                <input
                                  type="number"
                                  name="transactionFee"
                                  value={formAmount.transactionFee || ""}
                                  onChange={handleChange}
                                  onKeyDown={blockInvalidChar}
                                />
                              </div>
                            </>
                          )}
                          {formAmount.Billpay_method === "OnlinePayment" && (
                            <>
                              <div className="clm-itm-stl">
                                <label>
                                  UPI Id <span>:</span>
                                </label>
                                <input
                                  type="text"
                                  onKeyDown={blockInvalidChar}
                                  name="upiid"
                                  value={formAmount.upiid}
                                  onChange={handleChange}
                                />
                              </div>
                              <div className="clm-itm-stl">
                                <label>
                                  Transaction Id <span>:</span>
                                </label>
                                <input
                                  type="text"
                                  onKeyDown={blockInvalidChar}
                                  name="TransactionId"
                                  value={formAmount.TransactionId}
                                  onChange={handleChange}
                                />
                              </div>
                            </>
                          )}
                          <div className="clm-itm-stl">
                            <label>
                              Cash Amount <span>:</span>
                            </label>
                            <input
                              onKeyDown={blockInvalidChar}
                              type="number"
                              name="paidamount"
                              value={formAmount.paidamount}
                              onChange={handleChange}
                            />
                          </div>
                          <div className="clm-itm-stl">
                            <label>
                              AdditionalAmount <span>:</span>
                            </label>
                            <input
                              onKeyDown={blockInvalidChar}
                              type="number"
                              name="Additionalamount"
                              value={formAmount.Additionalamount}
                              onChange={handleChange}
                            />
                          </div>
                        </div>

                        <div className="Register_btn_con added_Register_btn_con">
                          <button
                            className="RegisterForm_1_btns added_RegisterForm_1_btns"
                            onClick={isEdit !== null ? handleUpdate : handleAdd}
                          >
                            {isEdit !== null ? "Update" : "Add"}
                          </button>
                        </div>

                        <div className="edwqw_c2">
                          <label>Amount in Words : </label>
                          <span
                            style={{
                              color: "#808080b5",
                              padding: "0px 0px 0px 5px",
                            }}
                          >
                            {NumberToWords(+initialState.totalNetAmount)}{" "}
                          </span>
                        </div>
                        <br />
                        {AppointmentRegisType === 'IP' && <div className="clm-itm-stl">
                          <label>
                            Remaining Credit <span>:</span>
                          </label>
                          <input
                            style={RemainingCredit < 50000 ? { backgroundColor: "Red" } : {}} value={RemainingCredit} readOnly
                          />
                        </div>}
                        <br />
                      </div>
                    </div>

                    <div className="EWDWDWDWDCC_0 wdwdxsxwsw3ed">
                      <div className="clm-itm-stl">
                        <label>Items:</label>
                        <input value={initialState.totalItems} readOnly />
                      </div>
                      <div className="clm-itm-stl">
                        <label>Unit:</label>
                        <input value={initialState.totalUnits} readOnly />
                      </div>

                      <div className="clm-itm-stl">
                        <label>Taxable Amount:</label>
                        <input value={initialState.totalTaxable} readOnly />
                      </div>
                      <div className="clm-itm-stl">
                        <label>GST Amount :</label>
                        <input value={initialState.totalGstamount} readOnly />
                      </div>
                      <div className="clm-itm-stl">
                        <label>Cash Discount :</label>
                        <input value={initialState.totalDiscount} readOnly />
                      </div>

                      <div className="clm-itm-stl">
                        <label>Total Amount:</label>
                        <input value={initialState.totalAmount} readOnly />
                      </div>
                      <div className="clm-itm-stl">
                        <label>Item Amount :</label>
                        <input
                          style={{ backgroundColor: "yellow" }}
                          value={initialState.totalNetAmount}
                          readOnly
                        />
                      </div>
                      <div className="clm-itm-stl">
                        <label>Round Off :</label>
                        <input value={initialState.Roundoff} readOnly />
                      </div>

                      <div className="clm-itm-stl">
                        <label>Paid Net Amount :</label>
                        <input
                          style={{ backgroundColor: "yellow" }}
                          value={initialState.totalAmountt}
                          readOnly
                        />
                      </div>
                      {Reimbursable && (
                        <div className="clm-itm-stl">
                          {console.log("innnnnnn", initialState)}
                          <label>Re-imbursable Amount :</label>
                          <input
                            style={{ backgroundColor: "yellow" }}
                            value={initialState.ReimbursableAmount}
                            readOnly
                          />
                        </div>
                      )}
                      <div className="clm-itm-stl">
                        <label>Paid Amount :</label>
                        <input value={initialState.PaidAmount} readOnly />
                      </div>
                      <div className="clm-itm-stl">
                        <label>Balance Amount :</label>
                        <input value={initialState.BalanceAmount} readOnly />
                      </div>
                    </div>
                  </div>

                  <br />
                  <div>
                    {billAmount.length !== 0 && (
                      <div className="Selected-table-container444 DEWSDXWED">
                        <table className="selected-medicine-table222 EDWEDE">
                          <thead>
                            <tr>
                              <th>S.No</th>
                              <th>Payment Type</th>
                              <th>Card Type</th>

                              <th>Cheque No</th>
                              <th>Bank Name</th>

                              <th>Amount</th>
                              <th>Additional Amount</th>
                              <th>Transaction Fee</th>
                              <th>Action </th>
                            </tr>
                          </thead>
                          <tbody>
                            {billAmount.map((row, index) => (
                              <tr key={index}>
                                <td>{index + 1}</td>
                                <td>{row.Billpay_method}</td>
                                <td>{row.CardType || "-"}</td>
                                <td>{row.ChequeNo || "-"}</td>
                                <td>{row.BankName || "-"}</td>
                                <td>{row.paidamount}</td>
                                <td>{row.Additionalamount}</td>
                                <td>{row.transactionFee}</td>
                                <td>
                                  <button onClick={() => handleEdit(index)}>
                                    <EditNoteIcon />
                                  </button>
                                </td>
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    )}
                  </div>
                </div>

                {isPrintButtonVisible && (
                  <div className="Register_btn_con added_Register_btn_con">
                    <select
                      className="print_option_bill"
                      name="printoption"
                      value={printoption}
                      onChange={(e) => setprintoption(e.target.value)} // Update state with selected value
                    >
                      {[
                        "PrintDetailed",
                        "PrintSummary",
                        "PrintNon-Reimbusable",
                        "PrintReimbuseable",
                      ].map((f) => (
                        <option key={f} value={f}>
                          {f}
                        </option> // Correctly return option elements
                      ))}
                    </select>
                    {printoption === "PrintDetailed" ? (
                      <button
                        className="RegisterForm_1_btns added_RegisterForm_1_btns"
                        onClick={() => handleSubmit()}
                      >
                        Print
                      </button>
                    ) : printoption === "PrintSummary" ? (
                      <button
                        className="RegisterForm_1_btns added_RegisterForm_1_btns"
                        onClick={() => handleSubmit(true)}
                      >
                        Print
                      </button>
                    ) : printoption === "PrintReimbuseable" ? (
                      <button
                        className="RegisterForm_1_btns added_RegisterForm_1_btns"
                        onClick={() => handleSubmit(false, true)} // Pass a second parameter for "PrintReimbuseable"
                      >
                        Print
                      </button>
                    ) : (
                      <button
                        className="RegisterForm_1_btns added_RegisterForm_1_btns"
                        onClick={() => handleSubmit(false, false, true)} // Pass a second parameter for "PrintReimbuseable"
                      >
                        Print
                      </button>
                    )}
                  </div>
                )}
              </div>
            </div>

            <ToastAlert Message={toast.message} Type={toast.type} />
          </div>
        </>
      ) : isPrintSummary ? (
        <ForPrintSumData />
      ) : printoption === "PrintReimbuseable" ? (
        <ForPrintReimbData />
      ) : printoption === "PrintNon-Reimbusable" ? (
        <ForPrintNon_ReimbData />
      ) : (
        <ForPrintData />
      )}
    </>
  );
};

export default QuickBilling;
