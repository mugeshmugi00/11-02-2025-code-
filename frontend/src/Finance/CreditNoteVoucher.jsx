import React from 'react'
import withVoucherManagement from './withVoucherManagement';
import AddBoxIcon from "@mui/icons-material/AddBox";
import ToastAlert from '../OtherComponent/ToastContainer/ToastAlert';
import {useSelector } from 'react-redux';
import VoucherEntrytable from './VoucherEntrytable';


const CreditNoteVoucher = ({
LedgerArr,
VoucherHead,
CreditAccountstate,
DebitAccountstate,
VoucherEntryarray,
NetTotalAmount,
AddEntryfunc,
SaveVouchersEntry,
VoucherHeadOnchange,
formStateOnchane,
CreditAccountstateOnchange,
EditVocherentry,
DeleteVocherentry
}) => {

  
 
  const toast = useSelector(state => state.userRecord?.toast);  
  
 
  return (
    <>
     <div className="Main_container_app">
     <h3>CreditNote Voucher</h3>

    <div className="RegisFormcon_1" >

     {VoucherHead?.VoucherNo && <div className="RegisForm_1">
        <label>Voucher No<span>:</span></label> 
        <input
        type='text'
        name='VoucherNo'
        value={VoucherHead?.VoucherNo}
        onChange={VoucherHeadOnchange}
        disabled
        />
        </div>}

        <div className="RegisForm_1">
        <label>Voucher Date<span>:</span></label> 
        <input
        type='date'
        name='VoucherDate'
        value={VoucherHead.VoucherDate}
        onChange={VoucherHeadOnchange}
        />
        </div>

        <div className="RegisForm_1">
        <label>Payment Type<span>:</span></label> 
        <select
        name='PaymentType'
        value={VoucherHead.PaymentType}
        onChange={VoucherHeadOnchange}
        >
        <option value=''>Select</option>
        <option value='Cash'>Cash</option>
        <option value='OnlinePayment'>OnlinePayment</option>
        <option value='Cheque'>Cheque</option>
        <option value='NEFT'>NEFT</option>
        <option value='RTGS'>RTGS</option>

        </select>
        </div>

        <div className="RegisForm_1">
        <label>Voucher Narration<span>:</span></label> 
        <textarea
        name='VoucherNarration'
        value={VoucherHead.VoucherNarration}
        onChange={VoucherHeadOnchange}
        >

        </textarea>
        </div>

    </div>

    <br/>

    <div className="RegisFormcon_1" >

    <div className="RegisForm_1">
    <label>Debit A/c<span>:</span></label> 
    <input
      name='DebitParticulars'
      value={DebitAccountstate.DebitParticulars}
      onChange={formStateOnchane}
      list='DebitParticulars'
    />
    <datalist
      id='DebitParticulars'
      >
        {LedgerArr.length !==0 && LedgerArr.map((ele,ind)=>(
        <option key={ind+'key'} value={`${ele.id}-${ele.LedgerName}`}>{ele.LedgerName}</option>
      ))        
      }
    </datalist>
    </div>

    <div className="RegisForm_1">
            <label>Unit / Tax<span>:</span></label> 

            <select
            name='UnitOrTax'
            value={DebitAccountstate.UnitOrTax}
            onChange={formStateOnchane}
            style={{width:'70px'}}
            disabled={DebitAccountstate.DebitParticulars === ''}
            >
            <option value=''>Select</option>
            <option value='Unit'>Unit</option>
            <option value='Tax'>Tax</option>
            </select>

            <input
            style={{width:'80px'}}
            type='UnitOrTaxValue'
            name='UnitOrTaxValue'
            value={DebitAccountstate.UnitOrTaxValue}
            onChange={formStateOnchane}
            disabled={DebitAccountstate.UnitOrTax === ''}
            />
        </div>

        <div className="RegisForm_1">
            <label style={{width:'105px'}}>Rate Per Unit / Taxable Value<span>:</span></label> 
            
            <select
            name='PerUnitOrTaxable'
            value={DebitAccountstate.PerUnitOrTaxable}
            onChange={formStateOnchane}
            style={{width:'100px'}}
            disabled={+DebitAccountstate.UnitOrTaxValue === 0}
            >
            <option value=''>Select</option>
            <option value='RatePerUnit'>Rate Per Unit</option>
            <option value='TaxableValue'>Taxable Value</option>
            </select>
            
            <input
            style={{width:'75px'}}
            type='number'
            name='RatePerUnitOrTaxableValue'
            value={DebitAccountstate.RatePerUnitOrTaxableValue}
            onChange={formStateOnchane}
            disabled={DebitAccountstate.PerUnitOrTaxable === ''}
            />
        </div>

    <div className="RegisForm_1">
        <label>Debit Amount<span>:</span></label> 
        <input
        type='number'
        name='DebitAmount'
        value={DebitAccountstate.DebitAmount}
        onChange={formStateOnchane}
        disabled
       /> 
    </div>


    <div className="Search_patient_icons" style={{cursor:'pointer'}}>
          <AddBoxIcon onClick={()=>AddEntryfunc('Debit')} />
      </div>

    </div>


    <div className="RegisFormcon_1" >

    <div className="RegisForm_1">
        <label>Credit A/c<span>:</span></label> 
        <input
        name='CreditParticulars'
        value={CreditAccountstate.CreditParticulars}
        onChange={CreditAccountstateOnchange}
        list='CreditParticulars'
        disabled={!CreditAccountstate?.id && (VoucherEntryarray.filter((ele)=> +ele.Debit !== 0).length === 0 || +CreditAccountstate.CreditAmount < 0 || 
            (NetTotalAmount.CreditTotalAmount ===  NetTotalAmount.DebitTotalAmount))}
         
        />
        <datalist
        id='CreditParticulars'>
        {LedgerArr.length !==0 && LedgerArr.map((ele,ind)=>(
          <option key={ind+'key'}  value={`${ele.id}-${ele.LedgerName}`}>{ele.LedgerName}</option>
        ))        
        }
        </datalist>

        </div>

        <div className="RegisForm_1">
            <label>Credit Amount<span>:</span></label> 
            <input
            type='number'
            name='CreditAmount'
            value={CreditAccountstate.CreditAmount}
            onChange={CreditAccountstateOnchange}
            disabled={!CreditAccountstate?.id && (VoucherEntryarray.filter((ele)=> +ele.Debit !== 0).length === 0 || +CreditAccountstate.CreditAmount < 0 || 
                (NetTotalAmount.CreditTotalAmount ===  NetTotalAmount.DebitTotalAmount))}      
            />
        </div>

        <div onClick={()=>AddEntryfunc('Credit')} className="Search_patient_icons" style={{cursor:'pointer'}}>
            <AddBoxIcon />
        </div>

    </div>


    <br/>
      
      {VoucherEntryarray.length !== 0 && (
          <VoucherEntrytable 
            VoucherEntryarray={VoucherEntryarray} 
            EditVocherentry={EditVocherentry} 
            DeleteVocherentry={DeleteVocherentry}
          />
        )}

        <br/>

        {VoucherEntryarray.length !==0 && <div className="Main_container_Btn">
            <button onClick={SaveVouchersEntry} >
              {VoucherHead?.VoucherNo ? 'Update':'Save'}
            </button>
        </div>}

        <br/>

     </div>

    <ToastAlert Message={toast.message} Type={toast.type} />
    </>
  )
}

export default withVoucherManagement(CreditNoteVoucher, 'CreditNoteVoucher');

