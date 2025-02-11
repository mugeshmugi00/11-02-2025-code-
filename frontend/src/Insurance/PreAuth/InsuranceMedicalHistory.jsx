import * as React from "react";
import { useEffect, useState } from "react";
import axios from "axios";
import { useDispatch, useSelector } from "react-redux";
import AddIcon from "@mui/icons-material/Add";
import RemoveIcon from "@mui/icons-material/Remove";



export default function InsuranceMedicalHistory() {

  
  const dispatchvalue = useDispatch();

  const userRecord = useSelector((state) => state.userRecord?.UserData);

  const InsuranceUpdatedata = {}

//   const InsuranceUpdatedata = useSelector(
//     (state) => state.InsuranceStore?.InsuranceUpdatedata
//   );

  
  // console.log("natha", IPPatientDetailes);


  const [formDataTxtarea, setFormDataTxtarea] = useState({
    ComplaintsDuration: "",
    HistoryPresentingIllness: "",
    PastHistory: "",
  });


  const [diabetes, setDiabetes] = useState("No");
  const [diabetesDuration, setDiabetesDuration] = useState("");
  const [diabetesMedication, setDiabetesMedication] = useState("");

  const [hyperTension, setHyperTension] = useState("No");
  const [hyperTensionDuration, setHyperTensionDuration] = useState("");
  const [hyperTensionMedication, setHyperTensionMedication] = useState("");

  const [hyperlipiDemias, setHyperlipiDemias] = useState("No");
  const [hyperlipiDemiasDuration, setHyperlipiDemiasDuration] = useState("");
  const [hyperlipiDemiasMedication, setHyperlipiDemiasMedication] =
    useState("");

  const [osteoarthritis, setOsteoarthritis] = useState("No");
  const [osteoarthritisDuration, setOsteoarthritisDuration] = useState("");
  const [osteoarthritisMedication, setOsteoarthritisMedication] = useState("");

  const [bronchialAsthma, setBronchialAsthma] = useState("No");
  const [bronchialAsthmaDuration, setBronchialAsthmaDuration] = useState("");
  const [bronchialAsthmaMedication, setBronchialAsthmaMedication] =
    useState("");

  const [cvd, setCvd] = useState("No");
  const [cvdDuration, setCvdDuration] = useState("");
  const [cvdMedication, setCvdMedication] = useState("");

  const [cva, setCva] = useState("No");
  const [cvaDuration, setCvaDuration] = useState("");
  const [cvaMedication, setCvaMedication] = useState("");

  const [kochs, setKochs] = useState("No");
  const [kochsDuration, setKochsDuration] = useState("");
  const [kochsMedication, setKochsMedication] = useState("");

  const [malignancy, setMalignancy] = useState("No");
  const [malignancyDuration, setMalignancyDuration] = useState("");
  const [malignancyMedication, setMalignancyMedication] = useState("");

  const [alcohol, setAlcohol] = useState("No");
  const [alcoholDuration, setAlcoholDuration] = useState("");
  const [alcoholNotes, setAlcoholNotes] = useState("");

  const [smoking, setSmoking] = useState("No");
  const [smokingDuration, setSmokingDuration] = useState("");
  const [smokingNotes, setSmokingNotes] = useState("");

  const [hiv, setHiv] = useState("No");
  const [hivDuration, setHivDuration] = useState("");
  const [hivNotes, setHivNotes] = useState("");

  const [hbSAg, setHbSAg] = useState("No");
  const [hbSAgDuration, setHbSAgDuration] = useState("");
  const [hbSAgNotes, setHbSAgNotes] = useState("");

  const [hcv, setHCV] = useState("No");
  const [hcvDuration, setHCVDuration] = useState("");
  const [hcvNotes, setHCVNotes] = useState("");

  const [diabetesFamily, setDiabetesFamily] = useState("No");
  const [diabetesRelationship, setDiabetesRelationship] = useState("");
  const [diabetesNotes, setDiabetesNotes] = useState("");

  const [hyperTensionFamily, setHyperTensionFamily] = useState("No");
  const [hyperTensionRelationshipFamily, setHyperTensionRelationshipFamily] = useState("");
  const [hyperTensionNotesFamily, setHyperTensionNotesFamily] = useState("");

  const [kochsFamily, setKochsFamily] = useState("No");
  const [kochsRelationship, setKochsRelationship] = useState("");
  const [kochsNotes, setKochsNotes] = useState("");

  const [geneticDisorderFamily, setGeneticDisorderFamily] = useState("No");
  const [geneticDisoderRelationship, setGeneticDisoderRelationship] = useState("");
  const [geneticDisoderNotes, setGeneticDisoderNotes] = useState("");



  const [medication, setMedication] = useState([
    {
      medicationName: "",
      medicationDuration: "",
    },
  ]);


// --------------------------------------------------------------

  const handleTextAreaChange = (event) => {
    const { name, value } = event.target;
    setFormDataTxtarea({
      ...formDataTxtarea,
      [name]: value,
    });
  };



  const handleCheckboxChange3 = (event) => {
    if(event.target.value === 'No'){
      setDiabetesDuration('')
      setDiabetesMedication('')
      setDiabetes(event.target.value);
    }else{
      setDiabetes(event.target.value);
    }
  };

  const handleDurationChange = (event) => {
    setDiabetesDuration(event.target.value);
  };

  const handleMedicationChange = (event) => {
    setDiabetesMedication(event.target.value);
  };

  const handleCheckboxChange4 = (event) => {
    if(event.target.value === 'No'){
    setHyperTension(event.target.value);
    setHyperTensionDuration('')
    setHyperTensionMedication('')
    }else{
    setHyperTension(event.target.value);
    }
  };


  const handleHyperTensionDurationChange = (event) => {
    setHyperTensionDuration(event.target.value);
  };

  const handleHyperTensionMedicationChange = (event) => {
    setHyperTensionMedication(event.target.value);
  };

  const handleCheckboxChange5 = (event) => {
    if(event.target.value === 'No'){

    setHyperlipiDemias(event.target.value);
    setHyperlipiDemiasDuration('')
    setHyperlipiDemiasMedication('')

    }else{
      setHyperlipiDemias(event.target.value);
    }
    
  };



  const handleHyperlipiDemiasDurationChange = (event) => {
    setHyperlipiDemiasDuration(event.target.value);
  };

  const handleHyperlipiDemiasMedicationChange = (event) => {
    setHyperlipiDemiasMedication(event.target.value);
  };

  const handleCheckboxChange6 = (event) => {
   if(event.target.value === 'No'){
    setOsteoarthritis(event.target.value);
    setOsteoarthritisDuration('')
    setOsteoarthritisMedication('')
   }else{
    setOsteoarthritis(event.target.value);
   }
  };

  const handleOsteoarthritisDurationChange = (event) => {
    setOsteoarthritisDuration(event.target.value);
  };

  const handleOsteoarthritisMedicationChange = (event) => {
    setOsteoarthritisMedication(event.target.value);
  };

  const handleCheckboxChange7 = (event) => {
    if(event.target.value === 'No'){
      setBronchialAsthmaDuration('')
      setBronchialAsthmaMedication('')
      setBronchialAsthma(event.target.value);
    }else{
      setBronchialAsthma(event.target.value);
    }
  };
  const handleBronchialAsthmaDurationChange = (event) => {
    setBronchialAsthmaDuration(event.target.value);
  };

  const handleBronchialAsthmaMedicationChange = (event) => {
    setBronchialAsthmaMedication(event.target.value);
  };

  const handleCheckboxChange8 = (event) => {
    if(event.target.value === 'No'){
      setCvdDuration('')
      setCvdMedication('')
      setCvd(event.target.value);
    }else{
      setCvd(event.target.value);
    }
    
  };
  const handleCvdDurationChange = (event) => {
    setCvdDuration(event.target.value);
  };

  const handleCvdMedicationChange = (event) => {
    setCvdMedication(event.target.value);
  };

  const handleCheckboxChange9 = (event) => {
    if(event.target.value === 'No'){
      setCvaDuration('')
      setCvaMedication('')
      setCva(event.target.value);
    }else{
      setCva(event.target.value);      
    }
  };

  const handleCvaDurationChange = (event) => {
    setCvaDuration(event.target.value);
  };

  const handleCvaMedicationChange = (event) => {
    setCvaMedication(event.target.value);
  };

  const handleCheckboxChange10 = (event) => {
    if(event.target.value === 'No'){
      setKochsDuration('')
      setKochsMedication('')
      setKochs(event.target.value);
    }else{
      setKochs(event.target.value);
    }
  };
  const handleKochsDurationChange = (event) => {
    setKochsDuration(event.target.value);
  };

  const handleKochsMedicationChange = (event) => {
    setKochsMedication(event.target.value);
  };

  const handleCheckboxChange11 = (event) => {
    if(event.target.value === 'No'){
      setMalignancyDuration('')
      setMalignancyMedication('')
      setMalignancy(event.target.value);
    }else{
      setMalignancy(event.target.value);
    }
  };
  const handleMalignancyDurationChange = (event) => {
    setMalignancyDuration(event.target.value);
  };

  const handleMalignancyMedicationChange = (event) => {
    setMalignancyMedication(event.target.value);
  };


  const handleCheckboxChangeAlcohol = (event) => {
    if(event.target.value === 'No'){
      setAlcoholDuration('')
      setAlcoholNotes('')
      setAlcohol(event.target.value);
    }else{
      setAlcohol(event.target.value);
    }
  };

  const handleAlcoholDurationChange = (event) => {
    setAlcoholDuration(event.target.value);
  };

  const handleAlcoholNotesChange = (event) => {
    setAlcoholNotes(event.target.value);
  };

  const handleCheckboxChangeSmoking = (event) => {
   if(event.target.value === 'No'){
    setSmokingDuration('')
    setSmokingNotes('')
    setSmoking(event.target.value);
   }else{
    setSmoking(event.target.value);
   }
  };

  const handleSmokingDurationChange = (event) => {
    setSmokingDuration(event.target.value);
  };

  const handleSmokingNotesChange = (event) => {
    setSmokingNotes(event.target.value);
  };

  const handleCheckboxChangeHIV = (event) => {
    if(event.target.value === 'No'){
      setHivDuration('')
      setHivNotes('')
      setHiv(event.target.value);
    }else{
      setHiv(event.target.value);
    }
  };

  const handleHIVDurationChange = (event) => {
    setHivDuration(event.target.value);
  };

  const handleHIVNotesChange = (event) => {
    setHivNotes(event.target.value);
  };

  const handleCheckboxChangeHbSAg = (event) => {
  if(event.target.value === 'No'){
    setHbSAgDuration('')
    setHbSAgNotes('')
    setHbSAg(event.target.value);
  }else{
    setHbSAg(event.target.value);
  }
  };

  const handleHbSAgDurationChange = (event) => {
    setHbSAgDuration(event.target.value);
  };

  const handleHbSAgNotesChange = (event) => {
    setHbSAgNotes(event.target.value);
  };

  const handleCheckboxChangeHCV = (event) => {
    if(event.target.value === 'No'){
      setHCVDuration('')
      setHCVNotes('')
      setHCV(event.target.value);
    }else{
      setHCV(event.target.value);
    }
  };

  const handleHCVDurationChange = (event) => {
    setHCVDuration(event.target.value);
  };

  const handleHCVNotesChange = (event) => {
    setHCVNotes(event.target.value);
  };


  const handleChangeRowMedication = (index, key, value) => {
    const updatedMedication = [...medication]; 
    updatedMedication[index][key] = value;
    setMedication(updatedMedication);
};

  const addRowMedication = () => {
    setMedication((prevRows) => [
      ...prevRows,
      {
        medicationName: "",
        medicationDuration: "",
      },
    ]);
  };
  const removeRowMedication = (index) => {
    setMedication((prevRows) =>
      prevRows.filter((row, rowIndex) => rowIndex !== index)
    );
  };

  const handleCheckboxChangeFamily = (event) => {
    if(event.target.value === 'No'){
      setDiabetesRelationship('')
      setDiabetesNotes('')
      setDiabetesFamily(event.target.value);
    }else{
      setDiabetesFamily(event.target.value);
    }
  };

  const handleRelationshipChangeFamily = (event) => {
    setDiabetesRelationship(event.target.value);
  };

  const handleNotesChangeFamily = (event) => {
    setDiabetesNotes(event.target.value);
  };

  const handleCheckboxChangeFamily2 = (event) => {
    if(event.target.value === 'No'){
      setHyperTensionRelationshipFamily('')
      setHyperTensionNotesFamily('')
      setHyperTensionFamily(event.target.value);
    }else{
      setHyperTensionFamily(event.target.value);
    }
  };
  const handleHyperTensionRelationshipChange = (event) => {
    setHyperTensionRelationshipFamily(event.target.value);
  };

  const handleHyperTensionNotesChange = (event) => {
    setHyperTensionNotesFamily(event.target.value);
  };

  const handleCheckboxChangeFamily3 = (event) => {
    if(event.target.value === 'No'){
      setKochsRelationship('')
      setKochsNotes('')
      setKochsFamily(event.target.value);
    }else{
      setKochsFamily(event.target.value);
    }
  };
  const handleKochsRelationshipChange = (event) => {
    setKochsRelationship(event.target.value);
  };

  const handleKochsNotesChange = (event) => {
    setKochsNotes(event.target.value);
  };

  const handleCheckboxChangeFamily4 = (event) => {
    if(event.target.value === 'No'){
      setGeneticDisoderRelationship('')
      setGeneticDisoderNotes('')
      setGeneticDisorderFamily(event.target.value);
    }else{
      setGeneticDisorderFamily(event.target.value);
    }
  };
  const handleGeneticDisorderRelationshipChange = (event) => {
    setGeneticDisoderRelationship(event.target.value);
  };

  const handleGeneticDisorderNotesChange = (event) => {
    setGeneticDisoderNotes(event.target.value);
  };


  const SavebtnFun =()=>{
    
    const params={

      MRN: InsuranceUpdatedata.MRN,
      ContactNumber:InsuranceUpdatedata.ContactNumber,

      Location:userRecord.location,
      createAt:userRecord.username,

      formDataTxtarea: formDataTxtarea,

      diabetesdata:{
        diabetes:diabetes,
        diabetesDuration:diabetesDuration,
        diabetesMedication:diabetesMedication,
      },
      hyperTensiondata:{
        hyperTension:hyperTension,
        hyperTensionDuration:hyperTensionDuration,
        hyperTensionMedication:hyperTensionMedication,

      },
      hyperlipiDemiasdata:{
        hyperlipiDemias:hyperlipiDemias,
        hyperlipiDemiasDuration:hyperlipiDemiasDuration,
        hyperlipiDemiasMedication:hyperlipiDemiasMedication,

      },
      osteoarthritisdata:{
        osteoarthritis:osteoarthritis,
        osteoarthritisDuration:osteoarthritisDuration,
        osteoarthritisMedication:osteoarthritisMedication,

      },
      bronchialAsthmadata:{
        bronchialAsthma:bronchialAsthma,
        bronchialAsthmaDuration:bronchialAsthmaDuration,
        bronchialAsthmaMedication:bronchialAsthmaMedication,

      },

      cvddata:{
        cvd:cvd,
        cvdDuration:cvdDuration,
        cvdMedication:cvdMedication,

      },

      cvadata:{
        cva:cva,
        cvaDuration:cvaDuration,
        cvaMedication:cvaMedication,

      },
      kochsdata:{
        kochs:kochs,
        kochsDuration:kochsDuration,
        kochsMedication:kochsMedication,

      },
      malignancydata:{
        malignancy:malignancy,
        malignancyDuration:malignancyDuration,
        malignancyMedication:malignancyMedication,
      },
      alcoholdata:{
        alcohol:alcohol,
        alcoholDuration:alcoholDuration,
        alcoholNotes:alcoholNotes,
      },
      smokingdata:{
        smoking:smoking,
        smokingDuration:smokingDuration,
        smokingNotes:smokingNotes,
      },
      hivdata:{
        hiv:hiv,
        hivDuration:hivDuration,
        hivNotes:hivNotes,
      },
      hbSAgdata:{
        hbSAg:hbSAg,
        hbSAgDuration:hbSAgDuration,
        hbSAgNotes:hbSAgNotes,
      },
      hcvdata:{
        hcv:hcv,
        hcvDuration:hcvDuration,
        hcvNotes:hcvNotes,
      },



      diabetesFamilydata:{
        diabetesFamily:diabetesFamily,
        diabetesRelationship:diabetesRelationship,
        diabetesNotes:diabetesNotes,
      },
      hyperTensionFamilydata:{
        hyperTensionFamily:hyperTensionFamily,
        hyperTensionRelationshipFamily:hyperTensionRelationshipFamily,
        hyperTensionNotesFamily:hyperTensionNotesFamily,
      },
      kochsFamilydata:{
        kochsFamily:kochsFamily,
        kochsRelationship:kochsRelationship,
        kochsNotes:kochsNotes,
      },
      geneticDisorderFamilydata:{
        geneticDisorderFamily:geneticDisorderFamily,
        geneticDisoderRelationship:geneticDisoderRelationship,
        geneticDisoderNotes:geneticDisoderNotes,
      },
      
      medication:medication,

      MainPageCompleted:"MainPage1",
      PageCompleted:"ExaminationFinding"
    }


    axios.post(`https://vesoftometic.co.in/Insurance/Post_Pre_Auth_Form_Medical_History`,params)
    .then((response) => {
        console.log('Form data submitted.',response.data)
        dispatchvalue({type: "InsurancePageChange",value:"ExaminationFinding"});


    })
    .catch((error) => {
        console.error(error);
    });




  }




  // -----------------------------------------------up



  
  useEffect(()=>{
    if(Object.values(InsuranceUpdatedata).length !== 0){
        // console.log('Vathuruchu',InsuranceUpdatedata)            
     axios.get(
    `https://vesoftometic.co.in/Insurance/get_Pre_Auth_Form_Medical_History`,{
        params: InsuranceUpdatedata.MRN
    }
    )
    .then((response) => {
    // console.log('vrrrr',response.data);
    
    const data=response.data[0]

    // console.log('lklkdata',data)

  if(Object.keys(data).length !==0){
    setFormDataTxtarea((prev)=>({
      ...prev,
      ComplaintsDuration:data.ComplaintsDuration,
      HistoryPresentingIllness:data.HistoryPresentingIllness,
      PastHistory:data.PastHistory,
    }))

    setDiabetes(data.diabetes)
    setDiabetesDuration(data.diabetesDuration)
    setDiabetesMedication(data.diabetesMedication)

    setHyperTension(data.hyperTension)
    setHyperTensionDuration(data.hyperTensionDuration)
    setHyperTensionMedication(data.hyperTensionMedication)


    setHyperlipiDemias(data.hyperlipiDemias)
    setHyperlipiDemiasDuration(data.hyperlipiDemiasDuration)
    setHyperlipiDemiasMedication(data.hyperlipiDemiasMedication)

    setOsteoarthritis(data.osteoarthritis)
    setOsteoarthritisDuration(data.osteoarthritisDuration)
    setOsteoarthritisMedication(data.osteoarthritisMedication)


    setBronchialAsthma(data.bronchialAsthma)
    setBronchialAsthmaDuration(data.bronchialAsthmaDuration)
    setBronchialAsthmaMedication(data.bronchialAsthmaMedication)

    setCvd(data.cvd)
    setCvdDuration(data.cvdDuration)
    setCvdMedication(data.cvdMedication)

    

    setCva(data.cva)
    setCvaDuration(data.cvaDuration)
    setCvaMedication(data.cvaMedication)


    setKochs(data.kochs)
    setKochsDuration(data.kochsDuration)
    setKochsMedication(data.kochsMedication)

    setMalignancy(data.malignancy)
    setMalignancyDuration(data.malignancyDuration)
    setMalignancyMedication(data.malignancyMedication)

    setAlcohol(data.alcohol)
    setAlcoholDuration(data.alcoholDuration)
    setAlcoholNotes(data.alcoholNotes)

    setSmoking(data.smoking)
    setSmokingDuration(data.smokingDuration)
    setSmokingNotes(data.smokingNotes)

    setHiv(data.hiv)
    setHivDuration(data.hivDuration)
    setHivNotes(data.hivNotes)

    setHbSAg(data.hbSAg)
    setHbSAgDuration(data.hbSAgDuration)
    setHbSAgNotes(data.hbSAgNotes)

    setHCV(data.hcv)
    setHCVDuration(data.hcvDuration)
    setHCVNotes(data.hcvNotes)

    setDiabetesFamily(data.diabetesFamily)
    setDiabetesRelationship(data.diabetesRelationship)
    setDiabetesNotes(data.diabetesNotes)

    setHyperTensionFamily(data.hyperTensionFamily)
    setHyperTensionRelationshipFamily(data.hyperTensionRelationshipFamily)
    setHyperTensionNotesFamily(data.hyperTensionNotesFamily)

    setKochsFamily(data.kochsFamily)
    setKochsRelationship(data.kochsRelationship)
    setKochsNotes(data.kochsNotes)


    setGeneticDisorderFamily(data.geneticDisorderFamily)
    setGeneticDisoderRelationship(data.geneticDisoderRelationship)
    setGeneticDisoderNotes(data.geneticDisoderNotes)
     
    if(data.medication.length!==0){
      setMedication(data.medication)
    }
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
    
        
        <div className="txtars3_wit_hdj">
            <label>Chief Complaints & Duration</label>
            <textarea
            name="ComplaintsDuration"
            placeholder="Enter Complaints & Duration"
            value={formDataTxtarea.ComplaintsDuration}
            onChange={handleTextAreaChange}
            ></textarea>
        </div>
        <br></br>
        <div className="txtars3_wit_hdj">
            <label>History of Presenting Illness</label>
            <textarea
            name="HistoryPresentingIllness"
            placeholder="Enter History of Presenting Illness"
            value={formDataTxtarea.HistoryPresentingIllness}
            onChange={handleTextAreaChange}
            ></textarea>
        </div>
        <br></br>
        <div className="txtars3_wit_hdj">
            <label>Past History</label>
            <textarea
            name="PastHistory"
            placeholder="Enter Past History"
            value={formDataTxtarea.PastHistory}
            onChange={handleTextAreaChange}
            ></textarea>
        </div>
        
        <div className="Selected-table-container">
            <table className="selected-medicine-table2 _hide_hover_table">
            <thead className="Spl_backcolr_09">
                <tr>
                <th className="HistoryOfChronicIllness">
                    History Of Chronic Illness
                </th>
                <th className="wiejdwi8">Duration in Years</th>
                <th className="wiejdwi8">Medication</th>
                </tr>
            </thead>

            <tbody>
                <tr>
                <td>
                    <div className="spac_betwn_hstychronc">
                    <label className="spac_betwn_hstychronc_label">
                        Diabetes <span>:</span>
                    </label>

                    <div className="ewj_i87_head">
                        <div className="ewj_i87">
                        <input
                            type="radio"
                            id="diabetesYes"
                            name="diabetesYes"
                            value="Yes"
                            checked={diabetes === "Yes"}
                            onChange={handleCheckboxChange3}
                        ></input>

                        <label htmlFor="diabetesYes">Yes</label>
                        </div>

                        <div className="ewj_i87">
                        <input
                            type="radio"
                            id="diabetesNo"
                            name="diabetesNo"
                            value="No"
                            checked={diabetes === "No"}
                            onChange={handleCheckboxChange3}
                        ></input>
                        <label htmlFor="diabetesNo">No</label>
                        </div>
                    </div>
                    </div>
                </td>
                <td>
                    {diabetes == "Yes" && (
                    <input
                        type="text"
                        className="duration_90"
                        value={diabetesDuration}
                        onChange={handleDurationChange}
                    ></input>
                    )}
                </td>
                <td>
                    {diabetes == "Yes" && (
                    <input
                        type="text"
                        className="medication_90"
                        value={diabetesMedication}
                        onChange={handleMedicationChange}
                    ></input>
                    )}
                </td>
                </tr>

                <tr>
                <td>
                    <div className="spac_betwn_hstychronc">
                    <label className="spac_betwn_hstychronc_label">
                        Hypertension <span>:</span>
                    </label>

                    <div className="ewj_i87_head">
                        <div className="ewj_i87">
                        <input
                            type="radio"
                            id="hyperTensionYes"
                            name="hyperTensionYes"
                            value="Yes"
                            checked={hyperTension === "Yes"}
                            onChange={handleCheckboxChange4}
                        ></input>

                        <label htmlFor="hyperTensionYes">Yes</label>
                        </div>

                        <div className="ewj_i87">
                        <input
                            type="radio"
                            id="hyperTensionNo"
                            name="hyperTensionNo"
                            value="No"
                            checked={hyperTension === "No"}
                            onChange={handleCheckboxChange4}
                        ></input>
                        <label htmlFor="hyperTensionNo">No</label>
                        </div>
                    </div>
                    </div>
                </td>
                <td>
                    {" "}
                    {hyperTension == "Yes" && (
                    <input
                        type="text"
                        className="duration_90"
                        value={hyperTensionDuration}
                        onChange={handleHyperTensionDurationChange}
                    ></input>
                    )}
                </td>
                <td>
                    {" "}
                    {hyperTension == "Yes" && (
                    <input
                        type="text"
                        className="medication_90"
                        value={hyperTensionMedication}
                        onChange={handleHyperTensionMedicationChange}
                    ></input>
                    )}
                </td>
                </tr>

                <tr>
                <td>
                    <div className="spac_betwn_hstychronc">
                    <label className="spac_betwn_hstychronc_label">
                        Hyperlipidemias <span>:</span>
                    </label>

                    <div className="ewj_i87_head">
                        <div className="ewj_i87">
                        <input
                            type="radio"
                            id="hyperlipiDemiasYes"
                            name="hyperlipiDemiasYes"
                            value="Yes"
                            checked={hyperlipiDemias === "Yes"}
                            onChange={handleCheckboxChange5}
                        ></input>

                        <label htmlFor="hyperlipiDemiasYes">
                            Yes
                        </label>
                        </div>

                        <div className="ewj_i87">
                        <input
                            type="radio"
                            id="hyperlipiDemiasNo"
                            name="hyperlipiDemiasNo"
                            value="No"
                            checked={hyperlipiDemias === "No"}
                            onChange={handleCheckboxChange5}
                        ></input>
                        <label htmlFor="hyperlipiDemiasNo">
                            No
                        </label>
                        </div>
                    </div>
                    </div>
                </td>
                <td>
                    {" "}
                    {hyperlipiDemias == "Yes" && (
                    <input
                        type="text"
                        className="duration_90"
                        value={hyperlipiDemiasDuration}
                        onChange={handleHyperlipiDemiasDurationChange}
                    ></input>
                    )}
                </td>
                <td>
                    {" "}
                    {hyperlipiDemias == "Yes" && (
                    <input
                        type="text"
                        className="medication_90"
                        value={hyperlipiDemiasMedication}
                        onChange={
                        handleHyperlipiDemiasMedicationChange
                        }
                    ></input>
                    )}
                </td>
                </tr>

                <tr>
                <td>
                    <div className="spac_betwn_hstychronc">
                    <label className="spac_betwn_hstychronc_label">
                        Osteoarthritis <span>:</span>
                    </label>

                    <div className="ewj_i87_head">
                        <div className="ewj_i87">
                        <input
                            type="radio"
                            id="osteoarthritisYes"
                            name="osteoarthritisYes"
                            value="Yes"
                            checked={osteoarthritis === "Yes"}
                            onChange={handleCheckboxChange6}
                        ></input>

                        <label htmlFor="osteoarthritisYes">
                            Yes
                        </label>
                        </div>

                        <div className="ewj_i87">
                        <input
                            type="radio"
                            id="osteoarthritisNo"
                            name="osteoarthritisNo"
                            value="No"
                            checked={osteoarthritis === "No"}
                            onChange={handleCheckboxChange6}
                        ></input>
                        <label htmlFor="osteoarthritisNo">No</label>
                        </div>
                    </div>
                    </div>
                </td>
                <td>
                    {" "}
                    {osteoarthritis == "Yes" && (
                    <input
                        type="text"
                        className="duration_90"
                        value={osteoarthritisDuration}
                        onChange={handleOsteoarthritisDurationChange}
                    ></input>
                    )}
                </td>
                <td>
                    {" "}
                    {osteoarthritis == "Yes" && (
                    <input
                        type="text"
                        className="medication_90"
                        value={osteoarthritisMedication}
                        onChange={
                        handleOsteoarthritisMedicationChange
                        }
                    ></input>
                    )}
                </td>
                </tr>

                <tr>
                <td>
                    <div className="spac_betwn_hstychronc">
                    <label className="spac_betwn_hstychronc_label">
                        Bronchial Asthma <span>:</span>
                    </label>

                    <div className="ewj_i87_head">
                        <div className="ewj_i87">
                        <input
                            type="radio"
                            id="bronchialAsthmaYes"
                            name="bronchialAsthmaYes"
                            value="Yes"
                            checked={bronchialAsthma === "Yes"}
                            onChange={handleCheckboxChange7}
                        ></input>

                        <label htmlFor="bronchialAsthmaYes">
                            Yes
                        </label>
                        </div>

                        <div className="ewj_i87">
                        <input
                            type="radio"
                            id="bronchialAsthmaNo"
                            name="bronchialAsthmaNo"
                            value="No"
                            checked={bronchialAsthma === "No"}
                            onChange={handleCheckboxChange7}
                        ></input>
                        <label htmlFor="bronchialAsthmaNo">
                            No
                        </label>
                        </div>
                    </div>
                    </div>
                </td>
                <td>
                    {" "}
                    {bronchialAsthma == "Yes" && (
                    <input
                        type="text"
                        className="duration_90"
                        value={bronchialAsthmaDuration}
                        onChange={handleBronchialAsthmaDurationChange}
                    ></input>
                    )}
                </td>
                <td>
                    {" "}
                    {bronchialAsthma == "Yes" && (
                    <input
                        type="text"
                        className="medication_90"
                        value={bronchialAsthmaMedication}
                        onChange={
                        handleBronchialAsthmaMedicationChange
                        }
                    ></input>
                    )}
                </td>
                </tr>

                <tr>
                <td>
                    <div className="spac_betwn_hstychronc">
                    <label className="spac_betwn_hstychronc_label">
                        C.V.D <span>:</span>
                    </label>

                    <div className="ewj_i87_head">
                        <div className="ewj_i87">
                        <input
                            type="radio"
                            id="cvdYes"
                            name="cvdYes"
                            value="Yes"
                            checked={cvd === "Yes"}
                            onChange={handleCheckboxChange8}
                        ></input>

                        <label htmlFor="cvdYes">Yes</label>
                        </div>

                        <div className="ewj_i87">
                        <input
                            type="radio"
                            id="cvdNo"
                            name="cvdNo"
                            value="No"
                            checked={cvd === "No"}
                            onChange={handleCheckboxChange8}
                        ></input>
                        <label htmlFor="cvdNo">No</label>
                        </div>
                    </div>
                    </div>
                </td>
                <td>
                    {" "}
                    {cvd == "Yes" && (
                    <input
                        type="text"
                        className="duration_90"
                        value={cvdDuration}
                        onChange={handleCvdDurationChange}
                    ></input>
                    )}
                </td>
                <td>
                    {" "}
                    {cvd == "Yes" && (
                    <input
                        type="text"
                        className="medication_90"
                        value={cvdMedication}
                        onChange={handleCvdMedicationChange}
                    ></input>
                    )}
                </td>
                </tr>

                <tr>
                <td>
                    <div className="spac_betwn_hstychronc">
                    <label className="spac_betwn_hstychronc_label">
                        C.V.A <span>:</span>
                    </label>

                    <div className="ewj_i87_head">
                        <div className="ewj_i87">
                        <input
                            type="radio"
                            id="cvaYes"
                            name="cvaYes"
                            value="Yes"
                            checked={cva === "Yes"}
                            onChange={handleCheckboxChange9}
                        ></input>

                        <label htmlFor="cvaYes">Yes</label>
                        </div>

                        <div className="ewj_i87">
                        <input
                            type="radio"
                            id="cvaNo"
                            name="cvaNo"
                            value="No"
                            checked={cva === "No"}
                            onChange={handleCheckboxChange9}
                        ></input>
                        <label htmlFor="cvaNo">No</label>
                        </div>
                    </div>
                    </div>
                </td>
                <td>
                    {" "}
                    {cva == "Yes" && (
                    <input
                        type="text"
                        className="duration_90"
                        value={cvaDuration}
                        onChange={handleCvaDurationChange}
                    ></input>
                    )}
                </td>
                <td>
                    {" "}
                    {cva == "Yes" && (
                    <input
                        type="text"
                        className="medication_90"
                        value={cvaMedication}
                        onChange={handleCvaMedicationChange}
                    ></input>
                    )}
                </td>
                </tr>

                <tr>
                <td>
                    <div className="spac_betwn_hstychronc">
                    <label className="spac_betwn_hstychronc_label">
                        Kochs <span>:</span>
                    </label>

                    <div className="ewj_i87_head">
                        <div className="ewj_i87">
                        <input
                            type="radio"
                            id="kochsYes"
                            name="kochsYes"
                            value="Yes"
                            checked={kochs === "Yes"}
                            onChange={handleCheckboxChange10}
                        ></input>

                        <label htmlFor="kochsYes">Yes</label>
                        </div>

                        <div className="ewj_i87">
                        <input
                            type="radio"
                            id="kochsNo"
                            name="kochsNo"
                            value="No"
                            checked={kochs === "No"}
                            onChange={handleCheckboxChange10}
                        ></input>
                        <label htmlFor="kochsNo">No</label>
                        </div>
                    </div>
                    </div>
                </td>
                <td>
                    {" "}
                    {kochs == "Yes" && (
                    <input
                        type="text"
                        className="duration_90"
                        value={kochsDuration}
                        onChange={handleKochsDurationChange}
                    ></input>
                    )}
                </td>
                <td>
                    {" "}
                    {kochs == "Yes" && (
                    <input
                        type="text"
                        className="medication_90"
                        value={kochsMedication}
                        onChange={handleKochsMedicationChange}
                    ></input>
                    )}
                </td>
                </tr>

                <tr>
                <td>
                    <div className="spac_betwn_hstychronc">
                    <label className="spac_betwn_hstychronc_label">
                        Malignancy <span>:</span>
                    </label>

                    <div className="ewj_i87_head">
                        <div className="ewj_i87">
                        <input
                            type="radio"
                            id="malignancyYes"
                            name="malignancyYes"
                            value="Yes"
                            checked={malignancy === "Yes"}
                            onChange={handleCheckboxChange11}
                        ></input>

                        <label htmlFor="malignancyYes">Yes</label>
                        </div>

                        <div className="ewj_i87">
                        <input
                            type="radio"
                            id="malignancyNo"
                            name="malignancyNo"
                            value="No"
                            checked={malignancy === "No"}
                            onChange={handleCheckboxChange11}
                        ></input>
                        <label htmlFor="malignancyNo">No</label>
                        </div>
                    </div>
                    </div>
                </td>
                <td>
                    {" "}
                    {malignancy == "Yes" && (
                    <input
                        type="text"
                        className="duration_90"
                        value={malignancyDuration}
                        onChange={handleMalignancyDurationChange}
                    ></input>
                    )}
                </td>
                <td>
                    {" "}
                    {malignancy == "Yes" && (
                    <input
                        type="text"
                        className="medication_90"
                        value={malignancyMedication}
                        onChange={handleMalignancyMedicationChange}
                    ></input>
                    )}
                </td>
                </tr>
            </tbody>
            </table>
        </div>
        

        <div className="Selected-table-container">
        <table className="selected-medicine-table2 _hide_hover_table">
            <thead className="Spl_backcolr_09">
            <tr>
                <th className="HistoryOfChronicIllness">
                Personal History
                </th>
                <th className="wiejdwi8">Duration in Years</th>
                <th className="wiejdwi8">Notes</th>
            </tr>
            </thead>

            <tbody>
            <tr>
                <td>
                <div className="spac_betwn_hstychronc">
                    <label className="spac_betwn_hstychronc_label">
                    Alcohol <span>:</span>
                    </label>

                    <div className="ewj_i87_head">
                    <div className="ewj_i87">
                        <input
                        type="radio"
                        id="alcoholYes"
                        name="alcoholYes"
                        value="Yes"
                        checked={alcohol === "Yes"}
                        onChange={handleCheckboxChangeAlcohol}
                        ></input>

                        <label htmlFor="alcoholYes">Yes</label>
                    </div>

                    <div className="ewj_i87">
                        <input
                        type="radio"
                        id="alcoholNo"
                        name="alcoholNo"
                        value="No"
                        checked={alcohol === "No"}
                        onChange={handleCheckboxChangeAlcohol}
                        ></input>
                        <label htmlFor="alcoholNo">No</label>
                    </div>
                    </div>
                </div>
                </td>
                <td>
                {" "}
                {alcohol == "Yes" && (
                    <input
                    type="text"
                    className="duration_90"
                    value={alcoholDuration}
                    onChange={handleAlcoholDurationChange}
                    ></input>
                )}
                </td>
                <td>
                {" "}
                {alcohol == "Yes" && (
                    <input
                    type="text"
                    className="medication_90"
                    value={alcoholNotes}
                    onChange={handleAlcoholNotesChange}
                    ></input>
                )}
                </td>
            </tr>
            <tr>
                <td>
                <div className="spac_betwn_hstychronc">
                    <label className="spac_betwn_hstychronc_label">
                    Smoking <span>:</span>
                    </label>

                    <div className="ewj_i87_head">
                    <div className="ewj_i87">
                        <input
                        type="radio"
                        id="smokingYes"
                        name="smokingYes"
                        value="Yes"
                        checked={smoking === "Yes"}
                        onChange={handleCheckboxChangeSmoking}
                        ></input>

                        <label htmlFor="smokingYes">Yes</label>
                    </div>

                    <div className="ewj_i87">
                        <input
                        type="radio"
                        id="smokingNo"
                        name="smokingNo"
                        value="No"
                        checked={smoking === "No"}
                        onChange={handleCheckboxChangeSmoking}
                        ></input>
                        <label htmlFor="smokingNo">No</label>
                    </div>
                    </div>
                </div>
                </td>
                <td>
                {" "}
                {smoking == "Yes" && (
                    <input
                    type="text"
                    className="duration_90"
                    value={smokingDuration}
                    onChange={handleSmokingDurationChange}
                    ></input>
                )}
                </td>
                <td>
                {" "}
                {smoking == "Yes" && (
                    <input
                    type="text"
                    className="medication_90"
                    value={smokingNotes}
                    onChange={handleSmokingNotesChange}
                    ></input>
                )}
                </td>
            </tr>
            <tr>
                <td>
                <div className="spac_betwn_hstychronc">
                    <label className="spac_betwn_hstychronc_label">
                    HIV <span>:</span>
                    </label>

                    <div className="ewj_i87_head">
                    <div className="ewj_i87">
                        <input
                        type="radio"
                        id="hivYes"
                        name="hivYes"
                        value="Yes"
                        checked={hiv === "Yes"}
                        onChange={handleCheckboxChangeHIV}
                        ></input>

                        <label htmlFor="hivYes">Yes</label>
                    </div>

                    <div className="ewj_i87">
                        <input
                        type="radio"
                        id="hivNo"
                        name="hivNo"
                        value="No"
                        checked={hiv === "No"}
                        onChange={handleCheckboxChangeHIV}
                        ></input>
                        <label htmlFor="hivNo">No</label>
                    </div>
                    </div>
                </div>
                </td>
                <td>
                {" "}
                {hiv == "Yes" && (
                    <input
                    type="text"
                    className="duration_90"
                    value={hivDuration}
                    onChange={handleHIVDurationChange}
                    ></input>
                )}
                </td>
                <td>
                {" "}
                {hiv == "Yes" && (
                    <input
                    type="text"
                    className="medication_90"
                    value={hivNotes}
                    onChange={handleHIVNotesChange}
                    ></input>
                )}
                </td>
            </tr>
            <tr>
                <td>
                <div className="spac_betwn_hstychronc">
                    <label className="spac_betwn_hstychronc_label">
                    HbSAg <span>:</span>
                    </label>

                    <div className="ewj_i87_head">
                    <div className="ewj_i87">
                        <input
                        type="radio"
                        id="hbSAgYes"
                        name="hbSAgYes"
                        value="Yes"
                        checked={hbSAg === "Yes"}
                        onChange={handleCheckboxChangeHbSAg}
                        ></input>

                        <label htmlFor="hbSAgYes">Yes</label>
                    </div>

                    <div className="ewj_i87">
                        <input
                        type="radio"
                        id="hbSAgNo"
                        name="hbSAgNo"
                        value="No"
                        checked={hbSAg === "No"}
                        onChange={handleCheckboxChangeHbSAg}
                        ></input>
                        <label htmlFor="hbSAgNo">No</label>
                    </div>
                    </div>
                </div>
                </td>
                <td>
                {" "}
                {hbSAg == "Yes" && (
                    <input
                    type="text"
                    className="duration_90"
                    value={hbSAgDuration}
                    onChange={handleHbSAgDurationChange}
                    ></input>
                )}
                </td>
                <td>
                {" "}
                {hbSAg == "Yes" && (
                    <input
                    type="text"
                    className="medication_90"
                    value={hbSAgNotes}
                    onChange={handleHbSAgNotesChange}
                    ></input>
                )}
                </td>
            </tr>
            <tr>
                <td>
                <div className="spac_betwn_hstychronc">
                    <label className="spac_betwn_hstychronc_label">
                    HCV <span>:</span>
                    </label>

                    <div className="ewj_i87_head">
                    <div className="ewj_i87">
                        <input
                        type="radio"
                        id="hcvYes"
                        name="hcvYes"
                        value="Yes"
                        checked={hcv === "Yes"}
                        onChange={handleCheckboxChangeHCV}
                        ></input>

                        <label htmlFor="hcvYes">Yes</label>
                    </div>

                    <div className="ewj_i87">
                        <input
                        type="radio"
                        id="hcvNo"
                        name="hcvNo"
                        value="No"
                        checked={hcv === "No"}
                        onChange={handleCheckboxChangeHCV}
                        ></input>
                        <label htmlFor="hcvNo">No</label>
                    </div>
                    </div>
                </div>
                </td>
                <td>
                {" "}
                {hcv == "Yes" && (
                    <input
                    type="text"
                    className="duration_90"
                    value={hcvDuration}
                    onChange={handleHCVDurationChange}
                    ></input>
                )}
                </td>
                <td>
                {" "}
                {hcv == "Yes" && (
                    <input
                    type="text"
                    className="medication_90"
                    value={hcvNotes}
                    onChange={handleHCVNotesChange}
                    ></input>
                )}
                </td>
            </tr>
            </tbody>
        </table>
        </div>

        <div className="Selected-table-container">
        <table className="selected-medicine-table2 _hide_hover_table">
            <thead className="Spl_backcolr_09">
            <tr>
                <th className="HistoryOfChronicIllness">
                Medication History
                </th>
                <th className="wiejdwi8">Duration</th>
                <th className="add32_Code">
                <span onClick={addRowMedication}>
                    <AddIcon className="add32_Code" />
                </span>
                </th>
            </tr>
            </thead>

            <tbody>
            {console.log(medication,'medication')}
            {medication?.map((row, index) => (
                <tr key={index}>
                <td>
                    <input
                    type="text"
                    className="Provisional_Diagnosis medication_43"
                    value={row.medicationName}
                    onChange={(e) =>
                        handleChangeRowMedication(
                        index,
                        "medicationName",
                        e.target.value
                        )
                    }
                    />
                </td>
                <td>
                    <input
                    type="text"
                    className="Provisional_Diagnosis medication_43"
                    value={row.medicationDuration}
                    onChange={(e) =>
                        handleChangeRowMedication(
                        index,
                        "medicationDuration",
                        e.target.value
                        )
                    }
                    />
                </td>
                <td className="add32_Code">
                    <span onClick={() => removeRowMedication(index)}>
                    <RemoveIcon className="add32_Code" />
                    </span>
                </td>
                </tr>
            ))}
            </tbody>
        </table>
        </div>

        <div className="Selected-table-container">
        <table className="selected-medicine-table2 _hide_hover_table">
            <thead className="Spl_backcolr_09">
            <tr>
                <th className="HistoryOfChronicIllness">
                Family History
                </th>
                <th className="wiejdwi8">Relationship</th>
                <th className="wiejdwi8">Notes</th>
            </tr>
            </thead>

            <tbody>
            <tr>
                <td>
                <div className="spac_betwn_hstychronc">
                    <label className="spac_betwn_hstychronc_label">
                    Diabetes <span>:</span>
                    </label>

                    <div className="ewj_i87_head">
                    <div className="ewj_i87">
                        <input
                        type="radio"
                        id="diabetesFamilyYes"
                        name="diabetesFamilyYes"
                        value="Yes"
                        checked={diabetesFamily === "Yes"}
                        onChange={handleCheckboxChangeFamily}
                        ></input>

                        <label htmlFor="diabetesFamilyYes">Yes</label>
                    </div>

                    <div className="ewj_i87">
                        <input
                        type="radio"
                        id="diabetesFamilyNo"
                        name="diabetesFamilyNo"
                        value="No"
                        checked={diabetesFamily === "No"}
                        onChange={handleCheckboxChangeFamily}
                        ></input>
                        <label htmlFor="diabetesFamilyNo">No</label>
                    </div>
                    </div>
                </div>
                </td>
                <td>
                    {diabetesFamily == "Yes" && (
                    <input
                        type="text"
                        className="duration_90"
                        value={diabetesRelationship}
                        onChange={handleRelationshipChangeFamily}
                    ></input>
                    )}
                </td>
                <td>
                    {diabetesFamily == "Yes" && (
                    <input
                        type="text"
                        className="medication_90"
                        value={diabetesNotes}
                        onChange={handleNotesChangeFamily}
                    ></input>
                    )}
                </td>

            </tr>
            <tr>
                <td>
                    <div className="spac_betwn_hstychronc">
                    <label className="spac_betwn_hstychronc_label">
                        Hypertension <span>:</span>
                    </label>

                    <div className="ewj_i87_head">
                        <div className="ewj_i87">
                        <input
                            type="radio"
                            id="hyperTensionFamilyYes"
                            name="hyperTensionFamilyYes"
                            value="Yes"
                            checked={hyperTensionFamily === "Yes"}
                            onChange={handleCheckboxChangeFamily2}
                        ></input>

                        <label htmlFor="hyperTensionFamilyYes">Yes</label>
                        </div>

                        <div className="ewj_i87">
                        <input
                            type="radio"
                            id="hyperTensionFamilyNo"
                            name="hyperTensionFamilyNo"
                            value="No"
                            checked={hyperTensionFamily === "No"}
                            onChange={handleCheckboxChangeFamily2}
                        ></input>
                        <label htmlFor="hyperTensionFamilyNo">No</label>
                        </div>
                    </div>
                    </div>
                </td>
                <td>
                    {" "}
                    {hyperTensionFamily == "Yes" && (
                    <input
                        type="text"
                        className="duration_90"
                        value={hyperTensionRelationshipFamily}
                        onChange={handleHyperTensionRelationshipChange}
                    ></input>
                    )}
                </td>
                <td>
                    {" "}
                    {hyperTensionFamily == "Yes" && (
                    <input
                        type="text"
                        className="medication_90"
                        value={hyperTensionNotesFamily}
                        onChange={handleHyperTensionNotesChange}
                    ></input>
                    )}
                </td>
                </tr>
                <tr>
                <td>
                    <div className="spac_betwn_hstychronc">
                    <label className="spac_betwn_hstychronc_label">
                        Kochs <span>:</span>
                    </label>

                    <div className="ewj_i87_head">
                        <div className="ewj_i87">
                        <input
                            type="radio"
                            id="kochsFamilyYes"
                            name="kochsFamilyYes"
                            value="Yes"
                            checked={kochsFamily === "Yes"}
                            onChange={handleCheckboxChangeFamily3}
                        ></input>

                        <label htmlFor="kochsFamilyYes">Yes</label>
                        </div>

                        <div className="ewj_i87">
                        <input
                            type="radio"
                            id="kochsFamilyNo"
                            name="kochsFamilyNo"
                            value="No"
                            checked={kochsFamily === "No"}
                            onChange={handleCheckboxChangeFamily3}
                        ></input>
                        <label htmlFor="kochsFamilyNo">No</label>
                        </div>
                    </div>
                    </div>
                </td>
                <td>
                    {" "}
                    {kochsFamily == "Yes" && (
                    <input
                        type="text"
                        className="duration_90"
                        value={kochsRelationship}
                        onChange={handleKochsRelationshipChange}
                    ></input>
                    )}
                </td>
                <td>
                    {" "}
                    {kochsFamily == "Yes" && (
                    <input
                        type="text"
                        className="medication_90"
                        value={kochsNotes}
                        onChange={handleKochsNotesChange}
                    ></input>
                    )}
                </td>
                </tr>

                <tr>
                <td>
                    <div className="spac_betwn_hstychronc">
                    <label className="spac_betwn_hstychronc_label">
                        Genetic Disorder <span>:</span>
                    </label>

                    <div className="ewj_i87_head">
                        <div className="ewj_i87">
                        <input
                            type="radio"
                            id="geneticDisorderFamilyYes"
                            name="geneticDisorderFamilyYes"
                            value="Yes"
                            checked={geneticDisorderFamily === "Yes"}
                            onChange={handleCheckboxChangeFamily4}
                        ></input>

                        <label htmlFor="geneticDisorderFamilyYes">Yes</label>
                        </div>

                        <div className="ewj_i87">
                        <input
                            type="radio"
                            id="geneticDisorderFamilyNo"
                            name="geneticDisorderFamilyNo"
                            value="No"
                            checked={geneticDisorderFamily === "No"}
                            onChange={handleCheckboxChangeFamily4}
                        ></input>
                        <label htmlFor="geneticDisorderFamilyNo">No</label>
                        </div>
                    </div>
                    </div>
                </td>
                <td>
                    {" "}
                    {geneticDisorderFamily == "Yes" && (
                    <input
                        type="text"
                        className="duration_90"
                        value={geneticDisoderRelationship}
                        onChange={handleGeneticDisorderRelationshipChange}
                    ></input>
                    )}
                </td>
                <td>
                    {" "}
                    {geneticDisorderFamily == "Yes" && (
                    <input
                        type="text"
                        className="medication_90"
                        value={geneticDisoderNotes}
                        onChange={handleGeneticDisorderNotesChange}
                    ></input>
                    )}
                </td>
                </tr>
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
