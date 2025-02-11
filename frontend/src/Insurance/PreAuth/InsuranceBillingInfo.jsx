import * as React from "react";
import { useEffect, useState } from "react";
import axios from "axios";
import { useDispatch, useSelector } from "react-redux";
import AddIcon from "@mui/icons-material/Add";
import RemoveIcon from "@mui/icons-material/Remove";



export default function InsuranceBillingInfo() {

  
  const dispatchvalue = useDispatch();

  const isSidebarOpen = useSelector((state) => state.userRecord?.isSidebarOpen);

  const userRecord = useSelector((state) => state.userRecord?.UserData);

//   const InsuranceUpdatedata = useSelector(
//     (state) => state.InsuranceStore?.InsuranceUpdatedata
//   );


  const InsuranceUpdatedata = {}

  const [billingInfo, setBillingInfo] = useState({
    dateofAdmission:"",
    typeofAdmission: "",
    durationStayinDays: "",
    dateofSurgery: "",    
    AvailedRateCard:'',
    EligibleRoomType:'',
    CreditBill:"No",
    IsDefaultPayer:'No',
    AllAreMedicalItems:'No',
    dateofDischarge: "",
    DischargeTypeBilling: "",    
  });


  const [CoPaymentCoverage, setCoPaymentCoverage] = useState("No");

  const [CoPaymentDetails,setCoPaymentDetails]=useState({
        CoPaymentType:'',
        CoPaymentTypeValue:'',
        CoPaymentLogic:'',
        CoPaymentToBeDeductedFrom:'',
    })

  const [rows6, setRows6] = useState([
    {
      costOfHospitalization: "",
      totalBillAmount: "",
    },
  ]);


//   -----------------------------------------------------


const handleChangeBillingInfo = (event) => {
    const { name, value } = event.target;

    setBillingInfo((prev)=>({
      ...prev,
      [name]: value,
    }))
  };

  const handleChangeRowBillingItem = (index, key, value) => {
    const newRows = [...rows6];
    newRows[index][key] = value;
    setRows6(newRows);
  };

  const addRow6 = () => {
    setRows6([
      ...rows6,
      {
        costOfHospitalization: "",
        totalBillAmount: "",
      },
    ]);
  };

  const removeRow6 = (index) => {
    const newRows = [...rows6];
    newRows.splice(index, 1);
    setRows6(newRows);
  };


 

  const SavebtnFun =()=>{
    

    const params={

      MRN: InsuranceUpdatedata.MRN,
      ContactNumber:InsuranceUpdatedata.ContactNumber,

      Location:userRecord.location,
      createAt:userRecord.username, 

      billingInfo:billingInfo,

      rows6:rows6,

      MainPageCompleted:"MainPage2",

      PageCompleted:"PreAuthDocuments"

    } 


    axios.post(`https://vesoftometic.co.in/Insurance/Post_Pre_Auth_Form_billing_info_details`,params)
    .then((response) => {
        console.log('Form data submitted.',response.data)
        dispatchvalue({type: "InsurancePageChange",value:"PreAuthDocuments"});
    })
    .catch((error) => {
        console.error(error);
    });

  }

 
 useEffect(() => {
    if (Object.values(InsuranceUpdatedata).length !== 0) {

        axios.get(
            `https://vesoftometic.co.in/Insurance/get_Pre_Auth_billing_info_details`, {
            params: InsuranceUpdatedata.MRN
        }
        )
            .then((response) => {
                // console.log('vrrrr',response.data);

                const data = response.data[0]

                // console.log('qqq', data.Billinginfolist)

                if(Object.keys(data).length !== 0){
                  setBillingInfo((prev) => ({
                    ...prev,
                    dateofAdmission: data.dateofAdmission,
                    typeofAdmission: data.typeofAdmission,
                    durationStayinDays: data.durationStayinDays,
                    dateofSurgery: data.dateofSurgery,
                    dateofDischarge: data.dateofDischarge,
                    DischargeTypeBilling: data.DischargeTypeBilling,
                  }));
  
                  setRows6(data.Billinginfolist)
                }

            })
            .catch((error) => {
                console.log(error);
            });

    }
}, [InsuranceUpdatedata])


const  handleCheckboxCoPayment = (event) => {
  if(event.target.value ==='No'){
  setCoPaymentCoverage(event.target.value)
  
  setCoPaymentDetails({
  CoPaymentType:'',
  CoPaymentTypeValue:'',
  CoPaymentLogic:'',
  CoPaymentToBeDeductedFrom:'',
  })

  }else{
  setCoPaymentCoverage(event.target.value)
  }
};


const HandleCoPaymentDetails =(e)=>{
  const {name,value}=e.target;
  
  setCoPaymentDetails((prev)=>({
      ...prev,
      [name]:value
  }))

}

  

  return (
    <>
      <div className="Main_container_app">     
        <>
        <div className="RegisFormcon_1">
           
           
            <div className="RegisForm_1">
                <label>
                Date Of Admission <span>:</span>
                </label>
                <input
                type="date"
                name="dateofAdmission"
                value={billingInfo.dateofAdmission}
                onChange={handleChangeBillingInfo}
                />
            </div>
           
            <div className="RegisForm_1">
                <label>
                Type Of Admission <span>:</span>
                </label>
                <select
                name="typeofAdmission"
                value={billingInfo.typeofAdmission}
                onChange={handleChangeBillingInfo}
                >
                <option value="">Select</option>
                <option value="Type1">Admission Type 1</option>
                <option value="Type2">Admission Type 2</option>
                <option value="Type3">Admission Type 3</option>
                </select>
            </div>
            
            <div className="RegisForm_1">
                <label>
                Duration(stay in Days) <span>:</span>
                </label>
                <input
                type="number"
                name="durationStayinDays"
                value={billingInfo.durationStayinDays}
                onChange={handleChangeBillingInfo}
                />
            </div>
                    
           
            <div className="RegisForm_1">
                <label>
                Date Of Surgery <span>:</span>{" "}
                </label>
                <input
                type="date"
                name="dateofSurgery"
                value={billingInfo.dateofSurgery}
                onChange={handleChangeBillingInfo}
                />
            </div>

            <div className="RegisForm_1">
              <label>
                Availed Rate Card <span>:</span>
              </label>
              <select
               name="AvailedRateCard"
               value={billingInfo.AvailedRateCard}
               onChange={handleChangeBillingInfo}
              >
            <option value=''>Select</option>
            <option value='Rate1'>Rate1</option>

            </select>

            </div>


            <div className="RegisForm_1">
              <label>
               Eligible Room Type <span>:</span>
              </label>
              <select
               name="EligibleRoomType"
               value={billingInfo.EligibleRoomType}
               onChange={handleChangeBillingInfo}
              >
                <option value="">Select</option>
                <option value="Room1">Room 1</option>
                <option value="Room2">Room 2</option>
                <option value="Room3">Room 3</option>
                <option value="Room4">Room 4</option>

            </select>
            
            </div>


            <div className="RegisForm_1">
              <label>
              Credit Bill <span>:</span>
              </label>

              <div className="ewj_i87_head">
                <div className="ewj_i87">
                <input
                    type="radio"
                    id="CreditBillYes"
                    name="CreditBill"
                    value="Yes"
                    checked={billingInfo.CreditBill === "Yes"}
                    onChange={handleChangeBillingInfo}
                ></input>

                <label htmlFor="CreditBillYes">Yes</label>
                </div>

                <div className="ewj_i87">
                <input
                    type="radio"
                    id="CreditBillNo"
                    name="CreditBill"
                    value="No"
                    checked={billingInfo.CreditBill === "No"}
                    onChange={handleChangeBillingInfo}
                ></input>
                <label htmlFor="CreditBillNo">No</label>
                </div>
            </div>
            
            </div>

            <div className="RegisForm_1">
              <label>
              IsDefault Payer <span>:</span>
              </label>

              <div className="ewj_i87_head">
                <div className="ewj_i87">
                <input
                    type="radio"
                    id="IsDefaultPayerYes"
                    name="IsDefaultPayer"
                    value="Yes"
                    checked={billingInfo.IsDefaultPayer === "Yes"}
                    onChange={handleChangeBillingInfo}
                ></input>

                <label htmlFor="IsDefaultPayerYes">Yes</label>
                </div>

                <div className="ewj_i87">
                <input
                    type="radio"
                    id="IsDefaultPayerNo"
                    name="IsDefaultPayer"
                    value="No"
                    checked={billingInfo.IsDefaultPayer === "No"}
                    onChange={handleChangeBillingInfo}
                ></input>
                <label htmlFor="IsDefaultPayerNo">No</label>
                </div>
            </div>
            
            </div>

            <div className="RegisForm_1">
              <label>
              All Are Medical Items <span>:</span>
              </label>

              <div className="ewj_i87_head">
                <div className="ewj_i87">
                <input
                    type="radio"
                    id="AllAreMedicalItemsYes"
                    name="AllAreMedicalItems"
                    value="Yes"
                    checked={billingInfo.AllAreMedicalItems === "Yes"}
                    onChange={handleChangeBillingInfo}
                ></input>

                <label htmlFor="AllAreMedicalItemsYes">Yes</label>
                </div>

                <div className="ewj_i87">
                <input
                    type="radio"
                    id="AllAreMedicalItemsNo"
                    name="AllAreMedicalItems"
                    value="No"
                    checked={billingInfo.AllAreMedicalItems === "No"}
                    onChange={handleChangeBillingInfo}
                ></input>
                <label htmlFor="AllAreMedicalItemsNo">No</label>
                </div>
            </div>
            
            </div>


            <div className="RegisForm_1">
                <label>
                Date Of Discharge <span>:</span>
                </label>
                <input
                type="date"
                name="dateofDischarge"
                value={billingInfo.dateofDischarge}
                onChange={handleChangeBillingInfo}
                />
            </div>
            
            <div className="RegisForm_1">
                <label>
                Discharge Type <span>:</span>
                </label>
                <select
                type="date"
                name="DischargeTypeBilling"
                value={billingInfo.DischargeTypeBilling}
                onChange={handleChangeBillingInfo}
                >
                <option value="">Select</option>
                <option value="DischargeType1">Discharge Type 1</option>
                <option value="DischargeType2">Discharge Type 2</option>
                <option value="DischargeType3">Discharge Type 3</option>
                <option value="DischargeType4">Discharge Type 4</option>
                </select>
            </div>
            
            </div>
            
            <br/>

            <div className="RegisForm_1">
              
              <label>
                CoPayment ? <span>:</span>
              </label>

              <div className="ewj_i87_head">
                <div className="ewj_i87">
                  <input
                    type="radio"
                    id="CoPaymentYes"
                    name="CoPayment"
                    value="Yes"
                    checked={CoPaymentCoverage === "Yes"}
                    onChange={handleCheckboxCoPayment}
                  ></input>

                  <label htmlFor="CoPaymentYes">Yes</label>
                </div>

                <div className="ewj_i87">
                  <input
                    type="radio"
                    id="CoPaymentNo"
                    name="CoPayment"
                    value="No"
                    checked={CoPaymentCoverage === "No"}
                    onChange={handleCheckboxCoPayment}
                  ></input>
                  <label htmlFor="CoPaymentNo">No</label>
                </div>
              </div>
            </div>
            <br/>

            {CoPaymentCoverage === "Yes" && (
            <div className="RegisFormcon_1">

            <div className="RegisForm_1">
        
            <label>Co-Payment Type<span>:</span></label>
            <select
            style={{width:'100px'}} 
            name='CoPaymentType'
            value={CoPaymentDetails.CoPaymentType}
            onChange={HandleCoPaymentDetails}
            >
            <option value=''>Select</option>
            <option value='Percentage'>Percentage</option>
            <option value='Value'>Value</option>
        
                
            </select>
            <input
            type='number'
            style={{width:'50px'}}
            name='CoPaymentTypeValue'
            value={CoPaymentDetails.CoPaymentTypeValue}
            onChange={HandleCoPaymentDetails}
            />
            </div>
        
            <div className="RegisForm_1">
        
            <label>Co-Payment Logic<span>:</span></label>
            <select
            name='CoPaymentLogic'
            value={CoPaymentDetails.CoPaymentLogic}
            onChange={HandleCoPaymentDetails}
            >
            <option value=''>Select</option>
            <option value='Logic1'>Logic1</option>
            </select>
            </div>
        
            <div className="RegisForm_1">
        
            <label style={{width:'135px'}}>Co-Payment To Be Deducted From<span>:</span></label>
            <select
            name='CoPaymentToBeDeductedFrom'
            value={CoPaymentDetails.CoPaymentToBeDeductedFrom}
            onChange={HandleCoPaymentDetails}
            >
            <option value=''>Select</option>
            <option value='Payment1'>Payment1</option>
            </select>
            </div>
            </div>
            )}

            <br/>


        </>
        <div className="Selected-table-container">
        <table className="selected-medicine-table2 _hide_hover_table">
            <thead className="Spl_backcolr_09">
            <tr>
                <th className="Provisional_Diagnosis">
                Billing Item
                </th>
                <th className="ICD_Code">Charges</th>

                <th className="add32_Code">
                <span onClick={addRow6}>
                    <AddIcon className="add32_Code" />
                </span>
                </th>
            </tr>
            </thead>
            <tbody>
            {rows6.map((row, index) => (
                <tr key={index}>
                <td>
                    <div className="bilng_itm_colum8">
                    <label>Expected Cost of Hospitalization*</label>
                    <input
                        type="text"
                        className="Provisional_Diagnosis"
                        value={row.costOfHospitalization}
                        onChange={(e) =>
                        handleChangeRowBillingItem(
                            index,
                            "costOfHospitalization",
                            e.target.value
                        )
                        }
                    />
                    </div>
                </td>
                <td>
                    <div className="bilng_itm_colum8">
                    <label>Total Bill Amount*</label>
                    <input
                        type="number"
                        className="Provisional_Diagnosis"
                        value={row.totalBillAmount}
                        onChange={(e) =>
                        handleChangeRowBillingItem(
                            index,
                            "totalBillAmount",
                            e.target.value
                        )
                        }
                    />
                    </div>
                </td>
                <td className="add32_Code">
                    <span onClick={() => removeRow6(index)}>
                    <RemoveIcon className="add32_Code" />
                    </span>
                </td>
                </tr>
            ))}
            </tbody>
        </table>
        </div>
               

      </div>

      {/* <div className="submit_button_prev_next">
            <button onClick={SavebtnFun}>
                Save
            </button>
        </div> */}
    </>
  );
}
