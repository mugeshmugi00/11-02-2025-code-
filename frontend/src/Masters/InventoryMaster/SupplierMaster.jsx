import React, { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { BlockInvalidcharecternumber } from '../../OtherComponent/OtherFunctions';
import ModelContainer from '../../OtherComponent/ModelContainer/ModelContainer';
import ToastAlert from '../../OtherComponent/ToastContainer/ToastAlert';
import axios from 'axios';
import PhotoCameraBackIcon from '@mui/icons-material/PhotoCameraBack';
import VisibilityIcon from '@mui/icons-material/Visibility';
const SupplierMaster = () => {
    const dispatchvalue = useDispatch();
    const navigate = useNavigate();
    const toast = useSelector(state => state.userRecord?.toast);
    const UrlLink = useSelector(state => state.userRecord?.UrlLink);
    const userRecord = useSelector((state) => state.userRecord?.UserData);
    const SupplierMasterStore = useSelector(state => state.Inventorydata?.SupplierMasterStore);

    const [SupplierMaster, setSupplierMaster] = useState({
        SupplierId: '',
        SupplierName: '',
        SupplierType: '',
        ContactPerson: '',
        ContactNumber: '',
        EmailAddress: '',
        Address: '',
        RegistrationNumber: '',
        GSTNumber: '',
        PANNumber: '',
        DruglicenseNo: '',
        PaymentTerms: '',
        CreditLimit: '',
        LeadTime: '',
        Notes: '',
        FileAttachment: null,
        BankName: '',
        AccountNumber: '',
        IFSCCode: '',
        BankBranch: '',

    })





    const formatLabel = (label) => {

        if (/[a-z]/.test(label) && /[A-Z]/.test(label) && !/\d/.test(label)) {
            return label
                .replace(/([a-z])([A-Z])/g, "$1 $2")
                .replace(/^./, (str) => str.toUpperCase());
        } else {
            return label;
        }
    };


    const getInputType = (name) => {

        if (['ContactNumber', 'CreditLimit', 'AccountNumber', 'PaymentTerms', 'LeadTime'].includes(name)) return 'number';
        return 'text';
    };





    const handleInputChange = (e) => {

        const { name, value, type, checked } = e.target;

        if (name === 'ContactNumber') {

            if (value.length > 10) {

                const tdata = {
                    message: 'ContactNumber only 10 degits numbers',
                    type: 'warn'
                };
                dispatchvalue({ type: 'toast', value: tdata });

            }

            else {
                setSupplierMaster((prev) => ({
                    ...prev,
                    [name]: value
                }))
            }

        }
        else if (['SupplierName', 'RegistrationNumber', 'GSTNumber', 'PANNumber', 'DruglicenseNo'].includes(name)) {

            setSupplierMaster((prev) => ({
                ...prev,
                [name]: value.toUpperCase()
            }))

        }

        else {
            setSupplierMaster((prev) => ({
                ...prev,
                [name]: type === 'checkbox' ? checked : value
            }))
        }


    }




    const handlefileOnchange = (e) => {

        const { files } = e.target


        if (files && files.length > 0) {
            let formattedValue = files[0];

            const allowedTypes = ['application/pdf', 'image/jpeg', 'image/png'];
            const maxSize = 5 * 1024 * 1024; // Example max size of 5MB
            if (!allowedTypes.includes(formattedValue.type) || formattedValue.type === '') {

                const tdata = {
                    message: 'Invalid file type. Please upload a PDF, JPEG, or PNG file.',
                    type: 'warn'
                };
                dispatchvalue({ type: 'toast', value: tdata });

            } else {
                if (formattedValue.size > maxSize) {
                    const tdata = {
                        message: 'File size exceeds the limit of 5MB.',
                        type: 'warn'
                    };
                    dispatchvalue({ type: 'toast', value: tdata });

                } else {
                    const reader = new FileReader();
                    reader.onload = () => {
                        setSupplierMaster((prev) => ({
                            ...prev,
                            FileAttachment: reader.result
                        }))

                    };
                    reader.readAsDataURL(formattedValue);




                }
            }

        } else {
            const tdata = {
                message: 'No file selected. Please choose a file to upload.',
                type: 'warn'
            };
            dispatchvalue({ type: 'toast', value: tdata });
        }

    }



    const Selectedfileview = (fileval) => {

        if (fileval) {
            let tdata = {
                Isopen: false,
                content: null,
                type: 'image/jpg'
            };
            if (['data:image/jpeg;base64', 'data:image/jpg;base64'].includes(fileval?.split(',')[0])) {
                tdata = {
                    Isopen: true,
                    content: fileval,
                    type: 'image/jpeg'
                };
            } else if (fileval?.split(',')[0] === 'data:image/png;base64') {
                tdata = {
                    Isopen: true,
                    content: fileval,
                    type: 'image/png'
                };
            } else if (fileval?.split(',')[0] === 'data:application/pdf;base64') {
                tdata = {
                    Isopen: true,
                    content: fileval,
                    type: 'application/pdf'
                };
            }

            dispatchvalue({ type: 'modelcon', value: tdata });
        } else {
            const tdata = {
                message: 'There is no file to view.',
                type: 'warn'
            };
            dispatchvalue({ type: 'toast', value: tdata });
        }
    }



    useEffect(() => {


        if (SupplierMasterStore && Object.keys(SupplierMasterStore).length !== 0) {
            console.log('SupplierMasterStore', SupplierMasterStore);

            const { id, ...rest } = SupplierMasterStore;

            setSupplierMaster((prev) => ({
                ...prev,
                ...rest,
            }))
        }

    }, [SupplierMasterStore])


    

    const saveSupplierdata = () => {
       
        let requiredfields = Object.keys(SupplierMaster).filter(f => 
            !['SupplierId', 'Notes', 'FileAttachment', 'SupplierType', 'ContactPerson', 'CreditLimit', 'DruglicenseNo'].includes(f)
        );
        console.log("requiredfields",requiredfields);
        
      
        let missingfield = requiredfields.filter((field) => !SupplierMaster[field]);
        console.log("missingfield",missingfield);
        if (missingfield.length !== 0) {
            const tdata = {
                message: `Please fill out all required fields: ${missingfield.join(", ")}`,
                type: 'warn',
            };
            dispatchvalue({ type: 'toast', value: tdata });
        } 
        
        else {
            const senddataaaa = {
                ...SupplierMaster,
                created_by: userRecord?.username
            }
            console.log(senddataaaa);

            axios.post(`${UrlLink}Inventory/Supplier_Master_Link`, senddataaaa)
                .then((res) => {
                    console.log(res.data);
                    let resdata = res.data
                    let type = Object.keys(resdata)[0]
                    let mess = Object.values(resdata)[0]
                    const tdata = {
                        message: mess,
                        type: type,
                    }
                    dispatchvalue({ type: 'toast', value: tdata });
                    if (type === 'success') {
                        navigate("/Home/InventoryMaster");
                        dispatchvalue({ type: "HrFolder", value: "SupplierMasterList" });
                        dispatchvalue({ type: "setPreviousFolder", value: null }); 
                        dispatchvalue({ type: "showMenu", value: true });
                        // navigate('/Home/SupplierMasterList');
                    }
                })
                .catch((err) => {
                    console.log(err);
                })
        }
    
    
    }


    return (
        <>
            <div className="Main_container_app">
                <h3>Supplier Master</h3>

                <div className="common_center_tag">
                    <span>Supplier Details</span>
                </div>

                <br />

                <div className="RegisFormcon_1">
                    {Object.keys(SupplierMaster)
                        .filter((f) => !['SupplierId', 'BankName', 'AccountNumber', 'IFSCCode', 'BankBranch'].includes(f))
                        .map((StateName, Index) => (
                            <div className="RegisForm_1" key={Index + 'key'}>
                                <label htmlFor={StateName}>
                                    <div className="imp_v_star">
                                        {['SupplierName', 'ContactNumber', 'EmailAddress', 'Address', 'RegistrationNumber', 'GSTNumber', 'PANNumber', 'PaymentTerms', 'LeadTime', 'BankName', 'AccountNumber', 'IFSCCode', 'BankBranch'].includes(StateName) ? (
                                            <>
                                                {formatLabel(StateName)}
                                                <span className="requirreg12">*</span>
                                            </>
                                        )
                                            : (
                                                formatLabel(StateName)
                                            )}
                                    </div>
                                    {StateName === 'LeadTime' ? '(days)' : StateName === 'PaymentTerms' ? '(Due days)' : ''}
                                    <span>:</span>
                                </label>

                                {['Address', 'Notes'].includes(StateName) ? (
                                    <textarea
                                        id={StateName}
                                        name={StateName}
                                        value={SupplierMaster[StateName]}
                                        onChange={handleInputChange}
                                    />
                                ) : StateName === 'SupplierType' ? (
                                    <select
                                        id={StateName}
                                        name={StateName}
                                        value={SupplierMaster[StateName]}
                                        onChange={handleInputChange}
                                    >
                                        <option value="">Select</option>
                                        <option value="Manufacturer">Manufacturer</option>
                                        <option value="Distributor">Distributor</option>
                                        <option value="Wholesaler">Wholesaler</option>
                                        <option value="Retailer">Retailer</option>
                                        <option value="OEM">OEM (Original Equipment Manufacturer)</option>
                                        <option value="Vendor">Vendor</option>
                                    </select>
                                ) : StateName === 'FileAttachment' ? (
                                    <>
                                        <input
                                            type="file"
                                            name={StateName}
                                            accept="image/jpeg,image/png,application/pdf"
                                            required
                                            id={`${StateName}_supplier`}
                                            autoComplete="off"
                                            onChange={handlefileOnchange}
                                            style={{ display: 'none' }}
                                        />
                                        <div
                                            style={{
                                                width: '87px',
                                                display: 'flex',
                                                justifyContent: 'flex-start',
                                                gap: '10px',
                                            }}
                                        >
                                            <label
                                                htmlFor={`${StateName}_supplier`}
                                                className="RegisterForm_1_btns choose_file_update"
                                            >
                                                <PhotoCameraBackIcon />
                                            </label>
                                            <button
                                                type="button"
                                                className="RegisterForm_1_btns choose_file_update"
                                                onClick={() => Selectedfileview(SupplierMaster.FileAttachment)}
                                            >
                                                <VisibilityIcon />
                                            </button>
                                        </div>
                                    </>
                                ) : (
                                    <input
                                        type={getInputType(StateName)}
                                        onKeyDown={getInputType(StateName) === 'number' ? BlockInvalidcharecternumber : null}
                                        id={StateName}
                                        name={StateName}
                                        value={SupplierMaster[StateName]}
                                        onChange={handleInputChange}
                                    />
                                )}
                            </div>
                        ))}
                </div>

                <br />
                <div className="common_center_tag">
                    <span>Bank Details</span>
                </div>
                <br />
                <div className="RegisFormcon_1">
                    {['BankName', 'AccountNumber', 'IFSCCode', 'BankBranch'].map((StateName2, Index) => (
                        <div className="RegisForm_1" key={Index + 'key'}>
                            <label htmlFor={StateName2}>
                                <div className="imp_v_star">
                                    {formatLabel(StateName2)}
                                    <span className="requirreg12">*</span> {/* Adds the required asterisk */}
                                </div>
                                <span>:</span>
                            </label>
                            <input
                                type={getInputType(StateName2)}
                                id={StateName2}
                                name={StateName2}
                                value={SupplierMaster[StateName2]}
                                onChange={handleInputChange}
                            />
                        </div>
                    ))}
                </div>


                <br />

                <div className="Main_container_Btn">
                    <button onClick={saveSupplierdata}>{SupplierMaster.SupplierId ? 'Update' : 'Save'}</button>
                </div>
            </div>
            <ToastAlert Message={toast.message} Type={toast.type} />
            <ModelContainer />
        </>
    );
}

export default SupplierMaster;
