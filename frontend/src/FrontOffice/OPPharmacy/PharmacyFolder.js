import React, { useState, useEffect } from "react";
import PharmacyBillingLIst from "./PharmacyBillingLIst";
import IPPharmacyBillingList from "../IpPharmacy/IPPharmacyBillingList";
import PharmacyWalkinQue from "./PharmacyWalkinQue";

import { useDispatch, useSelector } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import PharmacyBillingNew from "./PharmacyBillingNew";
import PharmacyBilling from "./PharmacyBilling";

const PharmacyFolder = () => {

    const activeHrFolder = useSelector((state) => state.userRecord?.HrFolder)
    const showMenu = useSelector((state) => state.userRecord?.showMenu); 

    // const [activeFolder, setActiveFolder] = useState("OPPharmachyBillingList");

    const [showFolders, setShowFolders] = useState(false);
  
  const dispatchvalue = useDispatch()

    const UserData = useSelector(state => state.userRecord?.UserData)
  
    const [subAccess, setSubAccess] = useState([])
      
    useEffect(() => {
      console.log(UserData, 'UserData')

      if (UserData) {
        
        const setAccess2 =
          (UserData.AccessTwo &&
            UserData.AccessTwo.split(',').map(item => item.trim())) ||
          []

        setSubAccess(setAccess2) // Update state for sub access
      }
    }, [UserData]) // Dependency array
        
  const activeFolder = useSelector((state) => state.userRecord?.activeFolder);

  const handleFolderClick = (folderName) => {
    
    dispatchvalue({ type: "setPreviousFolder", value: activeFolder }); // Save current folder
    dispatchvalue({ type: "setActiveFolder", value: folderName }); // Navigate to new folder
    dispatchvalue({ type: "showMenu", value: false });  // Close menu when navigating to homepage

  };

  useEffect(() => {

        console.log(activeHrFolder, 'activeHrFolder');

    if (activeHrFolder !== "") {
      dispatchvalue({ type: "setActiveFolder", value: activeHrFolder });
      dispatchvalue({ type: "HrFolder", value: "" }); // Reset HrFolder
    }
    setShowFolders(true);

  }, [activeHrFolder, dispatchvalue]);



    const renderFolderContent = () => {
        switch (activeFolder) {
          case "OPPharmachyBillingList":
            return <PharmacyBillingLIst />;
          case "IPPharmacyBillingList":
            return <IPPharmacyBillingList />;

            case "OPPharmachyBilling":
              return <PharmacyBilling />;

          case "PharmacyWalkinQue":
            return <PharmacyWalkinQue />;
            case "PharmacyBillingNew":
              return <PharmacyBillingNew />;

          default:
            return <PharmacyBillingLIst />;
        }
      };
  return (
    <div className="folder-container">
      {/* <h2>Pharmacys</h2> */}
      <div className={`folder-box-container ${showFolders ? "animate-show" : ""}`}>
        
       {showMenu && subAccess.includes('H8-1') && (
          <div onClick={() => handleFolderClick("OPPharmachyBillingList")}
            className="folder-box"> OP Pharmacy Billing
          </div>
        )}

       {showMenu && subAccess.includes('H8-2') && (

          <div onClick={() => handleFolderClick("IPPharmacyBillingList")}
            className="folder-box"> IP Pharmacy Billing
          </div>

        )}
       {showMenu && subAccess.includes('H8-3') && (

          <div onClick={() => handleFolderClick("PharmacyWalkinQue")}
            className="folder-box"> Pharmacy Walkin Que
          </div>

        )}







      </div>

      {renderFolderContent()}
    </div>
  )
}

export default PharmacyFolder