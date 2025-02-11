import React, { useState, useEffect, useCallback } from "react";
// import "react-draft-wysiwyg/dist/react-draft-wysiwyg.css";
import axios from "axios";
import { ToastContainer, toast } from "react-toastify";
import { useSelector } from "react-redux";
import AddIcon from "@mui/icons-material/Add";
import EditIcon from "@mui/icons-material/Edit";
import ReactGrid from "../OtherComponent/ReactGrid/ReactGrid";
import Button from "@mui/material/Button";
import EditNoteIcon from '@mui/icons-material/EditNote';



function AddInterpretation() {
  const urllink = useSelector((state) => state.userRecord?.UrlLink);

  const [header, setheader] = useState("");
  const [comments, setComments] = useState("");
  const [testname, setTestName] = useState("");
  const [Test_Code, setTestCode] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [addDatas, setAddDatas] = useState([]);
  const [addData, setAddData] = useState([]);
  const [isEditMode, setIsEditMode] = useState(false);
  const [filteredRows, setFilteredRows] = useState([]);
  const [selectedid, setSelectedid] = useState(null);
  console.log("addData", addData);
  // useEffect(() => {
  //   axios
  //     .get(`${urllink}usercontrol/gettestname`)
  //     .then((response) => {
  //       console.log(response.data);
  //       const data = response.data.test_name;
  //       const testcode = response.data.test_code;
  //       setTestName(data);
  //       setTestCode(testcode);
  //     })
  //     .catch((error) => {
  //       console.log(error);
  //     });
  // }, [urllink]);

  useEffect(() => {
    if (Array.isArray(addDatas)) {
      const lowerCaseNameQuery = searchQuery.toLowerCase();
      const filteredData = addDatas.filter((row) => {
        const lowerCasePatientName = row?.Test_Name
          ? row.Test_Name.toLowerCase()
          : "";
        return lowerCasePatientName.includes(lowerCaseNameQuery);
      });
      setFilteredRows(filteredData);
    } else {
      // Handle the case where ageData is not an array
      setFilteredRows([]);
    }
  }, [searchQuery, addDatas]);

  const handlesubmit = () => {
    const postdata = {
      testname: testname,
      header: header,
      comments: comments,
      Test_Code: Test_Code,
    };

    if (!header) {
      alert("please enter all inputs");
    } else {
      axios
        .post(`${urllink}usercontrol/insertinterpretation`, postdata)
        .then((response) => {
          console.log(response);
          successMsg(response.data.message);
          setComments("");
          setheader("");
          fetchAddInterpretationData();
        })
        .catch((error) => {
          console.log(error);
        });
    }
  };
  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setAddData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const fetchAddInterpretationData = useCallback(() => {
    axios
      .get(`${urllink}Masters/All_Other_Lab_Masters_POST_AND_GET?Type=Get_AllTests_For_Interpretation`)
      .then((response) => {
        const data = response.data;
        console.log("fetchAddInterpretationData", data);

        setAddDatas(data);
      })
      .catch((error) => {
        console.error("Error fetching AddInterpretationData  data:", error);
      });
  }, [urllink]);
  const handleEdit = (row) => {
    console.log(row);
    setheader(row.Header_interpretation);
    setComments(row.Comments);
    setTestName(row.Test_Name);
    setIsEditMode(true);
    setSelectedid(row.Test_Id); // Assuming `id` is the identifier
    setTestCode(row.Test_Code);
  };

  React.useEffect(() => {
    fetchAddInterpretationData();
  }, [fetchAddInterpretationData]);

  const handleUpdateMethod = () => {
    const updatedata = {
      method_id: selectedid, // Assuming `id` is the identifier
      header: header,
      comments: comments,
      testname: testname,
      Test_Code: Test_Code,
      Type: "Update_Testmaster_Interpretation_table"
    };

    axios
      .post(`${urllink}Masters/All_Other_Lab_Masters_POST_AND_GET`, updatedata)
      .then((response) => {
        console.log(response.data);
        successMsg(response.data.message);
        setIsEditMode(false);
        setSelectedid(null);
        setComments("");
        setheader("");

        setTestName("");
        fetchAddInterpretationData();
      })

      .catch((error) => {
        console.error("An error occurred:", error);
      });
  };
  const successMsg = (msg) => {
    toast.success(`${msg}`, {
      position: "top-center",
      autoClose: 1000,
      hideProgressBar: false,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
      theme: "dark",
      style: { marginTop: "50px" },
    });
  };

  // const errmsg = (errorMessage) => {
  //   toast.error(`${errorMessage}`, {
  //     position: "top-center",
  //     autoClose: 5000,
  //     hideProgressBar: false,
  //     closeOnClick: true,
  //     pauseOnHover: true,
  //     draggable: true,
  //     progress: undefined,
  //     theme: "dark",
  //     style: { marginTop: "50px" },
  //   });
  // };

  const handleSearchChange = (e) => {
    const { name, value } = e.target;

    if (name === "TestName") {
      setSearchQuery(value);
    }
  };

  const InterpretationMastercolumns = [
    {
      key: "id",
      name: "S.No",
      width: 70,
      frozen: true
    },
    {
      key: "Test_Name",
      name: "Test Name",
      width: 300,
      frozen: true
    },
    {
      key: "Header_interpretation",
      name: "Header interpretation",
      width: 200,
    },
    {
      key: "Comments",
      name: "Comments",
      width: 450,
    },

    {
      key: "EditAction",
      name: "Action",
      renderCell: (params) => (
        <Button
          onClick={() => handleEdit(params.row)}
        >
          <EditNoteIcon />
        </Button>
      ),
    },
  ];

  return (
    <>
      <div className="appointment">
        <br />

        <div className="RegisFormcon">
          <div className="RegisForm_1">
            <label htmlFor="selectTest">
              Test Name<span>:</span>
            </label>
            <input
              type="text"
              id="testname"
              name="selectTest"
              required
              value={testname}
              onChange={handleInputChange}
              readOnly
            />
          </div>
          <div className="RegisForm_1">
            <label htmlFor="validation">
              Header For interpretation <span>:</span>
            </label>
            <textarea
              id="remarks"
              name="remarks"
              value={header}
              onChange={(e) => {
                setheader(e.target.value);
              }}
              className="custom-textarea"
            ></textarea>
          </div>
          <div className="RegisForm_1">
            <label htmlFor="remarks">
              Comments<span>:</span>
            </label>
            <textarea
              id="remarks"
              name="remarks"
              value={comments}
              onChange={(e) => {
                setComments(e.target.value);
              }}
            ></textarea>
          </div>
        </div>
        <br />

        <div className="Register_btn_con">
          <button
            className="RegisterForm_1_btns"
            onClick={isEditMode ? handleUpdateMethod : handlesubmit}
          >
            {isEditMode ? "Update" : <AddIcon />}
          </button>
        </div>
        <div style={{ width: "100%", display: "grid", placeItems: "center" }}>
          <div className="con_1">
            <div className="inp_1">
              <label htmlFor="TestName">
                Test Name<span>:</span>
              </label>
              <input
                type="text"
                id="TestName"
                name="TestName"
                value={searchQuery}
                placeholder="Enter Test Name"
                onChange={handleSearchChange}
              />
            </div>
          </div>
        </div>
        <div className="Main_container_app">
          <ReactGrid
            columns={InterpretationMastercolumns}
            RowData={filteredRows}
          />
        </div>
        <ToastContainer />
      </div>
    </>
  );
}

export default AddInterpretation;
