import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import bgImg2 from "../Assets/bgImg2.jpg";
import AddBoxIcon from "@mui/icons-material/AddBox";
import ToastAlert from "../OtherComponent/ToastContainer/ToastAlert";
import DeleteIcon from "@mui/icons-material/Delete";
import axios from "axios";

const ClientMainpage = () => {

    const toast = useSelector((state) => state.userRecord?.toast);
    const UrlLink = useSelector((state) => state.userRecord?.UrlLink);
    const UserData = useSelector((state) => state.userRecord?.UserData);
    const dispatchvalue = useDispatch();
    const navigate = useNavigate();

    const ClientPatientDetailes = useSelector(state => state.Insurancedata?.ClientPatientDetailes)
    console.log("ClientPatientDetailes", ClientPatientDetailes)

    const [PatientDetails, setPatientDetails] = useState([]);

    const [ClientDetails, setClientDetails] = useState([]);


    useEffect(() => {
        if (ClientPatientDetailes?.RegistrationId && ClientPatientDetailes?.PatientId && ClientPatientDetailes?.PatientServiesType) {
            axios.get(`${UrlLink}Insurance/Insurance_Patient_Details?RegistrationId=${ClientPatientDetailes.RegistrationId}&PatientId=${ClientPatientDetailes.PatientId}&PatientServiesType=${ClientPatientDetailes.PatientServiesType}`)
                .then((res) => {
                    if (Array.isArray(res?.data)) {
                        setPatientDetails(res.data);
                    }
                    else {
                        console.log("Unexpected response format: Expected an array", res.data);
                    }
                })
                .catch((err) => {
                    console.error("Error fetching patient details:", err);
                })
        }

    }, [ClientPatientDetailes, UrlLink])





    useEffect(() => {
        if (ClientPatientDetailes?.ClientId) {
            axios.get(`${UrlLink}Insurance/Client_Details_get?ClientId=${ClientPatientDetailes?.ClientId}`)
                .then((res) => {

                    if (Array.isArray(res?.data)) {
                        console.log("res.dataclient", res.data)
                        setClientDetails(res.data); // Set data only if it is an array
                    } else {
                        console.log("Unexpected response format: Expected an array", res.data);
                    }

                })
                .catch((err) => {
                    console.error("Error fetching insurance details:", err);
                });
        }

    }, [ClientPatientDetailes, UrlLink])






    const [ClientMaindata, setClientMaindata] = useState({
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
    const [AmountState, setAmountState] = useState({
        SettlementDate: '',
        SettlementAmount: '',
        UTRNumber: '',
    })
    const [AmountArray, setAmountArray] = useState([])

    const [CoPaymentCoverage, setCoPaymentCoverage] = useState("No");

    const [CoPaymentDetails, setCoPaymentDetails] = useState({
        CoPaymentType: '',
        CoPaymentTypeValue: '',
        CoPaymentBillAmount: '',
        CoPaymentFinalAmount: '',
    })

    // useEffect(() => {

    //     axios.get(`${UrlLink}Insurance/Post_Client_Patient_Detailes?GetId=${ClientPatientDetailes?.id}`)
    //         .then((res) => {
    //             console.log('8888800', res.data);

    //             let getdata = res.data

    //             if (getdata && Object.keys(getdata).length > 0) {

    //                 let { AmountArray, CoPaymentCoverage, CoPaymentType, CoPaymentTypeValue, CoPaymentBillAmount, CoPaymentFinalAmount, ...rest } = getdata;
    //                 setAmountArray(AmountArray || [])
    //                 setClientMaindata({ ...rest })
    //                 setCoPaymentCoverage(CoPaymentCoverage || 'No')
    //                 setCoPaymentDetails({
    //                     CoPaymentType: CoPaymentType || '',
    //                     CoPaymentTypeValue: CoPaymentTypeValue || '',
    //                     CoPaymentBillAmount: CoPaymentBillAmount || '',
    //                     CoPaymentFinalAmount: CoPaymentFinalAmount || ''
    //                 });

    //             }


    //         })
    //         .catch((err) => {
    //             console.log(err);
    //         })

    // }, [ClientPatientDetailes, UrlLink])

    useEffect(() => {
        const fetchClientPatientDetails = async () => {
            try {
                if (!ClientPatientDetailes?.id) return;

                const response = await axios.get(`${UrlLink}Insurance/Post_Client_Patient_Detailes?GetId=${ClientPatientDetailes.id}`);
                const data = response.data;
                console.log('Fetched client patient details:', data);

                if (data && Object.keys(data).length > 0) {
                    const {
                        AmountArray = [],
                        CoPaymentCoverage = 'No',
                        CoPaymentType = '',
                        CoPaymentTypeValue = '',
                        CoPaymentBillAmount = '',
                        CoPaymentFinalAmount = '',
                        ...rest
                    } = data;

                    setAmountArray(AmountArray);
                    setClientMaindata(rest);
                    setCoPaymentCoverage(CoPaymentCoverage || 'No');
                    setCoPaymentDetails({
                        CoPaymentType,
                        CoPaymentTypeValue,
                        CoPaymentBillAmount,
                        CoPaymentFinalAmount,
                    });
                }
            } catch (error) {
                console.log('Error fetching client patient details:');
            }
        };

        fetchClientPatientDetails();
    }, [ClientPatientDetailes?.id, UrlLink]);

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
                setClientMaindata((prev) => ({
                    ...prev,
                    [name]: value,
                }))
            }
            else if (value === '') {
                setClientMaindata((prev) => ({
                    ...prev,
                    [name]: value,
                    TdsAmount: '',
                    FinalSettlementAmount: ''
                }))
            }
        }
        else if (name === 'TdsPercentage') {
            if (value !== '') {
                setClientMaindata((prev) => ({
                    ...prev,
                    [name]: value,
                }))
            }
            else if (value === '') {
                setClientMaindata((prev) => ({
                    ...prev,
                    [name]: value,
                    TdsAmount: '',
                    FinalSettlementAmount: ''
                }))
            }
        }
        else {
            setClientMaindata((prev) => ({
                ...prev,
                [name]: value,
            }))
        }


    }

    useEffect(() => {
        const { ApprovedAmount} = ClientMaindata;

        const approvedAmount = parseFloat(ApprovedAmount) || 0;
        const tdsPercentage = parseFloat(10) || 0;

        let tdsAmount = 0; // Initialize as a number
        let finalSettlementAmount = 0; // Initialize as a number

        if (approvedAmount > 0 && tdsPercentage > 0) {
            tdsAmount = (approvedAmount * tdsPercentage) / 100;
            finalSettlementAmount = approvedAmount - tdsAmount;
        }

        setClientMaindata((prev) => ({
            ...prev,
            TdsPercentage:tdsPercentage,
            TdsAmount: tdsAmount.toFixed(2),  // Format as string with two decimal places
            FinalSettlementAmount: finalSettlementAmount.toFixed(2),
        }));
    }, [ClientMaindata.ApprovedAmount]);


    const handelOnchageAmountState = (e) => {

        const { name, value } = e.target

        setAmountState((prev) => ({
            ...prev,
            [name]: value,
        }))

    }

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
        else {
            setCoPaymentCoverage(value);
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



    const HandelDeleteAmount = (id) => {

        let RemoveData = AmountArray.filter((ele) => ele.id !== id);

        RemoveData = RemoveData.map((ele, ind) => {
            return { ...ele, id: ind + 1 };
        })

        setAmountArray(RemoveData)

    };



    const SaveClientRais = (status) => {


        const SubPostFun = (status) => {
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

            let params = {
                TableId: ClientPatientDetailes?.id,
                ...ClientMaindata,
                CoPaymentCoverage: CoPaymentCoverage,
                CoPaymentDetails: { ...CoPaymentDetails },
                AmountArray: AmountArray,
                Created_By: UserData?.username,
                Status: status || '',
            }

            console.log('Sending params:', params);

            axios.post(`${UrlLink}Insurance/Post_Client_Patient_Detailes`, params)
                .then((res) => {
                    console.log(res.data);

                    let resdata = res.data
                    let type = Object.keys(resdata)[0]
                    let mess = Object.values(resdata)[0]
                    const tdata = {
                        message: mess,
                        type: type,
                    }
                    dispatchvalue({ type: 'toast', value: tdata });
                    if (type === 'success') {
                        navigate('/Home/ClientDashboard');
                    }
                })
                .catch((err) => {
                    console.log(err);
                })
        }



        if (status) {
            let ConformStatus = window.confirm("Are you sure you want to change the status to 'Completed'? Once the status is 'Completed,' it cannot be edited.")
            if (ConformStatus) {
                SubPostFun(status)
            }

        } else {
            SubPostFun()
        }

    }



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
                                    {ClientPatientDetailes?.PatientId}
                                </span>
                            </div>
                            <div className="RegisForm_1 ">
                                <label htmlFor="PatientName">
                                    Patient Name <span>:</span>{" "}
                                </label>
                                <span className="dctr_wrbvh_pice" htmlFor="PatientName">
                                    {ClientPatientDetailes?.PatientName}

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
                                    {ClientPatientDetailes?.RegistrationId}
                                </span>
                            </div>


                        </div>
                    </div>

                </div>
                <br />

                <div className="RegisFormcon_1">
                    <div className="RegisForm_1">
                        <label htmlFor="ClientName">
                            Client Name<span>:</span>
                        </label>
                        <span className="dctr_wrbvh_pice" id="InsuranceName">
                            {Array.isArray(ClientDetails) && ClientDetails.length > 0
                                ? `${ClientDetails[0]?.Client_Name || ""}`
                                : ""}
                        </span>
                    </div>
                    <div className="RegisForm_1">
                        <label htmlFor="ContactPerson">
                            Contact Person<span>:</span>
                        </label>
                        <span className="dctr_wrbvh_pice" id="InsuranceName">
                            {Array.isArray(ClientDetails) && ClientDetails.length > 0
                                ? `${ClientDetails[0]?.ContactPerson || ""}`
                                : ""}
                        </span>
                    </div>

                    <div className="RegisForm_1">
                        <label htmlFor="PhoneNumber">
                            Phone Number<span>:</span>
                        </label>
                        <span className="dctr_wrbvh_pice" id="InsuranceName">
                            {Array.isArray(ClientDetails) && ClientDetails.length > 0
                                ? `${ClientDetails[0]?.PhoneNumber || ""}`
                                : ""}
                        </span>
                    </div>
                    <div className="RegisForm_1">
                        <label htmlFor="MailId">
                            MailId<span>:</span>
                        </label>
                        <span className="dctr_wrbvh_pice" id="InsuranceName">
                            {Array.isArray(ClientDetails) && ClientDetails.length > 0
                                ? `${ClientDetails[0]?.MailId || ""}`
                                : ""}
                        </span>
                    </div>
                </div>

                <br />

                <div className="RegisForm_1">

                    <label>
                        CoPayment ? <span>:</span>
                    </label>

                    <div className="ewj_i87_head">
                        <div className="ewj_i87">
                            <input
                                type="radio"
                                id="CoPaymentYes"
                                name="CoPayment"
                                value="Yes"
                                checked={CoPaymentCoverage === "Yes"}
                                onChange={handleCheckboxCoPayment}
                            ></input>

                            <label htmlFor="CoPaymentYes">Yes</label>
                        </div>

                        <div className="ewj_i87">
                            <input
                                type="radio"
                                id="CoPaymentNo"
                                name="CoPayment"
                                value="No"
                                checked={CoPaymentCoverage === "No"}
                                onChange={handleCheckboxCoPayment}
                            ></input>
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
                            value={ClientMaindata.PreAuthDate}
                            onChange={HandelOnchangeState}
                        />

                    </div>


                    <div className="RegisForm_1">


                        <label>PreAuth Amount<span>:</span></label>
                        <input
                            type='number'
                            name='PreAuthAmount'
                            value={ClientMaindata.PreAuthAmount}
                            onChange={HandelOnchangeState}
                        />

                    </div>

                    <div className="RegisForm_1">


                        <label>Discharge Date<span>:</span></label>
                        <input
                            type='date'
                            name='DischargeDate'
                            value={ClientMaindata.DischargeDate}
                            onChange={HandelOnchangeState}
                        />

                    </div>

                    <div className="RegisForm_1">


                        <label>Final Bill Amount<span>:</span></label>
                        <input
                            type='number'
                            name='FinalBillAmount'
                            value={ClientMaindata.FinalBillAmount}
                            onChange={HandelOnchangeState}
                        />

                    </div>

                    <div className="RegisForm_1">


                        <label>Raised Amount<span>:</span></label>
                        <input
                            type='number'
                            name='RaisedAmount'
                            value={ClientMaindata.RaisedAmount}
                            onChange={HandelOnchangeState}
                        />

                    </div>

                    <div className="RegisForm_1">


                        <label>Approved Amount<span>:</span></label>
                        <input
                            type='number'
                            name='ApprovedAmount'
                            value={ClientMaindata.ApprovedAmount}
                            onChange={HandelOnchangeState}
                        />

                    </div>
                    <div className="RegisForm_1">
                        <label>TDS %<span>:</span></label>
                        <input
                            name='TdsPercentage'
                            value={ClientMaindata.TdsPercentage}
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
                            value={ClientMaindata.TdsAmount}
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
                            value={ClientMaindata.FinalSettlementAmount}
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
                            value={ClientMaindata.CourierDate}
                            onChange={HandelOnchangeState}
                        />

                    </div>


                    <div className="RegisForm_1">


                        <label>Settlement Date Count<span>:</span></label>
                        <input
                            type='number'
                            name='SettlementDateCount'
                            value={ClientMaindata.SettlementDateCount}
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
                        <button onClick={() => SaveClientRais('')}>
                            Save
                        </button>
                    </div>


                    {AmountArray.length !== 0 && <div className="Main_container_Btn">
                        <button onClick={() => SaveClientRais('COMPLETED')}>
                            Compleate
                        </button>
                    </div>}

                </div>

            </div>

            <ToastAlert Message={toast.message} Type={toast.type} />
        </>
    )
}

export default ClientMainpage;


