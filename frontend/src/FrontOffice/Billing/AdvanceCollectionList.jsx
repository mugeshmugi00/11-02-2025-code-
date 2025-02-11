import axios from "axios";
import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import Button from "@mui/material/Button";
import ReactGrid from "../../OtherComponent/ReactGrid/ReactGrid";
import ToastAlert from "../../OtherComponent/ToastContainer/ToastAlert";
import { useNavigate } from "react-router-dom";
import LoupeIcon from "@mui/icons-material/Loupe";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";

const AdvanceCollectionList = () => {
  const UrlLink = useSelector((state) => state.userRecord?.UrlLink);
  const UserData = useSelector((state) => state.userRecord?.UserData);
  const toast = useSelector((state) => state.userRecord?.toast);
  const dispatchvalue = useDispatch();
  const navigate = useNavigate();
  const [Filterdata, setFilterdata] = useState([]);
  const [SearchQuery, setSearchQuery] = useState({
    searchBy: "",
    Status: "Pending",
  });

  useEffect(() => {
    axios.get(`${UrlLink}Frontoffice/get_overall_advance_details`)
        .then((res) => {
            const ress = res?.data?.AdvanceDetails

            if (Array.isArray(ress)) {
              console.log('billllll',ress);
              
                setFilterdata(ress);
            } else {
                setFilterdata([]);
            }
        })
        .catch((err) => {
            console.log(err);
        });
}, [UrlLink]);

  const handleSearchChange = (e) => {
    const { name, value } = e.target;
    setSearchQuery((prev) => ({
      ...prev,
      [name]: value,
    }));
  };
  const handlenewDocRegister = () => {
    navigate("/Home/AdvanceCollectionBilling");
  };

  const PatientOPRegisterColumns = [
    {
      key: "PatientId",
      name: "Patient Id",
    },
    {
      key: "PatientName",
      name: "Patient Name",
    },   
    {
      key: "RegistrationId",
      name: "Registration Id",
    },   

    {
      key: "PhoneNo",
      name: "PhoneNo",
    },
    {
      key: "AdvanceAmount",
      name: "Advance Amount",
    },
    {
      key: "Date",
      name: "Date",
    },
    {
      key: "Time",
      name: "Time",
    },
    {
      key: "ReceivedBy",
      name: "Received By",
    },
  ];

  return (
    <>
      <>
        <div className="Main_container_app">
          <h3>Advance Collection List</h3>
          <div className="search_div_bar">
            <div className=" search_div_bar_inp_1">
              <label htmlFor="">
                Search Here
                <span>:</span>
              </label>
              <input
                type="text"
                name="searchBy"
                value={SearchQuery.searchBy}
                placeholder="Patient ID or Name or PhoneNo "
                onChange={(e) => handleSearchChange(e)}
              />
            </div>
            {/* <div className=" RegisForm_1">
              <label htmlFor="">
                Status
                <span>:</span>
              </label>
              <select
                id=""
                name="Status"
                value={SearchQuery.Status}
                onChange={handleSearchChange}
              >
                <option value="">Select</option>
                <option value="Pending">Pending</option>
                <option value="Completed">Completed</option>
              </select>
            </div> */}
            <button
              className="search_div_bar_btn_1"
              onClick={handlenewDocRegister}
              title="New Advance Billing"
            >
              <LoupeIcon />
            </button>
          </div>
          <ReactGrid columns={PatientOPRegisterColumns} RowData={Filterdata} />
        </div>
        <ToastAlert Message={toast.message} Type={toast.type} />
      </>
    </>
  );
};

export default AdvanceCollectionList;
