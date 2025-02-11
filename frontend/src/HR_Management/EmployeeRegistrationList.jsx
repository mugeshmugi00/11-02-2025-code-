import axios from 'axios'
import React, { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux';
import Button from "@mui/material/Button";
import EditIcon from "@mui/icons-material/Edit";
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import ReactGrid from '../OtherComponent/ReactGrid/ReactGrid';
import ToastAlert from '../OtherComponent/ToastContainer/ToastAlert';
import { useNavigate } from 'react-router-dom';
import LoupeIcon from "@mui/icons-material/Loupe";


const EmployeeRegistrationList = () => {
    const UrlLink = useSelector(state => state.userRecord?.UrlLink);
    const toast = useSelector(state => state.userRecord?.toast);
    const pagewidth = useSelector(state => state.userRecord?.pagewidth);
    const dispatchvalue = useDispatch();
    const navigate = useNavigate()
    
    
    const [EmployeeRegisterData, setEmployeeRegisterData] = useState([])
    const [Departments, setDepartments] = useState([])
    const [Designations, setDesignations] = useState([])
    const [GetEmployeeRegisterData, setGetEmployeeRegisterData] = useState(false)
    const [EmployeeRegisterFIlteredData, setEmployeeRegisterFIlteredData] = useState([])
    const [SearchQuery, setSearchQuery] = useState('')
    
    useEffect(() => {
        axios.get(`${UrlLink}HR_Management/Employee_Registration_Details`)
            .then((res) => {
                const ress = res.data
                console.log(ress,'ress');
                setEmployeeRegisterData(Array.isArray(ress) ? ress : []);

               

            })
            .catch((err) => {
                console.log(err);
            })
        dispatchvalue({ type: 'EmployeeListId', value: {} })
    }, [UrlLink, dispatchvalue])


    
    const EmployeeRegisterColumns = [
        {
            key: "id",
            name: "S.No ",
            frozen: true
        },
        {
            key: "Employee_Id",
            name: "Employee Id",
            filter: true,
            type: 'input-text',
            frozen:  true,
        },
        {
            key: "FullName",
            name: "Employee Name",
            filter: true,
            frozen: true
        },
        {
            key: "Phone",
            name: "Contact Number",
            frozen:true
        },
        {
            key: "Department",
            name: "Department",
            frozen: true
        },
        {
            key: "Designation",
            name: "Designation",
            frozen: true
        },
        {
            key: "Created_by",
            name: "created By",
        },


        {
            key: "Action",
            name: "Action",
            renderCell: (params) => (
                <>
                    <Button
                        className="cell_btn"
                        onClick={() => handleEditEmpDetails(params.row)}
                    >
                        <EditIcon className="check_box_clrr_cancell" />
                    </Button>
                </>
            ),
        },

       

        {
            key: "UserAction",
            name: "User Action",
            renderCell: (params) => (
                <>{
                   
                        params.row.usercreated ? (
                            <>user created</>
                        )
                            :
                            (
                                <Button
                                    className="cell_btn"
                                    onClick={() => handleEmpUserRegister(params.row)}
                                >
                                    <ArrowForwardIcon className="check_box_clrr_cancell" />
                                </Button>
                            )

                }

                </>
            ),
        }

    ]


    
   

    const handlenewEmpRegister = () => {

        dispatchvalue({ type: 'EmployeeListId', value: {} })

        navigate("/Home/HR");
        dispatchvalue({ type: 'HrFolder', value:'EmployeeRegistration'});
        dispatchvalue({ type: "setPreviousFolder", value: null }); 
        dispatchvalue({ type: "showMenu", value: true });

    }


    const handleEmpUserRegister = (params) => {

        dispatchvalue({ type: 'UsercreateEmpdata', value: { EmployeeId: params.Employee_Id, Type: 'EMPLOYEE' } })
        dispatchvalue({ type: 'UserListId', value: {} })

        navigate("/Home/HR");
        dispatchvalue({ type: 'HrFolder', value:'UserRegisterMaster'});
        dispatchvalue({ type: "setPreviousFolder", value: null }); 
        dispatchvalue({ type: "showMenu", value: true });
    }

    const handleEditEmpDetails = (employee) =>{
        console.log("employee",employee);


        console.log(employee,'55555555555555');
        
        const { Employee_Id } = employee;
        dispatchvalue({ type: 'EmployeeListId', value: { Employee_Id } });

        const updatedEmployeeListId = { Employee_Id }; // Capture the PatientId
        console.log(updatedEmployeeListId, 'Employee_Id after dispatch');
    

        navigate("/Home/HR");
        dispatchvalue({ type: 'HrFolder', value:'EmployeeRegistration'});
        dispatchvalue({ type: "setPreviousFolder", value: null }); 
        dispatchvalue({ type: "showMenu", value: true });


        dispatchvalue({type: 'HrFolder',value:'EmployeeRegistration'})

    }

    
    return (
        <>
            <div className="Main_container_app">
                <h3>Employee List</h3>
                <div className="search_div_bar">
                    <div className=" search_div_bar_inp_1">
                        <label htmlFor="">Search Here
                            <span>:</span>
                        </label>
                        <input
                            type="text"
                            value={SearchQuery}
                            placeholder='Name or Number'
                            // onChange={(e) => setSearchQuery(e.target.value)}
                             />
                    </div>
                    <button
                        className="search_div_bar_btn_1"
                        onClick={handlenewEmpRegister}
                        title="New Doctor Register"
                    >
                        <LoupeIcon />
                    </button>

                </div>
                <ReactGrid columns={EmployeeRegisterColumns} RowData={EmployeeRegisterData} />

            </div>
            <ToastAlert Message={toast.message} Type={toast.type} />
        </>
    )
}

export default EmployeeRegistrationList;