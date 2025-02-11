import React, { useEffect, useState } from 'react'



import axios from 'axios';

const EWaste = () => {

    const [date,setDate]=useState()
      const [eWst,seteWst]=useState({
        wst_type:'E-Waste',
      })
      
    
    
      const loadValue = (e) => {
        const { name, value } = e.target;
        seteWst({ ...eWst, [name]: value });
      
      };
    
      const formSubmit = (event) => {
        event.preventDefault();
    
          const waste={
           wst:eWst
          }
          // axios.post('http://127.0.0.1:8000/biowaste',{data:waste})
          // .then(response=>console.log(response.data))
          console.log(waste)
       
      };

  return (
    <div className="Main_container_app">
    <h3>Genrel Waste</h3>
    <form method="post" onSubmit={formSubmit}>
    
    <div className='RegisFormcon' style={{margin:"20px"}}>
     <div className='RegisForm_1'>
     <label>Genrel Waste</label>

     </div>
     <div className='RegisForm_1'>
     <label>Bag Count</label> <span>:</span><input type='number' name='BagCount' value={eWst.bagCount} onChange={loadValue} required></input>

     </div>
     <div className='RegisForm_1'>
     <label>Weight</label> <span>:</span><input type='number' name='Weight' value={eWst.weight} onChange={loadValue} required></input>

     </div>
    </div>


   

    <div className='Main_container_Btn'><button type='submit'>Save</button></div>
    </form>


</div>
  )
}

export default EWaste;
