
import React, { useCallback, useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";

import Button from "@mui/material/Button";
import EditIcon from "@mui/icons-material/Edit";
import VisibilityIcon from "@mui/icons-material/Visibility";
import axios from "axios";
import ModelContainer from "../../OtherComponent/ModelContainer/ModelContainer";
import ToastAlert from "../../OtherComponent/ToastContainer/ToastAlert";
import ReactGrid from "../../OtherComponent/ReactGrid/ReactGrid";
import Visibility from '@mui/icons-material/Visibility';

const RatecardMaster = () => {

  const dispatchvalue = useDispatch();
  const navigate = useNavigate();
  const [InsuranceData, setInsuranceData] = useState([]);
  const [DoctorRateCardData, setDoctorRateCardData] = useState([]);
  const [modifiedRows, setModifiedRows] = useState({});
  const [ServiceProcedureForm, setServiceProcedureForm] = useState("Service");
  console.log("ServiceProcedureForm", ServiceProcedureForm);
  const [ServiceProcedureColumns, setServiceProcedureColumns] = useState([]);
  const [ServiceProcedureData, setServiceProcedureData] = useState([]);
  const [getChanges, setgetChanges] = useState(false);
  const [loading, setLoading] = useState(false);
  const pagewidth = useSelector((state) => state.userRecord?.pagewidth);
  const UrlLink = useSelector((state) => state.userRecord?.UrlLink);
  const toast = useSelector((state) => state.userRecord?.toast);
  const [SearchQuery, setSearchQuery] = useState({
    Type: "",
    SearchBy: "",
  });
  // Fetch Insurance Data
  useEffect(() => {
    axios.get(`${UrlLink}Masters/Insurance_client_master_details`).then((response) => {
      setInsuranceData(response.data);
    });
  }, [UrlLink]);

  // Fetch Doctor RateCard Data
  useEffect(() => {
    axios.get(`${UrlLink}Masters/Overall_services_link`).then((response) => {
      console.log('1111111', response.data);

      setDoctorRateCardData(response.data);
    });
  }, [UrlLink]);

  // Handler for OP/IP ratecard changes
  const handleRateCardChange = (e, doctorIndex, ratecardIndex, type, field) => {
    const value = e.target.value;
    const newModifiedRows = { ...modifiedRows };

    // Track modified row and field
    if (!newModifiedRows[doctorIndex]) {
      newModifiedRows[doctorIndex] = {};
    }
    newModifiedRows[doctorIndex][`${type}_ratecard_${ratecardIndex}_${field}`] = value;
    setModifiedRows(newModifiedRows);

    // Update original state
    const newData = [...DoctorRateCardData];
    const ratecardDetails = newData[doctorIndex].Ratecarddetails[type];

    // Update the appropriate field (consultation_curr_fee or follow_up_curr_fee) based on the field type
    if (field === 'consultation') {
      ratecardDetails[ratecardIndex].consultation_curr_fee = value;
    } else if (field === 'follow_up') {
      ratecardDetails[ratecardIndex].follow_up_curr_fee = value;
    } else if (field === 'emg') {
      ratecardDetails[ratecardIndex].emg_consultant_curr_fee = value;
    }

    setDoctorRateCardData(newData);
  };

  // Handler for Doctor Contribution changes
  const handleDoctorContributionChange = (e, doctorIndex, contributionIndex, type) => {
    const value = e.target.value;
    const newModifiedRows = { ...modifiedRows };

    // Track modified row and field
    if (!newModifiedRows[doctorIndex]) {
      newModifiedRows[doctorIndex] = {};
    }
    newModifiedRows[doctorIndex][`${type}_contribution_${contributionIndex}`] = value;
    setModifiedRows(newModifiedRows);

    // Update original state
    const newData = [...DoctorRateCardData];
    const contributions = newData[doctorIndex].Contribution;

    // Update the corresponding contribution field (OP or IP)
    if (type === "OP") {
      contributions[contributionIndex].doctor_contribution_OP = value;
    } else if (type === "IP") {
      contributions[contributionIndex].doctor_contribution_IP = value;
    }

    setDoctorRateCardData(newData);
  };

  // Generic handler for Insurance, Client, and Corporate changes
  const handleFieldChange = (e, doctorIndex, section, fieldIndex) => {
    const value = e.target.value;
    const newModifiedRows = { ...modifiedRows };

    // Track modified row and field
    if (!newModifiedRows[doctorIndex]) {
      newModifiedRows[doctorIndex] = {};
    }
    newModifiedRows[doctorIndex][`${section}_${fieldIndex}`] = value;
    setModifiedRows(newModifiedRows);

    // Update original state
    const newData = [...DoctorRateCardData];
    const sectionData = newData[doctorIndex][section];

    // Update the corresponding field (consultation_curr_fee or follow_up_curr_fee) based on section
    sectionData[fieldIndex].consultation_curr_fee = value;

    setDoctorRateCardData(newData);
  };


  // Submit only modified rows
  const handleSubmit = async () => {
    try {
      const payload = Object.keys(modifiedRows).map((doctorIndex) => {
        const updates = modifiedRows[doctorIndex];
        const doctor = DoctorRateCardData[doctorIndex];
        const updatedDoctor = { doctor_id: doctor.id };

        // Update Ratecarddetails
        updatedDoctor.Ratecarddetails = {
          OP: doctor.Ratecarddetails.OP.map((ratecard, ratecardIndex) => ({
            RatecardType: ratecard.RatecardType,
            consultation_curr_fee: updates[`OP_ratecard_${ratecardIndex}`] || ratecard.consultation_curr_fee,
            follow_up_curr_fee: updates[`OP_followup_${ratecardIndex}`] || ratecard.follow_up_curr_fee,
            emg_consultant_curr_fee: updates[`OP_emg_${ratecardIndex}`] || ratecard.emg_consultant_curr_fee,
          })),
          IP: doctor.Ratecarddetails.IP.map((ratecard, ratecardIndex) => ({
            RatecardType: ratecard.RatecardType,
            consultation_curr_fee: updates[`IP_ratecard_${ratecardIndex}`] || ratecard.consultation_curr_fee,
            follow_up_curr_fee: updates[`IP_followup_${ratecardIndex}`] || ratecard.follow_up_curr_fee,
            emg_consultant_curr_fee: updates[`IP_emg_${ratecardIndex}`] || ratecard.emg_consultant_curr_fee,
          })),
        };

        // Update Contribution
        updatedDoctor.Contribution = {};

        if (doctor.Contribution[0]?.doctor_contribution_OP) {
          updatedDoctor.Contribution.doctor_contribution_OP = updates[`OP_contribution_0`] || doctor.Contribution[0].doctor_contribution_OP;
        }

        if (doctor.Contribution[1]?.doctor_contribution_IP) {
          updatedDoctor.Contribution.doctor_contribution_IP = updates[`IP_contribution_1`] || doctor.Contribution[1].doctor_contribution_IP;
        }

        // Update InsuranceDetails, ClientDetails, CorporateDetails
        ["InsuranceDetails", "ClientDetails", "CorporateDetails"].forEach((section) => {
          updatedDoctor[section] = doctor[section].map((item, index) => ({
            RatecardName: item.RatecardName,
            consultation_curr_fee: updates[`${section}_${index}`] || item.consultation_curr_fee,
            follow_up_curr_fee: updates[`${section}_followup_${index}`] || item.follow_up_curr_fee,
            emg_consultant_curr_fee: updates[`${section}_emg_${index}`] || item.emg_consultant_curr_fee,
          }));
        });

        return updatedDoctor;
      });

      console.log("Payload:", payload);

      const response = await axios.post(`${UrlLink}Masters/UpdateRatecardDetails`, payload);
      const resData = response.data;
      const mess = Object.values(resData)[0];
      const typp = Object.keys(resData)[0];
      console.log("submit data:", response.data);
      console.log("submit data:", resData);
      const tdata = {
        message: mess,
        type: typp,
      };

      dispatchvalue({ type: "toast", value: tdata });

      // if (response.status === 200) {
      //   setModifiedRows({});
      //   console.log("Ratecard updated successfully");
      //   dispatchvalue({ type: "SHOW_TOAST", payload: { message: "Ratecard updated successfully!", type: "success" } });
      // } else {
      //   console.error("Failed to update ratecard");
      //   dispatchvalue({ type: "SHOW_TOAST", payload: { message: "Failed to update ratecard.", type: "error" } });
      // }
    } catch (error) {
      console.error("Error while updating ratecard:", error);
      dispatchvalue({ type: "SHOW_TOAST", payload: { message: "Error while updating ratecard.", type: "error" } });
    }
  };


  const handlesearch = (e) => {
    const { name, value } = e.target;
    setSearchQuery((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleselectChange = (e) => {
    const { value } = e.target;
    setLoading(true);
    setTimeout(() => {
      setServiceProcedureForm(value);
      setSearchQuery({
        Type: "",
        SearchBy: "",
      });
      setLoading(false);
    }, 200);
  };



  const handleeditstatus = useCallback(
    (params) => {
      const data = {
        MasterType: ServiceProcedureForm,
        id: params.id,
      };
      axios
        .post(
          `${UrlLink}Masters/update_status_Service_Procedure_Detials_link`,
          data
        )
        .then((res) => {
          const resres = res.data;
          let typp = Object.keys(resres)[0];
          let mess = Object.values(resres)[0];
          const tdata = {
            message: mess,
            type: typp,
          };

          dispatchvalue({ type: "toast", value: tdata });
          setgetChanges((prev) => !prev);
        })
        .catch((err) => {
          console.log(err);
        });
    },
    [ServiceProcedureForm, UrlLink, dispatchvalue]
  );


  const handleRatecardview = useCallback(
    (params) => {
      const data = {
        MasterType: ServiceProcedureForm,
        id: params.id,
      };
      dispatchvalue({ type: "ServiceProcedureRatecardView", value: data });

      navigate("/Home/Master");
      dispatchvalue({ type: 'HrFolder', value:'ServiceProcedureRatecard'});
      dispatchvalue({ type: "setPreviousFolder", value: null }); 
      dispatchvalue({ type: "showMenu", value: true });



    },
    [ServiceProcedureForm, dispatchvalue, navigate]
  );
  useEffect(() => {
    const commonColumns = [
      { key: "IsGst", name: "IsGst" },
      { key: "GSTValue", name: "GSTValue" },
      {
        key: "Status",
        name: "Status",
        frozen: pagewidth > 1000 ? true : false,
        renderCell: (params) => (
          <Button
            className="cell_btn"
            onClick={() => handleeditstatus(params.row)}
          >
            {params.row.Status}
          </Button>
        ),
      },
      {
        key: "RatecardView",
        name: "Ratecard View",
        renderCell: (params) => (
          <Button
            className="cell_btn"
            onClick={() => handleRatecardview(params.row)}
          >
            <VisibilityIcon />
          </Button>
        ),
      },

    ];

    const ServiceColumns = [
      {
        key: "id",
        name: "Service ID",
        frozen: pagewidth > 500 ? true : false,
      },
      {
        key: "ServiceName",
        name: "Service Name",
        frozen: pagewidth > 700 ? true : false,
      },
      { key: "ServiceType", name: "Service Type" },
      { key: "Department", name: "Department" },
      ...commonColumns,
    ];

    const ProcedureColumns = [
      {
        key: "id",
        name: " Procedure Id",
        frozen: pagewidth > 500 ? true : false,
      },
      {
        key: "ProcedureName",
        name: "Therapy Name",
        frozen: pagewidth > 700 ? true : false,
      },
      { key: "Type", name: "Procedure Type" },
      ...commonColumns,
    ];

    setServiceProcedureColumns(
      ServiceProcedureForm === "Service" ? ServiceColumns : ProcedureColumns
    );
  }, [
    ServiceProcedureForm,
    pagewidth,
    handleeditstatus,
    handleRatecardview,
  ]);

  useEffect(() => {
    const fetchdata = async () => {
      try {
        const data = {
          MasterType: ServiceProcedureForm,
          ...SearchQuery,
        };
        const [filteredRows] = await Promise.all([
          axios.get(`${UrlLink}Masters/Service_Procedure_Master_Detials_link`, {
            params: data,
          }),
        ]);
        setServiceProcedureData(filteredRows.data);
        // setMastertypedata(Mastertypedata.data)
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchdata();
  }, [UrlLink, getChanges, ServiceProcedureForm, SearchQuery]);
  // ----------------doctormaster
  const [UserRegisterData, setUserRegisterData] = useState([])
  const [GetUserRegisterData, setGetUserRegisterData] = useState(false)
  const [UserRegisterFIlteredData, setUserRegisterFIlteredData] = useState([])
  const [SearchQuery1, setSearchQuery1] = useState('')

  useEffect(() => {
    axios.get(`${UrlLink}Masters/get_Doctor_Detials_link`)
      .then((res) => {
        const ress = res.data
        if (Array.isArray(ress)) {
          setUserRegisterData(ress)
        } else {
          setUserRegisterData([])
        }

      })
      .catch((err) => {
        console.log(err);
      })
    dispatchvalue({ type: 'DoctorListId', value: {} })
  }, [UrlLink, GetUserRegisterData, dispatchvalue])


  useEffect(() => {

    const lowercasesearch = SearchQuery1.toLowerCase()
    const filteralldata = UserRegisterData.filter((row) => {
      const LowerName = row.Name.toLowerCase()
      const Mobile = row.ContactNumber.toString()
      const Docdtype = row.DoctorType.toLowerCase()

      return (
        LowerName.includes(lowercasesearch) ||
        Mobile.includes(lowercasesearch) ||
        Docdtype.includes(lowercasesearch)

      )

    })

    setUserRegisterFIlteredData(filteralldata)

  }, [SearchQuery1, UserRegisterData])


  const handleeditDoctorstatus = (params) => {
    const data = { DoctorId: params.id }
    axios.post(`${UrlLink}Masters/update_status_Doctor_Detials_link`, data)
      .then((res) => {
        const resres = res.data
        let typp = Object.keys(resres)[0]
        let mess = Object.values(resres)[0]
        const tdata = {
          message: mess,
          type: typp,
        }

        dispatchvalue({ type: 'toast', value: tdata });
        setGetUserRegisterData(prev => !prev)
      })
      .catch((err) => {
        console.log(err);
      })

  }
  const HandleRateCardView = (params) => {

    const { id } = params
    dispatchvalue({ type: 'DoctorListId', value: { DoctorId: id } })
    navigate('/Home/DoctorRatecardList')
  }

  const UserRegisterColumns = [
    {
      key: "id",
      name: "Doctor Id",
      filter: true,
      type: 'input-text',
      frozen: true,
      width: 300
    },
    {
      key: "ShortName",
      name: "Doctor Name",
      filter: true,
      frozen: true
    },
    {
      key: "ContactNumber",
      name: "Contact Number",
      frozen: true
    },
    {
      key: "DoctorType",
      name: "Doctor Type",
      frozen: true
    },
    {
      key: "Status",
      name: "Status",
      frozen: true,
      renderCell: (params) => (

        <Button
          className="cell_btn"
          onClick={() => handleeditDoctorstatus(params.row)}
        >
          {params.row.Status}
        </Button>
      )

    },
    {
      key: "Email",
      name: "Email",

    },


    {
      key: "Qualification",
      name: "Qualification",
    },
    {
      key: "Department",
      name: "Department",
    },
    {
      key: "Designation",
      name: "Designation",
    },
    {
      key: "Specialization",
      name: "Specialization",
    },
    {
      key: "Category",
      name: "Category",
    },
    {
      key: "createdBy",
      name: "created By",
    },



    {
      key: "RatecardAction",
      name: "Rate Card View",
      renderCell: (params) => (
        <>{
          params.row.DoctorType === 'Referral' ?
            (
              <>
                No Ratecard
              </>
            )
            :
            (
              <Button
                className="cell_btn"
                onClick={() => HandleRateCardView(params.row)}
              >
                <Visibility className="check_box_clrr_cancell" />
              </Button>
            )

        }

        </>
      ),
    },

  ]


  // RoomMasterService

  const [floorData, setFloorData] = useState([]);
  const [doctorRateCardColumns, setDoctorRateCardColumns] = useState([]);
  const [editing, setEditing] = useState(null);
  const [getChangess, setGetChangess] = useState(false);

  // useEffect(() => {
  //         axios
  //             .get(`${UrlLink}Masters/floor_ward_ratecard_view_by_doctor_id?DoctorId=${DoctorListId.DoctorId}`)
  //             .then((res) => {
  //                 const { FloorWardDetails } = res.data;
  //                 setFloorData(Array.isArray(FloorWardDetails) ? FloorWardDetails : []);
  //             })
  //             .catch((err) => console.error(err));
  // }, [UrlLink, navigate, getChanges]);

  const handleChange = useCallback((e, rowIdx, column) => {
    const updatedRow = floorData.map((row, index) =>
      index === rowIdx ? { ...row, [column]: e.target.value } : row
    );
    setFloorData(updatedRow);
  }, [floorData]);

  const handleDoubleClick = useCallback((rowIdx, column) => {
    setEditing({ rowIdx, column });
  }, []);

  const handleSaveChanges = useCallback((row, column) => {
    const editData = {
      // doctor_id: DoctorListId?.DoctorId,
      floor_id: row.FloorId,
      ward_id: row.WardId,
      updated_rate: row[column],
      column: column,
    };

    const confirmChange = window.confirm("Do you want to save the changes?");
    if (confirmChange) {
      axios.post(`${UrlLink}Masters/floor_ward_ratecard_update`, editData)
        .then((res) => {
          const tdata = {
            message: res.data.message || "Rate updated successfully",
            type: res.data.status || "success",
          };
          dispatchvalue({ type: 'toast', value: tdata });
        })
        .catch((err) => console.error(err));
      setGetChangess((prev) => !prev);
    }
    setEditing(null);
  }, [UrlLink, dispatchvalue]);

  const handleKeyDown = useCallback((e, row, column) => {
    if (e.key === 'Enter') {
      handleSaveChanges(row, column);
    } else if (['e', 'E', '+', '-'].includes(e.key)) {
      e.preventDefault();
    }
  }, [handleSaveChanges]);

  useEffect(() => {
    const columns = [
      { key: "FloorName", name: "Floor Name", frozen: true },
      { key: "WardName", name: "Ward Name", frozen: true },
      { key: "PrevRate", name: "Previous Rate" },
      {
        key: "CurrentRate",
        name: "Current Rate",
        editable: true,
        renderCell: (params) => (
          editing && editing.rowIdx === params.rowIndex && editing.column === 'CurrentRate' ? (
            <input
              type="number"
              className="ratecard_inputs"
              autoFocus
              onKeyDown={(e) => handleKeyDown(e, params.row, 'CurrentRate')}
              value={params.row.CurrentRate || ''}
              onChange={(e) => handleChange(e, params.rowIndex, 'CurrentRate')}
            />
          ) : (
            <div onDoubleClick={() => handleDoubleClick(params.rowIndex, 'CurrentRate')}>
              {params.row.CurrentRate || ''}
            </div>
          )
        ),
      },
    ];

    setDoctorRateCardColumns(columns);
  }, [editing, handleKeyDown, handleChange, handleDoubleClick]);


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
    axios.get(`${UrlLink}Masters/Location_Detials_link`)
      .then((res) => {
        const ress = res.data
        setLocationData(ress)
      })
      .catch((err) => {
        console.log(err);
      })
  }, [UrlLink])





  // room name ------------
  const userRecord = useSelector((state) => state.userRecord?.UserData);
  const [LocationData, setLocationData] = useState([]);
  const [IsBuildingGet, setIsBuildingGet] = useState(false)



  const [RoomName, setRoomName] = useState({

    Location: '',
    BuildingName: '',
    BlockName: '',
    FloorName: '',
    WardName: '',
    RoomId: '',
  })
  const [RoomData, setRoomData] = useState([])
  const [Room_Building_by__loc, setRoom_Building_by__loc] = useState([])
  const [Room_block_by_Building, setRoom_block_by_Building] = useState([])
  const [Room_Floor_by_Block, setRoom_Floor_by_Block] = useState([])
  const [Room_ward_by_FLoor, setRoom_ward_by_FLoor] = useState([])
  useEffect(() => {
    if (RoomName.Location) {
      axios.get(`${UrlLink}Masters/get_building_Data_by_location?Location=${RoomName.Location}`)
        .then(res => {
          if (Array.isArray(res.data)) {
            setRoom_Building_by__loc(res.data)
          } else {
            setRoom_Building_by__loc([])
          }

        })
        .catch(err => {
          setRoom_Building_by__loc([])
          console.log(err);
        })
    }

  }, [RoomName.Location, UrlLink])

  useEffect(() => {
    if (RoomName.BuildingName) {
      const data = {
        Building: RoomName.BuildingName,
      }
      axios.get(`${UrlLink}Masters/get_block_Data_by_Building`, { params: data })
        .then(res => {
          if (Array.isArray(res.data)) {
            setRoom_block_by_Building(res.data)
          } else {
            setRoom_block_by_Building([])
          }
        })
        .catch(err => {
          setRoom_block_by_Building([])
          console.log(err);
        })
    }

  }, [RoomName.BuildingName, UrlLink])

  useEffect(() => {
    if (RoomName.BlockName) {
      const data = {
        Block: RoomName.BlockName,
      }
      axios.get(`${UrlLink}Masters/get_Floor_Data_by_Building_block_loc`, { params: data })
        .then(res => {
          if (Array.isArray(res.data)) {
            setRoom_Floor_by_Block(res.data)
          } else {
            setRoom_Floor_by_Block([])
          }

        })
        .catch(err => {
          setRoom_Floor_by_Block([])
          console.log(err);
        })
    }

  }, [RoomName.BlockName, UrlLink])

  useEffect(() => {
    if (RoomName.FloorName) {
      const data = {
        Floor: RoomName.FloorName,
      }
      axios.get(`${UrlLink}Masters/get_Ward_Data_by_Building_block_Floor_loc`, { params: data })
        .then(res => {
          if (Array.isArray(res.data)) {
            setRoom_ward_by_FLoor(res.data)
          } else {
            setRoom_ward_by_FLoor([])
          }

        })
        .catch(err => {
          setRoom_ward_by_FLoor([])
          console.log(err);
        })
    }

  }, [RoomName.FloorName, UrlLink])


  const handlechangeRoom = (e) => {
    const { name, value } = e.target
    if (name === 'Location') {
      setRoomName((prev) => ({
        ...prev,
        [name]: value,
        BuildingName: '',
        BlockName: '',
        FloorName: '',
        WardName: '',
      }))
    } else if (name === 'BuildingName') {
      setRoomName((prev) => ({
        ...prev,
        [name]: value,
        BlockName: '',
        FloorName: '',
        WardName: '',
      }))
    } else if (name === 'BlockName') {
      setRoomName((prev) => ({
        ...prev,
        [name]: value,
        FloorName: '',
        WardName: '',
      }))
    } else if (name === 'FloorName') {
      setRoomName((prev) => ({
        ...prev,
        [name]: value,
        WardName: '',
      }))
    } else if (name === 'WardName') {
      setRoomName((prev) => ({
        ...prev,
        [name]: value,
      }))
    } else {
      setRoomName((prev) => ({
        ...prev,
        [name]: value.toUpperCase(),
        GST: ''
      }))

    }
  }

  const HandleEditRoomStatus = (params) => {
    const data = {
      RoomId: params.id,
      Statusedit: true
    }
    const confirmation = window.confirm('Are you sure you want to update the status? All the children room and bed statuses will be changed.');
    if (confirmation) {
      axios.post(`${UrlLink}Masters/Room_Master_Detials_link`, data)
        .then((res) => {
          const resres = res.data
          let typp = Object.keys(resres)[0]
          let mess = Object.values(resres)[0]
          const tdata = {
            message: mess,
            type: typp,
          }

          dispatchvalue({ type: 'toast', value: tdata });
          setIsBuildingGet(prev => !prev)
        })
        .catch((err) => {
          console.log(err);
        })
    }
  }
  const HandleEditRoom = (params) => {
    const { id, BuildingId, BlockId, FloorId, Location_Id, WardId, Current_Charge, GST_val } = params
    setRoomName({
      Location: Location_Id,
      BuildingName: BuildingId,
      BlockName: BlockId,
      FloorName: FloorId,
      WardName: WardId,
    })
  }

  const HandleSaveRoom = () => {
    const exist = Object.keys(RoomName).filter(p => p !== 'RoomId').filter((field) => !RoomName[field])
    if (exist.length === 0) {


      const data = {
        ...RoomName,
        created_by: userRecord?.username || ''
      }
      axios.post(`${UrlLink}Masters/Room_Master_Detials_link`, data)
        .then((res) => {
          const resres = res.data
          let typp = Object.keys(resres)[0]
          let mess = Object.values(resres)[0]
          const tdata = {
            message: mess,
            type: typp,
          }

          dispatchvalue({ type: 'toast', value: tdata });
          setIsBuildingGet(prev => !prev)
          setRoomName({
            Location: '',
            BuildingName: '',
            BlockName: '',
            FloorName: '',
            WardName: '',
          })
        })
        .catch((err) => {
          console.log(err);
        })
    } else {
      const tdata = {
        message: `Please provide ${exist.join(' and ')}`,
        type: 'warn'
      }
      dispatchvalue({ type: 'toast', value: tdata });
    }
  }

  useEffect(() => {
    axios.get(`${UrlLink}Masters/Room_Master_Detials_link`)
      .then((res) => {
        const ress = res.data
        setRoomData(ress)
      })
      .catch((err) => {
        console.log(err);
      })
  }, [IsBuildingGet, UrlLink])

  const [Roomdata, setRoomdata] = useState([]);
  // Fetch data from API
  useEffect(() => {
    axios
      .get(`${UrlLink}Masters/Get_RoomDetails_Ratecard`) // Replace with your API URL
      .then((response) => {
        setRoomdata(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
        setLoading(false);
      });
  }, []);

  const handleEdit = (floorIndex, wardIndex, field, subfield, value, type) => {
    const updatedData = [...Roomdata];
    if (type === "insurance") {
      updatedData[floorIndex].Wards[wardIndex].InsuranceDetails[subfield].Fee = value;
    } else {
      updatedData[floorIndex].Wards[wardIndex].Ratecarddetails[field][subfield].consultation_curr_fee = value;
    }
    setRoomdata(updatedData);
  };

  const renderTableRows = () => {
    return Roomdata.map((floor, floorIndex) =>
      floor.Wards.map((ward, wardIndex) => (
        <tr key={`${floorIndex}-${wardIndex}`}>
          <td>{wardIndex + 1}</td>
          <td>RoomCharges</td>
          <td>{floor.FloorName}</td>
          <td>{ward.WardName}</td>
          <td>{ward.CategoryType ? "AC" : "Non-AC"}</td>
          <td>
            {ward.Ratecarddetails.General.map((item, index) => (
              <div key={index}>
                <input
                  type="text"
                  value={item.consultation_curr_fee}
                  onChange={(e) =>
                    handleEdit(floorIndex, wardIndex, "General", index, e.target.value)
                  }
                />
              </div>
            ))}
          </td>
          <td>
            {ward.Ratecarddetails.Special.map((item, index) => (
              <div key={index}>
                <input
                  type="text"
                  value={item.consultation_curr_fee}
                  onChange={(e) =>
                    handleEdit(floorIndex, wardIndex, "Special", index, e.target.value)
                  }
                />
              </div>
            ))}
          </td>
          <td>
            {ward.InsuranceDetails.map((ins, index) => (
              <div key={index}>
                <input
                  type="text"
                  value={ins.Fee}
                  onChange={(e) =>
                    handleEdit(floorIndex, wardIndex, null, index, e.target.value, "insurance")
                  }
                />
              </div>
            ))}
          </td>
          <td>
            {ward.ClientDetails.length > 0
              ? ward.ClientDetails.map((client, index) => (
                <div key={index}>
                  <input
                    type="text"
                    value={client.Fee || ""}
                    onChange={(e) =>
                      handleEdit(floorIndex, wardIndex, null, index, e.target.value, "client")
                    }
                  />
                </div>
              ))
              : "-"}
          </td>
          <td>
            {ward.CorporateDetails.length > 0
              ? ward.CorporateDetails.map((corp, index) => (
                <div key={index}>
                  <input
                    type="text"
                    value={corp.Fee || ""}
                    onChange={(e) =>
                      handleEdit(floorIndex, wardIndex, null, index, e.target.value, "corporate")
                    }
                  />
                </div>
              ))
              : "-"}
          </td>
        </tr>
      ))
    );
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  const Room = Roomdata?.flatMap((floor) =>
    floor.Wards?.flatMap((ward) => ward.Ratecarddetails?.General.map((ratecard, index) => ({
      ratecardType: ratecard.RatecardType,
    }))
    )
  );

  console.log("Room Data:", Room);

  return (
    <div className="Main_container_app">
      <h3>RateCard Master</h3>

      <div className="RegisterTypecon">
        <div className="RegisterType">
          {["Service", "Procedure", "DoctorRateCard", "Room/Ward_Service",].map((p, ind) => (
            <div className="registertypeval" key={ind + "key"}>
              <input
                type="radio"
                id={p}
                name="appointment_type"
                checked={ServiceProcedureForm === p}
                onChange={handleselectChange}
                value={p}
              />
              <label htmlFor={p}>{p === "Procedure" ? "Therapy" : p}</label>
            </div>
          ))}
        </div>
      </div>
      <br />
      <div className="search_div_bar">
        {ServiceProcedureForm !== "DoctorRateCard" && ServiceProcedureForm !== "Room/Ward_Service" && (
          <div className=" search_div_bar_inp_1">
            <label htmlFor="">
              {ServiceProcedureForm} Type
              <span>:</span>
            </label>
            <select
              name="Type"
              value={SearchQuery.Type}
              onChange={handlesearch}
            >
              <option value="">Select</option>
              {ServiceProcedureForm === "Service" &&
                ["OP", "IP", "Both"].map((val, ind) => (
                  <option key={ind} value={val}>
                    {val === "Both" ? "both IP and OP" : val}
                  </option>
                ))}
              {ServiceProcedureForm === "Procedure" &&
                ["Interventional", "Diagnostic"].map((val, ind) => (
                  <option key={ind} value={val}>
                    {val}
                  </option>
                ))}
            </select>
          </div>
        )}
        {ServiceProcedureForm !== "DoctorRateCard" && ServiceProcedureForm !== "Room/Ward_Service" && (
          <div className="search_div_bar_inp_1">
            <label htmlFor="">
              Search Here
              <span>:</span>
            </label>
            <input
              type="text"
              name="SearchBy"
              value={SearchQuery.SearchBy}
              placeholder={`By ${ServiceProcedureForm} ...`}
              onChange={handlesearch}
            />
          </div>
        )}


      </div>

      <br />
      {ServiceProcedureForm !== "DoctorRateCard" && ServiceProcedureForm !== "Room/Ward_Service" && (
        <ReactGrid
          columns={ServiceProcedureColumns}
          RowData={ServiceProcedureData}
        />
      )}

      {ServiceProcedureForm === 'DoctorRateCard' && (
        <>
           <div className="Selected-table-container">
                                <table className="selected-medicine-table2">
              <thead>
                <tr>
                  <th rowSpan="2">S.No</th>
                  <th rowSpan="2">Service</th>
                  <th rowSpan="2">Doctor Name</th>
                  <th rowSpan="2">Specialization</th>

                  {/* Main OP and IP Headers */}
                  <th className="text_aln_th_center" colSpan={DoctorRateCardData[0]?.Ratecarddetails?.OP.length * 2}>OP</th>
                  <th className="text_aln_th_center"  colSpan={DoctorRateCardData[0]?.Ratecarddetails?.IP.length * 2}>IP</th>

                  {/* Doctor Contribution (OP and IP) */}
                  <th className="text_aln_th_center" colSpan="2">Doctor Contribution</th>

                  {/* Insurance Columns */}
                  {DoctorRateCardData[0]?.InsuranceDetails.length > 0 && (
                    <th className="text_aln_th_center" colSpan={DoctorRateCardData[0]?.InsuranceDetails.length}>Insurance</th>
                  )}

                  {/* Client Columns */}
                  {DoctorRateCardData[0]?.ClientDetails.length > 0 && (
                    <th className="text_aln_th_center" colSpan={DoctorRateCardData[0]?.ClientDetails.length}>Client</th>
                  )}

                  {/* Corporate Columns */}
                  {DoctorRateCardData[0]?.CorporateDetails.length > 0 && (
                    <th colSpan={DoctorRateCardData[0]?.CorporateDetails.length}>Corporate</th>
                  )}
                </tr>
                <tr>
                  {/* Generate OP Ratecard Sub-columns (OP - Consultation, Follow-up) */}
                  {DoctorRateCardData[0]?.Ratecarddetails?.OP.map((ratecard, index) => (
                    <>
                      <th key={`op-consultation-${ratecard.RatecardType}-${index}`}>{ratecard.RatecardType} - Consultation</th>
                      <th key={`op-followup-${ratecard.RatecardType}-${index}`}>{ratecard.RatecardType} - Follow-up</th>
                    </>
                  ))}


                  {/* Generate IP Ratecard Sub-columns (IP - Consultation, Follow-up) */}
                  {DoctorRateCardData[0]?.Ratecarddetails?.IP.map((ratecard, index) => (
                    <>
                      <th key={`ip-consultation-${ratecard.RatecardType}-${index}`}>{ratecard.RatecardType} - Consultation</th>
                      <th key={`ip-followup-${ratecard.RatecardType}-${index}`}>{ratecard.RatecardType} - Follow-up</th>
                    </>
                  ))}

                  {/* Doctor Contribution Sub-columns (OP and IP %) */}
                  <th>OP(%)</th>
                  <th>IP(%)</th>

                  {/* Insurance Sub-columns */}
                  {DoctorRateCardData[0]?.InsuranceDetails.map((insurance, index) => (
                    <th key={`insurance-${index}`}>{insurance.RatecardName}</th>
                  ))}

                  {/* Client Sub-columns */}
                  {DoctorRateCardData[0]?.ClientDetails.map((client, index) => (
                    <th key={`client-${index}`}>{client.RatecardName}</th>
                  ))}

                  {/* Corporate Sub-columns */}
                  {DoctorRateCardData[0]?.CorporateDetails.map((corporate, index) => (
                    <th key={`corporate-${index}`}>{corporate.RatecardName}</th>
                  ))}
                </tr>
              </thead>

              <tbody>
                {DoctorRateCardData.map((doctor, index) => (
                  <tr key={index}>
                    <td>{index + 1}</td>
                    <td>{doctor.Service}</td>
                    <td>{doctor.doctor_name}</td>
                    <td>{doctor.Specialization}</td>

                    {/* Dynamically render OP Ratecard data */}
                    {doctor.Ratecarddetails?.OP.map((ratecard, ratecardIndex) => (
                      <>
                        <td key={`op-consultation-${ratecardIndex}`}>
                          <input
                            type="number"
                            value={ratecard.consultation_curr_fee}
                            onChange={(e) => handleRateCardChange(e, index, ratecardIndex, "OP", "consultation")}
                          />
                        </td>
                        <td key={`op-followup-${ratecardIndex}`}>
                          <input
                            type="number"
                            value={ratecard.follow_up_curr_fee}
                            onChange={(e) => handleRateCardChange(e, index, ratecardIndex, "OP", "follow_up")}
                          />
                        </td>
                      </>
                    ))}

                    {/* Dynamically render IP Ratecard data */}
                    {doctor.Ratecarddetails?.IP.map((ratecard, ratecardIndex) => (
                      <>
                        <td key={`ip-consultation-${ratecardIndex}`}>
                          <input
                            type="number"
                            value={ratecard.consultation_curr_fee}
                            onChange={(e) => handleRateCardChange(e, index, ratecardIndex, "IP", "consultation")}
                          />
                        </td>
                        <td key={`ip-followup-${ratecardIndex}`}>
                          <input
                            type="number"
                            value={ratecard.follow_up_curr_fee}
                            onChange={(e) => handleRateCardChange(e, index, ratecardIndex, "IP", "follow_up")}
                          />
                        </td>
                      </>
                    ))}

                    {/* Doctor Contribution Inputs */}
                    <td>
                      <input
                        type="number"
                        value={doctor.Contribution[0]?.doctor_contribution_OP}
                        onChange={(e) => handleDoctorContributionChange(e, index, 0, "OP")}
                      />
                    </td>
                    <td>
                      <input
                        type="number"
                        value={doctor.Contribution[1]?.doctor_contribution_IP}
                        onChange={(e) => handleDoctorContributionChange(e, index, 1, "IP")}
                      />
                    </td>

                    {/* Dynamically render Insurance fields */}
                    {doctor.InsuranceDetails.map((insurance, insuranceIndex) => (
                      <td key={`insurance-${insuranceIndex}`}>
                        <input
                          type="number"
                          value={insurance.consultation_curr_fee}
                          onChange={(e) => handleFieldChange(e, index, "InsuranceDetails", insuranceIndex)}
                        />
                      </td>
                    ))}

                    {/* Dynamically render Client fields */}
                    {doctor.ClientDetails.map((client, clientIndex) => (
                      <td key={`client-${clientIndex}`}>
                        <input
                          type="number"
                          value={client.consultation_curr_fee}
                          onChange={(e) => handleFieldChange(e, index, "ClientDetails", clientIndex)}
                        />
                      </td>
                    ))}

                    {/* Dynamically render Corporate fields */}
                    {doctor.CorporateDetails.map((corporate, corporateIndex) => (
                      <td key={`corporate-${corporateIndex}`}>
                        <input
                          type="number"
                          value={corporate.consultation_curr_fee}
                          onChange={(e) => handleFieldChange(e, index, "CorporateDetails", corporateIndex)}
                        />
                      </td>
                    ))}

                  </tr>
                ))}
              </tbody>
            </table>

          </div>
          <br />

          <div className="Register_btn_con">
          <button className="RegisterForm_1_btns" onClick={handleSubmit} >
            Save 
          </button>
          </div>
        </>
      )}
      {ServiceProcedureForm === 'Room/Ward_Service' && (
        <>
          <div className="RegisFormcon_1">
            {Object.keys(RoomName).filter(p => p !== 'RoomId').map((field, indx) => (
              <div className="RegisForm_1" key={indx}>
                <label> {formatLabel(field)} <span>:</span> </label>
                {
                  (field === 'GST' && (parseInt(RoomName.RoomCharge, 0) < 5000 || RoomName.RoomCharge === '')) || field === 'RoomCharge' ?
                    <input
                      type={field === 'RoomCharge' ? 'number' : 'text'}
                      name={field}
                      onKeyDown={(e) => (field === 'RoomCharge') && (['+', '-', 'e', 'E'].includes(e.key) && e.preventDefault())}
                      autoComplete='off'
                      required
                      readOnly={field === 'GST' && (RoomName.RoomCharge ? parseInt(RoomName.RoomCharge, 0) < 5000 : true)}
                      value={RoomName[field]}
                      onChange={handlechangeRoom}
                    />
                    :
                    <select
                      name={field}
                      required
                      disabled={RoomName.RoomId}
                      value={RoomName[field]}
                      onChange={handlechangeRoom}
                    >
                      <option value=''>Select</option>
                      {field === 'BuildingName' &&
                        Room_Building_by__loc.map((p, index) => (
                          <option key={index} value={p.id}>{p.BuildingName}</option>
                        ))
                      }
                      {field === 'BlockName' &&
                        Room_block_by_Building.map((p, index) => (
                          <option key={index} value={p.id}>{p.BlockName}</option>
                        ))
                      }
                      {field === 'FloorName' &&
                        Room_Floor_by_Block.map((p, index) => (
                          <option key={index} value={p.id}>{p.FloorName}</option>
                        ))
                      }
                      {field === 'WardName' &&
                        Room_ward_by_FLoor.map((p, index) => (
                          <option key={index} value={p.id}>{p.WardName}</option>
                        ))
                      }
                      {field === 'Location' &&
                        LocationData.map((p, index) => (
                          <option key={index} value={p.id}>{p.locationName}</option>
                        ))
                      }
                    </select>
                }
              </div>
            ))}
          </div>
          <br />
          <div className="Main_container_Btn">
            <button onClick={HandleSaveRoom}>
              {RoomName.RoomId ? "Update" : "Add"}
            </button>
          </div>
          <br />
          <div className="Selected-table-container">
          <table className="selected-medicine-table2">
              <thead>
                <tr>
                  <th rowSpan="2">S.No</th>
                  <th rowSpan="2">Service</th>
                  <th rowSpan="2">Floor Type</th>
                  <th rowSpan="2">Ward Type</th>
                  <th rowSpan="2">Category Type</th>

                  <th className="text_aln_th_center" colSpan="3">
                    General
                  </th>

                  <th className="text_aln_th_center" colSpan="3">
                    Special
                  </th>

                  {/* Insurance Columns */}
                  {
                    Roomdata?.Wards?.map((ward, wardIndex) => (
                      ward?.InsuranceDetails?.map((insurance, insuranceIndex) => (
                        insurance?.RatecardName && insurance?.RatecardName.length > 0 && (
                          <th key={`insurance-${wardIndex}-${insuranceIndex}`} colSpan={insurance?.RatecardName.length}>
                            Insurance
                          </th>
                        )
                      ))
                    ))
                  }
                  {/* Client Columns */}
                  {DoctorRateCardData[0]?.ClientDetails.length > 0 && (
                    <th className="text_aln_th_center" colSpan={DoctorRateCardData[0]?.ClientDetails.length}>Client</th>
                  )}

                  {/* Corporate Columns */}
                  {DoctorRateCardData[0]?.CorporateDetails.length > 0 && (
                    <th colSpan={DoctorRateCardData[0]?.CorporateDetails.length}>Corporate</th>
                  )}
                </tr>
                <tr>
                  {/* {Roomdata?.flatMap((floor) =>
                    floor.Wards?.flatMap((ward) =>
                      ["General", "Special"]?.flatMap((type) =>
                        (ward.Ratecarddetails?.[type] || []).map((ratecard, index) => (
                          <th key={`${type}-${ratecard.RatecardType}-${index}`}>{ratecard.RatecardType}</th>
                        ))
                      )
                    )
                  )} */}
                  {/* Generate OP Ratecard Sub-columns (OP - Consultation, Follow-up) */}
                  {
                    [...new Set(Roomdata?.flatMap((floor) =>
                      floor.Wards?.flatMap((ward) => ward.Ratecarddetails?.General.map((ratecard) => ratecard.RatecardType))
                    ))].map((ratecardType, index) => (
                      <th key={`charges-${ratecardType}-${index}`}>
                        {ratecardType}
                      </th>
                    ))
                  }
                  {
                    [...new Set(Roomdata?.flatMap((floor) =>
                      floor.Wards?.flatMap((ward) => ward.Ratecarddetails?.Special.map((ratecard) => ratecard.RatecardType))
                    ))].map((ratecardType, index) => (
                      <th key={`charges-${ratecardType}-${index}`}>
                        {ratecardType}
                      </th>
                    ))
                  }
                  {
                    [
                      ...new Set(
                        Roomdata?.flatMap((floor) =>
                          floor.Wards?.flatMap((ward) =>
                            ward?.InsuranceDetails?.map((insurance) => insurance?.RatecardName)
                          )
                        )
                      )
                    ].map((ratecardType, index) => (
                      <th key={`charges-${ratecardType}-${index}`}>
                        {ratecardType}
                      </th>
                    ))
                  }
                  {/* {
                    Roomdata?.flatMap((floor) =>
                      floor.Wards?.flatMap((ward) => ward.InsuranceDetails
                      )).map((ratecardType, index) => (
                        <th key={`charges-${ratecardType.RatecardName}-${index}`}>
                          {ratecardType.RatecardName}
                        </th>
                      ))
                  } */}
                  {/* Generate IP Ratecard Sub-columns (IP - Consultation, Follow-up)
                  {DoctorRateCardData[0]?.Ratecarddetails?.IP.map((ratecard, index) => (
                    <>
                      <th key={`ip-consultation-${ratecard.RatecardType}-${index}`}>{ratecard.RatecardType} - Consultation</th>
                      <th key={`ip-followup-${ratecard.RatecardType}-${index}`}>{ratecard.RatecardType} - Follow-up</th>
                    </>
                  ))} */}

                  {/* Insurance Sub-columns */}
                  {DoctorRateCardData[0]?.InsuranceDetails.map((insurance, index) => (
                    <th key={`insurance-${index}`}>{insurance.RatecardName}</th>
                  ))}

                  {/* Client Sub-columns */}
                  {DoctorRateCardData[0]?.ClientDetails.map((client, index) => (
                    <th key={`client-${index}`}>{client.RatecardName}</th>
                  ))}

                  {/* Corporate Sub-columns */}
                  {DoctorRateCardData[0]?.CorporateDetails.map((corporate, index) => (
                    <th key={`corporate-${index}`}>{corporate.RatecardName}</th>
                  ))}
                </tr>
              </thead>

              <tbody>
                {DoctorRateCardData.map((doctor, index) => (
                  <tr key={index}>
                    <td>{index + 1}</td>
                    <td>{doctor.Service}</td>
                    <td>{doctor.doctor_name}</td>
                    <td>{doctor.Specialization}</td>

                    {/* Dynamically render OP Ratecard data */}
                    {doctor.Ratecarddetails?.OP.map((ratecard, ratecardIndex) => (
                      <>
                        <td key={`op-consultation-${ratecardIndex}`}>
                          <input
                            type="number"
                            value={ratecard.consultation_curr_fee}
                            onChange={(e) => handleRateCardChange(e, index, ratecardIndex, "OP", "consultation")}
                          />
                        </td>
                        <td key={`op-followup-${ratecardIndex}`}>
                          <input
                            type="number"
                            value={ratecard.follow_up_curr_fee}
                            onChange={(e) => handleRateCardChange(e, index, ratecardIndex, "OP", "follow_up")}
                          />
                        </td>
                      </>
                    ))}

                    {/* Dynamically render IP Ratecard data */}
                    {doctor.Ratecarddetails?.IP.map((ratecard, ratecardIndex) => (
                      <>
                        <td key={`ip-consultation-${ratecardIndex}`}>
                          <input
                            type="number"
                            value={ratecard.consultation_curr_fee}
                            onChange={(e) => handleRateCardChange(e, index, ratecardIndex, "IP", "consultation")}
                          />
                        </td>
                        <td key={`ip-followup-${ratecardIndex}`}>
                          <input
                            type="number"
                            value={ratecard.follow_up_curr_fee}
                            onChange={(e) => handleRateCardChange(e, index, ratecardIndex, "IP", "follow_up")}
                          />
                        </td>
                      </>
                    ))}

                    {/* Doctor Contribution Inputs */}
                    <td>
                      <input
                        type="number"
                        value={doctor.Contribution[0]?.doctor_contribution_OP}
                        onChange={(e) => handleDoctorContributionChange(e, index, 0, "OP")}
                      />
                    </td>
                    <td>
                      <input
                        type="number"
                        value={doctor.Contribution[1]?.doctor_contribution_IP}
                        onChange={(e) => handleDoctorContributionChange(e, index, 1, "IP")}
                      />
                    </td>

                    {/* Dynamically render Insurance fields */}
                    {doctor.InsuranceDetails.map((insurance, insuranceIndex) => (
                      <td key={`insurance-${insuranceIndex}`}>
                        <input
                          type="number"
                          value={insurance.consultation_curr_fee}
                          onChange={(e) => handleFieldChange(e, index, "InsuranceDetails", insuranceIndex)}
                        />
                      </td>
                    ))}

                    {/* Dynamically render Client fields */}
                    {doctor.ClientDetails.map((client, clientIndex) => (
                      <td key={`client-${clientIndex}`}>
                        <input
                          type="number"
                          value={client.consultation_curr_fee}
                          onChange={(e) => handleFieldChange(e, index, "ClientDetails", clientIndex)}
                        />
                      </td>
                    ))}

                    {/* Dynamically render Corporate fields */}
                    {doctor.CorporateDetails.map((corporate, corporateIndex) => (
                      <td key={`corporate-${corporateIndex}`}>
                        <input
                          type="number"
                          value={corporate.consultation_curr_fee}
                          onChange={(e) => handleFieldChange(e, index, "CorporateDetails", corporateIndex)}
                        />
                      </td>
                    ))}

                  </tr>
                ))}
              </tbody>
            </table>

          </div>
        </>
      )
      }
      <ModelContainer />
      <ToastAlert Message={toast.message} Type={toast.type} />
    </div>
  );
}
export default RatecardMaster;
