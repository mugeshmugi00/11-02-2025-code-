import * as React from "react";
import { useEffect, useState } from "react";
import axios from "axios";
import { useDispatch, useSelector } from "react-redux";
import AddIcon from "@mui/icons-material/Add";
import RemoveIcon from "@mui/icons-material/Remove";
import Modal from 'react-modal';
import HighlightOffIcon from "@mui/icons-material/HighlightOff";
import Button from '@mui/material/Button';
import { useNavigate } from "react-router-dom";





export default function InsurancePreAuthDocuments() {

 

  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [modalContent, setModalContent] = useState('');


  const navigate = useNavigate();
  

  const userRecord = useSelector((state) => state.userRecord?.UserData);

//   const InsuranceUpdatedata = useSelector(
//     (state) => state.InsuranceStore?.InsuranceUpdatedata
//   );

  const InsuranceUpdatedata = {}

  // console.log('InsuranceUpdatedatalllllkkk',)

  



  const yourStyles={
    position: 'absolute',
    inset: '100px',
    border: '1px solid rgb(204, 204, 204)',
    background: 'rgb(97 90 90 / 75%)',
    overflow: 'auto',
    borderRadius: '4px',
    outline: 'none',
    padding: '0px'
  }



  const [rows7, setRows7] = useState([
    {
      Name:'photoIdentityCard',
      Document_file:null,
      Document_Remarks: "",
      Document_Date: "",
      Document_Ack: false,
    },
  ]);

  const [rows8, setRows8] = useState([
    {
      Name:'signedForm',
      Document_file: null,
      Document_Remarks: "",
      Document_Date: "",
      Document_Ack: false,
    },
  ]);

  const [rows9, setRows9] = useState([
    { 
      Name:'otherDocument',
      Document_file:null,
      Document_Remarks: "",
      Document_Date: "",
      Document_Ack: false,
    },
  ]);

  


  const base64toFile = (base64String, fileName, mimeType) => {
    if (!base64String) {
      console.error("base64String is undefined or null.");
      return null;
    }
  
    const padding = "=".repeat((4 - (base64String.length % 4)) % 4);
    const paddedBase64String = base64String + padding;
  
    try {
      const byteString = atob(paddedBase64String);
      const arrayBuffer = new ArrayBuffer(byteString.length);
      const int8Array = new Uint8Array(arrayBuffer);
  
      for (let i = 0; i < byteString.length; i++) {
        int8Array[i] = byteString.charCodeAt(i);
      }
  
      const blob = new Blob([arrayBuffer], { type: mimeType });
      return new File([blob], fileName, { type: mimeType });
    } catch (error) {
      console.error("Error decoding base64 string:", error);
      return null;
    }
  };
  

// ------------------------------------------------------------------------------------

const handleChangeRowDocuments = (index, key, value) => {

  console.log('hay',index, key, value)
    const updatedRows = [...rows7];
    updatedRows[index][key] = value;
    setRows7(updatedRows);
  };

  const addRow7 = () => {
    setRows7((prevRows) => [
      ...prevRows,
      {
        Name:'photoIdentityCard',
        Document_file: null,
        Document_Remarks: "",
        Document_Date: "",
        Document_Ack: false,
      },
    ]);
  };
  const removeRow7 = (index) => {
    setRows7((prevRows) =>
      prevRows.filter((row, rowIndex) => rowIndex !== index)
    );
  };

  const handleChangeRowDocuments2 = (index, key, value) => {
    const updatedRows = [...rows8];
    updatedRows[index][key] = value;
    setRows8(updatedRows);
  };

  const addRow8 = () => {
    setRows8((prevRows) => [
      ...prevRows,
      {
        Name:'signedForm',
        Document_file:null,
        Document_Remarks: "",
        Document_Date: "",
        Document_Ack:false,

      },
    ]);
  };
  const removeRow8 = (index) => {
    setRows8((prevRows) =>
      prevRows.filter((row, rowIndex) => rowIndex !== index)
    );
  };

  const handleChangeRowDocuments3 = (index, key, value) => {
    const updatedRows = [...rows9];
    updatedRows[index][key] = value;
    setRows9(updatedRows);
  };

  const addRow9 = () => {
    setRows9((prevRows) => [
      ...prevRows,
      {
        Name:'otherDocument',
        Document_file:null,
        Document_Remarks: "",
        Document_Date: "",
        Document_Ack:false,
      },
    ]);
  };
  const removeRow9 = (index) => {
    setRows9((prevRows) =>
      prevRows.filter((row, rowIndex) => rowIndex !== index)
    );
  };

  

  
 

  const SavebtnFun =()=>{

    const MRN = InsuranceUpdatedata.MRN
    const ContactNumber=InsuranceUpdatedata.ContactNumber

    const Location = userRecord.location 
    const createAt = userRecord.username 


    console.log('mmmm',rows7,rows8,rows9)

    const formData = new FormData();

    formData.append('MRN', MRN);
    formData.append('ContactNumber', ContactNumber);
    formData.append('Location', Location);
    formData.append('createAt', createAt);

    formData.append('rows7', JSON.stringify(rows7));
    formData.append('rows8', JSON.stringify(rows8));
    formData.append('rows9', JSON.stringify(rows9));
    
    // Append Document_file from each row to formData
    const appendFiles = (formData, rows, prefix) => {
        rows.forEach((row, index) => {
            if (row && row.Document_file) {
                formData.append(`${prefix}[${index}][Document_file]`, row.Document_file);
            }
        });
    };
    
    appendFiles(formData, rows7, 'rows7');
    appendFiles(formData, rows8, 'rows8');
    appendFiles(formData, rows9, 'rows9');


    axios.post(`https://vesoftometic.co.in/Insurance/Post_Pre_Auth_Form_Submit_Documents_data`,formData)
    .then((response) => {
        console.log('Form data submitted.',response.data)
        // cleardata()
    })
    .catch((error) => {
        console.error(error);
    });


  }


  

// --------------------------------------------------------

  // const SubmitDocFun =()=>{

  //   let params={
  //     Papersstatus:"SUBMITTED",
  //     MRN: InsuranceUpdatedata.MRN,
  //     ContactNumber:InsuranceUpdatedata.ContactNumber,
  //     Location:userRecord.location,
  //     createAt:userRecord.username,
  //   }

  //   axios.post(`https://vesoftometic.co.in/Insurance/Update_Papersstatus_Insurance`,params)
  //   .then((response) => {
  //       console.log('Form data submitted.',response.data)

  //       navigate("/Home/Insurance-Dashboard");


  //   })
  //   .catch((error) => {
  //       console.error(error);
  //   });

  // }

// console.log('kkk',rows7,rows8,rows9)

  
 useEffect(() => {
  if (Object.values(InsuranceUpdatedata).length !== 0 && InsuranceUpdatedata.Papersstatustype === "ORIGINAL") {
      // console.log('Vathuruchu', InsuranceUpdatedata)
      axios.get(
          `https://vesoftometic.co.in/Insurance/get_Pre_Auth_Submit_Documents_data`, {
          params: InsuranceUpdatedata.MRN
      }
      )
          .then((response) => {
              // console.log('vrrrr',response.data);

              const data = response.data
              const photo_id_data=data.photo_id_data
              const signed_form_data=data.signed_form_data
              const other_document_data=data.other_document_data
              // console.log('qqq', photo_id_data,other_document_data,signed_form_data)

              const updatedRows7 = photo_id_data.map((element) => {
                const file = base64toFile(element.Document_file, element.DecoFile1name, element.DecoFile1type);
                return {...element, Document_file: file};
            });
            
            const updatedRows8 = signed_form_data.map((element) => {
                const file = base64toFile(element.Document_file, element.DecoFile1name, element.DecoFile1type);
                return {...element, Document_file: file};
            });
            
            const updatedRows9 = other_document_data.map((element) => {
                const file = base64toFile(element.Document_file, element.DecoFile1name, element.DecoFile1type);
                return {...element, Document_file: file};
            });
            
           if(updatedRows7.length !==0){
            setRows7(updatedRows7);
           }
          if(updatedRows8.length !==0){
            setRows8(updatedRows8);
           }
          if(updatedRows9.length !==0){            
            setRows9(updatedRows9);
           }

          })
          .catch((error) => {
              console.log(error);
          });

  }
}, [InsuranceUpdatedata])




// ------------------File

const handleVisibilityClick = async (ConsentForm) => {
  console.log('ConsentForm', ConsentForm.type);

  if (ConsentForm.type !== "application/pdf") {
    const fileURL = URL.createObjectURL(ConsentForm);
    setModalContent(fileURL);
    setModalIsOpen(true);
  } else {
    // Convert the PDF file to a base64 string
    const base64String = await readFileAsBase64(ConsentForm);
    const Pdffile = `data:application/pdf;base64,${base64String}`;
    console.log('Pdffile', Pdffile);
    setModalContent(Pdffile);
    setModalIsOpen(true);
  }
};

const readFileAsBase64 = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result.split(',')[1]);
    reader.onerror = (error) => reject(error);
  });
};

