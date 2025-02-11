import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import InventoryNurseStation from "./InventoryNurseStation";

const NurseStationFolder = () => {
  const activeHrFolder = useSelector((state) => state.userRecord?.HrFolder);

  const showMenu = useSelector((state) => state.userRecord?.showMenu);
  const dispatchvalue = useDispatch();

  // const [activeFolder, setActiveFolder] = useState("OP_patients");
  const [showFolders, setShowFolders] = useState(false);
  const UserData = useSelector((state) => state.userRecord?.UserData);

  const [subAccess, setSubAccess] = useState([]);

  useEffect(() => {
    console.log(UserData, "UserData");

    if (UserData) {
      const setAccess2 =
        (UserData.AccessTwo &&
          UserData.AccessTwo.split(",").map((item) => item.trim())) ||
        [];

      setSubAccess(setAccess2);
    }
  }, [UserData]); 

  const activeFolder = useSelector((state) => state.userRecord?.activeFolder);

  const handleFolderClick = (folderName) => {
    dispatchvalue({ type: "setPreviousFolder", value: activeFolder });
    dispatchvalue({ type: "setActiveFolder", value: folderName }); 
    dispatchvalue({ type: "showMenu", value: false }); 
  };

  useEffect(() => {
    console.log(activeHrFolder, "activeHrFolder");

    if (activeHrFolder !== "") {
      dispatchvalue({ type: "setActiveFolder", value: activeHrFolder });
      dispatchvalue({ type: "HrFolder", value: "" });
    }
    setShowFolders(true);
  }, [activeHrFolder, dispatchvalue]);

  const renderFolderContent = () => {
    switch (activeFolder) {
      case "InventoryNurseStation":
        return <InventoryNurseStation />;
  
        default:
          return <InventoryNurseStation />;
     
    }
  };

  return (
    <div className="folder-container">
      {/* <h2>Out Patients Reception</h2> */}
      
      <div
        className={`folder-box-container ${showFolders ? "animate-show" : ""}`}
      >
        {showMenu && subAccess.includes("F6-1") && (
          <div
            onClick={() => handleFolderClick("InventoryNurseStation")}
            className="folder-box"
          >
            {" "}
            Inventory
          </div>
        )}

        {showMenu && subAccess.includes("F6-2") && (
          <div
            onClick={() => handleFolderClick("PatientQueList")}
            className="folder-box"
          >
            {" "}
            Patients Que List
          </div>
        )}

        {showMenu && subAccess.includes("F6-3") && (
          <div onClick={() => handleFolderClick("BreakageMaintenance")} className="folder-box">
            {" "}
            Breakage/Maintenance
          </div>
        )}

        {/* {showMenu && subAccess.includes("F6-4") && (
          <div
            onClick={() => handleFolderClick("Pharmacy")}
            className="folder-box"
          >
            {" "}
            Pharmacy
          </div>
        )}

        {showMenu && subAccess.includes("F6-5") && (
          <div
            onClick={() => handleFolderClick("Beds")}
            className="folder-box"
          >
            {" "}
            Beds
          </div>
        )}

        {showMenu && subAccess.includes("F6-6") && (
          <div
            onClick={() => handleFolderClick("Service")}
            className="folder-box"
          >
            {" "}
            Service
          </div>
        )} */}
      </div>
      {renderFolderContent()}
    </div>
  );
};

export default NurseStationFolder;
