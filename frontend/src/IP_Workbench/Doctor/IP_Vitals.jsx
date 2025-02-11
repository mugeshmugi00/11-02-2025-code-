import React, { useState, useEffect } from 'react'
import { useDispatch, useSelector } from "react-redux";
// import { format } from "date-fns";
import ReactGrid from '../../OtherComponent/ReactGrid/ReactGrid';
import axios from 'axios';
import ToastAlert from '../../OtherComponent/ToastContainer/ToastAlert';
import { IconButton } from '@mui/material';
import VisibilityIcon from '@mui/icons-material/Visibility';
import Button from "@mui/material/Button";
import AddIcon from "@mui/icons-material/Add";
import ToggleButton from "@mui/material/ToggleButton";
import ToggleButtonGroup from "@mui/material/ToggleButtonGroup";


const IP_Vitals = () => {
    const dispatch = useDispatch();
    const UrlLink = useSelector(state => state.userRecord?.UrlLink);
    const toast = useSelector(state => state.userRecord?.toast);
    const IP_DoctorWorkbenchNavigation = useSelector(state => state.Frontoffice?.IP_DoctorWorkbenchNavigation);
    console.log(IP_DoctorWorkbenchNavigation,'IP_DoctorWorkbenchNavigation');

    const userRecord = useSelector((state) => state.userRecord?.UserData);
    const [openModal2, setOpenModal2] = useState(false);
    const [openModalNewScore, setOpenModalNewScore] = useState(false);

    const openModal = () => {
      setOpenModal2(true);
    };


    
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
       
        Temperature: '',
        PulseRate: '',
        SPO2: '',
        HeartRate: '',
        RespiratoryRate: '',
        SBP: '',
        DBP: '',
        Height: '',
        Weight: '',
        BMI: '',
        WC: '',
        HC: '',
        BSL:'',
        Painscore:'',
        SupplementalOxygen:'',
        LevelOfConsiousness:'',
        CapillaryRefillTime:'',
        // ETCO2: "",
        // BreathSounds: "",
        // Date: "",
        // Time: "",
    });

    const [IntakeData, setIntakeData] = useState({
        IntakeType: "",
        IntakeMode: "",
        Site: "",
        Measurement1: "",
        MeasurementType1: "ml",
        Duration: "",
        DurationType: "hours",
        Remarks1: "",
    });
    
    const [OutputData, setOutputData] = useState({
    OutputType: "",
    Measurement2: "",
    MeasurementType2:'ml',
    Remarks2: "",
    });
    const [Balance, setBalanceData] = useState({
    totalInputDay: "",
    totalOutputDay: "",
    balance: "",
    balanceType: "",
    })
    
    
    const [type, setType] = useState("Vital");
    const [InputOutputType, setInputOutputType] = useState("Intake");
    const blockInvalidChar = e => ['e', 'E', '+', '-'].includes(e.key) && e.preventDefault();

    const [gridData, setGridData] = useState([])
    const [IsGetData, setIsGetData] = useState(false)

    const [IsViewMode, setIsViewMode] = useState(false)
    const [IsGetInOutBalanceData, setIsGetInOutBalanceData] = useState(false)


    const [IsInOutBalanceViewMode, setIsInOutBalanceViewMode] = useState(false)
    const [intakeDetailsData, setIntakeDetailsData] = useState([]);
    const [outputDetailsData, setOutputDetailsData] = useState([]);
    const [balanceDetailsData, setBalanceDetailsData] = useState([]);

    const [totalMeasurement1, setTotalMeasurement1] = useState(0);
    const [totalMeasurement2, setTotalMeasurement2] = useState(0);

  
    const colorStyles = {
        normal: 'green',
        minlow: 'yellow',
        maxlow: 'yellow',
        minmedium: 'orange',
        maxmedium: 'orange',
        minhigh: 'red',
        maxhigh: 'red',
      };
      
    
      const getColorByStatus = (status) => {
        switch (status) {
            case 3:
                return 'red';
            case 2:
                return 'orange';
            case 1:
                return 'yellow';
            case 0:
                return 'green';
            default:
                return ''; // Default color for undefined or other values
        }
    };
    

    const getColorStyle = (status) => {
        return colorStyles[status] || ''; // Default color if no match
      };
      
      const renderColorBox = (status) => {
        // Ensure `status` is defined and is a string
        if (typeof status !== 'string' || status.length === 0) {
            return null; // Or render a default/fallback element
        }
    
        return (
            <div
                style={{
                    width: '40px', // Slightly larger for better visibility
                    height: '40px', // Slightly larger for better visibility
                    backgroundColor: getColorStyle(status),
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    marginRight: '15px', // Increased spacing
                    borderRadius: '8px', // Rounded corners
                    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)', // Subtle shadow for depth
                    border: '1px solid rgba(0, 0, 0, 0.2)', // Light border for contrast
                    fontSize: '12px', // Adjust font size for the box
                    fontWeight: 'bold', // Bold text
                    color: '#fff', // Text color for better contrast
                }}
            >
                {status.charAt(0).toUpperCase()} {/* Display first letter of the range */}
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
      
    const VitalsFormColumns = [
        {
            key: 'id',
            name: 'S.No',
            frozen: true
        },
        { key: 'Type', name: 'Type',frozen: true },
        // { key: 'PrimaryDoctorId', name: 'Doctor Id',frozen: true },
        { key: 'PrimaryDoctorName', name: 'Doctor Name',frozen: true },
      
        {
            key: 'Date',
            name: 'Date',
            frozen: true
        },
        {
            key: 'Time',
            name: 'Time',
            frozen: true
        },
       
       
       
        {
            key: 'view',
            frozen: true,
            name: 'View',
            renderCell: (params) => (
              <IconButton onClick={() => handleView(params.row)}>
                <VisibilityIcon />
              </IconButton>
            ),
          },
        
    ]

    const IntakeColumns = [
        { key: 'id', name: 'S.No' ,frozen: true},
        // { key: 'VisitId', name: 'Visit ID',frozen: true },
        // { key: 'PrimaryDoctorId', name: 'Doctor Id', frozen: true },
        { key: 'PrimaryDoctorName', name: 'Doctor Name', frozen: true },
        { key: 'IntakeType', name: 'Intake Type' },
        { key: 'IntakeMode', name: 'Intake Mode' },
        // { key: 'Site', name: 'Site' },
        { key: 'Measurement1', name: 'Measurement' },
        { key: 'MeasurementType1', name: 'Measurement Type' },
        { key: 'Duration', name: 'Duration' },
        { key: 'Remarks', name: 'Remarks' },
        { key: 'Date', name: 'Date',frozen: true},
        { key: 'Time', name: 'Time',frozen: true },
        // {
        //   key: 'view',
        //   name: 'View',
        //   frozen: true,
        //   renderCell: (params) => (
        //     <IconButton onClick={() => handleView(params.row)}>
        //       <VisibilityIcon />
        //     </IconButton>
        //   ),
        // },
        // { key: 'TotalMeasurement1', name: 'Total Measurement',frozen: true }
      ];
    
      const OutputColumns = [
        { key: 'id', name: 'S.No',frozen: true },
        // { key: 'VisitId', name: 'Visit ID',frozen: true },
        // { key: 'PrimaryDoctorId', name: 'Doctor Id', frozen: true },
        { key: 'PrimaryDoctorName', name: 'Doctor Name', frozen: true },
        { key: 'OutputType', name: 'Output Type' },
        { key: 'Measurement2', name: 'Measurement' },
        { key: 'MeasurementType2', name: 'Measurement Type' },
        { key: 'Remarks2', name: 'Remarks' },
        { key: 'Date', name: 'Date',frozen: true,},
        { key: 'Time', name: 'Time' ,frozen: true,},
        // {
        //   key: 'view',
        //   name: 'View',
        //   frozen: true,
        //   renderCell: (params) => (
        //     <IconButton onClick={() => handleView(params.row)}>
        //       <VisibilityIcon />
        //     </IconButton>
        //   ),
        // },
        // { key: 'TotalMeasurement2', name: 'Total Measurement',frozen: true }
    
      ];
    
    
      const BalanceColumns = [
        { key: 'id', name: 'S.No' ,frozen: true},
        // { key: 'VisitId', name: 'Visit ID',frozen: true },
        // { key: 'PrimaryDoctorId', name: 'Doctor Id', frozen: true },
        { key: 'PrimaryDoctorName', name: 'Doctor Name', frozen: true },
        { key: 'totalInputDay', name: 'Total Input (Day)' },
        { key: 'totalOutputDay', name: 'Total Output (Day)' },
        { key: 'balance', name: 'Balance' },
        { key: 'balanceType', name: 'Balance Type' },
        { key: 'Date', name: 'Date' ,frozen: true},
        { key: 'Time', name: 'Time' ,frozen: true},
        // {
        //   key: 'view',
        //   name: 'View',
        //   frozen: true,
        //   renderCell: (params) => (
        //     <IconButton onClick={() => handleView(params.row)}>
        //       <VisibilityIcon />
        //     </IconButton>
        //   ),
        // },
      ];
    


// Handle setting the form data when viewing
const handleView = (data) => {
    setVitalFormData({
        Temperature: data.Temperature || '',
        PulseRate: data.PulseRate || '',
        SPO2: data.SPO2 || '',
        HeartRate: data.HeartRate || '',
        RespiratoryRate: data.RespiratoryRate || '',
        SBP: data.SBP || '',
        DBP: data.DBP || '',
        Height: data.Height || '',
        Weight: data.Weight || '',
        BMI: data.BMI || '',
        WC: data.WC || '',
        HC: data.HC || '',
        BSL: data.BSL || '',
        Painscore: data.Painscore || '',
        SupplementalOxygen: data.SupplementalOxygen || '',
        LevelOfConsiousness: data.LevelOfConsiousness || '',
        CapillaryRefillTime: data.CapillaryRefillTime || '',
        
        // ETCO2: data.EtCO2 || '',
        // BreathSounds: data.BreathSounds || '',
        // Date: data.Date || '',
        // Time: data.Time || '',
        // Createdby: data.Createdby || '',
    });
    setIsViewMode(true);
};


// Handle clearing the form and resetting the view mode
const handleClear = () => {
setVitalFormData({
    Temperature: '',
    PulseRate: '',
    SPO2: '',
    HeartRate: '',
    RespiratoryRate: '',
    SBP: '',
    DBP: '',
    Height: '',
    Weight: '',
    BMI: '',
    WC: '',
    HC: '',
    BSL: '',
    Painscore:'',
    SupplementalOxygen:'',
    LevelOfConsiousness:'',
    CapillaryRefillTime:'',
    // ETCO2:'',
    // BreathSounds:'',
    // Date: '',
    // Time: '',
    // Createdby: '',
});
setIsViewMode(false);
};
  

    // useEffect(() => {
    //     axios.get(`${UrlLink}Ip_Workbench/IP_Vitals_Form_Details_Link`,{params:{RegistrationId:IP_DoctorWorkbenchNavigation?.RegistrationId}})
    //         .then((res) => {
    //             const ress = res.data
    //             console.log(ress)
    //             setGridData(ress)
    
    //         })
    //         .catch((err) => {
    //             console.log(err);
    //         })
    //   }, [UrlLink,IP_DoctorWorkbenchNavigation,IsGetData])
    
    

    useEffect(() => {

        const RegistrationId = IP_DoctorWorkbenchNavigation?.RegistrationId;
        const departmentType = IP_DoctorWorkbenchNavigation?.RequestType;

        if (RegistrationId) {
            axios.get(`${UrlLink}Ip_Workbench/IP_Vitals_Form_Details_Link`, {
                params: {
                    RegistrationId: RegistrationId,
                    DepartmentType: departmentType,
                    Type: 'Doctor'
                }
            })
            .then((res) => {
                const data = res.data;
                console.log('API Data:', data); // Check the data structure here
                
                // Access the `vital_details` array from the response
                if (data && Array.isArray(data.vital_details)) {
                    setGridData(data.vital_details);
                } else {
                    console.error('vital_details is not an array:', data);
                }
            })
            .catch((err) => {
                console.error('Error fetching data:', err);
            });
        }    
    }, [UrlLink, IP_DoctorWorkbenchNavigation, IsGetData]);
  

    useEffect(() => {
        const RegistrationId = IP_DoctorWorkbenchNavigation?.RegistrationId;
        const departmentType = IP_DoctorWorkbenchNavigation?.RequestType;
        
        if (RegistrationId ) {
          axios
            .get(`${UrlLink}Ip_Workbench/IP_InputOutputBalance_Details_Link`, {
              params: {
                RegistrationId: RegistrationId,
                DepartmentType: departmentType
                },
            })
          .then((res) => {
              const { intake_details, output_details,balance_details} = res.data;
    
              console.log('Intake Details:', intake_details);
              console.log('Output Details:', output_details);
              console.log('balance Details:', balance_details);

    
              // Set the data for each grid separately
              setIntakeDetailsData(intake_details || []);
              setOutputDetailsData(output_details || []);
              setBalanceDetailsData(balance_details || []);
              calculateTotalMeasurement1(intake_details || []);
              calculateTotalMeasurement2(output_details || []);
          })
          .catch((err) => {
            console.error(err);
          });
        }
      }, [IsGetInOutBalanceData, UrlLink, IP_DoctorWorkbenchNavigation]);
    
    
    

      const getTodayDate = () => {
        const today = new Date();
        const year = today.getFullYear();
        const month = String(today.getMonth() + 1).padStart(2, '0');
        const day = String(today.getDate()).padStart(2, '0');
        return `${day}-${month}-${year.toString().slice(-2)}`;
      };
    
    
      const calculateTotalMeasurement1 = (data) => {
        const todayDate = getTodayDate();
        const total = data
          .filter(item => item.Date === todayDate)
          .reduce((sum, item) => sum + (parseFloat(item.Measurement1) || 0), 0);
        setTotalMeasurement1(total);
        setBalanceData(prev => {
          const updatedBalance = total - prev.totalOutputDay;
          return {
            ...prev,
            totalInputDay: total,
            balance: updatedBalance,
            balanceType: updatedBalance < 0 ? "Negative" : "Positive"
          };
        });
      };
    
      const calculateTotalMeasurement2 = (data) => {
        const todayDate = getTodayDate();
        const total = data
          .filter(item => item.Date === todayDate)
          .reduce((sum, item) => sum + (parseFloat(item.Measurement2) || 0), 0);
        setTotalMeasurement2(total);
        setBalanceData(prev => {
          const updatedBalance = prev.totalInputDay - total;
          return {
            ...prev,
            totalOutputDay: total,
            balance: updatedBalance,
            balanceType: updatedBalance < 0 ? "Negative" : "Positive"
          };
        });
      };

      const HandleOnChange = (e) => {
        const { name, value } = e.target;
        const formattedValue = value.trim();
        setVitalFormData((prevFormData) => ({
            ...prevFormData,
            [name]: formattedValue,
        }));
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        console.log(name, value);
    
        if (InputOutputType === "Intake") {
          setIntakeData((prev) => ({
            ...prev,
            [name]: value,
          }));
        } else if (InputOutputType === "Output") {
          setOutputData((prev) => ({
            ...prev,
            [name]: value,
          }));
        } else {
          setBalanceData((prev) => ({
            ...prev,
            [name]: value,
          }));
        }
      };
    


    const handleChange = (event) => {
        setType(event.target.value);
    };
     
    const handleInOutBalance = (event) => {
    setInputOutputType(event.target.value);
    };
    
      const columns = [
        {
            key: 'temperature_status',
            name: 'Temperature Status',
            renderCell: (params) => (
                <div
                    style={{
                        backgroundColor: getColorByStatus(params.row.temperature_status),
                        width: '100%',
                        height: '100%',
                        textAlign: 'center',
                        color: '#fff',
                        fontWeight: 'bold',
                        borderRadius: '4px',
                        padding: '5px'
                    }}
                >
                    {params.row.temperature_status}
                </div>
            )
        },
        {
            key: 'spo2_status',
            name: 'SPO2 Status',
            renderCell: (params) => (
                <div
                    style={{
                        backgroundColor: getColorByStatus(params.row.spo2_status),
                        width: '100%',
                        height: '100%',
                        textAlign: 'center',
                        color: '#fff',
                        fontWeight: 'bold',
                        borderRadius: '4px',
                        padding: '5px'
                    }}
                >
                    {params.row.spo2_status}
                </div>
            )
        },
        {
            key: 'heartrate_status',
            name: 'Heart Rate Status',
            renderCell: (params) => (
                <div
                    style={{
                        backgroundColor: getColorByStatus(params.row.heartrate_status),
                        width: '100%',
                        height: '100%',
                        textAlign: 'center',
                        color: '#fff',
                        fontWeight: 'bold',
                        borderRadius: '4px',
                        padding: '5px'
                    }}
                >
                    {params.row.heartrate_status}
                </div>
            )
        },
        {
            key: 'RespiratoryStatus',
            name: 'Respiratory Status',
            renderCell: (params) => (
                <div
                    style={{
                        backgroundColor: getColorByStatus(params.row.RespiratoryStatus),
                        width: '100%',
                        height: '100%',
                        textAlign: 'center',
                        color: '#fff',
                        fontWeight: 'bold',
                        borderRadius: '4px',
                        padding: '5px'
                    }}
                >
                    {params.row.RespiratoryStatus}
                </div>
            )
        },
        {
            key: 'sbp_status',
            name: 'SBP Status',
            renderCell: (params) => (
                <div
                    style={{
                        backgroundColor: getColorByStatus(params.row.sbp_status),
                        width: '100%',
                        height: '100%',
                        textAlign: 'center',
                        color: '#fff',
                        fontWeight: 'bold',
                        borderRadius: '4px',
                        padding: '5px'
                    }}
                >
                    {params.row.sbp_status}
                </div>
            )
        },
        {
            key: 'SupplementalOxygen_status',
            name: 'Supplemental Oxygen Status',
            renderCell: (params) => (
                <div
                    style={{
                        backgroundColor: getColorByStatus(params.row.SupplementalOxygen_status),
                        width: '100%',
                        height: '100%',
                        textAlign: 'center',
                        color: '#fff',
                        fontWeight: 'bold',
                        borderRadius: '4px',
                        padding: '5px'
                    }}
                >
                    {params.row.SupplementalOxygen_status}
                </div>
            )
        },
        {
            key: 'LevelOfConsiousness_Status',
            name: 'Level of Consciousness Status',
            renderCell: (params) => (
                <div
                    style={{
                        backgroundColor: getColorByStatus(params.row.LevelOfConsiousness_Status),
                        width: '100%',
                        height: '100%',
                        textAlign: 'center',
                        color: '#fff',
                        fontWeight: 'bold',
                        borderRadius: '4px',
                        padding: '5px'
                    }}
                >
                    {params.row.LevelOfConsiousness_Status}
                </div>
            )
        },
        {
            key: 'CapillaryRefillTime_Status',
            name: 'Capillary Refill Time Status',
            renderCell: (params) => (
                <div
                    style={{
                        backgroundColor: getColorByStatus(params.row.CapillaryRefillTime_Status),
                        width: '100%',
                        height: '100%',
                        textAlign: 'center',
                        color: '#fff',
                        fontWeight: 'bold',
                        borderRadius: '4px',
                        padding: '5px'
                    }}
                >
                    {params.row.CapillaryRefillTime_Status}
                </div>
            )
        },
    ];
    
    const calculateTotalScore = (row) => {
    const fields = [
      'LevelOfConsiousness_Status',
      'RespiratoryStatus',
      'SupplementalOxygen_status',
      'heartrate_status',
      'temperature_status',
      'spo2_status',
      'sbp_status',
      'CapillaryRefillTime_Status'
    ];

    return fields.reduce((total, field) => {
      const value = row[field];
      return total + (value !== null ? value : 0); // Ensure we handle null values
    }, 0);
  };

//   const getScoreCategory = (score) => {
//     if (score >= 0 && score <= 4) {
//         return 'Low';
//     } else if (score >= 5 && score <= 6) {
//         return 'Medium';
//     } else if (score >= 7 && score <= 21) {
//         return 'High';
//     } else {
//         return 'Unknown';
//     }
// };

const calculateAge = (dob) => {
  const dobDate = new Date(dob);
  const today = new Date();
  let age = today.getFullYear() - dobDate.getFullYear();
  const monthDifference = today.getMonth() - dobDate.getMonth();
  if (monthDifference < 0 || (monthDifference === 0 && today.getDate() < dobDate.getDate())) {
      age--;
  }
  return age;
};

const dob = IP_DoctorWorkbenchNavigation?.DOB; // Ensure this matches the structure of your state
const age = dob ? calculateAge(dob) : null;


const getScoreCategory = (score, age) => {
  if (age >= 16) {
      // Score categories for age 16 and above
      if (score >= 0 && score <= 4) {
          return 'Low';
      } else if (score >= 5 && score <= 6) {
          return 'Medium';
      } else if (score >= 7 && score <= 21) {
          return 'High';
      } else {
          return 'Unknown';
      }
  } else {
      // Score categories for age below 16
      if (score >= 0 && score <= 2) {
          return 'Low';
      } else if (score >= 3 && score <= 5) {
          return 'Medium';
      } else if (score >= 6 && score <= 12) {
          return 'High';
      } else {
          return 'Unknown';
      }
  }
};

  // Example usage in render or function
  const totalScore = gridData.length > 0 ? calculateTotalScore(gridData[gridData.length - 1]) : 0;
  // const scoreCategory = getScoreCategory(totalScore);
  const scoreCategory = age !== null ? getScoreCategory(totalScore, age) : 'Unknown';
  console.log(totalScore, 'totalScore');

    

  const handleVitalFormSubmit = () => {
        
    const RegistrationId = IP_DoctorWorkbenchNavigation?.RegistrationId;
    const DepartmentType = IP_DoctorWorkbenchNavigation?.RequestType;

    if (!RegistrationId) {
        dispatch({ type: 'toast', value: { message: 'Registration ID is missing', type: 'error' } });
        return;
    }
    const senddata={
        // ...VitalFormData,
        Temperature: VitalFormData.Temperature || null,
        PulseRate: VitalFormData.PulseRate || null,
        SPO2: VitalFormData.SPO2 || null,
        HeartRate: VitalFormData.HeartRate || null,
        RespiratoryRate: VitalFormData.RespiratoryRate || null,
        SBP: VitalFormData.SBP || null,
        DBP: VitalFormData.DBP || null,
        Height: VitalFormData.Height || null,
        Weight: VitalFormData.Weight || null,
        BMI: VitalFormData.BMI || null,
        WC: VitalFormData.WC || null,
        HC: VitalFormData.HC || null,
        BSL: VitalFormData.BSL || null,
        Painscore: VitalFormData.Painscore || null,
        SupplementalOxygen: VitalFormData.SupplementalOxygen || '',
        LevelOfConsiousness: VitalFormData.LevelOfConsiousness || '',
        CapillaryRefillTime: VitalFormData.CapillaryRefillTime || '',
        RegistrationId,
        DepartmentType,
        Createdby:userRecord?.username,
        Type:'Doctor',

        
    }

    console.log(senddata,'senddata');
    
    axios.post(`${UrlLink}Ip_Workbench/IP_Vitals_Form_Details_Link`, senddata)
    .then((res) => {
        const [type, message] = [Object.keys(res.data)[0], Object.values(res.data)[0]];
        dispatch({ type: 'toast', value: { message, type } });
        setIsGetData(prev => !prev);
        handleClear();
        })
        .catch((err) => console.log(err));
    
}


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
                         
                        </>
                        <br />
                          <div className="Main_container_Btn">
                            <button
                              onClick={() => setOpenModalNewScore(false)} // Close the grid
                            >
                              Close
                            </button>
                          </div>
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
        {/* <ToastAlert Message={toast.message} Type={toast.type} /> */}
      </div>
        
            

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


                
{type === "Vital" ? (
                    Object.keys(VitalFormData).map((p, index) => (
                        <div className='RegisForm_1' key={p}>
                            <label htmlFor={`${p}_${index}`}>
                                {formatLabel(p)} <span>:</span>
                            </label>
                            {p === 'SupplementalOxygen' ? (
                                <select
                                id={`${p}_${index}`}
                                name={p}
                                value={VitalFormData[p]}
                                onChange={HandleOnChange}
                                readOnly={IsViewMode}
                                disabled = {IsViewMode}

                                >
                                <option value="">Select</option>
                                <option value="Yes">Yes</option>
                                <option value="No">No</option>
                                </select>
                            ) : p === 'LevelOfConsiousness' ? (
                                <select
                                id={`${p}_${index}`}
                                name={p}
                                value={VitalFormData[p]}
                                onChange={HandleOnChange}
                                readOnly={IsViewMode}
                                disabled = {IsViewMode}

                                >
                                <option value="">Select</option>
                                <option value="Alert">Alert</option>
                                <option value="Responsive to Voice">V - Responsive to Voice</option>
                                <option value="Responsive to Pain">P - Responsive to Pain</option>
                                <option value="Unresponsive">U - Unresponsive</option>
                                </select>
                            ) :  p === 'CapillaryRefillTime' ? (
                                <select
                                id={`${p}_${index}`}
                                name={p}
                                value={VitalFormData[p]}
                                onChange={HandleOnChange}
                                readOnly={IsViewMode}
                                // disabled = {IsViewMode}
                                disabled={IsViewMode || +IP_DoctorWorkbenchNavigation.Age > 18}

                                >
                                <option value="">Select</option>
                                <option value="under 2 seconds">under 2 seconds</option>
                                <option value="3 to 4 seconds">3-4 seconds</option>
                                <option value="greaterthan 4 seconds"> {`>4 seconds`}</option>
                                </select>
                            ) : (
                                <input
                                id={`${p}_${index}`}
                                autoComplete='off'
                                type={p === 'Date' ? 'date' : p === 'Time' ? 'time' : 'text'}
                                name={p}
                                value={VitalFormData[p]}
                                readOnly={IsViewMode}
                                onChange={HandleOnChange}
                                />
                            )}
                        </div>
                        
                    ))
                    
                ) : type === "NewsScore" ? (
                    <div style={{ display: 'flex', alignItems: 'center',marginLeft: '20%',justifyContent:'center' }}>
                        {renderColorBox('minhigh')}Min High
                        {renderColorBox('minmedium')}Min Medium
                        {renderColorBox('minlow')}Min Low
                        {renderColorBox('normal')}Normal
                        {renderColorBox('maxlow')}Max Low
                        {renderColorBox('maxmedium')}Max Medium
                        {renderColorBox('maxhigh')}Max High
                    </div>
                    
                ) : null}
        
             
               
                {type !== "NewsScore" && (
                    <div style={{ width: "100%", display: "grid", placeItems: "center" }}>
                    <ToggleButtonGroup
                    value={InputOutputType}
                    exclusive
                    onChange={handleInOutBalance}
                    aria-label="Platform"
                    >
                    <ToggleButton
                        value="Intake"
                        style={{
                        height: "30px",
                        width: "100px",
                        backgroundColor:
                            InputOutputType === "Intake"
                            ? "var(--selectbackgroundcolor)"
                            : "inherit",
                        }}
                        className="togglebutton_container"
                    >
                        Intake
                    </ToggleButton>
                    <ToggleButton
                        value="Output"
                        style={{
                        backgroundColor:
                            InputOutputType === "Output"
                            ? "var(--selectbackgroundcolor)"
                            : "inherit",
                        width: "100px",
                        height: "30px",
                        }}
                        className="togglebutton_container"
                    >
                        Output
                    </ToggleButton>
                    <ToggleButton
                        value="Balance"
                        style={{
                        backgroundColor:
                            InputOutputType === "Balance"
                            ? "var(--selectbackgroundcolor)"
                            : "inherit",
                        width: "100px",
                        height: "30px",
                        }}
                        className="togglebutton_container"
                    >
                        Balance
                    </ToggleButton>
                    </ToggleButtonGroup>
                    </div>
                )}
                
                {type !== "NewsScore" && InputOutputType === "Intake" && intakeDetailsData.length > 0 && (
                    <>
                    <ReactGrid columns={IntakeColumns} RowData={intakeDetailsData} />
                    <div style={{ padding: '10px', fontWeight: 'bold' }}>
                        Total Measurement: {totalMeasurement1} ml 
                    </div>
                    </>
                )}
                {type !== "NewsScore" && InputOutputType === "Output" && outputDetailsData.length > 0 && (
                    <>
                    <ReactGrid columns={OutputColumns} RowData={outputDetailsData} />
                    <div style={{ padding: '10px', fontWeight: 'bold' }}>
                        Total Measurement: {totalMeasurement2} ml 
                    </div>
                    </>
                )}

                {type !== "NewsScore" && InputOutputType === "Balance" && balanceDetailsData.length > 0 && (
                    <ReactGrid columns={BalanceColumns} RowData={balanceDetailsData} />
                )}
                
                <div className="Main_container_Btn">
                    {IsViewMode && (
                        <button onClick={handleClear}>Clear</button>
                    )}
                    {!IsViewMode &&  type === 'Vital' &&(
                        <button onClick={handleVitalFormSubmit}>Submit</button>
                    )}
                </div>
                
                
                {type === "Vital" && (
                  <div style={{display:'flex',alignItems:'center',marginLeft: '40%', textAlign: 'center', marginTop: '20px' }}>
                    <h2>EWS Score: {totalScore} ({scoreCategory})</h2>
                  </div>
                )}


    </div>

   

    <br />

<div className="Main_container_Btn">
  <button onClick={() => setOpenModal2(false)}>Close</button>
</div>

 </div>
</div>



)
}
                

        






                {/* {type === "Vital" && gridData.length > 0 && (
                    <>
                    <ReactGrid columns={VitalsFormColumns} RowData={gridData} />
                    
                    </>
                )}

                {type === "NewsScore" && gridData.length > 0 && (
                    <>
                    <ReactGrid columns={columns} RowData={gridData} />
                    
                    </>
                )} */}


                <ToastAlert Message={toast.message} Type={toast.type} />
            
            
    
          
        </>    
      );
      
      
}


export default IP_Vitals;

