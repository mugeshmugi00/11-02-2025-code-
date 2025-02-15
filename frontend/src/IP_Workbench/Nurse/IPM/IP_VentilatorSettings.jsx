import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import ReactGrid from "../../../OtherComponent/ReactGrid/ReactGrid";
import axios from "axios";
import ToastAlert from "../../../OtherComponent/ToastContainer/ToastAlert";
import { IconButton } from "@mui/material";
import VisibilityIcon from "@mui/icons-material/Visibility";

const IP_VentilatorSettings = () => {
  const dispatch = useDispatch();
  const UrlLink = useSelector((state) => state.userRecord?.UrlLink);
  const toast = useSelector((state) => state.userRecord?.toast);
  const IP_DoctorWorkbenchNavigation = useSelector(
    (state) => state.Frontoffice?.IP_DoctorWorkbenchNavigation
  );
  console.log(IP_DoctorWorkbenchNavigation, "IP_DoctorWorkbenchNavigation");

  const userRecord = useSelector((state) => state.userRecord?.UserData);

  const formatLabel = (label) => {
    if (/[a-z]/.test(label) && /[A-Z]/.test(label) && !/\d/.test(label)) {
      return label
        .replace(/([a-z])([A-Z])/g, "$1 $2")
        .replace(/^./, (str) => str.toUpperCase());
    } else {
      return label;
    }
  };

  const [Ventilator, setVentilator] = useState({
    Mode: "",
    BreathsPerMin: "",
    PressSupport: "",
    PeakPress: "",
    Peep: "",
    MeanPress: "",
    MV: "",
    ITV: "",
    ETV: "",
    F2O2: "",
    VentilatorAssociatedPneumonia: "",
    Status: "",
    Remarks: "",
  });

  const [gridData, setGridData] = useState([]);
  const [IsGetData, setIsGetData] = useState(false);

  const [IsViewMode, setIsViewMode] = useState(false);

  const VentilatorColumns = [
    {
      key: "id",
      name: "S.No",
      frozen: true,
    },
    { key: "PrimaryDoctorName", name: "Doctor Name", frozen: true },

    {
      key: "CurrDate",
      name: "Date",
      frozen: true,
    },
    {
      key: "CurrTime",
      name: "Time",
      frozen: true,
    },

    {
      key: "view",
      frozen: true,
      name: "View",
      renderCell: (params) => (
        <IconButton onClick={() => handleView(params.row)}>
          <VisibilityIcon />
        </IconButton>
      ),
    },

    // { key: 'Mode', name: 'Mode'},
    // { key: 'BreathsPerMin', name: 'Breaths PerMin'},
    // { key: 'PressSupport', name: 'Press Support'},
    // { key: 'PeakPress', name: 'Peak Press'},
    // { key: 'Peep', name: 'Peep'},
    // { key: 'MeanPress', name: 'Mean Press'},
    // { key: 'Mv', name: 'Mv'},
    // { key: 'Itv', name: 'Itv'},
    // { key: 'Etv', name: 'Etv'},
    // { key: 'F2o2', name: 'F2o2'},
    // { key: 'VentilatorAssociatedPneumonia', name: 'Ventilator Associated Pneumonia'},
    // { key: 'Status', name: 'Status'},
    // { key: 'Remarks', name: 'Remarks'},
  ];

  // Handle setting the form data when viewing
  const handleView = (data) => {
    setVentilator({
      Mode: data.Mode || "",
      BreathsPerMin: data.BreathsPerMin || "",
      PressSupport: data.PressSupport || "",
      PeakPress: data.PeakPress || "",
      Peep: data.Peep || "",
      MeanPress: data.MeanPress || "",
      MV: data.Mv || "",
      ITV: data.Itv || "",
      ETV: data.Etv || "",
      F2O2: data.F2o2 || "",
      Status: data.Status || "",
      Remarks: data.Remarks || "",
      VentilatorAssociatedPneumonia: data.VentilatorAssociatedPneumonia || "",
    });
    setIsViewMode(true);
  };

  // Handle clearing the form and resetting the view mode
  const handleClear = () => {
    setVentilator({
      Mode: "",
      BreathsPerMin: "",
      PressSupport: "",
      PeakPress: "",
      Peep: "",
      MeanPress: "",
      MV: "",
      ITV: "",
      ETV: "",
      F2O2: "",
      Status: "",
      Remarks: "",
      VentilatorAssociatedPneumonia: "",
    });
    setIsViewMode(false);
  };

  useEffect(() => {
    const RegistrationId = IP_DoctorWorkbenchNavigation?.RegistrationId;
    const departmentType = IP_DoctorWorkbenchNavigation?.RequestType;

    if (RegistrationId) {
      axios
        .get(`${UrlLink}Ip_Workbench/IP_Ventilator_Details_Link`, {
          params: {
            RegistrationId: RegistrationId,
            DepartmentType: departmentType,
          },
        })
        .then((res) => {
          const ress = res.data;
          console.log(ress);
          setGridData(ress);
        })
        .catch((err) => {
          console.log(err);
        });
    }
  }, [UrlLink, IP_DoctorWorkbenchNavigation, IsGetData]);

  const HandleOnChange = (e) => {
    const { name, value } = e.target;
    const formattedValue = value.trim();
    setVentilator((prevFormData) => ({
      ...prevFormData,
      [name]: formattedValue,
    }));

      // Adjust height for textarea elements
  if (e.target.name === 'Remarks') {
    adjustHeight(e);
  }
  };

  const handleSubmit = () => {
    const RegistrationId = IP_DoctorWorkbenchNavigation?.RegistrationId;
    const DepartmentType = IP_DoctorWorkbenchNavigation?.RequestType;

    if (!RegistrationId) {
      dispatch({
        type: "toast",
        value: { message: "Registration ID is missing", type: "error" },
      });
      return;
    }
    console.log(IP_DoctorWorkbenchNavigation?.RegistrationId);

    const senddata = {
      ...Ventilator,
      RegistrationId,
      Createdby: userRecord?.username,
      DepartmentType,
    };

    console.log(senddata, "senddata");

    axios
      .post(`${UrlLink}Ip_Workbench/IP_Ventilator_Details_Link`, senddata)
      .then((res) => {
        const [type, message] = [
          Object.keys(res.data)[0],
          Object.values(res.data)[0],
        ];
        dispatch({ type: "toast", value: { message, type } });
        setIsGetData((prev) => !prev);
        handleClear();
      })
      .catch((err) => console.log(err));
  };


  const adjustHeight = (e) => {
    e.target.style.height = "auto"; // Reset height to calculate scrollHeight
    e.target.style.height = `${e.target.scrollHeight}px`; // Set height to scrollHeight
  };



  return (
    <>
      <div className="RegisFormcon_1">
        <div className="common_center_tag">
          <span>Ventilator Settings</span>
        </div>

        <div className="RegisFormcon" style={{justifyContent:'flex-start'}}>
        <div className="RegisForm_1">
              <label>
              Ventilator Type<span>:</span>
              </label>
              <select type="date">
                <option>Select</option>
              </select>
            </div>
</div>

        <div className="dhgwhgdw_i9">
          <div className="RegisFormcon" style={{justifyContent:'flex-start'}}>
            <div className="RegisForm_1">
              <label>
                Incubation Date<span>:</span>
              </label>
              <input type="date"></input>
            </div>

            <div className="RegisForm_1">
              <label>
                Incubation Time<span>:</span>
              </label>
              <input type="time"></input>
            </div>


          </div>




  <div className="RegisFormcon" style={{justifyContent:'flex-end'}}>
            <div className="RegisForm_1">
              <label>
              Excubation Date<span>:</span>
              </label>
              <input type="date"></input>
            </div>

            <div className="RegisForm_1">
              <label>
              Excubation Time<span>:</span>
              </label>
              <input type="time"></input>
            </div>

            
          </div>        </div>
          <br />
          {/* <br /> */}


          <div className="RegisFormcon">
  {/* Render the form fields excluding the "Remarks" field */}
  {Object.keys(Ventilator).map((p, index) => (
    p !== "Remarks" && (
      <div className="RegisForm_1" key={p}>
        <label htmlFor={`${p}_${index}`}>
          {p === "MV" ? (
            "MV (L/min)"
          ) : p === "ITV" ? (
            "ITV (ml)"
          ) : p === "ETV" ? (
            "ETV (ml)"
          ) : p === "PressSupport" ? (
            <label>PRESS Support (cmH2O)</label>
          ) : p === "F2O2" ? (
            <label> F2O2</label>
          ) : p === "PeakPress" ? (
            <label>Peak PRESS (cmH2O)</label>
          ) : p === "Peep" ? (
            <label>PEEP (cmH2O)</label>
          ) : p === "MeanPress" ? (
            <label>Mean PRESS (cmH2O)</label>
          ) : (
            formatLabel(p)
          )}
          <span>:</span>
        </label>
        {p === "Mode" ? (
          <select
            id={`${p}_${index}`}
            name={p}
            value={Ventilator[p]}
            onChange={HandleOnChange}
            readOnly={IsViewMode}
            disabled={IsViewMode}
          >
            <option value="">Select</option>
            <option value="VAC">VAC</option>
            <option value="PAV">PAV</option>
            <option value="PSV">PSV</option>
            <option value="SIMV">SIMV</option>
          </select>
        ) : p === "VentilatorAssociatedPneumonia" ? (
          <select
            id={`${p}_${index}`}
            name={p}
            value={Ventilator[p]}
            onChange={HandleOnChange}
            readOnly={IsViewMode}
            disabled={IsViewMode}
          >
            <option value="">Select</option>
            <option value="Yes">Yes</option>
            <option value="No">No</option>
          </select>
        ) : p === "Status" ? (
          <select
            id={`${p}_${index}`}
            name={p}
            value={Ventilator[p]}
            onChange={HandleOnChange}
            readOnly={IsViewMode}
            disabled={IsViewMode}
          >
            <option value="">Select</option>
            <option value="PatientReintubated">Patient Reintubated</option>
            <option value="PatientExtubated">Patient Extubated</option>
            <option value="Dead">Dead</option>
          </select>
        ) : (
          <input
            id={`${p}_${index}`}
            autoComplete="off"
            type={p === "Date" ? "date" : p === "Time" ? "time" : "number"}
            name={p}
            value={Ventilator[p]}
            onChange={HandleOnChange}
            readOnly={IsViewMode}
          />
        )}
      </div>
    )
  ))}
</div>





 <div className="RegisFormcon extend_textarea_new">
 <div className="RegisForm_1 extend_textarea_new"

 >
    <label htmlFor="Remarks">Remarks <span>:</span></label>
    <textarea
      id="Remarks"
      name="Remarks"
      value={Ventilator.Remarks}
      onChange={(e) => {
        HandleOnChange(e);  
        adjustHeight(e);  
      }}
      readOnly={IsViewMode}
      placeholder="Enter your remarks here"
    />
  </div>
  </div>


      </div>
      <div className="Main_container_Btn">
        {IsViewMode && <button onClick={handleClear}>Clear</button>}
        {!IsViewMode && <button onClick={handleSubmit}>Submit</button>}
      </div>

      {gridData.length >= 0 && (
        <ReactGrid columns={VentilatorColumns} RowData={gridData} />
      )}

      <ToastAlert Message={toast.message} Type={toast.type} />
    </>
  );
};

export default IP_VentilatorSettings;
