import React, { useCallback, useEffect, useState } from "react";
import EditIcon from "@mui/icons-material/Edit";
import axios from "axios";
import Button from "@mui/material/Button";
import { useDispatch, useSelector } from "react-redux";
import ToastAlert from "../OtherComponent/ToastContainer/ToastAlert";
import ReactGrid from "../OtherComponent/ReactGrid/ReactGrid";
import AddCircleOutlineIcon from "@mui/icons-material/AddCircleOutline";
import { useNavigate } from "react-router-dom";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import ArrowDropDownOutlinedIcon from "@mui/icons-material/ArrowDropDownOutlined";
import ArrowDropUpOutlinedIcon from "@mui/icons-material/ArrowDropUpOutlined";
import Box from "@mui/material/Box";
import Collapse from "@mui/material/Collapse";
import EditNoteIcon from "@mui/icons-material/EditNote";
import HighlightOffIcon from "@mui/icons-material/HighlightOff";

function DutyRosterMasterList() {
  const [dutyData, setDutyData] = useState([]);
  const navigate = useNavigate();
  const UrlLink = useSelector((state) => state.userRecord?.UrlLink);
  const [openRow, setOpenRow] = useState(null); // Store the currently open row
  const dispatchvalue = useDispatch();
  const toast = useSelector((state) => state.userRecord?.toast);
  const [editShiftId, setEditShiftId] = useState(null);
  const [editedTimes, setEditedTimes] = useState({});

  const toggleRow = (subDepartmentId) => {
    // Toggle only one row at a time
    setOpenRow((prevOpenRow) =>
      prevOpenRow === subDepartmentId ? null : subDepartmentId
    );
  };

  const fetchmasterdata = useCallback(() => {
    axios
      .get(`${UrlLink}HR_Management/DutyRosterMasters`)
      .then((response) => {
        console.log(response);
        setDutyData(response.data);
      })
      .catch((err) => console.error(err));
  }, [UrlLink]);

  useEffect(() => {
    fetchmasterdata();
  }, [fetchmasterdata]);

  const handlenavigate = () => {
    dispatchvalue({
      type: "DeptShiftMasterEdit",
      value: {},
    });
    navigate("/Home/HR");
    dispatchvalue({ type: 'HrFolder', value:'DutyRoster'});
    dispatchvalue({ type: "setPreviousFolder", value: null }); 
    dispatchvalue({ type: "showMenu", value: true });
  };

  const handleDutyStatus = (params) => {
    console.log(params);
    const data = {
      ShiftId: params.ShiftId,
      Statusedit: true,
      Status: params.Status,
    };
    axios
      .post(`${UrlLink}HR_Management/DutyRosterMasters`, data)
      .then((res) => {
        console.log(res);
        const response = res.data;
        const type = Object.keys(response)[0];
        const mess = Object.values(response)[0];
        dispatchvalue({ type: "toast", value: { message: mess, type } });
        fetchmasterdata();
      })
      .catch((err) => console.error(err));
  };

  const handleEditClick = (ShiftId, StartTime, EndTime, ShiftName) => {
    setEditShiftId(ShiftId);
    setEditedTimes({
      StartTime: StartTime,
      EndTime: EndTime,
      ShiftId: ShiftId,
      ShiftName: ShiftName,
      SingleShiftEdit: true,
    });
  };

  const handleUpdate = (ShiftId) => {
    // Update logic here, e.g., send editedTimes to the backend
    console.log("Updated Shift:", ShiftId, editedTimes);
    axios
      .post(`${UrlLink}HR_Management/DutyRosterMasters`, editedTimes)
      .then((res) => {
        console.log(res);
        const response = res.data;
        const type = Object.keys(response)[0];
        const mess = Object.values(response)[0];
        dispatchvalue({ type: "toast", value: { message: mess, type } });
        fetchmasterdata();
        // Reset editing state
        setEditShiftId(null);
        setEditedTimes({});
      })
      .catch((err) => console.error(err));
  };

  const handleChange = (field, value) => {
    setEditedTimes((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleCancelEdit = () => {
    // Reset editing state
    setEditShiftId(null);
    setEditedTimes({});
  };

  const DutyMasterColumn = [
    { key: "ShiftId", name: "Shift ID", frozen: true },
    {
      key: "ShiftName",
      name: "Shift Name",
      frozen: true,
      renderCell: (params) =>
        editShiftId === params.row.ShiftId ? (
          <input
            type="text"
            value={editedTimes.ShiftName}
            style={{
              width: "120px",
              border: "1px solid var(--ProjectColor)",
              borderRadius: "5px",
              padding: "5px",
              backgroundColor: "var(--selectbackgroundcolor)",
            }}
            onChange={(e) => handleChange("ShiftName", e.target.value)}
          />
        ) : (
          params.row.ShiftName
        ),
    },

    {
      key: "display_starttime",
      name: "Start Time",
      renderCell: (params) =>
        editShiftId === params.row.ShiftId ? (
          <input
            type="time"
            value={editedTimes.StartTime}
            style={{
              width: "80px",
              border: "1px solid var(--ProjectColor)",
              borderRadius: "5px",
              padding: "5px",
              backgroundColor: "var(--selectbackgroundcolor)",
            }}
            onChange={(e) => handleChange("StartTime", e.target.value)}
          />
        ) : (
          params.row.display_starttime
        ),
    },
    {
      key: "display_EndTime",
      name: "End Time",
      renderCell: (params) =>
        editShiftId === params.row.ShiftId ? (
          <input
            type="time"
            value={editedTimes.EndTime}
            style={{
              width: "80px",
              border: "1px solid var(--ProjectColor)",
              borderRadius: "5px",
              padding: "5px",
              backgroundColor: "var(--selectbackgroundcolor)",
            }}
            onChange={(e) => handleChange("EndTime", e.target.value)}
          />
        ) : (
          params.row.display_endtime
        ),
    },
    {
      key: "Action",
      name: "Actions",
      children: [
        {
          key: "Edit",
          name: "Edit",
          renderCell: (params) =>
            editShiftId === params.row.ShiftId ? (
              <div
                style={{
                  display: "flex",
                  width: "70px",
                  flexDirection: "column",
                }}
              >
                <div>
                  <Button
                    className="update_btn"
                    onClick={() => handleUpdate(params.row.ShiftId)}
                  >
                    Update
                  </Button>
                </div>
                <div>
                  <Button className="cancel_btn" onClick={handleCancelEdit}>
                    Cancel
                  </Button>
                </div>
              </div>
            ) : (
              <div style={{ display: "flex", flexDirection: "column" }}>
                <div>
                  <Button
                    className="edit_btn"
                    onClick={() =>
                      handleEditClick(
                        params.row.ShiftId,
                        params.row.StartTime,
                        params.row.EndTime,
                        params.row.ShiftName
                      )
                    }
                  >
                    Edit
                  </Button>
                </div>
              </div>
            ),
        },
        {
          key: "Status",
          name: "Status",
          renderCell: (params) => (
            <Button
              // className="cell_btn"
              className="update_btn"
              onClick={() => handleDutyStatus(params.row)}
            >
              {params.row.Status === true ? "Active" : "Inactive"}
            </Button>
          ),
        },
      ],
    },
  ];

  const HandleDeptShiftEdit = (row) => {
    console.log(row);
    dispatchvalue({
      type: "DeptShiftMasterEdit",
      value: row,
    });

    navigate("/Home/HR");
    dispatchvalue({ type: 'HrFolder', value:'DutyRoster'});
    dispatchvalue({ type: "setPreviousFolder", value: null }); 
    dispatchvalue({ type: "showMenu", value: true });


  };

  return (
    <div className="Main_container_app">
      <h3>Duty Roster Master</h3>
      <br />
      <div>
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
                <TableCell width={100}>Edit</TableCell>
                <TableCell width={100}>Total Shifts</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {Array.isArray(dutyData) &&
                dutyData.map((row, index) => (
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
                          onClick={() => toggleRow(row.Department)}
                        >
                          {openRow === row.Department ? (
                            <ArrowDropUpOutlinedIcon />
                          ) : (
                            <ArrowDropDownOutlinedIcon />
                          )}
                        </span>
                      </TableCell>
                      <TableCell>{index + 1}</TableCell>
                      <TableCell>{row.department_name}</TableCell>
                      <TableCell>
                        <Button
                          className="update_btn"
                          onClick={() => HandleDeptShiftEdit(row)}
                        >
                          <EditIcon />
                        </Button>
                      </TableCell>
                      <TableCell>{row.ShiftCounts}</TableCell>
                    </TableRow>

                    <TableRow>
                      <TableCell
                        style={{ paddingBottom: 0, paddingTop: 0 }}
                        colSpan={6}
                      >
                        <Collapse
                          in={openRow === row.Department}
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
                              ></div>
                              <ReactGrid
                                columns={DutyMasterColumn}
                                RowData={row?.shifts}
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
      <div className="NewList-export-buttons">
        <span>Row length </span>
        <span> : {dutyData?.length}</span>
      </div>
      <ToastAlert Message={toast.message} Type={toast.type} />
    </div>
  );
}

export default DutyRosterMasterList;
