import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import ReactGrid from '../../OtherComponent/ReactGrid/ReactGrid';
import Button from "@mui/material/Button";
import EditIcon from "@mui/icons-material/Edit";
import ToastAlert from '../../OtherComponent/ToastContainer/ToastAlert';
import axios from 'axios';
import PhotoCameraBackIcon from "@mui/icons-material/PhotoCameraBack";


const ConsentFormsMaster = () => {
    const dispatchvalue = useDispatch();
    const UrlLink = useSelector(state => state.userRecord?.UrlLink);
    const userRecord = useSelector((state) => state.userRecord?.UserData);
    const toast = useSelector(state => state.userRecord?.toast);
    const [DepartmentData, setDepartmentData] = useState([]);
    const [Consent, setConsent] = useState({
        ConsentId: '',
        Department: '',
        ConsentFormsName: '',
        ConsentFile: null,
    });
    const [ConsentData, setConsentData] = useState([]);
    const [IsConsentGet, setIsConsentGet] = useState(false);

    useEffect(() => {
        axios.get(`${UrlLink}Masters/Department_Detials_link`)
            .then((res) => {
                setDepartmentData(res.data);
            })
            .catch((err) => {
                console.log(err);
            });
    }, [UrlLink]);

    useEffect(() => {
        axios.get(`${UrlLink}Masters/ConsentName_Detials_link`)
            .then((res) => {
                setConsentData(res.data);
            })
            .catch((err) => {
                console.log(err);
            });
    }, [IsConsentGet, UrlLink]);

    const handleeditConsentName = (params) => {
        setConsent({
            ConsentId: params.id,
            Department: params.DepartmentId,
            ConsentFormsName: params.ConsentFormsName,
            ConsentFile: null
        });
    };

    const handleConsentSubmit = () => {
        if (Consent.Department && Consent.ConsentFormsName) {
            const formData = new FormData();
            formData.append('ConsentId', Consent.ConsentId);
            formData.append('Department', Consent.Department);
            formData.append('ConsentFormsName', Consent.ConsentFormsName);
            formData.append('created_by', userRecord?.username || '');
            if (Consent.ConsentFile) {
                formData.append('ConsentFile', Consent.ConsentFile);
            }

            axios.post(`${UrlLink}Masters/ConsentName_Detials_link`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            })
                .then((res) => {
                    const tdata = {
                        message: res.data.success || res.data.warn,
                        type: res.data.success ? 'success' : 'warn',
                    };
                    dispatchvalue({ type: 'toast', value: tdata });
                    setIsConsentGet(prev => !prev);
                    setConsent({
                        ConsentId: '',
                        Department: '',
                        ConsentFormsName: '',
                        ConsentFile: null
                    });
                })
                .catch((err) => {
                    console.log(err);
                });
        } else {
            const tdata = {
                message: `Please provide both Department Name and Consent name.`,
                type: 'warn'
            };
            dispatchvalue({ type: 'toast', value: tdata });
        }
    };

    const handleConsentChange = (e) => {
        const { name, value } = e.target;
        setConsent(prevState => ({
            ...prevState,
            [name]: value,
        }));
    };

    const handleFileChange = (e) => {
        setConsent(prevState => ({
            ...prevState,
            ConsentFile: e.target.files[0],
        }));
    };

    return (
        <>
            <div className="Main_container_app">
                <h3>Consent Form Masters</h3>
                <div className="common_center_tag">
                    <span>Consent</span>
                </div>
                <div className="RegisFormcon_1">
                    {['Department', 'ConsentFormsName'].map((field, indx) => (
                        <div className="RegisForm_1" key={indx}>
                            <label>{field === 'Department' ? 'Department' : 'ConsentForms Name'} <span>:</span></label>
                            {field === 'Department' ?
                                <select name={field} value={Consent[field]} onChange={handleConsentChange}>
                                    <option value=''>Select Department</option>
                                    {DepartmentData.filter(p => p.Status === 'Active').map((dept, index) => (
                                        <option key={index} value={dept.id}>{dept.DepartmentName}</option>
                                    ))}
                                </select>
                                :
                                <input type="text" name={field} value={Consent[field]} onChange={handleConsentChange} />
                            }
                        </div>
                    ))}
                    <div className="RegisForm_1">
                        <label>Upload  <span>:</span></label>
                        <div className="RegisterForm_2">  <input type="file"              accept="image/jpeg, image/png, application/pdf"
               style={{ display: "none" }}
               id="ConsentForm"
               onChange={handleFileChange} />

<div
              style={{
                width: "120px",
                display: "flex",
                justifyContent: "flex-start",
                gap: "20px",
              }}
            >
              <label
                title='Choose Consent Form'
                htmlFor={'ConsentForm'}
                className="RegisterForm_1_btns choose_file_update"
              >
                <PhotoCameraBackIcon />
              </label>
              </div>
                   </div>
                    </div>
                </div>
                <div className="Main_container_Btn">
                    <button onClick={handleConsentSubmit}>{Consent.ConsentId ? 'Update' : 'Save'}</button>
                </div>



                {ConsentData.length > 0 &&
                    <ReactGrid columns={[
                        { key: "id", name: "Consent Id", frozen: true },
                        { key: "created_by", name: "Created By", frozen: true },
                        { key: "Department", name: "Department Name" },
                        { key: "ConsentFormsName", name: "ConsentForms Name" },
                        {
                            key: "Action",
                            name: "Action",
                            renderCell: (params) => (
                                <Button className="cell_btn" onClick={() => handleeditConsentName(params.row)}>
                                    <EditIcon className="check_box_clrr_cancell" />
                                </Button>
                            ),
                        }
                    ]} RowData={ConsentData} />
                }
            </div>
            <ToastAlert Message={toast.message} Type={toast.type} />
        </>
    );
}

export default ConsentFormsMaster;
