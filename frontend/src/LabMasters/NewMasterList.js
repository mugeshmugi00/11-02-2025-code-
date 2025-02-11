import React, { useState, useEffect, useCallback } from "react";
import Box from "@mui/material/Box";
import Collapse from "@mui/material/Collapse";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import axios from "axios";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import Button from "@mui/material/Button";
import ArrowDropDownOutlinedIcon from "@mui/icons-material/ArrowDropDownOutlined";
import ArrowDropUpOutlinedIcon from "@mui/icons-material/ArrowDropUpOutlined";
import ReactGrid from "../OtherComponent/ReactGrid/ReactGrid";
import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline";
import ToastAlert from "../OtherComponent/ToastContainer/ToastAlert";
import EditNoteIcon from '@mui/icons-material/EditNote';
import UploadIcon from '@mui/icons-material/Upload';
import PhotoCameraBackIcon from "@mui/icons-material/PhotoCameraBack";


export default function NewMasterList() {
  const [data, setData] = useState([]);
  const [openRow, setOpenRow] = useState(null); // Store the currently open row
  const [searchQuery, setSearchQuery] = useState("");
  const UrlLink = useSelector(state => state.userRecord?.UrlLink);
  const toast = useSelector((state) => state.userRecord?.toast);
  // const UrlLink = useSelector((state) => state.userRecord?.UrlLink);
  const dispatchvalue = useDispatch();
  const navigate = useNavigate();
  const [searchQuery1, setSearchQuery1] = useState("");
  const [SelectedFile, setSelectedFile] = useState(null);
  const [filteredRows, setFilteredRows] = useState([]);
  const userRecord = useSelector((state) => state.userRecord?.UserData);
  console.log(userRecord)
  const fetchget_department_and_their_tests = useCallback(() => {
    axios
      .get(`${UrlLink}Masters/All_Other_Lab_Masters_POST_AND_GET?Type=TestMaster`)
      .then((response) => {
        console.log(response.data);
        const data = response.data.data;
        setData(data);
      })
      .catch((error) => {
        console.error("Error fetching test description data:", error);
      });
  }, [UrlLink]);

  useEffect(() => {
    fetchget_department_and_their_tests();
  }, [fetchget_department_and_their_tests]);

  const toggleRow = (subDepartmentId) => {
    // Toggle only one row at a time
    setOpenRow((prevOpenRow) =>
      prevOpenRow === subDepartmentId ? null : subDepartmentId
    );
  };

  const handleEditClick = (test) => {
    console.log(test);
    const updatedRowWithEditMode = { ...test, isEditMode: true };
    console.log(updatedRowWithEditMode)

    dispatchvalue({ type: "TestMasterEditData", value: updatedRowWithEditMode });
    navigate("/Home/TestMaster");
  };

  const handleSearchChange = (e) => {
    setSearchQuery1(e.target.value);
  };

  const handleSearchChange1 = (e) => {
    setSearchQuery(e.target.value);
  };

  const filterTestsBySearchQuery = (tests) => {
    return tests.filter((test) =>
      test.Test_Name.toLowerCase().includes(searchQuery.toLowerCase())
    );
  };

  const handlenavigate = () => {
    // navigate("/Home/TestMaster");

    navigate("/Home/MasterFolder");
    dispatchvalue({ type: 'HrFolder', value:'TestMaster'});
    dispatchvalue({ type: "setPreviousFolder", value: null }); 
    dispatchvalue({ type: "showMenu", value: true });

    dispatchvalue({ type: "TestMaster", value: null });
  };

  const hadleeditstatus = (params) => {
    console.log(params);

    let newstatus;
    if (params.Status === "Active") {
      newstatus = "Inactive";
    } else if (params.Status === "Inactive") {
      newstatus = "Active";
    }

    axios
      .post(
        `${UrlLink}Masters/Update_All_Masters_Status_update?Test_Code=${params.Test_Code}&newstatus=${newstatus}&Type=TestMaster`
      )
      .then((res) => {
        console.log(res);
        successMsg(res.data.message);
        fetchget_department_and_their_tests();
      })

      .catch((err) => {
        console.error();
      });
  };

  const Agesetupcolumns = [
    {
      key: "id",
      name: "S.No",
      width: 70,
      frozen: true,
    },
    {
      key: "Test_Name",
      name: "Test Name",
      width: 281,
      frozen: true,
    },
    // {
    //   key: "Method_Name",
    //   name: "Method Name",
    // },
    {
      key: "Gender",
      name: "Gender",
    },
    // {
    //   key: "Specimen_Name",
    //   name: "Specimen Name",
    // },
    {
      key: "EditAction",
      name: "Edit",
      width: 70,
      renderCell: (params) => (
        <Button
          onClick={() => handleEditClick(params.row)}
        >
          <EditNoteIcon />
        </Button>
      ),
    },

    {
      key: "Status",
      name: "Status",
      width: 70,

      renderCell: (params) =>
        params.row.Status === "Inactive" ? (
          <Button onClick={() => hadleeditstatus(params.row)}>
            <span style={{ color: "red" }}>{params.row.Status}</span>
          </Button>
        ) : (
          <Button onClick={() => hadleeditstatus(params.row)}>
            <span style={{ color: "black" }}>{params.row.Status}</span>
          </Button>
        ),
    },
  ];

  const handleFileChange = (event) => {
    setSelectedFile(null);
    setSelectedFile(event.target.files[0]);
  };

  useEffect(() => {
    const lowerCaseQuery2 = searchQuery1.toLowerCase();

    const filteredData = Array.isArray(data) && data?.filter((row) => {
      const lowerCasesub_department_name = row.sub_department_name
        ? row.sub_department_name.toLowerCase()
        : "";
      return lowerCasesub_department_name.includes(lowerCaseQuery2);
    });

    setFilteredRows(filteredData);
  }, [searchQuery1, data]);

  const handleCsvupload = () => {
    console.log(SelectedFile);
    const formData = new FormData();
    formData.append("file", SelectedFile);
    formData.append("Type", "TestMaster_CSV");
    formData.append("created_by", userRecord?.username);

    if (SelectedFile) {
      axios
        .post(`${UrlLink}Masters/All_CSV_Files_Upload`, formData, {
          headers: { "Content-Type": "multipart/form-data" },
        })
        .then((response) => {
          console.log(response);
          // successMsg("File Processed Successfully");
          // fetch_testmasterdata();

          const reste = response?.data;
          const typp = Object.keys(reste)[0];
          const mess = Object.values(reste)[0];
          const tdata = {
              message: mess,
              type: typp,
          };
          dispatchvalue({ type: "toast", value: tdata });
          setSelectedFile(null);
        })
        .catch((error) => {
          console.log(error);
          alert(error);
        });
    } else {
      // userwarn("Choose File");
    }
  };

  const successMsg = (message) => {
    toast.success(message, {
      position: "top-center",
      autoClose: 5000,
      hideProgressBar: false,
      closeOnClick: true,
      pauseOnHover: true,
      draggable: true,
      progress: undefined,
      theme: "dark",
      style: { marginTop: "50px" },
    });
  };

  const hadleeditstatus1 = (params) => {
    console.log(params);

    let newstatus;
    if (params.Status === "Active") {
      newstatus = "Inactive";
    } else if (params.Status === "Inactive") {
      newstatus = "Active";
    }

    axios
      .post(
        `${UrlLink}Masters/Update_All_Masters_Status_update?subdepartment_code=${params.sub_department_code}&newstatus=${newstatus}&Type=SubMainDepartment`
      )
      .then((res) => {
        console.log(res);
        successMsg(res.data.message);
        fetchget_department_and_their_tests();
      })

      .catch((err) => {
        console.error();
      });
  };

  return (
    <div className="appointment">
      <div className="h_head">
        <h4>Test Master List</h4>
      </div>
      <br />

      <div className="search_div_bar">
        <div className=" search_div_bar_inp_1">
          <label htmlFor="input">
            Department Name <span>:</span>
          </label>
          <input
            type="text"
            name="TestName"
            id="TestName"
            value={searchQuery1}
            onChange={handleSearchChange}
            placeholder="Enter Department Name"
          />
        </div>
        <div className=" search_div_bar_inp_1">
          <label>
            {" "}
            TestMaster Excel File<span>:</span>{" "}
          </label>
          <input
            type="file"
            accept=".xlsx, .xls, .csv"
            id="Servicechoose"
            required
            style={{ display: "none" }}
            onChange={handleFileChange}
          />
          <label
          title="Choose File"
            htmlFor="Servicechoose"
            className="RegisterForm_1_btns choose_file_update"
          >
       <PhotoCameraBackIcon />
          </label>
          <button
          title="Upload"
            className="RegisterForm_1_btns choose_file_update"
            onClick={handleCsvupload}
          >
<UploadIcon />
          </button>
        </div>
      </div>
      <div className="search_div_bar">
        <button
          className="RegisterForm_1_btns"
          type="submit"
          onClick={handlenavigate}
        >
          <AddCircleOutlineIcon />
        </button>
      </div>


      <div className="NewTest_Master_grid_M_head_M">
        <TableContainer className="NewTest_Master_grid_M">
          <Table className="dehduwhd_o8i">
            <TableHead>
              <TableRow>
                <TableCell width={10} />
                <TableCell width={50}>S.No</TableCell>
                <TableCell width={400}>Department</TableCell>
                <TableCell width={100}>Status</TableCell>
                <TableCell width={100}>Test Count</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {Array.isArray(filteredRows) && filteredRows.map((row, index) => (
                <React.Fragment key={index}>
                  <TableRow
                    style={{
                      backgroundColor:
                        index % 2 === 1
                          ? "var(--selectbackgroundcolor)"
                          : "white",
                    }}
                  >
                    <TableCell>
                      <span
                        aria-label="expand row"
                        // size="small"
                        className="newmasterbseiuhfuisehbutton"
                        onClick={() => toggleRow(row.sub_department_id)}
                      >
                        {openRow === row.sub_department_id ? (
                          <ArrowDropUpOutlinedIcon />
                        ) : (
                          <ArrowDropDownOutlinedIcon />
                        )}
                      </span>
                    </TableCell>
                    <TableCell>{index + 1}</TableCell>
                    <TableCell>{row.sub_department_name}</TableCell>
                    <TableCell>
                      {row.Status === "Inactive" ? (
                        <Button onClick={() => hadleeditstatus1(row)}>
                          <span style={{ color: "red" }}>{row.Status}</span>
                        </Button>
                      ) : (
                        <Button onClick={() => hadleeditstatus1(row)}>
                          <span style={{ color: "black" }}>{row.Status}</span>
                        </Button>
                      )}
                    </TableCell>
                    <TableCell>{row.Testcount}</TableCell>
                  </TableRow>

                  <TableRow>
                    <TableCell
                      style={{ paddingBottom: 0, paddingTop: 0 }}
                      colSpan={6}
                    >
                      <Collapse
                        in={openRow === row.sub_department_id} // Only expand the row that matches the openRow
                        timeout="auto"
                        unmountOnExit
                      >
                        <Box sx={{ margin: 1 }}>
                          <div className="Main_container_app">
                            <div
                              style={{
                                width: "100%",
                                display: "grid",
                                placeItems: "center",
                              }}
                            >
                              <div className="con_1">
                                <div className="inp_1">
                                  <label htmlFor="input">
                                    Test Name <span>:</span>
                                  </label>
                                  <input
                                    type="text"
                                    value={searchQuery}
                                    onChange={handleSearchChange1}
                                    placeholder="Enter Test Name"
                                  />
                                </div>
                              </div>
                            </div>

                            <ReactGrid
                              columns={Agesetupcolumns}
                              RowData={filterTestsBySearchQuery(row.tests)}
                            />
                          </div>
                        </Box>
                      </Collapse>
                    </TableCell>
                  </TableRow>
                </React.Fragment>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </div>

      <div className="RegisFormcon" style={{justifyContent:'center'}}>
        <div className="RegisForm_1">
          <label>Row length</label> <span>:</span>
          <label>{filteredRows?.length}</label>

        </div>
      </div>
      <ToastAlert Message={toast.message} Type={toast.type} />
    </div>
  );
}
