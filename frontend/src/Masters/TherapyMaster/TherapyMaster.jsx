import React, { useState, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux';
import ReactGrid from '../../OtherComponent/ReactGrid/ReactGrid';
import Button from "@mui/material/Button";
import EditIcon from "@mui/icons-material/Edit";
import axios from "axios";
import ToastAlert from '../../OtherComponent/ToastContainer/ToastAlert';
import ListIcon from '@mui/icons-material/List';

const TherapyMaster = () => {
    const UrlLink = useSelector(state => state.userRecord?.UrlLink);
    const userRecord = useSelector((state) => state.userRecord?.UserData);
    const toast = useSelector(state => state.userRecord?.toast);
    const dispatchvalue = useDispatch();
    const [TherapyTypeData, setTherapyTypeData] = useState([]);
    const [TherapyTypePage, setTherapyTypePage] = useState('TherapyMaster')
    const [Specialities, setSpecialities] = useState([])

    // -----------------------TherapyTypeMaster
    const [TherapyType, setTherapyType] = useState({
        TherapyId: '',
        // Department:'',
        TherapyType: '',
        TherapyName: '',
        SubprocedureName: '',
        Description: '',
        IsRequireMedication:false,
        IpAmount : '',
        OpAmount: '',
        IsGst: false,
        GSTvalue: ''

    });

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        if (name === 'TherapyName') {
            setTherapyType((prevState) => ({
                ...prevState,
                [name]: value?.toUpperCase()?.trim(),
            }));
        }
        else if (name === 'Description') {
            setTherapyType((prevState) => ({
                ...prevState,
                [name]: value?.toUpperCase()?.trim(),
            }));
        }
        
        else if (name === 'IsRequireMedication') {
            setTherapyType((prevState) => ({
                ...prevState,
                [name]: value === "true",
            }));
        }
        else if (name === 'IsGst') {
            setTherapyType((prevState) => ({
                ...prevState,
                [name]: value === "true",
            }));
        }
        
        else {
            setTherapyType((prevState) => ({
                ...prevState,
                [name]: value,
            }));
        }

    };
    const [IsTherapyTypeGet, setIsTherapyTypeGet] = useState(false);

    const handleTherapyTypeubmit = () => {
        if (TherapyType.TherapyName) {
            const data = {
                ...TherapyType,
                created_by: userRecord?.username || ''
            }
            axios.post(`${UrlLink}Masters/TherapyType_Master_link`, data)
                .then((res) => {
                    const resData = res.data;
                    const mess = Object.values(resData)[0];
                    const typp = Object.keys(resData)[0];
                    const tdata = {
                        message: mess,
                        type: typp,
                    }
                    dispatchvalue({ type: 'toast', value: tdata })
                    setIsTherapyTypeGet(prev => !prev)
                    setTherapyType({
                        TherapyId: '',
                        TherapyType: '',
                        TherapyName: '',
                        SubprocedureName: '',
                        Description: '',
                        IsRequireMedication:false,
                        IpAmount : '',
                        OpAmount: '',
                        IsGst: false,
                        GSTvalue: ''
                                    })
                })
                .catch((err) => {
                    console.log(err);
                })
        }
        else {
            const tdata = {
                message: "Please Provide TherapyType.",
                type: 'warn'
            }
            dispatchvalue({ type: 'toast', value: tdata });
        }
    };

    useEffect(() => {
        axios.get(`${UrlLink}Masters/TherapyType_Master_link`)
            .then((res) => {
                const ress = res.data;
                console.log(ress, 'gdtgdtgdtdgdtdg');
                
                setTherapyTypeData(ress)
            })
            .catch((err) => {
                console.log(err);
            })
    }, [IsTherapyTypeGet, UrlLink])

    const handleeditTherapyType = (params) => {
        const { id, ...rest } = params
        setTherapyType((prev) => ({
            ...prev,
            TherapyId: id,
            ...rest
        }))
    }

    const handleeditTherapyTypeStatus = (params) => {
        const data = {
            TherapyId: params.id,
            Statusedit: true
        }
        axios.post(`${UrlLink}Masters/TherapyType_Master_link`, data)
            .then((res) => {
                const resres = res.data;
                console.log("resres",resres);
                let typp = Object.keys(resres)[0]
                let mess = Object.values(resres)[0]
                const tdata = {
                    message: mess,
                    type: typp,
                }

                dispatchvalue({ type: 'toast', value: tdata });
                setIsTherapyTypeGet(prev => !prev)
            })
            .catch((err) => {
                console.log(err);
            })
    }
    const TheropyTypeColumns = [
        {
            key: "id",
            name: "Therapy Id",
            frozen: true
        },
        {
            key: "created_by",
            name: "Created By ",
            frozen: true
        },
        {
            key: "SpecialityName",
            name: "Speciality Name",
            frozen: true
        },
        {
            key: "TherapyName",
            name: "Therapy Name",
      
        },
        {
            key: "SubprocedureName",
            name: "Sub Therapy Name",
      
        },
        {
            key: "Description",
            name: "Description",
      
        },
        {
            key: "IpAmount",
            name: "IpAmount",
      
        },
        {
            key: "OpAmount",
            name: "OpAmount",
      
        },
        {
            key: "GSTvalue",
            name: "GST Value",
      
        },
        {
            key: "OldIpAmount",
            name: "Old IpAmount",
      
        },
        {
            key: "OldOpAmount",
            name: "Old OpAmount",
      
        },
        {
            key: "IsRequireMedication",
            name: "IsMedications",
            renderCell: (params) => (
                <>{params.row.IsRequireMedication ? "Yes" : "No"}</>
            ),
        },
        {
            key: "status",
            name: "Status",
            renderCell: (params) => (
                <>
                    <Button
                        className="cell_btn"
                        onClick={() => handleeditTherapyTypeStatus(params.row)}
                    >
                        {params.row.status}
                    </Button>
                </>
            ),
        },
        {
            key: "Action",
            name: "Action",
            renderCell: (params) => (
                <>
                    <Button
                        className="cell_btn"
                        onClick={() => handleeditTherapyType(params.row)}
                    >
                        <EditIcon className="check_box_clrr_cancell" />
                    </Button>
                </>
            ),
        }
    ]

    useEffect(()=>{
        axios.get(`${UrlLink}Masters/Speciality_Detials_link`)
        .then((response)=>{
            console.log(response.data, 'shhhhdhdhhdhdhdhdhd');

            setSpecialities(response.data)
            
        })
        .catch((error)=>{
            console.log(error);
            
        })
    },[])


    // ----------------------SubTherapyTypeMaster_______
  
    const formatLabel = (label) => {
        if (/[a-z]/.test(label) && /[A-Z]/.test(label) && !/\d/.test(label)) {
            return label
                .replace(/([a-z])([A-Z])/g, "$1 $2")
                .replace(/^./, (str) => str.toUpperCase());
        } else {
            return label;
        }
    };
    

    return (
        <>
            <div className="Main_container_app">
                <h3>Therapy Masters</h3>
                <div className="RegisterTypecon">
                    <div className="RegisterType">
                        {["TherapyMaster"].map((p, ind) => (
                            <div className="registertypeval" key={ind}>
                                <input
                                    type="radio"
                                    id={p}
                                    name="appointment_type"
                                    checked={TherapyTypePage === p}
                                    onChange={(e) => {
                                        setTherapyTypePage(e.target.value)
                                    }}
                                    value={p}
                                />
                                <label htmlFor={p}>
                                    {p}
                                </label>
                            </div>
                        ))}
                    </div>
                </div>
                <br />
                {/* ----------------------TherapyType */}
                {TherapyTypePage === 'TherapyMaster' &&
                    <>
                        <div className="common_center_tag">
                            
                            <span>Therapy Master</span>

                        </div>
                        <br />
                        <div className="RegisFormcon_1">
                           
                            <div className="RegisForm_1">
                                <label> Therapy Department <span>:</span> </label>
                                
                                <select 
                                name="TherapyType" 
                                id="TherapyType"
                                value={TherapyType.TherapyType}
                                onChange={handleInputChange}
                                >
                                    <option value="">Select</option>
                               { Specialities.map((val, ind) => (
                                                <option key={ind} value={val.Speciality_Id}>{val.SpecialityName}</option>
                                            ))}
                                </select>
                            </div>
                            <div className="RegisForm_1">
                                <label> Therapy Name <span>:</span> </label>
                                <input
                                    type="text"
                                    placeholder='Enter Therapy Name'
                                    name='TherapyName'
                                    required
                                    value={TherapyType.TherapyName}
                                    onChange={handleInputChange}
                                />
                            </div>
                            <div className="RegisForm_1">
                                <label>Sub Therapy Name <span>:</span> </label>
                                <input
                                    type="text"
                                    placeholder='Enter Sub Therapy Name'
                                    name='SubprocedureName'
                                    required
                                    value={TherapyType.SubprocedureName}
                                    onChange={handleInputChange}
                                />
                            </div>
                            <div className="RegisForm_1">
                                <label>Description
                                    <span>:</span>
                                </label>
                                <textarea
                                    name="Description"
                                    required
                                    value={TherapyType.Description}
                                    autoComplete="off"
                                    onChange={handleInputChange}
                                />
                            </div>

                            <div className="RegisForm_1">
                                <label> Op Amount<span>:</span> </label>
                                <input
                                    type="number"
                                    // placeholder='Enter Sub Therapy Name'
                                    name='OpAmount'
                                    required
                                    value={TherapyType.OpAmount}
                                    onChange={handleInputChange}
                                />
                            </div>
                            <div className="RegisForm_1">
                                <label> Ip Amount<span>:</span> </label>
                                <input
                                    type="number"
                                    // placeholder='Enter Sub Therapy Name'
                                    name='IpAmount'
                                    required
                                    value={TherapyType.IpAmount}
                                    onChange={handleInputChange}
                                />
                            </div>

                            <div className="RegisForm_1">
                                <label>
                                    Is GST<span>:</span>
                                </label>


                                <div style={{
                                    display: "flex",
              justifyContent: "flex-start",
              width: "120px",
              gap: "10px",
                                }}>
                                    <label htmlFor="IsGst" style={{ width: "auto" }}>Yes</label>
                                    <input
                                        type="radio"
                                        id="IsGst"
                                        name="IsGst"
                                        value="true" // Value associated with this option
                                        style={{ width: "15px" }}
                                        checked={TherapyType.IsGst === true} // Checked when Subtype is true
                                        onChange={handleInputChange}
                                    />
                                    <label htmlFor="subtypeNo" style={{ width: "auto" }}>No</label>
                                    <input
                                        type="radio"
                                        id="IsGst"
                                        name="IsGst"
                                        value="false" // Value associated with this option
                                        style={{ width: "15px" }}
                                        checked={TherapyType.IsGst === false} // Checked when Subtype is false
                                        onChange={handleInputChange}
                                    />
                                </div>
                            </div> 

                           {TherapyType.IsGst === true &&
                            <div className="RegisForm_1">
                                <label> GST Value<span>:</span> </label>
                                <input
                                    type="number"
                                    // placeholder='Enter Sub Therapy Name'
                                    name='GSTvalue'
                                    required
                                    value={TherapyType.GSTvalue}
                                    onChange={handleInputChange}
                                />
                            </div>
                            
                            }

                            <div className="RegisForm_1">
                                <label>
                                    Is Requires Medications<span>:</span>
                                </label>
                                <div style={{

                                 display: "flex",
              justifyContent: "flex-start",
              width: "120px",
              gap: "10px",
                                }}>
                                    <label htmlFor="IsRequireMedicationyes" style={{ width: "auto" }}>Yes</label>
                                    <input
                                        type="radio"
                                        id="IsRequireMedicationyes"
                                        name="IsRequireMedication"
                                        value="true" // Value associated with this option
                                        style={{ width: "15px" }}
                                        checked={TherapyType.IsRequireMedication === true} // Checked when Subtype is true
                                        onChange={handleInputChange}
                                    />
                                    <label htmlFor="IsRequireMedicationno" style={{ width: "auto" }}>No</label>
                                    <input
                                        type="radio"
                                        id="IsRequireMedicationno"
                                        name="IsRequireMedication"
                                        value="false" // Value associated with this option
                                        style={{ width: "15px" }}
                                        checked={TherapyType.IsRequireMedication === false} // Checked when Subtype is false
                                        onChange={handleInputChange}
                                    />
                                </div>
                            </div>
                            
                        </div>
                        <br />
                        <div className="Main_container_Btn">
                            <button onClick={handleTherapyTypeubmit}>
                                {TherapyType.TherapyId ? 'Update' : 'Save'}
                            </button>
                        </div>
                        <br />
                        {TherapyTypeData.length > 0 &&
                            <ReactGrid columns={TheropyTypeColumns} RowData={TherapyTypeData} />}
                    </>
                }



<ToastAlert Message={toast.message} Type={toast.type} />

            </div>

        </>
    )
}

export default TherapyMaster
