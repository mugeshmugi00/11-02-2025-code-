import {
  Button,
  Checkbox,
  debounce,
  FormControlLabel,
  TextField,
} from "@mui/material";
import axios from "axios";
import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import AddIcon from "@mui/icons-material/Add";
import CheckIcon from "@mui/icons-material/Check";
import EditIcon from "@mui/icons-material/Edit";
import CancelIcon from "@mui/icons-material/Cancel";
import { useLocation } from "react-router-dom";


const OtCharges = () => {
  

  const [isConsumable, setIsConsumable] = useState(false);
  const [isConsignment, setIsConsignment] = useState(false);
  const [consumableText, setConsumableText] = useState("");
  const [consignmentText, setConsignmentText] = useState("");

  const [itemName, setItemName] = useState("");
  const [quantity, setQuantity] = useState("");
  const [consumableAmount, setConsumableAmount] = useState("");
  const [consumableData, setConsumableData] = useState([]);
  const [consignmentData, setConsignmentData] = useState([]);

  const [checkboxes, setCheckboxes] = useState([]);
  const [inventoryItems, setInventoryItems] = useState([]);
  const [searchResults, setSearchResults] = useState([]);
  const [availableQuantity, setAvaibleQuantity] = useState(0);

  const [equipmentName, setequipmentName] = useState("");
  const [quantity1, setQuantity1] = useState("");
  const [amount1, setAmount1] = useState("");

  const [otconsumable,setotconsumable] = useState([]);
  const [otconsignment,setotconsignment] = useState([]);
  const [otequipment ,setotequipment] = useState([]);
  const [Crewdata,setCrewdata] = useState([]);
    const [load,setload] = useState([]);

    const [surgeon, setSurgeon] = useState([]);
    const [assistantSurgeon, setAssistantSurgeon] = useState([]);
    const [anaesthesiologist, setAnaesthesiologist] = useState([]);
    const [scrubNurse, setScrubNurse] = useState([]);
    const [circulatingNurse, setCirculatingNurse] = useState([]);
    const mergedNurses = [...scrubNurse, ...circulatingNurse];

    const [technician, setTechnician] = useState([]);
    const [others, setOthers] = useState([]);

    const [selectedService, setSelectedService] = useState("");
    const [filteredData, setFilteredData] = useState([]);


  

  const UrlLink = useSelector((state) => state.userRecord?.UrlLink);
  const location = useLocation();
  const { params } = location.state || {};

  const [otCharges, setOtCharges] = useState([]);
  const [newCharge, setNewCharge] = useState({
    serviceName: "",
    units: "",
    perHourCost: "",
    amount: "",
    id: Date.now(),
    duration : params?.Duration,
    identify : "",
    quantity  : ""

  });

  const [otrent,setotrent] = useState(params.theatrerent);
  const [otname,setotname] = useState(params.TheatreName);
  const [selectedConsignment, setSelectedConsignment] = useState("");
  const [selectedequipment,setselectedequipment] = useState("");
  

  console.log('received params',otCharges);

  const [consignmentNames, setConsignmentNames] = useState([]);
  const [consumables, setConsumables] = useState([]);

  const [equipmentNames, setequipmentNames] = useState([]);
  const [equipments, setequipmentss] = useState([]);


useEffect(() => {
    
    const names = otconsignment.map(item => item.consignmentname);
    setConsignmentNames(names);
}, [otconsignment]);

useEffect(() => {

  const names = otequipment.map(item => item.equipmentname);
  setequipmentNames(names);
}, [otequipment]);


  useEffect(() => {
    axios.get(`${UrlLink}Masters/Consumable_details?patientid=${params?.patientId}`)
        .then((res) => {
          
          setotconsumable(res.data)
        })
        .catch((err) => console.log(err));
  }, [UrlLink]);

  useEffect(() => {
    axios.get(`${UrlLink}Masters/Consignment_details?patientid=${params?.patientId}`)
        .then((res) => {
         
          setotconsignment(res.data)
        })
        .catch((err) => console.log(err));
  }, [UrlLink]);

  useEffect(() => {
    axios.get(`${UrlLink}Masters/Equipment_details?patientid=${params?.patientId}`)
        .then((res) => {
         
          setotequipment(res.data)
        })
        .catch((err) => console.log(err));
  }, [UrlLink]);

  useEffect(() => {
    axios.get(`${UrlLink}Masters/Surgical_Team_details?patientid=${params?.patientId}`)
      
        .then((res) => {
          const data = res.data;
  
         
          
          setCrewdata(res.data);
          // setEntries({
  
          //   id : data[0].id,
          //   surgeon: data[0].surgeonId.split(", ").map(id => id.trim()),
          //   surgeonname: data[0].surgeon.split(", ").map(id => id.trim()),
          //   assistantSurgeon: data[0].assistantSurgeonId.split(", ").map(id => id.trim()),
          //   assistantSurgeonname: data[0].assistantSurgeon.split(", ").map(id => id.trim()),
          //   anaesthesiologist: data[0].anaesthesiologistId.split(", ").map(id => id.trim()),
          //   anaesthesiologistname: data[0].anaesthesiologist.split(", ").map(id => id.trim()),
          //   scrubNurse: data[0].scrubNurseId.split(", ").map(id => id.trim()),
          //   scrubNursename: data[0].scrubNurse.split(", ").map(id => id.trim()),
          //   technician: data[0].technicianId.split(", ").map(id => id.trim()),
          //   technicianname: data[0].technician.split(", ").map(id => id.trim()),
          //   circulatingNurse: data[0].circulatingNurseId.split(", ").map(id => id.trim()),
          //   circulatingNursename: data[0].circulatingNurse.split(", ").map(id => id.trim()),
          //   othersname: data[0].others.split(", ").map(id => id.trim()),
          //   others: data[0].othersId.split(", ").map(id => id.trim()),
  
          // });}
        }
        )
        .catch((err) => console.log(err));
  
  
  }, [UrlLink]);


  useEffect(() => {
    if (Crewdata && Crewdata.length > 0) {
     
      let tempSurgeon = [];
      
      let tempAssistantSurgeon = [];
      
      let tempAnaesthesiologist = [];
      
      let tempScrubNurse = [];
     
      let tempCirculatingNurse = [];
    
      let tempTechnician = [];
    
      let tempOthers = [];

      // Loop through each object in the array
      Crewdata.forEach((data) => {
        // Split values and store them in temp arrays
        
        if (data.surgeon) tempSurgeon.push(...data.surgeon.split(", ").map(name => name.trim()));

        
        if (data.assistantSurgeon) tempAssistantSurgeon.push(...data.assistantSurgeon.split(", ").map(name => name.trim()));

      
        if (data.anaesthesiologist) tempAnaesthesiologist.push(data.anaesthesiologist);

        
        if (data.scrubNurse) tempScrubNurse.push(data.scrubNurse);

        
        if (data.circulatingNurse) tempCirculatingNurse.push(data.circulatingNurse);

        
        if (data.technician) tempTechnician.push(data.technician);


        if (data.others) tempOthers.push(...data.others.split(", ").map(name => name.trim()));
      });

      // Update state
     
      setSurgeon(tempSurgeon);
     
      setAssistantSurgeon(tempAssistantSurgeon);
      
      setAnaesthesiologist(tempAnaesthesiologist);
     
      setScrubNurse(tempScrubNurse);
   
      setCirculatingNurse(tempCirculatingNurse);
      
      setTechnician(tempTechnician);
     
      setOthers(tempOthers);
    }
  }, [Crewdata]);

  useEffect(() => {
    if (!otconsumable) return; // Exit early if otconsumable is not available
  
    const createNewotConsumables = (data) => {
      return data.map((consumableData) => ({
        category: consumableData.Categoryname,
        price : consumableData.price,
        name: consumableData.Productname,
        quantity: parseInt(consumableData.Quantity),
        checkboxes: Array(parseInt(consumableData.Quantity)).fill(false),
        isEditing: false,
      }));
    };
  
    const newConsumables = createNewotConsumables(otconsumable);
    setConsumables(newConsumables);
  
    console.log(newConsumables, 'newConsumables');
    console.log(consumables, 'consumables'); 
    console.log(otconsignment,'otconsignment');
  
  }, [otconsumable]); // Dependency array ensures this runs when otconsumable changes
  
  const renderConsumablesTable = () => {
      return (
        <div className="Selected-table-container">
          <table className="selected-medicine-table2">
            <thead>
              <tr>
                <th>Category</th>
                <th>Product Name/Code</th>
                <th>Quantity</th>
              </tr>
            </thead>
            <tbody>
              {consumables.map((consumable, index) => (
                <tr key={index}>
                  <td>{consumable.category}</td>
                  <td>{consumable.name}</td>
                  <td>
                    <div
                      style={{
                        display: "flex",
                        alignItems: "center",
                        marginRight: "5px",
                      }}
                    >
                      {consumable.isEditing ? (
                        <input
                          type="number"
                          value={consumable.quantity}
                          onChange={(e) => handleQuantityChange(e, index)}
                        />
                      ) : (
                        consumable.quantity
                      )}
  
                      <div style={{ display: "flex", flex: "warp" }}>
                        {Array.from(
                          { length: consumable.quantity },
                          (_, checkboxIndex) => (
                            <label key={checkboxIndex}>
                              <Checkbox
                                type="checkbox"
                                // name={`checkbox-${index}-${i}`}
                                checked={
                                  consumable.checkboxes[checkboxIndex] || false
                                }
                                onChange={(e) =>
                                  handleCheckboxChange(e, index, checkboxIndex)
                                }
                              />
                            </label>
                          )
                        )}
                      </div>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
    };


  const handleServiceChange = (event) => {
    const { name, value } = event.target;
    const selectedValue = value;
    setSelectedService(selectedValue);

    setNewCharge((prevState) => ({
      ...prevState, 
      [name]: value,
    }));

    // Filter data based on selection
    switch (selectedValue) {
      case "PRIMARY SURGEON":
        setFilteredData(surgeon);
        break;
      case "ASSISTING SURGEON":
        setFilteredData(assistantSurgeon);
        break;
      case "ANESTHETIST":
        setFilteredData(anaesthesiologist);
        break;
      case 'OPERATION THEATER':
        
        setNewCharge((prevState) => ({
          ...prevState, 
          units : otname,
          perHourCost : otrent,         
        }));
        break;
      case 'NURSE':
          setFilteredData(mergedNurses);
          break;
      case 'TECHNICIAN':
            setFilteredData(technician);
            break;
      

      case 'CONSIGNMENT' :
 
        setFilteredData(consignmentNames);
        break;

      case 'EQUIPMENT' :
         
          setFilteredData(equipmentNames);
          
          break;
        


      default:
        setFilteredData([]);   
        break;
    }
  };


 

  // Fetching the inventory items from the API
  useEffect(() => {
    axios
      .get(`${UrlLink}Masters/Inventory_Master_Detials_link`)
      .then((res) => {
        if (Array.isArray(res.data)) {
          setInventoryItems(res.data);
        } else {
          console.error("API response is not an array", res.data);
        }
      })
      .catch((err) => {
        console.error("Error fetching inventory data:", err);
      });
  }, [UrlLink]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    console.log(value,name);

   

      if(name === "units" && selectedService !==  'OPERATION THEATER' && selectedService !==  'CONSIGNMENT' && selectedService !== 'EQUIPMENT'){
  
        if (!isNaN(value) && value.trim() !== ""){

          console.log('number');

          setNewCharge((prevState) => ({
            ...prevState, 
            identify: 'number',
            [name]: value,
          }));
            
        }

        else{
          console.log('string');
          setNewCharge((prevState) => ({
            ...prevState, 
            identify : 'string',
            [name]: value,
          }));

        }
      }

      else if (name === "units" && selectedService ===  'CONSIGNMENT') {

       
        const selectedName = value;
        console.log(selectedName);
        console.log(value);
        setSelectedConsignment(selectedName);

        // Find corresponding quantity
        const selectedItem = otconsignment.find(item => item.consignmentname === selectedName);
        console.log(selectedItem);
        setNewCharge((prevState) => ({
          ...prevState,
          units : value,
          quantity : selectedItem.quantity,
          amount: value * selectedItem.quantity
          
        }));
      }

      else if (name === "units" && selectedService ===  'EQUIPMENT') {

       
        const selectedName = value;
        console.log(selectedName);
        console.log(value);
        setselectedequipment(selectedName);

        // Find corresponding quantity
        const selectedItem = otequipment.find(item => item.equipmentname === selectedName);
        console.log(selectedItem);
        setNewCharge((prevState) => ({
          ...prevState,
          units : value,
          quantity : selectedItem.quantity,
          amount: value * selectedItem.quantity
          
        }));
      }

      else if (name === "units" && selectedService ===  'OPERATION THEATER') {

        console.log('premkumar',selectedService);
        setNewCharge((prevState) => ({
          ...prevState,
          units : value,
          perHourCost : otrent,
          amount: otrent * prevState.duration
        }));
      }

      else if (name === "perHourCost" &&  selectedService !==  'OPERATION THEATER' && selectedService !== 'CONSIGNMENT' && selectedService !== 'EQUIPMENT') {

        console.log('vathi',selectedService);
        setNewCharge((prevState) => ({
          ...prevState,
          [name]: value,
          amount: value * (prevState.identify === 'string' ? prevState.duration : prevState.units),
        }));
      }

      else if (name === "quantity" && selectedService ===  'OPERATION THEATER'){

        setNewCharge((prevState) => ({
          ...prevState,
          [name]: value,
          amount: value * prevState.perHourCost,
        }));

      }

      else if (name === "perHourCost"  && selectedService === 'CONSIGNMENT'){

        setNewCharge((prevState) => ({
          ...prevState, 
          [name]: value,
          amount : prevState.quantity * value,
        }));

      }

      else if (name === "perHourCost"  && selectedService === 'EQUIPMENT'){

        console.log('EQUIPMENTEQUIPMENT');

        setNewCharge((prevState) => ({
          ...prevState, 
          [name]: value,
          amount : prevState.quantity * value,
        }));

      }

      else{

        
        setNewCharge((prevState) => ({
          ...prevState, 
          [name]: value,
        }));

      }

  };

  const handleAddRow = () => {

    console.log(newCharge,'Received Params');
    setOtCharges((prevState) => [
      ...prevState,
      {
        ...newCharge,
        isConsumable,
        isConsignment,
        consumableText,
        consignmentText,
        itemName,
        consumableAmount,
      },
    ]);

    setNewCharge({
      serviceName: selectedService,
      units: "",
      perHourCost: "",
      amount: "",
      id: Date.now(),
      isEditing: false,
      duration : params?.Duration,
      identify : "",
      quantity  : "",

    });
    setIsConsumable(false);
    setIsConsignment(false);
    setConsumableText("");
    setConsignmentText("");
    setItemName("");
    setQuantity("");
    setConsumableAmount("");
  };

  const handleAddConsumable = () => {
    if (itemName && quantity && consumableAmount) {
      setConsumableData((prevData) => [
        ...prevData,
        { itemName, quantity, consumableAmount },
      ]);
      setItemName("");
      setQuantity("");
      setConsumableAmount("");
      setAvaibleQuantity(0);
    }
  };

  const handleAddConsignment = () => {
    if (equipmentName && quantity1 && amount1) {
      setConsignmentData((prevData) => [
        ...prevData,
        { equipmentName, quantity1, amount1 },
      ]);
      setequipmentName("");
      setQuantity1("");
      setAmount1("");
    }
  };

  const handleQuantityChange = (e) => {
    const newQuantity = parseInt(e.target.value) || 0;
    setQuantity(newQuantity);
    setCheckboxes(new Array(newQuantity).fill(false));
  };

  const handleProductSelect = (product) => {
    setItemName(product);
    setAvaibleQuantity(product);
  };

  const handleEditCharge = (rowId) => {
    setOtCharges((prevState) =>
      prevState.map((charge) =>
        charge.id === rowId ? { ...charge, isEditing: true } : charge
      )
    );
  };

  const handleSaveEdit = (index) => {
    setOtCharges((prevState) =>
      prevState.map((charge, i) =>
        i === index ? { ...charge, isEditing: false } : charge
      )
    );
  };

  const handleCancelEdit = (index) => {
    setOtCharges((prevState) =>
      prevState.map((charge, i) =>
        i === index ? { ...charge, isEditing: false } : charge
      )
    );
  };

  const handleEditConsumable = (index) => {
    const updatedData = [...consumableData];
    updatedData[index].isEditing = true;
    setConsumableData(updatedData);
  };

  const handleSaveConsumable = (index) => {
    const updatedData = [...consumableData];
    updatedData[index].isEditing = false;
    setConsumableData(updatedData);
  };

  const handleCancelConsumable = (index) => {
    const updatedData = [...consumableData];
    updatedData[index].isEditing = false;
    setConsumableData(updatedData);
  };

  const handleEditConsignment = (index) => {
    const updatedData = [...consignmentData];
    updatedData[index].isEditing = true;
    setConsignmentData(updatedData);
  };

  const handleSaveConsignment = (index) => {
    const updatedData = [...consignmentData];
    updatedData[index].isEditing = false;
    setConsignmentData(updatedData);
  };

  const handleCancelConsignment = (index) => {
    const updatedData = [...consignmentData];
    updatedData[index].isEditing = false;
    setConsignmentData(updatedData);
  };

  


  const handleconSubmit = async () => {

    console.log(consumables,'consumables');

    const updatedConsumables = consumables.map((item) => ({
      ...item,
      uncheckedCount: item.checkboxes.filter((checked) => !checked).length,
    }));
    
    console.log(updatedConsumables);

    // updatedConsumables.forEach((item) => {

    //   console.log(item.name);
    //   setNewCharge((prev) => ({
    //     ...prev, // Preserve the previous state
    //     serviceName: "Consumables", // Fixed value for serviceName
    //     units: item.name, // Map name of the product
    //     perHourCost: "", // Keep this empty or assign a default value
    //     amount: (parseFloat(item.price) * item.uncheckedCount).toFixed(2), // Calculate amount
    //     id: Date.now(), // Assign unique ID
    //     duration: params?.Duration, // Keep duration from params
    //     identify: item.category, // Map category to identify
    //   }));

    //   setOtCharges((prevState) => [
    //     ...prevState,
    //     {
    //       ...newCharge,
    //       isConsumable,
    //       isConsignment,
    //       consumableText,
    //       consignmentText,
    //       itemName,
    //       quantity,
    //       consumableAmount,
    //     },
    //   ]);

    //   setNewCharge({
    //     serviceName: selectedService,
    //     units: "",
    //     perHourCost: "",
    //     amount: "",
    //     id: Date.now(),
    //     isEditing: false,
    //     duration : params?.Duration,
    //     identify : ""
    //   });
    //   setIsConsumable(false);
    //   setIsConsignment(false);
    //   setConsumableText("");
    //   setConsignmentText("");
    //   setItemName("");
    //   setQuantity("");
    //   setConsumableAmount("");
    // });
    
    updatedConsumables.forEach((item) => {
      // Construct the new charge directly
      const newCharge = {
        serviceName: "Consumables", // Fixed value for serviceName
        units: item.name, // Map name of the product
        perHourCost: "", // Keep this empty or assign a default value
        amount: (parseFloat(item.price) * item.uncheckedCount).toFixed(2), // Calculate amount
        id: Date.now(), // Assign unique ID
        duration: params?.Duration, // Keep duration from params
        identify: item.category, // Map category to identify
        isConsumable,
        isConsignment,
        consumableText,
        consignmentText,
        itemName,
        quantity,
        consumableAmount,
      };
    
      // Update the charges state
      setOtCharges((prevState) => [...prevState, newCharge]);
    
      // Reset values after adding charge
      setIsConsumable(false);
      setIsConsignment(false);
      setConsumableText("");
      setConsignmentText("");
      setItemName("");
      setQuantity("");
      setConsumableAmount("");
      setConsumables([]);
    });
    
  };

  const handlebillSubmit = async () => {
    const data = {
      ...otCharges,
      'RegistrationId' : params?.RegistrationId,
    };

    console.log(data,'data');
    axios.post(`${UrlLink}Masters/OT_Billing_details`, data)
    .then((res) => {
  
      const response = res.data;
                  // const messageType = Object.keys(response)[0];
                  // const messageContent = Object.values(response)[0];
                  // console.log(messageType);
                  // console.log(messageContent);
                  // dispatchvalue({
                  //     type: 'toast',
                  //     value: { message: messageContent, type: messageType },
                  // });
     
        setload((prev)=>!prev);
    })
    .catch((err) => console.log(err));

    
  };
  
  // const handleCheckboxChange = (e, rowIndex, checkboxIndex) => {
  //   const updatedData = [...consumableData];
  //   const isChecked = e.target.checked;
  //   if (!updatedData[rowIndex].checkboxes) {
  //     updatedData[rowIndex].checkboxes = [];
  //   }

  //   updatedData[rowIndex].checkboxes[checkboxIndex] = isChecked;

  //   setConsumableData(updatedData);
  // };

  console.log(otCharges,'otcharges');

  const handleCheckboxChange = (e, rowIndex, checkboxIndex) => {
    const checked = e.target.checked;
    setConsumables((prev) =>
      prev.map((item, i) =>
        i === rowIndex
          ? {
              ...item,
              checkboxes: item.checkboxes.map((cb, j) =>
                j === checkboxIndex ? checked : cb
              ),
            }
          : item
      )
    );
  };
  

  return (
    <div className="Main_container_app">
      <h4>OT Charges</h4>

      <div className="RegisFormcon_1">
        <div className="RegisForm_1">
          <label>
            Service Name<span>:</span>
          </label>
          <select
            name="serviceName"
            value={selectedService}
            onChange={handleServiceChange}
            required
          >
            <option value="">Select Service</option>
            <option value="PRIMARY SURGEON">PRIMARY SURGEON FEE</option>
            <option value="ASSISTING SURGEON">ASSISTING SURGEN FEE</option>
            <option value="ANESTHETIST">ANESTHETIST FEE</option>
            <option value="PHYSICIAN">PHYSICIAN FEE</option>
            <option value="CONSUMABLE">CONSUMABLE FEE</option>
            <option value="CONSIGNMENT">CONSIGNMENT FEE</option>
            <option value="CONSULTANT">CONSULTANT FEE</option>
            <option value="NURSE">NURSE FEE</option>
            <option value="TECHNICIAN">TECHNICIAN FEE</option>
            <option value="OPERATION THEATER">OPERATION THEATER CHARGES</option>
            <option value="EQUIPMENT">EQUIPMENT CHARGES</option>
            <option value="BLOOD">BLOOD</option>
            <option value="OXYGEN/OTHER GAS">OXYGEN/OTHER GAS</option>
            <option value="SURGICAL APPLIANCE">
              SURGICAL APPLIANCE CHARGE
            </option>
          </select>
        </div>

        <div className="RegisForm_1">
          <label>
            Name<span>:</span>
          </label>
          <input
            type="text"
            name="units"
            value={newCharge.units}
            onChange={handleInputChange}
            list='Surgeonlist'
            required

          />

          <datalist id="Surgeonlist">
              {Array.isArray(filteredData) &&
                  filteredData.map((f, i) => (
                      <option key={i} value={f}></option>
                  ))}
          </datalist>
        </div>

        <div className="RegisForm_1">
          <label>
            Per Hour/Unit Cost<span>:</span>
          </label>
          <input
            type="number"
            name="perHourCost"
            value={newCharge.perHourCost}
            onChange={handleInputChange}
            required
          />
        </div>

        <div className="RegisForm_1">
          <label>
            Quantity/Duration<span>:</span>
          </label>
          <input
            type="number"
            name="quantity"
            value={newCharge.quantity}
            onChange={handleInputChange}
            required
          />
        </div>

       

        <div className="RegisForm_1">
          <label>
            Amount<span>:</span>
          </label>
          <input
            type="number"
            name="amount"
            value={newCharge.amount}
            onChange={handleInputChange}
           // readOnly
          />
        </div>
      </div>

      <div className="Main_container_Btn">
        <Button onClick={handleAddRow}>
          <AddIcon />
        </Button>
      </div>

      <div className="Selected-table-container">
        <table className="selected-medicine-table2">
          <thead>
            <tr>
              <th>S.No</th>
              <th>Service Name</th>
              <th>Name</th>
              <th>Per Hour/Unit Cost</th>
              <th>Duration/Quantity</th>
              <th>Amount</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {otCharges.map((charge, index) => (
              <tr key={charge.id}>
                <td>{index + 1}</td>
                <td>
                  {charge.isEditing ? (
                    <input
                      type="text"
                      name="serviceName"
                      value={charge.serviceName}
                      onChange={(e) => {
                        const updatedCharges = [...otCharges];
                        updatedCharges[index].serviceName = e.target.value;
                        setOtCharges(updatedCharges);
                      }}
                    />
                  ) : (
                    charge.serviceName
                  )}
                </td>
                <td>
                  {charge.isEditing ? (
                    <input
                      type="number"
                      name="units"
                      value={charge.units}
                      onChange={(e) => {
                        const updatedCharges = [...otCharges];
                        updatedCharges[index].units = e.target.value;
                        updatedCharges[index].amount =
                          updatedCharges[index].units *
                          updatedCharges[index].perHourCost;
                        setOtCharges(updatedCharges);
                      }}
                    />
                  ) : (
                    charge.units
                  )}
                </td>
                <td>
                  {charge.isEditing ? (
                    <input
                      type="number"
                      name="perHourCost"
                      value={charge.perHourCost}
                      onChange={(e) => {
                        const updatedCharges = [...otCharges];
                        updatedCharges[index].perHourCost = e.target.value;
                        updatedCharges[index].amount =
                          updatedCharges[index].units *
                          updatedCharges[index].perHourCost;
                        setOtCharges(updatedCharges);
                      }}
                    />
                  ) : (
                    charge.perHourCost ? charge.perHourCost : '-'
                  )}
                </td>
                <td>

                {charge.isEditing ? (
                    <input
                      type="number"
                      name="quantity"
                      value={charge.quantity}
                      onChange={(e) => {
                        const updatedCharges = [...otCharges];
                        updatedCharges[index].quantity = e.target.value;
                        updatedCharges[index].amount =
                          updatedCharges[index].units *
                          updatedCharges[index].perHourCost;
                        setOtCharges(updatedCharges);
                      }}
                    />
                  ) : (
                    charge.quantity ?  charge.quantity : '-'
                  )}

                </td>
                <td>
                  {charge.isEditing ? (
                    <input type="number" value={charge.amount} readOnly />
                  ) : (
                    charge.amount
                  )}
                </td>
                <td>
                  {charge.isEditing ? (
                    <>
                      <Button onClick={() => handleSaveEdit(index)}>
                        <CheckIcon />
                      </Button>
                      <Button onClick={() => handleCancelEdit(index)}>
                        <CancelIcon />
                      </Button>
                    </>
                  ) : (
                    <Button onClick={() => handleEditCharge(charge.id)}>
                      <EditIcon />
                    </Button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

     
   

{consumables.length > 0 && (
  <>
    {renderConsumablesTable()}
    <div className="Main_container_Btn">
      <button onClick={handleconSubmit}>Save</button>
    </div>
  </>
)}     

<div className="Main_container_Btn">
      <button onClick={handlebillSubmit}>Proceed Billing</button>
    </div>
        
      </div>  
  );
};

export default OtCharges;
