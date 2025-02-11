import * as React from "react";
import { useEffect, useState } from "react";
import axios from "axios";
import { useDispatch, useSelector } from "react-redux";
import AddIcon from "@mui/icons-material/Add";
import RemoveIcon from "@mui/icons-material/Remove";





export default function InsuranceDiagnosis() {

  
  const dispatchvalue = useDispatch();

  const isSidebarOpen = useSelector((state) => state.userRecord?.isSidebarOpen);

  const userRecord = useSelector((state) => state.userRecord?.UserData);

  const InsuranceUpdatedata = {}

//   const InsuranceUpdatedata = useSelector(
//     (state) => state.InsuranceStore?.InsuranceUpdatedata
//   );




  const [rows, setRows] = useState([
    { provisionalDiagnosis: "", icdCode: "", type: "Primary" },
  ]);

  const [rows2, setRows2] = useState([
    { finalDiagnosis: "", icdCode2: "", type2: "Primary" },
  ]);


// -----------------------------------------------------------------

const addRow = () => {
    setRows([
      ...rows,
      { provisionalDiagnosis: "", icdCode: "", type: "Primary" },
    ]);
  };



const handleChangeRow = (index, key, value) => {
    const newRows = [...rows];
    newRows[index][key] = value;
    setRows(newRows);
  };


  const removeRow = (index) => {
    const newRows = [...rows];
    newRows.splice(index, 1);
    setRows(newRows);
  };

  const addRow2 = () => {
    setRows2([
      ...rows2,
      {
        finalDiagnosis: "",
        icdCode2: "",
        type2: "Primary",
      },
    ]);
  };

  const handleChangeRow2 = (index, key, value) => {
    const newRows = [...rows2];
    newRows[index][key] = value;
    setRows2(newRows);
  };

  const removeRow2 = (index) => {
    const newRows = [...rows2];
    newRows.splice(index, 1);
    setRows2(newRows);
  };




  const SavebtnFun =()=>{

    const params={

      MRN: InsuranceUpdatedata.MRN,
      ContactNumber:InsuranceUpdatedata.ContactNumber,

      Location:userRecord.location || '',
      createAt:userRecord.username || '',

      rows:rows,

      rows2:rows2,
      
      MainPageCompleted:"MainPage1",

      PageCompleted:"TreatmentInfo"
    } 

    axios.post(`https://vesoftometic.co.in/Insurance/Post_Pre_Auth_Form_diagnosis`,params)
    .then((response) => {
        console.log('Form data submitted.',response.data)
        dispatchvalue({type: "InsurancePageChange",value:"TreatmentInfo"});
    })
    .catch((error) => {
        console.error(error);
    });

  }


  useEffect(()=>{
    if(Object.values(InsuranceUpdatedata).length !== 0){
        console.log('Vathuruchu',InsuranceUpdatedata)            
     axios.get(
    `https://vesoftometic.co.in/Insurance/get_Pre_Auth_Form_diagnosis`,{
        params: InsuranceUpdatedata.MRN
    }
    )
    .then((response) => {
    // console.log('vrrrr',response.data);
    
    const data=response.data

    let data1=data.data1

    let data2=data.data2


    if(data1.length !==0){
      
    setRows(data.data1)
    }


    if(data2.length !==0){
      
      setRows2(data.data2)
      }
    
    
    

    })
    .catch((error) => {
    console.log(error);
    });

    }
},[InsuranceUpdatedata])



 
  return (
    <>
     <div className="Supplier_Master_Container">
    
    
    <div className="Selected-table-container">
    <table className="selected-medicine-table2 _hide_hover_table">
        <thead className="Spl_backcolr_09">
        <tr>
            <th className="Provisional_Diagnosis">
            Provisional Diagnosis
            </th>
            <th className="ICD_Code">ICD Code</th>
            <th className="ICD_Code">Type</th>
            <th className="add32_Code">
            <span onClick={addRow}>
                <AddIcon className="add32_Code" />
            </span>
            </th>
        </tr>
        </thead>
        <tbody>
        {rows.map((row, index) => (
            <tr key={index}>
                <td>
                    <input
                        className="Provisional_Diagnosis"
                        value={row.provisionalDiagnosis}
                        onChange={(e) =>
                        handleChangeRow(index,"provisionalDiagnosis",e.target.value)
                        }
                    />
                </td>
                <td>
                    <input
                        className="ICD_Code"
                        value={row.icdCode}
                        onChange={(e) =>
                        handleChangeRow(index,"icdCode",e.target.value)
                        }
                    />
                </td>
                <td>
                    <select
                        className="Type_code"
                        value={row.type}
                        onChange={(e) =>
                        handleChangeRow(index, "type", e.target.value)
                        }
                    >
                        <option value="Primary">Primary</option>
                        <option value="Secondary">Secondary</option>
                        <option value="Comorbidity">Comorbidity</option>
                    </select>
                </td>
                <td className="add32_Code">
                    <span onClick={() => removeRow(index)}>
                        <RemoveIcon className="add32_Code" />
                    </span>
                </td>
            </tr>
            ))}
        </tbody>
    </table>
    </div>
    <br></br>
    <div className="Selected-table-container">
    <table className="selected-medicine-table2 _hide_hover_table">
        <thead className="Spl_backcolr_09">
        <tr>
            <th className="Provisional_Diagnosis">
            Final Diagnosis
            </th>
            <th className="ICD_Code">ICD Code</th>
            <th className="ICD_Code">Type</th>
            <th className="add32_Code">
            <span onClick={addRow2}>
                <AddIcon className="add32_Code" />
            </span>
            </th>
        </tr>
        </thead>
        <tbody>
        {rows2.map((row, index) => (
            <tr key={index}>
            <td>
                <input
                className="Provisional_Diagnosis"
                value={row.finalDiagnosis}
                onChange={(e) =>
                    handleChangeRow2(
                    index,
                    "finalDiagnosis",
                    e.target.value
                    )
                }
                />
            </td>
            <td>
                <input
                className="ICD_Code"
                value={row.icdCode2}
                onChange={(e) =>
                    handleChangeRow2(
                    index,
                    "icdCode2",
                    e.target.value
                    )
                }
                />
            </td>
            <td>
                <select
                className="Type_code"
                value={row.type2}
                onChange={(e) =>
                    handleChangeRow2(
                    index,
                    "type2",
                    e.target.value
                    )
                }
                >
                <option value="Primary">Primary</option>
                <option value="Secondary">Secondary</option>
                <option value="Comorbidity">Comorbidity</option>
                </select>
            </td>
            <td className="add32_Code">
                <span onClick={() => removeRow2(index)}>
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
