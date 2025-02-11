
const initstate={
    FinanceMasterEdit:{},
    FinanceLedgerMasterEdit:{},
    FinanceVouchersEdit:{}


}


const Financedata =(state=initstate,action)=>{

    switch(action.type){

        case 'FinanceMasterEdit':
            return {...state,FinanceMasterEdit:action.value}
        case 'FinanceLedgerMasterEdit':
            return {...state,FinanceLedgerMasterEdit:action.value}
        case 'FinanceVouchersEdit':
            return {...state,FinanceVouchersEdit:action.value}
        default:
            return state;

    }
}

export default Financedata;