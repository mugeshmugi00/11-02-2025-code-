import * as React from "react";
import { useEffect, useState } from "react";
import axios from "axios";
import { useDispatch, useSelector } from "react-redux";



export default function InsuranceExaminationFinding() {

  
  const dispatchvalue = useDispatch();

  const isSidebarOpen = useSelector((state) => state.userRecord?.isSidebarOpen);

  const userRecord = useSelector((state) => state.userRecord?.UserData);

  const InsuranceUpdatedata = {}
 

//   const InsuranceUpdatedata = useSelector(
//     (state) => state.InsuranceStore?.InsuranceUpdatedata
//   );

  


  const[RelevantClinicalFindings,setRelevantClinicalFindings]=useState('')


  const handleTextAreaChange2= (event) => {
    setRelevantClinicalFindings(event.target.value)
  };





  const SavebtnFun =()=>{

    const params={

      MRN: InsuranceUpdatedata.MRN,
      ContactNumber:InsuranceUpdatedata.ContactNumber,

      Location:userRecord.location,
      createAt:userRecord.username,

      RelevantClinicalFindings:RelevantClinicalFindings,
      
      MainPageCompleted:"MainPage1",

      PageCompleted:"Diagnosis"

    }   

    axios.post(`https://vesoftometic.co.in/Insurance/Post_Pre_Auth_Form_Examination_Finding`,params)
    .then((response) => {
        console.log('Form data submitted.',response.data)
        dispatchvalue({type: "InsurancePageChange",value:"Diagnosis"});

    })
    .catch((error) => {
        console.error(error);
    });
  }

  
  useEffect(()=>{
    if(Object.values(InsuranceUpdatedata).length !== 0){
        console.log('Vathuruchu',InsuranceUpdatedata)            
     axios.get(
    `https://vesoftometic.co.in/Insurance/get_Pre_Auth_Form_Medical_History`,{
        params: InsuranceUpdatedata.MRN
    }
    )
    .then((response) => {
    // console.log('vrrrr',response.data);
    
    const data=response.data[0]
    
    if(Object.keys(data).length !==0){
      setRelevantClinicalFindings(data.RelevantClinicalFindings)
    }
    

    })
    .catch((error) => {
    console.log(error);
    });

    }
},[InsuranceUpdatedata])





  return (
    <>
     <div className="Supplier_Master_Container">
    
        
        <div className="txtars3_wit_hdj" >
            <label>Relevant Clinical Findings</label>
            <textarea
            style={{height:'150px'}}
            name="RelevantClinicalFindings"
            placeholder="Enter Relevant Clinical Findings"
            value={RelevantClinicalFindings}
            onChange={handleTextAreaChange2}
            ></textarea>
        
        </div>
        <br></br>

      </div>

      {/* <div className="submit_button_prev_next">
            <button onClick={SavebtnFun}>
                Save
            </button>
        </div> */}
    </>
  );
}
