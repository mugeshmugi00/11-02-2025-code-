import React, { useEffect, useState } from 'react';
import './Leave.css';
import axios from 'axios';
import SearchIcon from '@mui/icons-material/Search';

const EmployeeLeave = ({userRecord}) => {
  // console.log(userRecord)
  const [formData, setFormData] = useState({
    employeeId: '',
    employeeName: '',
    department: '',
    leaveType: '',
    fromDate: '',
    toDate: '',
    fromtime: '',
    totime: '',
    prDate: '',
    reason: '',
    location: userRecord.location,
    createdby: userRecord.username

  });

  console.log(formData)
  const Getpatientdata = () => {
    if (formData.employeeId === '') {
      // Show alert and set employeeName to empty when employeeId is empty
      alert('Enter employee ID');
      setFormData(prevFormData => ({
        ...prevFormData,
        employeeName: ''
      }));
    } else {
      if (formData.employeeId) {
        axios.get(`${urllink}HRmanagement/get_employeename?employeedid=${formData.employeeId}`)
          .then((response) => {
            console.log(response.data);
  
            if (response.data === 'error') {
              // Show alert if employee name is not available
              setFormData(prevFormData => ({
                ...prevFormData,
                employeeName: ''
              }));
              alert('Employee name not available for the provided Employee ID');
            } else {
              // Set the employeeName in formData if it's available
              setFormData(prevFormData => ({
                ...prevFormData,
                employeeName: response.data.employeeName
              }));
            }
          })
          .catch((error) => {
            console.log(error);
          });
      } else {
        // Reset employeeName when employeeId is empty
        setFormData(prevFormData => ({
          ...prevFormData,
          employeeName: ''
        }));
      }
    }
  }
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(formData);

    const formDataObject = new FormData();
    formDataObject.append('employeeId', formData.employeeId);
    formDataObject.append('employeeName', formData.employeeName);
    formDataObject.append('department', formData.department);
    formDataObject.append('leaveType', formData.leaveType);
    formDataObject.append('fromDate', formData.fromDate);
    formDataObject.append('toDate', formData.toDate);
    formDataObject.append('fromtime', formData.fromtime);
    formDataObject.append('totime', formData.totime);
    formDataObject.append('prDate', formData.prDate);
    formDataObject.append('reason', formData.reason);
    formDataObject.append('location', formData.location);
    formDataObject.append('createdby', formData.createdby);

    axios.post(`${urllink}HRmanagement/insert_leave_register`,formDataObject,{
      headers: {
        'Content-Type': 'multipart/form-data',
    },
    })
    .then((response)=>{
      console.log(response.data)
    })
    .catch((error)=>{
      console.log(error)
    })
}

  return (
    <div className='leaveform'>
      <div className='user_patienthead'>
        <h3>Leave Form</h3>
      </div>
     
        <div className="RegisFormcon leavecon">
          <div className='RegisForm_1 leaveform_1'>
            <label htmlFor="employeeId">Employee ID <span>:</span></label>
            <input type="text" id="employeeId" name="employeeId" placeholder="Enter Employee ID" onChange={handleChange} />
            <span onClick={Getpatientdata}
          style={{color:'orange',position:'relative',right:"60px",top:"4px",cursor:"pointer"}}>
          <SearchIcon/>
          </span>
          </div>
        </div>
        <div className="RegisFormcon leavecon ">
          <div className='RegisForm_1 leaveform_1'>
            <label htmlFor="employeeName">Employee Name <span>:</span></label>
            <input type="text" id="employeeName" name="employeeName" value={formData.employeeName} placeholder="Enter Employee Name" onChange={handleChange} />
          </div>
        </div>
        <div className="RegisFormcon leavecon ">
        <div className='RegisForm_1 leaveform_1'>
          <label htmlFor="department">Department <span>:</span></label>
          <select id="department" name="department" onChange={handleChange}>
          <option  value="">Select</option>
            <option value="doctor">Doctor</option>
            <option value="nurse">Nurse</option>
            <option value="frontoffice">Front Office</option>
          </select>
        </div>
      </div>
        <div className="RegisFormcon leavecon">
          <div className='RegisForm_1 leaveform_1'>
            <label htmlFor="leaveType">Leave Type <span>:</span></label>
            <select id="leaveType" name="leaveType" onChange={handleChange}>
              <option value="select">Select Type</option>
              <option value="casual">Casual Leave</option>
              <option value="sick">Sick Leave</option>
              <option value="permission">Permission</option>
              <option value="annual">Annual Leave</option>
            </select>
          </div>
        </div>
        {(formData.leaveType === "casual" || formData.leaveType === "sick" || formData.leaveType === "annual") && (
          <>
            <div className="RegisFormcon leavecon">
              <div className='RegisForm_1 leaveform_1'>
                <label htmlFor="fromDate">From Date <span>:</span> </label>
                <input type="date" id="fromDate" name="fromDate" onChange={handleChange} />
              </div>
            </div>
            <div className="RegisFormcon leavecon">
              <div className='RegisForm_1 leaveform_1'>
                <label htmlFor="toDate">To Date <span>:</span></label>
                <input type="date" id="toDate" name="toDate" onChange={handleChange} />
              </div>
            </div>
          </>
        )}
        {
          formData.leaveType === "permission" && (
            <>
              <div className="RegisFormcon leavecon">
                <div className='RegisForm_1 leaveform_1'>
                  <label htmlFor="prDate"> Date <span>:</span> </label>
                  <input type="date" id="prDate" name="prDate" onChange={handleChange} />
                </div>
              </div>
              <div className="RegisFormcon leavecon">
                <div className='RegisForm_1 leaveform_1'>
                  <label htmlFor="fromtime">From Time <span>:</span></label>
                  <input type="time" id="fromtime" name="fromtime" onChange={handleChange} />
                </div>
              </div>
              <div className="RegisFormcon leavecon">
                <div className='RegisForm_1 leaveform_1'>
                  <label htmlFor="totime">To Time <span>:</span></label>
                  <input type="time" id="totime" name="totime" onChange={handleChange} />
                </div>
              </div>

            </>
          )
        }

        <div className="RegisFormcon leavecon">
          <div className='RegisForm_1 leaveform_1'>
            <label htmlFor="reason">Reason for Leave <span>:</span></label>
            <textarea id="reason" name="reason" rows="4" cols="3" onChange={handleChange}></textarea>
          </div>
        </div>
        <div className="Register_btn_con">
          <button onClick={handleSubmit} className="RegisterForm_1_btns">Submit</button>
        </div>
      
    </div>
  );
}

export default EmployeeLeave;
