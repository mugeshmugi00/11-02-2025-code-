import axios from 'axios'
import React, { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux';
import ToastAlert from '../OtherComponent/ToastContainer/ToastAlert';
import { useNavigate } from 'react-router-dom';


const BalanceSheet = () => {

    const dispatchvalue = useDispatch();
    
    const navigate = useNavigate()

    const toast = useSelector(state => state.userRecord?.toast);

    const UrlLink = useSelector(state => state.userRecord?.UrlLink);
    
    const [liablityarr,setliablityarr]=useState([])
    
    const [assetarr,setassetarr]=useState([])

    console.log('kkkkkkkkkkk',liablityarr,assetarr);
    

    useEffect(()=>{
        axios.get(`${UrlLink}finance/getbalancesheetreport`)
        .then((res)=>{
            console.log('vvvvv33444',res.data);
            let Objeget=res.data

            if(Objeget && Object.keys(Objeget).length !==0){
                
                let getliablityarr=Objeget.AsetArr || []
                let getassetarr=Objeget.liabilityArr || []

                setliablityarr(getliablityarr)
                setassetarr(getassetarr)
            }
        })
        .catch((err)=>{
            console.log(err);            
        })
    },[UrlLink])

  return (
    <>
     <div className="Main_container_app">
        <h3>Balance Sheet</h3>
        <br/>


        <div style={{display:'flex'}}>
        {liablityarr.length !==0 &&  <div className="for">
              <div className="Selected-table-container">
                
                <span>Liability</span>  
                  <table className="selected-medicine-table2">
                      <thead>
                          <tr>
                              <th id="slectbill_ins" style={{ width: "350px",height:'30px' }}>Particulars</th>
                              <th id="slectbill_ins" style={{ width: "140px",height:'30px' }}>Total</th>
                          </tr>
                      </thead>
                      <tbody>
                          {liablityarr.length !==0 &&  liablityarr.map((item, index) => (
                              <tr key={index}>
                                  {item.ledgerarr.length !==0 ? 
                                  <>
                                  <td style={{ width: "140px",height:'30px',cursor:'pointer' }} className="cell_btn" >{item.GroupName}</td> 
                                  <td style={{ width: "140px",height:'30px'}} >{item.TotalCredit || ''}</td>
                                  </>
                                  :
                                  <>
                                  <td style={{ width: "140px",height:'30px',fontWeight:'bold'}} >{item.GroupName}</td>
                                  <td style={{ width: "140px",height:'30px',fontWeight:'bold'}} >{item.TotalCredit || ''}</td>
                                  </>
                                  }
                              </tr>
                          ))}
                      </tbody>
                  </table>
              </div>
          </div>}
          {assetarr.length !==0 &&  <div className="for">
              <div className="Selected-table-container">
                
                <span>Income</span>  
                  <table className="selected-medicine-table2">
                      <thead>
                          <tr>
                              <th id="slectbill_ins" style={{ width: "350px",height:'30px' }}>Particulars</th>
                              <th id="slectbill_ins" style={{ width: "140px",height:'30px' }}>Total</th>
                          </tr>
                      </thead>
                      <tbody>
                          {assetarr.length !==0 &&  assetarr.map((item, index) => (
                              <tr key={index}>
                                {item.ledgerarr.length !==0 ?
                                  <>
                                  <td style={{ width: "140px",height:'30px',cursor:'pointer' }} className="cell_btn" >{item.GroupName}</td> 
                                  <td style={{ width: "140px",height:'30px'}} >{item.TotalDebit || ''}</td>
                                  </>
                                  :
                                  <>
                                  <td style={{ width: "140px",height:'30px',fontWeight:'bold'}}>{item.GroupName}</td>
                                  <td style={{ width: "140px",height:'30px',fontWeight:'bold'}} >{item.TotalDebit || ''}</td>
                                  </>}
                              </tr>
                          ))}
                      </tbody>
                  </table>
              </div>
          </div>}
        </div>

      </div>
    </>
  )
}

export default BalanceSheet;