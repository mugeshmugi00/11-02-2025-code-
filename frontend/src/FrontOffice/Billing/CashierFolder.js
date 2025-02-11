import React, { useState, useEffect } from "react";
import GeneralBillingList from "./GeneralBillingList";
import QuickBilling from "./Billing";
import OverAllQuickBilling from "./QuickBilling";
import IPBillingList from "../IPBilling/IPBillingList";
import IPBilling from "../Billing/IPBilling";
import CashierDashboard from "./CashierDashboard";
import IP_BillingDischargeQueslist from "../../IP_Workbench/Nurse/Discharge/IP_BillingDischargeQueslist";
import LabQueuelist from "./LabQueuelist";
import AdvanceCollection from "./AdvanceCollection";
import AdvanceCollectionList from "./AdvanceCollectionList";
import { useDispatch, useSelector } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import GeneralBillingEditList from "./GeneralBillingEditList";
import IPBillingEditList from "./IPBillingEditList";
import RiskManagementList from "./RiskManagementList";
import OPBillingReport from "./OPBIllingReport";
import IPBillingReport from "./IPBIllingReport";
import GeneralBillingListCashier from "./GeneralBillingListCashier";
import QuickBillingCashier from "./BillingCashier";
import OverAllQuickBillingFront from "./QuickBillingFrontOffice";

function CashierFolder() {

    const activeHrFolder = useSelector((state) => state.userRecord?.HrFolder)
    const showMenu = useSelector((state) => state.userRecord?.showMenu); 

    const dispatchvalue = useDispatch()

  // const [activeFolder, setActiveFolder] = useState("CashierDashboard");
  const [showFolders, setShowFolders] = useState(false); // State to control folder display animation

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

  

  // Render the content dynamically based on the active folder
  const renderFolderContent = () => {
    switch (activeFolder) {
      case "CashierDashboard":
        return <CashierDashboard />;
      case "GeneralBillingListCashier":
        return <GeneralBillingListCashier />;
        case "OverAllQuickBillingFront":
          return <OverAllQuickBillingFront />;
      case "GeneralBillingEditList":
        return <GeneralBillingEditList />;
      case 'QuickBillingCashier':
        return <QuickBillingCashier />;
      case "OverAllQuickBilling":
        return <OverAllQuickBilling />;
      case "OPBillingReport":
        return <OPBillingReport />;
      case "IPBillingReport":
        return <IPBillingReport />;

      case "IPBillingList":
        return <IPBillingList />;
      case "IPBilling":
        return <IPBilling />;
      case "IPBillingEditList":
        return <IPBillingEditList />;
      
      case "IP_BillingDischargeQueslist":
        return <IP_BillingDischargeQueslist />;
      case "LabQueuelist":
        return <LabQueuelist />;
      case "AdvanceCollection":
        return <AdvanceCollectionList />;
      case "RiskManagementList":
        return <RiskManagementList />;

      default:
        return <CashierDashboard />;
    }
  };

  return (
    <div className="folder-container">
      {/* <h2>Cashier</h2> */}
      <div
        className={`folder-box-container ${showFolders ? "animate-show" : ""}`}
      >
       {showMenu && subAccess.includes('I9-1') && (
          <div
            onClick={() => handleFolderClick("CashierDashboard")}
            className="folder-box"
          >
            Cashier Dashboard
          </div>
        )}

       {showMenu && subAccess.includes('I9-2') && (
          <div
            onClick={() => handleFolderClick("GeneralBillingListCashier")}
            className="folder-box"
          >
            OP Billing
          </div>
        )}
       {showMenu && subAccess.includes('I9-3') && (
          <div
            onClick={() => handleFolderClick("GeneralBillingEditList")}
            className="folder-box"
          >
            OP Billing Edit List
          </div>
        )}

       {showMenu && subAccess.includes('I9-4') && (
          <div
            onClick={() => handleFolderClick("IPBillingList")}
            className="folder-box"
          >
            IP Billing
          </div>
        )}
       {showMenu && subAccess.includes('I9-5') && (
          <div
            onClick={() => handleFolderClick("IPBillingEditList")}
            className="folder-box"
          >
            IP Billing Edit List
          </div>
        )}
       {showMenu && subAccess.includes('I9-6') && (
          <div
            onClick={() => handleFolderClick("IP_BillingDischargeQueslist")}
            className="folder-box"
          >
            IP Billing Discharge Queslist
          </div>
        )}
       {showMenu && subAccess.includes('I9-7') && (
          <div
            onClick={() => handleFolderClick("LabQueuelist")}
            className="folder-box"
          >
            Lab Billing list
          </div>
        )}
       {showMenu && subAccess.includes('I9-8') && (
          <div
            onClick={() => handleFolderClick("AdvanceCollection")}
            className="folder-box"
          >
            Advance Collection
          </div>
        )}
       {showMenu && subAccess.includes('I9-9') && (
          <div
            onClick={() => handleFolderClick("RiskManagementList")}
            className="folder-box"
          >
            Risk Management List
          </div>
        )}
       {showMenu && subAccess.includes('I9-10') && (
          <div
            onClick={() => handleFolderClick("OPBillingReport")}
            className="folder-box"
          >
            OP Billing Report
          </div>
        )}

        {showMenu && subAccess.includes('I9-11') && (
          <div
            onClick={() => handleFolderClick("IPBillingReport")}
            className="folder-box"
          >
            IP Billing Report
          </div>
        )}
      </div>
      
      <br />

      {renderFolderContent()}
    </div>
  );
}

export default CashierFolder;
