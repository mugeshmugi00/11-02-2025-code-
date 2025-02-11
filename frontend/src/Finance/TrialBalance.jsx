
import axios from 'axios'
import React, { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux';
import ToastAlert from '../OtherComponent/ToastContainer/ToastAlert';
import { useNavigate } from 'react-router-dom';





const TrialBalance = () => {

    const dispatchvalue = useDispatch();

    const navigate = useNavigate()
    

  
    const UrlLink = useSelector(state => state.userRecord?.UrlLink);

    const toast = useSelector(state => state.userRecord?.toast);
    
    const[Trialbalancearr,setTrialbalancearr]=useState([])

    const [Itemlist,setItemlist]=useState([])
    
    const [selectRoom, setselectRoom] = useState(false);

    const [GroupTotal,setGroupTotal]=useState({
      GroupDebitTotal:0,
      GroupCreditTotal:0,
      DiffrentDebitamount:0,
      DiffrentCreditamount:0
    })

useEffect(()=>{
    axios.get(`${UrlLink}finance/gettrialbalance`)
    .then((res)=>{console.log('0000--11',res.data);
      let getdata=res.data

      if(getdata && Array.isArray(getdata) && getdata.length !==0){
        setTrialbalancearr(getdata)
      }

    })
    .catch((err)=>{console.log(err);
    })
},[UrlLink])



useEffect(()=>{

  if(Trialbalancearr && Array.isArray(Trialbalancearr) && Trialbalancearr.length !==0)
  {

    let TotalDebit = Trialbalancearr.reduce((num,ele)=> num+= +ele.TotalDebit,0).toFixed(2) || 0
    let TotalCredit =Trialbalancearr.reduce((num,ele)=> num+= +ele.TotalCredit,0).toFixed(2) || 0
    

    if(TotalDebit === TotalCredit){
      setGroupTotal((prev)=>({
        ...prev,
        GroupDebitTotal:TotalDebit,
        GroupCreditTotal:TotalCredit
      }))
    }
    else{

      let diffamount=+TotalDebit > +TotalCredit ? +TotalDebit - +TotalCredit : +TotalCredit - +TotalDebit

      setGroupTotal((prev)=>({
        ...prev,
        GroupDebitTotal: +TotalCredit > +TotalDebit ? (+diffamount + +TotalDebit).toFixed(2): TotalDebit,
        GroupCreditTotal: +TotalDebit > +TotalCredit ? (+diffamount + +TotalCredit).toFixed(2) : TotalCredit,
        DiffrentDebitamount:+TotalDebit > +TotalCredit ? diffamount : 0,
        DiffrentCreditamount:+TotalCredit > +TotalDebit ? diffamount : 0
      }))

    }
  }

},[Trialbalancearr])





const ItemView =(row)=>{

   

  let Item=row || []

  if(Item && Item.length !==0){
      setselectRoom(true)        
      setItemlist(Item)
  }else{

      const tdata = {
          message: 'There is no data to view.',
          type: 'warn'
      };
      dispatchvalue({ type: 'toast', value: tdata });

  }

}
  
const MovieToListPage=(row)=>{

  console.log('---)))0000row',row);

  let {
    id,
    ledgerid,
    LedgerName,
    OpeningBalance,
    DebitOrCredit,
    ledger_Debit,
    ledger_Credit,
    Debit,
    Credit,
    ClosingBalance,
    NatureOfGroupId} =row;

  let sendObj ={
    id:ledgerid,
    LedgerName:LedgerName,
    NatureOfgroupId:NatureOfGroupId,
    OpeningBalance:OpeningBalance + ' ' + DebitOrCredit,
    DebitOrCredit:DebitOrCredit,
    Debit:ledger_Debit,
    Credit:ledger_Credit,
    ClosingBalance:ClosingBalance
  }

  if(sendObj && Object.keys(sendObj).length !==0)
  {
    dispatchvalue({ type: 'FinanceLedgerMasterEdit', value: sendObj })
    navigate('/Home/SingleLedgerList');
  }

}
  
  return (
  <>
  <div className="Main_container_app">
  <h3>Trial Balance</h3>
  <br/>

  <div className="Selected-table-container">
  {Trialbalancearr && (
  <table className="selected-medicine-table2">
    <thead>
      <tr>
        <th id="slectbill_ins" style={{ width: "140px", height: "30px" }}>
          Particulars
        </th>
        <th id="slectbill_ins" style={{ width: "40px", height: "30px" }}>
          Debit
        </th>
        <th id="slectbill_ins" style={{ width: "40px", height: "30px" }}>
          Credit
        </th>
      </tr>
    </thead>
    <tbody>
      {Trialbalancearr.map((group, index) => (
        <React.Fragment key={index}>
          <tr>
            <td style={{ fontWeight: "bold" }}>{group.GroupName}</td>
            <td style={{ fontWeight: "bold" }}>{group.TotalDebit}</td>
            <td style={{ fontWeight: "bold" }}>{group.TotalCredit}</td>
          </tr>

          {group.ledgerarr && group.ledgerarr.length !== 0 && (
            <tr>
              <td
                style={{ textAlign: "right", cursor: "pointer" }}
                onClick={() => ItemView(group.ledgerarr)}
                className="cell_btn"
              >
                {group.GroupName}
              </td>
              <td style={{ textAlign: "right" }}>
                {group.ledgerarr.reduce((num, ele) => (num += +ele.Debit), 0).toFixed(2) || 0}
              </td>
              <td style={{ textAlign: "right" }}>
                {group.ledgerarr.reduce((num, ele) => (num += +ele.Credit), 0).toFixed(2) || 0}
              </td>
            </tr>
          )}

          {group.SubGroup &&
            group.SubGroup.length !== 0 &&
            group.SubGroup.map((ledger, idx) => (
              <tr key={ledger.id}>
                <td
                  style={{ textAlign: "right", cursor: "pointer" }}
                  onClick={() => ItemView(ledger.ledgerarr)}
                  className="cell_btn"
                >
                  {ledger.GroupName}
                </td>
                <td style={{ textAlign: "right" }}>{ledger.TotalDebit}</td>
                <td style={{ textAlign: "right" }}>{ledger.TotalCredit}</td>
              </tr>
            ))}

          <tr>
            <td style={{ height: "30px" }}></td>
            <td style={{ height: "30px" }}></td>
            <td style={{ height: "30px" }}></td>
          </tr>
        </React.Fragment>
      ))}

      {GroupTotal.DiffrentDebitamount || GroupTotal.DiffrentCreditamount ? (
        <tr>
          <td style={{ height: "30px" }}>Difference in opening balance</td>
          <td style={{ height: "30px" }}>{GroupTotal.DiffrentCreditamount}</td>
          <td style={{ height: "30px" }}>{GroupTotal.DiffrentDebitamount}</td>
        </tr>
      ) : null}
    </tbody>
    <tfoot>
      <tr>
        <td colSpan="1" style={{ textAlign: "right", fontWeight: "bold" }}>
          Grand Total:
        </td>
        <td style={{ width: "40px", fontWeight: "bold" }}>{GroupTotal.GroupDebitTotal}</td>
        <td style={{ width: "40px", fontWeight: "bold" }}>{GroupTotal.GroupCreditTotal}</td>
      </tr>
    </tfoot>
  </table>
)}

    </div>
    
  </div>

<ToastAlert Message={toast.message} Type={toast.type} />

{selectRoom && Itemlist.length !==0 &&(
    <div className="loader" onClick={() => setselectRoom(false)}>
    <div className="loader_register_roomshow"   onClick={(e) => e.stopPropagation()}>
    <br/>
    
    <div className="common_center_tag">
        <span>Particulars</span>
    </div>
    <br/>
    <br/>

    {Itemlist.length !==0 &&  <div className="for">

      <div className="Selected-table-container">
                  <table className="selected-medicine-table2">
                      <thead>
                          <tr>
                              <th id="slectbill_ins" style={{ width: "100px" }}>S.No</th>
                              <th id="slectbill_ins" style={{ width: "140px" }}>LedgerName</th>
                              <th id="slectbill_ins" style={{ width: "140px" }}>Opening Balance</th>
                              <th id="slectbill_ins" style={{ width: "140px" }}>Debit</th>
                              <th id="slectbill_ins" style={{ width: "140px" }}>Credit</th>
                              <th id="slectbill_ins" style={{ width: "140px" }}>Closing Balance</th>
                          </tr>
                      </thead>
                      <tbody>
                          {Itemlist.length !==0 &&  Itemlist.map((item, index) => (
                              <tr key={index}>
                                  <td style={{ width: "100px"}}>{item.id}</td>
                                  <td style={{ width: "140px" , cursor:'pointer'}} className="cell_btn" onClick={()=>MovieToListPage(item)}>{item.LedgerName }</td>
                                  <td style={{ width: "140px" }}>{item.OpeningBalance + ' ' + item.DebitOrCredit }</td>                             
                                  <td style={{ width: "140px" }}>{+item.ledger_Debit || 0}</td>
                                  <td style={{ width: "140px" }}>{+item.ledger_Credit || 0}</td>
                                  <td style={{ width: "140px" }}>{item.ClosingBalance || 0}</td>
                              </tr>
                          ))}
                      </tbody>

                  </table>
              </div>

     
    </div>}
    </div>
    </div>
    )}

  </>
  )
}

export default TrialBalance;