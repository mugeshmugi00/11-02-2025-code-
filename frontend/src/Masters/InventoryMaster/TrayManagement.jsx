
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useSelector, useDispatch } from 'react-redux';
import ToastAlert from '../../OtherComponent/ToastContainer/ToastAlert';
import { useNavigate } from 'react-router-dom';


const TrayManagement = () => {

    const UrlLink = useSelector(state => state.userRecord?.UrlLink);

    const toast = useSelector(state => state.userRecord?.toast);
    const userRecord = useSelector((state) => state.userRecord?.UserData);

    const navigate = useNavigate();

    const dispatchvalue = useDispatch();




    const [TrayArray, setTrayArray] = useState([])

    const [ShelfArray, setShelfArray] = useState([])

    const [RackArray, setRackArray] = useState([])

    const [LocationData, setLocationData] = useState([]);

    const [StoreData, setStoreData] = useState([])

    const [ProductArray, setProductArray] = useState([])


    const [mapingState, setmapingState] = useState({
        Location: '',
        StoreLocation: '',
        RackName: '',
        ShelfName: '',
        TrayName: '',
    })



    const [Productmapstate, setProductmapstate] = useState({
        ItemCode: '',
        ItemName: '',
        ProductCategory: '',
        SubCategory: '',
    });



    useEffect(() => {

        if (userRecord && Object.keys(userRecord).length !== 0) {

            setmapingState((prev) => ({
                ...prev,
                Location: userRecord?.location,
            }))

        }

    }, [userRecord])

    useEffect(() => {

        axios.get(`${UrlLink}Inventory/GET_Product_Detials_For_Tray_link`)
            .then((res) => {
                // console.log('eeeeee',res.data);
                let data = res.data;

                if (data && Array.isArray(data)) {
                    setProductArray(data)
                }
            })
            .catch((err) => {
                console.log(err);
            })

    }, [UrlLink])



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




    useEffect(() => {

        if (mapingState.Location !== '') {
            axios.get(`${UrlLink}Masters/Inventory_Master_Detials_link?SearchLocation=${mapingState.Location}`)
                .then((res) => {
                    const ress = res.data
                    setStoreData(ress)
                })
                .catch((err) => {
                    console.log(err);
                })
        }

        if (mapingState.Location !== '' && mapingState.StoreLocation !== 0) {

            const params = {
                SearchLocation: mapingState.Location,
                StoreLocation: mapingState.StoreLocation,
                Statuschek: 'Statuschek',
            };

            axios.get(`${UrlLink}Masters/Rack_Detials_link`, { params })
                .then((res) => {
                    console.log('kkkk', res.data);

                    let data = res.data

                    if (Array.isArray(data) && data.length !== 0) {
                        setRackArray(data)
                    }
                    else {
                        setRackArray([])
                    }

                })
                .catch((err) => {
                    console.log(err);
                })
        }

        if (mapingState.Location !== '' && mapingState.StoreLocation !== 0 && mapingState.RackName !== 0) {

            const params = {
                SearchLocation: mapingState.Location,
                StoreLocation: mapingState.StoreLocation,
                RackName: mapingState.RackName,
                Statuschek: 'Statuschek',
            };

            axios.get(`${UrlLink}Masters/Shelf_Detials_link`, { params })
                .then((res) => {
                    // console.log(res.data);
                    let data = res.data

                    if (Array.isArray(data) && data.length !== 0) {
                        setShelfArray(data)
                    }
                    else {
                        setShelfArray([])
                    }

                })
                .catch((err) => {
                    console.log(err);
                })

        }

        if (mapingState.Location !== '' && mapingState.StoreLocation !== 0
            && mapingState.RackName !== 0 && mapingState.ShelfName !== 0) {


            const params = {
                SearchLocation: mapingState.Location,
                StoreLocation: mapingState.StoreLocation,
                RackName: mapingState.RackName,
                ShelfName: mapingState.ShelfName,
                Statuschek: 'Statuschek',
                BookingStatus: 'Available'
            };

            axios.get(`${UrlLink}Masters/Tray_Detials_link`, { params })
                .then((res) => {
                    let data = res.data
                    // console.log('0000',data);
                    if (Array.isArray(data) && data.length !== 0) {
                        setTrayArray(data)
                    }
                    else {
                        setTrayArray([])
                    }
                })
                .catch((err) => {
                    console.log(err);
                })
        }


    }, [UrlLink, mapingState])






    const formatLabel = (label) => {

        if (/[a-z]/.test(label) && /[A-Z]/.test(label) && !/\d/.test(label)) {
            return label
                .replace(/([a-z])([A-Z])/g, "$1 $2")
                .replace(/^./, (str) => str.toUpperCase());
        } else {
            return label;
        }
    };


    const HandelChange = (e) => {

        const { name, value } = e.target
        if (name === 'StoreLocation') {

            setmapingState((prev) => ({
                ...prev,
                [name]: value,
                RackName: '',
                ShelfName: '',
                TrayName: '',
            }))
        }
        else if (name === 'RackName') {

            setmapingState((prev) => ({
                ...prev,
                [name]: value,
                ShelfName: '',
                TrayName: '',
            }))
        }
        else if (name === 'ShelfName') {

            setmapingState((prev) => ({
                ...prev,
                [name]: value,
                TrayName: '',
            }))
        }
        else {
            setmapingState((prev) => ({
                ...prev,
                [name]: value
            }))
        }

    }

    const HandelItemChange = (e) => {

        const { name, value } = e.target

        if (name === 'ItemCode') {

            let findItem = ProductArray.find((ele) => +ele.Item_Code === +value)

            if (findItem) {
                setProductmapstate((prev) => ({
                    ...prev,
                    [name]: value,
                    ItemName: findItem.Item_Name,
                    ProductCategory: findItem.Product_Category,
                    SubCategory: findItem.Sub_Category,
                }))
            }
            else {
                setProductmapstate((prev) => ({
                    ...prev,
                    [name]: value,
                    ItemName: '',
                    ProductCategory: '',
                    SubCategory: '',
                }))
            }

        }
        else if (name === 'ItemName') {

            let findItem = ProductArray.find((ele) => ele.Item_Name === value)

            if (findItem) {
                setProductmapstate((prev) => ({
                    ...prev,
                    [name]: value,
                    ItemCode: findItem.Item_Code,
                    ProductCategory: findItem.Product_Category,
                    SubCategory: findItem.Sub_Category,
                }))
            }
            else {
                setProductmapstate((prev) => ({
                    ...prev,
                    [name]: value,
                    ItemCode: '',
                    ProductCategory: '',
                    SubCategory: '',
                }))
            }

        }
        else {

            setProductmapstate((prev) => ({
                ...prev,
                [name]: value,
            }))
        }

    }


    const HandelSave = () => {

        if (mapingState.TrayName === '' || Productmapstate.ItemCode === '') {
            const tdata = {
                message: 'TrayName and ItemName mandatory',
                type: 'warn',
            }

            dispatchvalue({ type: 'toast', value: tdata });
        }
        else {
            let Senddata = {
                ...mapingState,
                ...Productmapstate,
                created_by: userRecord?.username || '',
            }


            axios.post(`${UrlLink}Masters/Difine_Tray_For_Products`, Senddata)
                .then((res) => {
                    console.log(res.data)

                    let resdata = res.data
                    let type = Object.keys(resdata)[0]
                    let mess = Object.values(resdata)[0]
                    const tdata = {
                        message: mess,
                        type: type,
                    }

                    dispatchvalue({ type: 'toast', value: tdata });

                    if (type === 'success') {
                        // navigate('/Home/TrayManagementList');
                        navigate("/Home/InventoryMaster");
                        dispatchvalue({ type: "HrFolder", value: "TrayManagementList" });
                        dispatchvalue({ type: "setPreviousFolder", value: null }); 
                        dispatchvalue({ type: "showMenu", value: true });

                    }
                    else if (type === 'Update') {

                        let ItemConfirmed = window.confirm(mess);

                        if (ItemConfirmed) {

                            let Senddata = {
                                ...mapingState,
                                ...Productmapstate,
                                created_by: userRecord?.username || '',
                                ItemConfirmed: ItemConfirmed,
                            }


                            axios.post(`${UrlLink}Masters/Difine_Tray_For_Products`, Senddata)
                                .then((res) => {
                                    console.log(res.data)

                                    let resdata = res.data
                                    let type = Object.keys(resdata)[0]
                                    let mess = Object.values(resdata)[0]
                                    const tdata = {
                                        message: mess,
                                        type: type,
                                    }

                                    dispatchvalue({ type: 'toast', value: tdata });

                                    if (type === 'success') {
                                        navigate('/Home/TrayManagementList');
                                    }

                                })
                                .catch((err) => {
                                    console.log(err);
                                })



                        }

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
                <h3>Tray Management</h3>
                <div className="common_center_tag">
                    <span>Tray Detailes</span>
                </div>
                <br />

                <div className="RegisFormcon_1">
                    {
                        Object.keys(mapingState).filter((ele) => ele !== 'id').map((StateName, ind) => {

                            let OprationArray = []

                            switch (StateName) {
                                case 'Location':
                                    OprationArray = LocationData;
                                    break;
                                case 'StoreLocation':
                                    OprationArray = StoreData;
                                    break;
                                case 'RackName':
                                    OprationArray = RackArray;
                                    break;
                                case 'ShelfName':
                                    OprationArray = ShelfArray;
                                    break;
                                case 'TrayName':
                                    OprationArray = TrayArray;
                                    break;
                                default:
                                    OprationArray = []

                            }


                            return (
                                <div className="RegisForm_1" key={ind + 'key'}>
                                    <label htmlFor={StateName}>{formatLabel(StateName)} <span>:</span></label>

                                    <select
                                        id={StateName}
                                        name={StateName}
                                        value={mapingState[StateName]}
                                        onChange={HandelChange}
                                        disabled={(mapingState.StoreLocation === '' && StateName === 'RackName') || (mapingState.RackName === '' && StateName === 'ShelfName') ||
                                            (mapingState.ShelfName === '' && StateName === 'TrayName') || StateName === 'Location'
                                        }
                                    >
                                        <option value=''>Select</option>
                                        {
                                            OprationArray.map((option, index) => (
                                                <option key={index} value={option.id}>
                                                    {StateName === 'RackName' ? option.RackName :
                                                        StateName === 'ShelfName' ? option.Shelf_Name :
                                                            StateName === 'TrayName' ? option.Tray_Name :
                                                                StateName === 'Location' ? option.locationName :
                                                                    StateName === 'StoreLocation' ? option.StoreName : ''}

                                                </option>
                                            ))
                                        }
                                    </select>
                                </div>
                            )
                        })
                    }
                </div>

                <br />
                <div className="common_center_tag">
                    <span>Product Detailes</span>
                </div>
                <br />


                <div className="RegisFormcon_1">

                    {Object.keys(Productmapstate).map((StateName, Ind) => (

                        <div className="RegisForm_1" key={Ind + 'key'}>
                            <label htmlFor={StateName}>{formatLabel(StateName)} <span>:</span></label>
                            {
                                <>
                                    <input
                                        id={StateName}
                                        name={StateName}
                                        value={Productmapstate[StateName]}
                                        onChange={HandelItemChange}
                                        type='text'
                                        list={StateName + 'List'}
                                        disabled={['ProductCategory', 'SubCategory'].includes(StateName)}
                                    />
                                    <datalist
                                        id={StateName + 'List'}
                                    >
                                        {
                                            ProductArray.map((option, index) => (
                                                <option key={index + 'key'} value={StateName === 'ItemCode' ? option.Item_Code : option.Item_Name}>
                                                </option>
                                            ))
                                        }
                                    </datalist>
                                </>
                            }


                        </div>

                    ))

                    }

                </div>
                <br />
                <div className="Main_container_Btn">
                    <button
                        onClick={HandelSave}
                    >
                        {mapingState.id ? 'Update' : 'Save'}
                    </button>
                </div>

            </div>
            <ToastAlert Message={toast.message} Type={toast.type} />
        </>
    )
}

export default TrayManagement