const closeModal = () => {
  setModalIsOpen(false);
  setModalContent('');
};

  return (
    <>
     <div className="Supplier_Master_Container">
    
               
    <div className="RegisFormcon column_regisFormcon_forinsurance">
    <div className="h_heade34">
        <h3>Pre-Auth Documents</h3>
    </div>

    <div className="Selected-table-container">
        <table className="selected-medicine-table2 _hide_hover_table">
        <thead className="Spl_backcolr_09">
            <tr>
            <th className="Provisional_Diagnosis">File Name</th>
            <th className="ICD_Code">Remarks</th>
            <th className="ICD_Code">Submitted Date</th>
            <th className="ICD_Code">ACK</th>
            <th className="ICD_Code">Action</th>
            </tr>
        </thead>
        <tbody>
            {rows7.map((row, index) => (
            <tr key={index}>
                <td>
                {rows7[index]['Document_file'] === null ? <span>Photo Identity Card</span>
                :<span style={{color:'blue', cursor: 'pointer'}} onClick={() => handleVisibilityClick(rows7[index]['Document_file'])} >Photo Identity Card</span>}
                <label className="file-labelx">
                    <input
                    type="file"
                    className="file-inputx"
                    accept="image/pdf"
                    onChange={(e) => {
                        const file = e.target.files[0];
                        console.log('1100',file)
                        handleChangeRowDocuments(index, 'Document_file', file);
                    }}
                    />
                    <span className="file-buttonx">
                    Choose file
                    </span>
                </label>
                </td>
                <td>
                <input
                    type="text"
                    className="ICD_Code"
                    value={row.Document_Remarks}
                    onChange={(e) =>
                    handleChangeRowDocuments(
                        index,
                        "Document_Remarks",
                        e.target.value
                    )
                    }
                />
                </td>
                <td>
                <input
                    type="date"
                    className="medication_90"
                    value={row.Document_Date}
                    onChange={(e) =>
                    handleChangeRowDocuments(
                        index,
                        "Document_Date",
                        e.target.value
                    )
                    }
                />
                </td>
                <td>
                <input
                    type="checkbox"
                    className="medication_90"
                    checked={row.Document_Ack}
                    onChange={(e) =>
                    handleChangeRowDocuments(
                        index,
                        "Document_Ack",
                        e.target.checked
                    )
                    }
                />
                </td>
                <td className="add32_Code">
                {index === 0 ? (
                    <span
                    className="add32_Code"
                    onClick={addRow7}
                    >
                    <AddIcon className="add32_Code" />
                    </span>
                ) : (
                    <span
                    className="add32_Code"
                    onClick={() => removeRow7(index)}
                    >
                    <RemoveIcon className="add32_Code" />
                    </span>
                )}
                </td>
            </tr>
            ))}

            {rows8.map((row, index) => (
            <tr key={index}>
                <td>
                {rows8[index]['Document_file'] === null ? <span>Signed Form</span>
                :<span style={{color:'blue', cursor: 'pointer'}} onClick={() => handleVisibilityClick(rows8[index]['Document_file'])} >Signed Form</span>}
                <label className="file-labelx">
                    <input
                    type="file"
                    className="file-inputx"
                    accept="image/pdf"
                    onChange={(e) =>{
                        const file = e.target.files[0];
                        handleChangeRowDocuments2(index, 'Document_file', file);
                    }}
                    />
                    <span className="file-buttonx">
                    Choose file
                    </span>
                </label>
                </td>
                <td>
                <input
                    type="text"
                    className="ICD_Code"
                    value={row.Document_Remarks}
                    onChange={(e) =>
                    handleChangeRowDocuments2(
                        index,
                        "Document_Remarks",
                        e.target.value
                    )
                    }
                />
                </td>
                <td>
                <input
                    type="date"
                    className="medication_90"
                    value={row.Document_Date}
                    onChange={(e) =>
                    handleChangeRowDocuments2(
                        index,
                        "Document_Date",
                        e.target.value
                    )
                    }
                />
                </td>
                <td>
                <input
                    type="checkbox"
                    className="medication_90"
                    checked={row.Document_Ack}
                    onChange={(e) =>
                    handleChangeRowDocuments2(
                        index,
                        "Document_Ack",
                        e.target.checked
                    )
                    }
                />
                </td>
                <td className="add32_Code">
                {index === 0 ? (
                    <span
                    className="add32_Code"
                    onClick={addRow8}
                    >
                    <AddIcon className="add32_Code" />
                    </span>
                ) : (
                    <span
                    className="add32_Code"
                    onClick={() => removeRow8(index)}
                    >
                    <RemoveIcon className="add32_Code" />
                    </span>
                )}
                </td>
            </tr>
            ))}

            {rows9.map((row, index) => (
            <tr key={index}>
                <td>
                {rows9[index]['Document_file'] === null ? <span>Other Documents</span>
                :<span style={{color:'blue', cursor: 'pointer'}} onClick={() => handleVisibilityClick(rows9[index]['Document_file'])} >Other Documents</span>}
                <label className="file-labelx">
                    <input
                    type="file"
                    className="file-inputx"
                    accept="image/pdf"
                    onChange={(e) =>{
                        const file = e.target.files[0];
                        handleChangeRowDocuments3(index, 'Document_file', file);
                    }}
                    />
                    <span className="file-buttonx">
                    Choose file
                    </span>
                </label>
                </td>
                <td>
                <input
                    type="text"
                    className="ICD_Code"
                    value={row.Document_Remarks}
                    onChange={(e) =>
                    handleChangeRowDocuments3(
                        index,
                        "Document_Remarks",
                        e.target.value
                    )
                    }
                />
                </td>
                <td>
                <input
                    type="date"
                    className="medication_90"
                    value={row.Document_Date}
                    onChange={(e) =>
                    handleChangeRowDocuments3(
                        index,
                        "Document_Date",
                        e.target.value
                    )
                    }
                />
                </td>
                <td>
                <input
                    type="checkbox"
                    className="medication_90"
                    checked={row.Document_Ack}
                    onChange={(e) =>
                    handleChangeRowDocuments3(
                        index,
                        "Document_Ack",
                        e.target.checked
                    )
                    }
                />
                </td>
                <td className="add32_Code">
                {index === 0 ? (
                    <span
                    className="add32_Code"
                    onClick={addRow9}
                    >
                    <AddIcon className="add32_Code" />
                    </span>
                ) : (
                    <span
                    className="add32_Code"
                    onClick={() => removeRow9(index)}
                    >
                    <RemoveIcon className="add32_Code" />
                    </span>
                )}
                </td>
            </tr>
            ))}

        </tbody>
        </table>
    </div>
    </div>


      </div>

       
        {/* <div style={{display:'flex',justifyContent:'center',gap:'20px'}}>
        <div className="submit_button_prev_next">
            <button onClick={SavebtnFun}>
                Save                
            </button>
          </div>
        
        </div> */}
        

        

        <Modal isOpen={modalIsOpen} onRequestClose={closeModal}style={{ content: { ...yourStyles } }}>
        <div className="pdf_img_show">
          {modalContent.toString().toLowerCase().startsWith("data:application/pdf;base64,") ? (
            <iframe
              title="PDF Viewer"
              src={modalContent}
              style={{
                width: "100%",
                height: "435px",
                border: "1px solid rgba(0, 0, 0, 0.5)", // Black border with reduced opacity
              }}
            />
          ) : (
            <img
              src={modalContent}
              alt="Concern Form"
              style={{
                width: "80%",
                height: "75%",
                marginTop: "20px",
              }}
            />
          )}
          <div className="jhuhhjh">
            <Button
              style={{ color: "white" }}
              className="clse_pdf_img"
              onClick={closeModal}
            >
              <HighlightOffIcon
                style={{
                  fontSize: "40px",
                  backgroundColor: "#54d854bf",
                  borderRadius: "40px",
                }}
              />
            </Button>
          </div>
        </div>
      </Modal>

    </>
  );
}
