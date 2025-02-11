import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ReactGrid from '../../OtherComponent/ReactGrid/ReactGrid';
import { Button } from '@mui/material';
import EditIcon from "@mui/icons-material/Edit";
import { useSelector } from 'react-redux';
import PersonSearchIcon from "@mui/icons-material/PersonSearch";


const ChecklistMasterEntry = () => {
    const [categories, setCategories] = useState([]);
    const [allSubcategories, setAllSubcategories] = useState([]);
    const [filteredSubcategories, setFilteredSubcategories] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState('');
    const [selectedSubcategory, setSelectedSubcategory] = useState('');
    const [newItem, setNewItem] = useState({ itemname: '' });
    const [editingItem, setEditingItem] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');
    const [CheckListMasterEntryData, setCheckListMasterEntryData] = useState([]);
    const UrlLink = useSelector(state => state.userRecord?.UrlLink);


    const Handlesearch = () => {
        if (!searchTerm.trim()) {
            fetchAllData(); // Reload full data if search is empty
            return;
        }
        const filteredData = CheckListMasterEntryData.filter(item =>
            item.item_name.toLowerCase().includes(searchTerm.toLowerCase())
        );
        setCheckListMasterEntryData(filteredData);
    };


    // Fetch all data on initial load
    useEffect(() => {
        fetchAllData();
        fetchCategories();
        fetchAllSubcategories();
    }, [UrlLink]);

    // Function to fetch all data
    const fetchAllData = () => {
        axios.get(`${UrlLink}AccetCategory/ChecklistMasterEntry_get/`)
            .then(response => {
                if (response.data.status === 'success') {
                    const formattedData = Array.isArray(response.data.data)
                        ? response.data.data.map(item => ({
                            ...item,
                            subcategories: item.subcategories || []
                        }))
                        : [];
                    setCheckListMasterEntryData(formattedData);
                }
            })
            .catch(error => {
                console.error('Error fetching all data:', error);
                setCheckListMasterEntryData([]);
            });
    };
    const fetchCategories = () => {
        axios.get(`${UrlLink}AccetCategory/asset_categories_list/`)
            .then(response => {
                setCategories(response.data);
            })
            .catch(error => {
                console.error('Error fetching asset categories:', error);
            });
    };

    const fetchAllSubcategories = () => {
        axios.get(`${UrlLink}AccetCategory/get_asset_subcategories/`)
            .then(response => {
                setAllSubcategories(response.data);
            })
            .catch(error => {
                console.error('Error fetching all asset subcategories:', error);
            });
    };

    useEffect(() => {
        if (selectedCategory) {
            filterSubcategories(selectedCategory);
            setSelectedSubcategory((prev) => prev || '');
        }
    }, [selectedCategory]);


    useEffect(() => {
        if (selectedCategory || selectedSubcategory) {
            fetchFilteredData();
        } else {
            fetchAllData();
        }
    }, [selectedCategory, selectedSubcategory]);

    const fetchFilteredData = () => {
        const params = {};
        if (selectedCategory) params.asset_category = selectedCategory;
        if (selectedSubcategory) params.subcategory = selectedSubcategory;

        axios.get(`${UrlLink}AccetCategory/ChecklistMasterEntry_get/`, { params })
            .then(response => {
                if (response.data.status === 'success') {
                    const formattedData = response.data.data.map(item => ({
                        ...item,
                        subcategories: Array.isArray(item.subcategories) ? item.subcategories : [] // Ensure it's always an array
                    }));
                    setCheckListMasterEntryData(formattedData);
                }
            })
            .catch(error => {
                console.error('Error fetching filtered data:', error);
                setCheckListMasterEntryData([]);
            });
    };

    useEffect(() => {
        console.log("Updated selectedSubcategory:", selectedSubcategory);
    }, [selectedSubcategory]);


    const filterSubcategories = (categoryId) => {
        if (!categoryId) {
            setFilteredSubcategories([]);
            return;
        }
        const filtered = allSubcategories.filter(sub => sub.category.toString() === categoryId.toString());
        setFilteredSubcategories(filtered);
    };

    const handleCategoryChange = (e) => {
        setSelectedCategory(e.target.value);
    };

    const handleSubcategoryChange = (e) => {
        const newValue = e.target.value;
        console.log("Subcategory changed to:", newValue);
        setSelectedSubcategory(newValue);
    };



    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewItem(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const itemToSubmit = {
            item_name: newItem.itemname,
            asset_category: selectedCategory,
            subcategories: selectedSubcategory ? [selectedSubcategory] : []
        };

        if (editingItem) {
            handleUpdate(itemToSubmit);
        } else {
            handleAdd(itemToSubmit);
        }
    };

    const handleAdd = (itemToSubmit) => {
        axios.post(`${UrlLink}AccetCategory/ChecklistMasterEntry_post/`, itemToSubmit)
            .then(response => {
                if (response.data.status === 'success') {
                    fetchAllData();
                    setNewItem({ itemname: '' });
                }
            })
            .catch(error => {
                console.error('Error adding new checklist item:', error);
            });
    };

    const handleEdit = (item) => {
        console.log("Editing Item:", item);
        console.log("Category:", item.asset_category);
        console.log("Subcategories:", item.subcategories); // Corrected log

        setEditingItem(item);
        setNewItem({ itemname: item.item_name });
        setSelectedCategory(item.asset_category);

        // Check if subcategories exist and set the first one
        if (item.subcategories && item.subcategories.length > 0) {
            setSelectedSubcategory(item.subcategories[0] || '');
            console.log("Subcategories:", item.subcategories);

        } else {
            setSelectedSubcategory('');
        }

        filterSubcategories(item.asset_category);
    };





    const handleUpdate = (itemToSubmit) => {
        axios.put(`${UrlLink}AccetCategory/ChecklistMasterEntry_Put/${editingItem.id}/`, itemToSubmit)
            .then(response => {
                if (response.data.status === 'success') {
                    fetchAllData();
                    setEditingItem(null);
                    setNewItem({ itemname: '' });
                }
            })
            .catch(error => {
                console.error('Error updating checklist item:', error);
            });
    };

    const toggleStatus = async (item) => {
        try {
            const updatedItem = { ...item, status: item.status === 'active' ? 'inactive' : 'active' };
            await axios.put(`${UrlLink}AccetCategory/ChecklistMasterEntry_Put/${item.id}/`, updatedItem);
            fetchAllData();
        } catch (error) {
            console.error('Error toggling item status:', error);
        }
    };

    const CheckListMasterEntryColumns = [
        {
            key: 'id',
            name: 'Item ID',
        },
        {
            key: 'item_name',
            name: 'Item Name',
        },
        {
            key: 'asset_category',
            name: 'Asset Category',
            renderCell: (params) => categories.find(c => c.id === params.row.asset_category)?.name || 'N/A'
        },
        {
            key: 'subcategories',
            name: 'Subcategories',
            renderCell: (params) => {
                if (!params.row.subcategories || params.row.subcategories.length === 0) {
                    return 'N/A';
                }
                return params.row.subcategories
                    .map(id => allSubcategories.find(s => s.id === id)?.name || 'Unknown')
                    .join(', ');
            }
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
            key: "Action",
            name: 'Action',
            renderCell: (params) => (
                <Button className="cell_btn" onClick={() => handleEdit(params.row)}>
                    <EditIcon className="check_box_clrr_cancell" />
                </Button>
            )
        }
    ];

    return (
        <div className="Main_container_app">
            <h3>Check List Master</h3>
            <br />
            <div className="RegisForm_1" >
                <label>
                    Search Items<span>:</span>
                </label>
                <input
                    type="text"
                    placeholder="Search items..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
                <span>
                    <PersonSearchIcon onClick={Handlesearch} />
                </span>
            </div>
            <br />
            <div className="RegisFormcon_1" style={{ justifyContent: 'center' }}>
                <div className="RegisForm_1">
                    <label>
                        Asset Category <span>:</span>
                    </label>
                    <select
                        value={selectedCategory}
                        onChange={handleCategoryChange}
                    >
                        <option value="">All Categories</option>
                        {categories.map(category => (
                            <option key={category.id} value={category.id}>{category.name}</option>
                        ))}
                    </select>
                </div>

                <div className="RegisForm_1">
                    <label>
                        Subcategory <span>:</span>
                    </label>
                    <select value={selectedSubcategory || ""} onChange={handleSubcategoryChange}>
                        <option value="">All Subcategories</option>
                        {filteredSubcategories.map((sub) => (
                            <option key={sub.id} value={sub.id}>
                                {sub.name}
                            </option>
                        ))}
                    </select>
                </div>
            </div>
            <br />
            {(selectedCategory || editingItem) && (
                <div className="RegisFormcon_1">
                    <div className="RegisForm_1">
                        <label>
                            Item Name <span>:</span>
                        </label>
                        <input
                            type="text"
                            name="itemname"
                            value={newItem.itemname}
                            onChange={handleInputChange}
                            placeholder="Item Name"
                            required
                        />
                    </div>
                </div>
            )}

            <div className="Main_container_Btn">
                <button onClick={handleSubmit} style={{ width: "95px" }}>
                    {editingItem ? "Update" : "Add"}
                </button>
            </div>

            <ReactGrid columns={CheckListMasterEntryColumns} RowData={CheckListMasterEntryData} />
        </div>
    );
};

export default ChecklistMasterEntry;