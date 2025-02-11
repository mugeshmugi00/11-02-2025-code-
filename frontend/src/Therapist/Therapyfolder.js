import React, { useState, useEffect } from "react";


import { useDispatch, useSelector } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import TherapistQuelist from "./TherapistQuelist";



const Therapyfolder = () => {

    const activeHrFolder = useSelector((state) => state.userRecord?.HrFolder)
    const showMenu = useSelector((state) => state.userRecord?.showMenu); 
    const dispatchvalue = useDispatch()
    
    // const [activeFolder, setActiveFolder] = useState("RadiologyQuelist");
    const [showFolders, setShowFolders] = useState(false);
  
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
          case "RadiologyQuelist":
            return <TherapistQuelist/>;
          // case "Mritechnician":
          //   return <Mritechnician />;
          // case "Cttechnician":
          //   return <Cttechnician />;
          // case "XRayTechnician":
          //   return <XRayTechnician />;
          // case "IP_RadiologyDischargeQueslist":
          //   return <IP_RadiologyDischargeQueslist />;
        
          default:
            return <TherapistQuelist />;
        }
      };
  
  return (
    <div className="folder-container">
      {/* <h2>Therapist</h2> */}
      <div className={`folder-box-container ${showFolders ? "animate-show" : ""}`}>

     {showMenu && subAccess.includes('N14-1') && (
         <div onClick={() => handleFolderClick("RadiologyQuelist")}
                className="folder-box"> Therapy Quelist</div>
      )}
      {/* {subAccess.includes('P16-2') && (

         <div onClick={() => handleFolderClick("Mritechnician")}
                className="folder-box"> MRI Technician</div>
      )} */}
      {/* {subAccess.includes('P16-3') && (

         <div onClick={() => handleFolderClick("Cttechnician")}
                className="folder-box"> CT Technician</div>
      )}

{subAccess.includes('P16-4') && (

         <div onClick={() => handleFolderClick("XRayTechnician")}
                className="folder-box"> XRay Technician</div>
)}
     {showMenu && subAccess.includes('P16-5') && (

         <div onClick={() => handleFolderClick("IP_RadiologyDischargeQueslist")}
                className="folder-box"> Discharge Queslist</div>

      )} */}





      </div>

      {renderFolderContent()}
    </div>
  )
}

export default Therapyfolder


