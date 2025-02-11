import React, { useState, useEffect } from 'react'
import { useDispatch, useSelector } from "react-redux";
import ReactGrid from '../../../OtherComponent/ReactGrid/ReactGrid';
import axios from 'axios';
import ToastAlert from '../../../OtherComponent/ToastContainer/ToastAlert';
import { IconButton } from '@mui/material';
import VisibilityIcon from '@mui/icons-material/Visibility';



const IP_SurgicalSite = () => {
    const dispatch = useDispatch();
    const UrlLink = useSelector(state => state.userRecord?.UrlLink);
    const toast = useSelector(state => state.userRecord?.toast);
    const IP_DoctorWorkbenchNavigation = useSelector(state => state.Frontoffice?.IP_DoctorWorkbenchNavigation);
    console.log(IP_DoctorWorkbenchNavigation,'IP_DoctorWorkbenchNavigation');

    const userRecord = useSelector((state) => state.userRecord?.UserData);
    const blockInvalidChar = e => ['e', 'E', '+', '-'].includes(e.key) && e.preventDefault();

    
    const formatLabel = (label) => {

        if (/[a-z]/.test(label) && /[A-Z]/.test(label) && !/\d/.test(label)) {
            return label
                .replace(/([a-z])([A-Z])/g, "$1 $2")
                .replace(/^./, (str) => str.toUpperCase());
        } else {
            return label;
        }
    };

   

    const [SurgicalSite, setSurgicalSite] = useState({
        Skin: "",
        Wound: "",
        Dressing: "",
        SurgicalSiteInfection: "",
        Remarks: "",

    });


    const [gridData, setGridData] = useState([])
    const [IsGetData, setIsGetData] = useState(false)

    const [IsViewMode, setIsViewMode] = useState(false)
  
    
      
    const SurgicalSiteColumns = [
        {
            key: 'id',
            name: 'S.No',
            frozen: true
        },
        { key: 'PrimaryDoctorName', name: 'Doctor Name',frozen: true },
      
        {
            key: 'CurrDate',
            name: 'Date',
            frozen: true
        },
        {
            key: 'CurrTime',
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
        { key: 'Skin', name: 'Skin'},
        { key: 'Wound', name: 'Wound'},
        { key: 'Dressing', name: 'Dressing'},
        { key: 'SurgicalSiteInfection', name: 'SurgicalSiteInfection'},
        { key: 'Remarks', name: 'Remarks'},

        
    ]

     // Handle setting the form data when viewing
     const handleView = (data) => {
        setSurgicalSite({
            Skin: data.Skin || '',
            Wound: data.Wound || '',
            Dressing: data.Dressing || '',
            SurgicalSiteInfection: data.SurgicalSiteInfection || '',
            Remarks: data.Remarks || '',
            
            
        });
        setIsViewMode(true);
    };
    
  
  // Handle clearing the form and resetting the view mode
  const handleClear = () => {
    setSurgicalSite({
        Skin: '',
        Wound: '',
        Dressing: '',
        SurgicalSiteInfection: '',
        Remarks: '',
        
    });
    setIsViewMode(false);
};

  

    useEffect(() => {
        const RegistrationId = IP_DoctorWorkbenchNavigation?.RegistrationId;
        const departmentType = IP_DoctorWorkbenchNavigation?.RequestType;

        if (RegistrationId) {
            axios.get(`${UrlLink}Ip_Workbench/IP_SurgicalSite_Details_Link`,{
                params:{
                    RegistrationId: RegistrationId,
                    DepartmentType: departmentType,
                    // Type: 'Nurse'

                }})
                .then((res) => {
                    const ress = res.data
                    console.log(ress)
                    setGridData(ress)
        
                })
                .catch((err) => {
                    console.log(err);
                })
        }
      }, [UrlLink,IP_DoctorWorkbenchNavigation,IsGetData])
    
    


      const HandleOnChange = (e) => {
        const { name, value } = e.target;
        const formattedValue = value.trim();
        setSurgicalSite((prevFormData) => ({
            ...prevFormData,
            [name]: formattedValue,
        }));

        if (e.target.name === 'Remarks') {
            adjustHeight(e);
          }

    };

    const adjustHeight = (e) => {
        e.target.style.height = "auto"; // Reset height to calculate scrollHeight
        e.target.style.height = `${e.target.scrollHeight}px`; // Set height to scrollHeight
      };

      

    const handleSubmit = () => {
        
        const RegistrationId = IP_DoctorWorkbenchNavigation?.RegistrationId;
        const DepartmentType = IP_DoctorWorkbenchNavigation?.RequestType;

        if (!RegistrationId) {
            dispatch({ type: 'toast', value: { message: 'Registration ID is missing', type: 'error' } });
            return;
        }

        const senddata={
            ...SurgicalSite,
            RegistrationId,
            Createdby: userRecord?.username,
            DepartmentType,
            // Type:'Nurse'
            
        }

        console.log(senddata,'senddata');
        
        axios.post(`${UrlLink}Ip_Workbench/IP_SurgicalSite_Details_Link`, senddata)
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
                <div className="RegisFormcon_1" >
                    <div className="common_center_tag">
                        <span>Surgical Site</span>
                    </div>
                    
                    {
                        Object.keys(SurgicalSite).map((p, index) =>(    
                               p !== 'Remarks' && 
                        (
                            <div className='RegisForm_1' key={p}>
                                <label htmlFor={`${p}_${index}`}>
                                    {p === "NoOfDays" ? (
                                        "No.of Days"
                                      ) : (
                                        formatLabel(p)
                                      )} 
                                    
                                    <span>:</span>
                                </label>
                                {p === 'Skin' ? (
                                <select
                                    id={`${p}_${index}`}
                                    name={p}
                                    value={SurgicalSite[p]}
                                    onChange={HandleOnChange}
                                    disabled = {IsViewMode}
                                    readOnly={IsViewMode}
                                    >
                                    <option value="">Select</option>
                                    <option value="Pink">Pink</option>
                                    <option value="Flushed">Flushed</option>
                                    <option value="Pale">Pale</option>
                                    <option value="Cyanotic">Cyanotic</option>
                                    <option value="Mottled">Mottled</option>
                                    <option value="Dusky">Dusky</option>
                                    <option value="Jaundice">Jaundice</option>
          
                                    
                                </select>
                            ) : p === 'Wound' ? (
                                <select
                                    id={`${p}_${index}`}
                                    name={p}
                                    value={SurgicalSite[p]}
                                    onChange={HandleOnChange}
                                    disabled = {IsViewMode}
                                    readOnly={IsViewMode}
                                    >
                                    <option value="">Select</option>
                                    <option value="Clear">Clean</option>
                                    <option value="Oozing">Oozing</option>
                                    <option value="Gaping">Gaping</option>
                                    <option value="Open">Open</option>
                                    <option value="Infected">Infected</option>
                                </select>
                            ) : p === 'Dressing' ? (
                                <select
                                    id={`${p}_${index}`}
                                    name={p}
                                    value={SurgicalSite[p]}
                                    onChange={HandleOnChange}
                                    disabled = {IsViewMode}
                                    readOnly={IsViewMode}
                                    >
                                    <option value="">Select</option>
                                    <option value="Betadine">Betadine</option>
                                    <option value="AntibioticIrrigation">Antibiotic Irrigation</option>
                                </select>
                            ) : p === 'SurgicalSiteInfection' ? (
                                <select
                                    id={`${p}_${index}`}
                                    name={p}
                                    value={SurgicalSite[p]}
                                    onChange={HandleOnChange}
                                    disabled = {IsViewMode}
                                    readOnly={IsViewMode}
                                    >
                                    <option value="">Select</option>
                                    <option value="Yes">Yes</option>
                                    <option value="No">No</option>
                                    
                                </select>
                            ) :(
                                <input
                                id={`${p}_${index}`}
                                autoComplete='off'
                                type={(p === 'InsertionDate' || p === 'RemovalDate') ? 'date' : p === 'RemovalTime' ? 'time' : 'text'}
                                name={p}
                                value={SurgicalSite[p]}
                                onChange={HandleOnChange}
                                // disabled = {IsViewMode}
                                readOnly={IsViewMode}
                                />
                            )}
                            </div>

                        ))) 
                    }
                </div>
<br />

                <div className="RegisFormcon extend_textarea_new">
        <div className="RegisForm_1 extend_textarea_new"

        >
        <label htmlFor="Remarks">
            Remarks<span>:</span>
        </label>
        <textarea
            id="Remarks"
            name="Remarks"
            value={SurgicalSite.Remarks} // Ensure you're using the correct data object (SurgicalSite instead of DrainageTubes)
            onChange={HandleOnChange}
            // disabled = {IsViewMode}
            readOnly={IsViewMode}
            placeholder="Enter your remarks here"
        />
    </div>


                </div>
                <div className="Main_container_Btn">
            
                    {IsViewMode && (
                        <button onClick={handleClear}>Clear</button>
                    )}
                    {!IsViewMode && (
                        <button onClick={handleSubmit}>Submit</button>
                    )}
                </div>

                {gridData.length >= 0 &&
                    <ReactGrid columns={SurgicalSiteColumns} RowData={gridData} />
                }
            
            <ToastAlert Message={toast.message} Type={toast.type} />

        </>
    )
}


export default IP_SurgicalSite;