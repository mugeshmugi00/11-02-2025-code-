import React, { useEffect, useState } from "react";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import axios from "axios";
import Button from "@mui/material/Button";
import { useDispatch, useSelector } from "react-redux";
import ToastAlert from "../OtherComponent/ToastContainer/ToastAlert";
import ReactGrid from "../OtherComponent/ReactGrid/ReactGrid";
import { useNavigate } from "react-router-dom";

function DutyRoster() {
  const UrlLink = useSelector((state) => state.userRecord?.UrlLink);
  const userRecord = useSelector((state) => state.userRecord?.UserData);
  const toast = useSelector((state) => state.userRecord?.toast);
  const [Departments, setDepartments] = useState([]);
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const DeptShiftMasterEdit = useSelector(
    (state) => state.Frontoffice?.DeptShiftMasterEdit
  );
  console.log(DeptShiftMasterEdit);

  const [dutyMasterData, setDutyMasterData] = useState({
    ShiftId: "",
    DepartmentName: "",
    Department: "",
    ShiftName: "",
    StartTime: "",
    EndTime: "",
  });

  const [IsdutyGet, setIsDutyGet] = useState(false);
  const [dutyData, setDutyData] = useState([]);
  const [shifts, setShifts] = useState([]);
  const [shiftCounter, setShiftCounter] = useState(1);

  const [is_edit, setis_edit] = useState(false);
  const [Statusedit, setStatusedit] = useState(false);

  useEffect(() => {
    if (DeptShiftMasterEdit && Object.keys(DeptShiftMasterEdit).length > 0) {
      setDutyMasterData((prev) => ({
        ...prev,
        DepartmentName: DeptShiftMasterEdit?.department_name,
        Department: DeptShiftMasterEdit?.Department,
      }));
      setis_edit(true);
      setShifts(DeptShiftMasterEdit?.shifts);
    }
  }, [DeptShiftMasterEdit]);
  const handleChange = (e) => {
    const { name, value } = e.target;
    setDutyMasterData((prevData) => {
      if (name === "DepartmentName") {
        const selectDept = Departments.find(
          (dpt) => dpt.DepartmentName === value
        );
        return {
          ...prevData,
          [name]: value,
          Department: selectDept?.id || "",
        };
      }
      return {
        ...prevData,
        [name]: value,
      };
    });
  };
  console.log(dutyMasterData);
  const addShift = () => {
    if (
      dutyMasterData.ShiftName &&
      dutyMasterData.StartTime &&
      dutyMasterData.EndTime &&
      dutyMasterData.DepartmentName
    ) {
      if (dutyMasterData.ShiftId) {
        setShifts((prevShifts) =>
          prevShifts.map((shift) =>
            shift.ShiftId === dutyMasterData.ShiftId ? dutyMasterData : shift
          )
        );
      } else {
        setShifts((prevShifts) => [
          ...prevShifts,
          { ...dutyMasterData, ShiftId: shiftCounter },
        ]);
        setShiftCounter((prevCounter) => prevCounter + 1);
      }
      setDutyMasterData({
        ShiftId: "",
        DepartmentName: dutyMasterData.DepartmentName,
        Department: dutyMasterData.Department,
        ShiftName: "",
        StartTime: "",
        EndTime: "",
      });
    } else {
      const mess = "Please add at least one shift.";
      const type = "warn";
      dispatch({ type: "toast", value: { message: mess, type } });
    }
  };

  const handleDutyMasterSubmit = async () => {
    console.log(shifts);
    if (shifts.length > 0) {
      const data = shifts.map((shift) => ({
        ...shift,
        Location: userRecord?.location || "",
        Created_by: userRecord?.username || "",
        is_edit: is_edit,
        Statusedit: Statusedit,
      }));
      console.log(data);

      try {
        const res = await axios.post(
          `${UrlLink}HR_Management/DutyRosterMasters`,
          data
        );
        console.log(res.data);
        const rest = res.data;
        console.log(rest);
        const type = Object.keys(rest)[0];
        const mess = Object.values(rest)[0];

        dispatch({ type: "toast", value: { message: mess, type } });

        setIsDutyGet((prev) => !prev);
        setShifts([]);
        setDutyMasterData({
          ShiftId: "",
          DepartmentName: "",
          Department: "",
          ShiftName: "",
          StartTime: "",
          EndTime: "",
        });
        setShiftCounter(1);
        navigate("/Home/HR");
      } catch (err) {
        console.error("Error:", err);
      }
    } else {
      dispatch({
        type: "toast",
        value: { message: "Please add at least one shift.", type: "warn" },
      });
    }
  };

  useEffect(() => {
    axios
      .get(`${UrlLink}Masters/Department_Detials_link`)
      .then((res) => setDepartments(res.data))
      .catch((err) => console.error(err));
  }, [UrlLink]);

  useEffect(() => {
    axios
      .get(`${UrlLink}HR_Management/Duty_Master`)
      .then((response) => setDutyData(response.data))
      .catch((err) => console.error(err));
  }, [IsdutyGet, UrlLink]);

  const handleEditDuty = (params) => {
    setDutyMasterData({
      ShiftId: params.row.ShiftId,
      DepartmentName: params.row.DepartmentName,
      Department: params.row.Department,
      ShiftName: params.row.ShiftName,
      StartTime: params.row.StartTime,
      EndTime: params.row.EndTime,
    });
  };

  const handleDeleteShift = (shiftId) => {
    setShifts((prevShifts) =>
      prevShifts.filter((shift) => shift.ShiftId !== shiftId)
    );
  };

  const DutyMasterColumn = [
    { key: "ShiftId", name: "ShiftId", frozen: true },
    {
      key: "DepartmentName",
      name: "Department",
      frozen: true,
    },
    { key: "ShiftName", name: "Shift Name", frozen: true },
    { key: "StartTime", name: "Start Time" },
    { key: "EndTime", name: "End Time" },
    {
      key: "Edit",
      name: "Edit",
      renderCell: (params) => (
        <Button className="cell_btn" onClick={() => handleEditDuty(params)}>
          <EditIcon className="check_box_clrr_cancell" />
        </Button>
      ),
    },
    {
      key: "Delete",
      name: "Delete",
      renderCell: (params) => (
        <Button
          className="cell_btn"
          onClick={() => handleDeleteShift(params.row.ShiftId)}
        >
          <DeleteIcon className="check_box_clrr_cancell" />
        </Button>
      ),
    },
  ];

  const formFields = [
    {
      label: "Department Name",
      name: "DepartmentName",
      type: "text",
      list: "departments",
    },
    { label: "Shift Name", name: "ShiftName", type: "text" },
    { label: "Shift Start Time", name: "StartTime", type: "time" },
    { label: "Shift End Time", name: "EndTime", type: "time" },
  ];

  return (
    <>
      <div className="Main_container_app">
        <h3>Duty Roster Master</h3>
        <br />

        <div className="RegisFormcon_1">
          {formFields.map((field) => (
            <div className="RegisForm_1" key={field.name}>
              <label>
                {field.label} <span>:</span>
              </label>
              <input
                type={field.type}
                name={field.name}
                value={dutyMasterData[field.name]}
                onChange={handleChange}
                list={field.list || undefined}
                disabled={is_edit && field.name === "DepartmentName"}
                autoComplete="off"
              />
              {field.list === "departments" && (
                <datalist id={field.list}>
                  {Departments.map((dpt) => (
                    <option key={dpt.id} value={dpt.DepartmentName} />
                  ))}
                </datalist>
              )}
            </div>
          ))}
        </div>
        <br />
        <div className="Main_container_Btn">
          <button onClick={addShift}>
            {dutyMasterData.ShiftId ? "Update Shift" : "Add Shift"}
          </button>
          <button onClick={handleDutyMasterSubmit}>Save</button>
        </div>
        {console.log(shifts)}
        {shifts.length > 0 && (
          <ReactGrid columns={DutyMasterColumn} RowData={shifts} />
        )}
        <ToastAlert Message={toast.message} Type={toast.type} />
      </div>
    </>
  );
}

export default DutyRoster;



