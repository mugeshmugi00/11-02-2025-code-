
import React, { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux';
import ModelContainer from '../../OtherComponent/ModelContainer/ModelContainer';
import axios from 'axios';
import ReactGrid from '../../OtherComponent/ReactGrid/ReactGrid';
import EditIcon from "@mui/icons-material/Edit";
import Button from "@mui/material/Button";
import DeleteOutlineIcon from '@mui/icons-material/DeleteOutline';
import ToastAlert from '../../OtherComponent/ToastContainer/ToastAlert';
import { useNavigate } from 'react-router-dom';




const GoodsReceiptNote = () => {

  const dispatchvalue = useDispatch();
  const UrlLink = useSelector(state => state.userRecord?.UrlLink);
  const toast = useSelector(state => state.userRecord?.toast);
  const userRecord = useSelector((state) => state.userRecord?.UserData);
  
  const navigate = useNavigate();



  const today = new Date();
  const currentDate = today.toISOString().split('T')[0];
    

  const [StoreData, setStoreData] = useState([])


  const POdata = useSelector(state => state.Inventorydata?.GoodsReceiptNoteList);

  const Editdata = useSelector(state => state.Inventorydata?.GoodsReceiptNoteEdit);

  console.log('Editdata',Editdata);
  
  const [LocationData, setLocationData] = useState([]);

  const [selectRoom2, setselectRoom2] = useState(false);
  
  const [NewItemProductArray,setNewItemProductArray]=useState([])
  
  const [POItemArrays,setPOItemArrays]=useState([])

  const [GRNItemlist,setGRNItemlist]=useState([])

  const [SupplierProductArray,setSupplierProductArray]=useState([])
  
  

  // console.log('GRNItemlist----',GRNItemlist);
  

  const [GRNState,setGRNState]=useState({
    GRNDate:currentDate,
    PONumber:'',
    SupplierCode:'',
    SupplierName:'',
    SupplierBillNumber:'',
    SupplierBillDate:'',
    SupplierBillDueDate:'',
    SupplierBillAmount:'',
    GRNLocation:'',
    StorageLocation:'',
    ReceivingPersonName:'',
    IsFOCAvailable:false,
    FOCMethod:'',
  })

  const[SupplierBillfile,setSupplierBillfile]=useState(null)

  const [Amountstate,setAmountstate]=useState({
    TotalTaxableAmount:'',
    TotalTaxAmount:'',
    TotalAmount:'',
    TotalDiscountMethod:'',
    TotalDiscountType:'',
    TotalDiscount:'',
    FinalTotalTaxableAmount:'',
    FinalTotalTaxAmount:'',
    FinalTotalAmount:'',
    RoundOff:'',
    NetAmount:'',
  })


const [ItemFulldetailes,setItemFulldetailes]=useState({
  NotInPurchaseOrder:false,
  ItemCode:'',
  ItemName:'',
  IsSellable:'', 
}) 


const [GRNItemState,setGRNItemState]=useState({
  IsFOCProduct:false,  
  FOCItemCode:'',
  FOCItemName:'',
  GRNMRP:'',  
  PurchaseRateTaxable:'',   
  TaxType:'',
  TaxPercentage:'',
  PurchaseRateWithTax:'',
  OrderQty:'',  
// BillQty not in edit
  BillQty:'',
  ReceivedQty:'',
  PendingQty:'',
  ExtraQty:'',
  IsFOCQtyAvailable:false,
  FOCQty:'',
  TotalPackQty:'',
  IsMRPAsSellablePrice:true,
  SellablePrice:'',
  SellableQtyPrice:'',
  TotalPackTaxableAmount:'',
  TotalTaxAmount:'',
  TotalPackAmount:'',
  BatchNo:'',
  IsManufactureDateAvailable:false,
  ManufactureDate:'',
  IsExpiryDateAvailable:false,
  ExpiryDate:'',
  DiscountMethod:'',
  DiscountType:'',
  Discount:'',
  FinalTotalPackTaxableAmount:'',
  FinalTotalTaxAmount:'',
  FinalTotalPackAmount:'',
})




const [POItemChange,setPOItemChange]=useState({
  PONumber: '',
  SupplierName: '',
  POItemId: '',
  ItemCode: '',
  ItemName: '',
  PurchasePack:'',
  OrderQty: '',
  ReceivedQty: '',
  BalanceQty: '',
  CancelQty:'',
  ItemStatus:'',
  Reason: '',
})

// ---------------------------------clear fun

const ClearGRNItemState =()=>{

  setGRNItemState({
    IsFOCProduct:false,  
    FOCItemCode:'',
    FOCItemName:'',
    GRNMRP:'',  
    PurchaseRateTaxable:'',   
    TaxType:'',
    TaxPercentage:'',
    PurchaseRateWithTax:'',
    OrderQty:'',
    BillQty:'',
    ReceivedQty:'',  
    PendingQty:'', 
    ExtraQty:'',
    IsFOCQtyAvailable:false, 
    FOCQty:'',
    TotalPackQty:'',
    IsMRPAsSellablePrice:true,
    SellablePrice:'',
    SellableQtyPrice:'',
    TotalPackTaxableAmount:'',
    TotalTaxAmount:'',
    TotalPackAmount:'',
    BatchNo:'',
    IsManufactureDateAvailable:false,
    ManufactureDate:'',
    IsExpiryDateAvailable:false,
    ExpiryDate:'',
    DiscountMethod:'',
    DiscountType:'',
    Discount:'',
    FinalTotalPackTaxableAmount:'',
    FinalTotalTaxAmount:'',
    FinalTotalPackAmount:'',
  })

}

const ClearItemFulldetailes =()=>{

  setItemFulldetailes({
    NotInPurchaseOrder:false,
    ItemCode:'',
    ItemName:'',    
    IsSellable:'',
  }) 

}




const clearRemovedata =()=>{
  setPOItemChange({
    PONumber: '',
    SupplierName: '',
    POItemId: '',
    ItemCode: '',
    ItemName: '',
    PurchasePack:'',
    OrderQty: '',
    ReceivedQty: '',
    BalanceQty: '',
    CancelQty:'',
    ItemStatus:'',
    Reason: '',
  })
}




useEffect(() => {
  axios.get(`${UrlLink}Masters/Location_Detials_link`)
      .then((res) => {
          const ress = res.data
          setLocationData(ress)
      })
      .catch((err) => {
          console.log(err);
      })


}, [UrlLink])


// ------------------------Total Amount-------------------


useEffect(()=>{

  if(GRNItemlist && GRNItemlist.length !==0){

    // console.log('veerrr',GRNItemlist, GRNItemlist.length !==0);
    

    let STotalTaxableAmount= 0;
    let STotalTaxAmount = 0;
    let STotalAmount =0;
    

    GRNItemlist.forEach((item)=>{
      STotalTaxableAmount += +item.FinalTotalPackTaxableAmount;
      STotalTaxAmount += +item.FinalTotalTaxAmount;
      STotalAmount += +item.FinalTotalPackAmount;
    })

    const OneConv1 = Math.round(STotalAmount).toFixed(2);
    const SecConv1 = OneConv1 - STotalAmount;

    setAmountstate((prev)=>({
      ...prev,
      TotalTaxableAmount:STotalTaxableAmount.toFixed(2),
      TotalTaxAmount:STotalTaxAmount.toFixed(2),
      TotalAmount:STotalAmount.toFixed(2),
      FinalTotalTaxableAmount:STotalTaxableAmount.toFixed(2),
      FinalTotalTaxAmount:STotalTaxAmount.toFixed(2),
      FinalTotalAmount:STotalAmount.toFixed(2),
      RoundOff:SecConv1.toFixed(2),
      NetAmount:OneConv1,
    }))

  }
  else{

    setAmountstate({
      TotalTaxableAmount:'',
      TotalTaxAmount:'',
      TotalAmount:'',
      TotalDiscountMethod:'',
      TotalDiscountType:'',
      TotalDiscount:'',
      FinalTotalTaxableAmount:'',
      FinalTotalTaxAmount:'',
      FinalTotalAmount:'',
      RoundOff:'',
      NetAmount:'',
    })
  }

},[GRNItemlist])




useEffect(() => {

  if(GRNItemlist.length !==0 && Amountstate.TotalAmount !==''){

  let checkdis=GRNItemlist?.some(ele=> +ele.Discount !== 0) 
  

  if(checkdis && Amountstate.TotalDiscountMethod !== '' && Amountstate.TotalDiscount !==''){
    
      let discapply=GRNItemlist.filter(ele=>ele.Discount !=='')

      let discNotapply=GRNItemlist.filter(ele=>ele.Discount ==='')

      // console.log('Dis22',discNotapply,discapply);

      let DiscApplay_TotalTaxableAmount= 0;
      let DiscApplay_TotalTaxAmount = 0;
      let DiscApplay_TotalAmount =0;

      let DiscNotApplay_TotalTaxableAmount= 0;
      let DiscNotApplay_TotalTaxAmount = 0;
      let DiscNotApplay_TotalAmount =0;

      if (discapply.length !==0){

        discapply.forEach((item)=>{
          DiscApplay_TotalTaxableAmount += +item.FinalTotalPackTaxableAmount;
          DiscApplay_TotalTaxAmount += +item.FinalTotalTaxAmount;
          DiscApplay_TotalAmount += +item.FinalTotalPackAmount;
        })
        
      }
      if (discNotapply.length !==0){

        discNotapply.forEach((item)=>{
          DiscNotApplay_TotalTaxableAmount += +item.FinalTotalPackTaxableAmount;
          DiscNotApplay_TotalTaxAmount += +item.FinalTotalTaxAmount;
          DiscNotApplay_TotalAmount += +item.FinalTotalPackAmount;
        })
        
      }

    if (Amountstate.TotalDiscountMethod === 'BeforeTax') {
    
      let TotalNet = +DiscNotApplay_TotalTaxableAmount || 0;
      
      if (Amountstate.TotalDiscountType === 'Cash') {
        TotalNet -= +Amountstate.TotalDiscount;
      }else if (Amountstate.TotalDiscountType === 'Percentage') {
        TotalNet -= TotalNet * (+Amountstate.TotalDiscount / 100);
      }
    
      const TtaxAmount = (TotalNet * +DiscNotApplay_TotalTaxAmount) / +DiscNotApplay_TotalTaxableAmount;
      const NetTotal = TotalNet + TtaxAmount;
      // console.log(DiscApplay_TotalTaxAmount,TtaxAmount,'000000');
      
      const BT_TaxableTotal=DiscApplay_TotalTaxableAmount + TotalNet
      const BT_TaxTotal=DiscApplay_TotalTaxAmount + TtaxAmount
      const BT_NetTotal=DiscApplay_TotalAmount + NetTotal

      const OneConv1 = Math.round(BT_NetTotal).toFixed(2);
      const SecConv1 = OneConv1 - BT_NetTotal;



      console.log('ssssssssss111',BT_TaxableTotal,BT_TaxTotal,BT_NetTotal);
      
      
      setAmountstate((prev) => ({
        ...prev,
        FinalTotalTaxableAmount: BT_TaxableTotal.toFixed(2),
        FinalTotalTaxAmount: BT_TaxTotal.toFixed(2),
        FinalTotalAmount: BT_NetTotal.toFixed(2),
        RoundOff: SecConv1.toFixed(2),
        NetAmount: OneConv1,
      }));
    
    }

    else if (Amountstate.TotalDiscountMethod === 'AfterTax') {
      let FinTotal = +DiscNotApplay_TotalAmount || 0;
  
      if (Amountstate.TotalDiscountType === 'Cash') {
        FinTotal -= +Amountstate.TotalDiscount;
      } else if (Amountstate.TotalDiscountType === 'Percentage') {
        FinTotal -= FinTotal * (+Amountstate.TotalDiscount / 100);
      }

      const AftNetamount=DiscApplay_TotalAmount + FinTotal
  
      const OneConv1 = Math.round(AftNetamount).toFixed(2);
      const SecConv1 = OneConv1 - AftNetamount;


      setAmountstate((prev) => ({
        ...prev,
        FinalTotalTaxableAmount: (+Amountstate.TotalTaxableAmount).toFixed(2),
        FinalTotalTaxAmount: (+Amountstate.TotalTaxAmount).toFixed(2),
        FinalTotalAmount: AftNetamount.toFixed(2),
        RoundOff: SecConv1.toFixed(2),
        NetAmount: OneConv1,
      }));
    }
      

    

  }
  //  --------------------------------------------------

  else if (Amountstate.TotalDiscountMethod === 'BeforeTax'&& Amountstate.TotalDiscount !=='') {

  
    let TotalNet = +Amountstate.TotalTaxableAmount || 0;
  if (Amountstate.TotalDiscountType === 'Cash') {
    TotalNet -= +Amountstate.TotalDiscount;
  } else if (Amountstate.TotalDiscountType === 'Percentage') {
    TotalNet -= TotalNet * (+Amountstate.TotalDiscount / 100);
  }

  const TtaxAmount = (TotalNet * +Amountstate.TotalTaxAmount) / +Amountstate.TotalTaxableAmount;
  const NetTotal = TotalNet + TtaxAmount;

  const OneConv1 = Math.round(NetTotal).toFixed(2);
  const SecConv1 = OneConv1 - NetTotal;

  setAmountstate((prev) => ({
    ...prev,
    FinalTotalTaxableAmount: TotalNet.toFixed(2),
    FinalTotalTaxAmount: TtaxAmount.toFixed(2),
    FinalTotalAmount: NetTotal.toFixed(2),
    RoundOff: SecConv1.toFixed(2),
    NetAmount: OneConv1,
  }));
  } 
  else if (Amountstate.TotalDiscountMethod === 'AfterTax'&& Amountstate.TotalDiscount !=='') {

    
    let FinTotal = +Amountstate.TotalAmount || 0;

  if (Amountstate.TotalDiscountType === 'Cash') {
    FinTotal -= +Amountstate.TotalDiscount;
  } else if (Amountstate.TotalDiscountType === 'Percentage') {
    FinTotal -= FinTotal * (+Amountstate.TotalDiscount / 100);
  }

  const OneConv1 = Math.round(FinTotal).toFixed(2);
  const SecConv1 = OneConv1 - FinTotal;


  setAmountstate((prev) => ({
    ...prev,
    FinalTotalTaxableAmount: (+Amountstate.TotalTaxableAmount).toFixed(2),
    FinalTotalTaxAmount: (+Amountstate.TotalTaxAmount).toFixed(2),
    FinalTotalAmount: FinTotal.toFixed(2),
    RoundOff: SecConv1.toFixed(2),
    NetAmount: OneConv1,
  }));
  }
  
  else {

    const OneConv1 = Math.round(+Amountstate.TotalAmount).toFixed(2);
    const SecConv1 = OneConv1 - +Amountstate.TotalAmount;

    // console.log('111',Amountstate.TotalTaxableAmount);
    // console.log('222',Amountstate.TotalTaxAmount);
    // console.log('333',Amountstate.TotalAmount);

    setAmountstate((prev) => ({
      ...prev,
      FinalTotalTaxableAmount: Amountstate.TotalTaxableAmount,
      FinalTotalTaxAmount: Amountstate.TotalTaxAmount,
      FinalTotalAmount: Amountstate.TotalAmount,
      RoundOff: SecConv1.toFixed(2),
      NetAmount: OneConv1,
    }));

  }
}
}, [Amountstate.TotalDiscount, Amountstate.TotalDiscountMethod, Amountstate.TotalDiscountType,Amountstate.TotalAmount,GRNItemlist]);





// ------------------------------------------------------




const formatLabel = (label) => {

  if (/[a-z]/.test(label) && /[A-Z]/.test(label) && !/\d/.test(label)) {
      return label
          .replace(/([a-z])([A-Z])/g, "$1 $2")
          .replace(/^./, (str) => str.toUpperCase());
  } else {
      return label;
  }
};



const getInputType = (name) => {
  if(['GRNDate','SupplierBillDate','SupplierBillDueDate'].includes(name)) return 'date';
  if (['SupplierBillAmount'].includes(name)) return 'number';
  return 'text';
  };

// -------------------------useEffect LOcation datas




useEffect(()=>{




  if(GRNState.GRNLocation && GRNState.GRNLocation !== ''){


    console.log('----????',GRNState.GRNLocation);
    

    axios.get(`${UrlLink}Masters/Inventory_Master_Detials_link?SearchLocation=${GRNState.GRNLocation}`)
    .then((res) => {
        const ress = res.data
        // console.log('vvvv',res.data);
        
        setStoreData(ress)
    })
    .catch((err) => {
        console.log(err);
    })
   }

},[GRNState.GRNLocation])




useEffect(() => {
  if(ItemFulldetailes.NotInPurchaseOrder && GRNState.SupplierCode !=='' &&  POItemArrays.length !==0 ){ 
      
      const POitems=POItemArrays?.map(ele => +ele.ItemCode)
      
      axios.get(`${UrlLink}Inventory/PO_SupplierWise_product_Get?SupplierId=${GRNState.SupplierCode}&POitems=${POitems}`)
      .then((res) => {
          let data = res.data

          if (Array.isArray(data) && data.length !== 0) {
             
              // console.log(data,'---++---');
              
              setNewItemProductArray(data)
          }
          else {
              setNewItemProductArray([])
          }

      })
      .catch((err) => {
          console.log(err)
      })
  }
  

}, [UrlLink,GRNState,POItemArrays,ItemFulldetailes])



useEffect(() => {
  if(GRNState.SupplierCode !==''){ 
        
      axios.get(`${UrlLink}Inventory/PO_SupplierWise_product_Get?SupplierId=${GRNState.SupplierCode}&SupplierTwo=${true}`)
      .then((res) => {
          let data = res.data

          // console.log('345098',data);
          
          if (Array.isArray(data) && data.length !== 0) {
             
              // console.log(data,'---QQQQQQ111---');
              
              setSupplierProductArray(data)
          }
          else {
            setSupplierProductArray([])
          }

      })
      .catch((err) => {
          console.log(err)
      })
  }
  

}, [UrlLink,GRNState.SupplierCode])



// ----------------------------PO Item Data Grit AND  in useEffect




const HandelEditdata =(row)=>{

  // console.log('1111',row);

  const { id, 
    Item_Status,
    Reason , 
    Received_Qty,
    Balance_Qty,
    ItemCode,
    ItemName,
    Is_Manufacture_Date_Available,
    Is_Expiry_Date_Available,
    ...rest} = row ;

  setItemFulldetailes({
    NotInPurchaseOrder:false,
    ItemCode:ItemCode || '',
    ItemName:ItemName || '', 
    ...rest,    
  })

  setGRNItemState((prev) => ({
    ...prev,
    IsFOCProduct:false,
    GRNMRP: rest.MRP || '',
    PurchaseRateTaxable: rest.PurchaseRateBeforeGST || '',
    TaxPercentage: rest.GST || '',
    PurchaseRateWithTax: rest.PurchaseRateAfterGST || '',
    OrderQty: rest.PurchaseQty || '',
    BillQty:Balance_Qty || '', 
    IsManufactureDateAvailable:Is_Manufacture_Date_Available || false,
    IsExpiryDateAvailable:Is_Expiry_Date_Available || false
  }));

}



const HandelDeletePOdata =(row)=>{


  // console.log('[[[[[[[[row]]]]]]]]',row);
  
  setselectRoom2(true)

  setPOItemChange((prev)=>({
    ...prev,
    PONumber:GRNState.PONumber,
    SupplierName:GRNState.SupplierName,
    POItemId:row.id,
    ItemCode:row.ItemCode,
    ItemName:row.ItemName,
    PurchasePack:row.PackType,
    OrderQty:row.PurchaseQty,
    BalanceQty:row.Balance_Qty,
    ReceivedQty:row.Received_Qty,
    CancelQty:row.Balance_Qty,
  }))

  

}




const PoItemcolumn=[
  {
    key:'id',
    name:'PO Item Id',
    frozen:true
  },
  {
    key:'ItemCode',
    name:'Item Code',
    frozen:true
  },
  {
    key:'ItemName',
    name:'Item Name',
    frozen:true
  },
  {
    key:'ProductCategory',
    name:'Product Category',    
    frozen:true
  },
  {
    key:'SubCategory',
    name:'Sub Category',    
    frozen:true
  },
  {
    key:'GenericName',
    name:'Generic Name',
    
  },
  {
    key:'ManufacturerName',
    name:'Manufacturer Name',
  },
  {
    key:'HSNCode',
    name:'HSN Code',
  },
  {
    key:'Strength',
    name:'Strength'
  },
  {
    key:'StrengthType',
    name:'StrengthType',
  },
  {
    key:'Volume',
    name:'Volume',
  },
  {
    key:'VolumeType',
    name:'Volume Type',
  },
  {
    key:'PackType',
    name:'Pack Type',
  },
  {
    key:'PackQty',
    name:'Pack Qty',
  },
  {
    key:'PurchaseQty',
    name:'Purchase Qty'
  },
  {
    key:'Received_Qty',
    name:'Received Qty'
  },
  {
    key:'Balance_Qty',
    name:'Balance Qty'
  },
  {
    key:'Action',
    name:'Action',
    renderCell:(params) =>(
      +params.row.Balance_Qty === 0 ?
      <>
      No Action
      </>
      :
      <div style={{display:'flex'}}>
      <Button className="cell_btn" 
        onClick={()=>HandelEditdata(params.row)}               
        >
        <EditIcon className="check_box_clrr_cancell" />
        </Button>

        <Button className="cell_btn" 
        onClick={()=>HandelDeletePOdata(params.row)}               
        >
        <DeleteOutlineIcon className="check_box_clrr_cancell" />
        </Button>
      </div>
    )
  }



]




// -------------------File Onchange and viwe



const handlefileOnchange =(e)=>{

  const { name, value, files } = e.target


  if (files && files.length > 0) {
    let formattedValue = files[0];

    const allowedTypes = ['application/pdf', 'image/jpeg', 'image/png'];
    const maxSize = 5 * 1024 * 1024; // Example max size of 5MB
    if (!allowedTypes.includes(formattedValue.type) || formattedValue.type === '') {
  
        const tdata = {
            message: 'Invalid file type. Please upload a PDF, JPEG, or PNG file.',
            type: 'warn'
        };
        dispatchvalue({ type: 'toast', value: tdata });

    } else {
        if (formattedValue.size > maxSize) {
            const tdata = {
                message: 'File size exceeds the limit of 5MB.',
                type: 'warn'
            };
            dispatchvalue({ type: 'toast', value: tdata });

        } else {
            const reader = new FileReader();
            reader.onload = () => {
              setSupplierBillfile(reader.result)
               
            };
            reader.readAsDataURL(formattedValue);




        }
    }

} else {
    const tdata = {
        message: 'No file selected. Please choose a file to upload.',
        type: 'warn'
    };
    dispatchvalue({ type: 'toast', value: tdata });
}

}


const Selectedfileview = (fileval) => {
  // console.log('fileval',fileval);
  
  if (fileval) {
      let tdata = {
          Isopen: false,
          content: null,
          type: 'image/jpg'
      };
      if (['data:image/jpeg;base64', 'data:image/jpg;base64'].includes(fileval?.split(',')[0])) {
          tdata = {
              Isopen: true,
              content: fileval,
              type: 'image/jpeg'
          };
      } else if (fileval?.split(',')[0] === 'data:image/png;base64') {
          tdata = {
              Isopen: true,
              content: fileval,
              type: 'image/png'
          };
      } else if (fileval?.split(',')[0] === 'data:application/pdf;base64') {
          tdata = {
              Isopen: true,
              content: fileval,
              type: 'application/pdf'
          };
      }

      dispatchvalue({ type: 'modelcon', value: tdata });
  } else {
      const tdata = {
          message: 'There is no file to view.',
          type: 'warn'
      };
      dispatchvalue({ type: 'toast', value: tdata });
  }
}


// -----------------GRN Edit --------------------------------


useEffect(()=>{
  
  if(Editdata && Object.keys(Editdata).length !==0 && Object.keys(POdata).length === 0){

    axios.get(`${UrlLink}Inventory/PO_Goods_Reciept_Note_GET_Details_link?GRN_Number=${Editdata.GRN_Number}`)
    .then((res)=>{
      console.log(res.data,'{{{{{{{{'); 

      let getdata = res.data

      setGRNState({
      GRNNumber:getdata?.id,
      GRNDate:getdata?.GrnDate,
      PONumber:getdata?.Purchase_order_Detials,
      SupplierCode:getdata?.SupplierCode,
      SupplierName:getdata?.SupplierName,
      SupplierBillNumber:getdata?.Supplier_Bill_Number,
      SupplierBillDate:getdata?.Supplier_Bill_Date,
      SupplierBillDueDate:getdata?.Supplier_Bill_Due_Date,
      SupplierBillAmount:getdata?.Supplier_Bill_Amount,
      GRNLocation:getdata?.GRNLocation,
      StorageLocation:getdata?.Store_location_pk,
      ReceivingPersonName:getdata?.Received_person,
      IsFOCAvailable:getdata?.Is_Foc_Available,
      FOCMethod:getdata?.Foc_Method,
      })

      setSupplierBillfile(getdata?.FileAttachment)
      
      setAmountstate({
      TotalTaxableAmount:+getdata?.Taxable_Amount,
      TotalTaxAmount:+getdata?.Tax_Amount,
      TotalAmount:+getdata?.Total_Amount,
      TotalDiscountMethod:getdata?.Total_Discount_Method,
      TotalDiscountType:getdata?.Total_Discount_Type,
      TotalDiscount:+getdata?.Discount_Amount,
      FinalTotalTaxableAmount:+getdata?.Final_Taxable_Amount,
      FinalTotalTaxAmount:+getdata?.Final_Tax_Amount,
      FinalTotalAmount:+getdata?.Final_Total_Amount ,
      RoundOff:+getdata?.Round_off_Amount,
      NetAmount:+getdata?.Net_Amount
    })

    setGRNItemlist(getdata?.GRN_Items)

    console.log('PO_Items',getdata.PO_Items);
    
    setPOItemArrays(getdata?.PO_Items)



    })
    .catch((err)=>{
      console.log(err);
      
    })


    




    //   console.log('??/',Editdata.Final_Tax_Amount);


    

  }

},[POdata,Editdata])



// -----------------------GRN Head Detailes----------------



useEffect(()=>{

  if(POdata && Object.keys(POdata).length !==0 && Object.keys(Editdata).length === 0)
  {

    console.log('POdata----',POdata);
    

    axios.get(`${UrlLink}Inventory/Supplier_Master_Link?SupplierId=${POdata.SupplierId}`)
    .then((res)=>{
        // console.log('pppp',res.data);
        let Objdata=res.data

        if (Objdata){

          const paymentTermsDays = Objdata.PaymentTerms;  
          const supplierBillDate = new Date(GRNState.GRNDate);
          const dueDate = new Date(supplierBillDate);
          dueDate.setDate(supplierBillDate.getDate() + paymentTermsDays);

          const formattedDueDate = dueDate.toISOString().split('T')[0];

          setGRNState((prev)=>({
            ...prev,
            PONumber:POdata.id,
            SupplierCode:POdata.SupplierId,
            SupplierName:POdata.SupplierName,     
            SupplierBillDueDate: formattedDueDate,
            GRNLocation:POdata.ShippingLocation,
          }))
        }
        // console.log(POdata.Item_Details,'oooo9999999');
        
        if(POdata.Item_Details.length !==0){
          setPOItemArrays(POdata.Item_Details)
        }

    })
    .catch((err)=>{
        console.log(err);
        
    })

    

   

  }

},[POdata,Editdata])




const HandeleOnchange=(e)=>{


  const { name, value, type, checked } = e.target;

  if(name === 'SupplierBillNumber'){
    setGRNState((prev)=>({
      ...prev,
      [name]:value.toUpperCase(),
    }))
  }
  else if(name === 'SupplierBillDate') {

    setGRNState((prev) => ({
        ...prev,
        [name]: value,
    }));
  }
  else if(name === 'IsFOCAvailable') {

    setGRNState((prev) => ({
        ...prev,
        [name]: value === 'Yes',
        FOCMethod:'',
    }));
  }
  else if(name==='FOCMethod'){

    setGRNState((prev) => ({
      ...prev,
      [name]: value ,   
     }));
  }

  else
  {
    setGRNState((prev)=>({
      ...prev,
     [name]: type === 'checkbox' ? checked : value,
    }))

  }

}


// -------------------------PO Item Entry detailes


const HandeleOnchangePOItem =(e)=>{



  const { name, value, type, checked } = e.target;


  if(name === 'NotInPurchaseOrder') {

    setItemFulldetailes({
        [name]: value === 'Yes',
        ItemCode:'',
        ItemName:'',        
        IsSellable:'',
    });
  }
  else if (name === 'ItemCode'){

    let find = NewItemProductArray.find((ele)=> ''+ele.ItemCode === ''+value)

    if (find){

        let {ItemCode,ItemName,
          Is_Manufacture_Date_Available,
          Is_Expiry_Date_Available,...rest} =find;

        setItemFulldetailes({
            NotInPurchaseOrder:true,
            [name]:value,
            ItemName:ItemName || '',
            ...rest,
        })

        setGRNItemState((prev)=>({
          ...prev,
          GRNMRP:rest.MRP || '',
          PurchaseRateTaxable:rest.PurchaseRateBeforeGST || '',
          TaxPercentage:rest.GST || '',
          PurchaseRateWithTax:rest.PurchaseRateAfterGST || '',
          IsManufactureDateAvailable:Is_Manufacture_Date_Available || false,
          IsExpiryDateAvailable:Is_Expiry_Date_Available || false
        }))


    } 
    else{

      setItemFulldetailes({ 
            NotInPurchaseOrder:true,   
            [name]:value,
            ItemName:'',             
        })

    }
    
}
else if(name === 'ItemName'){

    let find = NewItemProductArray.find((ele)=>ele.ItemName === value)

    if (find){

      let {ItemCode,ItemName,
        Is_Manufacture_Date_Available,
        Is_Expiry_Date_Available,...rest} =find;


        setItemFulldetailes({ 
            NotInPurchaseOrder:true,               
            ItemCode:ItemCode || '',
            [name]:value,
            ...rest,
        })


        setGRNItemState((prev)=>({
          ...prev,
          GRNMRP:rest.MRP || '',
          PurchaseRateTaxable:rest.PurchaseRateBeforeGST || '',
          TaxPercentage:rest.GST || '',
          PurchaseRateWithTax:rest.PurchaseRateAfterGST || '',
          IsManufactureDateAvailable:Is_Manufacture_Date_Available || false,
          IsExpiryDateAvailable:Is_Expiry_Date_Available || false
        }))
    } 
    else{

      setItemFulldetailes({
            NotInPurchaseOrder:true, 
            ItemCode:'',     
            [name]:value,     
        })

    }

}

 else{

  setItemFulldetailes((prev)=>({
    ...prev,
    [name]: type === 'checkbox' ? checked : value,
  }))

 }


}


// ------------------------Item Entry Detailes




const HandelItemstate = (e) => {

  
  const { name, value, type, checked } = e.target;

  if (name === 'ReceivedQty' ) {
 
    
   
    if (!GRNItemState.ExtraQty && +GRNItemState.BillQty < +value && !ItemFulldetailes.NotInPurchaseOrder) {
      

      const ExtraReciveQty = window.confirm('Are you sure you want to receive a quantity greater than the ordered quantity? Confirm to proceed with this quantity.');

      if(!ExtraReciveQty) {
        return;
      }

    }

    // console.log(+GRNItemState.BillQty < +value,+GRNItemState.BillQty,+value,'eeeee12345');
    

    const PendQty = !ItemFulldetailes.NotInPurchaseOrder ? +GRNItemState.BillQty < +value ?  '' : +GRNItemState.BillQty - +value :'';
    
    const ExtQty = !ItemFulldetailes.NotInPurchaseOrder ? +GRNItemState.BillQty < +value ?  +value - +GRNItemState.BillQty : '' :'';
    
      const TotalQty = +ItemFulldetailes.PackQty * +value;

    const MRP_condition=ItemFulldetailes.IsSellable === 'Yes' ? (+GRNItemState.GRNMRP).toFixed(2) : ''

    const TotaQtyMrp = +ItemFulldetailes.PackQty === +ItemFulldetailes.LeastSellableUnit
    ? +GRNItemState.GRNMRP
    : +GRNItemState.GRNMRP / +ItemFulldetailes.PackQty ;

    const Total_Qty_MRP_condition=ItemFulldetailes.IsSellable === 'Yes' ? TotaQtyMrp.toFixed(2) : ''


    const TotalPackTaxableAmount = GRNItemState.PurchaseRateTaxable * +value;
    const TaxAmount = TotalPackTaxableAmount * (GRNItemState.TaxPercentage / 100);
    const TotalPackAmount = GRNItemState.PurchaseRateWithTax * +value;

    setGRNItemState((prev) => ({
      ...prev,
      [name]: value,
      PendingQty: value ? PendQty : '',
      ExtraQty:value ? ExtQty : '',
      IsFOCQtyAvailable:false,
      FOCQty:'',
      TotalPackQty: value ? TotalQty : '',
      SellablePrice:value ? MRP_condition : '',
      SellableQtyPrice:value ? Total_Qty_MRP_condition : '',
      TotalPackTaxableAmount: value ? TotalPackTaxableAmount.toFixed(2) : '',
      TotalTaxAmount: value ? TaxAmount.toFixed(2) : '',
      TotalPackAmount: value ? TotalPackAmount.toFixed(2) : '',
      FinalTotalPackTaxableAmount:value ? TotalPackTaxableAmount.toFixed(2) : '',
      FinalTotalTaxAmount:value ? TaxAmount.toFixed(2) : '',
      FinalTotalPackAmount:value ? TotalPackAmount.toFixed(2) : '',
    }));

    return;
  }

  if (name === 'GRNMRP') {
    const SellableQtyPrice = +ItemFulldetailes.PackQty === +ItemFulldetailes.LeastSellableUnit
      ? +value || ''
      : value ? (+value / +ItemFulldetailes.PackQty).toFixed(2) : '';

    const MRP_condition=ItemFulldetailes.IsSellable === 'Yes' ? +value.toFixed(2) : ''
    
    const Total_Qty_MRP_condition=ItemFulldetailes.IsSellable === 'Yes' ? SellableQtyPrice.toFixed(2) : ''


    setGRNItemState((prev) => ({
      ...prev,
      [name]: value,
      SellablePrice:MRP_condition,
      SellableQtyPrice:Total_Qty_MRP_condition,
    }));

    return;
  }

  if (name === 'PurchaseRateTaxable') {
    setGRNItemState((prev) => ({
      ...prev,
      [name]: value,
      TaxType:'',
      TaxPercentage:'',
      PurchaseRateWithTax:'',
      ReceivedQty:'',  
      PendingQty:'',   
      ExtraQty:'',
      TotalPackQty:'',
      TotalPackTaxableAmount:'',
      TotalTaxAmount:'',
      TotalPackAmount:'',
      DiscountMethod:'',
      DiscountType:'',
      Discount:'',
      FinalTotalPackTaxableAmount:'',
      FinalTotalTaxAmount:'',
      FinalTotalPackAmount:'',  
    }));

    return;
  }

  if (name === 'TaxPercentage') {
    const TaxAmount = +GRNItemState.PurchaseRateTaxable * (+value / 100);
    const TotalPackAmount = +GRNItemState.PurchaseRateTaxable + TaxAmount;

    setGRNItemState((prev) => ({
      ...prev,
      [name]: value,
      PurchaseRateWithTax: TotalPackAmount.toFixed(2),
      ReceivedQty:'',  
      PendingQty:'',
      ExtraQty:'',   
      TotalPackQty:'',
      TotalPackTaxableAmount:'',
      TotalTaxAmount:'',
      TotalPackAmount:'',
      DiscountMethod:'',
      DiscountType:'',
      Discount:'',
      FinalTotalPackTaxableAmount:'',
      FinalTotalTaxAmount:'',
      FinalTotalPackAmount:'',    
    }));

    return;
  }

  if (name === 'BatchNo') {

    setGRNItemState((prev) => ({
      ...prev,
      [name]: value.toUpperCase(),
    }));

    return;
  }

  if (name === 'DiscountMethod') {

    setGRNItemState((prev) => ({
      ...prev,
      [name]: value,
      DiscountType:'',
      Discount:'',
      FinalTotalPackTaxableAmount: +GRNItemState.TotalPackTaxableAmount || '',
      FinalTotalTaxAmount: +GRNItemState.TotalTaxAmount || '',
      FinalTotalPackAmount:+GRNItemState.TotalPackAmount || '',
    }));


  return;
  }

  if (name === 'DiscountType') {

    setGRNItemState((prev) => ({
      ...prev,
      [name]: value,
      Discount:'',
      FinalTotalPackTaxableAmount: +GRNItemState.TotalPackTaxableAmount || '',
      FinalTotalTaxAmount: +GRNItemState.TotalTaxAmount || '',
      FinalTotalPackAmount: +GRNItemState.TotalPackAmount || '',
    }));


  return;
  }



 if (name === 'Discount') {

  
    if (GRNItemState.DiscountMethod === 'BeforeTax') {
      let TotalPackAm = +GRNItemState.TotalPackTaxableAmount;

      if (GRNItemState.DiscountType === 'Cash') {
        TotalPackAm -= +value;
      } else if (GRNItemState.DiscountType === 'Percentage') {
        TotalPackAm -= TotalPackAm * (+value / 100);
      }

      const TaxAmount = TotalPackAm * (GRNItemState.TaxPercentage / 100);
      const TotalPackAmount = TotalPackAm + TaxAmount;

      setGRNItemState((prev) => ({
        ...prev,
        [name]: value,
        FinalTotalPackTaxableAmount: TotalPackAm.toFixed(2) || '',
        FinalTotalTaxAmount: TaxAmount.toFixed(2) || '',
        FinalTotalPackAmount: TotalPackAmount.toFixed(2) || '',
      }));
    }
    else if(GRNItemState.DiscountMethod === 'AfterTax'){

      let TotalPackAm = +GRNItemState.TotalPackAmount 

      if (GRNItemState.DiscountType === 'Cash') {
        TotalPackAm -= +value;
      } else if (GRNItemState.DiscountType === 'Percentage') {
        TotalPackAm -= TotalPackAm * (+value / 100);
      }

      setGRNItemState((prev) => ({
        ...prev,
        [name]: value,
        FinalTotalPackTaxableAmount: +GRNItemState.TotalPackTaxableAmount || '',
        FinalTotalTaxAmount: +GRNItemState.TotalTaxAmount || '',
        FinalTotalPackAmount: TotalPackAm.toFixed(2) || '',
      }));

    }
  
  return;
  } 


  if(name === 'IsFOCProduct'){

    setGRNItemState((prev) => ({
      ...prev,
      [name]: value === 'Yes',
      FOCQty:'',   
    }));

    return;
  }

  // if(name === 'IsManufactureDateAvailable'){
  //   setGRNItemState((prev) => ({
  //     ...prev,
  //     [name]: value === 'Yes',
  //     ManufactureDate:'',
  //   }));

  //   return;
  // }

  // if(name === 'IsExpiryDateAvailable'){
  //   setGRNItemState((prev) => ({
  //     ...prev,
  //     [name]: value === 'Yes',
  //     ExpiryDate:'',
  //   }));

  //   return;
  // }

  if(name === 'IsFOCQtyAvailable'){

    let TotalQty = +ItemFulldetailes.PackQty * (+GRNItemState.ReceivedQty)

    setGRNItemState((prev) => ({
      ...prev,
      [name]: value === 'Yes',
      FOCQty:'',
      TotalPackQty:TotalQty ,
    }));

    return;
  }

  if(name === 'IsMRPAsSellablePrice'){

    const TotaQtyMrp = +ItemFulldetailes.PackQty === +ItemFulldetailes.LeastSellableUnit
    ? +GRNItemState.GRNMRP
    : +GRNItemState.GRNMRP / +ItemFulldetailes.PackQty ;

    setGRNItemState((prev) => ({
      ...prev,
      [name]: value === 'Yes',
      SellablePrice:(+GRNItemState.GRNMRP).toFixed(2) || '',
      SellableQtyPrice:TotaQtyMrp.toFixed(2),
    }));
    return;

  }

  if(name === 'FOCQty'){

    const TotalQty = value ? +ItemFulldetailes.PackQty * (+GRNItemState.ReceivedQty + +value) :
      +ItemFulldetailes.PackQty * (+GRNItemState.ReceivedQty)

    setGRNItemState((prev) => ({
      ...prev,
      [name]: value,
      TotalPackQty:TotalQty ,
    }));

    return;
  }

  if(name === 'SellablePrice'){

    const TotaQtyMrp = +ItemFulldetailes.PackQty === +ItemFulldetailes.LeastSellableUnit
    ? +value
    : +value / +ItemFulldetailes.PackQty ;

    setGRNItemState((prev) => ({
      ...prev,
      [name]: value,
      SellableQtyPrice:TotaQtyMrp.toFixed(2),
    }));

    return;
  }

  if (name === 'FOCItemCode'){

    let find = SupplierProductArray.find(ele =>''+ele.ItemCode === ''+value)
    
    setGRNItemState((prev) => ({
      ...prev,
      [name]: value,
      FOCItemName: find ? find.ItemName : '',
    }));
  
    return;
  }

  if (name === 'FOCItemName'){

    let find = SupplierProductArray.find(ele =>ele.ItemName === value)

    // console.log(find,value,'Foc itemmmmmm');
    
    setGRNItemState((prev) => ({
      ...prev,
      [name]: value,
      FOCItemCode: find ? find.ItemCode : '',
    }));

    return;
  }
  
  setGRNItemState((prev) => ({
    ...prev,
    [name]: type === 'checkbox' ? checked : value,
  }));

  
};


// --------------------------------------------------------------



const handelonAdd =()=>{



  let requiredFields = [
    'GRNMRP',
    'PurchaseRateTaxable',
    'TaxPercentage',
    'PurchaseRateWithTax',
    'ReceivedQty',
    'TotalPackQty',
    'TotalPackTaxableAmount',
    'TotalTaxAmount',
    'TotalPackAmount',
    'BatchNo',
  ];

  if(+GRNItemState.TaxPercentage !==0){
    requiredFields.push('TaxType')
  } 
  if (GRNItemState.IsFOCProduct && GRNState.FOCMethod !== 'Invoice' && GRNState.FOCMethod !== '') {
    requiredFields = requiredFields.filter(
      ele => ['BatchNo', 'TotalPackQty'].includes(ele)
    );
  }

  if(GRNItemState.IsManufactureDateAvailable) requiredFields.push('ManufactureDate')

  if(GRNItemState.IsExpiryDateAvailable) requiredFields.push('ExpiryDate')

  if(GRNItemState.IsFOCQtyAvailable) requiredFields.push('FOCQty')

  if(!GRNItemState.IsFOCProduct && ItemFulldetailes.IsSellable === 'Yes') requiredFields.push('SellableQtyPrice')
  
  

  let GRNItemStateFields = requiredFields.filter((field) => !GRNItemState[field]);

  if(GRNItemStateFields.length !== 0) {
    dispatchvalue({
      type: 'toast',
      value: {
        message: `Please fill out all required fields: ${GRNItemStateFields.join(", ")}`,
        type: 'warn',
      },
    });
  }
  else{

    const CheckDublicate =GRNItemlist.some((ele)=>ele.ItemCode === GRNItemState.ItemCode && ele.BatchNo === GRNItemState.BatchNo && +ele.id !== +GRNItemState.id)

    if(CheckDublicate){

      dispatchvalue({
        type: 'toast',
        value: {
          message: `This item with the same batch number has already been entered.`,
          type: 'warn',
        },
      });


    }
    else{ 
      
      const AdditemFun=()=>{

        // console.log('checking--log---',GRNItemState.ReceivedQty,GRNItemState.PendingQty,typeof(GRNItemState.PendingQty));
        

        const updatedPoItemlist = POItemArrays.map((ele) => {
          if (''+ele.ItemCode === ''+ItemFulldetailes.ItemCode) {
            
            // console.log(ele.ItemCode,ele.ItemName,'eeekkkkkkeee');
              if (+GRNItemState.BillQty < +GRNItemState.ReceivedQty){

                return {
                  ...ele,
                  Received_Qty:+ele.Received_Qty + +GRNItemState.ReceivedQty,
                  Balance_Qty: +GRNItemState.PendingQty,
                };

              }
              else{

                return {
                  ...ele,
                  Received_Qty: +ele.PurchaseQty - +GRNItemState.PendingQty,
                  Balance_Qty: +GRNItemState.PendingQty,
                };

              }
              
          }
          return ele;
        });
      
      
        //  console.log('222-eee',updatedPoItemlist);
         
  
          if(GRNItemState.id){
            
            setPOItemArrays(updatedPoItemlist)  
  
            setGRNItemlist((prev)=>
              prev.map((product)=> +product.id === +GRNItemState.id ?
             {NotInPurchaseOrder:ItemFulldetailes.NotInPurchaseOrder,
              ItemCode:ItemFulldetailes.ItemCode,
              ItemName:ItemFulldetailes.ItemName,
              ...GRNItemState} : 
             product)
            )
            ClearGRNItemState()
          }
          else{

          //  console.log('updatedPoItemlist',updatedPoItemlist);
  
           setPOItemArrays(updatedPoItemlist)
        
            setGRNItemlist((prev)=>[
              ...prev,
              { id:prev.length+1,
                NotInPurchaseOrder:ItemFulldetailes.NotInPurchaseOrder,
                ItemCode:ItemFulldetailes.ItemCode,
                ItemName:ItemFulldetailes.ItemName,
                ...GRNItemState}
            ])
            
            ClearGRNItemState() 

            ClearItemFulldetailes() 

  
          }
        
          setAmountstate((prev)=>({
            ...prev,
            TotalDiscountMethod:'',
            TotalDiscountType:'',
            TotalDiscount:'',
          }))
        
      }
      
      // console.log('000---0000',GRNItemState.PendingQty,typeof(GRNItemState.PendingQty))
      
      if(GRNItemState.PendingQty){  

        let confirmCon = window.confirm(`Are you sure pending Qty is ${GRNItemState.PendingQty} Can I proceed to add the product?`);
        
        if(confirmCon){
          AdditemFun()
        }
          
      }
      else{
        AdditemFun()
        
      }
      

    

    }

  }


}


// ----------------------------------------



const HandelGrnItemDeletedata = (row) => {


  // console.log('row---2D', row);
  // console.log('row---3D', +row.ReceivedQty, row.ItemCode);

  ClearGRNItemState()

  let ChangeQty = +row?.ReceivedQty; 
  let ChangeItemCode = row?.ItemCode;

  let ExtraQty=row?.ExtraQty;

  let UpdatePoItemlist = POItemArrays.map((ele) => {
    // console.log(ele.ItemCode ,'pppppp',ExtraQty,typeof(ExtraQty));


    if (''+ele.ItemCode === ''+ChangeItemCode) {
      ele.Balance_Qty = +ExtraQty !== 0 ? +ele.Balance_Qty + (ChangeQty - +ExtraQty)  : +ele.Balance_Qty + ChangeQty;
      ele.Received_Qty = +ele.Received_Qty - ChangeQty;
    }
    return ele;
  });

  setPOItemArrays(UpdatePoItemlist);

  let updatedGRNItemlist = GRNItemlist.filter((ele) => ele.id !== row.id);

  let reorderedGRNItemlist = updatedGRNItemlist.map((ele, index) => ({
    ...ele,
    id: index + 1, 
  }));

  setGRNItemlist(reorderedGRNItemlist);
};







const GRNItemcolumn=[
  {
    key:'id',
    name:'S.No',
    frozen:true
  },
  {
    key:'ItemCode',
    name:'Item Code',
    frozen:true
  },
  {
    key:'ItemName',
    name:'Item Name',
    frozen:true
  },
  {
    key:'IsFOCProduct',
    name:'Is FOC Product',
    renderCell:(params) =>(
      <div style={{display:'flex'}}>
          {params.row.IsFOCProduct?'Yes':'No'}
        </div>
    )
  },
  {
    key:'GRNMRP',
    name:'GRN MRP'
  },
  {
    key:'PurchaseRateTaxable',
    name:'Purchase Rate Taxable'
  },
  {
    key:'TaxType',
    name:'Tax Type'
  },
  {
    key:'TaxPercentage',
    name:'Tax Percentage'
  },
  {
    key:'PurchaseRateWithTax',
    name:'Purchase Rate WithTax'
  },
  {
    key:'OrderQty',
    name:'Order Qty'
  },
  {
    key:'ReceivedQty',
    name:'Received Qty'
  },
  {
    key:'PendingQty',
    name:'Pending Qty'
  },
  {
    key:'ExtraQty',
    name:'Extra Qty'
  },
  {
    key:'FOCQty',
    name:'FOC Qty'
  },
  {
    key:'TotalPackQty',
    name:'Total Pack Qty'
  },
  {
    key:'SellablePrice',
    name:'Sellable Price'
  },
  {
    key:'SellableQtyPrice',
    name:'Sellable Qty Price'
  },
  {
    key:'BatchNo',
    name:'Batch No',
  },
  {
    key:'ManufactureDate',
    name:'Manufacture Date',
  },
  {
    key:'ExpiryDate',
    name:'Expiry Date',
  },
  {
    key:'TotalPackTaxableAmount',
    name:'Total Taxable Amount'
  },
  {
    key:'TotalTaxAmount',
    name:'Total TaxAmount'
  },
  {
    key:'TotalPackAmount',
    name:'Total Amount'
  },
  {
    key:'DiscountMethod',
    name:'Discount Method',
  },
  {
    key:'DiscountType',
    name:'Discount Type',
  },
  {
    key:'Discount',
    name:'Discount',
  },
  {
    key:'FinalTotalPackTaxableAmount',
    name:'FinalTotalPackTaxableAmount',
  },
  {
    key:'FinalTotalTaxAmount',
    name:'FinalTotalTaxAmount',
  },
  {
    key:'FinalTotalPackAmount',
    name:'FinalTotalPackAmount',
  },
  {
    key:'Action',
    name:'Action',
    renderCell:(params) =>(
      <div style={{display:'flex'}}>
 
        <Button className="cell_btn" 
          onClick={()=>HandelGrnItemDeletedata(params.row)}               
          >
          <DeleteOutlineIcon className="check_box_clrr_cancell" />
          </Button>
        </div>
    )
  } 



]



const HandelAmountState=(e)=>{

  const {name,value}=e.target

  if(name === 'TotalDiscountMethod'){

    setAmountstate((prev)=>({
      ...prev,
      [name]:value,
      TotalDiscountType:'',
      TotalDiscount:'',
    }))

  }
  else if(name === 'TotalDiscountType'){

    setAmountstate((prev)=>({
      ...prev,
      [name]:value,
      TotalDiscount:'',
    }))
  }
 
  
  else{

    setAmountstate((prev)=>({
      ...prev,
      [name]:value,
    }))
  }

}





const HandleOnchangePORemoveQty =(e)=>{

  const { name, value }=e.target

  if(name === 'CancelQty'){

    const CancelQty = +POItemChange.OrderQty - +value

    setPOItemChange((prev)=>({
      ...prev,
      [name]:value,
      BalanceQty:value? +CancelQty :'',
    }))
  }
  else{
    setPOItemChange((prev)=>({
      ...prev,
      [name]:value,
    }))
  }

}



const RemoveQtyFun =()=>{

console.log('hiii',POItemChange);

let requiredFields = [
  'BalanceQty',
  'CancelQty',
  'ItemStatus',
  'Reason',
];

let POItemChangeStateFields = requiredFields.filter((field) => !POItemChange[field]);

if(POItemChangeStateFields.length !== 0) {
  dispatchvalue({
    type: 'toast',
    value: {
      message: `Please fill out all required fields: ${POItemChangeStateFields.join(", ")}`,
      type: 'warn',
    },
  });
}
else{
  
  const RemovePoItemlist=POItemArrays.filter((ele,ind)=>{
    if(''+ele.ItemCode === ''+POItemChange.ItemCode){  
      // console.log('POItemChange.ReceivedQty',POItemChange.ReceivedQty);
          
      +POItemChange.ReceivedQty > 0? ele.Balance_Qty = 0 : ele.Balance_Qty = +ele.PurchaseQty - +POItemChange.CancelQty
      ele.PurchaseQty = +ele.PurchaseQty - +POItemChange.CancelQty
      ele.Item_Status=POItemChange.ItemStatus
      ele.Reason=POItemChange.Reason
    } 
    return ele;

  })



  setPOItemArrays(RemovePoItemlist)

  setselectRoom2(false)

  clearRemovedata()

}


}





const SaveGRNfunc =()=>{

  let SupprequiredFields =[
    'SupplierBillNumber',
    'SupplierBillDate',
    'SupplierBillDueDate',
    'SupplierBillAmount',
    'StorageLocation',
    'ReceivingPersonName',
  ]

  if(GRNState.IsFOCAvailable) SupprequiredFields.push('FOCMethod')
  
  let SupplierField=SupprequiredFields.filter((field) => !GRNState[field])

  let PoItemlistcheck=POItemArrays.some((ele)=> +ele.Balance_Qty > 0)

  if(SupplierField.length !== 0) {
    dispatchvalue({
      type: 'toast',
      value: {
        message: `Please fill out all required fields: ${SupplierField.join(", ")}`,
        type: 'warn',
      },
    });
  }
  else if(PoItemlistcheck){

    dispatchvalue({
      type: 'toast',
      value: {
        message: `Please enter all quantities or cancel the items.`,
        type: 'warn',
      },
    });
  }
  else if(+GRNState.SupplierBillAmount !== +Amountstate.NetAmount){

    dispatchvalue({
      type: 'toast',
      value: {
        message: "Supplier Bill Amount and GRN Net Amount need to be the same.",
        type: 'warn',
      },
    });
  
  }
  else {

    let Senddata={
      GRNState:GRNState,
      POItemArrays:POItemArrays,
      SupplierBillfile:SupplierBillfile,
      GRNItemlist:GRNItemlist,
      Amountstate:Amountstate,
      Created_by:userRecord?.username
    }

    // console.log('Senddata-----',Senddata);
    

    axios.post(`${UrlLink}Inventory/PO_Goods_Reciept_Note_Details_link`,Senddata)
    .then((res)=>{
      console.log(res.data); 
      
      let resdata=res.data
      let type = Object.keys(resdata)[0]
      let mess = Object.values(resdata)[0]
      const tdata = {
          message: mess,
          type: type,
      }
      dispatchvalue({ type: 'toast', value: tdata });
      if(type ==='success'){
        navigate('/Home/GoodsReceiptNoteList');
        }
    })
    .catch((err)=>{
      console.log(err);
      
    })

  }


 }
 




  return (
    <>
    <div className="Main_container_app">
        <h3>Goods Receipt Note</h3>

        <br/>

        <div className="RegisFormcon_1">

          {
            Object.keys(GRNState).map((StateName,Index)=>{
              return(
                <div className="RegisForm_1" key={Index+'key'}>

                  <label htmlFor={StateName}>{formatLabel(StateName)} <span>:</span></label>


                  {
                   ['GRNLocation','StorageLocation','FOCMethod'].includes(StateName) ?

                  <select
                    id={StateName}
                    name={StateName}
                    value={GRNState[StateName]}
                    onChange={HandeleOnchange}
                    disabled={(!GRNState.IsFOCAvailable && StateName === 'FOCMethod') || (StateName === 'GRNLocation')}
                  >
                  <option value=''>Select</option>
                  {
                  StateName === 'GRNLocation' ?  
                  LocationData.map((ele,ind)=>(
                      <option key={ind+'key'} value={ele.id} >{ele.locationName}</option>
                  ))
                  :
                  StateName === 'StorageLocation' ?  
                  StoreData.map((ele,ind)=>(
                      <option key={ind+'key'} value={ele.id} >{ele.StoreName}</option>
                    ))
                    :
                    ['Invoice', 'Individual Item'].map((ele, ind) => (
                      <option key={ind + 'key'} value={ele} >{"For " + ele}</option>
                    ))

                  }
                  </select>
                  :
                  StateName === 'IsFOCAvailable' ?
                  (<div style={{ display: 'flex', justifyContent: 'flex-start', gap: '10px', width: '150px' }}>
                      <label style={{ width: 'auto' }} htmlFor={`${StateName}_yes`}>
                          <input
                              required
                              id={`${StateName}_yes`}
                              type="radio"
                              name={StateName}
                              value='Yes'
                              style={{ width: '15px' }}
                              checked={GRNState[StateName]}
                              onChange={HandeleOnchange}

                          />
                          Yes
                      </label>
                      <label style={{ width: 'auto' }} htmlFor={`${StateName}_No`}>
                          <input
                              required
                              id={`${StateName}_No`}
                              type="radio"
                              name={StateName}
                              value='No'
                              style={{ width: '15px' }}
                              checked={!GRNState[StateName]}
                              onChange={HandeleOnchange}
                          />
                          No
                      </label>
                  </div>
                  ) :

                  
                  <input
                    type={getInputType(StateName)}
                    id={StateName}
                    name={StateName}
                    value={GRNState[StateName]}
                    onChange={HandeleOnchange}
                    max={StateName === 'SupplierBillDate' ? currentDate:'' }
                    disabled={['SupplierBillDueDate', 'GRNDate', 'PONumber', 'SupplierCode', 'SupplierName'].includes(StateName)} 
                  />
                  }
                </div>

              )})
          }

        <>
        <div className="RegisForm_1">
        <label htmlFor='SupplierBillfile'>File Attachment :</label>
          <input
              type='file'
              name='SupplierBillfile'
              accept='image/jpeg,image/png,application/pdf'
              required
              id='SupplierBillfile'
              autoComplete='off'
              onChange={handlefileOnchange}
              style={{ display: 'none' }}
          />
          <div style={{ width: '150px', display: 'flex', justifyContent: 'space-around' }}>
              <label
                  htmlFor='SupplierBillfile'
                  className="RegisterForm_1_btns choose_file_update"
              >
                  Choose File
              </label>
              <button className='fileviewbtn' 
              onClick={() => Selectedfileview(SupplierBillfile)}
              >view</button>

            </div>
          </div>
        </>
        </div>
        <br/>
        <div className="common_center_tag">
          <span>PO PRODUCT LIST</span>
        </div>

        <div className='RegisFormcon_1 jjxjx_'>
        <ReactGrid columns={PoItemcolumn} RowData={POItemArrays} />
        </div>

   
          <div className="common_center_tag">
           <span>PO ITEM DETAILES</span>
          </div> 
          <br/>
          <div className="RegisFormcon_1">

            {
              Object.keys(ItemFulldetailes).length !==0 && Object.keys(ItemFulldetailes).map((StateName,Index)=>{
                return(
                  <div className="RegisForm_1" key={Index+'key'}>
                    <label htmlFor={StateName}>{formatLabel(StateName)} <span>:</span></label>
                    
                    
                   { StateName === 'NotInPurchaseOrder' ?
                    (<div style={{ display: 'flex', justifyContent: 'flex-start', gap: '10px', width: '150px' }}>
                        <label style={{ width: 'auto' }} htmlFor={`${StateName}_yes`}>
                            <input
                                required
                                id={`${StateName}_yes`}
                                type="radio"
                                name={StateName}
                                value='Yes'
                                style={{ width: '15px' }}
                                checked={ItemFulldetailes[StateName]}
                                onChange={HandeleOnchangePOItem}
                                disabled={POItemArrays.some(ele => ''+ele.ItemCode === ''+ItemFulldetailes.ItemCode)}
                            />
                            Yes
                        </label>
                        <label style={{ width: 'auto' }} htmlFor={`${StateName}_No`}>
                            <input
                                required
                                id={`${StateName}_No`}
                                type="radio"
                                name={StateName}
                                value='No'
                                style={{ width: '15px' }}
                                checked={!ItemFulldetailes[StateName]}
                                onChange={HandeleOnchangePOItem}
                                disabled={POItemArrays.some(ele => ''+ele.ItemCode === ''+ItemFulldetailes.ItemCode)}

                            />
                            No
                        </label>
                    </div>
                    ) :
                    
                    <>
                    <input 
                    type='text'
                    id={StateName}
                    name={StateName}
                    list={StateName+'List'}
                    value={ItemFulldetailes[StateName]}
                    onChange={HandeleOnchangePOItem}
                    disabled={!ItemFulldetailes.NotInPurchaseOrder ? StateName : !['ItemCode','ItemName'].includes(StateName)}
                    />
                    {['ItemCode','ItemName'].includes(StateName) &&
                    <datalist
                    id={StateName+'List'}
                    >                    
                    {
                    NewItemProductArray.map((option,index)=>(
                    <option key={index+'key'} value={StateName === 'ItemCode' ? option.ItemCode : option.ItemName}>                         
                    </option>
                    ))
                    } 
                    </datalist>
                    }

                    </>
                  }
                  </div>
                )
              })
            }

          </div>
          <br/>

          {ItemFulldetailes.ItemCode !=='' &&<>
          <div className="common_center_tag">
           <span>GRN ENTRY DETAILES</span>
          </div> 
          <br/>
          <div className="RegisFormcon_1">

            {
              Object.keys(ItemFulldetailes).length !==0 && ((GRNState.FOCMethod === 'Invoice' || GRNState.FOCMethod === '') || GRNItemState.IsFOCProduct === false ? ItemFulldetailes.IsSellable === 'No' ?Object.keys(GRNItemState).filter(ele => !['FOCItemCode','FOCItemName','IsMRPAsSellablePrice','SellablePrice','SellableQtyPrice'].includes(ele)) : Object.keys(GRNItemState).filter(ele => ele !== 'FOCItemCode' && ele !== 'FOCItemName') : Object.keys(GRNItemState).filter(ele => ['IsFOCProduct','FOCItemCode','FOCItemName','FOCQty','TotalPackQty','BatchNo','IsManufactureDateAvailable','ManufactureDate','IsExpiryDateAvailable','ExpiryDate'].includes(ele))) .map((StateName,Index)=>{
                return(
                  <div className="RegisForm_1" key={Index+'key'}>
                    <label htmlFor={StateName}>{StateName === 'IsMRPAsSellablePrice' ? 'Is MRP As Sellable Price' : formatLabel(StateName)} <span>:</span></label>
                  {[ 'IsFOCProduct' ,'IsFOCQtyAvailable','IsMRPAsSellablePrice','IsManufactureDateAvailable','IsExpiryDateAvailable' ].includes(StateName)?
                    (<div style={{ display: 'flex', justifyContent: 'flex-start', gap: '10px', width: '150px' }}>
                        <label style={{ width: 'auto' }} htmlFor={`${StateName}_yes`}>
                            <input
                                required
                                id={`${StateName}_yes`}
                                type="radio"
                                name={StateName}
                                value='Yes'
                                style={{ width: '15px' }}
                                checked={GRNItemState[StateName]}
                                onChange={HandelItemstate}
                                disabled={(POItemArrays.some(ele => ''+ele.ItemCode === ''+ItemFulldetailes.ItemCode) && StateName ==='IsFOCProduct') || 
                                  ((GRNState.FOCMethod === 'Invoice' || GRNState.FOCMethod === '') && StateName ==='IsFOCProduct')
                               || (GRNState.FOCMethod === '' && StateName ==='IsFOCQtyAvailable' ) || ['IsManufactureDateAvailable','IsExpiryDateAvailable'].includes(StateName) }
                            />
                            Yes
                        </label>
                        <label style={{ width: 'auto' }} htmlFor={`${StateName}_No`}>
                            <input
                                required
                                id={`${StateName}_No`}
                                type="radio"
                                name={StateName}
                                value='No'
                                style={{ width: '15px' }}
                                checked={!GRNItemState[StateName]}
                                onChange={HandelItemstate}
                                disabled={(POItemArrays.some(ele => ''+ele.ItemCode === ''+ItemFulldetailes.ItemCode) && StateName ==='IsFOCProduct') || 
                                  ((GRNState.FOCMethod === 'Invoice' || GRNState.FOCMethod === '') && StateName ==='IsFOCProduct')
                               || (GRNState.FOCMethod === '' && StateName ==='IsFOCQtyAvailable' ) || ['IsManufactureDateAvailable','IsExpiryDateAvailable'].includes(StateName)}
                            />
                            No
                        </label>
                    </div>
                    ) :
                    ['TaxType','TaxPercentage','DiscountMethod','DiscountType'].includes(StateName)?

                    <select
                    id={StateName}
                    name={StateName}
                    value={GRNItemState[StateName]} 
                    onChange={HandelItemstate}   
                    disabled={(GRNItemState.DiscountMethod === '' && StateName === 'DiscountType') ||
                    (GRNItemState.TotalPackTaxableAmount === '' && StateName === 'DiscountMethod') || (Amountstate.TotalDiscountMethod !== "" && StateName === 'DiscountMethod')}
                    >

                    <option value=''>Select</option>
                    { StateName === 'TaxType' ?
                    <>
                    <option value='GST'>GST</option>
                    <option value='IGST'>IGST</option>
                    </>
                    :

                    StateName === 'TaxPercentage' ?
                    <>
                    <option value='0'>0</option>
                    <option value='5'>5%</option>
                    <option value='12'>12%</option>
                    <option value='18'>18%</option>
                    <option value='28'>28%</option>
                    </>
                    :
                    StateName === 'DiscountMethod' ?
                    <>
                    <option value='BeforeTax'>Before Tax</option>
                    <option value='AfterTax'>After Tax</option>
                    </>
                    :
                    <>
                    <option value='Cash'>Cash</option>
                    <option value='Percentage'>Percentage</option>
                    </>
                    }
                    </select>

                    :
                    <>
                    <input 
                    type={['ManufactureDate','ExpiryDate'].includes(StateName) ? 'date' : ['FOCItemCode','FOCItemName','BatchNo'].includes(StateName)? 'text' :'number'}
                    id={StateName}
                    name={StateName}
                    list={StateName+'List'}
                    value={GRNItemState[StateName]}
                    onChange={HandelItemstate}   
                    min={StateName === 'ExpiryDate' ? currentDate :''} 
                    max={StateName === 'ManufactureDate' ? currentDate :''}
                    readOnly={(!['FOCItemCode','FOCItemName','GRNMRP','PurchaseRateTaxable','TaxType','TaxPercentage','PurchaseRateWithTax','ReceivedQty','FOCQty',
                      'SellablePrice','BatchNo','ManufactureDate','ExpiryDate','DiscountMethod','DiscountType','Discount'].includes(StateName))}  
                    disabled={(GRNItemState.DiscountType === '' && StateName === 'Discount') || 
                       (GRNState.FOCMethod === '' && StateName === 'FOCQty') ||
                      (!GRNItemState.IsManufactureDateAvailable && StateName === 'ManufactureDate') ||
                      (!GRNItemState.IsExpiryDateAvailable && StateName === 'ExpiryDate') ||  (!GRNItemState.IsFOCProduct && !GRNItemState.IsFOCQtyAvailable && StateName === 'FOCQty')
                      ||(GRNItemState.IsMRPAsSellablePrice && StateName === 'SellablePrice') }
                    />

                    {['FOCItemCode','FOCItemName'].includes(StateName) &&
                      <datalist
                      id={StateName+'List'}
                      >                    
                      {
                      SupplierProductArray.map((option,index)=>(
                      <option key={index+'key'} value={StateName === 'FOCItemCode' ? option.ItemCode : option.ItemName}>                         
                      </option>
                      ))
                      } 
                      </datalist>
                    }
                    </>
                    
                    }
                  </div>
                
                )
              })
            }

          </div>
           </>   }


           <br/>
      
      <div className="Main_container_Btn">
        <button onClick={handelonAdd}>
           {GRNItemState.id ?'Update' : 'Add'}
        </button>
        </div>

        <br/>

      {GRNItemlist.length !==0 && 

        <>
        <div className="common_center_tag">
        <span>GRN PRODUCT LIST</span>
        </div> 


        <div className='RegisFormcon_1 jjxjx_'>
        <ReactGrid columns={GRNItemcolumn} RowData={GRNItemlist} />
        </div>
    

        <div className="RegisFormcon_1">
          {
            Object.keys(Amountstate).map((StateName3,Index)=>{
              return(
                <div className="RegisForm_1" key={Index+'key'}>
                <label htmlFor={StateName3}>{formatLabel(StateName3)} :</label>
                
                {
                ['TotalDiscountMethod','TotalDiscountType'].includes(StateName3) ?

                <select
                 type={getInputType(StateName3)}
                 id={StateName3}
                 name={StateName3}
                 value={Amountstate[StateName3]} 
                 onChange={HandelAmountState}
                 disabled={(StateName3 === 'TotalDiscountType' && Amountstate.TotalDiscountMethod === '') 
                   || (GRNItemlist.length === 0 && StateName3 === 'TotalDiscountMethod') || ( GRNItemlist.every((ele) =>
                    ["BeforeTax", "AfterTax"].includes(ele.DiscountMethod) ? StateName3 === 'TotalDiscountMethod' :'')) }   
                 
                 >
                  <option value=''>Select</option>
                  {
                    StateName3 === 'TotalDiscountMethod' ?
                    <>
                    <option value='BeforeTax'>Before Tax</option>
                    <option value='AfterTax'>After Tax</option>
                    </>
                    :
                    <>
                    <option value='Cash'>Cash</option>
                    <option value='Percentage'>Percentage</option>
                    </>
                  }
                </select>
                
                :
                <input
                 type={getInputType(StateName3)}
                 id={StateName3}
                 name={StateName3}
                 value={Amountstate[StateName3]} 
                 onChange={HandelAmountState}
                 readOnly ={(StateName3 !== 'TotalDiscount') || 
                  (StateName3 === 'TotalDiscount' && Amountstate.TotalDiscountType === '')
                 }                
                 />
                }
                </div>
              )
            })
          }
        </div>

        <br/>
        <div className="Main_container_Btn">
        <button onClick={SaveGRNfunc}>
        {GRNState.GRNNumber ?'Update' : 'Save' }
        </button>
        </div>
        </>

        }


        </div>
      
      {selectRoom2 && POItemArrays.length !==0 &&(
       
       <div className="loader" onClick={() => setselectRoom2(false)}>
       <div className="loader_register_roomshow"   onClick={(e) => e.stopPropagation()}>
       <br/>
       

       <div className="Main_container_app">


       <div className="common_center_tag">
           <span>Purchase Order Item Quantity Edit</span>
       </div>
       <br/>
       <br/>

       <div className="RegisFormcon_1">

       {Object.keys(POItemChange).map((StateName,Index)=>{
         return(

           <div className="RegisForm_1" key={Index+'key'}>
           
           <label htmlFor={StateName}>{formatLabel(StateName)} :</label>
           
           {['ItemStatus'].includes(StateName) ?

             <select
              type={getInputType(StateName)}
               id={StateName}
               name={StateName}
               value={POItemChange[StateName]}
               onChange={HandleOnchangePORemoveQty}
               disabled={POItemChange.CancelQty === '' ? StateName === 'ItemStatus' :''}
             >
               <option value=''>Select</option>
               {                    
                 <>
                 <option value='Waiting For GRN'>Waiting For GRN</option>
                 <option value='Canceled'>Cancel</option>
                 </>
               }

               </select>

               :
               ['Reason'].includes(StateName) ?
               <textarea
               type={getInputType(StateName)}
               id={StateName}
               name={StateName}
               value={POItemChange[StateName]}
               onChange={HandleOnchangePORemoveQty}
               >

               </textarea>
               :
               <input
               type={getInputType(StateName)}
               id={StateName}
               name={StateName}
               value={POItemChange[StateName]}
               readOnly={(!['CancelQty'].includes(StateName)) ||
                 (+POItemChange.ReceivedQty ? StateName ==='CancelQty' :'')
               }
               onChange={HandleOnchangePORemoveQty}
             />

           }

           </div>
           

         )
        })

        }

    
           
           <div className="Main_container_Btn">
             <button onClick={RemoveQtyFun}>
               Save
             </button>
             </div>
       </div>
       </div>

       </div>
       </div>



       )}
        
        


      <ToastAlert Message={toast.message} Type={toast.type} />
      <ModelContainer />

    </>
  )
}

export default GoodsReceiptNote;