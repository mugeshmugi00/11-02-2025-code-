import React, { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux';
import ReactGrid from '../../OtherComponent/ReactGrid/ReactGrid';
import Button from "@mui/material/Button";
import EditIcon from "@mui/icons-material/Edit";
import ToastAlert from '../../OtherComponent/ToastContainer/ToastAlert';
import axios from 'axios';


const RoomMaster = () => {
    const dispatchvalue = useDispatch();
    const UrlLink = useSelector(state => state.userRecord?.UrlLink);
    const userRecord = useSelector((state) => state.userRecord?.UserData);
    const toast = useSelector(state => state.userRecord?.toast);
    const [LocationData, setLocationData] = useState([]);
    const [IsBuildingGet, setIsBuildingGet] = useState(false)

    const [MasterOptions, setMasterOptions] = useState('Room')

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

    const [RoomName, setRoomName] = useState({

        Location: '',
        BuildingName: '',
        BlockName: '',
        FloorName: '',
        WardName: '',
        RoomCharge: 0,
        DoctorCharges: 0,
        NurseCharges: 0,
        // GST: 'Nill',
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
                RoomCharge: 0,
                DoctorCharges: 0,
                NurseCharges: 0,
                // GST: 'Nill',
            }))
        } else if (name === 'BuildingName') {
            setRoomName((prev) => ({
                ...prev,
                [name]: value,
                BlockName: '',
                FloorName: '',
                WardName: '',
                RoomCharge: 0,
                DoctorCharges: 0,
                NurseCharges: 0,
                // GST: 'Nill',
            }))
        } else if (name === 'BlockName') {
            setRoomName((prev) => ({
                ...prev,
                [name]: value,
                FloorName: '',
                WardName: '',
                RoomCharge: 0,
                DoctorCharges: 0,
                NurseCharges: 0,
                // GST: 'Nill',
            }))
        } else if (name === 'FloorName') {
            setRoomName((prev) => ({
                ...prev,
                [name]: value,
                WardName: '',
                RoomCharge: 0,
                DoctorCharges: 0,
                NurseCharges: 0,
                // GST: 'Nill',
            }))
        } else if (name === 'WardName') {
            setRoomName((prev) => ({
                ...prev,
                [name]: value,
                RoomCharge: 0,
                DoctorCharges: 0,
                NurseCharges: 0,
                // GST: 'Nill',
            }))
        } else if (name === 'RoomCharge') {
            if (+value < 5000) {
                setRoomName((prev) => ({
                    ...prev,
                    [name]: value.toUpperCase(),
                    // GST: 'Nill'
                }))

            } else {
                setRoomName((prev) => ({
                    ...prev,
                    [name]: value.toUpperCase(),
                    // GST: ''
                }))

            }
        } else {
            setRoomName((prev) => ({
                ...prev,
                [name]: value.toUpperCase()
            }))
        }

    }

    const RoomColumns = [
        {
            key: "id",
            name: "Ward Id",
            frozen: true
        },
        {
            key: "Location_Name",
            name: "Location",
            frozen: true
        },
        {
            key: "BuildingName",
            name: "Building Name",
        },
        {
            key: "BlockName",
            name: "Block Name",
        },
        {
            key: "FloorName",
            name: "Floor Name",
        },
        {
            key: "WardName",
            name: "Ward Name",
        },
        {
            key: "RoomCharge",
            name: "Room Charge",
            children: [
                {
                    key: "Prev_Charge",
                    name: "Previous Charge",
                    width: 120
                },
                {
                    key: "Current_Charge",
                    name: "Current Charge",
                    width: 120
                },
            ]
        },
        // {
        //     key: "GST_val",
        //     name: "GST",
        // },
        {
            key: "TotalRoomCharge",
            name: "Total Room Charge",
            children: [
                {
                    key: "Total_Prev_Charge",
                    name: "Previous Charge",
                    width: 120
                },
                {
                    key: "Total_Current_Charge",
                    name: "Current Charge",
                    width: 120
                },
            ]
        },
        {
            key: "Status",
            name: "Status",
            frozen: true,
            renderCell: (params) => (
                <>
                    <Button
                        className="cell_btn"
                        onClick={() => HandleEditRoomStatus(params.row)}
                    >
                        {params.row.Status}
                    </Button>
                </>
            ),
        },
        {
            key: "Doctor_Charge",
            name: "Doctor Charges",
        },
        {
            key: "Nurse_Charge",
            name: "Nurse Charges",
        },
        {
            key: "Action",
            name: "Action",
            renderCell: (params) => (
                <>
                    <Button
                        className="cell_btn"
                        onClick={() => HandleEditRoom(params.row)}
                    >
                        <EditIcon className="check_box_clrr_cancell" />
                    </Button>
                </>
            ),
        }
    ]

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
            RoomCharge: Current_Charge,
            // GST: GST_val,
            RoomId: id,
        })
    }

    const HandleSaveRoom = () => {
        const exist = Object.keys(RoomName).filter(p => p !== 'RoomId' && p !== 'RoomCharge' &&  p !== 'DoctorCharges' &&  p !== 'NurseCharges' ).filter((field) => !RoomName[field])
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
                        RoomCharge: 0,
                        DoctorCharges: 0,
                        NurseCharges: 0,
                        // GST: 'Nill',
                        RoomId: '',

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
                console.log('111111', ress);

                setRoomData(ress)
            })
            .catch((err) => {
                console.log(err);
            })
    }, [IsBuildingGet, UrlLink])




    // room master  ------------

    const [RoomMasterName, setRoomMasterName] = useState({

        Location: '',
        BuildingName: '',
        BlockName: '',
        FloorName: '',
        WardName: '',
        BedCharge: '',
        // GST: '',
        TotalCharge: '',
        RoomNo: '',
        BedNo: '',
        RoomMasterId: '',
    })
    const [RoomMasterData, setRoomMasterData] = useState([])
    const [RoomMaster_Building_by__loc, setRoomMaster_Building_by__loc] = useState([])
    const [RoomMaster_block_by_Building, setRoomMaster_block_by_Building] = useState([])
    const [RoomMaster_Floor_by_Block, setRoomMaster_Floor_by_Block] = useState([])
    const [RoomMaster_ward_by_FLoor, setRoomMaster_ward_by_FLoor] = useState([])
    const [RoomMaster_Room_by_Ward, setRoomMaster_Room_by_Ward] = useState([])


    useEffect(() => {
        if (RoomMasterName.Location) {
            axios.get(`${UrlLink}Masters/get_building_Data_by_location?Location=${RoomMasterName.Location}`)
                .then(res => {
                    if (Array.isArray(res.data)) {
                        setRoomMaster_Building_by__loc(res.data)
                    } else {
                        setRoomMaster_Building_by__loc([])
                    }
                })
                .catch(err => {
                    setRoomMaster_Building_by__loc([])
                    console.log(err);
                })
        }

    }, [RoomMasterName.Location, UrlLink])

    useEffect(() => {
        if (RoomMasterName.BuildingName) {
            const data = {
                Building: RoomMasterName.BuildingName,
            }
            axios.get(`${UrlLink}Masters/get_block_Data_by_Building`, { params: data })
                .then(res => {
                    if (Array.isArray(res.data)) {
                        setRoomMaster_block_by_Building(res.data)
                    } else {
                        setRoomMaster_block_by_Building([])
                    }
                })
                .catch(err => {
                    setRoomMaster_block_by_Building([])
                    console.log(err);
                })
        }

    }, [RoomMasterName.BuildingName, UrlLink])

    useEffect(() => {
        if (RoomMasterName.BlockName) {
            const data = {
                Block: RoomMasterName.BlockName,
            }
            axios.get(`${UrlLink}Masters/get_Floor_Data_by_Building_block_loc`, { params: data })
                .then(res => {
                    if (Array.isArray(res.data)) {
                        setRoomMaster_Floor_by_Block(res.data)
                    } else {
                        setRoomMaster_Floor_by_Block([])
                    }

                })
                .catch(err => {
                    setRoomMaster_Floor_by_Block([])
                    console.log(err);
                })
        }

    }, [RoomMasterName.BlockName, UrlLink])

    useEffect(() => {
        if (RoomMasterName.FloorName) {
            const data = {

                Floor: RoomMasterName.FloorName,
            }
            axios.get(`${UrlLink}Masters/get_Ward_Data_by_Building_block_Floor_loc`, { params: data })
                .then(res => {

                    if (Array.isArray(res.data)) {
                        setRoomMaster_ward_by_FLoor(res.data)
                    } else {
                        setRoomMaster_ward_by_FLoor([])
                    }
                })
                .catch(err => {
                    setRoomMaster_ward_by_FLoor([])
                    console.log(err);
                })
        }

    }, [RoomMasterName.FloorName, UrlLink])

    useEffect(() => {
        if (RoomMasterName.WardName) {
            const data = {
                Ward: RoomMasterName.WardName,
            }
            axios.get(`${UrlLink}Masters/get_RoomType_Data_by_Building_block_Floor_ward_loc`, { params: data })
                .then(res => {
                    if (Array.isArray(res.data)) {

                        console.log('111111111', res.data);
                        setRoomMaster_Room_by_Ward(res.data)
                    } else {
                        setRoomMaster_Room_by_Ward([])
                    }

                })
                .catch(err => {
                    setRoomMaster_Room_by_Ward([])
                    console.log(err);
                })
        }

    }, [RoomMasterName.WardName, UrlLink])

    useEffect(() => {
        if (RoomMaster_Room_by_Ward.length > 0 && RoomMasterName.WardName) {
            console.log(RoomMaster_Room_by_Ward, 'RoomMaster_Room_by_Ward');
            console.log(RoomMasterName.WardName, 'RoomMasterName.WardName');
            
            const datass = RoomMaster_Room_by_Ward.find(p => p.id1 === + RoomMasterName.WardName);
            console.log(datass, 'Matching RoomMaster_Room_by_Ward item');
        }
    }, [RoomMaster_Room_by_Ward, RoomMasterName.WardName]);

    const handlechangeRoomMaster = (e) => {
        const { name, value } = e.target
        if (name === 'Location') {
            setRoomMasterName((prev) => ({
                ...prev,
                [name]: value,
                BuildingName: '',
                BlockName: '',
                FloorName: '',
                WardName: '',
                BedCharge: '',
                GST: '',
                TotalCharge: '',
                RoomNo: '',
                BedNo: '',
            }))
        } else if (name === 'BuildingName') {
            setRoomMasterName((prev) => ({
                ...prev,
                [name]: value,
                BlockName: '',
                FloorName: '',
                WardName: '',
                BedCharge: '',
                GST: '',
                TotalCharge: '',
                RoomNo: '',
                BedNo: '',
            }))
        } else if (name === 'BlockName') {
            setRoomMasterName((prev) => ({
                ...prev,
                [name]: value,
                FloorName: '',
                WardName: '',
                BedCharge: '',
                GST: '',
                TotalCharge: '',
                RoomNo: '',
                BedNo: '',
            }))
        } else if (name === 'FloorName') {
            setRoomMasterName((prev) => ({
                ...prev,
                [name]: value,
                WardName: '',
                BedCharge: '',
                GST: '',
                TotalCharge: '',
                RoomNo: '',
                BedNo: '',
            }))
        }
        // else if (name === 'WardName') {
        //     setRoomMasterName((prev) => ({
        //         ...prev,
        //         [name]: value,
        //         BedCharge: '',
        //         GST: '',
        //         TotalCharge: '',
        //         RoomNo: '',
        //         BedNo: '',
        //     }))
        // } 
        else if (name === 'WardName') {
            if (value) {
                axios.get(`${UrlLink}Masters/get_RoomType_Data_by_Building_block_Floor_ward_loc?Ward=${value}`)
                    .then(res => {
                        if (Array.isArray(res.data)) {

                            console.log('111111111', res.data);
                            setRoomMaster_Room_by_Ward(res.data)

                            const datass = res?.data.find(p => p.id1 === +value)
                            console.log(datass, 'value', value);
                            setRoomMasterName((prev) => ({
                                ...prev,
                                [name]: value,
                                BedCharge: datass?.BedCharge,
                                GST: datass?.GST,
                                TotalCharge: datass?.TotalCharge,
                                RoomNo: '',
                                BedNo: '',
                            }))
                        } else {
                            setRoomMaster_Room_by_Ward([])
                            setRoomMasterName((prev) => ({
                                ...prev,
                                [name]: value,
                                BedCharge: "",
                                GST: "",
                                TotalCharge: "",
                                RoomNo: '',
                                BedNo: '',
                            }))
                        }

                    })
                    .catch(err => {
                        setRoomMaster_Room_by_Ward([])
                        console.log(err);
                    })

            } else {
                setRoomMasterName((prev) => ({
                    ...prev,
                    [name]: value,
                    BedCharge: '',
                    GST: '',
                    TotalCharge: '',
                    RoomNo: '',
                    BedNo: '',
                }))
            }

        }
        else {
            setRoomMasterName((prev) => ({
                ...prev,
                [name]: value.toUpperCase()
            }))
        }



    }

    const RoomMasterColumns = [
        {
            key: "id",
            name: "Room Master Id",
            frozen: true
        },
        {
            key: "LocationName",
            name: "Location",
            frozen: true
        },
        {
            key: "BuildingName",
            name: "Building Name",
        },
        {
            key: "BlockName",
            name: "Block Name",
        },
        {
            key: "FloorName",
            name: "Floor Name",
        },
        {
            key: "WardName",
            name: "Ward Name",
        },
        {
            key: "RoomNo",
            name: "Room No",
        },
        {
            key: "BedNo",
            name: "Bed No",
        },
        {
            key: "BedCharge",
            name: "Bed Charge",
        },
        // {
        //     key: "GST",
        //     name: "GST",
        // },
        {
            key: "TotalCharge",
            name: "Total Charge",
        },

        {
            key: "Status",
            name: "Status",
            frozen: true,
            renderCell: (params) => (
                <>
                    <Button
                        className="cell_btn"
                        onClick={() => handleeditRoomMasterstatus(params.row)}
                    >
                        {params.row.Status}
                    </Button>
                </>
            ),
        },
        {
            key: "Action",
            name: "Action",
            renderCell: (params) => (
                <>
                    <Button
                        className="cell_btn"
                        onClick={() => handleeditRoomMaster(params.row)}
                    >
                        <EditIcon className="check_box_clrr_cancell" />
                    </Button>
                </>
            ),
        }
    ]
    const handleeditRoomMasterstatus = (params) => {
        const data = {
            RoomMasterId: params.id,
            Statusedit: true
        }
        const conformation = window.confirm('Are you sure ,want to update the status')
        if (conformation) {
            axios.post(`${UrlLink}Masters/Room_Master_Master_Detials_link`, data)
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
    const handleeditRoomMaster = (params) => {
        const { id, ...rest } = params
        console.log(rest);
        setRoomMasterName((prev) => ({
            ...prev,
            RoomMasterId: id,
            BuildingName: rest.BuildingId,
            BlockName: rest.BlockId,
            FloorName: rest.FloorId,
            WardName: rest.WardId,
            // RoomName: rest.RoomId,
            Location: rest.LocationId,
            BedCharge: rest.BedCharge,
            // GST: rest.GST,
            TotalCharge: rest.TotalCharge,
            RoomNo: rest.RoomNo,
            BedNo: rest.BedNo,

        }))
    }
    const HandleSaveRoomMaster = () => {
        const exist = Object.keys(RoomMasterName).filter(p => p !== 'RoomMasterId').filter((field) => !RoomMasterName[field])
        if (exist.length === 0) {


            const data = {
                ...RoomMasterName,
                created_by: userRecord?.username || ''
            }
            axios.post(`${UrlLink}Masters/Room_Master_Master_Detials_link`, data)
                .then((res) => {
                    const resres = res.data
                    console.log(resres, '----');
                    let typp = Object.keys(resres)[0]
                    let mess = Object.values(resres)[0]
                    const tdata = {
                        message: mess,
                        type: typp,
                    }

                    dispatchvalue({ type: 'toast', value: tdata });
                    setIsBuildingGet(prev => !prev)
                    setRoomMasterName({
                        Location: '',
                        BuildingName: '',
                        BlockName: '',
                        FloorName: '',
                        WardName: '',
                        BedCharge: '',
                        GST: '',
                        TotalCharge: '',
                        RoomNo: '',
                        BedNo: '',
                        RoomMasterId: '',

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
        axios.get(`${UrlLink}Masters/Room_Master_Master_Detials_link`)
            .then((res) => {
                const ress = res.data
                console.log('22222222',ress);
                
                setRoomMasterData(ress)
            })
            .catch((err) => {
                console.log(err);
            })
    }, [IsBuildingGet, UrlLink])


    return (
        <>
            <div className="Main_container_app">
                <h3>Room Master</h3>
                <div className="RegisterTypecon">
                    <div className="RegisterType">
                        {["Room", "Bed"].map((p, ind) => (
                            <div className="registertypeval" key={ind}>
                                <input
                                    type="radio"
                                    id={p}
                                    name="appointment_type"
                                    checked={MasterOptions === p}
                                    onChange={(e) => {
                                        setMasterOptions(e.target.value)
                                    }}
                                    value={p}
                                />
                                <label htmlFor={p}>
                                    {p}
                                </label>
                            </div>
                        ))}
                    </div>

                </div>

                <br />



                {/*-----------------------------Room Name-----------------------------------------------------------------------*/}

                {MasterOptions === 'Room' &&
                    <>
                        {/* <div className="common_center_tag">
                    <span>Room Name</span>
                </div>   */}
                        {/* <br/> */}
                        <div className="RegisFormcon_1">
                            {Object.keys(RoomName).filter(p => p !== 'RoomId').map((field, indx) => (
                                <div className="RegisForm_1" key={indx}>
                                    <label> {formatLabel(field)} <span>:</span> </label>
                                    {
                                        (field === 'GST' && (parseInt(RoomName.RoomCharge, 0) < 5000 || RoomName.RoomCharge === '')) || field === 'RoomCharge' || field === 'DoctorCharges' || field === 'NurseCharges' ?
                                            <input
                                                type={field === 'RoomCharge' || field === 'DoctorCharges' || field === 'NurseCharges' ? 'number' : 'text'}
                                                name={field}
                                                onKeyDown={(e) => (field === 'RoomCharge' || field === 'DoctorCharges' || field === 'NurseCharges') && (['+', '-', 'e', 'E'].includes(e.key) && e.preventDefault())}
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
                                                {/* {field === 'GST' &&
                                                    <>
                                                        <option value='28'>28 %</option>
                                                        <option value='18'>18 %</option>
                                                        <option value='12'>12 %</option>
                                                        <option value='5'>5 %</option>
                                                    </>
                                                } */}
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
                        <ReactGrid columns={RoomColumns} RowData={RoomData} />
                    </>
                }
                {/* -----------room master -------*/}
                {MasterOptions === 'Bed' &&
                    <>
                        <div className="common_center_tag">
                            <span>Room Master</span>
                        </div>
                        <br />
                        <div className="RegisFormcon_1">
                            {
                                Object.keys(RoomMasterName).filter(p => !['RoomMasterId'].includes(p)).map((field, indx) => (
                                    <div className="RegisForm_1" key={indx}>
                                        <label> {formatLabel(field)} <span>:</span> </label>
                                        {
                                            ['RoomNo', 'BedNo', 'BedCharge', 'TotalCharge'].includes(field) ?
                                                <input
                                                    type={'text'}
                                                    name={field}
                                                    autoComplete='off'
                                                    required
                                                    readOnly={['BedCharge', 'GST', 'TotalCharge'].includes(field)}
                                                    value={RoomMasterName[field]}
                                                    onChange={handlechangeRoomMaster}
                                                />
                                                :
                                                <select
                                                    name={field}
                                                    required
                                                    disabled={RoomMasterName.RoomMasterId}
                                                    value={RoomMasterName[field]}
                                                    onChange={handlechangeRoomMaster}
                                                >
                                                    <option value=''>Select</option>
                                                    {field === 'BuildingName' &&
                                                        RoomMaster_Building_by__loc.map((p, index) => (
                                                            <option key={index} value={p.id}>{p.BuildingName}</option>
                                                        ))
                                                    }
                                                    {field === 'BlockName' &&
                                                        RoomMaster_block_by_Building.map((p, index) => (
                                                            <option key={index} value={p.id}>{p.BlockName}</option>
                                                        ))
                                                    }
                                                    {field === 'FloorName' &&
                                                        RoomMaster_Floor_by_Block.map((p, index) => (
                                                            <option key={index} value={p.id}>{p.FloorName}</option>
                                                        ))
                                                    }
                                                    {field === 'WardName' &&
                                                        RoomMaster_ward_by_FLoor.map((p, index) => (
                                                            <option key={index} value={p.id}>{p.WardName}</option>
                                                        ))
                                                    }
                                                    {/* {field === 'RoomName' &&
                                                RoomMaster_Room_by_Ward.map((p, index) => (
                                                    <option key={index} value={p.id}>{p.RoomName}</option>
                                                ))
                                            } */}
                                                    {field === 'Location' &&
                                                        LocationData.map((p, index) => (
                                                            <option key={index} value={p.id}>{p.locationName}</option>
                                                        ))
                                                    }

                                                </select>
                                        }
                                    </div>
                                ))
                            }

                        </div>
                        <br />
                        <div className="Main_container_Btn">
                            <button onClick={HandleSaveRoomMaster}>
                                {RoomMasterName.RoomMasterId ? "Update" : "Add"}
                            </button>
                        </div>
                        <br />
                        <ReactGrid columns={RoomMasterColumns} RowData={RoomMasterData} />

                    </>
                }
            </div>
            <ToastAlert Message={toast.message} Type={toast.type} />
        </>
    )
}

export default RoomMaster;