import React, { useCallback, useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import { MdBlock } from "react-icons/md";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBed } from "@fortawesome/free-solid-svg-icons";
import axios from "axios";

const RoomDetialsSelect = () => {
  const [RoomDataforRegister, setRoomDataforRegister] = useState([]);
  const UserData = useSelector((state) => state.userRecord?.UserData);
  const UrlLink = useSelector((state) => state.userRecord?.UrlLink);
  const RegisterRoomShow = useSelector(
    (state) => state.Frontoffice?.RegisterRoomShow
  );

  console.log(RegisterRoomShow,'RegisterRoomShow');
  
  const dispatchvalue = useDispatch();
  const [searchdata, setsearchdata] = useState({
    Building: "",
    Block: "",
    Floor: "",
    Ward: "",
  });
  const [uniquedata, setuniquedata] = useState({});

  console.log(uniquedata,'uniquedata');
  
  useEffect(() => {
    dispatchvalue({ type: "SelectRoomRegister", value: {} });
  }, [dispatchvalue]);

  // useEffect(() => {
  //   if (RegisterRoomShow.val && RegisterRoomShow.type) {
  //     const data = {
  //       location: UserData?.location,
  //       RegisterType: RegisterRoomShow.type,
  //     };
  //     axios
  //       .get(`${UrlLink}Masters/get_filter_Data_for_registration`, {
  //         params: data,
  //       })
  //       .then((res) => {
  //         const data = res.data;
  //         console.log(data,'data');

  //         setuniquedata(data);
  //         Object.keys(data)
  //           .filter((p) => !["Ward"].includes(p))
  //           .forEach((element) => {
  //             if (data[element].length === 1) {
  //               setsearchdata((prev) => ({
  //                 ...prev,
  //                 [element]: data[element][0].id,
  //               }));
  //             }
  //           });
  //       })
  //       .catch((err) => {
  //         setuniquedata({});
  //         console.log(err);
  //       });
  //   }
  // }, [UserData, UrlLink, RegisterRoomShow.type]);



  useEffect(() => {
    if (RegisterRoomShow.val && RegisterRoomShow.type) {
      const data = {
        location: UserData?.location,
        RegisterType: RegisterRoomShow.type,
        ...searchdata,
      };
  
      console.log(data, "Fetching filtered data...");
      
      axios
        .get(`${UrlLink}Masters/get_filter_Data_for_registration`, { params: data })
        .then((res) => {
          const data = res.data;
          console.log(data, "Updated filtered data");
  
          setuniquedata(data);
        })
        .catch((err) => {
          setuniquedata({});
          console.log(err);
        });
    }
  }, [UserData, UrlLink, RegisterRoomShow.type, searchdata]);
  


  useEffect(() => {
    if (RegisterRoomShow.val && RegisterRoomShow.type) {
      const data = {
        location: UserData?.location,
        RegisterType: RegisterRoomShow.type,
        ...searchdata,
      };

      console.log(data,'data');
      
      axios
        .get(`${UrlLink}Masters/get_Room_Master_Data_for_registration`, {
          params: data,
        })
        .then((res) => {
          const data = res.data;

          console.log(data,'data');
          
          if (Array.isArray(data)) {
            console.log('2222222222222',data);
            
            setRoomDataforRegister(data);
          } else {
            setRoomDataforRegister([]);
          }
        })
        .catch((err) => {
          setRoomDataforRegister([]);
          console.log(err);
        });
    }
  }, [UserData, UrlLink, RegisterRoomShow.type, searchdata]);

  const selectroom = (room) => {
    console.log('roooooooooooommmmmmm',room);

    dispatchvalue({ type: "SelectRoomRegister", value: { ...room } });
    dispatchvalue({
      type: "RegisterRoomShow",
      value: { type: "", val: false },
    });
  };


  const handleinpchangeRoomDetails = (e) => {
    const { name, value } = e.target;
    console.log(name, 'name');
    console.log(value, 'value');
  
    setsearchdata((prev) => {
      let newData = { ...prev, [name]: value };
  
      // Reset dependent fields when a selection is changed
      if (name === "Building") {
        const isBlockValid = uniquedata.Block?.some(
          (b) => b.id === newData.Block && b.BuildingId === value
        );
  
        newData.Block = isBlockValid ? newData.Block : "";
        newData.Floor = "";
        newData.Ward = "";
      } else if (name === "Block") {
        newData.Floor = "";
        newData.Ward = "";
      } else if (name === "Floor") {
        newData.Ward = "";
      }
  
      return newData;
    });
  };







  return (
    <div
      className="loader"
      onClick={() =>
        dispatchvalue({
          type: "RegisterRoomShow",
          value: { type: "", val: false },
        })
      }
    >
      <div
        className="loader_register_roomshow"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="DivCenter_container">Select Room Details </div>
        <div className="RegisFormcon_1">
          {Object.keys(searchdata).map((field, index) => (
            <div className="RegisForm_1" key={index}>
              <label htmlFor={`${field}_${index}`}>
                {field === 'Building' ? 'Building Name':
                field === 'Block' ? 'Block Name':
                field === 'Floor' ? 'Floor Name':
                field === 'Ward' ? 'Ward Name':
                field}
                <span>:</span>
              </label>

              
              {/* <select
                id={`${field}_${index}`}
                name={field}
                value={searchdata[field]}
                // disabled={
                //   uniquedata[field]?.length === 1 
                  
                // }
                onChange={(e) =>
                  setsearchdata((prev) => ({
                    ...prev,
                    [field]: e.target.value,
                  }))
                }
              > */}

                <select
                  id={`${field}_${index}`}
                  name={field}
                  value={searchdata[field]}
                  onChange={handleinpchangeRoomDetails}
                  // onChange={(e) => {
                  //   const value = e.target.value;
                    
                  //   setsearchdata((prev) => {
                  //     const newData = { ...prev, [field]: value };

                  //     // Reset dependent fields when a selection is changed
                  //     if (field === "Building") {
                  //       newData.Block = "";
                  //       newData.Floor = "";
                  //       newData.Ward = "";
                  //     } else if (field === "Block") {
                  //       newData.Floor = "";
                  //       newData.Ward = "";
                  //     } else if (field === "Floor") {
                  //       newData.Ward = "";
                  //     }

                  //     return newData;
                  //   });
                  // }}
                >
                <option value="">Select</option>


                {/* Building Dropdown */}
          {field === "Building" &&
            uniquedata.Building?.map((b, indx) => (
              <option key={indx} value={b.id}>
                {b.Name}
              </option>
            ))}

          {/* Block Dropdown (Filtered by selected Building) */}
          {field === "Block" &&
            uniquedata.Block?.map((b, indx) => (
                <option key={indx} value={b.id}>
                  {b.Name}
                </option>
              ))}

          {/* Floor Dropdown (Filtered by selected Block) */}
          {field === "Floor" &&
            uniquedata.Floor?.map((f, indx) => (
                <option key={indx} value={f.id}>
                  {f.Name}
                </option>
              ))}

          {/* Ward Dropdown (Filtered by selected Floor) */}
          {field === "Ward" &&
            uniquedata.Ward?.map((w, indx) => (
                <option key={indx} value={w.id}>
                  {w.Name}
                </option>
              ))}
                
                {/* {field === "Building" && Array.from(
                  new Set(uniquedata.filter(
                    (p) => p.Building === searchdata.Building
                  ).flatMap((catg) => catg.Building))
                )?.map((catg,indx) => (
                  <option key={indx} value={catg}>
                      {catg}
                  </option>
                ))}

                {field === "Block" && Array.from(
                  new Set(uniquedata.filter(
                    (p) => p.Block === searchdata.Block
                  ).flatMap((catg) => catg.Block))
                )?.map((catg,indx) => (
                  <option key={indx} value={catg}>
                    {catg}
                  </option>
                ))}

                {Array.isArray(uniquedata[field]) &&
                  uniquedata[field].map((p, indx) => (
                    <option key={indx} value={p.id}>
                      {p.Name}
                    </option>
                  ))} */}


              </select>
            </div>
          ))}
        </div>
        <br />

        <div className="Rooms_avail_card">
          
          {RoomDataforRegister.map((room, index) => (
            <Card
              sx={{ maxWidth: 350 }}
              onClick={() => selectroom(room)}
              key={index}
            >
              <div className="tooltip-trigger">
                <CardContent className="Rooms_avail_card_container">
                  <Typography
                    sx={{ fontSize: 14 }}
                    color="text.secondary"
                    gutterBottom
                    component="div"
                    className="Rooms_avail_card_container_container"
                  >
                    <div className="Rooms_avail_card_one">
                      <div className="Rooms_avail_card_neww">
                        <label htmlFor="">
                          Building <span>:</span>
                        </label>
                        <div>{room?.BuildingName}</div>
                      </div>
                      <div className="Rooms_avail_card_neww">
                        <label htmlFor="">
                          Block Name<span>:</span>
                        </label>
                        <div>{room?.BlockName}</div>
                      </div>
                    </div>
                    <div className="Rooms_avail_card_one">
                      <div className="Rooms_avail_card_neww">
                        <label htmlFor="">
                          Floor Name <span>:</span>
                        </label>
                        <div>{room?.FloorName}</div>
                      </div>
                      <div className="Rooms_avail_card_neww">
                        <label htmlFor="">
                          Ward Type <span>:</span>
                        </label>
                        <div>{room?.WardName}</div>
                      </div>
                    </div>
                    <div className="Rooms_avail_card_one">
                      {/* <div className="Rooms_avail_card_neww">
                        <label htmlFor="">
                          Room Type <span>:</span>
                        </label>
                        <div>{room?.RoomName}</div>
                      </div> */}
                      <div className="Rooms_avail_card_neww">
                        <label htmlFor="">
                          Room No <span>:</span>
                        </label>
                        <div>{room?.RoomNo}</div>
                      </div>
                    </div>
                    <div className="Rooms_avail_card_one">
                      <div className="Rooms_avail_card_neww">
                        <label htmlFor="">
                          Bed No <span>:</span>
                        </label>
                        <div>{room?.BedNo}</div>
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
                    {room.Status !== "Inactive" ? (
                      <FontAwesomeIcon
                        icon={faBed}
                        style={{
                          color:
                            room.BookingStatus === "Occupied"
                              ? "red"
                              : room.BookingStatus === "Maintance"
                              ? "orange"
                              : room.BookingStatus === "Booked"
                              ? "blue"
                              : "green",
                        }}
                        className={`Rooms_avail_carditems_availableIcon`}
                      />
                    ) : (
                      <MdBlock
                        style={{
                          color: "red",
                        }}
                        className={`Rooms_avail_carditems_availableIcon`}
                      />
                    )}
                  </Typography>
                </CardContent>
                <CardActions className="Rooms_avail_card_btns">
                  {room.Status === "Inactive" ? (
                    <Button size="small" style={{ color: "red" }}>
                      InActive
                    </Button>
                  ) : (
                    <>
                      {room.BookingStatus === "Occupied" && (
                        <Button size="small" style={{ color: "red" }}>
                          Occupied
                        </Button>
                      )}
                      {room.BookingStatus === "Maintance" && (
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
                    </>
                  )}
                </CardActions>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};

export default RoomDetialsSelect;
