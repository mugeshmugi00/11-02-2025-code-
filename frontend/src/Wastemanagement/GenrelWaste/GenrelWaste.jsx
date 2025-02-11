import React, { useEffect, useState } from 'react'



import axios from 'axios';


function GenrelWaste() {
  const [date,setDate]=useState()
  const [genrelWst,setWst]=useState({
    wst_type:'Genrel Waste',
  })
  


  const loadValue = (e) => {
    const { name, value } = e.target;
    setWst({ ...genrelWst, [name]: value });
  
  };

  const formSubmit = (event) => {
    event.preventDefault();

      const waste={
       wst:genrelWst
      }
      // axios.post('http://127.0.0.1:8000/biowaste',{data:waste})
      // .then(response=>console.log(response.data))
      console.log(waste)
   
  };
  return (
    <div className="Main_container_app">
        <h3>Genrel Waste</h3>
        <form method="post" onSubmit={formSubmit}>
        {/* <div className="RegisterTypecon">
          <div  className='RegisForm_1'>
          <label>Enter Date</label> <span>:</span><input type='date' name='date' value={date} onChange={loadValue} required></input>

          </div>
        </div> */}
        <div className='RegisFormcon' style={{margin:"20px"}}>
         <div className='RegisForm_1'>
         <label>Genrel Waste</label>

         </div>
         <div className='RegisForm_1'>
         <label>Bag Count</label> <span>:</span><input type='number' name='BagCount' value={genrelWst.bagCount} onChange={loadValue} required></input>

         </div>
         <div className='RegisForm_1'>
         <label>Weight</label> <span>:</span><input type='number' name='Weight' value={genrelWst.weight} onChange={loadValue} required></input>

         </div>
        </div>


       

        <div className='Main_container_Btn'><button type='submit'>Save</button></div>
        </form>


    </div>
  )
}

export default GenrelWaste
