import axios from 'axios'
import React, { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux';
import Button from "@mui/material/Button";
import ReactGrid from '../../OtherComponent/ReactGrid/ReactGrid';
import ToastAlert from '../../OtherComponent/ToastContainer/ToastAlert';
import { useNavigate } from 'react-router-dom';
import LoupeIcon from "@mui/icons-material/Loupe";
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';


function GeneralBillingRadiologyQuelist() {

    const UrlLink = useSelector(state => state.userRecord?.UrlLink);
    const UserData = useSelector((state) => state.userRecord?.UserData);
    const toast = useSelector(state => state.userRecord?.toast);
    const dispatchvalue = useDispatch();
    const navigate = useNavigate()
    const [Filterdata, setFilterdata] = useState([])
    const [SearchQuery, setSearchQuery] = useState({
        searchBy: "",
        Status: "Unpaid"
    })

    useEffect(() => {
        axios.get(`${UrlLink}Frontoffice/Get_Radiology_Billing_Details`, { params: { ...SearchQuery,location:UserData?.location } })
            .then((res) => {
                const ress = res.data;

                if (Array.isArray(ress)) {
                    setFilterdata(ress);
                } else {
                    setFilterdata([]);
                }
            })
            .catch((err) => {
                console.log(err);
            });
    }, [UrlLink, SearchQuery, UserData?.location]);


    const handleSearchChange = (e) => {
        const { name, value } = e.target
        setSearchQuery((prev) => ({
            ...prev,
            [name]: value
        }))
    }

    const handlenewDocRegister = () => {
        dispatchvalue({ type: 'OPBillingData', value: {type:'OP'} })
        dispatchvalue({ type: 'IPBillingData', value: {} })
        // navigate('/Home/OverAllQuickBilling')
        navigate("/Home/CashierFolder");
        dispatchvalue({ type: "HrFolder", value: "OverAllQuickBilling" });
        dispatchvalue({ type: "setPreviousFolder", value: null });
        dispatchvalue({ type: "showMenu", value: true });
    }

    const HandleMovedatatobill = (params) => {

        console.log(params.Status,'params');
        dispatchvalue({ type: 'OPBillingData', value: params })
        dispatchvalue({ type: 'IPBillingData', value: {} })
        // navigate('/Home/QuickBilling')

        if (params.Status == "Unpaid"){

            console.log('unpaid');
            navigate("/Home/FrontOfficeFolder");
            dispatchvalue({ type: "HrFolder", value: "RadiologyGeneralBilling"});
            dispatchvalue({ type: "setPreviousFolder", value: null });
            dispatchvalue({ type: "showMenu", value: true });

        }

        else {
            navigate("/Home/FrontOfficeFolder");
            dispatchvalue({ type: "HrFolder", value: "QuickBilling" });
            dispatchvalue({ type: "setPreviousFolder", value: null });
            dispatchvalue({ type: "showMenu", value: true });
        }
        
    }

    const PatientOPRegisterColumns = [
        {
            key: "id",
            name: "ID",
        },
        {
            key: "Date",
            name: "Date",
        },
        {
            key: "PatientId",
            name: "Patient Id",
        },
        {
            key: "Patient_Name",
            name: "Patient Name",
        },
        {
            key: "PhoneNo",
            name: "PhoneNo",
        },
        {
            key: "Doctor_ShortName",
            name: "Doctor Name",

        },
        {
            key: 'PatientCategory',
            name: 'Patient Category',
        },
        {
            key: 'VisitPurpose',
            name: 'VisitPurpose',
        },
        {
            key: "Action",
            name: "Action",
            renderCell: (params) => {
                if (params.row.Status === 'Pending') {
                    return (
                        <Button
                            className="cell_btn"
                            onClick={() => HandleMovedatatobill(params.row)}
                        >
                            <ArrowForwardIcon className="check_box_clrr_cancell" />
                        </Button>
                    );
                } else if (params.row.Status === 'Unpaid') {
                    return (
                        <Button
                            className="cell_btn unpaid_btn"
                            onClick={() => HandleMovedatatobill(params.row)}
                        >
                            <ArrowForwardIcon className="check_box_clrr_unpaid" />
                        </Button>
                    );
                } else {
                    return 'No Action';
                }
        },
    }


    ]

  return (
   
    <>
    <>
        <div className="Main_container_app">
        
            <h3>Radiology Billing Quelist</h3>
            <div className="search_div_bar">
                <div className=" search_div_bar_inp_1">
                    <label htmlFor="">Search Here
                        <span>:</span>
                    </label>
                    <input
                        type="text"
                        name='searchBy'
                        value={SearchQuery.searchBy}
                        placeholder='Patient ID or Name or PhoneNo '
                        onChange={(e) => handleSearchChange(e)} />
                </div>
                <div className=" RegisForm_1">
                    <label htmlFor="">Status
                        <span>:</span>
                    </label>
                    <select
                        id=''
                        name='Status'
                        value={SearchQuery.Status}
                        onChange={handleSearchChange}
                    >
                        <option value=''>Select</option>
                        <option value='Pending'>Pending</option>
                        <option value='Paid'>Completed</option>
                        <option value='Unpaid'>Unpaid</option>
                    </select>
                </div>
                <button
                    className="search_div_bar_btn_1"
                    onClick={handlenewDocRegister}
                    title="New Doctor Register"
                >
                    <LoupeIcon />
                </button>

            </div>
            <ReactGrid columns={PatientOPRegisterColumns} RowData={Filterdata} />

        </div>
        <ToastAlert Message={toast.message} Type={toast.type} />
    </>
</>
  )
}

export default GeneralBillingRadiologyQuelist
