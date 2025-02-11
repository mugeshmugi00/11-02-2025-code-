import axios from 'axios';
import React, { useCallback, useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { formatLabel } from '../../OtherComponent/OtherFunctions';
import ToastAlert from '../../OtherComponent/ToastContainer/ToastAlert';
import ReactGrid from '../../OtherComponent/ReactGrid/ReactGrid';
import Button from "@mui/material/Button";
import EditIcon from "@mui/icons-material/Edit";
import ManageSearchIcon from '@mui/icons-material/ManageSearch';

const SupplierProductMap = () => {

    const dispatchvalue = useDispatch();
    const navigate = useNavigate();
    const toast = useSelector(state => state.userRecord?.toast);
    const UrlLink = useSelector(state => state.userRecord?.UrlLink);
    const userRecord = useSelector((state) => state.userRecord?.UserData);
    const SupplierMasterStore = useSelector(state => state.Inventorydata?.SupplierMasterStore);
    const [ProductDetialsDataForMaping, setProductDetialsDataForMaping] = useState([])
    const [MappedProductDetialsData, setMappedProductDetialsData] = useState([])
    const [getdata, setgetdata] = useState(false)
    const [SupplierProductDetials, setSupplierProductDetials] = useState({
        ItemCode: '',
        ItemName: '',
        MRP: '',
        PurchaseRateBeforeGST: '',
        GST: 0,
        PurchaseRateAfterGST: '',
        pk: ''
    })

    useEffect(() => {
        if (Object.keys(SupplierMasterStore).length !== 0) {
            axios.get(`${UrlLink}Inventory/Supplier_product_Mapping_link`, {
                params: {
                    SupplierId: SupplierMasterStore?.SupplierId,
                    mappedProducts: true,
                    ItemCode: SupplierProductDetials.ItemCode,
                    ItemName: SupplierProductDetials.ItemName
                }
            })
                .then((res) => {
                    const resdata = res.data
                    setProductDetialsDataForMaping(Array.isArray(resdata) ? resdata : [])
                })
                .catch((err) => {
                    console.log(err);
                    setProductDetialsDataForMaping([])

                })
        }

    }, [SupplierProductDetials.ItemCode, SupplierProductDetials.ItemName, UrlLink, SupplierMasterStore])


    useEffect(() => {
        if (Object.keys(SupplierMasterStore).length === 0) {
            navigate('/Home/SupplierMasterList');
        } else {
            axios.get(`${UrlLink}Inventory/Supplier_product_Mapping_link?SupplierId=${SupplierMasterStore?.SupplierId}`)
                .then((res) => {
                    const resdata = res.data
                    console.log('resdata-=---',resdata);
                    
                    setMappedProductDetialsData(Array.isArray(resdata) ? resdata : [])
                })
                .catch((err) => {
                    console.log(err);
                    setMappedProductDetialsData([])

                })
        }
    }, [getdata, UrlLink, SupplierMasterStore])




    useEffect(() => {

        if(SupplierProductDetials.MRP && SupplierProductDetials.PurchaseRateBeforeGST)
        {
        let purchaserate = parseFloat(SupplierProductDetials.PurchaseRateBeforeGST, 0) || 0;
        let totalAmount

        let GSTValue = +SupplierProductDetials.GST;
        totalAmount = purchaserate + ((purchaserate * GSTValue) / 100);
            
        if (parseFloat(SupplierProductDetials.MRP) >= totalAmount) {
            setSupplierProductDetials((prev) => ({
                ...prev,
                PurchaseRateAfterGST: totalAmount.toFixed(3)
            }))
        } else {
            const tdata = {
                message: `The purchase rate after GST must be smaller than the MRP ${SupplierProductDetials.MRP}.`,
                type: 'warn',
            }
            dispatchvalue({ type: 'toast', value: tdata });
            setSupplierProductDetials((prev) => ({
                ...prev,
                PurchaseRateAfterGST: '',
                PurchaseRateAfterGST: ''
            }))
        }  
    }

    }, [SupplierProductDetials.GST, SupplierProductDetials.PurchaseRateBeforeGST, SupplierProductDetials.MRP])


    const handlesearchItems = (type = 'id') => {
        if (SupplierProductDetials.ItemCode || SupplierProductDetials.ItemName) {
            let find = ProductDetialsDataForMaping.find((ele) => "" + ele.id === SupplierProductDetials.ItemCode)
            if (type !== 'id') {
                find = ProductDetialsDataForMaping.find((ele) => "" + ele.ItemName === SupplierProductDetials.ItemName)
            }
            if (find) {
                const { id, ItemName, ...rest } = find
                setSupplierProductDetials((prev) => ({
                    pk: prev.pk,
                    ItemCode: id,
                    ItemName: ItemName,
                    ...rest,
                    MRP: '',
                    PurchaseRateBeforeGST: '',
                    GST:0,
                    PurchaseRateAfterGST: '',
                }))
            } else {
                const tdata = {
                    message: `Please enter valid Item Code or Item Name to search.`,
                    type: 'warn',
                }
                dispatchvalue({ type: 'toast', value: tdata });
            }
        } else {

            setSupplierProductDetials((prev) => ({
                pk: prev.pk,
                ItemCode: type === 'id' ? prev.ItemCode : '',
                ItemName: type !== 'id' ? prev.ItemName : '',
                MRP: '',
                PurchaseRateBeforeGST: '',
                GST:0,
                PurchaseRateAfterGST: '',
            }))
            const tdata = {
                message: `Please fill atleast any one of the Item Code or Item Name to search.`,
                type: 'warn',
            }
            dispatchvalue({ type: 'toast', value: tdata });
        }
    }

    const handleInputChange = (e) => {
        const { name, value } = e.target
        if (name === 'ItemCode') {

            setSupplierProductDetials((prev) => ({
                pk: prev.pk,
                [name]: value,
                ItemName: '',
                MRP: '',
                PurchaseRateBeforeGST: '',
                GST:0,
                PurchaseRateAfterGST: '',
            }))


        } else if (name === 'ItemName') {

            setSupplierProductDetials((prev) => ({
                pk: prev.pk,
                ItemCode: '',
                [name]: value,
                MRP: '',
                PurchaseRateBeforeGST: '',
                GST:0,
                PurchaseRateAfterGST: '',
            }))


        } else if (name === 'MRP') {
            setSupplierProductDetials((prev) => ({
                ...prev,
                [name]: value,
                PurchaseRateBeforeGST: '',
                GST:0,
                PurchaseRateAfterGST: ''
            }))
        } else {
            setSupplierProductDetials((prev) => ({
                ...prev,
                [name]: value
            }))
        }
    }
    const handlestatuschange = (params) => {
        const dataaa = {
            pk: params.SupplierPoductId,
            edit: true,
            statusedit: true
        }
        axios.post(`${UrlLink}Inventory/Supplier_product_Mapping_link`, dataaa)
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
                setgetdata(prev => !prev)
            })
            .catch((err) => {
                console.log(err);
            })
    }
    const HandelEditdata = (params) => {
        if (params.Status === 'Inactive') {
            const tdata = {
                message: `${params.ItemCode} - ${params.ItemName} is currently inactive. You need to activate it before editing.`,
                type: 'warn'
            };
            dispatchvalue({ type: 'toast', value: tdata });
        } else {
            const { id, SupplierPoductId,Is_Manufacture_Date_Available,Is_Expiry_Date_Available,PackType, PackQuantity, Status, ...data } = params
            setSupplierProductDetials({
                ...data,
                pk: SupplierPoductId,
            })
        }
    }

    const handlesaveproducts = () => {
        const senddata = {
            SupplierId: SupplierMasterStore?.SupplierId,
            ...SupplierProductDetials,
            created_by: userRecord?.username,
            edit: SupplierProductDetials.pk ? true : false
        }
        const missingFields = [
            'ItemCode',
            'ItemName',
            'MRP',
            'PurchaseRateBeforeGST',
            'PurchaseRateAfterGST',

        ].filter(field => !senddata[field])
        if (missingFields.length !== 0) {
            const tdata = {
                message: `Please fill out all required fields: ${missingFields.join(', ')}`,
                type: 'warn'
            }
            dispatchvalue({ type: 'toast', value: tdata })
        } else {
            axios.post(`${UrlLink}Inventory/Supplier_product_Mapping_link`, senddata)
                .then((res) => {
                    console.log(res.data);
                    let resdata = res.data
                    let type = Object.keys(resdata)[0]
                    let mess = Object.values(resdata)[0]
                    const tdata = {
                        message: mess,
                        type: type,
                    }
                    setProductDetialsDataForMaping([])
                    setSupplierProductDetials({
                        ItemCode: '',
                        ItemName: '',
                        MRP: '',
                        PurchaseRateBeforeGST: '',
                        GST:0,
                        PurchaseRateAfterGST: '',
                        pk: ''
                    })

                    dispatchvalue({ type: 'toast', value: tdata });
                    setgetdata(prev => !prev)
                })
                .catch((err) => {
                    console.log(err);
                })
        }

    }

    const SupplierProductColumn = [
        { key: 'id', name: 'S.No' },
        { key: 'ItemCode', name: 'ItemCode' },
        { key: 'ItemName', name: 'Item Name' },
        { key: 'ProductCategory', name: 'Product Category' },
        { key: 'SubCategory', name: 'Sub Category' },
        { key: 'ManufacturerName', name: 'Manufacturer Name' },
        { key: 'GenericName', name: 'Generic Name' },
        { key: 'HSNCode', name: 'HSN Code' },
        { key: 'MRP', name: 'MRP' },
        { key: 'PurchaseRateBeforeGST', name: 'Purchase Rate Before GST', width: 180 },
        { key: 'GST', name: 'GST' },
        { key: 'PurchaseRateAfterGST', name: 'Purchase Rate After GST', width: 180 },
        {
            key: 'Status',
            name: 'Status',
            renderCell: (params) => (
                <Button className="cell_btn" onClick={() => handlestatuschange(params.row)}>
                    {params.row.Status}
                </Button>
            )
        },
        {
            key: 'Action',
            name: 'Action',
            renderCell: (params) => (
                <Button className="cell_btn" onClick={() => HandelEditdata(params.row)}>
                    <EditIcon className="check_box_clrr_cancell" />
                </Button>
            )
        },
    ]
    return (
        <>
            <div className="Main_container_app">
                <h3>Supplier Product Mapping </h3>
                <br />
                <div className="common_center_tag">
                    <span>Supplier Details</span>
                </div>

                <br />
                <div className="RegisFormcon_1">
                    {
                        ['SupplierId', 'SupplierName', 'SupplierType', 'ContactPerson', 'ContactNumber'].map((StateName, Index) => {
                            return (
                                <div className="RegisForm_1" key={Index + 'key'}>
                                    <label htmlFor={StateName}> {formatLabel(StateName)} {StateName === 'LeadTime' ? '(days)' : StateName === 'PaymentTerms' ? '(Due days)' : ''}
                                        <span>:</span></label>

                                    <input
                                        type={'text'}
                                        id={StateName}
                                        name={StateName}
                                        value={SupplierMasterStore[StateName]}
                                        disabled
                                    />

                                </div>
                            )
                        })
                    }
                </div>
                <br />
                <div className="common_center_tag">
                    <span>Product Details</span>
                </div>
                <br />
                <div className="RegisFormcon_1">
                    {
                        Object.keys(SupplierProductDetials).filter(f => f !== 'pk').map((StateName, Index) => {
                            return (
                                <div className="RegisForm_1" key={Index + 'key'}>
                                    <label htmlFor={StateName}>
                                        {formatLabel(StateName)} {StateName === 'LeadTime' ? '(days)' : StateName === 'PaymentTerms' ? '(Due days)' : ''}
                                        <span>:</span>
                                    </label>

                                    {['GST'].includes(StateName) ?
                                        <select
                                            id={StateName}
                                            name={StateName}
                                            value={SupplierProductDetials[StateName]}
                                            onChange={handleInputChange}
                                            disabled={['ProductCategory', 'SubCategory'].includes(StateName) && SupplierProductDetials.pk}

                                        >
                                            <option value=''>Select</option>


                                            {StateName === 'GST' &&
                                                ['0', '5', '12', '18', '28'].map((field, indx) => (
                                                    <option key={indx} value={field}>{field}</option>

                                                ))

                                            }

                                        </select>
                                        :
                                        ['ItemCode', 'ItemName'].includes(StateName) ?
                                            <div className='Search_patient_icons'>
                                                <input
                                                    type={'text'}
                                                    id={StateName}
                                                    name={StateName}
                                                    list={`${StateName}_list`}
                                                    value={SupplierProductDetials[StateName]}
                                                    onChange={handleInputChange}
                                                    disabled={['ItemCode', 'ItemName'].includes(StateName) && SupplierProductDetials.pk}
                                                />
                                                <datalist id={`${StateName}_list`}>
                                                    {StateName === 'ItemCode' &&
                                                        ProductDetialsDataForMaping.map((field, indx) => (
                                                            <option key={indx} value={field.id}>
                                                                {`${field.id} | ${field.ItemName}`}
                                                            </option>
                                                        ))
                                                    }
                                                    {StateName === 'ItemName' &&
                                                        ProductDetialsDataForMaping.map((field, indx) => (
                                                            <option key={indx} value={field.ItemName}>
                                                                {`${field.id} | ${field.ItemName}`}
                                                            </option>
                                                        ))
                                                    }
                                                </datalist>

                                                <span onClick={(e) => handlesearchItems(StateName === 'ItemCode' ? 'id' : 'name')}>
                                                    <ManageSearchIcon />
                                                </span>

                                            </div> :
                                            <input
                                                type={['PurchaseRateBeforeGST', 'MRP',].includes(StateName) ? 'number' : 'text'}
                                                id={StateName}
                                                name={StateName}
                                                value={SupplierProductDetials[StateName]}
                                                onChange={handleInputChange}
                                                readOnly={['ProductCategory', 'SubCategory', 'ItemCode', 'ItemName'].includes(StateName) && SupplierProductDetials.pk}
                                                disabled={!['PurchaseRateBeforeGST', 'GST', 'MRP',].includes(StateName)}
                                            />
                                    }


                                </div>
                            )
                        })
                    }
                </div>
                <div className="Main_container_Btn">
                    <button onClick={handlesaveproducts}>
                        {SupplierProductDetials.pk ? "Update" : "Save"}
                    </button>
                </div>
                {console.log(MappedProductDetialsData)}

                <div className='RegisFormcon_1 jjxjx_'>
                    <ReactGrid columns={SupplierProductColumn} RowData={MappedProductDetialsData} />

                </div>

            </div>




            <ToastAlert Message={toast.message} Type={toast.type} />

        </>
    )
}

export default SupplierProductMap;