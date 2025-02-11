import React, { useState, useEffect} from "react";
import { useDispatch, useSelector } from "react-redux";
import ReactGrid from "../../OtherComponent/ReactGrid/ReactGrid";
import Button from "@mui/material/Button";
import EditIcon from "@mui/icons-material/Edit";
import axios from "axios";
import ToastAlert from "../../OtherComponent/ToastContainer/ToastAlert";
import PhotoCameraBackIcon from "@mui/icons-material/PhotoCameraBack";




const RadiologyMaster = () => {

  const dispatchvalue = useDispatch();
  const UrlLink = useSelector((state) => state.userRecord?.UrlLink);
  const userRecord = useSelector((state) => state.userRecord?.UserData);
  const UserData = useSelector((state) => state.userRecord?.UserData);
  const toast = useSelector(state => state.userRecord?.toast);
  const Usersessionid = useSelector((state) => state.userRecord?.Usersessionid);
  const [isEditing, setIsEditing] = useState(true);
  

  // ----------------------RadiologyName--------
  const [RadiologyName, setRadiologyName] = useState({
    RadiologyId: "",
    RadiologyName: "",
    Location: "",
  });
  // console.log(RadiologyName)
  const [LocationData, setLocationData] = useState([]);
  const [IsRadiologyGet, setIsRadiologyGet] = useState(false);
  const [RadiologyNames, setRadiologyNames] = useState([]);
  useEffect(() => {
    axios.get(`${UrlLink}Masters/Location_Detials_link`, {
      headers: {
        'Apikey': UserData.api_key,
        'Apipassword': UserData.api_password,
        'Sessionid': Usersessionid.session_id
      }
    })
      .then((res) => {
        const ress = res.data
        setLocationData(ress)
      })
      .catch((err) => {
        console.log(err);
      })
  }, [UrlLink,UserData])

  const handleRadiologyChange = (e) => {
    const { name, value } = e.target;

    if (name === 'Location') {
      // Update Location and reset RadiologyName when location changes
      setRadiologyName((prev) => ({
        ...prev,
        [name]: value,
        RadiologyName: '', // Reset RadiologyName on location change
      }));
    } else if (name === "RadiologyName") {
      // Update the relevant field, applying toUpperCase and trim
      setRadiologyName((prev) => ({
        ...prev,
        [name]: value?.toUpperCase()?.trim(),
      }));
    }
  };


  const handleeditRadiologyStatus = (params) => {

    const data = {
      RadiologyId: params.id,
      Statusedit: true,

    }
    axios.post(`${UrlLink}Masters/Radiology_Names_link`, data, {
      headers: {
        'Apikey': UserData.api_key,
        'Apipassword': UserData.api_password,
        'Sessionid': Usersessionid.session_id
      }
    })
      .then((res) => {
        const resres = res.data
        let typp = Object.keys(resres)[0]
        let mess = Object.values(resres)[0]
        const tdata = {
          message: mess,
          type: typp,
        }
        dispatchvalue({ type: 'toast', value: tdata });
        setIsRadiologyGet(prev => !prev)
      })
      .catch((err) => {
        console.log(err);
      })
  };
  const RadiologyColumns = [
    {
      key: "id",
      name: "Radiology Id",
      frozen: true,
    },
    {
      key: "created_by",
      name: "Created By",
      frozen: true,
    },
    {
      key: "RadiologyName",
      name: "Radiology Department",
    },
    {
      key: "Location_Name",
      name: "Location Name",
    },
    {
      key: "Status",
      name: "Status",
      renderCell: (params) => (
        <Button
          className="cell_btn"
          onClick={() => handleeditRadiologyStatus(params.row)}
        >
          {params.row.Status}
        </Button>
      ),
    },
    {
      key: "EditAction",
      name: "Edit",
      renderCell: (params) => (
        <Button
          className="cell_btn"
          onClick={() => handleeditRadiology(params.row)}
        >
          <EditIcon className="check_box_clrr_cancell" />
        </Button>
      ),
    },
  ];


  const handleRadiologySubmit = () => {

    if (RadiologyName.RadiologyName) {
      const data = {
        ...RadiologyName,
        RadiologyName: RadiologyName.RadiologyName || "",
        Location: RadiologyName.Location || "",
        // AmountArray: drainsData2 || [],
        created_by: userRecord?.username || "",
      };
      console.log(" twodata", data)
      axios
        .post(`${UrlLink}Masters/Radiology_Names_link`, data, {
          headers: {
            'Apikey': UserData.api_key,
            'Apipassword': UserData.api_password,
            'Sessionid': Usersessionid.session_id
          }
        })
        .then((res) => {
          const [typp, mess] = Object.entries(res.data)[0];
          dispatchvalue({ type: "toast", value: { message: mess, type: typp } });
          setIsRadiologyGet((prev) => !prev);
          setRadiologyName({
            RadiologyId: "",
            RadiologyName: "",
            Location: "",
          });
          // setDrainsData2([{ id: 1, From: "0", To: "", Amount: "" }]);
        })
        .catch((err) => {
          console.log(err);
        });
    } else {
      dispatchvalue({ type: "toast", value: { message: "Please provide the Radiology Name.", type: "warn" } });
    }
  };
  const handleeditRadiology = (params) => {
    console.log("23456", params);
    const { id, ...rest } = params;
    setRadiologyName({
      RadiologyId: id,
      Location: rest?.Location_Id,
      ...rest,
    });

  };

  useEffect(() => {
    axios
      .get(`${UrlLink}Masters/Radiology_Names_link`, {
        headers: {
          'Apikey': UserData.api_key,
          'Apipassword': UserData.api_password,
          'Sessionid': Usersessionid.session_id
        }
      })
      .then((response) => {
        setRadiologyNames(response.data);
        console.log("response235999", response.data);
      })
      .catch((err) => {
        console.log(err);
      });
  }, [IsRadiologyGet, UrlLink]);

  // ----------testname--------
  const [TestName, setTestName] = useState({
    TestNameId: "",
    RadiologyId: "",
    RadiologyName: "",
    TestName: "",
    Amount: "",
    TestCode: "",
    Prev_Amount: "",
    Location: "",
    BookingFees: "",
    Prev_BookingFees: "",
    Status: "Active",
  });

  const [TestNames, setTestNames] = useState([]);
  const [IsTestNameGet, setIsTestNameGet] = useState(false);
  



  const handleeditTestNameLast = (params) => {
    console.log("Params", params);
    setIsEditing(false); // Set editing state to false

    const { id, Curr_Amount, TestCode, Prev_Amount, Status, Prev_BookingFees, Curr_BookingFees, ...rest } = params; // Destructure params

    // Check if Sub_test_data is empty or not present
    if (!params.Sub_test_data || params.Sub_test_data.length === 0) {
      setTestName((prev) => ({
        ...prev,
        TestNameId: id,
        Prev_Amount: Prev_Amount || 0.0,
        Prev_BookingFees: Prev_BookingFees || 0.0,
        Amount: Curr_Amount || 0.0, // Set Curr_Amount correctly here
        TestCode: TestCode,
        BookingFees: Curr_BookingFees || 0.0, // Set Curr_BookingFees correctly here
        Location: rest.locationid,
        ...rest,
      }));
    } else {
// Set joy state to true to show the grid
    
      setTestName((prev) => ({
        ...prev,
        TestNameId: id,
        TestCode: TestCode,
        Status: Status,
        Location: rest.locationid,
        ...rest,
      }));

     
    }
  };



  const handleTestNameChange = (e) => {
    const { name, value } = e.target;
    if (name === "Location") {
      setTestName((prev) => ({
        ...prev,
        [name]: value,
        RadiologyName: '',
        TestName: "",
        Amount: "",
        BookingFees: "",
        Prev_BookingFees: ""
        // Reset RadiologyName on location change
      }));
    }
    else if (name === "RadiologyName") {
      // Clear other fields when RadiologyName changes
      setTestName((prevState) => ({
        ...prevState,
        RadiologyName: value?.toUpperCase()?.trim(),
        TestName: "",
        BookingFees: "",
        Amount: "",
        Prev_BookingFees: ""
      }));
    } else if (name === "TestName") {
      // Clear SubTestName and reset Types when TestName changes
      setTestName((prevState) => ({
        ...prevState,
        TestName: value?.toUpperCase()?.trim(),
        Prev_BookingFees: ""

      }));
    } else {
      // Update other fields
      setTestName((prevState) => ({
        ...prevState,
        [name]: value?.toUpperCase()?.trim(),
      }));
    }
  };






  const handleTestNameSubmit = () => {
    // Check if all required fields for TestName are filled
    if (
      TestName.RadiologyName !== "" &&
      TestName.TestName !== "" 
      // TestName.Types !== ""
    ) {
      const RadId = RadiologyNames.find(
        (p) => p.RadiologyName === TestName.RadiologyName
      );

      const data = {
        TestNameId: TestName.TestNameId,
        RadiologyName: RadId.id,
        TestName: TestName.TestName,
        Amount: TestName.Amount,
        created_by: userRecord?.username || "",
        location: userRecord?.location || "",
        TestCode: TestName.TestCode,
        Prev_BookingFees: TestName.Prev_BookingFees,
        Prev_Amount: TestName.Prev_Amount,
        BookingFees: TestName.BookingFees,
        Status: "Active",
      };

      // Logging data for debugging
      console.log("senddata123", data);

      // Create a new FormData object
      const formData = new FormData();

      // Append the data fields to FormData
      Object.keys(data).forEach((key) => {
        formData.append(key, data[key]);
      });

      // Append the file from ChooseFile if it exists
      if (ChooseFile.ChooseFileOne) {
        console.log('ChooseFile', ChooseFile.ChooseFileOne);
        formData.append('ChooseFile', ChooseFile.ChooseFileOne);
      }

      axios
        .post(`${UrlLink}Masters/Radiology_details_link`, formData, {
          headers: {
            'Apikey': UserData.api_key,
            'Apipassword': UserData.api_password,
            'Sessionid': Usersessionid.session_id,
            'Content-Type': 'multipart/form-data', // Add this line
          },
        })
        .then((res) => {
          const resData = res.data;
          const type = Object.keys(resData)[0];
          const message = Object.values(resData)[0];
          const tdata = {
            message: message,
            type: type,
          };
          dispatchvalue({ type: "toast", value: tdata });
          setIsTestNameGet((prev) => !prev);
          setTestName({
            TestNameId: "",
            RadiologyId: "",
            RadiologyName: "",
            TestName: "",
            Amount: "",
            SubTestName: "",
            TestCode: "",
            Prev_Amount: "",
            BookingFees: "",
            Location: "",
            Prev_BookingFees: "",
            Status: "Active",
          });
          setIsEditing(true);
          setChooseFile({ ChooseFileOne: null });
        })
        .catch((err) => {
          console.log(err);
        });
    } else {
      const tdata = {
        message: "Please provide Radiology Name, Test Name.",
        type: "warn",
      };
      dispatchvalue({ type: "toast", value: tdata });
    }
  };

 



  const formatLabel = (label) => {
    if (/[a-z]/.test(label) && /[A-Z]/.test(label) && !/\d/.test(label)) {
      return label
        .replace(/([a-z])([A-Z])/g, "$1 $2")
        .replace(/^./, (str) => str.toUpperCase());
    } else {
      return label;
    }
  };

  useEffect(() => {
    axios
      .get(`${UrlLink}Masters/Radiology_details_link`, {
        headers: {
          'Apikey': UserData.api_key,
          'Apipassword': UserData.api_password,
          'Sessionid': Usersessionid.session_id
        }
      })
      .then((res) => {
        const ress = res.data;
        console.log("testname", ress);
        setTestNames(ress);
      })
      .catch((err) => {
        console.log(err);
      });
  }, [IsTestNameGet, UrlLink]);
  const handleeditTestNameStatus = (params) => {
    console.log("paramsteststatus", params);
  
    // Create a FormData object to handle the form data and file
    const formData = new FormData();
  
    // Append all necessary fields to FormData
    formData.append('TestCode', params.TestCode);
    formData.append('TestName', params.TestName);
    formData.append('RadiologyName', params.RadiologyId);
    formData.append('BookingFees', params.Curr_BookingFees || ''); // Add a default value if null
    formData.append('Prev_Amount', params.Prev_Amount || ''); // Add a default value if null
    formData.append('Prev_BookingFees', params.Prev_BookingFees || ''); // Add a default value if null
    formData.append('Status', params.Status === 'Active' ? 'InActive' : 'Active');
  
    // Only append the file if it's available
    if (params.ChooseFile) {
      formData.append('ChooseFile', params.ChooseFile);
    }
  
    // Make the Axios POST request
    axios
      .post(`${UrlLink}Masters/Radiology_details_link`, formData, {
        headers: {
          'Apikey': UserData.api_key,
          'Apipassword': UserData.api_password,
          'Sessionid': Usersessionid.session_id,
          'Content-Type': 'multipart/form-data', // Required for form data
        },
      })
      .then((res) => {
        const resres = res.data;
        let typp = Object.keys(resres)[0];
        let mess = Object.values(resres)[0];
        const tdata = {
          message: mess,
          type: typp,
        };
        dispatchvalue({ type: 'toast', value: tdata });
        setIsTestNameGet((prev) => !prev);
      })
      .catch((err) => {
        console.log(err);
      });
  };
  
 
  const TestNameColumns = [
    {
      key: "id",
      name: "S.No",
      frozen: true,
    },
    {
      key: "created_by",
      name: "Created By",
      frozen: true,
    },
    {
      key: "RadiologyName",
      name: "Radiology Department",
      frozen: true,
      width:180,
    },
    {
      key: "TestCode",
      name: "Test Code",
      frozen: true,
    },
    {
      key: "TestName",
      name: "Test Name",
      width:180,
    },
    {
      key: "BookingFees",
      name: "Booking Fees",
      children: [
        {
          key: "Prev_BookingFees",
          name: "Prev Booking Fees",
          width:200,
          renderCell: (params) =>
            params.row.Types === "Yes" ? <>-</> : <>{params.row.Prev_BookingFees}</>,
        },
        {
          key: "Curr_BookingFees",
          name: "Curr Booking Fees",
          width:200,
          renderCell: (params) =>
            params.row.Types === "Yes" ? <>-</> : <>{params.row.Curr_BookingFees}</>,
        },
      ],
    },
    {
      key: "Amount",
      name: "Amount",
      children: [
        {
          key: "Prev_Amount",
          name: "Prev Amount",
          width:180,
          renderCell: (params) =>
            params.row.Types === "Yes" ? <>-</> : <>{params.row.Prev_Amount}</>,
        },
        {
          key: "Curr_Amount",
          name: "Curr Amount",
          width:180,
          renderCell: (params) =>
            params.row.Types === "Yes" ? <>-</> : <>{params.row.Curr_Amount}</>,
        },
      ],
    },
  
  
      {
      key: "Status",
      name: "Status",
      renderCell: (params) => (
        <Button
          className="cell_btn"
          onClick={() => handleeditTestNameStatus(params.row)}
        >
          {params.row.Status}
        </Button>
      ),
    },
    {
      key: "Action",
      name: "Action",
      renderCell: (params) => (
        <>
          <Button
            className="cell_btn"
            onClick={() => handleeditTestNameLast(params.row)}
          >
            <EditIcon className="check_box_clrr_cancell" />
          </Button>
        </>
      ),
    },
  ];



  const [ChooseFile, setChooseFile] = useState({
    ChooseFileOne: null,
  });
 








  const handleinpchangeDocumentsForm = (e) => {
    const { name, files } = e.target;

    if (files && files.length > 0) {
      let formattedValue = files[0];

      // Update the allowed types to include Word documents
      const allowedTypes = [
        "application/pdf",
        "image/jpeg",
        "image/png",
        "application/msword", // For .doc files
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document" // For .docx files
      ];
      const maxSize = 5 * 1024 * 1024; // Max size of 5MB

      if (!allowedTypes.includes(formattedValue.type) || formattedValue.type === "") {
        const tdata = {
          message: "Invalid file type. Please upload a PDF, JPEG, PNG, DOC, or DOCX file.",
          type: "warn",
        };
        dispatchvalue({ type: "toast", value: tdata });
      } else if (formattedValue.size > maxSize) {
        const tdata = {
          message: "File size exceeds the limit of 5MB.",
          type: "warn",
        };
        dispatchvalue({ type: "toast", value: tdata });
      } else {
        const reader = new FileReader();
        reader.onload = () => {
          setChooseFile((prev) => ({
            ...prev,
            [name]: reader.result,
          }));
        };
        reader.readAsDataURL(formattedValue);
      }
    } else {
      const tdata = {
        message: "No file selected. Please choose a file to upload.",
        type: "warn",
      };
      dispatchvalue({ type: "toast", value: tdata });
    }
  };






  return (
    <>
      <div className="Main_container_app">
        <div className="common_center_tag">
          <span>Radiology</span>
        </div>
        <div className="RegisFormcon_1">
          <div className="RegisForm_1">
            <label> Location <span>:</span> </label>

            <select
              name='Location'
              required
              disabled={Boolean(RadiologyName.RadiologyId)}
              value={RadiologyName.Location}
              onChange={handleRadiologyChange}
            >
              <option value=''>Select</option>
              {
                LocationData.map((p) => (
                  <option key={p.id} value={p.id}>{p.locationName}</option>
                ))
              }
            </select>
          </div>
          <div className="RegisForm_1">
            <label>
              Radiology Department <span>:</span>
            </label>
            <input
              type="text"
              name="RadiologyName"
              required
              value={RadiologyName.RadiologyName}
              autoComplete="off"
              onChange={handleRadiologyChange}
            />
          </div>


        </div>
        <div className="Main_container_Btn">
          <button onClick={handleRadiologySubmit}>
            {RadiologyName.RadiologyId ? "Update" : "Save"}
          </button>
        </div>
        {RadiologyNames.length > 0 && (
          <ReactGrid columns={RadiologyColumns} RowData={RadiologyNames} />
        )}









        {/*------------------TestNames--------------------- */}
        <div className="common_center_tag">
          <span>Test Name</span>
        </div>
        <div className="RegisFormcon_1">
          <div className="RegisForm_1">
            <label> Location <span>:</span> </label>

            <select
              name='Location'
              required
              disabled={TestName.TestNameId}
              value={TestName.Location}
              onChange={handleTestNameChange}
            >
              <option value=''>Select</option>
              {
                LocationData.map((p) => (
                  <option key={p.id} value={p.id}>{p.locationName}</option>
                ))
              }
            </select>
          </div>
          <div className="RegisForm_1">
            <label>
              Radiology Department <span>:</span>
            </label>
            <select
              name="RadiologyName"
              required
              value={TestName.RadiologyName}
              onChange={handleTestNameChange}
              disabled={!isEditing}
            >
              <option value="">Select</option>
              {RadiologyNames?.map((dept, indx) => (
                <option key={indx} value={dept.RadiologyName}>
                  {dept.RadiologyName}
                </option>
              ))}
            </select>
          </div>
          <div className="RegisForm_1">
            <label>
              Test Name <span>:</span>
            </label>
            <input
              type="text"
              name="TestName"
              required
              value={TestName.TestName}
              autoComplete="off"
              disabled={!isEditing}
              onChange={handleTestNameChange}
            />
          </div>
          <div className="RegisForm_1">

            <label>
              Test Amount <span>:</span>
            </label>
            <input
              type="number"
              name="Amount"
              autoComplete="off"
              onKeyDown={(e) =>
                ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()
              }
              required
              value={TestName.Amount}
              onChange={handleTestNameChange}
            />
          </div>

          <div className="RegisForm_1">
              <label>
                BookingFees <span>:</span>
              </label>
              <input
                type="number"
                name="BookingFees"
                autoComplete="off"
                onKeyDown={(e) =>
                  ["e", "E", "+", "-"].includes(e.key) && e.preventDefault()
                }
                required
                value={TestName.BookingFees}
                onChange={handleTestNameChange}
              />
            </div>



            <div className="RegisForm_1">
              {Object.keys(ChooseFile).map((field, indx) => (
                <div className="RegisForm_1" key={indx}>
                  <label htmlFor={`${field}_${indx}_${field}`}>
                    {formatLabel(field)} <span>:</span>
                  </label>
                  <input
                    type="file"
                    name={field}
                    accept="image/jpeg, image/png, application/pdf, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    required
                    id={`${field}_${indx}_${field}`}
                    autoComplete="off"
                    onChange={handleinpchangeDocumentsForm}
                    style={{ display: "none" }}
                  />
                  <div
                    style={{
                      width: "87px",
                      display: "flex",
                      justifyContent: "flex-start",
                      gap: "10px",
                    }}
                  >
                    <label
                      htmlFor={`${field}_${indx}_${field}`}
                      className="RegisterForm_1_btns choose_file_update"
                    >
                <PhotoCameraBackIcon />
                </label>
          
                  </div>
                </div>
              ))}
            </div>



        



        </div>
      

        <div className="Main_container_Btn">
          <button onClick={handleTestNameSubmit}>
            {TestName.TestNameId ? "Update" : "Save"}
          </button>
        </div>
        {TestNames.length > 0 && (
          <ReactGrid columns={TestNameColumns} RowData={TestNames} />
        )}

      </div>



      <ToastAlert Message={toast.message} Type={toast.type} />
    </>
  );
};

export default RadiologyMaster;













