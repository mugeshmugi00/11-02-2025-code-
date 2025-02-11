import React, { useState, useEffect } from 'react'
import axios from 'axios';
import { useDispatch, useSelector } from 'react-redux';
import Button from "@mui/material/Button";
import "./op_patients.css";
import CancelIcon from "@mui/icons-material/Cancel";
import UpdateIcon from "@mui/icons-material/Update";
import HighlightOffIcon from "@mui/icons-material/HighlightOff";
import ReactGrid from '../OtherComponent/ReactGrid/ReactGrid';
import ToastAlert from '../OtherComponent/ToastContainer/ToastAlert'
import CheckCircleIcon from '@mui/icons-material/CheckCircle';  // Completed Icon
import LoginIcon from '@mui/icons-material/Login';  // Check-In Icon
import LogoutIcon from '@mui/icons-material/Logout';

const OP_patients = () => {

    const UrlLink = useSelector(state => state.userRecord?.UrlLink);
    const pagewidth = useSelector(state => state.userRecord?.pagewidth);

    const [DoctorNames, setDoctorNames] = useState([]);

    const [PatientRegisterData, setPatientRegisterData] = useState([]);

    console.log("PatientRegisterData", PatientRegisterData);
    const [TotalPatientCount, setTotalPatientCount] = useState(0);

    const [DoctorNameData, setDoctorNameData] = useState([]);
    console.log("DoctorNameData", DoctorNameData)

    const [reshedule, setReshedule] = useState({
        Status: "Reshedule",
        VisitId: '',
        newPatientId: '',
        registrationid: '',
        Reshedulereason: '',
        doctorname: '',
        speciality: '',
        doctorid: ''
    });
    console.log("reshedule", reshedule);


    const formatDate = (date) => {
        const d = new Date(date);
        const month = (d.getMonth() + 1).toString().padStart(2, "0");
        const day = d.getDate().toString().padStart(2, "0");
        const year = d.getFullYear();
        return `${year}-${month}-${day}`;
    };
    const currentdate = formatDate(new Date());
    const [searchOPParams, setSearchOPParams] = useState({
        query: "",
        Doctor: "",
        datetype: "",
        date: "",
        todate: "",
    });

    console.log("searchDoctorParams", searchOPParams);

    const UserData = useSelector((state) => state.userRecord?.UserData);

    useEffect(() => {
        const fetchdat = async () => {

            const postdata = {
                LocationId: UserData?.location,
                Date: formatDate(new Date()),
                Speciality: reshedule?.speciality,
            };
            console.log("Doctrrrrr", postdata);

            try {
                const response = await axios.get(
                    `${UrlLink}Frontoffice/get_available_doctor_by_speciality`,
                    { params: postdata }
                );

                setDoctorNameData(response.data);


            } catch (error) {
                setDoctorNameData([]);
                console.error("Error fetching referral doctors:", error);
            }
        };
        if (reshedule.speciality) {
            fetchdat();
        }
    }, [UrlLink, UserData.location, reshedule?.speciality]);


    const [IsPatientStatusGet, setIsPatientStatusGet] = useState(false);

    const dispatchvalue = useDispatch();

    const toast = useSelector(state => state.userRecord?.toast);

    const [OpenModalCancel, setOpenModalCancel] = useState(false);

    const [cancel, setCancel] = useState({
        Status: "Cancelled",
        VisitId: '',
        newPatientId: '',
        registrationid: '',
        Cancelreason: ''
    });

    const [SpecializationData, setSpecializationData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [specializationResponse] = await Promise.all([
                    axios.get(`${UrlLink}Masters/Speciality_Detials_link`),
                ]);
                setSpecializationData(specializationResponse.data);

            } catch (error) {
                console.error("Error fetching data:", error);
            }
        };
        fetchData();
    }, [UrlLink]);


    const [ShowModalReschedule, setShowModalReschedule] = useState(false);
    useEffect(() => {
        axios.get(`${UrlLink}Masters/get_patient_appointment_details`, { params: searchOPParams })
            .then((res) => {
                const ress = res.data;
                console.log(ress, 'rrrrrrrrrrrrrrrrr');

                if (Array.isArray(ress)) {
                    setPatientRegisterData(ress);
                    setTotalPatientCount(ress[0]?.TotalPatientCount || 0);
                }
                else {
                    setPatientRegisterData([]);
                    setTotalPatientCount(0);
                }
            })
            .catch((err) => {
                console.log(err);
            });
    }, [UrlLink, searchOPParams, IsPatientStatusGet,]);


    useEffect(() => {
        axios.get(`${UrlLink}Masters/get_All_DoctorNames`)
            .then((res) => {
                const ress = res.data;
                console.log("DoctorsNames", ress);
                if (Array.isArray(ress)) {
                    setDoctorNames(ress);
                } else {
                    setDoctorNames([]);
                }
            })
            .catch((err) => {
                console.log(err);
            });
    }, [UrlLink]);



    const handleSearchChange = (e) => {
        const { name, value } = e.target;

        // Handle changes based on the datetype
        if (name === "datetype") {
            if (value === "CurrentDate") {
                setSearchOPParams({
                    ...searchOPParams,
                    datetype: value,
                    date: currentdate, // Set the date to current date
                    todate: "", // Clear todate
                });
            } else if (value === "CustomDate") {
                setSearchOPParams({
                    ...searchOPParams,
                    datetype: value,
                    date: "", // Keep date empty for custom date
                    todate: "", // Keep todate empty as well
                });
            } else {
                setSearchOPParams({
                    ...searchOPParams,
                    datetype: "",
                    date: "",
                    todate: "", // Clear both date and todate if no option selected
                });
            }
        } else {
            setSearchOPParams({
                ...searchOPParams,
                [name]: value,
            });
        }
    };





    const handleColorChangeCheckin = (rowss, color) => {
        const Status = 'InProgress';
        const VisitId = rowss?.VisitId;
        const newPatientId = rowss?.PatientId;
        const registrationid = rowss?.RegistrationId;

        if (VisitId && newPatientId && registrationid) {
            axios
                .post(`${UrlLink}Masters/StatusUpdate_Details_Patient`, {
                    newPatientId,
                    VisitId,
                    Status,
                    registrationid,
                })
                .then((res) => {
                    const resres = res.data;
                    const typp = Object.keys(resres)[0];
                    const mess = Object.values(resres)[0];
                    const tdata = {
                        message: mess,
                        type: typp,
                    };
                    dispatchvalue({ type: "toast", value: tdata });

                    // Update the UI and state
                    setIsPatientStatusGet((prev) => !prev);

                })
                .catch((err) => {
                    console.error("Error updating status:", err);
                    dispatchvalue({
                        type: "toast",
                        value: { message: 'Error updating status', type: 'warn' },
                    });
                });
        } else {
            dispatchvalue({
                type: "toast",
                value: { message: 'PatientID and VisitId are required.', type: 'warn' },
            });
        }
    };





    const handleColorChangeCheckOut = (rowss, color) => {


        const Status = 'CheckOut';
        const VisitId = rowss?.VisitId;
        const newPatientId = rowss?.PatientId;
        const registrationid = rowss?.RegistrationId;



        if (VisitId && newPatientId && Status) {
            axios
                .post(`${UrlLink}Masters/StatusUpdate_Details_Patient`, {
                    newPatientId,
                    VisitId,
                    Status,
                    registrationid,
                })
                .then((res) => {
                    const resres = res.data;
                    console.log("resres", resres);
                    const typp = Object.keys(resres)[0];
                    const mess = Object.values(resres)[0];
                    const tdata = {
                        message: mess,
                        type: typp,
                    };
                    dispatchvalue({ type: "toast", value: tdata });
                    setIsPatientStatusGet((prev) => !prev);

                })
                .catch((err) => {
                    console.error("Error updating status:", err);
                    dispatchvalue({
                        type: "toast",
                        value: { message: 'Error updating status', type: 'warn' },
                    });
                });
        } else {
            const tdata = {
                message: 'PatientID and Visitid not found.',
                type: 'warn',
            };
            dispatchvalue({ type: "toast", value: tdata });
        }
    };

    const handleColorChangeCancel = (rowss) => {
        if (rowss?.VisitId && rowss?.PatientId && rowss?.id) {
            setCancel((prev) => ({
                ...prev,
                VisitId: rowss?.VisitId,
                newPatientId: rowss?.PatientId,
                registrationid: rowss?.RegistrationId,
            }));
            setOpenModalCancel(true);
        }
        else {
            setOpenModalCancel(false);
            const tdata = {
                message: 'PatientID and Visitid not found.',
                type: 'warn',
            };
            dispatchvalue({ type: "toast", value: tdata });
        }

    };

    const handleColorChangeReschedule = (rowss) => {
        console.log("handleColorChangeReschedule", rowss)
        if (rowss?.VisitId && rowss?.PatientId && rowss?.id) {



            setReshedule((prev) => ({
                ...prev,
                VisitId: rowss?.VisitId,
                newPatientId: rowss?.PatientId,
                registrationid: rowss?.RegistrationId,
                speciality: rowss?.Specilization || '',
                doctorname: '',
                doctorid: rowss?.Doctorid || '',
            }));

            const selectedSpeciality = SpecializationData.find(p => p.SpecialityName === reshedule.speciality);
            if (selectedSpeciality) {
                setReshedule(prev => ({ ...prev, speciality: selectedSpeciality.id }));
            }
            setShowModalReschedule(true);
        }
        else {
            setShowModalReschedule(false);
            const tdata = {
                message: 'PatientID and Visitid not found.',
                type: 'warn',
            };
            dispatchvalue({ type: "toast", value: tdata });
        }

    }


    const handleCloseModal = () => {
        setOpenModalCancel(false);
        setShowModalReschedule(false);
    }

    const handleColorChangeCompleted = (rowss, color) => {
        const Status = 'Completed';
        const VisitId = rowss?.VisitId;
        const newPatientId = rowss?.PatientId;
        const registrationid = rowss?.RegistrationId;

        if (VisitId && newPatientId && registrationid) {
            axios
                .post(`${UrlLink}Masters/StatusUpdate_Details_Patient`, {
                    newPatientId,
                    VisitId,
                    Status,
                    registrationid,
                })
                .then((res) => {
                    const resres = res.data;
                    const typp = Object.keys(resres)[0];
                    const mess = Object.values(resres)[0];
                    const tdata = {
                        message: mess,
                        type: typp,
                    };
                    dispatchvalue({ type: "toast", value: tdata });

                    // Update the UI and state
                    setIsPatientStatusGet((prev) => !prev);
                    setPatientRegisterData((prevRows) =>
                        prevRows.map((row) =>
                            row.id === rowss.id ? { ...row, bgColour: color } : row
                        )
                    );
                })
                .catch((err) => {
                    console.error("Error updating status:", err);
                    dispatchvalue({
                        type: "toast",
                        value: { message: 'Error updating status', type: 'warn' },
                    });
                });
        } else {
            dispatchvalue({
                type: "toast",
                value: { message: 'PatientID and VisitId are required.', type: 'warn' },
            });
        }

    }

    const PatientOPRegisterColumns = [
        {
            key: "id",
            name: "S.No",
            frozen: pagewidth > 500 ? true : false
        },

        {
            key: "PatientId",
            name: "Patient Id",
            frozen: pagewidth > 500 ? true : false
        },
        {
            key: "PatientName",
            name: "Patient Name",
            frozen: true,
            renderCell: (params) => {
                let bgColor;
                if (params.row.Status === "InProgress") {
                    bgColor = "#e3ff7e"; // Background color for Inprogress
                } else if (params.row.Status === "CheckOut") {
                    bgColor = "#88e76cfd"; // Background color for CheckOut
                } else if (params.row.Status === "Cancelled") {
                    bgColor = "#f55e5e";
                }
                else if (params.row.Status === "Reshedule") {
                    bgColor = "#c794dffd";
                }
                else if (params.row.Status === "Completed") {
                    bgColor = "#4169E1";
                }
                else {
                    bgColor = "transparent"; // Default background color
                }

                return (
                    <div
                        style={{
                            backgroundColor: bgColor,
                            width: "100%",
                            height: "100%",
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "center",
                            color: "black", // Adjust text color for visibility
                            padding: "4px",
                            borderRadius: "4px",
                            fontWeight: "bold"
                        }}
                    >
                        {params.row.PatientName}
                    </div>
                );
            }
        },
        {
            key: "PhoneNo",
            name: "Phone Number"
        },

        {
            key: "Age",
            name: "Age",
        },
        {
            key: "Gender",
            name: "Gender",
        },
        {
            key: "VisitType",
            name: "Visit Type",
        },

        {
            key: "Status",
            name: "Status",
        },
        {
            key: "DoctorName",
            name: "Doctor Name",
        },
        {
            key: "Action",
            name: "Action",

            renderCell: (params) => (
                <>
                    <div className='actionv'>
                        <Button
                            className="cell_btn"
                            title='CheckIn'
                            onClick={() => handleColorChangeCheckin(params.row)}
                        >
                            <LoginIcon className="check_box_clrr_cancell" />
                        </Button>
                        <Button
                            className="cell_btn"
                            title='CheckOut'
                            onClick={() => handleColorChangeCheckOut(params.row)}
                        >
                            <LogoutIcon className="check_box_clrr_cancell" />
                        </Button>
                        <Button
                            className="cell_btn"
                            title='Completed'
                            onClick={() => handleColorChangeCompleted(params.row)}
                        >
                            <CheckCircleIcon className="check_box_clrr_cancell" />
                        </Button>
                        <Button
                            className="cell_btn"
                            title='Cancel'
                            onClick={() => handleColorChangeCancel(params.row)}
                        >
                            <CancelIcon className="check_box_clrr_cancell" />
                        </Button>
                        <Button
                            className="cell_btn"
                            title='Reshedule'
                            onClick={() => handleColorChangeReschedule(params.row)}
                        >
                            <UpdateIcon className="check_box_clrr_cancell" />
                        </Button>
                    </div>
                </>
            ),
        },

    ]

    const handleCancelOnChange = (e) => {
        const { name, value } = e.target; // Extract name and value

        setCancel((prev) => ({
            ...prev,
            [name]: value, // Dynamically update the relevant state field
        }));
    };




    const handleSaveCancelReason = () => {
        if (cancel.Cancelreason) {
            axios
                .post(`${UrlLink}Masters/StatusUpdate_Details_Patient_Cancel`, cancel)
                .then((res) => {
                    const resres = res.data;
                    console.log("resres", resres);
                    const typp = Object.keys(resres)[0];
                    const mess = Object.values(resres)[0];
                    const tdata = {
                        message: mess,
                        type: typp,
                    };
                    dispatchvalue({ type: "toast", value: tdata });
                    setIsPatientStatusGet((prev) => !prev);
                    handleCloseModal();
                    setCancel({
                        Status: 'Cancel',
                        VisitId: '',
                        newPatientId: '',
                        registrationid: '',
                        Cancelreason: ''

                    });

                })
                .catch((err) => {
                    console.error("Error updating status:", err);
                    dispatchvalue({
                        type: "toast",
                        value: { message: 'Error updating status', type: 'warn' },
                    });
                });
        }
        else {
            dispatchvalue({
                type: "toast",
                value: { message: 'Cancel reason required.', type: 'warn' },
            });
        }
    }

    const handleSpecChange = (e) => {
        const { name, value } = e.target;
        setReshedule((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const handleDocChange = (e) => {
        const { name, value } = e.target;
        setReshedule((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const handleRescheduleSave = () => {
        if (reshedule.Reshedulereason !== "" && reshedule.doctorname !== "") {
            axios
                .post(`${UrlLink}Masters/StatusUpdate_Details_Patient_Reshedule`, reshedule)
                .then((res) => {
                    const resres = res.data;
                    const typp = Object.keys(resres)[0];
                    const mess = Object.values(resres)[0];
                    const tdata = {
                        message: mess,
                        type: typp,
                    };
                    dispatchvalue({ type: "toast", value: tdata });
                    setIsPatientStatusGet((prev) => !prev);
                    handleCloseModal();
                    setReshedule({
                        Status: "Reshedule",
                        VisitId: '',
                        newPatientId: '',
                        registrationid: '',
                        Reshedulereason: '',
                        doctorname: '',
                        speciality: '',
                        doctorid: ''
                    });
                })
                .catch((err) => {
                    console.error("Error updating status:", err);
                    dispatchvalue({
                        type: "toast",
                        value: { message: 'Error updating status', type: 'warn' },
                    });
                })



        }
        else {
            dispatchvalue({
                type: "toast",
                value: { message: 'Reshedule reason and doctorname required.', type: 'warn' },
            });
        }

    }

    return (
        <div className='Main_container_app'>
            <h3>OP PATIENTS LIST</h3>

            <div className='patientcontain1'>
                <div className='action_color_block'>
                    <span style={{ backgroundColor: "#e3ff7e" }}>Checkin </span>
                    <span style={{ backgroundColor: "#88e76cfd" }}>Checkout </span>

                    <span style={{ backgroundColor: "#f55e5e" }}>Cancel</span>
                    <span style={{ backgroundColor: "#c794dffd" }}>Reshedule</span>
                    <span style={{ backgroundColor: "#4169E1" }}>Completed</span>
                </div>

                <div className="search_div_bar">
                    <div className="search_div_bar_inp_1">
                        <label htmlFor="">Search by
                            <span>:</span>
                        </label>
                        <input
                            type="text"
                            name='query'
                            value={searchOPParams.query}
                            placeholder='Search here... '
                            onChange={handleSearchChange}
                        />
                    </div>


                    <div className="search_div_bar_inp_1">
                        <label htmlFor="doctor">Doctor Name<span>:</span></label>
                        <select
                            id=''
                            name='Doctor'
                            value={searchOPParams.Doctor}
                            onChange={handleSearchChange}
                        >
                            <option value="">Select</option> {/* Default option */}
                            {DoctorNames.map((doctor, index) => (
                                <option key={index} value={doctor.id}>
                                    {doctor.ShortName}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div className="search_div_bar_inp_1">
                        <label htmlFor="">Choose Date
                            <span>:</span>
                        </label>
                        <select
                            name="datetype"
                            value={searchOPParams.datetype}
                            onChange={handleSearchChange}
                        >
                            <option value="">Select</option>
                            <option value="CurrentDate">Current Date</option>
                            <option value="CustomDate">Custom Date</option>
                        </select>
                    </div>
                    {searchOPParams.datetype === "CustomDate" && (
                        <>
                            <div className="search_div_bar_inp_1">
                                <label htmlFor="">From Date
                                    <span>:</span>
                                </label>
                                <input
                                    type="date"
                                    name="date"
                                    value={searchOPParams.date}
                                    onChange={handleSearchChange}
                                />
                            </div>
                            <div className="search_div_bar_inp_1">
                                <label htmlFor="">To Date
                                    <span>:</span>
                                </label>
                                <input
                                    type="date"
                                    name="todate"
                                    value={searchOPParams.todate}
                                    onChange={handleSearchChange}
                                />
                            </div>
                        </>
                    )}

                    {/* For Current Date, only show the From Date field */}
                    {searchOPParams.datetype === "CurrentDate" && (
                        <div className="search_div_bar_inp_1">
                            <label htmlFor="">From Date
                                <span>:</span>
                            </label>
                            <input
                                type="date"
                                name="date"
                                value={searchOPParams.date}
                                onChange={handleSearchChange}
                                disabled // Disable the input since it will always be the current date
                            />
                        </div>
                    )}

                    <div className="search_div_bar_inp_1">
                        <label htmlFor="">TotalPatient Count
                            <span>:</span>
                        </label>
                        <input
                            type="number"
                            name='TotalPatientCount'
                            value={TotalPatientCount}
                            style={{ fontWeight: 'bold', fontSize: '20px' }}
                            disabled
                        />

                    </div>



                </div>

                <div className='RegisFormcon_1 jjxjx_'>

                    <ReactGrid columns={PatientOPRegisterColumns} RowData={PatientRegisterData} />
                </div>


            </div>

            {OpenModalCancel && (
                <div className="modal-container" onClick={handleCloseModal}>
                    <div
                        className="App_Cancel_modal"
                        onClick={(e) => e.stopPropagation()}
                    >

                        <div className="common_center_tag">
                            <span>Register Cancel Reason</span>
                        </div>
                        <textarea
                            name="Cancelreason" // Key in the state to update
                            id="Cancelreason" // Identifier for the textarea
                            label="Cancellation Reason" // Informational label (optional)
                            value={cancel.Cancelreason || ""} // Controlled input with fallback
                            onChange={handleCancelOnChange} // Handles state updates
                        />
                        <div className="Main_container_Btn button">
                            <button onClick={handleSaveCancelReason}>Save</button>
                        </div>
                    </div>
                </div>
            )}
            {ShowModalReschedule && (
                <>
                    <div className="modal-container" onClick={handleCloseModal}>
                        <div className="Doc_Cal_modal" onClick={(e) => e.stopPropagation()}>

                            <div className="common_center_tag">
                                <span>Registration Re-Schedule</span>
                            </div>
                            <br></br>
                            <div className='RegisFormcon_1'>
                                <div className="RegisForm_1">
                                    <label htmlFor="Specialization">
                                        Specialization<span>:</span>
                                    </label>
                                    <select
                                        name="speciality"
                                        id="speciality"
                                        value={reshedule.speciality || ""}
                                        onChange={handleSpecChange}
                                    >
                                        <option value="">Select</option>
                                        {SpecializationData.filter((p) => p.Status === "Active").map((p) => (
                                            <option key={p.id} value={p.id}>
                                                {p.SpecialityName}
                                            </option>
                                        ))}
                                    </select>
                                </div>
                                <br></br>

                                <div className="RegisForm_1">
                                    <label htmlFor="DoctorName">
                                        Doctor Name<span>:</span>
                                    </label>
                                    <select
                                        name="doctorname"
                                        id="doctorname"
                                        value={reshedule?.doctorname || ""}
                                        onChange={handleDocChange}
                                    >
                                        <option value="">Select</option>
                                        {Array.isArray(DoctorNameData) &&
                                            DoctorNameData.filter((p) => p.schedule?.[0]?.working === "yes" && reshedule.doctorid !== p.doctor_id).map((p) => (
                                                <option key={p.doctor_id} value={p.doctor_id}>
                                                    {p.doctor_name}
                                                </option>
                                            ))}
                                    </select>
                                </div>
                                <br></br>

                                <div className="RegisForm_1">
                                    <label htmlFor="ChangingReason">
                                        Changing Reason<span>:</span>
                                    </label>
                                    <textarea
                                        name="Reshedulereason"
                                        id="Reshedulereason"
                                        value={reshedule.Reshedulereason || ""}
                                        onChange={(e) =>
                                            setReshedule((prev) => ({
                                                ...prev,
                                                Reshedulereason: e.target.value,
                                            }))
                                        }
                                    />
                                </div>
                            </div>
                            <br></br>
                            <div className="Main_container_Btn button">
                                <button onClick={handleRescheduleSave}>Save</button>
                            </div>
                        </div>
                    </div>

                    <button onClick={handleCloseModal} className="booked_app_btn">
                        <HighlightOffIcon />
                    </button>
                </>
            )}



            <ToastAlert Message={toast.message} Type={toast.type} />



        </div>
    )
}

export default OP_patients

