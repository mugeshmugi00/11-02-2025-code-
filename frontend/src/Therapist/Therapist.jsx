import axios from 'axios';
import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import Button from "@mui/material/Button";
import ListIcon from '@mui/icons-material/List';
import ReactGrid from '../OtherComponent/ReactGrid/ReactGrid';

const Therapist = () => {
    const workbenchformData = useSelector(state => state.Frontoffice?.TherapistWorkbenchNavigation);
    const userRecord = useSelector((state) => state.userRecord?.UserData);
    const urllink = useSelector((state) => state.userRecord?.UrlLink);
    const [SelectedProcedure, setSelectedProcedure] = useState([]);
    const [summa, setsumma] = useState(false);
    const [Therapist, setTherapist] = useState({
        OrderId: '',
        Therapyname: '',
        SubTherapyName: '',
        Currentdate: '', // This will hold the current date
        RemainingSession: '',
        Remarks: ''
    });

    useEffect(() => {
        if (workbenchformData?.Patient_id && workbenchformData?.Visit_id) {
            axios.get(`${urllink}Ip_Workbench/Insert_Ip_Procedure_Order?Patientid=${workbenchformData.Patient_id}&Visitid=${workbenchformData.Visit_id}`)
                .then((response) => {
                    setSelectedProcedure(response.data);
                })
                .catch((error) => {
                    console.log(error);
                });
        }

        // Set the current date when component mounts or useEffect runs
        setTherapist((prev) => ({
            ...prev,
            Currentdate: new Date().toISOString().split('T')[0], // Assign current date in 'YYYY-MM-DD' format
        }));
    }, [urllink, workbenchformData, summa]);

    const TheropyTypeColumns = [
        { key: "id", name: "S No", frozen: true },
        { key: "Patient_id", name: "Patient Id", frozen: true },
        { key: "Visit_id", name: "Visit Id", frozen: true },
        { key: "AppointmentDate", name: "Appointment Date" },
        { key: "Doctor_Name", name: "Doctor Name" },
        { key: "Therapy_Name", name: "Therapy Name" },
        { key: "Sub_Therapy_Name", name: "Sub Therapy Name" },
        { key: "Sessions", name: "Total Sessions" },
        { key: "Status", name: "Status" },
        { key: "Completed_Session", name: "Completed Session" },
        { key: "Remaining_Sessions", name: "Remaining Sessions" },
        {
            key: "Edit",
            name: "Action",
            renderCell: (params) => (
                <Button className="cell_btn" onClick={() => handlestopSessions(params.row)}>
                    <ListIcon style={{ color: 'green' }} />
                </Button>
            ),
        }
    ];

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
    
        setTherapist((prev) => ({
          ...prev,
          [name]: type === 'checkbox' ? (checked ? 'Yes' : 'No') : value, // Handle checkbox for Yes/No
        }));
    };

    const handlestopSessions = (data) => {
        console.log(data, 'data');
        // Reset Therapist state and set Currentdate to today
        setTherapist({
            OrderId: data.orderid,
            Therapyname: data.Therapy_Name,
            SubTherapyName: data.Sub_Therapy_Name,
            Currentdate: new Date().toISOString().split('T')[0], // Set the current date here as well
            RemainingSession: data.Remaining_Sessions
        });
    };


    const handleComplete =()=>{
        const postdata = {
            Patient_id : workbenchformData?.Patient_id,
            Registration_Id : workbenchformData?.Registration_id,
            createdBy : userRecord?.username,
            Location : userRecord?.location,
            ...Therapist
        }

        console.log(postdata, 'postdata00000033993000039930');
        
        axios.post(`${urllink}Ip_Workbench/Insert_Completed_therapy`, postdata)
        .then((response)=>{
            console.log(response.data);
            setsumma(prev=>(!prev))
            
            setTherapist({
                OrderId: '',
                Therapyname: '',
                SubTherapyName: '',
                Currentdate: '',
                RemainingSession: '',
                Remarks: ''
            })
        })
        .catch((error)=>{
            console.log(error);
            
        })
    }

    return (
        <div className='Main_container_app'>
            <ReactGrid columns={TheropyTypeColumns} RowData={SelectedProcedure} />


<br />
            <div className="RegisFormcon">
                {
                    Object.keys(Therapist).map((item, index) => (
                        <div className="RegisForm_1" key={index}>
                            <label htmlFor={item}>{item.replace(/([A-Z])/g, ' $1').toUpperCase()} <span>:</span></label>
                           {
                            item === 'Remarks'? 

                            <textarea
                            name={item}
                            value={Therapist[item]}
                            onChange={handleChange}
                          />
                          :
                           
                           <input 
                                type="text" 
                                name={item} 
                                id={item}
                                value={Therapist[item]}
                                onChange={handleChange}
                                readOnly={!(item === 'Remarks')} // Correct readOnly logic
                            />}
                        </div>
                    ))
                }
            </div>

            <div className="Register_btn_con">
            <button className="RegisterForm_1_btns" onClick={handleComplete}>
              Complete
            </button>
            
          </div>

          <p>Completed List</p>
        </div>
    );
};

export default Therapist;
