import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ReactGrid from '../../OtherComponent/ReactGrid/ReactGrid';
import { Button } from '@mui/material';
import EditIcon from "@mui/icons-material/Edit";
import { useSelector } from 'react-redux';



const AssetManagement = () => {
    const convertToNumber = (value) => {
        if (value === '' || value === null || value === undefined) return null;
        return Number(value);
    };

    const [RackMasterPage, setRackMasterPage] = useState('AssetRegister')
    const UrlLink = useSelector(state => state.userRecord?.UrlLink);


    // -------------------------------------------------AssetReg-------------------------------------
    const [assetCategories, setAssetCategories] = useState([]);
    const [subcategories, setSubcategories] = useState([]);
    const [suppliers, setSuppliers] = useState([]);
    const [isEditing, setIsEditing] = useState(false);
    const [assetId, setAssetId] = useState(null);
    const [error, setError] = useState('');
    const [assets, setAssets] = useState([]);



    const initialFormState = {
        id: '',
        name: '',
        category: '',
        asset_subcategory: '',
        supplier: '',
        Company_Brand: '',
        // department: '',
        current_location: '',
        room_no: '',
        condition: '',
        status: '',
        purchase_date: '',
        purchase_price: '',
        market_value: '',
        total_working_life: '',
        expected_working_life: '',
        valuation_method: '',
        is_new_asset: true,
        depreciation_method: '',
        depreciation_rate: '',
        salvage_value: '',
        appreciation_rate: '',
    };

    const [AssetformData, setAssetFormData] = useState(initialFormState);



    useEffect(() => {
        const initializeData = async () => {
            try {
                await Promise.all([
                    fetchAssetsList(),
                    fetchAssetCategories(),
                    // fetchDepartmentsAsset()
                ]);
            } catch (error) {
                setError('Failed to initialize data');
            }
        };

        initializeData();
    }, []);

    const fetchAssetsList = async () => {
        try {
            const response = await axios.get(`${UrlLink}AccetCategory/Asset_Reg_Get/`);
            console.log("API Response:", response.data);

            const processedData = response.data.map(asset => {
                const baseCode = `${asset.name.substring(0, 2).toUpperCase()}/${asset.current_location.split(' ').map(word => word[0]).join('').toUpperCase()
                    }/${new Date(asset.purchase_date).toISOString().slice(2, 10).replace(/-/g, '')}`;

                const existingCodes = response.data.map(item => item.asset_code);

                let count = 1;
                let uniqueCode = baseCode;

                while (existingCodes.includes(uniqueCode)) {
                    uniqueCode = `${baseCode}/${String(count).padStart(2, '0')}`;
                    count++;
                }

                return {
                    ...asset,
                    is_new_asset: asset.is_new_asset ?? false,
                    purchase_date: asset.purchase_date ? new Date(asset.purchase_date).toISOString().split('T')[0] : 'N/A',
                    current_value: asset.current_value ? parseFloat(asset.current_value).toFixed(2) : 'N/A',
                    asset_code: uniqueCode
                };
            });

            setAssets(processedData);
        } catch (error) {
            setError('Error fetching assets list');
        }
    };



    const fetchAssetCategories = async () => {
        try {
            const response = await axios.get(`${UrlLink}AccetCategory/asset_categories_list/`);
            setAssetCategories(response.data);
        } catch (error) {
            setError('Error fetching asset categories');
        }
    };

    const fetchSubcategoriesAssetList = async (categoryId) => {
        if (!categoryId) {
            setSubcategories([]);
            return;
        }
        try {
            const response = await axios.get(
                `${UrlLink}AccetCategory/get_asset_subcategories/?category_id=${categoryId}`);
            setSubcategories(response.data);
        } catch (error) {
            setError('Error fetching subcategories');
            setSubcategories([]);
        }
    };

    const fetchSuppliers = async (subcategoryId) => {
        if (!subcategoryId) {
            setSuppliers([]);
            return;
        }
        try {
            const response = await axios.get(
                `${UrlLink}AccetCategory/suppliers_Data_Get/?subcategory_id=${subcategoryId}`);
            setSuppliers(response.data);
        } catch (error) {
            setError('Error fetching suppliers');
            setSuppliers([]);
        }
    };

    const handleInputChange = (e) => {
        const { name, value, type, checked } = e.target;
        const newValue = type === 'checkbox' ? checked : value;

        setAssetFormData(prevData => ({
            ...prevData,
            [name]: newValue
        }));

        if (name === 'category') {
            fetchSubcategoriesAssetList(value);
            setAssetFormData(prevData => ({
                ...prevData,
                asset_subcategory: '',
                supplier: '',
                category: value
            }));
        } else if (name === 'asset_subcategory') {
            fetchSuppliers(value);
            setAssetFormData(prevData => ({
                ...prevData,
                supplier: '',
                Company_Brand: '',
                asset_subcategory: value
            }));
        } else if (name === 'valuation_method') {
            setAssetFormData(prevData => ({
                ...prevData,
                depreciation_method: '',
                depreciation_rate: '',
                salvage_value: '',
                appreciation_rate: '',
                valuation_method: value
            }));
        }
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError('');

        // Generate asset code
        const baseCode = `${AssetformData.name.substring(0, 2).toUpperCase()}/${AssetformData.current_location.split(' ').map(word => word[0]).join('').toUpperCase()
            }/${new Date(AssetformData.purchase_date).toISOString().slice(2, 10).replace(/-/g, '')}`;

        const existingCodes = assets.map(item => item.asset_code);

        let count = 1;
        let uniqueCode = baseCode;

        while (existingCodes.includes(uniqueCode)) {
            uniqueCode = `${baseCode}/${String(count).padStart(2, '0')}`;
            count++;
        }

        const formDataToSubmit = {
            ...AssetformData,
            purchase_date: AssetformData.purchase_date 
            ? new Date(AssetformData.purchase_date).toISOString().split('T')[0]  // This will give YYYY-MM-DD
            : null,
            asset_code: uniqueCode,
            asset_subcategory: AssetformData.asset_subcategory || null,
            supplier: AssetformData.supplier ? [AssetformData.supplier] : [],
            purchase_price: convertToNumber(AssetformData.purchase_price),
            market_value: convertToNumber(AssetformData.market_value),
            total_working_life: convertToNumber(AssetformData.total_working_life),
            expected_working_life: convertToNumber(AssetformData.expected_working_life),
            depreciation_rate: convertToNumber(AssetformData.depreciation_rate),
            salvage_value: convertToNumber(AssetformData.salvage_value),
            appreciation_rate: convertToNumber(AssetformData.appreciation_rate)
        };
        console.log("Submitting FormData:", formDataToSubmit);


        try {
            let response;
            if (AssetformData.id) {
                // Update existing asset (PUT request)
                response = await axios.put(`${UrlLink}AccetCategory/Asset_Reg_put/${AssetformData.id}/`, formDataToSubmit);
            } else {
                // Create new asset (POST request)
                response = await axios.post(`${UrlLink}AccetCategory/Asset_Reg_post/`, formDataToSubmit);
            }
            console.log('Response:', response.data);
            
            await fetchAssetsList();
            resetForm();
        } catch (error) {
            console.error('Error payload:', formDataToSubmit);
            console.error('Error response:', error.response?.data);
            setError(error.response?.data?.error || 'Failed to create asset');
        }
    };

    const handleEditAssetReg = (row) => {
        setAssetId(row.id);
        setIsEditing(true);
        setAssetFormData({
            ...initialFormState,
            ...row,
            category: row.category?.toString() || '',
            asset_subcategory: row.asset_subcategory || '',
            supplier: row.supplier?.toString() || '',
            // department: row.department?.toString() || ''
        });

        if (row.category) fetchSubcategoriesAssetList(row.category);
        if (row.asset_subcategory) fetchSuppliers(row.asset_subcategory);
    };

    const resetForm = () => {
        setAssetFormData(initialFormState);
        setIsEditing(false);
        setAssetId(null);
        setSubcategories([]);
        setSuppliers([]);
    };

    const toggleStatusAssetReg = async (row) => {
        try {
            const newStatus = row.status === 'active' ? 'inactive' : 'active';
            await axios.put(
                `${UrlLink}AccetCategory/Asset_Reg_put/${row.id}/`,
                { status: newStatus },
            );
            await fetchAssetsList();
        } catch (error) {
            setError('Error updating status');
        }
    };

    const assetRegColumn = [
        {
            key: 'Asset_id',
            name: 'Asset id',
        },
        {
            key: 'Asset_name',
            name: 'Asset Name',
        },
        {
            key: 'asset_code',
            name: 'Asset Code',
            renderCell: (params) => params.row.asset_code || 'N/A'
        }
        , {
            key: 'category_name',
            name: 'category Name',
        }, {
            key: 'subcategory_name',
            name: 'subcategory Name',
            renderCell: (params) => (Array.isArray(params.row.subcategory_name) ? params.row.subcategory_name.join(', ') : 'N/A')

        }, {
            key: 'supplier_name',
            name: 'supplier Name',
        }, {
            key: 'Company_Brand',
            name: 'Company Brand',
        },
        {
            key: 'is_new_asset',
            name: 'Is New Asset',
            renderCell: (params) => (params.row.is_new_asset ? "Yes" : "No")
        },
        // {
        //     key: 'department_name',
        //     name: 'department Name',
        // }, 
        {
            key: 'current_location',
            name: 'current location',
        }, {
            key: 'room_no',
            name: 'room No',
        }, {
            key: 'condition',
            name: 'condition',
        }, {
            key: 'purchase_date',
            name: 'purchase Date',
        }, {
            key: 'purchase_price',
            name: 'purchase Price',
        },
        {
            key: 'market_value',
            name: 'market Value',
        },
        {
            key: 'total_working_life',
            name: 'Total Working Life',
        }, {
            key: 'life_completed',
            name: 'Life Completed',
        }, {
            key: 'life_remain',
            name: 'life Remain',
        }, {
            key: 'current_value',
            name: 'current Value',
        }, {
            key: 'expected_working_life',
            name: 'Expected Working Life',
        }, {
            key: 'valuation_method',
            name: 'Valuation Method',
        }, {
            key: 'depreciation_method',
            name: 'Depreciation Method',
        }, {
            key: 'depreciation_rate',
            name: 'Depreciation Rate',
        }, {
            key: 'appreciation_rate',
            name: 'Appreciation Rate',
        },
        {
            key: 'status',
            name: 'status',
            renderCell: (params) => (
                <Button className="cell_btn" onClick={() => toggleStatusAssetReg(params.row)}>
                    {params.row.status === 'active' ? "ACTIVE" : "INACTIVE"}
                </Button>
            )
        }, {
            key: 'Actions',
            name: 'Actions',
            renderCell: (params) => (
                <Button className="cell_btn" onClick={() => handleEditAssetReg(params.row)}>
                    <EditIcon className="check_box_clrr_cancell" />
                </Button>
            )
        },
    ]
    //  ------------------------------------------------------------------------------------------------
    // -------------------------------------------AssetList---------------------------------------------
    //// AssetList States
    const [AssetListSearchTerm, setAssetListSearchTerm] = useState('');
    const [AssetListCategories, setAssetListCategories] = useState([]);
    const [AssetListSubcategories, setAssetListSubcategories] = useState([]);
    // const [AssetListDepartments, setAssetListDepartments] = useState([]);
    const [AssetListData, setAssetListData] = useState([]);
    const [AssetListEditing, setAssetListEditing] = useState(null);
    const [AssetListRegData, setAssetListRegData] = useState([]);

    // AssetList Filters
    const [AssetListFilters, setAssetListFilters] = useState({
        name: '',
        category_id: '',
        subcategory_id: '',
        // department: '',
        asset_code: '',
        supplier: '',
        status: '',
        condition: '',
        valuation_method: '',
    });
    console.log("AssetListData:", AssetListData);


    useEffect(() => {
        AssetListFetchCategories();
        AssetListFetchRegData();
    }, []);



    useEffect(() => {
        AssetListFetchAssets();
    }, [AssetListFilters, AssetListSearchTerm]);

    useEffect(() => {
        console.log('Filters:', AssetListFilters);
        AssetListFetchAssets();
    }, [AssetListFilters, AssetListSearchTerm]);

    // Fetch categories
    const AssetListFetchCategories = async () => {
        try {
            const response = await axios.get(`${UrlLink}AccetCategory/asset_categories_list/`);
            setAssetListCategories(response.data);
        } catch (error) {
            console.error('Error fetching categories:', error);
        }
    };

    // Fetch registration data
    const AssetListFetchRegData = async () => {
        try {
            const response = await axios.get(`${UrlLink}AccetCategory/Asset_Reg_Get/`);
            setAssetListRegData(response.data);
        } catch (error) {
            console.error('Error fetching asset registration data:', error.response ? error.response.data : error.message);
        }
    };

    // Fetch subcategories
    const AssetListFetchSubcategories = async (categoryId) => {
        try {
            const response = await axios.get(`${UrlLink}AccetCategory/get_asset_subcategories/?category_id=${categoryId}`);
            setAssetListSubcategories(response.data);
        } catch (error) {
            console.error('Error fetching subcategories:', error);
        }
    };

    // Fetch departments
    // const AssetListFetchDepartments = async () => {
    //     try {
    //         const response = await axios.get('http://localhost:8000/api/departments/');
    //         setAssetListDepartments(response.data);
    //     } catch (error) {
    //         console.error('Error fetching departments:', error);
    //     }
    // };

    // Fetch assets
    const AssetListFetchAssets = async () => {
        try {
            console.log("Fetching asset list...");

            const params = {
                name: AssetListSearchTerm.trim() || '',
                asset_code: AssetListFilters.asset_code || '',  // Include asset_code in params
                category_id: AssetListFilters.category_id || '',
                subcategory_id: AssetListFilters.subcategory_id || '',
                supplier: AssetListFilters.supplier || '',
                status: AssetListFilters.status || '',
                condition: AssetListFilters.condition || '',
                valuation_method: AssetListFilters.valuation_method || '',
            };

            console.log("Sending Params:", params);

            const response = await axios.get(`${UrlLink}AccetCategory/assetList_Get/`, { params });
            console.log("Full Response:", response.data);
            setAssetListData(response.data);
        } catch (error) {
            console.error("Error fetching assets:", error.response?.data || error.message);
            setAssetListData([]);
        }
    };

    const AssetListUpdateAssets = async (assetId) => {
        try {
            if (!assetId) {
                console.error("No asset ID provided for update");
                return;
            }

            // Validate asset code format
            if (!AssetListFilters.asset_code) {
                alert("Asset code is required!");
                return;
            }

            const updateData = {
                id: assetId,
                name: AssetListFilters.name,
                asset_code: AssetListFilters.asset_code,
                category_id: AssetListFilters.category_id,
                subcategory_id: AssetListFilters.subcategory_id,
                supplier: AssetListFilters.supplier,
                status: AssetListFilters.status,
                condition: AssetListFilters.condition,
                valuation_method: AssetListFilters.valuation_method,
            };

            console.log("Sending update data:", updateData);

            const response = await axios.put(`${UrlLink}AccetCategory/assetList_PUT/${assetId}/`, updateData);
            console.log("Update response:", response.data);

            setAssetListEditing(null);
            await AssetListFetchAssets();
            alert("Asset updated successfully!");
        } catch (error) {
            console.error("Error updating asset:", error);
            alert("Failed to update asset. Please try again.");
        }
    };

    // Handle search
    const AssetListHandleSearch = (e) => {
        setAssetListSearchTerm(e.target.value);
    };

    // Handle filter changes
    const AssetListHandleFilterChange = (e) => {
        const { name, value } = e.target;

        setAssetListFilters(prevFilters => ({
            ...prevFilters,
            [name]: value,
        }));

        if (name === 'category') {
            setAssetListFilters(prevFilters => ({
                ...prevFilters,
                subcategory: '',
            }));
            AssetListFetchSubcategories(value);
        }
    };

    // // Handle page change
    // const AssetListHandlePageChange = (newPage) => {
    //     setCurrentPage(newPage);
    // };

    // Print function
    const AssetListHandlePrint = () => {
        window.print();
    };

    const AssetListHandle = async () => {
        console.log("Handling asset request...");
        if (AssetListFilters.category) {
            await AssetListUpdateAssets();
        } else {
            await AssetListFetchAssets();
        }
    };

    // Handle edit asset
    const AssetListHandleEdit = (asset) => {
        console.log("Selected Asset:", asset);

        setAssetListEditing(asset);
        setAssetListFilters({
            name: asset.name || '',
            asset_code: asset.asset_code || '',  
            category_id: asset.category?.id || '',
            subcategory_id: asset.subcategory?.[0]?.id || '',
            supplier: Array.isArray(asset.supplier) ? asset.supplier[0] : asset.supplier || '',
            status: asset.status || '',
            condition: asset.condition || '',
            valuation_method: asset.valuation_method || '',
        });

        if (asset.category?.id) {
            AssetListFetchSubcategories(asset.category.id);
        }
    };

    const toggleStatusAssetList = async (asset) => {
        try {
            const newStatus = { ...asset, status: asset.status === 'active' ? 'inactive' : 'active' };

            await axios.put(`${UrlLink}AccetCategory/assetList_PUT/`, {
                asset_id: asset.id,
                status: newStatus,
            });
            AssetListFetchAssets();
        } catch (error) {
            console.error('Error updating asset status:', error);
        }
    };


    // AssetList Columns
    const AssetListColumns = [
        { key: "name", name: "Name" },
        {
            key: 'asset_code',
            name: 'Asset Code',
            renderCell: (params) => params.row.asset_code || 'N/A'
        },
        {
            key: "category",
            name: "Category",
            renderCell: (params) => params.row.category?.name || 'N/A'
        },
        {
            key: "subcategory",
            name: "Subcategory",
            renderCell: (params) => {
                const subcategories = params.row.subcategory || [];
                return subcategories.map(sub => sub.name).join(', ') || 'N/A';
            }
        }
        ,
        { key: "supplier", name: "Supplier" },
        { key: "condition", name: "Condition" },
        { key: "valuation_method", name: "Valuation Method" },
        {
            key: "status", name: "Status",
            renderCell: (params) => (
                <Button className="cell_btn" onClick={() => toggleStatusAssetList(params.row)}>
                    {params.row.status === 'active' ? "ACTIVE" : "INACTIVE"}
                </Button>
            )
        },
        // {
        //     key: "Actions", name: "Actions",
        //     renderCell: (params) => (
        //         <Button className="cell_btn" onClick={() => AssetListHandleEdit(params.row)}>
        //             <EditIcon className="check_box_clrr_cancell" />
        //         </Button>
        //     )
        // },
    ];



    // -----------------------------Search Asset---------------------------------------
    const [searchAsset_List, setSearchAsset_List] = useState([]);
    const [searchAsset_CategoryList, setSearchAsset_CategoryList] = useState([]);
    const [searchAsset_SubcategoryList, setSearchAsset_SubcategoryList] = useState([]);
    // const [searchAsset_DepartmentList, setSearchAsset_DepartmentList] = useState([]);
    const [searchAsset_Data, setSearchAsset_Data] = useState([]);
    const [searchAsset_SelectedForEditing, setSearchAsset_SelectedForEditing] = useState(null);

    const [searchAsset_Filters, setSearchAsset_Filters] = useState({
        assetName: '',
        categoryId: '',
        subcategoryId: '',
        // departmentId: '',
        valuationMethod: '',
        conditionStatus: '',
        assetStatus: '',
    });

    useEffect(() => {
        fetchSearchAsset_List();
        fetchCategoryList();
        // fetchDepartmentList();
    }, []);

    useEffect(() => {
        if (searchAsset_Filters.categoryId) {
            fetchSubcategoryList(searchAsset_Filters.categoryId);
        } else {
            setSearchAsset_SubcategoryList([]);
        }
    }, [searchAsset_Filters.categoryId]);

    const fetchSearchAsset_List = async () => {
        try {
            // const params = new URLSearchParams(searchAsset_Filters);
            const response = await axios.get(`${UrlLink}AccetCategory/assetList_Get/`);
            console.log("setSearchAsset_List", setSearchAsset_List(response.data));

            // setSearchAsset_List(response.data);
            setSearchAsset_Data(response.data);
        } catch (error) {
            console.error('Error fetching assets:', error);
        }
    };

    const fetchCategoryList = async () => {
        try {
            const response = await axios.get(`${UrlLink}AccetCategory/asset_categories_list/`);
            console.log("fetchCategoryList", setSearchAsset_CategoryList(response.data));
        } catch (error) {
            console.error('Error fetching asset c*ategories:', error);
        }
    };

    const fetchSubcategoryList = async (categoryId) => {
        try {
            const response = await axios.get(`${UrlLink}AccetCategory/get_asset_subcategories/?category_id=${categoryId}`);
            setSearchAsset_SubcategoryList(response.data);
        } catch (error) {
            console.error('Error fetching subcategories:', error);
        }
    };

    // const fetchDepartmentList = async () => {
    //     try {
    //         const response = await axios.get('http://localhost:8000/api/departments/');
    //         setSearchAsset_DepartmentList(response.data);
    //     } catch (error) {
    //         console.error('Error fetching departments:', error);
    //     }
    // };

    const handleSearchChange = (e) => {
        const { name, value } = e.target;
        setSearchAsset_Filters(prevFilters => {
            const newFilters = { ...prevFilters, [name]: value };
            if (name === 'categoryId') {
                newFilters.subcategoryId = '';
            }
            return newFilters;
        });
    };

    useEffect(() => {
        fetchCategoryList();
    }, []);

    const handleSearch = async () => {
        const { assetName, categoryId, subcategoryId, valuationMethod, conditionStatus, assetStatus } = searchAsset_Filters;

        if (!assetName && !categoryId && !subcategoryId && !valuationMethod && !conditionStatus && !assetStatus) {
            alert("Please fill at least one field before searching.");
            return;
        }

        try {
            // Convert filters to URL parameters
            const params = new URLSearchParams();
            if (assetName) params.append('name', assetName);
            if (categoryId) params.append('category', categoryId);
            if (subcategoryId) params.append('subcategory', subcategoryId);
            if (valuationMethod) params.append('valuation_method', valuationMethod);
            if (conditionStatus) params.append('condition', conditionStatus);
            if (assetStatus) params.append('status', assetStatus);

            const response = await axios.get(`${UrlLink}AccetCategory/assetList_Get/?${params.toString()}`);
            setSearchAsset_Data(response.data);
            setSearchAsset_List(response.data);
        } catch (error) {
            console.error('Error fetching filtered assets:', error);
            alert('Error fetching data. Please try again.');
        }
    };


    const toggleStatusSearchAsset = async (asset) => {
        const updatedStatus = asset.status === 'active' ? 'inactive' : 'active';
        try {
            await axios.patch(`http://localhost:8000/api/assets/${asset.id}/`, { status: updatedStatus });

            const updatedAssets = searchAsset_List.map(item =>
                item.id === asset.id ? { ...item, status: updatedStatus } : item
            );
            setSearchAsset_List(updatedAssets);
            setSearchAsset_Data(updatedAssets);
        } catch (error) {
            console.error('Error toggling asset status:', error);
        }
    };

    const handleEditSearchAssetCategory = (asset) => {
        console.log('Editing asset category:', asset);
        setSearchAsset_SelectedForEditing(asset);
    };



    const assetSearchColumn = [
        { key: 'id', name: 'ID' },
        { key: 'name', name: 'Name' },
        {
            key: 'asset_code',
            name: 'Asset Code',
            renderCell: (params) => params.row.asset_code || '-'
        },

        {
            key: 'category',
            name: 'Category Name',
            renderCell: (params) => params.row.category?.name || '-'  // Extract 'name' from category object
        },

        {
            key: 'asset_subcategory',
            name: 'Subcategory Name',
            renderCell: (params) => params.row.subcategory?.length > 0 ? params.row.subcategory[0]?.name : '-'
        },

        {
            key: 'supplier_name',
            name: 'Supplier Name',
            renderCell: (params) => Array.isArray(params.row.supplier) ? params.row.supplier.join(', ') : '-'
        },

        { key: 'condition', name: 'Condition' },

        {
            key: 'status',
            name: 'Status',
            renderCell: (params) => (
                <Button className="cell_btn" onClick={() => toggleStatusSearchAsset(params.row)}>
                    {params.row.status === 'active' ? "ACTIVE" : "INACTIVE"}
                </Button>
            )
        },

        // {
        //     key: 'Actions',
        //     name: 'Actions',
        //     renderCell: (params) => (
        //         <Button className="cell_btn" onClick={() => handleEditSearchAssetCategory(params.row)}>
        //             <EditIcon className="check_box_clrr_cancell" />
        //         </Button>
        //     )
        // },
    ];

    // -------------------------------------------------------------------------------------------------
    // ------------------------AssetManagement-----------------------------

    const [AssetManagement_assets, setAssetManagement_Assets] = useState([]);
    const [AssetManagement_isEditing, setAssetManagement_IsEditing] = useState(false);
    const [editingAssetId_AssetManagement, setEditingAssetId_AssetManagement] = useState(null);
    const [assetManagementData, setAssetManagementData] = useState([]);



    const [AssetManagement_formData, setAssetManagement_FormData] = useState({
        id: '', name: '', category: '', asset_subcategory: '', supplier: '',
        department: '', current_location: '', room_no: '', condition: '',
        status: '', purchase_date: '', purchase_price: '', market_value: '',
        total_working_life: '', expected_working_life: '', valuation_method: '',
        is_new_asset: true, depreciation_method: '', depreciation_rate: '',
        salvage_value: '', appreciation_rate: ''
    });

    useEffect(() => {
        fetchAsset_AssetManagement();
    }, []);

    const fetchAsset_AssetManagement = async () => {
        try {
            const response = await axios.get(`${UrlLink}AccetCategory/Asset_Reg_Get/`);
            setAssets(response.data);
        } catch (error) {
            console.error('Error fetching assets:', error.response ? error.response.data : error.message);
        }
    };

    const handleEditAsset_AssetManagement = (asset) => {
        setAssetManagement_FormData({
            id: asset.id, name: asset.name, category: asset.category.toString(),
            asset_subcategory: asset.asset_subcategory.toString(), supplier: asset.supplier.toString(),
            department: asset.department.toString(), current_location: asset.current_location,
            room_no: asset.room_no, condition: asset.condition, status: asset.status,
            purchase_date: asset.purchase_date, purchase_price: asset.purchase_price.toString(),
            market_value: asset.market_value ? asset.market_value.toString() : '',
            total_working_life: asset.total_working_life.toString(),
            expected_working_life: asset.expected_working_life.toString(),
            valuation_method: asset.valuation_method, is_new_asset: asset.is_new_asset,
            depreciation_method: asset.depreciation_method || '',
            depreciation_rate: asset.depreciation_rate ? asset.depreciation_rate.toString() : '',
            salvage_value: asset.salvage_value ? asset.salvage_value.toString() : '',
            appreciation_rate: asset.appreciation_rate ? asset.appreciation_rate.toString() : ''
        });

        setEditingAssetId_AssetManagement(true);
        setEditingAssetId_AssetManagement(asset.id);
    };

    const toggleStatus_AssetManagement = (asset) => {
        const updatedAsset = { ...asset, status: asset.status === 'active' ? 'inactive' : 'active' };
        setAssets(assets.map(a => (a.id === asset.id ? updatedAsset : a)));
    };

    const handle_Print_Assetmanagemnet = () => {

    }
    const handle_AssetManagementData_Search = () => {

    }


    const assetManagementColumns = [
        { key: 'name', name: 'Name', frozen: true },
        { key: 'asset_code', name: 'Asset Code', frozen: true },
        {
            key: 'category',
            name: 'Category',
        },
        {
            key: 'asset_subcategory',
            name: 'Subcategory',
        },
        {
            key: 'supplier',
            name: 'Supplier',
        },
        {
            key: 'status', name: 'Status', renderCell: (params) => (
                <Button className="cell_btn" onClick={() => toggleStatus_AssetManagement(params.row)}>
                    {params.row.status === 'active' ? "ACTIVE" : "INACTIVE"}
                </Button>
            )
        },
        { key: 'purchase_date', name: 'Purchase Date' },
        { key: 'purchase_price', name: 'Purchase Price' },
        // {
        //     key: 'actions', name: 'Actions', renderCell: (params) => (
        //         <Button className="cell_btn" onClick={() => handleEditAsset_AssetManagement(params.row)}>
        //             <EditIcon className="check_box_clrr_cancell" />
        //         </Button>
        //     )
        // }
    ];
    // ----------------------------------------------------------------------------------------------------

    return (
        <div className="Main_container_app">
            <h3>Asset Management</h3>
            <br />
            <div className="RegisterTypecon">
                <div className="RegisterType">

                    {["AssetRegister", "AssetList", "Searchasset", "AssetManagementData"].map((p, ind) => (

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
            <br />
            {/* -------------------------------------AssetRegister----------------------------- */}
            {RackMasterPage === 'AssetRegister' && <>
                <br />

                <div className="RegisFormcon_1">
                    <div className="RegisForm_1">
                        <label>Asset Name <span>:</span></label>
                        <input
                            type="text"
                            name="name"
                            value={AssetformData.name}
                            onChange={handleInputChange}
                            placeholder="Asset Name"
                            required
                        />
                    </div>

                    <div className="RegisForm_1">
                        <label>Category <span>:</span></label>
                        <select
                            name="category"
                            value={AssetformData.category}
                            onChange={handleInputChange}
                            required
                        >
                            <option value="">Select Category</option>
                            {assetCategories.map((category) => (
                                <option key={category.id} value={category.id}>
                                    {category.name}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div className="RegisForm_1">
                        <label>Subcategory <span>:</span></label>
                        <select
                            name="asset_subcategory"
                            value={AssetformData.asset_subcategory}
                            onChange={handleInputChange}
                            required
                            disabled={!AssetformData.category}
                        >
                            <option value="">Select Subcategory</option>
                            {subcategories.map((subcategory) => (
                                <option key={subcategory.id} value={subcategory.id}>
                                    {subcategory.name}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div className="RegisForm_1">
                        <label>Supplier <span>:</span></label>
                        <select
                            name="supplier"
                            value={AssetformData.supplier}
                            onChange={handleInputChange}
                            required
                            disabled={!AssetformData.asset_subcategory}
                        >
                            <option value="">Select Supplier</option>
                            {suppliers.map((supplier) => (
                                <option key={supplier.id} value={supplier.id}>
                                    {supplier.name}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div className="RegisForm_1">
                        <label>Company / Brand <span>:</span></label>
                        <input
                            type="text"
                            name="Company_Brand"
                            value={AssetformData.Company_Brand}
                            onChange={handleInputChange}
                            placeholder="Company Brand Name"
                            required
                        />
                    </div>

                    {/* <div className="RegisForm_1">
                            <label>Department <span>:</span></label>
                            <select
                                name="department"
                                value={AssetformData.department}
                                onChange={handleInputChange}
                                required
                            >
                                <option value="">Select Department</option>
                                {departments.map((department) => (
                                    <option key={department.id} value={department.id}>
                                        {department.name}
                                    </option>
                                ))} 
                            </select>
                        </div> */}

                    <div className="RegisForm_1">
                        <label>
                            Asset is new:
                            <input
                                type="checkbox"
                                name="is_new_asset"
                                checked={AssetformData.is_new_asset}
                                onChange={handleInputChange}
                            />
                        </label>
                    </div>

                    <div className="RegisForm_1">
                        <label>Purchase Date <span>:</span></label>
                        <input
                            type="date"
                            name="purchase_date"
                            value={AssetformData.purchase_date}
                            onChange={handleInputChange}
                            required
                        />
                    </div>

                    <div className="RegisForm_1">
                        <label>Purchase Price <span>:</span></label>
                        <input
                            type="number"
                            name="purchase_price"
                            value={AssetformData.purchase_price}
                            onChange={handleInputChange}
                            placeholder="Purchase Price"
                            required
                        />
                    </div>

                    <div className="RegisForm_1">
                        <label>Total Working Life (years) <span>:</span></label>
                        <input
                            type="number"
                            name="total_working_life"
                            value={AssetformData.total_working_life}
                            onChange={handleInputChange}
                            placeholder="Total Working Life"
                            required
                        />
                    </div>

                    <div className="RegisForm_1">
                        <label>Current Location <span>:</span></label>
                        <input
                            type="text"
                            name="current_location"
                            value={AssetformData.current_location}
                            onChange={handleInputChange}
                            placeholder="Current Location"
                            required
                        />
                    </div>

                    <div className="RegisForm_1">
                        <label>Room Number <span>:</span></label>
                        <input
                            type="text"
                            name="room_no"
                            value={AssetformData.room_no}
                            onChange={handleInputChange}
                            placeholder="Room Number"
                        />
                    </div>

                    <div className="RegisForm_1">
                        <label>Condition <span>:</span></label>
                        <select
                            name="condition"
                            value={AssetformData.condition}
                            onChange={handleInputChange}
                            required
                        >
                            <option value="">Select Condition</option>
                            <option value="GOOD">Good</option>
                            <option value="FAIR">Fair</option>
                            <option value="BAD">Bad</option>
                        </select>
                    </div>

                    <div className="RegisForm_1">
                        <label>Status <span>:</span></label>
                        <select
                            name="status"
                            value={AssetformData.status}
                            onChange={handleInputChange}
                            required
                        >
                            <option value="">Select Status</option>
                            <option value="IN_USE">In Use</option>
                            <option value="MAINTENANCE">Under Maintenance</option>
                            <option value="SCRAPPED">Scrapped</option>
                        </select>
                    </div>

                    <div className="RegisForm_1">
                        <label>Market Value <span>:</span></label>
                        <input
                            type="number"
                            name="market_value"
                            value={AssetformData.market_value}
                            onChange={handleInputChange}
                            placeholder="Market Value"
                        />
                    </div>

                    <div className="RegisForm_1">
                        <label>Valuation Method <span>:</span></label>
                        <select
                            name="valuation_method"
                            value={AssetformData.valuation_method}
                            onChange={handleInputChange}
                            required
                        >
                            <option value="">Select Valuation Method</option>
                            <option value="DEPRECIATION">Depreciation</option>
                            <option value="APPRECIATION">Appreciation</option>
                            <option value="NONE">No Valuation</option>
                        </select>
                    </div>

                    <div className="RegisForm_1">
                        <label>Expected Working Life (Years) <span>:</span></label>
                        <input
                            type="number"
                            name="expected_working_life"
                            value={AssetformData.expected_working_life}
                            onChange={handleInputChange}
                            placeholder="Expected Working Life (Years)"
                            required
                        />
                    </div>

                    {AssetformData.valuation_method === 'DEPRECIATION' && (
                        <div>
                            <div className="RegisForm_1">
                                <label>Depreciation Method <span>:</span></label>
                                <select
                                    name="depreciation_method"
                                    value={AssetformData.depreciation_method}
                                    onChange={handleInputChange}
                                    required
                                >
                                    <option value="">Select Depreciation Method</option>
                                    <option value="STRAIGHT_LINE">Straight Line</option>
                                    <option value="DECLINING_BALANCE">Declining Balance</option>
                                </select>
                            </div>

                            <div className="RegisForm_1">
                                <label>Depreciation Rate <span>:</span></label>
                                <input
                                    type="number"
                                    name="depreciation_rate"
                                    value={AssetformData.depreciation_rate}
                                    onChange={handleInputChange}
                                    placeholder="Depreciation Rate"
                                    required
                                />
                            </div>

                            <div className="RegisForm_1">
                                <label>Salvage Value <span>:</span></label>
                                <input
                                    type="number"
                                    name="salvage_value"
                                    value={AssetformData.salvage_value}
                                    onChange={handleInputChange}
                                    placeholder="Salvage Value"
                                    required
                                />
                            </div>
                        </div>
                    )}

                    {AssetformData.valuation_method === 'APPRECIATION' && (
                        <div className="RegisForm_1">
                            <label>Appreciation Rate <span>:</span></label>
                            <input
                                type="number"
                                name="appreciation_rate"
                                value={AssetformData.appreciation_rate}
                                onChange={handleInputChange}
                                placeholder="Appreciation Rate"
                                required
                            />
                        </div>
                    )}


                </div>
                <div className="Main_container_Btn">
                    <button onClick={handleSubmit} style={{ width: "95px" }}>
                        {isEditing ? 'Update Asset' : 'Add Asset'}
                    </button>
                </div>

                <ReactGrid columns={assetRegColumn} RowData={assets} />

            </>}
            {/* ------------------------------ AssetList --------------------------- */}
            {RackMasterPage === 'AssetList' && <>
                <br />

                <div className="RegisFormcon_1">
                    <div className="RegisForm_1">
                        <label>
                            Search by Name <span>:</span>
                        </label>
                        <input
                            type="text"
                            name="name"
                            placeholder="Search by name..."
                            value={AssetListSearchTerm.name}
                            onChange={AssetListHandleSearch}
                        />
                    </div>

                    <div className="RegisForm_1">
                        <label>
                            Category <span>:</span>
                        </label>
                        <select name="category_id" value={AssetListFilters.category_id} onChange={AssetListHandleFilterChange}>
                            <option value="">Filter by Category</option>
                            {AssetListCategories.map((category) => (
                                <option key={category.id} value={category.id}>
                                    {category.name}
                                </option>
                            ))}
                        </select>
                    </div>

                    <div className="RegisForm_1">
                        <label>
                            Subcategory <span>:</span>
                        </label>
                        <select
                            name="subcategory_id"
                            value={AssetListFilters.subcategory_id}
                            onChange={AssetListHandleFilterChange}
                            disabled={!AssetListFilters.category}
                        >
                            <option value="">Filter by Subcategory</option>
                            {AssetListSubcategories.map((subcategory) => (
                                <option key={subcategory.id} value={subcategory.id}>
                                    {subcategory.name}
                                </option>
                            ))}
                        </select>
                    </div>

                    {/* <div className="RegisForm_1">
                            <label>
                                Department <span>:</span>
                            </label>
                            <select name="department" value={AssetListFilters.department} onChange={AssetListHandleFilterChange}>
                                <option value="">Filter by Department</option>
                                {AssetListDepartments.map((department) => (
                                    <option key={department.id} value={department.id}>
                                        {department.name}
                                    </option>
                                ))}
                            </select>
                        </div> */}

                    <div className="RegisForm_1">
                        <label>
                            Status <span>:</span>
                        </label>
                        <select name="status" value={AssetListFilters.status} onChange={AssetListHandleFilterChange}>
                            <option value="">Filter by Status</option>
                            <option value="IN_USE">In Use</option>
                            <option value="MAINTENANCE">Under Maintenance</option>
                            <option value="SCRAPPED">Scrapped</option>
                        </select>
                    </div>

                    <div className="RegisForm_1">
                        <label>
                            Condition <span>:</span>
                        </label>
                        <select name="condition" value={AssetListFilters.condition} onChange={AssetListHandleFilterChange}>
                            <option value="">Filter by Condition</option>
                            <option value="GOOD">Good</option>
                            <option value="FAIR">Fair</option>
                            <option value="BAD">Bad</option>
                        </select>
                    </div>

                    <div className="RegisForm_1">
                        <label>
                            Valuation Method <span>:</span>
                        </label>
                        <select name="valuation_method" value={AssetListFilters.valuation_method} onChange={AssetListHandleFilterChange}>
                            <option value="">Filter by Valuation Method</option>
                            <option value="DEPRECIATION">Depreciation</option>
                            <option value="APPRECIATION">Appreciation</option>
                            <option value="NONE">No Valuation</option>
                        </select>
                    </div>
                </div>

                <div className="Main_container_Btn">
                    <button onClick={AssetListHandlePrint} style={{ width: "95px" }}>
                        Print
                    </button>
                </div>
                <div className="Main_container_Btn">
                    <button onClick={AssetListHandle} style={{ width: "95px" }}>
                        Search
                    </button>
                </div>

                <ReactGrid
                    columns={AssetListColumns}
                    RowData={Array.isArray(AssetListData) ? AssetListData : []}
                />

            </>}
            {/* -------------------------Serach Asset-------------------------- */}
            {RackMasterPage === 'Searchasset' && <>
                <br />
                <div className="Main_container_app">

                    <div className="RegisFormcon_1">
                        <div className="RegisForm_1">
                            <label>
                                Category <span>:</span>
                            </label>
                            <select
                                name="categoryId"
                                value={searchAsset_Filters.categoryId}
                                onChange={handleSearchChange}
                            >
                                <option value="">All Categories</option>
                                {searchAsset_CategoryList.map(category => (
                                    <option key={category.id} value={category.id.toString()}>
                                        {category.name}
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div className="RegisForm_1">
                            <label>
                                Subcategory <span>:</span>
                            </label>
                            <select
                                name="subcategoryId"
                                value={searchAsset_Filters.subcategoryId}
                                onChange={handleSearchChange}
                                disabled={!searchAsset_Filters.categoryId}
                            >
                                <option value="">All Subcategories</option>
                                {searchAsset_SubcategoryList.map(subcategory => (
                                    <option key={subcategory.id} value={subcategory.id.toString()}>
                                        {subcategory.name}
                                    </option>
                                ))}
                            </select>
                        </div>

                        {/* <div className="RegisForm_1">
                            <label>
                                Department <span>:</span>
                            </label>
                            <select
                                name="departmentId"
                                value={searchAsset_Filters.departmentId}
                                onChange={handleSearchChange}
                            >
                                <option value="">All Departments</option>
                                {fetchSearchAsset_DepartmentList.map(department => (
                                    <option key={department.id} value={department.id.toString()}>
                                        {department.name}
                                    </option>
                                ))}
                            </select>
                        </div> */}
                    </div>

                    <div className="RegisFormcon_1">
                        <div className="RegisForm_1">
                            <label>
                                Asset Name <span>:</span>
                            </label>
                            <input
                                type="text"
                                name="assetName"
                                value={searchAsset_Filters.assetName}
                                onChange={handleSearchChange}
                                placeholder="Search by Name"
                            />
                        </div>

                        <div className="RegisForm_1">
                            <label>
                                Valuation Method <span>:</span>
                            </label>
                            <select
                                name="valuationMethod"
                                value={searchAsset_Filters.valuationMethod}
                                onChange={handleSearchChange}
                            >
                                <option value="">All Valuation Methods</option>
                                <option value="DEPRECIATION">Depreciation</option>
                                <option value="APPRECIATION">Appreciation</option>
                                <option value="NONE">No Valuation</option>
                            </select>
                        </div>

                        <div className="RegisForm_1">
                            <label>
                                Condition <span>:</span>
                            </label>
                            <select
                                name="conditionStatus"
                                value={searchAsset_Filters.conditionStatus}
                                onChange={handleSearchChange}
                            >
                                <option value="">All Conditions</option>
                                <option value="GOOD">Good</option>
                                <option value="FAIR">Fair</option>
                                <option value="BAD">Bad</option>
                            </select>
                        </div>

                        <div className="RegisForm_1">
                            <label>
                                Status <span>:</span>
                            </label>
                            <select
                                name="assetStatus"
                                value={searchAsset_Filters.assetStatus}
                                onChange={handleSearchChange}
                            >
                                <option value="">All Status</option>
                                <option value="IN_USE">In Use</option>
                                <option value="MAINTENANCE">Under Maintenance</option>
                                <option value="SCRAPPED">Scrapped</option>
                            </select>
                        </div>
                    </div>

                    <div className="Main_container_Btn">
                        <button onClick={handleSearch} style={{ width: "95px" }}>
                            Search
                        </button>
                    </div>

                    <ReactGrid columns={assetSearchColumn} RowData={searchAsset_Data} />
                </div>

            </>}
            {/* ------------------------------AssetManagementData--------------------------- */}
            {RackMasterPage === 'AssetManagementData' && <>
                <br />
                <div className="Main_container_app">
                    <div className="Main_container_Btn">
                        <button onClick={handle_Print_Assetmanagemnet} style={{ width: "95px" }}>
                            Print
                        </button>
                    </div>
                    <div className="Main_container_Btn">
                        <button onClick={handle_AssetManagementData_Search} style={{ width: "95px" }}>
                            Search
                        </button>
                    </div>

                    <ReactGrid columns={assetManagementColumns} RowData={assetManagementData} />
                </div>
            </>}

        </div>
    );
};

export default AssetManagement;
