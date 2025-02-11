import React, { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux';
import VisibilityIcon from '@mui/icons-material/Visibility';
import ReactGrid from '../../OtherComponent/ReactGrid/ReactGrid';
import ToastAlert from "../../OtherComponent/ToastContainer/ToastAlert";
import Button from "@mui/material/Button";
import CancelIcon from "@mui/icons-material/Cancel";
import axios from 'axios';
import UpdateIcon from "@mui/icons-material/Update";
import HighlightOffIcon from "@mui/icons-material/HighlightOff";
// import AppointmentCaender from "../AppointmentRequestList/AppointmentCalender.css";


const PharmacyWalkinQue = () => {
  // Function to format date as MM/DD/YYYY
  const formatDate = (date) => {
    const d = new Date(date);
    const month = (d.getMonth() + 1).toString().padStart(2, "0");
    const day = d.getDate().toString().padStart(2, "0");
    const year = d.getFullYear();
    return `${year}-${month}-${day}`;
  };
  const UrlLink = useSelector(state => state.userRecord?.UrlLink);
  // const [searchDoctorParams, setsearchDoctorParams] = useState({Doctor:'' });
  // console.log("123",searchDoctorParams);
  const dispatchvalue = useDispatch();
  const [OpenModalCancel, setOpenModalCancel] = useState(false);
  const [OpenModalCancel1, setOpenModalCancel1] = useState(false);
  const [OpenModalCancel11, setOpenModalCancel11] = useState(false);
  const [PatientRegisterData, setPatientRegisterData] = useState([]);
  const [CancelReason, setCancelReason] = useState("");
  const [CancelReason1, setCancelReason1] = useState("");
  const userRecord = useSelector((state) => state.userRecord?.UserData);
  console.log(CancelReason);
  const [modalIsOpen, setModalIsOpen] = useState(false);
  // const [selectedrow, setSelectedRow] = useState(false);
  const [DoctorNameData, setDoctorNameData] = useState([]);
  const [SpecializationData, setSpecializationData] = useState([]);
  const [RegistrationCancelId, setRegistrationCancelId] = useState("");
  const [ResheduleReson, setResheduleReson] = useState(false);
  const pagewidth = useSelector(state => state.userRecord?.pagewidth);
  const toast = useSelector((state) => state.userRecord?.toast);
  const [previousDoctorId, setPreviousDoctorId] = useState("");
  const UserData = useSelector((state) => state.userRecord?.UserData);


  const [searchOPParams, setsearchOPParams] = useState({
    SearchbyDate: formatDate(new Date()),
    SearchbyFirstName: '',
    SearchbyPhoneNumber: '',
    SearchSpecialization: '',
    SearchDoctor: '',
    SearchStatus: 'Registered',
  });


  console.log("ss", previousDoctorId);

  const fetchData = async () => {
    try {
      const response = await axios.get(`${UrlLink}DrugAdminstrations/get_OP_Pharmacy_Billing_datas`, {
        params: searchOPParams
      });

      const result = response.data;
      console.log("Fetched Data:", result);

      if (Array.isArray(result)) {
        setPatientRegisterData(result);
      } else {
        setPatientRegisterData([]);
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, [UrlLink, searchOPParams]);

  const [ReScheduleEdit, setReScheduleEdit] = useState({
    ChangingReason: "",
    Specialization: "",
    DoctorName: "",
  });
  const [ShowModalReschedule, setShowModalReschedule] = useState(false);
  const [ReScheduleId, setReScheduleId] = useState("");


  const handleSearchChange = (e) => {

    setReScheduleEdit({
      CancelReason: "",
      Specialization: "",
      DoctorName: "",
    });


    const { name, value } = e.target

    setsearchOPParams({ ...searchOPParams, [name]: value });


  };

  const handleModalVisibleReshedule = (params) => {
    let resheduleCancel = params.ChangingReason;

    if (resheduleCancel) {
      setResheduleReson(resheduleCancel);
      setOpenModalCancel11(true);

    }
    else {
      const tdata = {
        message: 'There is no data to view.',
        type: 'warn'
      };
      dispatchvalue({ type: 'toast', value: tdata });
    }
  }

  const PatientOPRegisterColumns = [
    {
      key: "id",
      name: "S.No",
      frozen: pagewidth > 500 ? true : false
    },
    {
      key: "Billing_Invoice_No",
      name: "Billing Invoice No",
      frozen: pagewidth > 500 ? true : false
    },
    {
      key: "PatientID",
      name: "Patient ID",
      width: 150,
      frozen: pagewidth > 500 ? true : false
    },
    {
      key: "PatientName",
      name: "Patient Name",
      width: 150,
      frozen: pagewidth > 500 ? true : false
    },
    {
      key: "Billing_Date",
      name: 'Billing Date',
    },
    {
      key: "Total_Items",
      name: "Total Items",
    },

    {
      key: "Total_Qty",
      name: "Total Qty",
    },
    {
      key: "Total_Amount",
      name: "Total Amount",
      frozen: pagewidth > 500 ? true : false
    },
    {
      key: "Paid_Amount",
      name: "Paid Amount",
    },
    {
      key: "created_by",
      name: "Billed by",
    },
  ];


  const handleModalVisible = (params) => {
    let reasonCancel = params.Reason;
    if (reasonCancel) {
      setCancelReason1(reasonCancel);
      setOpenModalCancel1(true);
    } else {
      const tdata = {
        message: 'There is no data to view.',
        type: 'warn'
      };
      dispatchvalue({ type: 'toast', value: tdata });
    }
  };

  const handleCancelAppointmentRequest = (params) => {
    console.log("RegisterCancel", params);
    setRegistrationCancelId(params.RegistrationId);
    setOpenModalCancel(true);
  }


  const handleCancelReason = () => {
    const UpdateRegister = {
      RegistrationId: RegistrationCancelId,
      CancelReason: CancelReason,
      created_by: userRecord?.username || "",
    };
    axios
      .post(`${UrlLink}Frontoffice/Register_Request_Cancel`, UpdateRegister)
      .then((response) => {
        const resData = response.data;
        const mess = Object.values(resData)[0];
        const typp = Object.keys(resData)[0];
        const tdata = {
          message: mess,
          type: typp,
        };
        dispatchvalue({ type: "toast", value: tdata });
        setCancelReason("");
        setRegistrationCancelId("");
        handleCloseModal();
      })
      .catch((err) => {
        console.log(err);
      });

  };
  const handleCloseModal = () => {
    setModalIsOpen(false);
    setOpenModalCancel(false);
    setOpenModalCancel1(false);
    setShowModalReschedule(false);
    setOpenModalCancel11(false);
  };

  const handleSpecChange = (e) => {
    const { name, value } = e.target;
    setReScheduleEdit((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleDocChange = (e) => {
    const { name, value } = e.target;
    setReScheduleEdit((prev) => ({
      ...prev,
      [name]: value,
    }));
  };



  // useEffect(() => {
  //   if (ReScheduleEdit?.Specialization && UrlLink) {
  //     axios
  //       .get(
  //         `${UrlLink}Masters/get_Doctor_by_Speciality_Detials?Speciality=${ReScheduleEdit.Specialization}`
  //       )
  //       .then((reponse) => {
  //         let data = reponse.data;

  //         setDoctorNameData(data);
  //         console.log("specialization",data);
  //       })
  //       .catch((err) => {
  //         console.log(err);
  //       });
  //   }
  // }, [UrlLink, ReScheduleEdit.Specialization]);

  useEffect(() => {
    const fetchdat = async () => {

      const postdata = {
        LocationId: UserData?.location,
        Date: formatDate(new Date()),
        Speciality: ReScheduleEdit?.Specialization || searchOPParams?.SearchSpecialization,
      };
      console.log("Doctrrrrr", postdata);

      try {
        const response = await axios.get(
          `${UrlLink}Frontoffice/get_available_doctor_by_speciality`,
          { params: postdata }
        );

        setDoctorNameData(response.data);
        console.log("Doctrrrrr", response.data);
      } catch (error) {
        setDoctorNameData([]);
        console.error("Error fetching referral doctors:", error);
      }
    };
    if (ReScheduleEdit.Specialization || searchOPParams.SearchSpecialization) {
      fetchdat();
    }
  }, [UrlLink, UserData.location, searchOPParams?.SearchSpecialization, ReScheduleEdit?.Specialization]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [specializationResponse] = await Promise.all([
          axios.get(`${UrlLink}Masters/Speciality_Detials_link`),
        ]);
        setSpecializationData(specializationResponse.data);
        console.log(specializationResponse.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };
    fetchData();
  }, [UrlLink]);
  const handleAppointmentReschedule = (params) => {
    console.log("paramsupdate", params);
    const PreviousDoctor = params.DoctorId;
    setPreviousDoctorId(PreviousDoctor);
    setShowModalReschedule(true);
    setReScheduleId(params.RegistrationId);
  };

  const handleReschedule = () => {
    const updatedReschedule = {
      ...ReScheduleEdit,
      PreviousDoctor: previousDoctorId,
      RegistrationId: ReScheduleId,
      created_by: userRecord?.username || "",
    };
    console.log("updatedReschedule", updatedReschedule);
    axios
      .post(
        `${UrlLink}Frontoffice/Registration_Reshedule_Details`,
        updatedReschedule
      )
      .then((response) => {
        const ress = response.data;
        const mess = Object.values(ress)[0];
        const typp = Object.keys(ress)[0];
        console.log("submit data", ress);
        const tdata = {
          message: mess,
          type: typp,
        };
        dispatchvalue({ type: "toast", value: tdata });
        setReScheduleEdit({
          CancelReason: "",
          Specialization: "",
          DoctorName: "",
        });
        handleCloseModal();
        fetchData();
      })
      .catch((e) => {
        console.log(e);
      });

  }
  return (
    <>
      <div className="Main_container_app">
        <h3>OPD Queue List</h3>
        {/* <div className='DivCenter_container'>OP Patient Details </div> */}
        <div className="RegisFormcon_1" style={{ marginTop: '10px' }}>

          <div className="RegisForm_1" >

            <label htmlFor="input">
              Current Date<span>:</span>
            </label>
            <input
              type="date"
              name="SearchbyDate"
              value={searchOPParams.SearchbyDate}
              onChange={handleSearchChange}
            />
          </div>

          <div className="RegisForm_1" >
            <label htmlFor="input">
              First Name<span>:</span>
            </label>
            <input
              type="text"
              name="SearchbyFirstName"
              value={searchOPParams.SearchbyFirstName}
              onChange={handleSearchChange}
            />
          </div>

          <div className="RegisForm_1" >
            <label htmlFor="input">
              Phone Number<span>:</span>
            </label>
            <input
              type="number"
              name="SearchbyPhoneNumber"
              value={searchOPParams.SearchbyPhoneNumber}
              onChange={handleSearchChange}
            />
          </div>
{/* 
          <div className="RegisForm_1">
            <label htmlFor="input">
              Specialization<span>:</span>
            </label>
            <select
              name="SearchSpecialization"
              value={searchOPParams.SearchSpecialization}
              onChange={handleSearchChange}
            >
              <option value="">Select</option>

              {SpecializationData.filter((p) => p.Status === "Active").map((p) => (
                <option key={p.id} value={p.id}>
                  {p.SpecialityName}
                </option>
              ))}

            </select>
          </div>

          <div className="RegisForm_1">
            <label htmlFor="input">
              Doctor<span>:</span>
            </label>
            <select
              name="SearchDoctor"
              value={searchOPParams.SearchDoctor}
              onChange={handleSearchChange}
            >
              <option value="">Select</option>

              {DoctorNameData && Array.isArray(DoctorNameData) &&
                DoctorNameData.map((p) => (
                  <option key={p.doctor_id} value={p.doctor_id}>
                    {p.doctor_name}
                  </option>
                ))}

            </select>
          </div> */}

          {/* <div className="RegisForm_1">
            <label htmlFor="SearchStatus">Status
              <span>:</span>
            </label>
            <select
              id='SearchStatus'
              name='SearchStatus'
              value={searchOPParams.SearchStatus}
              onChange={handleSearchChange}
            >
              <option value='Registered'>Registered</option>
              <option value='Completed'>Completed</option>
              <option value='Cancelled'>Cancelled</option>
            </select>
          </div> */}


        </div>


        <ToastAlert Message={toast.message} Type={toast.type} />
        <br />
        <ReactGrid columns={PatientOPRegisterColumns} RowData={PatientRegisterData} />
      </div>
    </>
  )
}

export default PharmacyWalkinQue
