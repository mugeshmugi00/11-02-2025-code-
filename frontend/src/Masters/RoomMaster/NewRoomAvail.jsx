import React, { useState, useEffect, useCallback } from 'react'
import { useDispatch, useSelector } from 'react-redux';
import './NewRoomAvail.css'
import Tooltip from "@mui/material/Tooltip";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import axios from "axios";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBed } from "@fortawesome/free-solid-svg-icons";
import ReactGrid from '../../OtherComponent/ReactGrid/ReactGrid';
import { MdBlock } from "react-icons/md";

function CustomTooltip({ content, children }) {
  return (
    <Tooltip title={content} placement="top" arrow>
      {children}
    </Tooltip>
  );
}
const NewRoomAvail = () => {
  const dispatchvalue = useDispatch();
  const UrlLink = useSelector(state => state.userRecord?.UrlLink);
  const userRecord = useSelector((state) => state.userRecord?.UserData);
  const toast = useSelector(state => state.userRecord?.toast);
  const [RoomdataColumnsData, setRoomdataColumnsData] = useState([]);
  const [RoomDatas, setRoomDatas] = useState([]);
  const [RoomdataColumns, setRoomdataColumns] = useState([]);


  const [Roomdata, setRoomdata] = useState({
    Building: '',
    Block: '',
    Floor: '',
    Ward: '',

  });

  console.log(Roomdata, 'Roomdata');
  const [Building, setBuilding] = useState([]);
  const [Block_by_building, setBlock_by_building] = useState([]);
  const [Floor_by_block, setFloor_by_block] = useState([]);
  const [Ward_by_floor, setWard_by_floor] = useState([]);

  // const [bed]


  console.log(Ward_by_floor);

  const [filtertypes, setfiltertypes] = useState({
    wardtype: '',
    status: 'Total'
  })
  const handleheaderclicked = useCallback((params) => {
    setfiltertypes((prev) => ({
      ...prev,
      status: params,
      wardtype: ''
    }))
  }, [])
  const handlecellclicked = useCallback((params, field) => {
    console.log(params, field);

    setfiltertypes((prev) => ({
      ...prev,
      status: field,
      wardtype: params.roomname
    }))
  }, [])


  const handleChange = (e) => {

    const { name, value } = e.target
    if (name === 'Building') {
      setRoomdata((prev) => ({
        ...prev,
        [name]: value,
        Block: '',
        Floor: '',
        Ward: '',
      }))
    }

    else if (name === 'Block') {
      setRoomdata((prev) => ({
        ...prev,
        [name]: value,
        Floor: '',
        Ward: '',
      }))

    }

    else if (name === 'Floor') {
      setRoomdata((prev) => ({
        ...prev,
        [name]: value,
        Ward: '',
      }))

      setWard_by_floor([]);
      //setRoomDatas([]);
      setRoomdataColumns([]);

    }

    // else if(name === 'Ward') {
    //   setRoomdata((prev) => ({
    //     ...prev,
    //     [name]: value,

    // }))

    // }

  };



  // useEffect(() => {
  //   if (userRecord && userRecord?.location) {
  //     axios
  //       .get(
  //         `${UrlLink}Masters/get_room_count_data_total?Location=${userRecord?.location}`
  //       )
  //       .then((response) => {
  //         const { totalcount, totaldata } = response.data;

  //         const RoomdataColumns = [
  //           {
  //             key: "roomname",
  //             name: "Ward Name",
  //             width: 250,
  //             renderCell: (params) => (
  //               <div
  //                 className={`datatableheadercchecked ${
  //                   filtertypes.wardtype === params.row.roomname
  //                     ? "selectedheader"
  //                     : ""
  //                 }`}
  //               >
  //                 {params.row.ward_name}
  //               </div>
  //             ),
  //           },
  //           {
  //             Key : "Roomno",
  //             name : "Room No"
  //           },
  //           {
  //             key: "Beds",
  //             name: "Beds",
  //             width: "auto",
  //             renderCell: (params) => {
  //               const { Available, Occupied, Maintenance, Requested } =
  //                 params.row;

  //               // Helper function to get background color for each status
  //               const getBedStatusColor = (status) => {
  //                 switch (status) {
  //                   case "Available":
  //                     return "rose";
  //                   case "Occupied":
  //                     return "green";
  //                   case "Maintenance":
  //                     return "grey";
  //                   case "Requested":
  //                     return "yellow";
  //                   default:
  //                     return "white";
  //                 }
  //               };

  //               // Function to create bed boxes with their numbers and status
  //               const renderBeds = (bedCount, status, patientData) => {
  //                 return [...Array(bedCount)].map((_, index) => {
  //                   const bedNumber = index + 1;
  //                   const statusColor = getBedStatusColor(status);
  //                   const patient = patientData ? patientData[bedNumber - 1] : null;

  //                   return (
  //                     <div
  //                       key={bedNumber}
  //                       className={`bed-box ${statusColor}`}
  //                       title={`Bed No: ${bedNumber} - Status: ${status}`}
  //                     >
  //                       {bedNumber}
  //                       {patient && (
  //                         <div className="patient-details">
  //                           <strong>{patient.name}</strong>
  //                           <p>Age: {patient.age}</p>
  //                           <p>Status: {patient.status}</p>
  //                         </div>
  //                       )}
  //                     </div>
  //                   );
  //                 });
  //               };

  //               // Assuming each row has the patient details for each bed
  //               const availableBeds = params.row.AvailablePatients || [];
  //               const occupiedBeds = params.row.OccupiedPatients || [];
  //               const maintenanceBeds = params.row.MaintenancePatients || [];
  //               const requestedBeds = params.row.RequestedPatients || [];

  //               return (
  //                 <div className="beds-container">
  //                   {renderBeds(Available, "Available", availableBeds)}
  //                   {renderBeds(Occupied, "Occupied", occupiedBeds)}
  //                   {renderBeds(Maintenance, "Maintenance", maintenanceBeds)}
  //                   {renderBeds(Requested, "Requested", requestedBeds)}
  //                 </div>
  //               );
  //             },
  //           },
  //           {
  //             key: "Total",
  //             name: "Total",
  //             width: 50,
  //           },
  //         ];

  //         setRoomdataColumns(RoomdataColumns);
  //         setRoomdataColumnsData(totaldata);
  //       })
  //       .catch((error) => {
  //         console.log(error);
  //       });
  //   }
  // }, [
  //   userRecord,
  //   userRecord?.location,
  //   filtertypes,
  //   handleheaderclicked,
  //   handlecellclicked,
  // ]);


  //   const RoomColumns = [

  //     {
  //         key: "WardName",
  //         name: "WardName",
  //         frozen: true
  //     },
  //     {
  //         key: "RoomNo",
  //         name: "RoomNo",
  //     }
  //     ,
  //     {
  //         key: "BedNo",
  //         name: "BedNo",
  //     }

  // ];





  useEffect(() => {
    const data = {
      location: userRecord?.location,
      ...filtertypes
    }
    if (data.location && data.status) {
      axios.get(
        `${UrlLink}Masters/get_Room_Master_Data`, { params: data }
      )
        .then((response) => {
          const data = response.data;
          setRoomDatas(data);
        })
        .catch((error) => {
          console.log(error);
        });
    }

  }, [filtertypes, userRecord?.location])



  useEffect(() => {
    const data = {
      location: userRecord?.location,
      ...filtertypes
    }
    if (data.location && data.status) {
      axios.get(
        `${UrlLink}Masters/get_Building_data`, { params: data }
      )
        .then((response) => {
          const data = response.data;
          setBuilding(data);
        })
        .catch((error) => {
          console.log(error);
        });
    }

  }, [UrlLink]);


  useEffect(() => {

    console.log(Roomdata.Building, 'Roomdata.Building');
    const data = {
      location: userRecord?.location,
      Building: Roomdata.Building
    }

    axios.get(
      `${UrlLink}Masters/get_block_Data_by_Building`, { params: data }
    )
      .then((response) => {
        const data = response.data;
        setBlock_by_building(data);
      })
      .catch((error) => {
        console.log(error);
      });


  }, [Roomdata.Building]);

  useEffect(() => {

    console.log(Roomdata.Building, 'Roomdata.Building');
    const data = {
      location: userRecord?.location,
      Block: Roomdata.Block
    }

    axios.get(
      `${UrlLink}Masters/get_floor_data_by_Block`, { params: data }
    )
      .then((response) => {
        const data = response.data;
        setFloor_by_block(data);
      })
      .catch((error) => {
        console.log(error);
      });


  }, [Roomdata.Block]);

  useEffect(() => {

    console.log(Roomdata.Building, 'Roomdata.Building');
    const data = {
      location: userRecord?.location,
      Floor: Roomdata.Floor
    }

    axios.get(
      `${UrlLink}Masters/get_Ward_details_by_floor`, { params: data }
    )
      .then((response) => {
        const data = response.data;
        console.log(data, 'datadatadata');
        setWard_by_floor(data);
      })
      .catch((error) => {
        console.log(error);
      });


  }, [Roomdata.Floor]);

  useEffect(() => {

    console.log(Roomdata.Building, 'Roomdata.Building');
    const data = {
      location: userRecord?.location,
      Floor: Roomdata.Floor
    }

    axios.get(
      `${UrlLink}Masters/get_bed_details_by_ward`, { params: data }
    )
      .then((response) => {
        const data = response.data;
        setWard_by_floor(data);
      })
      .catch((error) => {
        console.log(error);
      });


  }, [Roomdata.Floor]);


  const roomCards = RoomDatas.map((room, index) => {
    // Check if 'attender' is an array and join it if it is, otherwise display an empty string
    const attendersText = Array.isArray(room?.attenders)
      ? room?.attenders.join(", ")
      : room?.attenders;

    const tooltipContent = (
      <div>
        Patient : {room?.PatientName}
        <br />
        Age : {room?.Age}
        <br />
        Attenders : {attendersText}
        <br />
        Contact : {room?.attenderPhoneNo}
        <br />
        Admitted Date : {room?.Admitdate}
        <br />
        {`Admission Purpose  : ${room?.AdmissionPurpose || ''}`}
      </div>
    );

    console.log('Ward_by_floor', Ward_by_floor);

    return (
      <CustomTooltip
        content={["Occupied", "Booked", "Requested"].includes(room.BookingStatus) ? tooltipContent : ""}
        key={index}
      >
        <Card sx={{ maxWidth: 350 }}>
          <div className="tooltip-trigger">
            <CardContent className="Rooms_avail_card_container">
              <Typography
                sx={{ fontSize: 14 }}
                color="text.secondary"
                gutterBottom
                component="div"
                className="Rooms_avail_card_container_container"
              >
                <div className='no_v_rooms'>{room?.RoomNo} </div>
                {/* <div className="Rooms_avail_card_one">
                  <div className="Rooms_avail_card_neww">
                    <label htmlFor="">
                      Building <span>:</span>
                    </label>
                    <div>{room?.BuildingName}</div>
                  </div> */}
                {/* <div className="Rooms_avail_card_neww">
                    <label htmlFor="">
                      Block Name<span>:</span>
                    </label>
                    <div>{room?.BlockName}</div>
                  </div>
                </div> */}
                {/* <div className="Rooms_avail_card_one">
                  <div className="Rooms_avail_card_neww">
                    <label htmlFor="">
                      Floor Name <span>:</span>
                    </label>
                    <div>{room?.FloorName}</div>
                  </div> */}
                {/* <div className="Rooms_avail_card_neww">
                    <label htmlFor="">
                      Ward Type <span>:</span>
                    </label>
                    <div>{room?.WardName}</div>
                  </div>
                </div> */}
                {/* <div className="Rooms_avail_card_one">
                  <div className="Rooms_avail_card_neww">
                    <label htmlFor="">
                      Room Type <span>:</span>
                    </label>
                    <div>{room?.RoomName}</div>
                  </div> */}
                {/* <div className="Rooms_avail_card_neww">
                    <label htmlFor="">
                      Room No <span>:</span>
                    </label>
                    <div>{room?.RoomNo}</div>
                  </div>
                </div> */}
                <div className="Rooms_avail_card_one">
                  <div className="Rooms_avail_card_neww">
                    <label htmlFor="">
                      Bed No <span>:</span>
                    </label>
                    <div>{room?.BedNo}</div>
                  </div>
                  <div className="Rooms_avail_card_neww">
                    <label htmlFor="">
                      Patient<span>:</span>
                    </label>
                    <div>{room?.PatientName}</div>
                  </div>
                  <div className="Rooms_avail_card_neww">
                    <label htmlFor="">
                      Age<span>:</span>
                    </label>
                    <div>{room?.Age}</div>
                  </div>
                  <div className="Rooms_avail_card_neww">
                    <label htmlFor="">
                      Charge <span>:</span>
                    </label>
                    <div>{room?.TotalCharge}</div>
                  </div>
                </div>
              </Typography>
              <Typography variant="h5" className="Rooms_avail_card_icon">
                {room.Status !== 'Inactive' ?
                  <FontAwesomeIcon
                    icon={faBed}
                    style={{
                      color:
                        room.BookingStatus === "Occupied"
                          ? "red"
                          : room.BookingStatus === "Maintenance"
                            ? "orange"
                            : room.BookingStatus === "Booked" ?
                              "blue" :
                              room.BookingStatus === "Requested" ?
                                'grey' : "green",
                    }}
                    className={`Rooms_avail_carditems_availableIcon`}
                  />
                  :
                  <MdBlock
                    style={{
                      color: "red"
                    }}
                    className={`Rooms_avail_carditems_availableIcon`}
                  />
                }
              </Typography>
            </CardContent>
            <CardActions className="Rooms_avail_card_btns">
              {
                room.Status === 'Inactive' ?
                  (
                    <Button size="small" style={{ color: "red" }}>
                      InActive
                    </Button>
                  ) :
                  (
                    <>


                      {room.BookingStatus === "Occupied" && (
                        <Button size="small" style={{ color: "red" }}>
                          Occupied
                        </Button>
                      )}
                      {room.BookingStatus === "Maintenance" && (
                        <Button size="small" style={{ color: "orange" }}>
                          Under Maintenance
                        </Button>
                      )}
                      {room.BookingStatus === "Available" && (
                        <Button size="small" style={{ color: "green" }}>
                          Available
                        </Button>
                      )}
                      {room.BookingStatus === "Booked" && (
                        <Button size="small" style={{ color: "blue" }}>
                          Booked
                        </Button>
                      )}
                      {room.BookingStatus === "Requested" && (
                        <Button size="small" style={{ color: "grey" }}>
                          Requested
                        </Button>
                      )}
                    </>
                  )
              }


            </CardActions>
          </div>
        </Card>
      </CustomTooltip>
    );
  });





  //   return (
  //     <>
  //     <div className="Main_container_app">
  //       <h3>Room Management</h3>

  //       <div className="search_div_bar">

  //            <div className="RegisForm_1">
  //               <label>
  //                 Building Name <span>:</span>
  //               </label>
  //               <select
  //                 name="Building"
  //                 //value={OtRequest.Speciality}
  //                 onChange={handleChange}
  //               >
  //                 <option value="">Select</option>
  //                { Building.map((p, index) => (
  //                      <option key={index} value={p.id}>{p.BuildingName}</option>
  //                  ))}
  //               </select>
  //           </div>

  //           <div className="RegisForm_1">
  //               <label>
  //                  Block Name <span>:</span>
  //               </label>
  //               <select
  //                 name="Block"
  //                 //value={OtRequest.Speciality}
  //                 onChange={handleChange}
  //               >
  //                 <option value="">Select</option>
  //                { Block_by_building.map((p, index) => (
  //                      <option key={index} value={p.id}>{p.BlockName}</option>
  //                  ))}
  //               </select>
  //           </div>

  //           <div className="RegisForm_1">
  //               <label>
  //                  Floor Name <span>:</span>
  //               </label>
  //               <select
  //                 name="Floor"
  //                 //value={OtRequest.Speciality}
  //                 onChange={handleChange}
  //               >
  //                 <option value="">Select</option>
  //                { Floor_by_block.map((p, index) => (
  //                      <option key={index} value={p.id}>{p.FloorName}</option>
  //                  ))}
  //               </select>
  //           </div>

  //       <br />
  //       <div className="doctor_schedule_table_wrapper">
  //         <div className="wdu6wtc_s8x5">
  //           <span class="available">Available</span>
  //           <span class="occupied">Occupied</span>
  //           <span class="discharge">Discharge Advised</span>
  //           <span class="housekeeping">Housekeeping</span>
  //           <span class="maintenance">Maintenance</span>
  //         </div>
  //         <br />
  //         <ReactGrid columns={RoomdataColumns} RowData={RoomdataColumnsData} />
  //         <div className="Rooms_avail_card">{roomCards}</div>

  //         </div>

  //       </div>
  //       </div>


  //     </>
  //   )
  // }


  return (
    // <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
    //   <h1 style={{ textAlign: "center" }}>Ward Management</h1>
    <>
      <div className="Main_container_app">
        <h3>Room Management</h3>
        <div className="search_div_bar">
          <div className="RegisForm_1">
            <label>
              Building Name <span>:</span>
            </label>
            <select
              name="Building"
              //value={OtRequest.Speciality}
              onChange={handleChange}
            >
              <option value="">Select</option>
              {Array.isArray(Building) && Building.map((p, index) => (
                <option key={index} value={p.id}>{p.BuildingName}</option>
              ))}
            </select>
          </div>

          <div className="RegisForm_1">
            <label>
              Block Name <span>:</span>
            </label>
            <select
              name="Block"
              //value={OtRequest.Speciality}
              onChange={handleChange}
            >
              <option value="">Select</option>
              {Array.isArray(Block_by_building) && Block_by_building.map((p, index) => (
                <option key={index} value={p.id}>{p.BlockName}</option>
              ))}
            </select>
          </div>

          <div className="RegisForm_1">
            <label>
              Floor Name <span>:</span>
            </label>
            <select
              name="Floor"
              //value={OtRequest.Speciality}
              onChange={handleChange}
            >
              <option value="">Select</option>
              {Array.isArray(Floor_by_block) && Floor_by_block.map((p, index) => (
                <option key={index} value={p.id}>{p.FloorName}</option>
              ))}
            </select>
          </div>
          {/* <div className="RegisForm_1">
            <label>
              Ward Name <span>:</span>
            </label>
            <select
              name='Ward'
              onChange={handleChange}
            >
              <option value="">Select</option>
              {Array.isArray(Ward_by_floor) && Ward_by_floor.map((p, index) => (
                <option key={index} value={p.id}>{p.WardName}</option>
              ))}
            </select>
          </div> */}
        </div>
      </div>
      <div className="wdu6wtc_s8x5">
        <span class="available">Available</span>
        <span class="occupied">Occupied</span>
        <span class="discharge">Discharge Advised</span>
        <span class="housekeeping">Housekeeping</span>
        <span class="maintenance">Maintenance</span>
      </div>
      <br></br><br></br>
      <div className="Selected-table-container">
        <table className="selected-medicine-table2">
          <thead>
            <tr>
              <th>Ward Name</th>
              <th>Room No</th>
              <th>Beds</th>
              <th>Total</th>
            </tr>
          </thead>
          <tbody>
            {Array.isArray(Ward_by_floor) && Ward_by_floor.map((ward) => (
              <tr key={ward.WardId}>
                <td>{ward.WardName}</td>
                <td>
                  {ward.Rooms.map((room) => (
                    <div key={room.RoomNo}>{room.RoomNo ? room.RoomNo : "-"}</div>
                  ))}
                </td>
                
                <td>
                  {ward.Rooms.map((room) =>
                    room.Beds.map((bed) => (
                      <span
                        key={bed.BedId}
                        style={{
                          display: "inline-block",
                          backgroundColor: bed.status === "Occupied" ? "#8EFF8E" : "#ffcccc",
                          color: "black",
                          borderRadius: "5px",
                          width: "60px",
                          height: "18px",
                          textAlign: "center",
                          margin: "2px",
                        }}
                      >
                        {bed.BedNo}
                      </span>
                    ))
                  )}
                </td>
                <td>
                  {ward.Rooms.reduce(
                    (sum, room) => sum + room.Beds.length,
                    0
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="Rooms_avail_card">{roomCards}</div>
    </>
  );
}

export default NewRoomAvail;