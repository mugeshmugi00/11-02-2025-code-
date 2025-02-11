import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import axios from 'axios';
import ReactGrid from '../../OtherComponent/ReactGrid/ReactGrid';
import { Button } from '@mui/material';
import EditIcon from "@mui/icons-material/Edit";

const Suppliers = () => {
    const [formData, setFormData] = useState({
        name: '',
        contact_info: '',
        email: '',
        asset_category: '',
        subcategories: [],
        status: 'active',
        ranking: '1',
        remarks: ''
    });
    const [suppliers, setSuppliers] = useState([]);
    const [assetCategories, setAssetCategories] = useState([]);
    const [allSubcategories, setAllSubcategories] = useState([]);
    const [displayedSubcategories, setDisplayedSubcategories] = useState([]);
    const [editingSupplier, setEditingSupplier] = useState(null);
    const UrlLink = useSelector(state => state.userRecord?.UrlLink);



    useEffect(() => {
        fetchSuppliers();
        fetchAssetCategories();
        fetchAllSubcategories();
    }, []);

    const fetchSuppliers = async () => {
        try {
            const response = await axios.get(`${UrlLink}AccetCategory/suppliers_Data_Get/`);
            setSuppliers(response.data);
        } catch (error) {
            console.error('Error fetching suppliers:', error);
        }
    };

    const fetchAssetCategories = async () => {
        try {
            const response = await axios.get(`${UrlLink}AccetCategory/asset_categories_list/`);
            setAssetCategories(response.data);
        } catch (error) {
            console.error('Error fetching asset categories:', error);
        }
    };

    const fetchAllSubcategories = async () => {
        try {
            const response = await axios.get(`${UrlLink}AccetCategory/get_asset_subcategories/`);
            setAllSubcategories(response.data);
        } catch (error) {
            console.error('Error fetching all subcategories:', error);
        }
    };

    const fetchSubcategories = (categoryId) => {
        const filteredSubcategories = allSubcategories.filter(subcat => subcat.category === parseInt(categoryId));
        setDisplayedSubcategories(filteredSubcategories);

        // Preserve selected subcategories during editing
        if (editingSupplier) {
            const selectedSubcategories = editingSupplier.subcategories.map(subcat => subcat.id);
            setFormData(prev => ({ ...prev, subcategories: selectedSubcategories }));
        }
    };


    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => {
            const updatedData = { ...prev, [name]: value };
            if (name === 'asset_category') {
                fetchSubcategories(value);
            }
            return updatedData;
        });
    };

    const handleSubcategoryChange = (e) => {
        const { value, checked } = e.target;
        setFormData(prev => ({
            ...prev,
            subcategories: checked
                ? [...prev.subcategories, parseInt(value)]
                : prev.subcategories.filter(id => id !== parseInt(value))
        }));
    };


    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            if (editingSupplier) {
                await axios.put(`${UrlLink}AccetCategory/suppliers_Data_Put/${editingSupplier.id}/`, formData);

            } else {
                await axios.post(`${UrlLink}AccetCategory/suppliers_Data/`, formData);
            }
            fetchSuppliers();
            resetForm();
        } catch (error) {
            console.error('Error saving supplier:', error);
        }
    };

    const handleEdit = (supplier) => {
        setEditingSupplier(supplier);

        // Fetch the subcategories for the asset category of this supplier
        setFormData({
            name: supplier.name,
            contact_info: supplier.contact_info,
            email: supplier.email,
            asset_category: supplier.asset_category,
            subcategories: supplier.subcategories.map(subcat => subcat), // Ensure the subcategories are stored as IDs
            status: supplier.status,
            ranking: supplier.ranking.toString(),
            remarks: supplier.remarks
        });

        // Fetch all subcategories for the selected asset category
        fetchSubcategories(supplier.asset_category);
    };


    const resetForm = () => {
        setFormData({
            name: '',
            contact_info: '',
            email: '',
            asset_category: '',
            subcategories: [],
            status: 'active',
            ranking: '1',
            remarks: ''
        });
        setEditingSupplier(null);
        setDisplayedSubcategories([]); // Clear displayed subcategories
    };
    const toggleStatus = async (supplier) => {
        try {
            const updatedSupplier = { ...supplier, status: supplier.status === 'active' ? 'inactive' : 'active' };

            await axios.put(`${UrlLink}AccetCategory/suppliers_Data_Put/${supplier.id}/`, updatedSupplier);

            fetchSuppliers();
        } catch (error) {
            console.error('Error toggling supplier status:', error);
        }
    };

    const supplierColumns = [
        {
            key: 'id',
            name: 'Supplier ID',
            frozen: true
        },
        {
            key: 'name',
            name: 'Supplier Name',
            frozen: true
        },
        {
            key: 'contact_info',
            name: 'Contact Info'
        },
        {
            key: 'email',
            name: 'Email'
        },
        {
            key: 'asset_category',
            name: 'Asset Category',
            renderCell: (params) => assetCategories.find(c => c.id === params.row.asset_category)?.name || 'N/A'
        },
        {
            key: 'subcategories',
            name: 'Subcategories',
            renderCell: (params) => params.row.subcategories.map(id => allSubcategories.find(s => s.id === id)?.name).join(', ')
        },
        {
            key: 'status',
            name: 'Status',
            renderCell: (params) => (
                <Button className="cell_btn" onClick={() => toggleStatus(params.row)}>
                    {params.row.status === 'active' ? "ACTIVE" : "INACTIVE"}
                </Button>
            )
        },
        {
            key: 'ranking',
            name: 'Ranking'
        },
        {
            key: 'remarks',
            name: 'Scheme/Remarks'
        },
        {
            key: 'action',
            name: 'Action',
            renderCell: (params) => (
                <Button className="cell_btn" onClick={() => handleEdit(params.row)}>
                    <EditIcon className="edit_icon" />
                </Button>
            )
        }
    ];

    return (
        <div className="Main_container_app">
            <h3>Supplier Management</h3>

            <div className="RegisFormcon_1">
                <div className="RegisForm_1">
                    <label>Supplier Name:</label>
                    <input
                        type="text"
                        name="name"
                        value={formData.name}
                        onChange={handleInputChange}
                        placeholder="Supplier Name"
                        required
                    />
                </div>

                <div className="RegisForm_1">
                    <label>Contact Info:</label>
                    <input
                        type="text"
                        name="contact_info"
                        value={formData.contact_info}
                        onChange={handleInputChange}
                        placeholder="Contact Info"
                        required
                    />
                </div>

                <div className="RegisForm_1">
                    <label>Email:</label>
                    <input
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleInputChange}
                        placeholder="Email"
                        required
                    />
                </div>

                <div className="RegisForm_1">
                    <label>Asset Category:</label>
                    <select
                        name="asset_category"
                        value={formData.asset_category}
                        onChange={handleInputChange}
                        required
                    >
                        <option value="">Select Asset Category</option>
                        {assetCategories.map(category => (
                            <option key={category.id} value={category.id}>{category.name}</option>
                        ))}
                    </select>
                </div>

                {formData.asset_category && (
                    <div className="RegisForm_1" style={{ display: 'flex', flexDirection: 'column' }}>
                        <label>Subcategories:</label>
                        <div style={{display:'flex',flexWrap:'wrap',gap:'10px'}}>
                            {displayedSubcategories.map(subcat => (
                                <label key={subcat.id} style={{display:'flex',alignItems:'center'}}>
                                    <input
                                        type="checkbox"
                                        value={subcat.id}
                                        checked={formData.subcategories.includes(subcat.id)}
                                        onChange={handleSubcategoryChange}
                                    />
                                    {subcat.name}
                                </label>
                            ))}
                        </div>

                    </div>
                )}


                <div className="RegisForm_1">
                    <label>Status:</label>
                    <select
                        name="status"
                        value={formData.status}
                        onChange={handleInputChange}
                    >
                        <option value="active">Active</option>
                        <option value="inactive">Inactive</option>
                    </select>
                </div>

                <div className="RegisForm_1">
                    <label>Ranking:</label>
                    <select
                        name="ranking"
                        value={formData.ranking}
                        onChange={handleInputChange}
                    >
                        {[1, 2, 3, 4, 5].map(rank => (
                            <option key={rank} value={rank}>{rank}</option>
                        ))}
                    </select>
                </div>

                <div className="RegisForm_1">
                    <label>Scheme/Remarks:</label>
                    <input
                        type="text"
                        name="remarks"
                        value={formData.remarks}
                        onChange={handleInputChange}
                        placeholder="Scheme or Remarks"
                    />
                </div>
            </div>

            <div className="Main_container_Btn">
                <button onClick={handleSubmit} style={{ width: "120px" }}>
                    {editingSupplier ? "Update Supplier" : "Add Supplier"}
                </button>
            </div>

            <ReactGrid columns={supplierColumns} RowData={suppliers} />
        </div>
    );


}
export default Suppliers;