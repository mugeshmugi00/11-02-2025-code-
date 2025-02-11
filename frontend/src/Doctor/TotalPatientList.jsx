import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import ReactGrid from '../OtherComponent/ReactGrid/ReactGrid';
import Button from "@mui/material/Button";
import EditIcon from "@mui/icons-material/Edit";
import { useNavigate } from 'react-router-dom';
import Diversity1Icon from "@mui/icons-material/Diversity1";
import PersonIcon from "@mui/icons-material/Person";
import PersonAddAlt1Icon from "@mui/icons-material/PersonAddAlt1";
// import './Patient.css';
import '../PatientManagement/Patient.css';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';



const TotalPatientList = () => {
    const UrlLink = useSelector(state => state.userRecord?.UrlLink);
    const pagewidth = useSelector(state => state.userRecord?.pagewidth);
    const navigate = useNavigate();
    const dispatchvalue = useDispatch();

    const [IpPatientCount, setIpPatientCount] = useState(0);
    const [OpPatientCount, setOpPatientCount] = useState(0);
    const [CasualityPatientCount, setCasualityPatientCount] = useState(0);
    const [WardPatientCount, setWardPatientCount] = useState(0);
    
    const [Flag, setFlag] = useState(0);
    const [isHost, setIsHost] = useState(false);

    console.log(Flag,'Flaggggggg');
    console.log(isHost,'isHost');
    

    // ------------OP-----------------------
    const UserData = useSelector(state => state.userRecord?.UserData)

    const [searchOPParams, setsearchOPParams] = useState({ query: '', status: 'Registered', DoctorId: UserData?.Doctor });
    // const [searchOPParams, setsearchOPParams] = useState({ query: '', status: 'Pending' });
    const [searchDoctorParams, setsearchDoctorParams] = useState({Doctor:'',DoctorId: UserData?.Doctor,status: 'Registered' });
    console.log("123",searchDoctorParams);
    console.log("1111111111",searchOPParams);
    const [PatientRegisterData, setPatientRegisterData] = useState([]);
    console.log(PatientRegisterData,'PatientRegisterData');
    
    
    const [DocWisePatientRegisterData, setDocWisePatientRegisterData] = useState([]);

    const [DoctorNames, setDoctorNames] = useState([]);
    const [DepartmentData, setDepartmentData] = useState([]);
    console.log(DepartmentData,'DepartmentData');
    
    const [isSelected, setIsSelected] = useState('OP');

    const [showTooltip, setShowTooltip] = useState(null);
    const [hoveredFlagIndex, setHoveredFlagIndex] = useState(null);
    const [showTooltip2, setShowTooltip2] = useState(false);

    console.log(UserData,'UserData');
    

    // const [showTooltip, setShowTooltip] = useState(false);

    // const [isIPSelected, setIsIPSelected] = useState(false);

    // const handleOPClick = () => setIsOPSelected(1);
    // const handleIPClick = () => setIsIPSelected(true);

    // ------------IP-----------------------
   
    const [searchIPParams, setsearchIPParams] = useState({
        query: '',
        status: 'Admitted',
        type: 'IP',
        DoctorId: UserData?.Doctor,
        // SelectedWard : SelectedWard
    });

    const [IpPatientRegisterData, setIpPatientRegisterData] = useState([])
    console.log(IpPatientRegisterData,'IpPatientRegisterData');
    
    const [WardGet,setWardGet] = useState([])
 
    const [SelectedWard, setSelectedWard] = useState('');
    console.log(SelectedWard,'SelectedWard');


   

    
    // ------------Casuality-----------------------

    const [SearchCasualityParams, setSearchCasualityParams] = useState({
        query: '',
        status: 'Pending',
        type: 'Casuality' 
        });

    const [CasualityPatientRegisterData, setCasualityPatientRegisterData] = useState([])


    //==========================================================================
    
    const [SearchEmergencyParams, setSearchEmergencyParams] = useState({
        query: '',
        status: 'Admitted',
        type: 'Casuality' 
        });

    const [EmergencyPatientRegisterData, setEmergencyPatientRegisterData] = useState([])

    
    //==========================================================================
    
    // ------------OP-----------------------

   
    useEffect(() => {
        console.log(searchOPParams,'searchOPParams');
        

            axios.get(`${UrlLink}Frontoffice/get_patient_appointment_details_withoutcancelled`, { params: searchOPParams })
            .then((res) => {
                const ress = res.data;
                console.log("OPpppppppppppppp",ress);
                if (Array.isArray(ress)) {
                    setPatientRegisterData(ress);
                } else {
                    setPatientRegisterData([]);
                }
            })
            .catch((err) => {
                console.log(err);
            });
        
        
    }, [UrlLink, searchOPParams,UserData]);




    
    useEffect(() => {
       
            axios.get(`${UrlLink}Frontoffice/get_patient_appointment_details_specifydoctor`, { params: searchDoctorParams })
                .then((res) => {
                    const ress = res.data;
                    console.log(ress,'rrrrrrrrrrrrrrrrr');
                    
                    if (Array.isArray(ress)) {
                        setPatientRegisterData(ress);
                    } 
                    else {
                        setPatientRegisterData([]);
                    }
                })
                .catch((err) => {
                    console.log(err);
                });
        
    }, [UrlLink, searchDoctorParams,UserData]);


    useEffect(() => {
        axios.get(`${UrlLink}Masters/get_All_DoctorNames`)
            .then((res) => {
                const ress = res.data;
                console.log("DoctorsNames",ress);
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


    const handleeditOPPatientRegister = (params) => {
        console.log('params',params)
        const { RegistrationId } = params;
        axios.get(`${UrlLink}OP/get_workbenchquelist_doctor`, { params: { RegistrationId: RegistrationId, Type: 'OP' } })
            .then((res) => {
                console.log(res,'OPpppppppppppppp');
                dispatchvalue({ type: 'DoctorWorkbenchNavigation', value: { ...res.data } });
                dispatchvalue({type:'SpecialityWise_DoctorWorkbenchNavigation', value: {}})
               
                navigate('/Home/DoctorFolder');
                dispatchvalue({ type: 'HrFolder', value:'DoctorWorkbenchNavigation'});
                dispatchvalue({ type: "setPreviousFolder", value: null }); 
                dispatchvalue({ type: "showMenu", value: true });
            })
            .catch((err) => {
                console.log(err);
            })

    }

    // const handleeditOPPatientRegister = (params) => {
    //     const { RegistrationId } = params;
    //     axios.get(`${UrlLink}OP/get_workbenchquelist_doctor`, { params: { RegistrationId, Type: 'OP' } })
    //         .then((res) => {
    //             console.log(res.data,'iiiiiiii');
    //             if(res.data && Object.keys(res.data).length!==0){

    //             dispatchvalue({ type: 'DoctorWorkbenchNavigation', value: res.data });
    //             console.log('ooooooooooooooooo',res.data)
    //             navigate('/Home/DoctorWorkbenchNavigation');
    //             }
    //         })
    //         .catch((err) => {
    //             console.log(err);
    //         });
    // };


    const handleSearchChange = (e) => {
        const { name, value } = e.target

        setsearchOPParams({ ...searchOPParams, [name]: value });


    };


    const handleDoctorSearch = (e) => {
        const { name, value } = e.target;
        console.log("Selected Doctor ID:", value);
      
        // Update searchDoctorParams state with the selected doctor ID
        setsearchDoctorParams({ ...searchDoctorParams, [name]: value });
      
      };


      const PatientOPRegisterColumns = [
        {
            key: "id",
            name: "S.No",
            frozen: pagewidth > 500 ? true : false
        },
       {
            key: "FlaggingColour",
            name: "Flagging Colour",
            frozen: true,
            renderCell: (params) => (
                <div
                    style={{
                        backgroundColor: params.row.FlaggingColour || "transparent",
                        width: "20px",
                        height: "20px",
                        cursor: "pointer",
                        position: "relative",
                    }}
                    onMouseEnter={() => setShowTooltip(params.row.id)} // Show tooltip for this row
                    onMouseLeave={() => setShowTooltip(null)} // Hide tooltip
                >
                    {/* <h4>{params.row.Flagging ? params.row.Flagging : "N/A"}</h4> */}

                    {/* Conditional rendering of the tooltip */}
                    {showTooltip === params.row.id && (
                        <div
                            style={{
                                position: "absolute",
                                top: "-15px",
                                left: "50%",
                                transform: "translateX(-50%)",
                                backgroundColor: "#d2cdd4",
                                color: "#000",
                                padding: "5px 10px",
                                borderRadius: "4px",
                                fontSize: "12px",
                                whiteSpace: "nowrap",
                                
                            }}
                        >
                            {params.row.Flagging ? params.row.Flagging : "N/A"}
                        </div>
                    )}
                </div>
            ),
        },
        
        {
            key: "PatientId",
            name: "Patient Id",
            frozen: pagewidth > 500 ? true : false
        },
        {
            key: "PatientName",
            name: "Patient Name",
            width: 200,
            frozen:  true 
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
            key: "PhoneNo",
            name: "PhoneNo",
        },
        {
            key: "Complaint",
            name: "Complaint",
        },
        // {
        //     key: "VisitId",
        //     name: "VisitId",
        // },
        // {
        //     key: "isMLC",
        //     name: "isMLC",
            
        // },
        // {
        //     key: "isRefferal",
        //     name: "isRefferal",
        // },
        // {
        //     key: "Status",
        //     name: "Status",
        // },
        {
            key: "Specilization",
            name: "Specilization",
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
                    <Button
                        className="cell_btn"
                        onClick={() => handleeditOPPatientRegister(params.row)}
                    >
                        <ArrowForwardIcon className="check_box_clrr_cancell" />
                    </Button>
                </>
            ),
        },
    ]


    // ------------IP-----------------------


    useEffect(() => {
        axios.get(`${UrlLink}Masters/Ward_Detials_link`)
            .then((res) => {
                const ress = res.data;
                console.log("Roommmmmmmmm",ress);
                if (Array.isArray(ress)) {
                    setWardGet(ress);
                } else {
                    setWardGet([]);
                }
            })
            .catch((err) => {
                console.log(err);
            });
    }, [UrlLink]);



    useEffect(() => {
        const fetchData = async () => {
            try {
                let response;
                console.log(searchIPParams,'searchIPParams');
                

                // Fetch IP data or Casuality data based on the 'type' in searchIPParams
                if (searchIPParams.type === 'IP') {
                    response = await axios.get(`${UrlLink}Frontoffice/get_ip_Patient_registration_details_for_workbench`, { params: searchIPParams });
                } 
                // else if (searchIPParams.type === 'Casuality') {
                //     response = await axios.get(`${UrlLink}Frontoffice/get_patient_casuality_details`, { params: searchIPParams });
                // }

                const data = response.data;
                console.log(data,'dataaaaaaaaaaaa');
                

                // Check if the response is an array
                if (Array.isArray(data)) {
                    setIpPatientRegisterData(data);
                } else {
                    setIpPatientRegisterData([]);
                }
            } catch (err) {
                console.log(err);
            }
        };

        fetchData();
    }, [UrlLink, searchIPParams]); 



    const handleIPTypeChange = (e) => {
        const newType = e.target.value;
        // Determine the new status based on the selected type
        const newStatus = newType === 'Casuality' ? 'Pending' : 'Admitted';

        // Update both type and status in state
        setsearchIPParams({ ...searchIPParams, type: newType, status: newStatus });
    };

    const handleeditIPPatientRegister = (params, type) => {
        console.log('params', params);
        const { RegistrationId } = params;

        const requestType = type || searchIPParams.type; // Use selected type or fallback to default

        axios.get(`${UrlLink}OP/get_workbenchquelist_doctor`, { params: { RegistrationId, Type: requestType } })
            .then((res) => {
                console.log(res);
                dispatchvalue({ type: 'IP_DoctorWorkbenchNavigation', value: { ...res.data, ...params,RequestType:requestType } });
                navigate('/Home/DoctorFolder');
                dispatchvalue({ type: 'HrFolder', value:'IP_DoctorWorkbenchNavigation'});
            })
            .catch((err) => {
                console.log(err);
            });
    };

    const handleIPSearchChange = (e) => {
        const { name, value } = e.target

        setsearchIPParams({ ...searchIPParams, [name]: value });
        if (name === "Ward") {
            setSelectedWard(value);
        }
    };

    

    const PatientIPRegisterColumns = [
        {
            key: "id",
            name: "S.No",
            frozen: pagewidth > 500 ? true : false
        },
        {
            key: "FlaggingColour",
            name: "Flagging Colour",
            frozen: true,
            renderCell: (params) => (
                <div
                    style={{
                        backgroundColor: params.row.FlaggingColour || "transparent",
                        width: "20px",
                        height: "20px",
                        cursor: "pointer",
                        position: "relative",
                    }}
                    onMouseEnter={() => setShowTooltip(params.row.id)} // Show tooltip for this row
                    onMouseLeave={() => setShowTooltip(null)} // Hide tooltip
                >
                    {/* <h4>{params.row.Flagging ? params.row.Flagging : "N/A"}</h4> */}

                    {/* Conditional rendering of the tooltip */}
                    {showTooltip === params.row.id && (
                        <div
                            style={{
                                position: "absolute",
                                top: "-15px",
                                left: "50%",
                                transform: "translateX(-50%)",
                                backgroundColor: "#d2cdd4",
                                color: "#000",
                                padding: "5px 10px",
                                borderRadius: "4px",
                                fontSize: "12px",
                                whiteSpace: "nowrap",
                                
                            }}
                        >
                            {params.row.Flagging ? params.row.Flagging : "N/A"}
                        </div>
                    )}
                </div>
            ),
        },
        {
            key: "PatientId",
            name: "Patient Id",
            frozen: pagewidth > 500 ? true : false
        },
        {
            key: "PatientName",
            name: "Patient Name",
            width: 200,
            frozen: pagewidth > 500 ? true : false
        },
        {
            key: "Age",
            name: "Age",
        },
        {
            key: "Gender",
            name: "Gender",
        },

        // {
        //     key: "WardName",
        //     name: "WardName",
        //     width :200,
        // },

        {
            key: "PhoneNo",
            name: "PhoneNo",
        },
       
        {
            key: "Complaint",
            name: "Complaint",
        },
        // {
        //     key: "isMLC",
        //     name: "isMLC",
            
        // },
        // {
        //     key: "isRefferal",
        //     name: "isRefferal",
        // },
        // {
        //     key: "Status",
        //     name: "Status",
        // },
        // {
        //     key: "Specilization",
        //     name: "Specilization",
        // },
        {
            key: "DoctorName",
            name: "Doctor Name",
        },
        {
            key: "Action",
            name: "Action",
            renderCell: (params) => (
                (params.row.Status === 'Admitted' || params.row.Status === 'Pending') ? (
                    <Button
                        className="cell_btn"
                        onClick={() => handleeditIPPatientRegister(params.row, searchIPParams.type)} // Use selected type
                    >
                        <ArrowForwardIcon className="check_box_clrr_cancell" />
                    </Button>
                ) : (
                    '-'
                )
            ),
        }
    ]


    // ------------Casuality-----------------------

    useEffect(() => {
        const fetchData = async () => {
            try {
                let response;

                // Fetch IP data or Casuality data based on the 'type' in searchIPParams
                if (SearchCasualityParams.type === 'Casuality') {
                    response = await axios.get(`${UrlLink}Frontoffice/get_patient_casuality_details`, { params: SearchCasualityParams });
                }

                const data = response.data;
                console.log(data,'dataaaaaa');
                

                // Check if the response is an array
                if (Array.isArray(data)) {
                    setCasualityPatientRegisterData(data);
                } else {
                    setCasualityPatientRegisterData([]);
                }
            } catch (err) {
                console.log(err);
            }
        };

        fetchData();
    }, [UrlLink, SearchCasualityParams]); 

    // const handleCasualityTypeChange = (e) => {
    //     const { name, value } = e.target

    //     setSearchCasualityParams({ ...searchOPParams, [name]: value });

    // };

    const handleCasualityTypeChange = (e) => {
        const newType = e.target.value;
        // Determine the new status based on the selected type
        const newStatus = newType === 'Casuality' ? 'Pending' : 'Admitted';

        // Update both type and status in state
        setsearchIPParams({ ...searchIPParams, type: newType, status: newStatus });
    };



    const handleeditCasualityPatientRegister = (params, type) => {
        console.log('params', params);
        const { RegistrationId } = params;

        const requestType = type || SearchCasualityParams.type; // Use selected type or fallback to default

        axios.get(`${UrlLink}OP/get_workbenchquelist_doctor`, { params: { RegistrationId, Type: requestType } })
            .then((res) => {
                console.log(res);
                dispatchvalue({ type: 'IP_DoctorWorkbenchNavigation', value: { ...res.data, ...params,RequestType:requestType } });
                navigate('/Home/DoctorFolder');
                dispatchvalue({ type: 'HrFolder', value:'IP_DoctorWorkbenchNavigation'});
            })      
            .catch((err) => {
                console.log(err);
            });
    };


    const handleCasualitySearchChange = (e) => {
        const { name, value } = e.target

        setSearchCasualityParams({ ...SearchCasualityParams, [name]: value });

    };

    const PatientCasualityRegisterColumns = [
        {
            key: "id",
            name: "S.No",
            frozen: pagewidth > 500 ? true : false
        },
        {
            key: "FlaggingColour",
            name: "Flagging Colour",
            frozen: true,
            renderCell: (params) => (
                <div
                    style={{
                        backgroundColor: params.row.FlaggingColour || "transparent",
                        width: "20px",
                        height: "20px",
                        cursor: "pointer",
                        position: "relative",
                    }}
                    onMouseEnter={() => setShowTooltip(params.row.id)} // Show tooltip for this row
                    onMouseLeave={() => setShowTooltip(null)} // Hide tooltip
                >
                    {/* <h4>{params.row.Flagging ? params.row.Flagging : "N/A"}</h4> */}

                    {/* Conditional rendering of the tooltip */}
                    {showTooltip === params.row.id && (
                        <div
                            style={{
                                position: "absolute",
                                top: "-15px",
                                left: "50%",
                                transform: "translateX(-50%)",
                                backgroundColor: "#d2cdd4",
                                color: "#000",
                                padding: "5px 10px",
                                borderRadius: "4px",
                                fontSize: "12px",
                                whiteSpace: "nowrap",
                                
                            }}
                        >
                            {params.row.Flagging ? params.row.Flagging : "N/A"}
                        </div>
                    )}
                </div>
            ),
        },
        {
            key: "PatientId",
            name: "Patient Id",
            frozen: pagewidth > 500 ? true : false
        },
        {
            key: "PatientName",
            name: "Patient Name",
            width: 150,
            frozen: pagewidth > 500 ? true : false
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
            key: "PhoneNo",
            name: "PhoneNo",
        },
      
       
        {
            key: "Complaint",
            name: "Complaint",
        },
        // {
        //     key: "isMLC",
        //     name: "isMLC",
          
        // },
        // {
        //     key: "isRefferal",
        //     name: "isRefferal",
        // },
        // {
        //     key: "Status",
        //     name: "Status",
        // },
        // {
        //     key: "Specilization",
        //     name: "Specilization",
        // },
        // {
        //     key: "DoctorName",
        //     name: "Doctor Name",
        // },
        {
            key: "Action",
            name: "Action",
            renderCell: (params) => (
                (params.row.Status === 'Pending') ? (
                    <Button
                        className="cell_btn"
                        onClick={() => handleeditCasualityPatientRegister(params.row, SearchCasualityParams.type)} // Use selected type
                    >
                        <ArrowForwardIcon className="check_box_clrr_cancell" />
                    </Button>
                ) : (
                    '-'
                )
            ),
        }
    ]


    // ------------Emergency-----------------------

    useEffect(() => {
        const fetchData = async () => {
            try {
                let response;

                // Fetch IP data or Casuality data based on the 'type' in searchIPParams
                if (SearchEmergencyParams.type === 'Casuality') {
                    response = await axios.get(`${UrlLink}Frontoffice/get_Emergency_patient_details_for_Quelist`, { params: SearchEmergencyParams });
                }

                const data = response.data;
                console.log(data,'dataaaaaa');
                

                // Check if the response is an array
                if (Array.isArray(data)) {
                    setEmergencyPatientRegisterData(data);
                } else {
                    setEmergencyPatientRegisterData([]);
                }
            } catch (err) {
                console.log(err);
            }
        };

        fetchData();
    }, [UrlLink, SearchEmergencyParams]); 

    const handleeditEmergencyPatientRegister = (params, type) => {
        console.log('params', params);
        const { RegistrationId } = params;

        const requestType = type || SearchCasualityParams.type; // Use selected type or fallback to default

        axios.get(`${UrlLink}OP/get_workbenchquelist_doctor`, { params: { RegistrationId, Type: requestType } })
            .then((res) => {
                console.log(res);
                dispatchvalue({ type: 'IP_DoctorWorkbenchNavigation', value: { ...res.data, ...params,RequestType:requestType } });
                navigate('/Home/DoctorFolder');
                dispatchvalue({ type: 'HrFolder', value:'IP_DoctorWorkbenchNavigation'});
            })
            .catch((err) => {
                console.log(err);
            });
    };


    const handleEmergencySearchChange = (e) => {
        const { name, value } = e.target

        setSearchEmergencyParams({ ...SearchCasualityParams, [name]: value });

    };

    const PatientEmergencyRegisterColumns = [
        {
            key: "id",
            name: "S.No",
            frozen: pagewidth > 500 ? true : false
        },
        {
            key: "FlaggingColour",
            name: "Flagging Colour",
            frozen: true,
            renderCell: (params) => (
                <div
                    style={{
                        backgroundColor: params.row.FlaggingColour || "transparent",
                        width: "20px",
                        height: "20px",
                        cursor: "pointer",
                        position: "relative",
                    }}
                    onMouseEnter={() => setShowTooltip(params.row.id)} // Show tooltip for this row
                    onMouseLeave={() => setShowTooltip(null)} // Hide tooltip
                >
                    {/* <h4>{params.row.Flagging ? params.row.Flagging : "N/A"}</h4> */}

                    {/* Conditional rendering of the tooltip */}
                    {showTooltip === params.row.id && (
                        <div
                            style={{
                                position: "absolute",
                                top: "-15px",
                                left: "50%",
                                transform: "translateX(-50%)",
                                backgroundColor: "#d2cdd4",
                                color: "#000",
                                padding: "5px 10px",
                                borderRadius: "4px",
                                fontSize: "12px",
                                whiteSpace: "nowrap",
                                
                            }}
                        >
                            {params.row.Flagging ? params.row.Flagging : "N/A"}
                        </div>
                    )}
                </div>
            ),
        },
        {
            key: "PatientId",
            name: "Patient Id",
            frozen: pagewidth > 500 ? true : false
        },
        {
            key: "PatientName",
            name: "Patient Name",
            width: 150,
            frozen: pagewidth > 500 ? true : false
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
            key: "PhoneNo",
            name: "PhoneNo",
        },
      
       
        {
            key: "Complaint",
            name: "Complaint",
        },
       
        {
            key: "Action",
            name: "Action",
            renderCell: (params) => (
                (params.row.Status === 'Admitted') ? (
                    <Button
                        className="cell_btn"
                        onClick={() => handleeditEmergencyPatientRegister(params.row, SearchEmergencyParams.type)} // Use selected type
                    >
                        <ArrowForwardIcon className="check_box_clrr_cancell" />
                    </Button>
                ) : (
                    '-'
                )
            ),
        }
    ]


    const addSerialNumbers = (data) => {
        return data.map((item, index) => ({
            ...item,
            id: index + 1  // Assigns a unique id starting from 1 for each data set
        }));
    };


    useEffect(() => {
      
        axios.get(`${UrlLink}Masters/Flagg_color_Detials_link`)
          .then((res) => setFlag(res?.data))
          .catch((err) => console.log(err));
    }, [UrlLink]);

    useEffect(() => {
      
    axios.get(`${UrlLink}Masters/Department_Detials_link`)
        .then((res) => setDepartmentData(res?.data))
        .catch((err) => console.log(err));
    }, [UrlLink]);

    
   
    const allDepartments = ["OP", "IP", "CASUALITY", "ICU", "CCU"];
    const [DepartmentNames,setDepartmentNames] = useState([]);
   
  
    

   
    // useEffect(() => {
    //     if (UserData?.username === "host" || UserData?.username === "admin") {
    //       setIsHost(true); // Host or admin is allowed to see all departments
    //     } else {
    //         setIsHost(false); // Non-host will only see departments assigned to them
            
    //         const userDepartments = UserData?.DepartmentId
    //         ? DepartmentData.filter((item) => item.Department_Id === UserData.DepartmentId)
    //         : [];

    //         console.log(userDepartments, 'userDepartments');
  
    //         const Departmentnames = UserData?.Department
    //         ? DepartmentData.filter((item) => item.Department_Name === UserData.Department)
    //         : [];
    //         // If userDepartments is available, find matching department data
    //         if (userDepartments.length > 0) {
    //             const DepData = DepartmentData?.find(
    //             (p) => p?.Department_Id === UserData?.DepartmentId && p?.Department_Name === UserData?.Department
    //             );
    //             console.log(DepData, "DepDataaaaaaaaaaaaaaa");
    //         }
    //     }
    //   }, [UserData, DepartmentData]);
      
    useEffect(() => {
        if (UserData?.username === "host" || UserData?.username === "admin") {
            setIsHost(true); 
        } else {
            setIsHost(false); 
            
            if (UserData?.DepartmentId && Array.isArray(UserData?.DepartmentId)) {
                const assignedDepartments = DepartmentData?.filter((item) =>
                    UserData.DepartmentId.includes(item.id)
                );

                console.log(assignedDepartments,'assignedDepartments');
                
                
                if (assignedDepartments.length > 0) {
                    setDepartmentNames(assignedDepartments.map(dep => dep.DepartmentName));
                } else {
                    setDepartmentNames([]);  
                }
            }
        }
    }, [UserData, DepartmentData]);
      

  return (
    <>
        <div className="Main_container_app">
            <div className='DivCenter_container'>Patients List </div>

            {/*------------- Patient Counts --------------------- */}
            
            <div className="con_1 ">
                
            {
                (isHost ? allDepartments : DepartmentNames)?.map((department) => (
                    <div className="chart_body_1_child_1 dww3" key={department} onClick={() => setIsSelected(department)}>
                        <div className="chart_body_1_child_1_body">
                            <div className="chart_body_1_child_1_body_icon">
                                <Diversity1Icon />
                            </div>
                            <div className="chart_body_1_child_1_body_name">
                                {department === 'CASUALITY' ? 'Casuality / Emergency Patients' : `${department} Patients`}
                            </div>
                        </div>
                    </div>
                ))
            }
               
               

            </div>

            { isSelected === 'OP' ?  (
                <>
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
                        <div className="RegisFormcon">
                            <label>Status <span>:</span></label>
                            <div
                                style={{
                                display: "flex",
                                justifyContent: "space-between",
                                width: "180px",
                                }}
                            >
                                <label style={{ width: "auto" }} htmlFor="status_yes">
                                <input
                                    required
                                    id="status_yes"
                                    type="radio"
                                    name="status"
                                    value="Registered"
                                    style={{ width: "15px" }}
                                    checked={searchOPParams.status === "Registered"}
                                    onChange={handleSearchChange}
                                />
                                Registered
                                </label>
                                <label style={{ width: "auto" }} htmlFor="status_in">
                                <input
                                    required
                                    id="status_in"
                                    type="radio"
                                    name="status"
                                    value="Inprogress"
                                    style={{ width: "15px" }}
                                    checked={searchOPParams.status === "Inprogress"}
                                    onChange={handleSearchChange}
                                />
                                Inprogress
                                </label>
                                <label style={{ width: "auto" }} htmlFor="status_no">
                                <input
                                    required
                                    id="status_no"
                                    type="radio"
                                    name="status"
                                    value="Completed"
                                    style={{ width: "15px" }}
                                    checked={searchOPParams.status === "Completed"}
                                    onChange={handleSearchChange}
                                />
                                Completed
                                </label>
                            </div>
                        </div>
                        {/* <div className="search_div_bar_inp_1">
                            <label htmlFor="">Status
                                <span>:</span>
                            </label>
                            <select
                                id=''
                                name='status'
                                value={searchOPParams.status}
                                onChange={handleSearchChange}
                            >
                                <option value='Pending'>Pending</option>
                                <option value='Completed'>Completed</option>
                            </select>
                        </div> */}

                        {UserData.Doctor ? (
                            <div className="search_div_bar_inp_1">
                            <label htmlFor="doctor">
                                Doctor Name<span>:</span>
                            </label>
                            <input
                                type="text"
                                id="doctor"
                                name="Doctor"
                                value={UserData.DoctorName || "Doctor name not available"}
                                readOnly
                            />
                            </div>
                        ):(
                            <div className="search_div_bar_inp_1">
                                <label htmlFor="doctor">Doctor Name<span>:</span></label>
                                <select
                                    id='doctor'
                                    name='Doctor'
                                    value={searchDoctorParams.Doctor}
                                    onChange={handleDoctorSearch}
                                >
                                    <option value="">Select</option> {/* Default option */}
                                    {DoctorNames.map((doctor, index) => (
                                    <option key={index} value={doctor.id}>
                                        {doctor.ShortName}
                                    </option>
                                    ))}
                                </select>
                            </div>
                        )}
                        



                    </div>
                
                    <ReactGrid columns={PatientOPRegisterColumns} RowData={PatientRegisterData} />
                </>
            ) :

                isSelected  === 'IP' ? (
                <>

                <div className="search_div_bar">
                    <div className=" search_div_bar_inp_1">
                        <label htmlFor="">Search by
                            <span>:</span>
                        </label>
                        <input
                            type="text"
                            name='query'
                            value={searchIPParams.query}
                            placeholder='Search here ... '
                            onChange={handleIPSearchChange}
                        />
                    </div>
                    <div className="search_div_bar_inp_1">
                        <label htmlFor="">Status
                            <span>:</span>
                        </label>
                        <select
                            id=''
                            name='status'
                            value={searchIPParams.status}
                            onChange={handleIPSearchChange}
                        >
                            {/* <option value=''>Select</option> */}
                            {/* <option value='Pending'>Pending</option> */}
                            <option value='Admitted'>Admitted</option>
                            <option value='Cancelled'>Cancelled</option>
                            {/* <option value='Pending'>Pending</option>
                            <option value='Completed'>Completed</option> */}
                        </select>
                    </div>

                    <div className="search_div_bar_inp_1">
                        <label> Ward Type <span>:</span> </label>
                        <select
                            name="Ward"
                            required
                            value={SelectedWard}
                            onChange={handleIPSearchChange}
                        >
                            <option value="">Select Ward</option>
                            {/* Exclude ICU and CCU wards */}
                            {WardGet.filter(ward => 
                                ward.Status === 'Active' && ward.WardName !== 'ICU' && ward.WardName !== 'CCU' && ward.WardName !== 'CASUALITY'
                            ).map((ward, indx) => (
                                <option key={indx} value={ward.WardName}>
                                    {ward.WardName}
                                </option>
                            ))}
                        </select>
                    </div>

                    {/* <div className="search_div_bar_inp_1">
                        <label>Type<span>:</span></label>
                        <select value={searchIPParams.type} onChange={handleIPTypeChange}>
                            <option value="IP">IP</option>
                            <option value="Casuality">Casuality</option>
                        </select>
                    </div> */}


                </div>


                {/* <ReactGrid columns={PatientIPRegisterColumns} RowData={IpPatientRegisterData} /> */}
            
                <ReactGrid
                    columns={PatientIPRegisterColumns}
                    RowData={
                        IpPatientRegisterData.filter(patient =>
                            // Filter by SelectedWard and exclude ICU and CCU wards
                            (SelectedWard ? patient.WardName === SelectedWard : true) &&
                            patient.WardName !== 'ICU' && patient.WardName !== 'CCU'
                        )
                    }
                />


                </>

                
            ) : isSelected === 'CASUALITY' ? (
                <>
                <div className="search_div_bar">
                    <div className=" search_div_bar_inp_1">
                        <label htmlFor="">Search by
                            <span>:</span>
                        </label>
                        <input
                            type="text"
                            name='query'
                            value={SearchEmergencyParams.query}
                            placeholder='Search here ... '
                            onChange={handleEmergencySearchChange}
                        />
                    </div>
                    <div className="search_div_bar_inp_1">
                        <label htmlFor="">Status
                            <span>:</span>
                        </label>
                        <select
                            id=''
                            name='status'
                            value={SearchEmergencyParams.status}
                            onChange={handleEmergencySearchChange}
                        >
                            {/* <option value=''>Select</option> */}
                            {/* <option value='Pending'>Pending</option> */}
                           
                            <option value='Admitted'>Admitted</option>
                            <option value='Completed'>Completed</option>
                        </select>
                    </div>

                    


                </div>
                <ReactGrid columns={PatientEmergencyRegisterColumns} RowData={EmergencyPatientRegisterData} />
            
                </>
            ) :   isSelected  === 'ICU' ? (
                <>

                <div className="search_div_bar">
                    <div className=" search_div_bar_inp_1">
                        <label htmlFor="">Search by
                            <span>:</span>
                        </label>
                        <input
                            type="text"
                            name='query'
                            value={searchIPParams.query}
                            placeholder='Search here ... '
                            onChange={handleIPSearchChange}
                        />
                    </div>
                    <div className="search_div_bar_inp_1">
                        <label htmlFor="">Status
                            <span>:</span>
                        </label>
                        <select
                            id=''
                            name='status'
                            value={searchIPParams.status}
                            onChange={handleIPSearchChange}
                        >
                            <option value='Admitted'>Admitted</option>
                            <option value='Cancelled'>Cancelled</option>
                            
                        </select>
                    </div>

                    {/* <div className="search_div_bar_inp_1">
                        <label> Ward Type <span>:</span> </label>
                        <select
                            name="Ward"
                            required
                            value={SelectedWard}
                            onChange={handleIPSearchChange}
                        >
                            <option value="">Select Ward</option>
                            {WardGet.filter(ward => 
                                ward.Status === 'Active' && ward.WardName === 'ICU'
                            ).map((ward, indx) => (
                                <option key={indx} value={ward.WardName}>
                                    {ward.WardName}
                                </option>
                            ))}
                        </select>
                    </div> */}

                   


                </div>


            
                <ReactGrid
                    columns={PatientIPRegisterColumns}
                    RowData={
                        addSerialNumbers(
                            IpPatientRegisterData.filter(patient =>
                                // Filter by SelectedWard and exclude ICU and CCU wards
                                (SelectedWard ? patient.WardName === SelectedWard : true) &&
                                patient.WardName === 'ICU'
                            )
                        )
                    }
                />


                </>

                
            ) :   isSelected  === 'CCU' ? (
                <>

                <div className="search_div_bar">
                    <div className=" search_div_bar_inp_1">
                        <label htmlFor="">Search by
                            <span>:</span>
                        </label>
                        <input
                            type="text"
                            name='query'
                            value={searchIPParams.query}
                            placeholder='Search here ... '
                            onChange={handleIPSearchChange}
                        />
                    </div>
                    <div className="search_div_bar_inp_1">
                        <label htmlFor="">Status
                            <span>:</span>
                        </label>
                        <select
                            id=''
                            name='status'
                            value={searchIPParams.status}
                            onChange={handleIPSearchChange}
                        >
                            <option value='Admitted'>Admitted</option>
                            <option value='Cancelled'>Cancelled</option>
                            
                        </select>
                    </div>

                    {/* <div className="search_div_bar_inp_1">
                        <label> Ward Type <span>:</span> </label>
                        <select
                            name="Ward"
                            required
                            value={SelectedWard}
                            onChange={handleIPSearchChange}
                        >
                            <option value="">Select Ward</option>
                            {WardGet.filter(ward => 
                                ward.Status === 'Active' && ward.WardName === 'CCU'
                            ).map((ward, indx) => (
                                <option key={indx} value={ward.WardName}>
                                    {ward.WardName}
                                </option>
                            ))}
                        </select>
                    </div> */}

                  

                </div>


            
                <ReactGrid
                    columns={PatientIPRegisterColumns}
                    RowData={
                        addSerialNumbers(
                            IpPatientRegisterData.filter(patient =>
                                (SelectedWard ? patient.WardName === SelectedWard : true) &&
                                patient.WardName === 'CCU'
                            )
                        )
                    }
                />


                </>

                
            ) : null}


            <div style={{ marginTop: "40px", textAlign: "center" }}>
                
                <div style={{ display: "flex", justifyContent: "center", gap: "70px", flexWrap: "wrap" }}>
                    {Array.isArray(Flag) && Flag?.map((flag, indx) => (
                        <div
                            key={indx}
                            style={{
                                width: "15px",
                                height: "15px",
                                backgroundColor: flag.FlaggColor,
                                border: "1px solid black",
                                position:"relative",
                                cursor: "pointer",
                             
                            }}
                            onMouseEnter={() => setHoveredFlagIndex(indx)}
                            onMouseLeave={() => setHoveredFlagIndex(null)}
                        >
                            {hoveredFlagIndex === indx && (
                                <div
                                    style={{
                                        position: "absolute",
                                        top: "-25px",
                                        left: "50%",
                                        transform: "translateX(-50%)",
                                        backgroundColor: "#d2cdd4",
                                        color: "#000",
                                        padding: "5px 10px",
                                        borderRadius: "4px",
                                        fontSize: "12px",
                                        whiteSpace: "nowrap",
                                    }}
                                >
                                    {flag.FlaggName || "No flagging data"}
                                </div>
                            )}
                        </div>
                        
                    ))}
                </div>
            </div>



        </div>
    
    </>
  )
}

export default TotalPatientList;