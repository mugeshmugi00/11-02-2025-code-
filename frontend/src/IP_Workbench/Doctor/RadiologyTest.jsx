
import React, { useState, useEffect } from "react";
import axios from "axios";
import { useDispatch, useSelector } from "react-redux";
import ReactGrid from "../../OtherComponent/ReactGrid/ReactGrid";
import ToastAlert from "../../OtherComponent/ToastContainer/ToastAlert";
import { FaTrash } from 'react-icons/fa';
import Button from "@mui/material/Button";
import ToggleButton from "@mui/material/ToggleButton";
import ToggleButtonGroup from "@mui/material/ToggleButtonGroup";
import ModelContainer from "../../OtherComponent/ModelContainer/ModelContainer";
import VisibilityIcon from '@mui/icons-material/Visibility';



const RadiologyTest = () => {
    const [TestNames, setTestNames] = useState([]);
    const UrlLink = useSelector((state) => state.userRecord?.UrlLink);
    const userRecord = useSelector((state) => state.userRecord?.UserData);
    const toast = useSelector((state) => state.userRecord?.toast);
    const IP_DoctorWorkbenchNavigation = useSelector(state => state.Frontoffice?.IP_DoctorWorkbenchNavigation);
    
    const dispatchvalue = useDispatch();
    const [completeArr, SetCompleteArr] = useState([]);
    const [type, setType] = useState("AddTest");
    const handlePageChange = (event, newType) => {
        if (newType !== null && newType !== type) {
            setType(newType);
        }
    };
    useEffect(() => {
        axios
            .get(`${UrlLink}Masters/Radiology_details_link_view`)
            .then((res) => {
                const ress = res.data;
                setTestNames(ress);
            })
            .catch((err) => {
                console.log(err);
            });
    }, [UrlLink]);

    const [SubtestNo, setSubtestNo] = useState([]);
   

 


    const handleCheckboxSubtestNo = (Curr_Amount, testid, TestName, Radiologyid, RadiologyName, TestCode,SubTestType) => {

        const isChecked = SubtestNo.some(item => item.TestCode === TestCode);
        if (isChecked) {
            const newCheckedState = SubtestNo.filter(item => item.TestCode !== TestCode);
            setSubtestNo(newCheckedState);
        } else {
            const newCheckedState = [...SubtestNo, { Radiologyid, RadiologyName, testid, TestName, Curr_Amount, TestCode,SubTestType }];
            setSubtestNo(newCheckedState);
        }
    };

    const handleRemoveTestName = (row) => {
        // Remove from SubtestNo (if applicable)
        const newSubtestNoState = SubtestNo.filter(
            item => item.testid !== row.testid || item.Radiologyid !== row.Radiologyid
        );
        setSubtestNo(newSubtestNoState);
    };
   




    const IndivitualColumns = [

        {
            key: "id",
            name: "S.No",
            frozen: true,

        },
        {
            key: "TestCode",
            name: "Test Code",
        },
        {
            key: "RadiologyName",
            name: "Radiology Name",
        },


        {
            key: "TestName",
            name: "Test Name",
        },
        {
            key: "Action",
            name: "Action",
            renderCell: (params) => (
                <Button
                    className="cell_btn"
                    onClick={() => handleRemoveTestName(params.row)}
                >
                    <FaTrash className="check_box_clrr_cancell" />
                </Button>
            ),
        },
    ];


   





    const transformFavouriteData = (SubtestNo) => {
        return SubtestNo.map((sutestno, ind) => ({
            Radiologyid: sutestno.Radiologyid, // Correctly assign Radiologyid
            RadiologyName: sutestno.RadiologyName,
            TestCode: sutestno.TestCode,
            TestName: sutestno.TestName,
            testid: sutestno.testid, // Correctly assign testid
            id: ind + 1,  // Ensure unique key for each row
        }));
    };

    const transformedFavouriteData1 = transformFavouriteData(SubtestNo);

    const [RadiologyTest, setRadiologyTest] = useState({
        RadiologyTestId: "",
        SubtestNoArr: "",
    });
    const [IsRadilogyGet, setIsRadilogyGet] = useState(false);
    const [no, setno] = useState([]);
   

    const handleSubmitRadiologyTest = () => {
        if (SubtestNo.length > 0) {
            const data = {
                RadiologyTestId: RadiologyTest.RadiologyTestId,
                SubtestNoArr: SubtestNo,
                created_by: userRecord?.username || "",
                Register_Id: IP_DoctorWorkbenchNavigation?.RegistrationId || "",
                RegisterType:"IP"
            };
            console.log("data", data);
            axios.post(`${UrlLink}OP/Radiology_Request_Detailslink`, data)
                .then((res) => {
                    const resData = res.data;
                    const type = Object.keys(resData)[0];
                    const message = Object.values(resData)[0];
                    const tdata = {
                        message: message,
                        type: type,
                    };
                    dispatchvalue({ type: "toast", value: tdata });
                    setIsRadilogyGet((prev) => !prev);
                    setRadiologyTest({

                        RadiologyTestId: "",
                        CheckedTestNameArr: [],
                        SubtestNoArr: [],
                    });
                    setSubtestNo([]);
                })
                .catch((err) => {
                    console.log(err);
                });
        }
        else {
            const tdata = {
                message: "Please Select TestNames .",
                type: "warn",
            }
            dispatchvalue({ type: "toast", value: tdata });
        }
    };

    useEffect(()=>{
        const params = {
            Register_Id: IP_DoctorWorkbenchNavigation.RegistrationId,
            RegisterType:"IP"
        };
        axios.get(`${UrlLink}OP/Radiology_Request_Detailslink`,{params})
        .then((res)=>{
            const ress = res.data;
            setno(ress?.IsSubTestNo);
        })
        .catch((err)=>{
            console.log(err);
        });
    },[IsRadilogyGet,UrlLink,IP_DoctorWorkbenchNavigation.RegistrationId]);



    const noColumns = [

        {
            key: "id",
            name: "S.No",
            frozen: true,

        },
      
        {
            key: "RadiologyName",
            name: "Radiology Name",
        },


        {
            key: "TestName",
            name: "Test Name",
        },
       
    ];


    useEffect(() => {
        if (IP_DoctorWorkbenchNavigation?.pk) { // Ensure pk exists
            const params = {
                Register_Id: IP_DoctorWorkbenchNavigation.pk,
                RegisterType: "IP"
            };

            axios.get(`${UrlLink}OP/Radiology_Complete_Details_Link`, { params })
                .then((res) => {
                    const ress = res.data;
                    SetCompleteArr(ress); // Update state with the response
                })
                .catch((err) => {
                    console.error("Error fetching data:", err);
                });
        }
    }, [UrlLink, IP_DoctorWorkbenchNavigation?.pk]); // Add pk to the dependency array

    const RadiologyColumns = [

        {
            key: "id",
            name: "S.No",
           frozen:true,

        },

        {
            key: "RadiologistName",
            name: "Radiologist Name",
        },
        {
            key: "TechnicianName",
            name: "Technician Name",
        },
        {
            key: "RadiologyName",
            name: "Radiology Name",
        },
        {
            key: "TestName",
            name: "TestName",
        },
        {
            key: "Action",
            name: "Action",
            renderCell: (params) => (
                <Button
                    key={params.row.id} // Assuming `id` is unique for each row
                    className="cell_btn"
                    onClick={() => handleViewComplete(params.row)}
                >
                    <VisibilityIcon className="check_box_clrr_cancell" />
                </Button>
            ),
        }

    ];


    const [Radiology, setRadiology] = useState({
        ReportDate: "",
        ReportTime: "",
        RadiologistName: "",
        TechnicianName: "",
        Report: "",
    });
    const [ChooseFile, setChooseFile] = useState({
        ChooseFileOne: null,
        ChooseFileTwo: null,
        ChooseFileThree: null,
    });
    const [IsViewMode, setIsViewMode] = useState(false);
    const Selectedfileview = (fileval) => {
        console.log("fileval", fileval);
        if (fileval) {
            let tdata = {
                Isopen: false,
                content: null,
                type: "image/jpg",
            };
            if (
                ["data:image/jpeg;base64", "data:image/jpg;base64"].includes(
                    fileval?.split(",")[0]
                )
            ) {
                tdata = {
                    Isopen: true,
                    content: fileval,
                    type: "image/jpeg",
                };
            } else if (fileval?.split(",")[0] === "data:image/png;base64") {
                tdata = {
                    Isopen: true,
                    content: fileval,
                    type: "image/png",
                };
            } else if (fileval?.split(",")[0] === "data:application/pdf;base64") {
                tdata = {
                    Isopen: true,
                    content: fileval,
                    type: "application/pdf",
                };
            }

            dispatchvalue({ type: "modelcon", value: tdata });
        } else {
            const tdata = {
                message: "There is no file to view.",
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
    const handleClear = () => {
        setRadiology({
            ReportDate: "",
            ReportTime: "",
            RadiologistName: "",
            TechnicianName: "",
            Report: "",
        });

        setChooseFile({
            ChooseFileOne: null,
            ChooseFileTwo: null,
            ChooseFileThree: null,
        });
    };
    const handleViewComplete = (row) => {
        setIsViewMode(true);
        setRadiology({
            ...row,
            ReportDate: row.ReportDate || "",
            ReportTime: row.ReportTime || "",
            RadiologistName: row.RadiologistName || "",
            TechnicianName: row.TechnicianName || "",
            Report: row.Report || "",
        });
        setChooseFile({
            ChooseFileOne: row.Report_fileone,
            ChooseFileTwo: row.Report_filetwo,
            ChooseFileThree: row.Report_filethree,
        });

    };
    const showAllFilesInModel = () => {
        const fileValues = Object.values(ChooseFile).filter(file => file); // Filter out null values
    
        if (fileValues.length > 0) {
            const tdata = {
                Isopen: true,
                content: fileValues, // Pass all files as an array
                type: "multiple", // Add a type to signify multiple files
            };
            dispatchvalue({ type: "modelcon", value: tdata }); // Dispatch to open modal
        } else {
            const tdata = {
                message: "There are no files to view.",
                type: "warn",
            };
            dispatchvalue({ type: "toast", value: tdata });
        }
    };


    const adjustHeight = (e) => {
        e.target.style.height = "auto"; // Reset height to calculate scrollHeight
        e.target.style.height = `${e.target.scrollHeight}px`; // Set height to scrollHeight
      };

    return (
      <>
      <br />

                  <div className="for">
                  <div className="RegisFormcon">
                  <div style={{ width: "100%", display: "grid", placeItems: "center" }}>
                        <ToggleButtonGroup
                            value={type}
                            exclusive
                            onChange={handlePageChange}
                            aria-label="Platform"
                        >
                            <ToggleButton
                                value="AddTest"
                                style={{
                                    height: "30px",
                                    width: "180px",
                                    backgroundColor:
                                        type === "AddTest"
                                            ? "var(--selectbackgroundcolor)"
                                            : "inherit",
                                }}
                                className="togglebutton_container"
                            >
                                Add Test
                            </ToggleButton>
                            <ToggleButton
                                value="ViewTest"
                                style={{
                                    backgroundColor:
                                        type === "ViewTest"
                                            ? "var(--selectbackgroundcolor)"
                                            : "inherit",
                                    width: "180px",
                                    height: "30px",
                                }}
                                className="togglebutton_container"
                            >
                                View Test
                            </ToggleButton>
                        </ToggleButtonGroup>
                    </div>
      
                                   
                    {type === "AddTest" && (
  <>
    <div className="displayuseraccess">
      {TestNames.map((item) => (
        <div key={item.id} className="displayuseraccess_child">
          {/* Display RadiologyName */}
          <label
            htmlFor={item.id}
            style={{ fontSize: "20px", fontWeight: "bold" }}
            className="par_acc_lab"
          >
            {item.RadiologyName}
          </label>

          {/* Check if TestNames is not empty */}
          {item.TestNames.length > 0 ? (
            item.TestNames.map((test) => (
              <div
                key={test.id}
                style={{ marginLeft: "20px", marginTop: "5px" }}
              >
                {/* Checkbox for selecting test */}
                <input
                  type="checkbox"
                  id={test.id}
                  onChange={() =>
                    handleCheckboxSubtestNo(
                      test.Curr_Amount,
                      test.id,
                      test.TestName,
                      item.id,
                      item.RadiologyName,
                      test.TestCode
                    )
                  }
                  checked={SubtestNo.some(
                    (checkedItem) =>
                      checkedItem.TestCode === test.TestCode
                  )}
                  style={{ marginRight: "10px" }}
                />
                <label htmlFor={test.id} className="chi_acc_lab">
                  {test.TestName}
                </label>
              </div>
            ))
          ) : (
            <p>No test available for this radiology.</p> // Handle case where no tests are available
          )}
        </div>
      ))}
    </div>

    {/* Display selected individual tests */}
    {transformedFavouriteData1.length > 0 && (
      <>
        <div className="common_center_tag">
          <span>Selected Test Name</span>
        </div>
        <ReactGrid columns={IndivitualColumns} RowData={transformedFavouriteData1} />
      </>
    )}

    {/* Display selected subtests */}
   
    {/* Save Button */}
    <div className="Main_container_Btn">
      <button onClick={handleSubmitRadiologyTest}>Save</button>
    </div>

              <div className="RegisFormcon_1 jjxjx_">
    {no?.length > 0 && (
     
        <ReactGrid columns={noColumns} RowData={no} />

    )}
    </div>
  </>
)}

                  {type === "ViewTest" && (

<>

<div className="RegisFormcon_1 jjxjx_">
    {completeArr?.length > 0 && (


            <ReactGrid columns={RadiologyColumns} RowData={completeArr} />
  
    )}
    </div>


    {completeArr.length === 0 && (
        <div className="DivCenter_container">
            No Test was complete during the previous visit.
        </div>
    )}
    <br></br>
    <div className="RegisFormcon_1">
        <div className="RegisForm_1">
            <label htmlFor="ReportDate">
                Report Date <span>:</span>
            </label>
            <input
                type="date"
                id="ReportDate"
                name="ReportDate"
                value={Radiology.ReportDate}
                readOnly={IsViewMode}
            />
        </div>
        <div className="RegisForm_1">
            <label htmlFor="ReportTime">
                Report Time <span>:</span>
            </label>
            <input
                type="time"
                id="ReportTime"
                name="ReportTime"
                value={Radiology.ReportTime}
                readOnly={IsViewMode}
            />
        </div>
        <div className="RegisForm_1">
            <label htmlFor="ReceiptNo">
                Radiologist Name <span>:</span>
            </label>
            <input
                type="text"
                id="RadiologistName"
                name="RadiologistName"
                value={Radiology.RadiologistName}
                readOnly={IsViewMode}
                required
            />
        </div>
        <div className="RegisForm_1">
            <label htmlFor="ReportTime">
                Technician Name <span>:</span>
            </label>
            <input
                type="text"
                id="TechnicianName"
                name="TechnicianName"
                value={Radiology.TechnicianName}
                readOnly={IsViewMode}
            />
        </div>
    </div>
    <div className="RegisFormcon_1">
        {Object.keys(ChooseFile).map((field, indx) => (
            <div className="RegisForm_1" key={indx}>
                <label htmlFor={`${field}_${indx}_${field}`}>
                    {" "}
                    {formatLabel(field)} <span>:</span>{" "}
                </label>

                <div
                    style={{
                        width: "150px",
                        display: "flex",
                        justifyContent: "space-around",
                    }}
                >
                    <button
                        className="fileviewbtn"
                        onClick={() => Selectedfileview(ChooseFile[field])}
                    >
                        view
                    </button>
                </div>
            </div>
        ))}
    </div>

 
    <div className="RegisFormcon_1">
                                   <div className="RegisForm_1">
                                    <label htmlFor="ReportTime">
                                        View All <span>:</span>
                                    </label>
                                    <button
                                    className="fileviewbtn"
                                    onClick={showAllFilesInModel}
                                >
                                    ViewAll
                                </button>
                                </div>
                            </div> 

    <div className="eds_kji88">
        <label htmlFor="Report">
            Report <span>:</span>
        </label>
        <textarea
            type="text"
            id="Report"
            name="Report"
            value={Radiology.Report}
            onChange={adjustHeight}
            readOnly={IsViewMode}
            required
        />
    </div>


    {IsViewMode && (
        <div className="Main_container_Btn">
            <button onClick={handleClear}>
                Clear
            </button>
        </div>
    )}


</>
)}        
 <ModelContainer />
 <ToastAlert Message={toast.message} Type={toast.type} />
        </div>
        </div>
        </>

    );

};

export default RadiologyTest;

