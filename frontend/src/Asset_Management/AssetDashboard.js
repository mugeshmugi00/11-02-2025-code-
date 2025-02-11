// src/components/AssetDashboard.js
import React, { useState, useEffect } from "react";
import { useDispatch, useSelector } from 'react-redux'
// import DepartmentList from './rev/DepartmentList';
// import AssetCategoryList from './AssetCategoryList';
// import SupplierList from '../../../frontend1/src/components/rev/SupplierList';
// import UserControlList from '../../../frontend1/src/components/UserControlList';
// import AddEditDepartment from '../../../frontend1/src/components/AddEditDepartment';
// import AddEditAssetCategory from './AddEditAssetCategory';
// import AddEditSupplier from './AddEditSupplier';
// import AddEditUser from './rev/AddEditUser';
 
// import AssetCategories from './Asset_Management/AssetCategories';
// import AssetSubCategoryManagement from './Asset_Management/AssetSubCategoryManagement';
// import suppliers from './Asset_Management/suppliers';
// import ServiceProviderMangement from './Asset_Management/ServiceProviderMangement';
// import ChecklistMasterEntry from './Asset_Management/ChecklistMasterEntry';
// import ChecklistManagement from './Asset_Management/ChecklistManagement';
// import AssetManagement from './Asset_Management/AssetManagement';
// import AssetDocumentsupload from './Asset_Management/AssetDocumentsupload';
// import AssetRelationship from './Asset_Management/AssetRelationship';
// import AssetAMC from './Asset_Management/AssetAMC';
 
import AssetAMC from "../folder add/Asset_Management/AssetAMC";
 
import AssetCategories from "../folder add/Asset_Management/AssetCategories";
import ServiceProviderMangement from "../folder add/Asset_Management/ServiceProviderMangement";
import AssetRelationship from "../folder add/Asset_Management/AssetRelationship";
import AssetDocumentsupload from "../folder add/Asset_Management/AssetDocumentsupload";
import AssetManagement from "../folder add/Asset_Management/AssetManagement";
import ChecklistManagement from "../folder add/Asset_Management/ChecklistManagement";
import ChecklistMasterEntry from "../folder add/Asset_Management/ChecklistMasterEntry";
import Suppliers from "../folder add/Asset_Management/Suppliers";
import AssetSubCategoryManagement from "../folder add/Asset_Management/AssetSubCategoryManagement";
 
 
 
 
 
 
const AssetDashboard = () => {
    const activeHrFolder = useSelector((state) => state.userRecord?.HrFolder)
    const showMenu = useSelector((state) => state.userRecord?.showMenu);
    const dispatchvalue = useDispatch()
 
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
 
            case "AssetCategories":
                return <AssetCategories />
            case "AssetSubCategoryManagement":
                return < AssetSubCategoryManagement />
            case "Suppliers":
                return < Suppliers />
 
            case "ServiceProviderMangement":
                return < ServiceProviderMangement />
 
            case "ChecklistMasterEntry":
                return < ChecklistMasterEntry />
 
            case "ChecklistManagement":
                return < ChecklistManagement />
 
            case "AssetManagement":
                return < AssetManagement />
 
            case "AssetDocumentsupload":
                return < AssetDocumentsupload />
 
            case "AssetRelationship":
                return < AssetRelationship />
 
            case "AssetAMC":
                return < AssetAMC />
 
            default:
                return <AssetCategories />;
        }
    };
    return (
        <div className="folder-container">
            <div className={`folder-box-container ${showFolders ? "animate-show" : ""}`}>
 
 
                {showMenu && subAccess.includes('Q17-1') && (
                    <div onClick={() => handleFolderClick("AssetCategories")}
                        className="folder-box" > Asset Categories </div>
                )}
 
                {showMenu && subAccess.includes('Q17-2') && (
                    <div onClick={() => handleFolderClick("AssetSubCategoryManagement")}
                        className="folder-box" > Asset SubCategory Management </div>
                )}
 
                {showMenu && subAccess.includes('Q17-3') && (
                    <div onClick={() => handleFolderClick("Suppliers")}
                        className="folder-box" > Suppliers </div>
                )}
 
                {showMenu && subAccess.includes('Q17-4') && (
                    <div onClick={() => handleFolderClick("ServiceProviderMangement")}
                        className="folder-box" > Service Provider Mangement </div>
                )}
 
                {showMenu && subAccess.includes('Q17-5') && (
                    <div onClick={() => handleFolderClick("ChecklistMasterEntry")}
                        className="folder-box" > Checklist Master Entry </div>
                )}
 
                {showMenu && subAccess.includes('Q17-6') && (
                    <div onClick={() => handleFolderClick("ChecklistManagement")}
                        className="folder-box" > Checklist Management </div>
                )}
 
                {showMenu && subAccess.includes('Q17-7') && (
                    <div onClick={() => handleFolderClick("AssetManagement")}
                        className="folder-box" > Asset Management </div>
                )}
 
                {showMenu && subAccess.includes('Q17-8') && (
                    <div onClick={() => handleFolderClick("AssetDocumentsupload")}
                        className="folder-box" > Asset Documents </div>
                )}
 
 
                {showMenu && subAccess.includes('Q17-9') && (
                    <div onClick={() => handleFolderClick("AssetRelationship")}
                        className="folder-box" > Asset Relationship </div>
                )}
 
                {showMenu && subAccess.includes('Q17-10') && (
                    <div onClick={() => handleFolderClick("AssetAMC")}
                        className="folder-box" > Asset AMC </div>
                )}
             
 
            </div>
 
            {renderFolderContent()}
        </div>
    );
};
 
export default AssetDashboard;