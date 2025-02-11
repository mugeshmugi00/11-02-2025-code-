import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { addDays, format } from "date-fns";
import bgImg2 from "../Assets/bgImg2.jpg";
import AddBoxIcon from "@mui/icons-material/AddBox";
import ToastAlert from "../OtherComponent/ToastContainer/ToastAlert";
import DeleteIcon from "@mui/icons-material/Delete";
import axios from "axios";



function InsuranceMainpage() {

  const toast = useSelector((state) => state.userRecord?.toast);
  const UrlLink = useSelector((state) => state.userRecord?.UrlLink);
  const UserData = useSelector((state) => state.userRecord?.UserData);

  const InsurancePatientDetailes = useSelector(state => state.Insurancedata?.InsurancePatientDetailes)
  // console.log("InsurancePatientDetailes", InsurancePatientDetailes);

  const dispatchvalue = useDispatch();
  const navigate = useNavigate();


  const [PatientDetails, setPatientDetails] = useState([]);

  const [InsuranceDetails, setInsuranceDetails] = useState([]);


  const [InsuranceMaindata, setInsuranceMaindata] = useState({
    PreAuthDate: '',
    PreAuthAmount: '',
    DischargeDate: '',
    FinalBillAmount: '',
    RaisedAmount: '',
    ApprovedAmount: '',
    CourierDate: '',
    SettlementDateCount: '',
    TdsPercentage: 10,
    TdsAmount: '',
    FinalSettlementAmount: ''

  })
  const [insurancetype, setInsurancetype] = useState({
    insurancetype: '',
    policynumber: ''

  })

  const [CoPaymentCoverage, setCoPaymentCoverage] = useState("No");
  console.log("CoPaymentCoverage", CoPaymentCoverage)

  const [CoPaymentDetails, setCoPaymentDetails] = useState({
    CoPaymentType: '',
    CoPaymentTypeValue: '',
    CoPaymentBillAmount: '',
    CoPaymentFinalAmount: '',
  })
  console.log("CoPaymentDetails", CoPaymentDetails)

  const handleCheckboxCoPayment = (event) => {
    const value = event.target.value;
    // Always update the state with the selected value
    if (value === 'No') {
      setCoPaymentCoverage(value); 
      setCoPaymentDetails({
        CoPaymentType: '',
        CoPaymentTypeValue: '',
        CoPaymentBillAmount: '',
        CoPaymentFinalAmount: '',
      });
    }
  else{
    setCoPaymentCoverage(value); 
  }
  };


  const [Employee, setEmployee] = useState({
    IsEmployee: 'No',
    CompanyName: '',
    Employeeid: '',
    EmployeeDesignation: '',

  })

  const [AmountState, setAmountState] = useState({
    SettlementDate: '',
    SettlementAmount: '',
    UTRNumber: '',
  })

  const [AmountArray, setAmountArray] = useState([])






  useEffect(() => {
    const fetchPatientDetails = async () => {
      try {
        const response = await axios.get(`${UrlLink}Insurance/Post_Insurance_Patient_Detailes?GetId=${InsurancePatientDetailes?.id}`);
        const data = response.data;
        console.log("data123",data);

        if (data && Object.keys(data).length > 0) {
          const {
            AmountArray = [],
            CoPaymentCoverage = 'No',
            insurancetype = '',
            policynumber = '',
            CoPaymentType = '',
            CoPaymentTypeValue = '',
            CoPaymentBillAmount = '',
            CoPaymentFinalAmount = '',
            IsEmployee = 'No',
            CompanyName = '',
            Employeeid = '',
            EmployeeDesignation = '',
            ...rest
          } = data;

          setInsurancetype({
            insurancetype,
            policynumber,
          });

          setEmployee({
            IsEmployee,
            CompanyName,
            Employeeid,
            EmployeeDesignation,
          });

          setCoPaymentDetails({
            CoPaymentType,
            CoPaymentTypeValue,
            CoPaymentBillAmount,
            CoPaymentFinalAmount,
          });

          setCoPaymentCoverage(CoPaymentCoverage || 'No');
          setAmountArray(AmountArray);
          setInsuranceMaindata(rest);
        }
      } catch (error) {
        console.log('Error fetching patient details:');
      }
    };

    if (InsurancePatientDetailes?.id) {
      fetchPatientDetails();
    }
  }, [InsurancePatientDetailes?.id, UrlLink]);


  useEffect(() => {
    if (InsurancePatientDetailes?.RegistrationId && InsurancePatientDetailes?.PatientId && InsurancePatientDetailes?.PatientServiesType) {
      axios.get(`${UrlLink}Insurance/Insurance_Patient_Details?RegistrationId=${InsurancePatientDetailes.RegistrationId}&PatientId=${InsurancePatientDetailes.PatientId}&PatientServiesType=${InsurancePatientDetailes.PatientServiesType}`)
        .then((res) => {
          if (Array.isArray(res?.data)) {
            setPatientDetails(res.data); // Set data only if it is an array
          } else {
            console.log("Unexpected response format: Expected an array", res.data);
          }
        })
        .catch((err) => {
          console.error("Error fetching patient details:", err);
        });
    }
  }, [InsurancePatientDetailes, UrlLink]);


  useEffect(() => {
    if (InsurancePatientDetailes?.InsuranceId) {
      axios.get(`${UrlLink}Insurance/Insurance_Details_get?InsuranceId=${InsurancePatientDetailes?.InsuranceId}`)
        .then((res) => {

          if (Array.isArray(res?.data)) {
            setInsuranceDetails(res.data); // Set data only if it is an array
          } else {
            console.log("Unexpected response format: Expected an array", res.data);
          }

        })
        .catch((err) => {
          console.error("Error fetching insurance details:", err);
        });
    }

  }, [InsurancePatientDetailes, UrlLink])




  const clearAmountState = () => {

    setAmountState({
      SettlementDate: '',
      SettlementAmount: '',
      UTRNumber: '',
    })
  }

  const HandelOnchangeState = (event) => {
    const { name, value } = event.target
    if (name === 'ApprovedAmount') {
      if (value !== '') {
        setInsuranceMaindata((prev) => ({
          ...prev,
          [name]: value,
        }))
      }
      else if (value === '') {
        setInsuranceMaindata((prev) => ({
          ...prev,
          [name]: value,
          TdsAmount: '',
          FinalSettlementAmount: ''
        }))
      }
    }
    else if (name === 'TdsAmount') {
      if (value !== '') {
        setInsuranceMaindata((prev) => ({
          ...prev,
          [name]: value,
        }))
      }
      else if (value === '') {
        setInsuranceMaindata((prev) => ({
          ...prev,
          [name]: value,
          FinalSettlementAmount: ''
        }))
      }
    }
    else {
      setInsuranceMaindata((prev) => ({
        ...prev,
        [name]: value,
      }))
    }


  }

  useEffect(() => {
    const { ApprovedAmount } = InsuranceMaindata;

    const approvedAmount = parseFloat(ApprovedAmount) || 0;
    const tdsPercentage = parseFloat(10) || 0;

    let tdsAmount = 0; // Initialize as a number
    let finalSettlementAmount = 0; // Initialize as a number

    if (approvedAmount > 0 && tdsPercentage > 0) {
      tdsAmount = (approvedAmount * tdsPercentage) / 100;
      finalSettlementAmount = approvedAmount - tdsAmount;
    }

    setInsuranceMaindata((prev) => ({
      ...prev,
      TdsPercentage:tdsPercentage,
      TdsAmount: tdsAmount.toFixed(2),  // Format as string with two decimal places
      FinalSettlementAmount: finalSettlementAmount.toFixed(2),
    }));
  }, [InsuranceMaindata.ApprovedAmount]);


  const handelOnchageAmountState = (e) => {

    const { name, value } = e.target

    setAmountState((prev) => ({
      ...prev,
      [name]: value,
    }))

  }

  const handleEmployeeOnChange = (e) => {
    const { name, value } = e.target;
    console.log("name", name, value);

    if (name === 'IsEmployee') {
      if (value === 'Yes') {
        setEmployee((prev) => ({
          ...prev,
          [name]: value
        }));
      } else if (value === 'No') {
        setEmployee((prev) => ({
          ...prev,
          [name]: value,
          CompanyName: '',
          Employeeid: '',
          EmployeeDesignation: ''
        }));
      }
    }
    else {
      setEmployee((prev) => ({
        ...prev,
        [name]: value
      }));
    }
  };


  const HandeleSaveAmount = () => {

    const requiredFileds = [
      'SettlementDate',
      'SettlementAmount',
      'UTRNumber',
    ]

    const missingFields = requiredFileds.filter((ele) => !AmountState[ele])

    if (missingFields.length > 0) {
      const tdata = {
        message: `Please fill empty fields: ${missingFields.join(", ")}`,
        type: "warn",
      };
      dispatchvalue({ type: "toast", value: tdata });
    }
    else {

      setAmountArray((prev) => [
        ...prev,
        { 'id': prev.length + 1, ...AmountState }
      ])

    }

    clearAmountState()


  }


  const HandelDeleteAmount = (id) => {

    let RemoveData = AmountArray.filter((ele) => ele.id !== id);

    RemoveData = RemoveData.map((ele, ind) => {
      return { ...ele, id: ind + 1 };
    })

    setAmountArray(RemoveData)

  };



  const SaveInsuranceRais = (status) => {

    const SubPostFun = (status) => {

      // Validation for Employee fields if Employee is marked as 'Yes'
      if (Employee.IsEmployee === 'Yes') {
        if (!Employee.CompanyName || !Employee.EmployeeDesignation || !Employee.Employeeid) {
          const tdata = {
            message: "Please fill Company Name, Employee ID, and Employee Designation",
            type: "warn"
          };
          dispatchvalue({ type: "toast", value: tdata });
          return; // Stop execution if validation fails
        }
      }

      // Validation for CoPaymentCoverage
      if (CoPaymentCoverage === 'Yes') {
        if (!CoPaymentDetails.CoPaymentType || !CoPaymentDetails.CoPaymentBillAmount || !CoPaymentDetails.CoPaymentTypeValue) {
          const tdata = {
            message: "Please fill CoPaymentType, CoPaymentBillAmount, and CoPaymentTypeValue",
            type: "warn"
          };
          dispatchvalue({ type: "toast", value: tdata });
          return; // Stop execution if validation fails
        }
      }

      // Prepare parameters
      let params = {
        TableId: InsurancePatientDetailes?.id,
        ...InsuranceMaindata,
        CoPaymentCoverage: CoPaymentCoverage,
        CoPaymentDetails: { ...CoPaymentDetails }, // Correct spread syntax for object
        insurancetype: { ...insurancetype }, // Correct spread syntax for object
        Employee: { ...Employee }, // Correct spread syntax for object
        AmountArray: AmountArray,
        Created_By: UserData?.username,
        Status: status || '',
      };

      console.log('Sending params:', params);

      // API call
      axios.post(`${UrlLink}Insurance/Post_Insurance_Patient_Detailes`, params)
        .then((res) => {
          let resdata = res.data;
          let type = Object.keys(resdata)[0];
          let mess = Object.values(resdata)[0];
          const tdata = {
            message: mess,
            type: type,
          };
          dispatchvalue({ type: 'toast', value: tdata });
          
          
          if (type === 'success') {
            navigate('/Home/InsuranceDashboard');
          }
        })
        .catch((err) => {
          console.log(err);
        });
    };

    if (status) {
      let ConformStatus = window.confirm("Are you sure you want to change the status to 'Completed'? Once the status is 'Completed,' it cannot be edited.");
      if (ConformStatus) {
        SubPostFun(status);
      }
    } else {
      SubPostFun();
    }
  };


  const HandleCoPaymentDetails = (e) => {
    const { name, value } = e.target;

    if (name === 'CoPaymentBillAmount') {
      if (value !== '') {
        setCoPaymentDetails((prev) => ({
          ...prev,
          [name]: value,
        }));
      }
      else if (value == '') {
        setCoPaymentDetails((prev) => ({
          ...prev,
          [name]: value,
          CoPaymentTypeValue: '',
          CoPaymentType: '',
          CoPaymentFinalAmount: ''
        }));
      }

    }
    else if (name === 'CoPaymentType') {
      if (value !== '') {
        setCoPaymentDetails((prev) => ({
          ...prev,
          [name]: value
        }));
      } else if (value === '') {
        setCoPaymentDetails((prev) => ({
          ...prev,
          [name]: value,
          CoPaymentTypeValue: '',
          CoPaymentFinalAmount: ''
        }));
      }
    }
    else {
      setCoPaymentDetails((prev) => ({
        ...prev,
        [name]: value
      }));
    }
  };

  useEffect(() => {
    const { CoPaymentBillAmount, CoPaymentType, CoPaymentTypeValue } = CoPaymentDetails;

    const billAmount = parseFloat(CoPaymentBillAmount) || 0;
    const coPaymentValue = parseFloat(CoPaymentTypeValue) || 0;

    let finalAmount = '';
    if (CoPaymentType === 'Percentage' && billAmount > 0 && coPaymentValue > 0) {
      const percentageAmount = (billAmount * coPaymentValue) / 100;
      finalAmount = (billAmount - percentageAmount).toFixed(2);
    } else if (CoPaymentType === 'Value' && billAmount > 0 && coPaymentValue > 0) {
      finalAmount = (billAmount - coPaymentValue).toFixed(2);
    }

    setCoPaymentDetails((prev) => ({
      ...prev,
      CoPaymentFinalAmount: finalAmount,
    }));
  }, [CoPaymentDetails.CoPaymentBillAmount, CoPaymentDetails.CoPaymentType, CoPaymentDetails.CoPaymentTypeValue]);


  return (
    <>
      <div className='Main_container_app'>

        <div className="new-patient-registration-form" >
          <br />
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
                  {InsurancePatientDetailes?.PatientId}
                </span>
              </div>
              <div className="RegisForm_1 ">
                <label htmlFor="PatientName">
                  Patient Name <span>:</span>{" "}
                </label>
                <span className="dctr_wrbvh_pice" htmlFor="PatientName">
                  {InsurancePatientDetailes?.PatientName}

                </span>
              </div>
              <div className="RegisForm_1">
                <label htmlFor="AgeGender">
                  Age / Gender<span>:</span>
                </label>
                <span className="dctr_wrbvh_pice" id="AgeGender">
                  {Array.isArray(PatientDetails) && PatientDetails.length > 0
                    ? `${PatientDetails[0]?.Age || ""} / ${PatientDetails[0]?.Gender || ""}`
                    : ""}
                </span>
              </div>
              <div className="RegisForm_1">
                <label htmlFor="PhoneNo">
                  Phone Number<span>:</span>
                </label>
                <span className="dctr_wrbvh_pice" id="PhoneNo">
                  {Array.isArray(PatientDetails) && PatientDetails.length > 0
                    ? `${PatientDetails[0]?.PhoneNo || ""}`
                    : ""}
                </span>
              </div>
              <div className="RegisForm_1">
                <label htmlFor="DoctorName">
                  Doctor Name<span>:</span>
                </label>
                <span className="dctr_wrbvh_pice" id="DoctorName">
                  {Array.isArray(PatientDetails) && PatientDetails.length > 0
                    ? `${PatientDetails[0]?.DoctorName || ""}`
                    : ""}
                </span>
              </div>
              <div className="RegisForm_1">
                <label htmlFor="PurposeofAdmission">
                  Purpose of Admission<span>:</span>
                </label>
                <span className="dctr_wrbvh_pice" id="PurposeofAdmission">
                  {Array.isArray(PatientDetails) && PatientDetails.length > 0
                    ? `${PatientDetails[0]?.PurposeofAdmission || ""}`
                    : ""}
                </span>
              </div>
              <div className="RegisForm_1">
                <label htmlFor="PurposeDateofAdmissionofAdmission">
                  Date of Admission<span>:</span>
                </label>
                <span className="dctr_wrbvh_pice" id="DateofAdmission">
                  {Array.isArray(PatientDetails) && PatientDetails.length > 0
                    ? `${PatientDetails[0]?.DateofAdmission || ""}`
                    : ""}
                </span>
              </div>
              <div className="RegisForm_1">
                <label htmlFor="isMlc">
                  IsMLC<span>:</span>
                </label>
                <span className="dctr_wrbvh_pice" id="isMlc">
                  {Array.isArray(PatientDetails) && PatientDetails.length > 0
                    ? `${PatientDetails[0]?.isMlc || ""}`
                    : ""}
                </span>
              </div>





              <div className="RegisForm_1 ">
                <label htmlFor="Age">
                  Registration ID <span>:</span>{" "}
                </label>
                <span className="dctr_wrbvh_pice" htmlFor="Age">
                  {InsurancePatientDetailes?.RegistrationId}
                </span>
              </div>


            </div>
          </div>

        </div>

        <br />

        <div className="RegisFormcon_1">

          <div className="RegisForm_1">
            <label htmlFor="InsuranceName">
              Insurance Name<span>:</span>
            </label>
            <span className="dctr_wrbvh_pice" id="InsuranceName">
              {Array.isArray(InsuranceDetails) && InsuranceDetails.length > 0
                ? `${InsuranceDetails[0]?.Insurance_Name || ""}`
                : ""}
            </span>
          </div>

          <div className="RegisForm_1">
            <label htmlFor="InsuranceName">
              Payer Zone<span>:</span>
            </label>
            <span className="dctr_wrbvh_pice" id="InsuranceName">
              {Array.isArray(InsuranceDetails) && InsuranceDetails.length > 0
                ? `${InsuranceDetails[0]?.Payer_Zone || ""}`
                : ""}
            </span>
          </div>
          <div className="RegisForm_1">
            <label htmlFor="InsuranceName">
              PayerMember Id<span>:</span>
            </label>
            <span className="dctr_wrbvh_pice" id="InsuranceName">
              {Array.isArray(InsuranceDetails) && InsuranceDetails.length > 0
                ? `${InsuranceDetails[0]?.PayerMember_Id || ""}`
                : ""}
            </span>
          </div>
          <div className="RegisForm_1">
            <label htmlFor="InsuranceName">
              Contact Person<span>:</span>
            </label>
            <span className="dctr_wrbvh_pice" id="InsuranceName">
              {Array.isArray(InsuranceDetails) && InsuranceDetails.length > 0
                ? `${InsuranceDetails[0]?.ContactPerson || ""}`
                : ""}
            </span>
          </div>
          <div className="RegisForm_1">
            <label htmlFor="InsuranceName">
              Phone Number<span>:</span>
            </label>
            <span className="dctr_wrbvh_pice" id="InsuranceName">
              {Array.isArray(InsuranceDetails) && InsuranceDetails.length > 0
                ? `${InsuranceDetails[0]?.PhoneNumber || ""}`
                : ""}
            </span>
          </div>
          <div className="RegisForm_1">
            <label htmlFor="InsuranceName">
              MailId<span>:</span>
            </label>
            <span className="dctr_wrbvh_pice" id="InsuranceName">
              {Array.isArray(InsuranceDetails) && InsuranceDetails.length > 0
                ? `${InsuranceDetails[0]?.MailId || ""}`
                : ""}
            </span>
          </div>
          <div className="RegisForm_1">
            <label htmlFor="policynumber">
              Policy / Card Number<span>:</span>
            </label>
            <input
              type="text"
              id="policynumber"
              name="policynumber"
              value={insurancetype.policynumber}
              onChange={(e) => setInsurancetype({ ...insurancetype, policynumber: e.target.value })}
            />
          </div>
          <div className="RegisForm_1">
            <label htmlFor="insurancetype">
              Insurance Type<span>:</span>
            </label>
            <select
              id="insurancetype"
              name="insurancetype"
              value={insurancetype.insurancetype}
              onChange={(e) => setInsurancetype({ ...insurancetype, insurancetype: e.target.value })}
            >
              <option value="">Select</option>
              <option value="Cashless">Cashless</option>
              <option value="Reimbursable">Reimbursable</option>
            </select>
          </div>


        </div>
        <br></br>

        <div className="RegisForm_1">
          <label htmlFor="IsEmployee" >
            Employee ? <span>:</span>
          </label>
          <div className="ewj_i87_head">
            <div className="ewj_i87">

              <input
                type="radio"
                name="IsEmployee"
                value="Yes"
                checked={Employee.IsEmployee === "Yes"}
                onChange={handleEmployeeOnChange}
              />

              <label htmlFor="employedYes">Yes</label>
            </div>
            <div className="ewj_i87">

              <input
                type="radio"
                name="IsEmployee"
                value="No"

                checked={Employee.IsEmployee === "No"}
                onChange={handleEmployeeOnChange}
              />

              <label htmlFor="employedNo">No</label>
            </div>
          </div>
        </div>



        <br></br>
        <div className="RegisFormcon_1">
          {Employee.IsEmployee === 'Yes' && (
            <>
              <div className="RegisForm_1">
                <label htmlFor="CompanyName">
                  Company Name<span>:</span>
                </label>
                <input
                  type="text"
                  id="CompanyName"
                  name="CompanyName"
                  value={Employee.CompanyName}
                  onChange={handleEmployeeOnChange}
                />
              </div>

              <div className="RegisForm_1">
                <label htmlFor="Employeeid">
                  Employee ID<span>:</span>
                </label>
                <input
                  type="text"
                  id="Employeeid"
                  name="Employeeid"
                  value={Employee.Employeeid}
                  onChange={handleEmployeeOnChange}
                />
              </div>

              <div className="RegisForm_1">
                <label htmlFor="EmployeeDesignation">
                  Employee Designation<span>:</span>
                </label>
                <input
                  type="text"
                  id="EmployeeDesignation"
                  name="EmployeeDesignation"
                  value={Employee.EmployeeDesignation}
                  onChange={handleEmployeeOnChange}
                />
              </div>
            </>
          )}
        </div>

        <br></br>

        <div className="RegisForm_1">
          <label>
            CoPayment ? <span>:</span>
          </label>

          <div className="ewj_i87_head">
            <div className="ewj_i87">
              <input
                type="radio"
                name="CoPaymentCoverage"
                value="Yes"
                checked={CoPaymentCoverage === "Yes"}
                onChange={handleCheckboxCoPayment}
              />
              <label htmlFor="CoPaymentYes">Yes</label>
            </div>

            <div className="ewj_i87">
              <input
                type="radio"
                name="CoPaymentCoverage"
                value="No" // Corrected from CoPaymentCoverage to "No"
                checked={CoPaymentCoverage === "No"}
                onChange={handleCheckboxCoPayment}
              />
              <label htmlFor="CoPaymentNo">No</label>
            </div>
          </div>
        </div>
        <br />
        {CoPaymentCoverage === "Yes" && (
          <div className="RegisFormcon_1">
            <div className="RegisForm_1">

              <label>Bill Amount<span>:</span></label>
              <input
                name='CoPaymentBillAmount'
                value={CoPaymentDetails.CoPaymentBillAmount}
                onChange={HandleCoPaymentDetails}
                autoComplete="off"
                onKeyDown={(e) =>
                  ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()
                }
              />

            </div>

            <div className="RegisForm_1">

              <label>Co-Payment Type<span>:</span></label>
              <select
                style={{ width: '100px' }}
                name='CoPaymentType'
                value={CoPaymentDetails.CoPaymentType}
                onChange={HandleCoPaymentDetails}
              >
                <option value=''>Select</option>
                <option value='Percentage'>Percentage</option>
                <option value='Value'>Value</option>


              </select>
              <input
                type='number'
                style={{ width: '50px' }}
                name='CoPaymentTypeValue'
                value={CoPaymentDetails.CoPaymentTypeValue}
                onChange={HandleCoPaymentDetails}
                autoComplete="off"
                onKeyDown={(e) =>
                  ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()
                }
              />
            </div>

            <div className="RegisForm_1">

              <label>CoPayment Amount<span>:</span></label>
              <input
                type='number'
                style={{ width: '50px' }}
                name='CoPaymentFinalAmount'
                value={CoPaymentDetails.CoPaymentFinalAmount}
                onChange={HandleCoPaymentDetails}
                autoComplete="off"
                onKeyDown={(e) =>
                  ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()
                }
                disabled
              />

            </div>






          </div>
        )}


        <br />

        <div className="RegisFormcon_1">

          <div className="RegisForm_1">


            <label>PreAuth Date<span>:</span></label>
            <input
              type='date'
              name='PreAuthDate'
              value={InsuranceMaindata.PreAuthDate}
              onChange={HandelOnchangeState}
            />

          </div>


          <div className="RegisForm_1">


            <label>PreAuth Amount<span>:</span></label>
            <input
              type='number'
              name='PreAuthAmount'
              value={InsuranceMaindata.PreAuthAmount}
              onChange={HandelOnchangeState}
            />

          </div>

          <div className="RegisForm_1">


            <label>Discharge Date<span>:</span></label>
            <input
              type='date'
              name='DischargeDate'
              value={InsuranceMaindata.DischargeDate}
              onChange={HandelOnchangeState}
            />

          </div>

          <div className="RegisForm_1">


            <label>Final Bill Amount<span>:</span></label>
            <input
              type='number'
              name='FinalBillAmount'
              value={InsuranceMaindata.FinalBillAmount}
              onChange={HandelOnchangeState}
            />

          </div>

          <div className="RegisForm_1">


            <label>Raised Amount<span>:</span></label>
            <input
              type='number'
              name='RaisedAmount'
              value={InsuranceMaindata.RaisedAmount}
              onChange={HandelOnchangeState}
            />

          </div>

          <div className="RegisForm_1">


            <label>Approved Amount<span>:</span></label>
            <input
              type='number'
              name='ApprovedAmount'
              value={InsuranceMaindata.ApprovedAmount}
              onChange={HandelOnchangeState}
            />

          </div>
          <div className="RegisForm_1">
            <label>TDS %<span>:</span></label>
            <input
              name='TdsPercentage'
              value={InsuranceMaindata.TdsPercentage}
              onChange={HandelOnchangeState}
              autoComplete="off"
              onKeyDown={(e) =>
                ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()
              }
              disabled
            />
          </div>
          <div className="RegisForm_1">
            <label>TDS Amount<span>:</span></label>
            <input
              name='TdsAmount'
              value={InsuranceMaindata.TdsAmount}
              onChange={HandelOnchangeState}
              autoComplete="off"
              onKeyDown={(e) =>
                ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()
              }
              disabled
            />
          </div>
          <div className="RegisForm_1">
            <label>Final Settlement Amount<span>:</span></label>
            <input
              name='FinalSettlementAmount'
              value={InsuranceMaindata.FinalSettlementAmount}
              onChange={HandelOnchangeState}
              autoComplete="off"
              onKeyDown={(e) =>
                ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()
              }
              disabled
            />
          </div>



          <div className="RegisForm_1">


            <label>Courier Date<span>:</span></label>
            <input
              type='date'
              name='CourierDate'
              value={InsuranceMaindata.CourierDate}
              onChange={HandelOnchangeState}
            />

          </div>


          <div className="RegisForm_1">


            <label>Settlement Date Count<span>:</span></label>
            <input
              type='number'
              name='SettlementDateCount'
              value={InsuranceMaindata.SettlementDateCount}
              onChange={HandelOnchangeState}
            />

          </div>

        </div>

        <br />
        <div className="RegisFormcon_1">

          <div className="RegisForm_1">


            <label>Settlement Date<span>:</span></label>
            <input
              type='date'
              name='SettlementDate'
              value={AmountState.SettlementDate}
              onChange={handelOnchageAmountState}
            />

          </div>

          <div className="RegisForm_1">


            <label>Settlement Amount<span>:</span></label>
            <input
              type='number'
              name='SettlementAmount'
              value={AmountState.SettlementAmount}
              onChange={handelOnchageAmountState}
            />

          </div>

          <div className="RegisForm_1">

            <label>UTR Number<span>:</span></label>
            <input
              type='text'
              name='UTRNumber'
              value={AmountState.UTRNumber}
              onChange={handelOnchageAmountState}
            />

            <div onClick={HandeleSaveAmount} className="Search_patient_icons" style={{ cursor: 'pointer' }}>
              <AddBoxIcon />
            </div>

          </div>

        </div>


        <br />

        {AmountArray.length !== 0 && <div className="for">
          <div className="Selected-table-container">
            <table className="selected-medicine-table2">
              <thead>
                <tr>
                  <th id="slectbill_ins" style={{ width: "160px" }}>S.No</th>
                  <th id="slectbill_ins" style={{ width: "260px" }}>Settlement Date</th>
                  <th id="slectbill_ins" style={{ width: "160px" }}>Settlement Amount</th>
                  <th id="slectbill_ins" style={{ width: "260px" }}>UTR Number</th>
                  <th id="slectbill_ins" style={{ width: "160px" }}>Action</th>
                </tr>
              </thead>
              <tbody>
                {AmountArray.length !== 0 && AmountArray.map((item, index) => (
                  <tr key={index}>
                    <td style={{ width: "160px" }}>{item.id}</td>
                    <td style={{ width: "260px" }}>{item.SettlementDate}</td>
                    <td style={{ width: "160px" }}>{item.SettlementAmount}</td>
                    <td style={{ width: "160px" }}>{item.UTRNumber}</td>
                    <td style={{ width: "160px" }} >
                      <DeleteIcon onClick={() => HandelDeleteAmount(item.id)} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>}

        <div style={{ display: 'flex', gap: '30px' }}>
          <div className="Main_container_Btn">
            <button onClick={() => SaveInsuranceRais('')}>
              Save
            </button>
          </div>


          {AmountArray.length !== 0 && <div className="Main_container_Btn">
            <button onClick={() => SaveInsuranceRais('COMPLETED')}>
              Compleate
            </button>
          </div>}

        </div>

      </div>

      <ToastAlert Message={toast.message} Type={toast.type} />
    </>
  );
}

export default InsuranceMainpage;

// # Extract common fields
// PreAuthDate = data.get('PreAuthDate')
// PreAuthAmount = data.get('PreAuthAmount')
// DischargeDate = data.get('DischargeDate')
// FinalBillAmount = data.get('FinalBillAmount')
// RaisedAmount = data.get('RaisedAmount')
// ApprovedAmount = data.get('ApprovedAmount')
// CourierDate = data.get('CourierDate')
// SettlementDateCount = data.get('SettlementDateCount')
// Created_By = data.get('Created_By')
// Status = data.get('Status')
// AmountArray = data.get('AmountArray')

// # Extract nested fields
// insurance_type_data = data.get('insurancetype', {})  # Extract insurancetype as a dictionary
// InsuranceType = insurance_type_data.get('insurancetype')
// PolicyNumber = insurance_type_data.get('policynumber')

// employee_data = data.get('Employee', {})  # Extract Employee as a dictionary
// IsEmployee = employee_data.get('IsEmployee')
// CompanyName = employee_data.get('CompanyName')
// EmployeeID = employee_data.get('Employeeid')
// EmployeeDesignation = employee_data.get('EmployeeDesignation')

// copayment_details = data.get('CoPaymentDetails', {})  # Extract CoPaymentDetails as a dictionary
// CoPaymentType = copayment_details.get('CoPaymentType')
// CoPaymentTypeValue = copayment_details.get('CoPaymentTypeValue')
// CoPaymentBillAmount = copayment_details.get('CoPaymentBillAmount')
// CoPaymentFinalAmount = copayment_details.get('CoPaymentFinalAmount')

// # Print or use the extracted data
// print(f"Insurance Type: {InsuranceType}, Policy Number: {PolicyNumber}")
// print(f"Employee Info: {IsEmployee}, {CompanyName}, {EmployeeID}, {EmployeeDesignation}")
// print(f"CoPayment Details: {CoPaymentType}, {CoPaymentTypeValue}, {CoPaymentBillAmount}, {CoPaymentFinalAmount}")
