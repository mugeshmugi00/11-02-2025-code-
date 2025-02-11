import * as React from "react";
import { useEffect, useState } from "react";
import axios from "axios";
import { useDispatch, useSelector } from "react-redux";
import AddIcon from "@mui/icons-material/Add";
import RemoveIcon from "@mui/icons-material/Remove";



export default function InsuranceTreatmentInfo() {


    const dispatchvalue = useDispatch();

    const isSidebarOpen = useSelector((state) => state.userRecord?.isSidebarOpen);

    const userRecord = useSelector((state) => state.userRecord?.UserData);

    const InsuranceUpdatedata = {}

    // const InsuranceUpdatedata = useSelector(
    //     (state) => state.InsuranceStore?.InsuranceUpdatedata
    // );


    const [rows3, setRows3] = useState([
        {
            department: "",
            treatingDoctor: "",
            contactNumber3: "",
            registrationNumber: "",
            medicalCouncil: "",
        },
    ]);


    const [checkboxStateTreatment, setCheckboxStateTreatment] = useState({
        icuManagement: false,
        dialysis: false,
        chemotherapy: false,
        radiation: false,
    });

    const [medicalManagement, setMedicalManagement] = useState("No");
    const [TreatmentTxtareaDetails, setTreatmentTxtareaDetails] = useState('');

    const [rows4, setRows4] = useState([
        {
            treatment: "",
            pcsHospitalCode: "",
        },
    ]);

    const [surgicalManagement, setSurgicalManagement] = useState("No");

    const [additionalSurgicalOptions, setAdditionalSurgicalOptions] = useState([]);

    


    //   -----------------------------------------------------------

    const addRow3 = () => {
        setRows3([
            ...rows3,
            {
                department: "",
                treatingDoctor: "",
                contactNumber3: "",
                registrationNumber: "",
                medicalCouncil: "",
            },
        ]);
    };

    const handleChangeRow3 = (index, key, value) => {
        const newRows = [...rows3];
        newRows[index][key] = value;
        setRows3(newRows);
    };


    const removeRow3 = (index) => {
        const newRows = [...rows3];
        newRows.splice(index, 1);
        setRows3(newRows);
    };

    const handleCheckboxChangeTreatment = (event) => {
        const { name, checked } = event.target;
        setCheckboxStateTreatment({ ...checkboxStateTreatment, [name]: checked });
    };


    const handleCheckboxChangeMedical = (event) => {
        setMedicalManagement(event.target.value);
    };

    const handleTextAreaChangeDetails = (event) => {
        const { name, value } = event.target;
        setTreatmentTxtareaDetails(event.target.value);
    };


    const addRow4 = () => {
        setRows4([
            ...rows4,
            {
                treatment: "",
                pcsHospitalCode: "",
            },
        ]);
    };
    const handleChangeRow4 = (index, key, value) => {
        const newRows = [...rows4];
        newRows[index][key] = value;
        setRows4(newRows);
    };



    const removeRow4 = (index) => {
        const newRows = [...rows4];
        newRows.splice(index, 1);
        setRows4(newRows);
    };

    const handleCheckboxChangeSurgical = (event) => {
        setSurgicalManagement(event.target.value);
    };

  
   
   


    const addAdditionalSurgicalOption = () => {
        setAdditionalSurgicalOptions((prevOptions) => [
            ...prevOptions,
            {
                departmentSurgical: '',
                surgeonSurgical: '',
                CheckboxStates: {
                    laAnesthesia: false,
                    raAnesthesia: false,
                    saAnesthesia: false,
                    eaAnesthesia: false,
                    gaAnesthesia: false,
                },
                Type: "elective",
                procedureTables: []
            },
        ]);

       
    };
    console.log('additionalSurgicalOptions', additionalSurgicalOptions);
    const removeAdditionalSurgicalOption = () => {
        if (additionalSurgicalOptions.length > 0) {
            const updatedOptions = [...additionalSurgicalOptions];

            updatedOptions.pop();

            setAdditionalSurgicalOptions(updatedOptions);
        }
    };





    const addRow5 = (tableIndex) => {
        setAdditionalSurgicalOptions((prev) => {
            let updated = [...prev];
            let newrow = updated[tableIndex]['procedureTables'];
            newrow =[
                ...updated[tableIndex]['procedureTables'],
                {
                    procedureSurgical: "",
                    pcdHospitalCodeSurgical: "",
                },
            ];
            updated[tableIndex]['procedureTables'] = newrow;
            return updated;
        })
       
    };

    const removeRow5 = (tableIndex, rowIndex) => {
        setAdditionalSurgicalOptions((prev) => {
            let updated = [...prev];
            let newrow = updated[tableIndex]['procedureTables'];
            newrow =[
                ...updated[tableIndex]['procedureTables']
                
            ].splice(rowIndex, 1);
            updated[tableIndex]['procedureTables'] = newrow;
            return updated;
        })
        
    };




   

    const SavebtnFun = () => {

        const params = {

            MRN: InsuranceUpdatedata.MRN,
            ContactNumber: InsuranceUpdatedata.ContactNumber,

            Location: userRecord.location || '',
            createAt: userRecord.username || '',

            rows3: rows3,

            checkboxStateTreatment: checkboxStateTreatment,
            medicalManagement: medicalManagement,
            TreatmentTxtareaDetails: TreatmentTxtareaDetails,

            rows4: rows4,

            surgicalManagement: surgicalManagement,

            additionalSurgicalOptions: additionalSurgicalOptions,  //jhjhjjj

            MainPageCompleted:"MainPage1",


            PageCompleted: "BillingInfo"

        }

        // console.log('paramssssss',params)

        axios.post(`https://vesoftometic.co.in/Insurance/Post_Pre_Auth_Form_Treatment_info`, params)
            .then((response) => {
                console.log('Form data submitted.', response.data)
                dispatchvalue({type: "InsurancePageChange",value:"BillingInfo"});

            })
            .catch((error) => {
                console.error(error);
            });


    }


    useEffect(() => {
        if (Object.values(InsuranceUpdatedata).length !== 0) {
            // console.log('Vathuruchu', InsuranceUpdatedata)
            axios.get(
                `https://vesoftometic.co.in/Insurance/get_Pre_Auth_Treatment_info`, {
                params: InsuranceUpdatedata.MRN
            }
            )
                .then((response) => {
                    // console.log('vrrrr',response.data);

                    const data = response.data[0]

                    console.log('veera', data)

                   if(Object.keys(data).length !==0){
                    
                    if(data.rows3.length !==0){
                        setRows3(data.rows3)
                    }

                    setCheckboxStateTreatment((prev) => ({
                        ...prev,
                        icuManagement: data.icuManagement,
                        dialysis: data.dialysis,
                        chemotherapy: data.chemotherapy,
                        radiation: data.radiation,
                    }))

                    setMedicalManagement(data.Treatment_medical_management)
                    setSurgicalManagement(data.Treatment_surgical_management)

                    setTreatmentTxtareaDetails(data.Details)
                    
                    if(data.rows4.length !==0 ){
                    setRows4(data.rows4)
                    }

                    // console.log('RRR',data.surgical_management)

                    if(data.surgical_management.length !==0){
                    setAdditionalSurgicalOptions(data.surgical_management)
                    }
                    
                   }
                })
                .catch((error) => {
                    console.log(error);
                });

        }
    }, [InsuranceUpdatedata])






    return (
        <>
            <div className="Supplier_Master_Container">
                <>
                    <div className="Selected-table-container">
                        <table className="selected-medicine-table2 _hide_hover_table">
                            <thead className="Spl_backcolr_09">
                                <tr>
                                    <th className="Provisional_Diagnosis">
                                        Department
                                    </th>
                                    <th className="ICD_Code">Treating Doctor</th>
                                    <th className="ICD_Code">Contact Number</th>
                                    <th className="ICD_Code">Registration Number</th>
                                    <th className="ICD_Code">Medical Council</th>
                                    <th className="add32_Code">
                                        <span onClick={addRow3}>
                                            <AddIcon className="add32_Code" />
                                        </span>
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                {rows3.map((row, index) => (
                                    <tr key={index}>
                                        <td>
                                            <select
                                                className="department_tretmt"
                                                value={row.department}
                                                onChange={(e) =>
                                                    handleChangeRow3(
                                                        index,
                                                        "department",
                                                        e.target.value
                                                    )
                                                }
                                            >
                                                <option value="">Select</option>
                                                <option value="Cardiology">Cardiology</option>
                                                <option value="Urology">Urology</option>
                                                <option value="Dermatology">
                                                    Dermatology
                                                </option>
                                            </select>
                                        </td>
                                        <td>
                                            <select
                                                className="department_tretmt_with"
                                                value={row.treatingDoctor}
                                                onChange={(e) =>
                                                    handleChangeRow3(
                                                        index,
                                                        "treatingDoctor",
                                                        e.target.value
                                                    )
                                                }
                                            >
                                                <option value="">Select</option>
                                                <option value="Dr.Vishwa MBBS,MBA">
                                                    Dr.Vishwa MBBS,MBA
                                                </option>
                                                <option value="Dr.Tamil B.SC,MS,MBBS">
                                                    Dr.Tamil B.SC,MS,MBBS
                                                </option>
                                                <option value="Dr.Rajesh MBBS,BA">
                                                    Dr.Rajesh MBBS,BA
                                                </option>
                                            </select>
                                        </td>
                                        <td>
                                            <input
                                                type="number"
                                                className="ICD_Code"
                                                value={row.contactNumber3}
                                                onChange={(e) =>
                                                    handleChangeRow3(
                                                        index,
                                                        "contactNumber3",
                                                        e.target.value
                                                    )
                                                }
                                            />
                                        </td>
                                        <td>
                                            <input
                                                type="number"
                                                className="ICD_Code"
                                                value={row.registrationNumber}
                                                onChange={(e) =>
                                                    handleChangeRow3(
                                                        index,
                                                        "registrationNumber",
                                                        e.target.value
                                                    )
                                                }
                                            />
                                        </td>
                                        <td>
                                            <input
                                                type="text"
                                                className="ICD_Code"
                                                value={row.medicalCouncil}
                                                onChange={(e) =>
                                                    handleChangeRow3(
                                                        index,
                                                        "medicalCouncil",
                                                        e.target.value
                                                    )
                                                }
                                            />
                                        </td>
                                        <td className="add32_Code">
                                            <span onClick={() => removeRow3(index)}>
                                                <RemoveIcon className="add32_Code" />
                                            </span>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                    <br></br>

                    <div className="div_ckkkbox_head">
                        <div className="tremt_chkbox_info">
                            <label className="checkbox-label">
                                <input
                                    type="checkbox"
                                    className="checkbox-input"
                                    name="icuManagement"
                                    checked={checkboxStateTreatment.icuManagement}
                                    onChange={handleCheckboxChangeTreatment}
                                />
                                ICU Management
                            </label>
                            <label className="checkbox-label">
                                <input
                                    type="checkbox"
                                    className="checkbox-input"
                                    name="dialysis"
                                    checked={checkboxStateTreatment.dialysis}
                                    onChange={handleCheckboxChangeTreatment}
                                />
                                Dialysis
                            </label>
                            <label className="checkbox-label">
                                <input
                                    type="checkbox"
                                    className="checkbox-input"
                                    name="chemotherapy"
                                    checked={checkboxStateTreatment.chemotherapy}
                                    onChange={handleCheckboxChangeTreatment}
                                />
                                Chemotherapy
                            </label>
                            <label className="checkbox-label">
                                <input
                                    type="checkbox"
                                    className="checkbox-input"
                                    name="radiation"
                                    checked={checkboxStateTreatment.radiation}
                                    onChange={handleCheckboxChangeTreatment}
                                />
                                Radiation
                            </label>
                        </div>
                    </div>
                    <br></br>

                    <div className="RegisFormcon column_regisFormcon_forinsurance Spl_backcolr_09">
                        <div className="RegisForm_1 column_RegisForm_1_forinsurance Spl_backcolr_09_bottom">
                            <label className="fe_l5f">
                                Medical Management <span>:</span>
                            </label>

                            <div className="ewj_i87_head">
                                <div className="ewj_i87">
                                    <input
                                        type="radio"
                                        id="medicalManagementYes"
                                        name="medicalManagement"
                                        value="Yes"
                                        checked={medicalManagement === "Yes"}
                                        onChange={handleCheckboxChangeMedical}
                                    ></input>

                                    <label htmlFor="medicalManagementYes">Yes</label>
                                </div>

                                <div className="ewj_i87">
                                    <input
                                        type="radio"
                                        id="medicalManagementNo"
                                        name="medicalManagement"
                                        value="No"
                                        checked={medicalManagement === "No"}
                                        onChange={handleCheckboxChangeMedical}
                                    ></input>
                                    <label htmlFor="medicalManagementNo">No</label>
                                </div>
                            </div>
                        </div>
                    </div>

                    {medicalManagement === "Yes" && (
                        <>

                            <div className="txtars3_wit_hdj">
                                <label>Details</label>
                                <textarea
                                    name="details"
                                    placeholder="Enter Details"
                                    value={TreatmentTxtareaDetails}
                                    onChange={handleTextAreaChangeDetails}
                                ></textarea>
                            </div>


                            <>
                                <div className="Selected-table-container">
                                    <table className="selected-medicine-table2 _hide_hover_table">
                                        <thead className="Spl_backcolr_09">
                                            <tr>
                                                <th className="Provisional_Diagnosis">
                                                    Treatment
                                                </th>
                                                <th className="ICD_Code">
                                                    ICD 10 PCS/Hospital Code
                                                </th>

                                                <th className="add32_Code">
                                                    <span onClick={addRow4}>
                                                        <AddIcon className="add32_Code" />
                                                    </span>
                                                </th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {rows4.map((row, index) => (
                                                <tr key={index}>
                                                    <td>
                                                        <select
                                                            className="department_tretmt_with"
                                                            value={row.treatment}
                                                            onChange={(e) =>
                                                                handleChangeRow4(
                                                                    index,
                                                                    "treatment",
                                                                    e.target.value
                                                                )
                                                            }
                                                        >
                                                            <option value="">Select</option>
                                                            <option value="Treatment1">
                                                                Treatment 1
                                                            </option>
                                                            <option value="Treatment2">
                                                                Treatment 2
                                                            </option>
                                                            <option value="Treatment3">
                                                                Treatment 3
                                                            </option>
                                                        </select>
                                                    </td>
                                                    <td>
                                                        <input
                                                            className="Provisional_Diagnosis"
                                                            value={row.pcsHospitalCode}
                                                            onChange={(e) =>
                                                                handleChangeRow4(
                                                                    index,
                                                                    "pcsHospitalCode",
                                                                    e.target.value
                                                                )
                                                            }
                                                        />
                                                    </td>
                                                    <td className="add32_Code">
                                                        <span onClick={() => removeRow4(index)}>
                                                            <RemoveIcon className="add32_Code" />
                                                        </span>
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>
                            </>
                        </>
                    )}
                    <br></br>

                    <div className="RegisFormcon column_regisFormcon_forinsurance Spl_backcolr_09">
                        <div className="RegisForm_1 column_RegisForm_1_forinsurance Spl_backcolr_09_bottom">
                            <label className="fe_l5f">
                                Surgical Management <span>:</span>
                            </label>

                            <div className="ewj_i87_head">
                                <div className="ewj_i87">
                                    <input
                                        type="radio"
                                        id="surgicalManagementYes"
                                        name="surgicalManagement"
                                        value="Yes"
                                        checked={surgicalManagement === "Yes"}
                                        onChange={handleCheckboxChangeSurgical}
                                    ></input>

                                    <label htmlFor="surgicalManagementYes">Yes</label>
                                </div>

                                <div className="ewj_i87">
                                    <input
                                        type="radio"
                                        id="surgicalManagementNo"
                                        name="surgicalManagement"
                                        value="No"
                                        checked={surgicalManagement === "No"}
                                        onChange={handleCheckboxChangeSurgical}
                                    ></input>
                                    <label htmlFor="surgicalManagementNo">No</label>
                                </div>
                            </div>
                        </div>
                    </div>
                </>
                {surgicalManagement === "Yes" &&
                    additionalSurgicalOptions.map((option, index) => (
                        <>
                            {/* {department3.map((department, index) => ( */}
                            <>
                                <div key={index}>
                                    <div className="surgical_flex_srtgt">
                                        <div className="RegisForm_1 column_RegisForm_1_forinsurance surgical_flex_srtgt_div">
                                            <label>
                                                Department <span>:</span>{" "}
                                            </label>
                                            <select
                                                className="department_tretmt"
                                                name="departmentSurgical"
                                                value={option.departmentSurgical}
                                                onChange={(e) =>
                                                    setAdditionalSurgicalOptions((prev) => {
                                                        let updated = [...prev];
                                                        let newrow = updated[index];
                                                        newrow['departmentSurgical'] = e.target.value;
                                                        updated[index] = newrow;
                                                        return updated;
                                                    })
                                                }
                                               
                                            >
                                                <option value="">Select</option>
                                                <option value="Cardiology">Cardiology</option>
                                                <option value="Urology">Urology</option>
                                                <option value="Dermatology">
                                                    Dermatology
                                                </option>
                                            </select>
                                        </div>
                                        <div className="RegisForm_1 column_RegisForm_1_forinsurance surgical_flex_srtgt_div">
                                            <label>
                                                {" "}
                                                Surgeon <span>:</span>{" "}
                                            </label>
                                            <select
                                                className="department_tretmt"
                                                name="surgeonSurgical"
                                                value={option.surgeonSurgical}
                                                onChange={(e) =>
                                                    setAdditionalSurgicalOptions((prev) => {
                                                        let updated = [...prev];
                                                        let newrow = updated[index];
                                                        newrow['surgeonSurgical'] = e.target.value;
                                                        updated[index] = newrow;
                                                        return updated;
                                                    })
                                                }
                                                
                                            >
                                                <option value="">Select</option>
                                                <option value="Dr.Vishwa MBBS,MBA">
                                                    Dr.Vishwa MBBS,MBA
                                                </option>
                                                <option value="Dr.Tamil B.SC,MS,MBBS">
                                                    Dr.Tamil B.SC,MS,MBBS
                                                </option>
                                                <option value="Dr.Rajesh MBBS,BA">
                                                    Dr.Rajesh MBBS,BA
                                                </option>
                                            </select>
                                        </div>

                                        <div className="div_ckkkbox_head dwcw3wd">
                                            <div className="RegisForm_1 column_RegisForm_1_forinsurance surgical_flex_srtgt_div efws">
                                                <label
                                                    style={{ width: "280px", padding: "5px" }}
                                                >
                                                    {" "}
                                                    Type of Anesthesia <span>:</span>{" "}
                                                </label>
                                            </div>
                                            <div className="jkdll_piss_head">
                                                {Object.keys(option.CheckboxStates).map((ppp, indx) => (

                                                    <div className="jkdll_piss" key={indx}> {console.log(ppp, indx, index)}
                                                        <label className="checkbox-label">
                                                            <input
                                                                type="checkbox"
                                                                className="checkbox-input"
                                                                name={ppp}
                                                                checked={option.CheckboxStates[ppp]}
                                                                onChange={(e) => {
                                                                    setAdditionalSurgicalOptions((prev) => {
                                                                        let updated = [...prev];
                                                                        let newrow = updated[index];
                                                                        newrow['CheckboxStates'][ppp] = e.target.checked;
                                                                        updated[index] = newrow;
                                                                        return updated;
                                                                    });
                                                                }}
                                                            />

                                                            {ppp === "laAnesthesia" ? 'LA'
                                                                : ppp === "raAnesthesia" ? "RA"
                                                                    : ppp === "saAnesthesia" ? "SA"
                                                                        : ppp === "eaAnesthesia" ? "EA"
                                                                            : 'GA'
                                                            }
                                                        </label>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </>
                            {/* // ))} */}

                            <div className="RegisFormcon column_regisFormcon_forinsurance Spl_backcolr_09">
                                <div className="RegisForm_1 column_RegisForm_1_forinsurance Spl_backcolr_09_bottom">
                                    <label>
                                        Type <span>:</span>
                                    </label>

                                    <div className="ewj_i87_head">
                                        <div className="ewj_i87 ewj_i87_secd">
                                            <input
                                                type="radio"
                                                name={option['Type']}
                                                value="emergency"
                                                checked={option['Type'] === "emergency"}
                                                onChange={(e) =>
                                                    setAdditionalSurgicalOptions((prev) => {
                                                        let updated = [...prev];
                                                        let newrow = updated[index];
                                                        newrow['Type'] = e.target.value;
                                                        updated[index] = newrow;
                                                        return updated;
                                                    })
                                                }
                                            ></input>
                                            <label htmlFor={`emergencyYes${index}`}>
                                                Emergency
                                            </label>
                                        </div>

                                        <div className="ewj_i87 ewj_i87_secd">
                                            <input
                                                type="radio"
                                                name={option['Type']}
                                                value="elective"
                                                checked={option['Type'] === "elective"}
                                                onChange={(e) =>
                                                    setAdditionalSurgicalOptions((prev) => {
                                                        let updated = [...prev];
                                                        let newrow = updated[index];
                                                        newrow['Type'] = e.target.value;
                                                        updated[index] = newrow;
                                                        return updated;
                                                    })
                                                }
                                            ></input>
                                            <label htmlFor={`electiveYes${index}`}>
                                                Elective
                                            </label>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div className="Selected-table-container">
                                <table className="selected-medicine-table2 _hide_hover_table">
                                    <thead className="Spl_backcolr_09">
                                        <tr>
                                            <th className="Provisional_Diagnosis">
                                                Procedure
                                            </th>
                                            <th className="ICD_Code">
                                                ICD 10 PCS / Hospital Code
                                            </th>
                                            <th className="add32_Code">
                                                <span onClick={() => addRow5(index)}>
                                                    {" "}
                                                    {/* Pass index to addRow5 */}
                                                    <AddIcon className="add32_Code" />
                                                </span>
                                            </th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {option?.procedureTables &&
                                            option?.procedureTables.map((row, rowIndex) => (
                                                <tr key={rowIndex}>{console.log(row)}
                                                    <td>
                                                        <input
                                                            className="Provisional_Diagnosis"
                                                            value={row.procedureSurgical}
                                                            onChange={(e) =>
                                                                
                                                                setAdditionalSurgicalOptions((prev) => {
                                                                    let updated = [...prev];
                                                                    let newrow = updated[index];
                                                                    newrow['procedureTables'][rowIndex]['procedureSurgical'] = e.target.value;
                                                                    updated[index] = newrow;
                                                                    return updated;
                                                                })
                                                            }
                                                        />
                                                    </td>
                                                    <td>
                                                        <input
                                                            className="ICD_Code"
                                                            value={row.pcdHospitalCodeSurgical}
                                                            onChange={(e) =>
                                                                setAdditionalSurgicalOptions((prev) => {
                                                                    let updated = [...prev];
                                                                    let newrow = updated[index];
                                                                    newrow['procedureTables'][rowIndex]['pcdHospitalCodeSurgical'] = e.target.value;
                                                                    updated[index] = newrow;
                                                                    return updated;
                                                                })
                                                            }
                                                        />
                                                    </td>
                                                    <td className="add32_Code">
                                                        <span
                                                            onClick={() =>
                                                                removeRow5(index, rowIndex)
                                                            }
                                                        >
                                                            {" "}
                                                            {/* Pass index and rowIndex to removeRow5 */}
                                                            <RemoveIcon className="add32_Code" />
                                                        </span>
                                                    </td>
                                                </tr>
                                            ))}
                                    </tbody>
                                </table>
                            </div>
                        </>
                    ))}

                {surgicalManagement === "Yes" && (
                    <>
                    <br/>
                    <div className="SUGCL_AD_PO0">
                        <div
                            className="add32_Code_POK8"
                            onClick={addAdditionalSurgicalOption}
                        >
                            <AddIcon />
                        </div>

                        {additionalSurgicalOptions.length > 0 && (
                            <div
                                className="add32_Code_POK8"
                                onClick={removeAdditionalSurgicalOption}
                            >
                                <RemoveIcon />
                            </div>
                        )}
                    </div>
                    </>
                )}


            </div>

            {/* <div className="submit_button_prev_next">
                <button onClick={SavebtnFun}>
                    Save
                </button>
            </div> */}

        </>
    );
}
