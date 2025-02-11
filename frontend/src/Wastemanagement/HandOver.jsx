import React, { useState,useEffect, useCallback } from "react";
import axios from 'axios';
import { useSelector } from 'react-redux';


const HandOver = () => {

  const UrlLink = useSelector(state => state.userRecord?.UrlLink);


  const [totalWst,settotal] = useState({})
  const [hand,sethand]=useState({
    Category:'',
    Color:'',
    Weight:'',
    Collector:'',
    CollectorContact:'',
    Incharge:'',
  })
  const [errors, setErrors] = useState({});


  console.log('hand-------',hand);
  
  const [data,setdata]=useState({})

  const clearhandstate=()=>{
    sethand({
      Category:'', 
      Color:'',
      Weight:'',
      Collector:'',
      CollectorContact:'',
      Incharge:'',
    })
  }


  const validateForm = useCallback(() => {
    let isValid = true;
    let newErrors = {};

    if (!hand.Category || hand.Category === "Select") {
      newErrors.category = "Please select a waste category.";
      isValid = false;
    }
    if (!hand.Color || hand.Color === "Select") {
      newErrors.color = "Please select a waste color.";
      isValid = false;
    }
    if (!hand.Weight || hand.Weight <= 0) {
      newErrors.weight = "Please enter a valid weight.";
      isValid = false;
    }
    if (!hand.Collector.trim()) {
      newErrors.collector = "Collector name is required.";
      isValid = false;
    }
    if (!hand.CollectorContact.match(/^\d{10}$/)) {
      newErrors.collectorContact = "Enter a valid 10-digit contact number.";
      isValid = false;
    }
    if (!hand.Incharge.trim()) {
      newErrors.incharge = "Incharge name is required.";
      isValid = false;
    }

    setErrors(newErrors);
    return isValid;
  },[hand.Category, hand.Collector, hand.CollectorContact, hand.Color, hand.Incharge,hand.Weight])

  const fetchdata=useCallback(()=>{

    axios.get(`${UrlLink}wasteManagement/handoverlist`)
    .then(response=>{setdata(response.data)})
    .catch(error => console.error("Error fetching data:", error))

    axios.get(`${UrlLink}wasteManagement/totalWaste`)
    .then(response=>{settotal(response.data)})
    .catch(error => console.error("Error fetching data:", error))

  },[settotal,setdata,UrlLink])



  useEffect(()=>{
    

    fetchdata()
  
  },[fetchdata,UrlLink])

  useEffect(()=>{
    fetchdata()
  },[fetchdata])

  const loadhandover = (e) => {
    const { name, value } = e.target;
    sethand({ ...hand, [name]: value });
  };

  const submit = useCallback(()=>{
    console.log(hand)
    if (validateForm()) {
    axios.post(`${UrlLink}wasteManagement/handover`,{data:hand})
      .then((response)=>{console.log(response.data)
      fetchdata()
      clearhandstate()
      })
      .catch(error => console.error("Error fetching data:", error))
    }else {
      console.log("Validation Failed", errors);
    }
      
  },[UrlLink,hand,fetchdata,errors,validateForm])

  
  return (
    <div className='Main_container_app'>
      <div className="Main_container_app">
        <h3>Available Waste</h3>
       
        
        <div className='RegisFormcon' style={{margin:"20px"}}>
         <div className='RegisForm_1'>
         <label style={{backgroundColor:"red",color:"white"}}>Bio Red Waste</label>
         {totalWst.red ?(<label style={{border:"1px solid black"}}>{totalWst.red}</label>):(<label>Loading...</label>) }
         </div>
         
        </div>

        <div className='RegisFormcon' style={{margin:"20px"}}>
         <div className='RegisForm_1'>
         <label style={{backgroundColor:"blue",color:"white"}}>Bio Blue Waste</label>
         {totalWst.blue ?(<label style={{border:"1px solid black"}}>{totalWst.blue}</label>):(<label>Loading...</label>) }
         </div>
         
        </div>

        <div className='RegisFormcon' style={{margin:"20px"}}>
         <div className='RegisForm_1'>
         <label style={{backgroundColor:"yellow",color:"white"}}>Bio Yellow Waste</label>
         {totalWst.yellow ?(<label style={{border:"1px solid black"}}>{totalWst.yellow}</label>):(<label>Loading...</label>) }
         </div>
         
        </div>

        <div className='RegisFormcon' style={{margin:"20px"}}>
         <div className='RegisForm_1'>
         <label style={{backgroundColor:"green",color:"white"}}>Genrel Waste</label>
         {totalWst.green ?(<label style={{border:"1px solid black"}}>{totalWst.green}</label>):(<label>Loading...</label>) }
         </div>
         
        </div>

        <div className='RegisFormcon' style={{margin:"20px"}}>
         <div className='RegisForm_1'>
         <label style={{backgroundColor:"black",color:"white"}}>E Waste</label>
         {totalWst.black ?(<label style={{border:"1px solid black"}}>{totalWst.black}</label>):(<label>Loading...</label>) }
         </div>
         
        </div>

        <div className='RegisFormcon' style={{margin:"20px"}}>
         <div className='RegisForm_1'>
         <label style={{border:"1px solid black"}}>Total Waste</label>
         {totalWst.green ?(<label style={{border:"1px solid black"}}>{totalWst.red+totalWst.blue+totalWst.yellow+totalWst.green+totalWst.black}</label>):(<label>Loading...</label>) }
         </div>
         
        </div>





    </div>

    <div className="Main_container_app">
        <h3>HandOver Waste</h3>
       
        
        <div className='RegisFormcon' style={{margin:"20px"}}>
         <div className='RegisForm_1'>
         <label>Waste Category</label><span>:</span>
         <select name="Category" value={hand.Category} onChange={loadhandover}>
          <option >select</option>
          <option value="Bio Waste">Bio Waste</option>
          <option value="Generel Waste">Genrel Waste</option>
          <option value="E Waste">E Waste</option>
         </select>
         </div>

         <div className='RegisForm_1'>

          {hand.Category==="Bio Waste"? <div className='RegisForm_1'>
         <label>Waste Color</label><span>:</span>
         <select name="Color" value={hand.Color} onChange={loadhandover}>
          <option value='' >select</option>
          <option value="Red">Red</option>
          <option value="Yellow">Yellow</option>
          <option value="Blue">Blue</option>
         </select>
         </div>:
         (<div className='RegisForm_1'>
          <label>Waste Color</label><span>:</span>
          <select name="Color" value={hand.Color} onChange={loadhandover}>
           <option value='' >select</option>
           <option value="Green">Green</option>
           <option value="Black">Black</option>
          </select>
          </div>)
         }
         
         </div>
         <div className='RegisForm_1'>
         <label>Waste Weight</label><span>:</span>
         <input type="number" name="Weight" value={hand.Weight} onChange={loadhandover}/>

         </div>
         <div className='RegisForm_1'>
         <label>Waste Collecting Person</label><span>:</span>
         <input type="text" name="Collector" value={hand.Collector} onChange={loadhandover}/>

         </div>

         <div className='RegisForm_1'>
         <label>Collecting Person Contact</label><span>:</span>
         <input type="number" name="CollectorContact" value={hand.CollectorContact} onChange={loadhandover}/>

         </div>

         <div className='RegisForm_1'>
         <label>Waste Incharge Person</label><span>:</span>
         <input type="text" name="Incharge" value={hand.Incharge} onChange={loadhandover}/>

         </div>
         
        </div>

        
        <div className='Main_container_Btn'><button type='submit' onClick={submit}>Save</button></div>


    </div>

    <div className="ReactGridWrapper">
<table border="1" className="responsive-table-M007">
        <thead>
          <tr>
            <th style={{colspan:"1", rowspan:"2" ,style:"text-align: center; vertical-align: middle;"}}>S.No</th>
            <th style={{colspan:"1", rowspan:"2" ,style:"text-align: center; vertical-align: middle;"}}>Date</th>
            <th style={{colspan:"1", rowspan:"2" ,style:"text-align: center; vertical-align: middle;"}}>Waste Category</th>
            <th style={{colspan:"1", rowspan:"2" ,style:"text-align: center; vertical-align: middle;"}}>Waste Color</th>
            <th style={{colspan:"1", rowspan:"2" ,style:"text-align: center; vertical-align: middle;"}}>Weight</th>
            <th style={{colspan:"1", rowspan:"2" ,style:"text-align: center; vertical-align: middle;"}}>Waste Collecting Person</th>
            <th style={{colspan:"1", rowspan:"2" ,style:"text-align: center; vertical-align: middle;"}}>Collecting Person Contact</th>
            <th style={{colspan:"1", rowspan:"2" ,style:"text-align: center; vertical-align: middle;"}}>Waste Incharge Person</th>

          </tr>
        </thead>
        <tbody>
          {data.length>0 ? data.map((item,index) => (
            <tr key={item.id}>
              <td>{index+1}</td>
              <td>{item.date}</td>
              <td>{item.wasteCategory}</td>
              <td><label style={{backgroundColor:`${item.wasteColor}`,color:"white",width:"100px",}}>{item.wasteColor}</label></td> 
              <td>{item.weight}Kg</td>
              <td>{item.collecter}</td>
              <td>{item.collecterCnt}</td>

              <td>{item.incharge}</td>
            </tr>
            
          )) :(<tbody><tr><td className="no-data">Data Loading...</td></tr></tbody>)}
        </tbody>
      </table>

      </div>

    </div>
  )
}

export default HandOver
