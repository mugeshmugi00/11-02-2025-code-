import React, { useEffect, useState } from 'react'




import axios from 'axios';


function BioWaste() {
  const [date, setDate] = useState('');
  const [waste, setWaste] = useState({
    red: { bagCount: '', weight: '' },
    green: { bagCount: '', weight: '' },
    yellow: { bagCount: '', weight: '' },
    blue: { bagCount: '', weight: '' },
  })

  // const loadValue = (e) => {
  //   const { name, value } = e.target;
  //   setred({ ...red, [name]: value });
  //   setgreen({ ...green, [name]: value });
  //   setyellow({ ...yellow, [name]: value });
  //   setblue({ ...blue, [name]: value });
  // };

  const loadValue = (e, color) => {
    const { name, value } = e.target;
    setWaste((prevWaste) => ({
      ...prevWaste,
      [color]: {
        ...prevWaste[color],
        [name]: value,
      },
    }));
  };

  const formSubmit = (event) => {
    event.preventDefault();

      const wst_data={
        date:date,
        waste:waste,
      }
      axios.post('http://127.0.0.1:8000/wasteManagement/biowaste',{data:wst_data})
      .then(response=>console.log(response.data))
      console.log(waste)
   
  };

  return (
    <div className="Main_container_app">
        <h3>Bio-Waste</h3>
        <form method="post" onSubmit={formSubmit}>
        {/* <div className="RegisterTypecon">
          <div  className='RegisForm_1'>
          <label>Enter Date</label> <span>:</span><input type='date' name='date' value={date} onChange={(e)=>setDate(e.target.value)} required></input>

          </div>
        </div> */}
        <div className='RegisFormcon' style={{margin:"20px"}}>
         <div className='RegisForm_1'>
         <label style={{backgroundColor:"red",color:"white"}}>Red Waste</label>

         </div>
         <div className='RegisForm_1'>
         <label>Bag Count</label> <span>:</span><input type='number' name='bagCount' value={waste.red.bagCount} onChange={(e) => loadValue(e, "red")} required></input>

         </div>
         <div className='RegisForm_1'>
         <label>Weight</label> <span>:</span><input type='number' name='weight' value={waste.red.weight} onChange={(e) => loadValue(e, "red")} required></input>

         </div>
        </div>


        <div className='RegisFormcon' style={{margin:"20px"}}>
         <div className='RegisForm_1'>
         <label style={{backgroundColor:"Green",color:"white"}}>Green Waste</label>

         </div>
         <div className='RegisForm_1'>
         <label>Bag Count</label> <span>:</span><input type='number' name='bagCount' value={waste.green.b} onChange={(e) => loadValue(e, "green")} required></input>

         </div>
         <div className='RegisForm_1'>
         <label>Weight</label> <span>:</span><input type='number' name='weight' value={waste.green.weight} onChange={(e) => loadValue(e, "green")} required></input>

         </div>
        </div>

        <div className='RegisFormcon' style={{margin:"20px"}}>
         <div className='RegisForm_1'>
         <label style={{backgroundColor:"yellow",color:"white"}}>Yellow Waste</label>

         </div>
         <div className='RegisForm_1'>
         <label>Bag Count</label> <span>:</span><input type='number' name='bagCount' value={waste.yellow.bagCount} onChange={(e) => loadValue(e, "yellow")} required></input>

         </div>
         <div className='RegisForm_1'>
         <label>Weight</label> <span>:</span><input type='number' name='weight' value={waste.yellow.weight} onChange={(e) => loadValue(e, "yellow")} required></input>

         </div>
        </div>

        <div className='RegisFormcon' style={{margin:"20px"}}>
         <div className='RegisForm_1'>
         <label style={{backgroundColor:"blue",color:"white"}}>Blue Waste</label>

         </div>
         <div className='RegisForm_1'>
         <label>Bag Count</label> <span>:</span><input type='number' name='bagCount' value={waste.blue.bagCount} onChange={(e) => loadValue(e, "blue")} required></input>

         </div>
         <div className='RegisForm_1'>
         <label>Weight</label> <span>:</span><input type='number' name='weight' value={waste.blue.weight} onChange={(e) => loadValue(e, "blue")} required></input>

         </div>
        </div>

        <div className='Main_container_Btn'><button type='submit'>Save</button></div>
        </form>


    </div>
  )
}

export default BioWaste
