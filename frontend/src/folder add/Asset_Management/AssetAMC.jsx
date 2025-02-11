
import axios from 'axios';
import React, { useCallback, useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import ToastAlert from '../../OtherComponent/ToastContainer/ToastAlert';
import { Button } from '@mui/material';
import ReactGrid from '../../OtherComponent/ReactGrid/ReactGrid';
import EditIcon from "@mui/icons-material/Edit";
import { format, differenceInDays } from 'date-fns';

const AssetAMC = () => {
    const [RackMasterPage, setRackMasterPage] = useState('AssetAMC')
    const [assetCategories, setAssetCategories] = useState([]);
    const [subcategories, setSubcategories] = useState([]);
    const [assets, setAssets] = useState([]);
    const [amcs, setAmcs] = useState([]);  // Fetch AMC List
    const [serviceProviders, setServiceProviders] = useState([]);
    const [error, setError] = useState('');
    const [selectedCategory, setSelectedCategory] = useState('');
    const [selectedSubcategory, setSelectedSubcategory] = useState('');
    const [selectedAsset, setSelectedAsset] = useState('');
    const [assetAMCData, setassetAMCData] = useState([]);

    const [isEditing, setIsEditing] = useState(false);  // Track editing state
    const [amcId, setAmcId] = useState(null);  // Store AMC ID for editing

    const [formData, setFormData] = useState({
        provider: '',
        start_date: '',
        end_date: '',
        cost: '',
        terms: '',
        warranty_type: 'partial',
        is_active: true,
    });

    useEffect(() => {
        fetchAssetCategories();
        fetchAMCs();  // Fetch AMC list on component mount
    }, []);

    // Fetch Asset Categories
    const fetchAssetCategories = async () => {
        try {
            const response = await axios.get('http://localhost:8000/api/asset-categories/');
            setAssetCategories(response.data);
        } catch (error) {
            console.error('Error fetching asset categories:', error);
        }
    };

    // Fetch Subcategories based on selected Category
    const fetchSubcategories = async (categoryId) => {
        try {
            const response = await axios.get(`http://localhost:8000/api/assets/get_subcategories/?category_id=${categoryId}`);
            setSubcategories(response.data);
        } catch (error) {
            console.error('Error fetching subcategories:', error);
        }
    };

    // Fetch Assets based on selected Subcategory
    const fetchAssets = async (subcategoryId) => {
        if (!subcategoryId) return;  // Don't make a request if no subcategory is selected

        try {
            const response = await axios.get(`http://localhost:8000/api/assets/get_assets_by_subcategory/?subcategory_id=${subcategoryId}`);
            if (response.data) {
                setAssets(response.data);
            }
        } catch (error) {
            console.error('Error fetching assets:', error);
        }
    };

    // Fetch Service Providers based on selected Subcategory
    /*const fetchServiceProviders = async (subcategoryId) => {
      if (!subcategoryId) return;
    
      try {
        const response = await axios.get(`http://localhost:8000/api/assets/get_service_providers/?subcategory_id=${subcategoryId}`);
        if (response.data) {
          setServiceProviders(response.data);
        }
      } catch (error) {
        console.error('Error fetching service providers:', error);
      }
    };*/
    const fetchServiceProviders = async (subcategoryId) => {
        if (!subcategoryId) {
            setServiceProviders([]);
            return;
        }
        try {
            const response = await axios.get(`http://localhost:8000/api/assets/get_serviceproviders?subcategory_id=${subcategoryId}`);
            setServiceProviders(response.data);
            setError('');
        } catch (error) {
            console.error('Error fetching Service Provider:', error.response ? error.response.data : error.message);
            setServiceProviders([]);
            setError('Failed to fetch Service Provider. Please try again.');
        }
    };



    // Call fetchServiceProviders when subcategory changes
    useEffect(() => {
        if (selectedSubcategory) {
            fetchServiceProviders(selectedSubcategory);
        }
    }, [selectedSubcategory]);


// Fetch AMCs List
const fetchAMCs = async () => {
    try {
        const response = await axios.get('http://localhost:8000/api/amcs/');
        setAmcs(response.data);  

        setassetAMCData(response.data); 

    } catch (error) {
        console.error('Error fetching AMCs:', error);
    }
};


    // Handle Category Change
    const handleCategoryChange = (e) => {
        const categoryId = e.target.value;
        setSelectedCategory(categoryId);
        setSelectedSubcategory('');
        setSelectedAsset('');
        setSubcategories([]);
        setAssets([]);
        if (categoryId) {
            fetchSubcategories(categoryId);
        }
    };

    // Handle Subcategory Change
    const handleSubcategoryChange = (e) => {
        const subcategoryId = e.target.value;
        setSelectedSubcategory(subcategoryId);
        setSelectedAsset('');
        setAssets([]);
        if (subcategoryId) {
            fetchAssets(subcategoryId);
        }
    };

    // Handle Form Input Change
    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    };

    // Handle Form Submission
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const dataToSend = {
                ...formData,
                asset: selectedAsset,
                cost: parseFloat(formData.cost),
            };

            let response;
            if (isEditing && amcId) {
                response = await axios.put(`http://localhost:8000/api/amcs/${amcId}/`, dataToSend);
            } else {
                response = await axios.post('http://localhost:8000/api/amcs/', dataToSend);
            }

            if (response.status === 201 || response.status === 200) {
                alert(`AMC successfully ${isEditing ? 'updated' : 'added'}!`);
                fetchAMCs();  // Refresh the AMC list after submission
                resetForm();
            }
        } catch (error) {
            console.error('Error saving AMC:', error);
        }
    };

    const handleEdit = (amc) => {
        setFormData({
            asset: amc.asset.toString(),
            provider: amc.provider ? amc.provider.toString() : '',
            start_date: amc.start_date,
            end_date: amc.end_date,
            cost: amc.cost.toString(),
            terms: amc.terms,
            warranty_type: amc.warranty_type,
            is_active: amc.is_active,
        });
        setIsEditing(true);
        setAmcId(amc.id);  // Store AMC ID for editing
    };

    const handleDelete = async (id) => {
        try {
            await axios.delete(`http://localhost:8000/api/amcs/${id}/`);
            fetchAMCs();  // Refresh the AMC list after deletion
        } catch (error) {
            console.error('Error deleting AMC:', error);
        }
    };

    const resetForm = () => {
        setFormData({
            asset: '',
            provider: '',
            start_date: '',
            end_date: '',
            cost: '',
            terms: '',
            warranty_type: 'partial',
            is_active: true,
        });
        setIsEditing(false);
    };

    const toggleStatus = async (amc) => {
        try {
            const updatedStatus = amc.status === 'active' ? 'inactive' : 'active';
            const response = await axios.patch(`http://localhost:8000/api/amcs/${amc.AMC_id}/`, { status: updatedStatus });

            if (response.status === 200) {
                setAmcs(prevAmcs =>
                    prevAmcs.map(item =>
                        item.AMC_id === amc.AMC_id ? { ...item, status: updatedStatus } : item
                    )
                );
            }
        } catch (error) {
            console.error('Error toggling AMC status:', error);
        }
    };

    const handleEditAssetCategory = (amc) => {
        setFormData({
            asset: amc.AMC_asset_name.toString(),
            provider: amc.AMC_provider_name ? amc.AMC_provider_name.toString() : '',
            start_date: amc.AMC_start_date,
            end_date: amc.AMC_end_date,
            cost: amc.AMC_cost.toString(),
            warranty_type: amc.warranty_type,
            is_active: amc.status === 'active',
        });
        setIsEditing(true);
        setAmcId(amc.AMC_id); // Store AMC ID for editing
    };


    const assetAMCColumn = [
        {
            key: 'AMC_id',
            name: 'AMC ID',
        },
        {
            key: 'AMC_asset_name',
            name: 'AMC Asset Name'
        },
        {
            key: 'AMC_provider_name',
            name: 'AMC Provider Name',
        },
        {
            key: 'AMC_start_date',
            name: 'AMC Start Date',
        },
        {
            key: 'AMC_end_date',
            name: 'AMC End Date',
        },
        {
            key: 'AMC_cost',
            name: 'AMC Cost',
        },
        {
            key: 'warranty_type',
            name: 'Warranty Type',
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
            key: 'Action',
            name: 'Action',
            renderCell: (params) => (
                <Button className="cell_btn" onClick={() => handleEditAssetCategory(params.row)}>
                    <EditIcon className="check_box_clrr_cancell" />
                </Button>
            )
        }
    ]
    // -----------------------------Asset AMC Near Expiry----------------------------------------

    const [amcss, setAMCs] = useState([]);

    useEffect(() => {
        axios.get('http://localhost:8000/api/amcs/')
            .then(response => {
                const today = new Date();
                const upcomingAMCs = response.data.filter(amc => {
                    const endDate = new Date(amc.end_date);
                    const daysLeft = differenceInDays(endDate, today);
                    return daysLeft > 0 && daysLeft <= 14;
                });
                setAMCs(upcomingAMCs);
            })
            .catch(error => console.error(error));
    }, []);


    return (
        <>
            <div className="Main_container_app">
                <h3>Asset AMC</h3>

                <br />
                <div className="RegisterTypecon">
                    <div className="RegisterType">

                        {["AssetAMC", "AMCNearExpiry"].map((p, ind) => (

                            <div className="registertypeval" key={ind}>
                                <input
                                    type="radio"
                                    id={p}
                                    name="appointment_type"
                                    checked={RackMasterPage === p}
                                    onChange={(e) => {
                                        setRackMasterPage(e.target.value)
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
                {/* -------------------------Asset AMC------------------------- */}
                {RackMasterPage === 'AssetAMC' && <>
                    <br />
                    <div className="Main_container_app">

                        <div className="RegisFormcon_1" >
                            {/* Asset Category Dropdown */}
                            <div className="RegisForm_1">
                                <label>Asset Category <span>:</span></label>
                                <select value={selectedCategory} onChange={handleCategoryChange} required>
                                    <option value="">Select Asset Category</option>
                                    {assetCategories.map((category) => (
                                        <option key={category.id} value={category.id}>{category.name}</option>
                                    ))}
                                </select>
                            </div>

                            {/* Asset Subcategory Dropdown */}
                            <div className="RegisForm_1">
                                <label>Asset Subcategory <span>:</span></label>
                                <select value={selectedSubcategory} onChange={handleSubcategoryChange} disabled={!selectedCategory} required>
                                    <option value="">Select Asset Subcategory</option>
                                    {subcategories.map((subcategory) => (
                                        <option key={subcategory.id} value={subcategory.id}>{subcategory.name}</option>
                                    ))}
                                </select>
                            </div>

                            {/* Asset Dropdown */}
                            <div className="RegisForm_1">
                                <label>Asset <span>:</span></label>
                                <select value={selectedAsset} onChange={(e) => setSelectedAsset(e.target.value)} disabled={!selectedSubcategory} required>
                                    <option value="">Select Asset</option>
                                    {assets.map((asset) => (
                                        <option key={asset.id} value={asset.id}>{asset.name}</option>
                                    ))}
                                </select>
                            </div>

                            {/* Provider */}
                            <div className="RegisForm_1">
                                <label>Provider <span>:</span></label>
                                <input type="text" name="provider" value={formData.provider} onChange={handleInputChange} placeholder="Provider" required />
                            </div>

                            {/* Start Date */}
                            <div className="RegisForm_1">
                                <label>Start Date <span>:</span></label>
                                <input type="date" name="start_date" value={formData.start_date} onChange={handleInputChange} required />
                            </div>

                            {/* End Date */}
                            <div className="RegisForm_1">
                                <label>End Date <span>:</span></label>
                                <input type="date" name="end_date" value={formData.end_date} onChange={handleInputChange} required />
                            </div>

                            {/* Cost */}
                            <div className="RegisForm_1">
                                <label>Cost <span>:</span></label>
                                <input type="number" name="cost" value={formData.cost} onChange={handleInputChange} placeholder="Cost" required />
                            </div>

                            {/* Terms */}
                            <div className="RegisForm_1">
                                <label>Terms and Conditions <span>:</span></label>
                                <textarea name="terms" value={formData.terms} onChange={handleInputChange} placeholder="Terms and Conditions" required />
                            </div>


                            {/* Warranty Type */}
                            <div className="RegisForm_1">
                                <label>Warranty Type <span>:</span></label>
                                <select name="warranty_type" value={formData.warranty_type} onChange={handleInputChange} required>
                                    <option value="partial">Parts Only</option>
                                    <option value="full">Full Replacement</option>
                                </select>
                            </div>

                            {/* Active Status */}
                            <div className="RegisForm_1">
                                <label>Active <span>:</span></label>
                                <input type="checkbox" name="is_active" checked={formData.is_active} onChange={(e) => setFormData((prevData) => ({ ...prevData, is_active: e.target.checked }))} />
                            </div>
                        </div>

                        <div className="Main_container_Btn">
                            <button onClick={handleSubmit} style={{ width: "95px" }}>Add AMC</button>
                        </div>
                        <ReactGrid columns={assetAMCColumn} RowData={assetAMCData} />
                    </div>

                </>}
                {/* -------------------------AMCNearExpiry----------------------- */}
                {RackMasterPage === 'AMCNearExpiry' && <>
                    <br />
                    <div className="Main_container_app">
                        <h2>AMCs Near Expiry</h2>
                        <div className="RegisFormcon_1" >

                            <div className="RegisForm_1">
                                <ul>
                                    {amcss.map(amc => (
                                        <li key={amc.id}>
                                            AMC for {amc.asset} - Ends on {format(new Date(amc.end_date), 'yyyy-MM-dd')}
                                            (in {differenceInDays(new Date(amc.end_date), new Date())} days)
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    </div>

                </>}
            </div>
        </>
    )
}
export default AssetAMC;