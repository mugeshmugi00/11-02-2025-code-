import React, { useEffect, useState, useCallback } from 'react';
import { useSelector } from 'react-redux';
import ReactGrid from '../../OtherComponent/ReactGrid/ReactGrid';
import { Button } from '@mui/material';
import EditIcon from "@mui/icons-material/Edit";
import axios from 'axios';

const AssetCategories = () => {
    const UrlLink = useSelector(state => state.userRecord?.UrlLink);
    const [categoryName, setCategoryName] = useState('');
    const [status, setStatus] = useState('active');
    const [categories, setCategories] = useState([]);
    const [editingCategoryId, setEditingCategoryId] = useState(null);
    const [isUpdating, setIsUpdating] = useState(false);

    // Fetch categories from database when component mounts
    const fetchCategories = useCallback(async () => {
        try {
            const response = await axios.get(`${UrlLink}AccetCategory/asset_categories_list/`);  // Added trailing slash here
            setCategories(response.data); // Set fetched categories to state
            console.log("asset_categories_list:",response)
        } catch (error) {
            console.error("Error fetching categories", error);
        }
    }, [UrlLink]);
    

    // Fetch category by ID for editing
    const fetchCategoryById = useCallback(async (id) => {
        try {
            const response = await axios.get(`${UrlLink}AccetCategory/get_asset_category/${id}/`);  // Added trailing slash here
            setCategoryName(response.data.name);
            setStatus(response.data.status);
            setEditingCategoryId(response.data.id);
        } catch (error) {
            console.error("Error fetching category", error);
        }
    }, [UrlLink]);
    
    
    useEffect(() => {
        fetchCategories();
    }, [fetchCategories]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const newCategory = { name: categoryName.toUpperCase(), status };
        
        try {
            if (editingCategoryId) {
                console.log("Updating category with ID", editingCategoryId);
                const response = await axios.put(
                    `${UrlLink}AccetCategory/update_asset_category/${editingCategoryId}/`, 
                    newCategory,
                    { headers: { 'Content-Type': 'application/json' } }
                );
                console.log("Update response", response);
                setCategories(categories.map((cat) => (cat.id === editingCategoryId ? { ...cat, ...newCategory } : cat)));
                setIsUpdating(false);
            } else {
                console.log("Adding new category");
                const response = await axios.post(`${UrlLink}AccetCategory/asset_categories/`, newCategory);
                setCategories([...categories, response.data]);
            }
        
            setCategoryName('');
            setStatus('active');
            setEditingCategoryId(null);
        } catch (error) {
            console.error("Error adding/updating category", error);
            if (error.response) {
                console.log("Error response:", error.response);
            }
        }
    };
    
    
    

    const handleEditAssetCategory = (category) => {
        fetchCategoryById(category.id);  
    };

    const assetCategoriesColumn = [
        {
            key: 'id',
            name: 'Asset Category ID',
            frozen: true
        },
        {
            key: 'name',
            name: 'Asset Category Name',
            frozen: true
        },
        {
            key: 'status',
            name: 'Status',
            renderCell: (params) => (
                <Button disabled={isUpdating} className="cell_btn">
                    {params.row.status === 'active' ? "ACTIVE" : "INACTIVE"}
                </Button>
            )
        },
        {
            key: 'Action',
            name: 'Action',
            renderCell: (params) => (
                <Button className="cell_btn" onClick={() => handleEditAssetCategory(params.row)}>
                    <EditIcon className="check_box_clrr_cancell" />
                </Button>
            )
        }
    ];

    return (
        <div className="Main_container_app">
            <h3>Asset Categories</h3>

            <div className="RegisFormcon_1" style={{ justifyContent: 'center' }}>
                <div className="RegisForm_1">
                    <label>
                        Asset Category Name <span>:</span>
                    </label>
                    <input
                        type="text"
                        name="categoryName"
                        value={categoryName}
                        onChange={(e) => setCategoryName(e.target.value)}
                        placeholder="Asset Category Name"
                        autoComplete="off"
                        required
                    />
                </div>

                <div className="RegisForm_1">
                    <label>
                        Status <span>:</span>
                    </label>
                    <select
                        name="status"
                        value={status}
                        onChange={(e) => setStatus(e.target.value)}
                    >
                        <option value="active">Active</option>
                        <option value="inactive">Inactive</option>
                    </select>
                </div>
            </div>

            <div className="Main_container_Btn">
                <button onClick={handleSubmit} style={{ width: "95px" }}>
                    {editingCategoryId ? "Update Category" : "Add Category"}
                </button>
            </div>

            {/* ReactGrid will now display the categories fetched from the database */}
            <ReactGrid columns={assetCategoriesColumn} RowData={categories} />
        </div>
    );
};

export default AssetCategories;
