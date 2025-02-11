import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import ToastAlert from '../OtherComponent/ToastContainer/ToastAlert'
import ReactGrid from '../OtherComponent/ReactGrid/ReactGrid';

const TherapyInformation = () => {

  const DoctorWorkbenchNavigation = useSelector(state => state.Frontoffice?.TherapistWorkbenchNavigation); 
  const userRecord = useSelector((state) => state.userRecord?.UserData);
  const UrlLink = useSelector(state => state.userRecord?.UrlLink);
  const toast = useSelector(state => state.userRecord?.toast)
  const dispatchvalue =useDispatch()
  
  const [TherapyInformation, setTherapyInformation] = useState({
    AlreadyTherapyTaken: 'No',
    CompletedDate: '',
    BeforeTherapyConditions:'',
    OnTherapyConditions:'',
    AfterTherapyConditions:'',
    NextReviewDate:''
  });

  const [Informations, setInformations] = useState([]);
 
  const formatLabel = (label) => {
    if (/[a-z]/.test(label) && /[A-Z]/.test(label) && !/\d/.test(label)) {
      return label
        .replace(/([a-z])([A-Z])/g, '$1 $2')
        .replace(/^./, (str) => str.toUpperCase());
    } else {
      return label;
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    setTherapyInformation((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? (checked ? 'Yes' : 'No') : value, // Handle checkbox for Yes/No
    }));
  };

  const handleSave = () =>{
   const postdata = {
    Patient_id : DoctorWorkbenchNavigation?.Patient_id,
    Registration_Id : DoctorWorkbenchNavigation?.Registration_id,
    createdBy : userRecord?.username,
    Location : userRecord?.location,
    ...TherapyInformation
   }
   console.log(postdata, 'dmdmkdmkmdjdmdk');
  
   axios.post(`${UrlLink}Ip_Workbench/Insert_therapy_information`,postdata)
   .then((response)=>{
    console.log(response.data);
    setTherapyInformation(({
      
      AlreadyTherapyTaken: 'No',
      CompletedDate: '',
      BeforeTherapyConditions:'',
      OnTherapyConditions:'',
      AfterTherapyConditions:'',
      NextReviewDate:''
    }))
    dispatchvalue({ type: 'toast', value: response.data[0].success })
    
   })
   .catch((error)=>{
    console.log(error);
    dispatchvalue({ type: 'toast', value: error })
    
   })
  };

  useEffect(()=>{
    axios.get(`${UrlLink}Ip_Workbench/Insert_therapy_information?Patientid=${DoctorWorkbenchNavigation?.Patient_id}&Visitid=${DoctorWorkbenchNavigation?.Visit_id}`)
    .then((response)=>{
      console.log(response);
      setInformations(response.data)
    })
    .catch((error)=>{
      console.log(error);
      
    })
  },[])


  
  const TheropyTypeColumns = [
    {
        key: "Informationid",
        name: "S No",
        frozen: true
    },
    {
      key: "createdBy",
      name: "createdBy",

  },
    {
        key: "Patientid",
        name: "Patient Id",
        frozen: true
    },
    {
        key: "Visitid",
        name: "Visit Id",
        frozen: true
    },
    {
        key: "AlreadyTherapyTaken",
        name: "Already Therapy Taken",
  
    },
    {
        key: "CompletedDate",
        name: "Completed Date",
  
    },
    {
        key: "BeforeTherapyConditions",
        name: "Before Therapy Conditions",
  
    },
    {
        key: "OnTherapyConditions",
        name: "On Therapy Conditions",
  
    },
    {
        key: "AfterTherapyConditions",
        name: "After Therapy Conditions",
  
    },
    {
        key: "NextReviewDate",
        name: "Next Review Date",
  
    }
]



  return (
    <div className='Main_container_app'>
      <div className="RegisFormcon">
        {Object.keys(TherapyInformation).map((item,index)=>(
          <div className="RegisForm_1" key={index}>
            <label htmlFor={item}>{formatLabel(item)} <span>:</span></label>
{item === 'AlreadyTherapyTaken' ? (
 <input
 type="checkbox"
 name={item}
 checked={TherapyInformation[item] === 'Yes'} // Check if it is 'Yes' for checked state
 onChange={handleChange}
/>
):
 
(item === 'CompletedDate' || item === 'NextReviewDate' )?
            <input 
            type="date" 
            name={item} 
            value={TherapyInformation[item]}
            onChange={handleChange}
             />
            :
            <textarea 
            name={item} 
            id="" 
            value={TherapyInformation[item]} 
            onChange={handleChange}
            ></textarea>
            }
          </div>
        ))}
      </div>

      <div className="Register_btn_con">
            <button className="RegisterForm_1_btns" onClick={handleSave}>
              Save
            </button>
            
          </div>


          {<ReactGrid columns={TheropyTypeColumns} RowData={Informations} />}
          <ToastAlert Message={toast.message} Type={toast.type} />
    </div>
  )
}

export default TherapyInformation;





